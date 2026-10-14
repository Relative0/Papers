# Audit additions and independent proofs

**Issued:** 24 September 2026. **Status:** additions produced during the audit, not claims that were already in v0.1-v0.5. These are mathematical proofs and reproducible constructions, not a novelty certification. Source identifiers R01-R22 refer to `LITERATURE_SOURCES.md`.

## A1. Integral one-bit incidence theorem and complete relative homology

Let P be a finite poset of height at most two, where height counts strict inequalities. Let b:P -> {0,1}, and put

\[
x\le_Qy\quad\Longleftrightarrow\quad x\le_Py\text{ and }b(x)\le b(y),
\qquad K=\Delta P,\quad L=\Delta Q.
\]

All vertices survive. Write E and T for the deleted edges and triangles. With the order orientation, the only possibly nonzero relative boundary is

\[
B:C_2(K,L;\mathbb Z)=\mathbb Z^T\longrightarrow
C_1(K,L;\mathbb Z)=\mathbb Z^E.
\]

For a triangle x<y<z, the boundary is [y,z]-[x,z]+[x,y]. The four deleted binary patterns have the following columns:

| Pattern | Deleted edges | Integral coefficients |
|---|---|---|
| 010 | yz | +1 |
| 101 | xy | +1 |
| 100 | xy, xz | +1, -1 |
| 110 | xz, yz | -1, +1 |

Every other binary pattern retains the triangle. In particular, a deleted triangle never has zero or three deleted edges.

Construct the graph G with vertex set E together with one formal root for every connected component of P. A two-entry column is an oriented edge between its two deleted-edge vertices. A one-entry column is an oriented edge between that vertex and its component root. Then B is an oriented incidence matrix with all root rows removed. This observation strengthens v0.4 Proposition `prop:incidence` from F2 to Z.

**Theorem.** B is totally unimodular. Let c0 be the number of connected components of G containing no root, and let beta1(G)=|T|-|V(G)|+c(G). Then

\[
H_2(K,L;\mathbb Z)\cong\mathbb Z^{\beta_1(G)},\qquad
H_1(K,L;\mathbb Z)\cong\mathbb Z^{c_0},\qquad H_0(K,L;\mathbb Z)=0.
\]

Thus every integral relative homology group is free, and its ranks are independent of the coefficient field.

**Proof.** The oriented incidence matrix of a graph is totally unimodular: in any square submatrix, a column with at most one nonzero allows determinant induction; if every column has two entries, their opposite signs make the row sum zero. Deleting rows preserves this property. Each graph component has at most one root, since its vertices and edges stay inside one coarse component and there is just one root there. On a component with a root, reduced incidence has full row rank and cokernel zero. On one without a root, ordinary incidence has cokernel Z. In either case, the kernel is its integral cycle space. Direct sums give the formula. Isolated roots contribute neither a row nor a homology generator. Empty E and T give the zero complex, as required. QED.

**Collapse consequence.** All six equivalences in v0.4's repair-forest theorem remain correct. They can now include integral homology equivalence and homology equivalence over any one field. If the graph is a rooted forest, choose a nonroot leaf. It is a deleted edge with exactly one current deleted triangle above it. No retained triangle contains a deleted edge because L is a subcomplex. There are no higher cells. Consequently this is an actual free-face collapse, not merely algebraic cancellation. Repetition ends precisely at L. Multi-edges, when present, produce graph cycles and do not invalidate this argument.

**Prior-art assessment:** graph incidence and total unimodularity are standard; relative torsion interpretations are established [R03,R04]. The binary-labelled-poset recognition step is the specific adaptation. This is not a new matrix-tree theorem.

## A2. Exact observation-design parameter as coloring and generalized Boolean rank

Let P and Q be partial orders on the same finite set V, with Q contained in P. The package defines odim_P(Q) as the least k for which there is a map a:V -> {0,1}^k satisfying

\[
x\le_Qy\iff \bigl(x\le_Py\text{ and }a(x)\le a(y)\bigr).
\]

No injectivity is imposed on a, and a is not an order embedding of Q in general.

Let D={(x,y):x<_P y and x not<=_Q y}. Define a simple conflict graph Gamma(P,Q) on D by declaring two distinct demands (x,y),(u,v) adjacent when

\[
x\le_Qv\quad\text{or}\quad u\le_Qy.
\]

**Theorem.** With chromatic number zero for the empty graph,

\[
\operatorname{odim}_P(Q)=\chi(\Gamma(P,Q)).
\]

**Proof.** Each coordinate must be isotone on Q, so its truth set U is a Q-upset. It deletes exactly those demands (x,y) with x in U and y not in U. Two conflicting demands cannot both be deleted by this bit: for example x<=_Q v would force v into U whenever x is in U.

