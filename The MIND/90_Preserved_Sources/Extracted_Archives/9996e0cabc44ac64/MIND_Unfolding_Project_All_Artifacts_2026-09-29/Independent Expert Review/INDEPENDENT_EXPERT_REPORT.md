# Independent mathematical referee report: MIND unfolding v0.4

Review date: 29 September 2026. Target: `Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex` and its 27-page PDF in `Manuscript Convergence 2026-09-29`.

**Recommended disposition: revise before submission.** The carrier-splitting, matching, interaction-complex, degree-two, and explicit torsion results in Sections 7–9 withstand this review. Their proofs, with the manuscript's augmented-chain conventions, support the stated conclusions over the stated coefficients. I found no fatal error in that mathematical core. This conclusion rests on the arguments below, not on passing enumerations.

The manuscript as a whole needs two precise repairs: make the admissibility assumptions on *every* nerve cover explicit in Theorem 11.2, and repair the fixed-arity definition and exceptional one-factor case of Theorem 2.4. The corrected distinction between descent on X and descent on Y is valid. Some further wording should distinguish homological detection from detection of all topological or support changes. Publication novelty is **not verified**. Much of the paper is standard machinery or a direct specialization; the potentially publishable core is the product-poset recognition, graph/transitivity restrictions, and sharp signed integral examples taken together.

This is a fresh AI mathematical review, not independent human peer review or formal proof certification. I read the entire v0.4 source and recorded an initial dependency map and concerns **before** reading earlier review verdicts. I then consulted the requested mathematical supplements and relevant companion claims, derived the arguments and witnesses, retrieved primary literature, and finally compared with internal reviews. No subagents were used. No manuscript, source archive, or earlier certificate was edited. All new files are in this separate directory.

## 1. Claim-by-claim assessment

“Verified” means the proof was checked or independently supplied in this report. Computation is additional evidence. Page numbers below are the manuscript's printed/PDF page numbers. “Valid with repair” distinguishes the intended result from an insufficiently specified literal formulation.

