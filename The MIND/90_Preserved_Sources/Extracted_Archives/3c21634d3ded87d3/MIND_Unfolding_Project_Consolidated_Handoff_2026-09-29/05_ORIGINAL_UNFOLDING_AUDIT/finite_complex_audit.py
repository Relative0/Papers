#!/usr/bin/env python3
"""Exact finite homology, mapping-cone, gluing and symmetry examples.

Coefficients: F_2 throughout.  No third-party dependencies.
"""
from itertools import combinations, permutations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def canonical(simplex):
    return tuple(sorted(simplex))


def closure(max_simplices):
    S=set()
    for sig in max_simplices:
        sig=canonical(sig)
        for r in range(1,len(sig)+1):
            for face in combinations(sig,r):
                S.add(face)
    return S


def simplices_by_dim(K):
    out={}
    for s in K:
        out.setdefault(len(s)-1,[]).append(s)
    for k in out:
        out[k]=sorted(out[k])
    return out


def rank_mod2(M):
    if not M:
        return 0
    A=[[(x&1) for x in row] for row in M]
    nrow=len(A); ncol=len(A[0]) if nrow else 0
    r=0
    for c in range(ncol):
        piv=None
        for i in range(r,nrow):
            if A[i][c]:
                piv=i; break
        if piv is None:
            continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(nrow):
            if i!=r and A[i][c]:
                A[i]=[a^b for a,b in zip(A[i],A[r])]
        r+=1
        if r==nrow: break
    return r


def boundary_matrix(K, k, bases=None):
    bd=simplices_by_dim(K)
    if bases is None:
        src=bd.get(k,[]); tgt=bd.get(k-1,[])
    else:
        src=bases.get(k,[]); tgt=bases.get(k-1,[])
    if k<=0:
        return tgt,src,[]
    ridx={s:i for i,s in enumerate(tgt)}
    M=[[0]*len(src) for _ in tgt]
    for j,s in enumerate(src):
        for face in combinations(s,len(s)-1):
            face=canonical(face)
            if face in ridx:
                M[ridx[face]][j]^=1
    return tgt,src,M


def betti(K):
    bd=simplices_by_dim(K)
    maxd=max(bd) if bd else -1
    ranks={}
    dims={k:len(bd.get(k,[])) for k in range(maxd+1)}
    for k in range(1,maxd+1):
        _,_,M=boundary_matrix(K,k)
        ranks[k]=rank_mod2(M)
    b={}
    for k in range(maxd+1):
        r_k=ranks.get(k,0)
        r_k1=ranks.get(k+1,0)
        b[k]=dims[k]-r_k-r_k1
    return b,ranks,dims


def inclusion_chain_map(K,L):
    bK=simplices_by_dim(K); bL=simplices_by_dim(L)
    maps={}
    for k,src in bK.items():
        tgt=bL.get(k,[]); idx={s:i for i,s in enumerate(tgt)}
        M=[[0]*len(src) for _ in tgt]
        for j,s in enumerate(src):
            M[idx[s]][j]=1
        maps[k]=(src,tgt,M)
    return maps


def matmul_mod2(A,B):
    if not A or not B:
        # Need dimensions externally for corner cases; examples all nonempty when used.
        return []
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%2
             for j in range(len(B[0]))] for i in range(len(A))]


def chain_map_check(K,L):
    maps=inclusion_chain_map(K,L)
    maxd=max(simplices_by_dim(K))
    checks=[]
    for k in range(1,maxd+1):
        _,_,dK=boundary_matrix(K,k)
        _,_,dL=boundary_matrix(L,k)
        Uk=maps[k][2]; Ukm1=maps[k-1][2]
        lhs=matmul_mod2(dL,Uk)
        rhs=matmul_mod2(Ukm1,dK)
        checks.append({"degree":k,"dL_U":lhs,"U_dK":rhs,"equal":lhs==rhs})
    return checks


