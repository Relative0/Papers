#!/usr/bin/env python3
"""Verification suite for the exclusive-inversion matching theorem.

This script is intentionally self contained. It verifies:
  * full doubled-product / missing-copy relative pair model;
  * exact matching-link homology formula over Z for all n<=4 cases;
  * the same formula over F_2 in targeted n=5 samples;
  * product-edge-link suspension identity over F_2 through n=5;
  * neutrality when there is no exclusive inversion edge (n<=4);
  * the smallest forest-but-not-matching failure of naive pairwise additivity;
  * Boolean-lattice endpoint examples B_2 and B_3 directly over Z.

Availability code per coarse state:
  0 = {0} only, 1 = {1} only, 2 = {0,1} split.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import defaultdict
from dataclasses import dataclass
import json, csv, random, time
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

OUT = Path(__file__).resolve().parent

# ---------------- finite posets ----------------

def natural_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    seen=set()
    for bits in range(1<<len(pairs)):
        le=[[False]*n for _ in range(n)]
        for i in range(n): le[i][i]=True
        for k,(i,j) in enumerate(pairs):
            if bits>>k & 1: le[i][j]=True
        for k in range(n):
            for i in range(n):
                if le[i][k]:
                    for j in range(n):
                        if le[k][j]: le[i][j]=True
        key=tuple(tuple(r) for r in le)
        if key not in seen:
            seen.add(key); yield le

def strict(le,i,j): return i!=j and le[i][j]

def chains(le):
    """All nonempty strict chains, indexed by simplex dimension."""
    n=len(le); out=defaultdict(list)
    for i in range(n): out[0].append((i,))
    def extend(c):
        last=c[-1]
        for j in range(last+1,n):
            if strict(le,last,j):
                d=c+(j,); out[len(d)-1].append(d); extend(d)
    for i in range(n): extend((i,))
    return out

def induced_le(le, verts):
    return [[le[i][j] for j in verts] for i in verts]

# ---------------- integer chain algebra ----------------

def integer_boundary(ch):
    maxd=max(ch.keys(), default=0)
    mats={}
    for d in range(1,maxd+1):
        rows=ch[d-1]; cols=ch[d]; ri={c:i for i,c in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,c in enumerate(cols):
            for k in range(len(c)):
                f=c[:k]+c[k+1:]
                M[ri[f]][j] += -1 if k%2 else 1
        mats[d]=M
    return mats

def relative_chains_and_boundary(leK, leL=None, L_vertex_subset=None):
    """Relative simplicial chains C_*(Delta K, Delta L).

    Either leL is an order on same vertex set with Delta L subset Delta K,
    or L_vertex_subset is a subset of K vertices and L is the induced subcomplex.
    """
    chK=chains(leK)
    if leL is not None:
        chL=chains(leL)
        Lsets={d:set(v) for d,v in chL.items()}
    elif L_vertex_subset is not None:
        S=set(L_vertex_subset)
        Lsets={d:{c for c in cs if all(v in S for v in c)} for d,cs in chK.items()}
    else:
        Lsets={}
    maxd=max(chK.keys(), default=0)
    rel={d:[c for c in chK[d] if c not in Lsets.get(d,set())] for d in range(maxd+1)}
    mats={}
    for d in range(1,maxd+1):
        rows=rel[d-1]; cols=rel[d]; ri={c:i for i,c in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,c in enumerate(cols):
            for k in range(len(c)):
                f=c[:k]+c[k+1:]
                i=ri.get(f)
                if i is not None:
                    M[i][j] += -1 if k%2 else 1
        mats[d]=M
    return rel,mats

def _dm(M, shape):
    rows,cols=shape
    if rows==0 or cols==0:
        return DomainMatrix.zeros(shape, ZZ)
    return DomainMatrix([[ZZ(x) for x in row] for row in M], shape, ZZ)

def homology_Z(dims, mats):
    """Integral homology of finite free chain complex.

    Return degree -> {free:int, torsion:[positive invariant factors >1]}.
    Uses a Smith decomposition of d_n to obtain a primitive Z-basis for ker d_n,
    then Smith form again for im d_{n+1} in that kernel basis.
    """
    maxd=max(dims.keys(), default=0)
    out={}
    for n in range(maxd+1):
        cn=dims.get(n,0)
        # d_n: C_n -> C_{n-1}
        if n==0:
            rank_dn=0
            T=Matrix.eye(cn)
        else:
            rdim=dims.get(n-1,0)
            A=_dm(mats.get(n, [[0]*cn for _ in range(rdim)]), (rdim,cn))
            D,S,Tdm=smith_normal_decomp(A)
            Dm=D.to_Matrix(); T=Tdm.to_Matrix()
            rank_dn=sum(1 for i in range(min(Dm.rows,Dm.cols)) if Dm[i,i]!=0)
        kdim=cn-rank_dn
        # coordinates of im d_{n+1} in the kernel basis
        p=dims.get(n+1,0)
        if p==0 or kdim==0:
            rank_im=0; tors=[]
        else:
            B=Matrix(mats.get(n+1, [[0]*p for _ in range(cn)]))
            if B.rows==0: B=Matrix.zeros(cn,p)
            Tinv=T.inv()
            C=Tinv*B
            # d_n d_{n+1}=0 => first rank_dn rows are zero
            for i in range(rank_dn):
                if any(C[i,j] != 0 for j in range(C.cols)):
                    raise AssertionError(f'boundary composition/kernel coordinates failed in degree {n}')
            Cker=C[rank_dn:,:]
            Cdm=DomainMatrix.from_Matrix(Cker).convert_to(ZZ)
            SD,_,_=smith_normal_decomp(Cdm)
            Sm=SD.to_Matrix()
            inv=[]
            for i in range(min(Sm.rows,Sm.cols)):
                if Sm[i,i]!=0: inv.append(abs(int(Sm[i,i])))
            rank_im=len(inv)
            tors=[d for d in inv if d>1]
        out[n]={'free': kdim-rank_im, 'torsion': tors}
    # trim high zero groups
    while out and max(out) > 0 and out[max(out)]=={'free':0,'torsion':[]}:
        del out[max(out)]
    return out

def ordinary_homology_Z(le):
    ch=chains(le); mats=integer_boundary(ch)
    dims={d:len(cs) for d,cs in ch.items()}
    return homology_Z(dims,mats)

def reduced_homology_Z(le):
    n=len(le)
    if n==0:
        return {-1:{'free':1,'torsion':[]}}
    H=ordinary_homology_Z(le)
    H={d:{'free':v['free'],'torsion':list(v['torsion'])} for d,v in H.items()}
    if 0 not in H: H[0]={'free':0,'torsion':[]}
    H[0]['free']-=1
    if H[0]['free']==0 and not H[0]['torsion']: del H[0]
    return H

def add_groups(A,B):
    out={d:{'free':v['free'],'torsion':list(v['torsion'])} for d,v in A.items()}
    for d,v in B.items():
        o=out.setdefault(d,{'free':0,'torsion':[]})
        o['free']+=v['free']; o['torsion']+=v['torsion']; o['torsion'].sort()
    return {d:v for d,v in sorted(out.items()) if v['free'] or v['torsion']}

def shift_groups(A,s):
    return {d+s:{'free':v['free'],'torsion':list(v['torsion'])} for d,v in A.items()}

def normalize_groups(H, include_h0=True):
    return {int(d):{'free':int(v['free']),'torsion':sorted(map(int,v['torsion']))}
            for d,v in H.items() if v['free'] or v['torsion']}

# ---------------- GF2 quick homology ----------------

def gf2_rank(M):
    if not M: return 0
    A=[[(x&1) for x in row] for row in M]
    m=len(A); n=len(A[0]) if m else 0; r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(m):
            if i!=r and A[i][c]:
                for j in range(c,n): A[i][j]^=A[r][j]
        r+=1
        if r==m: break
    return r

def homology_f2(dims,mats):
    out={}
    for n,cn in dims.items():
        rn=gf2_rank(mats.get(n,[])) if n>=1 else 0
        rn1=gf2_rank(mats.get(n+1,[])) if (n+1) in mats else 0
        b=cn-rn-rn1
        if b: out[n]=b
    return out

# ---------------- carrier profile / models ----------------

def full_product_poset(le):
    n=len(le); verts=[(s,a) for s in range(n) for a in (0,1)]
    idx={v:i for i,v in enumerate(verts)}; N=2*n
    D=[[False]*N for _ in range(N)]
    for i,(s,a) in enumerate(verts):
        for j,(t,b) in enumerate(verts):
            if le[s][t] and a<=b: D[i][j]=True
    return verts,D,idx

def available_vertices(n,avail,idx):
    V=[]
    for s,a in enumerate(avail):
        if a in (0,2): V.append(idx[(s,0)])
        if a in (1,2): V.append(idx[(s,1)])
    return V

def exclusive_sets(avail):
    Z={i for i,a in enumerate(avail) if a==0} # 0-only
    P={i for i,a in enumerate(avail) if a==1} # 1-only
    C={i for i,a in enumerate(avail) if a==2}
    return P,Z,C

def exclusive_edges(le,avail):
    P,Z,_=exclusive_sets(avail)
    return [(p,z) for p in sorted(P) for z in sorted(Z) if strict(le,p,z)]

def matching_edges(E):
    seen=set()
    for p,z in E:
        if ('p',p) in seen or ('z',z) in seen: return False
        seen.add(('p',p)); seen.add(('z',z))
    return True

def coarse_edge_link_poset(le,p,z):
    verts=[]
    for x in range(len(le)):
        if x in (p,z): continue
        if strict(le,x,p) or (strict(le,p,x) and strict(le,x,z)) or strict(le,z,x):
            verts.append(x)
    return induced_le(le,verts), verts

def matching_formula_Z(le,avail):
    ans={}
    for p,z in exclusive_edges(le,avail):
        lkle,_=coarse_edge_link_poset(le,p,z)
        RH=reduced_homology_Z(lkle)
        ans=add_groups(ans,shift_groups(RH,2))
    return normalize_groups(ans)

def relative_pair_Z(le,avail):
    verts,D,idx=full_product_poset(le)
    V=available_vertices(len(le),avail,idx)
    rel,mats=relative_chains_and_boundary(D,L_vertex_subset=V)
    dims={d:len(cs) for d,cs in rel.items()}
    return normalize_groups(homology_Z(dims,mats))

def relative_pair_f2(le,avail):
    verts,D,idx=full_product_poset(le)
    V=available_vertices(len(le),avail,idx)
    rel,mats=relative_chains_and_boundary(D,L_vertex_subset=V)
    dims={d:len(cs) for d,cs in rel.items()}
    return homology_f2(dims,mats)

def formula_f2(le,avail):
    out=defaultdict(int)
    for p,z in exclusive_edges(le,avail):
        lk,_=coarse_edge_link_poset(le,p,z)
        if len(lk)==0:
            out[1]+=1 # reduced H_-1 shifted by 2
            continue
        ch=chains(lk); bm=integer_boundary(ch); dims={d:len(cs) for d,cs in ch.items()}
        H=homology_f2(dims,bm)
        # reduced H0
        if 0 in H:
            if H[0]-1:
                out[2]+=H[0]-1
        # higher
        for d,b in H.items():
            if d>=1: out[d+2]+=b
    return dict(sorted((d,b) for d,b in out.items() if b))

# -------- product edge link suspension check over F2 --------

def open_interval_product_edge(le,p,z):
    verts,D,idx=full_product_poset(le)
    a=idx[(p,0)]; b=idx[(z,1)]
    mids=[i for i in range(len(D)) if strict(D,a,i) and strict(D,i,b)]
    return induced_le(D,mids)

def reduced_betti_f2(le):
    if len(le)==0: return {-1:1}
    ch=chains(le); bm=integer_boundary(ch); dims={d:len(cs) for d,cs in ch.items()}
    H=homology_f2(dims,bm); out={}
    if H.get(0,0)-1: out[0]=H[0]-1
    for d,b in H.items():
        if d>=1 and b: out[d]=b
    return out

def link_product_edge_poset(le,p,z):
    verts,D,idx=full_product_poset(le)
    a=idx[(p,0)]; b=idx[(z,1)]
    vals=[]
    for i in range(len(D)):
        if i in (a,b): continue
        # link vertex iff can appear with edge in a chain: i<a or a<i<b or b<i
        if strict(D,i,a) or (strict(D,a,i) and strict(D,i,b)) or strict(D,b,i): vals.append(i)
    return induced_le(D,vals)

def suspension_shift(H): return {d+1:b for d,b in H.items()}

# ---------------- Boolean lattice ----------------

def boolean_lattice(m):
    vals=list(range(1<<m)); n=len(vals)
    le=[[False]*n for _ in range(n)]
    for i,a in enumerate(vals):
        for j,b in enumerate(vals):
            le[i][j]=(a & b)==a
    return le

# ---------------- main tests ----------------

def main():
    t0=time.time(); rows=[]
    total=match_cases=match_nonempty=match_fail=neutral_edgefree_fail=0
    posets_by_n={}
    integral_checked=0
    for n in range(1,5):
        posets=list(natural_posets(n)); posets_by_n[n]=posets
        for pid,le in enumerate(posets):
            for avail in product(range(3), repeat=n):
                total+=1
                E=exclusive_edges(le,avail)
                actual=None
                if not E:
                    H2=relative_pair_f2(le,avail)
                    if H2: neutral_edgefree_fail+=1
                if matching_edges(E):
                    match_cases+=1
                    if E: match_nonempty+=1
                    actual=relative_pair_Z(le,avail)
                    pred=matching_formula_Z(le,avail)
                    integral_checked+=1
                    if actual!=pred:
                        match_fail+=1
                        raise AssertionError(('integral matching formula fail',n,pid,avail,E,actual,pred))
                    if E and len(rows)<250:
                        rows.append({'n':n,'poset_id':pid,'avail':' '.join(map(str,avail)),
                                     'edges':';'.join(f'{p}<{z}' for p,z in E),
                                     'actual_Z':json.dumps(actual,sort_keys=True),
                                     'pred_Z':json.dumps(pred,sort_keys=True)})
    # product edge link suspension over all comparable pairs through n=5
    suspension_checks=0
    for n in range(2,6):
        posets=list(natural_posets(n)); posets_by_n[n]=posets
        for le in posets:
            for p in range(n):
                for z in range(n):
                    if not strict(le,p,z): continue
                    LK=link_product_edge_poset(le,p,z)
                    CL,_=coarse_edge_link_poset(le,p,z)
                    a=reduced_betti_f2(LK); b=suspension_shift(reduced_betti_f2(CL))
                    if a!=b: raise AssertionError(('link suspension fail',n,p,z,a,b))
                    suspension_checks+=1
    # random n=5 profile checks (F2), all natural-posets with deterministic pseudo-random profiles
    rng=random.Random(20260929)
    n5=posets_by_n[5]
    random_trials=3000; sampled_matching=0
    for _ in range(random_trials):
        le=rng.choice(n5); avail=tuple(rng.randrange(3) for _ in range(5))
        E=exclusive_edges(le,avail)
        if E and matching_edges(E):
            sampled_matching+=1
            a=relative_pair_f2(le,avail); b=formula_f2(le,avail)
            if a!=b: raise AssertionError(('n5 F2 fail',avail,E,a,b))
    # minimal forest-not-matching counterexample: 3-chain with profile 1,0,0
    le3=[[i<=j for j in range(3)] for i in range(3)]
    av=(1,0,0); E=exclusive_edges(le3,av)
    actual3=relative_pair_Z(le3,av)
    naive3=matching_formula_Z(le3,av) # intentionally applies pair-sum outside matching
    if matching_edges(E): raise AssertionError('counterexample graph unexpectedly matching')
    if actual3==naive3: raise AssertionError('forest-not-matching counterexample did not fail naive formula')
    # Boolean endpoint examples, direct for B2/B3, predicted for B4
    bool_rows=[]
    for m in (2,3):
        le=boolean_lattice(m); n=len(le); av=[2]*n; av[0]=1; av[-1]=0
        actual=relative_pair_Z(le,tuple(av)); pred=matching_formula_Z(le,tuple(av))
        if actual!=pred: raise AssertionError(('Boolean endpoint fail',m,actual,pred))
        bool_rows.append({'m':m,'coarse_states':n,'actual_Z':actual,'pred_Z':pred})
    m=4; le=boolean_lattice(m); n=len(le); av=[2]*n; av[0]=1; av[-1]=0
    bool_rows.append({'m':m,'coarse_states':n,'actual_Z':'not brute-forced','pred_Z':matching_formula_Z(le,tuple(av))})

    summary={
        'exhaustive_n_le_4_total_profiles':total,
        'matching_cases_integral_snf_checked':integral_checked,
        'matching_cases':match_cases,
        'matching_cases_with_nonempty_exclusive_edges':match_nonempty,
        'matching_formula_failures':match_fail,
        'edge_free_neutrality_failures_f2':neutral_edgefree_fail,
        'product_edge_link_suspension_checks_through_n5':suspension_checks,
        'random_n5_trials':random_trials,
        'random_n5_matching_nonempty_cases_checked_f2':sampled_matching,
        'forest_not_matching_counterexample':{
            'coarse_poset':'3-chain 0<1<2', 'availability':[1,0,0],
            'exclusive_edges':E,
            'actual_relative_Z':actual3,
            'naive_pair_sum_Z':naive3
        },
        'boolean_endpoint_examples':bool_rows,
        'elapsed_seconds':round(time.time()-t0,3)
    }
    (OUT/'verification_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True))
    with (OUT/'matching_cases_sample.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['n','poset_id','avail','edges','actual_Z','pred_Z']); w.writeheader(); w.writerows(rows)
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
