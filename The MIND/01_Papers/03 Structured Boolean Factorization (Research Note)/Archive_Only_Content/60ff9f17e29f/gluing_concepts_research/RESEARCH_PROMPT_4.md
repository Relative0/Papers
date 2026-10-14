# Research Prompt 4 — Gluing, Decomposition, and Disentanglement of Concepts

**Working title:** *Gluing Concepts: Composition, Reconstruction, and Clean Decomposition in Simplicial Mental Spaces*

**Primary historical source:** the 2015 Master's thesis *On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces*.

**Relationship to the other research threads:** This project is deliberately adjacent to, but distinct from, the **Unfolding / Mental Space** project. It should be allowed to discover that gluing is an inverse, adjoint, partial inverse, closure, or entirely different operation from unfolding. Do not assume the answer in advance.

## Role

Act as an independent mathematical research team specializing in simplicial complexes and simplicial sets, algebraic topology, combinatorial topology, category theory, sheaf and cosheaf theory, homological algebra, Boolean/propositional structure, formal concept structures, Correspondence Matrices where relevant, and factorization/independence/decomposition problems.

Treat the 2015 thesis as a **historical source of ideas**, not as a mathematical authority. The thesis is fixed and must not be silently repaired.

The present research clarification is that the intended primitive objects of interest are **concepts represented simplicially**, with particular interest in treating a concept itself as a simplex and in composing lower-order concepts into higher-order simplices. Note, however, that the thesis sometimes defines a "concept" as a connected simplicial complex rather than a single simplex. Do not silently identify these two notions. Determine whether the modern theory should use:

1. a simplex as a concept;
2. a simplicial complex as a concept;
3. a simplex as an atomic concept and a complex as a mental/conceptual structure;
4. some other two-level distinction.

Make this choice explicit.

## 1. Historical seed to recover exactly

The thesis contains two related gluing ideas.

First, after "unfolding" a higher-dimensional logical simplex into lower-dimensional pieces, it asks whether those pieces can be **glued or integrated back** into the higher-dimensional simplex. It gives a triangle example and a tetrahedral example, and explicitly wonders whether there is an "integrator" that builds higher-order simplices from lower-order faces.

Second, in the later Mental Space discussion, overlapping concepts are compared by relative/subspace structure, and the thesis proposes using **compatible sections on presheaves** to glue information from smaller concepts into sheaves or higher-order concepts.

Recover all of this material faithfully before modernizing it.

Create a source map containing every gluing example; every decomposition/unfolding example relevant to gluing; every use of common faces, shared attributes, subspace intersections, presheaves, sheaves, or higher-order concepts; and every later logical-triangle/logical-square construction that may amount to gluing along shared data.

For each item classify it as:

`historical intuition | precise definition | worked example | unsupported claim | possible modern analogue`.

## 2. Central mathematical problem

The central question is:

\[
\boxed{
\text{When can lower-order concepts be glued into a higher-order concept, and when can the result be cleanly decomposed back?}
}
\]

Suppose concepts \(C_1,\ldots,C_r\) are represented by simplices or subcomplexes. We want to understand an operation schematically written

\[
G(C_1,\ldots,C_r)=C,
\]

where \(C\) is a larger-order concept.

Then ask whether there exists a decomposition or disentangling operation

\[
D(C)=\{C_1,\ldots,C_r\}
\]

such that, in an appropriate sense,

\[
D(G(C_1,\ldots,C_r))
\cong
\{C_1,\ldots,C_r\}.
\]

Do **not** assume such a decomposition is unique or even possible. Determine what additional structure is required to make the problem nontrivial.

## 3. What exactly is "gluing"?

Investigate several mathematically distinct notions rather than choosing one prematurely.

For simplices/complexes \(\sigma,\tau\), study gluing by:

- identification along a common face;
- pushouts in simplicial complexes;
- pushouts in simplicial sets;
- unions satisfying \(\sigma\cap\tau=\rho\) for a specified common face \(\rho\);
- joins;
- products;
- wedges;
- colimits of diagrams of simplices;
- CW-type attachment;
- horn filling;
- nerve constructions;
- clique/flag closure;
- sheaf-theoretic gluing of compatible local data;
- cosheaf aggregation;
- Boolean/logical conjunction or other logical composition.

