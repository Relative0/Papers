# Structural theorem notes: exact core interaction and degree two

Independent derivation, 2026-09-29. These notes prove the statements explicitly marked as theorems. The later exact eight-state example in `C4_COUNTEREXAMPLE_PROOF.md` resolves the C4 E2-collapse question negatively. No priority over standard filtered-complex theory is claimed.

## 1. Conventions and the exact chain complex

Use the frozen notation `K = Delta(Q x 2)`, `L = Delta Q^psi`, and `U = K_P union K_Z`. The mixed-core filtration belongs on `C_*(K,U)`, not directly on `C_*(K,L)`. The known two-colour shift is

`H_n(Cone(Delta pi);R) = H_{n+1}(K,U;R)`.

Here cone homology means reduced mapping-cone homology. Let a mixed core `S` have `r` missing vertices in their poset order, and let `T` be an available simplex in `Lambda_S = lk_K(S)[V(L)]`. Reorient the simplex by listing all vertices of `S` first and then all vertices of `T`; the shuffle sign from the original poset order is part of this basis change. The resulting differential is

`d(S wedge T) = sum_i (-1)^i (S minus s_i) wedge T + (-1)^r S wedge d(T)`,

where a term with a nonmixed remaining core is zero in `(K,U)`. The empty available simplex is included in augmented degree `-1`. Thus

`C_m(K,U) = direct_sum_{mixed S} Ctilde_{m-|S|}(Lambda_S)`

as modules, with the stated differential. All link inclusions from deleting a core vertex are actual inclusions: `Lambda_S subset Lambda_(S minus s_i)`.

With total relative degree `m=r+q`,

`E^0_(r,q) = direct_sum_|S|=r Ctilde_q(Lambda_S)`,

`d^0 = (-1)^r d_link`,

`E^1_(r,q) = direct_sum_|S|=r Htilde_q(Lambda_S)`,

and `d^1` is the signed sum of the homology maps of those link inclusions. The differential `d^k` has bidegree `(-k,k-1)`. Convergence is to the associated graded of `H_(r+q)(K,U)`, hence of cone homology in degree `r+q-1`.

**Bounded-core theorem.** If the maximum mixed-core cardinality is `R>=2`, then `E^(R-1)=E^infinity`. Indeed the only possibly nonzero columns are `2,...,R`, so every differential with `k>=R-1` has zero source or target. This includes `R=2 => E^1` collapse and `R=3 => E^2` collapse. It is a column-counting theorem and should not receive an independent novelty claim.

## 2. Exact two-column theorem and integral qualifications

Suppose there are no mixed cores of size four or more. Define ordinary augmented chain complexes

`A = direct_sum_|S|=2 Ctilde_*(Lambda_S)`,

`B = direct_sum_|S|=3 Ctilde_*(Lambda_S)`.

Let `h:B -> A` be the signed sum of link inclusions from deleting one missing vertex, retaining only mixed faces. In degree `m`, the relative differential is

`d(a,b) = (d a + h b, -d b)`

on `A_(m-2) plus B_(m-3)`. Therefore there is a literal chain isomorphism

`C_*(K,U) = Cone(h)[2]`.

Consequently, over any coefficient ring,

`H_n(Cone(Delta pi)) = H_(n-1)(Cone(h))`,

and the mapping-cone long exact sequence gives

`0 -> coker(H_(n-1)h) -> H_n(Cone(Delta pi)) -> ker(H_(n-2)h) -> 0`.

This is an exact necessary-and-sufficient acyclicity criterion: all reduced cone homology vanishes if and only if `H_q(h)` is an isomorphism for every augmented degree `q`.

Over a field the short exact sequence splits, noncanonically. Over `Z`, it also splits whenever the right-hand kernel is free abelian. In general, `E^2` collapse alone does not identify integral cone homology as the direct sum of kernel and cokernel. Nor do the abstract link homology groups, with no chain maps or extension information, automatically determine the integral result. The chain-level mapping cone remains exact without qualification.

