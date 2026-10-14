#!/usr/bin/env python3
"""Exact finite computations for the Gluing Concepts audit.

Only Python stdlib is used. Complexes are finite abstract simplicial complexes
represented as frozensets of frozenset vertices, always including the empty face.
"""
from __future__ import annotations
from itertools import combinations
from collections import Counter, defaultdict
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)


def powerset(iterable):
    xs = tuple(iterable)
    for r in range(len(xs)+1):
        for c in combinations(xs, r):
            yield frozenset(c)


def closure_from_facets(facets):
    out = {frozenset()}
    for f in facets:
        f = frozenset(f)
        out.update(powerset(f))
    return frozenset(out)


def vertices(K):
    return frozenset().union(*K) if K else frozenset()


def facets(K):
    fs=[]
    for s in K:
        if s and not any(s < t for t in K):
            fs.append(s)
    return tuple(sorted(fs, key=lambda x:(len(x), tuple(sorted(map(str,x))))))


def induced(K, A):
    A=frozenset(A)
    return frozenset(s for s in K if s <= A)


def union(K,L):
    return frozenset(set(K)|set(L))


def intersection(K,L):
    return frozenset(set(K)&set(L))


def join(K,L):
    if vertices(K) & vertices(L):
        raise ValueError("join expects disjoint vertex sets")
    return frozenset(a|b for a in K for b in L)


def minimal_nonfaces(K, V=None):
    if V is None: V=vertices(K)
    V=tuple(sorted(V, key=str))
    out=[]
    for s in powerset(V):
        if not s or s in K: continue
        if all((s-{v}) in K for v in s):
            out.append(s)
    return tuple(sorted(out, key=lambda x:(len(x), tuple(sorted(map(str,x))))))


def gf2_rank(rows):
    rows=[int(r) for r in rows if r]
    rank=0
    while rows:
        pivot=max(rows)
        rows.remove(pivot)
        bit=1 << (pivot.bit_length()-1)
        new=[]
        for r in rows:
            new.append(r ^ pivot if (r & bit) else r)
        rows=[r for r in new if r]
        rank += 1
    return rank


def boundary_rank(K,k):
    cols=sorted([s for s in K if len(s)==k+1], key=lambda x:tuple(sorted(map(str,x))))
    rows=sorted([s for s in K if len(s)==k], key=lambda x:tuple(sorted(map(str,x))))
    if k<=0 or not cols or not rows: return 0
    ridx={s:i for i,s in enumerate(rows)}
    bitrows=[0 for _ in rows]
    for j,s in enumerate(cols):
        for v in s:
            f=s-{v}
            bitrows[ridx[f]] |= 1<<j
    return gf2_rank(bitrows)


def betti(K):
    maxdim=max((len(s)-1 for s in K if s), default=-1)
    dims=[sum(1 for s in K if len(s)==k+1) for k in range(maxdim+1)]
    dr=[boundary_rank(K,k) for k in range(maxdim+1)]
    # d_{maxdim+1} rank is zero
    return [dims[k]-dr[k]-(dr[k+1] if k+1<len(dr) else 0) for k in range(maxdim+1)]


def euler(K):
    return sum(((-1)**(len(s)-1)) for s in K if s)


def interaction_components(K):
    V=sorted(vertices(K), key=str)
    parent={v:v for v in V}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def un(a,b):
        a,b=find(a),find(b)
        if a!=b: parent[b]=a
    for nf in minimal_nonfaces(K,V):
        nf=list(nf)
        for x in nf[1:]: un(nf[0],x)
    comps=defaultdict(set)
    for v in V: comps[find(v)].add(v)
    return tuple(sorted((frozenset(c) for c in comps.values()), key=lambda c:tuple(sorted(map(str,c)))))


def finest_join_reconstruction(K):
    comps=interaction_components(K)
    if not comps:
        return frozenset({frozenset()})
    out=induced(K,comps[0])
    for C in comps[1:]:
        out=join(out,induced(K,C))
    return out


def bipartitions(V):
    V=tuple(sorted(V,key=str))
    if len(V)<2: return
    first=V[0]
    rest=V[1:]
    # fix first in A to quotient factor swapping
    for mask in range(1<<(len(rest))):
        A={first}
        for i,x in enumerate(rest):
            if mask&(1<<i): A.add(x)
        B=set(V)-A
        if B:
            yield frozenset(A),frozenset(B)


