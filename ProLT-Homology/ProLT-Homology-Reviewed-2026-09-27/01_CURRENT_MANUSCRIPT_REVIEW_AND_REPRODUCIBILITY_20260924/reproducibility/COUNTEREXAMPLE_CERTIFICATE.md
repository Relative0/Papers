# ProLT post-audit theorem update: the two-bit height-two conjecture is false

**Date:** 24 September 2026

## Question

Let `P` be a finite poset of height at most two, let

\[
\alpha:P\to\{0,1\}^2,
\]

and define the thinned order `Q` on the same vertices by

\[
x\le_Q y \iff x\le_P y\text{ and }\alpha(x)\le\alpha(y)\text{ coordinatewise}.
\]

Writing `K=Delta(P)` and `L=Delta(Q)`, does `F_2`-homology neutrality of `L -> K` force a direct simplicial collapse `K \searrow L`?

## Answer

**No.** There is a seven-vertex counterexample. It is vertex-minimal: a complete enumeration of all naturally labelled posets of height at most two on at most six vertices, together with all two-bit vertex labels, finds no counterexample. Every finite poset has a natural labelling, so this covers every isomorphism type through six vertices.

The counterexample is stronger than required: its relative integer boundary matrix has determinant `-1`, so the inclusion is an integral homology equivalence; both endpoint posets beat-reduce to a point, so the inclusion is also a homotopy equivalence; nevertheless no direct deleted-edge/deleted-triangle collapse can even start.

## Seven-vertex certificate

Use vertices `0,1,2,3,4,5,6`. The strict order of `P` is

```text
(0,2) (0,3) (0,4) (0,5) (0,6)
(1,2) (1,4) (1,5) (1,6)
(2,5) (2,6)
(3,5) (3,6)
(4,5)
```

This has height two. Assign the two-bit labels

```text
0: 10
1: 01
2: 01
3: 00
4: 11
5: 00
6: 01
```

The retained strict order `Q` is

```text
(0,4)
(1,2) (1,4) (1,6)
(2,6)
(3,5) (3,6)
```

The deleted edges, in row order, are

```text
e1=(0,2)
e2=(0,3)
e3=(0,5)
e4=(0,6)
e5=(1,5)
e6=(2,5)
e7=(4,5)
```

The deleted triangles, in column order, are

```text
t1=(0,2,5)
t2=(0,2,6)
t3=(0,3,5)
t4=(0,3,6)
t5=(0,4,5)
t6=(1,2,5)
t7=(1,4,5)
```

With the usual ordered simplicial orientation, the relative boundary matrix
`B_Z : C_2(K,L;Z) -> C_1(K,L;Z)` is

\[
B_{\mathbb Z}=
\begin{pmatrix}
 1& 1& 0& 0& 0& 0& 0\\
 0& 0& 1& 1& 0& 0& 0\\
-1& 0&-1& 0&-1& 0& 0\\
 0&-1& 0&-1& 0& 0& 0\\
 0& 0& 0& 0& 0&-1&-1\\
 1& 0& 0& 0& 0& 1& 0\\
 0& 0& 0& 0& 1& 0& 1
\end{pmatrix}.
\]

Exact calculation gives

\[
\det B_{\mathbb Z}=-1.
\]

Hence `B_Z` is unimodular and the relative homology vanishes over `Z`, and therefore over every field, including `F_2`.

## Why direct collapse fails

The deleted-edge/deleted-triangle support graph has exactly three perfect matchings. Equivalently, the determinant expansion has three nonzero fitting-orientation terms, with signed contributions `-1,+1,-1`, summing to `-1`.

The deleted-edge triangle-degrees are

```text
(0,2): 2
(0,3): 2
(0,5): 3
(0,6): 2
(1,5): 2
(2,5): 2
(4,5): 2
```

Thus no deleted edge lies in exactly one remaining deleted triangle at the initial stage. A relative elementary collapse `K -> L` would have to begin by pairing a deleted edge with its unique deleted triangle coface. No such edge exists, so a direct collapse is impossible.

Equivalently, by the post-audit matching theorem for height-two relative complexes, direct collapse is equivalent to uniqueness of the perfect matching; here there are three.

## Endpoint homotopy type

Both `P` and `Q` admit complete beat-point reductions to a single point. One certificate is:

```text
P:
3 down->0,
4 up->5,
0 up->2,
1 up->2,
5 down->2,
2 up->6.

Q:
0 up->4,
2 down->1,
4 down->1,
1 up->6,
5 down->3,
3 up->6.
```

Therefore both finite spaces/order complexes are contractible. The inclusion `L -> K` is a homotopy equivalence, despite the absence of a direct relative collapse.

## Minimality in vertex count

An optimized exhaustive checker was cross-validated at five vertices against the earlier independent Python computation:

```text
n=5
posets=330
profiles=337,920
F2-neutral=103,562
neutral but non-direct-collapse=0
```

It then completed all six-vertex cases:

```text
n=6
posets=4,117
profiles=16,863,232
square relative matrices=3,865,228
F2-neutral=3,767,044
neutral but non-direct-collapse=0
```

The first seven-vertex witness above was found by the same natural-poset/all-label enumeration. Hence seven vertices are necessary and sufficient.

The seven-vertex run was stopped upon finding the first witness; no claim is made here about the total number of seven-vertex witnesses or minimality in the number of deleted cells.

## Consequences for the manuscript

1. The formerly open two-bit question is settled **negatively**.
2. The earlier eight-state, three-bit example is no longer the sharp bit-count boundary. The collapse equivalence already fails with **two** observation bits.
3. The one-bit theorem remains genuinely sharp in bit count: one bit forces the forest/collapse equivalence at height two, while two bits do not.
4. The two-bit counterexample is especially strong because it is integral-homology-neutral and homotopy-neutral, not merely `F_2`-neutral.
5. The block paper no longer needs a conjectural two-bit section; instead it should present this seven-state example as the exact first bit-complexity failure, while crediting general fitting-orientation cancellation as standard higher-dimensional rooted-forest behavior.
6. The focused one-bit paper gains a clean sharpness theorem: **one bit is the maximal bit count for which the height-two homology-neutrality => direct-collapse implication holds universally.**

## Reproducibility files

- `verify_two_bit_height_two_counterexample.py` — exact standalone certificate checker.
- `two_bit_height2_exhaustive.cpp` — optimized enumeration used for the completed n<=6 search and discovery at n=7.
- `two_bit_n5_fast.out`, `two_bit_n6_fast.out` — completed search summaries.
