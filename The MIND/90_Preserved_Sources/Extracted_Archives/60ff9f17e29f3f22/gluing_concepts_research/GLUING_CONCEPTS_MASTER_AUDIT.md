# Gluing Concepts — Master Mathematical Audit

**Working title:** *Gluing Concepts: Composition, Reconstruction, and Clean Decomposition in Simplicial Mental Spaces*  
**Historical source:** Brian Droncheff, *On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces* (2015)  
**Audit date:** 28 September 2026  
**Status:** research audit and finite-computation package; not a publication or novelty claim.

---

## 1. Executive determination

The historical thesis contains a real and recoverable mathematical research seed, but it combines several operations that must be separated before the program becomes rigorous:

1. **simplicial gluing:** assemble subcomplexes along specified overlaps;
2. **completion/filling:** add a higher-dimensional simplex/cell not present in the pieces;
3. **local-to-global semantic gluing:** reconstruct globally coherent data from compatible restrictions;
4. **factorization/separability:** decompose a structured whole into genuinely independent factors.

The central correction is that these operations are **not equivalent**. In particular, the union of all faces of a simplex is generally its boundary, not the filled simplex, and decomposition into faces is not decomposition into independent factors.

### Recommended ontology

Adopt the two-level model requested in option 3:

- an **atomic concept** is a finite labelled simplex;
- a **conceptual/mental structure** is a finite simplicial complex assembled from atomic concepts;
- any nontrivial claim about independence, semantics, or recoverability uses a **structured concept**
  \[
  \mathcal C=(K,\lambda,\mathcal S),
  \]
  where \(K\) is the carrier complex, \(\lambda\) is label/provenance data, and \(\mathcal S\) is a declared semantic layer such as a finite relation, Boolean/CM object, or sheaf.

This preserves both historical uses of “concept” without silently identifying a simplex with an arbitrary connected complex.

### End-state assessment

\[
\boxed{\textbf{Outcome 4 — Requires additional structure}}
\]

Bare simplices make join decomposition too permissive: every vertex partition of a simplex gives a join factorization. Ordinary simplicial gluing is standard and non-completing. The project becomes mathematically substantive only after labels, logical constraints, semantic relations, provenance, sheaf data, or CM structure are added.

The most promising next result is not another gluing construction. It is the **succinct structured factorization problem**: compute the finest partition across which both a compact simplicial carrier and an intensionally represented Boolean/CM semantic layer factor, without expanding the full truth table.

---

## 2. Historical recovery: what the thesis actually says

The thesis is treated here as a fixed historical source, not as mathematical authority. The following source map is also supplied machine-readably in `data/thesis_source_map.csv`.

| Thesis location | Topic | Classification | Historical content | Modern assessment |
|---|---|---|---|---|
| PDF pp. 26–29 | simplices, complexes, chains | precise setup | Introduces simplicial/chain language and foreshadows concepts as complexes. | Retain standard definitions only; cycles are not automatically concepts/symmetries. |
| p. 50 | \(X\land Y\) as higher-order concept | historical intuition | Calls a conjunction a higher-order concept and suggests distinguishing constituents by measurement. | Semantic composition seed; not yet simplicial gluing. |
| p. 52 | definition of concept | precise definition + unsupported claims | Defines a concept as a connected simplicial complex with pairwise edge connectivity, then makes topological claims. | Best modernized as an atomic-simplex/complex distinction, with topology stated separately. |
| pp. 54–55 | concept order / p-adic hierarchy | intuition + examples | Order tracks fixed attributes / p-adic depth. | Keep distinct from simplicial dimension. |
| pp. 56–58 | Matte-Blanco unfolding / \(\partial\) | intuition + thesis definition | Defines a logical “unfolding” that omits a vertex, negates it, and disjoins terms. | This is **not** the standard simplicial boundary. |
| pp. 59–60 | triangle unfolding; green-box | worked examples | Decomposes logical simplices into differentiated lower-order pieces. | Separate logical transformation from geometric face exposure. |
| p. 61 | explicit gluing motivation | historical intuition | After unfolding, asks to build lower-dimensional expressions back up by “gluing” or “integrating.” | This is the core recoverability question. |
| pp. 62–63 | triangle reconstruction; tetrahedron; “integrator” | worked examples + unsupported claim/open question | Conjoins side formulas to recover \(X\land Y\land Z\); says four triangular faces build a tetrahedron and asks for an integrator, mentioning CW complexes. | Boolean reconstruction is distinct from simplicial union; four faces give \(\partial\Delta^3\), so a filler is extra data. |
| p. 66 | shared p-adic attributes | intuition | Uses intersections to encode common attributes. | Natural overlap object, but representation-specific padding must not be universalized. |
| pp. 74–80 | ProLT, presheaves, restrictions | definitions + proposed extension | Introduces presheaf-like restrictions and aims to build larger complexes by gluing smaller concepts. | Genuine sheaf gluing requires existence and uniqueness, not just restrictions. |
| p. 82 | relative topology and compatible sections | historical intuition + close modern analogue | Proposes gluing compatible sections into sheaves or higher-order concepts. | Closest sound analogue is ordinary sheaf descent. |
| pp. 86–87 | overlapping concepts; “pink flower” | worked example + unsupported recoverability | Unfolds overlapping concepts and says partition pieces can be glued back. | Requires a specified semantic gluing map and retained provenance. |
| pp. 88–91 | logical triangles/squares | worked diagrams + possible analogue | “Glues” logical triangles sharing operators into exact squares; some pairs fail. | Treat as algebraic/diagrammatic compatibility, not automatically as a simplicial pushout. |

