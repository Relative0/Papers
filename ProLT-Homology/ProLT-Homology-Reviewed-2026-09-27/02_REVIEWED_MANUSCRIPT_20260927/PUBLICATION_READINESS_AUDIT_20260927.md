# Publication-readiness audit — 27 September 2026

## Manuscript

**Binary Order Thinning of Finite Posets: Homology, Collapses, and Sharp Limits**  
Reviewed/revised source: `binary_order_thinning_finite_posets_reviewed_v3.tex`

## Nature of this review

This was a role-separated specialist and adversarial review performed within ChatGPT, not external human peer review. I deliberately treated the previous audit material in the package as untrusted evidence and rechecked the mathematical and computational claims against the manuscript, source code, fresh local reruns, and a current literature search.

The review perspectives were:

1. finite-poset / finite-topology referee;
2. algebraic-topology and integral-homology referee;
3. discrete-Morse / simple-homotopy referee;
4. algebraic-combinatorics / rooted-forest referee;
5. computational-reproducibility referee;
6. hostile novelty referee (“this is standard machinery in new notation”);
7. hostile correctness/refutability referee (“find a proof gap or a smaller counterexample”);
8. handling-editor pass for focus, claims, presentation, and submission hygiene.

## Executive decision

**Scientific decision: GO for submission as a focused research note / article, after ordinary submission housekeeping.**

I found no unresolved mathematical correctness blocker in the revised manuscript. The principal one-bit theorem, the seven-state two-bit counterexample, the computer-assisted minimality claim, and the cone–whisker higher-height construction survived reconstruction and attack. The main substantive revision was to narrow and document the novelty claim around the rooted-forest / matching / collapse machinery, which has closer antecedents than the earlier draft made explicit.

The residual risks are not theorem failures:

- theorem-level *firstness* can never be established conclusively by search alone; the revised paper now avoids relying on such a claim;
- the exhaustive minimality statement remains computer-assisted by design;
- before an actual journal upload, the author should add whatever author metadata the venue requires and place the reproducibility package in a persistent public archive (commit/tag and preferably DOI), then cite that archive in the manuscript or data-availability field.

## Specialist and hostile referee findings

### Referee A — finite posets / finite topology

**Finding:** The same-carrier thinning model is stated cleanly and the height convention is consistent. The one-bit triangle-word classification produces exactly the claimed relative columns. The cone–whisker construction is valid and the logical-quotient caveat correctly separates same-carrier thinning from refinements that split a current quotient point.

**Requested change:** Keep the finite-space/McCord discussion narrow so that weak homotopy equivalence is not silently upgraded to ordinary homotopy equivalence.

**Disposition:** Already correctly handled in the manuscript; retained.

### Referee B — algebraic topology / integral homology

**Finding:** The relative chain complex at height two is correctly reduced to `C_2 -> C_1`, and the formulas for `H_2`, `H_1`, and `H_0` follow from the rooted incidence graph.

**Attack:** The prior sentence “full row rank and zero cokernel” was too fast over `Z`; full row rank alone only gives finite cokernel.

**Revision made:** The proof now explicitly uses a spanning tree to exhibit a square maximal minor of determinant `±1`, hence the reduced incidence map is surjective over `Z`. This closes the integral-cokernel argument rather than relying on rank alone.

**Disposition:** Resolved.

### Referee C — discrete Morse / simple homotopy

**Finding:** The two-layer matching argument is correct, but the mechanism is not a novelty of this paper. Standard discrete-Morse results already connect suitable acyclic matchings and collapse when the unmatched cells form the target subcomplex; Contreras–Tawfeek give a particularly close rooted-forest formulation.

**Hostile version:** “Lemma 4.1 looks like standard discrete Morse theory repackaged as a new lemma.”

**Revision made:** The lemma is now explicitly described as a two-layer specialization of standard theory, with Forman, Kozlov, and Contreras–Tawfeek cited. The direct proof is retained because it is short and makes the relative collapse order transparent. The main theorem now claims novelty only for the Boolean thinning forcing the reduced-incidence form and for the sharp failure regimes.

**Disposition:** Resolved.

### Referee D — algebraic combinatorics / rooted forests

