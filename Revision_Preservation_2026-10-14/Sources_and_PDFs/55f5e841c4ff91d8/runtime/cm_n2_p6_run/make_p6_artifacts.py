from __future__ import annotations
import csv, hashlib, json, statistics, shutil
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
D=json.loads((HERE/'n2_p6_results.json').read_text())
P6='cm_innode_sig_sparse'; P5='cm_packed_sig_sparse'; DD='direct_innode_sparse_anf'
P6B='cm_innode_sig_build_sparse'; P5B='cm_packed_sig_build_sparse'; DB='direct_build_sparse'

def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}
def symmap(rows): return {(r['case_id'],r['arm']):r for r in rows}

def make_csv(corpus):
    sym=D[f'{corpus}_symbolic_rows']; lower=D[f'{corpus}_lower_timing_rows']; pipe=D[f'{corpus}_pipeline_timing_rows']
    lm=medmap(lower,'lower_ns'); pm=medmap(pipe,'pipeline_ns'); bm=medmap(pipe,'dag_build_ns'); sm=symmap(sym)
    cases=sorted({r['case_id'] for r in sym},key=lambda x:((int(x.split(':')[0]) if corpus=='gatep' else x.split(':')[0]),x))
    out=[]
    for c in cases:
        row={'case_id':c}
        if corpus=='gatep': row.update(depth=int(c.split(':')[0]),case=int(c.split(':')[1]))
        row.update({
          'direct_lower_us':lm[(c,DD)]/1e3,'p6_lower_us':lm[(c,P6)]/1e3,'p5_lower_us':lm[(c,P5)]/1e3,
          'p6_over_direct_lower':lm[(c,P6)]/lm[(c,DD)],'p6_over_p5_lower':lm[(c,P6)]/lm[(c,P5)],
          'direct_pipeline_us':pm[(c,DB)]/1e3,'p6_pipeline_us':pm[(c,P6B)]/1e3,'p5_pipeline_us':pm[(c,P5B)]/1e3,
          'p6_over_direct_pipeline':pm[(c,P6B)]/pm[(c,DB)],'p6_over_p5_pipeline':pm[(c,P6B)]/pm[(c,P5B)],
          'direct_build_us':bm[(c,DB)]/1e3,'p6_build_us':bm[(c,P6B)]/1e3,'p5_build_us':bm[(c,P5B)]/1e3,
          'p6_over_direct_build':bm[(c,P6B)]/bm[(c,DB)],'p6_over_p5_build':bm[(c,P6B)]/bm[(c,P5B)],
          'direct_multiplications':sm[(c,DD)]['multiplications'],'p6_multiplications':sm[(c,P6)]['multiplications'],
          'direct_pair_terms':sm[(c,DD)]['pair_terms'],'p6_pair_terms':sm[(c,P6)]['pair_terms'],
          'direct_peak_monomials':sm[(c,DD)]['peak_monomials'],'p6_peak_monomials':sm[(c,P6)]['peak_monomials'],
          'p6_selector_candidates':sm[(c,P6)].get('selector_candidates',0),'p6_selector_accepted':sm[(c,P6)].get('selector_accepted',0),
          'p6_accepted_shared':sm[(c,P6)].get('selector_accepted_shared',0),'p6_fold_lowerings':sm[(c,P6)].get('fold_lowerings',0)})
        out.append(row)
    fn=HERE/(f'N2_P6_{corpus.upper()}_CASE_SUMMARY.csv')
    with fn.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    return fn
make_csv('gatep'); make_csv('natural')

G=D['gatep']; N=D['natural']
def R(s,k): return s[k]['geomean_ratio']
def CI(s,k): return s[k]['bootstrap']['ci95']
profile=json.loads((HERE/'P6_POSTHOC_BUILD_MEMORY.json').read_text())

