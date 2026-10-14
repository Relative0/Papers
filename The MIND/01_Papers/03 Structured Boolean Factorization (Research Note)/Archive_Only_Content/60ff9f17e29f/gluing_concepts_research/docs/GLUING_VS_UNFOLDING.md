# Gluing vs. Unfolding

## 1. Historical operator versus standard boundary

The thesis's distinguishing/unfolding operator \(\partial\) is **not** the standard simplicial boundary map. Historically it takes an \(n\)-simplex-like logical expression, omits one vertex at a time, negates the omitted variable, and disjoins the resulting formulas. That carries semantic information not present in the ordinary chain boundary.

Accordingly, the modern project should reserve different notation:

- \(\partial_{\mathrm{ch}}\): the chain boundary in homology;
- \(U\): a chosen unfolding/decomposition operation;
- \(G\) or \(\operatorname{colim}\): a gluing/assembly operation;
- \(F\): a filler/completion operation when a higher simplex is intentionally added.

This avoids inheriting the thesis's overloaded \(\partial\).

## 2. Face exposure is not independent factorization

For a simplex \(\Delta^n\), deleting the top-dimensional simplex leaves its boundary \(\partial\Delta^n\), a union of codimension-one faces. This is a **face decomposition**. The faces overlap heavily.

By contrast, join factorization asks for disjoint vertex blocks whose allowed faces combine freely. A simplex has the trivial/maximal property
\[
\Delta(V)=*_{v\in V}\Delta\{v\},
\]
so its finest join factors are individual vertices. The boundary faces are therefore not the independent factors.

This answers one of the central questions decisively:

> “Unfolding into faces” and “disentangling into independent factors” are fundamentally different operations.

## 3. Can gluing invert unfolding?

### 3.1 Plain pushout/union: generally no

Take the filled tetrahedron \(\Delta^3\). If unfolding forgets its top simplex and returns the four triangular faces, ordinary re-union returns only \(\partial\Delta^3\). Thus
\[
G(U(\Delta^3))\ne\Delta^3
\]
for plain simplicial union.

### 3.2 Declared filler: a restricted partial inverse

Define \(U_{\max}\) on a declared simplex by deleting only its maximal simplex while retaining its boundary. Define \(F\) on an object specifically marked as “the boundary of this labeled simplex” by adding that one top face. Then
\[
F(U_{\max}(\Delta(V)))=\Delta(V).
\]
This is a useful **partial inverse with provenance**, not an intrinsic inverse on all complexes.

### 3.3 Why provenance matters

The same boundary-shaped subcomplex can occur inside a much larger complex, and a cycle need not be intended to be filled. Adding every available top simplex is a completion convention, not a consequence of ordinary topology. The global complex alone does not remember which holes were deliberately produced by unfolding and which were original.

## 4. Tetrahedron test

Let \(V=\{a,b,c,d\}\).

- Union of all four triangular faces: \(\partial\Delta^3\), with \(\beta=(1,0,1)\) over \(\mathbb F_2\).
- Filled tetrahedron: \(\Delta^3\), with \(\beta=(1,0,0,0)\).
- Three triangular faces: a 3-dimensional horn-shaped subcomplex (topologically a disk), with \(\beta=(1,0,0)\).

The package's exact computation confirms that the four-face union differs from the filled tetrahedron by precisely the top simplex \(\{a,b,c,d\}\).

### Are all four faces necessary?

The answer depends entirely on the completion semantics.

- **Plain union:** even all four are insufficient for the filled tetrahedron; they produce only the boundary.
- **Explicit boundary filler:** all four certify the full boundary before filling.
- **Horn filler:** three specified faces form a horn; a simplicial set satisfying an appropriate filling condition admits a filler, but existence and uniqueness are additional structure.
- **Flag completion:** the complete graph \(K_4\) in the 1-skeleton already forces all four triangles *and* the tetrahedron. Hence not even the triangles are necessary once flag semantics are adopted.

Therefore the thesis's tetrahedral picture does not determine one mathematical “integrator.” It points to a family of completion mechanisms.

## 5. Thesis triangle reconstruction

The thesis's triangle example obtains \(X\land Y\land Z\) by Boolean conjunction of formulas associated with the sides. That should be formalized as a semantic reconstruction map
\[
G_{\mathrm{Bool}}:\prod_i \mathcal F(U_i)\longrightarrow\mathcal F(U)
\]
(or another explicitly typed operation), not identified with the simplicial union of edges. The topological carrier and the formula layer may be coupled, but they are not the same operation.

## 6. Sheaf gluing as a better inverse paradigm

If unfolding means “restrict a global semantic section to a cover,” then a genuine sheaf supplies the cleanest inverse statement available:

1. start with global section \(s\in\mathcal F(U)\);
2. restrict to \(s_i=s|_{U_i}\);
3. the local sections automatically agree on overlaps;
4. the sheaf axiom reconstructs a unique \(s\).

In this limited sense, **restriction and sheaf gluing are mutually inverse at the level of compatible section data**. This is much closer to the thesis's later presheaf/sheaf language than the simplicial-face example.

But this does not imply that a semantic object decomposes into independent factors; it only says a global section is determined by coherent local restrictions.

## 7. Possible adjunction/closure questions

The following are mathematically sensible future questions, but none should be asserted without proof:

- Is a chosen “fill every declared boundary” construction a left adjoint to a forgetful/unfolding functor in a category of **marked** complexes?
- Is flag completion a useful closure operator for a mental-space subcategory, and what information does it destroy?
- Can the thesis's logical unfolding be expressed as restriction in a presheaf and its “integrator” as sheafification or a colimit?
- Does CM rank separability commute with such restriction/gluing operations?

The right strategy is to construct the category first and test an adjunction second.

## 8. Conclusion

There is no single equation \(G=U^{-1}\) supported by the historical material. The evidence instead supports a three-way distinction:

- **unfolding/restriction** exposes local or lower-order information;
- **gluing** assembles compatible pieces without automatically completing missing higher cells;
- **completion/filling** asserts an additional higher-order whole.

That separation is not a failure of the program. It is the clarification needed to turn the historical intuition into a sound modern theory.
