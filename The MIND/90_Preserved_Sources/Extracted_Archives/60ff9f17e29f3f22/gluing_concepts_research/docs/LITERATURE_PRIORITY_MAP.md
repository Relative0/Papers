# Literature and Priority Map — Gluing Concepts

## Scope and method

This search was organized by **mathematical structure**, not by the phrase “mental space.” It covered simplicial/categorical gluing, join decomposition, sheaf/cosheaf local-to-global methods, Boolean and relational factorization, Formal Concept Analysis, formal conceptual blending, conceptual spaces, contextuality, and current work through September 2026.

The priority conclusion is conservative: the project contains a useful modern synthesis and one clean cross-layer factorization lemma, but the broad ingredients all have substantial antecedents. No claim that “concepts can be glued” or “concepts can be decomposed” is currently defensible as a new theorem by itself.

## Closest antecedents

| Area | Source | Exact overlap with this project | Priority consequence |
|---|---|---|---|
| Simplicial pushouts/colimits | Standard category of simplicial complexes; e.g. Clara Löh, *Applied Algebraic Topology* lecture notes | Common-face gluing is a categorical colimit; under literal inclusions it is the union after identifying the overlap. | Ordinary simplicial gluing is standard. |
| Mayer–Vietoris | Allen Hatcher, *Algebraic Topology* (2002), Ch. 2 | The short exact chain sequence and resulting long exact Mayer–Vietoris sequence are the standard chain-level account of a union. | Chain-level “interaction of overlap” is useful but not novel. |
| Nerve theorem | Standard nerve theorem; e.g. Chazal–de Silva–Glisse–Oudot course material | A good cover is recoverable up to homotopy from its intersection nerve. | Nerve is an assembly invariant, but not a full semantic reconstruction mechanism. |
| Sheaf gluing | Stacks Project, Tag 006S (current) | Sections agreeing on pairwise overlaps glue uniquely in a sheaf. | The thesis's later “compatible sections” idea has a direct standard formalization. |
| Cosheaves | Justin Curry, *Sheaves, Cosheaves and Applications* (2013), arXiv:1303.3255 | Covariant local-to-global aggregation on cell complexes. | Cosheaf aggregation is a natural tool, not a new construction. |
| Conceptual blending by colimits/pushouts | Bou, Plaza & Schorlemmer, “Amalgams, Colimits, and Conceptual Blending,” in *Concept Invention* (2018); Schorlemmer & Plaza (2021) | Conceptual blending is formalized representation-independently with category-theoretic amalgams/colimits; the 2021 paper proves essential equivalence to Goguen's pushout model in an ordered category of partial maps. | This is the closest direct priority barrier to a broad “gluing concepts by pushout” claim. |
| Formal governing principles for blends | Bourou et al., “Characterising cognitively useful blends” (2024) | Continues the category-theoretic blending program and formalizes integration/topology-preservation principles. | The literature is active and already asks when a blend is structurally appropriate. |
| Sheaf semantic compositionality | Steven Phillips, “Sheaving—a universal construction for semantic compositionality” (2020) | Uses sheafification/local-to-global coherence as a model of semantic compositionality. | Very close to using sheaves to glue local concept information into a coherent whole. |
| Join decomposition of complexes | Kevin Marshall & Jeremy L. Martin, “Hopf monoids of set families,” *Australasian Journal of Combinatorics* 92(3) (2025), 419–449 | For simplicial complexes the product is join; the paper identifies a unique finest join representation via its support-system/fundamental-inflator formalism. | A canonical finest join decomposition is already explicit in current literature. |
| Stanley–Reisner/join factorization | Amelotte & Briggs, “Product decompositions of moment-angle manifolds and B-rigidity” (2023) | Shows a nontrivial tensor-product decomposition of relevant Koszul homology iff the simplicial complex decomposes as a join of full subcomplexes, in its Gorenstein setting. | Algebraic detection of joins has strong prior art. |
| Boolean function decomposition | Ashenhurst, Curtis, Karp; survey: Jan C. Bioch, “Decomposition of Boolean Functions” | Classical variable-partition/function-composition theory for Boolean functions. | General Boolean “disentanglement” is long-established; CM claims must be narrower. |
| Finite relational factorization | Olteanu, Koch & Antova, “World-set decompositions” (2008; ICDT 2007 precursor) | Relational product decomposition, polynomial factorization, and a unique maximal decomposition for WSD relations. | Cartesian semantic factorization and prime factors are established tools. |
| Formal Concept Analysis | Ganter & Wille, *Formal Concept Analysis: Mathematical Foundations*, 2nd ed. (2024) | Entire chapters on “Parts, factors, and bonds” and “Decompositions of concept lattices.” | “Concept factor/decomposition” already has a mature mathematical literature. |
| FCA independent subcontexts | Aragón, Medina-Moreno & Ramírez-Poussa (2025) | Defines independent subcontexts and relates their decompositions to independent blocks of concept lattices. | Especially close to the project's independence/disentanglement vocabulary. |
| Conceptual spaces / composition | Lewis & Lawry (2016) | Hierarchical conjunctive concept combination with non-compositional effects. | Cognitive concept combination is already mathematically developed outside topology. |
| Classical concepts in a Cantor space | Javier Belastegui (2025) | Uses Cantor space for classical concepts and proves compositionality by combining definitions. | Directly relevant to the broader ultrametric/Cantor mental-space direction. |
| Sheaf contextuality | Abramsky & Brandenburger (2011) | Contextuality is characterized as obstruction to global sections over a measurement cover. | Global-section obstruction language is established and should be borrowed precisely. |
| 2026 conceptual blending | Spencer K. Lynn, “Conceptual blending in humans and language models” (2026) | Current cognitive analysis of selective feature integration into blends. | Confirms that “blend is not simply union” remains a current cognitive point, but it does not supply the project's simplicial theorem. |

