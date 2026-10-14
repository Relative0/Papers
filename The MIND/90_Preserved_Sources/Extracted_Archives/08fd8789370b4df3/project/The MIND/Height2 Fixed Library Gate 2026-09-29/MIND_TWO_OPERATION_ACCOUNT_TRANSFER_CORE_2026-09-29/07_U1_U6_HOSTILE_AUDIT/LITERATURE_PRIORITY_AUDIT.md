# Literature and priority audit through September 2026

This audit is conservative: absence of an exact phrase is not evidence of novelty.

## U1/U2 — finite topologies and preorders

Finite topology/preorder equivalence and the fact that `T0` corresponds to antisymmetry are classical. A recent accessible statement is:

- Mrozek et al., *Conley Index for Multivalued Maps on Finite Topological Spaces*, Foundations of Computational Mathematics (2024/2025 online context), https://link.springer.com/article/10.1007/s10208-024-09685-4
- Jonathan Barmak, *Algebraic Topology of Finite Topological Spaces and Applications*, Springer, 2011, DOI 10.1007/978-3-642-22003-6.

**Priority effect:** U1 is standard. U2's repaired fiber/cross-fiber interpretation is a synthesis, not a claim to the quotient-order foundations.

## U3 — lexicographic sums

The intermediate `F=sum_p B_p` matches the standard lexicographic sum/substitution of posets: within a fiber use its order; when index `p<q`, every point of the `p`-fiber is below every point of the `q`-fiber.

- Sage/Stanford finite-poset documentation: https://sporadic.stanford.edu/reference/combinat/sage/combinat/posets/posets.html

**Priority effect:** lexicographic sum is standard. The potentially useful project-specific step is identifying it canonically from ProLT fiber profiles and then separating its expansion map from descent thinning.

## U4 — mapping cones and the octahedral axiom

The cone of a map gives the standard distinguished triangle, and composable maps fit the octahedral pattern connecting `Cone(f)`, `Cone(gf)`, and `Cone(g)`.

- Stacks Project, *Cones and distinguished triangles*: https://stacks.math.columbia.edu/tag/09P1
- Stacks Project, *Distinguished triangles in the homotopy category*: https://stacks.math.columbia.edu/tag/014P

**Priority effect:** the octahedral LES is standard homological algebra. Do not claim it. The application to the U3 refinement factorization is the only project-specific content.

## U5/U6 — pullbacks, saturation, and measurement availability

Pullbacks are fiber products; in sets and concrete ordered settings the relevant square selects exactly the elements lying over the surviving base. Saturated subsets of a quotient are unions of whole quotient fibers. U5/U6 are therefore close to standard fiber/saturation mathematics.

- nLab pullback overview: https://ncatlab.org/nlab/show/pullback

The epistemic-update interpretation also has established neighbors. Public Announcement Logic updates a model by deleting worlds at which the announced formula is false:

- Stanford Encyclopedia of Philosophy, *Dynamic Epistemic Logic*: https://plato.stanford.edu/entries/dynamic-epistemic/
- SEP, *Logic and Information*: https://plato.stanford.edu/entries/logic-information/

**Priority effect:** U5 is a standard pullback criterion in project notation. U6 is a useful synthesis identifying non-cartesianity with “newly enabled measurement” under a fine-measurability hypothesis.

## Observation design — 2-dimension and Test Cover

Bit-vector encodings of a poset into a Boolean lattice, minimizing the number of coordinates, are the classical 2-dimension problem:

- Habib et al., *Computational aspects of the 2-dimension of partially ordered sets*, Theoretical Computer Science 312 (2004) 401–431, DOI 10.1016/j.tcs.2003.10.029, https://www.sciencedirect.com/science/article/pii/S0304397503005747

Pair separation from a prescribed test pool is classical Test Cover:

- Gutin, Muciaccia, Yeo, *(Non-)existence of polynomial kernels for the Test Cover problem*, Information Processing Letters 113 (2013) 123–126, DOI 10.1016/j.ipl.2012.12.008, https://www.sciencedirect.com/science/article/abs/pii/S0020019012003183

**Priority effect:** unrestricted U-design is standard territory. Novelty, if any, must come from ProLT-specific admissibility/cost/topological constraints.

## Adaptive identification and restricted query languages

Decision-tree optimization and constrained query families are deeply established:

- Hyafil & Rivest, *Constructing optimal binary decision trees is NP-complete*, Information Processing Letters 5 (1976) 15–17, DOI 10.1016/0020-0190(76)90095-8.
- Karbasi & Zadimoghaddam, *Constrained Binary Identification Problem*, STACS 2013, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2013.550
- Dagan, Filmus, Gabizon, Moran, *Twenty (Simple) Questions*, STOC 2017, DOI 10.1145/3055399.3055422, arXiv:1611.01655. This explicitly studies restricted sets of yes/no questions while trying to retain optimal information performance.
- Nowak, *The Geometry of Generalized Binary Search*, IEEE Transactions on Information Theory 57 (2011); arXiv:0910.4397. It studies adaptively chosen near-balanced queries and logarithmic query complexity under geometric conditions.
- Cicalese et al./related poset-search literature: *On the complexity of searching in trees and partially ordered structures*, Theoretical Computer Science 412 (2011) 6879–6896, DOI 10.1016/j.tcs.2011.08.042.
- Eisel, McMullen, Muth, *An efficient search strategy for hidden ideals in pointed partially ordered sets* (2025/2026 publication cycle), DOI 10.61091/jcmcc128-11, arXiv:2505.07604.

**Priority effect on A1:** the general topic “adaptive identification under restricted queries” is emphatically not new. The potentially new item is only the exact query language induced by the ProLT chain homotopy classification and the resulting “exactly one redundant query is necessary/sufficient” corollary. This should be presented as a narrow ProLT theorem unless a deeper priority audit finds a direct equivalent.

## Bottom line

- U1: standard.
- U2: repaired useful synthesis.
- U3: standard lexicographic construction + useful ProLT factorization.
- U4: standard octahedral machinery + useful application.
- U5: standard pullback/fiber criterion in ProLT form.
- U6: useful saturation/measurement-availability synthesis.
- A1: correct and nontrivial as a ProLT consequence; novelty plausible but modest and should remain explicitly provisional.
