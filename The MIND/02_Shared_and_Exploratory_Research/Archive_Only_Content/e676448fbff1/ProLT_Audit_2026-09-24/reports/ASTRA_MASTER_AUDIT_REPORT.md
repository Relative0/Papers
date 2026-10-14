# Master audit: Propositional Logical Topology, v0.1-v0.5

**Issued:** 24 September 2026  
**Object audited:** the supplied core v0.8, two historical notes, chronological research notes v0.1-v0.5, ledger, and verification package.  
**Overall decision:** **freeze the valid mathematics, issue an explicit correction to the dimension branch, and narrow the publication program.** The package is not ready for submission unchanged.

This is an independent mathematical and computational assessment, not a rewritten manuscript and not a formal proof-assistant certification. The source snapshot is preserved. Claim IDs refer to `CLAIM_AUDIT_TABLE.csv`; R01-R22 to `LITERATURE_SOURCES.md`; A1-A6 to `AUDIT_ADDITIONS_AND_PROOFS.md`.

## 1. Executive assessment

The research has a sound central object and a correct, useful exact theorem. It also contains one unequivocally false proposed identification, a downstream invalid complexity argument, and a smaller boundary-matrix setup defect. Most of the large foundations layer is standard mathematics presented in a sensible observation-language dictionary.

The strongest surviving result is the **one-bit, height-two preservation theorem**: for the specified same-vertex order thinning, homology neutrality over F2 forces an actual simplicial collapse. Independent inspection confirms why this unusually strong implication holds. Every deleted triangle has one or two deleted edges, with opposite signs in the two-edge case. The integral relative boundary is a reduced graph-incidence matrix. Rooted-forest elimination is therefore an actual free-face collapse, not merely an algebraic cancellation. The audit strengthens the result to all coefficients and computes the complete integral relative groups.

The most important correction is v0.5's assertion that relative observation dimension equals classical poset 2-dimension when the coarse order is total. It is false on two vertices. The inherited NP-completeness argument consequently fails. A replacement theorem identifies the parameter exactly with conflict-graph coloring and generalized Boolean rectangle covering; it proves general NP-completeness even for height-one coarse posets, but does **not** settle the claimed total-order restriction.

There is real material to preserve, but not a defensible case for automatically producing three research papers. My preferred output is **one focused finite-poset paper plus one foundations technical report**. A block-interaction paper and a dimension note remain conditional on additional structural results and narrower prior-art positioning.

### Evidence summary

The claim table has **114 rows**, including **all 82 theorem/proposition/corollary/example environments** in the five chronological notes, plus major examples, base claims, historical problems, and audit additions. Of the 82 named environments, 77 require no mathematical statement repair under their stated conventions. Five require action: the two nonempty-universality qualifications, the false dimension equality, the invalid inherited-hardness proof, and the rooted-forest row-support setup. Additional prose/source corrections are listed separately, especially the v0.1 syzygy phrase and empty v0.3 TeX.

All five original scripts passed. Independent code reproduced the key counts, checked the named interaction examples with signed matrices and all perfect matchings, tested 274,738 one-bit profiles through six vertices, and extended two-bit checks to 337,920 five-vertex profiles. Explicit integer-torsion witnesses and higher-height one-bit witnesses were constructed and checked. No brute-force result is used as a substitute for a general proof.

## 2. Source discipline and package integrity

The archive opened successfully. The manifest was inspected first; the core and historical notes preceded v0.1-v0.5; the ledger was used only after the primary notes; verifier inspection/reruns preceded the external novelty search.

One primary source-format defect was found: `ProLT_Controlled_Refinement_Regimes_v0.3.tex` is **zero bytes**. Its 15-page PDF is readable, so the mathematics could be audited, but source-build reproducibility for that note is absent. The core was supplied as a readable 18-page PDF. No unreadable PDF prevented the audit, and no missing manuscript was inferred from the prompt alone.

The supplied PDFs and TeX contain polished arguments, but their status labels were not accepted as evidence. In particular, the ledger's organization does not rescue the false dimension equality or its descendants. A source snapshot, hashes, script outputs, and new certificates accompany the reports.

## 3. Reconstructing the base object

Let S be the finite current valuation carrier, ordinarily a subset of the full Boolean valuation space Omega_P. Let Phi=(phi_i)_{i in I} be an indexed observation family, and put

    o_Phi(v) = { i : v satisfies phi_i }.

