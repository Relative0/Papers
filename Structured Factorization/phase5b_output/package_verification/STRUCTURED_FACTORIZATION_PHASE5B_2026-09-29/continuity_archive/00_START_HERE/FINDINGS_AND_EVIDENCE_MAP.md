# FINDINGS AND EVIDENCE MAP

This file maps the important claims to the proof, code, data, and report artifacts that support or attack them. A new agent should use it to avoid re-deriving context from filenames alone.

## Phase 4 — direct extraction and persistent SAT

| Finding | Status | Main exposition | Code | Data/evidence |
|---|---|---|---|---|
| Fixed-cut AND separability iff Boolean flattening rank <= 1 | frozen baseline | `01_KEY_DOCS/PHASE4_MASTER_REPORT.md`, Phase 3 material inside Phase 4 package | `03_UNPACKED_PHASE4/structured_factorization_phase4/baseline_phase3/...` | Phase 3 package material nested in Phase 4 |
| Compressed-SDD cut criterion: factor across vtree cut iff <=1 nonfalse compressed sub | PROVED | `01_KEY_DOCS/PHASE4_SDD_DIRECT_EXTRACTION.md`, `PHASE4_MASTER_REPORT.md` §2.2 | `03_UNPACKED_PHASE4/structured_factorization_phase4/code/sdd_direct_extraction.py` | `.../data/sdd_extraction_validation.json` |
| Recursive compressed-SDD extraction gives finest vtree-laminar factorization | PROVED | same as above | same | exhaustive 4-variable validation |
| Fixed balanced vtree hides many semantic factors | OBSERVED EXHAUSTIVELY | `PHASE4_MASTER_REPORT.md` §2.4 | `sdd_direct_extraction.py` | `sdd_extraction_validation.json` |
| Support-disjoint/read-once CM/LM operator-tree rank recursion | PROVED for stated class | `01_KEY_DOCS/PHASE4_CM_LM_OPERATOR_DAG_THEOREM.md`, `PHASE4_MASTER_REPORT.md` §3 | `.../code/cm_operator_tree_factor.py` | `.../data/operator_tree_validation.json` |
| Persistent selector-controlled four-corner SAT encoding is assumption-equivalent to fresh cut formula | PROVED/VALIDATED | `01_KEY_DOCS/PHASE4_INCREMENTAL_SAT_COMPARATOR.md`, `PHASE4_MASTER_REPORT.md` §4 | `.../code/incremental_four_corner.py`, `validate_incremental.py` | `.../data/incremental_validation.json`, example CNF/queries |
| Direct extraction + residual exact SAT architecture | exact workflow | `01_KEY_DOCS/PHASE4_HYBRID_DIRECT_RESIDUAL_ALGORITHM.md` | Phase 4 code | Phase 4 validation files |
| Learned-clause/runtime speedup from persistent SAT | NOT ESTABLISHED | Phase 4 reports | no industrial CDCL backend used | none — must be tested in Phase 5B |

## Phase 5 — vtree adaptation and defect localization

| Finding | Status | Main exposition | Code | Data/evidence |
|---|---|---|---|---|
| `max_T |E_T(f)| = |Pi_f|` | PROVED | `01_KEY_DOCS/PHASE5_PHASE5_T2_MASTER_REPORT.md` §2, `PHASE5_THEOREM_NOTE_DRAFT.tex` | `04_UNPACKED_PHASE5/phase5_output/code/vtree_exhaustive.py` for small-universe check | `.../data/n4_vtree_exhaustive.json`, `n4_vtree_per_tree.csv` |
| Carrier + semantic blocks are simultaneously vtree subtrees iff combined family is laminar | PROVED | Phase 5 master report §3, theorem note, `PHASE5_VTREE_ADAPTATION_FORMALISM.md` | structural theorem; benchmark code exercises crossing cases | n5 benchmark data |
| Four-corner witness support crossing lemma | PROVED | master report §4, `PHASE5_DEFECT_LOCALIZATION_ANALYSIS.md`, theorem note | `.../code/defect_localization.py` | `.../data/defect_localization_counterexamples.json` |
| Singleton/singleton witness gives sound must-link | PROVED COROLLARY | same | same | same |
| Every failed cut has a singleton-pair witness | REFUTED | master report Theorem 4.3, defect analysis | `defect_localization.py` | `defect_localization_counterexamples.json` |
| Pairwise rank-two interaction graph always recovers semantic prime blocks | REFUTED | same | same | same infinite-family construction/computation |
| Positive irredundant CNF components equal semantic prime factors | PROVED, PRIOR-ART-DOMINATED CONTROL | master report §5 | benchmark generator/analysis | n5 benchmark family |
| Complete n=4 all-function/all-vtree counts | COMPLETE EXHAUSTIVE | `PHASE5_EXHAUSTIVE_SMALL_UNIVERSE_RESULTS.md`, master report §6 | `vtree_exhaustive.py` | `n4_vtree_exhaustive.json`, `n4_vtree_per_tree.csv` |
| n=5 synthetic vtree benchmark | COMPLETE, SMALL/SYNTHETIC | `PHASE5_BENCHMARK_RESULTS.md`, master report §7 | `benchmark_vtrees.py` | `n5_benchmark_results.json`, records/summary CSVs, manifest, stdout |
| Dynamic vtree search, graph-guided compilation, component decomposition, SAT/QBF bi-decomposition have substantial prior art | PRIORITY BOUNDARY | `PHASE5_LITERATURE_PRIORITY_AUDIT.md`, master report §8 | n/a | references recorded in reports; re-search before publication |
| Real SDD + incremental SAT end-to-end improvement | NOT DONE | `PHASE5_NEXT_RESEARCH_GATE.md` | Phase 5B task | no evidence yet |

## Theorem status file

Machine-readable theorem status is preserved at:

`01_KEY_DOCS/PHASE5_theorem_status.csv`

and in the full Phase 5 package at:

`04_UNPACKED_PHASE5/phase5_output/data/theorem_status.csv`

## Reproducibility entry points

For exact commands, package versions, and generation details, read:

- `01_KEY_DOCS/PHASE4_REPRODUCIBILITY.md`
- `01_KEY_DOCS/PHASE5_REPRODUCIBILITY.md`
- the README/reproducibility files inside the full packages.

## Priority warning

The priority audit is an evidence-backed snapshot, not proof of novelty. Before manuscript claims are finalized, the next agent must run a current theorem-level literature search and distinguish:

- established KC/SDD/vtree techniques;
- established Boolean bi-decomposition/component methods;
- genuinely new theorem statements or proof formulations in this project.
