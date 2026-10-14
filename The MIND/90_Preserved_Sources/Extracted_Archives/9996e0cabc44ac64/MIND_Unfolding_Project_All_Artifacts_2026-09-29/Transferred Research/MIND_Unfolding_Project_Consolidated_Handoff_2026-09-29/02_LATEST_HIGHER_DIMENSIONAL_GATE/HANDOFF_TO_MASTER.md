# Handoff to Master -- Higher-Dimensional Inversion Gate

**Status:** Gate reaches **Level A mathematically**, with conservative novelty language required.

## Strongest theorem

Let `P` be the 1-only coarse states and `Z` the 0-only coarse states after a Boolean carrier split.  Form the exclusive inversion graph

\[
E_psi=\{(p,z)\in P\times Z:p<z\}.
\]

If `E_psi` is a matching, then for all `n`

\[
H_n(Cone(Delta pi);Z)
\cong
\bigoplus_{(p,z)\in E_psi}
\widetilde H_{n-2}(lk_{Delta Q}[p,z];Z).
\]

This holds over arbitrary coefficients and is all-dimensional.

## Why it works

Replace the split completion by the full doubled product `D=Q x 2`.  The refined carrier is the induced subposet obtained by deleting `(p,0)` for 1-only states and `(z,1)` for 0-only states.  Separately deleting each colour is homotopy-neutral.  Mixed relative simplices correspond to chain-supported bicliques of the exclusive inversion graph.  A matching allows only one-edge mixed cores, forcing a chain-level direct sum.

## High-dimensional canonical example

For `Q=B_m`, bottom 1-only, top 0-only, all other states split:

\[
H_m(Cone)=Z.
\]

Direct SNF check: `B_3` gives `H_3=Z`.

## Sharp counterexample

Do **not** weaken matching to forest.  The 3-chain profile `(1,0,0)` has a two-edge star exclusive graph and actual `H_1=Z`, while independent edge-link summation gives zero.

## Torsion warning

Matching does not imply TU or torsion-freeness.  With `Q=0hat + R + 1hat` and endpoint-only inversion,

\[
H_n(Cone)=\widetilde H_{n-2}(Delta R),
\]

so arbitrary finite-poset torsion transfers.

## Boolean/Horn conclusions

- whole refined relation meet-closed (Horn) -> refined and projected posets have minima -> homotopy-neutral;
- dual-Horn is dual;
- finite distributive lattice endpoint profile is neutral unless the lattice is Boolean, in which case `B_r` gives a single `Z` in degree `r`.

## Computation

- 3,242 matching cases through 4 coarse states checked integrally by SNF: 0 failures;
- 1,707 product-link suspension checks through 5 states: 0 failures;
- 639 nonempty matching five-state random cases checked over F2: 0 failures;
- Horn relations exhaustively checked through 4 refined coordinates;
- 10 small distributive lattices checked integrally.

## Literature boundary

Closest prior art is Chachólski--Jin--Scolamiero--Tombari (2021) on vertex-cover obstruction complexes and cofiber decompositions.  Generic deletion/cofiber machinery is not new.  The candidate project-specific result is the exact observation-theoretic two-colour matching reduction and coarse-edge-link formula.

## Recommended manuscript action

Add a new theorem section after the general carrier-splitting factorization.  Do not replace the general theorem.  Insert the matching theorem, Boolean/distributive corollaries, forest counterexample, and torsion sharpness.

## Next research target

Build the **exclusive-inversion interaction spectral sequence** beyond matching.  First attack exclusive graphs of maximum degree 2 / chordal or Ferrers biclique structure, and characterize when the core-size spectral sequence collapses at `E^2`.