Generate a topology on S by the positive truth sets of the observations. The smallest open neighborhood of v is the set of w whose signatures contain o_Phi(v). Thus, with the core's convention,

    v <=_Phi w  iff  every open containing v also contains w
                 iff o_Phi(v) subseteq o_Phi(w).

This fixes the direction. The quotient by topological indistinguishability is precisely the realized-signature poset P_Phi, ordered by inclusion. Equal signatures, not logically equivalent formulas considered abstractly, are what identify states. The space is T0 exactly when the signature map is injective on the current carrier. These are standard finite-Alexandrov facts [R01-R02].

### 3.1 The quotient really is an ordinary homotopy equivalence

Choose one representative in each indistinguishability class. The resulting section s:P_Phi->S is continuous because the preorder relation depends only on signatures. The quotient q satisfies q s=id, while s q(v) is indistinguishable from v for every v. Consequently the maps s q and id are homotopic; one can use pointwise comparable finite-space maps or the elementary homotopy whose values stay in the same indistinguishability class. Therefore q is an ordinary homotopy equivalence of finite spaces.

By contrast, the McCord map |Delta(P_Phi)|->P_Phi is a **weak** homotopy equivalence. It supplies the homology comparison needed here but must not be relabelled an ordinary equivalence in general. The package's v0.1 canonical theorem makes the correct distinction. Barmak's principal-fiber theorem acts at the order-complex level and already gives a simple-homotopy equivalence under its stated hypotheses [R02].

This distinction is consequential for algorithms. Beat-point reduction is a finite-space contractibility certificate, not a complete order-complex contractibility decision procedure. The package's undecidability theorem explicitly concerns Delta(r), which is the right object.

### 3.2 Observation acquisition versus premise restriction

Adding observations gives a finer topology on the same S. The identity from fine to coarse is continuous, and its quotient map forgets new coordinates. Before T0, a coarse signature class can split into several new profiles. After T0—or more generally whenever new observations are constant on every coarse signature class—vertices can be identified and the operation is only deletion of comparisons.

Adding a premise instead replaces S by its model subset. At the signature level it keeps the induced subposet of signatures still represented. Removing some but not all valuations in one coarse class is invisible to the quotient. Thus order-complex homology is a topology invariant but not a complete invariant of model multiplicities or semantic consequence.

A new observation is redundant exactly when its truth set is already open: equivalently, it is constant on indistinguishability classes and its induced bit is isotone on P_Phi. A finite upset has the positive DNF obtained from its minimal true signatures. Positive-formula redundancy is therefore an elementary finite-order fact, not a newly discovered logical completeness theorem.

### 3.3 Invariance targets must remain separate

Symmetric XOR/Hamming difference uses the indexed observation presentation and weights. Directed loss vanishes in the order-compatible direction and does not behave as the same symmetric coboundary. With positive weights, symmetric Hamming topology on distinct realized signatures is discrete; it is not the upper-set topology unless that order is already discrete.

The observation compatibility complex is a Dowker/nerve construction on an incidence relation. It changes differently from the state order complex. A tautological observation preserves the signature order up to isomorphism but supplies a cone vertex to the compatibility complex. Duplicate coordinates and weights can affect presentation-level objects without changing the finite topology. The core's recognition of these differences is correct and worth preserving.

## 4. Chronological claim audit

### 4.1 v0.1 — sound foundations, mostly standard

**Canonical and relative layers.** The realization, functoriality, premise-subcomplex, relative exact-sequence, refinement-projection, and cone-exact-sequence statements are correct. The normalized chain map must send a simplex with identified image vertices to zero. The U and G groups are ordinary relative homology of model-signature pairs. They may be useful, but their definitions alone do not establish a new invariant with stronger logical content than the pair itself [R18].

In particular, entailment implies the relevant pair is unchanged, but vanishing relative groups does not imply entailment. On a carrier with the empty observation family, every nonempty model subset has the same singleton signature quotient. A genuine semantic restriction can therefore leave every proposed relative group zero.

**Boolean cochains.** Delta=lambda differences is delta(lambda); telescoping and the H1 integration criterion are correct. An actual signature-difference field is always exact. A nonzero obstruction can occur only for independently prescribed local data, such as the hypothetical one-edge scalar field on the Rips four-cycle in Example E. That example is valid. It is not evidence that ordinary observation signatures generate a contextuality obstruction. Contextuality cohomology needs additional support/presheaf data [R16].

