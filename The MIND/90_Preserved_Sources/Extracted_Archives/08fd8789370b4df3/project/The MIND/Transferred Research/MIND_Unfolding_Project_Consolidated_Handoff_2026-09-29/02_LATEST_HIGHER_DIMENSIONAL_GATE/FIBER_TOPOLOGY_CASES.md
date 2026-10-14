# Controlled Fiber Topology Cases

## 1. Existing localization from the carrier-splitting gate

For the projection

\[
\pi:Q^\psi\to Q,
\]

the lower fiber over `s` has a maximum `(s,1)` whenever outcome 1 exists over `s`.  Thus lower-fiber obstructions can occur only at 0-only states.  Dually, upper-fiber obstructions can occur only at 1-only states.

This remains a useful first localization, but it does not itself compute the cone when exceptional fibers are noncontractible.

## 2. Björner--Wachs--Welker benchmark

The BWW poset fiber theorem gives a wedge decomposition of `Delta P` in terms of `Delta Q` and lower fibers when each lower fiber has connectivity at least the length of the strict lower base interval.  It subsumes the classical Quillen contractible-fiber lemma and has homology/Cohen--Macaulay variants.

This is the correct prior-art benchmark for any proposed fiber decomposition.

## 3. Why the new matching theorem is different

The exclusive-inversion matching theorem does not assume the relevant fibers or links are highly connected.  In fact its one-edge realization can transfer arbitrary finite-poset homology and torsion.  The theorem therefore gives an exact integral group formula in cases where a BWW connectivity hypothesis may fail completely.

The price is structural: the 1-only-to-0-only inversion relation must be a matching.

## 4. Edge links as local defect objects

Within the matching class the local object is not a lower fiber but the coarse edge link

\[
lk_{Delta Q}[p,z]
=
Delta Q_{<p} * Delta(p,z) * Delta Q_{>z}.
\]

This makes geometric localization transparent:

- a global minimum below `p` cones off the link;
- a global maximum above `z` cones off the link;
- nontrivial defects live on genuinely internal local neighborhoods or on the global endpoint edge of a bounded poset.

## 5. Controlled-link corollaries

The matching formula immediately yields the following useful subclasses.

### Acyclic-link class

If every relevant edge link is integrally acyclic, then the carrier split is an integral homology equivalence.

### Shellable-link class

If every relevant edge link is shellable and pure, its reduced homology is free and concentrated in top dimension.  Therefore the cone homology is torsion-free and concentrated in the corresponding degrees shifted by two.

### Cohen--Macaulay-link class

If every relevant edge link is Cohen--Macaulay over a field `k`, then the cone homology over `k` is concentrated according to the top-dimensional link homology.  This is a coefficient-dependent structural corollary, not an integral torsion theorem.

## 6. What was not proved

No theorem was found saying that a finite list of possible exceptional fiber homotopy types automatically gives a wedge decomposition of the carrier cone.  Without additional null-homotopy/connectivity assumptions, that would overreach the general fiber literature.

The exact new classification is therefore kept in the matching/link language rather than rephrased as a broad new fiber theorem.