results=f'''# N2/P6 — Two-Word In-Node Semantic Annotation

Preregistration SHA-256: `898781343d0e9379bdf37d7c053eece3deb9c674b7bc514d2722504d97b0f60b`  
Frozen harness SHA-256: `6afec487a6a1a91b29fd8c4adc8ac4dcef4c787f9987b24111b00dd82f408030`

## Result in one sentence

**P6 preserved P5's propagated-fold semantics and its strong lowering-stage savings, but moving the two packed words into Python node objects did not reduce construction cost: on Gate-P P6 lowering was 0.6641x direct, while the complete pipeline remained 1.2444x direct, and simultaneous P6 construction was actually 1.0246x P5.**

## Gate-P primary results

| comparison | cases | geometric-mean ratio | bootstrap 95% CI | cases below reference |
|---|---:|---:|---:|---:|
| P6 / direct lowering | 36 | **{R(G,'p6_over_direct:lower_ns'):.4f}x** | {CI(G,'p6_over_direct:lower_ns')[0]:.4f}-{CI(G,'p6_over_direct:lower_ns')[1]:.4f} | {G['p6_over_direct:lower_ns']['cases_below_1']}/36 |
| P6 / P5 lowering | 36 | {R(G,'p6_over_p5:lower_ns'):.4f}x | {CI(G,'p6_over_p5:lower_ns')[0]:.4f}-{CI(G,'p6_over_p5:lower_ns')[1]:.4f} | {G['p6_over_p5:lower_ns']['cases_below_1']}/36 |
| P6 pipeline / direct | 36 | **{R(G,'p6_build_over_direct:pipeline_ns'):.4f}x** | {CI(G,'p6_build_over_direct:pipeline_ns')[0]:.4f}-{CI(G,'p6_build_over_direct:pipeline_ns')[1]:.4f} | {G['p6_build_over_direct:pipeline_ns']['cases_below_1']}/36 |
| P6 pipeline / P5 | 36 | {R(G,'p6_build_over_p5:pipeline_ns'):.4f}x | {CI(G,'p6_build_over_p5:pipeline_ns')[0]:.4f}-{CI(G,'p6_build_over_p5:pipeline_ns')[1]:.4f} | {G['p6_build_over_p5:pipeline_ns']['cases_below_1']}/36 |
| P6 DAG build / direct | 36 | **{R(G,'p6_build_over_direct:dag_build_ns'):.4f}x** | {CI(G,'p6_build_over_direct:dag_build_ns')[0]:.4f}-{CI(G,'p6_build_over_direct:dag_build_ns')[1]:.4f} | 0/36 |
| P6 DAG build / P5 | 36 | **{R(G,'p6_build_over_p5:dag_build_ns'):.4f}x** | {CI(G,'p6_build_over_p5:dag_build_ns')[0]:.4f}-{CI(G,'p6_build_over_p5:dag_build_ns')[1]:.4f} | {G['p6_build_over_p5:dag_build_ns']['cases_below_1']}/36 |

Predeclared Gate-P lowering signal: **PASS**.  
Predeclared Gate-P construction-inclusive signal: **NO PASS**.

The workload-weighted secondary ratios were **{G['weighted_p6_over_direct:lower_ns']:.4f}x** for lowering and **{G['weighted_p6_build_over_direct:pipeline_ns']:.4f}x** for the complete pipeline. Thus expensive Gate-P cases still cross the end-to-end break-even point collectively, but the preregistered case-balanced endpoint remains above 1.

## Exact P6/P5 mathematical equivalence

P6 matched P5 case-by-case on final ANF digest, multiplications, pair terms, peak monomials, evaluated ANF nodes, candidate counts, accept/reject decisions, estimated costs, shared-fold decisions, and consumed folds.

Gate-P totals for both P5 and P6:

- demanded binary nodes checked: **{G['p6_diag']['selector_nodes_checked']}**;
- demanded propagated candidates: **{G['p6_diag']['selector_candidates']}**;
- accepted / consumed folds: **{G['p6_diag']['selector_accepted']} / {G['p6_diag']['fold_lowerings']}**;
- accepted shared folds: **{G['p6_diag']['selector_accepted_shared']}**;
- propagated signature nodes present: **{G['p6_diag']['propagated_signature_nodes']}**.

Symbolic work versus direct was therefore unchanged from P5/P4:

- multiplications: **{G['symbolic_p6_over_direct']['multiplications']['geomean_ratio']:.4f}x**;
- pair terms: **{G['symbolic_p6_over_direct']['pair_terms']['geomean_ratio']:.4f}x**;
- evaluated ANF nodes: **{G['symbolic_p6_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.4f}x**;
- peak monomials: **{G['symbolic_p6_over_direct']['peak_monomials']['geomean_ratio']:.4f}x**.

## The P6 hypothesis did not hold in Python

The intended representation change was successful mechanically: persistent metadata is exactly two integer fields on each node and there are no P5-style per-field side arrays. But simultaneous timing shows **P6 construction was {R(G,'p6_build_over_p5:dag_build_ns'):.4f}x P5**, not faster. The complete P6/P5 pipeline was statistically indistinguishable from parity at **{R(G,'p6_build_over_p5:pipeline_ns'):.4f}x**.

This is stronger evidence than comparing P6 to the older P5 run alone, because P5 was replayed simultaneously under the same randomized schedules. Any apparent difference between the historical P5/direct build ratio and this run should therefore be treated as run-to-run variation.

## Memory

Predeclared full-pipeline traced peak on Gate-P:

- P6 / direct: **{G['pipeline_python_peak_p6_over_direct']['geomean_ratio']:.4f}x**;
- P6 / P5: **{G['pipeline_python_peak_p6_over_p5']['geomean_ratio']:.4f}x**.

A post-hoc build-only `tracemalloc` diagnostic found:

- P6 / direct construction peak: **{profile['summary']['p6_over_direct_geomean']:.4f}x**;
- P6 / P5 construction peak: **{profile['summary']['p6_over_p5_geomean']:.4f}x**.

So two Python integer slots are not a memory win over P5's C-backed `array`/`bytearray` side storage. Downstream ANF savings still make the full fold-rich pipeline peak lower than direct.

## Depth behavior

| Gate-P depth | P6/direct lowering | P6/direct full pipeline |
|---:|---:|---:|
| 6 | {G['depth_p6_over_direct_lower']['6']['geomean_ratio']:.4f}x | {G['depth_p6_build_over_direct_pipeline']['6']['geomean_ratio']:.4f}x |
| 8 | {G['depth_p6_over_direct_lower']['8']['geomean_ratio']:.4f}x | {G['depth_p6_build_over_direct_pipeline']['8']['geomean_ratio']:.4f}x |
| 10 | {G['depth_p6_over_direct_lower']['10']['geomean_ratio']:.4f}x | {G['depth_p6_build_over_direct_pipeline']['10']['geomean_ratio']:.4f}x |

The algebraic benefit strengthens with depth, while the complete pipeline still remains above direct case-balanced at every tested depth.

## Natural EPFL replay

The frozen ten natural cases again produced **{N['p6_diag']['selector_candidates']} demanded propagated candidate and {N['p6_diag']['selector_accepted']} accepted folds**. Therefore these measurements remain abstention/annotation overhead, not evidence of natural CM-folding acceleration.

| comparison | ratio | bootstrap 95% CI |
|---|---:|---:|
| P6 / direct lowering | {R(N,'p6_over_direct:lower_ns'):.4f}x | {CI(N,'p6_over_direct:lower_ns')[0]:.4f}-{CI(N,'p6_over_direct:lower_ns')[1]:.4f} |
| P6 pipeline / direct | {R(N,'p6_build_over_direct:pipeline_ns'):.4f}x | {CI(N,'p6_build_over_direct:pipeline_ns')[0]:.4f}-{CI(N,'p6_build_over_direct:pipeline_ns')[1]:.4f} |
| P6 pipeline / P5 | {R(N,'p6_build_over_p5:pipeline_ns'):.4f}x | {CI(N,'p6_build_over_p5:pipeline_ns')[0]:.4f}-{CI(N,'p6_build_over_p5:pipeline_ns')[1]:.4f} |
| P6 build / direct | {R(N,'p6_build_over_direct:dag_build_ns'):.4f}x | {CI(N,'p6_build_over_direct:dag_build_ns')[0]:.4f}-{CI(N,'p6_build_over_direct:dag_build_ns')[1]:.4f} |

## Verification

- Fresh randomized fuzz: **1000/1000 passed**.
- Recorded benchmark rows: **5842**, all successful.
- Independent verifier: **PASS**.
- All P6/P5 symbolic decision/work fields matched exactly.
- All six pinned EPFL Git blobs reverified.
- Natural selection reverified at the same ten cases; `bar` again supplied zero timed cases.

## Bottom line

P6 rules out a tempting implementation hypothesis: **in CPython, putting the two packed words directly on every node is not cheaper than P5's compact C-backed side arrays.** The propagated-signature mechanism still gives a clear lowering-stage win on fold-rich Gate-P, but the construction path remains about 2.5x the minimal ordinary builder and prevents a case-balanced end-to-end win.
'''
(HERE/'N2_P6_RESULTS.md').write_text(results,encoding='utf-8')

