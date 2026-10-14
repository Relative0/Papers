# Native Boolean CM Rotation Phase

Strict-Boolean investigation of CM rotation, the 4x4 phase operator `P`, XOR interference, modal superposition, and the relationship between the native operator algebra and the earlier cyclic-convolution shorthand.

No signed lift, complex amplitude arithmetic, or Born probabilities are used in the core derivations.

## Files

- `NATIVE_ROTATION_PHASE_INVESTIGATION.md` — main report.
- `code/verify_native_rotation.py` — exact finite verification.
- `data/native_rotation_results.json` — structured results.
- `data/console_output.txt` — raw run output.
- `data/test_output.txt` — regression tests.
- `tests/test_native_rotation_phase.py` — 10 tests.

Run:

```bash
python code/verify_native_rotation.py
python -m pytest -q tests/test_native_rotation_phase.py
```
