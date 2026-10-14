#!/usr/bin/env python3
"""Exact local models and a bounded targeted search for higher pages."""
import json
from itertools import combinations
from pathlib import Path
import random
import time
import verify_interaction as v

ROOT=Path(__file__).resolve().parent


def poset(n,relations):
    le=[[i==j for j in range(n)] for i in range(n)]
    for i,j in relations: le[i][j]=True
    for k in range(n):
        for i in range(n):
            for j in range(n): le[i][j]|=le[i][k] and le[k][j]
    if any(le[i][j] and le[j][i] for i in range(n) for j in range(i+1,n)):
        raise ValueError('relations are not a poset')
    if any(le[i][j] for i in range(n) for j in range(i)):
        raise ValueError('indices must follow a linear extension')
    return le


def local_models():
    examples=[
        ('minimal_ordered_star',poset(3,[(0,1),(1,2)]),(1,0,0)),
        ('unordered_star',poset(3,[(0,1),(0,2)]),(1,0,0)),
        ('P4_height_two',poset(4,[(0,2),(1,2),(1,3)]),(1,1,0,0)),
        ('P4_two_supported_triples',poset(4,[(0,1),(0,2),(1,3),(2,3)]),(1,1,0,0)),
        ('K22_height_two',poset(4,[(0,2),(0,3),(1,2),(1,3)]),(1,1,0,0)),
        ('K22_one_ordered_colour',poset(4,[(0,1),(1,2),(1,3)]),(1,1,0,0)),
        ('K22_four_chain',poset(4,[(0,1),(1,2),(2,3)]),(1,1,0,0)),
        ('C6_height_two',poset(6,[(0,3),(0,5),(1,3),(1,4),(2,4),(2,5)]),(1,1,1,0,0,0)),
        ('K13_ordered_leaves',poset(4,[(0,1),(1,2),(2,3)]),(1,0,0,0)),
    ]
    rows=[]
    for name,le,av in examples:
        cells,boundaries=v.mixed_complex(le,av)
        result=v.filtered_f2(cells,boundaries)
        mixed=v.integral_mixed(cells,boundaries)
        cone=v.baseline.relative_pair_Z(le,av)
        assert {d-1:g for d,g in mixed.items()}==cone
        rows.append({'name':name,**v.serial_case(le,av,result,v.graph_classes(le,av)),
                     'mixed_homology_Z':mixed,'cone_homology_Z':cone,
                     'mixed_cells':[{'vertices':list(c),'core_size':p} for c,p in cells],
                     'integer_boundary_columns':[{str(i):a for i,a in col.items()} for col in boundaries]})
    (ROOT/'local_interaction_models.json').write_text(json.dumps(rows,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps([{'name':r['name'],'max_core':r['max_core'],'differential_ranks':r['differential_ranks'],'cone_homology_Z':r['cone_homology_Z']} for r in rows],indent=2),flush=True)


def targeted_stars(trials=10000):
    start=time.monotonic(); rng=random.Random(2026092902)
    summary={'seed':2026092902,'requested_trials':trials,'cases':0,'d1_nonzero':0,'d2_nonzero':0,'d3plus_nonzero':0,'max_cells':0,'witnesses':[]}
    counts={}
    for trial in range(trials):
        n=rng.choice([7,8,9,10])
        density=rng.choice([0.10,0.20,0.35,0.50,0.70])
        edges=[(0,j) for j in range(1,n)]
        edges.extend((i,j) for i in range(1,n) for j in range(i+1,n) if rng.random()<density)
        le=poset(n,edges)
        av=(1,)+tuple(rng.choice([0,0,2]) for _ in range(n-1))
        cells,boundaries=v.mixed_complex(le,av)
        result=v.filtered_f2(cells,boundaries)
        summary['cases']+=1; counts[n]=counts.get(n,0)+1
        summary['max_cells']=max(summary['max_cells'],len(cells))
        dr=result['differential_ranks']
        summary['d1_nonzero']+=bool(dr.get('1'))
        summary['d2_nonzero']+=bool(dr.get('2'))
        summary['d3plus_nonzero']+=any(int(r)>=3 for r in dr)
        if any(int(r)>=2 for r in dr):
            summary['witnesses'].append(v.serial_case(le,av,result,v.graph_classes(le,av)))
            # The first higher-page witness is a complete reproducible record;
            # avoid extending the budget after the target is attained.
            break
        if (trial+1)%1000==0:
            print(json.dumps({'star_trials':trial+1,'elapsed_seconds':round(time.monotonic()-start,3)}),flush=True)
    summary['per_n']=counts; summary['elapsed_seconds']=round(time.monotonic()-start,3)
    (ROOT/'targeted_star_search.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)


def minimize_first_star():
    data=json.loads((ROOT/'targeted_star_search.json').read_text())
    if not data['witnesses']:
        return
    witness=data['witnesses'][0]
    le=poset(witness['n'],witness['strict_relations'])
    availability=witness['availability']
    checked={}
    for size in range(4,len(le)+1):
        checked[size]=0
        for subset in combinations(range(1,len(le)),size-1):
            vertices=(0,)+subset
            sub=[[le[i][j] for j in vertices] for i in vertices]
            av=tuple(availability[i] for i in vertices)
            cells,boundaries=v.mixed_complex(sub,av)
            result=v.filtered_f2(cells,boundaries)
            checked[size]+=1
            if result['differential_ranks'].get('2'):
                out=v.serial_case(sub,av,result,v.graph_classes(sub,av))
                out['original_vertices']=vertices
                out['induced_subsets_checked_by_size']=checked
                out['minimality_scope']='Minimum cardinality among induced restrictions of the first ten-state witness retaining its bottom; no global minimality claim. Sizes below four cannot support d2.'
                (ROOT/'minimal_star_d2.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
                print(json.dumps({'minimized_star_states':size,'induced_subsets_checked':checked}),flush=True)
                return


if __name__=='__main__':
    local_models()
    targeted_stars()
    minimize_first_star()
