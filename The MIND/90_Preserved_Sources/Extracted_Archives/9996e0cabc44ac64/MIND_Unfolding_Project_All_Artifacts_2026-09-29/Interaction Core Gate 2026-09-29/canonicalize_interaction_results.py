#!/usr/bin/env python3
"""Canonicalize saved exhaustive cases; never rerun homology computations.

Coarse posets are canonicalized under every vertex permutation. Exclusive
graphs preserve the P/Z bipartition, retain isolated exclusive vertices, and
omit split vertices. Both raw natural-label counts and a one-representative-
per-unlabelled-coarse-poset view are reported. Availability assignments in the
latter view are not further quotiented by coarse-poset automorphisms.
"""
from collections import Counter, defaultdict
import csv
from functools import lru_cache
from itertools import permutations
import json
from pathlib import Path
import time
import verify_interaction as v

ROOT=Path(__file__).resolve().parent


@lru_cache(None)
def perms(n):
    return tuple(permutations(range(n)))


def canonical_poset(le):
    n=len(le)
    return min(sum(1 << (i*n+j) for i in range(n) for j in range(n)
                   if i!=j and le[order[i]][order[j]])
               for order in perms(n))


@lru_cache(None)
def canonical_graph(p,z,bits):
    # bits is the row-major P-to-Z adjacency matrix in natural vertex order.
    code=min(sum(1 << (i*z+j) for i in range(p) for j in range(z)
                 if bits & (1 << (pp[i]*z+zz[j])))
             for pp in perms(p) for zz in perms(z))
    return f'P{p}_Z{z}_b{code:x}'


def summarize(row):
    return {'cases':1,'nonzero_d1_cases':int(int(row['d1_rank'])>0),
            'nonzero_d2_cases':int(int(row['d2_rank'])>0),
            'nonzero_higher_cases':int(int(row['higher_rank'])>0),
            'nonzero_homology_cases':int(int(row['total_f2_betti'])>0),
            'sum_d1_rank':int(row['d1_rank']),
            'sum_d2_rank':int(row['d2_rank']),
            'sum_higher_rank':int(row['higher_rank']),
            'sum_total_f2_betti':int(row['total_f2_betti'])}


def main():
    start=time.monotonic()
    posets={n:list(v.baseline.natural_posets(n)) for n in range(1,6)}
    canonical_ids={}; representatives={}; catalog=[]
    for n,family in posets.items():
        by_code=defaultdict(list)
        for pid,le in enumerate(family):
            by_code[canonical_poset(le)].append(pid)
        for index,(code,pids) in enumerate(sorted(by_code.items())):
            name=f'Q{n}_{index:02d}'
            representative=min(pids)
            representatives[(n,name)]=representative
            for pid in pids: canonical_ids[(n,pid)]=name
            le=family[representative]
            catalog.append({'n':n,'canonical_poset_id':name,'canonical_code_hex':f'{code:x}',
                            'representative_natural_poset_id':representative,
                            'natural_poset_ids':pids,
                            'representative_strict_relations':[[i,j] for i in range(n) for j in range(n) if i!=j and le[i][j]]})
    aggregates=defaultdict(Counter)
    metadata={}; per_n=Counter(); excluded=Counter(); coarse_used=defaultdict(set)
    with (ROOT/'interaction_case_summary.csv').open(newline='',encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            if row['scope']!='exhaustive':
                excluded[row['scope']]+=1
                continue
            n=int(row['n']); pid=int(row['poset_id'])
            le=posets[n][pid]; av=tuple(map(int,row['availability']))
            P=[i for i,a in enumerate(av) if a==1]
            Z=[i for i,a in enumerate(av) if a==0]
            bits=sum(1 << (i*len(Z)+j) for i,p in enumerate(P) for j,z in enumerate(Z) if le[p][z])
            graph=canonical_graph(len(P),len(Z),bits)
            if graph not in metadata:
                code=int(graph.split('_b')[1],16)
                edges=[[i,j] for i in range(len(P)) for j in range(len(Z)) if code&(1 << (i*len(Z)+j))]
                metadata[graph]={'graph_id':graph,'P_vertices':len(P),'Z_vertices':len(Z),
                                 'edges':len(edges),'canonical_P_Z_edges':edges,
                                 'isolated_P':len(P)-len({i for i,j in edges}),
                                 'isolated_Z':len(Z)-len({j for i,j in edges})}
            values=summarize(row)
            aggregates[('all_natural_labels',graph)].update(values)
            per_n[('all_natural_labels',n)]+=1
            coarse_id=canonical_ids[(n,pid)]
            coarse_used[('all_natural_labels',graph)].add(coarse_id)
            if representatives[(n,coarse_id)]==pid:
                aggregates[('one_representative_per_unlabelled_coarse_poset',graph)].update(values)
                per_n[('one_representative_per_unlabelled_coarse_poset',n)]+=1
                coarse_used[('one_representative_per_unlabelled_coarse_poset',graph)].add(coarse_id)
    rows=[]
    for (scope,graph),values in sorted(aggregates.items()):
        rows.append({'scope':scope,**metadata[graph],**dict(values),
                     'unlabelled_coarse_posets_represented':len(coarse_used[(scope,graph)])})
    expected={1:1,2:2,3:5,4:16,5:63}
    actual=Counter(item['n'] for item in catalog)
    assert dict(actual)==expected
    assert sum(r['cases'] for r in rows if r['scope']=='all_natural_labels')==90201
    assert sum(r['cases'] for r in rows if r['scope']=='one_representative_per_unlabelled_coarse_poset')==sum(expected[n]*3**n for n in expected)
    # Removing redundant natural labels retains every observed graph type.
    assert {r['graph_id'] for r in rows if r['scope']=='all_natural_labels'}=={r['graph_id'] for r in rows if r['scope']=='one_representative_per_unlabelled_coarse_poset'}
    summary={
        'source':'interaction_case_summary.csv; exhaustive rows only',
        'homology_recomputed':False,
        'coarse_poset_equivalence':'all vertex permutations; directed strict order preserved',
        'graph_equivalence':'independent permutations within P and within Z; colours not swapped; isolated P/Z retained; split states omitted',
        'availability_scope':'all profiles on each chosen unlabelled coarse-poset representative; profile automorphism quotient is not claimed',
        'naturally_labelled_posets_by_n':{n:len(family) for n,family in posets.items()},
        'unlabelled_coarse_posets_by_n':dict(actual),
        'unlabelled_coarse_posets_total':len(catalog),
        'exclusive_graph_isomorphism_types':len(metadata),
        'case_counts_by_scope_and_n':[{'scope':scope,'n':n,'cases':count} for (scope,n),count in sorted(per_n.items())],
        'excluded_rows':dict(excluded),
        'exclusion_reason':'Random n=6 posets cannot be reconstructed from the random-trial ID in the saved CSV without replaying their generator; no random case is silently grouped as exhaustive.',
        'elapsed_seconds':round(time.monotonic()-start,3),
        'coarse_poset_catalog':catalog,'graph_type_aggregates':rows}
    (ROOT/'interaction_isomorphism_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf-8')
    fields=[key for key in rows[0] if key!='canonical_P_Z_edges']
    with (ROOT/'interaction_graph_isomorphism_types.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader()
        for row in rows: writer.writerow({key:row[key] for key in fields})
    print(json.dumps({key:summary[key] for key in ['homology_recomputed','unlabelled_coarse_posets_by_n','unlabelled_coarse_posets_total','exclusive_graph_isomorphism_types','case_counts_by_scope_and_n','excluded_rows','elapsed_seconds']},indent=2))


if __name__=='__main__': main()