Conversely, let S be an independent set of demands. Take U to be the Q-upward closure of all first entries of demands in S. No second entry of a demand in S belongs to U: such membership would say that a first entry lies below that second entry, giving either a conflict or a forbidden self-demand. Therefore this one bit deletes all demands in S and preserves every Q-comparison. A coloring supplies one bit per color class. Conversely, assign each demand to any coordinate deleting it; each resulting color class is independent. QED.

**Exact established optimization framework.** Form a generalized binary matrix indexed by V x V:

\[
M_{xy}=\begin{cases}
0&x\le_Qy,\\
1&x\le_Py\text{ but }x\not\le_Qy,\\
?&\text{otherwise}.
\end{cases}
\]

A rectangle is allowed to contain 1s and question marks but no zeros, and only the 1s must be covered. Then

\[
\operatorname{odim}_P(Q)=\operatorname{br}(M),
\]

where br is generalized Boolean rank, or the generalized rectangle-cover number [R07,R08]. Indeed, a bit U supplies U x (V\U). Conversely, any allowed rectangle A x B can be enlarged to the valid upset cut U x (V\U), where U=up_Q A: the absence of zeros says U intersects B trivially. The conflict graph above is the complement of the rectangle-cover compatibility graph on required entries. Thus the general covering/coloring mechanism is established mathematics, not an independently new type of dimension.

**Corrected complexity theorem.** For explicitly represented same-ground-set P,Q, deciding odim_P(Q)<=k is NP-complete. It is already NP-hard for k=3 when both orders have height at most one.

Given a graph H on vertices 1,...,m, create minima a_i and maxima b_i. In Q, put a_i<b_j and a_j<b_i exactly when ij is an edge of H. Let P add the m diagonal comparisons a_i<b_i. Both relations are partial orders of height at most one. Their demands are exactly (a_i,b_i), and the conflict graph is H. Thus odim_P(Q)=chi(H). The construction is polynomial. Membership in NP follows from the n-coordinate principal-ideal bound: a binary label certificate has polynomial size, and all ordered pairs can be checked directly. For k>=n the answer is immediately yes.

**Important limitation:** this repairs the unrestricted complexity claim, not the original assertion that hardness already holds when P is total. That restricted claim remains unproved in this audit.

**Useful immediate bounds.**

\[
\omega(\Gamma)\le\operatorname{odim}_P(Q)
\le\min\{|D|,|V|,\dim_2(Q)\},
\]

and odim=0 exactly when P=Q. The |V| upper bound uses principal Q-ideals as labels; dim_2(Q) is only an upper bound, not an equality. A one-bit realization exists exactly when Gamma has no edges (and D is nonempty for equality to one).

**Exact target-antichain case.** If Q is the antichain on V and h is the maximum number of elements in a chain of nonempty P, then

\[
\operatorname{odim}_P(Q)=\lceil\log_2 h\rceil.
\]

Along a P-chain all labels must be distinct, proving the lower bound. Assign each element its longest-chain rank. Choose h distinct subsets of a k-set in reverse linear-extension order of the Boolean lattice. If rank(x)<rank(y), the assigned subset at x is not contained in the subset at y. Therefore every strict P-comparison is deleted. This gives the upper bound. For V empty define the value to be zero separately.

This shows especially clearly why Sperner's classical antichain embedding bound is not the right bound for this relative problem.

**Exact label minima for named examples.** The five-state compensating block has minimum one bit for its final Q, namely (1,0,0,0,1), even though its originally chosen two coordinates each behave differently. The thirteen-state torsion pair in A5 has minimum two bits. The eight-state noncollapse pair has minimum three: its original three-bit labels give an upper bound, while the demands (0,3), (2,5), and (3,6) form a triangle in the conflict graph. These three conflicts follow respectively from 0<=_Q5, 2<=_Q6, and reflexivity at 3. Thus the known eight-state pair cannot simply be relabelled with two bits. `minimize_named_labels.py` supplies independent standard-library certificates for all three statements.

## A3. Relative Mayer-Vietoris interaction sequence

Let A=K_1 and B=K_2 be the one-coordinate retained subcomplexes of K=Delta(P). Set I=A cap B and U=A cup B. Work over any commutative coefficient ring. There is a natural degreewise short exact sequence

\[
0\longrightarrow C_*(K,I)
\overset{d}{\longrightarrow}C_*(K,A)\oplus C_*(K,B)
\overset{e}{\longrightarrow}C_*(K,U)\longrightarrow0,
\]

where d([c])=([c],[c]) and e([a],[b])=[a-b]. This is exact simplex by simplex: a simplex is in both subcomplexes, only one, or neither. Hence

