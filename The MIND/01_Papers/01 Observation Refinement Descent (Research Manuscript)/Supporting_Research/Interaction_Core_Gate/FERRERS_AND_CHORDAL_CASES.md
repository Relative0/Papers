# Ferrers and chordal-bipartite cases: exact star theorem and collapse failures

Date: 2026-09-29. Finalized gate deliverable, combining the structural/literature investigation with certified computations from the parallel audit. The frozen manuscript was not edited.

## 1. The graph alone omits essential data

Ferrers means that the neighborhoods on either colour class are linearly ordered by inclusion (isolated vertices allowed). Chordal-bipartite means that there is no induced even cycle of length at least six. These conditions constrain cross-colour comparisons only. A mixed core additionally requires that its P vertices form a chain and its Z vertices form a chain. Available links and their inclusion maps are further data.

For example, both of the following have exclusive graph K_{2,2}, with P={p1,p2}, Z={z1,z2}, and no split states.

* If Q is the chain p1<p2<z1<z2, the largest mixed core has four vertices. The refined order complex has two contractible components, Q is contractible, and cone homology is Z in degree one only.
* If Q is the height-two poset with all four relations pi<zj and no same-colour relations, mixed cores have size two only. Delta Q is a four-cycle and the refined complex consists of four isolated points. The cone has H_1=Z^4 and no other reduced homology.

Thus even the complete Ferrers graph does not determine the interaction-core poset or the cone homology. This observation does not, by itself, disprove a universal E2-collapse statement.

## 2. Exact star realization of arbitrary induced-poset pairs

**Proposition.** Let R be a nonempty finite poset and C an arbitrary subset with its induced order. Write Z=R\\C. Set Q={p} ordinal-sum R, with p 1-only, all Z states 0-only, and every C state split. Then the exclusive graph is K_{1,|Z|}, together with any vacuous convention when Z is empty. For every coefficient ring A,

    H_n(Cone(Delta pi); A) = H_{n-1}(Delta R, Delta C; A).

Ordinary relative homology is intended, including C empty. In particular H_0(Delta R,empty) is ordinary H_0, not reduced H_0.

**Proof.** Write the refined order complex L as B union T, where

    B = Delta((R x {0}) union (C x {1})),
    T = Delta(({p} x {1}) union (C x {1})).

Every refined chain that contains (p,1) lies in T, and every other refined chain lies in B. The intersection is Delta(C x {1}). The map B -> Delta(R x {0}) induced by (c,1)->(c,0) and fixing the bottom row is an order-preserving descending retraction. Under this retraction the intersection map becomes Delta C -> Delta R. T is a cone, including the case C empty when it is a single vertex. Since the original inclusions of simplicial complexes are cofibrations, their union is a homotopy pushout. Hence L is homotopy equivalent to the homotopy cofiber of Delta C -> Delta R (with a disjoint cone point when C is empty). Q has a minimum, so the homotopy cofiber of L -> Delta Q has reduced homology shifted once from L. The cofiber-pair correspondence gives the formula. QED.

**Consequences.** Every finite simplicial pair (X,Y) is represented after barycentric subdivision by R=the nonempty-face poset of X and C=the nonempty-face poset of Y. Thus star exclusive graphs already encode arbitrary simplicial-pair homology, shifted once. This is a sharp warning against graph-only torsion-freeness, sphere, or numerical-homology classifications. It is an elementary mapping-cylinder/cofiber realization, not a new general topological mechanism. It does not prove or refute E2 collapse: the filtration itself still needs analysis.

## 3. Exact deletion recursion, and why graph elimination is insufficient

For a simplicial pair (K,U), with a vertex v of U, put

    K' = K-v, U' = U-v,
    J = lk_K(v), V = lk_U(v).

The standard relative deletion-link short exact sequence is

    0 -> C_*(K',U') -> C_*(K,U) -> C_{*-1}(J,V) -> 0.

With v oriented first, the quotient differential is minus the link differential. Equivalently C_*(K,U) is the mapping cone of the inclusion-induced chain map C_*(J,V)->C_*(K',U'). This includes the usual long exact homology sequence. It is an exact chain recursion; link homology groups without the attaching maps are not enough to compute the middle group.

