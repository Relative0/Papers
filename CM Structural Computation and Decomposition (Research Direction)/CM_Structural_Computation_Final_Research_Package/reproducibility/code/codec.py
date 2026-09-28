"""Compact deterministic SC bitstream, v1; not an optimal compression scheme.

Two magic bytes SC; then little-endian packed fields: version(3), kind(3),
n(5), scope variable IDs(4 each). Flat: truth(2**n). XOR: c(1), count(5),
then factors [scope-mask(n), truth(2**popcount(mask))]. Product: same without c.
Rank/cofactor: left mask(n), inner dimension/prototype count(17), tables,
then coefficients/references. Prototype index width is ceil(log2(k)).
Final byte padding is zero. Scopes within factors are canonicalized to the
outer scope order. This is a measured serialization, not a source certificate.
"""
from artifacts import Artifact

KINDS=('flat','xor','product','rank','cofactor')

class Writer:
    def __init__(self): self.value,self.width=0,0
    def put(self,v,w):
        if type(v) is not int or v<0 or v.bit_length()>w: raise ValueError('field overflow')
        self.value |= v << self.width
        self.width += w
    def finish(self): return b'SC'+self.value.to_bytes((self.width+7)//8,'little')

class Reader:
    def __init__(self,blob):
        if len(blob)>4_000_000 or not blob.startswith(b'SC'): raise ValueError('header/size')
        self.value=int.from_bytes(blob[2:],'little'); self.width=(len(blob)-2)*8; self.pos=0
    def get(self,w):
        if w<0 or self.pos+w>self.width: raise ValueError('truncated')
        out=(self.value >> self.pos)&((1 << w)-1)
        self.pos += w
        return out
    def finish(self):
        if self.width-self.pos>7 or self.value >> self.pos: raise ValueError('noncanonical trailing data')

def _indices(old,new):
    out=[]
    for a in range(1 << len(new)):
        env={v:(a >> (len(new)-j-1))&1 for j,v in enumerate(new)}
        out.append(sum(env[v] << (len(old)-j-1) for j,v in enumerate(old)))
    return out

def canonicalize(a):
    if a.kind=='flat': return a
    def reordered(scope,bits):
        new=tuple(v for v in a.scope if v in scope)
        indices=_indices(scope,new)
        return new,sum(((bits>>i)&1)<<j for j,i in enumerate(indices))
    p=a.payload
    if a.kind in ('xor','product'):
        factors=p[1] if a.kind=='xor' else p[0]
        new=tuple(reordered(scope,bits) for scope,bits in factors)
        return Artifact(a.kind,a.scope,(p[0],new) if a.kind=='xor' else (new,))
    left,right,one,two=p
    nl=tuple(v for v in a.scope if v in left); nr=tuple(v for v in a.scope if v in right)
    ri,ci=_indices(left,nl),_indices(right,nr)
    if a.kind=='rank':
        return Artifact('rank',a.scope,(nl,nr,tuple(one[i] for i in ri),
            tuple(sum(((b>>i)&1)<<j for j,i in enumerate(ci)) for b in two)))
    return Artifact('cofactor',a.scope,(nl,nr,
        tuple(sum(((b>>i)&1)<<j for j,i in enumerate(ci)) for b in one),tuple(two[i] for i in ri)))

def dumps_binary(artifact):
    from checker import validate_structure
    validate_structure(artifact)
    a=canonicalize(artifact)
    n=len(a.scope)
    if n>16 or any(v>15 for v in a.scope): raise ValueError('codec scope IDs must fit 4 bits')
    w=Writer(); w.put(1,3); w.put(KINDS.index(a.kind),3); w.put(n,5)
    for v in a.scope: w.put(v,4)
    p=a.payload
    def mask(scope): return sum(int(v in scope)<<j for j,v in enumerate(a.scope))
    if a.kind=='flat': w.put(p[0],1<<n)
    elif a.kind in ('xor','product'):
        factors=p[1] if a.kind=='xor' else p[0]
        if a.kind=='xor': w.put(p[0],1)
        w.put(len(factors),5)
        for scope,bits in factors:
            w.put(mask(scope),n); w.put(bits,1<<len(scope))
    else:
        left,right,one,two=p
        R,C=1<<len(left),1<<len(right)
        w.put(mask(left),n)
        if a.kind=='rank':
            r=len(two); w.put(r,17)
            for coef in one: w.put(coef,r)
            for row in two: w.put(row,C)
        else:
            k=len(one); w.put(k,17)
            for row in one: w.put(row,C)
            width=(k-1).bit_length()
            for j,flip in two: w.put(j,width); w.put(flip,1)
    return w.finish()

def loads_binary(blob):
    r=Reader(blob)
    if r.get(3)!=1: raise ValueError('version')
    tag,n=r.get(3),r.get(5)
    if tag>=len(KINDS) or n>16: raise ValueError('kind/dimension')
    kind=KINDS[tag]; scope=tuple(r.get(4) for _ in range(n))
    def subscope(mask): return tuple(v for j,v in enumerate(scope) if (mask>>j)&1)
    if kind=='flat': payload=(r.get(1<<n),)
    elif kind in ('xor','product'):
        c=r.get(1) if kind=='xor' else None
        count=r.get(5); factors=[]
        for _ in range(count):
            sub=subscope(r.get(n)); factors.append((sub,r.get(1<<len(sub))))
        payload=(c,tuple(factors)) if kind=='xor' else (tuple(factors),)
    else:
        left=subscope(r.get(n)); right=tuple(v for v in scope if v not in left)
        R,C=1<<len(left),1<<len(right); count=r.get(17)
        if kind=='rank':
            if count*(R+C)>r.width-r.pos: raise ValueError('truncated rank payload')
            payload=(left,right,tuple(r.get(count) for _ in range(R)),tuple(r.get(C) for _ in range(count)))
        else:
            if count<1: raise ValueError('empty dictionary')
            width=(count-1).bit_length()
            if count*C+R*(width+1)>r.width-r.pos: raise ValueError('truncated cofactor payload')
            one=tuple(r.get(C) for _ in range(count)); two=tuple((r.get(width),r.get(1)) for _ in range(R))
            payload=(left,right,one,two)
    r.finish()
    a=Artifact(kind,scope,payload)
    from checker import validate_structure
    validate_structure(a)
    return a
