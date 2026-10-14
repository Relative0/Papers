# Adversarial Specialist Reviews

## Referee A — finite-poset topology

**Attack.** The proposed classification is only Quillen/Björner–Wachs–Welker fiber theory in different notation.

**Finding.** Generic fiber criteria and wedge decompositions are indeed prior art.  The matching theorem is narrower but computes the complete integral cofiber homology directly from coarse edge links without assuming the connectivity conditions used in the standard fiber formula.  The defensible claim is therefore a specialized exact recognition theorem for the observation-refinement model, not a new general fiber theorem.

## Referee B — combinatorial topology / vertex deletion

**Attack.** The full-doubling argument is generic induced-subcomplex vertex deletion.

**Finding.** Substantially correct as a priority warning.  Chachólski–Jin–Scolamiero–Tombari develop obstruction complexes and homotopical decompositions associated with vertex covers, including multiple outside vertices.  What remains project-specific is the two-colour missing-copy structure forced by a Boolean observation, the exclusive inversion graph, the biclique interaction filtration, and the matching reduction to coarse edge links.

## Referee C — integral homology and total unimodularity

**Attack.** A matching interaction graph should force torsion-free homology and probably total unimodularity.

**Finding.** False.  The endpoint construction `Q = 0hat + R + 1hat` transfers `H~_*(Delta R; Z)` two degrees upward while the exclusive graph consists of one edge.  Thus arbitrary torsion occurs inside the matching class.  Dey–Hirani–Krishnamoorthy also show that TU is controlled by torsion-freeness of an entire family of pure relative subpairs, not by the global homology of one pair.

## Referee D — Horn/closure systems

**Attack.** Horn structure should yield the sought rich higher-dimensional classification.

**Finding.** Not in the strongest natural formulation.  A nonempty meet-closed refined relation has a minimum, and its coordinate projection is again meet-closed with a minimum.  Both order complexes are therefore contractible and the refinement is homotopy-neutral.  Dual-Horn is dual.  Horn is an exact neutral regime, not the source of rich higher homology.

## Hostile minimal-counterexample attack

**Target.** Relax “matching” to “forest”.

**Counterexample.** Take the coarse chain `0<1<2` and the availability profile `(1-only,0-only,0-only)`.  The exclusive graph is the two-edge star `K_{1,2}`, hence a forest.  Direct integral Smith normal form yields `H~_1(Cone)=Z`, whereas the independent sum of the two edge-link contributions is zero.

**Consequence.** Acyclicity of the exclusive inversion graph is insufficient.  The first shared endpoint creates a genuine three-vertex interaction core, so any theorem beyond matching must track higher cores/differentials.

## Referee consensus

Correctness confidence is high for the matching formula and its corollaries, given the chain-level proof and exhaustive/targeted computation.  Priority confidence is medium: the exact two-colour matching specialization was not located in the searched literature, but it sits close to established obstruction-complex and vertex-deletion machinery.  Publication wording should emphasize the observation-theoretic specialization and explicit link formula.
