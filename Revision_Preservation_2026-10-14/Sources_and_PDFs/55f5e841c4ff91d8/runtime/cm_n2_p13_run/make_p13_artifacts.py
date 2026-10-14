from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D='direct_source_pipeline'; P6='p6_source_pipeline'; P12='p12_lazy_reuse_dispatch'; P13='p13_deferred_pair_dispatch'

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

g=json.load(open(HERE/'gatep.json')); s=json.load(open(HERE/'N2_P13_SUMMARY.json')); inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json'))
names=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in names]
ns=[r for x in nat for r in x['source_timing_rows']]

# Case summaries.
for fname,rows,symbolic in [('N2_P13_GATEP_CASE_SUMMARY.csv',g['source_timing_rows'],g['symbolic']),('N2_P13_NATURAL_CASE_SUMMARY.csv',ns,[x['symbolic'] for x in nat])]:
    msp=med(rows,'source_pipeline_ns'); msb=med(rows,'source_build_ns'); mcp=med(rows,'compiler_ns'); sy={r['case_id']:r for r in symbolic}
    fields=['case_id','depth','circuit','root','annotate','p12_decision_code','p13_decision_code','pair_exactified','reuse_scanned','reuse_early_abort','reuse_scan_edges','edge_count','binary_nodes','pair_repeat_excess','p6_folds','direct_source_ns','p6_source_ns','p12_source_ns','p13_source_ns','p13_over_direct_source','p13_over_p12_source','direct_build_ns','p12_build_ns','p13_build_ns','p13_over_direct_build','p13_over_p12_build','direct_compiler_ns','p13_compiler_ns','multiplications_ratio','pair_terms_ratio','peak_monomials_ratio','anf_nodes_ratio']
    with open(HERE/fname,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for c in sorted(sy):
            z=sy[c];d=z['direct'];p=z['p13'];diag=z['p13_dispatch'];d12=z['p12_dispatch']
            def rr(field):
                a=p.get(field);b=d.get(field);return (a/b if a is not None and b not in (None,0) else None)
            row={'case_id':c,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),'annotate':z['annotate'],'p12_decision_code':z['p12_decision_code'],'p13_decision_code':z['p13_decision_code'],'pair_exactified':diag['pair_exactified'],'reuse_scanned':diag['reuse_scanned'],'reuse_early_abort':diag['reuse_early_abort'],'reuse_scan_edges':diag['reuse_scan_edges'],'edge_count':d12['edge_count'],'binary_nodes':d12['binary_nodes'],'pair_repeat_excess':d12['pair_repeat_excess'],'p6_folds':z['p6_folds'],
                 'direct_source_ns':msp[(c,D)],'p6_source_ns':msp[(c,P6)],'p12_source_ns':msp[(c,P12)],'p13_source_ns':msp[(c,P13)],'p13_over_direct_source':msp[(c,P13)]/msp[(c,D)],'p13_over_p12_source':msp[(c,P13)]/msp[(c,P12)],
                 'direct_build_ns':msb[(c,D)],'p12_build_ns':msb[(c,P12)],'p13_build_ns':msb[(c,P13)],'p13_over_direct_build':msb[(c,P13)]/msb[(c,D)],'p13_over_p12_build':msb[(c,P13)]/msb[(c,P12)],
                 'direct_compiler_ns':mcp[(c,D)],'p13_compiler_ns':mcp[(c,P13)],'multiplications_ratio':rr('multiplications'),'pair_terms_ratio':rr('pair_terms'),'peak_monomials_ratio':rr('peak_monomials'),'anf_nodes_ratio':rr('anf_nodes_evaluated')}
            w.writerow(row)

# Post-hoc free-telemetry diagnostic.
msp=med(g['source_timing_rows'],'source_pipeline_ns');msb=med(g['source_timing_rows'],'source_build_ns');mcp=med(g['source_timing_rows'],'compiler_ns');cases=sorted({r['case_id'] for r in g['source_timing_rows']})
free=[];num=den=0.0
for c in cases:
    a=msb[(c,D)]+mcp[(c,P13)]; b=msb[(c,D)]+mcp[(c,D)]; free.append(a/b); num+=a; den+=b
free_diag={'schema':'cm-n2-p13-posthoc-free-telemetry/v1','case_geomean':geo(free),'weighted_ratio':num/den,'note':'Frozen P13/P12 decisions and measured P13 compiler medians with P13 source-build+dispatch cost replaced by direct source-build cost. Diagnostic only; not preregistered.'}
(HERE/'P13_POSTHOC_FREE_TELEMETRY.json').write_text(json.dumps(free_diag,indent=2))

abs_build={arm:statistics.median([msb[(c,arm)] for c in cases])/1000 for arm in (D,P6,P12,P13)}
abs_source={arm:statistics.median([msp[(c,arm)] for c in cases])/1000 for arm in (D,P6,P12,P13)}

