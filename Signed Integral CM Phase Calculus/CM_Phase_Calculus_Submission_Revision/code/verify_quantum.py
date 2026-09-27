#!/usr/bin/env python3
"""Exact algorithm, phase, quotient, tensor and Clifford checks.
Only the explicitly labelled numerical cross-check uses floating point.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction
import itertools, json, random, time
from pathlib import Path
import numpy as np
from phase_calculus import *
OUT=Path(__file__).resolve().parents[1]/'data'

def val(a): return sum(v*np.exp(1j*np.pi*k/4) for k,v in enumerate(a))
def numeric(st): return np.array([val(a)/2**st.scale for a in st.coeff])
def nr_gate(vec,n,g):
    typ,*a=g; out=vec.copy()
    if typ=='H':
        bit=1<<(n-1-a[0])
        for i in range(len(out)):
            if not i&bit:
                j=i|bit; out[i]=(vec[i]+vec[j])/np.sqrt(2); out[j]=(vec[i]-vec[j])/np.sqrt(2)
    elif typ=='P':
        bit=1<<(n-1-a[0]); k=a[1]
        for i in range(len(out)):
            if i&bit: out[i]*=np.exp(1j*np.pi*k/4)
    else:
        bits=[1<<(n-1-q) for q in a]
        for i in range(len(out)):
            if typ=='CX': j=i^bits[1] if i&bits[0] else i
            elif typ=='X': j=i^bits[0]
            elif typ=='CCX': j=i^bits[2] if i&bits[0] and i&bits[1] else i
            else: raise ValueError(typ)
            out[j]=vec[i]
    return out

def clifford_group(n):
    # i^p X^x Z^z, bit q uses mask 1<<q. Exact signed Pauli action.
    ident=tuple((0,1<<q,0) if t==0 else (0,0,1<<q) for q in range(n) for t in range(2))
    generators=[('H',q) for q in range(n)]+[('S',q) for q in range(n)]
    generators += [('CX',c,t) for c in range(n) for t in range(n) if c!=t]
    def step(pa,g):
        p,x,z=pa; typ=g[0]
        if typ=='H':
            b=1<<g[1]; u=int(bool(x&b)); v=int(bool(z&b)); p=(p+2*u*v)%4
            if u!=v: x^=b; z^=b
        elif typ=='S':
            b=1<<g[1]
            if x&b: p=(p+1)%4; z^=b
        else:
            bc,bt=1<<g[1],1<<g[2]
            if x&bc: x^=bt
            if z&bt: z^=bc
        return (p,x,z)
    seen={ident}; todo=deque([ident])
    while todo:
        s=todo.popleft()
        for g in generators:
            t=tuple(step(p,g) for p in s)
            if t not in seen: seen.add(t); todo.append(t)
    return len(seen)

def expectation(st):
    out=[Fraction(),Fraction()]
    for i,p in enumerate(st.probabilities()):
        sign=(-1)**i.bit_count()
        out=[x+sign*y for x,y in zip(out,p)]
    return out

def main():
    start=time.monotonic(); results={}; checks=0
    grid=list(itertools.product((-1,0,1),repeat=4))
    for a in grid:
        u,v=norm_pair(a)
        assert mul(a,conjugate(a))==(u,v,0,-v)
        assert norm_pair(phase(a,1))==(u,v)
        for b in grid:
            n1=norm_pair(add(a,b)); n2=norm_pair(sub(a,b)); nb=norm_pair(b)
            assert (n1[0]+n2[0],n1[1]+n2[1])==(2*(u+nb[0]),2*(v+nb[1]))
            checks+=1
    results['exact_parallelogram_tests']=checks
    results['projective_Clifford_sizes']={str(n):clifford_group(n) for n in (1,2)}
    rng=random.Random(20260917); maxerr=0.0; steps=0
    for trial in range(240):
        n=1+trial%4; st=basis(n,trial%(1<<n)); nv=numeric(st)
        gates=[]
        for depth in range(24):
            choices=['H','P','X']+(['CX'] if n>1 else [])+(['CCX'] if n>2 else [])
            typ=rng.choice(choices)
            if typ=='H' or typ=='X': g=(typ,rng.randrange(n))
            elif typ=='P': g=(typ,rng.randrange(n),rng.randrange(8))
            else: g=(typ,*rng.sample(range(n),2 if typ=='CX' else 3))
            gates.append(g); st=st.apply(g); nv=nr_gate(nv,n,g); steps+=1
            assert st.norm()==(1,0)
            maxerr=max(maxerr,float(np.max(np.abs(numeric(st)-nv))))
        # Adjoints/involutions, checked exactly.
        assert st.h(0).h(0)==st
        assert st.p(0,1).p(0,7)==st
        if n>1: assert st.cx(0,1).cx(0,1)==st
    results['random_circuits']=240; results['exact_normalization_checks']=steps
    results['numerical_crosscheck_max_amplitude_error']=maxerr
    for trial in range(120):
        n=1+trial%3; gates=[]; hc=0
        for depth in range(16):
            typ=rng.choice(['H','P','X']+(['CX'] if n>1 else []))
            if typ=='H' and hc>=8: typ='P'
            if typ=='H': hc+=1; g=(typ,rng.randrange(n))
            elif typ=='X': g=(typ,rng.randrange(n))
            elif typ=='P': g=(typ,rng.randrange(n),rng.randrange(8))
            else: g=(typ,*rng.sample(range(n),2))
            gates.append(g)
        initial=trial%(1<<n)
        assert run(basis(n,initial),gates)==path_sum(n,gates,initial)
    results['independent_exact_path_sum_circuits']=120
    results['HSH']={str(k):[list(map(str,p)) for p in basis(1).h(0).p(0,2*k).h(0).probabilities()] for k in range(4)}
    results['HTH']=[list(map(str,p)) for p in basis(1).h(0).p(0,1).h(0).probabilities()]
    dj=[]
    for n in (2,3):
        good=0; total=0
        for bits in itertools.product((0,1),repeat=1<<n):
            if sum(bits) not in (0,1<<(n-1),1<<n): continue
            st=basis(n+1,1)
            for q in range(n+1): st=st.h(q)
            st=st.permute(lambda i,bs=bits:i^bs[i>>1])
            for q in range(n): st=st.h(q)
            p=st.probabilities(); pzero=(p[0][0]+p[1][0],p[0][1]+p[1][1])
            correct=pzero==((1,0) if sum(bits) in (0,1<<n) else (0,0))
            assert correct; good+=correct; total+=1
        dj.append({'n':n,'functions':total,'correct':good})
    results['Deutsch_Jozsa']=dj
    grover=[]
    for n in (2,3):
        ps=[]
        for marked in range(1<<n):
            st=basis(n)
            for q in range(n): st=st.h(q)
            st=st.oracle_phase(lambda i,m=marked:i==m)
            for q in range(n): st=st.h(q)
            st=st.oracle_phase(lambda i:i!=0)
            for q in range(n): st=st.h(q)
            assert st.norm()==(1,0)
            ps.append(list(map(str,st.probabilities()[marked])))
        grover.append({'n':n,'all_marked_probabilities':ps})
    results['Grover']=grover
    bell=basis(2).h(0).cx(0,1)
    results['Bell']={}
    for axes in ['ZZ','XX','ZX','XZ']:
        st=bell
        for q,axis in enumerate(axes):
            if axis=='X': st=st.h(q)
        results['Bell'][axes]=list(map(str,expectation(st)))
    CHSH=[]
    for a,b in itertools.product((0,1),repeat=2):
        st=bell.h(0) if a else bell
        # B0=(Z+X)/sqrt(2); B1=(Z-X)/sqrt(2).
        st=st.p(1,6).h(1).p(1,7 if b==0 else 1).h(1).p(1,2)
        CHSH.append(expectation(st))
        # Both local marginals remain 1/2, for all setting pairs.
        pp=st.probabilities()
        for q in (0,1):
            marg=[Fraction(),Fraction()]
            for i,p in enumerate(pp):
                if not i&(1<<(1-q)): marg=[x+y for x,y in zip(marg,p)]
            assert marg==[Fraction(1,2),Fraction()]
    total=[sum(((-1 if i==3 else 1)*c[j] for i,c in enumerate(CHSH)),Fraction()) for j in (0,1)]
    assert total==[0,2]
    results['CHSH']={'correlations':[list(map(str,c)) for c in CHSH],'S':list(map(str,total)),'exact_C8_measurements':True}
    # Original CM truth predicates produce reversible oracles and phase gates.
    def truth(cm,x,y): return (cm>>{(1,1):0,(1,0):1,(0,0):2,(0,1):3}[(x,y)])&1
    predchecks=0
    for a,b,k,x,y in itertools.product(range(16),range(16),range(8),(0,1),(0,1)):
        fa,fb=truth(a,x,y),truth(b,x,y)
        assert (k*(fa^fb))%8==(k*fa+k*fb-2*k*(fa&fb))%8
        predchecks+=1
    for a in range(16):
        d=truth(a,0,0); p=truth(a,1,0)^d; q=truth(a,0,1)^d
        r=truth(a,1,1)^truth(a,1,0)^truth(a,0,1)^d
        for x,y in itertools.product((0,1),repeat=2):
            assert truth(a,x,y)==(d^(p&x)^(q&y)^(r&x&y))
    results['predicate_phase_identity_checks']=predchecks
    results['all_16_pi_phase_oracle_decompositions']=True
    results['elapsed_seconds']=round(time.monotonic()-start,3)
    OUT.mkdir(exist_ok=True); (OUT/'quantum_summary.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
