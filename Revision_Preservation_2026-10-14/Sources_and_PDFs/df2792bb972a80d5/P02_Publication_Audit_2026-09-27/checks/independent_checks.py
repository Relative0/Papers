#!/usr/bin/env python3
"""Fresh bounded checks for P02. No original experiment code was supplied.
Python >=3.10, standard library only. Exhaustive domains are stated in JSON.
These computations do not replace the general proofs in the audit report.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, platform, random, sys, time
from pathlib import Path

def rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for v in vectors:
        while v:
            k = v.bit_length()-1
            if k in pivots: v ^= pivots[k]
            else:
                pivots[k]=v
                break
    return len(pivots)

def lin(v: int, cols: tuple[int,...] | list[int]) -> int:
    out=0
    while v:
        b=v & -v; out ^= cols[b.bit_length()-1]; v ^= b
    return out

GL2=[c for c in itertools.product(range(4),repeat=2) if rank(list(c))==2]

def oracle(v: int, n: int, secret: int, g0: tuple[int,...], g1: tuple[int,...]) -> int:
    out=0
    for x in range(1<<n):
        g=g1 if (secret & x).bit_count()%2 else g0
        out |= lin((v>>(2*x))&3,g)<<(2*x)
    return out

def truth_oracle(v: int, f: list[int], g0=(1,2), g1=(2,1), anc=1) -> int:
    out=0
    for x,bit in enumerate(f):
        g=g1 if bit else g0
        for a in range(anc):
            i=(x*anc+a)*2
            out |= lin((v>>i)&3,g)<<i
    return out

def deutsch_checks():
    report=[]
    for anc in [1,2]:
        dim=4*anc; standard_pass=0; total=0
        for g0,g1 in itertools.product(GL2,repeat=2):
            for v in range(1,1<<dim):
                vs=[truth_oracle(v,list(f),g0,g1,anc) for f in [(0,0),(0,1),(1,0),(1,1)]]
                rc=rank([vs[0],vs[3]]); rb=rank([vs[1],vs[2]])
                assert rank(vs)<rc+rb
                assert vs[0]^vs[3]==vs[1]^vs[2]
                if vs[0]^vs[3]==0: assert len(set(vs))==1
                total+=1
                if g0==(1,2) and g1==(2,1): standard_pass+=1
        report.append({'dimension':dim,'ancilla_dimension':anc,'invertible_pairs':36,'preparations_per_pair':(1<<dim)-1,'cases':total,'QXOR_preparations':standard_pass,'exact_one_query_solutions':0})
    return report

def dj_checks():
    cases=0
    for g0,g1 in itertools.product(GL2,repeat=2):
        for v in range(1,256):
            zero=truth_oracle(v,[0]*4,g0,g1)
            a=truth_oracle(v,[1,1,0,0],g0,g1)
            b=truth_oracle(v,[1,0,1,0],g0,g1)
            c=truth_oracle(v,[0,1,1,0],g0,g1)
            assert a^b^c==zero and zero!=0
            cases+=1
    return {'n':2,'dimension':8,'pairs':36,'preparations_per_pair':255,'operator_relation_cases':cases}

def tensor_binary(a: int,b: int,db: int) -> int:
    out=0
    while a:
        z=a&-a; out ^= b<<((z.bit_length()-1)*db); a^=z
    return out

def monomial_column(s: int,n:int,q:int) -> int:
    subsets=[j for j in range(1<<n) if j.bit_count()<=q]
    return sum(1<<i for i,j in enumerate(subsets) if s&j==j)

def evaluation_checks():
    rows=[]
    for n in range(1,8):
        for q in range(n+1):
            r=rank([monomial_column(s,n,q) for s in range(1<<n)])
            expect=sum(math.comb(n,j) for j in range(q+1)); assert r==expect
            rows.append({'n':n,'q':q,'rank':r,'formula':expect})
    count=0
    # Every nonempty promise of Boolean functions on three addresses.
    for promise_mask in range(1,1<<8):
        promise=[f for f in range(8) if promise_mask>>f&1]
        for q in range(4):
            e=[monomial_column(f,3,q) for f in promise]
            graphs=[]
            for f in promise:
                v=sum(1<<(2*x+((f>>x)&1)) for x in range(3))
                state=1
                for _ in range(q): state=tensor_binary(state,v,6)
                graphs.append(state)
            assert rank(e)==rank(graphs)
            count+=1
    return {'Boolean_cube_rank_checks':rows,'query_feature_vs_parallel_graph_rank_checks':count,'scope':'All 255 nonempty promises on 3 Boolean addresses, q=0,1,2,3; not a complexity-of-gates claim.'}

def random_gate(dim:int,rng:random.Random):
    cols=[1<<i for i in range(dim)]
    for _ in range(dim*2):
        a,b=rng.sample(range(dim),2)
        cols=[v ^ (((v>>a)&1)<<b) for v in cols]
    assert rank(cols)==dim
    return tuple(cols)

def make_tree(n:int,q:int,rng:random.Random,leaf_index:list[int],root=False):
    dim=2*(1<<n); gate=random_gate(dim,rng)
    if q==0 or (not root and rng.randrange(4)==0):
        i=leaf_index[0]; leaf_index[0]+=1
        return ('leaf',gate,i)
    g0=rng.choice(GL2); g1=rng.choice(GL2)
    mask=rng.randrange(1,(1<<dim)-1)
    return ('query',gate,g0,g1,mask,make_tree(n,q-1,rng,leaf_index),make_tree(n,q-1,rng,leaf_index))

def run_tree(tree,n:int,s:int,v:int):
    dim=2*(1<<n); v=lin(v,tree[1])
    if tree[0]=='leaf': return v<<(dim*tree[2])
    _,_,g0,g1,mask,left,right=tree
    v=oracle(v,n,s,g0,g1)
    return run_tree(left,n,s,v&mask) ^ run_tree(right,n,s,v&(((1<<dim)-1)^mask))

def adaptive_checks():
    rng=random.Random(27092026); polynomial=0; injectivity=0
    for n in range(1,5):
        for q in range(n+1):
            for _ in range(12):
                leaves=[0]; tree=make_tree(n,q,rng,leaves,True)
                dim=2*(1<<n); v=rng.randrange(1,1<<dim)
                records=[run_tree(tree,n,s,v) for s in range(1<<n)]
                assert all(records)
                coeff=records[:]
                for j in range(n):
                    for s in range(1<<n):
                        if s>>j&1: coeff[s]^=coeff[s^(1<<j)]
                assert all(c==0 for s,c in enumerate(coeff) if s.bit_count()>q)
                polynomial+=1
                if n<=3 and q<=2:
                    for s in range(1<<n):
                        assert rank([run_tree(tree,n,s,1<<i) for i in range(dim)])==dim
                        injectivity+=1
    return {'seed':27092026,'random_finite_tree_degree_checks':polynomial,'fixed_secret_stacked_map_rank_checks':injectivity,'scope':'Random finite complementary-projection instruments, early stopping, branch-specific gates and GL(2,2) pairs; not exhaustive over all instruments or dimensions.'}

def ring_mul(a:int,b:int) -> int:
    r=0
    for i in range(4):
        if b>>i&1: r ^= a<<i
    return r&15

def phase_checks():
    h=[[1,1],[1,5]]; mat=[[1]]; rows=[]
    for n in range(1,7):
        size=len(mat)
        new=[[0]*(2*size) for _ in range(2*size)]
        for i in range(size):
            for j in range(size):
                for a in range(2):
                    for b in range(2): new[2*i+a][2*j+b]=ring_mul(mat[i][j],h[a][b])
        mat=new; cols=[]
        for j in range(len(mat)):
            for k in range(4): cols.append(sum(ring_mul(mat[i][j],1<<k)<<(4*i) for i in range(len(mat))))
        r=rank(cols); assert r==4+2*n
        rows.append({'n':n,'A_module_rank':2**n,'binary_dimension':4*2**n,'binary_matrix_rank':r})
    primitive=0; primitive_eigen=0; all_nonzero_eigen=[]
    for a,b in itertools.product(range(16),repeat=2):
        prim=bool((a&1) or (b&1)); primitive+=prim
        eigen=(b==ring_mul(3,a) and a==ring_mul(3,b))
        if eigen and prim: primitive_eigen+=1
        if eigen and (a or b): all_nonzero_eigen.append([a,b])
    assert primitive==192 and primitive_eigen==0
    return {'rank_checks':rows,'primitive_candidates':primitive,'primitive_R_eigenvectors':primitive_eigen,'nonprimitive_nonzero_R_eigenvectors':all_nonzero_eigen}

def gate_bit(v:int,totalbits:int,k:int,transpose=False):
    out=0
    for i in range(1<<totalbits):
        if (v>>i)&1:
            out ^= 1<<i
            if ((i>>k)&1)==int(transpose): out ^= 1<<(i^(1<<k))
    return out

def unique_sat_checks():
    counts=[]
    for n in range(1,7):
        N=1<<n
        for marked in [None]+list(range(N)):
            v=1
            for k in range(n): v=gate_bit(v,n+1,k)
            w=0
            for i in range(2*N):
                if v>>i&1: w ^= 1<<(i^(N if (i&(N-1))==marked else 0))
            v=w
            for k in range(n): v=gate_bit(v,n+1,k)
            v=gate_bit(v,n+1,n,True)
            w=0
            for i in range(2*N):
                if v>>i&1: w^=1<<(i^((N-1) if i&N else 0))
            v=gate_bit(w,n+1,n,True)
            assert v and ((v==1) if marked is None else ((v&1)==0))
        counts.append({'n':n,'promised_cases':N+1})
    assert sum(x['promised_cases'] for x in counts)==132
    return counts

def simon_checks():
    tables=[]
    for shift in [1,2,3]:
        pair0={0,shift}; pair1=set(range(4))-pair0
        for a,b in itertools.permutations(range(4),2):
            f=[a if x in pair0 else b for x in range(4)]
            cols=[1<<(4*x+(y^f[x])) for x in range(4) for y in range(4)]
            table=[0]*65536
            for v in range(1,65536):
                z=v&-v; table[v]=table[v^z]^cols[z.bit_length()-1]
            tables.append(table)
    found=[]
    for v in range(1,65536):
        states=[t[v] for t in tables]
        rs=[rank(states[i:i+12]) for i in [0,12,24]]
        if sum(rs)==rank(states): found.append(v)
    assert found==[]
    return {'n':2,'no_ancilla_dimension':16,'queries':1,'nonzero_preparations':65535,'oracles':36,'shift_labels':3,'exact_discriminable_preparations':len(found)}

def f4mul(a:int,b:int)->int:
    v=0
    for i in range(2):
        if b>>i&1: v ^= a<<i
    if v&4: v ^= 7
    return v

def f4rank(rows):
    a=[list(v) for v in rows]; r=0
    for col in range(len(a[0]) if a else 0):
        p=next((i for i in range(r,len(a)) if a[i][col]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        inv=next(b for b in [1,2,3] if f4mul(a[r][col],b)==1)
        a[r]=[f4mul(x,inv) for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                k=a[i][col]; a[i]=[x^f4mul(k,y) for x,y in zip(a[i],a[r])]
        r+=1
    return r

def extension_field_checks():
    mats=[m for m in itertools.product(range(4),repeat=4) if f4rank([m[:2],m[2:]])==2]
    assert len(mats)==180
    rng=random.Random(27092027)
    for _ in range(2000):
        g0=rng.choice(mats); g1=rng.choice(mats)
        a=[rng.randrange(4) for _ in range(4)]
        if not any(a): a[0]=1
        vs=[]
        for i,j in [(0,0),(0,1),(1,0),(1,1)]:
            v=[]
            for k,bit in enumerate([i,j]):
                g=g1 if bit else g0; v += [f4mul(g[0],a[2*k])^f4mul(g[1],a[2*k+1]),f4mul(g[2],a[2*k])^f4mul(g[3],a[2*k+1])]
            vs.append(v)
        assert f4rank(vs)<f4rank([vs[0],vs[3]])+f4rank([vs[1],vs[2]])
    return {'field':'F4=F2[t]/(t^2+t+1)','GL2_size':180,'sampled_cases':2000,'seed':27092027,'exact_one_query_solutions':0}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--skip-simon',action='store_true'); parser.add_argument('--output',default='fresh_results.json'); args=parser.parse_args()
    results={'provenance':'New implementation written for this audit; not a rerun of the absent historical canonical runner.','python':sys.version,'platform':platform.platform(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':{}}
    stages=[('deutsch',deutsch_checks),('deutsch_jozsa',dj_checks),('evaluation_rank',evaluation_checks),('adaptive_trees',adaptive_checks),('ring_kickback',phase_checks),('UNIQUE_SAT',unique_sat_checks),('F4_Deutsch',extension_field_checks)]
    if not args.skip_simon: stages.append(('Simon',simon_checks))
    start=time.perf_counter()
    for name,func in stages:
        t=time.perf_counter(); value=func(); elapsed=time.perf_counter()-t
        results['checks'][name]={'result':value,'seconds':elapsed,'status':'PASS'}
        print(name,'PASS',round(elapsed,3),flush=True)
    results['total_seconds']=time.perf_counter()-start
    Path(args.output).write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__': main()
