#!/usr/bin/env python3
"""Bounded interaction-core audit, preserving the imported frozen gate.

The F2 spectral-sequence calculation is persistence reduction of the exact
filtered relative chain complex C(Delta(Q x 2), K_P union K_Z).  A finite
interval [a,b) of positive length b-a=r records one rank-one d^r pairing.
Its endpoints survive through E^r and disappear on E^(r+1).  Length zero
intervals record d^0.  This computes page dimensions and differential ranks,
not preferred matrices of the differentials.  Integral homology uses the
baseline's primitive-kernel-basis Smith decomposition.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parent
# Do not create bytecode files alongside the frozen imported handoff source.
sys.dont_write_bytecode = True
BASELINE = (ROOT.parent / "Transferred Research" /
            "MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29" /
            "02_LATEST_HIGHER_DIMENSIONAL_GATE" / "verify_matching_inversion_theorem.py")
spec = importlib.util.spec_from_file_location("frozen_matching_verifier", BASELINE)
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


def rank_bits(columns):
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = column
                break
            column ^= pivots[pivot]
    return len(pivots)


def product_cells(le):
    """All nonempty product simplices; cached per coarse poset by caller."""
    vertices, order, indices = baseline.full_product_poset(le)
    ch = baseline.chains(order)
    return [(c, sum(1 << v for v in c)) for d in sorted(ch) for c in ch[d]]


def mixed_complex(le, availability, cached_cells=None):
    """Return oriented mixed simplices, filtration and integer boundaries.

    A cell is represented by (tuple_of_product_indices, missing_core_size).
    Product index 2*s+a denotes (s,a). Boundaries are sparse signed columns.
    """
    if cached_cells is None:
        cached_cells = product_cells(le)
    lower = sum(1 << (2*s) for s, a in enumerate(availability) if a == 1)
    upper = sum(1 << (2*s+1) for s, a in enumerate(availability) if a == 0)
    missing = lower | upper
    cells = [(c, (mask & missing).bit_count()) for c, mask in cached_cells
             if mask & lower and mask & upper]
    cells.sort(key=lambda item: (item[1], len(item[0]), item[0]))
    indices = {c: j for j, (c, _) in enumerate(cells)}
    boundaries = []
    for c, p in cells:
        column = {}
        for k in range(len(c)):
            face = c[:k] + c[k+1:]
            row = indices.get(face)
            if row is not None:
                column[row] = -1 if k % 2 else 1
        boundaries.append(column)
    return cells, boundaries


def filtered_f2(cells, boundaries, check_e1=True):
    """Page dimensions keyed 'filtration,total_degree'; ranks keyed page r."""
    reduced = {}
    pairs = []
    zero_columns = set()
    d0_columns = defaultdict(list)
    raw_columns = defaultdict(list)
    counts = Counter((p, len(c)-1) for c, p in cells)
    for j, ((c, p), boundary) in enumerate(zip(cells, boundaries)):
        column = sum(1 << i for i in boundary)
        raw_columns[len(c)-1].append(column)
        d0_columns[(p, len(c)-1)].append(sum(1 << i for i in boundary if cells[i][1] == p))
        while column:
            pivot = column.bit_length() - 1
            if pivot not in reduced:
                reduced[pivot] = column
                pairs.append((pivot, j))
                break
            column ^= reduced[pivot]
        if not column:
            zero_columns.add(j)
    paired_births = {i for i, _ in pairs}
    if not paired_births <= zero_columns:
        raise AssertionError("persistence pivot is not a birth column")
    infinite = sorted(zero_columns - paired_births)
    differentials = Counter()
    detailed_differentials = Counter()
    for i, j in pairs:
        r = cells[j][1] - cells[i][1]
        if len(cells[j][0]) != len(cells[i][0]) + 1:
            raise AssertionError("persistence pair has wrong degree")
        differentials[r] += 1
        detailed_differentials[(r, cells[j][1], len(cells[j][0])-1)] += 1
    def page(s):
        out = Counter((cells[i][1], len(cells[i][0])-1) for i in infinite)
        for i, j in pairs:
            if cells[j][1] - cells[i][1] >= s:
                out[(cells[i][1], len(cells[i][0])-1)] += 1
                out[(cells[j][1], len(cells[j][0])-1)] += 1
        return {f"{p},{d}": n for (p, d), n in sorted(out.items()) if n}
    e1 = page(1)
    if check_e1:
        ranks = {key: rank_bits(cols) for key, cols in d0_columns.items()}
        independent = {f"{p},{d}": n-ranks.get((p,d),0)-ranks.get((p,d+1),0)
                       for (p,d),n in counts.items()}
        independent = {k:v for k,v in independent.items() if v}
        if independent != e1:
            raise AssertionError(("E1 versus associated graded", independent, e1))
        total_ranks = {d: rank_bits(cols) for d,cols in raw_columns.items()}
        dimensions = Counter(len(c)-1 for c,_ in cells)
        direct = {d: n-total_ranks.get(d,0)-total_ranks.get(d+1,0)
                  for d,n in dimensions.items()}
        direct = {d:v for d,v in direct.items() if v}
        survivor = dict(Counter(len(cells[i][0])-1 for i in infinite))
        if direct != survivor:
            raise AssertionError(("persistence versus total F2 homology", direct, survivor))
    return {"e1":e1, "e2":page(2), "e3":page(3),
            "einfinity":page(len(cells)+1),
            "differential_ranks":{str(r):n for r,n in sorted(differentials.items()) if r},
            "differential_bidegrees":{f"{r},{p},{d}":n for (r,p,d),n in sorted(detailed_differentials.items()) if r},
            "homology_f2":dict(sorted(Counter(len(cells[i][0])-1 for i in infinite).items())),
            "max_core":max((p for _,p in cells), default=0),
            "cells":len(cells)}


def integral_mixed(cells, boundaries):
    """Full Z homology, checking d^2=0 and using primitive kernel coordinates."""
    degree_indices = defaultdict(list)
    for i,(c,p) in enumerate(cells):
        degree_indices[len(c)-1].append(i)
    dims = {d:len(inds) for d,inds in degree_indices.items()}
    if not dims:
        return {}
    dims = {d:dims.get(d,0) for d in range(max(dims)+1)}
    positions = {d:{i:j for j,i in enumerate(inds)} for d,inds in degree_indices.items()}
    matrices = {}
    for d in range(1,max(dims)+1):
        matrix = [[0]*dims[d] for _ in range(dims[d-1])]
        for j, col in enumerate(degree_indices[d]):
            composed = Counter()
            for i, coefficient in boundaries[col].items():
                matrix[positions[d-1][i]][j] = coefficient
                for k, lower_coefficient in boundaries[i].items():
                    composed[k] += coefficient * lower_coefficient
            if any(composed.values()):
                raise AssertionError("integral boundary does not square to zero")
        matrices[d] = matrix
    return baseline.normalize_groups(baseline.homology_Z(dims, matrices))


def graph_classes(le, availability):
    edges = baseline.exclusive_edges(le, availability)
    degree = Counter(v for e in edges for v in e)
    adjacency = defaultdict(set)
    for a,b in edges:
        adjacency[a].add(b); adjacency[b].add(a)
    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for v in adjacency[stack.pop()]:
                if v in unseen:
                    unseen.remove(v); stack.append(v)
    forest = len(edges) == len(adjacency)-components
    p_vertices = [i for i,a in enumerate(availability) if a==1]
    ferrers = all(adjacency[a] <= adjacency[b] or adjacency[b] <= adjacency[a]
                  for a,b in combinations(p_vertices,2))
    # In a bipartite graph any obstruction to chordal bipartiteness is an
    # induced connected 2-regular subgraph on an even number >=6 of vertices.
    chordal = True
    vertices = sorted(adjacency)
    for size in range(6,len(vertices)+1,2):
        for subset in combinations(vertices,size):
            S=set(subset)
            if not all(len(adjacency[v]&S)==2 for v in S):
                continue
            reached={subset[0]}; stack=[subset[0]]
            while stack:
                for w in adjacency[stack.pop()]&S-reached:
                    reached.add(w); stack.append(w)
            if reached==S:
                chordal=False; break
        if not chordal: break
    maximum=max(degree.values(),default=0)
    return {"edges":edges,"maximum_degree":maximum,"matching":maximum<=1,
            "maximum_degree_2":maximum<=2,"forest":forest,
            "ferrers":ferrers,"chordal_bipartite":chordal}


def serial_case(le, availability, result, classes, n=None, pid=None):
    return {"n":len(le) if n is None else n,"poset_id":pid,
            "strict_relations":[[i,j] for i in range(len(le)) for j in range(len(le)) if i!=j and le[i][j]],
            "availability":list(availability),"classes":classes, **result}


def run(exhaustive_n=5, random_n=6, random_trials=5000):
    start=time.monotonic()
    counts=defaultdict(Counter)
    differentials=Counter()
    witnesses={}
    integral=[]
    integral_keys=set()
    max_cells=0
    examined=0
    per_n=Counter()
    csv_path=ROOT/'interaction_case_summary.csv'
    output=csv_path.open('w',newline='',encoding='utf-8')
    writer=csv.DictWriter(output,fieldnames=['scope','n','poset_id','availability','edges','max_degree','max_core','cells','e1_dimension','e2_dimension','d1_rank','d2_rank','higher_rank','total_f2_betti'])
    writer.writeheader()

    def inspect(le,availability,cached,pid,scope):
        nonlocal examined,max_cells
        examined+=1; per_n[len(le)]+=1
        classes=graph_classes(le,availability)
        cells,boundaries=mixed_complex(le,availability,cached)
        result=filtered_f2(cells,boundaries)
        max_cells=max(max_cells,len(cells))
        dr=result['differential_ranks']
        groups=['all']+[k for k in ['matching','maximum_degree_2','forest','ferrers','chordal_bipartite'] if classes[k]]
        for name in groups:
            counts[(scope,name)]['cases']+=1
            counts[(scope,name)]['nonempty_graph']+=bool(classes['edges'])
            counts[(scope,name)]['d1_nonzero']+=bool(dr.get('1'))
            counts[(scope,name)]['d2_nonzero']+=bool(dr.get('2'))
            counts[(scope,name)]['d3plus_nonzero']+=any(int(r)>=3 for r in dr)
            counts[(scope,name)]['nonzero_homology']+=bool(result['homology_f2'])
        for r,rank in dr.items(): differentials[r]+=rank
        case=serial_case(le,availability,result,classes,pid=pid)
        flags=[]
        if dr.get('1'): flags.append('first_d1')
        if dr.get('2'): flags.append('first_d2')
        if any(int(r)>=3 for r in dr): flags.append('first_d3plus')
        if dr.get('2') and classes['maximum_degree_2']: flags.append('degree2_d2')
        if dr.get('2') and classes['ferrers']: flags.append('ferrers_d2')
        if dr.get('2') and classes['chordal_bipartite']: flags.append('chordal_d2')
        if result['max_core']>=4: flags.append('first_four_core')
        if result['homology_f2'] and not classes['matching']: flags.append('first_interacting_homology')
        new_flags=[key for key in flags if key not in witnesses]
        for key in new_flags: witnesses[key]=case
        # Integral scope: all n<=3; all five-state d2 cases up to 100 unique;
        # first representative of each new phenomenon; deterministic sparse
        # n=4/5 sampling (index modulus), and targeted random witnesses.
        do_integral=(len(le)<=3 or bool(new_flags) or
                     (dr.get('2') and sum('d2' in v.get('reasons',[]) for v in integral)<100) or
                     (scope=='exhaustive' and examined%401==0))
        if do_integral:
            key=(tuple(tuple(row) for row in le),tuple(availability))
            if key not in integral_keys:
                integral_keys.add(key)
                hz=integral_mixed(cells,boundaries)
                pair=baseline.relative_pair_Z(le,availability)
                shifted={d-1:g for d,g in hz.items()}
                if shifted!=pair:
                    raise AssertionError(('two colour shift Z',case,hz,pair))
                reasons=(['d2'] if dr.get('2') else [])+new_flags
                integral.append({**case,'mixed_homology_Z':hz,'cone_homology_Z':pair,'reasons':reasons})
                if any(g['torsion'] for g in hz.values()) and 'first_torsion' not in witnesses:
                    witnesses['first_torsion']=integral[-1]
        writer.writerow({'scope':scope,'n':len(le),'poset_id':pid,
                         'availability':''.join(map(str,availability)),
                         'edges':len(classes['edges']),'max_degree':classes['maximum_degree'],
                         'max_core':result['max_core'],'cells':len(cells),
                         'e1_dimension':sum(result['e1'].values()),
                         'e2_dimension':sum(result['e2'].values()),
                         'd1_rank':dr.get('1',0),'d2_rank':dr.get('2',0),
                         'higher_rank':sum(rank for r,rank in dr.items() if int(r)>=3),
                         'total_f2_betti':sum(result['homology_f2'].values())})

    for n in range(1,exhaustive_n+1):
        poset_count=0
        for pid,le in enumerate(baseline.natural_posets(n)):
            poset_count+=1
            cached=product_cells(le)
            for availability in product(range(3),repeat=n):
                inspect(le,availability,cached,pid,'exhaustive')
        print(json.dumps({'completed_n':n,'posets':poset_count,'cases':per_n[n],
                          'elapsed_seconds':round(time.monotonic()-start,3)}),flush=True)
    rng=random.Random(20260929)
    for trial in range(random_trials):
        # Deterministic independently sampled transitive closures, not an
        # exhaustive or uniformly sampled isomorphism-class enumeration.
        le=[[i==j for j in range(random_n)] for i in range(random_n)]
        density=rng.choice([0.2,0.4,0.6,0.8])
        for i in range(random_n):
            for j in range(i+1,random_n): le[i][j]=rng.random()<density
        for k in range(random_n):
            for i in range(k):
                for j in range(k+1,random_n): le[i][j]|=le[i][k] and le[k][j]
        availability=tuple(rng.randrange(3) for _ in range(random_n))
        inspect(le,availability,product_cells(le),trial,'random')
    output.close()
    summary={'coefficient':'F2','method':'filtered boundary persistence; E1 independently checked by d0 block ranks; total homology independently checked by unfiltered ranks',
             'exhaustive_max_n':exhaustive_n,'exhaustive_posets':'all distinct naturally labelled transitive closures, not isomorphism-deduplicated',
             'random_n':random_n,'random_trials':random_trials,'seed':20260929,
             'total_cases':examined,'per_n':dict(per_n),'largest_mixed_chain_complex_cells':max_cells,
             'elapsed_seconds':round(time.monotonic()-start,3),
             'class_summary':[{"scope":scope,"class":name,**dict(values)} for (scope,name),values in sorted(counts.items())],
             'differential_total_ranks':dict(differentials),'witnesses':witnesses,
             'integral_checks':len(integral),'integral_torsion_cases':sum(any(g['torsion'] for g in v['mixed_homology_Z'].values()) for v in integral)}
    (ROOT/'interaction_verification.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
    (ROOT/'interaction_integral_checks.json').write_text(json.dumps(integral,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['witnesses','class_summary']},indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--exhaustive-n',type=int,default=5)
    parser.add_argument('--random-n',type=int,default=6)
    parser.add_argument('--random-trials',type=int,default=5000)
    args=parser.parse_args()
    run(args.exhaustive_n,args.random_n,args.random_trials)