### Historical conclusion

There are **two distinct gluing seeds** in the thesis:

- a geometric/logical **face-reconstruction** seed (triangle/tetrahedron/integrator);
- a semantic **compatible-sections** seed (presheaf/sheaf/local-to-global).

They should be developed separately and compared only after each is formalized.

---

## 3. What should “gluing” mean?

No single operation covers all intended cases. The default should be the least committal construction.

### 3.1 Default: pushout along a specified common subcomplex

Given embeddings
\[
D\hookrightarrow A,\qquad D\hookrightarrow B,
\]
define gluing as the pushout \(A\cup_D B\). When these are literal subcomplex inclusions, it is the ordinary simplicial union with the overlap identified.

**Key property:** it is **non-completing**. A new simplex does not appear merely because all its vertices are present in the pushout.

This is the mathematically clean model of “identify exactly the shared part.” It is associative up to the usual canonical isomorphism when organized as a colimit diagram, functorial in the diagram, and recoverable only if the input embeddings/provenance are retained.

### 3.2 Operations that must remain distinct

| Operation | Appropriate use | Does it add mixed/higher simplices? | Recoverability |
|---|---|---:|---|
| union/pushout along inclusion | exact common-face assembly | no | only with marked subobjects or intrinsic factor theorem |
| join | free combination of disjoint structural factors | yes, all cross-faces | canonical finest factors exist, but simplex case trivializes |
| wedge | share one basepoint | no mixed faces | basepoint-dependent |
| product | coordinate/product structure | category-dependent | can represent independent coordinates |
| colimit | general diagrammatic assembly | depends on category | diagram not determined by bare colimit |
| CW attachment | add a cell along boundary map | yes, declared cell | attachment map is essential data |
| horn filling | simplicial-set completion | adds chosen filler | existence/uniqueness need extra axioms |
| flag/clique completion | infer simplices from 1-skeleton cliques | potentially many | destroys information about which higher faces were explicit |
| nerve | record intersection pattern of pieces | creates an index complex | loses internal content of pieces |
| sheaf gluing | coherent local semantic data | produces global section, not carrier simplex | unique if sheaf axiom holds |
| cosheaf aggregation | aggregate local contributions | colimit-like | depends on cosheaf structure |
| Boolean conjunction / semantic composition | combine constraints/formulas | semantic, not automatically geometric | factorability depends on logic |

### 3.3 When does ordinary gluing produce one larger simplex?

For two simplices \(\Delta(S),\Delta(T)\), their ordinary union is a simplex iff one is contained in the other. If neither contains the other, some edge between a vertex unique to each side is missing. Therefore a higher simplex almost never arises from nontrivial ordinary gluing alone.

If “higher-order concept” is intended to mean a new filled simplex, the theory requires a **separate completion/filler operator**.

---

## 4. Higher-order concepts

The thesis uses “order” in several incompatible senses. The modern theory should type them explicitly:

- **simplicial order:** dimension;
- **attribute order:** number/depth of constrained semantic attributes;
- **assembly order:** position in a composition/colimit diagram;
- **logical order:** formula arity/complexity;
- **global-section order:** a global semantic state determined by a cover.

The most fertile formal definition is relational:

