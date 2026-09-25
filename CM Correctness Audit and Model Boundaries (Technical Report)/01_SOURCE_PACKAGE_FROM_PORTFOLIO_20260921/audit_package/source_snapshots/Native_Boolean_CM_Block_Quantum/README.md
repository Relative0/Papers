# Native Boolean CM Block Rebuild

This package rebuilds the CM Bell, GHZ, teleportation, and contextuality calculations using only ordinary Boolean matrices generated from the native four-position CM rotation `P`.

Core evolution uses only:

- Boolean AND on a routed row/column pair;
- XOR to combine routes;
- native CM rotation/permutation;
- ordinary Boolean block-matrix composition;
- tensor/branch wiring and transpose where required.

No separate coefficient-product primitive is used in the implementation.

## Main result

The prior phase algebra survives after a type correction. The 16 phase operators are exactly the 16 Boolean `4 x 4` matrices that commute with the native rotation `P`. A logical one-bit phase state is therefore an ordinary 8-bit Boolean vector, a two-bit state is a 16-bit vector, and the three-bit teleportation/GHZ workspace is a 32-bit vector.

The requested results were rebuilt independently in this representation:

- Bell support contradiction: reproduced exactly.
- Complete 192-basis two-party contextuality classification: reproduced exactly.
- Universal exact teleportation: reproduced with a 32x32 Boolean analyzer and 8x8 Boolean corrections; 1024 input/outcome checks pass.
- Teleportation resource classification: 24,576 of 65,536 resources are universal, exactly those whose 8x8 Boolean resource-transfer matrix has rank 8.
- GHZ support contradiction: reproduced exactly, including the minimum six-context witness.
- Rotation-weighted GHZ negative result: reproduced exactly for the tested basis families.
- Native block gate inventory: 24,576 reversible 8x8 block gates, 512 Boolean-orthogonal block gates, 192 projective reversible measurement bases, and 4 projective orthogonal bases.

A useful new result is that the standard Boolean Bell analyzer preserves the **exact Boolean rank of the resource transfer matrix on every one of its four outcomes**, for all 65,536 resources. Thus it is already rank-optimal for linear information retention. For the `(0,2)` resource its branches have rank 6, whereas the inverse of its natural preparation circuit gives only rank-4 branches. Universal recovery still fails, but the earlier natural analyzer was not optimal for partial transfer.

## Files

- `NATIVE_BLOCK_REBUILD.md` — detailed derivation, proofs, results, and interpretation.
- `RESULTS.md` — compact result ledger.
- `code/native_block.py` — strict Boolean block-matrix engine.
- `code/rebuild_results.py` — exhaustive rebuild and raw-data generator.
- `tests/test_native_block_quantum.py` — regression tests.
- `data/native_rebuild_summary.json` — machine-readable summary.
- `data/contextuality_native_by_rotation_class.csv` — complete 15-class contextuality table.
- `data/native_resource_inventory_65536.csv` — all resources, classes, Boolean ranks, separability, and teleportation status.
- `data/teleportation_native_all_256_x4.csv` — all 1,024 exact teleportation checks.

Run:

```bash
PYTHONPATH=code python code/rebuild_results.py
PYTHONPATH=code pytest -q tests
```

Current regression result: **12 passed**.
