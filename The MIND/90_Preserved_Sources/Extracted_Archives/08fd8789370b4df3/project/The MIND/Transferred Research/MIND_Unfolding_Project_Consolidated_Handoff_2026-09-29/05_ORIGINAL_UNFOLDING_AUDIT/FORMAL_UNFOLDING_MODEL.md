# Formal Unfolding Model
## A rigorous two-operator reconstruction

This document gives a mathematically coherent replacement for the 2015 thesis's conflation of logical unfolding and the chain boundary. It deliberately preserves the thesis's core intuition—successive differentiation of a concept—while separating the distinct structures needed to make that intuition precise.

---

## 1. Four levels that must be kept separate

A rigorous theory should distinguish four layers.

### Layer A — semantic attributes

Fix a finite attribute set

\[
A=\{a_1,\dots,a_m\}.
\]

A complete Boolean state is a valuation

\[
x\in\Omega_A:=\{0,1\}^A.
\]

A semantic concept may be represented by a truth set

\[
C\subseteq\Omega_A.
\]

This eliminates syntax dependence when the intended content is only propositional truth conditions.

### Layer B — observational structure

An observation system is a map

\[
q_k:\Omega_A\longrightarrow O_k,
\]

where the fiber \(q_k^{-1}(o)\) is an observational equivalence class at resolution \(k\). We say \(q_{k+1}\) refines \(q_k\) when

\[
q_{k+1}(x)=q_{k+1}(y)\implies q_k(x)=q_k(y).
\]

Equivalently, there is a map \(r_k:O_{k+1}\to O_k\) with

\[
q_k=r_k\circ q_{k+1}.
\]

This is a direct mathematical realization of "successive differentiation": finer observation splits coarse indistinguishability classes.

### Layer C — geometric representation

From observation data build a finite complex \(K_k\). The construction could be a:

- nerve of an observation cover;
- Čech or Vietoris–Rips complex;
- Dowker complex of an object-attribute relation;
- simplicial complex directly specified by compatible attributes;
- order complex of a poset of distinguishable states;
- hypergraph/simplicial closure of empirical co-occurrence data.

The chosen functor must be stated explicitly. Different choices answer different questions.

### Layer D — homological algebra

For a coefficient ring or field \(R\), form the ordinary simplicial chain complex

\[
\cdots\xrightarrow{d_{n+1}} C_n(K_k;R)
\xrightarrow{d_n}C_{n-1}(K_k;R)\xrightarrow{}\cdots
\]

with

\[
d^2=0.
\]

The operator \(d\) is purely topological. It is not the cognitive unfolding operator.

---

# 2. The thesis operator on a fixed factorization

## Definition 2.1 — Factorized concept

Let \(\mathsf B(A)\) denote Boolean functions on \(A\). A factorized concept is a finite ordered tuple

\[
F=(f_1,\dots,f_m),\qquad f_i\in\mathsf B(A).
\]

Its conjunction semantics is

\[
\Pi(F)=\bigwedge_{i=1}^m f_i.
\]

## Definition 2.2 — Thesis unfolding on a factorization

Define

\[
U_{\mathrm{th}}(F)
:=\bigvee_{j=1}^m
\left(\neg f_j\wedge\bigwedge_{i\ne j}f_i\right).
\]

At a valuation \(x\), this is true exactly when precisely one of the factor-values \(f_i(x)\) is false.

### Proposition 2.3 — Exact-one-false characterization

For every factorized concept \(F\),

\[
U_{\mathrm{th}}(F)(x)=1
\quad\Longleftrightarrow\quad
\#\{i:f_i(x)=0\}=1.
\]

**Proof.** Each disjunct selects one distinguished factor \(f_j\) to be false while requiring all remaining factors to be true. Two distinct disjuncts cannot simultaneously hold. ∎

---

# 3. Non-congruence theorem

The central mathematical obstruction to using \(U_{\mathrm{th}}\) as an operator on "the concept itself" is representation dependence.

