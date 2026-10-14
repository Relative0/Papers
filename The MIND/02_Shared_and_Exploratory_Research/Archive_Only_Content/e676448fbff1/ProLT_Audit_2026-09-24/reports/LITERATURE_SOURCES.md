# Literature sources and search record

Audit date: 24 September 2026. The identifiers below are used throughout the reports and claim table. URLs are included for independent checking. A title in this list does **not** mean that every result in that source was audited. Access scope is stated explicitly. This was a web-based primary-literature investigation, not a MathSciNet/Zentralblatt subscription search or a certified exhaustive novelty search.

## R01. Finite-space realization
Michael C. McCord, *Singular homology groups and homotopy groups of finite topological spaces*, Duke Mathematical Journal 33 (1966), 465-474. DOI: https://doi.org/10.1215/S0012-7094-66-03352-7 . Bibliographic entry and the relevant realization theorem were checked through R02. McCord's realization map is a **weak** homotopy equivalence. The finite Kolmogorov-quotient equivalence also has the elementary representative-section proof given in the master report; do not attribute an ordinary equivalence between every finite space and its order-complex realization to McCord.

## R02. Poset fibers, comparable maps, and Dowker duality
Jonathan A. Barmak, *On Quillen's Theorem A for posets*, Journal of Combinatorial Theory, Series A 118 (2011), 2445-2453. https://arxiv.org/abs/1005.0538 ; inspected full HTML: https://arxiv.org/html/1005.0538v1 . Exact overlaps: Theorems 1.1 and 1.2 (principal lower-fiber criterion and simple-homotopy strengthening), Proposition 2.2 (pointwise comparable monotone maps), Theorem 4.4 (Dowker duality, even simple type), and Theorem 5.4/Corollary 5.5 (homological versions). Dual upper-fiber versions follow by reversing orders. The paper's convention for lower-set topology must not silently replace the core's upper-set convention.

Related background: J. A. Barmak and E. G. Minian, *Simple homotopy types and finite spaces*, Advances in Mathematics 218 (2008), 87-104; located in R02's bibliography. This related paper was not independently read in full during this audit.

## R03. Higher-dimensional rooted forests and fitting orientations
Olivier Bernardi and Caroline J. Klivans, *Directed rooted forests in higher dimension*, Electronic Journal of Combinatorics 23(4) (2016), P4.35. DOI: https://doi.org/10.37236/5819 . https://arxiv.org/abs/1512.07757 ; inspected HTML and selected PDF pages: https://arxiv.org/html/1512.07757v4 . Exact overlaps: definitions of rooted forests and fitting orientations; Lemmas 14 and 17 on reduced boundary determinants/relative homology; Proposition 30 on the signed fitting-orientation expansion. These are the established objects underlying v0.5, not independent ProLT inventions.

## R04. Total unimodularity and relative torsion
Tamal K. Dey, Anil N. Hirani, and Bala Krishnamoorthy, *Optimal homologous cycles, total unimodularity, and linear programming*, SIAM Journal on Computing 40(4) (2011), 1026-1044. https://arxiv.org/abs/1001.0338 ; inspected https://arxiv.org/html/1001.0338v3 . Theorem 5.2 connects total unimodularity of boundary matrices with torsion-freeness for suitable relative pairs. Graph-incidence total unimodularity is considerably more elementary; the audit gives its direct proof rather than pretending that a new general TU theorem is needed.

## R05. Contractibility undecidability
Martin Tancer, *Recognition of collapsible complexes is NP-complete*, Discrete & Computational Geometry 55 (2016), 21-38. DOI: https://doi.org/10.1007/s00454-015-9747-1 . https://arxiv.org/abs/1211.6254 ; inspected Appendix A, Theorem 11 and its proof/discussion in the PDF. The stated safe form is undecidability of contractibility for finite complexes of dimension at most d, for every d >= 5. The appendix discusses a dimension-four strengthening. The audit needs only the d >= 5 form; it makes no claim about the present status of every lower-dimensional recognition problem. This is an effective undecidability reduction, not an NP-hardness reduction requiring compact formula encodings.

## R06. Classical poset 2-dimension
Michel Habib, Lhouari Nourine, Olivier Raynaud, and Eric Thierry, *Computational aspects of the 2-dimension of partially ordered sets*, Theoretical Computer Science 312 (2004), 401-431. DOI: https://doi.org/10.1016/j.tcs.2003.10.029 . Primary institutional record: https://hal-lirmm.ccsd.cnrs.fr/lirmm-00108552 . Paper text was inspected in an author-paper copy at https://www.academia.edu/19100821/Computational_aspects_of_the_2_dimension_of_partially_ordered_sets . Definition: an order embedding into a Boolean lattice must preserve and reflect **all ordered pairs**. Theorem 17 and Corollary 18 give the relevant NP-completeness result. They do not establish the package's false equality with relative observation dimension.

