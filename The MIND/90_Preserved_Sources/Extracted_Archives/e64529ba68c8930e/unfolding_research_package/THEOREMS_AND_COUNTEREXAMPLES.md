# Theorems and Counterexamples

This file isolates the mathematical statements that survive reconstruction, together with direct counterexamples to claims that do not.

All Boolean examples use ordinary two-valued semantics. Homology calculations in the finite examples use \(\mathbf F_2\) unless otherwise stated.

---

## T1. Fixed-factor thesis unfolding is well-defined

Let \(F=(f_1,\ldots,f_m)\) be a fixed ordered list of Boolean functions. Define

\[
U_{\rm th}(F)=\bigvee_j\left(\neg f_j\wedge\bigwedge_{i\ne j}f_i\right).
\]

Then \(U_{\rm th}(F)\) is a well-defined Boolean function and is true exactly where one factor-value is false.

**Classification:** sound.

---

## T2. Non-congruence / syntax-dependence theorem

The thesis unfolding does not descend through conjunction semantics to logical equivalence classes.

Take

\[
F=(X,Y),\qquad F'=(X,Y,X\vee Z).
\]

Although

\[
\bigwedge F\equiv\bigwedge F'\equiv X\wedge Y,
\]

at \((X,Y,Z)=(0,1,0)\),

