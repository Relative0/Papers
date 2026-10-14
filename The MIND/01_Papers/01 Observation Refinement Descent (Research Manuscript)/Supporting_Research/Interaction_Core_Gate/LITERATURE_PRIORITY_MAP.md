# Literature and priority map: interaction-core gate

Search performed 2026-09-29. This is a targeted primary-source audit through the current date, not a complete proof of priority. Search terms covered vertex-cover obstruction complexes, multi-vertex deletion, filtered relative chains, Ferrers resolutions, chordal-bipartite elimination, and biclique/Dowker constructions. No novelty conclusion rests on absence of the project's vocabulary.

## 1. Exact identification with existing obstruction complexes

Chacholski, Jin, Scolamiero and Tombari, *Homotopical decompositions of simplicial and Vietoris Rips complexes*, J. Applied and Computational Topology 5 (2021), 215-248. [Published primary source](https://link.springer.com/article/10.1007/s41468-021-00066-2); [preprint](https://arxiv.org/abs/2002.03409).

Published Corollary 7.2 gives the multiple-outside-vertices cofiber sequence; Theorem 8.6 bounds the homotopy fibers of a vertex-cover inclusion using obstruction complexes. The preprint numbering differs: Corollary 6.2 and Theorem 7.5.

**Exact translation:** take X=V(K)\\M0, Y=V(K)\\M1, A=X intersection Y=V(L). Then K_X union K_Y=U. For a mixed core S, their St(S,A) is precisely Lambda_S, including the empty-face convention. Their obstructing simplices are exactly the mixed missing cores. Therefore the core indexing and link objects are an instance of their construction. The project must not claim new general obstruction complexes. The product interpretation and any proved special collapse/computation can still be additional content. Priority confidence: high for overlap; low-to-medium for novelty of special formulas.

## 2. Poset-fiber decomposition: compare hypotheses, not slogans

Bjorner, Wachs and Welker, *Poset fiber theorems*, Trans. AMS 357 (2005), 1877-1899. [Author-hosted primary text](https://www.math.miami.edu/~wachs/papers/fibers.pdf).

Theorem 1.1 assumes each lower fiber is ell(f^{-1}(Q_{<q}))-connected and gives a wedge decomposition using lower fibers joined to upper intervals. Theorem 2.5 weakens this to null-homotopy of the relevant attachment maps; Theorem 4.1 gives a homology version with acyclicity and freeness hypotheses.

The interaction computation keeps nontrivial incidence maps rather than assuming they vanish. A two-column collapse therefore is not the displayed wedge formula. However, it is not categorically stronger than fiber theory: it is a narrower exact computation within standard diagram/relative-chain machinery. To claim a new theorem, specify which product-poset hypotheses force the collapse or identify the maps. Priority confidence: high about the distinction; no global priority certification.

## 3. Ferrers resolutions and independence complexes

Corso and Nagel, *Monomial and toric ideals associated to Ferrers graphs*. [Primary preprint](https://arxiv.org/abs/math/0609371). Their Ferrers edge ideals have explicit cellular minimal free resolutions and linearity properties. These are resolutions over a polynomial ring, not this relative simplicial chain complex.

Dochtermann and Engstrom, *Algebraic properties of edge ideals via combinatorial topology*, Electronic J. Combinatorics 16(2) (2009), R2. [Published primary text](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i2r2/pdf/). Proposition 3.7 identifies the independence complex of a Ferrers graph as contractible except in the complete-bipartite case, where it has the homotopy type of two points. Theorem 3.8 counts graph-ideal Betti numbers by Ferrers rectangles.

The project uses chain-supported rectangles with nonconstant available-link complexes attached. Neither cited result identifies that coefficient diagram or its attachment maps. A Ferrers diagram alone does not record same-colour comparabilities. Importing linear resolutions as E2-collapse is unjustified. Priority confidence: high on non-applicability without a new comparison map; moderate that a specialized result could contain additional content.

## 4. Chordal-bipartite elimination and independence topology

Golumbic and Goss, *Perfect Elimination and Chordal Bipartite Graphs* (1978). [Publisher primary record](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.3190020209). Their elimination theory is the classical graph-theoretic starting point; only the abstract/record was accessible in this audit.

Kurita et al., *An Efficient Algorithm for Enumerating Chordal Bipartite Induced Subgraphs in Sparse Graphs*. [Primary preprint](https://arxiv.org/abs/1903.02161). Theorem 5 provides the weak-simplicial vertex elimination characterization. This offers an enumeration/decomposition order, not a collapse of arbitrary decorated core diagrams.

Yetim, *Independence Complexes of Strongly Orderable Graphs* (2022). [Published primary text](https://dergipark.org.tr/en/download/article-file/1557508). Theorem 6 gives a contractible-or-sphere conclusion for chordal-bipartite independence complexes. The carrier cone is not that independence complex: the one-edge matching realization already transfers arbitrary torsion. Therefore this result cannot imply a sphere or torsion-free carrier theorem.

Civan, Deniz, Duginov and Yetim, *Chordal bipartite graphs, biclique vertex partitions and Castelnuovo-Mumford regularity of 1-subdivision graphs*. [Primary preprint](https://arxiv.org/abs/2410.15213). Its independence-complex statements concern subdivided graphs, another object requiring an explicit bridge before use here.

## 5. Biclique and Dowker priority through 2026

Brun and Grinberg, *The Dowker theorem via discrete Morse theory* (2024). [Primary preprint](https://arxiv.org/abs/2407.15454). It uses a biclique complex and explicit acyclic matchings to prove simple-homotopy equivalences between Dowker complexes. Thus bicliques and discrete Morse reductions of relation complexes are established machinery.

De Silva, Giusti, Itskov, Robinson, Sazdanovic, Schonsheck, Vaupel and Yoon, *Dowker's theorem for higher-order relations*, published 8 June 2026. [Published primary source](https://link.springer.com/article/10.1007/s41468-026-00239-x). Theorems 4.3.2 and 5.3.8 give functorial equivalences involving multiway Dowker complexes and a relational product. This was located and checked during the present audit.

Our mixed cores must satisfy same-colour chain conditions and carry a diagram S -> augmented chains of Lambda_S; the plain relation graph does not encode these decorations. No direct implication for the interaction spectral sequence was located. This is a limitation of the comparison, not proof of novelty. Priority confidence: high that broad biclique/Dowker claims would overreach; low-to-medium for an unlocated decorated specialization.

## 6. Theorem-level assessment

| Proposed output | Standard ingredient / closest antecedent | Actual additional content required | Priority assessment |
|---|---|---|---|
| Core-size spectral sequence, E0/E1 and signed d1 | Filtered chain complexes; CJS-T obstruction links | Exact bookkeeping for this product model | Standard machinery, useful explicit implementation |
| Collapse from a bounded number of core columns | Filtration-width argument | Prove structural class really has the asserted bound | Elementary specialized consequence; no broad novelty |
| Two-column exact sequence / iterated chain cone | Long exact sequence and mapping-cone algebra | Identify coefficient maps; handle extensions integrally | Useful exact formula, novelty modest unless simplified further |
| No-four-core theorem, including paths and cycles of length at least six | Above ingredients plus chain support | Transitivity identifies permitted overlap blocks; actual link maps are retained | Proved exact specialized theorem; mechanism standard, priority modest/unconfirmed |
| Unrestricted maximum-degree-two E2 collapse | Three-column spectral sequence | The remaining K2,2 secondary map must vanish | False: eight-state K2,2 has integral unit d2; E3 bound is sharp |
| Ferrers/chordal graph E2 collapse | Graph elimination, resolutions, independence topology | A compatible contraction of the available-link diagram | False in seven-state K1,3 and eight-state K2,2 witnesses; source analogies do not rescue it |
| Arbitrary-pair star realization | Homotopy pushout of a mapping cylinder with a cone | Observe it is realized by one Boolean carrier split | Elementary universality/sharpness corollary |
| All-exclusive star E2 theorem | One-row spectral sequence; ordinary simplicial homology | Identify every available link as two contractible components and all incidence maps | Exact specialized theorem; elementary standard ingredients, modest priority claim |
| Integral torsion created by interaction | Ordinary homology and induced link maps | RP2 face-poset star has torsion-free links but d1 homology Z/2 | Proved by explicit coefficient-diagram identification; direct computation is verification |

## 7. Recommended publication boundary

The defensible claim is an explicit calculation for a structured two-colour deletion in Delta(Q x 2), with proved restrictions on which obstruction complexes can interact. Do not say that obstruction complexes, biclique topology, spectral sequences, or graph elimination are new. A theorem can compute non-neutral cases beyond a sufficient fiber-contractibility criterion while still being a direct specialization of established homological machinery. A final manuscript decision should distinguish mathematical correctness, usefulness, and literature priority; these are separate assessments.
