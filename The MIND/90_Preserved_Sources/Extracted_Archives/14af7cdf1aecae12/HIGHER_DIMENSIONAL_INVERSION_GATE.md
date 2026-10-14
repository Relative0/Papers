# Higher-Dimensional Inversion Complex Classification Gate

**Project:** Mathematical Reconstruction of Matte-Blanco's Unfolding Function and Mental Space  
**Date:** 29 September 2026  
**Gate verdict:** **LEVEL A -- STRONG SUCCESS, with a conservative priority qualification.**

The gate found an exact all-dimensional **integral homology classification** on a natural noninteraction class: carrier-splitting systems whose **exclusive inversion graph is a matching**.  The classification is not restricted by height.  It can produce homology in arbitrarily high degree and can transfer torsion.  A second exact corollary gives a particularly clean Boolean/distributive-lattice classification.  The underlying simplicial deletion/cofiber technology has substantial prior art, so the publication claim should be the specialized observation-theoretic recognition and exact link formula, not the generic topology of deleting vertices.

---

## 1. Frozen setting

Let `Q` be a finite observational `T0` poset and let a new Boolean observation `psi` produce a refined carrier

\[
Q^\psi\subseteq Q\times\{0,1\},
\]

ordered by the product order.  Write

\[
A_a=\{s\in Q:(s,a)\in Q^\psi\},\qquad a\in\{0,1\}.
\]

Separate the coarse states into

\[
P=A_1\setminus A_0 \quad\text{(1-only)},\qquad
Z=A_0\setminus A_1 \quad\text{(0-only)},\qquad
C=A_0\cap A_1 \quad\text{(split)}.
\]

The preceding carrier-splitting gate used a split completion `Qhat^psi`.  The present gate found a second, more useful all-height model.

---

## 2. Full-doubling / missing-copy model

Let

\[
D=Q\times\mathbf 2,
\qquad K=\Delta D,
\qquad L=\Delta Q^\psi.
\]

The actual refined carrier is obtained from `D` by deleting exactly

\[
M_0=\{(p,0):p\in P\},
\qquad
M_1=\{(z,1):z\in Z\}.
\]

Thus `L` is the induced subcomplex of `K` on the remaining vertices.

The projection

\[
D\longrightarrow Q
\]

is a homotopy equivalence: it has both the bottom-row and top-row closure sections.  Consequently the homotopy cofiber of

\[
\Delta\pi:\Delta Q^\psi\to\Delta Q
\]

has the same reduced homology as the relative pair

\[
H_*(K,L;R).
\]

This model is useful because carrier splitting becomes a very special **two-colour vertex deletion problem** from the product order complex `Delta(Q x 2)`.

---

## 3. General two-colour deletion square

Delete the two kinds of missing vertices separately:

\[
K_P=K[V(K)\setminus M_0],
\qquad
K_Z=K[V(K)\setminus M_1],
\]

and put

\[
U=K_P\cup K_Z,
\qquad
L=K_P\cap K_Z.
\]

`K_P` retracts by the ascending closure operator `(s,a) -> (s,1)` to the full top row, while `K_Z` retracts by the descending closure operator `(s,a) -> (s,0)` to the full bottom row.  Hence both inclusions

\[
K_P\hookrightarrow K,
\qquad
K_Z\hookrightarrow K
\]

are homotopy equivalences.

The long exact sequences of triples plus simplicial excision therefore give, for every coefficient ring `R`,

\[
\boxed{
H_n(K,L;R)\cong H_{n+1}(K,U;R).
}
\tag{3.1}
\]

This is the fundamental algebraic reduction of the new gate.

A simplex lies in `K \ U` exactly when it contains **at least one missing lower copy** `(p,0)`, `p in P`, and **at least one missing upper copy** `(z,1)`, `z in Z`.

---

## 4. Exclusive inversion graph

Define the bipartite graph

\[
G_\psi=(P\sqcup Z,E_\psi),
\qquad
E_\psi=\{(p,z)\in P\times Z:p<z\text{ in }Q\}.
\]