The incidence coefficients `0,+1,-1` describe the maps between *link chain groups*. On link homology they are homomorphisms induced by inclusions; they are not automatically scalar incidence matrices in arbitrary homology bases. There is no resulting general total-unimodularity or torsion-freeness claim.

## 3. A stronger one-column criterion than graph matching

**Theorem (no comparable common-neighbour pair).** If every two exclusive vertices of one colour sharing an exclusive neighbour are incomparable in `Q`, then every mixed core has size exactly two, and the frozen matching formula holds unchanged:

`H_n(Cone(Delta pi);R) = direct_sum_(p,z)inE Htilde_(n-2)(lk_(Delta Q)[p,z];R)`.

**Proof.** A larger mixed core contains two missing vertices of the same colour that are comparable and have a common opposite-colour core vertex. Conversely such a pair and their common neighbour form a mixed 3-core. Under the hypothesis no missing vertex lies in the product link of any exclusive edge, because adjoining it would make a mixed 3-core. Thus each available edge link is its full product link. The chain direct sum and product-link suspension proof from the frozen matching theorem apply verbatim. This proves the assertion.

Graph matching is sufficient but not necessary. This theorem concerns the graph together with the order on each colour class; the graph alone does not record the needed comparabilities.

## 4. Universal component decomposition

**Theorem.** The relative chain complex is the direct sum of subcomplexes indexed by the nontrivial connected components of the exclusive graph.

**Proof.** The missing vertices of any mixed relative simplex form a complete bipartite graph, hence all belong to a single connected component. A surviving relative face still has at least one vertex of each colour and remains in that component. Therefore the basis and differential decompose as asserted. Available links in a component still depend on the entire coarse poset; this is not permission to replace `Q` by its induced exclusive-vertex subposet.

## 5. Transitivity restrictions in maximum degree two

For exclusive vertices,

`p<p' => N(p') subseteq N(p)`,

`z<z' => N(z) subseteq N(z')`.

These are immediate from transitivity of `Q`, and materially strengthen what follows from graph degree alone.

**Theorem.** If the exclusive graph has maximum degree at most two, then:

1. Every mixed core has cardinality at most four.
2. A four-core can occur only in a connected component `K_{2,2}=C_4`, and occurs there if and only if both colour classes are comparable pairs in `Q`.
3. In a cycle component `C_(2k)` with `k>=3`, there are no 3-cores. Consequently its homology contribution is the direct coarse-edge-link sum in Section 3.
4. In a path component with at least three edges, a 3-core can occur only on its first two or last two edges. In either case the leaf and the vertex at graph distance two must be comparable in the forced direction described below.

**Proof.** A mixed core is a biclique with each side a chain. Degree two bounds each biclique side by two. A 2-by-2 biclique in a degree-two graph is a whole `C_4` component. Two same-colour degree-two vertices can be comparable only if they have identical neighbourhoods, by the displayed inclusion and equal cardinalities. Identical two-element neighbourhoods give a `C_4` component. On a longer cycle there are no degree-one vertices and no twins, so no such comparable pair exists. In a path with at least three edges, a comparable same-colour common-neighbour pair therefore contains a degree-one leaf and its degree-two distance-two neighbour. These are exactly the pairs at the path ends.

For a `P`-coloured leaf `a` and degree-two `P`-vertex `b`, comparability must be `b<a`. For a `Z`-coloured leaf `y` and degree-two `Z`-vertex `x`, comparability must be `y<x`. The reverse directions would force an additional edge.

**Complete chain-level reduction outside the two-comparable-side C4 case.** Isolated edges contribute the frozen matching summands. A 2-edge path gives one star block if its endpoints are comparable, otherwise two independent edge blocks. A 3-edge path gives a 3-edge, at-most-2-triangle mapping-cone block. A path with at least four edges separates into two disjoint end blocks (each a star block if its endpoint comparability holds) and the remaining individual edge blocks. This last splitting is a literal direct sum because the two possible triples use disjoint edge sets. Longer even cycles consist entirely of individual edge blocks. Every such block has at most two columns, giving the exact cone and acyclicity theorem of Section 2.

