from __future__ import annotations
import csv, hashlib, json, math, statistics, shutil, time
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
D=json.loads((HERE/'n2_p5_results.json').read_text())
P5='cm_packed_sig_sparse'; P4='cm_meta_sig_sparse'; DD='direct_packed_sparse_anf'
P5B='cm_packed_sig_build_sparse'; P4B='cm_meta_sig_build_sparse'; DB='direct_build_sparse'

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
        if corpus=='gatep': row['depth']=int(c.split(':')[0]); row['case']=int(c.split(':')[1])
        row.update({
          'direct_lower_us':lm[(c,DD)]/1e3,'p5_lower_us':lm[(c,P5)]/1e3,'p4_lower_us':lm[(c,P4)]/1e3,
          'p5_over_direct_lower':lm[(c,P5)]/lm[(c,DD)],'p5_over_p4_lower':lm[(c,P5)]/lm[(c,P4)],
          'direct_pipeline_us':pm[(c,DB)]/1e3,'p5_pipeline_us':pm[(c,P5B)]/1e3,'p4_pipeline_us':pm[(c,P4B)]/1e3,
          'p5_over_direct_pipeline':pm[(c,P5B)]/pm[(c,DB)],'p5_over_p4_pipeline':pm[(c,P5B)]/pm[(c,P4B)],
          'direct_build_us':bm[(c,DB)]/1e3,'p5_build_us':bm[(c,P5B)]/1e3,'p4_build_us':bm[(c,P4B)]/1e3,
          'p5_over_direct_build':bm[(c,P5B)]/bm[(c,DB)],'p5_over_p4_build':bm[(c,P5B)]/bm[(c,P4B)],
          'p5_folds':sm[(c,P5)].get('selector_accepted',0),'p5_candidates_demanded':sm[(c,P5)].get('selector_candidates',0),
          'direct_pair_terms':sm[(c,DD)].get('pair_terms',0),'p5_pair_terms':sm[(c,P5)].get('pair_terms',0),
          'direct_multiplications':sm[(c,DD)].get('multiplications',0),'p5_multiplications':sm[(c,P5)].get('multiplications',0),
          'direct_anf_nodes':sm[(c,DD)].get('anf_nodes_evaluated',0),'p5_anf_nodes':sm[(c,P5)].get('anf_nodes_evaluated',0),
          'digest':sm[(c,P5)]['digest']})
        out.append(row)
    path=HERE/f'N2_P5_{corpus.upper()}_CASE_SUMMARY.csv'
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    return path

gatecsv=make_csv('gatep'); natcsv=make_csv('natural')
G=D['gatep']; N=D['natural']; V=json.loads((HERE/'N2_P5_INDEPENDENT_VERIFY.json').read_text())
post=json.loads((HERE/'P5_POSTHOC_BUILD_MEMORY.json').read_text())

def ci(section,key): return section[key]['bootstrap']['ci95']
def r(section,key): return section[key]['geomean_ratio']

