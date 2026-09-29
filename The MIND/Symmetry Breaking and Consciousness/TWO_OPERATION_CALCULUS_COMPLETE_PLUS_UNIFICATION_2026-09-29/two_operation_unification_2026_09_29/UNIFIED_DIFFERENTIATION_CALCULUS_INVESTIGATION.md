# Unified Differentiation Calculus Investigation

**Project:** Refinement, conditioning, constrained observation design, and adaptive protocols  
**Date:** 29 September 2026  
**Status:** exploratory theorem program with bounded exhaustive verification; novelty not claimed without a dedicated priority audit.

## 1. Executive finding

There is a clean unification, and it is stronger than treating pre-\(T_0\) splitting and post-\(T_0\) thinning as separate regimes.

The correct carrier-level object is the **observation specialization preorder** on the surviving worlds:

\[
x\preceq_{\Phi,S} y
\quad\Longleftrightarrow\quad
x,y\in S\ \text{and}\ \phi(x)\le \phi(y)\ \text{for every }\phi\in\Phi.
\]

Equivalently, if \(o_\Phi(x)\in\{0,1\}^{\Phi}\) is the observation signature,

\[
x\preceq_{\Phi,S}y
\iff
o_\Phi(x)\le o_\Phi(y)
\]

coordinatewise.

Adding an observation never performs two fundamentally different operations at this level. It simply **thins the preorder**:

\[
\preceq_{\Phi\cup\Theta,S}
=
\preceq_{\Phi,S}\cap \preceq_{\Theta,S}.
\]

Conditioning to \(T\subseteq S\) simply takes the induced subpreorder:

\[
\preceq_{\Phi,T}
=
\preceq_{\Phi,S}\cap(T\times T).
\]

Hence fixed refinement and fixed conditioning commute strictly on the world-level preorder.

The familiar phase transition at \(T_0\) appears only after quotienting the preorder by observational equivalence:

\[
x\equiv_\Phi y
\iff
x\preceq_\Phi y\ \text{and}\ y\preceq_\Phi x
\iff
o_\Phi(x)=o_\Phi(y).
\]

Before \(T_0\), thinning may delete one or both directions between two equivalent worlds and thereby **split a quotient point**. After \(T_0\), no nontrivial symmetric pair remains, so further refinement can only delete strict comparabilities: **order thinning**.

This gives one mechanism with two quotient-level manifestations.

The strongest structural extension found in this investigation is a canonical factorization of every finite refinement into:

1. **fiber expansion** of coarse observational states; followed by
2. **descent thinning** of the resulting order.

Support conditioning fits into a commuting refinement--conditioning prism. The only non-cartesian face is the fiber-expansion face, and its failure is exactly a saturation/measurement-availability obstruction. After relative \(T_0\), that obstruction vanishes automatically, recovering the existing post-\(T_0\) bifiltration.

---

## 2. Unified carrier-level calculus

Let \(\Omega\) be a finite world/valuation carrier, \(S\subseteq\Omega\) the current support, and \(\Phi\) a finite family of Boolean observations.

For one observation \(\theta\), define its two-level preorder

\[
x\preceq_\theta y
\iff
\theta(x)\le\theta(y).
\]

Then

\[
\preceq_{\Phi,S}
=
(S\times S)\cap\bigcap_{\phi\in\Phi}\preceq_\phi.
\]

### U1. Unified preorder-thinning theorem

For \(\Phi\subseteq\Psi\) and \(T\subseteq S\),

\[
\preceq_{\Psi,S}\subseteq\preceq_{\Phi,S},
\qquad
\preceq_{\Phi,T}=\preceq_{\Phi,S}\cap(T\times T),
\]

and

\[
\preceq_{\Psi,T}
=
\preceq_{\Psi,S}\cap(T\times T)
=
\bigl(\preceq_{\Phi,S}\cap(T\times T)\bigr)
\cap \preceq_{\Psi\setminus\Phi,T}.
\]

**Proof.** Coordinatewise inclusion under a larger observation family adds inequalities that must be satisfied; hence relations can only be deleted. Restricting the world set deletes vertices and all incident ordered pairs. Intersections of binary relations are associative and commutative. \(\square\)

### Interpretation

- **Pre-\(T_0\) splitting** = deletion of symmetric relations inside an old equivalence class.
- **Post-\(T_0\) thinning** = deletion of asymmetric/strict relations between already distinct states.
- **Conditioning** = vertex deletion in the same preorder.

