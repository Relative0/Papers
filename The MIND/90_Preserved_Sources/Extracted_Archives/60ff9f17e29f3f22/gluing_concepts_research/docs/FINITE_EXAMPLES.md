# Finite Examples and Exact Computation

All simplicial calculations below are reproduced by `code/gluing_audit.py`. Coefficients for homology are \(\mathbb F_2\). The JSON/CSV files in `data/` contain the exact machine-readable results.

## Example A — two concepts glued at one vertex

\[
A=\Delta\{a,b\},\quad B=\Delta\{b,c\},\quad D=A\cap B=\Delta\{b\}.
\]
Pushout/union facets:
\[
\{a,b\},\{b,c\}.
\]
Output:

- f-vector \((3,2)\);
- Betti numbers \((1,0)\);
- minimal nonface \(\{a,c\}\);
- finest join blocks \(\{a,c\}\mid\{b\}\).

The last point is instructive: the path is the cone on two points, so it is join-decomposable even though its **historical gluing** decomposition was the two incident edges. Assembly history and intrinsic factorization are different.

## Example B — two filled triangles glued along an edge

\[
A=\Delta\{a,b,c\},\quad B=\Delta\{b,c,d\},\quad D=\Delta\{b,c\}.
\]
Output:

- facets \(abc,bcd\);
- f-vector \((4,5,2)\);
- Betti numbers \((1,0,0)\);
- minimal nonface \(\{a,d\}\);
- finest join blocks \(\{a,d\}\mid\{b\}\mid\{c\}\).

Mayer–Vietoris is exact but homologically trivial because all pieces and the union are contractible. See `CHAIN_LEVEL_GLUING.md` for the explicit chain dimensions.

## Example C — tetrahedron from triangular faces

Let the four triangles be
\[
abc,abd,acd,bcd.
\]
Their union is the boundary \(\partial\Delta^3\):

- f-vector \((4,6,4)\);
- Betti numbers \((1,0,1)\);
- Euler characteristic 2;
- unique minimal nonface \(abcd\);
- join-irreducible.

The filled tetrahedron \(\Delta^3\) has:

- f-vector \((4,6,4,1)\);
- Betti numbers \((1,0,0,0)\);
- Euler characteristic 1;
- no minimal nonfaces;
- finest join decomposition into four singleton vertices.

The machine comparison shows that the filled tetrahedron differs from the four-face union by **exactly one simplex**, \(abcd\).

### Three faces and horn semantics

The union of three triangular faces is contractible, with Betti numbers \((1,0,0)\). It is the combinatorial shape underlying a 3-horn. Plain abstract-complex semantics do not fill it. A Kan-style simplicial-set semantics may supply a filler only under an additional filling condition.

### Flag semantics

The complete graph \(K_4\) as a 1-dimensional complex flag-completes to the filled tetrahedron. The script verifies this exactly. Therefore “all four triangles are necessary” is false under flag completion and “all four triangles are sufficient” is false under plain union. The answer is determined by the completion policy.

## Example D — compatible local data that fail to glue

Use the discrete two-point space \(X=\{p,q\}\) and the presheaf
\[
P(W)=\mathbb Z\;(W\ne\varnothing),\qquad P(\varnothing)=\{*\}.
\]
Restrictions among nonempty opens are identities; restrictions to the empty set are unique. Local sections 0 on \(\{p\}\) and 1 on \(\{q\}\) agree vacuously on the empty overlap but have no global section in \(P(X)=\mathbb Z\).

This is an exact presheaf counterexample. It cannot occur for a genuine Set-valued sheaf under the ordinary sheaf hypotheses.

## Example E — clean factorization

Let the minimal nonfaces be
\[
\{a_0,a_1\},\qquad\{b_0,b_1\}.
\]
The facets are all cross-edges \(a_i b_j\), giving a 4-cycle. Exact output:

- f-vector \((4,4)\);
- Betti numbers \((1,1)\);
- join components \(\{a_0,a_1\}\mid\{b_0,b_1\}\);
- exactly one unordered nontrivial binary join factorization.