The restriction v in U holds for every vertex in the present two-colour pair, because every singleton avoids at least one missing colour. For a general pair with v not in U, the analogous formula requires augmented link chains and the void-complex convention; the unaugmented formula above must not be used unchanged in degree zero.

For a missing vertex v of colour 0 in the two-colour deletion pair, V consists of link simplices avoiding every missing colour-1 vertex. Deleting v from K destroys the full product form Q x 2. Turning its coarse state into a split state instead keeps K but changes the relative subcomplex, a different operation.

Known bisimplicial/weak-simplicial elimination orders in chordal-bipartite graphs can organize an algorithm. They do not automatically give a compatible collapse of this simplicial pair. In particular deleting a graph edge pz is not necessarily a permitted poset edit: if p<c<z remains, transitivity forces p<z. A proof must lift graph elimination to the full relative chain complex and control the available-link attaching maps. No such general lift was established in this subtask.

## 4. Minimal graph examples and bounded-core consequences

The smallest chordal-bipartite non-Ferrers graph, if disconnected graphs are permitted, is 2K2; it is already matching. The smallest connected example is the four-edge path P5, whose extreme neighborhoods are incomparable. The three-edge path P4 is Ferrers and must not be mislabeled non-Ferrers.

For any graph with no K_{2,2}, mixed cores are stars (one colour has exactly one vertex). If the maximum degree is at most two and the graph has no K_{2,2} component, every mixed core has size at most three. A core-size spectral sequence therefore has only columns two and three, so E2=E-infinity by degree reasons. This covers all paths and cycles of length at least six; any separate analysis of K_{2,2} is the remaining maximum-degree-two issue. The page collapse gives an associated graded homology statement; integral extensions need a chain model or additional splitting argument.

For arbitrary Ferrers and chordal-bipartite graphs there is no uniform small bound on core size: Q can be a long chain with a P block followed by a Z block, giving a complete bipartite exclusive graph and arbitrarily large cores. In a fixed example with largest core size s, only columns 2,...,s occur, hence all d^r with r>=s-1 vanish and E^{s-1}=E-infinity for s>=2 (E1 when s=2). This is a standard filtration-width bound, not a class-specific collapse theorem.

## 5. Exact all-exclusive star theorem and interaction-created torsion

**Theorem.** In Section 2 take C empty, so Q={p}+R, p is 1-only and every R state is 0-only. Each mixed core has the form S={(p,0)} union (sigma x {1}), where sigma is a nonempty chain in R. Its available link is

    Lambda_S = {(p,1)} disjoint-union Delta(R_{<=min(sigma)} x {0}).

The second component is a cone, so the only reduced link homology is Htilde_0=Z. Choose the generator given by the isolated point minus any lower-component point. Core-deletion inclusions preserve this generator. With missing vertices oriented first, d1 is the negative ordinary simplicial differential of Delta R; uniform degree signs give a chain isomorphism to the usual complex. A k-simplex lies in core column k+2. All other rows vanish. Hence E2=E-infinity integrally and

    H_n(Cone(Delta pi);Z) = H_{n-1}(Delta R;Z).

The proof also works over arbitrary coefficients. There is only one surviving filtration grade per total degree, so no additive-extension ambiguity remains.

This is an exact interacting class of unbounded degree and core size. Its usefulness is the explicit coefficient-diagram identification, not new spectral-sequence machinery.

**Torsion consequence.** Let R be the nonempty-face poset of a triangulated real projective plane. Every Lambda_S has free reduced homology Z in degree zero, yet the d1 complex has Z/2 in degree one. Therefore the cone has H_1=Z and H_2=Z/2; interaction creates torsion independently of torsion in any available link. Moreover each coarse edge [p,z] link is the vertex link of z in the barycentric subdivision of the triangulated surface, hence a circle. The coarse edge links are torsion-free as well.

The script `verify_torsion_star.py` uses the ten triangles

    012, 013, 024, 035, 045, 125, 134, 145, 234, 235.