**Historical sequence.** The old formula-level sequence was not a well-defined exact sequence in an abelian category. The free-F2 repair is correct and canonically split because the union decomposes as overlap disjoint union exclusive part. This argument is elementary and works over any coefficient ring. It supplies no new long exact sequence or homotopical depth beyond that decomposition. The other historical note's ad hoc simplices, use of logical negation as additive negation, and mixed linear/affine reasoning should remain historical, not prerequisites.

**Compatibility and algebra.** Dowker duality, the tautology example, and minimal nonfaces as minimally inconsistent indexed observation sets are correct. Empty truth sets create ghost vertices unless conventions remove them. In Example B, the incompatibility ideal is (x1*x2*x3); the quoted “first syzygetic” event needs the correction in C08. A principal ideal has no nontrivial first module syzygy; the quotient resolution has the expected degree-three generator contribution.

The examples are consistent: Example A is the contractible Boolean-square order complex made of two filled triangles; Example B distinguishes a path-plus-isolated-point order complex from a compatibility circle; Example C gives a relative one-class after XOR premise restriction; Example D detects a split by cone homology; Example E uses an arbitrary nonintegrable field on a Rips cycle.

**Metric/persistence.** Fixed old weights plus added nonnegative weights give the claimed Rips anti-monotonicity. Averaging or reweighting can reverse it. Nested observations and premises give the stated diagrams, but ordinary versus multiparameter versus zigzag persistence depends on the actual index category and arrow directions. These are applications of standard machinery, not independent persistence theorems [R17-R18].

**Verdict:** all sixteen named claims survive; repair the syzygy interpretation and state degeneracy/empty conventions. Foundations report, not a new-homology research paper.

### 4.2 v0.2 — correct general classification machinery

The profile normal form Q={(p,a):a in B_p}, with product order, is correct. It precisely distinguishes splitting from non-splitting. Redundancy is the singleton-isotone case. After identifying vertices in a non-splitting refinement,

    x <=_Q y iff x <=_P y and a(x) <= a(y).

The relative chain basis consists of deleted chains; its differential simply discards faces retained in L. The mapping cone is equivalent at homology level to the ordinary pair (K,L) in this regime.

The adjoint criteria are correct. Taking the union of all new profiles below p produces the greatest principal lower fiber exactly when that union itself occurs at p; the dual intersection criterion handles least upper fibers. The possible/forced one-bit formulation is a direct specialization. The principal-fiber theorems are correctly about r^{-1}(down p) or r^{-1}(up p), **not** point fibers. Contractible and acyclic versions do different jobs, and neither becomes necessary merely because small tests pass [R02].

The cone criterion is exact for homology neutrality. Betti and Euler checks are only necessary shortcuts; equality of endpoint Betti numbers alone does not certify the map. The component criterion is exact because the refinement is surjective on vertices and therefore on coarse components.

The examples separate redundancy, section adjoints, principal-fiber tests, homotopy neutrality, and homology neutrality. Adding X to no observations shows that splitting need not be topologically destructive. XOR on the Boolean square is neutral without a section adjoint. The alternating chain profile shows that both principal-fiber orientations may fail although the actual map is neutral. Acyclic noncontractible complexes give the final homology-versus-homotopy separation.

Universality via minterm realization and principal ideals is correct for **nonempty** targets on a nonempty point-coarse carrier. Add that qualification. The contractibility-undecidability reduction is valid: start with a nonempty finite complex, take its face poset, realize it as a fine signature poset over a point, and ask whether Delta(r) is a homotopy equivalence. The high-dimensional classical theorem suffices [R05, Appendix A, Theorem 11, d>=5]. This is an effective encoding argument; it does not need or supply polynomial formula-size bounds. Homology neutrality remains decidable by finite matrix computation.

**Verdict:** correct standard/adapted framework, with two minor nonempty qualifications. A6 below strengthens its limitation theorem to a single bit after T0.

### 4.3 v0.3 — correct controlled results; chain novelty substantially reduced

The positive and anti-positive normal forms are correct. Post-T0 section-adjoint rigidity is also correct: a section of the same-vertex identity map is forced to be the identity, and monotonicity in both directions then forces the two orders to agree. This explains why adjoints cease to certify interesting proper thinnings in this regime.