| Manuscript identifier | Status | Evidence and dependencies |
|---|---|---|
| Proposition 2.3, exact-one-false characterization | Verified | Pointwise evaluation of the disjoint Boolean disjuncts. |
| Definition 2.1 / Theorem 2.4, p. 4 | **False without an arity restriction; valid with the repair in §2 below** | For one factor, U(f)=not f is a Boolean-function operator. The printed proof compares tuples of different lengths despite the fixed-length definition. The non-congruence claim is true for each fixed length at least two. |
| Sections 3–4; Theorem 4.2 | Verified, with a minor proof-detail omission | XOR is a vector difference; tetrahedron and Hamming-layer claims follow directly. For the convex-hull equality, a slice vertex cannot have two fractional coordinates; its integral coordinate sum rules out exactly one fractional coordinate. This supplies the short missing argument in part (iii). The nontrivial layer has dimension m−1 and is a simplex exactly at weights 1 and m−1. |
| Theorem 5.2 and Corollary 5.3 | Verified | Relative skeleton chains occur only in degree r. Skeleton homology follows from exactness of simplex chains, Euler characteristic, and the top-dimensional cycle rank. |
| Section 6 refinement distinctions and nerve warning | Verified within the finite signature model | Forgetting coordinates coarsens equivalence; adding truth regions refines the generated topology. A tautological indexed region cones its nerve. No inference from arbitrary observation-list extension to cover refinement is justified or needed. |
| Theorem 7.2, p. 9 | Verified | Lower split copies are up-beat points; the remaining section is Q. The actual order is exactly the bit-monotone suborder. Cofiber invariance applies to the resulting factorization. |
| Theorem 7.4, p. 10 | Verified | Same vertices; retained chains are exactly weakly increasing bit words. The relative basis and boundary follow by quotient. |
| Proposition 7.5 / Corollary 7.6 | Verified | Available isotone section and pointwise comparison with the identity; dual argument for A0. |
| Lower-fiber discussion, §7.3 | Verified as a conditional statement | A top available copy is a maximum of its lower fiber. The Björner–Wachs–Welker conclusion requires the separately stated hypotheses; it is not automatic. |
| Lemma 7.8 / Theorem 7.9, pp. 11–12 | Verified | Weighted chain count; signed reduced graph incidence; leaf collapses. All five asserted equivalences hold. See §3. |
| §7.5 higher-height sharpness | Verified for existence and unrestricted realization | Companion cone–whisker argument checked independently. A face-poset model of RP² suffices for height-three torsion. The companion's particular 13-point/14-state economy was not independently verified and is unnecessary here. |
| Equation (1), §8.1, p. 13 | Verified over every stated coefficient ring | Two relative-acyclic inclusions, two triple sequences, and simplicial excision. See §4. |
| Proposition 8.2, p. 14 | Verified | Explicit isotone available-bit section and comparison map. This proves homotopy equivalence, beyond merely homology equivalence. |
| Theorem 8.3, p. 14 | Verified | Unique mixed pair, actual chain direct sum, product-edge-link suspension, and the two-colour shift. Empty/disconnected cases checked. Naturality needs a specified category if asserted beyond the present statement. |
| Corollaries 8.4–8.5, pp. 14–15 | Verified | Contractible outside factors; atom crosscut. The hypothesis that the generating poset is nonempty handles the singleton-lattice exception. |
| §8.2 three-chain and matching-torsion boundaries | Verified | Three-chain hand calculation; endpoint realization transfers arbitrary reduced link homology. It refutes universal torsion-freeness/TU, not just a field formula. |
| Proposition 9.1, p. 16 | Verified | Explicit filtered chains, signs, augmented degree, bidegree and finite convergence; only associated graded homology is determined by E∞ in general. |
| Theorem 9.2, p. 16 | Verified | Actual isomorphism to Cone(h)[2]; long exact sequence gives the stated kernel/cokernel degrees and quasi-isomorphism criterion. Integral extension warning is correct. |
| Theorem 9.3 and path blocks, p. 17 | Verified | Transitivity forces neighborhood inclusions; four-cores are exactly the specified C4 components; longer cycles have no triple cores. Full-poset links remain essential. |
| §9.1 eight-state C4, pp. 17–18 | Verified | All nine links reconstructed; oriented paths give a unit d²; independent full-pair and mixed-complex integral checks agree. |
| §9.1 seven-state K1,3, p. 18 | Verified | All seven links reconstructed; explicit triple-link paths give a primitive d²; star-pair topology independently gives cone H2=Z. |
| Proposition 9.4, p. 18 | Verified | Every available link has two contractible components; inclusions preserve component-difference generators. The horizontal row is the ordinary chain complex of ΔR, with a sign change. |
| RP² torsion example, pp. 18 and 25 | Verified | Closed triangulated surface and integral homology, star formula, 181 available links, 31 coarse links. Verification of the large example uses the proved reduced model, not a full doubled-pair Smith reduction. |
| Proposition 9.5, pp. 18–19 | Verified | Nonempty finite whole-relation meet/join closure gives extrema in source and projected relation. Both complexes are contractible. |
| Lemma 10.3, p. 19 | Verified | A common point of a refined-cover intersection lies in every chosen parent, proving contiguity. Empty cover members must be deleted or treated as ghost indices. |
| Theorem 11.2(a), p. 20 | Verified | Same contiguity argument; no nerve theorem needed. |
| Theorem 11.2(b–d), p. 20 | **Valid with repair/explicit interpretation** | Correct if all three covers participate in compatible functorial nerve equivalences. Intersection contractibility alone does not suffice for the stated refining family. Counterexample and exact repair in §2. |
| Theorem 11.2(e–f), p. 20 | Verified on the intended inclusion site; general-site wording needs clarification | Separate sheaf/cosheaf descent on X and Y is correct. Use actual site morphisms and fiber-product/intersection diagrams, and a category admitting the requisite limits/colimits. |
| Example 11.3, p. 21 | Verified | Restriction Z²→Z is projection. This repairs the specific v0.3 support error. |
| Proposition 12.2; Section 13 | Verified in the stated inclusion-cover setting | Kernel/cokernel criterion is the bijectivity criterion for restriction. Subcomplex gluing is its union colimit. Boundary data do not specify a top cell. |
| Sections 14–17 | Verified at the elementary mathematical level | Listed small skeleton groups, subgroup inclusion under observation refinement, and persistence/zigzag distinctions. No psychological validity follows. |
| §11.1 claim that cone homology answers whether support/structure changed | Valid only after narrowing the wording | Cone homology detects failure of homology equivalence, not every change of support or homotopy type. |
| Section 18 publication-priority positioning | **Not verified as novelty** | Literal prior-art overlap established; specialized contribution assessed in §8. No completeness claim for the literature search. |
| Appendix historical enumeration totals and global minimality | **Not independently rerun/verified as exhaustive totals** | Documentation and code inspected for their stated scope. Selected witnesses reproduced; no full enumeration or minimality search performed. The manuscript correctly avoids global minimality. |

## 2. Prioritized findings and smallest repairs

### A. Missing cover admissibility in Theorem 11.2: substantive hypothesis clarification

The source at line 1226 says “Let V be a finite good cover of Y refining U|Y.” Definition 11.1 (lines 1213–1222) tests intersection contractibility, while the opening qualification refers to a pair for which a relative nerve theorem applies. Admissibility is a property of the covers and comparison maps, not just the pair of spaces. The proof needs a functorial nerve comparison for V as well as U and U|Y.

Under an intersection-only reading, take X=Y=[0,1], U={X}, and

    V1=[0,1/2),   V2=[1/2,1].

Both pieces are contractible, their intersection is empty, and they refine U. The pair and U are as well behaved as possible. Nevertheless N(V) is two points and N(U) is one point. The nerve map is not a homotopy equivalence; its chain cone has H1=Z, whereas H1(X,X)=0. Thus (b), (c), and (d) fail under that literal reading. This is not a counterexample if “the relative nerve theorem applies” is intended to quantify over **all** the displayed cover data; in that intended reading the problem is incomplete specification, not a failed nerve proof.

**Smallest repair:** require a finite simplicial pair with U and V covers by subcomplexes and all nonempty intersections, including restricted intersections, contractible. Alternatively explicitly require suitable numerable open covers and compatible natural nerve comparisons for U, U|Y, and V. A general version can specify a functorial span of homotopy equivalences from the covered spaces to the nerves. The finite-subcomplex version is sufficient and clean. No change to Sections 7–9 follows.