> A higher-order concept relative to a diagram is a structured object equipped with a declared assembly map from lower-order inputs, typically a colimit/pushout followed, when desired, by an explicitly named completion or semantic closure.

This avoids pretending these order notions are equivalent.

---

## 5. Clean gluing criteria

### 5.1 Simplicial carrier

A clean common-face gluing diagram should state:

1. the intended overlaps \(C_i\cap C_j\);
2. embeddings are injective away from the declared identifications;
3. the colimit lies in the intended category;
4. no completion is silently applied;
5. constituent images remain marked if historical recovery matters.

For inclusions of subcomplexes, these are straightforward and pairwise/higher intersections are inherited from the actual subobjects.

### 5.2 Semantic labels

Labels/attribute assignments must agree on identified vertices/faces. If the semantic layer is a presheaf/sheaf, restrictions must be functorial.

### 5.3 Sheaf compatibility

For a genuine Set-valued sheaf \(\mathcal F\) and cover \(U=\bigcup_iU_i\), the exact condition is
\[
s_i|_{U_i\cap U_j}=s_j|_{U_i\cap U_j}\quad\forall i,j.
\]
Then there exists a **unique** \(s\in\mathcal F(U)\) restricting to all \(s_i\). Pairwise agreement is sufficient in ordinary Set-valued sheaf theory; separate triple-overlap coherence is not an additional axiom.

A presheaf can fail this property; Example D below gives an exact failure.

---

## 6. Decomposition and “disentanglement”

The project should use **factorization/separability** as the neutral vocabulary.

Three problems must be separated:

1. **face decomposition:** expose lower-dimensional faces;
2. **assembly decomposition:** recover a chosen cover/pushout diagram;
3. **independent-factor decomposition:** partition variables/vertices into blocks with no mixed interaction according to a declared criterion.

Only the third is strong disentanglement.

### 6.1 Structural independence by join

For \(V=A\sqcup B\), define
\[
K\text{ structurally factors across }A|B
\iff
K=K|_A*K|_B.
\]
This says every allowed face on one side can combine freely with every allowed face on the other.

The exact criterion is that no minimal nonface crosses the partition. Connected components of the minimal-nonface hypergraph yield the canonical finest join factors.

### 6.2 Why a simplex is too weak

A simplex has no minimal nonfaces, so for every partition
\[
\Delta(V)=*_{B\in\Pi}\Delta(B).
\]
Thus a bare simplex treats **every partition** as structurally independent. This is the central reason the project ends in Outcome 4 rather than a simplex-only theory.

### 6.3 Semantic independence by finite relation

For admissible assignments \(R\) across attribute blocks, define independence by Cartesian product factorization. The extensional finite relation has a canonical prime factorization in established database theory.

### 6.4 CM/Boolean separability

The supplied current CM/LM manuscript proves the fixed-bipartition theorem
\[
f(a,b)=g(a)\land h(b)
\iff
\operatorname{rank}_{\mathbb F_2}[f]_{A|B}\le1,
\]
and identifies ordinary \(\mathbb F_2\)-rank with the minimum XOR sum of conjunctive factors. This is immediately useful as a semantic interaction measure, but broad Boolean decomposition is classical, so priority claims must remain narrow.

### 6.5 Cross-layer criterion

A robust clean decomposition should require **the same partition** to factor both the simplicial carrier and the semantic layer. This prevents a simplex's trivial structural factorability from deciding the semantics.

For an extensional finite relation, if \(\Pi_K\) is the finest structural partition and \(\Pi_R\) the prime semantic partition, the finest simultaneous partition is their **least common coarsening**. This is proved in `DECOMPOSITION_AND_SEPARABILITY.md`.

The package also contains a four-attribute example where both layers factor nontrivially but across crossing partitions, so the structured object has no nontrivial simultaneous factorization.

---

## 7. Gluing versus unfolding

The thesis's historical \(\partial\) should not be reused as the standard chain boundary. Use separate notation:

- \(\partial_{\mathrm{ch}}\): homological boundary;
- \(U\): unfolding/restriction;
- \(G\): gluing/colimit;
- \(F\): filler/completion.

### 7.1 Plain gluing is not an inverse

For a tetrahedron, deleting the top simplex exposes its four triangular faces. Re-union of those faces gives only the boundary:
\[
G(U(\Delta^3))=\partial\Delta^3\neq\Delta^3.
\]

### 7.2 A partial inverse is possible with provenance

