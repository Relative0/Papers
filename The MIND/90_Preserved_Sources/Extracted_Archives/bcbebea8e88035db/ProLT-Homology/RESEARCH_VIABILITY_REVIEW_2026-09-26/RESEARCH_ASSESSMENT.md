# Research viability assessment — BT

Binary Order Thinning of Finite Posets: Homology, Collapses, and Sharp Limits

Assessment date: **2026-09-26**. Decision: **CONTINUE_FOCUSED_RESEARCH**. Suggested review order: **1 of 16**.

**Recommended form:** Finite-poset topology article; technical report if priority is absorbed.

**External novelty confidence:** Moderate: a specific theorem package survives the comparisons, but firstness is unconfirmed.

## Decision and contribution

This is one of the strongest candidates for continued research. Its value is the exact recognition theorem for **one Boolean observation on a poset of height at most two**, together with sharp failures outside those hypotheses. “Height” counts strict inequalities. The result is substantially more specific than the broad ProLT vocabulary, and does not need that vocabulary to make sense to a topology reader.

The useful new-looking step is not that incidence matrices have torsion-free homology. It is that this particular order-thinning operation produces a reduced graph-incidence matrix and admits a constructive collapse criterion. For an ordered triangle, the four deletion patterns 010, 101, 100 and 110 yield either one deleted edge or two with opposite boundary signs. Deleted edges become graph vertices; triangles become graph edges, with roots for coarse components. This converts the relative chain complex into an object whose cycle and component counts are explicit. The rooted-forest condition then permits leaf pruning to provide actual elementary collapses.

## Claim-by-claim assessment

| Material | Assessment | Ownership |
|---|---|---|
| Binary height-two incidence recognition and integral relative homology | Best candidate for a distinct theorem package; check the reduction and all degenerate cases | BT |
| Forest, acyclic matching, relative acyclicity and literal-collapse equivalence | Potentially useful exact characterization, stronger than merely invoking a sufficient fiber theorem | BT |
| Seven-state two-bit example and height-three torsion boundary | Valuable sharpness evidence; minimality is partly computer-assisted | BT |
| One-bit thinning of a chain; Ferrers-complex dichotomy | Already recognized prior art, useful illustration | BT exposition only |
| General observation fibers and arbitrary safe refinement | Different problem; do not duplicate GR | GR |

[Bernardi–Klivans](https://arxiv.org/html/1512.07757v4) supplies close rooted-forest and matching antecedents, while [Dey–Hirani–Krishnamoorthy](https://arxiv.org/abs/1001.0338) supplies the wider total-unimodularity context. Their presence makes a broad “new forest theory” claim untenable, but does not by itself reproduce the binary-thinning recognition theorem. [Barmak’s Quillen-type result](https://arxiv.org/html/1005.0538) establishes simple homotopy equivalence under fiber conditions; it does not automatically provide the specific literal collapse proved here. [The Ferrers result](https://www.combinatorics.org/Volume_16/PDF/v16i2r2.pdf) is already credited in the manuscript and should remain outside the novelty paragraph. See the linked primary-source comparisons below.

## Proof and prior-review findings

The selected incidence and pruning arguments withstand this reading: a deleted edge cannot lie in a retained triangle; a nonroot leaf identifies the required free face. The seven-state matrix has determinant −1 but several matching terms with cancellation, so invertibility alone cannot justify a free-face elimination order. This is a meaningful boundary, not a cosmetic counterexample.

I broadly agree with the current readiness report’s recommendation to continue, but its earlier rerun claims remain inherited evidence. The full enumeration through six vertices was **not rerun in this review**. The earlier cleanup checked the seven-state certificate; that is also distinct from the fresh checks included here. Before submission, document why naturally labelled representatives and all four-valued profiles exhaust the claimed isomorphism classes, and independently reproduce the minimality run. An enumeration result is not a replacement for that coverage argument.

## Extensions worth testing

1. **Characterize additional multi-bit label patterns with a graph-incidence reduction.** A triangle with two deleted short edges and a retained long edge has two same-sign boundary coefficients, so the binary proof cannot simply be copied. First characterize when row/column reorientations produce genuine incidence columns; then look for a nontrivial label class with a complete criterion. Success is a structural theorem covering an infinite family beyond the current one-bit case. Stop if the statement only says that matrices already known to be incidence matrices have forest behavior.
2. **Produce compact independently checkable collapse/obstruction certificates.** The forest algorithm is already present, so implementing it alone is an artifact contribution. A useful extension would connect it to realistic observation-system inputs, give certificate size/runtime bounds, and exhibit cases where generic homology calculations miss the relevant collapse distinction. Keep the general observation-selection problem in GR.
3. **Study the first higher-dimensional boundary under restricted poset structure.** Arbitrary height is already capable of much more complicated topology. Specify a restricted family before searching, and seek a theorem rather than a larger list of examples.

## Practical gate

Continue with the current focused paper before adding more applications. Prepare a short theorem-to-theorem comparison with the forest literature and a reproducible minimality certificate. If the exact recognition result is found in equivalent language, retain the Boolean-observation formulation and checker as a technical report rather than inflating the novelty claim. No new theorem extension is required merely to justify evaluating this existing candidate.

## Evidence and review limits

Main source lines 175–585 and 710–979; current submission-readiness report; retained enumeration and seven-state certificates.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [ProLT-Homology/01_CURRENT_MANUSCRIPT_REVIEW_AND_REPRODUCIBILITY_20260924/binary_order_thinning_finite_posets_post_audit_v2.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/ProLT-Homology/01_CURRENT_MANUSCRIPT_REVIEW_AND_REPRODUCIBILITY_20260924/binary_order_thinning_finite_posets_post_audit_v2.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `247a079141496d8a458d481abb87f595b91926ebb16011cbe3dc1b19c5918c17`.
- [ProLT-Homology/01_CURRENT_MANUSCRIPT_REVIEW_AND_REPRODUCIBILITY_20260924/SUBMISSION_READINESS_CHECK.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/ProLT-Homology/01_CURRENT_MANUSCRIPT_REVIEW_AND_REPRODUCIBILITY_20260924/SUBMISSION_READINESS_CHECK.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `479c864e8226e3461b7629fc7485672635a6270356583c2e773f9f144dde88d0`.

### Primary-source comparisons

- [Bernardi and Klivans — Directed rooted forests in higher dimension](https://arxiv.org/html/1512.07757v4). Inspected: Relevant full-text discussion of fitting orientations and discrete vector fields. Comparison: Rooted forests and matching language predate BT; a fitting orientation need not be an acyclic gradient matching.
- [Barmak — On Quillen’s Theorem A for posets](https://arxiv.org/html/1005.0538). Inspected: Theorems 1.1–1.2 and comparable-map discussion. Comparison: Contractible inverse images of principal ideals imply simple homotopy equivalence; this is not a literal collapse criterion.
- [Dey, Hirani and Krishnamoorthy — Optimal Homologous Cycles, Total Unimodularity, and Linear Programming](https://arxiv.org/abs/1001.0338). Inspected: Abstract/theorem synopsis. Comparison: Boundary total unimodularity and relative torsion are established; BT must contribute the special incidence recognition.
- [Dochtermann and Engström — Algebraic properties of edge ideals via combinatorial topology](https://www.combinatorics.org/Volume_16/PDF/v16i2r2.pdf). Inspected: Full relevant text: Proposition 3.7 and its folding proof. Comparison: The chain/Ferrers homotopy dichotomy is already credited prior art, not an independent BT novelty claim.
