# HANDOFF README — Structured Factorization Research Continuity Package

**Prepared:** 29 September 2026  
**Purpose:** preserve the complete current state of the Structured Factorization research while moving to a different ChatGPT account, and give a fresh GPT-6 Astra Work agent enough context to continue without losing theorem, computation, code, benchmark, literature, or gate history.

## 1. What this package is

This is a **continuity/archive package**, not merely a Phase 5B prompt. It preserves:

- the full Phase 4 research package;
- the full Phase 5 T2 research package;
- the earlier focused Phase 5B handoff package;
- unpacked copies of the Phase 4 and Phase 5 code, data, reports, theorem notes, and reproducibility material;
- the original Phase 5 research request;
- a consolidated project-state snapshot and evidence map;
- the current next-agent prompt;
- broader research files presently available in this account/thread, kept separately so they are not lost during account transfer.

Nothing in `06_BROADER_PROJECT_CONTEXT/` is required to run Phase 5B unless the research itself calls for it. Those files are included for preservation and cross-project continuity.

## 2. Fastest safe reading order for a new agent

Read these files in this order before doing new research:

1. `00_START_HERE/HANDOFF_README.md` — this file.
2. `00_START_HERE/PROJECT_STATE_SNAPSHOT.md` — where the research currently stands.
3. `00_START_HERE/FINDINGS_AND_EVIDENCE_MAP.md` — what is proved/observed/refuted and where the evidence lives.
4. `00_START_HERE/DECISION_AND_GATE_HISTORY.md` — how Phase 3/4/5 converged to the current gate.
5. `00_START_HERE/NEXT_AGENT_PROMPT_PHASE5B.md` — the actual next research task.
6. `01_KEY_DOCS/PHASE5_PHASE5_T2_MASTER_REPORT.md` and `01_KEY_DOCS/PHASE5_NEXT_RESEARCH_GATE.md`.
7. The Phase 4 master report and the key Phase 4 SDD/SAT documents named in the Phase 5B prompt.

After orientation, **execute `NEXT_AGENT_PROMPT_PHASE5B.md` in full**. Do not silently replace it with a broader research agenda.

## 3. Current research state in one paragraph

Phase 4 established exact direct factor extraction for compressed SDDs **relative to vtree alignment**, exact CM-rank recursion for a support-disjoint/read-once CM/LM operator-tree class, and a persistent selector-controlled four-corner SAT encoding whose per-cut variation is expressed by assumptions. Phase 5 then proved an exact factor-exposure optimum over vtrees, a laminar compatibility obstruction for simultaneously hard-locking carrier and semantic factor blocks, and a sound CM-defect support-crossing lemma; it also refuted universal pairwise defect localization by an explicit infinite family. Exhaustive four-variable and synthetic five-variable studies were completed. However, no real industrial SDD compiler + incremental SAT end-to-end runtime campaign was completed. The current gate is therefore **G. MORE RESEARCH REQUIRED**, with a focused Phase 5B industrial validation rather than another broad theory sweep.

## 4. Continuity rules for the new agent

Treat prior theorem claims and empirical numbers as a **frozen research record to reproduce**, not as axioms. Preserve the exact distinction between:

- mathematically proved results;
- computational observations;
- known prior art;
- conjectural/open directions.

Do not use the semantic prime partition in any heuristic vtree objective except explicitly labelled oracle controls/evaluation. Do not turn a failed CM cut into a pairwise must-link unless singleton/singleton support is actually certified. Do not hard-lock carrier blocks across semantic crossings. Heuristics may change efficiency only; they must never change the exact returned factor partition.

Do not claim actual SDD node counts, SDD-size speedups, CDCL conflicts/propagations, learned-clause reuse, or industrial runtime gains unless a real maintained implementation supplied those measurements.

## 5. What the new agent should produce next

The Phase 5B agent should attempt real SDD and assumption-capable incremental SAT tooling, reproduce the frozen Phase 4/5 claims, implement the exact hybrid pipeline, compare standard SDD-size/treewidth/syntax baselines against factor-exposure, soft-carrier, and CM-defect-support objectives on frozen train/validation/held-out splits, and return a new complete research package with all code, data, versions, seeds, reports, theorem updates, negative results, and a clear next gate.

The preferred primary held-out metric is **total exact hybrid runtime**. Secondary metrics include residual SAT calls/work, residual variable volume, actual SDD size, peak memory, and direct factor exposure. Encoding-size reductions must not be mislabeled as solver speedups.

## 6. Important stop rule

If carrier/defect/factor-exposure-aware objectives do not beat standard syntax/treewidth/SDD-size baselines on held-out total runtime or a preregistered residual-work metric, record a **NO-GO** for the algorithmic extension. Preserve the surviving carrier/defect theorems as mathematical results instead of forcing a positive algorithm paper.

## 7. Package layout

- `00_START_HERE/` — orientation, state, evidence map, current prompt, transfer prompt.
- `01_KEY_DOCS/` — curated Phase 4/5 documents that matter most.
- `02_COMPLETE_PACKAGES/` — original complete Phase 4, Phase 5, and earlier Phase 5B ZIPs.
- `03_UNPACKED_PHASE4/` — browseable complete Phase 4 package, including code/data.
- `04_UNPACKED_PHASE5/` — browseable complete Phase 5 T2 package, including code/data.
- `05_ORIGINAL_REQUESTS/` — the original Phase 5 research prompt supplied by the user.
- `06_BROADER_PROJECT_CONTEXT/` — other research source files currently available in this account/thread, preserved for transfer.
- `PACKAGE_MANIFEST.tsv` — file path, size, and SHA-256 for every archived file.
- `SHA256SUMS.txt` — package checksums.

## 8. Preservation rule

Do not overwrite Phase 4 or Phase 5 artifacts. Create new Phase 5B outputs in a new directory/package and retain the older material verbatim for provenance. If a previous result is corrected, record the correction explicitly in a new research ledger and point to the superseded item; do not silently edit history.
