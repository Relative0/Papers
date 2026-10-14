# Formal Gluing Definitions

## 1. Recommended ontology

The 2015 thesis alternates between calling a concept a simplex-like unit and defining a concept as a connected simplicial complex. The cleanest modern repair is **not** to choose one and erase the other, but to separate levels.

**Atomic concept.** An atomic concept is a nonempty finite **labelled simplex**
\[
\sigma=\Delta(V_\sigma)=\{\tau:\tau\subseteq V_\sigma\},
\]
whose vertices carry declared semantic labels (attributes, predicates, variables, or other primitive features). The simplex asserts that the listed vertices participate jointly in one atomic conceptual episode/object. This is a modeling convention, not a psychological fact.

**Concept complex.** A conceptual/mental structure is a finite abstract simplicial complex \(K\). Its maximal simplices are atomic concepts; intersections encode shared sub-concepts/incidence. This retains the thesis's useful idea that concepts can themselves be assembled into a larger simplicial structure.

**Structured concept.** For nontrivial gluing and independence, the topological carrier should be enriched. The minimal useful schema is
\[
\mathcal C=(K,\lambda,\mathcal S),
\]
where \(K\) is a finite simplicial complex, \(\lambda\) is label/provenance data, and \(\mathcal S\) is an optional semantic layer (a Boolean relation/function, CM/LM truth tensor, presheaf/sheaf, or other constraint system). No theorem should depend on a semantic layer that has not been explicitly declared.

This is option 3 in the prompt: **a simplex as an atomic concept and a complex as a mental/conceptual structure**, with additional structure when the question is semantic rather than merely combinatorial.

## 2. Basic simplicial objects

An abstract simplicial complex on vertex set \(V\) is a downward-closed family \(K\subseteq 2^V\) containing \(\varnothing\). A simplex on \(S\subseteq V\) is \(\Delta(S)=2^S\). A subcomplex \(L\subseteq K\) is a downward-closed subfamily. The induced/full subcomplex on \(A\subseteq V\) is
\[
K|_A=\{\sigma\in K:\sigma\subseteq A\}.
\]

For two subcomplexes \(A,B\subseteq K\), their set-theoretic union and intersection are again subcomplexes. In particular, if \(K=A\cup B\), then \(A\cap B\) is the natural overlap object.

## 3. Default gluing: pushout along a specified overlap

Let
\[
D\xrightarrow{i}A,\qquad D\xrightarrow{j}B
\]
be simplicial embeddings. The **simplicial pushout** \(A\cup_D B\) is the categorical colimit of this span. When the maps are literal subcomplex inclusions, it is the ordinary union after identifying the common copy of \(D\).

The important property is negative as well as positive:

> **No-completion property.** A simplex is present in the pushout only because it came from \(A\) or \(B\) (after vertex identifications). The pushout does not invent cross-simplices whose vertices came from both sides.

This is exactly why two edges \(ab\) and \(bc\) glued at \(b\) form a path rather than a filled triangle, and why four triangular faces of a tetrahedron form its boundary rather than its 3-simplex interior.

### 3.1 When is a union of two simplices itself a simplex?

Let \(A=\Delta(S)\) and \(B=\Delta(T)\) be simplices and take the ordinary simplicial union. Then
\[
A\cup B\text{ is a simplex}\quad\Longleftrightarrow\quad S\subseteq T\text{ or }T\subseteq S.
\]

**Proof.** If one vertex set contains the other, the union is the larger simplex. Conversely, if neither contains the other, choose \(s\in S\setminus T\) and \(t\in T\setminus S\). A simplex on \(S\cup T\) would contain the edge \(\{s,t\}\), but that edge is in neither \(A\) nor \(B\), so it is absent from the union. ∎

Thus ordinary gluing of genuinely different concepts almost always yields a **general complex**, not one larger simplex.

## 4. Completion operations must be declared separately

If the intended cognitive operation is “glue pieces and then infer a larger atomic whole,” a second operation is required. Several mathematically inequivalent completions are possible.

| Completion | Input condition | Added structure | Key warning |
|---|---|---|---|
| Top-simplex filler | all proper faces of a specified \(\Delta^n\) are present | add the declared \(n\)-simplex | provenance/filler declaration is extra data |
| Flag/clique completion | a graph/1-skeleton | add every clique as a simplex | far stronger than ordinary gluing; may add many high faces |
| Horn filling | a simplicial-set horn \(\Lambda_k^n\to X\) | choose an extension \(\Delta^n\to X\) | fillers need not exist or be unique unless extra axioms hold |
| CW attachment | map \(S^{n-1}\to X\) | attach an \(n\)-cell | output is naturally a CW complex, not necessarily a simplicial complex without triangulation |
| Semantic closure | formulas/constraints plus a closure operator | add consequences | output depends on the chosen logic/closure system |