interp=f'''# N2/P6 Interpretation

## What changed

P6 kept the exact P5 mathematics and moved all persistent metadata into two integer fields on each node: one packed fanout/monomial-estimate word and one packed two-support-signature word. Candidate profitability arithmetic remained demand-time only.

This was the clean test suggested by P5: remove six independent side-container writes/lookups and see whether the successful propagated signature becomes cheap enough to survive complete compilation.

## What survived

The important algorithmic result survived perfectly. P6 and P5 made the same decisions and performed the same algebra on every benchmark case. Gate-P still reduced pair terms to about **{G['symbolic_p6_over_direct']['pair_terms']['geomean_ratio']:.3f}x**, multiplications to **{G['symbolic_p6_over_direct']['multiplications']['geomean_ratio']:.3f}x**, and evaluated ANF nodes to **{G['symbolic_p6_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.3f}x** direct. P6 lowering was **{R(G,'p6_over_direct:lower_ns'):.3f}x direct**, with the 95% interval entirely below 1.

So P6 does not weaken the conclusion that propagated two-support folding can reduce real pre-expansion work and lower wall time once the metadata already exists.

## What failed

The representation hypothesis failed. The simultaneous P6/P5 construction ratio is **{R(G,'p6_build_over_p5:dag_build_ns'):.3f}x**, with a 95% interval of **{CI(G,'p6_build_over_p5:dag_build_ns')[0]:.3f}-{CI(G,'p6_build_over_p5:dag_build_ns')[1]:.3f}**. That is a small but measurable regression rather than the hoped-for improvement.

The reason is plausible from the post-hoc diagnostics. P5's many logical fields live inside compact C-backed `array` and `bytearray` buffers. P6 reduces the number of logical containers and function calls, but each node now carries two Python-object references to Python integers, and signature packing/unpacking becomes Python integer arithmetic. Build-only `tracemalloc` likewise puts P6 at **{profile['summary']['p6_over_p5_geomean']:.3f}x P5** peak allocation.

The cProfile trace should not be used as a timing endpoint, but it confirms that P6 removed P5's array-append-heavy shape while introducing `InNode.__init__`, `pack_sig`, and integer bit-manipulation work. The preregistered randomized timings are the authoritative result.

## Why total pipeline is still close in expensive cases

P6's case-balanced complete-pipeline ratio is **{R(G,'p6_build_over_direct:pipeline_ns'):.3f}x direct**, so the strong endpoint fails. But the workload-weighted ratio is **{G['weighted_p6_build_over_direct:pipeline_ns']:.3f}x**, below 1, because the largest fold-rich cases save enough ANF work to amortize the annotation cost.

This reproduces the P5 crossover rather than improving it. Seven of 36 Gate-P cases beat direct end-to-end, and the depth-stratified pipeline ratio improves from **{G['depth_p6_build_over_direct_pipeline']['6']['geomean_ratio']:.3f}x** at depth 6 to **{G['depth_p6_build_over_direct_pipeline']['10']['geomean_ratio']:.3f}x** at depth 10.

## Natural circuits remain the control

The natural set again accepts zero folds. P6 lower is **{R(N,'p6_over_direct:lower_ns'):.3f}x direct** and complete pipeline is **{R(N,'p6_build_over_direct:pipeline_ns'):.3f}x**. This is useful because it exposes the annotation tax with essentially no algebraic compensation. No natural folding claim is warranted.

## Most informative next experiment

P6 suggests that the next representation should move in the opposite direction from Python in-node objects: keep the **two-word logical design**, but store it in **two C-backed 64-bit arrays (or one compact C/Rust/Cython struct array) indexed by node id**. That would combine P6's two-word compression with the storage property that made P5 surprisingly competitive.

A clean P7A would therefore use exactly:

- `array('Q') meta_word`;
- `array('Q') sig_word`;
- the same P6 packing layout and demand-time profitability arithmetic;
- exact P6/P5 decision equivalence;
- no other selector or threshold change.

That experiment directly tests whether the problem is the *six P5 containers* or the *Python-object placement chosen by P6*.

Separately, P7B could address the other persistent fact: natural formulas almost never activate the fold rule. A very cheap formula-level dispatch gate could bypass annotated construction entirely when amortization is implausible, but its threshold should be calibrated on a circuit-disjoint training set and frozen before held-out evaluation. Keeping P7A and P7B separate would preserve causal interpretability.
'''
(HERE/'N2_P6_INTERPRETATION.md').write_text(interp,encoding='utf-8')