def join_factorizations(K):
    out=[]
    for A,B in bipartitions(vertices(K)) or []:
        if join(induced(K,A),induced(K,B)) == K:
            out.append((A,B))
    return out


def fmt_set(s):
    if not s: return "{}"
    return "{"+",".join(sorted(map(str,s)))+"}"


def complex_record(name,K):
    return {
        "name":name,
        "vertices": sorted(map(str,vertices(K))),
        "facets": [sorted(map(str,s)) for s in facets(K)],
        "f_vector": [sum(1 for s in K if len(s)==k+1) for k in range(max((len(s)-1 for s in K if s),default=-1)+1)],
        "betti_F2": betti(K),
        "euler_characteristic": euler(K),
        "minimal_nonfaces": [sorted(map(str,s)) for s in minimal_nonfaces(K)],
        "join_components": [sorted(map(str,s)) for s in interaction_components(K)],
        "join_factorization_count_unordered_bipartitions": len(join_factorizations(K)),
        "finest_join_reconstruction_exact": finest_join_reconstruction(K)==K,
    }


def all_downsets(n):
    # All downsets of Boolean lattice on [n], including empty downset.
    ds=[frozenset(), frozenset({0})]  # n=0: masks universe is {0=empty face}
    if n==0: return ds
    for k in range(1,n+1):
        prev=ds
        high=1<<(k-1)
        ds=[]
        for D0 in prev:
            for D1 in prev:
                if D1 <= D0:
                    ds.append(frozenset(set(D0)|{m|high for m in D1}))
    return ds


def mask_to_complex(D,n):
    K=[]
    for m in D:
        K.append(frozenset(i for i in range(n) if m&(1<<i)))
    return frozenset(K)


def enumerate_counts(max_n=5):
    rows=[]
    validations=[]
    for n in range(1,max_n+1):
        ds=all_downsets(n)
        actual=[]
        singles={1<<i for i in range(n)}
        for D in ds:
            if 0 in D and singles <= set(D):
                actual.append(mask_to_complex(D,n))
        factors=Counter(len(interaction_components(K)) for K in actual)
        reconstruction_failures=0
        partition_checks=0
        partition_criterion_failures=0
        for K in actual:
            if finest_join_reconstruction(K) != K:
                reconstruction_failures += 1
            for A,B in bipartitions(vertices(K)) or []:
                partition_checks += 1
                lhs,rhs=partition_minimal_nonface_criterion(K,A,B)
                if lhs != rhs:
                    partition_criterion_failures += 1
        rows.append({
            "n_vertices":n,
            "all_downsets_Dedekind":len(ds),
            "complexes_using_all_vertices":len(actual),
            "join_decomposable_nontrivially":sum(c for f,c in factors.items() if f>=2),
            "join_indecomposable":factors.get(1,0),
            "factor_count_distribution":dict(sorted(factors.items())),
            "finest_join_reconstruction_failures":reconstruction_failures,
            "partition_criterion_checks":partition_checks,
            "partition_criterion_failures":partition_criterion_failures,
        })
    return rows


def flag_completion(K):
    V=vertices(K)
    edges={s for s in K if len(s)==2}
    return frozenset(s for s in powerset(V) if len(s)<=1 or all(frozenset(e) in edges for e in combinations(s,2)))

def partition_minimal_nonface_criterion(K,A,B):
    lhs = join(induced(K,A), induced(K,B)) == K
    rhs = all(nf <= A or nf <= B for nf in minimal_nonfaces(K))
    return lhs, rhs

def nerve(pieces):
    names=list(pieces)
    facets_nerve=[]
    # all nonempty subsets with nonempty total intersection of geometric face sets as vertex sets
    for r in range(1,len(names)+1):
        for comb in combinations(names,r):
            inter=set(vertices(pieces[comb[0]]))
            for nm in comb[1:]: inter &= set(vertices(pieces[nm]))
            if inter: facets_nerve.append(frozenset(comb))
    # maximal subsets
    maxf=[s for s in facets_nerve if not any(s<t for t in facets_nerve)]
    return closure_from_facets(maxf)



def set_partitions(items):
    """Generate set partitions of a finite iterable as tuples of frozenset blocks."""
    items=tuple(items)
    if not items:
        yield tuple()
        return
    first=items[0]
    for part in set_partitions(items[1:]):
        # first starts a new block
        yield (frozenset({first}),)+part
        # or joins an existing block; canonical insertion avoids duplicates
        for i in range(len(part)):
            new=list(part)
            new[i]=frozenset(set(new[i])|{first})
            yield tuple(new)


