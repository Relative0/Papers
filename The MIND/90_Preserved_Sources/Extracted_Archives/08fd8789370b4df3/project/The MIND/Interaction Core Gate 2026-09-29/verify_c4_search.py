#!/usr/bin/env python3
"""Reproducible bounded search for degree-two C4 interaction d2.

Uses verify_interaction's independently checked F2 persistence routine.
Samples labelled transitive closures, not uniform unlabelled posets.
Every sample has exactly four exclusive vertices a<b<x<y, with a,b
1-only, x,y 0-only, and every other vertex split. Thus the exclusive
graph is always C4 and both same-colour comparabilities hold.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from itertools import combinations

import verify_interaction as v

ROOT = Path(__file__).resolve().parent


def run(trials=20000, seed=2026092917):
    rng = random.Random(seed)
    started = time.monotonic()
    counts = Counter()
    signatures = set()
    witnesses = []
    max_cells = 0
    for trial in range(trials):
        n = 6 + trial % 5
        core = sorted(rng.sample(range(n), 4))
        a, b, x, y = core
        availability = [2] * n
        availability[a] = availability[b] = 1
        availability[x] = availability[y] = 0
        le = [[i == j for j in range(n)] for i in range(n)]
        density = rng.choice([0.08, 0.15, 0.25, 0.4, 0.6])
        for i in range(n):
            for j in range(i + 1, n):
                le[i][j] = rng.random() < density
        for u, w in zip(core, core[1:]):
            le[u][w] = True
        for k in range(n):
            for i in range(k):
                for j in range(k + 1, n):
                    le[i][j] |= le[i][k] and le[k][j]
        signature = (tuple(availability), tuple(tuple(row) for row in le))
        signatures.add(signature)
        cells, boundaries = v.mixed_complex(le, availability)
        result = v.filtered_f2(cells, boundaries)
        max_cells = max(max_cells, len(cells))
        counts[f'n{n}_cases'] += 1
        counts['d1_nonzero'] += bool(result['differential_ranks'].get('1'))
        counts['nonzero_e2_column4'] += any(k.startswith('4,') for k in result['e2'])
        counts['d2_nonzero'] += bool(result['differential_ranks'].get('2'))
        if result['differential_ranks'].get('2'):
            classes = v.graph_classes(le, availability)
            assert classes['maximum_degree'] == 2 and len(classes['edges']) == 4
            case = v.serial_case(le, availability, result, classes, pid=trial)
            if len(witnesses) < 20:
                case['mixed_homology_Z'] = v.integral_mixed(cells, boundaries)
                case['cone_homology_Z'] = v.baseline.relative_pair_Z(le, availability)
                shifted = {int(d)-1:g for d,g in case['mixed_homology_Z'].items()}
                assert shifted == case['cone_homology_Z']
                witnesses.append(case)
                print(json.dumps({'witness':case}), flush=True)
        assert not any(int(r)>2 for r in result['differential_ranks'])
        if (trial+1)%1000 == 0:
            print(json.dumps({'completed':trial+1,'d2_cases':counts['d2_nonzero'],
                              'e2_column4_cases':counts['nonzero_e2_column4'],
                              'seconds':round(time.monotonic()-started,3)}),flush=True)
    summary = {'coefficient':'F2', 'seed':seed, 'trials':trials,
               'scope':'random naturally labelled posets with fixed sampled exclusive four-chain; all other states split',
               'isomorphism_deduplicated':False,
               'distinct_labelled_poset_profile_pairs':len(signatures),
               'counts':dict(counts),'max_cells':max_cells,
               'witnesses':witnesses,
               'elapsed_seconds':round(time.monotonic()-started,3),
               'interpretation':'Finite search evidence only. Absence of a witness does not prove E2 collapse.'}
    (ROOT/'c4_search.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)


def audit_existing():
    summary=json.loads((ROOT/'c4_search.json').read_text(encoding='utf-8'))
    witness=min(summary['witnesses'],key=lambda c:c['n'])
    n=witness['n']
    le=[[i==j for j in range(n)] for i in range(n)]
    for i,j in witness['strict_relations']: le[i][j]=True
    av=witness['availability']
    exclusive=[i for i in range(n) if av[i]!=2]
    split=[i for i in range(n) if av[i]==2]
    restriction_checks=[]
    for size in range(len(split)):
        for chosen in combinations(split,size):
            keep=sorted(exclusive+list(chosen))
            restriction=v.baseline.induced_le(le,keep)
            profile=[av[i] for i in keep]
            cells,boundaries=v.mixed_complex(restriction,profile)
            result=v.filtered_f2(cells,boundaries)
            restriction_checks.append({'retained_original_vertices':keep,
                                       'd2_rank':result['differential_ranks'].get('2',0)})
    assert not any(c['d2_rank'] for c in restriction_checks)
    vertices,order,indices=v.baseline.full_product_poset(le)
    missing=[2*i+(0 if av[i]==1 else 1) for i in exclusive]
    available=[j for j in range(2*n) if j not in missing]
    core_data=[]
    for size in range(2,5):
        for core in combinations(missing,size):
            if not any(i%2==0 for i in core) or not any(i%2 for i in core): continue
            assert all(order[i][j] for i,j in zip(core,core[1:]))
            link_vertices=[t for t in available if all(order[t][s] or order[s][t] for s in core)]
            link_order=v.baseline.induced_le(order,link_vertices)
            homology=v.baseline.normalize_groups(v.baseline.reduced_homology_Z(link_order))
            core_data.append({'core_product_indices':core,'available_link_vertices':link_vertices,
                              'reduced_link_homology_Z':homology})
    # The first eight-state witness has canonical labels a,a',v,b,w,x,y,y'.
    assert n==8 and av==[1,2,2,1,2,0,0,2]
    paths={
        'abx':{(10,15):1,(7,15):-1},
        'aby':{(10,12):1,(8,12):-1,(8,9):1,(7,9):-1},
        'axy':{(4,10):-1,(4,5):1,(1,5):-1,(1,7):1},
        'bxy':{(2,10):-1,(2,7):1},
    }
    cores={'abx':(0,6,11),'aby':(0,6,13),'axy':(0,11,13),'bxy':(6,11,13)}
    for key,path in paths.items():
        vertices_in_link=next(set(c['available_link_vertices']) for c in core_data
                             if tuple(c['core_product_indices'])==cores[key])
        boundary=Counter()
        for (u,w),coefficient in path.items():
            assert u in vertices_in_link and w in vertices_in_link and order[u][w]
            boundary[w]+=coefficient;boundary[u]-=coefficient
        assert {i:c for i,c in boundary.items() if c}=={7:1,10:-1}
    cycle=Counter(paths['axy'])
    for edge,coefficient in paths['aby'].items(): cycle[edge]-=coefficient
    cycle={edge:c for edge,c in cycle.items() if c}
    edge_link_vertices=next(c['available_link_vertices'] for c in core_data
                           if tuple(c['core_product_indices'])==(0,13))
    edge_link=v.baseline.induced_le(order,edge_link_vertices)
    ch=v.baseline.chains(edge_link)
    mats=v.baseline.integer_boundary(ch)
    dims={d:len(cs) for d,cs in ch.items()}
    mapped_cycle={tuple(edge_link_vertices.index(i) for i in edge):coefficient
                  for edge,coefficient in cycle.items()}
    # Attach a 2-cell along this cycle: homology zero above H0 certifies a
    # primitive generator of the already checked integral H1=Z.
    existing=mats.get(2,[[0]*dims.get(2,0) for _ in ch[1]])
    mats[2]=[list(row)+[mapped_cycle.get(edge,0)] for row,edge in zip(existing,ch[1])]
    dims[2]=dims.get(2,0)+1
    filled=v.baseline.normalize_groups(v.baseline.homology_Z(dims,mats))
    assert filled=={0:{'free':1,'torsion':[]}}
    summary['exact_eight_state_audit']={
        'witness_trial':witness['poset_id'],
        'minimality_scope':'all 15 proper induced restrictions retaining all four exclusive vertices; no global minimality claim',
        'induced_restriction_checks':restriction_checks,
        'all_available_core_link_homology_Z':core_data,
        'path_fillings':[{'core':key,'edges':[[u,w,c] for (u,w),c in path.items()]}
                         for key,path in paths.items()],
        'd2_target_cycle':[[u,w,c] for (u,w),c in cycle.items()],
        'target_link_after_attaching_cycle_homology_Z':filled,
        'integral_d2_coefficient_up_to_orientation':1,
        'integral_e1_e2':{'4,0':{'free':1,'torsion':[]},'2,1':{'free':1,'torsion':[]}},
        'integral_e3_and_total_homology':{},
    }
    (ROOT/'c4_search.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(summary['exact_eight_state_audit'],indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--trials',type=int,default=20000)
    parser.add_argument('--seed',type=int,default=2026092917)
    parser.add_argument('--audit-existing',action='store_true')
    args=parser.parse_args()
    if args.audit_existing:
        audit_existing()
    else:
        run(args.trials,args.seed)