readme='''# N2/P6 Reproducibility README

This bundle contains the frozen P6 preregistration/harness, raw results, the frozen P1-P5/N1 dependencies, the exact EPFL inputs, per-case CSVs, independent verification, and explicitly post-hoc diagnostics.

## Frozen hashes

- `N2_P6_PREREGISTRATION.md`: `898781343d0e9379bdf37d7c053eece3deb9c674b7bc514d2722504d97b0f60b`
- `n2_p6_harness.py`: `6afec487a6a1a91b29fd8c4adc8ac4dcef4c787f9987b24111b00dd82f408030`

## Main reproduction

From `cm_n2_p6_run/`:

```bash
python n2_p6_harness.py --mode fuzz --out fuzz.json
python n2_p6_harness.py --mode selection --out selection.json
python n2_p6_harness.py --mode gatep --out gatep.json
```

Run `--mode natural-case --case-id <id>` for the ten frozen ids in `selection.json`. `cavlc:35` is slow under the execution environment; `run_p6_nat_chunk.py` reproduces the exact frozen schedule in deterministic slices.

Then run:

```bash
python combine_p6_results.py
python independent_verify.py
```

The independent verifier should report `PASS`.

`P6_POSTHOC_PROFILE.txt` and `P6_POSTHOC_BUILD_MEMORY.json` are post-hoc diagnostics and are not part of preregistered pass/fail criteria.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')
shutil.copy2(ROOT/'cm_n2_p4_run/EPFL_SOURCE_MANIFEST.json',HERE/'EPFL_SOURCE_MANIFEST.json')
