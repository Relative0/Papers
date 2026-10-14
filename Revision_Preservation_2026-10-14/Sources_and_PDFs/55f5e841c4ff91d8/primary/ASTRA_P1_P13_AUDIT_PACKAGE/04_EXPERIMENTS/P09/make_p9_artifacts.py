from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D='direct_source_pipeline'; P6='p6_source_pipeline'; P8='p8_full_source_dispatch'; P9='p9_min_source_dispatch'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def geo(xs):return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def med(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}

g=json.load(open(HERE/'gatep.json')); s=json.load(open(HERE/'N2_P9_SUMMARY.json')); inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json')); ver=json.load(open(HERE/'N2_P9_INDEPENDENT_VERIFY.json'))
names=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in names]
ns=[r for x in nat for r in x['source_timing_rows']]

# Case summaries
for fname,rows,symbolic in [('N2_P9_GATEP_CASE_SUMMARY.csv',g['source_timing_rows'],g['symbolic']),('N2_P9_NATURAL_CASE_SUMMARY.csv',ns,[x['symbolic'] for x in nat])]:
    msp=med(rows,'source_pipeline_ns'); msb=med(rows,'source_build_ns'); mcp=med(rows,'compiler_ns'); sy={r['case_id']:r for r in symbolic}
    fields=['case_id','depth','circuit','root','annotate','predicted_ratio','p6_folds','direct_source_ns','p6_source_ns','p8_source_ns','p9_source_ns','p9_over_direct_source','p9_over_p8_source','direct_build_ns','p8_build_ns','p9_build_ns','p9_over_direct_build','p9_over_p8_build','direct_compiler_ns','p9_compiler_ns','multiplications_ratio','pair_terms_ratio','peak_monomials_ratio','anf_nodes_ratio']
    with open(HERE/fname,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for c in sorted(sy):
            z=sy[c]; d=z['direct']; p=z['p9']
            def rr(field):
                a=p.get(field); b=d.get(field); return (a/b if a is not None and b not in (None,0) else None)
            row={'case_id':c,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),'annotate':z['annotate'],'predicted_ratio':z['predicted_ratio'],'p6_folds':z['p6_folds'],
                 'direct_source_ns':msp[(c,D)],'p6_source_ns':msp[(c,P6)],'p8_source_ns':msp[(c,P8)],'p9_source_ns':msp[(c,P9)],'p9_over_direct_source':msp[(c,P9)]/msp[(c,D)],'p9_over_p8_source':msp[(c,P9)]/msp[(c,P8)],
                 'direct_build_ns':msb[(c,D)],'p8_build_ns':msb[(c,P8)],'p9_build_ns':msb[(c,P9)],'p9_over_direct_build':msb[(c,P9)]/msb[(c,D)],'p9_over_p8_build':msb[(c,P9)]/msb[(c,P8)],
                 'direct_compiler_ns':mcp[(c,D)],'p9_compiler_ns':mcp[(c,P9)],'multiplications_ratio':rr('multiplications'),'pair_terms_ratio':rr('pair_terms'),'peak_monomials_ratio':rr('peak_monomials'),'anf_nodes_ratio':rr('anf_nodes_evaluated')}
            w.writerow(row)

# Posthoc free-telemetry diagnostic
msp=med(g['source_timing_rows'],'source_pipeline_ns'); msb=med(g['source_timing_rows'],'source_build_ns'); mcp=med(g['source_timing_rows'],'compiler_ns'); cases=sorted({r['case_id'] for r in g['source_timing_rows']})
free=[]; num=den=0.0
for c in cases:
    a=msb[(c,D)]+mcp[(c,P9)]; b=msb[(c,D)]+mcp[(c,D)]; free.append(a/b); num+=a; den+=b
free_diag={'schema':'cm-n2-p9-posthoc-free-telemetry/v1','case_geomean':geo(free),'weighted_ratio':num/den,'note':'Uses frozen P9 decisions and measured P9 compiler medians, replacing P9 source-build cost with direct source-build cost. Not a preregistered endpoint.'}
(HERE/'P9_POSTHOC_FREE_TELEMETRY.json').write_text(json.dumps(free_diag,indent=2))