\[
\cdots\to H_{n+1}(K,U)\to H_n(K,I)
\to H_n(K,A)\oplus H_n(K,B)
\to H_n(K,U)\to\cdots.
\]

**Interaction corollary.** If both coordinate inclusions induce homology isomorphisms, then naturally

\[
H_n(K,I)\cong H_{n+1}(K,U).
\]

The failure of joint homological neutrality is precisely the shifted defect of the union of the two individually retained complexes. This is a useful application of relative Mayer-Vietoris [R18], not a novel exact-sequence construction.

**Minimal test.** On the three-chain, the profiles 010 and 101 retain two different two-edge trees. Their union is the boundary of the original triangle, while their intersection is one edge plus the remaining isolated vertex. Thus H_2(K,U)=Z and H_1(K,I)=Z. The interaction is detected by an isomorphism in the connecting map. It is not just an unexplained change in Betti numbers.

For more coordinates, iterating this sequence or using the usual Cech double complex of intersections gives higher-order bookkeeping. No new spectral sequence is claimed here, and introducing one is not recommended without an example or theorem unavailable from this two-coordinate sequence. Homological conclusions do not automatically become homotopical conclusions.

## A4. Direct relative collapse is equivalent to a unique fitting orientation in height two

For an arbitrary block thinning Q contained in P of height at most two, let B be the relative edge-triangle matrix. Its bipartite support graph has deleted edges on one side and deleted triangles on the other. A perfect matching is a fitting orientation.

**Theorem.** The following are equivalent:

1. K collapses directly to L by deleted edge-triangle pairs.
2. The support graph has an acyclic perfect matching.
3. The support graph has exactly one perfect matching.

The empty matrix has the single empty matching and corresponds to the identity collapse.

**Proof.** A collapse gives a complete acyclic matching. Relative acyclic matching gives a collapse, since all unmatched cells form the subcomplex L. Alternatively, this implication follows directly by topologically ordering matched pairs.

For a perfect matching, a directed cycle in the reversed incidence graph is exactly an alternating cycle. Flipping such a cycle produces a second perfect matching. Conversely, the symmetric difference of two perfect matchings is a disjoint union of alternating cycles. Thus a perfect matching is acyclic exactly when it is the unique perfect matching. For a direct free-face argument, orient dependencies from a matched edge to every other edge in its triangle. An acyclic dependency graph has a source with no occurrences in other matched triangles; that deleted edge is free. Recurse. QED.

**Scope.** This is stronger than v0.5's stated sufficient condition, but it is standard matching/discrete-Morse reasoning [R03,R19]. It does not say that every homotopy-equivalent inclusion collapses directly. The package's eight-state example has three perfect matchings, all cyclic, yet both endpoint posets are beat-contractible.

## A5. Explicit block torsion and a general construction

### General realization

Let X be a connected finite two-dimensional simplicial complex, P its nonempty face poset, and K=Delta(P)=sd(X). In the comparability graph of P, take the bipartite subgraph joining rank-zero faces to all incident positive-dimensional faces. It is connected. Choose a spanning tree in this graph and retain precisely its oriented comparisons as Q. It is a poset because it has only two levels, so no new transitivity requirements arise. L=Delta(Q) is a tree containing every vertex of K.

Since L is nonempty and contractible,

\[
H_k(K,L;\mathbb Z)\cong\widetilde H_k(X;\mathbb Z)\quad(k\ge1).
\]

The block-universality construction, with a(v)=down_Q(v), realizes Q as an observation thinning of P. Wedges of finite triangulated Moore spaces therefore realize arbitrary finite abelian relative H_1-torsion in height two. This is an adaptation of face-poset realization and standard relative homology, not a new existence theorem about torsion in complexes.

### A clean 13-state Z/2 example

Use the regular CW decomposition of RP2 obtained by quotienting the boundary of an octahedron by the antipodal involution. It has three vertices a,b,c, six edges AB+,AB-,AC+,AC-,BC+,BC-, and four triangular cells indexed by signs (s,t) in {+,-}^2. The boundary edges of cell (s,t) are AB_s, AC_t, BC_(st). Each cell contains all three vertices. The face poset P has 13 elements, 36 strict comparisons, and 24 three-element chains. A spanning-tree suborder Q retains twelve vertex-to-positive-cell comparisons.

The resulting relative matrix is 24 x 24, with Smith diagonal

\[
(1,\ldots,1,2),\quad |\det B|=2.
\]

Therefore H_1(K,L;Z)=Z/2 and H_2(K,L;Z)=0. Over F2, the relative Betti numbers in degrees 0,1,2 are (0,1,1); over F3 and F5 they are all zero.

