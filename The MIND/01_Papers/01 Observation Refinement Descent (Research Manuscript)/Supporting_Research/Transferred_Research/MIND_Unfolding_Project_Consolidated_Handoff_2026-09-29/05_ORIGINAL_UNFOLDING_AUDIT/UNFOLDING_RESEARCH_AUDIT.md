# Mathematical Reconstruction of Matte-Blanco's Unfolding Function and Mental Space
## Independent research audit of the 2015 thesis

**Primary historical source:** Brian Droncheff, *On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces* (Master's thesis, 2015).

**Audit date:** 28 September 2026.

## Executive finding

There is a mathematically valuable core in the thesis, but it is not the chain-complex theory claimed there. The strongest recoverable structure is this:

> **A concept can be represented by structured incidence data; an unfolding step is best modeled as a refinement or distinction operation on that data; the genuine topological boundary operator must remain separate.**

The thesis's logical operator

\[
\partial[v_0,\ldots,v_n]
 = \bigvee_{j=0}^n \neg v_j\wedge[v_0,\ldots,\widehat v_j,\ldots,v_n]
\]

is mathematically meaningful once a representation is fixed. On a positive conjunction it is the Boolean predicate **"exactly one factor has been switched off"**. Equivalently, its individual summands are **gated Boolean partial derivatives** of the conjunction. It is also a directed one-step Hamming-neighborhood operator on a Boolean cube, or an incidence operator between consecutive ranks of a Boolean lattice.

However, as written in the thesis it is **not** a simplicial boundary, it is **not** intrinsically defined on Boolean functions modulo logical equivalence, its repeated action is not fully defined, and its natural OR-valued version does **not** satisfy \(\partial^2=0\). A clean square-zero operator appears only after a principled change of algebra: linearize the same incidence relation over \(\mathbf F_2\), or add the usual incidence signs over a general coefficient ring. That repaired object is a genuine simplicial cochain differential, but it must not be presented as identical to the original thesis operator.

The thesis's gluing intuition is also worth preserving, but the printed Boolean gluing example is false and the general claim requires missing compatibility/filler data. The right rigorous replacements are **colimits of subcomplexes, nerves, Čech constructions, sheaf/cosheaf descent, or explicit filler rules**. In particular, the proper faces of a simplex reconstruct its boundary, not automatically the filled simplex.

The thesis's proposed identification of cycles with symmetry does not survive. Homology measures cycles modulo boundaries; symmetry is naturally measured by an automorphism group or group action. Highly symmetric contractible complexes can have no nontrivial homology, while a complex can have a nontrivial cycle and trivial automorphism group.

The best modern architecture is therefore a two-operator theory:

\[
 d:C_n(K_k)\to C_{n-1}(K_k),\qquad d^2=0,
\]

for genuine topology, and

\[
 U_k:C_\bullet(K_k)\to C_\bullet(K_{k+1})
\]

for observation/refinement. If \(U_k\) is induced by a simplicial map, then

\[
 dU_k=U_kd
\]

automatically, and it gives a well-defined map on homology. The mapping cone

\[
H_\bullet(\operatorname{Cone}(U_k))
\]

then becomes a precise defect signature of what the unfolding step changes homologically.

---

# 1. Faithful reconstruction of the thesis proposal

This section reconstructs the thesis before repairing it.

## 1.1 Mental Space

The thesis first defines the **Mind** as comprising the unconscious and conscious, then defines a **Mental Space** as a representation of the Mind by a set of points endowed with a topology (§2, around PDF pp. 50–51).

It subsequently treats the points of Mental Space as **concepts** and attempts to equip conscious and unconscious domains with different topological behavior.

### Status

- **Standard mathematics used:** topological space.
- **Thesis-specific modeling choice:** mental objects are points of a topology.
- **Psychological interpretation:** topology is intended to encode distinguishability and relations among concepts.
- **Assessment:** **repairable / promising** as an abstract modeling choice; no particular topology follows from Matte-Blanco without additional axioms or data.

## 1.2 Concepts

In §2.1 the thesis defines a **concept** as a connected simplicial complex in which every 0-simplex is connected to every other by a 1-simplex, with no multiple edges. It then defines a category `Con` whose objects are concepts and whose morphisms are intended to be inclusions.

This definition mixes several levels:

1. an abstract simplicial complex;
2. its 1-skeleton;
3. a topological realization;
4. a mental/cognitive interpretation.

The pairwise-edge condition makes the 1-skeleton a complete graph, but it does **not** imply that all higher-dimensional simplices are present. For example, the boundary of a triangle has all three pairwise edges but does not contain the filled 2-simplex.

The proposed category is salvageable only if the inclusion relation includes equality; otherwise strict inclusion would omit identity morphisms.

### Status

- **Standard mathematics:** simplicial complexes, subcomplex inclusions, categories.
- **Thesis-specific definition:** concepts are complete-1-skeleton connected complexes.
- **Defect:** the thesis later treats pairwise connectivity as though it often determined higher simplices.
- **Assessment:** **repairable**, but the complete-graph requirement should not be built into the general definition of concept.

## 1.3 Hierarchical concepts and ultrametric balls

The thesis adapts Khrennikov's idea of categories encoded by \(p\)-adic/ultrametric balls. A concept of order \(k\) is described by fixing the first \(k\) attributes/digits. The kitten/cat example says that `kitten` carries an extra distinguishing attribute relative to `cat`: kitten implies cat, but cat does not imply kitten (§2.2, PDF p. 58).

This is one of the thesis's strongest intuitions: **differentiation corresponds to resolving more coordinates or attributes**.

That intuition is mathematically natural in:

- prefix trees and ultrametric balls;
- partitions and refining equivalence relations;
- filtrations of information;
- formal concept analysis;
- observation maps whose fibers encode indistinguishability.

The later claim that an ultrametric topology collapses to the indiscrete topology is false. Ultrametric spaces are metric spaces and hence Hausdorff; their balls are characteristically nested/disjoint and are often clopen. The useful idea is **hierarchical indistinguishability at a fixed observational scale**, not topological indiscreteness.

### Status

- **Hierarchical balls as categories:** **sound as a modeling construction**, with strong antecedents.
- **Ultrametric implies indiscrete topology:** **false**.
- **Observation-scale equivalence classes:** **promising repair**.

## 1.4 Matte-Blanco's unfolding as reconstructed by the thesis

Section 2.2 quotes/paraphrases Matte-Blanco's idea that conscious thought introduces additional asymmetrical relations successively and that words distinguish concepts. The kitten/cat example is used as a simple refinement: adding "young" separates `kitten` from the wider class `cat`.

The thesis then attempts to realize this by a distinguishing/unfolding operator.

## 1.5 The distinguishing/unfolding operator

Section 2.3 defines, schematically,

\[
\partial[v_0,\ldots,v_n]
 =\bigvee_j \neg v_j\wedge[v_0,\ldots,\widehat v_j,\ldots,v_n].
\]

The prose says that each codimension-one face is retained while the omitted vertex is negated. The operator is intended simultaneously as:

- a decomposition into faces;
- a logical distinction operation;
- a symmetry-breaking operation;
- an analogue of measurement.

For \(C=X\wedge Y\wedge Z\), Example 2.5 gives

\[
\partial C=(\neg X\wedge Y\wedge Z)\vee
(X\wedge\neg Y\wedge Z)\vee
(X\wedge Y\wedge\neg Z).
\]

This is exactly the Boolean function that is true when **exactly two of \(X,Y,Z\) are true**.

The `green box` example treats

\[
\partial(\text{green}\wedge\text{box})
=\text{green}\;\mathsf{XOR}\;\text{box}
\]

as a transition from a fused concept to distinguishable components.

That Boolean output should be interpreted carefully: XOR does not merely say that the two predicates can be separately inspected; it asserts that exactly one is true. Thus the psychological interpretation is stronger than the logic warrants.

## 1.6 Repeated unfolding

The thesis writes \(\partial^n\) and gives higher-step examples, but the definition only specifies the action on a positive logical simplex. The first output contains disjunctions and negated vertices, so **the iteration rule is under-specified**.

This is a central defect. The thesis nonetheless gives an Example 2.6 in which

\[
\partial^2(XYZ)
= X\wedge\neg(Y\wedge Z)
 \vee Y\wedge\neg(X\wedge Z)
 \vee Z\wedge\neg(X\wedge Y).
\]

Exhaustive truth-table computation shows that this is true for all assignments of Hamming weight 1 or 2. An exact two-step rank-layer interpretation would instead select only the assignments with exactly **two negations** (Hamming weight 1). The printed formula therefore does not implement the clean rank-by-rank unfolding suggested elsewhere in the thesis.

## 1.7 Gluing

Section 2.3.1 explicitly asks for an "integrator" or gluing operation that could rebuild higher-order simplices from unfolded lower-dimensional pieces.

This is a fertile idea, but the worked Boolean gluing Example 2.7 is false. The displayed left-hand side evaluates to true at \((X,Y,Z)=(0,1,1)\), whereas \(X\wedge Y\wedge Z\) is false. The accompanying finite script reproduces this counterexample.

A deeper issue remains even after correcting the Boolean formula: the proper faces of a simplex alone determine the **boundary**, not whether the higher-dimensional simplex is filled. Therefore reconstruction requires additional information: provenance, a filler rule, a flag condition, a gluing diagram, or local-to-global descent data.

## 1.8 Pink flower and successive assembly

Later in the thesis (§3.2.2–§3.3, around PDF p. 87), the concept `pink flower` is presented as a higher concept built from `pink` and `flower`, with possible order effects in which one component is brought into awareness first and then associated to the other.

This anticipates a modern distinction between:

- **decomposition/refinement** of a concept;
- **ordered observation histories**;
- **reconstruction/colimit assembly**.

The thesis itself does not provide a rigorous algebra of these histories, but the idea is mathematically salvageable.

## 1.9 Logical topology, presheaves and gluing

Section 3 introduces a proposed propositional logical topology (ProLT), categories of logical expressions/sets, and presheaf-like restriction maps. The thesis explicitly wants to glue local logical sections to form larger structures.

There are useful ideas here, but the definitions are not yet a valid sheaf theory. In particular:

- proposed "open sentence" conditions are not sufficient to establish a topology without a precise carrier set and closure proof;
- the role of syntax versus semantic truth sets is repeatedly conflated;
- restriction maps need a well-defined functorial domain and codomain;
- gluing of sections must distinguish reconstruction of **data on a fixed base** from reconstruction of the **base space itself**.

The most principled recovery is to choose an actual topological/simplicial base and place a presheaf, sheaf, or cosheaf of observations/data on it.

## 1.10 Exact sequences, homotopy and homology

The final chapters attempt logical analogues of exact sequences, projective resolutions, homotopy, and homology using Boolean/correspondence matrices.

These constructions are not sound as homological algebra in their present form. Among the defects:

- "homotopic" is defined as commutativity of morphisms between resolutions; this is not the definition of a chain homotopy;
- quotient expressions such as Boolean matrix quotients are used without an underlying abelian category/module structure that would make them ordinary quotients;
- exactness is asserted without correctly defined kernels/images of homomorphisms;
- the thesis later states or implies that triangulations are isomorphic rather than that homology is invariant under appropriate topological/chain equivalence.

The valuable part is the aspiration: **compare concept structures using chain complexes and homology**. The correct implementation is the standard one developed in `FORMAL_UNFOLDING_MODEL.md`.

---

# 2. Dependency map

| Thesis component | Mathematical dependency | Thesis-specific addition | Audit status | Recovery path |
|---|---|---|---|---|
| Mental Space | point-set topology | mental entities as points/concepts | Repairable | observation spaces, stratified/simplicial spaces |
| Concept | abstract simplicial complex | complete 1-skeleton mental concept | Repairable | arbitrary finite complex/hypergraph with semantics |
| Category `Con` | category theory | inclusions among concepts | Repairable | poset category of subcomplexes/refinements |
| Ultrametric categories | ultrametric spaces, trees | unconscious classes | Sound as model / not unique | fibers/balls at observational scale |
| Ultrametric \(\Rightarrow\) indiscrete | topology | symmetry claim | **False** | distinguish metric topology from observational quotient |
| Unfolding \(\partial\) | Boolean algebra + faces | negate omitted vertex | Repairable | gated Boolean derivative / Hamming incidence |
| \(\partial\) as boundary | chain complexes | same symbol and intuition | **False** | use separate \(d\) and \(U\) |
| repeated \(\partial\) | iteration | rank-by-rank differentiation | Under-specified | exact-layer Boolean-lattice lift |
| \(\partial^2=0\) implicitly suggested by topology | chain differential | logical unfolding | **False in original OR semantics** | \(\mathbf F_2\) or signed incidence differential |
| green box XOR | Boolean logic | independence/distinction metaphor | Speculative/misinterpreted | separate distinguishability from exclusivity |
| gluing by conjunction | Boolean algebra | reconstruction | **False in worked example** | colimits/descent/fillers |
| presheaves/sheaves | category/sheaf theory | logical restrictions | Repairable | sheaf/cosheaf over genuine base |
| cycles = symmetry | homology + group actions | psychological symmetry | **False** | Aut groups + quotient/fiber indistinguishability |
| exact logical sequences | homological algebra | Boolean matrices | Defective | genuine chain complexes/modules |
| homotopy | chain/topological homotopy | commutative resolutions | **False definition** | chain homotopies / simplicial contiguity |
| homology of concepts | simplicial homology | cognitive interpretation | Promising | standard homology and induced maps |

---

# 3. Audit of the original unfolding operator

## 3.1 Exact domain and codomain

The thesis formula is not intrinsically typed. There are at least three possible readings.

### Syntactic factorization reading

Let \(\mathsf{Fact}_m(A)\) be ordered \(m\)-tuples \(F=(f_1,\dots,f_m)\) of Boolean formulas over atoms \(A\). Define

\[
U_{\rm th}(F)
=\bigvee_{j=1}^m \left(\neg f_j\wedge\bigwedge_{i\ne j} f_i\right).
\]

Then

\[
U_{\rm th}:\mathsf{Fact}_m(A)\longrightarrow \mathsf B(A),
\]

where \(\mathsf B(A)\) is the Boolean algebra of truth functions on \(A\).

This is a mathematically valid operation **on a chosen factorization**.

### Decorated-face reading

For a simplex \(\sigma=\{v_0,\dots,v_n\}\), define a decorated codimension-one face

\[
(\sigma\setminus\{v_j\},\;\neg v_j).
\]

Then unfolding lands not in the ordinary simplicial chain group but in a set/module of **decorated faces**.

This is the interpretation closest to the thesis's geometric prose.

### Boolean truth-set reading

A formula defines a set \(A\subseteq\{0,1\}^m\). For the all-true vertex \(\mathbf 1\), one-step unfolding produces its directed Hamming neighbors obtained by changing one 1 to 0.

This is representation-independent only after the semantic state space and direction of permitted flips are explicitly chosen.

## 3.2 Not well-defined modulo logical equivalence

The factorization reading does **not** descend to a function on Boolean equivalence classes.

Take

\[
F=(X,Y),\qquad F'=(X,Y,X\vee Z).
\]

The conjunctions are equivalent:

\[
X\wedge Y\equiv X\wedge Y\wedge(X\vee Z).
\]

But at \((X,Y,Z)=(0,1,0)\),

\[
U_{\rm th}(F)=1,
\qquad
U_{\rm th}(F')=0.
\]

Hence logically equivalent concepts can unfold differently when expressed with different redundant factors.

**Conclusion:** the original operator is syntactic/factorization-sensitive. A canonical factorization, a provenance structure, or a semantic replacement is required.

## 3.3 What grading changes?

The thesis describes a codimension-one face operation, but the Boolean summand

\[
\neg v_j\wedge \bigwedge_{i\ne j}v_i
\]

still depends on all \(n+1\) variables. Thus:

- geometric positive-face dimension drops by one **if the negated variable is treated only as a label**;
- Boolean arity does **not** drop;
- Hamming distance from the all-true valuation increases by one.

The cleanest grading is therefore not ordinary simplex dimension but **number of distinguished/negated coordinates**.

## 3.4 Relation to the Boolean derivative

For the monomial

\[
f(x_1,\dots,x_m)=\bigwedge_{i=1}^m x_i,
\]

the standard Boolean partial derivative is

\[
\frac{\partial_B f}{\partial x_j}
=f|_{x_j=0}\;\mathsf{XOR}\;f|_{x_j=1}
=\bigwedge_{i\ne j}x_i.
\]

The thesis summand is therefore

\[
\neg x_j\wedge\frac{\partial_B f}{\partial x_j}.
\]

So the one-step thesis operator is an OR of **gated Boolean derivatives**. The computation script verifies this identity exhaustively through arity five.

It is not itself the usual Boolean derivative because the deleted coordinate is reintroduced as a negative gate, and the coordinatewise derivatives are aggregated by OR rather than XOR.

## 3.5 Boolean-lattice / Hamming interpretation

Let \(e_S\) denote the minterm in which coordinates in \(S\) are false and all others true. Define

\[
D_\vee(e_S)=\bigvee_{j\notin S}e_{S\cup\{j\}}.
\]

Then

\[
D_\vee^k(e_\varnothing)
=\bigvee_{|S|=k}e_S.
\]

Thus repeated unfolding traverses exact Hamming shells around the all-true vertex. It is nilpotent after depth \(m+1\), but generally not square-zero.

This is a strong formal reconstruction of the thesis's intended "successive differentiation".

## 3.6 When does square-zero appear?

Linearize the same rank-incidence relation:

\[
D(e_S)=\sum_{j\notin S}e_{S\cup\{j\}}.
\]

Over \(\mathbf Z\), every two-coordinate enlargement is reached in two orders, so

\[
D^2(e_S)
=2\sum_{\substack{T\supset S\\|T|=|S|+2}}e_T.
\]

Therefore \(D^2\neq0\) over \(\mathbf Z\) in nontrivial dimensions.

Over \(\mathbf F_2\), \(2=0\), hence

\[
D^2=0.
\]

Over an arbitrary commutative ring, one may add standard orientation signs to obtain the usual simplicial coboundary, whose square is zero.

This is a decisive structural result:

> The thesis's combinatorial incidence pattern is close to a cochain differential, but its Boolean-OR semantics is not a differential. Square-zero emerges only after changing the coefficient algebra or adding incidence signs.

## 3.7 Information loss and reconstruction

The OR aggregation discards provenance: after two or more source states are combined, the same output term may have multiple parents. Thus the operator is not generally invertible.

A particularly simple semantic non-injectivity occurs for directed 1-to-0 Hamming unfolding: any state with no outgoing 1-to-0 move maps to the empty set, as does the empty source set.

What can be recovered depends on retained metadata:

- with full parent labels, reconstruction is trivial;
- with only a union of children, generally not;
- with a prescribed concept class (e.g. one known parent simplex), recovery may be possible;
- with a closure/filler axiom, recovery can become canonical.

## 3.8 Adjoint / Galois connection

Let \(R\subseteq X\times Y\) encode an unfolding relation. The existential relational image

\[
U_!(A)=\{y\in Y:\exists x\in A,\;xRy\}
\]

has a right adjoint

\[
U^*(B)=\{x\in X:R(x)\subseteq B\}.
\]

Then

\[
U_!(A)\subseteq B\quad\Longleftrightarrow\quad A\subseteq U^*(B).
\]

This is a genuine Galois connection. It supplies a mathematically natural "integration-like" residual, although not an inverse. The composites \(U^*U_!\) and \(U_!U^*\) yield closure/interior-type operators.

---

# 4. Minimal principled repair

The repair should preserve the thesis's idea while changing as little as possible.

## 4.1 Do not reuse \(\partial\)

Reserve

\[
d:C_n(K)\to C_{n-1}(K)
\]

for the genuine chain differential.

Call the cognitive/observational operation \(U\) (unfolding) or \(R\) (refinement).

## 4.2 Preserve the logical operator as a separate semantic object

The original operator can survive as either:

1. a factorization-sensitive Boolean operator \(U_{\rm th}\), explicitly presented as syntactic; or
2. a representation-invariant Hamming/refinement relation \(U^-\) on semantic states.

Neither should be called a chain boundary.

## 4.3 Build complexes functorially from observations

For each observation level \(k\), define a finite simplicial complex \(K_k\). An unfolding/refinement step should be represented by a simplicial map

\[
u_k:K_k\to K_{k+1}
\]

when such a direction is natural, or by the reverse-direction map induced by cover refinement when that is the canonical geometry.

The induced chain map

\[
U_k=C_\bullet(u_k)
\]

then satisfies

\[
dU_k=U_kd.
\]

No extra axiom is needed: this is functoriality of simplicial chains.

## 4.4 If refinement has no canonical forward map, use zigzags

A finer cover naturally maps to a coarser cover after choosing containment assignments, usually producing

\[
N(\mathcal U_{k+1})\to N(\mathcal U_k)
\]

rather than the desired coarse-to-fine direction. Different valid assignments are often contiguous and induce the same homology map, but a forward simplicial map need not be canonical.

Therefore a psychologically natural temporal sequence can produce an algebraic zigzag

\[
K_0\leftarrow K_1\to K_2\leftarrow\cdots,
\]

for which zigzag persistence is the appropriate invariant.

---

# 5. Filtrations and mapping cones

A monotone accumulation of observed relations gives a filtration

\[
K_0\subseteq K_1\subseteq K_2\subseteq\cdots.
\]

Then ordinary persistent homology records classes born and killed as the representation becomes richer.

If a step is a chain map \(U:C\to D\), its mapping cone has

\[
\operatorname{Cone}(U)_n=D_n\oplus C_{n-1}
\]

and sits in the standard long exact sequence. Two especially important facts are:

1. \(U\) is a quasi-isomorphism iff \(\operatorname{Cone}(U)\) is acyclic.
2. For an inclusion \(K\hookrightarrow L\), the cone is quasi-isomorphic to the relative chain complex \(C_*(L,K)\).

Therefore cone homology measures **homological change introduced by unfolding**, not a generic notion of psychological difference.

Spectral sequences become useful only after a genuine multi-stage filtration is fixed. For finite one-step examples, relative homology and mapping cones are clearer and sufficient.

---

# 6. Reconstruction and gluing

## 6.1 Exact simplicial gluing

If \(K=K_1\cup K_2\), then \(K\) is the categorical pushout/colimit of

\[
K_1\leftarrow K_1\cap K_2\rightarrow K_2
\]

in the category of simplicial complexes with suitable maps. More generally, a cover by subcomplexes reconstructs the union from the full intersection diagram.

This is exact combinatorial reconstruction because the gluing data includes the intersections.

## 6.2 Nerves and Čech constructions

For a cover \(\mathcal U\), the nerve records which finite families have nonempty common intersection. Under a good-cover hypothesis, the nerve is homotopy equivalent to the union.

This reconstructs topology up to homotopy, not necessarily the exact original combinatorial object.

## 6.3 Sheaves and cosheaves

A sheaf formalizes compatible local observations that glue to a unique global section on a fixed base. A cosheaf formalizes covariant assembly and is often closer to "building a larger concept from local pieces."

Important distinction:

> Sheaf gluing reconstructs **data over a base**. It does not, by itself, reconstruct the base simplicial complex from its sections.

For concept reconstruction one may need both a geometric gluing diagram for the base and a sheaf/cosheaf for the attached semantic data.

## 6.4 No-go theorem for bare proper faces

The proper codimension-one faces of a simplex do not encode the presence of the simplex itself.

For a triangle, the three edges glue to \(S^1\), not automatically to the filled disk \(\Delta^2\).

Thus the thesis's hoped-for inverse to unfolding cannot exist on bare face data without additional structure.

## 6.5 Conditions under which reconstruction becomes a theorem

Recovery is available under assumptions such as:

- **provenance:** each unfolded face remembers its parent;
- **flag closure:** every clique is required to span a simplex;
- **specified fillers:** compatible boundaries have designated fillers;
- **full Čech data:** all intersections and inclusion maps are retained;
- **descent:** local semantic sections agree on overlaps and satisfy the relevant sheaf/cosheaf axiom;
- **known generative class:** the parent is known a priori to lie in an identifiable restricted class.

---

# 7. Cycles, symmetry and asymmetry

The thesis's proposed identification fails in both directions.

## 7.1 Symmetry without homology

A filled triangle \(\Delta^2\) has automorphism group \(S_3\), so it is highly symmetric, but

\[
H_1(\Delta^2)=0.
\]

Thus symmetry does not require a nontrivial cycle class.

## 7.2 Homology without symmetry

Take a triangle cycle \(a-b-c-a\), attach one leaf to \(a\), and attach a path of length two to \(b\). The resulting graph has

\[
\beta_1=1
\]

but its automorphism group is trivial: the attachments distinguish all cycle vertices.

Thus a nontrivial cycle does not imply symmetry.

## 7.3 Correct separation of concepts

Use different mathematical objects for different questions:

- **topological hole:** \(H_n(K)\);
- **combinatorial symmetry:** \(\operatorname{Aut}(K)\);
- **symmetry under a specified group:** a group action \(G\curvearrowright K\);
- **observational indistinguishability:** an equivalence relation or fibers of an observation map \(q:X\to O\);
- **symmetry breaking under refinement:** splitting of fibers/orbits, or reduction of a stabilizer subgroup.

This produces genuine theorems rather than metaphorical identification.

---

# 8. Exact finite prototype

The full calculation is in `FINITE_EXAMPLES.md` and `finite_complex_audit.py`. The prototype uses four attributes \(a,b,c,d\):

\[
K_0=\text{path }a-b-c,
\]

\[
K_1=\text{cycle }a-b-c-d-a,
\]

\[
K_2=K_1\cup\{ac,abc,acd\},
\]

a disk triangulated by diagonal \(ac\).

Over \(\mathbf F_2\):

- \(H_0(K_0)=\mathbf F_2\), \(H_1(K_0)=0\);
- \(H_0(K_1)=\mathbf F_2\), \(H_1(K_1)=\mathbf F_2\);
- \(H_0(K_2)=\mathbf F_2\), \(H_1(K_2)=H_2(K_2)=0\).

The inclusions are chain maps. The first step creates a 1-cycle; the second kills it by adding two 2-simplices. Correspondingly,

\[
H_1(K_1,K_0)\cong \mathbf F_2,
\qquad
H_2(K_2,K_1)\cong \mathbf F_2,
\]

and the same nonzero dimensions appear in the respective mapping cones.

This is exactly the kind of calculation the thesis was trying to reach, but with the algebraic roles properly separated.

---

# 9. Literature and novelty conclusion

The literature map is in `LITERATURE_PRIORITY_MAP.md`. The main priority findings are:

1. **Ultrametric mental spaces are not novel to the thesis.** Khrennikov had already developed \(m\)-adic/ultrametric mental-space models, including categories encoded by balls; Murtagh explicitly connected Matte-Blanco's bi-logic with metric/ultrametric hierarchical topology.
2. **Concepts/knowledge represented by simplicial complexes also have substantial antecedents.** Valencia and Giavitto used simplices/complexes for knowledge representation and analogy; later work uses simplicial complexes for concept extraction, epistemic logic, databases, neural codes and cognitive maps.
3. **Formal Concept Analysis and Dowker complexes provide very close mathematical machinery** for object-attribute relations, concept lattices, dual nerves and homotopy information.
4. **Sheaf gluing and global-section obstructions are standard mature mathematics.** They are powerful for a reconstruction theory but cannot be claimed as novel merely by being applied to concepts.
5. **Persistent and zigzag homology are standard machinery** for changing complexes.
6. **Boolean differential calculus is a mature field**, so the gated-derivative identification should be positioned as a reinterpretation of the thesis operator, not a new Boolean calculus.
7. In the search conducted through 28 September 2026, I did **not** locate an antecedent that combines Matte-Blanco's specific unfolding idea with a rigorously separated simplicial chain differential, observation/refinement chain maps, mapping-cone change invariants, and descent-based concept reconstruction. That is a plausible synthesis niche, but this is a search result, not proof of priority.

---

# 10. Final classification

| Recovered material | Classification | Reason |
|---|---|---|
| Mental Space as a structured mathematical state space | **Promising open direction** | broad but flexible; needs observational semantics |
| concepts as simplicial complexes | **Repairable / promising** | useful modeling language; original complete-graph condition too restrictive |
| ultrametric hierarchy of concepts | **Sound as a model, not unique** | strong prior literature; useful for hierarchical indistinguishability |
| ultrametric topology is indiscrete | **False** | contradicts standard metric topology |
| one-step logical unfolding on a fixed conjunction | **Sound** | exactly-one-false / gated Boolean derivative interpretation |
| unfolding modulo logical equivalence | **False without extra structure** | factorization counterexample |
| unfolding as ordinary simplicial boundary | **False** | wrong codomain/algebra; no square-zero law |
| exact-layer Hamming unfolding | **Repairable and mathematically clean** | faithful to successive differentiation |
| \(\mathbf F_2\) incidence differential | **Sound after explicit modification** | square-zero cochain differential |
| original repeated \(\partial\) formulas | **Speculative / internally inconsistent** | iteration not defined; Example 2.6 mixes layers |
| gluing by the printed Boolean formula | **False** | direct truth-table counterexample |
| reconstruction by colimits/descent | **Sound replacement** | standard exact local-to-global formalism |
| cycles equal symmetry | **False** | counterexamples both directions |
| automorphism/fiber refinement theory of symmetry | **Promising** | clean separation of topology and symmetry |
| logical exact sequences/homology as written | **False / nonstandard** | kernels, quotients and homotopy not correctly typed |
| two-operator \((d,U)\) refinement theory | **Promising open direction** | gives a coherent mathematical research program |
| cone homology as unfolding defect | **Sound and useful** | standard homological invariant with direct interpretation |

---

# 11. Single strongest next theorem to attack

## Observation–Refinement Descent and Cone Theorem

The strongest next target is a theorem unifying refinement, homology and gluing.

### Proposed theorem target

Let \(X\) be represented at observation levels \(k\) by finite covers \(\mathcal U_k\), with \(\mathcal U_{k+1}\) refining \(\mathcal U_k\). Let \(K_k=N(\mathcal U_k)\) be the nerve. Prove, under explicit hypotheses, that:

1. every refinement choice induces a simplicial map
   \[
   r_k:K_{k+1}\to K_k;
   \]
2. any two valid refinement choices are contiguous, hence induce the same map on homology;
3. if both covers are good covers of the same underlying space, \((r_k)_*\) is an isomorphism and
   \[
   H_*(\operatorname{Cone}(C_*(r_k)))=0;
   \]
4. if a refinement also changes the represented support/relations, the cone homology equals the precise relative defect associated with that change;
5. a compatible sheaf/cosheaf of concept data satisfies descent, so local differentiated pieces reconstruct a unique/global (or colimit) concept exactly when the relevant descent obstruction vanishes.

### Why this is the right next theorem

It turns the thesis's central metaphor into a rigorous statement:

- **successive differentiation** becomes cover/refinement;
- **transformation between complexes** becomes a simplicial/chain map;
- **what changed** becomes cone/relative homology;
- **what stayed topologically the same** becomes quasi-isomorphism;
- **reconstruction** becomes descent/colimit gluing;
- **noncanonical choices** are controlled by contiguity and homotopy.

Several ingredients are standard individually, so novelty would need to come from the exact observation semantics, hypotheses, and the way the theorem links them. The first research task should therefore be to formulate the observation category precisely enough that this statement becomes neither tautological nor merely a restatement of the nerve theorem.

---

# Reproducibility

Run:

```bash
python3 run_all.py
```

The package contains:

- `unfolding_boolean_audit.py`
- `finite_complex_audit.py`
- `boolean_audit_results.json`
- `finite_complex_results.json`
- `run_all_output.txt`

All finite calculations in this audit are reproducible from those scripts.
