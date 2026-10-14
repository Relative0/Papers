# Decomposition and Separability

## 1. Three decompositions that must not be conflated

The historical material uses “unfolding,” “faces,” and “distinguishing” in ways that can suggest a single decomposition operation. Modernly there are at least three different problems.

1. **Face decomposition:** describe a simplex/complex by lower-dimensional faces.
2. **Assembly decomposition:** recover a chosen cover/pushout diagram that built the object.
3. **Independent-factor decomposition:** factor the object into parts with no mixed interaction according to a declared product/join/semantic criterion.

Only the third deserves the name **disentanglement** in the strong sense sought by this project.

## 2. Simplicial join separability

Let \(K\) be a finite complex on vertex set \(V=A\sqcup B\). Define structural independence across the cut \(A|B\) by
\[
K=K|_A*K|_B.
\]
This says exactly that every allowed face on \(A\) can be freely combined with every allowed face on \(B\).

### Theorem 2.1 — minimal-nonface criterion

Let \(\mathcal M(K)\) be the set of minimal nonfaces of \(K\). Then
\[
K=K|_A*K|_B
\quad\Longleftrightarrow\quad
\text{every }M\in\mathcal M(K)\text{ lies wholly in }A\text{ or wholly in }B.
\]

**Proof.** A face belongs to a finite complex iff it contains no minimal nonface. If a minimal nonface crosses the cut, its two pieces are faces of the induced factors but their union is forbidden, contradicting the join condition. Conversely, if every minimal nonface is contained in one block, a set \(\sigma_A\cup\sigma_B\) can be forbidden only because one block already contains a minimal nonface, exactly reproducing the join of the restrictions. ∎

This is an elementary standard consequence of the join/minimal-nonface formalism, not a novelty claim.

### Corollary 2.2 — canonical finest join decomposition

Form a hypergraph \(H_K\) on \(V\) whose hyperedges are the minimal nonfaces of \(K\). Connect vertices whenever they occur in a common hyperedge and take connected components
\[
V=V_1\sqcup\cdots\sqcup V_r.
\]
Then
\[
K=K|_{V_1}*\cdots*K|_{V_r},
\]
and every other join decomposition is obtained by grouping these finest blocks.

Recent work on Hopf monoids of set families states this in the language of a support system/fundamental inflator and explicitly identifies a unique minimum partition describing the finest join representation. Thus this should be treated as a standard structural tool.

### Computational verification

The supplied script independently enumerated every labeled finite complex using all vertices for \(n\le5\):

| vertices | complexes | join-indecomposable | nontrivially join-decomposable | unordered partition checks | criterion failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 2 | 0 |
| 3 | 9 | 5 | 4 | 27 | 0 |
| 4 | 114 | 84 | 30 | 798 | 0 |
| 5 | 6,894 | 6,348 | 546 | 103,410 | 0 |

Across all 7,020 complexes and 104,237 tested unordered bipartitions there were zero disagreements between the join test and the minimal-nonface criterion, and zero failures of the finest-component reconstruction. This is validation, not evidence of novelty.

## 3. Why a simplex alone is too weak

For a simplex \(\Delta(V)\), there are **no** minimal nonfaces. Hence the finest join factors are the individual vertices and, for every partition \(V=A\sqcup B\),
\[
\Delta(V)=\Delta(A)*\Delta(B).
\]

Thus a simplex by itself declares *maximum combinatorial freedom* between all vertex blocks. It cannot distinguish a psychologically meaningful factorization from an arbitrary partition. This is the main obstruction to a simplex-only theory of independent concepts.

## 4. Relational/cartesian separability

Let a semantic concept be a finite relation
\[
R\subseteq X_A\times X_B
\]
across disjoint attribute blocks. Define independence by
\[
R=\pi_A(R)\times\pi_B(R).
\]
For finite \(R\), since \(R\subseteq\pi_A(R)\times\pi_B(R)\) automatically,
\[
R\text{ factors}\quad\Longleftrightarrow\quad
|R|=|\pi_A(R)|\,|\pi_B(R)|.
\]

This gives a representation-independent semantic criterion: all locally allowed assignments can combine freely. Relational prime factorization has an established database-theory literature and efficient algorithms, so the criterion is a tool, not a new result.

## 5. Boolean/CM separability