**Finding:** Bernardi–Klivans and related higher-dimensional rooted-forest work is genuinely close. Mukherjee (2018, 2020) and Contreras–Tawfeek (2024) strengthen the need to distinguish standard forest/fitting-orientation/collapse technology from the new specialization.

**Revision made:** Added and discussed the closest antecedents:

- S. K. Mukherjee, *On the topology of rooted forests in higher dimensions*, Topology Appl. 247 (2018), 50–56;
- S. K. Mukherjee, *On the rooted forests in triangulated closed manifolds*, Linear Multilinear Algebra 68 (2020), 2034–2043;
- I. Contreras and A. R. Tawfeek, *On Discrete Gradient Vector Fields and Laplacians of Simplicial Complexes*, Ann. Comb. 28 (2024), 67–91.

A nearby but mathematically distinct Boolean/order-complex paper was also added:

- A. Björner, M. Goresky, R. MacPherson, *Topological aspects of Boolean functions*, Pure Appl. Math. Q. 20 (2024), 1029–1063.

Their Boolean construction uses the order complex of the true-state subposet, whereas the present paper keeps the carrier and deletes order relations.

**Disposition:** Resolved to the level reasonably possible by literature search. No exact antecedent to the one-bit height-two Boolean *relation-thinning incidence recognition* was found, but the paper does not claim that a search proves firstness.

### Referee E — computational reproducibility

**Finding:** The seven-state checker exactly reconstructs the posets, deleted cells, relative matrix, determinant, `F_2` rank, perfect matchings, deleted-edge degrees, and beat reductions. The exhaustive C++ checker enumerates naturally labelled transitive relations of height at most two and all `4^n` two-bit labellings. Natural labellings are sufficient because every finite poset has a linear extension; isomorphic objects may be duplicated but none are omitted.

**Hostile attack:** “The minimality code only tests `F_2` neutrality and does not test the endpoint homotopy condition, so why does it prove minimality for Theorem 7.2?”

**Revision made:** The proof now states the superset logic explicitly. Every integral-homology-neutral target counterexample is necessarily `F_2`-neutral, so any target example on at most six vertices would lie inside the larger class searched. Therefore the absence of any `F_2`-neutral noncollapsible case already excludes a smaller target example; a separate homotopy test is unnecessary for the lower bound.

**Fresh rerun, 27 September 2026:** all one-bit regression assertions passed. The exact seven-state checker returned `VERIFIED`. The exhaustive checker again returned `NO_COUNTEREXAMPLE` for every `n=1,...,6`; at `n=6` it enumerated 4,117 naturally labelled height-two posets and 16,863,232 two-bit profiles, including 3,767,044 `F_2`-neutral cases.

**Disposition:** Resolved. Remaining best practice is persistent external archiving of the exact code and logs used for submission.

### Hostile Referee 1 — novelty attack

**Attack:** “The paper is graph incidence plus standard discrete Morse/rooted-forest theory dressed in Boolean language.”

**Assessment:** This criticism is partly correct about the machinery and would have been damaging if the paper implied otherwise. It is not correct about the entire paper: the nontrivial content is the recognition that the one-bit height-two thinning rule *forces* the relative boundary into reduced graph-incidence form, yielding coefficient-independent equivalences, together with explicit sharp failures in the bit-count and height directions.

**Revision made:** Rewrote the abstract, introduction, matching lemma, and positioning section to state this boundary explicitly and cite the closest forest/collapse antecedents.

**Disposition:** Resolved as a positioning issue, not a mathematical defect.

### Hostile Referee 2 — “break the theorem or the certificate” attack

**Attack targets:**

- integral cokernel step;
- equivalence of acyclic perfect matching and direct relative collapse;
- possibility that natural labelling misses a poset;
- possibility that the `F_2` filter is too weak to certify target minimality;
- exact seven-state determinant/matching/noncollapse data;
- possibility that both endpoints are not actually contractible.

**Outcome:** One proof-writing gap (integral cokernel justification) was found and repaired. The remaining attacks did not produce a counterexample. Fresh exact computation reproduced determinant `-1`, full `F_2` rank 7, exactly three perfect matchings, all deleted-edge degrees at least two, and beat reductions of both endpoint posets to a point.

**Disposition:** Passed after repair.

## Revision log

The reviewed v3 manuscript incorporates the following substantive changes:

