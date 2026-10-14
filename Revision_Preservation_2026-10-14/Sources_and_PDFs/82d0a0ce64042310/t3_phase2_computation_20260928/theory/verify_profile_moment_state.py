#!/usr/bin/env python3
from __future__ import annotations
from itertools import product, combinations
from math import comb
import json, random, pathlib

OUT = pathlib.Path('/mnt/data/t1_t3_work/phase2/t3_verification_results.json')

def subsets(coords, h):
    coords=tuple(coords)
    out=[]
    for j in range(min(h,len(coords))+1):
        out.extend(combinations(coords,j))
    return out

def bit(assign, i, d):
    # coordinate i in 0..d-1, little-endian convention
    return (assign >> i) & 1

def dot2(a,b):
    return (a & b).bit_count() & 1

def factor_count(U,W,p,q,r,rho):
    total=0
    for x in range(1<<p):
        ok=True
        for side,i,b in rho:
            if side=='X' and bit(x,i,p)!=b:
                ok=False; break
        if not ok: continue
        for y in range(1<<q):
            ok2=True
            for side,i,b in rho:
                if side=='Y' and bit(y,i,q)!=b:
                    ok2=False; break
            if not ok2: continue
            total += dot2(U[x], W[y])
    return total

def build_state(U,W,p,q,r,k,anchor='X'):
    # For current proof artifact we implement anchor X; symmetric anchor Y verified by swapping externally.
    assert anchor=='X'
    profiles=sorted(set(U))
    nonzero=[a for a in profiles if a!=0]
    Xcoords=tuple(range(p)); Ycoords=tuple(range(q))
    A={}
    for a in nonzero:
        for T in subsets(Xcoords,k):
            c=0
            for x in range(1<<p):
                if U[x]==a and all(bit(x,i,p)==1 for i in T):
                    c += 1
            A[(a,T)] = c
    B={}
    for a in nonzero:
        for T in subsets(Ycoords,k):
            s=0
            for y in range(1<<q):
                if all(bit(y,j,q)==1 for j in T):
                    s += -1 if dot2(a,W[y]) else 1
            B[(a,T)] = s
    return {'p':p,'q':q,'r':r,'h':k,'Xcoords':Xcoords,'Ycoords':Ycoords,'profiles':tuple(nonzero),'A':A,'B':B}

def query_state(st):
    dx=len(st['Xcoords']); dy=len(st['Ycoords'])
    nonzero=st['profiles']
    alpha_non=[st['A'][(a,())] for a in nonzero]
    alpha0=(1<<dx)-sum(alpha_non)
    sign=alpha0*(1<<dy)
    for a,aa in zip(nonzero,alpha_non):
        sign += aa*st['B'][(a,())]
    rc=1<<(dx+dy)
    num=rc-sign
    assert num%2==0
    return num//2

def update_state(st,side,i,b):
    h=st['h']
    assert h>=1
    if side=='X':
        assert i in st['Xcoords']
        Xnew=tuple(c for c in st['Xcoords'] if c!=i)
        Ynew=st['Ycoords']
        Anew={}
        for a in st['profiles']:
            for T in subsets(Xnew,h-1):
                if b==1:
                    v=st['A'][(a,tuple(sorted(T+(i,))))]
                else:
                    v=st['A'][(a,T)]-st['A'][(a,tuple(sorted(T+(i,))))]
                Anew[(a,T)]=v
        Bnew={(a,T):v for (a,T),v in st['B'].items() if len(T)<=h-1}
    else:
        assert side=='Y' and i in st['Ycoords']
        Xnew=st['Xcoords']
        Ynew=tuple(c for c in st['Ycoords'] if c!=i)
        Bnew={}
        for a in st['profiles']:
            for T in subsets(Ynew,h-1):
                if b==1:
                    v=st['B'][(a,tuple(sorted(T+(i,))))]
                else:
                    v=st['B'][(a,T)]-st['B'][(a,tuple(sorted(T+(i,))))]
                Bnew[(a,T)]=v
        Anew={(a,T):v for (a,T),v in st['A'].items() if len(T)<=h-1}
    return {**st,'h':h-1,'Xcoords':Xnew,'Ycoords':Ynew,'A':Anew,'B':Bnew}