def canonical_partition(part):
    return tuple(sorted((frozenset(b) for b in part), key=lambda b: tuple(sorted(map(str,b)))))


def relation_factors_over_partition(rows, attrs, part):
    """Cartesian factorization of a finite relation across a declared partition."""
    attrs=tuple(attrs)
    pos={a:i for i,a in enumerate(attrs)}
    R={tuple(r) for r in rows}
    if not R:
        return False  # avoid empty-relation convention issues in this audit
    sizes=[]
    for block in part:
        idx=[pos[a] for a in block]
        proj={tuple(r[i] for i in idx) for r in R}
        sizes.append(len(proj))
    prod=1
    for n in sizes: prod*=n
    return len(R)==prod


def finest_relation_partition(rows, attrs):
    """Brute-force exact prime Cartesian partition for small finite relations."""
    valid=[]
    seen=set()
    for part in set_partitions(tuple(attrs)):
        c=canonical_partition(part)
        key=tuple(tuple(sorted(map(str,b))) for b in c)
        if key in seen: continue
        seen.add(key)
        if relation_factors_over_partition(rows, attrs, c):
            valid.append(c)
    if not valid: return None, []
    m=max(len(p) for p in valid)
    finest=[p for p in valid if len(p)==m]
    return (finest[0] if len(finest)==1 else None), finest


