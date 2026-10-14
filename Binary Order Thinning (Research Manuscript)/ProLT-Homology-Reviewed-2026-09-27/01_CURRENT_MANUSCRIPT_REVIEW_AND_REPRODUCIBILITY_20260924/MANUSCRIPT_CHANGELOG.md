# Manuscript changelog

## Specialist-panel revision v2 - 24 September 2026

This revision implements the adversarial panel audit of post-audit v1.  The central
one-bit theorem and the seven-state counterexample are unchanged in substance; the
revision strengthens the proof architecture, tightens the logical interpretation and
prior-art positioning, and improves exposition.

### A. Matching/collapse logic made self-contained

- Corrected the main theorem's matching condition so it is stated on the relative
  cells themselves rather than referring to cells of `L` as unmatched elements of a
  relative face poset.
- Added the **two-layer matching--collapse lemma** for same-vertex inclusions of
  dimension at most two.  It proves directly that an acyclic perfect matching of the
  deleted edge--triangle incidence graph is equivalent to an actual relative collapse.
- Reworked Proposition 7.1 so direct collapse <-> acyclic perfect matching follows from
  that lemma, while acyclic perfect matching <-> unique perfect matching follows from
  the alternating-cycle/symmetric-difference argument.
- Removed reliance on any overly broad reading of generic discrete Morse theory.

### B. Coefficient change made explicit via UCT

- Replaced the informal field-change sentence with the universal coefficient theorem
  short exact sequence.
- Used freeness of the integral relative groups to kill the Tor term and recover the
  field-dimension formulas.

### C. Logical-observation scope tightened

- Added the required **factor-through-the-current-$T_0$-quotient** hypothesis.
- Explicitly states that if a new observation splits a current observational-equivalence
  class, the refined carrier gains points and is not merely a same-carrier thinning.

### D. Ferrers prior art sharpened

- Identified the incomparability graph of a binary-thinned chain as a Ferrers graph and
  wrote `Delta(Q)=Ind(Inc(Q))` explicitly.
- Added Dochtermann--Engstrom (2009), Proposition 3.7, for the relevant Ferrers
  independence-complex dichotomy.
- Updated Claesson--Kitaev--Ragnarsson--Tenner to the published *Australasian Journal
  of Combinatorics* citation.
- Updated Cianci--Ottina to the published 2018 *Journal of Combinatorial Theory,
  Series A* citation.

### E. Sharpness and terminology tightened

- Strengthened bit-count sharpness from a two-bit failure to failure for every block
  size `r >= 2`, by padding the seven-state labeling with constant coordinates.
- Replaced informal `redundant/defective/nonredundant` labels in the chain theorem and
  Boolean-diamond table with the precise mathematical conditions they denote.

### F. Exposition and visual QA

- Added a schematic of the two one-bit incidence-column types.
- Added the explicit bipartite support graph for the seven-state two-bit example.
- Recompiled to a 16-page PDF with no LaTeX warnings, undefined references, overfull
  boxes, or underfull boxes in the final build log.
- Rendered all pages and visually inspected the new figures, main theorem, chain
  prior-art paragraph, seven-state support graph, logical-interpretation section, and
  bibliography.

## Post-audit reconstruction v1 - 24 September 2026

This is a reconstruction, not a copy-edit of the earlier omnibus ProLT manuscript. The
new paper is organized around one theorem: a single Boolean order thinning of a finite
poset of height at most two has a graph-incidence relative defect, so homology
neutrality is equivalent to a direct simplicial collapse. The paper then proves that
this rigidity is sharp in both bit count and height.

### 1. Central theorem rebuilt in integral form

- Replaced the earlier F2-only height-two matrix framing with the audited integral
  statement.
- Classified the four deleted three-chain profiles `010`, `101`, `100`, and `110`
  with their signed integral boundary coefficients.
- Defined the rooted incidence graph using one formal root per connected component of
  the coarse poset.
- Proved that the relative integral boundary is a reduced oriented graph-incidence
  matrix and therefore totally unimodular.
- Added the complete relative homology formula
  `H_2 = Z^{beta_1(G)}`, `H_1 = Z^{c_0(G)}`, `H_0 = 0`.
- Upgraded the exact recognition theorem so that neutrality over F2, every field, and
  Z are equivalent to the rooted-forest condition, a complete acyclic relative
  matching, direct collapse, simple-homotopy equivalence, and homotopy equivalence.
- Made empty-defect and isolated-root cases explicit.

### 2. Root convention repaired

Earlier block/rooted-forest language could omit deleted edges unsupported by deleted
triangles. The new one-bit theorem uses the audited root convention directly: deleted
edges are graph vertices and each one-entry triangle column attaches its deleted edge
to the unique root of its coarse connected component. The paper does not reuse the
incorrect broader root-row shorthand.

