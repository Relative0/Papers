# CM/LM Operator-DAG Attack: Exact Read-Once Rank Recursion

**Phase 4 — 29 September 2026**

## 1. Boundary discovered by the attack

For a single-output operator DAG, genuine sharing of a nonconstant subexpression causes repeated variable support. The clean direct-factor theorem therefore lives on the support-decomposable/read-once subclass: every binary node has children with disjoint variable supports. For a single output, this is naturally a **read-once operator tree** modulo harmless sharing of constants/unary metadata.

This is not a weakness of the theorem statement; it isolates exactly the point at which DAG reuse introduces the cancellation/duplication phenomena that generic Boolean decomposition algorithms must handle.

---

## 2. Class

A **typed read-once CM/LM operator tree** has:

- one distinct Boolean attribute at each leaf;
- a binary Boolean connective \(\Theta\) at every internal node;
- no attribute appearing in two different leaf positions;
- every internal connective **essential in both inputs**.

For the theorem below, each connective is represented by its \(2\times2\) correspondence matrix \([\Theta]\) over \(\mathbb F_2\).

The essentiality assumption guarantees that each internal subfunction is nonconstant and depends on every leaf below it.

Because signed conjunctions arise, factor extraction must sometimes recurse on a complemented child function. Define

\[
\operatorname{PF}(u,\epsilon),\qquad \epsilon\in\{0,1\},
\]

to mean the semantic prime AND-factor partition of \(f_u\) when \(\epsilon=0\), and of \(\neg f_u\) when \(\epsilon=1\).

---

## 3. Rank dichotomy for essential binary connectives

There are ten Boolean binary connectives essential in both inputs.

Under ordinary \(\mathbb F_2\) matrix rank:

- **four** have rank one; these are exactly the four signed conjunctions
  \[
  X\wedge Y,
  \quad X\wedge\neg Y,
  \quad \neg X\wedge Y,
  \quad \neg X\wedge\neg Y;
  \]
- **six** have rank two (XOR/XNOR, OR/NAND, and the two directional implication-type pairs in suitable polarity conventions).

Complementing the output may move a connective from one side of this dichotomy to the other, so the recursion must use \([\Theta]\) or its entrywise complement according to \(\epsilon\).

---

## 4. Main operator-tree theorem

### Theorem 4.1 — CM-rank prime-factor recursion

Let an internal node \(u\) compute

\[
f_u=\Theta(g,h),
\]

where the supports \(A=\operatorname{supp}(g)\) and \(B=\operatorname{supp}(h)\) are disjoint. For requested output polarity \(\epsilon\), let

\[
M_u^{(\epsilon)}=
\begin{cases}
[\Theta],&\epsilon=0,\\
\neg[\Theta],&\epsilon=1,
\end{cases}
\]

where \(\neg\) is entrywise Boolean complement.

Then:

### Case I: rank two

If

\[
\operatorname{rank}_{\mathbb F_2}M_u^{(\epsilon)}=2,
\]

then every variable in \(A\cup B\) belongs to the same semantic prime factor block of the requested function. Hence

\[
\operatorname{PF}(u,\epsilon)=\{A\cup B\}.
\]

### Case II: rank one

If

\[
\operatorname{rank}_{\mathbb F_2}M_u^{(\epsilon)}=1,
\]

then, because the gate is essential in both inputs, the matrix contains a single `1`. Therefore there are signs \(\sigma,\tau\in\{0,1\}\) such that

\[
\Theta^{(\epsilon)}(g,h)
=
 g^{(\sigma)}\wedge h^{(\tau)},
\]

where \(q^{(0)}=q\) and \(q^{(1)}=\neg q\). Consequently

\[
\operatorname{PF}(u,\epsilon)
=
\operatorname{PF}(g,\sigma)
\cup
\operatorname{PF}(h,\tau).
\]

At a leaf \(x\), both \(x\) and \(\neg x\) have prime partition \(\{\{x\}\}\).

