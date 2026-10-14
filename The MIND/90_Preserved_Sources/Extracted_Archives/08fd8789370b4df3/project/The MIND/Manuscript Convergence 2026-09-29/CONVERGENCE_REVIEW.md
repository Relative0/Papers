# Manuscript convergence review — 29 September 2026

**Decision:** integrate the transferred matching section and the completed interaction-core gate into a separate v0.4 research draft. The frozen v0.3, original archive, and previous gate records remain unchanged. This is an internal proof/editorial review, not independent peer review or a certification of priority.

## Substantive correction to the frozen baseline

The original Observation–Refinement Descent and Cone Theorem, clauses (e) and (f), conflated reconstruction on a cover of X with reconstruction on a cover of a possibly proper subset Y. Good-cover hypotheses do not make sections on Y uniquely extend to X.

The revised Theorem 11.2 applies the sheaf and cosheaf axioms separately on the support actually covered. Compatible sheaf data on U reconstruct F(X); data on U restricted to Y or on V reconstruct F(Y). Refinement between covers of Y preserves the latter section. The restriction F(X) → F(Y) need not be bijective. For a cosheaf the comparison is G(Y) → G(X), with no isomorphism claimed. The admissible-site hypotheses are stated explicitly.

Example 11.3 records the obstruction: X={a,b} is discrete, Y={a}, and F is the sheaf of integer-valued functions. Singleton covers satisfy the good-cover conditions, but F(X)=Z² → F(Y)=Z is projection; every section on Y has many extensions. The nerve/cone assertions (a)–(d) do not rely on the invalid extension claim and are retained under their stated nerve-theorem hypotheses.

This is a correction of an established manuscript statement, not a new result of the interaction gate. It is deliberately visible in both the paper and this review.

## Theorem hierarchy after integration

| Layer | Retained statement and boundary |
|---|---|
| Observation model | Refinement is not a chain differential; structural homology and semantic descent remain separate. |
| Split completion | The completion is homotopy-neutral; actual refinement is order thinning. |
| Weighted height ≤2 | Rooted-incidence classification, total unimodularity, and the equivalence between acyclicity, rooted forest, relative collapse, and homotopy equivalence. A self-contained signed-incidence and leaf-collapse proof replaces reliance on an external companion. |
| Exclusive matching | Over the stated coefficient ring, cone homology is the sum of coarse edge-link reduced homology shifted by two. Empty links use augmented homology. Matching does not imply torsion-freeness or TU. |
| General mixed cores | Filter C(K,U) by missing-core size. E¹[p,q] is the sum of reduced H_q of the available links; cone degree is p+q−1. Differentials have bidegree (−r,r−1); maximal core size M gives E^(M−1)=E∞. |
| Cores of size ≤3 | C(K,U)=Cone(h)[2]. The cone groups fit the exact kernel/cokernel sequence, with integral extension data retained. Acyclicity is equivalent to h being a quasi-isomorphism. |
| Maximum exclusive degree 2 | E³ collapse is sharp. Excluding a C4 component with both same-colour pairs comparable gives E². Cycles of length ≥6 have no triple cores and admit the edge-link sum. Path endpoint interactions and the shared-middle-edge case are distinguished. |
| All-exclusive stars | E² collapse with cone H_n equal to ordinary H_(n−1)(ΔR), including ordinary H_0. The projective-plane face-poset example creates integral torsion from torsion-free local homology. |
| Whole-relation Horn closure | A nonempty finite meet-closed or join-closed relation and its projection have extrema, hence contractible order complexes. This elementary criterion concerns the whole relation. |

The rooted incidence graph is now denoted D_ψ to distinguish it from the exclusive inversion graph. Augmented links, coefficient conventions, normalized induced simplicial maps, chain-cone convention, and grading shifts are stated near the beginning.

## Negative results explicitly preserved

- Higher-dimensional order thinning can have arbitrary homotopy and torsion phenomena; the low-height graph theorem does not extend universally.
- The three-chain profile (1,0,0) has two contractible coarse edge links but cone H₁=Z. Its available-link interaction map is a primitive signed diagonal Z→Z².
- The seven-state K1,3 example has nonzero primitive d²: Z→Z². Forest, Ferrers, and chordal-bipartite hypotheses alone do not force E² collapse.
- The eight-state C4 example has a unit d²: Z→Z, proving the degree-two E³ bound sharp. The manuscript now lists the relevant links and gives the path-filling argument, in addition to the supplementary integer certificate.
- The 32-state all-exclusive star has cone H₁=Z and H₂=Z/2, although all 181 available links and all 31 coarse edge links have torsion-free homology.
- Spectral-sequence collapse does not determine integral extensions. Signed chain incidences do not imply that induced homology maps are totally unimodular.
- No witness is claimed globally minimal. Induced-restriction minimality and a bounded search are weaker statements.
- The new proper-support descent counterexample is retained alongside the historical negative results.