### 3. Two-bit sharpness replaced by the seven-state minimal example

- Removed the older eight-state three-bit example as the principal bit-count boundary.
- Added the explicit seven-element, height-two, two-bit construction.
- Included the full retained order, deleted edges, deleted triangles, exact 7x7
  integral boundary matrix, and determinant `-1`.
- Included all three perfect matchings/fitting orientations and their signed
  determinant contributions `-1,+1,-1`.
- Added the no-free-edge obstruction: deleted-edge triangle degrees are
  `(2,2,3,2,2,2,2)`, so a relative elementary collapse cannot begin.
- Added explicit beat-point reductions of both endpoint posets, proving that both
  order complexes are contractible and the inclusion is nevertheless a homotopy
  equivalence.
- Separated analytic existence from computer-assisted minimality.
- Reran the exhaustive checker through six vertices; the n=6 run again covered
  4,117 height-two naturally labelled posets and 16,863,232 two-bit label profiles
  with no counterexample.

### 4. Higher-height sharpness added in self-contained form

- Added the one-bit cone--whisker theorem for an arbitrary nonempty finite poset R.
- Proved that the coarse complex is a cone while the thinned complex collapses to
  `Delta(R)`.
- Added the shifted relative-homology formula
  `H_k(Delta P, Delta Q; Z) ~= H~_{k-1}(Delta R; Z)` for `k>=1`.
- Recorded the height-three Z/2 torsion consequence from a 13-point projective-plane
  finite model.
- Used this construction to explain, rather than merely assert, why the height-two
  hypothesis is essential.

### 5. Structural sufficient conditions narrowed and qualified

Retained only the repair-map material that directly supports the observation-thinning
interpretation:

- down-repair and up-repair maps;
- false-floor and true-ceiling criteria;
- join-closed falsity / meet-closed truth on finite semilattices;
- Horn-type and dual-Horn consequences with the semilattice and cofinality hypotheses
  stated explicitly;
- a short Boolean-diamond example illustrating redundancy, neutral nonredundancy, and
  a rootless homology defect.

No claim is made that Horn logic or closure operators are novel.

### 6. Chain material demoted to a controlled corollary

- Retained the exact one-bit chain trichotomy and counting formula only briefly.
- Added explicit prior-art caution for the Ferrers-independence-complex antecedent.
- Kept a direct beat-point proof, but did not use the chain theorem as a headline
  novelty claim.

### 7. False observation-dimension material removed

The manuscript contains none of the following audited-out claims:

- `odim_P(Q) = dim_2(Q)`;
- the dependent total-order hardness argument;
- a standalone observation-dimension theory.

The corrected observation-dimension/coloring material remains outside this paper as
recommended by the audit.

### 8. Homotopy language corrected

- The paper distinguishes order-complex homotopy equivalence from McCord's weak
  equivalence between a finite T0 space and its realization.
- Relative Betti-number calculations are never called homotopy tests by themselves.
- Beat-point arguments are used only when an explicit beat reduction is supplied.
- The height convention is stated at the start: height counts strict inequalities.

### 9. v0.3 source issue handled without fabricating history

The archived `ProLT_Controlled_Refinement_Regimes_v0.3.tex` is empty. The archived PDF
was used as the authority for the chain theorem and its proof. The missing historical
TeX source was **not** silently reconstructed and presented as the original. Instead,
the new manuscript contains a new, self-contained statement and proof of the retained
chain corollary, so the submission build has no dependency on the missing source.

### 10. Prior-art positioning tightened

The manuscript explicitly treats as established machinery:

- finite posets, order complexes, and McCord/Barmak finite-space methods;
- relative homology;
- graph incidence and total unimodularity;
- simplicial collapse and discrete Morse theory;
- higher-dimensional rooted forests, fitting orientations, determinant weights, and
  cancellation among several fitting orientations;
- Horn/dual-Horn closure properties;
- the Ferrers-graph antecedent relevant to the chain classification.

The paper positions only the exact Boolean order-thinning specialization and its sharp
limits as contribution candidates.

### 11. Reproducibility upgraded

The `reproducibility/` directory now contains:

- the seven-state exact verifier and both supplied and rerun output;
- the C++ all-posets/all-two-bit-labels checker;
- rerun outputs for n=1 through n=6 plus the supplied n=5/n=6 outputs;
- retained one-bit regression verifiers and rerun logs;
- the original absolute-path repair-forest verifier and a portable path-local copy;
- convenience run scripts and SHA-256 hashes.

### 12. Build and visual QA

The LaTeX manuscript was compiled repeatedly with `pdflatex` until there were no
undefined references/citations, overfull boxes, or LaTeX warnings in the final log.
The resulting PDF was rendered to page images and visually inspected, including the
title/abstract page, the seven-state theorem/matrix pages, the exhaustive-search table,
and the bibliography.