The completion policy should never be hidden inside the word “glue.”

## 5. Other gluing/composition notions

### 5.1 Join

For complexes \(K,L\) on disjoint vertex sets,
\[
K*L=\{\sigma\cup\tau:\sigma\in K,\tau\in L\}.
\]
The join **does** introduce all mixed simplices required by the definition. If \(K=\Delta(A)\) and \(L=\Delta(B)\), then
\[
\Delta(A)*\Delta(B)=\Delta(A\sqcup B).
\]
This makes join excellent for a notion of independent combinatorial factors, but dangerously weak if one begins with a simplex: every partition of its vertices yields a join decomposition.

### 5.2 Wedge

A wedge identifies chosen basepoints. It is useful for “share exactly one distinguished concept” but typically does not model attribute composition because it adds no mixed faces.

### 5.3 Products

Products depend on category. Geometric products of realizations, categorical products of abstract complexes, and products of simplicial sets are not interchangeable. They are better suited to independent coordinate systems than to the thesis's common-face examples.

### 5.4 Nerve

Given a family \(\{C_i\}\), the nerve \(N\) has a vertex for each \(C_i\) and a simplex \(\{i_0,\ldots,i_k\}\) exactly when the total intersection \(C_{i_0}\cap\cdots\cap C_{i_k}\) is nonempty. The nerve records **assembly/intersection pattern**, not the internal contents of each concept. Under good-cover hypotheses, it recovers the union's homotopy type.

### 5.5 Sheaf gluing

A presheaf \(\mathcal F\) assigns local data to regions and restriction maps to inclusions. It is a sheaf if compatible local sections over a cover glue to a **unique** global section. For ordinary Set-valued sheaves, equality on pairwise overlaps is the required compatibility condition; no independent triple-overlap axiom is needed once the restriction maps satisfy presheaf functoriality.

### 5.6 Cosheaf aggregation

A cosheaf reverses the variance: local information maps forward into larger regions and is reconstructed by a colimit condition. This is often conceptually closer to “aggregate parts into a whole,” whereas a sheaf is closer to “test whether local descriptions are globally coherent.” The two should not be conflated.

### 5.7 Boolean/logical composition

If concept semantics are encoded by Boolean relations or functions, operations such as conjunction may be defined independently of the simplicial carrier. The thesis's formulaic reconstructions belong here. A logical conjunction that recovers \(X\land Y\land Z\) is not automatically the same operation as union of three edges in a complex.


### 5.8 Comparative contract for the candidate gluing notions

The prompt asks that each candidate operation be checked against the same seven questions. The following table fixes those contracts. “Associative” means associative up to canonical isomorphism where the construction is categorical; “recoverable” refers to recovery from the **unmarked output** unless stated otherwise.