1. narrowed the novelty statement in the abstract;
2. added explicit close-prior-art discussion in the introduction;
3. added Mukherjee 2018, Mukherjee 2020, Contreras–Tawfeek 2024, and Björner–Goresky–MacPherson 2024 to the bibliography;
4. repaired the integral zero-cokernel proof with a `±1` spanning-tree minor;
5. labelled the matching–collapse lemma as a specialization of standard discrete-Morse theory;
6. narrowed the fitting-orientation discussion so standard machinery is not presented as new;
7. added the `F_2`-superset argument to the computer-assisted minimality proof;
8. recorded the fresh independent 27 September 2026 exhaustive rerun in the manuscript;
9. strengthened the positioning section to state exactly what is, and is not, claimed as the contribution.

## Publication-readiness scorecard — revised manuscript

The weighted numerical average is informative only; it does not override a serious correctness, priority, or reproducibility blocker. I found no such blocker after revision.

| Category | Weight | Score / 10 | Confidence | Principal finding |
|---|---:|---:|---|---|
| Mathematical correctness | 20% | **9.2** | High | Core theorems survived reconstruction; one integral proof step was tightened rather than changed. |
| Completeness of proofs/results | 8% | **9.0** | High | Main analytic claims are proved; minimality is clearly and appropriately computer-assisted. |
| Model and assumption discipline | 8% | **9.1** | High | Height, same-carrier thinning, quotient-factorization, coefficient scope, and direct-collapse scope are separated carefully. |
| Novelty and priority | 12% | **7.0** | Moderate | No exact collision found, but rooted-forest/matching/collapse antecedents are close and firstness cannot be certified by search. Claims are now narrowed accordingly. |
| Scientific significance | 8% | **7.5** | Moderate | A focused structural result with clean sharp boundaries; useful but appropriately presented as a specialized theorem rather than a sweeping new theory. |
| Literature coverage and positioning | 8% | **8.7** | High | Closest rooted-forest/discrete-gradient and Boolean/order-complex antecedents are now directly addressed. |
| Reproducibility | 7% | **9.2** | High | Fresh local reruns reproduce the exact example and exhaustive `n<=6` certificate; persistent public archival remains to be done. |
| Internal consistency | 6% | **9.0** | High | Theorem statements, proof scopes, computational claims, and conclusion now agree. |
| Resolution of prior reviewer concerns | 5% | **9.2** | High | Correctness, scope, priority, and reproducibility objections have concrete repairs. |
| Exposition and readability | 5% | **8.4** | Moderate–High | The paper is compact and readable, with an explicit main theorem and worked counterexample; literature positioning is substantially clearer. |
| Scope and structural focus | 4% | **9.0** | High | The paper stays centered on the one-bit theorem and its two sharp failure directions. |
| Evidence and citation quality | 4% | **8.7** | High | Primary/near-primary literature is used for the important positioning claims; computational evidence is separated from analytic proof. |
| Submission hygiene | 3% | **7.3** | High | TeX/PDF build cleanly apart from harmless underfull bibliography lines; venue-specific author metadata and a persistent code archive still need filling. |
| Venue/form fit | 2% | **8.0** | Moderate | Strongest as a focused combinatorial-topology / finite-poset research note or article; exact fit depends on target journal. |

**Weighted score: 8.58 / 10.**

## Submission verdict

### Ready scientifically?

**Yes.** I would now allow the revised manuscript to leave the internal-review loop and go to a real external specialist, preprint server, or journal submission process.

### What I would do before pressing a journal’s final “Submit” button

1. add the author affiliation/email/ORCID and MSC codes if the target venue requests them;
2. archive the exact reproducibility directory at a stable public commit/tag (ideally Zenodo or equivalent) and add the persistent identifier;
3. apply the target journal’s style and data/code-availability requirements.

Those are submission-hygiene items, not reasons for another broad mathematical rewrite.

### Should another broad hostile pass be run first?

**No broad pass is presently warranted.** Another unconstrained pass is more likely to churn wording than change the scientific result. The highest-value next review is a *real independent specialist* focused narrowly on (i) theorem-level priority for the Boolean incidence-recognition result and (ii) the computer-assisted minimality certificate. That is the normal external-peer-review step rather than a reason to keep the manuscript frozen internally.
