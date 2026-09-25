"""Exact C8 phase-count arithmetic; no floating point and no complex scalars.
A four-integer tuple is a polynomial in z with z**4=-1.
A State denotes its polynomial coefficients divided by 2**scale.
Qubit 0 is the leftmost bit; storage order is |00...0>,...,|11...1>.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable

Z8 = tuple[int,int,int,int]
ZERO: Z8=(0,0,0,0)
ONE: Z8=(1,0,0,0)
DELTA: Z8=(0,1,0,-1)  # z-z**3 = sqrt(2)

def add(a:Z8,b:Z8)->Z8: return tuple(x+y for x,y in zip(a,b))
def neg(a:Z8)->Z8: return tuple(-x for x in a)
def sub(a:Z8,b:Z8)->Z8: return add(a,neg(b))
def mul(a:Z8,b:Z8)->Z8:
    c=[0]*4
    for i in range(4):
        for j in range(4):
            c[(i+j)%4] += a[i]*b[j]*(1 if i+j<4 else -1)
    return tuple(c)
def phase(a:Z8,k:int)->Z8:
    b=a
    for _ in range(k%8): b=(-b[3],b[0],b[1],b[2])
    return b

def conjugate(a:Z8)->Z8: return (a[0],-a[3],-a[2],-a[1])
def norm_pair(a:Z8)->tuple[int,int]:
    x,y,z,t=a
    return (x*x+y*y+z*z+t*t, x*y+y*z+z*t-x*t)

@dataclass(frozen=True)
class State:
    coeff: tuple[Z8,...]
    scale: int=0
    def __post_init__(self):
        size=len(self.coeff)
        if size<2 or size&(size-1): raise ValueError('State length must be 2**n, n>=1')
        if self.scale<0: raise ValueError('Negative scale not supported')
    @property
    def n(self)->int: return len(self.coeff).bit_length()-1
    def canonical(self)->'State':
        c=self.coeff; s=self.scale
        while s and all(all(v%2==0 for v in a) for a in c):
            c=tuple(tuple(v//2 for v in a) for a in c); s-=1
        return State(c,s)
    def probabilities(self)->tuple[tuple[Fraction,Fraction],...]:
        den=1<<(2*self.scale)
        return tuple(tuple(Fraction(v,den) for v in norm_pair(a)) for a in self.coeff)
    def norm(self)->tuple[Fraction,Fraction]:
        ps=self.probabilities()
        return (sum((p[0] for p in ps),Fraction()),sum((p[1] for p in ps),Fraction()))
    def h(self,q:int)->'State':
        bit=self._bit(q); c=list(self.coeff)
        for i in range(len(c)):
            if i&bit: continue
            j=i|bit; a,b=self.coeff[i],self.coeff[j]
            c[i]=mul(add(a,b),DELTA); c[j]=mul(sub(a,b),DELTA)
        return State(tuple(c),self.scale+1).canonical()
    def p(self,q:int,k:int)->'State':
        bit=self._bit(q)
        return State(tuple(phase(a,k) if i&bit else a for i,a in enumerate(self.coeff)),self.scale).canonical()
    def permute(self,f:Callable[[int],int])->'State':
        dest=[f(i) for i in range(len(self.coeff))]
        if sorted(dest)!=list(range(len(dest))): raise ValueError('Not a basis permutation')
        out=[ZERO]*len(dest)
        for i,j in enumerate(dest): out[j]=self.coeff[i]
        return State(tuple(out),self.scale)
    def x(self,q:int)->'State':
        bit=self._bit(q); return self.permute(lambda i:i^bit)
    def cx(self,c:int,t:int)->'State':
        if c==t: raise ValueError('Control and target must differ')
        bc,bt=self._bit(c),self._bit(t)
        return self.permute(lambda i:i^bt if i&bc else i)
    def ccx(self,c1:int,c2:int,t:int)->'State':
        if len({c1,c2,t})!=3: raise ValueError('Distinct qubits required')
        b1,b2,bt=self._bit(c1),self._bit(c2),self._bit(t)
        return self.permute(lambda i:i^bt if i&b1 and i&b2 else i)
    def oracle_phase(self,f:Callable[[int],bool],k:int=4)->'State':
        return State(tuple(phase(a,k) if f(i) else a for i,a in enumerate(self.coeff)),self.scale).canonical()
    def _bit(self,q:int)->int:
        if not 0<=q<self.n: raise ValueError('Qubit outside register')
        return 1<<(self.n-1-q)
    def apply(self,gate:tuple)->'State':
        typ,*args=gate
        if typ=='H': return self.h(*args)
        if typ=='P': return self.p(*args)
        if typ=='CX': return self.cx(*args)
        if typ=='X': return self.x(*args)
        if typ=='CCX': return self.ccx(*args)
        raise ValueError(f'Unknown gate {typ}')

def basis(n:int,index:int=0)->State:
    if not 0<=index<(1<<n): raise ValueError('Invalid basis index')
    return State(tuple(ONE if i==index else ZERO for i in range(1<<n)))

def run(st:State,gates:Iterable[tuple])->State:
    for g in gates: st=st.apply(g)
    return st

def from_phase_counts(counts:list[list[int]],h:int)->State:
    """Eight nonnegative phase bins per output, denominator sqrt(2)**h."""
    c=tuple(tuple(row[k]-row[k+4] for k in range(4)) for row in counts)
    if h%2: c=tuple(mul(a,DELTA) for a in c)
    return State(c,(h+1)//2).canonical()

def path_sum(n:int,gates:list[tuple],initial:int=0)->State:
    """Independent exhaustive Feynman paths: Boolean paths plus integer phase counts."""
    paths=[(initial,0)]; h=0
    for gate in gates:
        typ,*a=gate; new=[]
        if typ=='H':
            bit=1<<(n-1-a[0]); h+=1
            for i,p in paths:
                x=bool(i&bit)
                new.extend([(i&~bit,p),(i|bit,(p+4*int(x))%8)])
        elif typ=='P':
            bit=1<<(n-1-a[0]); k=a[1]
            new=[(i,(p+k*bool(i&bit))%8) for i,p in paths]
        elif typ=='CX':
            bc,bt=[1<<(n-1-q) for q in a]
            new=[(i^bt if i&bc else i,p) for i,p in paths]
        elif typ=='X':
            bit=1<<(n-1-a[0]); new=[(i^bit,p) for i,p in paths]
        elif typ=='CCX':
            b1,b2,bt=[1<<(n-1-q) for q in a]
            new=[(i^bt if i&b1 and i&b2 else i,p) for i,p in paths]
        else: raise ValueError(typ)
        paths=new
    counts=[[0]*8 for _ in range(1<<n)]
    for i,p in paths: counts[i][p]+=1
    return from_phase_counts(counts,h)