An antitone label retains only comparisons between equal label values. If a coarse connected component contains multiple values, it splits; neutrality is therefore equivalent to constant profile on each coarse component. Adding all old-coordinate negations makes the quotient discrete.

Height-one homology rigidity has a particularly short proof: the relative chain complex has only C1=Z^(deleted edges), with C0=0 and no C2. Every deleted edge creates a nonzero relative class. At height two, the whole relative problem is the two-term boundary B:C2->C1. Invertibility is an exact field-homology criterion, and unequal edge/triangle counts obstruct neutrality. This is standard relative-chain algebra, not yet the special one-bit theorem.

**Independent chain proof.** Let b_1...b_n label an n-chain. A nondecreasing word changes no comparisons. A nonconstant nonincreasing word 1^a0^(n-a) gives two disjoint chains. In every other case, first bit 0 gives a global minimum, or last bit 1 gives a global maximum. In the remaining mixed case, delete each initial 1 as an up-beat point, using the first later 1 as its least strict upper element; the remaining initial 0 is a minimum. This proves the trichotomy without a Betti-number inference. Counting gives n+1, n-1, and 2^n-2n. Applying the same classification to every prefix/suffix proves the exact Quillen visibility tests and the count 2^(n-2)-(n-1) for n>=2.

**Prior-art consequence.** The incomparability graph of this refined chain is the bipartite inversion/Ferrers graph, and Delta(Q) is its independence complex. The introduction of Claesson-Kitaev-Ragnarsson-Tenner explicitly announces the corresponding point-versus-two-points simple-homotopy classification, citing an Ehrenborg-Kitaev work listed in preparation [R09]. The underlying proof was not located. Therefore the chain homotopy classification has strong prior-art overlap, while the direct beat proof and exact test-coverage counts remain useful exposition. It should not be advertised as an independently new classification without resolving that bibliographic history.

Block universality over a coarse chain and the refinement/update bifiltration are correct. They are elementary representation and diagram constructions. All eighteen named statements survive. Restore the empty TeX source before freezing the manuscript.

### 4.4 v0.4 — the strongest exact specialization

The repair-map, floor/ceiling, anchor, and semilattice arguments are correct applications of comparable monotone maps and closure/interior ideas. Horn truth sets supply meet closure; dual-Horn falsity sets supply join closure. The realized semilattice and upper/lower cofinality assumptions are indispensable. The full Boolean-lattice endpoint test correctly certifies XOR/XNOR, while NOR can isolate the bottom and change H0. These are useful sufficient conditions, not a general classification of logical fragments [R02,R20].

**The repair-forest proof survives every listed local concern.** Orient a triangle x<y<z by its order. Its boundary is [y,z]-[x,z]+[x,y]. The deleted bit patterns are exactly 010, 101, 100, and 110. The first two give one deleted edge; the last two give two, with opposite integral signs. No deleted triangle has three deleted edges. Attach singleton columns to a formal root in their coarse component, and interpret two-entry columns as graph edges. This gives a reduced integral incidence matrix.

On a rooted tree, a nonroot leaf corresponds to a deleted edge in exactly one remaining deleted triangle. A retained triangle cannot contain a deleted edge, because L is a subcomplex. Height<=2 excludes higher cofaces. Thus the leaf pair is genuinely free in the current complex. Repeating the operation collapses K to L. Disconnected coarse components, isolated roots, parallel edges, and empty deleted-cell sets cause no gap: parallel edges create cycles; isolated roots contribute nothing; the empty matching/collapse is valid.

Conversely, homotopy equivalence implies F2 homology equivalence, so B is invertible. Reduced graph incidence is invertible precisely when every graph component is a tree with exactly one root. The complete equivalence is therefore proved, not computationally guessed.

**Integral strengthening A1.** The matrix is totally unimodular. If c0 counts rootless repair-graph components and beta1 its graph cycle rank, then

    H1(K,L;Z) = Z^c0,     H2(K,L;Z) = Z^beta1,

and all other relative groups vanish. In particular, no one-bit height-two refinement can have relative torsion, and neutrality over any one field already implies integral neutrality and direct collapse.

