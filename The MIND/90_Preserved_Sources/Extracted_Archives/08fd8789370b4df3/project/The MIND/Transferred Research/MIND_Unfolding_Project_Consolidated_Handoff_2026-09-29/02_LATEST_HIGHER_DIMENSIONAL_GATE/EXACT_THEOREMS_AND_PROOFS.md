# Exact Theorems and Proofs

## T1. Missing-copy cofiber model

**Theorem.** Let `Q^psi subseteq Q x 2` be the refined signature poset and let `pi:Q^psi -> Q` be projection.  Put `K=Delta(Q x 2)` and regard `L=Delta Q^psi` as the induced subcomplex on the realized copies.  Then the mapping cone of `Delta pi` has the same reduced homology as the pair `(K,L)` over arbitrary coefficients.

**Proof.** The projection `Q x 2 -> Q` is a homotopy equivalence, with a closure section to either constant-bit row.  The map `Delta pi` is the composite `L -> K -> Delta Q`.  Homotopy cofibers are invariant under homotopy equivalence of the target, and the cofiber of a simplicial inclusion has reduced homology `H_*(K,L)`.  QED.

## T2. Two-colour shift

Let `P` be the 1-only states and `Z` the 0-only states.  Delete `P x {0}` and `Z x {1}` separately to get `K_P` and `K_Z`, and put `U=K_P union K_Z`, `L=K_P intersect K_Z`.

**Theorem.** For every `n` and every coefficient ring `R`,

\[
H_n(K,L;R)\cong H_{n+1}(K,U;R).
\]

**Proof.** `K_P` closes upward to the top row and `K_Z` closes downward to the bottom row, so `H_*(K,K_P)=H_*(K,K_Z)=0`.  The triple `(K,K_P,L)` gives `H_n(K,L) ~= H_n(K_P,L)`.  Excision for the union `U=K_P union K_Z` gives `H_n(K_P,L) ~= H_n(U,K_Z)`.  The triple `(K,U,K_Z)` gives `H_n(U,K_Z) ~= H_{n+1}(K,U)`.  Compose.  QED.

## T3. Empty-exclusive-graph neutrality

Define

\[
E_\psi=\{(p,z):p\in P,z\in Z,p<z\}.
\]

**Theorem.** If `E_psi` is empty, then `Delta pi` is a homotopy equivalence.

**Proof.** Define `b(s)=1` iff some `p in P` satisfies `p<=s`; otherwise set `b(s)=0`.  No `z in Z` can receive label `1`, because that would give an exclusive edge.  Thus `(s,b(s))` is an available refined state for every `s`, and `b` is isotone.  The section `r(s)=(s,b(s))` satisfies `pi r=id`.  On `Q^psi`, let `c_+(s,a)=(s,max(a,b(s)))`.  Then `id <= c_+ >= r pi`.  Comparable poset maps induce homotopic order-complex maps, so `r` is a homotopy inverse.  QED.

## T4. Interaction-core filtration

**Theorem.** The relative complex `C_*(K,U)` has a filtration by the number of missing vertices.  If `C_r` is the family of mixed `r`-vertex missing cores that form simplices of `K`, and

\[
\Lambda_S=lk_K(S)[V(L)],
\]

then

\[
gr_r C_m(K,U)
\cong
\bigoplus_{S\in C_r}\widetilde C_{m-r}(\Lambda_S).
\]

**Proof.** Every relative simplex has a unique missing core `S`.  Its remaining vertices are available and form a simplex in the indicated link.  A boundary face obtained by deleting an available vertex preserves `S`; deleting a missing vertex strictly lowers the filtration.  Therefore only the former survives in the associated graded differential, giving the augmented link complex with the stated degree shift.  QED.

**Corollary.** There is a convergent interaction spectral sequence whose first page is the direct sum of the reduced homologies of these available-link complexes.  The mixed cores are chain-supported bicliques of the exclusive inversion graph.

## T5. Exclusive-Inversion Matching Theorem

**Theorem.** If `E_psi` is a matching, then for every coefficient ring `R`,

\[
H_n(Cone(Delta pi);R)
\cong
\bigoplus_{(p,z)\in E_\psi}
\widetilde H_{n-2}(lk_{Delta Q}[p,z];R).
\]

**Proof.** Under matching, a relative simplex in `K\U` contains exactly one missing lower copy and exactly one missing upper copy; otherwise some exclusive vertex would have degree at least two.  Hence the chain complex splits directly over exclusive edges `e=((p,0)<(z,1))`.  The `e`-summand is the augmented chain complex of `lk_K e`, shifted by two.  T2 adds one further relative-degree shift.

It remains to identify the product link.  The link of `e` factors as

\[
Delta Q_{<p} * Delta((p,0),(z,1))_{Qx2} * Delta Q_{>z}.
\]

The middle interval is the union of two contractible induced subposets obtained by deleting `(z,0)` and `(p,1)` respectively; their intersection is `(p,z)_Q x 2`, homotopy equivalent to `(p,z)_Q`.  Therefore the middle interval has order complex homotopy equivalent to `Sigma Delta(p,z)_Q`.  Joining with the lower and upper factors gives

\[
lk_{Delta(Qx2)}e \simeq Sigma lk_{Delta Q}[p,z].
\]

Apply reduced homology.  QED.

## T6. Bounded-poset localization

**Theorem.** Assume `Q` has global minimum `0hat` and maximum `1hat`, and `E_psi` is a matching.  Then every exclusive edge other than `(0hat,1hat)` has contractible coarse edge link.  Hence only the global endpoint inversion can contribute to cone homology.

**Proof.** If `p != 0hat`, the lower-link factor `Delta Q_{<p}` has minimum `0hat` and is contractible.  If `z != 1hat`, the upper-link factor `Delta Q_{>z}` has maximum `1hat` and is contractible.  The edge link is their join with the open-interval factor.  A join with a nonempty contractible complex is contractible.  QED.

## T7. Distributive-lattice endpoint theorem

Let `L=J(R)` be a finite distributive lattice and use the endpoint matching profile: bottom is 1-only, top is 0-only, every other state splits.

**Theorem.** If `R` is an `r`-element antichain, so `L=B_r`, then

\[
H_r(Cone(Delta pi);Z) ~= Z
\]

and all other reduced cone homology vanishes.  If `R` is not an antichain, the cone is integrally acyclic.

**Proof.** T6 reduces the answer to the reduced homology of the proper part of `L`, shifted by two.  The atoms of `J(R)` are the singleton ideals generated by the minimal elements of `R`.  If `R` has a nonminimal element, the join of all atoms is still below the top element, so the atom crosscut complex is a full simplex and hence contractible.  If every element of `R` is minimal, `R` is an antichain, `J(R)=B_r`, and the atom crosscut complex is the boundary of an `(r-1)`-simplex, namely `S^{r-2}`.  Apply the crosscut theorem and shift by two.  QED.

## T8. Matching universality

**Theorem.** For every nonempty finite poset `R`, there is a carrier-splitting system with a one-edge exclusive matching such that

\[
H_n(Cone(Delta pi);Z)
\cong
\widetilde H_{n-2}(Delta R;Z).
\]

**Proof.** Take `Q=0hat ordinal-sum R ordinal-sum 1hat`.  Make `0hat` 1-only, `1hat` 0-only, and every `R` state split.  The exclusive graph has exactly the endpoint edge and its coarse edge link is `Delta R`.  Apply T5.  QED.

This theorem transfers arbitrary finite-poset torsion into the matching class and rules out a universal TU or wedge-of-spheres theorem there.