If an unfolded object is **marked** as “the boundary of this labelled simplex,” a filler can reinsert the top simplex. That gives a restricted partial inverse on a declared subcategory, not an intrinsic inverse on bare complexes.

### 7.3 Sheaf restriction/gluing is the cleanest inverse paradigm

If “unfolding” is reinterpreted as restriction of a global semantic section to a cover, then the sheaf axiom reconstructs the unique global section from its compatible restrictions. That is the strongest rigorous form of the thesis's inverse intuition presently available.

It still does **not** imply that the global section factors into independent constituents.

---

## 8. Chain-level gluing

For \(K=A\cup B\) and \(D=A\cap B\):
\[
0\to C_\bullet(D)
\to C_\bullet(A)\oplus C_\bullet(B)
\to C_\bullet(K)\to0
\]
with maps \(x\mapsto(x,-x)\) and \((a,b)\mapsto a+b\). This yields Mayer–Vietoris.

The exact sequence gives a rigorous bridge between overlap and global topology. Connecting homomorphisms can expose cycles created by the gluing pattern. Relative homology and mapping cones can measure what one piece adds beyond the overlap.

However, homology is not a complete independence detector. The package gives a contractible but join-irreducible four-vertex complex.

Likewise, degreewise vector-space splitting over a field is noncanonical and therefore too weak to count as conceptual independence.

---

## 9. Nerve analysis

For a cover \(\{C_i\}\), the nerve has:

- one vertex per constituent concept;
- an edge for nonempty pairwise overlap;
- a \(k\)-simplex for a nonempty \((k+1)\)-fold intersection.

It is an excellent **assembly/intersection invariant**. Under a good-cover hypothesis, it recovers the union's homotopy type.

It is not a full reconstruction of the internal concepts: two covers with the same nerve can have very different piece contents. The current ProLT manuscript correctly treats its relation nerve as presentation-dependent; that caution should carry over here.

---

## 10. Sheaf/cosheaf reconstruction

The thesis's late presheaf language is more mathematically promising for reconstruction than its tetrahedral picture.

### Sheaf role

A sheaf answers:

> Can locally specified concept states coexist as one unique global state?

This is a **coherence** question.

### Cosheaf role

A cosheaf is better suited to:

> Can local contributions be aggregated into a global object by a colimit-type rule?

This is an **aggregation** question.

### Independence is a third question

Neither coherence nor aggregation implies factorization. A complete structured theory can therefore use:

- simplicial carrier: overlap/assembly geometry;
- sheaf: semantic consistency;
- cosheaf: aggregation;
- relation/Boolean/CM layer: factorization and interaction.

This four-way separation is preferable to asking one structure to do all jobs.

---

## 11. Exact Examples A–G

All simplicial computations are reproduced by `code/gluing_audit.py`; exact records are in `data/finite_examples.json/.csv` and `data/diagnostics.json`.

### Example A — two concepts glued along a vertex

Facets: \(ab,bc\).  
Result: a path with \(f=(3,2)\), \(\beta=(1,0)\).  
Recoverability: exact if the two embedded input edges are marked; otherwise the historical cover is provenance.

### Example B — two filled triangles glued along an edge

Facets: \(abc,bcd\), overlap \(bc\).  
Result: a triangulated disk with \(f=(4,5,2)\), \(\beta=(1,0,0)\).  
Mayer–Vietoris is homologically trivial because all pieces and the union are contractible, although the chain-level identification is nontrivial.

### Example C — tetrahedron from triangular faces

Four-face union:
\[
\partial\Delta^3,
\qquad
f=(4,6,4),
\qquad
\beta=(1,0,1).
\]
Filled tetrahedron:
\[
\Delta^3,
\qquad
f=(4,6,4,1),
\qquad
\beta=(1,0,0,0).
\]
All four faces are insufficient under plain union. Three faces form a horn-like disk; under a declared horn-filling condition they may admit a filler. Under flag completion, the \(K_4\) 1-skeleton alone already forces the tetrahedron.

### Example D — compatible local data with no global gluing

Discrete \(X=\{p,q\}\); presheaf \(P(W)=\mathbb Z\) on nonempty opens and \(P(\varnothing)=\{*\}\). Local sections 0 and 1 agree vacuously on the empty overlap but no global integer restricts by identity to both.

This is possible for a presheaf; it is excluded by the sheaf axiom.

### Example E — clean factorization