For (e–f), the new support distinction is correct. On an ordinary open-set site, a non-open Y is not automatically an object with a map F(X)→F(Y); either require Y to be admissible or explicitly use the restricted/inverse-image sheaf and its adjunction map. The existing admissibility clause takes the first route. Specify that covers are by inclusion morphisms, their intersections represent the relevant pullbacks, and the cosheaf target is, for example, abelian groups or another suitable cocomplete category. An arbitrary site cannot replace fiber products by set intersections without explanation. These are scope qualifications, not a recurrence of the v0.3 extension error.

### B. Theorem 2.4 has a false one-factor case and an invalid fixed-arity witness

Definition 2.1 fixes F=(f1,…,fm) with m=|A| (source line 143 onward). Theorem 2.4 then denies the existence of a Boolean-function operator for every factorization, but the printed proof uses F=(X,Y) and F′=(X,Y,X∨Z), of different lengths. More basically, for m=1, Π(f)=f and U_th(f)=¬f; the asserted nonexistence is false.

**Smallest repair:** state m≥2 and replace the witness by two m-tuples

    F=(0,1,1,…,1),   F′=(0,0,1,…,1).

Both conjunctions are zero; the unfolding outputs are respectively one and zero. Constants belong to the declared Boolean-function algebra. This proves the fixed-arity claim for every m≥2 without new assumptions. Alternatively allow arbitrary finite factorizations in the definition, but that changes the declared domain. No later topology theorem depends on the printed witness or on the m=1 assertion.

### C. Novelty and theorem hierarchy: publication-level issue, not a correctness failure

The abstract already acknowledges classical machinery and unresolved priority. That restraint is appropriate. It should be made equally clear that the two-column exact sequence is standard mapping-cone algebra, that filtration-width collapse is standard, and that the matching result combines a standard local deletion calculation with a product-link identification. Merely naming the obstruction links or the spectral sequence does not establish a new construction. The source comparison in §8 exhibits the actual parameter identifications.

**Smallest repair:** lead a submission with the observation-product calculation and sharp graph-class boundaries, and classify the general algebra as tools or lemmas. State exactly which specialized results are proposed as contributions. The broad historical/descent narrative may remain interpretive material, but does not strengthen the publication-priority claim. No optional new research theorem is required to make the existing core defensible.

### D. Exposition and proof portability

At source line 1291, the question “Did the underlying support or compatibility structure change?” is said to be answered by cone/relative homology. A proper inclusion {0}⊂[0,1] already changes support while having zero relative homology. Beyond the special low-height theorem, a homology equivalence need not be a homotopy equivalence. Replace the assertion by “Does the chosen map fail to be a homology equivalence?” or explicitly describe cone homology as one obstruction.

The seven-state link assertions are short in the manuscript; the paths in §6 below make the primitive differential reviewable without trusting the JSON. Incorporating that small argument or making a permanent, clearly indexed supplement available would improve proof completeness for external readers. This is not an unresolved mathematical gap after consulting the supplied supplement and performing the derivation.

The theorem's matching isomorphism is not explicitly claimed natural, which is appropriate. If naturality is added, specify at least compatible order embeddings preserving availability and the core labels; arbitrary maps may identify vertices or send missing copies to available copies, and may not induce the proposed link maps. The exact sequence in Theorem 9.2 is naturally functorial in commutative squares of chain maps h. That does not assert a natural splitting.

## 3. Carrier splitting, weighted height, and the five equivalences

For every split s, the strict upper set of (s,0) in the lexicographic completion has minimum (s,1). Removing a lower split copy leaves this property true for all remaining lower split copies. The resulting section takes the upper copy at split states and the unique copy otherwise; it is isomorphic to Q. The projection therefore is a finite-space homotopy equivalence and induces an order-complex homotopy equivalence. The original projection factors through the same-carrier thinning inclusion. All relative/cone statements follow by postcomposing with this equivalence, with reduced homology for the topological cofiber.

A chain of r+1 coarse states can contain an extra vertex precisely at each split state. This proves hψ(Q)=dim ΔQ-hat, not merely an upper bound.

When that dimension is at most two, relative C0=0 and the only possible boundary is d2:C2→C1. Orient triangles by their chain order. The inversion-edge parts of their boundaries are:

| Bit word on vertices 0,1,2 | Surviving terms |
|---|---|
| 010 | +[1,2] |
| 100 | −[0,2]+[0,1] |
| 101 | +[0,1] |
| 110 | +[1,2]−[0,2] |

These are exactly oriented graph columns, after supplying the omitted formal-root entry in a one-entry column. Reversing a graph edge orientation is harmless. A formal root is retained even when isolated. There is one per connected coarse component; a defect-graph component cannot acquire two roots because every contributing triangle stays in one coarse component. Parallel edges count in the graph cycle rank.

The complex is the graph's chain complex relative to its root set, shifted up by one. Thus H2 is free of rank β1 and H1 is free of rank the number of rootless components; all other cone groups vanish. Graph incidence and its row-deleted matrices are totally unimodular. Acyclicity over Z, over every field, or indeed over any one nonzero field is therefore equivalent to β1=c0=0.

