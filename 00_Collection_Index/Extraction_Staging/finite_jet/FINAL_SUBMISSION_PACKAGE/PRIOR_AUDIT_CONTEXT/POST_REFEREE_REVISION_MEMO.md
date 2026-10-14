# Post-Referee Revision Memo
## *An Elementary Finite-Jet Approach to Sign Laws on Hyperplane Arrangements*
### 27 September 2026

This revision implements the six targeted P1 changes from the fresh adversarial referee pass. The theorem/proof core is preserved; the changes tighten priority, attribution, and quantifier language and add one standard arrangement reference.

## Changes implemented

1. **Broglia--Tognoli applicability is now stated with the missing hypothesis check.**
   - The introduction now records that for `n >= 2` the relevant mod-2 homology hypothesis is automatic on `R^n`.
   - The one-dimensional case is explicitly separated as elementary and covered by the paper's direct argument.
   - The text now acknowledges that Broglia--Tognoli already use a first-nonzero-Taylor-coefficient parity argument in a crossing example.

2. **Finite-order quantifiers were corrected.**
   - The former sentence calling the smooth flatness theorem the "simultaneous all-orders version" was replaced.
   - The paper now states correctly that the smooth theorem gives one common flat point, while the finite-`N` conclusions alone allow the vanishing point to depend on `N`.

3. **The constructive antecedent was strengthened and corrected.**
   - Rainer Remark 3.13 is now the principal general reference for positive-flat functions on prescribed closed sets under the paper's nonquasianalytic framework.
   - Langenbruch remains credited as an underlying/historical source rather than being used through an over-specific proposition whose hypotheses are stronger than the manuscript's minimal assumptions.
   - The manuscript now explicitly observes that a positive-flat function on the arrangement can be signed independently chamber-by-chamber and extended by zero to realize any chamber labeling.
   - The paper then explains why its squared-cutoff selector construction remains useful: it gives a direct explicit formula adapted to the affine defining forms.

4. **The polynomial factor-parity antecedent is now peer-reviewed first.**
   - Broglia--Tognoli Proposition 2.4 is cited as the principal antecedent for parity of factor multiplicities.
   - The 2014 MathOverflow discussion remains only as a secondary informal coordinate-orthant parallel.

5. **Contribution language was recalibrated throughout.**
   - Abstract, introduction, and conclusion no longer suggest that the first-nonzero-Taylor-term idea itself is the contribution.
   - The contribution is stated as the systematic arrangement-level packaging, explicit finite-order formulations, elementary explicit selector formulas, and normalized Denjoy--Carleman synthesis with exact counts.

6. **A standard oriented-matroid reference was added.**
   - Björner--Las Vergnas--Sturmfels--White--Ziegler, *Oriented Matroids*, 2nd ed. (1999), now anchors the standard sign-vector/chamber/tope vocabulary.

## Build and visual QA

- `pdflatex` completed successfully in two passes.
- No LaTeX warnings, undefined references, overfull boxes, or underfull boxes were reported on the final pass.
- The revised PDF is 15 pages (the previous revision was 14 pages).
- All 15 pages were rendered and visually inspected; no clipping, overlap, broken glyphs, or layout defects were found.

## Files

- `finite_jet_sign_laws_postreferee.tex` - revised source
- `finite_jet_sign_laws_postreferee_FINAL.pdf` - compiled manuscript
- `POST_REFEREE_SOURCE_DIFF.patch` - exact diff from the preceding revised note
- `REFEREE_P1_PATCHES_SOURCE.md` - source patch recommendations that prompted this revision