## Theorem 3.1 — Thesis unfolding does not descend to Boolean equivalence classes

There is no function

\[
\overline U:\mathsf B(A)\to\mathsf B(A)
\]

such that

\[
\overline U(\Pi(F))=U_{\mathrm{th}}(F)
\]

for every factorization \(F\).

### Proof

Take attributes \(X,Y,Z\) and two factorizations

\[
F=(X,Y),\qquad F'=(X,Y,X\vee Z).
\]

Their conjunctions agree:

\[
\Pi(F)=X\wedge Y
=X\wedge Y\wedge(X\vee Z)=\Pi(F').
\]

At \((X,Y,Z)=(0,1,0)\), the factor values of \(F\) are \((0,1)\), so exactly one is false and

\[
U_{\mathrm{th}}(F)=1.
\]

The factor values of \(F'\) are \((0,1,0)\), so two are false and

\[
U_{\mathrm{th}}(F')=0.
\]

Therefore equivalent conjunctions have different unfoldings. ∎

### Consequence

One must choose one of three positions:

1. **syntax/provenance matters**, so a concept includes its factorization;
2. define a **canonical normal form** and unfold only that form;
3. replace \(U_{\mathrm{th}}\) by a semantic operator on truth sets/observations.

For a theory of cognition, option 1 may actually be meaningful: different internal decompositions of extensionally equivalent concepts can encode different cognitive structure. But that must be declared rather than hidden.

---

# 4. Boolean-derivative interpretation

Let

\[
f(x_1,\dots,x_m)=\prod_{i=1}^m x_i
\]

where multiplication denotes Boolean conjunction.

The Boolean derivative in coordinate \(j\) is

\[
\partial^B_j f
:=f(x_j=0)\mathbin{\mathsf{XOR}}f(x_j=1).
\]

For the conjunction monomial,

\[
\partial^B_j f=\prod_{i\ne j}x_i.
\]

Hence the thesis's \(j\)-th summand is

\[
(1-x_j)\partial^B_j f.
\]

## Proposition 4.1 — Gated Boolean derivative

For a positive conjunction,

\[
U_{\mathrm{th}}(f)
=\bigvee_j\left(\neg x_j\wedge\partial^B_j f\right).
\]

This identity is verified exhaustively in `unfolding_boolean_audit.py` through arity five.

### Interpretation

- \(\partial^B_j f\) measures sensitivity of the conjunction to coordinate \(j\).
- The extra factor \(\neg x_j\) chooses the side where the distinguished coordinate is absent/false.
- OR aggregates all one-coordinate distinctions.

This places the thesis construction near established Boolean differential calculus without identifying it with the standard derivative.

---

# 5. Exact-layer unfolding on the Boolean lattice

The cleanest model of repeated differentiation is obtained by retaining which coordinates have been distinguished.

Let \([m]=\{1,\dots,m\}\). For \(S\subseteq[m]\), define the minterm

\[
e_S
:=\left(\bigwedge_{i\in S}\neg x_i\right)
\wedge
\left(\bigwedge_{i\notin S}x_i\right).
\]

The rank \(|S|\) is the number of distinguished/negated coordinates.

## Definition 5.1 — Idempotent unfolding

On the free join-semilattice generated by the \(e_S\), define

\[
D_\vee(e_S)=\bigvee_{j\notin S}e_{S\cup\{j\}},
\]

and extend by joins.

## Theorem 5.2 — Exact-layer theorem

For \(0\le k\le m\),

\[
D_\vee^k(e_\varnothing)
=\bigvee_{|S|=k}e_S.
\]

Moreover,

\[
D_\vee^{m+1}(e_\varnothing)=0.
\]

### Proof

Induct on \(k\). At step \(k\), every rank-\(k\) subset occurs. Applying \(D_\vee\) adds one new coordinate. Every rank-\(k+1\) subset has \(k+1\) rank-\(k\) parents, but idempotent join removes duplicates. No subset exists above rank \(m\). ∎

### Why this matches the thesis better than its printed iteration

The thesis repeatedly describes "one more differentiation" and, for a tetrahedron, gestures toward reaching single distinguished points after repeated application. Rank-by-rank traversal is the precise version of that idea.

This operator is **nilpotent**, not square-zero.

---

# 6. Linear incidence and the emergence of a differential

Replace idempotent join by module addition.

Let \(M_k(R)\) be the free \(R\)-module on \(k\)-subsets of \([m]\). Define

\[
D_k:M_k(R)\to M_{k+1}(R),
\qquad
D_k e_S=\sum_{j\notin S}e_{S\cup\{j\}}.
\]

## Proposition 6.1 — Unsigned square

Over any commutative ring,

\[
D_{k+1}D_k(e_S)
=2\sum_{\substack{T\supset S\\|T|=|S|+2}}e_T.
\]

### Proof

Every \(T=S\cup\{i,j\}\) is reached exactly twice, via \(i\) then \(j\) and via \(j\) then \(i\). ∎

## Corollary 6.2 — Characteristic-two square-zero

Over a ring of characteristic two, in particular \(\mathbf F_2\),

\[
D_{k+1}D_k=0.
\]

This is the unoriented simplicial cochain differential on a simplex.

## Proposition 6.3 — Signed repair over general coefficients

Fix an order on \([m]\) and define

\[
\delta e_S
=\sum_{j\notin S}(-1)^{\epsilon(j,S)}e_{S\cup\{j\}},
\]

where \(\epsilon(j,S)\) counts elements of \(S\) preceding \(j\). Then

\[
\delta^2=0.
\]

The two paths to each two-coordinate enlargement occur with opposite signs.

### Interpretation

The thesis stumbled onto the **incidence pattern** of a cochain complex. Its logical OR aggregation, however, belongs to an idempotent semiring rather than an additive chain module. The square-zero property is recovered only by an explicit algebraic change.

---

# 7. Representation-invariant semantic unfolding

If the model should depend only on semantic states, use a relation on the Boolean cube.

## Definition 7.1 — Directed Hamming refinement relation

For \(x,y\in\Omega_A\), write

\[
xRy
\]

when there is exactly one coordinate \(i\) such that

\[
x_i=1,\qquad y_i=0,
\]

and all other coordinates agree.

For \(C\subseteq\Omega_A\), define

\[
U_!(C)=\{y:\exists x\in C,\ xRy\}.
\]

This is a one-step outward distinction operator.

### Variants

Depending on interpretation one may use:

- undirected Hamming adjacency;
- only 1-to-0 flips;
- attribute-specific permitted directions;
- weighted edges;
- stochastic transition kernels;
- a relation on partial rather than complete valuations.

The choice is empirical/modeling content, not topology.

---

# 8. Adjoint integration and closure

For a relation \(R\subseteq X\times Y\), define existential direct image

\[
\exists_R(A)=\{y:\exists x\in A,\ xRy\}.
\]

Define the universal residual

\[
\forall_R(B)=\{x:R(x)\subseteq B\}.
\]

## Theorem 8.1 — Galois connection

\[
\exists_R(A)\subseteq B
\quad\Longleftrightarrow\quad
A\subseteq\forall_R(B).
\]

### Proof

If every successor of every \(x\in A\) lies in \(B\), then \(A\subseteq\forall_R(B)\). Conversely, if every \(x\in A\) has all successors in \(B\), every element existentially reached from \(A\) lies in \(B\). ∎

This gives a rigorous analogue of an "integration" or reconstruction constraint:

- \(\exists_R\) unfolds/propagates possibilities;
- \(\forall_R\) returns states all of whose unfoldings are compatible with the observed target.

It is an adjoint, not generally an inverse.

The composite

\[
\forall_R\exists_R
\]

is a closure-like operator on source states when the usual adjunction hypotheses are used. Dually \(\exists_R\forall_R\) is interior-like on target states.

---

# 9. Concepts as complexes

The theory now needs a functor from semantic/observational data to topology.

## Model 9A — Nerve of an observation cover

Let \(X\) be a state space and let

\[
\mathcal U_k=\{U_i^{(k)}\}_{i\in I_k}
\]

be observable categories at level \(k\). Define

\[
K_k=N(\mathcal U_k),
\]

with a simplex on \(J\subseteq I_k\) when

\[
\bigcap_{j\in J}U_j^{(k)}\ne\varnothing.
\]

This directly represents compatible co-occurrence of observational categories.

## Model 9B — Dowker complex of an object-attribute relation

For objects \(O\), attributes \(A\), and relation \(R\subseteq O\times A\), one Dowker complex has vertex set \(O\) and simplices consisting of object families sharing a common attribute; the dual has vertex set \(A\) and simplices consisting of attributes shared by a common object.

This is especially close to the thesis's "concepts from attributes" language and connects naturally to Formal Concept Analysis.

## Model 9C — Direct attribute hypergraph

Declare a subset \(\sigma\subseteq A\) to be a simplex exactly when those attributes are jointly compatible/observed. Taking downward closure gives an abstract simplicial complex.

This is the simplest finite prototype.

---

# 10. Genuine chain differential

For an ordered simplex \([v_0,\dots,v_n]\), define

\[
d_n[v_0,\dots,v_n]
=\sum_{i=0}^n(-1)^i[v_0,\dots,\widehat v_i,\dots,v_n].
\]

Then

\[
d_{n-1}d_n=0.
\]

Over \(\mathbf F_2\), signs disappear.

The homology is

\[
H_n(K;R)=\ker d_n/\operatorname{im}d_{n+1}.
\]

This is the only operator in the model that should be called a boundary differential.

---

# 11. Unfolding as a map between complexes

## Definition 11.1 — Simplicial unfolding map

Let \(K_k,K_{k+1}\) be observation complexes. An unfolding map is a simplicial map

\[
u_k:K_k\to K_{k+1}.
\]

It induces a chain map

\[
U_k=C_*(u_k):C_*(K_k;R)\to C_*(K_{k+1};R).
\]

## Theorem 11.2 — Chain compatibility

For every simplicial map \(u_k\),

\[
dU_k=U_kd.
\]

### Proof

The simplicial boundary is natural with respect to vertex maps. On each oriented simplex, taking its image and then summing its faces equals summing faces first and then taking their images. Degenerate simplices are sent to zero in normalized chains. ∎

## Corollary 11.3 — Induced homology map

There is a canonical homomorphism

\[
(U_k)_*:H_n(K_k;R)\to H_n(K_{k+1};R).
\]

This is the exact mathematical answer to the overarching question:

> **Yes. Successive differentiation can be represented rigorously as transformations between complexes, provided an unfolding step is specified as a simplicial map (or a correspondence whose induced map is controlled).**

---

# 12. Directionality problem in refinement

A subtlety is important enough to be built into the formal model.

Suppose \(\mathcal V\) refines a cover \(\mathcal U\), meaning every \(V\in\mathcal V\) lies in some \(U\in\mathcal U\). Choosing such a containing \(U\) for every \(V\) gives a simplicial map

\[
N(\mathcal V)\to N(\mathcal U).
\]

Thus **finer observation naturally maps to coarser observation**, opposite to a temporal "unfolding" arrow.

There are four mathematically honest choices:

1. reverse arrows and regard refinement as an inverse system;
2. use zigzag persistence;
3. choose a forward carrier/section and record the non-canonicity;
4. model temporal accumulation by inclusions of discovered subcomplexes rather than cover refinement.

A paper should choose one, not obscure the issue.

---

# 13. Contiguity controls noncanonical refinement choices

Two simplicial maps \(f,g:K\to L\) are contiguous if for every simplex \(\sigma\subseteq K\),

\[
f(\sigma)\cup g(\sigma)
\]

is a simplex of \(L\).

Contiguous maps are homotopic after geometric realization and induce the same map on homology.

In many nerve-refinement constructions, different choices of a containing coarse set are contiguous. This is the correct tool for proving that the induced homology map is canonical even when the simplicial map is not literally unique.

---

# 14. Mapping cone as unfolding defect

Let

\[
U:C_\bullet\to D_\bullet
\]

be a chain map. Define

\[
\operatorname{Cone}(U)_n=D_n\oplus C_{n-1}
\]

with differential

\[
d_{\mathrm{Cone}}(y,x)
=(d_Dy+Ux,-d_Cx).
\]

## Theorem 14.1 — Quasi-isomorphism criterion

\[
H_*(\operatorname{Cone}(U))=0
\]

if and only if \(U\) is a quasi-isomorphism.

Thus cone homology vanishes precisely when unfolding preserves all homology.

## Theorem 14.2 — Inclusion case

For an inclusion \(i:K\hookrightarrow L\),

\[
H_n(\operatorname{Cone}(C_*(i)))\cong H_n(L,K).
\]

Therefore cone homology records the relative topological information introduced by the step.

### Proposed terminology

For a finite-dimensional model define the **unfolding defect vector**

\[
\Delta(U)
=(\beta_0(\operatorname{Cone}U),\beta_1(\operatorname{Cone}U),\dots).
\]

This is mathematically precise. It should not be called a measure of consciousness or cognitive complexity without empirical justification.

---

# 15. Persistence and zigzags

## Ordinary filtration

If

\[
K_0\subseteq K_1\subseteq\cdots\subseteq K_N,
\]

then \(H_n(K_k)\) forms a persistence module. Long-lived intervals describe topological features stable across observational resolution.

## Zigzag filtration

If an unfolding step sometimes adds and sometimes removes simplices,

\[
K_0\to K_1\leftarrow K_2\to K_3\leftarrow\cdots,
\]

zigzag persistence is the correct theory.

This is likely more faithful than insisting that consciousness/refinement always monotonically adds information.

---

# 16. Gluing and reconstruction

## Definition 16.1 — Subcomplex cover

Let \(K=\bigcup_{i\in I}K_i\), where each \(K_i\) is a subcomplex.

The full intersection diagram contains all

\[
K_{i_0}\cap\cdots\cap K_{i_p}
\]

and all inclusion maps.

## Proposition 16.2 — Exact colimit reconstruction

The union \(K\) is the colimit of its subcomplex-cover intersection diagram.

This is the rigorous combinatorial form of gluing.

## Theorem 16.3 — Nerve reconstruction up to homotopy

If the cover is good—every nonempty finite intersection is contractible—then

\[
|N(\mathcal K)|\simeq |K|.
\]

This is reconstruction of homotopy type, not exact simplex-by-simplex recovery.

---

# 17. No-go result for bare boundary data

## Theorem 17.1 — Proper-face data do not determine a filler

The collection of all proper faces of an \(n\)-simplex does not determine whether the \(n\)-simplex itself is present in an ambient simplicial complex.

### Proof

For \(n=2\), the three edges and vertices occur both in the boundary complex \(\partial\Delta^2\) and in the filled simplex \(\Delta^2\). The proper-face data are identical, but one complex contains the 2-simplex and the other does not. Higher dimensions are analogous. ∎

### Corollary

A general inverse to face-unfolding is impossible unless extra information is retained.

---

# 18. Reconstruction regimes

## 18.1 Provenance regime

Each unfolded piece is stored as a pair

\[
(\tau,\mathrm{parent}(\tau)).
\]

The parent is then exactly recoverable. This is computationally trivial but conceptually important: reconstruction requires memory.

## 18.2 Flag regime

If concepts are restricted to flag complexes, the 1-skeleton determines the whole complex: every clique is filled.

This gives a strong reconstruction theorem but may be cognitively too restrictive because it prohibits genuinely higher-order relations not determined pairwise.

## 18.3 Horn/filler regime

In a simplicial-set formulation, one may specify which compatible horns admit fillers and whether fillers are unique. This separates:

- local compatibility;
- existence of a higher concept;
- uniqueness of that higher concept.

## 18.4 Descent regime

Let \(F\) be a sheaf of local semantic data. Compatible local sections \(s_i\in F(U_i)\) satisfying

\[
s_i|_{U_i\cap U_j}=s_j|_{U_i\cap U_j}
\]

glue uniquely to a global section when the sheaf axiom applies.

A cosheaf is often more natural for assembly of local pieces into a global aggregate.

---

# 19. Symmetry must be represented separately

## Definition 19.1 — Combinatorial symmetry

\[
\operatorname{Aut}(K)
\]

is the group of vertex permutations preserving the simplices of \(K\).

## Definition 19.2 — Observational indistinguishability

Given \(q:X\to O\), define

\[
x\sim_q y\iff q(x)=q(y).
\]

## Definition 19.3 — Refinement

An observation \(q'\) refines \(q\) when

\[
\sim_{q'}\;\subseteq\;\sim_q.
\]

Thus refinement breaks indistinguishability by splitting equivalence classes.

## Definition 19.4 — Group-theoretic symmetry breaking

If a group \(G\) acts on \(X\), an observation \(q\) may preserve a subgroup

\[
G_q=\{g\in G:q(gx)=q(x)\ \forall x\}.
\]

A finer observation can reduce

\[
G_{q'}\le G_q.
\]

This is a precise sense in which differentiation can break symmetry.

### Important separation

No general equation identifies

\[
H_n(K),\quad \operatorname{Aut}(K),\quad X/\!\sim_q.
\]

They measure different structures.

---

# 20. Suggested categorical packaging

A compact formal framework is the following.

## Definition 20.1 — Observation-refinement system

An observation-refinement system consists of:

1. a category \(\mathcal O\) of observational states;
2. a refinement relation/morphism \(r:o'\to o\) meaning \(o'\) is finer than \(o\);
3. a functor
   \[
   K:\mathcal O\to\mathbf{sComp}
   \]
   or, if refinement maps naturally reverse direction,
   \[
   K:\mathcal O^{op}\to\mathbf{sComp};
   \]
4. the chain functor
   \[
   C_*:\mathbf{sComp}\to\mathbf{Ch}_R;
   \]
5. homology
   \[
   H_n:\mathbf{Ch}_R\to R\text{-}\mathbf{Mod};
   \]
6. optionally, a sheaf/cosheaf of semantic data on \(K(o)\).

Then every refinement gives a diagram

\[
o'\to o
\quad\mapsto\quad
K(o')\to K(o)
\quad\mapsto\quad
C_*(K(o'))\to C_*(K(o))
\quad\mapsto\quad
H_n(K(o'))\to H_n(K(o)).
\]

This supplies the categorical backbone missing from the thesis.

---

# 21. The paper-level core

A possible publishable mathematical paper should not attempt to defend the thesis's full psychological claims. Its strongest mathematical spine is:

1. **representation-dependence theorem** for the historical operator;
2. **exact-layer theorem** for the repaired idempotent unfolding;
3. **characteristic-two/signed differential theorem** for the linearization;
4. **semantic Galois connection** for relational unfolding/integration;
5. **chain-map formulation** for observation/refinement complexes;
6. **mapping-cone defect invariant**;
7. **no-go theorem for reconstruction from bare faces**;
8. **descent/colimit reconstruction theorem under explicit hypotheses**;
9. **counterexample theorem separating homology from symmetry**.

The strongest contribution would be a theorem tying items 5–8 together for a specific, nontrivial observation functor rather than presenting them only as a framework.