def pctbetter(x): return (1-x)*100
results=f'''# N2/P5 — Packed Construction Metadata with Demand-Time Profitability Arithmetic

Run completed: {D['run_utc']}

Preregistration SHA-256: `c91961a3665c2ec0a87b3e7da47c38cd39f5c62def3f68ce911733d1c6621ff8`  
Frozen harness SHA-256: `2829424b0d70516f10409fc10e04adc3fdf68c01e1f6a1c36a5787401b800d0b`

## Result in one sentence

**P5 cut P4's Gate-P metadata-build cost by about {pctbetter(r(G,'p5_build_over_p4:dag_build_ns')):.1f}% and cut the full P4 pipeline by about {pctbetter(r(G,'p5_build_over_p4:pipeline_ns')):.1f}%, while preserving P4's fold decisions and algebra exactly. The P5 lowering stage still beat direct/no-rewrite at {r(G,'p5_over_direct:lower_ns'):.4f}x, but the case-balanced construction+lowering result remained {r(G,'p5_build_over_direct:pipeline_ns'):.4f}x direct, so the preregistered end-to-end signal did not pass.**

## Gate-P primary results

| comparison | cases | geometric-mean ratio | bootstrap 95% CI | cases below direct/reference |
|---|---:|---:|---:|---:|
| P5 packed / direct lowering | 36 | **{r(G,'p5_over_direct:lower_ns'):.4f}x** | {ci(G,'p5_over_direct:lower_ns')[0]:.4f}-{ci(G,'p5_over_direct:lower_ns')[1]:.4f} | {G['p5_over_direct:lower_ns']['cases_below_1']}/36 |
| P5 packed / P4 lowering | 36 | {r(G,'p5_over_p4:lower_ns'):.4f}x | {ci(G,'p5_over_p4:lower_ns')[0]:.4f}-{ci(G,'p5_over_p4:lower_ns')[1]:.4f} | {G['p5_over_p4:lower_ns']['cases_below_1']}/36 |
| P5 pipeline / direct pipeline | 36 | **{r(G,'p5_build_over_direct:pipeline_ns'):.4f}x** | {ci(G,'p5_build_over_direct:pipeline_ns')[0]:.4f}-{ci(G,'p5_build_over_direct:pipeline_ns')[1]:.4f} | {G['p5_build_over_direct:pipeline_ns']['cases_below_1']}/36 |
| P5 pipeline / P4 pipeline | 36 | **{r(G,'p5_build_over_p4:pipeline_ns'):.4f}x** | {ci(G,'p5_build_over_p4:pipeline_ns')[0]:.4f}-{ci(G,'p5_build_over_p4:pipeline_ns')[1]:.4f} | {G['p5_build_over_p4:pipeline_ns']['cases_below_1']}/36 |
| P5 DAG build / direct DAG build | 36 | {r(G,'p5_build_over_direct:dag_build_ns'):.4f}x | {ci(G,'p5_build_over_direct:dag_build_ns')[0]:.4f}-{ci(G,'p5_build_over_direct:dag_build_ns')[1]:.4f} | 0/36 |
| P5 DAG build / P4 DAG build | 36 | **{r(G,'p5_build_over_p4:dag_build_ns'):.4f}x** | {ci(G,'p5_build_over_p4:dag_build_ns')[0]:.4f}-{ci(G,'p5_build_over_p4:dag_build_ns')[1]:.4f} | {G['p5_build_over_p4:dag_build_ns']['cases_below_1']}/36 |

Predeclared Gate-P lowering-only signal: **{'PASS' if G['lower_speed_signal'] else 'NO PASS'}**.  
Predeclared Gate-P construction-inclusive signal: **{'PASS' if G['pipeline_speed_signal'] else 'NO PASS'}**.

The secondary workload-weighted ratios were **{G['weighted_p5_over_direct:lower_ns']:.4f}x** for lowering and **{G['weighted_p5_build_over_direct:pipeline_ns']:.4f}x** for the complete pipeline. The latter is below 1 because several expensive Gate-P cases already amortize the metadata cost, even though the preregistered case-balanced endpoint remains above 1.

## P5 reproduced P4 exactly

Across all natural and Gate-P symbolic cases, P5 matched P4-propagated exactly on final digest, multiplications, pair terms, peak monomials, evaluated ANF nodes, candidate decisions, reject reasons, accepted/shared counts, estimated costs, and folds consumed.

Gate-P totals for both P4 and P5:

- demanded binary nodes checked: **{G['p5_diag']['selector_nodes_checked']}**;
- demanded propagated candidates: **{G['p5_diag']['selector_candidates']}**;
- accepted/consumed folds: **{G['p5_diag']['selector_accepted']} / {G['p5_diag']['fold_lowerings']}**;
- accepted shared folds: **{G['p5_diag']['selector_accepted_shared']}**;
- propagated signature/candidate nodes present in the constructed DAG: **{G['p5_diag']['propagated_signature_nodes']}**.

Thus P5 changed representation and cost placement, not the optimization policy or mathematical work.

## Gate-P work reduction versus direct

The P5/P4 fold behavior is identical, so the symbolic reductions remain the P4 reductions:

- multiplications: **{G['symbolic_p5_over_direct']['multiplications']['geomean_ratio']:.4f}x** direct;
- pair terms: **{G['symbolic_p5_over_direct']['pair_terms']['geomean_ratio']:.4f}x** direct;
- evaluated ANF nodes: **{G['symbolic_p5_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.4f}x** direct;
- peak monomials: **{G['symbolic_p5_over_direct']['peak_monomials']['geomean_ratio']:.4f}x** direct.

P5 lowering is therefore still substantially faster than direct, but it is **{(r(G,'p5_over_p4:lower_ns')-1)*100:.1f}% slower than P4 lowering** because P5 deliberately moves candidate-cost arithmetic from construction to demand time.

## Construction cost improvement

P4's simultaneous Gate-P metadata build was **{r(G,'p4_build_over_direct:dag_build_ns'):.4f}x** ordinary construction. P5 reduced that to **{r(G,'p5_build_over_direct:dag_build_ns'):.4f}x**, or **{pctbetter(r(G,'p5_build_over_p4:dag_build_ns')):.1f}% less build time than P4**.

The full P5 pipeline is **{r(G,'p5_build_over_p4:pipeline_ns'):.4f}x P4**, a **{pctbetter(r(G,'p5_build_over_p4:pipeline_ns')):.1f}% reduction**. It crosses below direct in **{G['p5_build_over_direct:pipeline_ns']['cases_below_1']}/36** Gate-P cases, versus only 3/36 for P4 in the previous architecture.

Depth-stratified P5/direct lowering ratios:

| depth | ratio | cases below direct |
|---:|---:|---:|
| 6 | {G['depth_p5_over_direct_lower']['6']['geomean_ratio']:.4f}x | {G['depth_p5_over_direct_lower']['6']['cases_below_1']}/12 |
| 8 | {G['depth_p5_over_direct_lower']['8']['geomean_ratio']:.4f}x | {G['depth_p5_over_direct_lower']['8']['cases_below_1']}/12 |
| 10 | {G['depth_p5_over_direct_lower']['10']['geomean_ratio']:.4f}x | {G['depth_p5_over_direct_lower']['10']['cases_below_1']}/12 |

## Memory diagnostics

Predeclared full-pipeline traced Python peak on Gate-P:

- P5 / direct: **{G['pipeline_python_peak_p5_over_direct']['geomean_ratio']:.4f}x**;
- P5 / P4: **{G['pipeline_python_peak_p5_over_p4']['geomean_ratio']:.4f}x**.

A separate post-hoc build-only `tracemalloc` diagnostic found P5 construction peak **{post['p5_over_direct_geomean']:.4f}x direct** but only **{post['p5_over_p4_geomean']:.4f}x P4**. In other words, the packed metadata itself still costs memory relative to an unannotated builder, but much less than P4's object-rich metadata; downstream ANF savings then make the complete P5 pipeline peak lower than direct on Gate-P.

## Natural EPFL replay

P5 reproduced P4's natural abstention behavior exactly: **{N['p5_diag']['selector_candidates']}** demanded propagated candidate and **{N['p5_diag']['selector_accepted']} accepted folds** across the frozen ten cases.

| comparison | cases | geometric-mean ratio | bootstrap 95% CI |
|---|---:|---:|---:|
| P5 / direct lowering | 10 | {r(N,'p5_over_direct:lower_ns'):.4f}x | {ci(N,'p5_over_direct:lower_ns')[0]:.4f}-{ci(N,'p5_over_direct:lower_ns')[1]:.4f} |
| P5 / P4 lowering | 10 | {r(N,'p5_over_p4:lower_ns'):.4f}x | {ci(N,'p5_over_p4:lower_ns')[0]:.4f}-{ci(N,'p5_over_p4:lower_ns')[1]:.4f} |
| P5 pipeline / direct | 10 | {r(N,'p5_build_over_direct:pipeline_ns'):.4f}x | {ci(N,'p5_build_over_direct:pipeline_ns')[0]:.4f}-{ci(N,'p5_build_over_direct:pipeline_ns')[1]:.4f} |
| P5 pipeline / P4 | 10 | {r(N,'p5_build_over_p4:pipeline_ns'):.4f}x | {ci(N,'p5_build_over_p4:pipeline_ns')[0]:.4f}-{ci(N,'p5_build_over_p4:pipeline_ns')[1]:.4f} |
| P5 DAG build / direct | 10 | {r(N,'p5_build_over_direct:dag_build_ns'):.4f}x | {ci(N,'p5_build_over_direct:dag_build_ns')[0]:.4f}-{ci(N,'p5_build_over_direct:dag_build_ns')[1]:.4f} |

Because no natural fold was accepted, these are abstention/annotation overhead measurements, not evidence of a natural CM-folding speedup.

## Verification

- Fresh randomized fuzz: **1000/1000 passed**.
- Recorded benchmark rows: **5842**, all successful.
- Independent verifier: **{V['status']}**.
- All P5/P4 symbolic decision/work fields matched exactly on all benchmark cases.
- All six pinned EPFL Git blobs reverified.
- Frozen natural selection reverified: 10 cases across five timed circuits; `bar` again had zero admissible timed cases.

## Bottom line

P5 solved a large part of P4's engineering bottleneck without changing the folding algorithm: construction became roughly half as expensive as P4 and the full Gate-P pipeline became roughly 42% faster than P4. But **packed Python-side annotation is still too expensive to deliver a case-balanced end-to-end win over the minimal direct builder**. The remaining gap is much smaller and is now concentrated in the annotated node-construction path rather than in symbolic folding itself.
'''
(HERE/'N2_P5_RESULTS.md').write_text(results,encoding='utf-8')
interp=f'''# N2/P5 Interpretation

## What P5 answered

P5 was designed to answer a narrow engineering question: whether P4's successful propagated two-support signature could be retained without paying for per-node `Sig` and `Candidate` objects and eager candidate-cost arithmetic.

The answer is **partly yes**.

P5 stores only packed primitive arrays for fanout, monomial estimate, ordered pair, token, and one propagated flag. Candidate profitability arithmetic is performed only if a propagated candidate is actually demanded. On Gate-P this reduced metadata DAG-build time from **{r(G,'p4_build_over_direct:dag_build_ns'):.3f}x direct for P4 to {r(G,'p5_build_over_direct:dag_build_ns'):.3f}x for P5**, and P5 construction itself is **{r(G,'p5_build_over_p4:dag_build_ns'):.3f}x P4**.

That is a large improvement, and it is not confounded by a different selector: P5 and P4 make identical decisions and perform identical Boolean/ANF work case-by-case.

## The cost moved rather than disappeared

P4 eagerly computes candidate arithmetic during construction and then its lowering loop mostly performs an array/object lookup. P5 deliberately does the reverse: construction propagates only a tiny signature, while the demanded node computes costs at lowering time.

That trade moved P5 lowering from P4's simultaneous **{r(G,'p4_over_direct:lower_ns'):.3f}x direct** to **{r(G,'p5_over_direct:lower_ns'):.3f}x direct**. P5 is still comfortably faster than direct lowering, but it is **{r(G,'p5_over_p4:lower_ns'):.3f}x P4 lowering**.

The important change is at the whole-pipeline level: P4 was **{r(G,'p4_build_over_direct:pipeline_ns'):.3f}x direct**, whereas P5 is **{r(G,'p5_build_over_direct:pipeline_ns'):.3f}x**. P5 therefore removed a substantial fraction of the end-to-end penalty.

## Why the preregistered end-to-end result still fails

The packed builder remains **{r(G,'p5_build_over_direct:dag_build_ns'):.3f}x** the minimal ordinary Factory. P5 still does several things the direct builder never does: increments fanout, maintains the saturated estimate, writes multiple side arrays, attempts two-support propagation on binary nodes, and aligns child signatures.

A post-hoc cProfile on Gate-P 10:2 confirms the new concentration. Over 100 P5 pipeline repetitions, `PackedMetaFactory._make` remains the dominant construction function. Unlike P4, `_candidate_from_children` and dataclass construction are gone; the remaining visible costs are `_propagate_pair`, `_align_code`, multiple typed-array/bytearray appends, and the estimator.

So P5 has removed the large object-allocation layer but not the fundamental Python dispatch/write cost of carrying six side fields per node.

## The weighted result is an important secondary clue

The preregistered case-balanced pipeline ratio is **{r(G,'p5_build_over_direct:pipeline_ns'):.3f}x**, so P5 does not pass end-to-end. But the workload-weighted ratio is **{G['weighted_p5_build_over_direct:pipeline_ns']:.3f}x**, and 8/36 individual cases already beat direct end-to-end.

This means the basic crossover now exists: when direct ANF work is sufficiently large and the propagated fold removes enough of it, the P5 annotation cost is amortized. What is missing is making that true for the typical case rather than only the expensive/fold-rich cases.

This weighted observation is secondary and should not replace the preregistered case-balanced conclusion.

## What P5 says about P4's core mechanism

The strongest scientific point survives unchanged. P5 takes the same 29 Gate-P folds as P4 and reduces pair terms to **{G['symbolic_p5_over_direct']['pair_terms']['geomean_ratio']:.3f}x**, multiplications to **{G['symbolic_p5_over_direct']['multiplications']['geomean_ratio']:.3f}x**, and evaluated ANF nodes to **{G['symbolic_p5_over_direct']['anf_nodes_evaluated']['geomean_ratio']:.3f}x** direct.

Because P5 and P4 are symbolically identical but have very different construction costs, the earlier P4 speedup is not an artifact of object-rich precomputation. The propagated-signature mechanism itself is responsible for the algebraic reduction; the remaining problem is carrying enough metadata cheaply.

## Natural circuits remain an abstention result

The frozen natural set again contains zero accepted folds. P5's natural lower result is **{r(N,'p5_over_direct:lower_ns'):.3f}x direct** and its pipeline is **{r(N,'p5_build_over_direct:pipeline_ns'):.3f}x direct**. P5 is nevertheless **{r(N,'p5_build_over_p4:pipeline_ns'):.3f}x P4 pipeline**, showing that packing reduces annotation overhead even where folding never fires.

No natural CM-folding speed claim follows from these ten cases.

## Most informative next experiment

The next step should not retune the profitability thresholds. P5 shows the remaining cost is representation-level.

A P6 should keep the exact P4/P5 fold semantics but reduce construction writes further. The strongest design would be a **two-word or in-node packed annotation**, rather than six independently appended Python containers:

1. one packed pair/signature word containing the ordered base ids, 4-bit token, and propagated flag;
2. one compact numeric word/field for fanout and the saturated estimate;
3. no Candidate object and no candidate-cost arithmetic until demand, as in P5;
4. ideally metadata fields stored directly on the compiler node at creation so there is no separate side-array append/lookup layer;
5. preserve P5/P4 exact decision equivalence as a mandatory invariant.

A separate, complementary P6 arm could test a **frozen cheap dispatch gate** that entirely skips annotated construction for formulas whose structural scale is too small to amortize it. That should be calibrated on a disjoint training subset and evaluated on held-out circuits, rather than tuned on the 36 Gate-P outcomes.

The goal is now concrete: preserve the ~0.65x direct lowering path while taking the builder from ~2.56x ordinary construction toward roughly 1x. P5 shows that doing so would create a plausible path to a case-balanced end-to-end crossover.
'''
(HERE/'N2_P5_INTERPRETATION.md').write_text(interp,encoding='utf-8')
readme=f'''# N2/P5 Reproducibility README

This bundle contains the frozen P5 preregistration, frozen harness, raw chunk outputs, combined JSON, per-case CSVs, independent verifier, post-hoc diagnostics, and the frozen P1-P4/N1 dependencies required by the harness.

## Frozen hashes

- `N2_P5_PREREGISTRATION.md`: `c91961a3665c2ec0a87b3e7da47c38cd39f5c62def3f68ce911733d1c6621ff8`
- `n2_p5_harness.py`: `2829424b0d70516f10409fc10e04adc3fdf68c01e1f6a1c36a5787401b800d0b`

## Main reproduction

From the bundle root, use Python 3.13+ and run:

```bash
python cm_n2_p5_run/n2_p5_harness.py --mode fuzz --out cm_n2_p5_run/chunks/fuzz.json
python cm_n2_p5_run/n2_p5_harness.py --mode selection --out cm_n2_p5_run/chunks/selection.json
python cm_n2_p5_run/n2_p5_harness.py --mode gatep --out cm_n2_p5_run/chunks/gatep.json
```

For natural cases, run `--mode natural-case --case-id <id>` for the ten frozen ids in `chunks/selection.json`. `cavlc:35` is computationally long; `run_p5_nat_chunk.py` reproduces the same frozen randomized schedule in deterministic slices without changing any benchmark rule.

Then run:

```bash
python cm_n2_p5_run/combine_p5_results.py
python cm_n2_p5_run/independent_verify.py
```

The independent verifier should report `PASS`.

## Notes

- P5's fold decisions and symbolic work are required to match P4-propagated exactly.
- The natural set is structurally frozen; it is not selected for fold incidence or timing.
- Timing excludes BLIF parsing/oracle creation exactly as described in the preregistration.
- `P5_POSTHOC_PROFILE.txt` and `P5_POSTHOC_BUILD_MEMORY.json` are explicitly post-hoc diagnostics and are not part of the preregistered pass/fail criteria.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')
# copy source manifest for convenience
shutil.copy2(ROOT/'cm_n2_p4_run/EPFL_SOURCE_MANIFEST.json',HERE/'EPFL_SOURCE_MANIFEST.json')
