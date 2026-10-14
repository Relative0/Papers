# Structured d-DNNF / SDD Direct Extraction Attack

**Phase 4 — 29 September 2026**

## 1. Result in one sentence

The unrestricted structured-d-DNNF route does **not** currently yield a clean polynomial direct-extraction theorem, but a strong exact result survives for **compressed SDDs**: at a vtree split, disjoint AND-factorability is visible directly from the compressed decision node, and the finest factorization whose blocks are vtree subtrees can be extracted by a purely structural recursion.

This is useful, but alignment with the vtree is essential. Exhaustive four-variable computation shows that a fixed balanced vtree can hide many genuine cross-vtree prime factors.

---

## 2. Why the attack narrows from structured d-DNNF to compressed SDD

A structured d-DNNF gives decomposable AND gates and deterministic OR gates, but it is not canonical and its OR structure need not expose equal cofactors syntactically. The tempting routes based on complementing, disjoining, or existentially projecting the compiled circuit are not benign in general: current knowledge-compilation results show that structured d-DNNF is not polynomially closed under negation, disjunction, or existential quantification.

Therefore this phase does **not** assert:

> every finest Cartesian/AND factor partition can be read from an arbitrary structured d-DNNF in polynomial time.

That remains unproved here.

A compressed SDD is stronger. At a declared vtree split \(X\mid Y\), its decision decomposition is

\[
f(X,Y)=\bigvee_{i=1}^{m}\bigl(p_i(X)\wedge s_i(Y)\bigr),
\]

where the primes \(p_i\) are mutually exclusive, exhaustive, and nonfalse, and compression makes the subs \(s_i\) pairwise distinct.

This makes the relevant cofactor structure explicit.

---

## 3. Vtree-cut factor theorem

### Theorem 3.1 — compressed-SDD cut criterion

Let

\[
f(X,Y)=\bigvee_{i=1}^{m} p_i(X)\wedge s_i(Y)
\]

be the compressed \((X,Y)\)-partition represented at an SDD decision node. Assume \(f\not\equiv 0\). Then the following are equivalent:

1. \(f\) is disjoint-AND separable across \(X\mid Y\):
   \[
   f(X,Y)=g(X)\wedge h(Y);
   \]
2. every nonfalse sub \(s_i\) is equivalent to the same function \(h\);
3. because the partition is compressed, there is **at most one nonfalse sub element**.

If the unique nonfalse sub is \(h\), then

\[
g=\bigvee_{i:s_i=h} p_i.
\]

In a compressed partition the equal-sub primes have already been merged, so \(g\) is the prime paired with the unique nonfalse sub.

### Proof

For any assignment \(x\) of \(X\), exactly one prime \(p_i\) is true. Therefore the right cofactor

\[
f_x(Y):=f(x,Y)
\]

is exactly the corresponding sub \(s_i(Y)\).

If \(f=g(X)\wedge h(Y)\), then for every \(x\),

\[
f_x=\begin{cases}
0,&g(x)=0,\\
h,&g(x)=1.
\end{cases}
\]

Thus all nonzero cofactors are the same function \(h\), hence every nonfalse sub is equivalent to \(h\).

Conversely, if every nonfalse sub is the same \(h\), let \(g\) be the disjunction of the primes paired with \(h\). The prime partition then gives exactly \(f=g\wedge h\). Compression turns the semantic equality of nonfalse subs into the syntactic statement that at most one nonfalse sub remains. ∎

### CM interpretation

The rows of the \(X\mid Y\) correspondence flattening are precisely the right cofactors. Over \(\mathbb F_2\), rank at most one means every nonzero row is identical. Hence Theorem 3.1 is the compressed-SDD form of the project's CM rank-one criterion.

---

## 4. Direct extraction along the vtree

Call a factor partition **\(T\)-laminar** if every factor block is the leaf set of a subtree of the vtree \(T\).

### Theorem 4.1 — finest \(T\)-laminar factorization

Given a complete compressed SDD for a nonfalse Boolean function \(f\), respecting a vtree \(T\), the unique finest \(T\)-laminar disjoint-AND factor partition can be extracted recursively:

1. at a leaf, return that variable;
2. at an internal vtree node \(v\) with split \(L\mid R\), inspect the compressed decision partition;
3. if more than one nonfalse sub occurs, return the whole leaf set of \(v\) as one block;
4. if at most one nonfalse sub occurs, obtain the left factor from its prime and the right factor from its sub, and recurse on the two child vtrees;
5. a constant-true side is a free cube and recursively splits to singleton factors.

With explicit decision elements and memoization, this is linear in the portion of the SDD/vtree visited, up to representation bookkeeping.

### Why the recursion is exact for the laminar target

If a nontrivial \(T\)-laminar factor partition refines the root subtree, then all its blocks lie wholly in the left or right child subtree. Regrouping those blocks shows that \(f\) must first factor across the root cut \(L\mid R\). Hence failure of the root criterion rules out *every* nontrivial \(T\)-laminar refinement. If the root criterion succeeds, the problem separates into the two child factors.

---

## 5. Prime-aligned direct-extraction corollary

### Corollary 5.1

If every semantic prime AND-factor block of \(f\) is the leaf set of a subtree of the chosen vtree \(T\), then the recursion in Theorem 4.1 returns the **full semantic prime partition**, not merely the \(T\)-laminar one.

Consequently, if the simplicial carrier prime partition \(\Pi_K\) is also supplied, the full simultaneous carrier/semantic partition is obtained by

\[
\Pi_{K,f}=\operatorname{LCC}(\Pi_K,\Pi_f)
\]

without SAT or QBF.

This gives a low-overhead compiled route under an explicit **prime-alignment** hypothesis.

---

## 6. Exhaustive small-universe validation

`code/sdd_direct_extraction.py` uses exact truth tables to construct the semantic compressed cofactor partition induced by the fixed balanced vtree

\[
((x_0,x_1),(x_2,x_3)).
\]

It exhaustively checked all **65,535 nonfalse four-variable Boolean functions**.

Results:

- root compressed-SDD cut criterion vs exact CM rank-one test: **0 failures**;
- recursive direct extraction vs exhaustive finest \(T\)-laminar factorization: **0 failures**;
- functions with a nontrivial unrestricted prime factorization: **2,601**;
- functions where the unrestricted prime partition is strictly finer than what this fixed vtree exposes: **2,376**.

Thus, among the 2,601 decomposable functions, only 225 have their full factorization exposed by this particular fixed balanced vtree. This is not a negative result about SDDs; it is a warning that **direct structural extraction is alignment-sensitive**.

The data are in `data/sdd_extraction_validation.json`.

---

## 7. Research conclusion for the structured-d-DNNF branch

The route separates into three levels:

1. **Arbitrary structured d-DNNF:** no full direct-extraction theorem established here. Current closure lower bounds block the obvious transformation-based route.
2. **Compressed SDD, fixed vtree:** exact direct extraction of the finest \(T\)-laminar factors.
3. **Prime-aligned compressed SDD:** exact full prime factor extraction, followed immediately by carrier LCC.

The strongest practical design is therefore hybrid:

- compile with a carrier/interaction-aware vtree;
- peel all factors exposed by compressed-SDD structure;
- send only unresolved cross-vtree candidate separations to the incremental four-corner SAT comparator.

That avoids pretending a fixed vtree reveals arbitrary Cartesian factors while still exploiting compiled structure aggressively.
