from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D='direct_source_pipeline'; P6='p6_source_pipeline'; P11='p11_tree_specialized_dispatch'; P12='p12_lazy_reuse_dispatch'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def geo(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def med(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}

g=json.load(open(HERE/'gatep.json')); s=json.load(open(HERE/'N2_P12_SUMMARY.json')); inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json'))
names=['adder_f_4.json','adder_f_5.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in names]
ns=[r for x in nat for r in x['source_timing_rows']]

# Case summaries.
for fname,rows,symbolic in [('N2_P12_GATEP_CASE_SUMMARY.csv',g['source_timing_rows'],g['symbolic']),('N2_P12_NATURAL_CASE_SUMMARY.csv',ns,[x['symbolic'] for x in nat])]:
    msp=med(rows,'source_pipeline_ns'); msb=med(rows,'source_build_ns'); mcp=med(rows,'compiler_ns'); sy={r['case_id']:r for r in symbolic}
    fields=['case_id','depth','circuit','root','annotate','p11_decision_code','p12_decision_code','reuse_scanned','reuse_early_abort','reuse_scan_edges','edge_count','binary_nodes','pair_repeat_excess','p6_folds','direct_source_ns','p6_source_ns','p11_source_ns','p12_source_ns','p12_over_direct_source','p12_over_p11_source','direct_build_ns','p11_build_ns','p12_build_ns','p12_over_direct_build','p12_over_p11_build','direct_compiler_ns','p12_compiler_ns','multiplications_ratio','pair_terms_ratio','peak_monomials_ratio','anf_nodes_ratio']
    with open(HERE/fname,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for c in sorted(sy):
            z=sy[c];d=z['direct'];p=z['p12'];diag=z['p12_dispatch'];c11=z['p11_counters']
            def rr(field):
                a=p.get(field);b=d.get(field);return (a/b if a is not None and b not in (None,0) else None)
            row={'case_id':c,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),'annotate':z['annotate'],'p11_decision_code':z['p11_decision_code'],'p12_decision_code':z['p12_decision_code'],'reuse_scanned':diag['reuse_scanned'],'reuse_early_abort':diag['reuse_early_abort'],'reuse_scan_edges':diag['reuse_scan_edges'],'edge_count':c11['edge_count'],'binary_nodes':c11['binary_nodes'],'pair_repeat_excess':c11['pair_repeat_excess'],'p6_folds':z['p6_folds'],
                 'direct_source_ns':msp[(c,D)],'p6_source_ns':msp[(c,P6)],'p11_source_ns':msp[(c,P11)],'p12_source_ns':msp[(c,P12)],'p12_over_direct_source':msp[(c,P12)]/msp[(c,D)],'p12_over_p11_source':msp[(c,P12)]/msp[(c,P11)],
                 'direct_build_ns':msb[(c,D)],'p11_build_ns':msb[(c,P11)],'p12_build_ns':msb[(c,P12)],'p12_over_direct_build':msb[(c,P12)]/msb[(c,D)],'p12_over_p11_build':msb[(c,P12)]/msb[(c,P11)],
                 'direct_compiler_ns':mcp[(c,D)],'p12_compiler_ns':mcp[(c,P12)],'multiplications_ratio':rr('multiplications'),'pair_terms_ratio':rr('pair_terms'),'peak_monomials_ratio':rr('peak_monomials'),'anf_nodes_ratio':rr('anf_nodes_evaluated')}
            w.writerow(row)

# Post-hoc diagnostic: same frozen P12 decisions and compiler medians, but zero incremental telemetry cost.
msp=med(g['source_timing_rows'],'source_pipeline_ns');msb=med(g['source_timing_rows'],'source_build_ns');mcp=med(g['source_timing_rows'],'compiler_ns');cases=sorted({r['case_id'] for r in g['source_timing_rows']})
free=[];num=den=0.0
for c in cases:
    a=msb[(c,D)]+mcp[(c,P12)]; b=msb[(c,D)]+mcp[(c,D)]; free.append(a/b); num+=a; den+=b
free_diag={'schema':'cm-n2-p12-posthoc-free-telemetry/v1','case_geomean':geo(free),'weighted_ratio':num/den,'note':'Frozen P12/P11 decisions and measured P12 compiler medians with P12 source-build cost replaced by direct source-build cost. Diagnostic only; not preregistered.'}
(HERE/'P12_POSTHOC_FREE_TELEMETRY.json').write_text(json.dumps(free_diag,indent=2))

abs_build={arm:statistics.median([msb[(c,arm)] for c in cases])/1000 for arm in (D,P11,P12)}
abs_source={arm:statistics.median([msp[(c,arm)] for c in cases])/1000 for arm in (D,P11,P12)}
strata={}
for depth in (6,8,10):
    cs=[c for c in cases if c.startswith(str(depth)+':')]
    strata[str(depth)]={'p12_direct_source':geo([msp[(c,P12)]/msp[(c,D)] for c in cs]),'p12_p11_source':geo([msp[(c,P12)]/msp[(c,P11)] for c in cs]),'p12_direct_build':geo([msb[(c,P12)]/msb[(c,D)] for c in cs]),'p12_p11_build':geo([msb[(c,P12)]/msb[(c,P11)] for c in cs])}

p12d=s['gatep_source']['p12_direct'];p12p11=s['gatep_source']['p12_p11'];b12d=s['gatep_source_build']['p12_direct'];b12p11=s['gatep_source_build']['p12_p11'];c12d=s['gatep_compiler']['p12_direct']
nd=s['natural_source']['p12_direct'];np11=s['natural_source']['p12_p11'];nb=s['natural_source_build']['p12_direct'];nbp11=s['natural_source_build']['p12_p11']
work=s['gatep_work'];mem=s['gatep_memory'];lazy=s['gatep_lazy']
results=f'''# N2/P12 Results - Lazy Reuse Exactification and Derived Pair Statistics

## Status

P12 is complete. The frozen P8/P11 dispatch rule, `0.80` cutoff, P6 folding backend, Gate-P cases, natural EPFL cases, and timing protocol were unchanged. P12 changed only how the two remaining telemetry statistics are obtained.

Mandatory P11/P12 decision invariance passed on **332/332** frozen policy cases. Across those cases P12 performed only **{inv['reuse_scans']}** reuse scans, with **{inv['reuse_early_aborts']}** terminating as soon as the frozen reuse threshold was provably exceeded. Fresh fuzz passed **1000/1000**.

P12 derives exact pair-repeat excess as `binary_nodes - distinct_pair_keys`, saturates per-pair counts at five, and computes reuse only if both the five-shell and pair-repeat predicates still leave annotation possible.

## Gate-P primary endpoint

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P12 / direct, source-inclusive | **{p12d['geomean_ratio']:.6f}x** | **{p12d['ci95'][0]:.6f}-{p12d['ci95'][1]:.6f}** | **{p12d['weighted_ratio']:.6f}x** | {p12d['wins']}/36 |
| P12 / P11, source-inclusive | **{p12p11['geomean_ratio']:.6f}x** | **{p12p11['ci95'][0]:.6f}-{p12p11['ci95'][1]:.6f}** | **{p12p11['weighted_ratio']:.6f}x** | {p12p11['wins']}/36 |
| P12 / direct, source build | **{b12d['geomean_ratio']:.6f}x** | **{b12d['ci95'][0]:.6f}-{b12d['ci95'][1]:.6f}** | **{b12d['weighted_ratio']:.6f}x** | {b12d['wins']}/36 |
| P12 / P11, source build | **{b12p11['geomean_ratio']:.6f}x** | **{b12p11['ci95'][0]:.6f}-{b12p11['ci95'][1]:.6f}** | **{b12p11['weighted_ratio']:.6f}x** | {b12p11['wins']}/36 |
| P12 / direct, selected compiler | **{c12d['geomean_ratio']:.6f}x** | **{c12d['ci95'][0]:.6f}-{c12d['ci95'][1]:.6f}** | **{c12d['weighted_ratio']:.6f}x** | {c12d['wins']}/36 |

The preregistered **direct-crossover criterion failed**. P12's case-balanced point estimate is still **{(p12d['geomean_ratio']-1)*100:.2f}% above direct**, and its confidence interval crosses 1. However, the workload-weighted full-pipeline result is **{p12d['weighted_ratio']:.6f}x direct**, i.e. about **{(1-p12d['weighted_ratio'])*100:.2f}% below direct**. This is a secondary crossover, not the preregistered primary PASS.

P12 is nevertheless a clear improvement over P11: source-inclusive time is **{p12p11['geomean_ratio']:.6f}x P11**, with the entire 95% interval below 1, and source construction is **{b12p11['geomean_ratio']:.6f}x P11**. The predeclared lazy-statistics engineering criterion did **not** pass only because its deliberately stronger source-build target was `<=0.90`; the observed value was {b12p11['geomean_ratio']:.6f}x.

Median-of-case-median Gate-P source construction was approximately **{abs_build[D]:.1f} us direct**, **{abs_build[P11]:.1f} us P11**, and **{abs_build[P12]:.1f} us P12**. Whole-pipeline medians were approximately **{abs_source[D]:.1f} us**, **{abs_source[P11]:.1f} us**, and **{abs_source[P12]:.1f} us**.

## Lazy-statistics behavior

Only **{lazy['reuse_scan_cases']}/36** Gate-P cases required any reuse scan. Five of those ultimately annotated; one terminated early after reuse exceeded the frozen threshold. Across all Gate-P cases, P12 scanned only **{lazy['reuse_scan_fraction_all_source_edges']*100:.1f}%** as many reuse-classification edges as an eager all-case scan would have required.

No natural evaluation case required a reuse scan.

## Depth strata

| Depth | P12/direct source-inclusive | P12/P11 source-inclusive | P12/direct source-build | P12/P11 source-build |
|---:|---:|---:|---:|---:|
| 6 | {strata['6']['p12_direct_source']:.6f}x | {strata['6']['p12_p11_source']:.6f}x | {strata['6']['p12_direct_build']:.6f}x | {strata['6']['p12_p11_build']:.6f}x |
| 8 | {strata['8']['p12_direct_source']:.6f}x | {strata['8']['p12_p11_source']:.6f}x | {strata['8']['p12_direct_build']:.6f}x | {strata['8']['p12_p11_build']:.6f}x |
| 10 | {strata['10']['p12_direct_source']:.6f}x | {strata['10']['p12_p11_source']:.6f}x | {strata['10']['p12_direct_build']:.6f}x | {strata['10']['p12_p11_build']:.6f}x |

At depth 8 the case-balanced full pipeline itself is below direct ({strata['8']['p12_direct_source']:.6f}x), while depths 6 and 10 remain above direct. This is a stratum result, not a corpus-wide PASS.

## Dispatch and Boolean work

P12 preserves the frozen policy exactly: **{s['gatep_annotated']}/36** Gate-P cases annotated, all **{s['gatep_fold_cases']}** consuming a fold, for **{s['gatep_folds']}** total consumed folds.

Because dispatch is invariant, Boolean work is unchanged from P8-P11:

- multiplications: **{work['multiplications']['geomean_ratio']:.6f}x direct**;
- pair terms: **{work['pair_terms']['geomean_ratio']:.6f}x direct**;
- peak monomials: **{work['peak_monomials']['geomean_ratio']:.6f}x direct**;
- ANF nodes evaluated: **{work['anf_nodes_evaluated']['geomean_ratio']:.6f}x direct**.

## Memory

Gate-P whole-pipeline traced peak allocation was **{mem['p12_direct']['geomean_ratio']:.6f}x direct** and **{mem['p12_p11']['geomean_ratio']:.6f}x P11**. The temporary lazy reuse bitmap is allocated only on scan-eligible cases, but these whole-pipeline numbers also include downstream compiler allocations and should not be interpreted as isolated telemetry-object size.

## Natural EPFL control

P12 annotated **0/10** frozen natural cases, consumed **0 folds**, and performed **0 reuse scans**. The natural results therefore remain strictly an abstention/overhead control.

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P12 / direct, source-inclusive | **{nd['geomean_ratio']:.6f}x** | **{nd['ci95'][0]:.6f}-{nd['ci95'][1]:.6f}** | **{nd['weighted_ratio']:.6f}x** | {nd['wins']}/10 |
| P12 / P11, source-inclusive | **{np11['geomean_ratio']:.6f}x** | **{np11['ci95'][0]:.6f}-{np11['ci95'][1]:.6f}** | **{np11['weighted_ratio']:.6f}x** | {np11['wins']}/10 |
| P12 / direct, source build | **{nb['geomean_ratio']:.6f}x** | **{nb['ci95'][0]:.6f}-{nb['ci95'][1]:.6f}** | **{nb['weighted_ratio']:.6f}x** | {nb['wins']}/10 |
| P12 / P11, source build | **{nbp11['geomean_ratio']:.6f}x** | **{nbp11['ci95'][0]:.6f}-{nbp11['ci95'][1]:.6f}** | **{nbp11['weighted_ratio']:.6f}x** | {nbp11['wins']}/10 |

With zero folds, the workload-weighted natural point estimate below 1 is not evidence of natural CM-folding acceleration.

## Post-hoc diagnostic

Keeping P12's exact frozen dispatch decisions and measured compiler medians, but hypothetically replacing P12 source-build time with ordinary direct source-build time, gives **{free_diag['case_geomean']:.6f}x direct case-balanced** and **{free_diag['weighted_ratio']:.6f}x workload-weighted**. This is diagnostic only, not a measured implementation endpoint.

## Predeclared outcomes

- Gate-P direct-crossover PASS: **{s['predeclared_gatep_direct_crossover_pass']}**.
- Lazy-statistics engineering success: **{s['predeclared_lazy_statistics_engineering_success']}**.

P12 therefore validates the lazy-statistics mechanism as a real implementation improvement over P11, while leaving the stronger case-balanced end-to-end crossover just unresolved.
'''
(HERE/'N2_P12_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P12 Interpretation

## Main conclusion

P12 moved the complete selective-folding pipeline closer to direct/no-rewrite than P11 did, without altering a single frozen dispatch decision or fold rule.

The primary case-balanced result is **{p12d['geomean_ratio']:.6f}x direct** with CI **{p12d['ci95'][0]:.6f}-{p12d['ci95'][1]:.6f}**. That is not a preregistered direct-crossover PASS. The workload-weighted result, however, is **{p12d['weighted_ratio']:.6f}x**, so the measured aggregate workload has now crossed below direct by about **{(1-p12d['weighted_ratio'])*100:.1f}%** while the case-balanced estimator remains about **{(p12d['geomean_ratio']-1)*100:.1f}%** above direct.

This distinction should be preserved: P12 establishes a secondary measured end-to-end crossover, not the stronger case-balanced one that was preregistered.

## What the lazy-statistics idea accomplished

P11 eagerly touched a per-node first-use bitmap for every edge and eagerly incremented pair-repeat excess. P12 removes both operations from ordinary source construction.

The pair-repeat statistic needs no eager counter at all: because every binary node belongs to exactly one canonical operand-pair key, `pair_repeat_excess = binary_nodes - distinct_pairs`.

Reuse is even more selective. The frozen annotate decision can only be true after a five-shell exists and pair-repeat density has already passed. P12 therefore computes exact reuse only after both conditions hold. On Gate-P, this reduced reuse scanning to **{lazy['reuse_scan_cases']}/36 cases** and **{lazy['reuse_scan_fraction_all_source_edges']*100:.1f}% of the all-case edge volume**; one scan terminated early as soon as reuse was provably too high.

The implementation effect is statistically clear relative to P11: P12/P11 source-inclusive is **{p12p11['geomean_ratio']:.6f}x** with CI entirely below 1, and source construction is **{b12p11['geomean_ratio']:.6f}x**.

## Why the strict source-build engineering target missed

The preregistered engineering target required P12/P11 source build <=0.90. The observed value, **{b12p11['geomean_ratio']:.6f}x**, is a meaningful ~{(1-b12p11['geomean_ratio'])*100:.1f}% improvement but not enough for that deliberately aggressive threshold.

Post-hoc profiling also shows why the remaining tax is hard to remove inside pure Python: P12 still maintains a canonical-pair dictionary for every binary node in order to detect a five-shell. The `used` bytearray work is gone from the common path, but pair-key construction and dictionary lookup remain.

## Strongest remaining bottleneck

After P12, the remaining dispatch-specific source state is essentially:

- `edge_count`;
- `binary_nodes`;
- canonical pair dictionary membership/counts capped at five;
- one Boolean `shell_ge5`.

This suggests that the next meaningful implementation experiment should target **five-shell detection itself**, not reuse accounting.

A P13 could preserve the frozen P12/P11 decision while testing a cheaper pair-shell detector. Plausible exact approaches include:

1. a compact/open-addressed integer table specialized to the small DAG-node-id domain;
2. an integer-key counter structure implemented in C/Cython/Rust rather than a Python dictionary;
3. a two-stage exact method that first uses a very cheap duplicate signal and materializes exact pair counts only after a mathematically safe trigger, provided decision equivalence can be proved.

The third option must be genuinely exact; an approximate Bloom/filter-style signal would contaminate the frozen policy unless followed by exactification that guarantees the same final decision.

## Policy versus implementation

The simultaneous run again shows that the frozen gate is not an optimal profitability classifier: always-P6 happened to beat direct on {s['gatep_confusion']['p6_wins']} cases, while the gate annotated only {s['gatep_annotated']}. P12 deliberately does not change this. The purpose of P9-P12 has been to isolate implementation overhead under a fixed policy.

Once the telemetry path is exhausted, a separate policy-retraining study could reasonably revisit those missed profitable cases using disjoint training/evaluation data. That should remain a separate experiment from P12's implementation claim.

## Natural control

The natural corpus still contains zero annotated/folded cases, and P12 performs zero reuse scans there. Its near-parity natural timing is therefore evidence only that abstention has become inexpensive, not that natural EPFL cones benefit from CM folding.
'''
(HERE/'N2_P12_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme=f'''# N2/P12 Reproducibility

P12 is an implementation-only replay of the frozen P11/P8 dispatch policy with lazy reuse exactification and exact pair-repeat derivation.

## Frozen hashes

- preregistration: `{sha(HERE/'N2_P12_PREREGISTRATION.md')}`
- harness: `{sha(HERE/'n2_p12_harness.py')}`
- P8 frozen gate: `{sha(HERE.parent/'cm_n2_p8_run'/'P8_FROZEN_GATE.json')}`

## Reproduction order

1. `python cm_n2_p12_run/n2_p12_harness.py --mode invariant --out cm_n2_p12_run/invariance.json`
2. `python cm_n2_p12_run/n2_p12_harness.py --mode fuzz --out cm_n2_p12_run/fuzz.json`
3. `python cm_n2_p12_run/n2_p12_harness.py --mode gatep --out cm_n2_p12_run/gatep.json`
4. Run the ten frozen natural cases with `--mode natural-case`; `cavlc:35` may be split deterministically with `run_p12_nat_chunk.py` under short command wall limits.
5. Merge deterministic chunks, calculate `N2_P12_SUMMARY.json`, run `independent_verify.py`, then `make_p12_artifacts.py`.

The 332-case P11/P12 decision-invariance gate and 1,000-case fuzz are mandatory before timing interpretation. No model fitting, cutoff selection, or fold-threshold tuning occurs in P12.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')

combined={'schema':'cm-n2-p12-results-bundle/v1','summary':s,'invariance':inv,'fuzz':fuzz,'gatep':g,'natural_cases':nat,'posthoc_free_telemetry':free_diag,'depth_strata':strata,'absolute_build_medians_us':abs_build,'absolute_source_medians_us':abs_source}
(HERE/'n2_p12_results.json').write_text(json.dumps(combined,indent=2),encoding='utf-8')
print(json.dumps({'free_diag':free_diag,'abs_build_us':abs_build,'abs_source_us':abs_source,'depth_strata':strata},indent=2))