The supplied current CM/LM manuscript already proves a particularly useful fixed-cut criterion. If a Boolean function \(f(a,b)\) is flattened across a chosen variable bipartition \(A|B\) into a truth matrix \([f]_{A|B}\), then the manuscript's theorem “Rank and conjunctive/XOR separability” states:

\[
f(a,b)=g(a)\land h(b)
\quad\Longleftrightarrow\quad
\operatorname{rank}_{\mathbb F_2}[f]_{A|B}\le1.
\]

For a nonzero function the factors are the ordinary rank-one factors and are unique over \(\mathbb F_2\). More generally, the minimum number of conjunctive terms in an XOR sum
\[
f=\bigoplus_{i=1}^k g_i(a)\land h_i(b)
\]
is exactly the \(\mathbb F_2\) matrix rank.

This is a strong candidate semantic layer because it distinguishes a filled simplex's trivial join structure from actual Boolean coupling. It also has a clean quantitative interaction measure (rank). However, general Boolean functional decomposition is classical (Ashenhurst, Curtis, Karp and subsequent logic-synthesis literature), so priority must be framed narrowly around the exact CM formalism rather than Boolean decomposition broadly.

## 6. Sheaf separability

Sheaf theory addresses **compatibility**, not automatically independence. If \(\mathcal F\) is a sheaf on \(K\) (or on a topology associated with it), compatible sections over a cover glue uniquely. That establishes local-to-global consistency.

A stronger factorization notion would ask whether the semantic sheaf itself decomposes, for example as an external product of sheaves supported on separate structural factors. Such a statement requires a precise product site/category and is not proved in the current project. It is a promising extension, not something to assume from vanishing cohomology alone.

## 7. Homology is an interaction diagnostic, not a complete separability test

Homology can reveal global holes created by gluing, and Mayer–Vietoris connecting maps can identify how overlap participates in them. But homological triviality does not imply independence.

Example F in the package is a four-vertex path. It is contractible, with \(H_0\cong\mathbb F_2\) and higher homology zero, yet its minimal-nonface hypergraph is connected and it has no nontrivial join decomposition. Thus even complete vanishing of reduced homology cannot certify structural separability.

Similarly, short exact sequences of chain groups over a field split noncanonically as vector spaces. Such algebraic splitting is too weak to mean conceptual independence unless the splitting respects additional combinatorial/semantic structure.

## 8. Example E — clean structural factorization

Let
\[
K=\partial\Delta^1_{\{a_0,a_1\}} * \partial\Delta^1_{\{b_0,b_1\}}.
\]
Its facets are
\[
\{a_0,b_0\},\{a_0,b_1\},\{a_1,b_0\},\{a_1,b_1\}.
\]
Geometrically this is a 4-cycle. The minimal nonfaces are exactly
\[
\{a_0,a_1\},\qquad\{b_0,b_1\}.
\]
The interaction hypergraph has two components, giving the canonical two-factor join decomposition. The computation reports Betti numbers \((1,1)\) over \(\mathbb F_2\).

## 9. Example F — irreducible interaction on the same four attributes

On the same vertex set let the minimal nonfaces be
\[
\{a_0,a_1\},\quad\{a_1,b_0\},\quad\{b_0,b_1\}.
\]
The facets become
\[
\{a_0,b_0\},\{a_0,b_1\},\{a_1,b_1\}.
\]
The minimal-nonface hypergraph is connected, so there is no nontrivial join factorization. The complex is nevertheless contractible. This cleanly separates “topologically simple” from “factorizable.”

## 10. Example G — smallest nonunique coarse join decomposition

The filled triangle \(\Delta\{a,b,c\}\) has a unique **finest** join decomposition into the three vertices, but three distinct unordered binary/coarse decompositions:
\[
\Delta\{a\}*\Delta\{b,c\},\quad
\Delta\{b\}*\Delta\{a,c\},\quad
\Delta\{c\}*\Delta\{a,b\}.
\]
No two-vertex complex has more than one unordered nontrivial bipartition, so this is the smallest example of nonunique coarse join decomposition. It also illustrates why “decomposition is unique” is false until “prime/finest” is specified.

## 11. Recommended definition of conceptual independence

No single criterion should be called independence without qualification. Use a hierarchy:

- **structural independence:** join factorization of the simplicial carrier;
- **semantic independence:** Cartesian factorization of the admissible-assignment relation;
- **CM conjunctive separability:** rank-one truth flattening across a fixed cut;
- **probabilistic independence:** only when a probability distribution has been supplied;
- **local-to-global compatibility:** sheaf gluing, not independence by itself.

A robust “cleanly disentangled concept” should satisfy at least structural and semantic independence across the **same partition**. Requiring multiple layers to agree makes the notion nontrivial and prevents the simplex problem from trivializing the theory.

## 12. Two-layer simultaneous decomposition theorem

Let a finite structured concept be \(\mathcal C=(K,R)\) on a common finite attribute set \(V\), where \(K\) is a simplicial complex and \(R\) is a nonempty finite relation. Let \(\Pi_K\) denote the canonical finest join partition of \(K\), and let \(\Pi_R\) denote the canonical prime Cartesian-product partition of \(R\) (the relational-factorization literature supplies such a maximal/prime decomposition for finite relations).

A partition \(\Pi\) is **simultaneously separable** when
\[
K=*_{B\in\Pi}K|_B
\qquad\text{and}\qquad
R=\prod_{B\in\Pi}\pi_B(R).
\]

### Theorem 12.1 — finest simultaneous partition

The simultaneously separable partitions are exactly the partitions that are coarsenings of both \(\Pi_K\) and \(\Pi_R\). Consequently there is a unique finest simultaneous partition,
\[
\Pi_{K,R}=\operatorname{LCC}(\Pi_K,\Pi_R),
\]
the **least common coarsening** of the two prime partitions.

**Proof.** By the canonical finest join decomposition, a partition is a valid join factorization precisely when it is obtained by grouping blocks of \(\Pi_K\). Likewise, by prime Cartesian factorization, every valid product decomposition of \(R\) is obtained by grouping prime relational factors. Therefore a simultaneous partition must be a common coarsening. Conversely, coarsening either valid factorization merely regroups factors; associativity of join and Cartesian product preserves both factorizations. The least common coarsening is therefore valid and refines every other simultaneous valid partition. ∎

A practical construction of \(\operatorname{LCC}\) is to put an edge between two attributes whenever they lie in a common block of either \(\Pi_K\) or \(\Pi_R\), then take connected components. Once the two prime partitions are known, this merge step is linear in their total block incidence.

This theorem is best treated as a **synthesis lemma**, not as a novelty claim: both prime decompositions have substantial antecedents, and the least-common-coarsening step is elementary partition theory.

### Example H — both layers factor, but not together

The reproducible file `data/structured_factorization_demo.json` uses four attributes. The simplicial layer has finest factors
\[
\{a_0,a_1\}\mid\{b_0,b_1\},
\]
while the semantic relation independently enforces equality on \((a_0,b_0)\) and on \((a_1,b_1)\), giving semantic prime factors
\[
\{a_0,b_0\}\mid\{a_1,b_1\}.
\]
The least common coarsening is the single four-attribute block. Thus each layer is separately separable, yet the **structured concept has no nontrivial simultaneous decomposition**. This is exactly why cross-layer alignment is a nontrivial design constraint.

## 13. Strongest next theorem / complexity problem

The strongest next problem is the **succinct structured factorization problem**.

> **Input:** a finite complex \(K\) given compactly (for example by facets/minimal nonfaces) and a Boolean semantic object \(f\) given intensionally (CNF, DNF, circuit, ANF, or a CM/LM tensor), on the same attribute set \(V\).  
> **Output:** the finest partition \(\Pi\) for which the simplicial carrier and the semantic object factor across the same blocks, or certify that only the one-block partition works.

For an extensional truth relation the two-layer theorem reduces the problem to two known prime decompositions followed by a least-common-coarsening merge. The genuinely open/interesting part is **succinct representation**: determine the complexity of recovering the semantic prime partition without expanding an exponential truth table, and characterize tractable subclasses (bounded-width CNF, read-once formulas, affine/ANF classes, flag carriers, bounded treewidth, fixed CM cut, etc.).

A useful theorem would either:

1. give a polynomial/FPT algorithm for a meaningful broad class, with a canonical structured factorization invariant; or
2. prove hardness for the general circuit/CNF input while isolating the largest tractable subclasses.

Only after that layer is settled should the project add sheaf/cosheaf product decompositions. This target is mathematically sharper than another general statement that “concepts can be glued,” and it directly operationalizes clean disentanglement.