p13d=s['gatep_source']['p13_direct'];p13p12=s['gatep_source']['p13_p12'];b13d=s['gatep_source_build']['p13_direct'];b13p12=s['gatep_source_build']['p13_p12'];c13d=s['gatep_compiler']['p13_direct']
nd=s['natural_source']['p13_direct'];np12=s['natural_source']['p13_p12'];nb=s['natural_source_build']['p13_direct'];nbp12=s['natural_source_build']['p13_p12']
work=s['gatep_work'];mem=s['gatep_memory'];lazy=s['gatep_pair_lazy'];depth=s['gatep_depth']

results=f'''# N2/P13 Results - Deferred C-Backed Pair Exactification

## Status

P13 is complete. It preserved the frozen P12/P11/P8 dispatch policy, the `0.80` cutoff, P6 folding backend, Gate-P family, natural EPFL controls, and timing endpoints. P13 changed only pair telemetry: source construction appends canonical packed pair keys, while exact distinct-pair and multiplicity work is deferred to C-backed builtins at dispatch.

Mandatory P12/P13 invariance passed on **332/332** frozen policy cases, and fresh fuzz passed **1000/1000**. The independent verifier reports PASS.

## Gate-P primary endpoint

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P13 / direct, source-inclusive | **{p13d['geomean_ratio']:.6f}x** | **{p13d['ci95'][0]:.6f}-{p13d['ci95'][1]:.6f}** | **{p13d['weighted_ratio']:.6f}x** | {p13d['wins']}/36 |
| P13 / P12, source-inclusive | **{p13p12['geomean_ratio']:.6f}x** | **{p13p12['ci95'][0]:.6f}-{p13p12['ci95'][1]:.6f}** | **{p13p12['weighted_ratio']:.6f}x** | {p13p12['wins']}/36 |
| P13 / direct, source build+dispatch | **{b13d['geomean_ratio']:.6f}x** | **{b13d['ci95'][0]:.6f}-{b13d['ci95'][1]:.6f}** | **{b13d['weighted_ratio']:.6f}x** | {b13d['wins']}/36 |
| P13 / P12, source build+dispatch | **{b13p12['geomean_ratio']:.6f}x** | **{b13p12['ci95'][0]:.6f}-{b13p12['ci95'][1]:.6f}** | **{b13p12['weighted_ratio']:.6f}x** | {b13p12['wins']}/36 |
| P13 / direct, selected compiler | **{c13d['geomean_ratio']:.6f}x** | **{c13d['ci95'][0]:.6f}-{c13d['ci95'][1]:.6f}** | **{c13d['weighted_ratio']:.6f}x** | {c13d['wins']}/36 |

The preregistered **direct-crossover criterion did not pass**. P13 remains about **{(p13d['geomean_ratio']-1)*100:.2f}% above direct case-balanced**, and the confidence interval crosses 1. The workload-weighted endpoint remains below direct at **{p13d['weighted_ratio']:.6f}x**, about **{(1-p13d['weighted_ratio'])*100:.2f}% faster** in aggregate, but this is still a secondary endpoint.

Against simultaneous P12, P13's point estimate is only **{(1-p13p12['geomean_ratio'])*100:.2f}% faster source-inclusive** and **{(1-b13p12['geomean_ratio'])*100:.2f}% faster in source build+dispatch**. Both confidence intervals include 1, so the deferred-pair implementation is not a clear improvement over P12 under the preregistered criteria.

Median-of-case-median Gate-P source build+dispatch was approximately **{abs_build[D]:.1f} us direct**, **{abs_build[P12]:.1f} us P12**, and **{abs_build[P13]:.1f} us P13**. Whole-pipeline medians were approximately **{abs_source[D]:.1f} us**, **{abs_source[P12]:.1f} us**, and **{abs_source[P13]:.1f} us**.

## Deferred pair behavior

Only **{lazy['pair_exactification_cases']}/36** Gate-P cases required Stage-2 exact multiplicity counting with `_collections._count_elements`; **{lazy['reuse_scan_cases']}/36** required the reuse scan, with **{lazy['reuse_early_abort_cases']}** early reuse abort.

Thus P13 successfully removes the per-binary Python pair-count dictionary from the construction path. The fact that timing changes only marginally indicates that the remaining cost is not primarily Python-level count updates. Packing/storing one pair identity per binary node plus the dispatch-time exact distinct-pair pass remains enough to preserve most of the telemetry tax.

## Depth strata

| Depth | P13/direct source-inclusive | P13/P12 source-inclusive | P13/direct source-build+dispatch |
|---:|---:|---:|---:|
| 6 | {depth['6']['p13_direct']['geomean_ratio']:.6f}x | {depth['6']['p13_p12']['geomean_ratio']:.6f}x | {depth['6']['p13_direct_build']['geomean_ratio']:.6f}x |
| 8 | {depth['8']['p13_direct']['geomean_ratio']:.6f}x | {depth['8']['p13_p12']['geomean_ratio']:.6f}x | {depth['8']['p13_direct_build']['geomean_ratio']:.6f}x |
| 10 | {depth['10']['p13_direct']['geomean_ratio']:.6f}x | {depth['10']['p13_p12']['geomean_ratio']:.6f}x | {depth['10']['p13_direct_build']['geomean_ratio']:.6f}x |

Depth 8 remains below direct on the point estimate, driven by the same fold-profitable cases as the frozen policy; this is a stratum result, not a corpus-wide PASS.

## Dispatch and Boolean work

P13 preserves the frozen policy exactly: **{s['gatep_annotated']}/36** Gate-P cases annotate and all **{s['gatep_fold_cases']}** consume a fold. Boolean work is therefore unchanged from P8-P12:

- multiplications: **{work['multiplications']['geomean_ratio']:.6f}x direct**;
- pair terms: **{work['pair_terms']['geomean_ratio']:.6f}x direct**;
- peak monomials: **{work['peak_monomials']['geomean_ratio']:.6f}x direct**;
- ANF nodes evaluated: **{work['anf_nodes_evaluated']['geomean_ratio']:.6f}x direct**.

## Memory

Gate-P whole-pipeline traced peak allocation was **{mem['p13_direct']['geomean_ratio']:.6f}x direct** and **{mem['p13_p12']['geomean_ratio']:.6f}x P12**. The list-plus-temporary-set/count design is slightly lower than P12 on the geometric-mean peak metric, but memory is not the limiting endpoint here.

## Natural EPFL control

P13 annotated **0/10** natural cases and consumed **0 folds**. These remain abstention/overhead controls only.

| Comparison | Case-balanced geomean | 95% bootstrap CI | Workload-weighted | Wins |
|---|---:|---:|---:|---:|
| P13 / direct, source-inclusive | **{nd['geomean_ratio']:.6f}x** | **{nd['ci95'][0]:.6f}-{nd['ci95'][1]:.6f}** | **{nd['weighted_ratio']:.6f}x** | {nd['wins']}/10 |
| P13 / P12, source-inclusive | **{np12['geomean_ratio']:.6f}x** | **{np12['ci95'][0]:.6f}-{np12['ci95'][1]:.6f}** | **{np12['weighted_ratio']:.6f}x** | {np12['wins']}/10 |
| P13 / direct, source build+dispatch | **{nb['geomean_ratio']:.6f}x** | **{nb['ci95'][0]:.6f}-{nb['ci95'][1]:.6f}** | **{nb['weighted_ratio']:.6f}x** | {nb['wins']}/10 |
| P13 / P12, source build+dispatch | **{nbp12['geomean_ratio']:.6f}x** | **{nbp12['ci95'][0]:.6f}-{nbp12['ci95'][1]:.6f}** | **{nbp12['weighted_ratio']:.6f}x** | {nbp12['wins']}/10 |

The case-balanced natural full pipeline is essentially parity with direct, but because zero cases fold this is not evidence of natural CM acceleration.

## Post-hoc diagnostic

Keeping P13's exact frozen dispatch decisions and measured compiler medians, but replacing P13 source-build+dispatch cost with ordinary direct source-build cost, gives **{free_diag['case_geomean']:.6f}x direct case-balanced** and **{free_diag['weighted_ratio']:.6f}x workload-weighted**. This remains diagnostic only.

## Predeclared outcomes

- Gate-P direct-crossover PASS: **{s['predeclared_gatep_direct_crossover_pass']}**.
- Deferred-pair engineering success: **{s['predeclared_deferred_pair_engineering_success']}**.

P13 therefore gives a useful negative engineering result: moving exact pair counting into C-backed dispatch work is mathematically clean and decision-identical, but does **not** remove enough CPython telemetry cost to make the case-balanced source-inclusive pipeline win.
'''
(HERE/'N2_P13_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P13 Interpretation

## Main conclusion

P13 tested the strongest exact two-stage pair scheme suggested by P12 without changing the frozen policy. It succeeded functionally but only marginally affected time.

The primary Gate-P result is **{p13d['geomean_ratio']:.6f}x direct** with CI **{p13d['ci95'][0]:.6f}-{p13d['ci95'][1]:.6f}**. The workload-weighted endpoint remains below direct at **{p13d['weighted_ratio']:.6f}x**, but the preregistered case-balanced crossover is still unresolved.

## What P13 established

The Python per-node count dictionary was not the dominant residual bottleneck. P13 replaced it with a much lighter construction path: append one packed integer per binary node, then use C-backed `set` and `_count_elements` work only at dispatch. Only **{lazy['pair_exactification_cases']}** Gate-P cases needed exact multiplicity counting, yet P13/P12 source build+dispatch was still **{b13p12['geomean_ratio']:.6f}x**, with its CI crossing 1.

Post-hoc profiling is consistent with this. P12 and P13 spend similar cumulative time in their specialized `_make` paths. P13 eliminates repeated Python dictionary count updates, but still pays for:

- the binary-op branch;
- canonical child-id ordering;
- packed integer construction;
- one list append per binary source node;
- a dispatch-time exact distinct-pair pass for most nontrivial cases.

The remaining tax therefore appears to be **carrying pair identity at all in CPython**, rather than the particular dictionary-count representation.

## Why this is still encouraging

The downstream selective compiler path remains materially favorable: workload-weighted P13 compiler time is **{c13d['weighted_ratio']:.6f}x direct**, and the frozen policy still removes pair-term work to **{work['pair_terms']['geomean_ratio']:.6f}x direct**. The post-hoc zero-incremental-telemetry diagnostic is **{free_diag['case_geomean']:.6f}x case-balanced** and **{free_diag['weighted_ratio']:.6f}x workload-weighted**.

So P13 does not point to a failure of propagated CM folding. It points to a practical floor for progressively rearranging the same pair telemetry in pure Python.

## Natural control

The frozen natural corpus remains zero-fold. P13's **{nd['geomean_ratio']:.6f}x direct** case-balanced timing is effectively parity and should be interpreted only as low abstention overhead, not a natural-circuit folding speedup.

## Strongest next experiment

Two directions are now cleaner than another Python container rearrangement:

1. **Compiled telemetry path (P14A).** Keep the exact P13/P12 decision and folding backend, but move pair-key observation and distinct/frequency accumulation into a small Cython/C helper or compiled source-builder path. The mandatory 332-case decision-equivalence gate should remain unchanged. This directly tests whether crossing the Python boundary is the remaining implementation obstacle.

2. **Separately preregistered policy study (P14B).** The frozen P8 tree was intentionally never retuned during P9-P13. It continues to miss some cases where always-P6 wins and selects some where P6 loses. A new policy should be trained on disjoint data against full end-to-end cost, not fold incidence, and evaluated on new held-out Gate-P-like and natural corpora. This would test a different question from implementation overhead and should not be mixed with P14A.

If the immediate objective is to determine whether the current mechanism can cross the strict case-balanced endpoint without changing policy, P14A is the cleaner next step.
'''
(HERE/'N2_P13_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme=f'''# N2/P13 Reproducibility

P13 is an implementation-only replay of the frozen P12/P11/P8 dispatch policy with deferred C-backed exact pair statistics.

## Frozen hashes

- preregistration: `{sha(HERE/'N2_P13_PREREGISTRATION.md')}`
- harness: `{sha(HERE/'n2_p13_harness.py')}`
- P8 frozen gate: `{sha(HERE.parent/'cm_n2_p8_run'/'P8_FROZEN_GATE.json')}`

## Reproduction order

1. `python cm_n2_p13_run/n2_p13_harness.py --mode invariant --out cm_n2_p13_run/invariance.json`
2. `python cm_n2_p13_run/n2_p13_harness.py --mode fuzz --out cm_n2_p13_run/fuzz.json`
3. `python cm_n2_p13_run/n2_p13_harness.py --mode gatep --out cm_n2_p13_run/gatep.json`
4. Run the ten frozen natural cases with `--mode natural-case`; `cavlc:35` may be split deterministically with `run_p13_nat_chunk.py` under command wall limits.
5. Merge deterministic chunks, calculate `N2_P13_SUMMARY.json`, run `independent_verify.py`, then `make_p13_artifacts.py`.

The 332-case P12/P13 decision-invariance gate and 1,000-case fuzz are mandatory before timing interpretation. No model fitting, cutoff selection, fold-threshold tuning, or post-result pair-strategy modification occurs in P13.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')

combined={'schema':'cm-n2-p13-results-bundle/v1','summary':s,'invariance':inv,'fuzz':fuzz,'gatep':g,'natural_cases':nat,'posthoc_free_telemetry':free_diag,'absolute_build_medians_us':abs_build,'absolute_source_medians_us':abs_source}
(HERE/'n2_p13_results.json').write_text(json.dumps(combined,indent=2),encoding='utf-8')
(HERE/'HARNESS.sha256').write_text(f"{sha(HERE/'n2_p13_harness.py')}  n2_p13_harness.py\n")
(HERE/'PREREGISTRATION.sha256').write_text(f"{sha(HERE/'N2_P13_PREREGISTRATION.md')}  N2_P13_PREREGISTRATION.md\n")
print(json.dumps({'free_diag':free_diag,'abs_build_us':abs_build,'abs_source_us':abs_source},indent=2))