Four-cycle with minimal nonfaces \(a_0a_1\) and \(b_0b_1\).  
It is exactly
\[
K|_{\{a_0,a_1\}}*K|_{\{b_0,b_1\}},
\]
with \(\beta=(1,1)\).

### Example F — irreducible interaction

On the same four vertices, minimal nonfaces \(a_0a_1,a_1b_0,b_0b_1\) connect the interaction hypergraph. The resulting path is contractible but has no nontrivial join factorization.

### Example G — smallest nonunique coarse join decomposition

The filled triangle has three distinct unordered binary join decompositions, but one unique finest decomposition into singleton vertices. This distinguishes coarse nonuniqueness from canonical prime decomposition.

---

## 12. Exhaustive finite computation and speedups

The program enumerated all labeled simplicial complexes **using all vertices** through \(n=5\):

| vertices | complexes | join-indecomposable | nontrivially join-decomposable | unordered partition checks | failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 2 | 0 |
| 3 | 9 | 5 | 4 | 27 | 0 |
| 4 | 114 | 84 | 30 | 798 | 0 |
| 5 | 6,894 | 6,348 | 546 | 103,410 | 0 |

Totals: **7,020 complexes**, **104,237 bipartition checks**, zero disagreements with the minimal-nonface criterion, and zero failures of finest-factor reconstruction.

### Speedups before brute force

1. **Do not enumerate partitions to find the finest structural factors.** Compute minimal nonfaces, connect co-occurring vertices, and take components.
2. **Flag complexes:** join decomposition reduces to connected components of the complement graph.
3. **Use isomorphism classes/canonical generation** for larger finite classification rather than labeled Dedekind enumeration.
4. **Semantic relation:** use relational prime-factorization algorithms rather than scanning every attribute partition.
5. **Fixed CM cut:** use ordinary \(\mathbb F_2\) rank directly.
6. **Cross-layer decomposition:** compute each prime partition first, then take their least common coarsening instead of testing every common partition.

The computational campaign validates the formal criteria; it does not itself establish novelty.

---

## 13. Literature/priority conclusion through 2026

The full source-by-source audit is in `LITERATURE_PRIORITY_MAP.md` and `data/literature_priority_map.csv`.

The closest priority barriers are:

- conceptual blending already modeled categorically by colimits/pushouts/amalgams;
- sheafification already proposed as a universal construction for semantic compositionality;
- unique finest join decompositions already appear in current simplicial/set-family literature;
- Boolean function decomposition is classical;
- relational prime product factorization has polynomial algorithms;
- Formal Concept Analysis has explicit mature theories of factors, concept-lattice decompositions, and recent independent-subcontext work.

Therefore the project should **not** claim novelty for pushout gluing, sheaf gluing, join factorization, Boolean decomposition, or “concept decomposition” broadly.

What survives is a potentially valuable synthesis: **require structural, semantic, and eventually local-to-global layers to agree on the same decomposition**, and study the algorithmics/obstructions of that agreement.

---

## 14. Answers to the project's 15 required questions

1. **Cleanest definition of a simplicial concept?**  
   Atomic labelled simplex + concept complex + optional semantic layer. This resolves the thesis's simplex/complex ambiguity without deleting either use.

2. **What does it mean to glue concepts?**  
   By default, a pushout/colimit along explicitly declared overlap maps. Completion is a second operation.

3. **What compatibility is necessary/sufficient?**  
   For the carrier: well-typed overlap maps/identifications. For labels: equality/compatibility on identified data. For sheaves: matching sections on pairwise overlaps, with the sheaf axiom supplying unique gluing.

4. **When does gluing produce a higher-order simplex?**  
   Plain union of two simplices only when one contains the other. Nontrivial higher simplices require a completion rule such as a declared filler, flag closure, or horn filler.

5. **When can constituents be recovered?**  
   Always from a **marked** gluing diagram; generally not from the bare colimit. Intrinsic recovery requires a canonical factorization theorem.

6. **Correct notion of independent concepts?**  
   No unqualified notion. Use structural join independence, semantic Cartesian independence, CM fixed-cut rank separability, or probabilistic independence only in their proper domains.

7. **When is a higher concept separable/factorizable?**  
   When the declared layer factors across a partition; for robust structured separability, require the same partition across carrier and semantics.

8. **When is it irreducible?**  
   When its canonical finest admissible partition is one block. The minimal-nonface hypergraph detects this for structural join factorization.