It checks all edge degrees are two, all six vertex links are connected five-cycles, and the f-vector is (6,15,10). Thus this is a connected closed surface with Euler characteristic one. Exact SNF confirms its H_1=Z/2. Its face poset has 31 vertices, giving a 32-state carrier example with graph K_{1,31}. `interaction_torsion_star.json` records SNF of all 181 available links, all 31 coarse edge links, and the reduced E1 interaction complex. The cone groups follow from the proved chain reduction. A direct SNF of the entire doubled 32-state relative pair was not performed, and no minimality is claimed.

## 6. Noncollapse witness from the parallel computational task

The gate's computation task supplied `minimal_star_d2.json`; the following independent topological argument proves its integral noncollapse. Let Q have covers

    0<1, 0<2, 1<3, 2<3, 2<5, 3<4, 3<6, 5<6,

with P={0}, Z={2,3,6}, C={1,4,5}. The exclusive graph is K_{1,3}, hence both Ferrers and chordal-bipartite. Write a_b for product vertex (a,b). The available-link table is:

| Missing core | Available link | Homotopy type |
|---|---|---|
| {0_0,2_1} | Four-cycle on 0_1,4_1,2_0,5_1 | S1 |
| {0_0,3_1} | Has maximum 4_1 | Point |
| {0_0,6_1} | Lower cone Delta(R_{<=6} x0), with the mapping cylinder from the two points {1_1,5_1}, and a cone over those points with apex 0_1 | S1 |
| {0_0,2_1,3_1} | Path 0_1--4_1--2_0 | Point |
| {0_0,2_1,6_1} | Path 0_1--5_1--2_0 | Point |
| {0_0,3_1,6_1} | Lower cone Delta({1,2,3} x0), with pendant path 1_0--1_1--0_1 | Point |
| {0_0,2_1,3_1,6_1} | Two points {0_1,2_0} | S0 |

For the third row, the lower-plus-upper-cylinder piece retracts downward onto the lower cone; it intersects the cone with apex 0_1 in two points. Their homotopy pushout is S1.

For total homology use Section 2. R=Q\\{0} is covered by the lower ideals of its maxima 4 and 6. Both ideals are cones and their intersection is the lower ideal of 3, another cone. Thus Delta R is contractible. Delta C is the edge 1<4 disjoint from the point 5. Hence H_1(Delta R,Delta C)=Z and every other relative group vanishes; cone H_2=Z only.

The link table gives integral E1=E2 with Z^2 in (p,q)=(2,1) and Z in (p,q)=(4,0), and no other terms. The sole possible higher differential is d2:Z->Z^2. The total homology computation forces this differential to be an injection with primitive image. In particular it is nonzero over every field. Over F2, in (core column,total chain degree) coordinates, the pages are

    E1=E2: (2,3) -> F2^2, (4,4) -> F2,
    rank d2: (4,4) -> (2,3) equals 1,
    E3=E-infinity: (2,3) -> F2.

Thus graph-only Ferrers and chordal-bipartite E2-collapse statements are false. The separate files `star_d2_integral_certificate.json` and `verify_d2_certificate.py` additionally provide oriented integer source/correction chains and SNF checks. This is minimal among induced restrictions of that witness, not a proved globally smallest example. It has seven coarse states and 79 mixed relative cells.

## 7. Verdict for these two classes

The all-exclusive star profile above gives an exact positive theorem, including arbitrarily large interacting cores and interaction-created torsion. Arbitrary split states invalidate a graph-only E2 theorem already for K_{1,3}.

There is also an eight-state K_{2,2} example in `C4_COUNTEREXAMPLE_PROOF.md`, with integral d2:Z->Z a unit isomorphism and zero cone homology. It lies simultaneously in maximum-degree-two, Ferrers, and chordal-bipartite classes. Thus even degree two plus Ferrers/chordality does not force E2 collapse. The seven-state star remains the smaller exhibited counterexample for Ferrers and chordal-bipartite hypotheses; the C4 example sharpens the maximum-degree boundary. Neither is claimed globally minimal.

The generic deletion recursion remains exact but requires chain maps. A sharper theorem should characterize which available-link diagrams admit a compatible elimination, rather than assuming a Ferrers diagram alone supplies that compatibility.
