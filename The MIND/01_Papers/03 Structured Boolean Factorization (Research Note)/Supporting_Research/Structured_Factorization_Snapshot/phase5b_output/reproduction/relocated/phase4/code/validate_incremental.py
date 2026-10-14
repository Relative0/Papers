#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, os, random, json, statistics, time
ROOT=os.path.dirname(__file__)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec)
    import sys; sys.modules[name]=m; spec.loader.exec_module(m); return m
inc=load('inc',os.path.join(ROOT,'incremental_four_corner.py'))
fc=inc.fc

def random_partition(n,rng,max_blocks=5):
    k=rng.randint(1,min(max_blocks,n))
    # guarantee nonempty blocks via shuffled round-robin then random assignment
    vs=list(range(1,n+1)); rng.shuffle(vs); blocks=[[] for _ in range(k)]
    for i,v in enumerate(vs[:k]): blocks[i].append(v)
    for v in vs[k:]: blocks[rng.randrange(k)].append(v)
    return [tuple(sorted(b)) for b in blocks]

def canon(part): return sorted(tuple(sorted(b)) for b in part)

def run(trials=120,seed=41):
    rng=random.Random(seed); rows=[]; failures=[]; total_queries=0
    for t in range(trials):
        n=rng.randint(2,8); f=fc.random_cnf(n,rng.randint(1,max(2,2*n)),rng.randint(1,min(4,n)),rng)
        blocks=random_partition(n,rng)
        if len(blocks)==1: blocks=[(blocks[0][0],),tuple(blocks[0][1:])] if len(blocks[0])>1 else [(1,),(2,)]
        enc=inc.build_controlled_encoding(n,f,blocks)
        q=0; mismatch=0; indep_clause_sum=0; indep_var_sum=0
        for Aidx in inc.all_block_cuts(blocks):
            q+=1; total_queries+=1
            m1=inc.solve_restart(enc,Aidx); sat1=m1 is not None
            A=enc.cut_A_variables(Aidx)
            e2=fc.build_defect_encoding(n,f,A); m2=fc.dpll(e2.clauses,e2.nvars); sat2=m2 is not None
            exact=not fc.brute_rank1(n,f,A)
            indep_clause_sum+=len(e2.clauses); indep_var_sum+=e2.nvars
            if not (sat1==sat2==exact): mismatch+=1
            if sat1:
                wit=inc.witness_from_model(enc,Aidx,m1); vals,ok=fc.verify_witness(f,wit)
                if not ok: mismatch+=1
        got,st=inc.factor_blocks_controlled(enc)
        got0,st0=fc.factor_blocks(n,f,blocks)
        if canon(got)!=canon(got0): mismatch+=1
        if mismatch: failures.append(t)
        rows.append({
            'trial':t,'n':n,'m':len(f),'blocks':[list(b) for b in blocks],'k':len(blocks),'queries':q,
            'controlled_vars':enc.nvars,'controlled_clauses':len(enc.clauses),
            'independent_total_vars_over_queries':indep_var_sum,
            'independent_total_clauses_over_queries':indep_clause_sum,
            'clause_emission_ratio_independent_over_controlled': (indep_clause_sum/len(enc.clauses) if enc.clauses else 0),
            'factor_partition_controlled':canon(got),'factor_partition_independent':canon(got0),
            'factor_sat_calls':st['sat_calls'],'ok':mismatch==0
        })
    return {'trials':trials,'total_queries':total_queries,'failures':failures,'rows':rows}

if __name__=='__main__':
    d=run(); ratios=[r['clause_emission_ratio_independent_over_controlled'] for r in d['rows'] if r['queries']]
    summary={'trials':d['trials'],'total_queries':d['total_queries'],'failure_count':len(d['failures']),
             'mean_queries':statistics.mean(r['queries'] for r in d['rows']),
             'mean_clause_emission_ratio':statistics.mean(ratios),
             'median_clause_emission_ratio':statistics.median(ratios)}
    print(json.dumps(summary,indent=2))
    out={'summary':summary,**d}
    with open('C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase4/data/incremental_validation.json','w') as f: json.dump(out,f,indent=2)
    # export a deterministic example bundle
    exf=[(1,-2,3),(-1,2),(3,-4),(4,5)]; exb=[(1,2),(3,),(4,5)]
    e=inc.build_controlled_encoding(5,exf,exb)
    inc.export_query_bundle(e,'C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase4/data/incremental_example_base.cnf','C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase4/data/incremental_example_queries.json')
