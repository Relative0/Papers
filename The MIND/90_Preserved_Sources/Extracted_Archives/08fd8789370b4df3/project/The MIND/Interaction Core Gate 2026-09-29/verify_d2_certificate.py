#!/usr/bin/env python3
"""Integral certificate for the seven-state K1,3 nonzero d2 witness."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import verify_interaction as v
from verify_local_interactions import poset

ROOT=Path(__file__).resolve().parent


def add_scaled(a,b,k):
    for i,x in b.items():
        a[i]=a.get(i,0)+k*x
        if not a[i]: del a[i]


def boundary(chain,boundaries):
    out={}
    for j,a in chain.items(): add_scaled(out,boundaries[j],a)
    return out


def serialize_chain(chain,cells):
    return [{'coefficient':a,'product_vertices':[[i//2,i%2] for i in cells[j][0]],
             'core_size':cells[j][1]} for j,a in sorted(chain.items())]


def run(data=None, output_name='star_d2_integral_certificate.json'):
    if data is None:
        data=json.loads((ROOT/'minimal_star_d2.json').read_text())
    le=poset(data['n'],data['strict_relations']); av=tuple(data['availability'])
    cells,columns=v.mixed_complex(le,av)
    # Unit-pivot integral persistence, tracking actual oriented chain changes.
    # This succeeds over Z only when every pivot is ±1; that condition is
    # asserted at every step, rather than silently rationalizing.
    pivot_columns={}; transforms={}; pair=None; all_pairs=[]
    for j,col in enumerate(columns):
        col=dict(col); transformation={j:1}
        while col:
            pivot=max(col)
            if pivot not in pivot_columns:
                if abs(col[pivot])!=1:
                    raise AssertionError(('nonunit integral pivot',j,pivot,col[pivot]))
                pivot_columns[pivot]=col
                transforms[pivot]=transformation
                length=cells[j][1]-cells[pivot][1]
                all_pairs.append({'birth_filtration':cells[pivot][1],
                                  'death_filtration':cells[j][1],
                                  'death_degree':len(cells[j][0])-1,'length':length})
                if length==2:
                    assert pair is None
                    pair=(pivot,j,dict(transformation),dict(col))
                break
            multiplier=-col[pivot]//pivot_columns[pivot][pivot]
            add_scaled(col,pivot_columns[pivot],multiplier)
            add_scaled(transformation,transforms[pivot],multiplier)
    assert pair is not None
    i,j,z,dz=pair
    assert boundary(z,columns)==dz
    x={a:b for a,b in z.items() if cells[a][1]==4}
    y={a:b for a,b in z.items() if cells[a][1]==3}
    dx=boundary(x,columns); dy=boundary(y,columns)
    d0x={a:b for a,b in dx.items() if cells[a][1]==4}
    d1x={a:b for a,b in dx.items() if cells[a][1]==3}
    d0y={a:b for a,b in dy.items() if cells[a][1]==3}
    d1y={a:b for a,b in dy.items() if cells[a][1]==2}
    assert not d0x
    check=dict(d1x); add_scaled(check,d0y,1)
    assert not check
    assert not boundary(d1y,columns)
    # Independently compute associated-graded homology integrally by retaining
    # only same-filtration boundary entries, and compare total two-colour SNF.
    e1={}
    for p in range(2,5):
        inds=[i for i,(_,q) in enumerate(cells) if q==p]
        positions={i:j for j,i in enumerate(inds)}
        subcells=[cells[i] for i in inds]
        subboundary=[{positions[i]:a for i,a in columns[j].items() if i in positions} for j in inds]
        e1[p]=v.integral_mixed(subcells,subboundary)
    total=v.integral_mixed(cells,columns)
    cone=v.baseline.relative_pair_Z(le,av)
    target_rank=e1[2].get(3,{}).get('free',0)
    assert target_rank in (1,2)
    assert e1=={2:{3:{'free':target_rank,'torsion':[]}},3:{},4:{4:{'free':1,'torsion':[]}}}
    expected_total={3:{'free':target_rank-1,'torsion':[]}} if target_rank>1 else {}
    expected_cone={2:{'free':target_rank-1,'torsion':[]}} if target_rank>1 else {}
    assert total==expected_total
    assert cone==expected_cone
    # With exactly these E1 entries, d1=0 and d2 is the only possible
    # differential. Total integral homology shows its map Z -> Z^2 is
    # injective and primitive. In suitable integral bases its matrix is [1,0].
    result={**data,'integral_e1_by_filtration_and_total_degree':e1,
            'mixed_homology_Z':total,'cone_homology_Z':cone,
            'unit_pivot_integer_reduction':True,'positive_length_pairs':[p for p in all_pairs if p['length']],
            'x_core4':serialize_chain(x,cells),'y_core3':serialize_chain(y,cells),
            'd1_x':serialize_chain(d1x,cells),'d0_y':serialize_chain(d0y,cells),
            'd2_target_d1_y':serialize_chain(d1y,cells),
            'identities_checked':['d0 x = 0','d1 x + d0 y = 0','d0(d1 y) = 0'],
            'integral_d2':f'Z -> Z^{target_rank} is primitive injective; Smith invariant factor [1]',
            'minimality_scope':data.get('minimality_scope','No global minimality claim is made.')}
    (ROOT/output_name).write_text(json.dumps(result,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['integral_e1_by_filtration_and_total_degree','mixed_homology_Z','cone_homology_Z','x_core4','y_core3','d2_target_d1_y','integral_d2']},indent=2),flush=True)


def c4_case():
    relations=[]
    for a,bs in [(0,[2,3,4,5,6,7]),(1,[2,3,4,5,6,7]),
                 (2,[5,6,7]),(3,[4,5,6,7]),(4,[6,7]),(5,[6,7])]:
        relations.extend((a,b) for b in bs)
    le=poset(8,relations); av=(1,2,2,1,2,0,0,2)
    cells,columns=v.mixed_complex(le,av)
    data=v.serial_case(le,av,v.filtered_f2(cells,columns),v.graph_classes(le,av))
    data['minimality_scope']='No global minimality claim is made. The structural search separately checks proper induced restrictions retaining all four exclusive states.'
    run(data,'c4_d2_integral_certificate.json')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=['star','c4','all'],default='star')
    args=parser.parse_args()
    if args.case in ('star','all'): run()
    if args.case in ('c4','all'): c4_case()