## High-priority sources with bibliographic details

1. **Schorlemmer, M. & Plaza, E.** “A uniform model of computational conceptual blending.” *Cognitive Systems Research* 65 (2021), 118–137. DOI: `10.1016/j.cogsys.2020.10.003`. The paper explicitly proves essential equivalence between an amalgam-based model and a pushout model of conceptual blending.
2. **Bou, F., Plaza, E. & Schorlemmer, M.** “Amalgams, Colimits, and Conceptual Blending.” In *Concept Invention* (Springer, 2018), pp. 3–29. Book DOI: `10.1007/978-3-319-65602-1`.
3. **Bourou, D. et al.** “Characterising cognitively useful blends: Formalising governing principles of conceptual blending.” *Cognitive Systems Research* 86 (2024), 101245. DOI: `10.1016/j.cogsys.2024.101245`.
4. **Phillips, S.** “Sheaving—a universal construction for semantic compositionality.” *Philosophical Transactions of the Royal Society B* 375 (2020), 20190303. DOI: `10.1098/rstb.2019.0303`.
5. **Marshall, K. & Martin, J. L.** “Hopf monoids of set families.” *Australasian Journal of Combinatorics* 92(3) (2025), 419–449; arXiv:2205.05772. Proposition 5.6 identifies the fundamental inflator with the unique finest join decomposition in the relevant support system.
6. **Amelotte, S. & Briggs, B.** “Product decompositions of moment-angle manifolds and B-rigidity.” *Canadian Mathematical Bulletin* 66 (2023), 1313–1325. DOI: `10.4153/S0008439523000383`.
7. **Olteanu, D., Koch, C. & Antova, L.** “World-set decompositions: Expressiveness and efficient algorithms.” *Theoretical Computer Science* 403 (2008), 265–284. DOI: `10.1016/j.tcs.2008.05.004`; arXiv:0705.4442. The paper gives polynomial relational factorization and states that its WSD minimization produces the unique maximal decomposition.
8. **Bioch, J. C.** “Decomposition of Boolean Functions.” In *Boolean Models and Methods in Mathematics, Computer Science, and Engineering* (Cambridge, 2010/online 2013), pp. 39–76. DOI: `10.1017/CBO9780511780448.005`.
9. **Ganter, B. & Wille, R.** *Formal Concept Analysis: Mathematical Foundations*, 2nd ed. (Springer, 2024). DOI: `10.1007/978-3-031-63422-2`.
10. **Aragón, R. G., Medina-Moreno, J. & Ramírez-Poussa, E.** “Independent subcontexts and blocks of concept lattices. Definitions and relationships to decompose fuzzy contexts.” *Fuzzy Sets and Systems* 509 (2025), 109345. DOI: `10.1016/j.fss.2025.109345`.
11. **Lewis, M. & Lawry, J.** “Hierarchical conceptual spaces for concept combination.” *Artificial Intelligence* 237 (2016), 204–227. DOI: `10.1016/j.artint.2016.04.008`.
12. **Belastegui, J.** “A conceptual space for classical concepts.” *Synthese* 206 (2025), article 71. DOI: `10.1007/s11229-025-05148-7`.
13. **Abramsky, S. & Brandenburger, A.** “The sheaf-theoretic structure of non-locality and contextuality.” *New Journal of Physics* 13 (2011), 113036. arXiv:1102.0264.
14. **Curry, J.** *Sheaves, Cosheaves and Applications* (2013), arXiv:1303.3255.
15. **Stacks Project**, Tag 006S, “Sheaves,” `https://stacks.math.columbia.edu/tag/006S`.
16. **Hatcher, A.** *Algebraic Topology* (Cambridge, 2002), especially Mayer–Vietoris in Chapter 2; freely available from Cornell.
17. **Chazal, F. et al.** computational topology course notes, nerve theorem / good covers, `https://geometrica.saclay.inria.fr/team/Fred.Chazal/papers/CGLcourseNotes/main.pdf`.
18. **Lynn, S. K.** “Conceptual blending in humans and language models.” *Frontiers in Psychology* 17 (2026), 1849083. DOI: `10.3389/fpsyg.2026.1849083`.