def matmul_vec_row(a,G,r):
    # G list of r rows as r-bit ints; row vector a times G
    out=0
    for j in range(r):
        v=0
        for i in range(r):
            v ^= ((a>>i)&1) & ((G[i]>>j)&1)
        out |= v<<j
    return out

def mat_vec(G,b,r):
    # G times column b
    out=0
    for i in range(r):
        v=(G[i] & b).bit_count() & 1
        out |= v<<i
    return out

def invert_matrix(G,r):
    rows=[G[i] | (1<<(r+i)) for i in range(r)]
    for c in range(r):
        piv=next((i for i in range(c,r) if (rows[i]>>c)&1),None)
        if piv is None: return None
        rows[c],rows[piv]=rows[piv],rows[c]
        for i in range(r):
            if i!=c and ((rows[i]>>c)&1): rows[i]^=rows[c]
    inv=[]
    mask=(1<<r)-1
    for i in range(r): inv.append((rows[i]>>r)&mask)
    return inv

def random_GL(r,rng):
    while True:
        G=[rng.randrange(1<<r) for _ in range(r)]
        inv=invert_matrix(G,r)
        if inv is not None: return G,inv

def gauge(U,W,G,Ginv,r):
    Ug=[matmul_vec_row(a,G,r) for a in U]
    Wg=[mat_vec(Ginv,b,r) for b in W]
    return Ug,Wg

def parity_reset_counterexample(k):
    n=k+1
    # return Q_k agreement by direct counts for parity and complement, then residual point mismatch after x0=0
    def f(x): return x.bit_count()&1
    def g(x): return 1-f(x)
    # every restriction <=k
    for s in range(k+1):
        for S in combinations(range(n),s):
            for vals in product((0,1), repeat=s):
                cf=cg=0
                for x in range(1<<n):
                    if all(((x>>i)&1)==v for i,v in zip(S,vals)):
                        cf+=f(x); cg+=g(x)
                if cf!=cg: return False
    # after fix x0=0, a full residual assignment differs
    # all remaining zero gives f=0,g=1
    return f(0)!=g(0)

def unordered_hist_counterexample():
    # p=q=r=1, U=x vs 1-x, W=y -> same unconditional U/W histograms and total count, restriction x=0 differs.
    p=q=r=1
    U1=[0,1]; U2=[1,0]; W=[0,1]
    h1=sorted(U1); h2=sorted(U2)
    wh=sorted(W)
    c1=factor_count(U1,W,p,q,r,[]); c2=factor_count(U2,W,p,q,r,[])
    r1=factor_count(U1,W,p,q,r,[('X',0,0)]); r2=factor_count(U2,W,p,q,r,[('X',0,0)])
    return {'same_U_hist':h1==h2,'same_W_hist':True,'same_total':c1==c2,'restricted_counts':[r1,r2]}

def one_bit_kappa_warning(n):
    # even/odd parity class: Q_{n-1} collision, but one class-id bit identifies source.
    def f(x): return x.bit_count()&1
    def g(x): return 1-f(x)
    equal=True
    k=n-1
    for s in range(k+1):
        # sample all for n<=5 in tests
        for S in combinations(range(n),s):
            for vals in product((0,1),repeat=s):
                cf=cg=0
                for x in range(1<<n):
                    if all(((x>>i)&1)==v for i,v in zip(S,vals)):
                        cf+=f(x); cg+=g(x)
                if cf!=cg: equal=False
    return equal