The complete order, original principal-ideal labels, relative matrix, and Smith output are in `torsion2_RP2_13.json`. The conflict-coloring theorem A2 compresses this same Q to **exactly two bits**, with labels in the JSON vertex order

    (0,1,3,1,2,3,2,1,1,0,0,0,0).

Direct comparison of every P-pair verifies that these labels give exactly the same Q. A conflict edge rules out one bit. Thus this is already a **two-observation** torsion example. It is rationally (and F3-) homology-neutral but not F2-neutral, so any proposed two-bit preservation theorem must retain the F2 hypothesis. The compression and lower-bound certificate are in `torsion2_RP2_13_minimal_labels.json`. The underlying 13-point RP2 model belongs to established finite-space topology [R15]. This is not claimed to be the smallest arbitrary relative torsion pair: lower bounds on absolute torsion do not by themselves prove lower bounds for every relative pair. It is a small clean construction, and minimality holds only within the absolute-torsion/tree-target route if one invokes R15's thirteen-point lower bound.

### A 79-state Z/3 example invisible to F2 homology

Construct the simplicial mapping cone of a degree-three covering map from a 9-cycle to a 3-cycle. Denote the base vertices by v_j (j modulo 3), domain vertices by u_i (i modulo 9), and cone vertex by w. For every i, with j=i modulo 3, take the three triangles

\[
[u_i,v_j,v_{j+1}],\quad [u_i,u_{i+1},v_{j+1}],\quad[w,u_i,u_{i+1}].
\]

The complex has f-vector (13,39,27), with H_1=Z/3 and H_2=0. Its face poset has 79 points. Apply the same spanning-tree construction. The relative 162 x 162 matrix has Smith diagonal (1,...,1,3). Over F2 and F5 it is invertible; over F3 its relative Betti vector is (0,1,1).

Thus an observation block may be F2-homology-neutral but not integrally homology-neutral and hence not homotopy-neutral. This answers the coefficient-sensitivity question constructively. The example is explicit, reproducible, and not claimed minimal. Files: `torsion3_base_complex.json`, `torsion3_Moore_79.json`.

## A6. One bit already realizes arbitrary topology in higher height

Let R be any nonempty finite poset and choose a minimal element z. Add a new greatest element t, forming P=R union {t}. Define b(z)=b(t)=0 and b(x)=1 for all other x in R.

**Theorem.** The thinning Q retains all comparisons of R and precisely the extra comparison z<t. Therefore

\[
\Delta(P)=\operatorname{cone}(\Delta R),\qquad
\Delta(Q)=\Delta R\cup_{\{z\}}[z,t],
\]

and Delta(Q) collapses to Delta(R). In particular,

\[
\Delta Q\hookrightarrow\Delta P\text{ is a homotopy equivalence}
\iff\Delta R\text{ is contractible},
\]

and

\[
H_k(\Delta P,\Delta Q;\mathbb Z)
\cong\widetilde H_{k-1}(\Delta R;\mathbb Z)\quad(k\ge1).
\]

**Proof.** Since z is minimal, every old comparison is either 0->1 or 1->1 (besides identities); none is lost. All comparisons x<t with x!=z are 1->0 and are deleted. The comparison z<t survives. The top vertex makes Delta(P) a cone, and t is a leaf in Delta(Q). The relative formula follows from the long exact sequence and contractibility of the cone. QED.

**Consequences.**

- Unrestricted homotopy-neutrality of the order-complex map is undecidable already for one bit, non-splitting refinement, and a coarse poset with a greatest element. Take R to be the face poset of an input finite nonempty complex. The reduction is effective; the classical unrestricted contractibility theorem supplies the impossibility [R05]. This statement concerns order-complex homotopy equivalence, not an unqualified ordinary finite-space homotopy decision problem.
- Taking the 13-point RP2 model for R gives a 14-state, height-three, one-bit refinement with relative H_2=Z/2. Its F2 relative Betti vector is (0,0,1,1).
- Taking the 79-point Moore model gives an 80-state, height-three, one-bit refinement with relative H_2=Z/3. It is F2-homology-neutral but not integrally neutral. Its F3 vector is (0,0,1,1).
- Taking an acyclic noncontractible finite complex, such as a triangulated punctured Poincare homology sphere, gives integral homology-neutrality without homotopy-neutrality for one bit in a higher-height regime.

This is a sharp explanation of why v0.4 requires its height restriction. A universal one-bit acyclic 'first descent' matching cannot exist, even when the coarse complex is a cone. Proposed higher-height matching theorems must impose real extra hypotheses, not just a bounded/coarse-contractible endpoint.

The construction and its checks are in `higher_height_and_edges.py` and the two `onebit_height3_...json` files. Its ingredients are elementary; its specific refinement formulation remains a candidate adaptation rather than an established novelty claim.