## Priority assessment by proposed contribution

### A. “A concept can be glued by a pushout/colimit”
**Priority status: blocked.** This is standard category theory and has been applied directly to conceptual blending.

### B. “Compatible local concept data can be glued by sheaves”
**Priority status: blocked as a broad claim.** The sheaf axiom is standard, and Phillips explicitly used sheafification for semantic compositionality.

### C. “A simplicial complex has a finest join factorization”
**Priority status: blocked as a broad claim.** Current join-decomposition literature already contains a unique-finest representation, and the minimal-nonface criterion used here is an elementary reformulation.

### D. “Boolean/relational concept semantics can be factorized”
**Priority status: blocked as a broad claim.** Boolean functional decomposition and finite relational product factorization are established.

### E. “A structured concept should require the *same partition* to factor both its simplicial carrier and its semantic layer”
**Priority status: plausible synthesis, not yet demonstrated as theorem-level novelty.** The least-common-coarsening theorem in this audit follows quickly once the two prime decompositions are available. I found no source in this search that packages exactly the simplicial-join and semantic-product factors together as a ‘concept’ invariant, but the ingredients are standard enough that this alone should not be advertised as a major new theorem without a dedicated priority search.

### F. “Succinct structured factorization for a compact complex plus Boolean/CM semantics”
**Priority status: promising open direction.** This is where the project may become technically distinctive: avoid explicit truth-table expansion, exploit structural decomposition as a speedup, classify complexity, and prove canonical factorization results for meaningful succinct classes.

## What is defensibly distinctive now?

The strongest defensible contribution is a **disciplined synthesis** that separates four notions that the thesis blended together:

1. non-completing simplicial gluing;
2. completion/filling of a higher simplex;
3. local-to-global semantic coherence;
4. independent-factor decomposition.

The synthesis then forces structural and semantic decompositions to use the same attribute partition. That is a useful research architecture, but the literature search does **not** yet justify a strong novelty claim.
