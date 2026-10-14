# Theorems, Counterexamples, and Open Problems

## Status key

- **Established/standard:** mathematically correct, but part of existing mathematics.
- **Established synthesis lemma:** proved here from standard ingredients; no novelty claim.
- **Computationally verified:** exhaustively checked in the bounded campaign stated below; not a substitute for proof.
- **Open research target:** not proved here.

## I. Established results used by the framework

### T1. Common-subcomplex gluing is non-completing

Let \(D\hookrightarrow A\) and \(D\hookrightarrow B\) be inclusions of abstract simplicial complexes. Their pushout in the inclusion case is the simplicial union \(A\cup_D B\) after identifying the common copy of \(D\). Every simplex in the result is inherited from \(A\) or \(B\); no new mixed simplex is generated merely because all its vertices are present.

**Status:** established/standard.

**Consequence:** gluing two edges at a common endpoint makes a path, not a triangle; gluing all four triangular faces of a tetrahedron makes its boundary, not its interior.

### T2. Union-of-two-simplices criterion

For simplices \(\Delta(S)\) and \(\Delta(T)\),
\[
\Delta(S)\cup\Delta(T)\text{ is a simplex}
\iff S\subseteq T\text{ or }T\subseteq S.
\]

**Proof.** If one is contained in the other, the union is the larger simplex. If neither is contained in the other, choose \(s\in S\setminus T\) and \(t\in T\setminus S\). The edge \(\{s,t\}\) would be required in \(\Delta(S\cup T)\) but occurs in neither input. ∎

**Status:** elementary standard lemma.

### T3. Tetrahedral boundary/filler obstruction

Let \(V=\{a,b,c,d\}\). The union of the four 2-faces of \(\Delta(V)\) is \(\partial\Delta^3\), while the filled tetrahedron is \(\Delta^3\). Over \(\mathbb F_2\),
\[
\beta(\partial\Delta^3)=(1,0,1),\qquad
\beta(\Delta^3)=(1,0,0,0).
\]
Thus the top simplex is genuinely additional data under ordinary simplicial gluing.

**Status:** established; exactly reproduced by `gluing_audit.py`.

### T4. Minimal-nonface criterion for a join cut

For a finite complex \(K\) on \(V=A\sqcup B\),
\[
K=K|_A*K|_B
\iff
\text{every minimal nonface of }K\text{ is contained entirely in }A\text{ or }B.
\]

**Proof idea:** a face is allowed iff it contains no minimal nonface. A crossing minimal nonface is precisely a mixed interaction forbidden by \(K\) but incorrectly admitted by the product of the two induced factors. ∎

**Status:** established/elementary reformulation of standard join structure.

### T5. Canonical finest structural join partition

Make a hypergraph on \(V\) whose hyperedges are the minimal nonfaces of \(K\). Its connected components \(V_1,\ldots,V_r\) give
\[
K=K|_{V_1}*\cdots*K|_{V_r},
\]
and every other join decomposition is obtained by merging these blocks.

**Status:** established. Contemporary work by Marshall & Martin gives a unique finest join representation in support-system/fundamental-inflator language. The formulation here is a direct minimal-nonface characterization.

### T6. Simplex trivialization theorem/design constraint

For every partition \(V=V_1\sqcup\cdots\sqcup V_r\),
\[
\Delta(V)=\Delta(V_1)*\cdots*\Delta(V_r).
\]
Hence a bare simplex cannot encode a privileged notion of conceptual independence.

**Status:** established; central design constraint.

### T7. Finite Cartesian semantic factorization test

For a nonempty finite relation \(R\subseteq X_A\times X_B\),
\[
R=\pi_A(R)\times\pi_B(R)
\iff
|R|=|\pi_A(R)|\,|\pi_B(R)|.
\]
The forward direction is immediate. For the reverse, \(R\) is always contained in the product of its projections, so equality of finite cardinalities forces equality of sets.

**Status:** established; finite relation factorization has a substantial database literature.

### T8. CM fixed-cut rank separability

The supplied current CM/LM manuscript proves, for a fixed variable bipartition \(A|B\),
\[
f(a,b)=g(a)\land h(b)
\iff
\operatorname{rank}_{\mathbb F_2}[f]_{A|B}\le1,
\]
and more generally the minimum number of conjunctive terms in an XOR sum equals the ordinary \(\mathbb F_2\)-rank of the flattening.

**Status:** established in the supplied CM manuscript; broad Boolean decomposition is prior art, so novelty must be scoped narrowly.

### T9. Sheaf matching-family theorem

For a Set-valued sheaf \(\mathcal F\) and an open cover \(U=\bigcup_iU_i\), local sections \(s_i\in\mathcal F(U_i)\) satisfying
\[
s_i|_{U_i\cap U_j}=s_j|_{U_i\cap U_j}\quad\forall i,j
\]
glue to a unique global section \(s\in\mathcal F(U)\).

**Status:** standard sheaf axiom.

**Important:** no extra independent triple-overlap equality is needed for ordinary Set-valued sheaves; higher coherence becomes relevant only for richer targets such as stacks/higher categories.

### T10. Mayer–Vietoris chain gluing

For \(K=A\cup B\) and \(D=A\cap B\), simplicial chains fit into
\[
0\to C_\bullet(D)\xrightarrow{x\mapsto(x,-x)}
C_\bullet(A)\oplus C_\bullet(B)
\xrightarrow{(a,b)\mapsto a+b}C_\bullet(K)\to0,
\]
which induces the Mayer–Vietoris long exact sequence.

**Status:** standard algebraic topology.