If the graph is a rooted forest, every nontrivial component has a nonroot leaf. The corresponding deleted simplicial edge belongs to exactly one remaining triangle. It cannot belong to a retained triangle, because a retained subcomplex contains every face of each of its triangles; and there are no higher simplices. It is genuinely a free face, so leaf removal produces the stated elementary collapse. Repeat until no relative cells remain. A collapse implies a homotopy equivalence and acyclic relative chains. Conversely, if Δπ is a homotopy equivalence, two-out-of-three with the completion projection makes the inclusion a homotopy equivalence, hence its relative homology vanishes and the graph is a rooted forest. This checks every direction without using an invalid general “acyclic cofiber implies equivalence” principle.

The defect graph here has **inversion edges as vertices and deleted triangles as edges**. It is not the exclusive graph Gψ, whose vertices are exclusive coarse states. The distinction is indispensable.

For the higher-height boundary, the companion adjoins a greatest t to R and gives a chosen minimal z and t bit zero, all other states bit one. Internal comparisons survive; only z<t survives at t. The refined complex is ΔR with a collapsible whisker, while the coarse complex is a cone. This proves the claimed universality and homology shift. Taking the face poset of a triangulated RP² gives height-three torsion directly, without relying on the companion's smaller-model citation. A disjoint neutral split state preserves positive cone homology if actual splitting is desired.

## 4. Two-colour model and matching formula

Let K=Δ(Q×2), L=ΔQψ, and let K_P and K_Z delete the lower and upper missing sets respectively. The map (s,a)↦(s,1) retracts K_P to the top row and the dual retracts K_Z to the bottom row. These retractions are compatible with the projection to Q, so the inclusions into K are homotopy equivalences. The triple and excision isomorphisms are

    H_n(K,L) ← H_n(K_P,L) = H_n(U,K_Z) ← H_(n+1)(K,U).

The arrows displayed are isomorphisms, including in degree zero; ordinary negative-degree relative groups are zero. The projection K→ΔQ gives H_n(cone π)=H_n(K,L). This proves the single downward shift from mixed relative degree to cone degree.

In a matching, any relative simplex has exactly two missing vertices, e=(p0,z1). Any further missing vertex in lk_K(e) would form a triple core and give degree at least two at an exclusive endpoint. Thus the **full** product-edge link equals the available link. The differential cannot mix different e-summands. Orienting e first gives

    C_m(K,U)= ⊕_e C-tilde_(m−2)(lk_K e).

In the open product interval between p0 and z1, remove z0 for the first piece and p1 for the second. The first closes to a top row with minimum p1; the second closes to a bottom row with maximum z0. The two endpoints are incomparable, so these order complexes really cover all chains. Their intersection is Δ((p,z)×2), equivalent to Δ(p,z). The union is therefore a suspension. If the coarse interval is empty, the two pieces are points with empty intersection and the union is S0, exactly the augmented suspension convention. The lower and upper link factors are ΔQ_<p and ΔQ_>z, so their joins give lk_K(e)≃Σ lk_ΔQ[p,z]. No Künneth freeness assumption is used.

Consequently, putting m=n+1 gives

    H_n(cone π;R) = ⊕_(p,z) H-tilde_(n−2)(lk_ΔQ[p,z];R).

This holds over every commutative coefficient ring as stated. A two-state chain with profile (1,0) has empty coarse edge link and cone H1=R; a direct calculation confirms the degree. Two disjoint such chains give R² in degree one. Negative cone degrees and degree zero vanish. The empty exclusive graph yields zero mixed complex, and the separate explicit section proves homotopy neutrality. Disconnected links are correctly handled by reduced H0; disconnected Q is handled componentwise by ordinary relative chains.

Bounded-poset localization follows because any nonglobal endpoint supplies a nonempty contractible outside factor. In J(R), the atoms are its minimal singleton ideals. Their join is top exactly when R is an antichain; otherwise the atom crosscut is a full simplex. For r=1, the proper part of B1 is empty and the answer is correctly H1=Z. This also checks the smallest distributive example.

## 5. Interaction filtration, two columns, and degree two

A relative simplex is uniquely S∪T, with p=|S| missing vertices of both colours and an available face T of dimension q, allowing T=∅ and q=−1. Its dimension is p+q. With missing vertices first,

    d(S∧T)=Σ_i (−1)^i (S−s_i)∧T + (−1)^p S∧∂T,

discarding a core face that loses mixedness. Deleting an available vertex preserves p; deleting a missing vertex lowers p by one and induces the actual inclusion of available links. Thus v²=h²=vh+hv=0. Independent signed enumeration checked this identity against every surviving ordinary boundary term in the ten test systems listed in §7.

The increasing filtration F_p is on **C(K,U)**, with E0_(p,q)=⊕ C-tilde_q(ΛS) and vertical sign (−1)^p. Therefore E1_(p,q)=⊕ H-tilde_q(ΛS), d1 is signed core deletion, and d^r has degree (−r,r−1). Cone degree is p+q−1. The filtration is finite and exhaustive over any coefficient ring. Its limit is gr_F H_(p+q)(K,U). Columns 2,…,M imply E^(M−1)=E∞; for M=2 this already means E1. The empty-core case is the zero complex. Augmentation is part of the construction, even where an actual product-model link happens to be nonempty.

With only columns two and three, the degree-m group is A_(m−2)⊕B_(m−3), and its boundary is (a,b)↦(∂a+hb,−∂b). This is exactly Cone(h)[2], with the paper's shift convention. The mapping-cone long exact sequence yields

    0 → coker H_(n−1)(h) → H_n(cone π) → ker H_(n−2)(h) → 0.

