from common import *
import csv,statistics
def main():
    cells={}
    for section in ('main','complement'):
        for line in (ROOT/'results'/f'trials_{section}.jsonl').open():
            x=json.loads(line)
            if x['status']!='PASS':continue
            key=(x['case_id'],x['k'],x['method'],x['mode'],x['batch']);cells.setdefault(key,[]).append(x)
    columns=['case_id','kind','design','n','p','q','actual_rank','supplied_width','k','orientation','s_row','s_column','method','mode','batch','repetitions','executed_queries_per_trial','dense_row_bits','sparse_row_bits','sparse_column_bits','adaptive_bits','raw_factor_bits','serialized_bytes','peak_process_rss_bytes','construction_ns','verification_including_oracle_ns','serialization_ns','loading_ns','indexing_ns','update_ns','query_ns','full_lifecycle_phase_ns','trial_wall_ns']
    with (ROOT/'LIFECYCLE_SUMMARY.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
        for key,items in sorted(cells.items()):
            x=items[0];p=x['payloads'];median=lambda fn:statistics.median(fn(v) for v in items)
            row={a:x[a] for a in ('case_id','kind','design','n','p','q','actual_rank','k','orientation','method','mode','batch','serialized_bytes')}
            row.update(supplied_width=x['r'],s_row=p['row_support'],s_column=p['column_support'],repetitions=len(items),executed_queries_per_trial=x['query_count'],dense_row_bits=p['dense_row_bits'],sparse_row_bits=p['sparse_row_bits'],sparse_column_bits=p['sparse_column_bits'],adaptive_bits=p['chosen_bits'],raw_factor_bits=p['raw_factor_bits'],peak_process_rss_bytes=median(lambda v:v['peak_rss_process_bytes']),verification_including_oracle_ns=median(lambda v:v['phases_ns']['verification']+v['oracle_preparation_ns']),full_lifecycle_phase_ns=median(lambda v:v['end_to_end_phases_ns']+v['oracle_preparation_ns']),trial_wall_ns=median(lambda v:v['trial_wall_ns']))
            for phase in ('construction','serialization','loading','indexing','update','query'):row[phase+'_ns']=median(lambda v:v['phases_ns'][phase])
            w.writerow(row)
    design=json.loads((ROOT/'results/DESIGN_TIMING_AGGREGATES.json').read_text());lookup={(x['design'],x['comparator']):x for x in design if x['kind']=='natural' and x['t3']=='t3_adaptive' and x['mode']=='warm_persistent'}
    lines=['# Independent-design timing summary','', 'Descriptive medians of paired comparator/T3 full-lifecycle ratios over the frozen k/batch cells, using two repetitions per cell. Values above 1 favor T3. These design rows are the independent observational units; cells and outputs are not independent designs. The T3 column is the secondary sparse orientation-adaptive implementation, not the primary dense prediction.','', '| Design | Raw factors / T3 | Historical histogram / T3 | Compiled packed / T3 | CUDD + native count / T3 |','|---|---:|---:|---:|---:|']
    for d in sorted({k[0] for k in lookup}):lines.append('| '+d+' | '+' | '.join(f"{lookup[d,c]['median_full_ratio_comparator_over_t3']:.3f}" for c in ('raw_factor','draft3_histogram','packed_native','cudd_native'))+' |')
    lines+=['','The compiled packed comparator has a lower design-median full lifecycle in every listed design. Router is a constant-only admitted slice and must not be presented as a nontrivial favorable application. T3 has lower full-lifecycle medians than the CUDD compilation path in each listed design, but the compiled CUDD online phase is faster at every design median. Construction/compilation and repeated counts therefore tell different stories.','','See `results/DESIGN_TIMING_AGGREGATES.json` for dense and adaptive states, both modes, per-design cells and online ratios. `LIFECYCLE_SUMMARY.csv` separates all requested payload and phase measures. Cold trials have only one repetition per panel cell; their full raw phases and isolated process RSS are in `results/COLD_SUMMARY.json`, not pooled with this table.']
    (ROOT/'DESIGN_LEVEL_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
if __name__=='__main__':main()
