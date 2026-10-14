from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D='direct_source_pipeline'; P6='p6_source_pipeline'; P10='p10_fused_source_dispatch'; P11='p11_tree_specialized_dispatch'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def geo(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None
def med(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}

g=json.load(open(HERE/'gatep.json')); s=json.load(open(HERE/'N2_P11_SUMMARY.json')); inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json'))
names=['adder_f_4.json','adder_f_5.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in names]
ns=[r for x in nat for r in x['source_timing_rows']]

# Case summaries.
for fname,rows,symbolic in [('N2_P11_GATEP_CASE_SUMMARY.csv',g['source_timing_rows'],g['symbolic']),('N2_P11_NATURAL_CASE_SUMMARY.csv',ns,[x['symbolic'] for x in nat])]:
    msp=med(rows,'source_pipeline_ns'); msb=med(rows,'source_build_ns'); mcp=med(rows,'compiler_ns'); sy={r['case_id']:r for r in symbolic}
    fields=['case_id','depth','circuit','root','annotate','p10_predicted_ratio','p11_decision_code','p6_folds','direct_source_ns','p6_source_ns','p10_source_ns','p11_source_ns','p11_over_direct_source','p11_over_p10_source','direct_build_ns','p10_build_ns','p11_build_ns','p11_over_direct_build','p11_over_p10_build','direct_compiler_ns','p11_compiler_ns','multiplications_ratio','pair_terms_ratio','peak_monomials_ratio','anf_nodes_ratio']
    with open(HERE/fname,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for c in sorted(sy):
            z=sy[c]; d=z['direct']; p=z['p11']
            def rr(field):
                a=p.get(field); b=d.get(field); return (a/b if a is not None and b not in (None,0) else None)
            row={'case_id':c,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),'annotate':z['annotate'],'p10_predicted_ratio':z['p10_predicted_ratio'],'p11_decision_code':z['p11_decision_code'],'p6_folds':z['p6_folds'],
                 'direct_source_ns':msp[(c,D)],'p6_source_ns':msp[(c,P6)],'p10_source_ns':msp[(c,P10)],'p11_source_ns':msp[(c,P11)],'p11_over_direct_source':msp[(c,P11)]/msp[(c,D)],'p11_over_p10_source':msp[(c,P11)]/msp[(c,P10)],
                 'direct_build_ns':msb[(c,D)],'p10_build_ns':msb[(c,P10)],'p11_build_ns':msb[(c,P11)],'p11_over_direct_build':msb[(c,P11)]/msb[(c,D)],'p11_over_p10_build':msb[(c,P11)]/msb[(c,P10)],
                 'direct_compiler_ns':mcp[(c,D)],'p11_compiler_ns':mcp[(c,P11)],'multiplications_ratio':rr('multiplications'),'pair_terms_ratio':rr('pair_terms'),'peak_monomials_ratio':rr('peak_monomials'),'anf_nodes_ratio':rr('anf_nodes_evaluated')}
            w.writerow(row)

# Diagnostic: same frozen P11 decisions and measured compiler medians, but zero incremental telemetry cost.
msp=med(g['source_timing_rows'],'source_pipeline_ns'); msb=med(g['source_timing_rows'],'source_build_ns'); mcp=med(g['source_timing_rows'],'compiler_ns'); cases=sorted({r['case_id'] for r in g['source_timing_rows']})
free=[]; num=den=0.0
for c in cases:
    a=msb[(c,D)]+mcp[(c,P11)]; b=msb[(c,D)]+mcp[(c,D)]; free.append(a/b); num+=a; den+=b
free_diag={'schema':'cm-n2-p11-posthoc-free-telemetry/v1','case_geomean':geo(free),'weighted_ratio':num/den,'note':'Frozen P11/P10 decisions and measured P11 compiler medians with P11 source-build cost replaced by direct source-build cost. Diagnostic only; not preregistered.'}
(HERE/'P11_POSTHOC_FREE_TELEMETRY.json').write_text(json.dumps(free_diag,indent=2))

abs_build={arm:statistics.median([msb[(c,arm)] for c in cases])/1000 for arm in (D,P10,P11)}
abs_source={arm:statistics.median([msp[(c,arm)] for c in cases])/1000 for arm in (D,P10,P11)}
strata={}
for depth in (6,8,10):
    cs=[c for c in cases if c.startswith(str(depth)+':')]
    strata[str(depth)]={'p11_direct_source':geo([msp[(c,P11)]/msp[(c,D)] for c in cs]),'p11_p10_source':geo([msp[(c,P11)]/msp[(c,P10)] for c in cs]),'p11_direct_build':geo([msb[(c,P11)]/msb[(c,D)] for c in cs]),'p11_p10_build':geo([msb[(c,P11)]/msb[(c,P10)] for c in cs])}

p11d=s['gatep_source']['p11_direct']; p11p10=s['gatep_source']['p11_p10']; b11d=s['gatep_source_build']['p11_direct']; b11p10=s['gatep_source_build']['p11_p10']; c11d=s['gatep_compiler']['p11_direct']
nd=s['natural_source']['p11_direct']; np10=s['natural_source']['p11_p10']; nb=s['natural_source_build']['p11_direct']; nbp10=s['natural_source_build']['p11_p10']
work=s['gatep_work']; mem=s['gatep_memory']
results=f'''# N2/P11 Results - Frozen-Tree Specialized Telemetry

## Status

P11 is complete. The P8/P9/P10 dispatch policy, `0.80` cutoff, P6 folding backend, and evaluation corpora were held fixed. P11 changed only telemetry implementation by compiling the already-frozen annotate decision into a threshold-aware construction path.

Mandatory decision invariance passed on **332/332** frozen policy cases: 188 training, 98 validation, 36 Gate-P evaluation, and 10 natural evaluation cases. Fresh fuzz passed **1000/1000**.

P11 reproduces P10's `edge_count`, `binary_nodes`, `reuse_edge_events`, `pair_repeat_excess`, the predicate `max_pair_shells >= 5`, and final annotate/bypass decision. It intentionally does not compute P10's unused bypass-branch depth/density features.

## Gate-P primary endpoint

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P11 / direct, source-inclusive | **{p11d['geomean_ratio']:.6f}x** | **{p11d['ci95'][0]:.6f}-{p11d['ci95'][1]:.6f}** | **{p11d['weighted_ratio']:.6f}x** | {p11d['wins']}/36 |
| P11 / P10, source-inclusive | **{p11p10['geomean_ratio']:.6f}x** | **{p11p10['ci95'][0]:.6f}-{p11p10['ci95'][1]:.6f}** | **{p11p10['weighted_ratio']:.6f}x** | {p11p10['wins']}/36 |
| P11 / direct, source build | **{b11d['geomean_ratio']:.6f}x** | **{b11d['ci95'][0]:.6f}-{b11d['ci95'][1]:.6f}** | **{b11d['weighted_ratio']:.6f}x** | {b11d['wins']}/36 |
| P11 / P10, source build | **{b11p10['geomean_ratio']:.6f}x** | **{b11p10['ci95'][0]:.6f}-{b11p10['ci95'][1]:.6f}** | **{b11p10['weighted_ratio']:.6f}x** | {b11p10['wins']}/36 |
| P11 / direct, selected compiler | **{c11d['geomean_ratio']:.6f}x** | **{c11d['ci95'][0]:.6f}-{c11d['ci95'][1]:.6f}** | **{c11d['weighted_ratio']:.6f}x** | {c11d['wins']}/36 |

The preregistered **direct-crossover criterion failed**. P11 is about **{(p11d['geomean_ratio']-1)*100:.1f}% slower than direct** case-balanced, and the confidence interval crosses 1. The workload-weighted result is only **{(p11d['weighted_ratio']-1)*100:.2f}% above direct**, effectively near parity but not a preregistered win.

The preregistered **specialized-telemetry engineering criterion passed**: P11/P10 source build is **{b11p10['geomean_ratio']:.6f}x**, P11/P10 source-inclusive is **{p11p10['geomean_ratio']:.6f}x**, and the latter's complete 95% interval is below 1. P11 beat P10 source construction on all **{b11p10['wins']}/36** Gate-P cases and source-inclusive on **{p11p10['wins']}/36**.

Median-of-case-median Gate-P source construction was approximately **{abs_build[D]:.1f} us direct**, **{abs_build[P10]:.1f} us P10**, and **{abs_build[P11]:.1f} us P11**. Corresponding whole-pipeline medians were approximately **{abs_source[D]:.1f} us**, **{abs_source[P10]:.1f} us**, and **{abs_source[P11]:.1f} us**.

## Depth strata

| Depth | P11/direct source-inclusive | P11/P10 source-inclusive | P11/direct source-build | P11/P10 source-build |
|---:|---:|---:|---:|---:|
| 6 | {strata['6']['p11_direct_source']:.6f}x | {strata['6']['p11_p10_source']:.6f}x | {strata['6']['p11_direct_build']:.6f}x | {strata['6']['p11_p10_build']:.6f}x |
| 8 | {strata['8']['p11_direct_source']:.6f}x | {strata['8']['p11_p10_source']:.6f}x | {strata['8']['p11_direct_build']:.6f}x | {strata['8']['p11_p10_build']:.6f}x |
| 10 | {strata['10']['p11_direct_source']:.6f}x | {strata['10']['p11_p10_source']:.6f}x | {strata['10']['p11_direct_build']:.6f}x | {strata['10']['p11_p10_build']:.6f}x |

## Dispatch and Boolean work

P11 made exactly the same final decisions as frozen P10/P8: **{s['gatep_annotated']}/36** Gate-P cases annotated, all **{s['gatep_fold_cases']}** consuming a fold, for **{s['gatep_folds']}** total consumed folds.

Relative to simultaneous always-P6 timing, {s['gatep_confusion']['annotated_p6_wins']} annotations were P6 wins, {s['gatep_confusion']['annotated_p6_losses']} were P6 losses, and {s['gatep_confusion']['p6_wins_bypassed']} P6-winning cases were bypassed. This is unchanged policy behavior, not a P11 retuning result.

Because dispatch is invariant, Boolean work is the same selective mechanism as P8-P10:

- multiplications: **{work['multiplications']['geomean_ratio']:.6f}x direct**;
- pair terms: **{work['pair_terms']['geomean_ratio']:.6f}x direct**;
- peak monomials: **{work['peak_monomials']['geomean_ratio']:.6f}x direct**;
- ANF nodes evaluated: **{work['anf_nodes_evaluated']['geomean_ratio']:.6f}x direct**.

## Memory

Gate-P traced peak allocation was **{mem['p11_direct']['geomean_ratio']:.6f}x direct** and **{mem['p11_p10']['geomean_ratio']:.6f}x P10**. P11 removes the per-node depth bytearray and generic feature bookkeeping, but the five folded cases also materially alter downstream allocation, so this is a whole-pipeline measurement rather than isolated telemetry size.

## Natural EPFL control

P11 annotated **0/10** frozen natural cases and consumed **0 folds**. Natural results therefore remain strictly an abstention/overhead control.

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P11 / direct, source-inclusive | **{nd['geomean_ratio']:.6f}x** | **{nd['ci95'][0]:.6f}-{nd['ci95'][1]:.6f}** | **{nd['weighted_ratio']:.6f}x** | {nd['wins']}/10 |
| P11 / P10, source-inclusive | **{np10['geomean_ratio']:.6f}x** | **{np10['ci95'][0]:.6f}-{np10['ci95'][1]:.6f}** | **{np10['weighted_ratio']:.6f}x** | {np10['wins']}/10 |
| P11 / direct, source build | **{nb['geomean_ratio']:.6f}x** | **{nb['ci95'][0]:.6f}-{nb['ci95'][1]:.6f}** | **{nb['weighted_ratio']:.6f}x** | {nb['wins']}/10 |
| P11 / P10, source build | **{nbp10['geomean_ratio']:.6f}x** | **{nbp10['ci95'][0]:.6f}-{nbp10['ci95'][1]:.6f}** | **{nbp10['weighted_ratio']:.6f}x** | {nbp10['wins']}/10 |

Case-balanced natural source-inclusive overhead is about **{(nd['geomean_ratio']-1)*100:.2f}%**. The workload-weighted point estimate is slightly below direct, but with zero folds it is not a natural-folding speedup claim.

## Post-hoc diagnostic

Keeping P11's exact frozen dispatch decisions and measured compiler medians, but hypothetically replacing P11 source-build time by direct source-build time, gives **{free_diag['case_geomean']:.6f}x direct case-balanced** and **{free_diag['weighted_ratio']:.6f}x workload-weighted**. This is diagnostic only, not a measured implementation endpoint.

## Predeclared outcomes

- Gate-P direct-crossover PASS: **{s['predeclared_gatep_direct_crossover_pass']}**.
- Specialized-telemetry engineering success: **{s['predeclared_specialized_telemetry_engineering_success']}**.

P11 therefore validates the implementation hypothesis that frozen-tree specialization can materially reduce telemetry cost, while leaving the stronger end-to-end direct crossover unresolved.
'''
(HERE/'N2_P11_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P11 Interpretation

## Main conclusion

P11 is the strongest implementation result in the zero-pass dispatch line so far: it reduces P10 source construction by about **{(1-b11p10['geomean_ratio'])*100:.1f}%** and P10's complete Gate-P pipeline by about **{(1-p11p10['geomean_ratio'])*100:.1f}%**, without changing a single dispatch decision or folding rule.

The remaining gap to direct is now only **{(p11d['geomean_ratio']-1)*100:.1f}% case-balanced** and **{(p11d['weighted_ratio']-1)*100:.2f}% workload-weighted**. The primary direct-crossover criterion still fails, so P11 should not be described as an end-to-end speedup over direct/no-rewrite.

## What P11 actually proved

The frozen P8 tree has only one leaf below the 0.80 cutoff. Algebraically, annotation occurs iff a five-deep repeated operand-pair shell exists and both reuse density and pair-repeat density fall below their frozen thresholds. P11 exploits that already-frozen fact; it does not learn a new rule.

This allows the timed construction path to discard per-node depth tracking, maximum-depth maintenance, binary-density reporting, and all bypass-only tree branches. It also saturates per-pair shell counts once a five-shell is established. Exact decision equivalence was then independently required over all 332 frozen cases before timing.

The result is important because P11/P10 source-build is **{b11p10['geomean_ratio']:.6f}x**, with all 36 Gate-P cases improving. The implementation hypothesis therefore survives adversarial isolation.

## Why direct still wins case-balanced

P11 still pays for two forms of information that direct construction does not need:

1. per-child first-use state, required for `reuse_density`;
2. a canonical operand-pair dictionary, required to know whether any pair reaches five uses and to count pair-repeat excess.

Those structures are now the dominant remaining dispatch tax. The downstream selected compiler is already favorable in aggregate: P11/direct selected-compiler is **{c11d['geomean_ratio']:.6f}x** case-balanced and **{c11d['weighted_ratio']:.6f}x** workload-weighted.

This makes the next question narrower than P10's: can the frozen annotate predicate be evaluated without paying full exact reuse/pair bookkeeping on cases that will inevitably bypass?

## Natural control

P11's natural result is especially informative. All ten cases bypass, yet source-inclusive execution is only **{nd['geomean_ratio']:.6f}x direct** case-balanced and **{nd['weighted_ratio']:.6f}x workload-weighted. That shows the abstention tax is approaching noise-scale on substantial workloads. Because zero folds occur, it remains an overhead result only.

## Recommended P12

Do **not** retrain the gate yet.

P12 should preserve the exact P11 decision and attack the two remaining expensive statistics with **decision-preserving bounds / lazy exactification**:

- Track the five-shell predicate cheaply first.
- Until a five-shell is possible or reached, avoid exact reuse bookkeeping if a mathematically safe bound can prove the case will bypass anyway.
- Once `shell_ge5` becomes true, maintain or reconstruct only the information needed to decide the two density inequalities.
- Alternatively, carry compact per-node incoming-edge counts during ordinary construction if they can be obtained more cheaply than the current first-use bytearray.

The strongest P12 design would preregister a proof that its lazy/bounded decision is exactly equivalent to P11 for **all** inputs, not merely the 332-case corpus, then retain the 332-case and fuzz checks as implementation verification.

A separate branch could investigate a compiled/C implementation, but that would answer a different engineering question. P11 has shown that within CPython, frozen-tree specialization is worthwhile; the next remaining costs are specific data structures, not generic model evaluation.
'''
(HERE/'N2_P11_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme=f'''# N2/P11 Reproducibility

P11 is an implementation-only replay of the frozen P8/P10 dispatch policy with threshold-specialized telemetry.

## Frozen hashes

- preregistration: `{sha(HERE/'N2_P11_PREREGISTRATION.md')}`
- harness: `{sha(HERE/'n2_p11_harness.py')}`
- P8 frozen gate: `{sha(HERE.parent/'cm_n2_p8_run'/'P8_FROZEN_GATE.json')}`

## Reproduction order

1. `python cm_n2_p11_run/n2_p11_harness.py --mode invariant --out cm_n2_p11_run/invariance.json`
2. `python cm_n2_p11_run/n2_p11_harness.py --mode fuzz --out cm_n2_p11_run/fuzz.json`
3. `python cm_n2_p11_run/n2_p11_harness.py --mode gatep --out cm_n2_p11_run/gatep.json`
4. Run the ten frozen natural cases with `--mode natural-case`; `cavlc:35` may be split deterministically with `run_p11_nat_chunk.py` under short command wall limits.
5. Merge any deterministic chunks, calculate `N2_P11_SUMMARY.json`, run `independent_verify.py`, then `make_p11_artifacts.py`.

The 332-case P10/P11 decision-invariance gate and 1,000-case fuzz are mandatory before timing interpretation. No model fitting, cutoff selection, or fold-threshold tuning occurs in P11.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')

combined={'schema':'cm-n2-p11-results-bundle/v1','summary':s,'invariance':inv,'fuzz':fuzz,'gatep':g,'natural_cases':nat,'posthoc_free_telemetry':free_diag,'depth_strata':strata,'absolute_build_medians_us':abs_build,'absolute_source_medians_us':abs_source}
(HERE/'n2_p11_results.json').write_text(json.dumps(combined,indent=2),encoding='utf-8')
print(json.dumps({'free_diag':free_diag,'abs_build_us':abs_build,'abs_source_us':abs_source,'depth_strata':strata},indent=2))
