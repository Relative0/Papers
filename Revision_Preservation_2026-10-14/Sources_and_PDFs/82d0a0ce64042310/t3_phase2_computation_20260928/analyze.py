from common import *
import statistics,csv
def med(xs):return statistics.median(xs)
def main():
    incidence=json.loads((ROOT/'results/NATURAL_INCIDENCE.json').read_text());protocol=json.loads((PRIOR/'corpus_v1/PROTOCOL.json').read_text())
    design_rows=[]
    for d in protocol['designs']:
        rows=[x for x in incidence if x['design']==d['design']]
        byk=[]
        for k in sorted({x['k'] for x in rows}):
            a=[x for x in rows if x['k']==k];byk.append({'k':k,'cut_cases':len(a),'dense_favorable':sum(x['dense_favorable'] for x in a),'sparse_row_favorable':sum(x['sparse_row_favorable'] for x in a),'adaptive_favorable':sum(x['adaptive_favorable'] for x in a)})
        design_rows.append({**d,'eligible_cut_cases':len({x['case_id'] for x in rows}),'strata':byk})
    write(ROOT/'results/DESIGN_INCIDENCE.json',design_rows)
    statuses=Counter();storage={};groups={};cold=[];queries=updates=0;failures=[];invariants=Counter()
    for section in ('main','complement','cold'):
        with (ROOT/'results'/f'trials_{section}.jsonl').open() as stream:
            for line in stream:
                x=json.loads(line);statuses[section+':'+x['status']]+=1
                if x['status']!='PASS':
                    failures.append({key:x.get(key) for key in ('case_id','method','k','mode','batch','rep','status','error')});continue
                queries+=x['query_count'];updates+=x['update_count']
                assert sum(v['executed_queries'] for v in x['operations'])==x['query_count']
                for op in x['operations']:
                    assert len(op['query_ns'])==op['executed_queries'] and op['count']==x['expected'][op['depth']]
                    if op['depth'] and x['method'].startswith('t3'):
                        z,_=x['path'][op['depth']-1];d=op['residual_p']+1 if z in x['left'] else op['residual_q']+1
                        assert op['moment_counter_operations']==op['s']*D(d-1,op['horizon']);invariants['update_formula_checks']+=1
                if x['method'].startswith('t3') and 'persistent_payload_bits' in x:
                    key='dense_row_bits' if x['method']=='t3_dense_row' else 'sparse_column_bits' if x['orientation']=='column' else 'sparse_row_bits'
                    assert x['persistent_payload_bits']==x['payloads'][key];invariants['initial_payload_formula_checks']+=1
                key=(x['case_id'],x['k'],x['method']);storage[key]={a:x.get(a) for a in ('case_id','design','family','kind','n','p','q','r','actual_rank','k','method','orientation','serialized_bytes','payloads')}
                ph=x['phases_ns'];full=sum(ph.values())+x.get('oracle_preparation_ns',0)
                if section=='cold':cold.append({**{a:x.get(a) for a in ('case_id','design','method','k','serialized_bytes','page_cache_before_load','peak_rss_consumer_bytes','peak_rss_producer_bytes','parent_child_wall_ns','producer_and_child_wall_ns')},'full_phase_ns':full,'process_inclusive_lifecycle_ns':x['producer_and_child_wall_ns']+x.get('oracle_preparation_ns',0),'phases_ns':ph})
                else:
                    g=(x['case_id'],x['k'],x['mode'],x['batch']);groups.setdefault(g,{}).setdefault(x['method'],[]).append({'full_ns':full,'phase_ns':x['end_to_end_phases_ns'],'online_ns':ph['update']+ph['query'],'query_ns':ph['query'],'update_ns':ph['update'],'trial_wall_ns':x['trial_wall_ns']})
    pairs=[]
    for g,methods in groups.items():
        for t3 in ('t3_dense_row','t3_sparse_row','t3_sparse_column','t3_adaptive'):
            if t3 not in methods:continue
            for other in ('raw_factor','draft3_histogram','packed_native','cudd_native'):
                if other not in methods:continue
                a,b=methods[t3],methods[other]
                pairs.append({'case_id':g[0],'k':g[1],'mode':g[2],'batch':g[3],'t3':t3,'comparator':other,
                  'reps':min(len(a),len(b)),'t3_full_ns':med([v['full_ns'] for v in a]),'other_full_ns':med([v['full_ns'] for v in b]),
                  't3_online_ns':med([v['online_ns'] for v in a]),'other_online_ns':med([v['online_ns'] for v in b])})
    cases={x['case_id']:x for x in json.loads((ROOT/'inputs/TIMING_CASES.json').read_text())+json.loads((ROOT/'inputs/COMPLEMENT_CONTROLS.json').read_text())}
    summary=[]
    design_groups={}
    for x in pairs:
        c=cases[x['case_id']]
        key=(c['design'],c['kind'],x['t3'],x['comparator'],x['mode'])
        design_groups.setdefault(key,[]).append(x)
    design_timing=[]
    for (design,kind,t3,comp,mode),a in sorted(design_groups.items()):
        design_timing.append({'design':design,'kind':kind,'t3':t3,'comparator':comp,'mode':mode,'paired_cells':len(a),
          'median_full_ratio_comparator_over_t3':med([x['other_full_ns']/x['t3_full_ns'] for x in a]),
          'median_online_ratio_comparator_over_t3':med([x['other_online_ns']/x['t3_online_ns'] for x in a]),
          'full_winning_cells':sum(x['t3_full_ns']<x['other_full_ns'] for x in a)})
    write(ROOT/'results/DESIGN_TIMING_AGGREGATES.json',design_timing)
    for kind in ('natural','synthetic'):
        for comparator in ('raw_factor','draft3_histogram','packed_native','cudd_native'):
            for t3 in ('t3_dense_row','t3_adaptive'):
                a=[x for x in pairs if cases[x['case_id']]['kind']==kind and x['comparator']==comparator and x['t3']==t3]
                summary.append({'kind':kind,'t3':t3,'comparator':comparator,'paired_cells':len(a),
                  'full_lifecycle_wins':sum(x['t3_full_ns']<x['other_full_ns'] for x in a),'online_wins':sum(x['t3_online_ns']<x['other_online_ns'] for x in a),
                  'designs_with_any_full_win':sorted({cases[x['case_id']]['design'] for x in a if x['t3_full_ns']<x['other_full_ns']})})
    dense=[x for x in storage.values() if x['method']=='t3_dense_row'];favorable=[x for x in dense if x['payloads']['dense_favorable']]
    byte_misses=[x for x in favorable if 8*x['serialized_bytes']>=x['payloads']['raw_factor_bits']]
    matched=[]
    for x in favorable:
        raw=storage.get((x['case_id'],x['k'],'raw_factor'))
        if raw and x['serialized_bytes']>=raw['serialized_bytes']:matched.append(x)
    results={'status':'PASS','trial_statuses':dict(statuses),'executed_queries':queries,'executed_updates':updates,'invariants':dict(invariants),
      'successful_dense_case_depths':len(dense),'dense_favorable_case_depths':len(favorable),'dense_favorable_but_bytes_not_below_ideal_raw_bits':len(byte_misses),
      'dense_favorable_but_bytes_not_below_matched_raw_serialization':len(matched),'summary':summary,
      'cold_verified_passes':len(cold),'all_cold_zero_resident_before_load':all(x['page_cache_before_load']['resident']==0 for x in cold)}
    write(ROOT/'results/ANALYSIS.json',results);write(ROOT/'results/STORAGE.json',list(storage.values()));write(ROOT/'results/PAIRED_CELLS.json',pairs)
    write(ROOT/'results/COLD_SUMMARY.json',cold);write(ROOT/'results/FAILURE_TIMEOUT_UNSUPPORTED.json',failures);write(ROOT/'results/DENSE_BYTE_EXCEPTIONS.json',byte_misses)
    write(ROOT/'results/DENSE_MATCHED_BYTE_EXCEPTIONS.json',matched)
    with (ROOT/'EXPERIMENT_MANIFEST.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['experiment','raw_file','sha256','status'])
        for p in sorted((ROOT/'results').glob('*')):
            if p.is_file():w.writerow([p.stem,p.relative_to(ROOT).as_posix(),sha(p.read_bytes()),'recorded; inspect per-row status'])
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