Call it the **exclusive inversion graph**.

It records exactly the places where a coarse comparison tries to run from a state where only outcome `1` is available to a later state where only outcome `0` is available.

For every relative simplex `sigma in K \ U`, let

\[
P(\sigma)=\{p\in P:(p,0)\in\sigma\},
\qquad
Z(\sigma)=\{z\in Z:(z,1)\in\sigma\}.
\]

Because `sigma` is a chain in `Q x 2`,

\[
P(\sigma)\times Z(\sigma)\subseteq E_\psi.
\]

Thus every higher interaction in the relative complex is supported on a **biclique** of the exclusive inversion graph.  This is the structural reason a matching is special: it forbids every mixed core larger than one edge.

---

## 5. Exact all-height theorem

### Theorem -- Exclusive-Inversion Matching Theorem

Assume that `E_psi` is a matching; equivalently, every `1`-only state and every `0`-only state participates in at most one exclusive inversion.

Then for every integer `n` and every coefficient ring `R`,

\[
\boxed{
H_n\!\left(\operatorname{Cone}(\Delta\pi);R\right)
\cong
\bigoplus_{(p,z)\in E_\psi}
\widetilde H_{n-2}\!\left(
\operatorname{lk}_{\Delta Q}[p,z];R
\right).
}
\tag{5.1}
\]

In particular, integrally,

\[
\boxed{
H_n\!\left(\operatorname{Cone}(\Delta\pi);\mathbb Z\right)
\cong
\bigoplus_{(p,z)\in E_\psi}
\widetilde H_{n-2}\!\left(
\operatorname{lk}_{\Delta Q}[p,z];\mathbb Z
\right).
}
\tag{5.2}
\]

The theorem is a complete homology classification on this class: Betti numbers and torsion are read off from coarse **edge links**.

### Immediate necessary-and-sufficient homological criterion

Under the matching hypothesis, the carrier split is an integral homology equivalence iff every relevant coarse edge link is integrally acyclic:

\[
\Delta\pi\text{ is a homology equivalence}
\iff
\widetilde H_*(\operatorname{lk}_{\Delta Q}[p,z];\mathbb Z)=0
\quad\forall(p,z)\in E_\psi.
\]

The same statement holds over any chosen coefficient field/ring with that coefficient system substituted.

---

## 6. Proof of the matching theorem

### 6.1 Unique mixed core

A simplex in `K \ U` contains at least one vertex `(p,0)` with `p in P` and one vertex `(z,1)` with `z in Z`.  Any such pair in the same product-order chain satisfies `p<z`, hence gives an edge of `E_psi`.

If a relative simplex contained two different missing lower vertices and one missing upper vertex, the latter would have degree at least two in `E_psi`.  Dually, two missing upper vertices and one missing lower vertex would force degree at least two on the lower endpoint.  Therefore, when `E_psi` is a matching, every simplex in `K \ U` contains a **unique** pair

\[
e=((p,0)<(z,1)),\qquad (p,z)\in E_\psi.
\]

### 6.2 Chain-level direct sum

The relative chain complex consequently splits:

\[
C_m(K,U;R)
=\bigoplus_{e\in E_\psi} C_m^{(e)}.
\]

For a fixed edge `e`, every relative simplex is uniquely `e union tau` with `tau` a simplex in `lk_K(e)`.  Deleting either endpoint of `e` lands in `U` and is zero in the relative quotient; deleting a vertex of `tau` remains in the same `e`-summand.  Hence, up to the harmless orientation sign,

\[
C_m^{(e)}\cong \widetilde C_{m-2}(\operatorname{lk}_K e).
\]

Thus

\[
H_m(K,U;R)
\cong
\bigoplus_{e\in E_\psi}
\widetilde H_{m-2}(\operatorname{lk}_K e;R).
\tag{6.1}
\]

Combining (3.1) and (6.1),

\[
H_n(K,L;R)
\cong
\bigoplus_{e\in E_\psi}
\widetilde H_{n-1}(\operatorname{lk}_K e;R).
\tag{6.2}
\]

