# Unfolding / Mental Space Research Package

This package is an independent mathematical reconstruction of the unfolding/Mental Space ideas in the 2015 thesis *On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces*.

## Main conclusions

1. The historical distinguishing operator is mathematically meaningful on a fixed factorization, where it computes an exactly-one-false Hamming layer.
2. It is not well-defined modulo Boolean equivalence and is not the ordinary simplicial boundary.
3. A clean repeated-unfolding model is rank traversal on the Boolean lattice.
4. Linearization over \(\mathbf F_2\), or a signed incidence version over general coefficients, gives a genuine square-zero cochain differential. This is an explicit modification, not the original operator.
5. Modern unfolding should use a separate simplicial/refinement map \(U_k\), with the genuine chain differential denoted \(d\). Then \(dU_k=U_kd\) when \(U_k\) is induced by a simplicial map.
6. Mapping-cone or relative homology measures topological changes between observation stages.
7. Bare faces do not reconstruct a filled simplex; rigorous reconstruction requires overlap/provenance/filler/descent data.
8. Homological cycles and symmetry are distinct invariants.

## Files

- `UNFOLDING_RESEARCH_AUDIT.md` — master audit and final classification.
- `THESIS_SOURCE_MAP.md` — structured reconstruction of thesis definitions, examples and claims.
- `FORMAL_UNFOLDING_MODEL.md` — rigorous two-operator model.
- `THEOREMS_AND_COUNTEREXAMPLES.md` — theorem/counterexample ledger.
- `FINITE_EXAMPLES.md` — exact four-attribute chain/homology/gluing prototype.
- `LITERATURE_PRIORITY_MAP.md` — literature and novelty search through 2026.
- `PROPOSED_THEOREM_SEQUENCE.md` — paper-level theorem sequence and strongest next target.
- `unfolding_boolean_audit.py` — Boolean/operator finite verification.
- `finite_complex_audit.py` — simplicial homology, cones, relative homology and automorphism checks.
- `run_all.py` — runs all computations.
- `boolean_audit_results.json` — machine-readable Boolean results.
- `finite_complex_results.json` — machine-readable topological results.
- `run_all_output.txt` — recorded successful run.

## Run

```bash
python3 run_all.py
```

No third-party Python packages are required.

## Strongest next theorem

The package recommends attacking an **Observation–Refinement Descent and Cone Theorem**: prove canonical homology maps for refinement up to contiguity; characterize homologically conservative refinement by cone acyclicity; and give exact reconstruction conditions via descent/colimits.
