# Literature and Priority Map -- Higher-Dimensional Inversion Gate

**Search horizon:** through 29 September 2026.  
**Method:** structural searches for poset fibers, induced-subcomplex vertex deletion, obstruction complexes, finite-space reductions, Horn closure systems, lattice order complexes, and total unimodularity.  Absence of the project terminology "carrier splitting" was not treated as novelty evidence.

## 1. Björner--Wachs--Welker: poset fiber decompositions

**Reference:** A. Björner, M. Wachs, V. Welker, *Poset fiber theorems*, Transactions of the AMS 357 (2005), 1877--1899.  Preprint: https://www.math.miami.edu/~wachs/papers/fibers.pdf

Their main theorem expresses the homotopy type of a poset in terms of the base and lower fibers under explicit connectivity hypotheses, subsuming Quillen/Baclawski/Babson fiber results.

**Overlap:** controlled-fiber decomposition and homotopy equivalence criteria.

**Difference:** the exclusive-inversion matching theorem gives exact integral cone homology from edge links without requiring those fiber-connectivity assumptions.  It is much narrower structurally.

## 2. Chachólski--Jin--Scolamiero--Tombari: vertex-cover obstruction complexes

**Reference:** W. Chachólski, A. Jin, M. Scolamiero, F. Tombari, *Homotopical decompositions of simplicial and Vietoris Rips complexes*, Journal of Applied and Computational Topology 5 (2021), 215--248. DOI: 10.1007/s41468-021-00066-2.  https://link.springer.com/article/10.1007/s41468-021-00066-2

They study inclusions induced by covers of a simplicial complex's vertex set, define obstruction complexes, and give homotopy-cofiber statements for one, two, and several outside vertices.  Their general theorem controls homotopy fibers of the inclusion by the obstruction complexes.

**Overlap:** this is the closest prior art to the full-doubling/missing-copy viewpoint.  In particular, the standard fact that deleting vertices produces cofiber/link obstructions is not new here.

**Candidate additional content:** in the observation-refinement product `Delta(Q x 2)`, the missing vertices have two special colours.  Their mixed simplices are exactly chain-supported bicliques of the exclusive inversion graph.  Matching of that graph forces a chain-level direct sum and yields the explicit coarse-edge-link formula.  I did not locate that exact specialization/formula in the searched source.

**Priority caution:** a specialist should still check whether this matching specialization is implicit in the authors' several-outside-points machinery.

## 3. Dey--Hirani--Krishnamoorthy: TU and torsion

**Reference:** T. K. Dey, A. N. Hirani, B. Krishnamoorthy, *Optimal Homologous Cycles, Total Unimodularity, and Linear Programming*, SIAM Journal on Computing 40(4) (2011), 1026--1044. DOI: 10.1137/100800245.  https://epubs.siam.org/doi/10.1137/100800245

They prove a topological characterization of total unimodularity of simplicial boundary matrices in terms of torsion-freeness of a family of pure relative subcomplex pairs.

**Consequence here:** torsion-free global cone homology is not enough to infer TU.  The matching realization transfers arbitrary torsion, so no blanket all-height TU theorem survives.

## 4. Stong; Barmak; Fernández--Minian

- R. E. Stong, *Finite topological spaces*, Trans. AMS 123 (1966), 325--340. DOI: 10.1090/S0002-9947-1966-0195042-2.
- J. A. Barmak, *On Quillen's Theorem A for posets*, JCTA 118 (2011), 2445--2453; arXiv:1005.0538.
- X. Fernández, E. G. Minian, *The cylinder of a relation and generalized versions of the Nerve Theorem*, arXiv:1801.07235.

**Overlap:** closure maps, beat-point reductions, simple-homotopy fiber criteria, mapping/relation cylinders.

**Difference:** these provide the standard finite-poset topology, not the specialized exclusive-inversion formula.

## 5. Horn / closure systems

Boolean relations closed componentwise under logical AND are exactly Horn-definable relations; this is standard Schaefer/Post-style Boolean relation theory.  A concise modern statement appears in the ICALP 2019 possibility-domain literature, and closure-system treatments identify Horn models with intersection-closed families.

**Overlap:** meet-closure itself is classical.

**Use here:** if the entire refined realized relation is meet-closed, it and its coordinate projection have minima, so the carrier cone is contractible.  This is a simple application, not a novelty claim about Horn logic.

## 6. Crosscut/shellability theory for distributive lattices

Modern crosscut-simplicial literature records that semidistributive lattices have interval order complexes that are contractible or spherical; distributive lattices are a special case.  See C. Defant and N. Williams, *Semidistrim Lattices*, Forum of Mathematics, Sigma 11 (2023), e50.

For the particular distributive lattice `J(R)`, the endpoint statement used here also follows directly from the classical crosscut theorem and the atom structure of `J(R)`: if `R` is not an antichain, the atom crosscut is a simplex; if `R` is an antichain, `J(R)` is Boolean and the crosscut is a sphere.

**Novelty status:** standard lattice topology applied as a corollary of the matching theorem.

## 7. 2026-current finite-poset work

A 2026 paper, *Discrete homotopy and homology theories for finite posets* (Advances in Applied Mathematics 177 (2026), 103074), develops discrete analogues of homotopy and homology for finite posets and relates the discrete homotopy groups to classical ones.

**Overlap:** finite-poset homotopy/homology environment.

**Difference:** no carrier-splitting, two-colour missing-copy, or matching edge-link classification was found there.

## 8. Priority table

| Result in this gate | Closest antecedent | Priority assessment |
|---|---|---|
| Full-doubling/missing-copy model | standard induced-subcomplex deletion; Chachólski et al. | **Not new topology; project-specific modeling reduction** |
| Two-colour shift `H_n(K,L) ~= H_{n+1}(K,U)` | LES/excision/Mayer--Vietoris | **Standard algebraic topology specialized here** |
| Biclique missing-core filtration | filtered relative chains + vertex deletion | **Potentially useful project-specific organization; do not make broad novelty claim yet** |
| Exclusive-inversion matching link formula | Chachólski obstruction complexes; link/cofiber theory | **Candidate substantive specialized theorem; exact statement not located** |
| Bounded-poset endpoint localization | elementary join/link argument | **Corollary** |
| Boolean/distributive sphere-or-zero rule | crosscut theorem | **Corollary; prior lattice topology** |
| Horn refined-relation neutrality | Horn meet closure + cone posets | **Application, not novelty** |
| Torsion universality inside matching | finite-poset realization + matching theorem | **Sharpness result specific to theorem** |

## 9. Recommended wording for a paper

Use wording such as:

> The underlying deletion and cofiber constructions are classical, and obstruction-complex methods for vertex covers are available in the literature.  Our contribution is the recognition that a Boolean observation split produces a two-colour deletion inside `Delta(Q x 2)`, for which the 1-only-to-0-only comparison graph controls interactions.  When this graph is a matching, the relative chain complex separates and yields an exact integral edge-link formula.

Avoid wording such as:

> We introduce a new general theory of vertex deletion or simplicial cofibers.

That would be inaccurate.