## Priority and reference audit

The audit positions claims against primary sources; it cannot establish absence of every prior equivalent theorem.

1. **Obstruction complexes:** Λ_S is the induced available-vertex part of the link of S, precisely the vertex-cover obstruction complex used by Chachólski, Jin, Scolamiero, and Tombari. Their general gluing and obstruction machinery is prior art. See the [published paper](https://link.springer.com/article/10.1007/s41468-021-00066-2), including Corollary 7.2 and Theorem 8.6. Candidate distinctiveness lies in the observation-product identification, exact class restrictions, and explicit integral failures.
2. **Poset fibers:** Björner–Wachs–Welker's fiber theorem requires its connectivity hypotheses. The manuscript invokes that framework conditionally and does not claim a blanket wedge decomposition. See the [authors' paper](https://www.math.miami.edu/~wachs/papers/fibers.pdf), Theorem 1.1.
3. **Total unimodularity:** Torsion of the relevant relative groups is central to Dey–Hirani–Krishnamoorthy's TU criterion; torsion-free global homology alone is insufficient. See the [published article](https://epubs.siam.org/doi/10.1137/100800245). The draft confines the unconditional incidence/TU conclusion to weighted height at most two.
4. **Nerves and refinement:** Contiguity of refinement choices and functorial nerve comparisons are classical. The draft cites [Bauer–Kerber–Roll–Rolle](https://arxiv.org/abs/2203.03571), [Ramras](https://link.springer.com/article/10.1007/s00454-025-00809-3), and [Leitão](https://arxiv.org/abs/2602.22784). These are attribution sources, not evidence that the observation-specific classification is already known or new.
5. **Other standard tools:** Chain cones, relative homology, spectral sequences, crosscut methods, and sheaf descent receive standard references. The Fernández–Minian bibliographic record was completed to DCG 63 (2020), 549–559, consistent with the [author's publication list](https://mate.dm.uba.ar/~gminian/publications.html).

The exact specialization remains a candidate contribution. This draft should not be described as publication-priority certified.

## Computation and verification scope

The manuscript distinguishes the transferred matching checks from the interaction-gate evidence: 90,201 exhaustive naturally labelled cases through five coarse states over F₂, 5,000 seeded six-state trials, 435 selected integral comparisons, nine local models, and a separate targeted C4 search. Canonical counts (87 coarse poset types, 16,761 profiles, 70 colour-preserving graph types) are postprocessing of bounded evidence, not new independent trials.

For this convergence phase, `verify_convergence.py` reruns only the two signed integral d² certificates and the torsion-star construction, directing all new outputs to `build/certificates/`. Every mathematical field is compared with the earlier certificates. The first comparison detected differences only in historical minimality annotations: the scripts/input records were updated after the earlier certificates, with revised wording and induced-subset counts. These metadata differences are explicitly preserved in the verification receipt; no mathematical discrepancy was found and no global minimality is inferred. The torsion-star calculation checks the reduced interaction model and all specified links, not a direct Smith reduction of the entire doubled pair. No large exhaustive enumeration was repeated.

The same script verifies the source ZIP hash, all 83 entries in the transferred SHA256 manifest, unchanged prior-gate files, and the integration input/output hashes. `VERIFICATION_RECEIPT.json` records actual results. `PDF_QA_RECEIPT.json` records compilation, page count, and visual inspection. The source builder asserts unique labels, resolved references, and existing bibliography keys.

The earlier gate's statement that LaTeX tooling was unavailable remains historical. The installed MiKTeX works when granted normal access to its existing per-user configuration and cache; sandbox access, not the manuscript source, caused the initial failure. Compilation uses `--disable-installer` and `--disable-write18`; no packages were installed and no shell escape was enabled.

## Editorial disposition and remaining boundaries

v0.4 is an integrated research draft, not a submission-ready article. The broad historical and semantic framework is retained so that integration does not silently discard the transferred project's scope. A focused paper led by the carrier-splitting and interaction theorems may be more suitable for submission, but that is a separate editorial decision.

The archived companion has the title-page author name **Brian Theory**, while the main paper uses **Brian Droncheff**. The bibliography records the archived name transparently; the intended public attribution should be confirmed before submission. The independent mathematical proof supplied here removes a dependency on accessing that companion for the low-height theorem.

No further mathematical theorem is required to finish this convergence phase. Before publication, obtain an independent expert review of the exact specialization and priority positioning, resolve author attribution and venue scope, and prepare a journal-specific version. The optional subsequent research question is whether a degree-two C4 interaction can realize a nonunit d² while all local link homology is free; it was not pursued here.
