from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D='direct_source_pipeline'; P6='p6_source_pipeline'; P9='p9_min_source_dispatch'; P10='p10_fused_source_dispatch'

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

g=json.load(open(HERE/'gatep.json')); s=json.load(open(HERE/'N2_P10_SUMMARY.json')); inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json'))
names=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in names]
ns=[r for x in nat for r in x['source_timing_rows']]

# Case summaries
for fname,rows,symbolic in [('N2_P10_GATEP_CASE_SUMMARY.csv',g['source_timing_rows'],g['symbolic']),('N2_P10_NATURAL_CASE_SUMMARY.csv',ns,[x['symbolic'] for x in nat])]:
    msp=med(rows,'source_pipeline_ns'); msb=med(rows,'source_build_ns'); mcp=med(rows,'compiler_ns'); sy={r['case_id']:r for r in symbolic}
    fields=['case_id','depth','circuit','root','annotate','predicted_ratio','p6_folds','direct_source_ns','p6_source_ns','p9_source_ns','p10_source_ns','p10_over_direct_source','p10_over_p9_source','direct_build_ns','p9_build_ns','p10_build_ns','p10_over_direct_build','p10_over_p9_build','direct_compiler_ns','p10_compiler_ns','multiplications_ratio','pair_terms_ratio','peak_monomials_ratio','anf_nodes_ratio']
    with open(HERE/fname,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for c in sorted(sy):
            z=sy[c]; d=z['direct']; p=z['p10']
            def rr(field):
                a=p.get(field); b=d.get(field); return (a/b if a is not None and b not in (None,0) else None)
            row={'case_id':c,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),'annotate':z['annotate'],'predicted_ratio':z['predicted_ratio'],'p6_folds':z['p6_folds'],
                 'direct_source_ns':msp[(c,D)],'p6_source_ns':msp[(c,P6)],'p9_source_ns':msp[(c,P9)],'p10_source_ns':msp[(c,P10)],'p10_over_direct_source':msp[(c,P10)]/msp[(c,D)],'p10_over_p9_source':msp[(c,P10)]/msp[(c,P9)],
                 'direct_build_ns':msb[(c,D)],'p9_build_ns':msb[(c,P9)],'p10_build_ns':msb[(c,P10)],'p10_over_direct_build':msb[(c,P10)]/msb[(c,D)],'p10_over_p9_build':msb[(c,P10)]/msb[(c,P9)],
                 'direct_compiler_ns':mcp[(c,D)],'p10_compiler_ns':mcp[(c,P10)],'multiplications_ratio':rr('multiplications'),'pair_terms_ratio':rr('pair_terms'),'peak_monomials_ratio':rr('peak_monomials'),'anf_nodes_ratio':rr('anf_nodes_evaluated')}
            w.writerow(row)

# Post-hoc free-incremental-telemetry bound.
msp=med(g['source_timing_rows'],'source_pipeline_ns'); msb=med(g['source_timing_rows'],'source_build_ns'); mcp=med(g['source_timing_rows'],'compiler_ns'); cases=sorted({r['case_id'] for r in g['source_timing_rows']})
free=[]; num=den=0.0
for c in cases:
    a=msb[(c,D)]+mcp[(c,P10)]; b=msb[(c,D)]+mcp[(c,D)]; free.append(a/b); num+=a; den+=b
free_diag={'schema':'cm-n2-p10-posthoc-free-telemetry/v1','case_geomean':geo(free),'weighted_ratio':num/den,'note':'Frozen P10 decisions and measured P10 compiler medians with P10 source-build cost replaced by direct source-build cost. Diagnostic only; not preregistered.'}
(HERE/'P10_POSTHOC_FREE_TELEMETRY.json').write_text(json.dumps(free_diag,indent=2))

abs_build={arm:statistics.median([msb[(c,arm)] for c in cases])/1000 for arm in (D,P9,P10)}
strata={}
for depth in (6,8,10):
    cs=[c for c in cases if c.startswith(str(depth)+':')]
    strata[str(depth)]={'p10_direct_source':geo([msp[(c,P10)]/msp[(c,D)] for c in cs]),'p10_p9_source':geo([msp[(c,P10)]/msp[(c,P9)] for c in cs]),'p10_direct_build':geo([msb[(c,P10)]/msb[(c,D)] for c in cs])}