# Absolute medians and depth strata
abs_build={}
for arm in (D,P8,P9): abs_build[arm]=statistics.median([msb[(c,arm)] for c in cases])/1000
strata={}
for depth in (6,8,10):
    cs=[c for c in cases if c.startswith(str(depth)+':')]
    strata[str(depth)]={'p9_direct_source':geo([msp[(c,P9)]/msp[(c,D)] for c in cs]),'p9_direct_build':geo([msb[(c,P9)]/msb[(c,D)] for c in cs])}

# Reports
p9d=s['gatep_source']['p9_direct']; p9p8=s['gatep_source']['p9_p8']; b9d=s['gatep_source_build']['p9_direct']; b9p8=s['gatep_source_build']['p9_p8']; c9d=s['gatep_compiler']['p9_direct']
nd=s['natural_source']['p9_direct']; np8=s['natural_source']['p9_p8']
work=s['gatep_work']; mem=s['gatep_memory']
results=f'''# N2/P9 Results - Minimal Frozen-Tree Source Telemetry

## Status

P9 is complete. The P8 dispatch policy was held exactly fixed while the telemetry implementation was reduced to the seven primitive counters needed by the five features actually used by the frozen P8 tree.

Mandatory invariance passed on all **332** frozen P8 cases: 188 training, 98 validation, 36 Gate-P evaluation, and 10 natural evaluation cases. P9 reproduced every used tree input, predicted leaf, and annotate/bypass decision exactly. Fresh fuzz also passed **1000/1000**.

## Gate-P primary endpoint

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P9 / direct, source-inclusive | **{p9d['geomean_ratio']:.6f}x** | **{p9d['ci95'][0]:.6f}-{p9d['ci95'][1]:.6f}** | **{p9d['weighted_ratio']:.6f}x** | {p9d['wins']}/36 |
| P9 / P8-full, source-inclusive | **{p9p8['geomean_ratio']:.6f}x** | **{p9p8['ci95'][0]:.6f}-{p9p8['ci95'][1]:.6f}** | **{p9p8['weighted_ratio']:.6f}x** | {p9p8['wins']}/36 |
| P9 / direct, source build | **{b9d['geomean_ratio']:.6f}x** | **{b9d['ci95'][0]:.6f}-{b9d['ci95'][1]:.6f}** | **{b9d['weighted_ratio']:.6f}x** | {b9d['wins']}/36 |
| P9 / P8-full, source build | **{b9p8['geomean_ratio']:.6f}x** | **{b9p8['ci95'][0]:.6f}-{b9p8['ci95'][1]:.6f}** | **{b9p8['weighted_ratio']:.6f}x** | {b9p8['wins']}/36 |
| P9 / direct, selected compiler path | **{c9d['geomean_ratio']:.6f}x** | **{c9d['ci95'][0]:.6f}-{c9d['ci95'][1]:.6f}** | **{c9d['weighted_ratio']:.6f}x** | {c9d['wins']}/36 |

The preregistered direct-crossover criterion **FAILED**: P9 remained about **{(p9d['geomean_ratio']-1)*100:.1f}% slower** than direct case-balanced. However, P9 was **{(1-p9p8['geomean_ratio'])*100:.1f}% faster than simultaneous P8-full** source-inclusive, with the entire 95% interval below 1.

The narrow telemetry-engineering criterion also failed because source build improved by **{(1-b9p8['geomean_ratio'])*100:.1f}%**, short of the preregistered 25% target, even though the source-inclusive P9/P8 target was satisfied.

Median Gate-P source-build time was approximately {abs_build[D]:.1f} us direct, {abs_build[P9]:.1f} us P9, and {abs_build[P8]:.1f} us P8-full.

## Dispatch and Boolean work

P9 necessarily made the same dispatches as frozen P8: **{s['gatep_annotated']}/36** cases annotated, all **{s['gatep_fold_cases']}** consuming a fold, for **{s['gatep_folds']}** total consumed folds. Against simultaneous always-P6 profitability, {s['gatep_confusion']['annotated_p6_wins']} annotations were P6 wins, {s['gatep_confusion']['annotated_p6_losses']} were P6 losses, and {s['gatep_confusion']['p6_wins_bypassed']} P6-winning cases were bypassed.

Relative to direct across all 36 cases, the frozen selective policy retained the same P8 work reductions:

- multiplications: **{work['multiplications']['geomean_ratio']:.6f}x**;
- pair terms: **{work['pair_terms']['geomean_ratio']:.6f}x**;
- peak monomials: **{work['peak_monomials']['geomean_ratio']:.6f}x**;
- ANF nodes evaluated: **{work['anf_nodes_evaluated']['geomean_ratio']:.6f}x**.

Because dispatch was held invariant, these are not new folding gains; P9 tests only whether the same gains can be exposed more cheaply.

## Memory

Gate-P traced peak allocation P9/direct was **{mem['p9_direct']['geomean_ratio']:.6f}x** and P9/P8-full was **{mem['p9_p8']['geomean_ratio']:.6f}x**. Thus P9 is approximately memory-neutral versus direct and modestly leaner than P8-full.

## Natural EPFL control

P9 annotated **0/10** frozen natural cases and consumed **0 folds**, so the natural corpus remains strictly an abstention/overhead control.

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P9 / direct, source-inclusive | **{nd['geomean_ratio']:.6f}x** | **{nd['ci95'][0]:.6f}-{nd['ci95'][1]:.6f}** | **{nd['weighted_ratio']:.6f}x** | {nd['wins']}/10 |
| P9 / P8-full, source-inclusive | **{np8['geomean_ratio']:.6f}x** | **{np8['ci95'][0]:.6f}-{np8['ci95'][1]:.6f}** | **{np8['weighted_ratio']:.6f}x** | {np8['wins']}/10 |

The case-balanced natural overhead is therefore only about **{(nd['geomean_ratio']-1)*100:.1f}%**, while the workload-weighted result is essentially parity. This is a substantial improvement in abstention cost, but it is not evidence of natural CM folding because no fold was taken.

## Post-hoc diagnostic

Keeping the exact frozen P9 decisions and compiler timings but replacing P9 source-build cost by measured direct source-build cost gives **{free_diag['case_geomean']:.6f}x** direct case-balanced and **{free_diag['weighted_ratio']:.6f}x** workload-weighted. This is not a preregistered endpoint; it estimates the remaining opportunity if telemetry could be fused into ordinary construction at negligible incremental cost.

## Measurement counts

- Gate-P timed rows: 2,880
- natural timed rows: 600
- total timed rows: **3,480**
- independent dispatch-invariance cases: **332**
- fresh fuzz cases: **1,000**

The long `cavlc:35` natural timing schedule was executed in deterministic ten-position chunks because of the execution-environment command limit, then merged without changing the frozen schedule, repetitions, arms, or policy.

## Conclusion

P9 improves P8 in the intended direction but does not reach the full direct crossover. Reducing telemetry from sixteen features to the seven primitives actually used by the frozen tree cut Gate-P source construction by about **{(1-b9p8['geomean_ratio'])*100:.1f}% relative to P8-full** and the full pipeline by about **{(1-p9p8['geomean_ratio'])*100:.1f}%**, while preserving every dispatch decision exactly. The remaining bottleneck is still source-time bookkeeping itself, not fold recognition or the selected compiler path.
'''
(HERE/'N2_P9_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P9 Interpretation

P9 answers a deliberately narrow question: if P8's model and choices are frozen, how much of its remaining tax comes from collecting telemetry that the model never uses?

The answer is: **some, but not most**. P9 removed all unused P8 counters and token-diversity bookkeeping while reproducing P8 exactly on 332 frozen cases. This produced a real simultaneous improvement: P9/P8 source build was **{b9p8['geomean_ratio']:.4f}x** and P9/P8 full source-inclusive time was **{p9p8['geomean_ratio']:.4f}x**. The pipeline improvement is statistically clear in this run. But P9 source construction still costs **{b9d['geomean_ratio']:.4f}x direct**, leaving the whole pipeline at **{p9d['geomean_ratio']:.4f}x direct**.

This matters because the selected compiler path itself is no longer the dominant problem. The simultaneous P9/direct compiler-path geomean is **{c9d['geomean_ratio']:.4f}x**, and the workload-weighted ratio is **{c9d['weighted_ratio']:.4f}x**. The frozen five-case annotation policy still removes enough work on its selected heavy cases that a post-hoc zero-incremental-telemetry calculation reaches **{free_diag['case_geomean']:.4f}x** case-balanced and **{free_diag['weighted_ratio']:.4f}x** workload-weighted.

The P9 profile localizes the remaining overhead. For 360 Gate-P source builds, the minimal `_make` wrapper accounts for about 0.052 s cumulative, including about 0.024 s in the ordinary base `_make`. The remaining work is per-new-node bookkeeping: depth propagation, incoming-use marking, canonical pair counting, and the extra Python call/control path. The plain profile for the same 360 builds totals about 0.062 s versus about 0.090 s for P9. These profile totals are diagnostic only; the randomized benchmark timings are authoritative.

The natural control is encouraging for a different reason. P9 takes no natural folds yet is only **{nd['geomean_ratio']:.4f}x** direct case-balanced and **{nd['weighted_ratio']:.4f}x** workload-weighted. Thus the abstention tax has been pushed close to practical parity on the large natural workload, even though Gate-P's small cases still expose the fixed source-builder cost.

## Recommended P10

The next clean experiment should keep the entire P8/P9 policy frozen again and attack only the remaining per-node source-construction path. Two changes are especially well motivated by the P9 profile:

1. **Fuse the seven-counter telemetry directly into a dedicated ordinary Factory `_make` implementation**, instead of wrapping `base.Factory._make` through `super()` and then revisiting the new node. Construct the cache key, create the node, and update only the needed counters in one Python frame/code path.
2. Add a **tree-aware lazy telemetry arm** as a separately preregistered comparator: the frozen tree's root is `max_pair_shells <= 4.5`. Natural cases never enter the right subtree, and only 24/36 Gate-P cases do. A lazy implementation can avoid maintaining features that are provably unreachable for a branch when it can do so without a second full traversal. Any such arm must preserve exact P8/P9 decisions on all 332 frozen cases before timing is interpreted.

I would test the fused implementation first because it is the cleaner causal experiment. The target is now concrete: P9 needs to remove roughly the remaining 63% source-build premium over direct. The post-hoc frozen-decision bound suggests that doing so is sufficient for an end-to-end crossover without changing the folding mathematics or dispatch model.
'''
(HERE/'N2_P9_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme=f'''# N2/P9 Reproducibility README

P9 reuses the exact frozen P8 decision tree/cutoff and P6 backend while replacing P8's full telemetry with seven primitive counters.

## Frozen hashes

- P9 preregistration: `{sha(HERE/'N2_P9_PREREGISTRATION.md')}`
- P9 harness: `{sha(HERE/'n2_p9_harness.py')}`
- P8 frozen gate: `{sha(HERE.parent/'cm_n2_p8_run'/'P8_FROZEN_GATE.json')}`

## Recommended reproduction order

From the workspace root:

1. `python cm_n2_p9_run/n2_p9_harness.py --mode invariant --out cm_n2_p9_run/invariance.json`
2. `python cm_n2_p9_run/n2_p9_harness.py --mode fuzz --out cm_n2_p9_run/fuzz.json`
3. `python cm_n2_p9_run/n2_p9_harness.py --mode gatep --out cm_n2_p9_run/gatep.json`
4. Run each natural case with `--mode natural-case`. For `cavlc:35`, use `run_p9_nat_chunk.py` in deterministic schedule chunks if the execution environment has a short command limit.
5. Merge the `cavlc:35` chunks, run `make_p9_artifacts.py`, then `independent_verify.py`.

The P8/P9 invariance check is mandatory before interpreting timing. The P9 harness imports the frozen P8/P6/P1 dependency harnesses included in this bundle.

P9 did not refit or retune the P8 gate.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')

combined={'schema':'cm-n2-p9-results-bundle/v1','summary':s,'independent_verify':ver,'invariance':inv,'fuzz':fuzz,'gatep':g,'natural_cases':nat,'posthoc_free_telemetry':free_diag,'depth_strata':strata,'absolute_build_medians_us':abs_build}
(HERE/'n2_p9_results.json').write_text(json.dumps(combined,indent=2),encoding='utf-8')
print('wrote artifacts')
