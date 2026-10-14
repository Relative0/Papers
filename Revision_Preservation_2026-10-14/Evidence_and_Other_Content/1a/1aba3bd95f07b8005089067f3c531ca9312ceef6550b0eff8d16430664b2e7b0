# Paper B restricted-dispatch revision notes

**Manuscript:** *From Continuous Scores to Guarded Boolean Operators: Exact Sign Quotients, Minimal Dispatch, and Fixed-Frame CM/LM Lifts*  
**Date:** 24 September 2026

## Main changes

1. **Restricted exact dispatch added as a first-class layer.**
   - Proves representation invariance: Boolean operator, CM, and fixed-frame LM induce the same equality relation on parameter space because the representation maps are injective.
   - Therefore any parameter-side guard cost has the same optimum for Boolean, CM, and fixed-frame LM dispatch.

2. **Minimum predicate basis formalized.**
   - For a finite certified base partition and finite candidate predicate library, exact dispatch is formulated as a weighted 0-1 hitting-set / minimum-test-set program.
   - The manuscript explicitly attributes the generic optimization problem to the classical minimum-test-set and predicate-minimization literature rather than claiming new NP-hardness.

3. **CM signature size / minimum polarity probes introduced.**
   - Defines the minimum number of truth-table/CM coordinates needed to identify every operator in a known realizable family.
   - Gives the exact binary ILP and the information-theoretic lower bound `ceil(log2 |O|)`.
   - Clarifies that the continuous probes are score signs / CM entries; the full fixed-frame LM is retrieved once the operator is identified.

4. **Principal nonlinear case study changed to** `F(x,y)=x+y+xy` **on signed magnitudes.**
   - Exact atlas: AND, X, Y, XNOR.
   - Three pairwise-disjoint curved polynomial switching boundaries.
   - Exact star transition graph with one CM-entry flip per boundary.
   - Symbolic identities provide strict sign certificates.

5. **Strict guard-language separation proved.**
   - No finite Boolean combination of affine-linear inequalities can represent the complete nonlinear atlas exactly.
   - Three quadratic score-sign predicates suffice.
   - The proof now uses a direct line/curve intersection argument rather than an unstated factorization claim.

6. **Exact probe minimum computed for the nonlinear atlas.**
   - Unique minimum probe set `{10,01,00}`.
   - CM signature size is exactly 3.
   - Score `g11` need not be probed because it is analytically invariant-positive.

7. **Walsh material demoted to an appendix calibration.**
   - Explicitly tied to classical homogeneous dichotomy counts (Cover) and oriented-matroid tope geometry.
   - Corrected unary (`n=1`) adjacency degeneracy is stated explicitly.

8. **Prior-art boundary strengthened.**
   - Adds Moret-Shapiro minimum test sets and Berman-DasGupta-Kao test-set approximation/probe-set work.
   - Keeps DSGRN, logical bifurcation, predicate abstraction, CAD/sign-condition methods, threshold chambers, and CM/LM lift as established antecedents.

## Verification and QA

- The exact symbolic/rational nonlinear verifier returns **PASS**.
- The revised LaTeX compiles to an 18-page PDF with resolved citations/cross-references and no final LaTeX layout warnings.
- The PDF was rendered page-by-page and visually inspected.
- A render comparison against the preceding major-revision PDF was also generated during QA.

## Research boundary after this revision

The manuscript does **not** claim a new generic minimum-test-set hardness theorem or a new CAD/DSGRN algorithm. Its research emphasis is the CM/LM-facing exactness and compression interface: which continuous sign facts are semantically necessary, which restricted predicates/probes are sufficient, and how the resulting finite operator identity transports losslessly into correspondence and logical-matrix representations.