**Novelty assessment:** the graph-incidence theorem and collapse machinery are established [R03-R04,R19]. The specific binary-order-thinning recognition is the narrow candidate contribution. I did not locate an exact earlier statement with all these hypotheses and equivalences; that supports `NOVELTY_UNCLEAR`, not “new.” The theorem is coherent and useful enough to anchor a tightly scoped manuscript, but its proof should openly reveal how little genuinely new machinery is required.

### 4.5 v0.5 — valuable limits, one major branch correction

The coordinatewise order-thinning description, joint-complex intersection theorem, and sufficiency of sequential neutrality are correct. “Every coordinate safe relative to the original P” is different from “every step safe relative to the current intermediate order.” This distinction explains why destructive interaction is possible without contradicting composition of equivalences.

Universality of same-vertex suborders is correct: label v by its principal Q-ideal. The basic dimension bound survives. The equality with classical 2-dimension does not.

**Two minimal counterexamples.** For P=Q a two-chain, odim=0 but dim2=1. For P a two-chain and Q an antichain, a single label word 10 deletes the only forward relation, so odim=1, while dim2(Q)=2. The coarse order handles reverse noncomparisons for free; an ordinary Boolean embedding cannot. The original inherited-hardness proof must be removed rather than cosmetically adjusted.

**Replacement A2.** Make each deleted comparison a demand. Two demands (x,y),(u,v) conflict iff x<=_Q v or u<=_Q y. A valid bit is a Q-upset. One bit can satisfy a collection of demands exactly when that collection is independent in the conflict graph: take the upward closure of their first endpoints. Therefore odim is exactly the graph's chromatic number. Equivalently, it is generalized Boolean rank of a 0/1/? matrix. This is an established covering framework [R07-R08], specialized to nested orders.

The explicit graph-to-height-one-poset reduction proves general NP-completeness. The total-coarse-order restriction remains unproved here. An additional exact easy case is target Q antichain: odim=ceil(log2 h), where h is the maximum number of elements in a P-chain. Distinct labels are necessary along a chain, and reverse Boolean-lattice linear-extension labels assigned by chain rank suffice.

The coefficient-sensitive boundary criterion is correct. A square integer matrix is rationally invertible iff its determinant is nonzero; integral neutrality requires determinant +/-1; mod-p neutrality requires p not dividing the determinant. Rectangular or singular cases require kernel/cokernel, not a scalar weight. The Bernardi-Klivans translation needs all deleted-edge rows present; a deleted edge lying in no triangle is omitted by the original triangle-generated setup. C03 repairs this. The nonsingular examples are unaffected [R03].

**Named examples.** The 010/101 example is correct and minimal for that three-chain mechanism. The five-state example has the stated compensation and a unimodular 3x3 matrix with a unique matching. The eight-state three-bit example has a unimodular 11x11 matrix and exactly three perfect matchings, each cyclic. Both endpoint posets are beat-contractible, so the inclusion is a homotopy equivalence, but no direct relative collapse exists. This refutes the block extension of the one-bit collapse equivalence. No global minimality claim follows from the small enumeration.

**Matching strengthening A4.** In this height-two two-layer incidence setting, a perfect matching is acyclic exactly when it is unique: a directed cycle is an alternating cycle, and the symmetric difference of two perfect matchings consists of alternating cycles. Thus unique fitting orientation is not merely sufficient; it is equivalent to direct relative collapse. This is a standard matching/Morse observation, and it explains the eight-state failure without redefining rooted-forest theory.

## 5. Interaction and coefficient-sensitive constructions

### 5.1 What Mayer-Vietoris actually contributes

For coordinate subcomplexes A,B of K, let I=A intersection B and U=A union B. There is a natural short exact sequence

    0 -> C(K,I) -> C(K,A) direct_sum C(K,B) -> C(K,U) -> 0,

with diagonal and difference maps. Its long exact sequence gives, when both individual inclusions are homology equivalences,

    H_n(K,I) is naturally isomorphic to H_(n+1)(K,U).

For 010/101, U is the boundary of the coarse triangle and I is an edge plus an isolated point. The connecting morphism identifies the union's relative two-class with the joint relative one-class. This supplies a meaningful explanation of interaction, but it is standard relative Mayer-Vietoris, not a newly discovered homology theory [R18]. Higher Cech-type bookkeeping is available; it should not be developed merely because it can be written down.

### 5.2 Torsion exists, and F2 can miss it completely