### 6.3 Product-edge link is a suspension of the coarse edge link

For `e=((p,0)<(z,1))`, the product edge link decomposes as

\[
\operatorname{lk}_{\Delta(Q\times\mathbf2)}e
=
\Delta(Q_{<p}) * \Delta M_{p,z} * \Delta(Q_{>z}),
\]

where

\[
M_{p,z}=((p,0),(z,1))_{Q\times\mathbf2}.
\]

Let `R=(p,z)_Q`.  The middle poset consists of `(p,1)`, `R x 2`, and `(z,0)`.  Remove `(z,0)`: the result closes upward onto the bit-1 row and has minimum `(p,1)`, hence is contractible.  Remove `(p,1)`: the result closes downward onto the bit-0 row and has maximum `(z,0)`, hence is contractible.  Their intersection is `R x 2`, homotopy equivalent to `R`.  Since `(p,1)` and `(z,0)` are incomparable, these two subcomplexes cover the middle order complex.  Therefore

\[
\Delta M_{p,z}\simeq \Sigma\Delta(p,z)_Q.
\]

Consequently

\[
\operatorname{lk}_{\Delta(Q\times\mathbf2)}e
\simeq
\Sigma\,\operatorname{lk}_{\Delta Q}[p,z].
\tag{6.3}
\]

Applying reduced homology to (6.2) and (6.3) proves (5.1).

---

## 7. Exact neutrality before the first inversion

The exclusive graph also gives a clean zeroth obstruction.

### Proposition -- isotone extension criterion

If `E_psi` is empty, then `Delta pi` is a homotopy equivalence.

Indeed, the prescribed partial Boolean labeling

- `b(p)=1` on `P`,
- `b(z)=0` on `Z`,

extends monotonically to all of `Q` iff there is no `p in P`, `z in Z` with `p<z`.  One explicit extension is

\[
b(s)=1 \iff \exists p\in P\text{ with }p\le s.
\]

The section `r(s)=(s,b(s))` satisfies `pi r=id_Q`.  Define

\[
c_+(s,a)=(s,\max\{a,b(s)\}).
\]

Then

\[
\operatorname{id}_{Q^\psi}\le c_+\ge r\pi,
\]

so `r pi` is homotopic to the identity through comparable monotone maps.

Thus a nonempty exclusive inversion graph is a necessary condition for a carrier-splitting homotopy defect.

---

## 8. General interaction-core filtration

The matching theorem is the collapse case of a broader all-height filtration.

For `sigma in K \ U`, define its **missing core**

\[
S(\sigma)=\sigma\cap(M_0\cup M_1).
\]

It contains vertices of both colours.  Filter the relative complex `C_*(K,U)` by core cardinality:

\[
F_r C_m
=
\langle\sigma:\ |S(\sigma)|\le r\rangle,
\qquad r\ge2.
\]

The boundary cannot increase the core size.  Let `C_r` denote the set of `r`-vertex mixed missing cores that are simplices of `K`, and for `S in C_r` let

\[
\Lambda_S
=
\operatorname{lk}_K(S)[V(L)]
\]

be the part of the link supported on available vertices.  Then

\[
\operatorname{gr}_r C_m(K,U)
\cong
\bigoplus_{S\in\mathcal C_r}
\widetilde C_{m-r}(\Lambda_S).
\tag{8.1}
\]

Hence there is a convergent spectral sequence whose first page is assembled from

\[
\widetilde H_*(\Lambda_S)
\]

indexed by mixed missing cores.  Every core projects to a chain-supported biclique of `G_psi`; differentials between filtration levels are exactly the interactions produced by deleting missing vertices.

For a matching there are no mixed cores with more than two vertices, so the filtration collapses immediately and gives Theorem (5.1).  For the old weighted-height-at-most-two regime, the only surviving core interactions are deleted edge/triangle incidences; the former rooted-incidence graph is the low-dimensional shadow of this filtration.

This filtration is the strongest general result found at this gate outside the exact matching class.  It is useful, but it is not advertised as a closed higher-dimensional classification.

