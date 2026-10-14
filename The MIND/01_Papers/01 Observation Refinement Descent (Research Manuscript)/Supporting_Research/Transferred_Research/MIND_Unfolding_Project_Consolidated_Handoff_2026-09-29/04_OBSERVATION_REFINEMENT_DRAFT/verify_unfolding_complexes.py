#!/usr/bin/env python3
"""Verification for Boolean unfolding layers, simplex skeletons, and mapping-cone profiles.

All homology computations are over F_2. No third-party dependencies.
"""
from itertools import combinations, product
from math import comb
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def rank_mod2(M):
    if not M:
        return 0
    A=[row[:] for row in M]
    nr=len(A); nc=len(A[0]) if nr else 0
    r=0
    for c in range(nc):
        piv=next((i for i in range(r,nr) if A[i][c]&1),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(nr):
            if i!=r and A[i][c]&1:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1
        if r==nr: break
    return r

def subsets(m, max_size=None):
    out=[]
    top=m if max_size is None else max_size
    for s in range(1,top+1):
        out += list(combinations(range(m),s))
    return out

def skeleton(m,r):
    """r-skeleton of the (m-1)-simplex, nonempty faces only."""
    return set(subsets(m,r+1))

def by_dim(K):
    d={}
    for s in K:
        d.setdefault(len(s)-1,[]).append(s)
    for k in d: d[k]=sorted(d[k])
    return d

def boundary_matrix(K,k):
    bd=by_dim(K)
    src=bd.get(k,[]); tgt=bd.get(k-1,[])
    if k<=0: return []
    idx={s:i for i,s in enumerate(tgt)}
    M=[[0]*len(src) for _ in tgt]
    for j,s in enumerate(src):
        for a in range(len(s)):
            f=s[:a]+s[a+1:]
            M[idx[f]][j]^=1
    return M

def betti(K):
    bd=by_dim(K)
    if not bd: return {}
    maxd=max(bd)
    ranks={k:rank_mod2(boundary_matrix(K,k)) for k in range(1,maxd+1)}
    return {k:len(bd.get(k,[]))-ranks.get(k,0)-ranks.get(k+1,0) for k in range(maxd+1)}

def relative_betti(L,K):
    """H_*(L,K), assuming K subset L."""
    bL=by_dim(L); bK=by_dim(K)
    maxd=max(bL) if bL else -1
    rb={k:[s for s in bL.get(k,[]) if s not in set(bK.get(k,[]))] for k in range(maxd+1)}
    ranks={}
    for k in range(1,maxd+1):
        src=rb.get(k,[]); tgt=rb.get(k-1,[]); idx={s:i for i,s in enumerate(tgt)}
        M=[[0]*len(src) for _ in tgt]
        for j,s in enumerate(src):
            for a in range(len(s)):
                f=s[:a]+s[a+1:]
                if f in idx: M[idx[f]][j]^=1
        ranks[k]=rank_mod2(M)
    return {k:len(rb.get(k,[]))-ranks.get(k,0)-ranks.get(k+1,0) for k in range(maxd+1)}

def gf2_rank_vectors(vectors):
    if not vectors: return 0
    # vectors as rows
    A=[list(v) for v in vectors]
    return rank_mod2(A)

def xor(a,b): return tuple(x^y for x,y in zip(a,b))

def exact_layer(m,k):
    p=(1,)*m
    states=[]
    for S in combinations(range(m),k):
        x=list(p)
        for i in S: x[i]^=1
        states.append(tuple(x))
    return states

def main():
    report={"affine_unfolding_simplex":{},"layers":{},"skeleton_filtration":{}}
    for m in range(2,9):
        p=(1,)*m
        kids=exact_layer(m,1)
        differences=[xor(p,k) for k in kids]
        report["affine_unfolding_simplex"][str(m)]={
            "parent":p,"children":kids,
            "difference_rank_over_F2":gf2_rank_vectors(differences),
            "expected_rank":m,
            "affinely_independent":gf2_rank_vectors(differences)==m,
        }
        report["layers"][str(m)]={}
        for k in range(m+1):
            L=exact_layer(m,k)
            report["layers"][str(m)][str(k)]={
                "count":len(L),"expected_binomial":comb(m,k),
                "constant_weight":sorted(set(sum(x) for x in L)),
                "expected_weight":m-k,
            }
        stages={}
        for r in range(0,m):
            K=skeleton(m,r)
            b=betti(K)
            expected_top = 0 if r==m-1 else comb(m-1,r+1)
            stages[str(r)]={
                "betti":b,
                "expected_reduced_top_rank":expected_top,
            }
            if r>=1:
                Kprev=skeleton(m,r-1)
                rel=relative_betti(K,Kprev)
                stages[str(r)]["relative_from_previous"]=rel
                stages[str(r)]["expected_relative_rank_in_degree_r"]=comb(m,r+1)
        report["skeleton_filtration"][str(m)]=stages

    # Attached-note 3-variable point set: G=111, D=110, E=101, F=011.
    G=(1,1,1); D=(1,1,0); E=(1,0,1); F=(0,1,1)
    report["logical_complexes_note_check"]={
        "points":{"G":G,"D":D,"E":E,"F":F},
        "differences_from_G":{"D":xor(G,D),"E":xor(G,E),"F":xor(G,F)},
        "affine_rank":gf2_rank_vectors([xor(G,D),xor(G,E),xor(G,F)]),
        "forms_tetrahedron_affinely":gf2_rank_vectors([xor(G,D),xor(G,E),xor(G,F)])==3,
        "D_xor_E":xor(D,E),
        "hamming_distance_D_E":sum(xor(D,E)),
        "warning":"XOR is a difference vector in F2^m; its Hamming weight is the Hamming distance. Chain addition is a separate operation on formal simplices."
    }

    out=HERE/"verification_results.json"
    out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(f"Wrote {out}")
    # Assertions for formulas used in the draft.
    for m,data in report["affine_unfolding_simplex"].items():
        assert data["affinely_independent"]
    for m,stages in report["skeleton_filtration"].items():
        mi=int(m)
        for r,s in stages.items():
            ri=int(r)
            if ri<mi-1:
                # reduced top rank = ordinary beta in positive degree; for r=0, beta0-1.
                if ri==0:
                    got=s["betti"].get(0,0)-1
                else:
                    got=s["betti"].get(ri,0)
                assert got==s["expected_reduced_top_rank"], (m,r,got,s)
            if ri>=1:
                rel=s["relative_from_previous"]
                assert rel.get(ri,0)==s["expected_relative_rank_in_degree_r"], (m,r,rel)
                assert all(v==0 for q,v in rel.items() if int(q)!=ri), (m,r,rel)
    print("All verification assertions passed.")

if __name__=="__main__":
    main()