def relative_complex(L,K):
    bL=simplices_by_dim(L); bK=simplices_by_dim(K)
    maxd=max(bL) if bL else -1
    bases={k:[s for s in bL.get(k,[]) if s not in set(bK.get(k,[]))]
           for k in range(maxd+1)}
    boundaries={}
    ranks={}
    for k in range(1,maxd+1):
        tgt=bases.get(k-1,[]); src=bases.get(k,[])
        ridx={s:i for i,s in enumerate(tgt)}
        M=[[0]*len(src) for _ in tgt]
        for j,s in enumerate(src):
            for face in combinations(s,len(s)-1):
                face=canonical(face)
                if face in ridx:
                    M[ridx[face]][j]^=1
        boundaries[k]=M
        ranks[k]=rank_mod2(M)
    bet={}
    for k in range(maxd+1):
        bet[k]=len(bases.get(k,[]))-ranks.get(k,0)-ranks.get(k+1,0)
    return bases,boundaries,bet


def cone_homology_of_inclusion(K,L):
    """Compute homology dimensions of Cone(C(K)->C(L)) over F2 directly."""
    bK=simplices_by_dim(K); bL=simplices_by_dim(L)
    maps=inclusion_chain_map(K,L)
    maxd=max(max(bK),max(bL))+1
    # Cone_n = L_n plus K_{n-1}.
    cone_dim={n:len(bL.get(n,[]))+len(bK.get(n-1,[])) for n in range(maxd+1)}
    ranks={}
    matrices={}
    for n in range(1,maxd+1):
        Ln=bL.get(n,[]); Knm1=bK.get(n-1,[])
        Lnm1=bL.get(n-1,[]); Knm2=bK.get(n-2,[])
        # d_cone(y,x) = (d_L y + U x, d_K x); signs vanish over F2.
        _,_,dL=boundary_matrix(L,n)
        if n-1 in maps:
            U=maps[n-1][2]
        else:
            U=[[0]*len(Knm1) for _ in Lnm1]
        if n-1>=1:
            _,_,dK=boundary_matrix(K,n-1)
        else:
            dK=[]
        rows=len(Lnm1)+len(Knm2); cols=len(Ln)+len(Knm1)
        M=[[0]*cols for _ in range(rows)]
        # dL block
        for i,row in enumerate(dL):
            for j,x in enumerate(row): M[i][j]=x
        # U block
        for i,row in enumerate(U):
            for j,x in enumerate(row): M[i][len(Ln)+j]=x
        # dK lower-right block
        if dK:
            for i,row in enumerate(dK):
                for j,x in enumerate(row): M[len(Lnm1)+i][len(Ln)+j]=x
        matrices[n]=M
        ranks[n]=rank_mod2(M)
    bet={n:cone_dim[n]-ranks.get(n,0)-ranks.get(n+1,0) for n in range(maxd+1)}
    return cone_dim,matrices,bet


def adjacency_from_edges(vertices, edges):
    E={frozenset(e) for e in edges}
    return {(u,v):(u==v or frozenset((u,v)) in E) for u in vertices for v in vertices}


def graph_automorphisms(vertices,edges):
    E={frozenset(e) for e in edges}
    autos=[]
    V=list(vertices)
    for p in permutations(V):
        f=dict(zip(V,p))
        mapped={frozenset((f[u],f[v])) for u,v in edges}
        if mapped==E:
            autos.append(f)
    return autos


def custom_boundary_with_order(K,k,src,tgt):
    ridx={s:i for i,s in enumerate(tgt)}
    M=[[0]*len(src) for _ in tgt]
    for j,s in enumerate(src):
        for face in combinations(s,len(s)-1):
            face=canonical(face)
            if face in ridx: M[ridx[face]][j]^=1
    return M