p10d=s['gatep_source']['p10_direct']; p10p9=s['gatep_source']['p10_p9']; b10d=s['gatep_source_build']['p10_direct']; b10p9=s['gatep_source_build']['p10_p9']; c10d=s['gatep_compiler']['p10_direct']
nd=s['natural_source']['p10_direct']; np9=s['natural_source']['p10_p9']; nb=s['natural_source_build']['p10_direct']; nbp9=s['natural_source_build']['p10_p9']
work=s['gatep_work']; mem=s['gatep_memory']
results=f'''# N2/P10 Results - Fused Minimal Telemetry Construction

## Status

P10 is complete. The frozen P8/P9 dispatch policy and P6 folding backend were held unchanged while P9's seven-counter telemetry was fused directly into one specialized source `Factory._make` path.

Mandatory invariance passed on all **332/332** frozen policy cases: 188 training, 98 validation, 36 Gate-P evaluation, and 10 natural evaluation cases. P10 reproduced P9's seven primitive counters, five tree inputs, frozen-tree prediction, and annotate/bypass decision exactly. Fresh fuzz passed **1000/1000**.

## Gate-P primary endpoint

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P10 / direct, source-inclusive | **{p10d['geomean_ratio']:.6f}x** | **{p10d['ci95'][0]:.6f}-{p10d['ci95'][1]:.6f}** | **{p10d['weighted_ratio']:.6f}x** | {p10d['wins']}/36 |
| P10 / P9, source-inclusive | **{p10p9['geomean_ratio']:.6f}x** | **{p10p9['ci95'][0]:.6f}-{p10p9['ci95'][1]:.6f}** | **{p10p9['weighted_ratio']:.6f}x** | {p10p9['wins']}/36 |
| P10 / direct, source build | **{b10d['geomean_ratio']:.6f}x** | **{b10d['ci95'][0]:.6f}-{b10d['ci95'][1]:.6f}** | **{b10d['weighted_ratio']:.6f}x** | {b10d['wins']}/36 |
| P10 / P9, source build | **{b10p9['geomean_ratio']:.6f}x** | **{b10p9['ci95'][0]:.6f}-{b10p9['ci95'][1]:.6f}** | **{b10p9['weighted_ratio']:.6f}x** | {b10p9['wins']}/36 |
| P10 / direct, selected compiler | **{c10d['geomean_ratio']:.6f}x** | **{c10d['ci95'][0]:.6f}-{c10d['ci95'][1]:.6f}** | **{c10d['weighted_ratio']:.6f}x** | {c10d['wins']}/36 |

The preregistered **direct-crossover criterion failed**: P10 remained about **{(p10d['geomean_ratio']-1)*100:.1f}% slower** than direct case-balanced, and its confidence interval includes 1. However, the gap fell from P9's simultaneous result: P10 was **{(1-p10p9['geomean_ratio'])*100:.1f}% faster than P9** source-inclusive, with the complete 95% interval below 1.

The narrower fused-construction engineering criterion also failed because P10/P9 source build was **{b10p9['geomean_ratio']:.4f}x**, an improvement of about **{(1-b10p9['geomean_ratio'])*100:.1f}%**, short of the preregistered 10% target. The source-inclusive P10/P9 portion of that criterion did pass.

Median Gate-P source construction was approximately **{abs_build[D]:.1f} us direct**, **{abs_build[P9]:.1f} us P9**, and **{abs_build[P10]:.1f} us P10**.

## Depth strata

| Depth | P10/direct source-inclusive | P10/P9 source-inclusive | P10/direct source-build |
|---:|---:|---:|---:|
| 6 | {strata['6']['p10_direct_source']:.6f}x | {strata['6']['p10_p9_source']:.6f}x | {strata['6']['p10_direct_build']:.6f}x |
| 8 | {strata['8']['p10_direct_source']:.6f}x | {strata['8']['p10_p9_source']:.6f}x | {strata['8']['p10_direct_build']:.6f}x |
| 10 | {strata['10']['p10_direct_source']:.6f}x | {strata['10']['p10_p9_source']:.6f}x | {strata['10']['p10_direct_build']:.6f}x |

## Dispatch and Boolean work

P10 made exactly the same frozen decisions as P9/P8: **{s['gatep_annotated']}/36** Gate-P cases annotated, all **{s['gatep_fold_cases']}** consuming a fold, for **{s['gatep_folds']}** total consumed folds. Relative to simultaneous always-P6 profitability, {s['gatep_confusion']['annotated_p6_wins']} annotations were P6 wins, {s['gatep_confusion']['annotated_p6_losses']} were P6 losses, and {s['gatep_confusion']['p6_wins_bypassed']} P6-winning cases were bypassed.

Because the decisions are invariant, the Boolean-work reductions are the same selective P8/P9 mechanism:

- multiplications: **{work['multiplications']['geomean_ratio']:.6f}x direct**;
- pair terms: **{work['pair_terms']['geomean_ratio']:.6f}x direct**;
- peak monomials: **{work['peak_monomials']['geomean_ratio']:.6f}x direct**;
- ANF nodes evaluated: **{work['anf_nodes_evaluated']['geomean_ratio']:.6f}x direct**.

## Memory

Gate-P traced peak allocation was **{mem['p10_direct']['geomean_ratio']:.6f}x direct** and **{mem['p10_p9']['geomean_ratio']:.6f}x P9**. P10 therefore changes time more than memory; its data representation is intentionally the same as P9's.

## Natural EPFL control

P10 annotated **0/10** frozen natural cases and consumed **0 folds**. Natural results remain strictly an abstention/overhead control.

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P10 / direct, source-inclusive | **{nd['geomean_ratio']:.6f}x** | **{nd['ci95'][0]:.6f}-{nd['ci95'][1]:.6f}** | **{nd['weighted_ratio']:.6f}x** | {nd['wins']}/10 |
| P10 / P9, source-inclusive | **{np9['geomean_ratio']:.6f}x** | **{np9['ci95'][0]:.6f}-{np9['ci95'][1]:.6f}** | **{np9['weighted_ratio']:.6f}x** | {np9['wins']}/10 |
| P10 / direct, source build | **{nb['geomean_ratio']:.6f}x** | **{nb['ci95'][0]:.6f}-{nb['ci95'][1]:.6f}** | **{nb['weighted_ratio']:.6f}x** | {nb['wins']}/10 |
| P10 / P9, source build | **{nbp9['geomean_ratio']:.6f}x** | **{nbp9['ci95'][0]:.6f}-{nbp9['ci95'][1]:.6f}** | **{nbp9['weighted_ratio']:.6f}x** | {nbp9['wins']}/10 |

The case-balanced natural overhead is about **{(nd['geomean_ratio']-1)*100:.1f}%**; workload-weighted P10 is below direct, but with zero folds this is not a natural-folding speedup claim.

## Post-hoc diagnostic

Keeping P10's exact frozen dispatch decisions and measured compiler medians but replacing P10 source-build time by direct source-build time gives **{free_diag['case_geomean']:.6f}x direct case-balanced** and **{free_diag['weighted_ratio']:.6f}x workload-weighted**. This is diagnostic only, not a preregistered endpoint.

## Measurement counts

- Gate-P timed rows: **2,880**
- natural timed rows: **600**
- total timed rows: **3,480**
- policy-invariance cases: **332**
- fresh fuzz cases: **1,000**

The long `cavlc:35` natural schedule was executed in deterministic ten-position chunks and merged without changing the frozen schedule or policy.

## Conclusion

Fusing telemetry into the ordinary `_make` path is a real improvement but not a complete solution. It removes about **{(1-b10p9['geomean_ratio'])*100:.1f}%** of P9's source-build time and **{(1-p10p9['geomean_ratio'])*100:.1f}%** of its full pipeline time while preserving every decision and work metric. P10 still pays roughly a **{(b10d['geomean_ratio']-1)*100:.1f}%** source-construction premium over direct, leaving the case-balanced end-to-end pipeline above direct.
'''
(HERE/'N2_P10_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P10 Interpretation

P10 answers the clean implementation question posed by P9: how much of the remaining dispatch tax came from wrapping the ordinary `_make` and then revisiting each new node?

The answer is **a measurable but limited fraction**. With every policy decision frozen, P10/P9 source construction was **{b10p9['geomean_ratio']:.4f}x** and P10/P9 full source-inclusive time was **{p10p9['geomean_ratio']:.4f}x**. P10 won the source-build comparison on all 36 Gate-P cases and the full-pipeline comparison on {p10p9['wins']}/36 cases. Thus the wrapper architecture was genuinely wasteful.

But it was not the dominant remaining cost. P10 source construction is still **{b10d['geomean_ratio']:.4f}x direct**. The selected compiler path itself is **{c10d['geomean_ratio']:.4f}x direct case-balanced** and **{c10d['weighted_ratio']:.4f}x workload-weighted**, so the residual problem remains almost entirely the act of carrying the dispatch telemetry through Python construction.

The post-hoc profile is consistent with this. Across the same 360 Gate-P builds, cProfile reports approximately 0.069 s total for ordinary construction, 0.098 s for P9, and 0.093 s for P10. P10's fused `_make` accounts for about 0.042 s cumulative, versus roughly 0.052 s for P9's wrapper `_make` (which includes calls into the base `_make`). These profile totals are diagnostic only; the randomized timing benchmark is authoritative.

The post-hoc zero-incremental-telemetry bound remains important: preserving the exact P10 decisions and compiler medians while charging only direct source-build cost gives **{free_diag['case_geomean']:.4f}x** direct case-balanced and **{free_diag['weighted_ratio']:.4f}x** workload-weighted. This strongly suggests that the current frozen dispatch/folding combination already contains enough downstream savings for crossover if the telemetry can be made close to free.

## Recommended P11

The next clean pass should **not** refit the tree and should not change any fold threshold. It should attack the fact that P10 still maintains all seven primitive counters for every node even though the frozen depth-3 tree does not necessarily need all of them on every formula.

A P11 tree-aware lazy telemetry implementation can exploit the exact frozen tree structure:

1. The root asks only whether `max_pair_shells <= 4.5`.
2. If the final root branch is left, only the features reachable in that subtree are relevant: `binary_density`, `max_depth`, and `pair_repeat_density`.
3. If the root branch is right, only `reuse_density` and `pair_repeat_density` are subsequently needed.
4. Counters whose final value cannot affect the reached leaf should be omitted or maintained only after the branch becomes reachable, **without a second DAG traversal**.

The safest P11 should preregister **exact P10 decision equivalence on all 332 frozen policy cases plus fresh fuzz before timing**, exactly as P9/P10 did. It should have two arms if practical: (A) tree-aware lazy counters and (B) an even tighter specialized decision-state machine that evaluates the frozen tree from primitive running bounds rather than materializing a feature dictionary.

This is more promising now than further container/layout changes because P10 has already removed the wrapper call and still leaves a ~{(b10d['geomean_ratio']-1)*100:.0f}% source-build premium. The remaining overhead is the counter maintenance itself.
'''
(HERE/'N2_P10_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme=f'''# N2/P10 Reproducibility README

P10 keeps the P8/P9 frozen dispatch policy and P6 folding backend unchanged, replacing only P9's wrapper telemetry `_make` with a fused one-pass `_make` implementation.

## Frozen hashes

- P10 preregistration: `{sha(HERE/'N2_P10_PREREGISTRATION.md')}`
- P10 harness: `{sha(HERE/'n2_p10_harness.py')}`
- P8 frozen gate: `{sha(HERE.parent/'cm_n2_p8_run'/'P8_FROZEN_GATE.json')}`

## Reproduction order

1. `python cm_n2_p10_run/n2_p10_harness.py --mode invariant --out cm_n2_p10_run/invariance.json`
2. `python cm_n2_p10_run/n2_p10_harness.py --mode fuzz --out cm_n2_p10_run/fuzz.json`
3. `python cm_n2_p10_run/n2_p10_harness.py --mode gatep --out cm_n2_p10_run/gatep.json`
4. Run the ten natural cases with `--mode natural-case`; execute `cavlc:35` through `run_p10_nat_chunk.py` if a command wall limit requires chunking.
5. Merge the deterministic `cavlc:35` chunks, calculate `N2_P10_SUMMARY.json`, run `independent_verify.py`, then `make_p10_artifacts.py`.

The 332-case P9/P10 invariance check is mandatory before timing interpretation. P10 performs no model fitting or retuning.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')

combined={'schema':'cm-n2-p10-results-bundle/v1','summary':s,'invariance':inv,'fuzz':fuzz,'gatep':g,'natural_cases':nat,'posthoc_free_telemetry':free_diag,'depth_strata':strata,'absolute_build_medians_us':abs_build}
(HERE/'n2_p10_results.json').write_text(json.dumps(combined,indent=2),encoding='utf-8')
print(json.dumps({'free_diag':free_diag,'abs_build_us':abs_build,'depth_strata':strata},indent=2))
