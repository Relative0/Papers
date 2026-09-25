# Paper B - fresh prior-art deep dive

## 1. Polynomial sign conditions

For polynomial scores `g_alpha`, an operator fiber is exactly the realization of a strict sign condition on the finite polynomial family. The connected operator chambers are the semi-algebraically connected components of that realization.

Direct precedents:

- S. Basu, R. Pollack, M.-F. Roy, *An asymptotically tight bound on the number of semi-algebraically connected components of realizable sign conditions*, Combinatorica 29 (2009), 523-546. DOI 10.1007/s00493-009-2357-x.
- G. Jeronimo, D. Perrucci, J. Sabia, *On sign conditions over real multivariate polynomials*, Discrete Comput. Geom. 44 (2010), 195-222. DOI 10.1007/s00454-009-9200-4.
- S. Basu, R. Pollack, M.-F. Roy, *Algorithms in Real Algebraic Geometry*, 2nd ed.

**Consequence:** semialgebraic finiteness/computation of Paper B's polynomial chambers is established machinery.

## 2. Cover/Schlaefli interpretation of the Walsh atlas

The nonconstant Walsh evaluation vectors are vertices of a centered regular simplex in dimension `N-1`, `N=2^n`. A coefficient vector is a homogeneous linear classifier on these `N` points.

Classical result:

- T. M. Cover, *Geometrical and Statistical Properties of Systems of Linear Inequalities with Applications in Pattern Recognition*, IEEE Trans. Electronic Computers EC-14 (1965), 326-334. DOI 10.1109/PGEC.1965.264137.

For `N` points in general position in homogeneous dimension `d=N-1`, the Schlaefli/Cover count is

`2 sum_{j=0}^{N-2} binom(N-1,j) = 2^N-2`.

This exactly matches the Walsh chamber count.

Equivalent arrangement view: `N` generic central hyperplanes in `R^(N-1)` have exactly `2^N-2` regions.

**Consequence:** the count is classical and should be derived/cited as such.

## 3. Oriented matroid / tope graph interpretation

The simplex-normal arrangement has underlying uniform matroid of rank `N-1` on `N` elements. Its topes are precisely the realizable nonzero sign patterns. Tope graphs of oriented matroids are induced/partial-cube sign graphs with adjacency given by one-coordinate changes across regular facets.

Useful references:

- A. Bjorner, M. Las Vergnas, B. Sturmfels, N. White, G. Ziegler, *Oriented Matroids*, 2nd ed., Cambridge, 1999.
- K. Knauer et al. / COM literature: tope graphs are induced subgraphs of hypercubes on the tope set, with edges corresponding to one-coordinate changes.
- Zaslavsky's region-count theorem / standard hyperplane-arrangement references.

**Consequence:** the hypercube-minus-two-opposite-vertices graph is not a new combinatorial graph theorem here; Paper B gives a concrete Walsh/Boolean interpretation of a classical tope graph.

## 4. Boolean Fourier analysis

Every real function on `{-1,+1}^n` has a unique Walsh-Fourier expansion. The empty-set coefficient is its mean. For a nonconstant sign function `h`, `h-E[h]` has zero mean and the same sign as `h`, so the nonconstant Walsh characters alone already give a sign representation.

Reference:

- R. O'Donnell, *Analysis of Boolean Functions*, Cambridge University Press; arXiv:2105.10386.

**Consequence:** the realization portion of the centered Walsh theorem has a one-line classical Fourier proof.

## 5. DSGRN and logical bifurcation frameworks

Already appropriately incorporated in the major revision:

- B. Cummins, T. Gedeon, S. Harker, K. Mischaikow, *DSGRN: Examining the Dynamics of Families of Logical Models*, Front. Physiol. 9 (2018), 549. DOI 10.3389/fphys.2018.00549.
- T. Gedeon, *Multi-parameter exploration of dynamics of regulatory networks*, BioSystems 190 (2020), 104113. DOI 10.1016/j.biosystems.2020.104113.
- P. Crawford-Kahrl, B. Cummins, T. Gedeon, *Joint realizability of monotone Boolean functions*, Theor. Comput. Sci. 922 (2022), 447-474. DOI 10.1016/j.tcs.2022.04.045.
- W. Abou-Jaoude, P. T. Monteiro, *On logical bifurcation diagrams*, J. Theor. Biol. 466 (2019), 39-63. DOI 10.1016/j.jtbi.2019.01.008.
- B. Cummins et al., *Boolean models coarsely sample continuous dynamics of regulatory networks*, arXiv:2606.14925 (2026).

**Consequence:** broad parameter-to-logic region decomposition is prior art; Paper B should continue to treat it as such.

## 6. Abstract interpretation and exact partitions

The sign domain and collecting-semantics perspective are classic abstract interpretation. Work on complete abstractions and partition refinement also studies coarsest partitions preserving observations/logics. The unrestricted fiber partition of a finite observation map is therefore best treated as a universal property/basic construction, not a novel optimization theorem.

## 7. Revised novelty boundary

The defensible distinctive layer is:

- one explicit zero/reachability/solver-state contract tailored to continuous-score-to-CM/LM transport;
- a typed end-to-end interface from certified score guards to Boolean operators, CMs, and fixed-frame LMs;
- potentially new results only if the paper adds restricted guard complexity/minimality, operator-quotient compression, a symmetry theorem, or certified nonlinear implementation/case study.