This is the cleanest single calculus found in the investigation.

### A globally monotone relation count

Define

\[
C(S,\Phi)
=
|\{(x,y)\in S^2:x\neq y,\ x\preceq_\Phi y\}|.
\]

Then \(C\) is nonincreasing under both observation refinement and support restriction. It remains informative on both sides of the \(T_0\) boundary, unlike the partition ambiguity \(A_2\), which becomes zero at \(T_0\).

For interpretation it is better to retain two components:

\[
A_{\rm eq}(S,\Phi)
=
\sum_{C\in S/\!\equiv_\Phi}{|C|\choose2},
\]

which counts indistinguishable unordered pairs, and the residual directed-comparability data of \(\preceq_\Phi\). Refinement can convert an indistinguishable pair into a one-way comparable pair or an incomparable pair; after \(T_0\), only the latter order-thinning mechanism remains.

---

## 3. Quotient layer and the \(T_0\) phase transition

Let

\[
P_{\Phi,S}=S/{\equiv_\Phi}\cong o_\Phi(S)
\]

with the induced coordinatewise order. This is the realized-signature poset / Kolmogorov quotient.

### U2. Quotient interpretation theorem

The passage

\[
(S,\preceq_{\Phi,S})\longmapsto P_{\Phi,S}
\]

turns a single relation-thinning operation into two visible effects:

1. if \(\equiv_\Phi\) strictly refines, quotient vertices split;
2. among the resulting quotient vertices, some old comparabilities can disappear.

The state is relatively \(T_0\) on \(S\) iff \(\equiv_\Phi\) is equality on \(S\), equivalently iff \(o_\Phi|_S\) is injective. At such a state, later refinement cannot split quotient vertices.

### Important consequence for adaptive protocols

\(T_0\) should be treated **branch-locally**. A global interface may fail to be \(T_0\) on \(\Omega\), while after several outcomes the restricted interface can already be \(T_0\) on the surviving support \(S_h\). From that node onward, no further observation can increase Boolean distinguishability among the surviving worlds; further refinement can only alter the positive observation order/topology.

This produces a natural **branch-local \(T_0\) frontier** in an adaptive decision tree.

---

## 4. Canonical factorization: fiber expansion followed by descent thinning

Let \(\Psi=(\Phi,\Theta)\) where \(\Theta\) is a block of new Boolean observations. Write

\[
P=P_{\Phi,S}.
\]

For each coarse signature \(p\in P\), let

\[
C_p=\{x\in S:o_\Phi(x)=p\}
\]

and define the new-coordinate fiber profile

\[
B_p
=
\{\alpha_\Theta(x):x\in C_p\}
\subseteq\{0,1\}^{\Theta}.
\]

The refined signature poset is

\[
Q=P_{\Psi,S}
\cong
\{(p,a):p\in P,\ a\in B_p\},
\]

with

\[
(p,a)\le_Q(q,b)
\iff
p\le_P q\ \text{and}\ a\le b.
\]

Now define the **fiber-expansion poset**

\[
F=\sum_{p\in P} B_p,
\]

the lexicographic sum of the fiber-profile posets over \(P\). Explicitly,

\[
(p,a)\le_F(q,b)
\iff
\begin{cases}
a\le b,&p=q,\\
\text{true},&p<q,\\
\text{false},&p\parallel q.
\end{cases}
\]

### U3. Canonical refinement factorization theorem

There is a canonical factorization

\[
Q\xhookrightarrow{\;j\;}F\xrightarrow{\;\pi\;}P,
\]

where:

- \(j\) is identity on vertices and deletes exactly the cross-fiber comparisons for which the new labels fail \(a\le b\);
- \(\pi(p,a)=p\) is a surjective monotone projection;
- the ordinary refinement projection \(r:Q\to P\) satisfies
  \[
  r=\pi\circ j.
  \]

**Proof.** \(Q\) and \(F\) have the same vertex set. Every relation in \(Q\) is a relation in \(F\): for \(p=q\) both use the fiber order; for \(p<q\), \(F\) keeps every cross-fiber pair while \(Q\) keeps only those with \(a\le b\). Projection to \(p\) is therefore monotone and surjective. \(\square\)

### Why this matters

