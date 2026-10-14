# Algebra of the Higher-Dimensional Inversion Chain Complex

## 1. Product model

Let `Q` be a finite poset and `Q^psi subseteq Q x {0,1}` the realized refined signatures.  Put

\[
D=Q\times\mathbf2,\quad K=\Delta D,\quad L=\Delta Q^\psi.
\]

Let

\[
P=A_1\setminus A_0,\qquad Z=A_0\setminus A_1.
\]

The vertices missing from `L` are

\[
M_0=P\times\{0\},\qquad M_1=Z\times\{1\}.
\]

This realizes the changing-carrier problem as an induced-subcomplex deletion from one fixed order complex.

## 2. Two-colour deletion pair

Define

\[
K_P=K[V\setminus M_0],\qquad K_Z=K[V\setminus M_1],
\]

\[
L=K_P\cap K_Z,\qquad U=K_P\cup K_Z.
\]

Both `K_P -> K` and `K_Z -> K` are homotopy equivalences by the top-row and bottom-row closure maps.  Consequently

\[
H_n(K,L;R)\cong H_{n+1}(K,U;R).
\]

The relative complex `C_*(K,U)` is free on chains containing at least one vertex of each missing colour.

## 3. Exclusive inversion graph

Let

\[
E_\psi=\{(p,z)\in P\times Z:p<z\}.
\]

For a relative simplex `sigma`, put

\[
P(\sigma)=\{p:(p,0)\in\sigma\},\qquad
Z(\sigma)=\{z:(z,1)\in\sigma\}.
\]

Then `P(sigma) x Z(sigma)` is a complete bipartite subgraph of `E_psi`.  Hence higher relative cells are controlled not by arbitrary subsets of inversions but by **chain-supported bicliques**.

This gives a sharper description than simply saying that the bit word has a descent.

## 4. Core-size filtration

Define the missing core

\[
S(\sigma)=\sigma\cap(M_0\cup M_1).
\]

Every relative simplex has `|S(sigma)| >= 2`.  Filter by

\[
F_r C_m(K,U)=\langle\sigma:|S(\sigma)|\le r\rangle.
\]

Since taking a face cannot increase the number of missing vertices, this is a chain filtration.

Let `C_r` be the family of `r`-vertex mixed missing cores that are themselves simplices of `K`.  For `S in C_r`, define

\[
\Lambda_S=\operatorname{lk}_K(S)[V(L)].
\]

In the associated graded complex, deleting a missing vertex lowers the filtration and disappears, while deleting an available vertex preserves the core.  Therefore

\[
\boxed{
\operatorname{gr}_r C_m(K,U)
\cong
\bigoplus_{S\in\mathcal C_r}
\widetilde C_{m-r}(\Lambda_S).
}
\]

A standard filtered-complex spectral sequence follows, with first-page terms built from

\[
\widetilde H_*(\Lambda_S).
\]

The first inter-core differentials delete one missing vertex and hence measure interactions among overlapping exclusive inversions.

## 5. Matching collapse

If `E_psi` is a matching, no relative simplex can contain more than two missing vertices.  Hence all mixed cores have exactly two vertices and are exactly the edges

\[
e=((p,0)<(z,1)),\qquad (p,z)\in E_\psi.
\]

Moreover every vertex in `lk_K(e)` is available: a missing vertex in the link would create another exclusive edge sharing `p` or `z`.

Thus the filtration has only one nonzero mixed-core level and collapses immediately:

\[
C_m(K,U)
\cong
\bigoplus_{e\in E_\psi}
\widetilde C_{m-2}(\operatorname{lk}_K e).
\]

This is a literal chain-level direct sum, not merely an equality of Betti numbers.

## 6. Product link versus coarse link

For `e=((p,0)<(z,1))`,

\[
\operatorname{lk}_K e
=
\Delta(Q_{<p})*\Delta M_{p,z}*\Delta(Q_{>z}),
\]

where `M_{p,z}=((p,0),(z,1))` in `Q x 2`.

Writing `R=(p,z)_Q`, cover `Delta M_{p,z}` by

- `M_{p,z} \ {(z,0)}`, which closes upward to a cone with minimum `(p,1)`;
- `M_{p,z} \ {(p,1)}`, which closes downward to a cone with maximum `(z,0)`.

Their intersection is `R x 2`, homotopy equivalent to `R`.  Hence

\[
\Delta M_{p,z}\simeq\Sigma\Delta R,
\]

and therefore

\[
\operatorname{lk}_{\Delta(Q\times2)}e
\simeq
\Sigma\operatorname{lk}_{\Delta Q}[p,z].
\]

## 7. Exact integral formula

Combining the direct sum, the product-link suspension, and

\[
H_n(K,L)\cong H_{n+1}(K,U),
\]

gives

\[
H_n(K,L;\mathbb Z)
\cong
\bigoplus_{(p,z)\in E_\psi}
\widetilde H_{n-2}(\operatorname{lk}_{\Delta Q}[p,z];\mathbb Z).
\]

The same argument works over arbitrary coefficients.

## 8. Why forests fail

A forest can contain a star.  If `p` is adjacent to two comparable `z_1<z_2`, then the relative triangle

\[
(p,0)<(z_1,1)<(z_2,1)
\]

has boundary connecting the two inversion-edge generators.  This is an inter-core differential.  The three-chain profile `(1,0,0)` is the smallest example.

Thus the correct higher-dimensional object is not the exclusive graph alone but the hierarchy of chain-supported bicliques plus their available links.

## 9. Relation to the original bit-word model

The earlier split-completion relative complex was described by nonmonotone bit words.  The full-doubling model repackages the same obstruction more effectively:

- split states contribute no missing copy;
- 1-only states remove their lower copy;
- 0-only states remove their upper copy;
- a genuine obstruction occurs only when a chain needs both missing colours.

The binary descent is therefore equivalent to a two-colour missing-vertex interaction after the homotopy-neutral doubling.
