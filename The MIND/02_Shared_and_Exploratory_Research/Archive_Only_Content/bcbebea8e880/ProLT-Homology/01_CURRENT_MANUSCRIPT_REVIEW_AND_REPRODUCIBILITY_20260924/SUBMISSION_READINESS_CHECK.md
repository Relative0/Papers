# Submission readiness check

**Artifact:** `Binary Order Thinning of Finite Posets: Homology, Collapses, and Sharp Limits`

**Assessment:** **GO for specialist circulation / journal-style submission preparation after panel revision v2.**
The specialist-panel issues identified in the adversarial review have been incorporated.
No mathematical or reproducibility blocker remains in the requested post-audit scope. Journal-specific formatting, author affiliation, and final bibliographic house
style remain ordinary pre-submission tasks rather than mathematical blockers.

## Mathematical gate

- [x] Height convention is explicit: height counts strict inequalities.
- [x] The one-bit height-two relative complex is stated over Z, not only F2.
- [x] All four deleted one-bit triangle patterns and integral signs are shown.
- [x] Root convention is repaired and self-contained.
- [x] Full integral relative homology is proved.
- [x] Torsion-freeness and coefficient independence are proved rather than inferred
  from finite computations.
- [x] Rooted-forest neutrality is converted into an actual free-face collapse.
- [x] The relative-cell matching condition is stated on the correct poset of deleted cells.
- [x] A dedicated two-layer lemma proves acyclic perfect matching <-> literal relative collapse.
- [x] Field coefficient change is justified by the universal coefficient theorem.
- [x] Bit-count failure is extended explicitly to every block size `r>=2` by constant-coordinate padding.
- [x] Empty-defect and isolated-root edge cases are covered.
- [x] Homology computations are not described as homotopy tests without an additional
  theorem.
- [x] The seven-state two-bit example is mathematically explicit and independent of
  the minimality search.
- [x] Determinant `-1`, three fitting orientations, and their signed cancellation are
  recorded.
- [x] No-initial-free-edge obstruction is explicit.
- [x] Both endpoint beat reductions are explicit.
- [x] The n<=6 minimality claim is visibly labelled computer-assisted.
- [x] Higher-height sharpness is proved by the cone--whisker construction.
- [x] Height-three torsion is stated with coefficient and degree qualifications.

## Audit-correction gate

- [x] False `odim_P(Q)=dim_2(Q)` equality removed.
- [x] Dependent total-order hardness argument removed.
- [x] No standalone observation-dimension theory remains.
- [x] Ordinary order-complex homotopy equivalence is distinguished from McCord weak
  equivalence.
- [x] Beat-point arguments are used with explicit reductions/standard hypotheses.
- [x] Horn statements retain semilattice and cofinality hypotheses.
- [x] The missing/empty v0.3 TeX source is not silently reconstructed as historical
  source. The archived PDF was used, and the retained chain theorem is reproved
  self-contained in the new manuscript.
- [x] Coefficient choices and integral-vs-field conclusions are stated explicitly.
- [x] The ProLT interpretation now requires the new observation to factor through the current T0 quotient; carrier-splitting refinements are explicitly excluded from the same-carrier theorem.

## Prior-art gate

- [x] Finite posets/order complexes and finite-space background credited to established
  literature.
- [x] Graph incidence and total unimodularity treated as standard.
- [x] Discrete Morse / acyclic matching machinery treated as standard.
- [x] Bernardi--Klivans rooted forests, fitting orientations, homological weights, and
  cancellation treated as established machinery.
- [x] Ferrers-graph prior-art overlap is disclosed before the chain corollary, with the incomparability/independence-complex correspondence made explicit.
- [x] Dochtermann--Engstrom Proposition 3.7 is cited for the Ferrers independence-complex dichotomy.
- [x] Claesson et al. and Cianci--Ottina use published bibliographic records.
- [x] Horn closure properties are not claimed as novel.
- [x] Contribution language is narrow: exact Boolean order-thinning recognition plus
  sharp limits, not a broad claim to a new topology of logic.

**Nonblocking literature caveat.** The prior-art position follows the completed audit
and its source matrix. As with any submission, a journal referee or an additional
field-specific search can still identify more closely related terminology. The paper
is written so that such an antecedent would affect novelty positioning rather than the
correctness of the central proofs.

## Reproducibility gate

- [x] Seven-state Python verifier rerun successfully (`VERIFIED`).
- [x] C++ exhaustive checker rebuilt with `-O3 -std=c++17`.
- [x] n=1 through n=6 rerun.
- [x] n=6 rerun again covered 4,117 height-two naturally labelled posets and
  16,863,232 two-bit profiles with no counterexample.
- [x] Retained one-bit height/homology and chain verifier rerun successfully.
- [x] Retained repair-forest verifier rerun through n=6 successfully.
- [x] Original absolute-path version of the repair-forest verifier preserved; a
  path-local portable copy is supplied and rerun.
- [x] Exact outputs, convenience scripts, and SHA-256 hashes included.

## Build gate

- [x] LaTeX compiles with `pdflatex`.
- [x] Multiple passes completed; cross-references and bibliography references resolve.
- [x] Final compile log has no LaTeX warnings, undefined references, overfull boxes, or
  underfull boxes detected by the build check.
- [x] PDF rendered to page images after the final content pass.
- [x] New one-bit incidence schematic visually checked.
- [x] New seven-state support-graph figure visually checked.
- [x] Title/abstract page visually checked.
- [x] Seven-state theorem/matrix pages visually checked.
- [x] Exhaustive-search table visually checked.
- [x] Bibliography visually checked.

## Scope gate

- [x] Historical formula-level exact sequences excluded.
- [x] Long mapping-cone/relative-homology tutorials excluded.
- [x] Generic Boolean cochain material excluded.
- [x] Dowker/Stanley--Reisner branch excluded.
- [x] Generic persistence branch excluded.
- [x] Premise/inference-gap homology branch excluded.
- [x] Cognitive/mental-space applications excluded.
- [x] Large Boolean-fragment catalogues excluded.

## Residual nonblocking items before a named-journal submission

1. Add the author's preferred affiliation, ORCID, email, acknowledgements, and funding
   statement if applicable.
2. Convert the neutral article layout to the target journal's class/style.
3. Normalize bibliography entries to that journal's preferred metadata format and,
   if desired, add DOIs to every entry for which one is available.
4. Archive the reproducibility bundle at a persistent repository for the final named-journal submission and replace local file references with a DOI/commit hash. This remains external submission housekeeping because no repository account/identifier was supplied in this editing pass.
5. The historical v0.3 TeX file remains missing/empty. This does not block the new
   manuscript because all retained material is self-contained, but it remains an
   archival housekeeping item for the broader project.
