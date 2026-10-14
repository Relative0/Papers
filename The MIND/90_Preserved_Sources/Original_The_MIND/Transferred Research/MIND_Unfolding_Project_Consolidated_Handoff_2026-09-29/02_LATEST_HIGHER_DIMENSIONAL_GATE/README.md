# Higher-Dimensional Inversion Complex Classification Gate

This package executes the requested research gate for the carrier-splitting inversion complex.

## Verdict

**Level A — Strong Success (mathematical), with conservative novelty language.**

The strongest result is the **Exclusive-Inversion Matching Theorem**.  If the bipartite graph from `1-only` coarse states to later `0-only` coarse states is a matching, then for every coefficient ring `R`

\[
\widetilde H_n(\operatorname{Cone}(\Delta\pi);R)
\cong
\bigoplus_{(p,z)\in E_\psi}
\widetilde H_{n-2}(\operatorname{lk}_{\Delta Q}[p,z];R).
\]

This is an all-height exact classification and can contain torsion.  The first nonmatching shared endpoint already destroys naive edgewise additivity.

## Main files

- `HIGHER_DIMENSIONAL_INVERSION_GATE.md` — master report and answers to the ten gate questions.
- `EXACT_THEOREMS_AND_PROOFS.md` — theorem statements and proofs.
- `INVERSION_CHAIN_COMPLEX.md` — chain-level and interaction-core formulations.
- `STRUCTURAL_CLASS_COMPARISON.md` — comparison of requested structural programs.
- `COUNTEREXAMPLES_AND_OBSTRUCTIONS.md` — sharpness and minimal failures.
- `BOOLEAN_HORN_CASES.md` — Boolean, Horn, dual-Horn, distributive cases.
- `FIBER_TOPOLOGY_CASES.md` — comparison with controlled-fiber theory.
- `TU_AND_TORSION_AUDIT.md` — TU boundary and torsion audit.
- `COMPUTATIONAL_CLASSIFICATION.md` — finite-search methodology and results.
- `LITERATURE_PRIORITY_MAP.md` — theorem-level prior-art map through September 2026.
- `ADVERSARIAL_REVIEWS.md` — independent and hostile specialist attacks.
- `MANUSCRIPT_REVISION_SECTION.tex` — proposed new paper section (gate reached Level A).
- `MANUSCRIPT_BIBLIOGRAPHY_ADDITIONS.tex` — references needed by that section.
- `HANDOFF_TO_MASTER.md` — compact integration handoff.

## Reproducible computation

- `verify_matching_inversion_theorem.py`
- `verify_boolean_horn_cases.py`
- `verify_distributive_corollary.py`
- `verification_summary.json`
- `boolean_horn_verification.json`
- `distributive_verification.json`
- `computed_case_summary.csv`
- `matching_cases_sample.csv`

Run the three verification scripts with Python 3 and SymPy installed.  The matching script performs exact integral Smith-normal-form calculations for the exhaustive small cases and additional deterministic finite-field checks at five coarse states.
