"""Deterministic, bounded verification accompanying the revised Paper B.

Run from any directory: python /path/to/code/verify_guarded_dispatch.py --out DIR
The universal topology and degree bounds are proved in the manuscript, not by
these finite computations. SymPy is used only for exact symbolic algebra.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import platform
import sys
import time

import sympy as sp
from guarded_dispatch import dispatch, score_vector, TRUTH_TABLES


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def symbolic_checks() -> dict:
    a, b, u, v = sp.symbols('a b u v')
    scores = (a+b+a*b, a-b-a*b, -a+b-a*b, -a-b+a*b)
    hs = scores[1:]
    targets = (u+v+1, v-u-1, u-v-1, 1-u-v)
    for g, t in zip(scores, targets, strict=True):
        check(sp.cancel((g/(a*b)).subs({a:1/u,b:1/v})-t) == 0, 'reciprocal identity')
    for i, j, target in ((0,1,-2*a*b),(0,2,-2*b),(1,2,-2*a)):
        check(sp.expand(hs[i]+hs[j]-target) == 0, 'pair sum identity')
    factorizations = []
    for i,h in enumerate(hs):
        factors = sp.factor_list(h, a,b)[1]
        check(len(factors)==1 and factors[0][1]==1 and sp.total_degree(factors[0][0])==2,
              'exact irreducibility factorization')
        A=sp.diff(h,b); B=sp.expand(h-A*b)
        check(sp.degree(A,b)==0 and not B.has(b), 'linear-in-b representation')
        check(sp.degree(sp.gcd(A,B), a)==0, 'primitive coefficient pair')
        check(sp.cancel(h.subs(b,-B/A))==0, 'rational curve parameterization')
        factorizations.append({'score':str(h),'A':str(A),'B':str(B),'root_b':str(sp.cancel(-B/A))})
    for i,j in combinations(range(3),2):
        check(sp.total_degree(sp.gcd(hs[i],hs[j]))==0, 'coprime score factors')
    quartics = [-sp.expand(hs[0]*hs[2]),-sp.expand(hs[1]*hs[2])]
    check(all(sp.total_degree(h)==4 for h in quartics), 'quartic degree')
    # All 4! bijective encodings force each bit to flip across two star edges.
    encodings=0
    for labels in permutations(tuple(product((0,1), repeat=2))):
        for bit in (0,1):
            check(sum(labels[0][bit]!=leaf[bit] for leaf in labels[1:])==2,
                  'two-test factor-incidence count')
        encodings+=1
    # Uniform coefficient scaling, checked symbolically.
    A,B,C,x,y=sp.symbols('A B C x y', nonzero=True)
    xp=C*x/B; yp=C*y/A
    check(sp.expand(A*B/C*(xp+yp+xp*yp)-(A*x+B*y+C*x*y))==0,'positive rescaling identity')
    return {'reciprocal_identities':4,'negative_pair_sum_identities':3,
            'primitive_irreducible_quadratics':factorizations,'quartics':[str(p) for p in quartics],
            'bijective_two_bit_encodings_checked':encodings,
            'scope':'Exact identities and algebraic prerequisites; see proof for the universal guard lower bound.'}


def rational_checks() -> dict:
    vals=sorted({Fraction(p,q) for p in range(1,25) for q in range(1,13)})
    reverse={v:k for k,v in TRUTH_TABLES.items()}
    counts=Counter(); maxobs=Counter()
    for a,b in product(vals, repeat=2):
        # Independent direct evaluation of the real model on actual representatives.
        direct=tuple(x+y+x*y for x,y in ((a,b),(a,-b),(-a,b),(-a,-b)))
        check(direct==score_vector(a,b), 'signed-input scores versus expanded scores')
        u,v=1/a,1/b
        normal=(u+v+1,v-u-1,u-v-1,1-u-v)
        check(tuple(s/(a*b) for s in direct)==normal,'rational reciprocal normal form')
        if any(s==0 for s in direct):
            expected='BOUNDARY'
        else:
            expected=reverse.get(tuple(int(s>0) for s in direct),'UNEXPECTED')
        check(expected!='UNEXPECTED','four-operator restriction')
        counts[expected]+=1
        for mode in ('coordinate','quartic'):
            r=dispatch(a,b,mode)
            check((r.operator if r.status=='EXACT' else r.status)==expected,'dispatcher matches direct evaluation')
            maxobs[mode]=max(maxobs[mode],r.sign_observations)
    # Each boundary is parametrized, including points not in the finite grid.
    boundary_counts=Counter()
    for t in vals:
        for key,point in (('C1',(t,t/(1+t))),('C2',(t/(1+t),t)),('C3',(1+t,(1+t)/t))):
            for mode in ('coordinate','quartic'):
                r=dispatch(*point,mode)
                check(r.status=='BOUNDARY' and r.truth_vector is None,'boundary rejection')
            boundary_counts[key]+=1
    # Reproduce the original 20 by 20 rational grid, with explicitly named outcomes.
    old=Counter()
    for p,q in product(range(1,21),repeat=2):
        r=dispatch(Fraction(p,4),Fraction(q,4))
        old[r.operator if r.status=='EXACT' else r.status]+=1
    witnesses={name:[str(a),str(b)] for name,(a,b) in zip(TRUTH_TABLES,
       ((Fraction(1,2),Fraction(1,2)),(Fraction(2),Fraction(1,2)),
        (Fraction(1,2),Fraction(2)),(Fraction(3),Fraction(3))),strict=True)}
    return {'distinct_positive_rationals':len(vals),'grid_points':len(vals)**2,
            'classification_counts':dict(sorted(counts.items())),
            'boundary_parameter_samples':dict(boundary_counts),
            'maximum_observed_sign_queries':dict(maxobs),
            'historical_400_point_grid':dict(old),'interior_witnesses':witnesses,
            'scope':'Exact finite tests; the chamber connectedness is established analytically.'}


def separating(family:tuple[int,...],subset:int,ncoords:int=4)->bool:
    signatures={tuple((f>>i)&1 for i in range(ncoords) if subset>>i&1) for f in family}
    return len(signatures)==len(family)


def test_set_checks() -> dict:
    # Every nonempty subfamily of all 16 binary truth tables, all 16 coordinate subsets.
    histogram=Counter(); comparisons=0
    for family_mask in range(1,1<<16):
        family=tuple(f for f in range(16) if family_mask>>f&1)
        # Independent pair-difference hitting constraints.
        differences={f^g for f,g in combinations(family,2)}
        optimum=4
        for subset in range(16):
            via_signatures=separating(family,subset)
            via_constraints=all(subset&difference for difference in differences)
            check(via_signatures==via_constraints,'hitting constraints agree with injectivity')
            if via_signatures:
                optimum=min(optimum,subset.bit_count())
            comparisons+=1
        check((len(family)-1).bit_length()<=optimum<=4,'signature information bound')
        histogram[optimum]+=1
    star=tuple(sum(bit<<i for i,bit in enumerate(table)) for table in TRUTH_TABLES.values())
    optsets=[s for s in range(16) if separating(star,s) and s.bit_count()==3]
    check(optsets==[14], 'unique minimum true-first coordinate subset')
    @lru_cache(None)
    def adaptive_cost(family:tuple[int,...])->int:
        if len(family)<=1:return 0
        candidates=[]
        for i in range(4):
            zero=tuple(f for f in family if not f>>i&1)
            one=tuple(f for f in family if f>>i&1)
            if zero and one:
                candidates.append(1+max(adaptive_cost(zero),adaptive_cost(one)))
        return min(candidates)
    check(adaptive_cost(star)==3,'optimal adaptive star cost')
    # Positive weights and repeated labels: a finite explicit atom/predicate example.
    rows=[(0,0,0),(0,1,0),(1,0,1),(1,1,1)]
    labels=['A','A','B','C']; weights=[3,1,2]
    feasible=[]
    for mask in range(8):
        signatures=[tuple(row[j] for j in range(3) if mask>>j&1) for row in rows]
        exact=all(labels[i]==labels[k] or signatures[i]!=signatures[k] for i,k in combinations(range(4),2))
        ds=[{j for j in range(3) if rows[i][j]!=rows[k][j]} for i,k in combinations(range(4),2) if labels[i]!=labels[k]]
        hits=all(any(mask>>j&1 for j in s) for s in ds)
        check(exact==hits,'weighted atom example')
        if exact:feasible.append((sum(w for j,w in enumerate(weights) if mask>>j&1),mask))
    return {'nonempty_operator_families':65535,'family_subset_comparisons':comparisons,
            'minimum_size_histogram':dict(sorted(histogram.items())),
            'star_unique_minimum_coordinates':['10','01','00'],
            'star_adaptive_minimum':adaptive_cost(star),'weighted_example_optimum':min(feasible),
            'scope':'All families of binary two-input truth tables; no general solver performance claim.'}


def truth(f:int,bits:tuple[int,...])->int:
    # Lexicographic binary indexing, separate from presentation reshaping.
    index=0
    for b in bits:index=2*index+b
    return (f>>index)&1


def minterm_extension(f:int,args:tuple[int,...])->int:
    result=0
    for beta in product((0,1),repeat=len(args)):
        term=truth(f,beta)
        for a,b in zip(args,beta,strict=True):
            term &= a if b else 1-a
        result |= term
    return result


def lifted_value(f:int,alpha:tuple[int,...],frame:tuple[int,...])->int:
    arguments=tuple(x if a else 1-x for a,x in zip(alpha,frame,strict=True))
    return minterm_extension(f,arguments)


def lm_checks() -> dict:
    entries=0;recoveries=0
    for n in range(1,4):
        vectors=list(product((0,1),repeat=n))
        for f in range(1<<(1<<n)):
            for alpha in vectors:
                check(lifted_value(f,alpha,(1,)*n)==truth(f,alpha),'LM all-true recovery using actual minterms')
                recoveries+=1
                for frame in vectors:
                    literal_tuple=tuple(int(x==a) for x,a in zip(frame,alpha,strict=True))
                    check(lifted_value(f,alpha,frame)==truth(f,literal_tuple),'LM all-valuation semantics')
                    entries+=1
    # All 16 binary superposition connectives, every ordered pair of 2-input functions.
    n=2;vectors=list(product((0,1),repeat=n));superpositions=0
    cache={(f,a,x):lifted_value(f,a,x) for f in range(16) for a in vectors for x in vectors}
    for H,f,g in product(range(16),repeat=3):
        composed=sum(truth(H,(truth(f,alpha),truth(g,alpha)))<<i for i,alpha in enumerate(vectors))
        for alpha,frame in product(vectors,repeat=2):
            left=cache[composed,alpha,frame]
            right=truth(H,(cache[f,alpha,frame],cache[g,alpha,frame]))
            check(left==right,'pointwise superposition')
            superpositions+=1
    return {'actual_minterm_recovery_cases':recoveries,'all_valuation_entry_cases':entries,
            'binary_superposition_entry_cases':superpositions,
            'scope':'Actual formula evaluation, replacing the historical truth[i] == truth[i] self-comparison.'}


def walsh_checks() -> dict:
    counts={};adjacency_counts={}
    # Integer-only witnesses; no floating rank calculation is used.
    for n in range(1,5):
        xs=list(product((-1,1),repeat=n));N=len(xs)
        phi=[[sp.prod(x[i] for i in range(n) if mask>>i&1) for mask in range(1,N)] for x in xs]
        # Convert exact symbolic products to native Python ints for bounded enumeration.
        phi=[[int(v) for v in row] for row in phi]
        for i in range(N):
            for j in range(N):
                check(sum(a*b for a,b in zip(phi[i],phi[j],strict=True))==(N-1 if i==j else -1),'Walsh simplex Gram identity')
        check(all(sum(row[j] for row in phi)==0 for j in range(N-1)),'Walsh centering')
        for mask in range(1,(1<<N)-1):
            selected=[j for j in range(N) if mask>>j&1];k=len(selected)
            coeff=[sum(phi[j][i] for j in selected) for i in range(N-1)]
            scores=[sum(c*v for c,v in zip(coeff,row,strict=True)) for row in phi]
            check(scores==[N-k if mask>>j&1 else -k for j in range(N)],'Walsh constructive witness')
        counts[n]=(1<<N)-2
        if n in (2,3):
            edges=0
            for mask in range(1,(1<<N)-1):
                for j in range(N):
                    other=mask^(1<<j)
                    if mask<other<(1<<N)-1:
                        signs=[i for i in range(N) if i!=j]
                        plus=[i for i in signs if mask>>i&1];minus=[i for i in signs if not mask>>i&1]
                        check(bool(plus) and bool(minus),'both common signs at a regular Walsh facet')
                        w=[0 if i==j else (len(minus) if i in plus else -len(plus)) for i in range(N)]
                        check(sum(w)==0 and sum(v==0 for v in w)==1,'explicit regular-facet witness')
                        edges+=1
            adjacency_counts[n]=edges
    return {'nonconstant_labelings_by_arity':counts,'total_constructive_labelings':sum(counts.values()),
            'regular_facet_witness_edges':adjacency_counts,
            'scope':'Bounded exact constructive checks through n=4; not a novelty claim.'}


def adversarial_checks() -> dict:
    rejected=[]
    for pair in ((0,1),(-1,2),(1,0),(1.0,1),(True,1),('not-a-rational',1)):
        try:dispatch(*pair)
        except (TypeError,ValueError,ZeroDivisionError):rejected.append([str(v) for v in pair])
        else:raise AssertionError('invalid input not rejected')
    boundary=score_vector(1,Fraction(1,2))
    check(tuple(int(s>0) for s in boundary[1:])==(0,0,0),'boundary collides with naive AND bits')
    check(dispatch(1,Fraction(1,2)).status=='BOUNDARY','naive zero-as-false mutation caught')
    check(TRUTH_TABLES['AND'][:3]==TRUTH_TABLES['XNOR'][:3],'omitted-coordinate collision exposed')
    # Deliberately bad LM: ignores signed-frame literals; a concrete case disagrees.
    f=12;alpha=(0,0);frame=(1,1)
    check(truth(f,frame)!=lifted_value(f,alpha,frame),'unsigned LM mutation must be detectable')
    # Enumerate every collecting sign set; exact reachable output iff strict singleton.
    statuses=[]
    for mask in range(8):
        S={s for i,s in enumerate((-1,0,1)) if mask>>i&1}
        definition_exact=bool(S) and 0 not in S and len({int(s>0) for s in S})==1
        singleton_exact=S in ({-1},{1})
        check(definition_exact==singleton_exact,'collecting sign exactness')
        statuses.append({'sign_set':sorted(S),'exact_strict_output':singleton_exact})
    return {'invalid_inputs_rejected':rejected,'collecting_sets':statuses,
            'regressions':['zero-as-false boundary collision','omitted 00 coordinate','unsigned LM substitution'],
            'scope':'Explicit counterexamples and input validation; not a formal verification system.'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'evidence'/'fresh_run')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    modules=[('symbolic',symbolic_checks),('rational',rational_checks),('test_sets',test_set_checks),
             ('lm',lm_checks),('walsh',walsh_checks),('adversarial',adversarial_checks)]
    results={};timing={}
    for name,fn in modules:
        start=time.perf_counter();results[name]=fn();timing[name]=round(time.perf_counter()-start,6)
        print(name+': PASS',flush=True)
    semantic={'status':'PASS','results':results}
    (args.out/'verification_results.json').write_text(json.dumps(semantic,indent=2,sort_keys=True)+'\n')
    provenance={'python':sys.version,'platform':platform.platform(),'sympy':sp.__version__,
                'module_elapsed_seconds':timing,'timing_scope':'One verification run; not dispatcher benchmarks.',
                'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__),Path(__file__).with_name('guarded_dispatch.py'))}}
    (args.out/'environment_and_run.json').write_text(json.dumps(provenance,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','output':str(args.out.resolve()),'seconds':sum(timing.values())},indent=2))

if __name__=='__main__':main()