Hence
\[
K=K|_{\{a_0,a_1\}}*K|_{\{b_0,b_1\}}.
\]

## Example F — irreducible interaction

On the same four vertices, take minimal nonfaces
\[
\{a_0,a_1\},\{a_1,b_0\},\{b_0,b_1\}.
\]
Output facets:
\[
\{a_0,b_0\},\{a_0,b_1\},\{a_1,b_1\}.
\]
Exact output:

- f-vector \((4,3)\);
- Betti numbers \((1,0)\);
- connected minimal-nonface interaction hypergraph;
- zero nontrivial join factorizations.

This is a contractible but structurally irreducible example.

## Example G — smallest nonunique coarse decomposition

For the filled triangle \(\Delta\{a,b,c\}\), the script finds three unordered nontrivial bipartition join decompositions:

\[
\{a\}|\{b,c\},\qquad
\{a,b\}|\{c\},\qquad
\{a,c\}|\{b\}.
\]

The **finest** decomposition is unique: the three singleton vertices. Thus nonuniqueness appears at the coarse/binary level, not at the prime/finest level.

## Example H — separately factorable layers with incompatible partitions

This additional diagnostic goes beyond the required A–G list and tests the structured two-layer criterion. Let the four attributes be
\[
V=\{a_0,a_1,b_0,b_1\}.
\]
Choose a simplicial carrier whose canonical finest join partition is
\[
\Pi_K=\{\{a_0,a_1\},\{b_0,b_1\}\},
\]
and a semantic relation
\[
R=\{(x,y,x,y):x,y\in\{0,1\}\},
\]
whose prime Cartesian partition is
\[
\Pi_R=\{\{a_0,b_0\},\{a_1,b_1\}\}.
\]
Both layers factor nontrivially, but their partitions cross. Their least common coarsening is the one-block partition \(\{V\}\). Hence there is **no nontrivial partition that simultaneously factorizes both layers**. The exact rows and computed partitions are stored in `data/structured_factorization_demo.json`.

This is a concrete reason to define a structured concept's independence by cross-layer agreement rather than by factorability of either layer in isolation.

## Exhaustive finite enumeration through five vertices

The script enumerates all downsets of the Boolean lattice and filters to complexes that actually use all labeled vertices.

| n | all downsets | complexes using all vertices | join-indecomposable | join-decomposable | finest-factor distribution |
|---:|---:|---:|---:|---:|---|
| 1 | 3 | 1 | 1 | 0 | 1:1 |
| 2 | 6 | 2 | 1 | 1 | 1:1, 2:1 |
| 3 | 20 | 9 | 5 | 4 | 1:5, 2:3, 3:1 |
| 4 | 168 | 114 | 84 | 30 | 1:84, 2:23, 3:6, 4:1 |
| 5 | 7,581 | 6,894 | 6,348 | 546 | 1:6348, 2:470, 3:65, 4:10, 5:1 |

The program then checks every unordered bipartition of every such complex. Across **104,237** partition tests it found:

- 0 failures of the minimal-nonface join criterion;
- 0 failures of reconstruction from the connected components of the minimal-nonface hypergraph.

These computations are best viewed as regression tests of the implementation and formal criterion, not as a novelty experiment.

## Complexity/speedup observations

The fastest canonical structural test is not “try every decomposition.” Compute minimal nonfaces, connect vertices that co-occur in one, and take connected components. This directly yields the finest join partition.

There is an input-representation caveat: a complex can have exponentially many minimal nonfaces relative to a compact facet list, so explicit minimal-nonface enumeration is output-sensitive and can be exponential. For flag complexes, the test collapses to connected components of the complement graph, which is polynomial and mirrors standard graph join decomposition.

For semantic relations supplied extensionally, Cartesian factorization can use database prime-factorization algorithms rather than testing all attribute partitions. For a fixed CM/Boolean bipartition, ordinary \(\mathbb F_2\) matrix rank gives the conjunctive/XOR separability measure directly.