A5 realizes a connected two-dimensional finite complex X by its face poset P and retains a spanning-tree suborder Q containing all vertices. Then H_k(Delta(P),Delta(Q);Z)=reduced H_k(X;Z) for k>=1. Principal-Q-ideal labels realize Q as a block refinement. This gives arbitrary finite abelian relative H1 torsion by standard Moore-space constructions.

The audit supplies two complete examples. A 13-state regular-CW face-poset model of RP2 yields a 24x24 relative matrix with Smith diagonal (1 repeated 23 times,2). Its relative H1 is Z/2. A 79-state degree-three Moore model yields a 162x162 matrix with Smith diagonal (1 repeated 161 times,3). Its relative H1 is Z/3; its F2 relative homology vanishes, but its integral homology does not. The latter is an explicit F2-neutral observation block that is not homotopy-neutral.

A final conflict-coloring check compresses the thirteen-state torsion witness to **exactly two observations**, without changing its order or boundary matrix. Its labels are supplied explicitly. This already refutes a two-bit extension based on rational homology neutrality; it does not refute the proposed F2-neutrality question because its determinant is even. The same check proves the eight-state noncollapse pair genuinely needs three bits: three specified deleted-comparison demands form a conflict triangle. The five-state compensating pair's final order can, separately, be realized by one bit.

The underlying small projective-plane model is established finite-space topology [R15]. These witnesses are clean, reproducible realizations, not globally minimal relative-pair claims. The original notes' general matrix framework already predicts coefficient sensitivity; the audit makes it concrete.

### 5.3 One bit in higher height is already universal

A6 gives a simple sharpness construction. Start with any nonempty finite poset R and minimal element z. Add a greatest element t. Give z and t bit0, and every other vertex bit1. Every old R-comparison survives; among comparisons into t only z<t survives. Thus the coarse order complex is a cone on Delta(R), while the fine complex is Delta(R) with a whisker attached at z.

The whisker collapses, so the refined complex has exactly the homotopy type of Delta(R). Consequently one-bit, non-splitting refinement over a coarse cone already realizes arbitrary finite-complex homotopy types in unrestricted height. The order-complex neutrality decision is undecidable even under those restrictions. Relative homology is shifted reduced homology of R.

Choosing the 13-state projective-plane model for R gives a **14-state, height-three, one-bit** refinement with relative H2=Z/2. The analogous Z/3 construction uses 80 states and is F2-neutral but not integrally neutral. This makes the height restriction essential and rules out an unrestricted first-descent/last-descent collapse algorithm. Further positive higher-height theorems need genuine extra hypotheses, not just a contractible coarse endpoint.

## 6. Reproducibility findings and limits

All original scripts passed, but pass/fail alone was insufficient. The independent audit checked actual maps through relative chains, reconstructed all named examples from orders and labels, and used integer Smith forms rather than numerical determinant approximations.

Completed coverage includes: 8,190 chain words through n=12 with actual beat checks; 274,738 height<=2 one-bit profiles through n=6, including all 184,088 exact-height-two profiles in the supplied table; the original 10,468 two-bit cases with 4,459 neutral and 100 destructive; and an extension of 337,920 five-vertex two-bit profiles with 103,562 neutral and 4,514 destructive. No two-bit neutral/noncollapse witness was found in the completed range. The same neutrality decisions held over F2,F3,F5 in that extension.

The natural-label convention represents every isomorphism type but may represent a type more than once. Counts are not uniform statistics on isomorphism classes. Some original “homotopy” checks only calculate homology. The last one-bit CSV forest column excludes redundant cases. The early 255-profile generator was rerun but not independently reimplemented exactly. A six-vertex **two-bit** extension timed out and produced no completed result; no coverage is claimed for it.

No formal proof assistant, independent human panel, or complete automated homotopy oracle was used. Full code, exact scope, unsuccessful-run disclosure, and certificates are in the reproducibility report. These limits do not weaken the explicit mathematical proofs, but they constrain computational and novelty claims.

## 7. Dependency and freeze audit