---

## 9. Bounded-poset and Boolean/distributive corollaries

Assume `Q` has a least element `0hat` and greatest element `1hat` and the exclusive inversion graph is a matching.

For a coarse edge `p<z`,

\[
\operatorname{lk}_{\Delta Q}[p,z]
=
\Delta(Q_{<p})*\Delta(p,z)*\Delta(Q_{>z}).
\]

If `p != 0hat`, the first factor has a minimum and is contractible.  If `z != 1hat`, the last factor has a maximum and is contractible.  Therefore **only the global endpoint inversion can contribute**:

\[
H_n(\operatorname{Cone}\Delta\pi;\mathbb Z)
\cong
\begin{cases}
\widetilde H_{n-2}(\Delta(Q\setminus\{\hat0,\hat1\});\mathbb Z),
& \hat0\in P,\ \hat1\in Z,\\
0,&\text{otherwise.}
\end{cases}
\tag{9.1}
\]

### Finite distributive lattices

Let `Q=L=J(R)` be a finite distributive lattice.  By the crosscut theorem, together with the standard atom structure of `J(R)`, the proper-part order complex is

- contractible if `R` is not an antichain;
- a sphere `S^{r-2}` if `R` is an `r`-element antichain, equivalently `L=B_r` is Boolean.

Therefore, under the endpoint matching profile,

\[
H_n(\operatorname{Cone}\Delta\pi;\mathbb Z)
\cong
\begin{cases}
\mathbb Z,&L=B_r\text{ and }n=r,\\
0,&\text{otherwise.}
\end{cases}
\tag{9.2}
\]

This gives genuine higher-dimensional examples:

\[
B_2\rightsquigarrow H_2\cong\mathbb Z,
\qquad
B_3\rightsquigarrow H_3\cong\mathbb Z,
\qquad
B_4\rightsquigarrow H_4\cong\mathbb Z.
\]

The first two were checked directly by integral Smith-normal-form computation; the `B_4` result follows from the theorem and was checked through the link formula.

---

## 10. Horn and dual-Horn regimes

A different conclusion holds when the **entire refined signature relation** is Horn.

If `Q^psi` is a nonempty meet-closed subset of a Boolean cube, then it has a least element (the meet of all realized refined signatures).  Its coordinate projection `Q` is also meet-closed, hence also has a least element.  Both order complexes are contractible, so

\[
\Delta\pi:\Delta Q^\psi\to\Delta Q
\]

is a homotopy equivalence.

Dually, a nonempty join-closed refined relation has a greatest element, as does its projection, and is again homotopy-neutral.

Thus **pure Horn/dual-Horn closure does not generate a nontrivial carrier-splitting defect**.  It is a useful exact neutral class, not the source of the desired higher-dimensional topology.

This is deliberately narrower than the companion paper's Horn-type repair criterion: it assumes closure of the full refined realized-signature relation itself, not merely that one truth region of an arbitrary observation is Horn-definable.

---

## 11. Torsion and universality inside the exact matching class

The matching condition controls **interaction between inversion defects**, not the topology of the coarse edge links.

Let `R` be any nonempty finite poset.  Form

\[
Q=\hat0\oplus R\oplus\hat1
\]

by adjoining a global bottom and top.  Make `0hat` 1-only, `1hat` 0-only, and every state of `R` genuinely split.  Then

\[
E_\psi=\{(\hat0,\hat1)\}
\]

is a one-edge matching and

\[
\operatorname{lk}_{\Delta Q}[\hat0,\hat1]=\Delta R.
\]

Therefore

\[
\boxed{
H_n(\operatorname{Cone}\Delta\pi;\mathbb Z)
\cong
\widetilde H_{n-2}(\Delta R;\mathbb Z).
}
\tag{11.1}
\]

Consequences:

1. nonzero cone homology occurs in arbitrarily high degree inside the matching class;
2. arbitrary integral torsion occurring in finite-poset homology transfers two degrees upward;
3. a universal wedge-of-spheres theorem is false even under exclusive-inversion matching;
4. matching does **not** imply total unimodularity.