For each candidate notion, determine:

1. what the inputs are;
2. what compatibility data is required;
3. whether the result is a simplex, a complex, or another object;
4. whether gluing introduces unintended faces/simplices;
5. whether the construction is associative or order-dependent;
6. whether the construction is functorial;
7. whether the original components remain recoverable.

A key issue is that ordinary union is **not automatically meaningful composition**. Identify conditions under which gluing produces a coherent higher-order concept rather than merely a set-theoretic union.

## 4. Higher-order concepts

Formalize the phrase "higher-order concept."

Test at least these possibilities:

- **Dimension/order:** a higher-order concept is an \(n\)-simplex assembled from lower-dimensional faces.
- **Attribute complexity:** a higher-order concept contains more jointly constrained attributes.
- **Categorical composition:** a higher-order concept is a colimit of a diagram of lower-order concepts.
- **Logical composition:** a higher-order concept is represented by a formula such as \(C=C_1\wedge C_2\).
- **Sheaf/global-section view:** a higher-order concept is a global object reconstructed from compatible local pieces.

Determine which notion best matches the thesis examples and which gives the most mathematically fertile modern theory.

Do not conflate these notions unless an equivalence theorem is proved.

## 5. Clean gluing criteria

Develop exact criteria for when concepts glue "cleanly."

Potential conditions to test include:

- intersections are exactly prescribed common faces;
- pairwise intersection data satisfy higher compatibility conditions;
- no unintended simplex is created by closure;
- local labels/attributes agree on overlaps;
- cocycle/descent conditions hold;
- the resulting colimit remains in the intended category;
- the gluing map is injective away from prescribed overlaps;
- the constituent concepts embed as identifiable subobjects.

Try to formulate necessary and sufficient conditions.

If a family \(\{C_i\}\) has overlap data \(C_{ij}\), investigate whether a condition analogous to

\[
s_i|_{C_{ij}}=s_j|_{C_{ij}}
\]

is enough for gluing, or whether higher-order compatibility is needed.

If sheaf language is appropriate, state the actual sheaf axiom and determine precisely what plays the role of open sets, local sections, restrictions, matching families, and global sections.

Do not use the word "sheaf" merely because pieces are being combined.

## 6. Decomposition and "disentanglement"

The thesis's unfolding operator decomposes a concept into differentiated lower-dimensional logical pieces. The present question is broader:

\[
\boxed{
\text{When can a composite concept be decomposed into genuinely independent constituent concepts?}
}
\]

"Independent" must be formally defined.

Investigate multiple candidate notions:

- disjoint variable support;
- Boolean factorization;
- direct product factorization;
- join factorization;
- tensor/rank-one factorization;
- categorical product/coproduct factorization;
- disconnected interaction hypergraph;
- vanishing mixed interaction terms;
- statistical/probabilistic independence, only if a probability model is actually present;
- separability in a modal/CM representation;
- triviality of a connecting homology/cohomology class;
- splitting of an exact sequence;
- decomposition of a sheaf/cosheaf into independent summands.

Do not import the quantum meaning of "entanglement" automatically.

Use the neutral term **factorization/separability** until a nonclassical entanglement structure is actually established.

## 7. Why a simplex alone may make independence trivial

Address an important possible obstacle.

An abstract simplex on vertex set \(V=A\sqcup B\) satisfies

\[
\Delta(V)\cong \Delta(A)*\Delta(B),
\]

so every simplex can be written as a join of simplices on a partition of its vertices.

Therefore **join decomposition by itself may be far too weak** to represent meaningful conceptual independence.

Determine what extra structure makes decomposition nontrivial, for example:

- labels or semantic attributes;
- logical constraints;
- incidence weights;
- CM/operator data;
- orientation;
- filtration depth;
- probability/measure;
- sheaf data;
- interaction terms;
- an ambient complex.

This issue should be treated as a theorem-level design constraint, not overlooked.

## 8. Canonical or unique decomposition

Given a higher-order concept \(C\), ask:

- Does a decomposition into primitive concepts exist?
- Is it unique?
- Unique up to permutation?
- Unique only after fixing an ambient category or variable partition?
- Is there a finest decomposition?
- A coarsest decomposition?
- A canonical decomposition?
- Is finding the minimum decomposition computationally hard?