9. **Is decomposition unique/canonical?**  
   Coarse decompositions need not be unique. The finest join decomposition and prime relational product decomposition are canonical in their respective settings. Their finest simultaneous partition is the least common coarsening.

10. **Is unfolding inverse to gluing?**  
    Not on bare complexes. A partial inverse is possible with declared filler/provenance; sheaf restriction/gluing gives a genuine local-to-global inverse statement at the section level.

11. **Faces versus independent factors?**  
    Fundamentally different. Boundary faces overlap; independent factors require free recombination/product structure.

12. **Do homology/Mayer–Vietoris/cohomology detect interaction?**  
    They can detect topological obstruction/attachment, but not all factorization. Contractible irreducible examples show homology is incomplete for independence.

13. **Can Correspondence Matrices help?**  
    Yes. The current CM flattening theorem gives an exact fixed-cut rank criterion for conjunctive/XOR separability. Its advantage should be studied algorithmically rather than assumed.

14. **Is there a theorem-level contribution beyond standard gluing?**  
    Not yet established as novel. The cross-layer least-common-coarsening theorem is useful but elementary once prime factors are known. The promising theorem-level work is succinct structured factorization and possibly sheaf/CM interaction.

15. **Connection to the broader Mental Space program?**  
    Strong as a mathematical architecture: simplicial carrier for incidence, ultrametric/other geometry for similarity, sheaf/cosheaf for local-global information, and Boolean/CM constraints for factorization. Psychological interpretation should remain a modeling hypothesis until independently justified.

---

## 15. The strongest theorem / finite classification problem to attack next

### Succinct Structured Factorization

**Input:**

- a finite simplicial complex \(K\) in a compact representation (facets, minimal nonfaces, flag graph, etc.);
- a Boolean semantic object \(f\) over the same attributes, represented intensionally by CNF/DNF/circuit/ANF or CM/LM data.

**Goal:** output the unique finest partition \(\Pi\) on which **both** layers factor, or certify that the one-block partition is the only simultaneous factorization, **without enumerating the full truth relation**.

The extensional relation case is already reduced to:

1. canonical simplicial join partition;
2. prime relational product partition;
3. least common coarsening.

The real mathematical problem is the succinct semantic case. The next paper-worthy result should establish either:

- a polynomial/FPT algorithm for a substantial class with a canonical invariant, or
- hardness for the general case together with a sharp tractable frontier.

This is more promising than extending brute-force counts to six vertices without a conjecture.

---

## 16. Final project classification

### Outcome 4 — Requires additional structure

The unification does **not** fail, but it must be conditional:

\[
\boxed{
\text{carrier gluing}
+\text{explicit completion}
+\text{semantic coherence}
+\text{factorization structure}
}
\]

is a coherent program.

What should be abandoned is the stronger historical identification

\[
\text{gluing faces}
=\text{recovering a filled simplex}
=\text{unfolding inverse}
=\text{independent-factor decomposition}.
\]

Those equalities are false in general. Once they are separated, the research direction becomes substantially cleaner and, in the structured/succinct factorization problem, potentially mathematically productive.

---

## 17. Package map

Required deliverables:

- `GLUING_CONCEPTS_MASTER_AUDIT.md` — this document.
- `FORMAL_GLUING_DEFINITIONS.md` — precise ontology and gluing operations.
- `DECOMPOSITION_AND_SEPARABILITY.md` — structural/semantic/CM factorization and simultaneous partition theorem.
- `GLUING_VS_UNFOLDING.md` — why gluing, filling, unfolding, and factorization differ.
- `CHAIN_LEVEL_GLUING.md` — exact chain sequence, Mayer–Vietoris, relative homology, mapping-cone interpretation.
- `SHEAF_LOCAL_TO_GLOBAL_ANALYSIS.md` — matching families, presheaf counterexample, sheaf/cosheaf roles.
- `FINITE_EXAMPLES.md` — exact A–G examples and finite enumeration.
- `LITERATURE_PRIORITY_MAP.md` — structure-based literature/priority audit through 2026.
- `THEOREMS_COUNTEREXAMPLES_OPEN_PROBLEMS.md` — consolidated theorem/counterexample/open-problem ledger.
- `data/research_ledger.csv` — concise requested ledger.
- `data/thesis_source_map.csv` — historical source map.
- `data/*.json/.csv` — exact machine-readable computation outputs.
- `code/gluing_audit.py` — reproducible standard-library computation.
