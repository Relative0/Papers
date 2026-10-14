# Bounded-Width Carrier-Aware Structured Factorization

**Date:** 29 September 2026

## 1. Input contract

Let `V` be the attribute set. The carrier is represented by its minimal-nonface hypergraph
\(\mathcal N(K)\), and the semantic layer by a CNF \(\varphi\) on `V`.

Define the **combined incidence graph** \(G_{K,\varphi}\) with three kinds of vertices:

- attribute vertices \(v\in V\);
- semantic clause vertices \(C\in\varphi\);
- structural hyperedge vertices \(N\in\mathcal N(K)\).

Join an attribute to a semantic clause when it occurs in the clause, and to a structural vertex when it belongs to that minimal nonface. Signs of semantic occurrences are labels and do not alter the underlying graph. Let

\[
\tau=\operatorname{tw}(G_{K,\varphi}).
\]

The connected components of the structural minimal-nonface hypergraph are the canonical carrier join factors.

## 2. Four-corner condition

For a cut \(S\mid \bar S\), introduce two assignments \(a_0,a_1\) on \(S\) and two assignments \(b_0,b_1\) on \(\bar S\). Define

\[
D_{\varphi,S}
=
(\varphi(a_0,b_0)\wedge\varphi(a_1,b_1))
\mathbin{\Updownarrow}
(\varphi(a_0,b_1)\wedge\varphi(a_1,b_0)).
\]

The cut is an AND-factor cut exactly when \(D_{\varphi,S}\) is false for every four-corner assignment. Equivalently, the implicit CM flattening has \(\mathbb F_2\)-rank at most one.

A cut is **carrier-compatible** exactly when no minimal nonface crosses it. Equivalently, the cut is a union of carrier prime blocks.

## 3. Pair-separation QBF

For attributes \(p,q\), define `SEP(p,q)` to ask whether some valid structured cut separates them:

\[
\exists S\;[
 p\in S\wedge q\notin S
 \wedge \operatorname{CarrierClosed}(S)
 \wedge \forall a_0,a_1,b_0,b_1\;\neg D_{\varphi,S}
].
\]

For a CNF/QDIMACS implementation, membership in \(S\) is represented by existential cut-control variables. The four assignments are universal variables. Tseitin variables for the four copies of the semantic computation may be quantified existentially after them, giving a fixed three-block prefix of the schematic form

\[
\exists S\;\forall U\;\exists Z\;\Psi_{p,q}(S,U,Z).
\]

The structural constraints enforce equal cut-control bits on every minimal-nonface hyperedge (a spanning forest of each structural component suffices). A multiplexer per input selects the appropriate corner value according to the cut-control bit.

## 4. Width-lift lemma

### Lemma

If the combined incidence graph has treewidth \(\tau\), then the QBF matrix \(\Psi_{p,q}\) can be constructed with incidence treewidth \(O(\tau)\).

### Proof sketch

Start from a tree decomposition of \(G_{K,\varphi}\). Replace each attribute occurrence in a bag by a constant number of local copies: its cut bit, its two left/right assignment copies, and the constant-size multiplexer auxiliaries. Replace each semantic clause by four corner copies and constant-size gate auxiliaries. Structural minimal-nonface vertices receive only constant-size compatibility gadgets. Every original incidence edge is therefore replaced by a constant-size local gadget whose vertices can be inserted into the bags containing that edge, with at most a constant-factor bag expansion. The final rank-defect XOR/AND gadget is constant size and can be attached at the root/output bags. Hence the new width is at most \(c(\tau+1)-1\) for an absolute constant \(c\).

The exact constant depends on the chosen Tseitin encoding and is not the conceptual point; the parameter is preserved up to a constant factor.

## 5. Main FPT theorem

### Theorem (carrier-aware bounded-incidence-width factorization)

For a simplicial carrier supplied by minimal nonfaces and a CNF semantic layer, the canonical finest simultaneous carrier/semantic AND-factor partition is computable in

\[
F(\tau)\,\operatorname{poly}(|K|+|\varphi|)
\]

time, where \(\tau=\operatorname{tw}(G_{K,\varphi})\).

### Proof

For every pair \(p,q\in V\), decide `SEP(p,q)` using the fixed-alternation QBF above. The QBF has bounded incidence treewidth as a function of \(\tau\). Known bounded-treewidth QBF algorithms therefore decide each query in FPT time for the fixed number of quantifier blocks.

Define

\[
p\equiv q \quad\Longleftrightarrow\quad \neg\operatorname{SEP}(p,q).
\]

Let \(\Pi_*\) be the canonical finest simultaneous factor partition.

- If \(p,q\) lie in the same block of \(\Pi_*\), no valid factor partition can separate them, because every valid partition is a coarsening of \(\Pi_*\).
- If they lie in different blocks, regroup the blocks of \(\Pi_*\) into a bipartition placing the block of \(p\) on one side and that of \(q\) on the other. Regrouping preserves both join and Cartesian/AND products, so a valid structured cut separates them.

Thus the equivalence classes of \(\equiv\) are exactly the blocks of \(\Pi_*\). At most \(O(|V|^2)\) pair queries are required, which preserves fixed-parameter tractability.

## 6. What this theorem does and does not establish

This is a useful **carrier-aware synthesis theorem**, but the current priority evidence does **not** support claiming the bounded-width algorithmic mechanism as fundamentally new. QBF-based Boolean bi-decomposition with unknown variable partitions dates at least to Chen--Janota--Marques-Silva (2012), SAT-based bi-decomposition earlier to Lee--Jiang--Hung (2008), and bounded-treewidth/fixed-alternation QBF is already FPT in the knowledge-compilation literature.

The mathematically specific contribution of the present program is therefore the alignment of:

1. the canonical simplicial carrier partition;
2. the CM four-corner/rank-one certificate;
3. carrier-constrained cut variables;
4. exact recovery of the *simultaneous* finest partition.

A publication claim should be framed as a synthesis/application unless a more specialized complexity bound, lower bound, or representation advantage survives a dedicated priority audit.

## 7. Lower-bound boundary

The carrier block count \(k=|\Pi_K|\) alone is not a useful FPT parameter for general CNF: the previous phase established coNP-hardness already for \(k=2\). Thus bounded **semantic/combined interaction width**, rather than merely a small number of carrier components, is essential to the tractability theorem.