Look for analogues of prime decomposition, connected-component decomposition, block decomposition, modular decomposition, tensor factorization, Boolean-function decomposition, hypergraph decomposition, and join decomposition of complexes.

If nonuniqueness is generic, characterize the ambiguity rather than hiding it.

## 9. Gluing versus unfolding

Study the relationship to the separate Unfolding project explicitly.

Let

\[
U:C\to \mathcal P(C)
\]

schematically denote unfolding/decomposition and let

\[
G:\mathcal P(C)\to C'
\]

denote gluing.

Test whether any of the following are valid:

\[
G\circ U=\mathrm{id},
\qquad
U\circ G=\mathrm{id},
\qquad
G\dashv U,
\]

or whether only weaker relations hold, such as

\[
G(U(C))\cong C
\]

after quotienting, closure, or forgetting some structure.

Also test whether unfolding produces **faces**, while disentanglement seeks **independent factors**. These may be very different operations.

This distinction is important:

\[
\boxed{
\text{decomposition into faces}
\neq
\text{factorization into independent concepts}
}
\]

unless a theorem establishes equivalence under special hypotheses.

## 10. Gluing and chain complexes

For a gluing

\[
C=A\cup B,
\qquad A\cap B=D,
\]

investigate the induced chain-level structures.

At minimum examine the standard short exact sequence

\[
0
\longrightarrow
C_\bullet(D)
\longrightarrow
C_\bullet(A)\oplus C_\bullet(B)
\longrightarrow
C_\bullet(C)
\longrightarrow
0
\]

when the hypotheses are satisfied, and the resulting Mayer-Vietoris sequence.

This may provide exactly the rigorous bridge the thesis was seeking between overlap, gluing, larger concepts, cycles/boundaries, and reconstruction.

Ask whether the "cost" or "interaction" of gluing is visible in connecting homomorphisms, relative homology, Mayer-Vietoris boundary maps, mapping cones, or homotopy pushouts.

Determine whether cleanly separable concepts correspond to special splitting behavior.

## 11. Gluing and the nerve

Given a family of concept pieces \(\{C_i\}\), construct the nerve

\[
N(\{C_i\}).
\]

Investigate whether:

- vertices represent constituent concepts;
- edges represent nonempty overlap;
- higher simplices represent compatible higher intersections;
- the nerve records the structure by which a larger concept is assembled.

Where appropriate, test conditions for a nerve theorem.

## 12. Gluing through presheaves/sheaves

The thesis explicitly gestures toward compatible sections of presheaves being glued into higher-order concepts.

Rebuild this from first principles.

Define a candidate site/base category and investigate

\[
F(U_i)
\]

as local concept data.

For a cover \(\{U_i\}\), determine whether compatible local sections

\[
s_i\in F(U_i)
\]

with

\[
s_i|_{U_i\cap U_j}
=
s_j|_{U_i\cap U_j}
\]

possess a unique global section

\[
s\in F\left(\bigcup_i U_i\right).
\]

If yes, identify precisely what the global section means as a concept.

If not, investigate the obstruction.

This may lead naturally to cohomology:

\[
\text{local compatibility} \not\Rightarrow \text{global concept}.
\]

If so, determine whether a nonzero cohomology class measures an obstruction to clean conceptual gluing.

## 13. Gluing in logical / CM representations

Where useful, translate the same examples into propositional and Correspondence-Matrix language.

For concepts represented by formulas \(L_1,L_2,\ldots\), ask when a composite

\[
L=G(L_1,\ldots,L_r)
\]

admits a factorization back into the \(L_i\).

Study:

- variable-support factorization;
- truth-table factorization;
- Boolean polynomial/ANF factorization;
- CM block/tensor factorization;
- operator decomposability;
- invariance under CM rotations or other transformations.

Determine whether the CM representation makes gluing or decomposition computationally easier to detect.

## 14. Required explicit examples

Construct a sequence of increasingly difficult examples.

### Example A — two concepts glued along a vertex
Determine the union, chain complex, homology, and recoverability.

### Example B — two triangles glued along an edge
Compute Mayer-Vietoris explicitly.

### Example C — tetrahedron from triangular faces
Revisit the thesis's historical example rigorously. Determine what data are sufficient to reconstruct the tetrahedron and whether all four faces are necessary.