This factorization precisely separates the two quotient-level mechanisms:

- \(F\to P\): **fiber expansion / point splitting**;
- \(Q\hookrightarrow F\): **descent thinning**.

If the coarse state is \(T_0\) on \(S\), every coarse class \(C_p\) is a singleton, so every \(B_p\) is a singleton and \(F\cong P\). The expansion stage disappears and the refinement is exactly same-vertex order thinning.

If there are no incompatible cross-fiber labels, then \(Q=F\) and the refinement is pure fiber expansion.

The standard object \(F\) is a lexicographic sum of posets; what is project-specific here is using it as the canonical intermediate object for the ProLT fiber-profile refinement.

---

## 5. Homological decomposition of a general refinement

Apply the order-complex functor and simplicial chains:

\[
\Delta Q\xrightarrow{\Delta j}\Delta F\xrightarrow{\Delta\pi}\Delta P.
\]

Let

\[
D^{\rm thin}_*=H_*\operatorname{Cone}(C_*(\Delta j)),
\]

\[
D^{\rm exp}_*=H_*\operatorname{Cone}(C_*(\Delta\pi)),
\]

and

\[
D^{\rm tot}_*=H_*\operatorname{Cone}(C_*(\Delta r)).
\]

Because \(j\) is a simplicial inclusion,

\[
D^{\rm thin}_*\cong H_*(\Delta F,\Delta Q)
\]

up to the standard cone/relative indexing convention.

### U4. Cone decomposition / octahedral sequence

The standard mapping-cone triangle for composable chain maps yields

\[
\operatorname{Cone}(j)
\longrightarrow
\operatorname{Cone}(r)
\longrightarrow
\operatorname{Cone}(\pi)
\longrightarrow
\operatorname{Cone}(j)[1],
\]

and hence a long exact sequence

\[
\cdots\to
D^{\rm thin}_k
\to
D^{\rm tot}_k
\to
D^{\rm exp}_k
\to
D^{\rm thin}_{k-1}
\to\cdots.
\]

This is a standard homological-algebra construction applied to the canonical ProLT factorization. It gives a principled way to separate and then recombine splitting and thinning defects.

### Post-\(T_0\) recovery

After \(T_0\), \(F\cong P\), so \(D^{\rm exp}=0\) and

\[
D^{\rm tot}\cong D^{\rm thin}\cong H_*(\Delta P,\Delta Q),
\]

recovering the existing post-\(T_0\)/non-splitting relative-homology picture.

---

## 6. Conditioning prism and the exact interaction criterion

Let \(T\subseteq S\). Construct the coarse, expansion, and refined posets at both supports:

\[
Q_T\hookrightarrow F_T\to P_T,
\]

\[
Q_S\hookrightarrow F_S\to P_S.
\]

Support inclusion gives a commuting prism

\[
\begin{array}{ccccc}
Q_T&\hookrightarrow&F_T&\to&P_T\\
\downarrow&&\downarrow&&\downarrow\\
Q_S&\hookrightarrow&F_S&\to&P_S.
\end{array}
\]

For \(p\in P_T\), write \(B_p^S\) and \(B_p^T\) for the fine label profiles realized before and after conditioning.

### U5. Cartesian fiber-saturation theorem

The right-hand expansion square

\[
\begin{array}{ccc}
F_T&\to&P_T\\
\downarrow&&\downarrow\\
F_S&\to&P_S
\end{array}
\]

is a pullback in finite posets iff

\[
B_p^T=B_p^S
\qquad\text{for every }p\in P_T.
\]

Equivalently: whenever the conditioned support still touches a coarse observational class, it must still realize **every refined signature** that was present over that coarse class.

The left-hand thinning square is always a pullback: it is simply restriction of the same-vertex suborder \(Q_S\subseteq F_S\) to the surviving fine-signature vertices.

### Fiber-completion defect

Define

\[
\mathfrak D_{\rm fib}(T\mid S;\Psi/\Phi)
=
\pi^{-1}(P_T)\setminus F_T.
\]

Its cardinality is

\[
d_{\rm fib}
=
\sum_{p\in P_T}
\bigl(|B_p^S|-|B_p^T|\bigr).
\]

It vanishes exactly when the expansion square is cartesian.

A topological version is available because

\[
F_T\subseteq \pi^{-1}(P_T):
\]

