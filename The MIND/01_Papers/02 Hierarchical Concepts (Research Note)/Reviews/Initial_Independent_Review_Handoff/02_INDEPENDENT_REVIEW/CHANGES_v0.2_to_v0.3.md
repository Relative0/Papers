# Justified manuscript repairs: v0.2 to v0.3

The archived v0.2 and transfer package were not edited. Current files are the v0.3 `.tex`, `.bib`, compiled `.pdf` and generated `.bbl` in `01_CURRENT_MANUSCRIPT/`. Machine-readable unified diffs are beside this report.

| Location | Change | Reason |
|---|---|---|
| Preamble/title | Point to v0.3 bibliography; use an actual LaTeX title line break. | Version correctness and removal of the single-backslash control-space artifact. |
| Introduction | Credit Lauro-Grotto's distant-object/perceptual analogy. | Fresh source evidence makes this a fairer statement of the correction. |
| Introduction | Cite Kleiner §§3.3–3.4. | §3.3 defines the quotient; §3.4 explains accessibility. |
| Introduction | Replace undefined 'complete family' wording with agreement under all cell-constant observables. | Matches the proved theorem without introducing unexplained terminology. |
| Theorem 2.2 | Explicitly call `(X,d)` ultrametric. | Makes the theorem locally readable without relying on contextual inheritance. |
| After Theorem 2.2 | Cite Ishiki Proposition 2.31 as an exact specialization. | His permitted zero internal pseudo-ultrametrics give precisely the displayed collapse; Proposition 2.32 is not needed. |
| Section 3 setup | Explicitly assume a totally bounded ultrametric space; cite the exact Mémoli–Smith–Wan threshold construction. | Repairs a local hypothesis omission and closer prior-art omission. |
| Proposition 3.1 proof | State positive separation/clopenness of completion cells and coordinate continuity; explain eventual constancy of quotient distances and the isometry. | Makes the compact-to-Hausdorff argument complete and the metric identification direct. |
| Prefix specialization | Define zero diagonal explicitly. | Removes an implicit convention. |
| Information section | State `F <= F'` locally; replace 'Neither cardinality' with 'Neither quantity'. | Entropy is not a cardinality; the formula needs refinement. |
| Interpretation | Add Matte-Blanco's own external-description distinction on pp.148–149. | Avoids overstating the historical criticism. |
| Bibliography | Add the 2023 Mémoli–Smith–Wan publication; identify the consulted 2018 Routledge reprint with 1975 origin; tighten Ishiki note. | Primary-source verification and precise attribution. |

No mathematical claim was promoted to novel. The adaptive theorem, all counterexamples and the completion qualification remain intact. No unrelated theory was added. Optional group height-zero/empty-sample explanations were documented in the review rather than lengthening the already correct manuscript.

The build scripts were replaced for the new folder layout. A small unmodified `logreq` dependency is supplied with its original README/license and upstream ZIP because the local TeX installation lacked it. These are build-support changes, not mathematical edits.