For example, using a finite-poset model of `RP^2` as `R` yields `Z/2` torsion in cone degree 3.  The 13-point projective-plane model cited in the companion paper gives a small explicit construction after adjoining the two endpoints, but minimality in the matching class is not claimed here.

---

## 12. Sharp failure outside the matching hypothesis

The smallest possible nonmatching exclusive graph already destroys naive edgewise additivity.

Take the three-element chain

\[
0<1<2
\]

with availability profile

\[
(\{1\},\{0\},\{0\}).
\]

Then

\[
E_\psi=\{(0,1),(0,2)\},
\]

a two-edge star, hence a forest but not a matching.

Direct integral computation gives

\[
H_1(\operatorname{Cone}\Delta\pi;\mathbb Z)\cong\mathbb Z.
\]

However both individual coarse edge links are contractible, so the naive sum of the matching formula predicts zero.

The missing 2-simplex containing `(0,0),(1,1),(2,1)` couples the two inversion edges.  Therefore:

\[
\boxed{\text{``exclusive inversion graph is a forest'' is not enough.}}
\]

Three coarse states are minimal for this failure because a nonmatching bipartite graph needs at least three incident vertices.

---

## 13. Total-unimodularity boundary

The earlier height-two theorem had a TU relative boundary matrix because its columns were signed graph-incidence columns.

That phenomenon does not survive the present all-height class.  Dey--Hirani--Krishnamoorthy characterize TU of a simplicial boundary matrix by torsion-freeness of a whole family of pure relative subcomplex pairs, not merely by torsion-freeness of one global homology group.  The matching realization (11.1) transfers arbitrary torsion, so matching cannot imply TU.

Even when every edge link is torsion-free and the cone homology is therefore free, that alone is insufficient to claim TU of all inversion boundary matrices.  No new all-dimensional forbidden-minor characterization of TU was established at this gate.

**Verdict for the TU program:** useful negative boundary, not a new TU theorem.

---

## 14. Computational evidence

The new verifier `verify_matching_inversion_theorem.py` performs exact integral Smith-normal-form computations on the full doubled-product relative pair.

### Exhaustive results

Across every naturally labelled finite coarse poset on at most four states and all fiber profiles `{0}`, `{1}`, `{0,1}`:

- **3,450** poset/profile cases were examined;
- **3,242** satisfied the exclusive-inversion matching condition and were checked integrally by Smith normal form;
- **566** of those had at least one exclusive inversion edge;
- **0** failures of formula (5.2) occurred;
- every profile with empty exclusive inversion graph was `F2`-acyclic, agreeing with the homotopy proof.

### Additional tests

- **1,707** product-edge-link suspension identities were checked over `F2` for all comparable pairs in all naturally labelled coarse posets through five states;
- **3,000** deterministic random five-state profile trials were run; **639** nonempty matching cases were checked directly over `F2`, with **0 failures**;
- direct integral computations give `H_2=Z` for the Boolean endpoint `B_2` example and `H_3=Z` for `B_3`;
- the three-chain star counterexample gives actual `H_1=Z` while the false pairwise-link extension predicts zero.

A separate Horn verifier exhaustively checked all nonempty Boolean relations through four coordinates:

- dimension 4 contains **4,959** meet-closed relations and **4,959** join-closed relations;
- every meet-closed relation and its projection had a least element;
- every join-closed relation and its projection had a greatest element.

A distributive-lattice verifier checked all order-ideal lattices generated by naturally labelled posets through three generators (10 cases): the endpoint formula agreed exactly with direct integral computation, with the Boolean cases spherical and every non-Boolean distributive case neutral.

---

## 15. Comparison of the four requested programs