## R07. Generalized Boolean rank and covering graphs
Reka Agnes Kovacs, *On Minimally Non-Firm Binary Matrices*, ISCO 2022. https://arxiv.org/abs/2206.04089 ; inspected https://arxiv.org/html/2206.04089v1 , especially Section 2. Generalized matrices have entries 0, 1, and question marks; rectangles must avoid zeros and cover all ones, while question marks need not be covered. The section also gives the associated covering-graph formulation. This is an exact existing optimization framework for the corrected observation-design parameter. R07 attributes the generalized formulation to R08.

## R08. Earlier generalized Boolean basis problem
Anna Lubiw, *The boolean basis problem and how to cover some polygons by rectangles*, SIAM Journal on Discrete Mathematics 3(1) (1990), 98-115. Located through R07, reference 13. The original paper was not obtained in full. Therefore the audit attributes the framework via the inspected R07 account; it does not claim to have verified a particular theorem number in Lubiw's original paper.

## R09. Ferrers-graph prior art for chain profiles
Anders Claesson, Sergey Kitaev, Kari Ragnarsson, and Bridget Eileen Tenner, *Boolean complexes for Ferrers graphs*, 2010 version. https://arxiv.org/abs/0808.2307 ; inspected https://arxiv.org/html/0808.2307v3 . Its introduction announces that the independence complex of a Ferrers graph has the simple homotopy type of two points in the rectangular case and a point otherwise. The cited source is Richard Ehrenborg and Sergey Kitaev, *Ferrers graphs, their independent sets and independence complexes*, listed **in preparation**. Repeated title/author searches did not locate that underlying proof. Thus there is strong prior-art overlap with the chain homotopy classification, but the original proof's publication status remains unresolved.

Important: the **Boolean complex** studied in the body of R09 is not the **independence complex** used in our translation. The relevance is the explicit introduction statement about the latter, not an identification of these two constructions. Isolated-vertex cases in the chain translation are handled by the elementary cone observation.

## R10. Boolean functions and order/relative complexes
Anders Bjorner, Mark Goresky, and Robert MacPherson, *Topological aspects of Boolean functions*, Pure and Applied Mathematics Quarterly 20(3) (2024), 1029-1063. Author-hosted primary paper: https://www.math.ias.edu/~goresky/pdf/BooleanPAMQ.pdf . Inspected Sections 2-3 and relevant later discussion, including PDF images. Section 2.5 explicitly uses the order complex of true Boolean vectors; Section 3 uses relative homology of associated pairs. This is significant prior art against broad claims that associating order or relative homology to Boolean data is new. It is not an exact theorem about every observation-refinement map in the package.

## R11. SAT/hypergraph topology
James Conant and Oliver Thistlethwaite, *Boolean formulae, hypergraphs and combinatorial topology*. https://arxiv.org/abs/0808.0739 ; inspected https://arxiv.org/html/0808.0739v2 . Proposition 1 identifies the theta complex with the Alexander dual of an independence complex; Theorems 1-2 describe the resulting dualities. These are different constructions from the positive-observation compatibility nerve, but they are essential comparison literature before claiming a new topology of satisfiability or inconsistency.

## R12. Formal contexts, hypergraphs, and Dowker structures
Robert E. Green, Cliff A. Joslyn, Audun Myers, Michael G. Rawson, and Michael Robinson, *The Topological Structures of the Orders of Hypergraphs* (2025). https://arxiv.org/abs/2504.11760 . Abstract and metadata inspected. The paper explicitly relates binary relations, hypergraphs, formal contexts, orders, and Dowker constructions. This is a verified nearby research connection, not a claim that every theorem in the paper was checked or that it proves the package's refinement results.

## R13. Rough-set attribute reduction
Yiyu Yao and Yan Zhao, *Discernibility matrix simplification for constructing attribute reducts*, Information Sciences 179(5) (2009), 867-882. Author-hosted paper: https://www2.cs.uregina.ca/~yyao/PAPERS/is_reduct_construction.pdf . Relevant search-indexed primary text and bibliographic data inspected; not a page-by-page audit. Fixed-family attribute reducts lead to discernibility covers/hitting-set formulations. The package permits designing arbitrary new Q-upsets, which is a different feasible family. The exact link is to separation/covering, not an automatic equivalence to every rough-set reduct problem.

## R14. Persistent Quillen-McCord theory
Vitalii Guzeev and Kohei Tanaka, *Quillen-McCord theorem for persistence finite posets* (12 May 2026). https://arxiv.org/abs/2605.11615 ; inspected https://arxiv.org/html/2605.11615v1 . Theorem 3.8 concerns finite-type filtrations and an interleaving bound under persistent fiber hypotheses, in an appropriate weak-equivalence/localized setting. The package's reference to this recent work is genuine. A two-parameter filtration constructed merely by inclusions is not itself this quantitative theorem.