### Example D — incompatible local data
Construct local pieces that pairwise appear compatible but do not admit the intended global gluing, if such an example exists in the chosen framework.

### Example E — clean factorization
Construct a higher-order logical/simplicial concept that decomposes into two independent concepts under the chosen independence criterion.

### Example F — irreducible interaction
Construct an example with the same apparent vertices/attributes that **cannot** be decomposed into independent factors.

### Example G — nonunique decomposition
Find the smallest example in which distinct decompositions produce the same global concept.

Every example must be exactly reproducible.

## 15. Computational program

For finite complexes up to feasible size:

- enumerate candidate gluings;
- classify intersections;
- compute pushouts/unions;
- calculate homology;
- test join decomposability;
- test factorization criteria;
- enumerate minimal decompositions;
- detect nonuniqueness;
- test reconstruction after unfolding;
- compare combinatorial and logical representations.

Look for mathematical speedups and canonical invariants before brute-force enumeration.

Record exact counts and counterexamples.

## 16. Literature and priority search through 2026

Conduct a current literature search based on structure, not merely the words "mental space" or "gluing concepts."

Search especially for:

- gluing simplicial complexes;
- simplicial pushouts and colimits;
- decomposition of simplicial complexes;
- join decompositions;
- simplicial factorization;
- nerve constructions;
- Mayer-Vietoris and reconstruction;
- sheaf-theoretic gluing;
- cosheaves;
- descent;
- formal concept analysis;
- conceptual spaces;
- compositional semantics;
- hypergraph decomposition;
- Boolean function decomposition;
- tensor/separability criteria;
- contextuality and sheaf obstruction;
- topological models of cognition;
- concept composition in mathematical psychology.

For every close antecedent, identify exactly which construction/theorem overlaps with the present project.

Do not make novelty claims until this search is complete.

## 17. Questions the project must ultimately answer

1. What is the mathematically cleanest definition of a simplicial **concept**?
2. What does it mean to glue concepts?
3. What compatibility data are necessary and sufficient?
4. When does gluing produce a higher-order simplex rather than a general complex?
5. When can the constituents be recovered?
6. What is the correct notion of independent concepts?
7. When is a higher concept separable/factorizable?
8. When is it irreducible?
9. Is decomposition unique or canonical?
10. Is unfolding inverse to gluing in any useful category?
11. Is "unfolding into faces" fundamentally different from "disentangling into independent factors"?
12. Do homology, relative homology, Mayer-Vietoris, or sheaf cohomology detect interaction or obstruction?
13. Can Correspondence Matrices provide a useful factorization test?
14. Is there a theorem-level contribution here beyond standard simplicial gluing?
15. How does this project connect to the broader Mental Space program without overclaiming a psychological interpretation?

## 18. Required deliverables

Return:

- `GLUING_CONCEPTS_MASTER_AUDIT.md`
- `FORMAL_GLUING_DEFINITIONS.md`
- `DECOMPOSITION_AND_SEPARABILITY.md`
- `GLUING_VS_UNFOLDING.md`
- `CHAIN_LEVEL_GLUING.md`
- `SHEAF_LOCAL_TO_GLOBAL_ANALYSIS.md`
- `FINITE_EXAMPLES.md`
- `LITERATURE_PRIORITY_MAP.md`
- `THEOREMS_COUNTEREXAMPLES_OPEN_PROBLEMS.md`
- reproducible scripts and machine-readable tables.

Also produce a concise research ledger with columns:

`Question | Status | Evidence | Counterexample | Next step`.

## 19. End-state assessment

At the end, classify the project into one of the following outcomes:

1. **Standard gluing only** — mathematically valid but largely existing topology.
2. **Useful new synthesis** — standard tools produce a coherent new concept-composition framework.
3. **New theorem-level structure** — one or more nontrivial results appear genuinely new.
4. **Requires additional structure** — simplices alone make gluing/decomposition too trivial, but labeled/logical/sheaf/CM structure repairs the problem.
5. **Unification fails** — gluing, unfolding, and disentanglement should remain separate theories.

Do not prefer unification merely because the 2015 thesis suggested it.

Finally identify the **single strongest theorem or finite classification problem** that should be attacked next.
