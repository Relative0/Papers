# p-Adic / Ultrametric Unconscious Audit Package

This package implements the requested modern audit of the 2015 thesis's p-adic / ultrametric unconscious model.

## Files

- `PADIC_UNCONSCIOUS_AUDIT.md` — main mathematical and literature audit.
- `CORRECTED_ULTRAMETRIC_MODEL.md` — rigorous replacement model using prefix ultrametric + observational quotients/filtration.
- `KHERNNIKOV_MATTE_BLANCO_PRIORITY_MAP.md` — chronology and priority map through 2026.
- `FINITE_HIERARCHY_EXAMPLE.md` — explicit four-attribute binary example.
- `THEOREM_COUNTEREXAMPLE_LEDGER.md` — claims classified as proved, standard, false, or requiring modeling assumptions.
- `reproducible_hierarchy.py` — dependency-free computation.
- `balls_depth4.csv` — all 31 prefix balls through depth 4.
- `distance_matrix.csv` — complete 16x16 prefix/2-adic distance matrix.
- `quotients.json` — quotient classes at depths 0-4.
- `computation_summary.json` — verification summary.

## Reproduce

Run:

```bash
python reproducible_hierarchy.py
```

The script exhaustively checks the ultrametric inequality on the 16 depth-4 states and verifies that the prefix distance matches the 2-adic distance under least-significant-digit-first encoding.