| Construction | Inputs | Compatibility data | Output type | Unintended/new faces? | Associative / order dependence | Functorial? | Are original components intrinsically recoverable? |
|---|---|---|---|---|---|---|---|
| common-face identification / simplicial pushout | complexes and maps \(D\to A,D\to B\) | maps must be simplicial; embeddings if literal common-face gluing is intended | simplicial complex | no completion; only images of input simplices survive, modulo identifications | binary pushouts compose through the corresponding finite colimit; parenthesization is harmless only after the diagram is fixed | yes, as a colimit construction | generally no; yes from a marked pushout diagram |
| pushout in simplicial sets | simplicial sets and simplicial maps | matching domain plus simplicial identities | simplicial set | no extra nondegenerate simplex merely from having its boundary; degeneracies are inherited categorically | canonical up to isomorphism as a colimit | yes | generally no without marked maps |
| literal union with prescribed \(\sigma\cap\tau=\rho\) | subcomplexes of an ambient complex | actual intersection must equal the declared overlap | simplicial complex | no | ordinary finite union is associative/commutative | functorial only relative to compatible ambient maps | generally no cover provenance from the union alone |
| join \(K*L\) | complexes on disjoint (or renamed-disjoint) vertices | disjoint factor supports | simplicial complex | **yes by design**: every cross-union \(\sigma\cup\tau\) is inserted | associative and commutative up to canonical isomorphism | yes | finest join factors can be canonical; coarse factors need not be unique |
| categorical/geometric product | objects in a declared category | coordinate maps; category must be fixed | product object; realization may not be simplicial without subdivision | not “faces” in the join sense; product cells/simplices depend on model | associative up to isomorphism | yes | factor recovery is a separate prime-factor problem and can fail to be unique in broad categories |
| wedge | pointed objects | chosen basepoints | pointed complex/space | no mixed faces beyond the identification | associative up to pointed isomorphism | yes for pointed maps | basepoint and wedge summands need not be intrinsic in arbitrary output |
| general colimit | a diagram of objects/morphisms | the full diagram | object of the chosen category | exactly those forced by that category's colimit, not a generic closure | diagram-independent parenthesization when computing the same colimit | yes | no in general; the diagram is extra provenance |
| CW attachment | \(X\), an \((n-1)\)-sphere and attaching map | continuous attaching map | CW complex | **yes by declaration**: a new \(n\)-cell is added | multiple attachments are order-independent only under explicit hypotheses/diagram formulations | functorial only for maps compatible with attaching data | attaching data are not normally determined by the unmarked result |
| horn filling | horn map \(\Lambda_k^n\to X\) | a chosen extension must exist | simplicial set with/through a filler | **yes by declaration**: an \(n\)-simplex filler | choice-dependent unless fillers are specified or unique | natural only in structures with coherent chosen fillers | not if several fillers exist |
| nerve | a family/cover \(\{U_i\}\) | finite-intersection incidences | index simplicial complex | simplices encode nonempty total intersections | independent of ordering of the index set up to relabeling | functorial for suitable cover maps | no; internal contents of \(U_i\) are discarded |
| flag/clique closure | graph or 1-skeleton | none beyond the graph | flag complex | **yes**, every clique becomes a simplex | deterministic/idempotent closure | yes for graph maps that induce simplicial maps | the pre-closure declaration of higher faces is lost |
| sheaf gluing | sheaf sections \(s_i\in F(U_i)\) | equality on pairwise overlaps | a global section, not a carrier simplex | not applicable to carrier faces | unique and order-independent once the cover is fixed | yes under morphisms of sheaves/sites | locals are recovered by restriction from the global section on the same cover |
| cosheaf aggregation | local cosheaf data over a cover | structure maps and the cosheaf colimit condition | global aggregate | not applicable to carrier faces | categorical colimit behavior | yes | generally not without injections/provenance; cosheaf axiom is about assembly, not factor recovery |
| Boolean/logical composition | formulas/relations/functions | shared-variable semantics and chosen connective/composition | formula/function/relation | may create semantic interaction terms, not geometric faces | depends on connective; \(\land,\lor,\oplus\) are associative, arbitrary compiler/composition need not be | syntax/semantic-map dependent | factor recovery is a Boolean/relational factorization problem, generally not unique without a prime criterion |

Two consequences are important. First, **pushout/union, completion, and join have different face-creation policies** and therefore cannot be alternate notations for one operation. Second, recoverability is usually a property of a marked diagram or a separate factorization theorem, not of colimits themselves.

## 6. Higher-order concept

No single historical use of “order” is mathematically stable: the thesis uses simplicial dimension, number of fixed attributes, p-adic depth, and logical conjunction in related ways. The modern project should use typed notions:

- **simplicial order**: \(\dim \sigma\) or \(\dim K\);
- **attribute order**: number/depth of semantic attributes;
- **assembly order**: position in a declared colimit/composition diagram;
- **logical order**: arity/complexity of the formula or relation.

The most useful neutral definition is:

> A **higher-order concept relative to a diagram** \(D\) is a structured object \(C\) equipped with a specified universal/semantic assembly map from the lower-order inputs, usually a pushout/colimit followed, if desired, by an explicitly named completion functor.

This makes “higher” relational rather than pretending that every dimension measure agrees.

## 7. Recoverability and provenance

A categorical colimit is unique up to isomorphism, but a bare output object generally does not determine the input diagram that produced it. Therefore define two variants:

**Unmarked gluing:** return only \(C=A\cup_D B\).

**Marked gluing:** return \((C;\iota_A,\iota_B,\iota_D)\), retaining the distinguished images of the pieces and overlap.

Marked gluing is the appropriate notion if “disentanglement” is supposed to recover the historical constituents. Unmarked gluing is appropriate only when decomposition is to be inferred intrinsically by a canonical factorization theorem.

## 8. Proposed category for the next theorem phase

A minimal research category \(\mathbf{SConcept}\) can have objects
\[
(K,\lambda,R)
\]
where \(K\) is a finite complex, \(\lambda\) labels vertices/faces, and \(R\) is a finite relation on a declared attribute set (or, in the CM specialization, a Boolean truth tensor). Morphisms should preserve faces and labels and map satisfying assignments consistently.

A richer variant replaces \(R\) by a presheaf/sheaf \(\mathcal F\) on the face poset. The project should prove results first for one precise category rather than allowing all semantic layers simultaneously.

## 9. Priority conclusion

All basic constructions in this document are standard mathematics. In particular, category-theoretic conceptual blending has already been explicitly modeled via colimits/pushouts/amalgams, and modern work continues that program. The project contribution cannot be “concepts can be glued by pushouts.” Its plausible contribution is a **carefully delimited structured concept calculus that compares several inequivalent gluing and factorization notions and proves when they agree**.