def main():
    rng=random.Random(20260928)
    checks=0
    # exhaustive all factors for p,q <=2, r<=2, all k; this includes duplicate/nonminimal factorizations.
    exhaustive_cases=0
    for p in range(1,3):
      for q in range(1,3):
       for r in range(1,3):
        vals=list(range(1<<r))
        Us=list(product(vals, repeat=1<<p))
        Ws=list(product(vals, repeat=1<<q))
        # avoid explosion for p=q=2,r=2 by sample if product > 65536
        pairs=len(Us)*len(Ws)
        if pairs>65536:
            samples=[(tuple(rng.choice(vals) for _ in range(1<<p)),tuple(rng.choice(vals) for _ in range(1<<q))) for _ in range(5000)]
        else:
            samples=((U,W) for U in Us for W in Ws)
        for U,W in samples:
          exhaustive_cases+=1
          for k in range(0,p+q+1):
            st=build_state(U,W,p,q,r,k)
            assert query_state(st)==factor_count(U,W,p,q,r,[]); checks+=1
            # random/all legal paths up to k; exhaustive coordinate permutations/values if n<=3, random otherwise
            coords=[('X',i) for i in range(p)]+[('Y',j) for j in range(q)]
            paths=[]
            maxs=min(k,len(coords))
            if len(coords)<=3:
                for s in range(maxs+1):
                    for chosen in combinations(coords,s):
                        for valsbits in product((0,1),repeat=s):
                            paths.append(list(zip(chosen,valsbits)))
            else:
                for _ in range(8):
                    s=rng.randint(0,maxs)
                    chosen=rng.sample(coords,s)
                    paths.append([((sd,i),rng.randint(0,1)) for sd,i in chosen])
            for path in paths:
                cur=st; rho=[]
                for ((sd,i),b) in path:
                    cur=update_state(cur,sd,i,b)
                    rho.append((sd,i,b))
                    assert query_state(cur)==factor_count(U,W,p,q,r,rho)
                    checks+=1
    # randomized larger + gauge tests
    gauge_checks=0
    for _ in range(500):
        p=rng.randint(1,5); q=rng.randint(1,5); r=rng.randint(1,3); k=rng.randint(0,min(4,p+q))
        U=tuple(rng.randrange(1<<r) for _ in range(1<<p)); W=tuple(rng.randrange(1<<r) for _ in range(1<<q))
        st=build_state(U,W,p,q,r,k)
        assert query_state(st)==factor_count(U,W,p,q,r,[]); checks+=1
        if r>=1:
            G,Ginv=random_GL(r,rng); Ug,Wg=gauge(U,W,G,Ginv,r)
            assert all(dot2(U[x],W[y])==dot2(Ug[x],Wg[y]) for x in range(1<<p) for y in range(1<<q))
            stg=build_state(Ug,Wg,p,q,r,k)
            assert query_state(stg)==query_state(st)
            # profile labels should permute by a -> aG; compare A and B moments where profile occurs
            maplab={a:matmul_vec_row(a,G,r) for a in st['profiles']}
            assert set(maplab.values())==set(stg['profiles'])
            for a in st['profiles']:
                ap=maplab[a]
                for T in subsets(range(p),k):
                    assert st['A'][(a,T)]==stg['A'][(ap,T)]
                for T in subsets(range(q),k):
                    assert st['B'][(a,T)]==stg['B'][(ap,T)]
                    gauge_checks+=1
    reset=[parity_reset_counterexample(k) for k in range(1,6)]
    onebit=[one_bit_kappa_warning(n) for n in range(1,6)]
    hist=unordered_hist_counterexample()
    assert all(reset) and all(onebit) and hist['same_U_hist'] and hist['same_total'] and hist['restricted_counts'][0]!=hist['restricted_counts'][1]
    # storage/crossover examples
    def D(d,k): return sum(comb(d,j) for j in range(min(d,k)+1))
    examples=[]
    for p,q,r,k in [(10,10,2,1),(10,10,2,2),(16,16,3,2),(20,20,3,2),(20,20,4,2),(20,20,4,4)]:
        m=(1<<r)-1
        B=m*((p+1)*D(p,k)+(q+2)*D(q,k))
        factor=r*((1<<p)+(1<<q))
        full=1<<(p+q)
        examples.append({'p':p,'q':q,'r':r,'k':k,'D_p':D(p,k),'D_q':D(q,k),'state_bits_worst':B,'factor_bits':factor,'full_truth_bits':full,'state_over_factor':B/factor})
    out={
      'status':'PASS','checks':checks,'enumerated_factor_cases':exhaustive_cases,'gauge_moment_checks':gauge_checks,
      'reset_horizon_parity_k_1_to_5':reset,'one_bit_kappa_warning_n_1_to_5':onebit,
      'unordered_histogram_counterexample':hist,'storage_examples':examples
    }
    OUT.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