In particular, the whole maximum-degree-two class has `E^3` collapse. The stronger `E^2` collapse is proved when no `C_4` component has both sides comparable. A general `E^2` theorem for the remaining C4 case is false: `C4_COUNTEREXAMPLE_PROOF.md` gives an eight-state example with integral `d^2=+/-1`, proving the E3 bound sharp.

## 6. Exact local models

### 6.1 K_(1,2), including the frozen obstruction

Let the centre be `p in P` and leaves `z_1,z_2 in Z`. If the leaves are incomparable there is no triangle and the one-column formula applies. If `z_1<z_2`, let `e_i=(p0,z_i1)` and `t=(p0,z_11,z_21)`. Then

`h: Ctilde(Lambda_t) -> Ctilde(Lambda_e1) plus Ctilde(Lambda_e2)`

is `(i_1,-i_2)` with the ordered orientations used above. The cone formula of Section 2 is the complete chain-level answer. The `K_(2,1)` answer follows by order duality and swapping colours, or directly from the corresponding oriented triangle.

For the minimal coarse chain `p<z_1<z_2` with availability `(1,0,0)`, the available vertices are `p1,z_10,z_20`. The first edge link is two points `p1,z_10`; the second is the disjoint union of `p1` and the segment `z_10<z_20`; the triangle link is two points `p1,z_10`. All have reduced `H_0=Z`. Both inclusion maps are isomorphisms, and `h_0` is the signed diagonal `Z -> Z^2`. Thus the relative cone has exactly `H_1=Z`, and the nonzero `d^1` has rank one. Both *coarse* edge links are contractible, so the independent coarse-link sum is zero. This recovers the frozen counterexample without suppressing it.

### 6.2 P4 (three exclusive edges)

Write edges as `ax,bx,by`, where `a` and `y` are the leaves. The only possible 3-cores are

`t_1=(b0,a0,x1)` if `b<a`,

`t_2=(b0,y1,x1)` if `y<x`.

Their signed boundaries are respectively `ax-bx` and `by-bx`, interpreted as the appropriate link inclusions. There is no four-core because `ay` is absent. Thus `A` has three edge-link summands and `B` has zero, one, or two triple-link summands. Section 2 gives the exact integral answer. When both triple cores exist, they interact through the shared middle edge `bx`; they cannot be treated as independent stars.

### 6.3 K_(2,2)=C4

Label the two `P` vertices `a,b` and the two `Z` vertices `x,y`.

* Neither colour pair comparable: four edge summands, no higher cores; one-column formula.
* Exactly one colour pair comparable: two triple cores and no four-core; two independent two-edge star blocks, hence the two-column theorem.
* Both pairs comparable: relabel so `a<b<x<y`. There are four edges, four triples, and one four-core.

In the last case set `A` to the sum of edge-link chains, `B` to the sum of triple-link chains, and `V=Ctilde(Lambda_abxy)`. Then

`C_m(K,U)=A_(m-2) plus B_(m-3) plus V_(m-4)`

with differential

`d(a,b,c)=(d a+h b, -d b+k c, d c)`.

In the triple order `abx,aby,axy,bxy`, the map `k` has signs `(-,+,-,+)`; every component is the natural link inclusion. The map `h` is determined by

`h(abx)=bx-ax`, `h(aby)=by-ay`,

`h(axy)=ax-ay`, `h(bxy)=bx-by`.

These formulas imply `h k=0`, including the actual inclusion maps. The second page has columns `coker(Hh)`, `ker(Hh)/im(Hk)`, and `ker(Hk)`. There is only one potentially nonzero higher differential:

`d^2: E^2_(4,q) -> E^2_(2,q+1)`.

It has the exact zigzag formula: represent a source class by `c in V_q` with `d c=0`; since `[k c]=0`, choose `b in B_(q+1)` with `d b=k c`. Then

`d^2[c]=[h b]` in `coker(H_(q+1)h)`.

The choice is immaterial on the stated page. There are no further differentials, so `E^3=E^infinity`. The eight-state example proved in `C4_COUNTEREXAMPLE_PROOF.md` has `E^2_(4,0)=E^2_(2,1)=Z` and `d^2=+/-1`, with all cone homology zero. Merely observing that the chain differential lowers core cardinality by at most one does not prove that `d^2=0`.

For the minimal four-chain with profile `(1,1,0,0)`, every available link above is homotopy equivalent to `S^0` and all component maps induce identity up to orientation. The horizontal complex has ranks `1 -> 4 -> 4`, with `k` injective and `h` rank three, so only one `Z` survives in the edge column. The cone has `H_1=Z` and no other reduced homology. This example does not test nonzero `d^2` because its possible source is already killed by `d^1`.

### 6.4 First chordal-bipartite non-Ferrers example

The smallest example without a connectedness requirement is `2K_2`, already a matching. The smallest connected example is `P5`, the four-edge path with edges `ax,bx,by,cy`. The only possible triangles are `bax` if `b<a` and `bcy` if `b<c`. These use disjoint edge sets and give two independent star blocks. Calling `P4` non-Ferrers would be incorrect: its neighbourhoods on each side are nested.

### 6.5 First longer even cycle

For `C6`, and indeed every `C_(2k)` with `k>=3`, same-colour neighbourhoods are distinct sets of size two. Transitivity therefore forbids comparability of a common-neighbour pair. No mixed 3-core exists. Its chain complex is exactly the edge-link direct sum, with no interaction differential at any page. Thus a graph cycle alone is not evidence of core interaction. C4 is the first cycle and the only degree-two cycle allowing a higher core.

## 7. Interaction torsion: updated exact star construction

The existing universality theorem supplies torsion inherited from coarse links in a one-edge matching. That must not be described as torsion created by interaction. A distinct realizable construction, independently checked with the root agent, does give torsion from d1: set `Q={p} ordinal-sum R`, `P={p}`, `Z=R`, and no split states. For each nonempty chain `sigma` of `R`, the mixed core is `p0 union sigma1`, with available link `{p1} disjoint-union Delta(R_<=min(sigma) at bit 0)`, homotopy equivalent to `S^0`. All links thus have torsion-free reduced homology, concentrated in degree zero. The horizontal complex is the negative ordinary, unaugmented chain complex of `Delta R` shifted one core degree. Therefore `H_n cone = H_(n-1)(Delta R)` with ordinary homology on the right. A face poset of a triangulation of `RP^2` gives `H_2 cone=Z/2` and `H_1 cone=Z`: torsion is produced by the d1 interaction complex, with no torsion in any available-link group. This is not a minimality claim. Extensions remain relevant in other integral examples.

## 8. Adversarial checkpoints

* The available links generally cannot be replaced by full coarse edge links outside the one-column case.
* The target shift is `H_n cone = H_(n+1)(K,U)`; omitting it shifts every spectral-sequence conclusion by one.
* Link homology includes degree `-1`, so empty links are retained.
* Spectral-sequence collapse computes associated graded modules, not canonical integral direct sums.
* A two-column bicomplex has no higher differential by support. A three-column one may have a nonzero zigzag differential despite having only vertical and horizontal chain components.
* Graph class alone does not determine homology or even the core poset; same-colour comparability and available links are essential.
* The first chordal-bipartite non-Ferrers connected example is P5, while disconnected 2K2 is smaller.
* All-degree-two E2 collapse is false by the exact eight-state C4 example. The correct unconditional bound is E3, and is sharp.