\[
U_{\rm th}(F)=1,\qquad U_{\rm th}(F')=0.
\]

Therefore no semantic operator \(\bar U\) depending only on the Boolean function \(\bigwedge F\) can agree with the thesis rule for every factorization.

**Classification:** sound negative theorem.

**Implication:** either internal factorization is part of a concept, or the operator must be replaced/canonicalized.

---

## T3. Gated Boolean derivative theorem

For

\[
f=x_1\wedge\cdots\wedge x_m,
\]

the standard Boolean derivative satisfies

\[
\partial_j^Bf=\bigwedge_{i\ne j}x_i.
\]

Hence

\[
U_{\rm th}(f)
=\bigvee_j\left(\neg x_j\wedge\partial_j^B f\right).
\]

The accompanying script verifies the identity exhaustively for all valuations through arity five.

**Classification:** sound; close antecedent in Boolean differential calculus.

---

## T4. Exact-layer unfolding theorem

Let \(e_S\) encode the minterm whose false-coordinate set is \(S\subseteq[m]\). Define

\[
D_\vee(e_S)=\bigvee_{j\notin S}e_{S\cup\{j\}}.
\]

Then

\[
D_\vee^k(e_\varnothing)=\bigvee_{|S|=k}e_S
\]

and

\[
D_\vee^{m+1}(e_\varnothing)=0.
\]

**Proof:** induction on Boolean-lattice rank; duplicates collapse under idempotent OR.

**Classification:** sound repaired construction.

---

## C1. Original unfolding is not a chain differential

Already for \(X\wedge Y\wedge Z\), one application is nonzero and a natural second exact-layer application is also nonzero. More generally \(D_\vee^2\ne0\) for \(m\ge2\).

Therefore the original Boolean-OR operation cannot satisfy the defining chain condition \(d^2=0\).

**Classification of "unfolding = boundary": false.**

---

## T5. Unsigned incidence square theorem

Linearize exact-layer unfolding over a commutative ring \(R\):

\[
D(e_S)=\sum_{j\notin S}e_{S\cup\{j\}}.
\]

Then

\[
D^2(e_S)=2\sum_{\substack{T\supset S\\|T|=|S|+2}}e_T.
\]

Every rank-two enlargement is reached in exactly two orders.

### Corollary

Over characteristic two,

\[
D^2=0.
\]

**Classification:** sound.

---

## T6. Signed incidence gives the standard differential

With standard incidence signs,

\[
\delta(e_S)=\sum_{j\notin S}(-1)^{\epsilon(j,S)}e_{S\cup\{j\}},
\]

one has

\[
\delta^2=0
\]

over arbitrary coefficients.

This is the simplicial cochain differential after identifying subsets with faces.

**Classification:** standard mathematics; provides the nearest genuine differential to the thesis operator.

---

## C2. Thesis Example 2.6 does not implement an exact second unfolding layer

The thesis prints

\[
E=X\wedge\neg(Y\wedge Z)
\vee Y\wedge\neg(X\wedge Z)
\vee Z\wedge\neg(X\wedge Y).
\]

Its truth set is

\[
001,010,011,100,101,110,
\]

that is, all nonconstant assignments.

The exact two-negation layer from \(111\) is only

\[
001,010,100.
\]

Thus the printed iteration combines two adjacent Hamming layers.

**Classification:** inconsistent with the clean rank-layer interpretation.

---

## T7. Relational unfolding has a right adjoint

For a relation \(R\subseteq X\times Y\), define

\[
\exists_R(A)=\{y:\exists x\in A,\,xRy\}
\]

and

\[
\forall_R(B)=\{x:R(x)\subseteq B\}.
\]

Then

\[
\exists_R(A)\subseteq B
\iff
A\subseteq\forall_R(B).
\]

Thus unfolding admits a canonical residual/integration-like operator in the sense of order theory.

**Classification:** standard relational adjunction; promising for the reconstructed theory.

---

## C3. There is no general inverse to relational unfolding

Let directed unfolding flip one coordinate from 1 to 0. The vertex \(00\cdots0\) has no outgoing moves, so

\[
U_!(\{00\cdots0\})=\varnothing
=U_!(\varnothing).
\]

Hence \(U_!\) is not injective on general subsets and has no inverse.

**Classification of a universal inverse "integrator": false without extra hypotheses.**

---

## C4. Thesis gluing Example 2.7 is false

The thesis displays

\[
[(X\wedge Y)\vee(Y\wedge Z)]
\wedge[(X\wedge Z)\vee(Y\wedge Z)]
\wedge[(X\wedge Y)\vee(Y\wedge Z)]
=X\wedge Y\wedge Z.
\]

At

\[
(X,Y,Z)=(0,1,1),
\]

the left side is true while the right side is false.

The computation is reproduced in `boolean_audit_results.json`.

**Classification:** false.

---

## T8. Bare proper faces do not determine a filled simplex

Let

\[
K=\partial\Delta^2,
\qquad
L=\Delta^2.
\]

Both have exactly the same vertices and edges. Thus all proper faces of the 2-simplex occur in both, but only \(L\) contains the 2-simplex.

Therefore proper-face data alone cannot determine whether the parent simplex exists.

The same construction works in every dimension.

**Classification:** sound no-go theorem.

---

## T9. Exact reconstruction from a subcomplex cover

If

\[
K=\bigcup_i K_i,
\]

then \(K\) is the colimit of the diagram containing the \(K_i\), all their finite intersections, and inclusion maps.

Thus gluing is exact when the incidence/overlap diagram is retained.

**Classification:** standard categorical topology.

---

## T10. Good-cover nerve theorem gives homotopy reconstruction

If a cover \(\{U_i\}\) has all nonempty finite intersections contractible, then

\[
N(\mathcal U)\simeq \bigcup_i U_i.
\]

Hence a nerve can recover homotopy type from compatible local pieces, but not necessarily the exact combinatorial presentation.

**Classification:** standard; central reconstruction tool.

---

## T11. Simplicial unfolding maps commute with the true boundary

If

\[
u:K\to L
\]

is simplicial, then the induced chain map satisfies

\[
d_LC_*(u)=C_*(u)d_K.
\]

Therefore it induces

\[
u_*:H_n(K)\to H_n(L).
\]

This is the principled modern version of a transformation between concept complexes.

**Classification:** standard and decisive.

---

## T12. Mapping cone detects homological change

For a chain map \(U:C\to D\),

\[
H_*(\operatorname{Cone}U)=0
\]

iff \(U\) is a quasi-isomorphism.

For an inclusion \(K\hookrightarrow L\),

\[
H_n(\operatorname{Cone}U)\cong H_n(L,K).
\]

Thus cone homology is a precise measure of topological change across an unfolding/refinement map.

**Classification:** standard; strong application to the thesis program.

---

## C5. Cycles are not symmetry

A filled triangle \(\Delta^2\) has

\[
\operatorname{Aut}(\Delta^2)\cong S_3
\]

but

\[
H_1(\Delta^2)=0.
\]

So strong symmetry can occur without nontrivial 1-homology.

**Classification of "cycle = symmetry": false.**

---

## C6. A nontrivial cycle need not have nontrivial symmetry

Consider the graph with triangle

\[
a-b-c-a
\]

plus one leaf at \(a\) and a length-two path at \(b\). It has

\[
\beta_1=1
\]

but trivial automorphism group.

The script checks all vertex permutations and finds exactly one automorphism, the identity.

Thus nontrivial homology does not imply symmetry.

---

## T13. Observation refinement is naturally an equivalence-relation refinement

Let \(q_k:X\to O_k\) be an observation map. Define

\[
x\sim_k y\iff q_k(x)=q_k(y).
\]

Then "greater differentiation" can be formalized as

\[
\sim_{k+1}\subseteq\sim_k.
\]

Equivalently, every fine observational class lies in a coarse class.

This is a minimal, representation-independent formalization of Matte-Blanco-style distinguishing.

**Classification:** sound definition; promising modeling axis.

---

## T14. Group-theoretic symmetry breaking under observation

Suppose \(G\curvearrowright X\). Define the observation-preserving subgroup

\[
G_q=\{g\in G:q(gx)=q(x)\text{ for all }x\}.
\]

If \(q'\) is finer than \(q\), then in many natural compatible refinement systems one expects

\[
G_{q'}\le G_q.
\]

This is a mathematically meaningful symmetry-breaking statement. The inclusion requires compatibility assumptions on the action and observation maps and should be proved in the chosen model rather than asserted universally.

**Classification:** promising theorem schema.

---

## T15. Contiguous refinement choices induce the same homology map

If two simplicial refinement maps

\[
f,g:K\to L
\]

are contiguous, then their geometric realizations are homotopic and

\[
f_*=g_*:H_n(K)\to H_n(L).
\]

This is the correct mechanism for obtaining canonical homological behavior from noncanonical cover-refinement choices.

**Classification:** standard; likely essential to the strongest next theorem.

---

# Summary ledger

| ID | Statement | Status |
|---|---|---|
| T1 | fixed-factor unfolding is exact-one-false | sound |
| T2 | unfolding is not invariant under logical equivalence | sound negative theorem |
| T3 | one-step operator is gated Boolean derivative | sound |
| T4 | exact-layer Boolean-lattice unfolding | sound repair |
| C1 | original unfolding is a chain boundary | false |
| T5 | unsigned incidence square is twice rank-two incidence | sound |
| T6 | characteristic-two / signed incidence is square-zero | sound/standard |
| C2 | thesis printed second iterate is exact rank-two layer | false |
| T7 | relational unfolding has a right adjoint | sound/standard |
| C3 | universal inverse exists | false |
| C4 | thesis Boolean gluing identity | false |
| T8 | bare proper faces do not determine filler | sound no-go |
| T9 | subcomplex cover reconstructs by colimit | sound/standard |
| T10 | good cover nerve recovers homotopy type | sound/standard |
| T11 | simplicial unfolding induces a chain map | sound/standard |
| T12 | cone homology detects quasi-isomorphism/relative change | sound/standard |
| C5 | symmetry implies homological cycle | false |
| C6 | homological cycle implies symmetry | false |
| T13 | distinction as refinement of observational equivalence | sound definition |
| T14 | symmetry breaking via observation-preserving subgroup | promising schema |
| T15 | contiguity removes refinement-choice ambiguity on homology | sound/standard |