| Dependency chain | Consequence / action |
|---|---|
| Core signatures -> T0 quotient -> order complex | Valid base; freeze as standard background |
| Core -> premise induced subposets -> relative groups | Valid; foundations report only without an application theorem |
| Core -> profiles -> non-splitting thinning -> relative deleted-chain complex | Valid structural pipeline; keep concise in focused paper |
| Deleted chains -> height-two B -> binary incidence -> forest -> actual collapse | Valid main theorem; freeze for Paper A with integral A1 |
| Repair/floor/semilattice -> qualified Horn corollaries | Valid sufficient conditions; keep hypotheses visible |
| Chain thinning -> beat classification -> counts and Quillen visibility | Valid, but Ferrers prior art reduces novelty; background/appendix |
| Block intersection -> relative MV -> interaction examples | Valid standard explanation; no standalone paper yet |
| Height-two B -> Smith/fitting orientations -> eight-state noncollapse | Valid after row-support patch; useful sharpness section |
| Universality -> odim definition -> claimed dim2 equality -> inherited hardness | Equality false; inheritance blocked; replace with A2 |
| Face-poset realization -> cone/whisker A6 | Valid audit addition; sharply limits unrestricted higher-height extensions |
| Old formula exactness -> later foundations | No necessary dependency: v0.1 replaces the invalid old construction |

The false dimension branch does **not** invalidate the forest theorem, chain classification, block matrix criterion, or interaction examples. The rooted-forest support defect is local and does not invalidate the already nonsingular examples. No orientation failure propagates through the base pipeline.

## 8. Publication assessment and terminology

The package's breadth currently obscures its best theorem. Most definitions are useful names for standard constructions, but a journal referee will ask what survives after the observation notation is removed. The answer should be the binary-labelled finite-poset characterization and its sharp boundaries, not “a new homological foundation for logic.”

The preferred manuscript is **Binary order thinning of finite posets: homology, collapses, and sharp limits**. Put the signed forest theorem, algorithm, and carefully chosen limitations at its center. Explain propositional realization as an application. Move the long foundations dictionary to an expository technical report. The alternative is separate one-bit and block papers, but only after the block paper gains a substantial structural theorem. The dimension branch is presently a corrected technical note, not a third research article.

Keep “repair graph” and “destructive interaction” only as explicitly defined descriptive terms. Use established language for mapping cones, relative homology, rooted forests, fitting orientations, and acyclic matchings. Explain odim immediately as a minimum Q-upset separation number and generalized covering problem. R22's recent “relative dimension” is a different invariant; avoid an unqualified name collision.

Real connections include information-system signatures, Dowker/formal-context relations, closure operators, graph incidence, and Boolean rectangle covering. Rough-set fixed-attribute reducts, SAT theta complexes, abstract interpretation, and contextuality cohomology are useful comparisons but not interchangeable models. Cognitive/mental-space claims remain speculative and should not support a mathematical significance claim.

## 9. Direct answers to the fifteen requested questions

### 1. Which results survive unchanged?

All sixteen named v0.1 claims, all eighteen v0.3 claims, and all fifteen v0.4 claims survive as mathematical statements. In v0.2, sixteen survive unchanged and the two universal-realization claims need a nonempty qualification. In v0.5, twelve survive without mathematical statement repair; the dimension equality, inherited complexity proof, and rooted-forest setup require the corrections above. The table preserves exact source statements and distinguishes additional prose repairs from theorem failure.

### 2. Which corrections invalidate downstream results?

The false dim2 equality invalidates its advertised complexity inheritance and weakens proposed Paper C. It has no dependency path into the topological preservation theorems. The rooted-forest zero-row issue requires a setup patch but leaves nonsingular examples and their determinant conclusions intact. Empty-target qualifications do not affect the undecidability reduction. The historical notes were already replaced rather than used as foundations.

### 3. What are the strongest five to ten mathematical items?

The strongest nine are: the exact one-bit height-two forest/collapse equivalence; its integral/free-homology strengthening; the eight-state block separation of homotopy equivalence from direct collapse; one-bit higher-height cone/whisker universality; the exact chain/Quillen classification; the qualified repair-map/semilattice criteria; the corrected conflict-coloring and general hardness theorem; coefficient-sensitive torsion block realization; and the relative Mayer-Vietoris explanation of two-coordinate interaction. Several are audit additions, not results already proved in the original versions.

### 4. Which are standard, adaptations, or novelty candidates?

Relative MV, integer boundary algebra, closure-map arguments, and generalized covering are standard. The chain homotopy types have a concrete Ferrers antecedent. The forest recognition, small constrained counterexamples, and cone/whisker refinement formulation are useful adaptations and possible narrow contribution candidates. None receives an unconditional novelty certification. Their exact residual content is recorded in the novelty matrix.

