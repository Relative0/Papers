# Computational Validation — Phase 3

Two independent validation layers were run.

## A. Four-corner SAT encoding

`code/four_corner_sat.py --self-test 200` generated 200 random CNFs with 2--7 variables and random nontrivial cuts. For every instance it compared:

1. satisfiability of the generated four-corner Tseitin CNF; and
2. exhaustive truth-table testing of all `2 x 2` minors of the implicit flattening.

Result:

- **200 tests**;
- **0 disagreements**;
- every SAT model decoded to a four-corner witness whose determinant defect re-evaluated to `1` in the original CNF.

Exact per-instance results are in `data/four_corner_selftest.json`.

## B. Recursive carrier-block factor recovery

`code/validate_factor_recovery.py` generated 80 additional random CNFs on 2--7 variables together with random carrier partitions. The recursive SAT-refinement algorithm was compared against exhaustive enumeration of every partition of the carrier blocks and direct Cartesian-product testing of the satisfying relation.

Result:

- **80 structured instances**;
- **0 factor-partition disagreements**.

On this small random sample:

- mean unordered cuts if individual variables had been searched: **19.35**;
- mean cuts admitted by the supplied carrier blocks before recursive pruning: **2.4125**;
- mean actual four-corner SAT calls made by recursive recovery: **1.825**;
- median ratio `(carrier cuts)/(all variable cuts)`: **1/7 ≈ 0.142857**.

These numbers are only engineering evidence on tiny random instances, not asymptotic performance claims. Exact records are in `data/factor_recovery_validation.json`.