This recursion computes the exact semantic prime AND-factor partition.

---

## 5. Proof of the rank-two case

Two lemmas do the work.

### Lemma 5.1 — every descendant variable is essential

In a read-once tree of essential gates, every leaf variable below a node is essential in that node's Boolean function.

**Reason.** Induct upward. If a variable can toggle the left child output, essentiality of the parent gate in its left input supplies a value of the right child output for which that toggle changes the parent output. The right child is nonconstant on disjoint variables, so the required output value is attainable. The right side is symmetric.

### Lemma 5.2 — every cross pair has a rank-two local slice

Take any \(x\in A\) and \(y\in B\). By Lemma 5.1, fix all other variables under \(g\) so that toggling \(x\) toggles \(g\); do the same for \(y\) and \(h\). On that fixed context, the four values of the requested function as \((x,y)\) range over \(\{0,1\}^2\) are exactly the four entries of \(M_u^{(\epsilon)}\), up to row/column permutations.

If \(M_u^{(\epsilon)}\) has rank two, its determinant over \(\mathbb F_2\) is one, and row/column permutations preserve nonzero determinant. Hence this local \(2\times2\) slice is a nonzero four-corner CM minor.

Any disjoint AND factorization separating \(x\) from \(y\) would force the corresponding flattening to have rank at most one, so every \(2\times2\) minor would vanish. Contradiction.

Thus no valid factor partition separates any cross pair \(x\in A,y\in B\). Since every left variable is tied to every right variable, all of \(A\cup B\) lies in one prime block. ∎

---

## 6. Carrier-aware corollary

Let \(\Pi_f\) be the semantic partition returned by the recursion and \(\Pi_K\) the canonical simplicial carrier partition from minimal-nonface connectivity.

Then the exact simultaneous structured partition is

\[
\boxed{\Pi_{K,f}=\operatorname{LCC}(\Pi_K,\Pi_f).}
\]

Hence this read-once CM/LM subclass admits full exact carrier-aware factor extraction with no SAT, QBF, or truth-table expansion.

With a tree representation and standard bookkeeping, the semantic pass is linear in the operator-tree size; the partition merge is linear/nearly linear in block incidence.

---

## 7. Computational validation

`code/cm_operator_tree_factor.py` enumerates the ten essential binary connectives and compares the CM-rank recursion against exact truth-table prime factorization.

The current campaign checked:

- all 10 ordered two-variable gate trees;
- all 200 ordered three-variable read-once gate trees;
- all 5,000 ordered four-variable read-once gate trees;
- 30,000 randomly selected five-variable trees from the 140,000 gate-labelled ordered trees in that finite family.

Total: **35,210** operator trees, with **0 discrepancies**.

This is validation, not a substitute for the proof.

---

## 8. Priority boundary

Read-once Boolean functions and their recognition/factorization have a long classical literature, including cograph-based factorization for the AND/OR basis and exact identification over generalized/arbitrary bounded-fan-in bases. Therefore this phase should **not** claim discovery of efficient read-once factorization.

What is project-specific is the concise CM formulation:

- gate rank one means recurse through a signed conjunction;
- gate rank two provides an explicit four-corner minor that fuses the two child supports;
- output complement is handled by the same two-state \(\operatorname{PF}(u,\epsilon)\) recursion;
- the result plugs directly into the carrier least-common-coarsening theorem.

Whether this exact CM-rank recursion has appeared in this form requires a dedicated theorem-level priority search before any firstness claim.

---

## 9. What fails beyond the class

True DAG sharing, repeated variables, and cancellation identities destroy the local exactness of this recursion. For example, two branches can contain the same subfunction and cancel under XOR, or an OR/AND absorption can make a syntactically shared dependency semantically irrelevant.

Therefore the next extension should not simply remove the read-once hypothesis. A meaningful next class would need an explicit certificate controlling repeated support—e.g. bounded read number, deterministic shared modules, or a canonicalized CM/LM DAG with equivalence/cancellation normalization.