Vanishing in every degree is equivalent to h being a quasi-isomorphism, including its augmented degree. Over a field the sequence splits noncanonically. Over Z it splits if the kernel on the right is free; it need not split otherwise. The chain-cone formula determines actual homology; the spectral-sequence page alone generally determines only its associated graded. E∞=0 does determine actual vanishing because the filtration is finite. No missing extension can rescue a nonzero group with zero associated graded.

For degree-two exclusive graphs, p<p′ implies N(p′)⊆N(p); z<z′ implies N(z)⊆N(z′). A mixed core is a biclique whose two colour classes are chains. Each class has at most two elements, and a four-core is a whole K2,2 component with both colour pairs comparable. Conversely those hypotheses produce the four-core. This proves E3 stabilization and the stated conditional E2 result.

Two comparable same-colour vertices of degree two must have identical neighborhoods. In a path of at least three edges, a supported triple consequently contains a leaf and its distance-two neighbor. For P-coloured leaf a and internal b, only b<a is possible; for Z-coloured leaf y and internal x, only y<x is possible. End triples have disjoint edge supports for paths of at least four edges. On a three-edge path they can share the middle edge and must be included in the same cone block. On a cycle of length at least six there are no such twins, hence no triple core; the matching chain argument applies to that component.

Boundary faces preserve the exclusive component, which gives the chain-level direct sum. The links must still be calculated in the **entire** Q. Even for p<c<z with c split and p,z exclusive, the whole-poset coarse edge link is a point, whereas restricting to the exclusive vertices makes it empty and incorrectly predicts H1=Z. The manuscript correctly retains this distinction.

For an ordered C4 core a<b<x<y, direct deletion gives k=(-,+,−,+) in triple order (abx,aby,axy,bxy), and h=(bx−ax, by−ay, ax−ay, bx−by). Substitution gives hk=0. If ∂c=0 and ∂b=kc, the total differential of (0,b,c) is (hb,0,0), proving the stated d² formula. This shows precisely why a double-complex boundary can have a nonzero higher differential.

## 6. Reconstruction of the witnesses

All homology in this section is integral; cone homology is reduced topological-cofiber homology.

**Three-chain (1,0,0).** The refined complex is an isolated point and an edge, while Q is contractible, so H1(cone)=Z. The missing vertices are 0_0,1_1,2_1. The first edge link and the triple link are two points; the second edge link is a point disjoint from an interval. In component-difference bases, deletion gives h0:Z→Z², 1↦(1,−1). Its cokernel is Z. Both coarse edge links are points, so their independent coarse-link contributions vanish. This refutes the forest extension of the coarse-link formula; it does not refute the correct two-column theorem.

**Seven-state star.** Use the covers and profile in the manuscript. Write A=023, B=026, C=036 for the three missing triple cores (each includes 0_0 and the indicated upper missing copies). The four-core link is {0_1,2_0}. The triple links and paths, oriented from 2_0 to 0_1, are:

| Core | Available link / chosen path |
|---|---|
| 023 | 2_0—4_1—0_1 |
| 026 | 2_0—5_1—0_1 |
| 036 | 2_0—3_0—1_0—1_1—0_1 |

All are contractible. The 02 edge link is the four-edge cycle with bipartition {0_1,2_0} and {4_1,5_1}. The 03 edge link is a cone with apex 4_1. The 06 edge link has maximal faces

    [0_1,1_1], [0_1,5_1], [1_0,1_1],
    [1_0,3_0,6_0], [2_0,3_0,6_0],
    [2_0,5_0,5_1], [2_0,5_0,6_0].

It collapses to a cycle: eliminate each triangle through an outer edge, then remove the resulting dangling edges; the remaining cycle passes through 0_1,1_1,1_0,3_0,2_0,5_1. These descriptions establish E1=E2 with Z² at (2,1) and Z at (4,0), and no other groups.

For c=[0_1]−[2_0], the triple corrections in order (023,026,036) have signs (−,+,−). Their horizontal boundary has components B−A at edge 02, A−C at edge 03, and C−B at edge 06. In particular B−A traverses the square 02 once. Thus d² is nonzero and primitive, without deducing primitivity merely from rational rank. The independent code checks the path boundaries and verifies that attaching the target cycle kills H1 without introducing torsion in each noncontractible target link.

For an independent abutment argument, put T=Q−{0}, C_split={1,4,5}. The two lower ideals of the maximal elements of T are cones, with their contractible intersection T_≤3; thus ΔT is contractible. ΔC_split is an edge and an isolated point. The refined complex is the union of a piece retracting to ΔT and a cone on ΔC_split, glued along ΔC_split. Hence H_n(cone)=H_(n−1)(ΔT,ΔC_split), which is Z in degree n=2 only. This confirms the primitive injection Z→Z² and disproves unconditional E2 collapse for forests, Ferrers graphs and chordal-bipartite graphs.

**Eight-state C4.** Use a,a′,v,b,w,x,y,y′ and the profile in §9.1. Its exclusive core is a0<b0<x1<y1. The four-core link is {b1,x0}. Triple links abx and bxy are the two-edge paths through y′1 and a′0 respectively; aby and axy are

    x0—y0—w0—w1—b1,
    x0—v0—v1—a1—b1.

