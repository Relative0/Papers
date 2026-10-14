from common import *
import ctypes as ct,struct
LIB=None
def lib():
    global LIB
    if LIB is None:
        LIB=ct.CDLL(str(ROOT/'native_count.so'))
        LIB.nc_load.argtypes=[ct.c_void_p,ct.c_size_t];LIB.nc_load.restype=ct.c_void_p
        LIB.nc_packed.argtypes=[ct.c_uint,ct.c_uint,ct.c_void_p,ct.c_void_p,ct.c_void_p];LIB.nc_packed.restype=ct.c_void_p
        LIB.nc_count.argtypes=[ct.c_void_p];LIB.nc_count.restype=ct.c_uint64
        LIB.nc_raw.argtypes=[ct.c_void_p,ct.c_size_t,ct.c_void_p,ct.c_size_t];LIB.nc_raw.restype=ct.c_uint64
        LIB.nc_update.argtypes=[ct.c_void_p,ct.c_uint,ct.c_int];LIB.nc_update.restype=ct.c_int
        LIB.nc_dump.argtypes=[ct.c_void_p,ct.c_void_p];LIB.nc_dump.restype=ct.c_size_t
        LIB.nc_free.argtypes=[ct.c_void_p]
    return LIB
class Native:
    def __init__(self,p):
        if not p:raise ValueError('native state rejected')
        self.p=p
    def __del__(self):
        if getattr(self,'p',None):lib().nc_free(self.p);self.p=None
    def count(self):return lib().nc_count(self.p)
    def update(self,z,b):
        if lib().nc_update(self.p,z,b):raise ValueError('invalid native update')
    def dumps(self):
        size=lib().nc_dump(self.p,None);b=ct.create_string_buffer(size);lib().nc_dump(self.p,b);return b.raw
    @classmethod
    def loads(cls,b):return cls(lib().nc_load(b,len(b)))
    @classmethod
    def packed(cls,c):
        if c['r']>64:raise ValueError('native factor width >64')
        names=(ct.c_uint32*c['n'])(*(c['left']+c['right']));u=(ct.c_uint64*len(c['U']))(*c['U']);w=(ct.c_uint64*len(c['W']))(*c['W'])
        return cls(lib().nc_packed(c['p'],c['q'],names,u,w))

def cudd_blob(c):
    from dd.cudd import BDD
    bdd=BDD();order=c['left']+c['right']
    if order:bdd.declare(*(f'x{v}' for v in order))
    bdd.configure(reordering=False)
    def bitfunc(values,scope,bit):
        def rec(start,length,depth):
            if length==1:return bdd.true if (values[start]>>bit)&1 else bdd.false
            half=length//2;lo=rec(start,half,depth+1);hi=rec(start+half,half,depth+1)
            return bdd.ite(bdd.var(f'x{scope[depth]}'),hi,lo)
        out=rec(0,len(values),0);rec=None;return out
    root=bdd.false
    for j in range(c['r']):root=bdd.apply('xor',root,bitfunc(c['U'],c['left'],j)&bitfunc(c['W'],c['right'],j))
    bdd.reorder();bdd.configure(reordering=False)
    order=[int(bdd.var_at_level(i)[1:]) for i in range(c['n'])]
    nodes=[];seen={bdd.true:1}
    def visit(node):
        if node.negated:return -visit(~node)
        if node in seen:return seen[node]
        lo,hi=visit(node.low),visit(node.high);idx=len(nodes)+2;seen[node]=idx;nodes.append((node.level,lo,hi));return idx
    rid=visit(root);visit=None
    blob=b'CBD1'+struct.pack('<I',c['n'])+struct.pack('<'+'I'*len(order),*order)+struct.pack('<Iq',len(nodes),rid)+b'\xff'*c['n']+b''.join(struct.pack('<Iqq',*x) for x in nodes)
    seen.clear();del root;del bdd
    return blob

class Raw:
    def __init__(self,c):self.c={k:c[k] for k in ('n','p','q','r','left','right','U','W')};self.rho={}
    def update(self,z,b):
        if z in self.rho or z not in self.c['left']+self.c['right'] or b not in (0,1):raise ValueError('update')
        self.rho[z]=b
    def count(self):
        # Direct pair enumeration, deliberately no transform or profile grouping.
        U=[self.c['U'][x] for x in selected(self.c['left'],self.rho)];W=[self.c['W'][y] for y in selected(self.c['right'],self.rho)]
        if self.c['r']>64:return sum((x&y).bit_count()%2 for x in U for y in W)
        u=(ct.c_uint64*len(U))(*U);w=(ct.c_uint64*len(W))(*W)
        return lib().nc_raw(u,len(U),w,len(W))
    def dumps(self):
        c=self.c;r=c['r'];acc=0;nb=0;data=bytearray()
        for v in c['U']+c['W']:
            acc|=v<<nb;nb+=r
            while nb>=8:data.append(acc&255);acc>>=8;nb-=8
        if nb:data.append(acc)
        meta=json.dumps({k:v for k,v in c.items() if k not in ('U','W')},separators=(',',':')).encode()
        return b'RAW1'+struct.pack('<I',len(meta))+meta+data
    @classmethod
    def loads(cls,blob):
        if blob[:4]!=b'RAW1':raise ValueError('raw header')
        m=struct.unpack_from('<I',blob,4)[0];c=json.loads(blob[8:8+m]);r=c['r'];data=blob[8+m:];total=(1<<c['p'])+(1<<c['q'])
        if len(data)!=(total*r+7)//8:raise ValueError('raw length')
        vals=[]
        for i in range(total):vals.append((int.from_bytes(data[i*r//8:(i*r+r+7)//8],'little')>>(i*r%8))&((1<<r)-1))
        c['U']=vals[:1<<c['p']];c['W']=vals[1<<c['p']:];return cls(c)

class Histogram(Raw):
    def count(self):
        # Historical Draft-3 profile/Walsh identity, supplied width retained.
        c=self.c;u=Counter(c['U'][i] for i in selected(c['left'],self.rho));w=Counter(c['W'][i] for i in selected(c['right'],self.rho))
        if c['r']>12:return sum(a*b for x,a in u.items() for y,b in w.items() if (x&y).bit_count()%2)
        a=[w.get(i,0) for i in range(1<<c['r'])];step=1
        while step<len(a):
            for j in range(0,len(a),2*step):
                for i in range(j,j+step):x,y=a[i],a[i+step];a[i],a[i+step]=x+y,x-y
            step*=2
        signed=sum(v*a[x] for x,v in u.items());return (sum(u.values())*sum(w.values())-signed)//2