### 5. Is the repair-forest theorem actually new?

Its graph/Morse substance is standard once the matrix is recognized. The potentially new content is the exact recognition and equivalence for one-bit order thinning under the height restriction. No exact earlier statement with all those hypotheses was located, but that is not proof of novelty. Position it as a sharply stated specialization, not a new general collapse or rooted-forest theorem.

### 6. Are the chain classification and counts known?

The homotopy classification is equivalent to the Ferrers independence-complex dichotomy announced in R09. The cited underlying proof remains unlocated. The exact counts and Quillen visibility follow very easily from the word classification. Preserve the direct proof but downgrade the novelty claim.

### 7. Is simultaneous interaction enough for a paper?

Not yet on its own. Intersections of separately neutral subcomplexes can behave badly by standard topology. A3 supplies the right exact-sequence explanation. A substantial structural two-bit or restricted-family theorem is the strongest route from interesting examples to a separate research article.

### 8. Is odim new, and what would make it publishable?

It is not classical dim2. It is exactly a generalized Boolean rectangle-cover number for a poset-defined 0/1/? matrix, or a conflict-graph chromatic number. That framework is established. A dedicated name for this restricted family was not verified. A theorem exploiting a prescribed coarse chain or another meaningful structural restriction is needed for a standalone paper.

### 9. Are there torsion/coefficient-sensitive examples?

Yes. The audit gives a 13-state height-two **two-bit** block with relative Z/2 and a 79-state block with relative Z/3. The latter is F2-neutral but not integrally neutral. Height-three one-bit examples on 14 and 80 states show that the one-bit field-independent conclusion also depends essentially on height<=2. All have exact certificates; global minimality is not claimed.

### 10. What should happen to the foundations?

A citable expository technical report is the best current form. Its value is a correct dictionary and well-chosen examples, not a new homology theory. The focused research paper needs only a few pages of this background.

### 11. How many papers, with which theorems?

Prepare one focused research manuscript: V4-11..15 and integral A1 as the core, selected V3 preliminaries, V5-14..15/A4 as the block boundary, and A6 as the higher-height boundary. Use small interaction/torsion examples selectively. Put V1, general V2, compatibility/cochains/persistence, and explanatory material into one foundations report. A second block paper and a dimension note are conditional, not current commitments.

### 12. What should be frozen?

Freeze the base quotient, profile normal form, standard fiber hierarchy, positive DNF, chain classification/counts, and foundations constructions. Freeze all existing examples with their certificates. Do not continue expanding cohomology, SR, persistence, or cognitive branches in parallel. Replace the false dimension claim in the ledger and keep deferred directions visible but inactive.

### 13. What is the single highest-value next theorem?

Determine whether every **two-bit height-two F2-neutral thinning collapses directly**. One bit is proved, three bits fail, and completed two-bit checks through five vertices find no exception. A proof or a compact counterexample would establish a meaningful bit-complexity boundary. Do not promote the finite evidence to a theorem.

### 14. What are the largest novelty risks?

The forest theorem may be regarded as an immediate incidence/Morse corollary; the chain theorem has Ferrers antecedents; dimension is generalized Boolean covering; closure/Horn criteria are standard operator arguments; and most foundations/persistence material is existing topology in a new vocabulary. These risks require a narrow contribution statement and precise citations, not a larger manuscript.

### 15. What would prevent acceptance today?

For Paper A: unresolved narrow novelty positioning, excessive standard-background volume, missing source reproducibility, and ambiguity between finite-space and order-complex homotopy. For proposed Paper B: examples and standard MV/rooted-forest machinery without an independent structural theorem. For proposed Paper C: a false central identification, a failed restricted-hardness proof, and insufficient separation from existing covering theory. For the foundations as a journal research paper: no demonstrated new theorem beyond a useful synthesis. These are repairable scope/evidence problems, not a reason to abandon the validated central mathematics.

## 10. Final decision

**Do not submit the package unchanged. Do not discard it.** Preserve the correct binary order-thinning theorem, its algorithm, and its sharp limits; correct the dimension branch openly; publish the foundational dictionary as exposition; and keep exactly one next theorem active. The result should be a smaller, more defensible research program with a clear mathematical object and verifiable claims.