### T11. Finest simultaneous structural-semantic partition

Let \(\Pi_K\) be the canonical finest join partition of \(K\), and \(\Pi_R\) the canonical prime Cartesian partition of a nonempty finite relation \(R\), both on the same attribute set. A partition supports both factorizations iff it is a coarsening of both. Therefore the unique finest simultaneous factorization is their **least common coarsening**.

**Status:** established synthesis lemma. It is useful, but the ingredients make a strong novelty claim unwarranted without a dedicated priority result.

## II. Exact counterexamples / obstruction examples

### C1. Four faces do not reconstruct the tetrahedron under ordinary union

Input: all four triangular faces.  
Output: \(\partial\Delta^3\), not \(\Delta^3\).

This blocks the thesis's informal identification of “gluing all faces” with “recovering the higher simplex” unless a filler/completion rule is declared.

### C2. Compatible presheaf data need not glue

On the discrete space \(X=\{p,q\}\), define
\[
P(W)=\mathbb Z\;(W\neq\varnothing),\qquad P(\varnothing)=\{*\},
\]
with identity restrictions between nonempty opens and the unique map to \(\varnothing\). Local sections \(0\) on \(\{p\}\) and \(1\) on \(\{q\}\) agree on their empty overlap but admit no global section in \(P(X)=\mathbb Z\).

This distinguishes a presheaf from a sheaf.

### C3. Homological triviality does not imply join separability

Example F is the four-vertex path with facets
\[
\{a_0,b_0\},\{a_0,b_1\},\{a_1,b_1\}.
\]
It is contractible but its minimal-nonface interaction hypergraph is connected, so it has no nontrivial join decomposition.

This blocks “zero homology = independent factors.”

### C4. Coarse decomposition is not unique

The filled triangle has three distinct unordered binary join decompositions, even though its finest prime join decomposition into singleton vertices is unique.

This blocks any unqualified statement that decomposition is unique.

### C5. Separate factorability need not align across layers

In Example H the simplicial prime partition is
\[
\{a_0,a_1\}|\{b_0,b_1\},
\]
while the semantic prime partition is
\[
\{a_0,b_0\}|\{a_1,b_1\}.
\]
Each layer factors nontrivially, but the least common coarsening is the one-block partition. Thus the structured concept is irreducible under the requirement that both layers use the same partition.

This is an especially important counterexample to “independent in each representation implies jointly independent.”

## III. Bounded computational validation

`code/gluing_audit.py` enumerates all labeled abstract simplicial complexes using all vertices for \(n\le5\). It checked **7,020 complexes** and **104,237 unordered bipartitions**.

| n | complexes using all vertices | join indecomposable | nontrivially decomposable | partition checks | criterion failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 2 | 0 |
| 3 | 9 | 5 | 4 | 27 | 0 |
| 4 | 114 | 84 | 30 | 798 | 0 |
| 5 | 6,894 | 6,348 | 546 | 103,410 | 0 |

It found zero failures of T4 and zero failures of reconstruction from the finest minimal-nonface components. These computations are regression/evidence checks, not priority evidence.

## IV. Open problems, ordered by value

### O1. Succinct structured factorization — **highest priority**

Input a complex \(K\) compactly and Boolean semantics \(f\) intensionally (CNF/DNF/circuit/ANF/CM), without expanding the truth table. Compute the finest common structural-semantic factorization.

Questions:

- complexity for unrestricted circuits/CNF;
- polynomial/FPT cases under bounded width/treewidth/read-once structure;
- whether structural factors can prune semantic factorization enough to yield substantial speedups;
- whether the CM representation gives a practically superior detector for relevant subclasses.

### O2. Product decomposition of concept sheaves

Define a precise category/site in which a semantic sheaf can decompose across a vertex/attribute partition. Determine whether there is a canonical finest product partition, and how it interacts with the carrier join partition and section-level factorization.

### O3. Marked unfolding/filling category

Construct a category of marked simplicial objects in which an unfolding operation records enough provenance for a filler to be a genuine inverse on a declared subcategory. Test whether a useful adjunction \(F\dashv U\) exists. Do not expect this on bare complexes.

### O4. Obstruction theory beyond ordinary sheaves

If local semantic data naturally form groupoids/categories rather than sets, determine whether higher descent obstructions provide a principled notion of failure to form a global concept. This should only be attempted after the Set-valued case is complete.

### O5. Interaction invariants from Mayer–Vietoris

Classify which ranks/images of connecting maps are stable/useful as measures of topological interaction while proving what they do **not** detect about semantic independence.

### O6. Finite classification extension

The exact enumeration can be extended beyond five vertices using canonical generation/isomorph rejection, but brute-force Dedekind enumeration becomes expensive. Before doing so, exploit:

- minimal-nonface hypergraphs directly;
- complement-graph decomposition for flag complexes;
- isomorphism classes rather than labeled complexes;
- structural factorization to split the search recursively.

A six-vertex campaign is useful only if tied to a sharper conjecture; raw counts alone are unlikely to produce a theorem.

## V. Single strongest next target

> **Succinct Structured Factorization Theorem/Complexity Classification.** Characterize and compute the canonical finest partition on which both a compact simplicial carrier and an intensionally represented Boolean/CM semantic object factor, without truth-table expansion.

The extensional relation case is already structurally solved by T11. The mathematical opportunity is therefore in the **succinct/algorithmic** case: prove a tractability theorem for a substantial class or a hardness theorem with a sharp tractable frontier. That is the most promising route from “useful synthesis” toward a genuine theorem-level contribution.