## R15. Small finite models and torsion
Nicolas Cianci and Miguel Ottina, *Poset splitting and minimality of finite models* (2015 preprint). https://arxiv.org/abs/1512.06088 ; inspected https://arxiv.org/html/1512.06088v1 . Theorem 5.7 treats small fundamental groups; Theorem 5.9 gives a thirteen-point lower bound for finite spaces with torsion homology. The thirteen-point projective-plane model is established prior art. Absolute-torsion lower bounds do not automatically prove minimality for all relative torsion pairs.

## R16. Cohomology of contextuality
Samson Abramsky, Shane Mansfield, and Rui Soares Barbosa, *The Cohomology of Non-Locality and Contextuality* (2012). https://arxiv.org/abs/1111.3620 . Abstract and relevant primary text inspected. The obstruction uses measurement-support/presheaf data. It is not identical to the constant-coefficient equation delta(lambda) on a signature order complex. Calling a signature coboundary an obstruction to contextuality would require an additional construction and proof.

## R17. Zigzag persistence
Gunnar Carlsson and Vin de Silva, *Zigzag Persistence*, Foundations of Computational Mathematics 10 (2010), 367-405. https://arxiv.org/abs/0812.0197 . Relevant primary abstract/text inspected, including interval-decomposition and examples. Changing directions in an indexed diagram justify zigzag methods. Merely mentioning both observation and premise changes does not determine whether a particular diagram is ordinary, multiparameter, or zigzag persistence.

## R18. Relative homology, cones, and Mayer-Vietoris
Allen Hatcher, *Algebraic Topology*, Cambridge University Press, 2002. Official free-book page: https://pi.math.cornell.edu/~hatcher/AT/ATpage.html . Chapters 2-3 are the standard background. The audit independently writes out the relative chain short exact sequence used for interaction, so no uninspected theorem-number claim is needed.

## R19. Discrete Morse theory
Robin Forman, *Morse Theory for Cell Complexes*, Advances in Mathematics 134 (1998), 90-145. DOI: https://doi.org/10.1006/aima.1997.1650 . Primary-paper copy: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/forman5.pdf . Relevant primary text located. Complete relative acyclic matchings and elementary collapses are standard machinery. The audit gives a direct alternating-cycle/free-face proof for the two-layer special case.

## R20. Boolean closure properties
Peter Jeavons, David A. Cohen, and Marc Gyssens, *Closure properties of constraints*, Journal of the ACM 44(4) (1997), 527-548. DOI: https://doi.org/10.1145/263867.263489 . Institutional primary record: https://documentserver.uhasselt.be/handle/1942/6848 . Metadata/abstract inspected. Horn model sets are meet-closed and dual-Horn model sets join-closed, with the usual finite Boolean-domain conventions. The observation-preservation statements additionally require the ambient realized semilattice and cofinality hypotheses; closure properties alone do not prove preservation.

## R21. Relative homotopy of relational structures
P. J. Witbooi, *Relative Homotopy in Relational Structures*. Author-hosted primary paper: https://math.uchicago.edu/~may/PEOPLE/Witbooi/witbooi8825.pdf . Theorem 5.3 was located in indexed primary text; venue/year not verified. It treats relative homotopy in relational/poset settings. This is nearby established language, not an exact identification of the package's mapping-cone invariant.

## R22. A recent terminology collision, not an equivalence
Dominik Durrschnabel, Jedrzej Hodor, Piotr Micek, Gerd Stumme, and William T. Trotter, *Relative Dimension of Posets* (September 2026). https://arxiv.org/abs/2609.05166 ; inspected https://arxiv.org/html/2609.05166v1 , Section 1.4. Its relative dimension uses a different realizer-based concept. It does **not** define odim_P(Q). It is a reason to avoid the unqualified title 'Relative Dimension of Posets', not evidence that the two parameters are equal.

## Search coverage and unresolved literature questions

Queries were organized by mathematical equivalence, not just ProLT terminology: finite T0 quotients/McCord; principal-fiber versus point-fiber theorems; deleting poset comparabilities; binary words/Ferrers independence complexes; rooted incidence forests and relative collapses; Horn/dual-Horn closure; poset 2-dimension/Boolean-lattice embeddings; generalized Boolean basis and question-mark matrices; attribute reducts/discernibility; Boolean-function and SAT/hypergraph topology; Dowker/formal-context topology; persistence and persistent Quillen theorems; constant-coefficient integration versus contextuality; and minimal finite-space torsion.

The major unresolved bibliographic issue is the Ehrenborg-Kitaev independence-complex paper announced in R09. The exact restricted observation-design problem for a prescribed total coarse order was not identified with a verified published complexity theorem. No exact earlier theorem was located with all of the one-bit height-two order-thinning hypotheses and collapse equivalences together. These are **limits of the search**, not positive novelty evidence.

No databases, papers, or private referee opinions are represented as consulted unless described above. No claim of an independent human review panel or formal proof-assistant verification is made.