def least_common_coarsening(*parts):
    """Finest partition that is a coarsening of every supplied partition."""
    universe=set().union(*(set().union(*p) if p else set() for p in parts))
    parent={x:x for x in universe}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def unite(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for part in parts:
        for block in part:
            block=list(block)
            for x in block[1:]: unite(block[0],x)
    comps=defaultdict(set)
    for x in universe: comps[find(x)].add(x)
    return canonical_partition(comps.values())

def relation_factorizes(rows, Aidx, Bidx):
    R={tuple(r) for r in rows}
    PA={tuple(r[i] for i in Aidx) for r in R}
    PB={tuple(r[i] for i in Bidx) for r in R}
    prod={a+b for a in PA for b in PB}
    # above assumes A then B order matches original only for equality of encoded tuples; use paired representation instead
    pairR={(tuple(r[i] for i in Aidx),tuple(r[i] for i in Bidx)) for r in R}
    return pairR == {(a,b) for a in PA for b in PB}, len(R), len(PA)*len(PB)


def main():
    # Examples
    A1=closure_from_facets([{"a","b"}]); A2=closure_from_facets([{"b","c"}]); A=union(A1,A2)
    B1=closure_from_facets([{"a","b","c"}]); B2=closure_from_facets([{"b","c","d"}]); B=union(B1,B2)
    facesC=[{"a","b","c"},{"a","b","d"},{"a","c","d"},{"b","c","d"}]
    C_boundary=closure_from_facets(facesC)
    C_filled=closure_from_facets([{"a","b","c","d"}])
    C_horn=closure_from_facets(facesC[:3])
    C_one_skeleton=closure_from_facets([{"a","b"},{"a","c"},{"a","d"},{"b","c"},{"b","d"},{"c","d"}])
    E=join(closure_from_facets([{"a0"},{"a1"}]), closure_from_facets([{"b0"},{"b1"}]))
    # F as complex determined by minimal nonfaces; construct from all subsets avoiding forbidden edges
    VF={"a0","a1","b0","b1"}; forbidden=[{"a0","a1"},{"a1","b0"},{"b0","b1"}]
    F=frozenset(s for s in powerset(VF) if not any(frozenset(q)<=s for q in forbidden))
    G=closure_from_facets([{"a","b","c"}])
    examples={
        "A_two_edges_glued_at_vertex":A,
        "B_two_filled_triangles_glued_along_edge":B,
        "C_tetrahedral_boundary_from_four_faces":C_boundary,
        "C_three_face_horn":C_horn,
        "C_K4_one_skeleton":C_one_skeleton,
        "C_filled_tetrahedron":C_filled,
        "E_clean_join_C4":E,
        "F_join_irreducible_four_vertex_interaction":F,
        "G_filled_triangle_nonunique_coarse_join":G,
    }
    records=[complex_record(n,K) for n,K in examples.items()]
    with open(os.path.join(DATA,"finite_examples.json"),"w",encoding="utf8") as f: json.dump(records,f,indent=2)
    with open(os.path.join(DATA,"finite_examples.csv"),"w",newline="",encoding="utf8") as f:
        w=csv.writer(f); w.writerow(["name","vertices","facets","f_vector","betti_F2","euler","minimal_nonfaces","join_components","join_bipartitions"])
        for r in records:
            w.writerow([r["name"],r["vertices"],r["facets"],r["f_vector"],r["betti_F2"],r["euler_characteristic"],r["minimal_nonfaces"],r["join_components"],r["join_factorization_count_unordered_bipartitions"]])
    counts=enumerate_counts(5)
    with open(os.path.join(DATA,"enumeration_counts.json"),"w",encoding="utf8") as f: json.dump(counts,f,indent=2)
    with open(os.path.join(DATA,"enumeration_counts.csv"),"w",newline="",encoding="utf8") as f:
        w=csv.writer(f); w.writerow(["n_vertices","all_downsets_Dedekind","complexes_using_all_vertices","join_decomposable_nontrivially","join_indecomposable","factor_count_distribution","finest_join_reconstruction_failures","partition_criterion_checks","partition_criterion_failures"])
        for r in counts: w.writerow([r[k] for k in ["n_vertices","all_downsets_Dedekind","complexes_using_all_vertices","join_decomposable_nontrivially","join_indecomposable","factor_count_distribution","finest_join_reconstruction_failures","partition_criterion_checks","partition_criterion_failures"]])
    # Specific diagnostic data
    diag={
        "example_A_intersection_facets":[sorted(x) for x in facets(intersection(A1,A2))],
        "example_B_intersection_facets":[sorted(x) for x in facets(intersection(B1,B2))],
        "example_C_boundaries_differ": C_boundary != C_filled,
        "example_C_boundary_missing_only_top_simplex": sorted([sorted(x) for x in (C_filled-C_boundary)], key=lambda x:(len(x),x)),
        "example_C_boundary_betti_F2":betti(C_boundary),
        "example_C_filled_betti_F2":betti(C_filled),
        "example_C_three_face_horn_betti_F2":betti(C_horn),
        "example_C_flag_completion_of_K4_is_filled_tetrahedron":flag_completion(C_one_skeleton)==C_filled,
        "example_C_union_of_four_faces_is_only_boundary":union(union(closure_from_facets([facesC[0]]),closure_from_facets([facesC[1]])),union(closure_from_facets([facesC[2]]),closure_from_facets([facesC[3]])))==C_boundary,
        "example_G_join_bipartitions":[[sorted(A),sorted(B)] for A,B in join_factorizations(G)],
        "E_reconstruction": finest_join_reconstruction(E)==E,
        "F_reconstruction": finest_join_reconstruction(F)==F,
    }
    # Two-layer structured factorization demo.  Each layer factorizes, but across
    # crossing prime partitions, so the finest simultaneous factorization is trivial.
    attrs=("a0","a1","b0","b1")
    # Semantic relation: equality on (a0,b0) independently of equality on (a1,b1).
    semantic_rows=[]
    for x in (0,1):
        for y in (0,1):
            semantic_rows.append((x,y,x,y))
    PK=canonical_partition(interaction_components(E))
    PR, PR_candidates=finest_relation_partition(semantic_rows,attrs)
    PS=least_common_coarsening(PK,PR) if PR is not None else None
    structured={
        "attributes":list(attrs),
        "simplicial_finest_partition":[sorted(b) for b in PK],
        "semantic_relation_rows":semantic_rows,
        "semantic_finest_partition":[sorted(b) for b in PR] if PR else None,
        "semantic_finest_partition_unique":PR is not None,
        "simultaneous_finest_partition_least_common_coarsening":[sorted(b) for b in PS] if PS else None,
        "nontrivial_simultaneous_factorization": bool(PS and len(PS)>1),
    }
    with open(os.path.join(DATA,"structured_factorization_demo.json"),"w",encoding="utf8") as f: json.dump(structured,f,indent=2)
    with open(os.path.join(DATA,"diagnostics.json"),"w",encoding="utf8") as f: json.dump(diag,f,indent=2)
    print(json.dumps({"counts":counts,"diagnostics":diag,"structured":structured,"records":records},indent=2))

if __name__=="__main__": main()
