#!/usr/bin/env python3
"""Exact finite regressions for Paper U v0.2 (Python >=3.10, standard library).

Run: python scripts/verify_paper_u.py --out evidence
The finite computations are regression evidence, not proofs of infinite claims.
No random seeds, network access, or third-party dependencies are used.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools as it
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable

Word = tuple[int, ...]
Perm = tuple[int, ...]
Frontier = frozenset[Word]

def words(m: int, depth: int) -> list[Word]:
    return list(it.product(range(m), repeat=depth))

def pref(s: Word, x: Word) -> bool:
    return x[:len(s)] == s

def lcp(x: Word, y: Word) -> int:
    return next((i for i, (a, b) in enumerate(zip(x, y)) if a != b), min(len(x), len(y)))

def dist(x: Word, y: Word, m: int = 2) -> Fraction:
    return Fraction(0) if x == y else Fraction(1, m**lcp(x, y))

def internal(f: Frontier) -> frozenset[Word]:
    return frozenset(s[:k] for s in f for k in range(len(s)))

def from_internal(I: Iterable[Word], m: int) -> Frontier:
    I = frozenset(I)
    if not I:
        return frozenset({()})
    return frozenset(v+(a,) for v in I for a in range(m) if v+(a,) not in I)

@lru_cache(None)
def frontiers(m: int, depth: int) -> tuple[Frontier, ...]:
    if depth == 0:
        return (frozenset({()}),)
    ans = [frozenset({()})]
    for fs in it.product(frontiers(m, depth-1), repeat=m):
        ans.append(frozenset((a,)+s for a, f in enumerate(fs) for s in f))
    return tuple(ans)

@lru_cache(None)
def automorphisms(m: int, depth: int) -> tuple[Perm, ...]:
    if depth == 0:
        return ((0,),)
    size = m**(depth-1)
    sub = automorphisms(m, depth-1)
    return tuple(tuple(sigma[a]*size + ps[a][j] for a in range(m) for j in range(size))
                 for sigma in it.permutations(range(m)) for ps in it.product(sub, repeat=m))

def compose(a: Perm, b: Perm) -> Perm:
    """a after b."""
    return tuple(a[b[i]] for i in range(len(a)))

def inverse(a: Perm) -> Perm:
    ans = [0]*len(a)
    for i, j in enumerate(a): ans[j] = i
    return tuple(ans)

def code(f: Frontier, x: Word) -> Word:
    matches = [s for s in f if pref(s, x)]
    assert len(matches) == 1
    return matches[0]

def generators(m: int, depth: int, f: Frontier) -> list[Perm]:
    leaves = words(m, depth)
    idx = {x:i for i,x in enumerate(leaves)}
    gs = []
    for k in range(depth):
        for v in words(m, k):
            if not any(pref(s,v) for s in f): continue
            for a in range(m-1):
                p = []
                for x in leaves:
                    y = x
                    if pref(v,x) and x[k] in (a,a+1):
                        y = x[:k]+(2*a+1-x[k],)+x[k+1:]
                    p.append(idx[y])
                gs.append(tuple(p))
    return gs

def expected_normal(f: Frontier, finer: Frontier, m: int) -> bool:
    for s in f:
        tails = {v[len(s):] for v in finer if pref(s,v)}
        depths = {len(t) for t in tails}
        if len(depths) != 1: return False
        h = next(iter(depths))
        if tails != set(words(m,h)): return False
    return True

def entropy(ps: Iterable[Fraction]) -> float:
    return -sum(float(p)*math.log2(float(p)) for p in ps if p)

def group_study(m: int, depth: int, out: Path) -> dict:
    leaves = words(m,depth)
    fs = frontiers(m,depth)
    aut = automorphisms(m,depth)
    groups, gens = {}, {}
    orbit_checks = 0
    for f in fs:
        codes = [code(f,x) for x in leaves]
        gf = frozenset(g for g in aut if all(codes[g[i]]==codes[i] for i in range(len(leaves))))
        groups[f] = gf
        gens[f] = generators(m,depth,f)
        assert set(gens[f]) <= gf
        for i in range(len(leaves)):
            assert {g[i] for g in gf} == {j for j in range(len(leaves)) if codes[j]==codes[i]}
            orbit_checks += 1
        assert len(f) == 1+(m-1)*len(internal(f))
        assert sum(Fraction(1,m**len(s)) for s in f)==1
    rows = []
    conjugation_checks = 0
    normal_count = 0
    lattice_checks = 0
    for f in fs:
        for h in fs:
            meet = from_internal(internal(f)&internal(h),m)
            join = from_internal(internal(f)|internal(h),m)
            assert meet in groups and join in groups
            lattice_checks += 1
            if not internal(f) <= internal(h): continue
            gf, gh = groups[f], groups[h]
            assert gh <= gf
            splits = len(internal(h)-internal(f))
            assert len(gf) == len(gh)*math.factorial(m)**splits
            normal = True
            for g in gens[f]:
                gi = inverse(g)
                for a in gh:
                    conjugation_checks += 1
                    if compose(compose(g,a),gi) not in gh:
                        normal = False
                        break
                if not normal: break
            assert normal == expected_normal(f,h,m), (m,depth,f,h,normal)
            normal_count += normal
            rows.append({'coarse':' '.join(''.join(map(str,s)) or 'eps' for s in sorted(f)),
                         'fine':' '.join(''.join(map(str,s)) or 'eps' for s in sorted(h)),
                         'coarse_group_order':len(gf),'fine_group_order':len(gh),
                         'new_internal_nodes':splits,'index':len(gf)//len(gh),'normal':normal})
    with (out/f'frontier_groups_m{m}_d{depth}.csv').open('w',newline='') as fp:
        wr=csv.DictWriter(fp,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    # The least sample-separating frontier is checked against every frontier.
    sample_checks = 0
    if len(leaves)<=9:
        for mask in range(1<<len(leaves)):
            sample = [x for i,x in enumerate(leaves) if mask>>i&1]
            Istar = frozenset(v for k in range(depth) for v in words(m,k)
                             if sum(pref(v,x) for x in sample)>=2)
            fstar=from_internal(Istar,m)
            assert len({code(fstar,x) for x in sample})==len(sample)
            for f in fs:
                separates=len({code(f,x) for x in sample})==len(sample)
                assert separates == (Istar<=internal(f))
                sample_checks += 1
    return {'m':m,'depth':depth,'leaf_count':len(leaves),'automorphism_count':len(aut),
            'frontier_count':len(fs),'comparable_pairs_including_equality':len(rows),
            'normal_pairs':normal_count,'nonnormal_pairs':len(rows)-normal_count,
            'conjugation_membership_checks':conjugation_checks,
            'orbit_checks':orbit_checks,'lattice_pair_checks':lattice_checks,
            'sample_frontier_checks':sample_checks}

def main(out: Path) -> None:
    out.mkdir(parents=True,exist_ok=True)
    pts=words(2,4)
    triples=0
    for x,y,z in it.product(pts,repeat=3):
        assert dist(x,z)<=max(dist(x,y),dist(y,z));triples+=1
    pseudo_triples=0
    radius_checks=0
    for k in range(5):
        dk=lambda x,y: Fraction(0) if x[:k]==y[:k] else dist(x,y)
        for x,y,z in it.product(pts,repeat=3):
            assert dk(x,z)<=max(dk(x,y),dk(y,z));pseudo_triples+=1
        for x in pts:
            cell={y for y in pts if x[:k]==y[:k]}
            assert cell=={y for y in pts if dist(x,y)<=Fraction(1,2**k)}
            if k: assert cell=={y for y in pts if dist(x,y)<Fraction(1,2**(k-1))}
            radius_checks+=1
        for x,y in it.product(pts,repeat=2):
            assert 0<=dist(x,y)-dk(x,y)<=Fraction(1,2**k)
    for x,y in it.product(pts,repeat=2):
        a=sum(b*2**i for i,b in enumerate(x));b=sum(c*2**i for i,c in enumerate(y))
        n=abs(a-b);v=0
        if n:
            while n%2==0: v+=1;n//=2
            assert dist(x,y)==Fraction(1,2**v)
            k=next(k for k in range(1,5) if x[:k]!=y[:k])
            assert dist(x,y)==Fraction(1,2**(k-1))
        else: assert dist(x,y)==0
    # Disjoint-ball quotient and its ultrametric for every depth-4 binary frontier.
    frontier_triples=0
    for f in frontiers(2,4):
        cell={x:code(f,x) for x in pts}
        dp=lambda x,y: Fraction(0) if cell[x]==cell[y] else dist(x,y)
        for x,y,z in it.product(pts,repeat=3):
            assert dp(x,z)<=max(dp(x,y),dp(y,z));frontier_triples+=1
    # Three-point nonregular isometry obstruction.
    mat=((0,Fraction(1,2),1),(Fraction(1,2),0,1),(1,1,0))
    isoms=[g for g in it.permutations(range(3)) if all(mat[i][j]==mat[g[i]][g[j]] for i,j in it.product(range(3),repeat=2))]
    assert len(isoms)==2
    assert {g[0] for g in isoms}=={0,1} and {g[2] for g in isoms}=={2}
    # Arbitrary partitions cannot in general preserve all cross-cell distances.
    p2=words(2,2);labels={(0,0):0,(1,0):0,(0,1):1,(1,1):2}
    bad=lambda x,y:Fraction(0) if labels[x]==labels[y] else dist(x,y)
    x,y,z=(1,0),(0,0),(0,1)
    assert bad(x,z)>bad(x,y)+bad(y,z)
    # XOR / anchored XOR. C alone has the same orbits as <C,S>.
    states=list(it.product((0,1),repeat=2))
    C=lambda t:(1-t[0],1-t[1]);S=lambda t:(t[1],t[0])
    for t in states:
        orbit={t,C(t),S(t),C(S(t))}
        fiber={u for u in states if u[0]^u[1]==t[0]^t[1]}
        assert orbit==fiber=={t,C(t)}
        anchored=lambda u:(u[0],u[0]^u[1])
        assert anchored(anchored(t))==t
    # Entropy of every frontier for several exact distributions on depth-3 leaves.
    pts3=words(2,3)
    measures=[{x:Fraction(1,8) for x in pts3},
              {x:Fraction(i+1,36) for i,x in enumerate(pts3)},
              {x:Fraction(int(i==0),1) for i,x in enumerate(pts3)}]
    ent_checks=0
    for mu in measures:
        mass=lambda s:sum(mu[x] for x in pts3 if pref(s,x))
        for f in frontiers(2,3):
            hf=entropy(mass(s) for s in f)
            expanded=sum(float(mass(v))*entropy(mass(v+(a,))/mass(v) for a in range(2))
                         for v in internal(f) if mass(v))
            assert math.isclose(hf,expanded,rel_tol=1e-12,abs_tol=1e-12)
            ent_checks+=1
    balanced=frozenset(words(2,2));comb=frozenset({(0,0,0),(0,0,1),(0,1),(1,)})
    hb=entropy(Fraction(1,2**len(s)) for s in balanced)
    hc=entropy(Fraction(1,2**len(s)) for s in comb)
    assert hb==2 and hc==1.75 and len(internal(balanced))==len(internal(comb))==3
    # Total variation between Bernoulli parameter values is not ultrametric.
    p,q,r=Fraction(0),Fraction(1,2),Fraction(1)
    assert abs(p-r)>max(abs(p-q),abs(q-r))
    results={'status':'ALL CHECKS PASSED','scope':'Finite regression checks; infinite statements are proved in the manuscript.',
             'prefix_depth4':{'points':16,'ultrametric_triples':triples,'truncated_pseudometric_triples':pseudo_triples,
                              'radius_cell_checks':radius_checks,'p_adic_pairs':256,'frontiers_checked':677,
                              'adaptive_collapse_triples':frontier_triples,'ball_count':31},
             'group_studies':[group_study(2,3,out),group_study(3,2,out)],
             'entropy_identity_cases':ent_checks,
             'counterexamples':{'nonregular_three_point_isometry_group_order':2,
                                'nonnormal_binary_frontier':['00','01','1'],
                                'same_index_entropy':{'index':8,'balanced_bits':hb,'comb_bits':hc},
                                'arbitrary_partition_triangle_violation':{'left':'1','right':'1/2'},
                                'bernoulli_tv_ultrametric_violation':['1','1/2','1/2']},
             'xor_orbit_and_reconstruction_cases':4}
    (out/'verification_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('evidence'))
    args=parser.parse_args()
    main(args.out)