\[
D^{\rm fib}_k
:=
H_k\bigl(\Delta\pi^{-1}(P_T),\Delta F_T\bigr).
\]

This distinguishes exact cartesian failure from its weaker homological effect.

---

## 7. Measurement availability becomes a cartesianity theorem

Let \(E\subseteq S\) be an outcome event and \(T=E\). Let

\[
\mathcal A_{\Phi,S}
\]

be the Boolean algebra generated by the current observation-signature cells on \(S\). Thus \(E\in\mathcal A_{\Phi,S}\) iff \(E\) is a union of coarse signature fibers.

Assume the outcome is available after refinement:

\[
E\in\mathcal A_{\Psi,S}.
\]

### U6. Newly-enabled measurement / non-cartesianity theorem

Under the above assumption, the following are equivalent:

1. \(E\in\mathcal A_{\Phi,S}\) (the measurement was already available);
2. the expansion-conditioning square is cartesian;
3. \(d_{\rm fib}=0\).

Consequently,

\[
E\in\mathcal A_{\Psi,S}\setminus\mathcal A_{\Phi,S}
\]

iff the expansion-conditioning square is non-cartesian.

**Proof.** Since \(E\) is fine-measurable, it contains either all or none of every fine-signature class. The cartesian condition says that if \(E\) meets a coarse class, it retains all fine classes over that coarse class. Together these say precisely that \(E\) contains either all or none of each coarse class, which is coarse measurability. \(\square\)

This gives a precise categorical version of the earlier "measurement enabled by refinement" idea. It is not quantum noncommutativity. It is failure of saturation with respect to the coarser quotient.

After relative \(T_0\), every coarse class is a singleton, \(\mathcal A_{\Phi,S}=2^S\), and this obstruction disappears.

---

## 8. Worked four-world example: splitting, thinning, and conditioning in one diagram

Let

\[
\Omega=\{00,01,10,11\},
\qquad
\Phi=\{X\},
\qquad
\Theta=\{Y\}.
\]

The coarse quotient has two states

\[
P_X=\{X=0<X=1\},
\]

each representing two worlds.

Within each coarse state, the new \(Y\)-profile is \(B_p=\{0<1\}\). The fiber-expansion poset is the lexicographic sum of two 2-chains, hence a 4-chain:

\[
(0,0)<(0,1)<(1,0)<(1,1).
\]

The actual refined signature order requires both \(X\) and \(Y\) to be nondecreasing. Therefore the relation

\[
(0,1)<(1,0)
\]

is deleted, producing the Boolean-square/diamond order on the four \((X,Y)\) signatures.

Thus this one refinement performs both:

- point splitting: two coarse states become four states;
- order thinning: one cross-fiber comparison is removed from the fiber expansion.

Now condition on \(Y=1\):

\[
T=\{01,11\}.
\]

Both coarse \(X\)-states remain represented, so the coarse quotient sees no state deletion. But only the \(Y=1\) refined state survives over each coarse state. Hence the fiber-completion defect has two missing refined states. The square is non-cartesian, exactly because \(Y=1\) was not measurable from \(X\) alone and became available only after adding \(Y\).

By contrast, conditioning on \(X=1\) is coarse-measurable. The corresponding square is cartesian.

---

## 9. Constrained observation design: one problem that contains both Test Cover and ProLT observation dimension

The carrier-preorder formulation suggests a general design problem.

Let \(R_0=\preceq_{\Phi,S}\) be the current preorder, \(\mathcal O\) an allowed pool of Boolean tests, and \(\mathcal T\) a target property or target preorder.

Choose a minimum-cost block \(\Theta\subseteq\mathcal O\) such that

\[
R_\Theta^{\rm new}
=
R_0\cap\bigcap_{\theta\in\Theta}R_\theta
\]

satisfies \(\mathcal T\), together with any required topological/homological constraints.

### Exact target-preorder realization

If \(R_1\subseteq R_0\) is any finite target preorder, then an unrestricted finite Boolean block realizing

\[
R_1
=
R_0\cap R_\Theta
\]

always exists.

One explicit construction assigns to each \(z\in S\) the coordinate

\[
\theta_z(x)=1[z\preceq_{R_1}x].
\]

Then the resulting bit-vector map order-embeds the quotient of \(R_1\) into a Boolean lattice, so its coordinate order is exactly \(R_1\). Since \(R_1\subseteq R_0\), intersecting with \(R_0\) gives \(R_1\).

