# Total Unimodularity and Torsion Audit

## 1. Low height

For weighted height at most two, the prior rooted-incidence theorem identifies the relative boundary map with a signed graph-incidence matrix.  That matrix is totally unimodular, so all relative integral homology is free and coefficient-independent.

## 2. What changes in high dimension

The all-height exclusive-inversion matching theorem gives

\[
H_n(Cone(Delta pi);Z)
\cong
\bigoplus_{(p,z)\in E_psi}
\widetilde H_{n-2}(lk_{Delta Q}[p,z];Z).
\]

Therefore torsion in an edge link is inherited directly by the cone.

The endpoint realization

\[
Q=0hat\oplus R\oplus1hat
\]

with only the endpoint inversion transfers

\[
\widetilde H_*(Delta R;Z)
\]

two degrees upward.  Choosing `R` with `Z/2` torsion gives torsion while `E_psi` remains a one-edge matching.

So:

\[
\boxed{\text{exclusive-inversion matching does not imply TU.}}
\]

## 3. Dey--Hirani--Krishnamoorthy benchmark

Dey, Hirani, and Krishnamoorthy prove that for a finite simplicial complex, a boundary matrix `partial_{p+1}` is totally unimodular iff all specified pure relative subcomplex pairs in dimensions `p,p+1` have torsion-free `H_p`.

This matters here because **global torsion-freeness of the carrier cone is weaker than TU**.  Even if every edge link in the matching theorem is torsion-free, that only controls the homology of the particular carrier-splitting pair; it does not automatically control every pure subpair required by the TU characterization.

## 4. Safe conclusions

1. If one relevant edge link has torsion, the carrier cone has torsion and the hoped-for blanket TU property fails.
2. If every relevant edge link has torsion-free integral homology, the carrier cone is torsion-free.
3. Statement 2 does **not** imply that every relative boundary matrix is TU.
4. The Boolean/distributive endpoint examples are torsion-free, but no new global TU theorem is claimed for them.

## 5. Small explicit torsion construction

Take a finite poset `R` whose order complex has `H_1 ~= Z/2`, for example a standard finite-poset model of `RP^2`.  Add global endpoints and use the one-edge matching profile.  Then

\[
H_3(Cone(Delta pi);Z)\cong Z/2.
\]

The companion paper cites a 13-point projective-plane model, giving a concrete small construction after adding the two endpoint states.  This is an explicit example, not a new minimality claim.

## 6. Forbidden-minor question

No finite forbidden-subconfiguration characterization of TU was obtained.  The matching realization shows why a graph-only obstruction list cannot work: a one-edge exclusive graph can already carry arbitrarily complicated torsion through its coarse edge link.

Any future TU classification must constrain the **link topology or link boundary matrices**, not only the exclusive inversion graph.