The edge links ax, by and bx are cones with the manuscript's stated apices. The remaining ay link has triangles [a1,b1,w1] and [v0,x0,y0], and edges [a1,v1], [v0,v1], [w0,w1], [w0,y0]. Collapse the two triangle ears to obtain a cycle. Every one of the nine links is thereby identified, not just its Euler characteristic.

Let P_t denote the four paths from x0 to b1. The triple correction is (−P_abx,P_aby,−P_axy,P_bxy). Its ay component is P_axy−P_aby, which goes once around the remaining cycle. The other components lie in contractible links. Thus d²:Z→Z is a unit, E3=0, and the cone is acyclic. This is a sharp E3 bound for maximum degree two, not a proof that every such C4 has nonzero d². The independent full calculations used 108 mixed cells and 340 direct-pair cells; the star used 79 and 205 respectively.

**All-exclusive star and RP².** For Q={p}⊕R, the refined complex is the disjoint union of a point and ΔR. Since Q is contractible, the cofiber long exact sequence already gives H_n(cone)=H_(n−1)(ΔR), with **ordinary H0**. This includes disconnected R: two isolated R states give cone H1=Z². There is no cone H0.

For the filtration proof, every mixed core is p0 followed by a nonempty R1-chain σ. Its available link is isolated p1 disjoint from the cone on R_≤min σ at bit zero. Taking the isolated component minus the lower component gives a consistent H-tilde_0 generator. Core deletion preserves it and gives minus the ordinary simplicial differential of ΔR. Only q=0 survives, so E2=E∞ and there is only one surviving filtration position in each total degree: no extension remains unresolved here.

The ten facets 012,013,024,035,045,125,134,145,234,235 have face vector (6,15,10), every edge in two triangles, and connected cyclic vertex links. This is a connected closed surface with Euler characteristic 1, hence RP². Independently cancelling integer unit chain entries on the original triangulation leaves one degree-zero generator and a differential [2] from degree two to degree one. Thus H0=Z, H1=Z/2. Its nonempty-face poset has 31 states, and adding p gives 32. Every coarse [p,z] link is the vertex link of z in the barycentric subdivision, hence a circle. Every available core link has only free reduced H0=Z. The star formula therefore gives cone H1=Z and H2=Z/2. This verifies precisely torsion created by interaction relative to those local links; it does not say that the chosen underlying R itself is torsion-free.

Neither explicit d² witness establishes global minimality. The RP² example is an existence construction, not a minimum-size result. None of these examples refutes the positive hypotheses actually stated in Theorems 8.3, 9.2 or 9.3.

## 7. Reproducibility, preservation, and limits

The new scripts are `independent_checks.py` and `rerun_selected_certificates.py`. They run with the installed Python 3.10.11 and SymPy 1.14.0; no package was installed. Commands, from the workspace root:

```powershell
python -B 'The MIND\Independent Expert Review\independent_checks.py'
python -B 'The MIND\Independent Expert Review\rerun_selected_certificates.py'
```

The first script imports no project verifier. It enumerates product chains independently by subsets, constructs signed relative boundaries, checks d²=0 and the missing-first shuffle formula, and computes integral homology by cancelling unit chain entries. It asserts that the residual source and target supports are disjoint before using residual Smith forms; it does not purport to be a general-purpose integer homology algorithm. The tested cases satisfy that assertion. Both explicit path witnesses are checked against actual link edges and boundaries. Attaching each indicated target cycle verifies primitivity over Z. Outputs are in `independent_results.json`.

| Independent test | Nonzero cone groups |
|---|---|
| One split state, empty exclusive graph | None |
| Two-state (1,0), empty coarse link | H1=Z |
| Two disjoint matching edges | H1=Z² |
| Endpoint matching on a diamond, disconnected coarse edge link | H2=Z |
| Three-chain (1,0,0) | H1=Z |
| Star with disconnected two-point R | H1=Z² |
| Three-edge path with two supported triples | H1=Z |
| Height-one C6 | H1=Z⁶ |
| Seven-state star | H2=Z |
| Eight-state C4 | None |

The original RP² triangulation was checked independently as described above. The test set is targeted, not exhaustive. These finite results support the hand proofs; they are not the reason universal theorems are marked verified.

Before running supplied code, I read `verify_d2_certificate.py`, `verify_torsion_star.py`, the relevant imported mixed-complex and local-model code, and the baseline chain/Smith routines. The second new script imports the original modules with bytecode disabled, replaces their output-directory variables, and invokes only the two d² certificate functions and the torsion-star verifier. It reads the star input from the original directory and writes regenerated results only into `regenerated_certificates/`. The 36.192-second run passed.

The baseline Smith routine obtains a primitive kernel basis from D=S*A*T, then expresses the next boundary in T^−1 coordinates and Smith-reduces its kernel rows. This is the correct integral procedure; subtracting rational ranks would not suffice. The wrapper separately checked the decomposition identity and unimodularity of the transformations on three matrices. The supplied d² reducer explicitly requires unit pivots and tracks signed chain transformations. Its interpretation of a primitive injection is also supported here by the independent geometric paths and independent integral reductions. A utility elsewhere concatenates torsion lists without canonical invariant-factor normalization; this can make future equality comparisons misleading but does not affect these certificates.

