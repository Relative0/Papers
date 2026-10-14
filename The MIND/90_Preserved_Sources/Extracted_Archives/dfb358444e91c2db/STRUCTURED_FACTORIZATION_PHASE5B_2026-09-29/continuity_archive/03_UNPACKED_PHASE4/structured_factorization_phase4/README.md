# Structured Factorization — Phase 4 Research Package

This package contains the Phase-4 attack requested on 29 September 2026:

1. structured d-DNNF / compressed-SDD direct extraction;
2. CM/LM operator-DAG direct extraction, which resolves exactly on a support-decomposable/read-once tree subclass;
3. selector-controlled incremental four-corner SAT as the exact computational comparator.

## Start here

- `PHASE4_MASTER_REPORT.md` — integrated findings and convergence decision.
- `docs/SDD_DIRECT_EXTRACTION.md` — compressed-SDD cut theorem, vtree-laminar extraction, exhaustive 4-variable study.
- `docs/CM_LM_OPERATOR_DAG_THEOREM.md` — signed CM-rank recursion for read-once operator trees.
- `docs/INCREMENTAL_SAT_COMPARATOR.md` — one-formula selector-controlled four-corner encoding.
- `docs/PRIORITY_AUDIT.md` — literature/priority boundaries.
- `docs/NEXT_RESEARCH_GATE.md` — recommended Phase-5 contracts.

## Code

- `code/sdd_direct_extraction.py`
- `code/cm_operator_tree_factor.py`
- `code/incremental_four_corner.py`
- `code/validate_incremental.py`
- `code/four_corner_sat_phase3_baseline.py`

## Data

- `data/sdd_extraction_validation.json`
- `data/operator_tree_validation.json`
- `data/incremental_validation.json`
- `data/incremental_amortization_sizes.json`
- `data/incremental_example_base.cnf`
- `data/incremental_example_queries.json`

## Principal supported conclusions

- no unrestricted polynomial direct-extraction theorem from arbitrary structured d-DNNF was established;
- compressed SDDs expose exact factorability across a vtree cut and support exact finest vtree-laminar extraction;
- a prime-aligned vtree exposes the full semantic prime factorization;
- support-decomposable/read-once CM/LM operator trees admit exact full factor extraction by local signed CM-rank recursion;
- one permanent carrier-selector four-corner CNF is exactly equivalent, cut by cut, to rebuilding independent four-corner instances;
- incremental SAT itself and read-once factorization are prior art, so claims must focus on the CM/carrier integration and exact cross-layer problem.