| Program | Outcome | Status |
|---|---|---|
| Boolean/Horn signature posets | Pure Horn/dual-Horn refined relations are exactly neutral; bounded/distributive matching gives a clean sphere-or-zero formula | **Exact, but the Horn part is topologically trivial; Boolean/distributive corollary is useful** |
| Bounded comparability | Height `<=2` remains completely classified by the prior rooted theorem; height 3 already allows torsion; coarse chains have a known Ferrers/independence-complex classification | **No new universal bounded-comparability classification** |
| Controlled lower/upper fibers | Classical fiber theorems give strong sufficient/decomposition results, but do not yield the new exact formula without added hypotheses | **Useful comparison, not the main result** |
| Descent / inversion filtration | Missing cores are bicliques of `G_psi`; the core-size filtration gives a spectral sequence; matching forces immediate collapse | **General mechanism + exact matching collapse** |

---

## 16. Literature and novelty boundary

The closest prior work found is not nerve theory but **simplicial vertex-deletion / obstruction-complex theory**.

1. Björner--Wachs--Welker, *Poset fiber theorems*, Trans. AMS 357 (2005), gives homotopy decompositions of a poset from lower fibers under connectivity assumptions.  This is the main benchmark for the controlled-fiber program.
2. Chachólski--Jin--Scolamiero--Tombari, *Homotopical decompositions of simplicial and Vietoris Rips complexes*, J. Applied and Computational Topology 5 (2021), studies induced subcomplexes obtained from vertex covers and measures failure by obstruction complexes.  Its one-, two-, and several-outside-point constructions are the closest antecedent to the missing-copy model.
3. Dey--Hirani--Krishnamoorthy, *Optimal Homologous Cycles, Total Unimodularity, and Linear Programming*, SIAM J. Comput. 40 (2011), gives the relevant topological characterization of TU boundary matrices.
4. Stong's finite-space reductions, Barmak's poset form of Quillen's Theorem A, and Fernández--Minian relation/mapping-cylinder methods are standard background for the closure and fiber arguments.
5. Horn model classes being closed under componentwise conjunction/intersection is classical Boolean-CSP / closure-system theory.
6. Crosscut/shellability theory for distributive and semidistributive lattices supplies the sphere-or-contractible behavior used in the lattice corollary.

### Conservative priority assessment

I did **not** locate the following exact statement in the searched literature:

> for a Boolean carrier split, if the 1-only-to-0-only comparison graph is a matching, the complete integral mapping-cone homology is the direct sum of two-degree-shifted reduced homologies of the corresponding coarse edge links.

However, this statement is built from standard vertex-deletion/cofiber ingredients, especially close to the obstruction-complex framework of Chachólski et al.  It should therefore be presented as a **specialized exact recognition theorem for the observation-refinement model**, not as a claim that link/cofiber decomposition itself is new.

A publication-priority claim should remain qualified until a specialist literature referee has checked whether the matching specialization occurs implicitly in the vertex-cover/deletion literature.

The 2026 search also found recent work on discrete homotopy/homology of finite posets, but not this two-colour carrier-splitting classification.

---

## 17. Adversarial specialist reviews

### Referee A -- finite-poset topology

**Attack:** "This is just Quillen/Björner--Wachs--Welker after rewriting the fibers."

**Finding:** not fully.  BWW supplies a powerful homotopy decomposition when lower fibers meet connectivity hypotheses.  The matching formula works integrally without those hypotheses and allows arbitrary torsion through coarse edge links.  The proof, however, uses standard poset/order-complex ideas.  **Revision:** claim exact specialization, not foundational new fiber theory.

### Referee B -- combinatorial topology

**Attack:** "The missing-copy proof is generic vertex deletion."

**Finding:** substantially correct as a priority warning.  Chachólski et al. explicitly develop obstruction complexes and cofiber sequences for one, two, and several outside vertices.  **Revision:** position the new content in the observation-theoretic identification of missing copies, the exclusive inversion graph, the biclique filtration, and the matching direct-sum reduction.

### Referee C -- integer homology / TU

**Attack:** "Matching should force torsion-free or TU matrices."

**Finding:** false.  The endpoint construction transfers arbitrary reduced integral homology of a coarse link two degrees upward, including torsion.  **Revision:** remove any blanket TU suggestion and retain only the exact homology formula.