`REPRODUCTION_RECEIPT.json` records that all mathematical fields in the three regenerated certificates match their originals. For the star, the new certificate adds induced-subset counts {4:84,5:126,6:126,7:27} and changes the minimality wording. For C4, it adds a sentence about proper induced restrictions. The torsion certificate is identical as parsed JSON. These are the exact annotation differences in the convergence receipt. They do not change the posets, profiles, signed chains, E1 groups, integral maps, or homology. They also do not independently certify any minimality claim; those searches were not rerun here.

All 184 files in the current-manuscript, interaction-supplement and consolidated-handoff trees were hashed before and after the selected reproduction and were unchanged. The integration receipt's input and output hashes match. The before/after hashes are retained in `source_hashes_at_verification.json`. I did not separately repeat the archive's entire nested-manifest/source-ZIP validation; the preservation check here has the expressly stated scope.

The PDF has 27 pages. Its complete text was extracted with pypdf; pages 14, 16, 18, 20 and 21 were visually inspected, including the matching formula, spectral-sequence and two-column formulas, star formula, and descent theorem. The theorem numbers agree with the source/build labels. This was a mathematical review, not full publication layout QA or a fresh TeX compilation. An initial PATH-resolved MiKTeX `pdftotext` call failed due to first-run configuration permissions; a guessed bundled `pdftotext` path and a PyMuPDF import were unavailable. Extraction then succeeded with pypdf and rendering with the available Poppler `pdftoppm`. No permission/configuration changes were made to solve those tooling failures.

**Material read:** the complete v0.4 source; selected passages in its extracted PDF text and selected rendered pages; all seven specifically requested mathematical supplement reports; the selected verifier source and original/generated certificates; the transferred exact-theorem and obstruction files; the companion cone–whisker section; the v0.3 descent statement/proof; and, last, the convergence review, integration/verification receipts, literature map, and all three named adversarial review reports.

**Material or claims not fully reviewed:** the complete historical thesis and logical-complex notes; the entire v0.3 manuscript as a separate review target; the full observation-topology companion; unrelated companion results, especially two-bit enumeration/minimality and the 13-point RP² model citation; every row of the 90,201-case CSV and all 435 selected historical integral records; random/targeted searches and isomorphism postprocessing as independently reproduced experiments; a direct Smith reduction of the 32-state full doubled pair; every page's typography; all references outside the targeted comparison below; global minimality; psychological interpretations; and the optional nonunit-C4-d² research question. None is silently claimed verified.

The historical 90,201 cases are over F2, the additional 5,000 six-state cases are sampled, and the 20,000 C4 trials are targeted. The 87 coarse types, 16,761 profiles and 70 exclusive graph types are postprocessing, not additional independent experiments. Integral conclusions in this report come from integral arguments or the explicitly named integer computations.

## 8. Prior art, exact overlap, and contribution

Primary sources were retrieved during this review. The following comparison is deliberately narrower than a certification that no equivalent theorem exists elsewhere.

**Chachólski–Jin–Scolamiero–Tombari.** Their published Definition 5.1, Corollary 7.2(2a) and Theorem 8.6 identify the direct antecedents. In the available v1 preprint these are Definition 4.1, Corollary 6.2 (p. 10) and Theorem 7.5 (p. 12). Set X=V(K)−M0, Y=V(K)−M1, A=V(L). Then X∪Y=V(K), K_X∪K_Y=U, and their obstructing simplices are exactly mixed missing cores. Since S∩A=∅, St(S,A)=ΛS after adding the empty face. For matching, put K_e=e*lk_K(e). Its deletion union is ∂e*lk_K(e)=U∩K_e; distinct blocks intersect only in U. Applying their corollary with σ=e and n=1 gives the local double-suspension relative homology. Summing blocks and applying the independently verified product-link suspension and two-colour shift gives Theorem 8.3. Thus its deletion mechanism is a **direct specialization**, with the product identification the specialized content. Theorem 8.6 is a fiber bound, not the paper's exact kernel/cokernel computation. [Published primary text](https://link.springer.com/article/10.1007/s41468-021-00066-2), [numbering cross-check in the primary preprint](https://arxiv.org/pdf/2002.03409).

**Björner–Wachs–Welker.** Theorem 1.1 (author PDF p. 2) requires each lower fiber to be ℓ(f^−1(Q_<q))-connected; Theorem 2.5 (p. 7) instead requires nonempty fibers and null-homotopic lower-fiber attachments. The identification here is f=π and the lower fibers are the manuscript's L_q. Matching does not force either hypothesis: take p<z and c<z, p one-only, z zero-only, c split. At z, the lower fiber has isolated p1 and the component c0<c1, c0<z0; the preimage below z meets both components. Its inclusion cannot be null-homotopic, and the fiber is not even connected. Consequently those theorems are not blanket corollaries yielding the matching formula by this f. The conditional invocation in §7 is accurate. [Author-hosted primary paper](https://www.math.miami.edu/~wachs/papers/fibers.pdf), Theorems 1.1 and 2.5; [published DOI](https://doi.org/10.1090/S0002-9947-04-03496-8).

