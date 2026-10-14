"""Summarize separate diagnostics; never alter primary comparisons."""
from pathlib import Path
import csv,json

ROOT=Path(__file__).resolve().parents[1]
def append_once(name,heading,body):
    p=ROOT/name;text=p.read_text(encoding='utf-8');text=text.split('\n'+heading)[0]
    p.write_text(text.rstrip()+'\n\n'+heading+'\n\n'+body.strip()+'\n',encoding='utf-8')

def main():
    moves=json.loads((ROOT/'data/move_diagnostics_summary.json').read_text())
    reuse=json.loads((ROOT/'data/sat_reuse_results.json').read_text());s=reuse['summary']
    assert s['full_campaign_pairing_complete'] and s['failed_or_incorrect_runs']==0
    example=next(x for x in map(json.loads,(ROOT/'data/move_diagnostics.jsonl').read_text().splitlines()) if x['delta_size']>0 and x['delta_exposure']>0)
    instance=next(x for x in json.loads((ROOT/'data/benchmark_manifest.json').read_text())['records'] if x['id']==example['id'])
    (ROOT/'data/size_exposure_tradeoff_example.json').write_text(json.dumps({'move':example,'input':instance},indent=2)+'\n')
    ratios=s['geometric_mean_paired_ratios']
    table='| SAT workload | Runs | Median end-to-end ms | Median solve ms | Total conflicts | Total propagations |\n|---|---:|---:|---:|---:|---:|\n'
    for name,m in s['methods'].items():
        table+=f"| {name} | {m['runs']} | {1000*m['end_to_end_seconds']['median']:.3f} | {1000*m['solve_seconds']['median']:.3f} | {m['counter_totals']['conflicts']} | {m['counter_totals']['propagations']} |\n"
    text=f'''# Supplementary measured diagnostics

These experiments ran after all principal trials and baseline selection were final. They do not tune objectives, change the primary metric, or rescue the failed algorithmic gate.

## Actual persistent versus fresh SAT

Twenty training instances, three repetitions and three implementations yielded {s['completed_runs']} complete runs and {s['checked_query_results']:,} independently checked cut answers, with zero discrepancies/timeouts. All cuts have the same deterministic order. The persistent/fresh-same-base comparison uses byte-identical controlled clauses; the third method constructs the original cut-specific Phase 3 formula. The controlled diagnostic deliberately uses the frozen Phase 4 encoder, without the new optional equality-support gates.

{table}

On paired instance medians, persistent/fresh-same-base geometric ratio is **{ratios['persistent_over_fresh_same_base']:.6f}**, and persistent/fresh-Phase3 is **{ratios['persistent_over_fresh_phase3']:.6f}**. This is real timing evidence for this small fixed-cut workload, including setup and encoding costs. It is not an encoding-size ratio. Repeated solver setup dominates much of the gap; neither retained learned-clause counts nor a causal attribution of all savings to learning is measured. Persistence is established prior art and already common to every principal method, so this result does not establish a new vtree adaptation benefit. Raw per-query counters/times and source hashes are preserved in data/sat_reuse_results.json.

## Move-by-move objective relation

The diagnostic maps all **{moves['original_move_occurrences']:,}** evaluated move occurrences onto **{moves['unique_moves']:,}** distinct input/tree-pair moves and **{moves['unique_residual_measurements']}** distinct certified-partition residual measurements. Every measurement completed and agreed with independent semantic and simultaneous truth. One fresh process measures each unique input/partition once, then the measurement is explicitly reused in every matching move record. This is exploratory profiling, not repeated timing inference.

Size/exposure classes: {json.dumps(moves['size_exposure_alignment'],sort_keys=True)}.

Size/SAT-call Pareto classes: {json.dumps(moves['size_sat_calls_pareto'],sort_keys=True)}.

The one observed tradeoff is `{example['id']}`: actual SDD element size **{example['parent_sdd_size']} to {example['candidate_sdd_size']}**, directly exposed blocks **{example['parent_exposed_blocks']} to {example['candidate_exposed_blocks']}**, residual SAT calls **{example['parent_sat_calls']} to {example['candidate_sat_calls']}**. The pure SAT solve-time diagnostic changes from {1000*example['parent_sat_seconds']:.4f} to {1000*example['candidate_sat_seconds']:.4f} ms, while its complete residual-stage diagnostic changes from {1000*example['parent_residual_seconds']:.3f} to {1000*example['candidate_residual_seconds']:.3f} ms. This illustrates why fewer calls and a tiny SAT-time difference are not automatically a total-runtime benefit. The latter timings are single measurements, not robust speed estimates.

`data/size_exposure_tradeoff_example.json` records CNF, both vtrees, partitions and measurements. It is a computational example of nonidentical size/exposure objectives. It does not show that globally size-optimal and globally exposure-optimal trees are necessarily disjoint, nor prove a general objective dominance theorem. No held-out move is selected to revise the frozen heuristic.

## Public controls

All three MIT-licensed official PySAT documentation CNFs passed, including one false formula handled outside the nonfalse prime-factor contract. Source URLs are in code/public_controls.py and data/public_control_results.json; attribution is retained in licenses/PySAT_LICENSE.txt. These are public smoke checks only. No public industrial corpus was run, and no result is described as industrial-scale validation.
'''
    (ROOT/'SUPPLEMENTARY_DIAGNOSTICS.md').write_text(text,encoding='utf-8')
    append_once('BENCHMARK_RESULTS.md','## Completed supplementary diagnostics',f"All {moves['original_move_occurrences']:,} move occurrences are covered; {moves['unique_residual_measurements']} measured residual states agree exactly. The separate SAT reuse comparison completes {s['completed_runs']} runs/{s['checked_query_results']:,} cut checks with zero discrepancies. Persistent/fresh-same-base paired geometric time ratio is {ratios['persistent_over_fresh_same_base']:.6f}. These post-campaign diagnostics and three public smoke checks do not change the primary NO-GO. See SUPPLEMENTARY_DIAGNOSTICS.md.")
    append_once('INCREMENTAL_SAT_PIPELINE.md','## Measured reuse diagnostic',f"Real Glucose4 comparisons completed {s['completed_runs']} runs and {s['checked_query_results']:,} exact cut-answer checks. Persistent/fresh-same-base paired geometric end-to-end ratio is {ratios['persistent_over_fresh_same_base']:.6f}; persistent/fresh-cut-specific-Phase3 ratio is {ratios['persistent_over_fresh_phase3']:.6f}. This closes the archived claim's measurement gap only on a small training-only all-cuts workload. It is known incremental-SAT engineering, not a new vtree-search gain or a measured learned-clause count. Full scope and component times: SUPPLEMENTARY_DIAGNOSTICS.md.")
    append_once('THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md','## T4 implementation observation: size and exposure can trade off',f"A recorded real-SDD move for {example['id']} increases size {example['parent_sdd_size']} to {example['candidate_sdd_size']} while increasing exposure {example['parent_exposed_blocks']} to {example['candidate_exposed_blocks']} and reducing residual calls {example['parent_sat_calls']} to {example['candidate_sat_calls']}. This is a reproducible finite computational observation, not a theorem about global optima or a priority claim. Exact inputs/vtrees are in data/size_exposure_tradeoff_example.json; timing limitations are in SUPPLEMENTARY_DIAGNOSTICS.md.")
    path=ROOT/'THEOREM_STATUS.csv'
    with path.open(newline='',encoding='utf-8') as f:reader=csv.DictReader(f);fields=reader.fieldnames;records=list(reader)
    additions=[
      {'id':'F4-F5-REPRO','claim':'Frozen Phase4/5 computational claims','status':'reproduced','hypotheses':'Exact archived seeds and finite universes','priority_posture':'Reproduction only','evidence':'REPRODUCTION_AUDIT.md','limits':'Not industrial runtime evidence'},
      {'id':'P5B-EXACT','claim':'Real hybrid output agrees with independent truth','status':'observed','hypotheses':'903 validation compilations and 2100 principal trials','priority_posture':'Implementation validation','evidence':'data/hybrid_validation.json; data/statistical_summary.json','limits':'Finite checks support but do not replace proof'},
      {'id':'P5B-PILOT','claim':'M5 improves total runtime over selected baseline','status':'failed_preregistered_gate','hypotheses':'Frozen 30-instance heldout pilot','priority_posture':'Negative empirical result','evidence':'data/statistical_summary.json','limits':'Does not refute different native implementations'},
      {'id':'P5B-REUSE','claim':'Persistent SAT reduces fixed-cut workload runtime','status':'observed','hypotheses':'20 training instances 180 runs 14220 checked answers','priority_posture':'Established technique measured here','evidence':'data/sat_reuse_results.json','limits':'No measured learned-clause count or industrial generalization'},
      {'id':'P5B-T4OBS','claim':'SDD size and direct exposure trade off on a move','status':'observed','hypotheses':'Explicit recorded CNF and two vtrees','priority_posture':'Computational example no novelty claim','evidence':'data/size_exposure_tradeoff_example.json','limits':'Not a global-optimum separation theorem'}]
    records=[r for r in records if r['id'] not in {a['id'] for a in additions}]+additions
    with path.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
    print(json.dumps({'supplement':'complete','moves':moves['unique_moves'],'sat_reuse_runs':s['completed_runs'],'public_controls':3}))

if __name__=='__main__':main()
