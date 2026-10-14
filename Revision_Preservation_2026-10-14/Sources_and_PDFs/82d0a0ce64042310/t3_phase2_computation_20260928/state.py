"""Independent implementation of the frozen T3 state. No source retained after construction.

Assignment indices are MSB-first within each named side. Moment subset masks use named IDs.
Allocated inactive cells remain until serialization; only active counters are serialized.
"""
from common import *
import struct

def moments(values,scope,h):
    values=list(values)
    # Superset zeta transform: one exact sum for each subset coordinate.
    for bit in range(len(scope)):
        for x in range(1<<len(scope)):
            if not x&(1<<bit):values[x]+=values[x|(1<<bit)]
    return {t:values[sum(1<<(len(scope)-1-j) for j,v in enumerate(scope) if t&(1<<v))]
            for t in subsets(scope,h)}

class State:
    __slots__=('p','q','r','k','h','orientation','dense','left','right','free_a','free_b','labels','A','B','last_operations')
    def __init__(self,c,k,orientation='row',dense=False):
        if not 0<=k<=c['n']:raise ValueError('budget')
        self.p,self.q,self.r,self.k,self.h=c['p'],c['q'],c['r'],k,k
        self.orientation=orientation;self.dense=dense;self.left=tuple(c['left']);self.right=tuple(c['right'])
        u,w=(c['U'],c['W']) if orientation=='row' else (c['W'],c['U'])
        self.free_a,self.free_b=(self.left,self.right) if orientation=='row' else (self.right,self.left)
        self.labels=tuple(range(1,1<<self.r)) if dense else tuple(sorted(set(u)-{0}))
        self.A={t:[] for t in subsets(self.free_a,k)};self.B={t:[] for t in subsets(self.free_b,k)}
        for a in self.labels:
            for t,v in moments((int(x==a) for x in u),self.free_a,k).items():self.A[t].append(v)
            for t,v in moments((1-2*((a&x).bit_count()%2) for x in w),self.free_b,k).items():self.B[t].append(v)
        self.last_operations=0
    @property
    def s(self):return len(self.labels)
    def count(self):
        da,db=len(self.free_a),len(self.free_b)
        sigma=((1<<da)-sum(self.A[0]))*(1<<db)+sum(a*b for a,b in zip(self.A[0],self.B[0]))
        num=(1<<(da+db))-sigma
        if num<0 or num%2:raise ArithmeticError('invalid moment state')
        return num//2
    def update(self,z,b):
        if type(b) is not int or b not in (0,1) or self.h<=0 or z not in self.free_a+self.free_b:raise ValueError('illegal cumulative update')
        side='free_a' if z in self.free_a else 'free_b';coords=getattr(self,side);free=tuple(v for v in coords if v!=z)
        table=self.A if side=='free_a' else self.B;ops=0
        for t in subsets(free,self.h-1):
            upper=table[t|(1<<z)]
            table[t]=list(upper) if b else [a-v for a,v in zip(table[t],upper)]
            ops+=self.s
        setattr(self,side,free);self.h-=1;self.last_operations=ops
    def payload_bits(self):
        a,b=(self.p,self.q) if self.orientation=='row' else (self.q,self.p)
        return self.s*((0 if self.dense else self.r)+(a+1)*D(len(self.free_a),self.h)+(b+2)*D(len(self.free_b),self.h))
    def dumps(self):
        # Fixed-width two's-complement counters; subset indices implicit in scope and horizon.
        a,b=(self.p,self.q) if self.orientation=='row' else (self.q,self.p)
        head=struct.pack('<4s10I',b'T3M1',self.p,self.q,self.r,self.k,self.h,int(self.orientation=='column'),int(self.dense),self.s,len(self.free_a),len(self.free_b))
        names=self.left+self.right+self.free_a+self.free_b
        head+=struct.pack('<'+'H'*len(names),*names)
        data=bytearray();acc=0;nb=0
        def put(v,width,signed=False):
            nonlocal acc,nb
            lo=-(1<<(width-1)) if signed else 0;hi=(1<<(width-1)) if signed else (1<<width)
            if not lo<=v<hi:raise OverflowError('counter width')
            acc|=(v&((1<<width)-1))<<nb;nb+=width
            while nb>=8:data.append(acc&255);acc>>=8;nb-=8
        if not self.dense:
            for label in self.labels:put(label,self.r)
        for table,coords,width,signed in ((self.A,self.free_a,a+1,False),(self.B,self.free_b,b+2,True)):
            for t in subsets(coords,self.h):
                for v in table[t]:put(v,width,signed)
        if nb:data.append(acc)
        assert len(data)==(self.payload_bits()+7)//8
        return head+data
    @classmethod
    def loads(cls,blob):
        if len(blob)<44:raise ValueError('short state')
        magic,p,q,r,k,h,col,dense,s,na,nb=struct.unpack_from('<4s10I',blob)
        if magic!=b'T3M1' or p+q>62 or not 0<=h<=k<=p+q or col>1 or dense>1 or na+nb!=p+q-(k-h):raise ValueError('header')
        o=object.__new__(cls);o.p,o.q,o.r,o.k,o.h=p,q,r,k,h;o.orientation='column' if col else 'row';o.dense=bool(dense)
        count=p+q+na+nb;offset=44+count*2
        if len(blob)<offset:raise ValueError('scope length')
        names=struct.unpack_from('<'+'H'*count,blob,44);o.left=names[:p];o.right=names[p:p+q];o.free_a=names[p+q:p+q+na];o.free_b=names[p+q+na:]
        if len(set(o.left+o.right))!=p+q:raise ValueError('duplicate source name')
        aa,bb=(o.right,o.left) if col else (o.left,o.right)
        if len(set(o.free_a))!=na or len(set(o.free_b))!=nb or not set(o.free_a)<=set(aa) or not set(o.free_b)<=set(bb):raise ValueError('free scope')
        if dense and s!=(1<<r)-1:raise ValueError('dense support')
        a,b=(q,p) if col else (p,q);bits=s*((0 if dense else r)+(a+1)*D(na,h)+(b+2)*D(nb,h))
        if len(blob)!=offset+(bits+7)//8:raise ValueError('state length')
        data=blob[offset:];pos=0
        def get(width,signed=False):
            nonlocal pos
            start=pos//8;shift=pos%8;v=(int.from_bytes(data[start:(pos+width+7)//8],'little')>>shift)&((1<<width)-1);pos+=width
            return v-(1<<width) if signed and v&(1<<(width-1)) else v
        o.labels=tuple(range(1,1<<r)) if dense else tuple(get(r) for _ in range(s))
        if tuple(sorted(set(o.labels)))!=o.labels or any(v==0 for v in o.labels):raise ValueError('profile labels')
        o.A={t:[get(a+1) for _ in range(s)] for t in subsets(o.free_a,h)}
        o.B={t:[get(b+2,True) for _ in range(s)] for t in subsets(o.free_b,h)}
        if bits%8 and data[-1]>>(bits%8):raise ValueError('nonzero padding')
        o.last_operations=0;return o