**Dey–Hirani–Krishnamoorthy.** Theorem 5.2, preprint p. 11, characterizes TU of ∂_(p+1) by torsion-freeness of H_p(L,L0) for **all** nested pure subcomplex pairs of dimensions p+1 and p. It is not a criterion using only global homology or only this manuscript's single relative pair. In Theorem 7.9, TU follows more directly from the actual reduced incidence matrix. The RP² examples correctly block a universal TU inference. This is **standard machinery/direct specialization**, not a new TU theorem. [Primary preprint](https://arxiv.org/pdf/1001.0338), [published source](https://epubs.siam.org/doi/10.1137/100800245).

**Filtered-complex algebra.** Weibel's Construction Theorem 5.4.1 (p. 132) and Classical Convergence Theorem 5.5.1 (p. 135) apply with C=C(K,U) and F_p defined above: boundary preservation and finite exhaustion have been checked explicitly. Exercises 5.1.1–5.1.2 (p. 121) already express the two-column extension and secondary zigzag. Proposition 9.1 and the algebra in Theorem 9.2 are therefore **standard machinery**, specialized through the identified link complexes and inclusions. [Primary book chapter](https://math.mit.edu/~hrm/palestine/weibel/05-spectral_sequences.pdf).

**Functorial nerves.** Bauer–Kerber–Roll–Rolle, Theorem 4.8 (retrieved preprint p. 28), gives natural homotopy-equivalence spans for good covers by subcomplexes. Apply it to (X,U), (Y,U|Y), and (Y,V); inclusion and refinement induce maps of covers. Good intersections and subcomplex inclusions verify its hypotheses, and the long exact sequences of pairs give Theorem 11.2(c). Theorem 5.9 (pp. 32–33) supplies the appropriate open/numerable or closed/cofibration alternatives. These are **direct specializations** once the cover hypotheses are made explicit. [Primary paper](https://arxiv.org/pdf/2203.03571), [published DOI](https://doi.org/10.1016/j.exmath.2023.04.005). Ramras's Definition 2.8 and Theorem 2.13 likewise impose actual cover-category conditions and give natural comparison zigzags; they do not remove that requirement. [Published primary source](https://link.springer.com/article/10.1007/s00454-025-00809-3). Leitão's cited 2026 cover-refinement paper exists; its detailed stability results were not audited here. [Primary record](https://arxiv.org/abs/2602.22784).

| Candidate contribution | Referee classification |
|---|---|
| Beat-point reduction and cofiber invariance | Standard machinery; split-completion recognition is a direct, useful specialization. |
| Weighted-height-two classification | Direct transfer of the companion's incidence result, now with a self-contained proof. |
| Matching coarse-edge-link formula | Direct deletion specialization plus a model-specific product-link identification; useful exact result, modest standalone novelty. |
| Interaction E1 page, page-width bound, two-column exact sequence | Standard filtered-chain and cone algebra after explicit identification. |
| Transitivity recognition of supported cores; path blocks and long cycles | Substantive specialized combinatorial result in this model, though short; exact priority unresolved. |
| Sharp degree-two E3 bound with eight-state unit d²; seven-state star primitive d² | Substantive specialized examples/class boundaries; potential contribution, priority unresolved. |
| Star realization and RP² torsion with free local links | Elementary realization and explicit specialized failure boundary; potential supporting result, not new general torsion machinery. |
| Cover/descent theorem, Boolean/Hamming and skeleton sections | Standard constructions and interpretations; not a new general descent or topology theorem. |

This is a stronger qualification of the matching theorem's standalone novelty than merely saying “deletion is classical.” It is not a disagreement with its proof. Conversely, the explicit failure of the BWW hypotheses above is a reason not to dismiss the whole matching statement by a slogan about fiber theorems. No failed search is used as positive evidence of novelty.

## 9. Comparison with earlier internal assessments and disposition

The internal reviews' sign, grading, extension, degree-two and torsion conclusions agree with the independent derivations and computations here. Their certificate-annotation explanation is reproduced exactly. Their correction of gluing on a proper support is valid and necessary. I do not treat those agreements as additional independent experiments.

The additional findings in this review are the explicit fixed-arity/one-factor defect, the precise admissibility issue for the refining cover with a concrete counterexample to an intersection-only reading, a concrete matching system where the BWW null-attachment hypothesis fails, and the explicit local identification showing how the matching deletion step follows from the established cofiber result. The cover issue is mainly a statement-scope problem under the intended interpretation; the one-factor case is an actual false literal assertion. Neither invalidates the central Sections 7–9 mathematics.

**Disposition: revise before submission, rather than reconsider the mathematical core.** The strongest defensible article would center on Boolean product-poset relative homology: neutral completion; matching coarse links; exact interaction chains; degree-two support classification and sharp E3 behavior; and the two explicit mechanisms of inherited versus interaction-created torsion. Retain the integral qualifications and negative examples. Required mathematical revisions are the arity repair, explicit cover/site hypotheses, and narrower homological-detection wording. Required positioning work is a precise contribution statement acknowledging direct specializations. A permanent, readable signed-witness supplement is advisable; no further search or conjecture is needed to support the established claims.

For publication, obtain independent human expert judgment on novelty and presentation after those repairs. The review request itself is complete. Any manuscript repair needs a new instruction, since this request expressly excludes implementing repairs. Keep that closely related work in this task to reuse the findings and file/version boundaries; gpt-6-sol with high reasoning is the least costly available model tier I would recommend for these bounded theorem-statement repairs, with no claim of measured pricing savings. Defer unrelated research. No further model run is required to complete this review.
