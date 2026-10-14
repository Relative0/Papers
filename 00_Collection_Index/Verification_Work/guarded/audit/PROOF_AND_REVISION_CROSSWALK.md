# Proof and revision crosswalk

The revised file supersedes the uploaded `guarded_boolean_operator_atlases_restricted_dispatch.tex`; it is not a different paper. Section numbers refer to the delivered 14-page revision.

| Original component or objection | Revised location | Disposition and reason |
|:--|:--|:--|
| Exact sign atlas / quotient | Proposition 2.1 | Retained, proved, and described as elementary. Distinguishes finite fibers from possibly infinitely many continuous-score chambers. |
| Semialgebraic finiteness | Section 2.1 | Retained as attributed sign-condition background, not a novelty theorem. |
| Nonlinear four-operator example | Theorem 2.2 | Retained and strengthened by reciprocal convex normal form, replacing informal connectedness reasoning. |
| Positive-coefficient family | Remark 2.3 | Explicit rescaling proves an elementary equivalence; not an independent novel classification. |
| Affine guard obstruction | Lemma 3.1; Theorem 3.2 | Strengthened to the full polynomial degree-cardinality threshold and a lower bound on each of two test polynomials. |
| Coordinates and feature lifting | Section 3.3 | Explicit reciprocal linearization; no coordinate-free impossibility or runtime improvement claimed. |
| Empty-guard uniqueness | Proposition 4.1 | Nonempty guards required; empty guards may be discarded but do not determine unique semantic outputs. |
| Partial observation and dictionary inference | Proposition 4.2 | Adds certified zero-free domain, complete dictionary, nonempty guard, and unique matching restriction. |
| Boundary silently treated as false | Section 4.2; code | Concrete (1,1/2) counterexample; exact trichotomy returns BOUNDARY. |
| Reachability, zero, mixed signs, UNKNOWN | Proposition 4.3; Section 4.3 | Separate collecting semantics and analysis status; no forced completion of unreachable cells. |
| Restricted finite predicate ILP | Section 5.1 | Retained as the classical pair-separation minimum-test-set formulation; no general new optimization claim. |
| Three-probe minimum | Proposition 5.1 | Scoped to the coordinate oracle; distinguishes fixed, adaptive worst case, target-specific, and expected costs. |
| CM/LM lift and representation invariance | Proposition 5.2 | Direct minterm/substitution proof. Free formal frame explicit. No dependence on an unpublished proof. |
| Worked usefulness example | Sections 2.2 and 5.3 | (2,1/2) yields projection X, its numeric CM, and its symbolic LM. |
| Single-entry crossing and trajectory claims | Propositions A.1 and A.2 | Retained as classical calibration; fixed-side sign hypotheses, relative endpoint intervals, and zero-event versus switch distinction. |
| Walsh realization and unary exception | Proposition A.3 | Complete constructive proof in appendix, attributed classical context. No headline novelty claim. |
| Missing current-version review mapping | This audit | Prior critiques mapped to the actual restricted-dispatch source; duplicate report copies not counted as independent reviews. |
| Hardcoded historical output path | Evidence and historical replay | Original failure preserved. Output-path-only repair reproduces historical JSON; new code is path-relative or accepts --out. |
| Historical tautological LM test | Fresh verifier | Replaced by actual minterm evaluation, all-valuation recovery checks, and binary superposition tests. |
| Broad contribution / novelty concern | Introduction, scope, conclusion | Not declared solved. Conditional methods-note positioning replaces broad framework claims. |
| General nonlinear certificate backend | Scope and conclusion | Not implemented and not claimed. The analytic example is complete; a general solver is future work only if pursued as a different contribution. |

The complete source diff is `manuscript_revision.diff`. The report records the reconstructed proof of every formal statement. Bounded tests supplement those proofs rather than replacing them.