This extends the post-\(T_0\) same-vertex realizability viewpoint to arbitrary finite preorder refinements.

### Unified minimum-observation number

Define

\[
\operatorname{odim}_{R_0}(R_1)
=
\min\{|\Theta|:R_1=R_0\cap R_\Theta\}.
\]

Specializations include:

- **pre-\(T_0\) separation / injectivity target:** minimum separating tests, i.e. Test Cover under a restricted pool;
- **post-\(T_0\) exact suborder target:** the relative observation-dimension direction already developed in ProLT;
- **mixed target:** simultaneous splitting of old classes and deletion of old strict relations.

The unrestricted/minimal-number theory should be compared carefully with Boolean/2-dimension, separating systems, and test-cover literature before any novelty claim.

### Topologically constrained version

The genuinely project-specific optimization is richer:

\[
\min_{\Theta\subseteq\mathcal O}
\sum_{\theta\in\Theta}c(\theta)
\]

subject to combinations of:

- target ambiguity or relative \(T_0\);
- exact/partial target preorder;
- homotopy preservation or a bounded mapping-cone defect;
- a prescribed post-\(T_0\) homology change;
- formula-language restrictions;
- CM/LM frame/compiler costs;
- robustness across a family of possible future supports.

The unconstrained separation special case is already NP-hard, so the full problem is NP-hard in general. The opportunity is exact/FPT/approximation results in ProLT-controlled regimes (bounded height, chain/tree-like coarse orders, bounded test arity/cost, bounded target defect).

---

## 10. Adaptive protocols

A deterministic adaptive protocol is a rooted decision tree. At node \(h\), retain the state

\[
\mathcal X_h=(S_h,\Phi_h).
\]

Choose a test \(\theta_h\) from the allowed pool, then execute the operational composite

\[
Q_{\theta_h=b}
=
M_{\theta_h=b}\circ R_{\theta_h}.
\]

The child state is

\[
\Phi_{hb}=\Phi_h\cup\{\theta_h\},
\qquad
S_{hb}=\{x\in S_h:\theta_h(x)=b\}.
\]

Each edge therefore has the entire unified structure above:

- preorder thinning;
- possible quotient-point splitting;
- possible descent thinning;
- support conditioning;
- fiber/cartesian defect;
- mapping-cone/topological defect.

### Branch-local stopping criterion

For pure identification, stop at node \(h\) when

\[
o_{\Phi_h}|_{S_h}
\]

is injective. Equivalently,

\[
A_{\rm eq}(S_h,\Phi_h)=0.
\]

At that point the branch has crossed its local \(T_0\) frontier.

### Bellman formulation

For worst-case query cost with optional topological penalty \(\tau\),

\[
V(S,\Phi)
=
\min_{\theta\in\mathcal O\setminus\Phi}
\left[
 c(\theta)+\tau(S,\Phi,\theta)
 +
 \max_{b:S_b\ne\varnothing}
 V(S_b,\Phi\cup\{\theta\})
\right].
\]

Expected-cost versions replace \(\max\) by an outcome-weighted expectation.

Possible \(\tau\) include:

- rank/Betti size of the refinement mapping cone;
- thinning defect \(H_*(\Delta F,\Delta Q)\);
- fiber-completion defect under likely outcome supports;
- formula/CM compilation cost;
- a penalty for crossing specified homotopy classes.

The finite state graph is acyclic after deleting redundant self-loops because \(\Phi\) only grows and \(S\) only shrinks.

### Four-world adaptive advantage

Let the worlds be \(\{a,b,c,d\}\) and available tests

\[
A=\{a,b\},\qquad B=\{a\},\qquad C=\{c\}.
\]

No pair of tests separates all four worlds, so a nonadaptive separating family needs all three.

An adaptive protocol uses only two tests on every branch:

1. query \(A\);
2. on the \(A=1\) branch query \(B\);
3. on the \(A=0\) branch query \(C\).

This is classical adaptive combinatorial search. The ProLT extension is to constrain or score each branch by its topology/order-complex transition.

The exhaustive four-world computation over all \(2^{16}=65{,}536\) pools of Boolean tests found:

- 64,152 pools permit full identification;
- 55,296 have nonadaptive optimum 2 and adaptive worst-case depth 2;
- 8,100 require 3 tests nonadaptively but only adaptive depth 2;
- 756 require depth 3 both nonadaptively and adaptively.

These counts are bounded finite evidence, not a theorem for general \(n\).

---

## 11. A joint defect object for refinement and conditioning

The existing post-\(T_0\) bifiltration records refinement and support restriction as two commuting deletion axes. A natural next invariant is not another scalar but the **total cofiber of an elementary square**.

For \(T\subseteq S\) and \(\Phi\subseteq\Psi\), consider the induced map of relative chain complexes

\[
C_*(K_{\Psi,S},K_{\Psi,T})
\longrightarrow
C_*(K_{\Phi,S},K_{\Phi,T}).
\]

Define provisionally

\[
J_*(\Psi/\Phi;T\subseteq S)
:=
H_*\operatorname{Cone}
\left(
C_*(K_{\Psi,S},K_{\Psi,T})
\to
C_*(K_{\Phi,S},K_{\Phi,T})
\right).
\]

Interpretation: \(J_*\) measures the change in the **conditioning defect** caused by refinement, equivalently the change in the **refinement defect** after restricting support. It is a candidate mixed derivative of the two-axis calculus.

This construction is standard homological algebra. The research question is whether, for ProLT-generated squares, it admits:

- a finite combinatorial description;
- a fiber-profile decomposition pre-\(T_0\);
- a deleted-cell description post-\(T_0\);
- exact low-height criteria;
- useful persistence summaries across an adaptive protocol.

That is a stronger target than merely re-proving commutativity.

---

## 12. CM/LM role in the unified theory

The structural theory above is representation-neutral. A Boolean test \(\theta\) can be supplied by a logical formula, a CM/LM object, or any equivalent truth function.

For CM/LM integration, keep three types distinct:

1. compact operator encoding \([\theta]\);
2. truth region/event \(E_\theta\subseteq\Omega\);
3. diagonal valuation effect/projector \(D_\theta\).

Then:

- **refinement** uses \(\theta\) as a new coordinate in the signature/preorder;
- **measurement** uses \(E_{\theta=b}\) or \(D_{\theta=b}\) to restrict the support;
- **design cost** may use formula complexity, frame transport, compiler cost, or allowed CM/LM operator classes.

Thus CM contributes a typed source of tests and effects, but the basic adaptive/query mathematics is not uniquely CM.

---

## 13. Relation to known mathematics and novelty discipline

Several layers are standard or close to standard:

- finite topologies are equivalent to specialization preorders, and \(T_0\) finite spaces correspond to posets;
- observational equivalence/attribute indiscernibility is standard in rough-set/information-system theory;
- saturated subsets of a quotient are unions of quotient fibers;
- lexicographic sums of posets are standard;
- mapping-cone/octrahedral relations are standard homological algebra;
- public-announcement and dynamic epistemic logics already model information updates by model restriction and more general action/product updates;
- formal-concept attribute exploration already studies interactive knowledge acquisition by queries;
- minimum test cover and adaptive combinatorial search already study static and adaptive separation strategies.

Therefore none of those ingredients should be claimed as new.

The most plausible project-specific contribution candidates are narrower:

1. the **canonical fiber-expansion / descent-thinning factorization** of ProLT observation refinement;
2. the **conditioning prism** and exact localization of non-cartesianity to the fiber-expansion face;
3. the **measurement-availability/cartesianity equivalence** for fine-measurable outcomes;
4. the mapping-cone decomposition of the project refinement defect into expansion and thinning pieces;
5. a **mixed joint-defect invariant** specialized to ProLT refinement/conditioning squares;
6. **constrained and adaptive observation design with ProLT topological/homological admissibility**, rather than ordinary separation alone;
7. branch-local \(T_0\) phase transitions in adaptive protocols, with topology continuing to evolve after Boolean distinguishability saturates.

Items 1--4 are mathematically clean enough for a focused theorem note, but their novelty must be checked against finite-space, poset-fibration, rough-set, and categorical data-refinement literatures. Item 6 has the best chance of yielding genuinely new optimization/combinatorial results because it combines classical separation with the project-specific ProLT defect constraints.

---

## 14. Exhaustive finite verification performed here

Three independent bounded checks were added.

### A. Preorder-transition census on four worlds

