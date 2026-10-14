# Independent Phase CM Tensor Audit

A robustness test of the native Boolean Correspondence-Matrix quantum-like construction when every subsystem carries its **own** 4-position phase register and multipartite composition is the literal Boolean Kronecker tensor product.

This package deliberately removes the shared-phase-register assumption.

## Main conclusion

Bell and support-GHZ contradictions survive. The 15-class contextuality hierarchy survives in aggregate over the complete 192 P-compatible local basis family. The compact 4-outcome arbitrary-state teleportation protocol does **not** survive; however a complete **64-outcome** Boolean Bell analyzer restores universal exact teleportation for all 256 local 8-bit states. The universal resource criterion remains full Boolean rank 8.

See `INDEPENDENT_PHASE_TENSOR_AUDIT.md` for definitions, proofs, failures, and interpretation.

## Reproduce

```bash
python code/independent_tensor_audit.py
pytest -q
```

Expected regression result: `12 passed`.

## Important files

- `INDEPENDENT_PHASE_TENSOR_AUDIT.md` — full audit
- `RESULTS.md` — short result ledger
- `code/native_block.py` — strict Boolean matrix engine
- `code/independent_tensor_audit.py` — audit and data generator
- `data/independent_tensor_summary.json` — machine-readable summary
- `data/contextuality_literal_choi_by_rotation_class.csv`
- `data/teleportation_literal_256x64.csv`
- `data/phase_bell_effect_basis_16.json`
- `data/ghz_literal_support_contexts.csv`

## Core operation rule

There is no ordinary scalar arithmetic in the CM-native presentation. All matrices are 0/1. Row-by-column composition routes bits with AND and combines converging routes with XOR.
