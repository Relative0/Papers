# CM Measurement Audit Package

This directory contains the deliverables for **Correspondence-Matrix Measurement as a Model of Logical Differentiation**.

## Core reports

- `CM_MEASUREMENT_AUDIT.md` — full audit, reconstruction, corrections, computations, and final answers.
- `MEASUREMENT_FORMALISM.md` — proposed rigorous state/effect/refinement/update formalism.
- `SYMMETRY_REDUCTION.md` — stabilizer analysis and corrected distinguishability criterion.
- `QUANTUM_STATUS_AUDIT.md` — classical/modal/GPT/effect-algebra/quantum-cognition boundary.
- `LITERATURE_PRIORITY_MAP.md` — bounded literature and priority search through September 2026.
- `THEOREM_SEQUENCE.md` — proposed theorem sequence for a publishable mathematical note/paper.

## Required tabular outputs

- `PROJECTOR_CLASSIFICATION.csv` — all 16 compact CMs under four multiplication laws.
- `SEQUENTIAL_MEASUREMENTS.csv` — compact-idempotent sequences plus all 256 canonical diagonal-effect sequences.

## Supplementary tables

- `DIAGONAL_EFFECT_PROJECTORS.csv` — image/kernel/rank data for the 16 canonical valuation-space effects.
- `SYMMETRY_TABLE.csv` — operand-swap and `D_4` symmetry data.
- `RESTRICTION_SYMMETRY_TRANSITIONS.csv` — all 256 state/effect restrictions and symmetry changes.
- `THREE_VARIABLE_EMBEDDING.csv` — explicit cylinder-extension examples.

## Reproducibility

- `cm_measurement_compute.py` — exhaustive primary computation.
- `verify_cm_measurement_independent.py` — independent implementation; does not import the primary script.
- `verification_report.json` — records a PASS with 553 assertions.
- `summary.json` — compact numerical summary.

## Main conclusion

The cleanest CM measurement is not "any outer product" and not the spectrum of every compact 2x2 CM. A Boolean CM defines a truth event, which canonically defines a **diagonal sharp effect on valuation space**. Selective measurement is event restriction/conditioning. **Observation refinement** is the separate operation that increases distinguishability. The core effect algebra is commuting/classical; genuinely modal or contextual measurement requires additional state/effect/context axioms.