All \(355\) observation-generated finite preorders/topologies on four labelled worlds were reconstructed. Of these, \(219\) are \(T_0\), agreeing with the known count of labelled four-point posets/T0 finite topologies.

Across all \(355\times16=5{,}680\) one-observation transitions:

| regime | transition type | count |
|---|---:|---:|
| pre-\(T_0\) | redundant | 660 |
| pre-\(T_0\) | splitting only | 578 |
| pre-\(T_0\) | thinning only | 338 |
| pre-\(T_0\) | both splitting and thinning | 600 |
| \(T_0\) | redundant | 1,678 |
| \(T_0\) | thinning only | 1,826 |

This directly confirms that pre-\(T_0\) is not synonymous with "splitting only": splitting and order thinning can occur simultaneously.

### B. Cartesian/saturation census

Across all 15 partitions of four worlds, all 16 one-bit refinements, and all 16 outcome events (3,840 cases), the fine-measurable-event theorem had **zero failures**:

\[
E\text{ fine measurable}
\quad\Longrightarrow\quad
\bigl(E\text{ coarse measurable}\iff d_{\rm fib}=0\bigr).
\]

The classification counts were:

- coarse measurable, fine measurable, cartesian: 1,504;
- newly fine-measurable, non-cartesian: 844;
- not fine-measurable, non-cartesian: 360;
- not fine-measurable, cartesian at the image level: 1,132.

The last class is why the fine-measurability hypothesis is essential.

### C. Adaptive/nonadaptive separation census

Across all 65,536 four-world Boolean-test pools, 64,152 permit full identification. Of these, 8,100 exhibit a strict adaptive advantage: nonadaptive optimum 3, adaptive worst-case depth 2.

---

## 15. Recommended theorem/research sequence

### Phase U1 — freeze the unified preorder model

Prove and write cleanly:

1. observation families as intersections of two-level preorders;
2. conditioning as induced-subpreorder restriction;
3. relative \(T_0\) as antisymmetry/injective signature on current support;
4. quotient-point splitting and order thinning as two quotient-level faces of one preorder deletion operation.

### Phase U2 — prove the canonical factorization

5. fiber-profile lexicographic expansion \(F\);
6. same-vertex descent thinning \(Q\subseteq F\);
7. exact characterization of when each stage is trivial;
8. mapping-cone octahedral sequence.

### Phase U3 — integrate conditioning

9. refinement--conditioning prism;
10. cartesian fiber-saturation criterion;
11. measurement-availability/cartesianity theorem;
12. fiber-completion defect and its relative homology.

### Phase U4 — constrained design

13. generalized relative observation dimension for preorders;
14. exact complexity inheritance from Test Cover;
15. tractable/FPT regimes using ProLT chain/height-two/tree-like theorems;
16. robustness across multiple possible supports/outcomes.

### Phase U5 — adaptive protocols

17. protocol state DAG and Bellman recurrence;
18. branch-local \(T_0\) frontier theorem;
19. adaptive/nonadaptive gap under ProLT constraints;
20. joint defect accumulated along paths or represented on the protocol tree.

### Phase U6 — novelty gate

Run a dedicated theorem-level audit against:

- finite Alexandrov/preorder topology;
- lexicographic sums and poset substitution;
- rough-set dynamic information systems;
- formal concept analysis / attribute exploration;
- dynamic epistemic logic and action models;
- separating systems, Test Cover, adaptive combinatorial search;
- multiparameter persistence and total cofibers of squares.

Do not draft a broad consciousness paper before this gate.

---

## 16. Overall conclusion

**Yes, the five strands can be unified.** The cleanest hierarchy is:

\[
\boxed{
\text{world-level preorder thinning}
\longrightarrow
\text{quotient fiber expansion + order thinning}
\longrightarrow
\text{conditioning prism}
\longrightarrow
\text{constrained design}
\longrightarrow
\text{adaptive protocol tree}
}
\]

The key conceptual improvement is that the pre-/post-\(T_0\) distinction is not two unrelated refinement operations. It is a phase transition in the **quotient presentation** of one monotone relation-deletion process.

The strongest immediate research target is the canonical factorization plus conditioning prism. The strongest longer-term target is **adaptive observation design subject to ProLT topological/homological constraints**, because classical test-cover and decision-tree theory handles ordinary distinguishability, while the ProLT geometry supplies an additional structure not present in the standard problem.