def main():
    K0=closure([("a","b"),("b","c")])
    K1=closure([("a","b"),("b","c"),("c","d"),("d","a")])
    K2=closure([("a","b","c"),("a","c","d")])

    Ks={"K0":K0,"K1":K1,"K2":K2}
    summary={}
    for name,K in Ks.items():
        b,r,d=betti(K)
        summary[name]={
            "simplices_by_dim":{str(k):[list(s) for s in v] for k,v in simplices_by_dim(K).items()},
            "betti":b,"boundary_ranks":r,"chain_dimensions":d
        }

    checks01=chain_map_check(K0,K1)
    checks12=chain_map_check(K1,K2)
    bases10,bounds10,bet10=relative_complex(K1,K0)
    bases21,bounds21,bet21=relative_complex(K2,K1)
    _,_,cone01=cone_homology_of_inclusion(K0,K1)
    _,_,cone12=cone_homology_of_inclusion(K1,K2)

    # Fixed display orders used in FINITE_EXAMPLES.md
    V0=[("a",),("b",),("c",)]
    E0=[("a","b"),("b","c")]
    V1=[("a",),("b",),("c",),("d",)]
    E1=[("a","b"),("b","c"),("c","d"),("a","d")]
    E2=[("a","b"),("b","c"),("c","d"),("a","d"),("a","c")]
    T2=[("a","b","c"),("a","c","d")]
    display={
        "K0_d1":custom_boundary_with_order(K0,1,E0,V0),
        "K1_d1":custom_boundary_with_order(K1,1,E1,V1),
        "K2_d1":custom_boundary_with_order(K2,1,E2,V1),
        "K2_d2":custom_boundary_with_order(K2,2,T2,E2),
    }

    # Symmetry counterexamples.
    triangle_V=["a","b","c"]
    triangle_E=[("a","b"),("b","c"),("c","a")]
    # One cycle plus nonisomorphic decorations at a,b,c -> trivial automorphism group.
    asym_V=["a","b","c","p","q","r"]
    asym_E=[("a","b"),("b","c"),("c","a"),("a","p"),("b","q"),("q","r")]
    aut_triangle=graph_automorphisms(triangle_V,triangle_E)
    aut_asym=graph_automorphisms(asym_V,asym_E)
    asym_K=closure(asym_E)
    asym_betti=betti(asym_K)[0]
    filled_triangle=closure([("a","b","c")])
    filled_aut=graph_automorphisms(triangle_V,triangle_E) # same vertex-edge symmetries extend to filled simplex
    filled_betti=betti(filled_triangle)[0]

    result={
        "filtration":summary,
        "chain_map_checks":{"K0_to_K1":checks01,"K1_to_K2":checks12},
        "relative_homology":{
            "K1_K0":{"bases":{str(k):[list(s) for s in v] for k,v in bases10.items()},"boundary_matrices":bounds10,"betti":bet10},
            "K2_K1":{"bases":{str(k):[list(s) for s in v] for k,v in bases21.items()},"boundary_matrices":bounds21,"betti":bet21}
        },
        "mapping_cone_betti":{"Cone_K0_to_K1":cone01,"Cone_K1_to_K2":cone12},
        "display_boundary_matrices":display,
        "symmetry_counterexamples":{
            "3_cycle_aut_group_size":len(aut_triangle),
            "filled_triangle_aut_group_size":len(filled_aut),
            "filled_triangle_betti":filled_betti,
            "asymmetric_unicyclic_graph_aut_group_size":len(aut_asym),
            "asymmetric_unicyclic_graph_betti":asym_betti,
            "asymmetric_graph_edges":[list(e) for e in asym_E],
        },
        "gluing":{
            "K2_exact_union": "triangle abc union triangle acd along edge ac",
            "K1_edge_cover_nerve": "four-cycle",
        }
    }
    out=HERE/"finite_complex_results.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")

    print("Betti numbers:")
    for n in ["K0","K1","K2"]: print(n, summary[n]["betti"])
    print("Chain maps verified:", all(c["equal"] for c in checks01+checks12))
    print("Relative H(K1,K0):",bet10," Cone:",cone01)
    print("Relative H(K2,K1):",bet21," Cone:",cone12)
    print("Aut sizes: cycle=",len(aut_triangle)," filled triangle=",len(filled_aut)," asymmetric unicyclic=",len(aut_asym))
    print("Asymmetric unicyclic Betti:",asym_betti)
    print(f"Wrote {out}")

if __name__=="__main__":
    main()
