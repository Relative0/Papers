# Structured Factorization Phase 3

This package continues Phase 2 along the two requested tracks:

1. bounded-width carrier-aware exact factorization;
2. SAT-based four-corner CM factorization.

Start with `PHASE3_MASTER_REPORT.md`.

## Files

- `docs/BOUNDED_WIDTH_CARRIER_AWARE_THEOREM.md` — formal theorem, QBF contract, proof.
- `docs/SAT_FOUR_CORNER_CM_ALGORITHM.md` — SAT construction and carrier-aware refinement.
- `docs/PRIORITY_AND_FRONTIER.md` — literature boundary and next targets.
- `docs/COMPUTATIONAL_VALIDATION.md` — exact validation summary.
- `code/four_corner_sat.py` — DIMACS encoder, validator, baseline factor recovery.
- `code/validate_factor_recovery.py` — exhaustive small-instance cross-check.
- `data/four_corner_selftest.json` — 200 fixed-cut validation records.
- `data/factor_recovery_validation.json` — 80 structured recovery records.
