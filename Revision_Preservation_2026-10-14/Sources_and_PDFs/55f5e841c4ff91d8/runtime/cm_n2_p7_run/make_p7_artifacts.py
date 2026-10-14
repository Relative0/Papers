from __future__ import annotations
import csv, hashlib, json, math, shutil, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
D=json.loads((HERE/'n2_p7_results.json').read_text())
P7='cm_cword_sig_sparse'; P6='cm_innode_sig_sparse'; P5='cm_packed_sig_sparse'; DD='direct_cword_sparse_anf'
P7B='cm_cword_sig_build_sparse'; P6B='cm_innode_sig_build_sparse'; P5B='cm_packed_sig_build_sparse'; DB='direct_build_sparse'

def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}
def symmap(rows):return {(r['case_id'],r['arm']):r for r in rows}
def make_csv(corpus):
    sym=D[f'{corpus}_symbolic_rows']; lower=D[f'{corpus}_lower_timing_rows']; pipe=D[f'{corpus}_pipeline_timing_rows']
    lm=medmap(lower,'lower_ns'); pm=medmap(pipe,'pipeline_ns'); bm=medmap(pipe,'dag_build_ns'); sm=symmap(sym)
    cases=sorted({r['case_id'] for r in sym},key=lambda x:((int(x.split(':')[0]) if corpus=='gatep' else x.split(':')[0]),x))
    out=[]
    for c in cases:
        row={'case_id':c}
        if corpus=='gatep':row.update(depth=int(c.split(':')[0]),case=int(c.split(':')[1]))
        row.update({
          'direct_lower_us':lm[(c,DD)]/1e3,'p7_lower_us':lm[(c,P7)]/1e3,'p6_lower_us':lm[(c,P6)]/1e3,'p5_lower_us':lm[(c,P5)]/1e3,
          'p7_over_direct_lower':lm[(c,P7)]/lm[(c,DD)],'p7_over_p6_lower':lm[(c,P7)]/lm[(c,P6)],'p7_over_p5_lower':lm[(c,P7)]/lm[(c,P5)],
          'direct_pipeline_us':pm[(c,DB)]/1e3,'p7_pipeline_us':pm[(c,P7B)]/1e3,'p6_pipeline_us':pm[(c,P6B)]/1e3,'p5_pipeline_us':pm[(c,P5B)]/1e3,
          'p7_over_direct_pipeline':pm[(c,P7B)]/pm[(c,DB)],'p7_over_p6_pipeline':pm[(c,P7B)]/pm[(c,P6B)],'p7_over_p5_pipeline':pm[(c,P7B)]/pm[(c,P5B)],
          'direct_build_us':bm[(c,DB)]/1e3,'p7_build_us':bm[(c,P7B)]/1e3,'p6_build_us':bm[(c,P6B)]/1e3,'p5_build_us':bm[(c,P5B)]/1e3,
          'p7_over_direct_build':bm[(c,P7B)]/bm[(c,DB)],'p7_over_p6_build':bm[(c,P7B)]/bm[(c,P6B)],'p7_over_p5_build':bm[(c,P7B)]/bm[(c,P5B)],
          'direct_multiplications':sm[(c,DD)]['multiplications'],'p7_multiplications':sm[(c,P7)]['multiplications'],
          'direct_pair_terms':sm[(c,DD)]['pair_terms'],'p7_pair_terms':sm[(c,P7)]['pair_terms'],
          'direct_peak_monomials':sm[(c,DD)]['peak_monomials'],'p7_peak_monomials':sm[(c,P7)]['peak_monomials'],
          'p7_selector_candidates':sm[(c,P7)].get('selector_candidates',0),'p7_selector_accepted':sm[(c,P7)].get('selector_accepted',0),
          'p7_folds':sm[(c,P7)].get('fold_lowerings',0)})
        out.append(row)
    path=HERE/f'N2_P7_{corpus.upper()}_CASE_SUMMARY.csv'
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    return path
make_csv('natural'); make_csv('gatep')
profile=json.loads((HERE/'P7_POSTHOC_BUILD_MEMORY.json').read_text())
G=D['gatep']; N=D['natural']
def R(s,k):return s[k]['geomean_ratio']
def CI(s,k):return s[k]['bootstrap']['ci95']
results=f'''# N2/P7 Results — Two C-Backed 64-bit Annotation Words

## Executive result

P7 preserves P4-P6's propagated-signature mathematics exactly, and the lowering-only speed signal remains a clear PASS on Gate-P. However, the hypothesized construction-time improvement from replacing P6's in-node Python integers with two `array('Q')` buffers **did not occur**. P7 construction is slower than simultaneous P6 and P5, so the preregistered end-to-end signal remains FAIL.

## Gate-P primary endpoints

| comparison | ratio | bootstrap 95% CI |
|---|---:|---:|
| P7 / direct lowering | **{R(G,'p7_over_direct:lower_ns'):.4f}x** | **{CI(G,'p7_over_direct:lower_ns')[0]:.4f}-{CI(G,'p7_over_direct:lower_ns')[1]:.4f}** |
| P7 / P6 lowering | {R(G,'p7_over_p6:lower_ns'):.4f}x | {CI(G,'p7_over_p6:lower_ns')[0]:.4f}-{CI(G,'p7_over_p6:lower_ns')[1]:.4f} |
| P7 / P5 lowering | {R(G,'p7_over_p5:lower_ns'):.4f}x | {CI(G,'p7_over_p5:lower_ns')[0]:.4f}-{CI(G,'p7_over_p5:lower_ns')[1]:.4f} |
| **P7 full pipeline / direct** | **{R(G,'p7_build_over_direct:pipeline_ns'):.4f}x** | **{CI(G,'p7_build_over_direct:pipeline_ns')[0]:.4f}-{CI(G,'p7_build_over_direct:pipeline_ns')[1]:.4f}** |
| P7 full pipeline / P6 | {R(G,'p7_build_over_p6:pipeline_ns'):.4f}x | {CI(G,'p7_build_over_p6:pipeline_ns')[0]:.4f}-{CI(G,'p7_build_over_p6:pipeline_ns')[1]:.4f} |
| P7 full pipeline / P5 | {R(G,'p7_build_over_p5:pipeline_ns'):.4f}x | {CI(G,'p7_build_over_p5:pipeline_ns')[0]:.4f}-{CI(G,'p7_build_over_p5:pipeline_ns')[1]:.4f} |
| **P7 DAG build / direct** | **{R(G,'p7_build_over_direct:dag_build_ns'):.4f}x** | **{CI(G,'p7_build_over_direct:dag_build_ns')[0]:.4f}-{CI(G,'p7_build_over_direct:dag_build_ns')[1]:.4f}** |
| P7 DAG build / P6 | **{R(G,'p7_build_over_p6:dag_build_ns'):.4f}x** | **{CI(G,'p7_build_over_p6:dag_build_ns')[0]:.4f}-{CI(G,'p7_build_over_p6:dag_build_ns')[1]:.4f}** |
| P7 DAG build / P5 | **{R(G,'p7_build_over_p5:dag_build_ns'):.4f}x** | **{CI(G,'p7_build_over_p5:dag_build_ns')[0]:.4f}-{CI(G,'p7_build_over_p5:dag_build_ns')[1]:.4f}** |

Lowering-only PASS: **{G['lower_speed_signal']}**. End-to-end PASS: **{G['pipeline_speed_signal']}**.

P7 beats direct lowering on {G['p7_over_direct:lower_ns']['cases_below_1']}/36 Gate-P cases and beats direct end-to-end on {G['p7_build_over_direct:pipeline_ns']['cases_below_1']}/36.

The workload-weighted complete-pipeline ratio is **{G['weighted_p7_build_over_direct:pipeline_ns']:.4f}x direct**. This is essentially parity, but remains a secondary endpoint and cannot replace the failed case-balanced preregistered criterion.

## Symbolic work and decision equivalence

P7, P6, and P5 agree exactly on all preregistered symbolic/selector fields. Gate-P totals are:

- demanded selector nodes: **{G['p7_diag']['selector_nodes_checked']}**;
- demanded propagated candidates: **{G['p7_diag']['selector_candidates']}**;
- accepted folds: **{G['p7_diag']['selector_accepted']}**;
- accepted shared folds: **{G['p7_diag']['selector_accepted_shared']}**;
- consumed folds: **{G['p7_diag']['fold_lowerings']}**;
- propagated-signature nodes: **{G['p7_diag']['propagated_signature_nodes']}**.

Relative to direct, P7 performs:

- multiplications: **{G['symbolic_p7_over_direct']['multiplications']['geomean_ratio']:.4f}x**;
- pair terms: **{G['symbolic_p7_over_direct']['pair_terms']['geomean_ratio']:.4f}x**;
- evaluated ANF nodes: **{G['symbolic_p7_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.4f}x**;
- peak monomials: **{G['symbolic_p7_over_direct']['peak_monomials']['geomean_ratio']:.4f}x**.

Thus the underlying folding mechanism still removes about **{(1-G['symbolic_p7_over_direct']['pair_terms']['geomean_ratio'])*100:.1f}%** of pair-product work on this fold-rich workload.

## Depth behavior

| Gate-P depth | P7/direct lowering | P7/direct full pipeline |
|---:|---:|---:|
| 6 | {G['depth_p7_over_direct_lower']['6']['geomean_ratio']:.4f}x | {G['depth_p7_build_over_direct_pipeline']['6']['geomean_ratio']:.4f}x |
| 8 | {G['depth_p7_over_direct_lower']['8']['geomean_ratio']:.4f}x | {G['depth_p7_build_over_direct_pipeline']['8']['geomean_ratio']:.4f}x |
| 10 | {G['depth_p7_over_direct_lower']['10']['geomean_ratio']:.4f}x | {G['depth_p7_build_over_direct_pipeline']['10']['geomean_ratio']:.4f}x |

The algebraic advantage again strengthens with depth. The construction tax still prevents a case-balanced full-pipeline crossover.

## Memory

Predeclared full-pipeline traced peak on Gate-P:

- P7 / direct: **{G['pipeline_python_peak_p7_over_direct']['geomean_ratio']:.4f}x**;
- P7 / P6: **{G['pipeline_python_peak_p7_over_p6']['geomean_ratio']:.4f}x**;
- P7 / P5: **{G['pipeline_python_peak_p7_over_p5']['geomean_ratio']:.4f}x**.

The post-hoc build-only diagnostic gives P7/direct **{profile['summary']['p7_over_direct_geomean']:.4f}x**, P7/P6 **{profile['summary']['p7_over_p6_geomean']:.4f}x**, and P7/P5 **{profile['summary']['p7_over_p5_geomean']:.4f}x** peak allocation. The two arrays help memory relative to P6/P5 build metadata, even though they do not improve construction wall time.

## Natural EPFL replay

The frozen natural set again has **{N['p7_diag']['selector_candidates']} demanded propagated candidate and {N['p7_diag']['selector_accepted']} accepted folds**. These are therefore abstention-overhead measurements only.

| comparison | ratio | bootstrap 95% CI |
|---|---:|---:|
| P7 / direct lowering | {R(N,'p7_over_direct:lower_ns'):.4f}x | {CI(N,'p7_over_direct:lower_ns')[0]:.4f}-{CI(N,'p7_over_direct:lower_ns')[1]:.4f} |
| P7 full pipeline / direct | {R(N,'p7_build_over_direct:pipeline_ns'):.4f}x | {CI(N,'p7_build_over_direct:pipeline_ns')[0]:.4f}-{CI(N,'p7_build_over_direct:pipeline_ns')[1]:.4f} |
| P7 build / direct | {R(N,'p7_build_over_direct:dag_build_ns'):.4f}x | {CI(N,'p7_build_over_direct:dag_build_ns')[0]:.4f}-{CI(N,'p7_build_over_direct:dag_build_ns')[1]:.4f} |

No natural-circuit CM-folding speed claim is warranted.

## Verification

- Fresh fuzz: **1000/1000 passed**.
- Recorded benchmark rows: **7774**, all successful.
- P7/P6/P5 symbolic decisions/work: exact match.
- EPFL source blobs: independently reverified.
- Independent verifier: see `N2_P7_INDEPENDENT_VERIFY.json`.
'''
(HERE/'N2_P7_RESULTS.md').write_text(results)
interp=f'''# N2/P7 Interpretation

## What P7 tested

P7 was deliberately narrow: keep P6's exact two-word logical format and P4-P6's exact propagation/profitability semantics, but store the words in two C-backed `array('Q')` buffers rather than as Python integer attributes on each node. This isolates storage placement from the folding algorithm.

## Main finding

The storage hypothesis is **not supported for wall time in CPython**. P7 build time is **{R(G,'p7_build_over_p6:dag_build_ns'):.3f}x P6** and **{R(G,'p7_build_over_p5:dag_build_ns'):.3f}x P5**, with both 95% intervals entirely above 1. P7's full pipeline is likewise **{R(G,'p7_build_over_p6:pipeline_ns'):.3f}x P6**.

This matters because P7 is not doing more optimization. It makes the same 29 Gate-P fold decisions, consumes all 29, and produces exactly the same ANF work. The regression is therefore representation/runtime overhead.

## Why two arrays can still be slower

The post-hoc profile is qualitative, not a timing endpoint, but it suggests a plausible mechanism. `array('Q')` still crosses the Python/C conversion boundary for every indexed read/write. P7 also performs packed-word masking/shifting on values returned from those arrays. P6 keeps the same packed words as ordinary Python integers directly reachable from the node object, while P5 uses narrower typed arrays/bytearrays for several fields. Fewer containers therefore does not imply fewer or cheaper Python-level operations.

The authoritative randomized endpoint says the key fact: P7 construction is ~7% slower than simultaneous P6/P5 on Gate-P despite using only two C-backed buffers.

## Memory is a different story

P7's full-pipeline traced peak is **{G['pipeline_python_peak_p7_over_direct']['geomean_ratio']:.3f}x direct**, **{G['pipeline_python_peak_p7_over_p6']['geomean_ratio']:.3f}x P6**, and **{G['pipeline_python_peak_p7_over_p5']['geomean_ratio']:.3f}x P5**. The separate build-only diagnostic also puts P7 below P6/P5 in peak allocation. So the representation is memory-efficient even though it is not time-efficient.

That distinction is useful: the remaining obstacle is not metadata size alone.

## Folding itself remains strong

P7 lowering is **{R(G,'p7_over_direct:lower_ns'):.3f}x direct**, with its entire confidence interval below 1. Pair terms remain **{G['symbolic_p7_over_direct']['pair_terms']['geomean_ratio']:.3f}x direct** and evaluated ANF nodes **{G['symbolic_p7_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.3f}x**. P7 is also modestly faster than P6 in lowering (**{R(G,'p7_over_p6:lower_ns'):.3f}x**) and statistically indistinguishable from P5 (**{R(G,'p7_over_p5:lower_ns'):.3f}x**).

The mechanism result therefore survives unchanged: propagated two-support information can substantially accelerate the actual sparse-ANF computation on fold-rich structure.

## End-to-end status

Case-balanced P7/direct full pipeline is **{R(G,'p7_build_over_direct:pipeline_ns'):.3f}x**, so the strong endpoint fails. The workload-weighted ratio is **{G['weighted_p7_build_over_direct:pipeline_ns']:.4f}x**, extremely close to parity. Six of 36 cases beat direct end-to-end.

This is close enough that a dispatch gate now becomes more scientifically interesting than another Python container rearrangement. The natural corpus accepts zero folds and pays a **{R(N,'p7_build_over_direct:pipeline_ns'):.3f}x** full-pipeline tax. Avoiding annotation entirely on low-opportunity formulas could remove that tax without changing fold-rich behavior.

## Most informative next experiment: P7B / P8 dispatch

The next pass should keep P5/P6/P7 folding semantics frozen and test only a formula-level bypass gate. To avoid tuning on the evaluation set:

1. create a calibration corpus disjoint from the 36 Gate-P evaluation cases and the ten frozen EPFL evaluation cones;
2. use only very cheap pre-annotation structural features available from the ordinary DAG (for example reachable-node count, binary-node count, depth, and perhaps repeated immediate operand-pair count if it can be obtained without a full reference scan);
3. choose a fixed rule whose purpose is to predict whether annotation cost can plausibly amortize;
4. freeze that rule before replaying Gate-P and the natural evaluation set;
5. dispatch to direct/no-rewrite when the gate says no, otherwise run the best annotated representation unchanged.

Given P7's result, I would use **P5 or P6 as the annotated backend**, not P7, because simultaneous timing shows them faster to construct. The question has shifted from “which Python metadata container wins?” to “can we avoid paying any metadata cost when the formula gives us no reason to?”
'''
(HERE/'N2_P7_INTERPRETATION.md').write_text(interp)
readme=f'''# N2/P7 Reproducibility README

P7 tests exactly two C-backed 64-bit annotation arrays with P6's frozen packing and P4-P6's frozen folding semantics.

## Frozen hashes

- preregistration: `{hashlib.sha256((HERE/'N2_P7_PREREGISTRATION.md').read_bytes()).hexdigest()}`
- final frozen harness after the pre-timing reporting-field fix: `{hashlib.sha256((HERE/'n2_p7_harness.py').read_bytes()).hexdigest()}`

The initial harness stopped before timing because the direct-control row omitted `output_unique_nodes`; only that reporting field was added before any P7 timing result was produced. The preregistration did not change.

## Main commands

```bash
python n2_p7_harness.py --mode fuzz --out fuzz.json
python n2_p7_harness.py --mode selection --out selection.json
python n2_p7_harness.py --mode gatep --out gatep.json
```

For the ten natural cases, `--mode natural-case` is sufficient for ordinary cases. `run_p7_nat_chunk.py` deterministically reproduces the same frozen schedules in slices for slow cases such as `cavlc:35`; `merge_heavy_cases.py` reconstructs the case payloads.

Then run:

```bash
python combine_p7_results.py
python independent_verify.py
```

`P7_POSTHOC_PROFILE.txt` and `P7_POSTHOC_BUILD_MEMORY.json` are explicitly post-hoc diagnostics and are not preregistered pass/fail endpoints.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme)
shutil.copy2(ROOT/'cm_n2_p6_run/EPFL_SOURCE_MANIFEST.json',HERE/'EPFL_SOURCE_MANIFEST.json')
print('artifacts written')