### Referee D -- Horn / closure systems

**Attack:** "Horn might give the desired nontrivial class."

**Finding:** when the whole refined relation is meet-closed, both refined and projected posets have minima and are contractible.  Pure Horn closure therefore trivializes the topological defect rather than classifying a rich one.  **Revision:** retain Horn as a neutral regime and use Boolean/distributive lattices as the nontrivial structured example.

### Hostile referee -- smallest destroyer

**Task:** destroy the edgewise formula as soon as matching is relaxed.

**Result:** the three-state chain with profile `(1-only, 0-only, 0-only)` does so.  The exclusive inversion graph is a forest, but the two inversion edges interact through a 2-simplex and produce `H_1=Z` even though the individual coarse edge links contribute zero.

This is a strong reason to keep the matching hypothesis explicit.

---

## 18. Success level

### **LEVEL A -- STRONG SUCCESS**

The rubric for Level A is met mathematically:

- the class is natural: noninteracting exclusive inversions;
- the classification is necessary-and-sufficient for all integral cone homology on that class;
- the theorem is all-dimensional;
- the proof is exact;
- exhaustive integral and targeted higher-order computation support it;
- a minimal failure outside the hypothesis is known.

The **priority confidence is lower than the correctness confidence** because general obstruction-complex/vertex-deletion theory is close prior art.  The paper should distinguish those two judgments.

---

## 19. Answers to the ten required questions

1. **Does a nontrivial higher-dimensional exact classification exist?**  **Yes.**  Exclusive-inversion matching gives an exact all-dimensional integral formula.
2. **Strongest class?**  Carrier-splitting systems for which the bipartite graph of `1`-only-to-`0`-only coarse comparisons is a matching.
3. **Exact theorem?**  Formula (5.2): the cone homology is the direct sum of two-degree-shifted reduced homologies of the corresponding coarse edge links.
4. **Integral, field-dependent, or rational?**  **Integral.**  It holds over arbitrary coefficients.
5. **Does torsion occur?**  **Yes.**  Arbitrary finite-poset link torsion can be transferred two degrees upward.
6. **Stronger than standard poset-fiber theory?**  **As a specialized computation, yes:** it gives exact groups without BWW connectivity hypotheses.  **As general topology, no:** its proof sits close to standard vertex-deletion/cofiber machinery.
7. **Does it recover the `h_psi(Q)<=2` rooted-forest theorem?**  On the matching locus, yes at the homology level.  The general interaction-core filtration specializes to the deleted-edge/deleted-triangle incidence complex underlying the full low-height theorem.  The matching theorem by itself does not subsume every low-height nonmatching case.
8. **Smallest counterexample outside the hypothesis?**  Three-chain `0<1<2` with profile `(1,0,0)`; exclusive graph `K_{1,2}`, actual `H_1=Z`, naive edge-link sum zero.
9. **Should it replace the carrier-splitting theorem as the paper's main result?**  **Not replace; strengthen.**  The carrier-splitting factorization is the general structural theorem.  The matching-link theorem should become the strongest exact all-height theorem immediately after it.
10. **Single next theorem?**  Construct and classify the **exclusive-inversion interaction spectral sequence** beyond matching, beginning with exclusive graphs of maximum degree two or chordal/Ferrers biclique structure, and determine conditions forcing collapse at `E^2`.

---

## 20. Recommended manuscript action

The result is strong enough to justify a new manuscript section, but not a wholesale rewrite of the paper yet.

Insert, in this order:

1. the full-doubling / missing-copy model;
2. the two-colour deletion square and shift isomorphism;
3. the exclusive inversion graph;
4. the interaction-core filtration;
5. the matching-link theorem and proof;
6. bounded-poset and Boolean/distributive corollaries;
7. the three-chain forest counterexample;
8. the torsion/universality sharpness result;
9. a literature paragraph explicitly crediting obstruction-complex deletion theory.

The next gate should attack degree-two interaction rather than broadening the theorem by wishful analogy from matching to forests.
