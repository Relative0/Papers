# ProLT Research Ledger: v0.1-v0.5

**Date:** 23 September 2026  
**Purpose:** Preserve the full mathematical research tree developed from *Propositional Logical Topology: Observation, Distinguishability, and Inference* (core v0.8), including results, constructions, examples, computational checks, prior-art boundaries, abandoned/repaired ideas, and future branches.

## 0. Executive map

The research program has developed in five stages:

1. **v0.1 - Homological Foundations:** establishes the canonical order-complex layer, relative homology for premise update, mapping cones for refinement, Boolean cochains, compatibility/Dowker topology, Stanley-Reisner encoding, Rips complexes, and persistence.
2. **v0.2 - Observation Refinement Classification:** classifies general refinements through fiber profiles, exact redundancy, non-splitting order deletion, adjoint/fiber criteria, mapping-cone homology, universality, and the impossibility of a universal homotopy classifier.
3. **v0.3 - Controlled Refinement Regimes:** studies post-T0 refinement, the positive/anti-positive logical fragments, bounded-height rigidity, exact chain classification, and the observation/premise bifiltration.
4. **v0.4 - Homotopy-Preserving Logical Observations:** develops arbitrary-height repair maps and closure-system guarantees, then completely solves the one-observation height-two case using a rooted repair forest.
5. **v0.5 - Simultaneous Observation Refinement:** shows that blocks are intersections of coordinate refinements, establishes same-vertex order-thinning universality and relative observation dimension, introduces destructive/compensating interaction, connects height-two block defects to higher-dimensional rooted forests, and shows the one-bit collapse equivalence fails for blocks.

A crucial conceptual pivot occurs at **T0**. Before T0, refinement may split observational equivalence classes. After T0, vertices are fixed and refinement acts purely by deleting order relations and therefore deleting simplices from the canonical order complex.

---

# 1. v0.1 - Homological Foundations for ProLTs

## 1.1 Base structures

- Finite valuation carrier `Omega_P={0,1}^P`.
- Indexed observation family `Phi=(phi_i)_{i in I}`.
- Observation signature `o_Phi(v)` and support representation.
- Realized-signature poset `P_Phi=o_Phi(Omega_P)`, ordered by inclusion.
- Restricted realized-signature posets `P_{Phi,S}` and premise-restricted `P_{Phi,Gamma}`.
- Canonical order complex `O_Phi=Delta(P_Phi)`.
- Restricted order complexes `O_{Phi,S}`.

## 1.2 Canonical topology-invariant homology

**Finite-space realization theorem.**
- The Kolmogorov quotient of the finite ProLT is the realized-signature poset.
- McCord's order-complex construction gives the same homology.
- Proposed notation: `H_k^ProLT(Phi;R)=H_k(O_Phi;R)`.

**Functoriality theorem.**
- Continuous ProLT maps descend to monotone maps between signature posets.
- These induce simplicial maps, chain maps, and homology maps.

## 1.3 Premise restriction and relative homology

- Premise acquisition is distinguished from observation refinement.
- `S' subset S` induces `O_{Phi,S'} subset O_{Phi,S}`.
- Standard short exact sequence of chain complexes and long exact sequence in relative homology.

Proposed invariants:
- **Update-relative homology** `U_k^Phi(Gamma)=H_k(O_Phi,O_{Phi,Gamma})`.
- **Inference-gap homology** `G_k^Phi(Gamma => psi)=H_k(O_{Phi,psi},O_{Phi,Gamma})` when `Gamma |= psi`.

Important limitation: nonzero relative homology is not logical invalidity; semantic consequence remains truth-region inclusion.

## 1.4 Observation refinement and mapping cones

- Canonical refinement projection `r_{Psi Phi}:P_Psi -> P_Phi` by forgetting new coordinates.
- Refinement projection is surjective and monotone.
- Chain mapping cone `D_*(Psi/Phi)=Cone(r_#)`.
- Proposed **refinement-defect homology** `D_k(Psi/Phi)`.
- Cone exact sequence.
- Vanishing of all cone homology is equivalent to the refinement inducing homology isomorphisms.

## 1.5 Boolean cochain calculus

**Boolean difference theorem.**
- Regard the signature labelling as an `F_2^I`-valued 0-cochain `lambda_Phi`.
- Then `Delta_Phi = delta lambda_Phi`.
- Therefore `delta Delta_Phi=0`.

Consequences:
- Triangle/path telescoping.
- Old identity `(a XOR b) XOR (b XOR c)=a XOR c` becomes a coboundary identity.
- Weighted Hamming distance is the weighted norm of this coboundary.
- Directed loss requires the source mask and is not determined by `Delta` alone.

**Boolean integration criterion.**
- A local difference cocycle `g` is globally integrable to a vertex labelling iff `[g]=0 in H^1`.
- On connected complexes, the potential is unique up to an additive constant vector.

## 1.6 Chains over F2 and repair of older notes

- Simplicial boundary over `F_2` has no alternating signs because `-1=1`.
- Distinction between:
  - XOR/addition of chains,
  - XOR of vertex labels/cochain differences,
  - scalar Hamming distance.

**Repair of old formula-level exact sequence.**
- Literal formulas/truth regions are not automatically objects in an abelian category.
- After free `F_2`-linearization:
  `0 -> F_2[A] -> F_2[U] -> F_2[E] -> 0`
  for overlap `A`, union `U`, and exclusive remainder `E`.
- The sequence is split and elementary, so it should not be sold as deep homological algebra.

## 1.7 Compatibility/Dowker layer

- Observation-side compatibility complex `K_Phi` from jointly satisfiable observation subfamilies.
- Valuation-side Dowker dual.
- Dowker duality gives homotopy-equivalent relation complexes.

**Topology/compatibility separation by tautology.**
- Adding a tautology leaves the ProLT topology, signature order complex, and signature distances unchanged.
- The compatibility complex becomes a cone and loses reduced homology.
- Therefore `K_Phi` and `O_Phi` have different invariance targets.

## 1.8 Stanley-Reisner route

- Stanley-Reisner ideal `I_Phi` of the compatibility complex.
- Minimal squarefree generators correspond to minimally jointly unsatisfiable observation subfamilies.
- Possible use of Hochster's formula, syzygies, Betti tables, Tor, and induced-subcomplex homology.
- Strong prior-art caution: Boolean formula/hypergraph topology is already developed.

## 1.9 Metric and persistence layer

- Logical Vietoris-Rips complexes `VR_r(S,d_Phi)`.
- Refinement with retained positive weights makes distance weakly larger, hence fixed-scale Rips complexes shrink.
- Premise accumulation also shrinks the vertex set.

**Monotone evidence-update filtration.**
- Successive observation refinements plus successive premise restrictions give a nested filtration after reversing the time index.
- Ordinary persistence suffices for monotone acquisition.
- Zigzag persistence is needed when observations/premises can be removed or retracted.

## 1.10 Worked examples

- `Phi=(X,Y)`: order complex is two filled triangles sharing an edge; contractible.
- `Phi=(X,Y,not(X and Y))`: canonical order homology and compatibility homology differ (`O_Phi` disconnected; `K_Phi` is `S^1`).
- Premise `X XOR Y`: creates nonzero relative `H_1` in the pair.
- Refinement `(X,not X)->(X)`: mapping cone detects the split.
- Rips square: actual signature difference is exact, while a hypothetical edge field can represent a nonzero `H^1` obstruction.

## 1.11 Deferred avenues first catalogued in v0.1

- Canonical topology computations.
- Refinement classification.
- Relative update/inference theory.
- Boolean cochain integrability and noisy/incomplete differences.
- Compatibility algebra and Stanley-Reisner invariants.
- Metric persistence.
- Cross-layer comparison theorems.
- Deferred evolving/"mental space" architecture:
  valuations -> signatures -> information posets -> complexes -> chain/cochain data -> time-indexed diagrams.

---

# 2. v0.2 - Observation Refinement Classification

## 2.1 Fiber-profile normal form

For each coarse signature `p`, let `C_p` be its coarse observational class and let `B_p` be the set of new-coordinate signatures realized inside that class.

**Fiber-profile normal-form theorem.**
- The refined poset is isomorphic to pairs `(p,a)` with `a in B_p`, ordered coordinatewise.
- The refinement map becomes projection `(p,a)->p`.
- This packages all refinement information into the family `(B_p)`.

## 2.2 Exact redundancy

**Redundancy/order-isomorphism theorem.** Equivalent conditions include:
- same topology before and after refinement;
- every new truth region was already open;
- every fiber profile is a singleton and the induced new-coordinate labelling is monotone;
- the refinement projection is an order isomorphism.

## 2.3 Non-splitting refinement and chain deletion

**Order-deletion theorem.**
- If refinement does not split coarse classes, the fine and coarse posets have the same vertices.
- `p<=_Psi q` iff `p<=_Phi q` and the new labels are coordinatewise nondecreasing.
- The fine order complex is a subcomplex of the coarse order complex.

**One-bit descent criterion.**
- A chain survives iff its new truth bits are nondecreasing.
- A chain is deleted iff it contains a `1->0` inversion.

**Post-T0 refinement filtration.**
- Once the ProLT is T0, all later refinements are automatically non-splitting.
- Later order complexes therefore form a decreasing simplicial filtration.

## 2.4 Relative descent chains

- In the non-splitting case, the refinement mapping cone becomes ordinary relative homology:
  `D_k(Psi/Phi) ~= H_k(O_Phi,O_Psi)`.
- The relative chain complex can be represented by deleted/descent chains.

## 2.5 Adjoint and fiber criteria

**Greatest-lower-fiber / least-upper-fiber criterion.**
- Explicit union/intersection conditions on fiber profiles yield right/left order adjoints.
- Either adjoint implies homotopy equivalence.

**One-observation possible/forced criterion.**
- `M_psi(p)` = psi possible somewhere in coarse class p.
- `m_psi(p)` = psi forced everywhere in coarse class p.
- Upward monotonicity of possibility gives a right adjoint.
- Upward monotonicity of forced truth gives a left adjoint.

**Quillen-McCord/Barmak contractible-fiber criterion.**
- Contractible lower (or upper) principal fibers imply simple homotopy equivalence.

**Acyclic-fiber criterion.**
- Acyclic fibers imply homology equivalence over the chosen coefficients.

These are sufficient, not necessary.

## 2.6 Exact homology classification

**Cone criterion.**
- Refinement is a homology equivalence iff all refinement-defect groups vanish.
- For finite complexes this is algorithmically decidable by matrix rank.

**Connected-component criterion.**
- The induced `H_0` map is always surjective because the refinement projection is surjective.
- It is an isomorphism exactly when every coarse connected component has connected inverse image.

## 2.7 Strict hierarchy of neutrality notions

Tracked distinctions among:
- redundancy/order isomorphism,
- adjoint-neutral refinement,
- Quillen/fiber-neutral refinement,
- homotopy-neutral refinement,
- homology-neutral refinement.

Explicit examples separate these notions.

## 2.8 Counterexamples and examples

- Refinement `(X,not X)->(X)` detects splitting.
- A four-state chain example gives a homotopy equivalence despite failure of both lower- and upper-fiber Quillen tests.
- Examples show mapping cone detects topology changes missed by simpler tests.

## 2.9 Universality and algorithmic limits

**Universality theorem.**
- Every finite poset can be realized as a refined signature poset over a one-point coarse ProLT.

**Every finite simplicial homotopy type occurs.**
- Use a face poset; its order complex is the barycentric subdivision.

**Undecidability theorem.**
- Unrestricted homotopy-neutral refinement is algorithmically undecidable because it contains finite-complex contractibility.

**Homology remains decidable.**
- Finite homology-neutrality can still be decided by mapping-cone matrices over a computable field.

This establishes a sharp homotopy/homology algorithmic divergence.

## 2.10 Small exhaustive verification

- Exhaustive finite tests supported the classification hierarchy and exact mapping-cone calculations.
- One reported run included 255 one-new-bit profiles over nonempty subposets of the Boolean square.

---

# 3. v0.3 - Controlled Refinement Regimes

## 3.1 Positive logical fragment = redundancy

**Positive-fragment characterization.** Equivalent conditions:
- `truth(psi)` is already open;
- it is the inverse image of an upset in the signature poset;
- the induced truth bit is constant on coarse classes and isotone;
- on the realized carrier it can be represented by a positive formula in the old observations.

**Syntactic closure corollary.**
- Finite conjunction/disjunction of old observations is topologically redundant, though it may alter weighted distance if added as a weighted coordinate.

## 3.2 Anti-positive/antitone fragment

- Anti-positive normal form for class-constant antitone observations.

**Antitone profile decomposition.**
- After T0, an antitone observation block decomposes the refined poset according to equal new-coordinate patterns.
- Nonconstant antitone behavior can disconnect old components.

**Negation refinement.**
- Adding negations of selected old coordinates partitions by those truth patterns.
- Adding all negations deletes every strict inclusion and yields the discrete/two-sided observation topology.

## 3.3 Adjoint rigidity after T0

**Adjoint-rigidity theorem.**
- Once T0 is reached, a later refinement projection has a left/right order adjoint iff it is an order isomorphism.
- Thus the nontrivial homotopy-neutral post-T0 phenomena lie beyond the simplest adjoint mechanism.

## 3.4 Bounded-height signature posets

**Height-one rigidity theorem.**
- For post-T0 coarse height <=1, homology-neutrality iff redundancy.
- Any proper edge deletion changes graph homology/Euler characteristic.

**First possible nontrivial neutrality.**
- Nonredundant but homology-neutral post-T0 refinement requires height at least 2.

**Height-two matrix classification.**
- Relative chain complex is `0 -> k[T_del] -> k[E_del] -> 0`.
- Homology-neutrality iff the relative boundary map is an isomorphism.

**Fast obstruction.**
- If numbers of deleted edges and deleted triangles differ, neutrality is impossible.

**Simple-collapse certificate.**
- If deleted edges and deleted triangles pair uniquely by incidence, the coarse complex collapses onto the refined one.

## 3.5 Exact one-bit theory over a coarse chain

**Exact chain trichotomy.** For a bit word on `C_n`:
- nondecreasing `0...01...1` => redundant;
- nonconstant nonincreasing `1...10...0` => defective;
- every other word => nonredundant but homotopy-neutral.

**Exact counts.**
- redundant: `n+1`;
- defective: `n-1`;
- nonredundant homotopy-neutral: `2^n-2n`.

**Exact Quillen visibility.**
- Characterizes exactly when all lower or upper principal fibers are contractible.
- Gives exact count of neutral chain refinements missed by both Quillen tests.
- `1010` is the first alternating example highlighted.

## 3.6 Block universality over a coarse chain

- Any partial order on the same state set for which the coarse chain is a linear extension can be realized by a finite block of observations.
- This foreshadows the stronger same-vertex thinning universality in v0.5.

## 3.7 Refinement/update bifiltration

- After T0, observation refinement and premise restriction each produce inclusions in the same direction on order complexes.
- `K_{a,b}=Delta(P_{Phi_a,S_{Gamma_b}})` gives a two-parameter inclusion system.
- Reversing indices yields a genuine bifiltration and hence a multiparameter persistence module.

## 3.8 Computation

- Exhaustive enumeration of small finite posets confirmed height-one rigidity and the height-two matrix criterion.
- Chain theorem checked through longer chain lengths.
- Reported height-two search found many nonredundant homology-neutral cases, showing height 2 is genuinely the first rich regime.

---

# 4. v0.4 - Homotopy-Preserving Logical Observations

## 4.1 Descent formulation

- A descent is a comparable pair `p<q` with `b(p)=1`, `b(q)=0`.
- A coarse chain survives iff its truth values are nondecreasing.

## 4.2 Arbitrary-height repair maps

**Down-repair theorem.**
- If there is a monotone `rho:P->P` with `rho(p)<=p` and `b(rho(p))=0`, refinement preserves homotopy.

**Up-repair theorem.**
- Dually, monotone strengthening into true states preserves homotopy.

**False-floor / true-ceiling theorem.**
- Greatest false states below every point or least true states above every point supply canonical repair maps.

**Component anchor criterion.**
- It is enough for each component to have a least false state or greatest true state.

**Boolean-lattice endpoint test.**
- On a full Boolean signature lattice, `b(empty)=0` or `b(I)=1` guarantees homotopy preservation.

## 4.3 Closure systems and logical fragments

**Join-closed falsity theorem.**
- In a finite join-semilattice, join-closed lower-cofinal false states yield a false floor and therefore preservation.

**Meet-closed truth theorem.**
- In a finite meet-semilattice, meet-closed upper-cofinal true states yield a true ceiling and therefore preservation.

**Horn-type corollary.**
- Horn model sets are meet closed; under the realized-signature/cofinality hypotheses, a Horn-defined observation is homotopy safe.

**Dual-Horn corollary.**
- Dual result via union/join closure of false states.

Important caution: not every Horn formula is automatically safe; the semilattice and cofinality hypotheses matter.

## 4.4 Height-two repair graph

- Classify deleted triangle words:
  - `010`, `101`: one deleted edge; anchor triangles.
  - `100`, `110`: two deleted edges; dependency triangles.
- Build a formal root per coarse connected component and a graph vertex per deleted edge.
- One-deleted-edge triangles join the root to the deleted edge.
- Two-deleted-edge triangles join the two deleted-edge vertices.

**Relative boundary = reduced incidence proposition.**
- Over `F_2`, the relative boundary matrix is exactly the repair-graph incidence matrix with root rows removed.

## 4.5 Exact repair-forest theorem

For post-T0 height <=2 and one new observation, the following are equivalent:
- homotopy equivalence;
- simple homotopy equivalence;
- direct collapse by deleted edge-triangle pairs;
- `F_2` homology equivalence;
- invertibility of the relative boundary matrix;
- repair graph is a forest with exactly one root in each component.

This is the strongest exact theorem in the one-observation line.

Consequences:
- greedy leaf-pruning algorithm decides preservation;
- every descent cluster must have exactly one anchor and no cyclic dependency.

## 4.6 Worked logical examples

- `Phi=(X,Y)`, add XOR: nonredundant but repair-forest safe.
- Add XNOR: likewise safe by the dual pattern.
- Add NOR: repair graph has an unrooted component; homotopy fails and `H_0` changes.

## 4.7 Higher-dimensional extension

- Complete acyclic relative discrete-Morse matching is a general sufficient preservation criterion.
- v0.4 repair forests are the solved height-two one-bit instance.
- Open target: canonical first-descent matchings in higher dimension.

## 4.8 Computation

- Repair-map criteria tested on all naturally labelled small transitive posets in the search range.
- Height-two repair-forest equivalence exhaustively checked through six vertices.
- Reported search covered 184,088 one-observation height-two refinements, including 38,067 nonredundant neutral cases; no counterexample to the theorem occurred.

---

# 5. v0.5 - Simultaneous Observation Refinement

## 5.1 Block refinement as order thinning

For a new observation block `Theta=(theta_1,...,theta_k)` define its Boolean vector labelling `alpha_Theta(p)`.

**Block order-thinning theorem.**
- Same vertices after T0.
- `p<=_Psi q` iff `p<=_Phi q` and `alpha(p)<=alpha(q)` coordinatewise.

**Intersection theorem.**
- The joint refined order is the intersection of the coordinatewise refined orders.
- The joint order complex is the intersection of the coordinate complexes.

## 5.2 Coordinatewise, sequential, and joint safety

Definitions:
- coordinatewise homotopy-neutral;
- sequentially homotopy-safe.

**Sequential safety proposition.**
- If the observations can be ordered so that every cumulative step is a homotopy equivalence, the whole block is jointly neutral.

Crucially, neither coordinatewise safety nor joint safety determines the other.

## 5.3 Same-vertex order-thinning universality

**Order-thinning universality theorem.**
- For any finite post-T0 coarse poset `P` and any same-vertex suborder `Q subset P`, a finite block of propositional observations realizes exactly `Q`.
- Explicit construction uses principal downsets of `Q` as Boolean coordinates.

This is stronger and more directly refinement-specific than the v0.2 arbitrary-poset universality result.

## 5.4 Relative observation dimension

Proposed invariant:
- `odim_P(Q)` = minimum number of new Boolean observations needed to realize target same-vertex thinning `Q subset P`.

Results:
- `0 <= odim_P(Q) <= |P|`, with `odim_P(P)=0`.
- If `P` is a total order extending `Q`, `odim_P(Q)` equals classical poset 2-dimension.
- Therefore deciding `odim_P(Q)<=k` is NP-complete already in this special case.

Open directions:
- bounds via width, height, deleted-comparison structure;
- approximation algorithms;
- complexity for structured coarse ProLTs;
- logical-cost/topological-effect tradeoffs.

## 5.5 Coefficient-sensitive height-two block defects

- Integral relative boundary matrix `B_Z` between deleted triangles and deleted edges.
- If square:
  - nonzero determinant over a field iff homology-neutral over that field;
  - determinant nonzero over Q iff rationally neutral;
  - determinant `+-1` iff integrally neutral;
  - prime divisors of the determinant indicate characteristic-dependent defects.
- Proposed integral refinement weight `|det B_Z|`, later identified with established rooted-forest homological weight rather than claimed new.

## 5.6 Correct prior-art framework: higher-dimensional rooted forests

- Bernardi-Klivans higher-dimensional rooted forests already provide the determinant/rooted-forest framework.
- The ProLT relative boundary submatrix is exactly their boundary submatrix up to orientation signs.
- Therefore rationally neutral height-two block defects correspond to higher-dimensional rooted forests when deleted cell counts match.

This was an important correction: a new ad-hoc "repair hypergraph" should not be claimed.

## 5.7 Fitting orientations and Morse safety

- Fitting orientations correspond to perfect matchings between deleted edges and deleted triangles respecting incidence.
- **Morse-safe block:** admits an acyclic fitting orientation.
- A Morse-safe block collapses and is simple-homotopy neutral.
- Unique fitting orientation is sufficient for Morse safety because an alternating cycle would create a second perfect matching.

## 5.8 Interaction defects

Proposed terminology:
- **Destructive interaction:** every coordinate is individually neutral relative to the same coarse complex but the joint block is not.
- **Compensating interaction:** joint block is neutral although no coordinate can serve as a neutral first step.

### Destructive example
- Three-chain with coordinate words `010` and `101`.
- Each one-bit refinement is neutral.
- Their intersection is one edge plus an isolated vertex, changing `H_0`.
- Mayer-Vietoris interpretation: two contractible trees with union a circle and disconnected intersection.

### Compensating example
- Five-state block with two-bit labels.
- Neither coordinate alone is neutral.
- Joint block has determinant 1 and unique fitting orientation, hence collapses and is neutral.

Therefore:
- coordinatewise safe does not imply jointly safe;
- jointly safe does not imply sequentially safe.

## 5.9 Failure of the one-bit collapse equivalence for blocks

- Explicit eight-state, three-bit example.
- Integral determinant 1.
- Exactly three fitting orientations, all cyclic as relative discrete vector fields.
- Both coarse and refined posets dismantle to points.
- Hence inclusion is a homotopy equivalence but no complete acyclic deleted-edge/deleted-triangle fitting orientation exists.

**Theorem:** the v0.4 equivalence
`homotopy-neutral <=> direct repair collapse`
is special to the one-bit height-two regime and fails for blocks.

## 5.10 Computation

Focused exact checks verify:
- destructive three-chain;
- compensating five-state block;
- eight-state multi-orientation example.

Exhaustive small block search:
- 10,468 two-bit refinements on naturally labelled height <=2 posets through four vertices;
- 4,459 were `F_2`-homology-neutral;
- all 4,459 small neutral cases admitted greedy collapse;
- 100 cases had both coordinates individually neutral but joint block unsafe.

Larger randomized searches were discovery tools only; no minimality claim was made for the eight-state example.

---

# 6. Cross-version relationships that should not be lost

## 6.1 T0 is the major phase transition

Before T0:
- refinement can split observational equivalence classes;
- fiber-profile theory is required;
- adjoints and coarse-class possibility/forced truth are meaningful.

After T0:
- vertices are fixed;
- refinement is order thinning;
- order complexes only lose simplices;
- relative homology and discrete Morse/collapse methods become especially natural.

## 6.2 Mapping cone -> relative homology after T0/non-splitting

General refinement is represented by a map and mapping cone.
Once fine and coarse vertices can be identified, that cone becomes the ordinary relative complex `(O_Phi,O_Psi)`.

## 6.3 One bit is unusually rigid

At height two, one bit gives a very special relative matrix: every deleted triangle has only one or two deleted edges, so the boundary matrix is a reduced graph-incidence matrix.
This is why homology-neutrality, homotopy-neutrality, rooted-forest structure, and direct collapse coincide.

Blocks break this rigidity:
- deleted triangles can have three deleted edges;
- boundary matrices become general higher-dimensional rooted-forest matrices;
- multiple fitting orientations and determinant cancellation appear;
- direct collapse is no longer necessary for homotopy equivalence.

## 6.4 Homotopy and homology separate in two different ways

General unrestricted refinement:
- homotopy-neutrality is undecidable;
- homology-neutrality is finite linear algebra.

Controlled one-bit height-two refinement:
- homology-neutrality and homotopy-neutrality coincide exactly.

Multi-bit blocks:
- they separate again; relative matrix neutrality does not encode every global homotopy mechanism.

## 6.5 Topology-invariant versus presentation-sensitive layers

Topology-invariant:
- `P_Phi`, `O_Phi`, canonical ProLT homology.

Presentation-sensitive:
- compatibility/Dowker complex `K_Phi`;
- Stanley-Reisner ideal;
- weighted distances;
- Rips complexes and persistence based on those weights.

The tautology theorem is the canonical warning not to conflate these layers.

## 6.6 Refinement versus premise update

- Refinement changes what distinctions are observable.
- Premise update changes which worlds remain possible.
- After T0 they can be placed in a common two-parameter inclusion diagram/bifiltration.
- This is the cleanest route toward evolving logical/decision-state models without conflating epistemic vocabulary with admissible-state restriction.

## 6.7 XOR plays several distinct roles

Do not conflate:
- Boolean formula XOR;
- `F_2` chain addition;
- signature XOR/coboundary `Delta=delta lambda`;
- Hamming norm of the XOR vector;
- XOR as a specific new logical observation (which happens to be homotopy-safe in the `(X,Y)` repair-forest example).

## 6.8 Rooted repair forest versus higher-dimensional rooted forest

- v0.4 rooted repair graph is a very rigid one-bit special case.
- v0.5 identifies the correct established generalization as Bernardi-Klivans higher-dimensional rooted forests.
- Any future novelty claim must concern the ProLT/logical realization constraints, interaction, or observation-design problems, not the general rooted-forest machinery itself.

---

# 7. Repaired, rejected, or intentionally deferred ideas

These should remain in the record to prevent accidental reintroduction.

- Literal formula-level short exact sequences were type-incorrect; use free linearization or chain complexes.
- Commutative truth-set squares are not automatically homotopies/homology just because two paths agree.
- Over plain `F_2` vector spaces, short exact sequences split and Ext is trivial; richer rings/modules/sheaves are needed for nontrivial extension theory.
- The observation compatibility nerve is not the homology of the ProLT topology.
- Ordinary nerve-theorem conclusions cannot be used without good-cover-style hypotheses.
- Mapping-cone homology measures failure of a map to be a quasi-isomorphism; it should not be described unqualifiedly as literal "new features".
- Quillen/McCord fiber criteria are sufficient, not necessary.
- Relative update homology does not by itself mean inference failure.
- The T0 quotient loses multiplicity/removal information inside an observational equivalence class; valuation-level or sheaf/cosheaf refinements would be needed if microstate multiplicity matters.
- The Rips layer is not a topological invariant of `tau_Phi`; it depends on presentation and weights.
- Directed loss is not a linear coboundary invariant alone.
- A new "repair hypergraph" should not be claimed: higher-dimensional rooted-forest theory already exists.
- Horn/dual-Horn preservation requires the stated semilattice and cofinality hypotheses; it is not a blanket statement about all Horn formulas.
- No cognitive/mental-space interpretation has yet been made part of the mathematical claims; that is intentionally deferred.

---

# 8. Active research branches not yet exhausted

## A. Observation-interaction topology

- Mayer-Vietoris analysis of `K_1 cap K_2` and `K_1 cup K_2`.
- Define an interaction invariant separating coordinate defects from genuinely joint defects.
- Conditions guaranteeing intersection of individually neutral refinements is neutral.
- Higher-order interactions for three or more observations.
- Persistence of the first interaction defect in evolving observation sequences.

## B. Relative observation dimension

- Bounds on `odim_P(Q)`.
- Approximation and parameterized algorithms.
- Complexity on bounded-height/width/treewidth-like coarse orders.
- Relationship to classical 2-dimension, Boolean dimension, and deleted-comparison representations.
- Observation-cost versus topological-change optimization.

## C. Coefficient sensitivity and torsion

- Find ProLT block examples with `|det B_Z|>1`.
- Determine whether restricted logical fragments force total unimodularity.
- Classify primes/coefficients at which a refinement defect appears.
- Relate torsion/homological weight to logical structure.

## D. Logical fragments

Systematic simultaneous-refinement study of:
- Horn;
- dual-Horn;
- affine/XOR;
- bijunctive/2-SAT;
- monotone;
- unate.

Questions:
- Which fragments force sequential safety?
- Which force unique fitting orientations?
- Which force total unimodularity?
- Which admit polynomial-time preservation certificates?

## E. Homotopy criteria beyond relative matchings

- Beat-point/dismantlability criteria.
- Quillen-fiber criteria adapted to block order thinning.
- Secondary Morse matchings not confined to deleted cells.
- Higher-dimensional first-descent matchings.

## F. Premise/update homology

- Develop `U_k^Phi(Gamma)` and inference-gap groups beyond definitions/examples.
- Vanishing/nonvanishing logical criteria.
- Compare premise sets with the same classical conclusion.
- Study alternating refinement and premise accumulation.

## G. Boolean cohomology / local-to-global differences

- Integrability on richer complexes.
- Noisy/incomplete local differences.
- Nearest cocycle / nearest coboundary optimization.
- Possible applications to consistency checking or distributed/local reasoning.

## H. Compatibility algebra

- Stanley-Reisner Betti tables and syzygies.
- What these add beyond minimally unsatisfiable sets.
- Comparison between compatibility/Dowker topology and canonical order topology.

## I. Persistence and evolving spaces

- Refinement/update bifiltration.
- Multiparameter persistence.
- Metric/Rips barcodes.
- Nonmonotone changes via zigzag persistence.
- Continuous score/threshold functions -> nested Boolean observations -> persistent complexes.
- Event times when repair forests fail or interaction defects first appear.

## J. Cross-layer comparison theorems

Seek explicit relations among:
- canonical order-complex homology;
- compatibility/Dowker homology;
- metric/Rips persistence;
- refinement-defect homology;
- premise-relative homology.

A nontrivial theorem connecting layers would likely be more valuable than adding another isolated invariant.

## K. Deferred continuous-to-discrete / "mental space" program

Potential later hierarchy:
- continuous real-valued functions/scores;
- threshold predicates;
- observation signatures;
- finite information posets;
- order/metric complexes;
- chain/cochain invariants;
- time-indexed or multiparameter diagrams;
- decision/syllogistic interpretations only after the mathematical layer is stable.

---

# 9. Suggested publication architecture

## Paper 1 - Strongest near-term research manuscript

**Working title:** *Homotopy-Neutral Observation Refinement in Finite Logical Information Posets*

Core material:
- post-T0 order-deletion formulation;
- positive-fragment redundancy characterization;
- height-one rigidity;
- height-two relative boundary classification;
- exact chain trichotomy and enumeration;
- repair maps/floor-ceiling criteria;
- Horn/dual-Horn preservation under hypotheses;
- exact height-two repair-forest theorem;
- XOR/XNOR/NOR examples;
- exhaustive verification.

Optional background only:
- a short statement of the general fiber-profile formulation and mapping cone.

Do not include:
- compatibility/Dowker/Stanley-Reisner material;
- Rips persistence;
- mental-space interpretation;
- simultaneous-block interaction except perhaps one final outlook paragraph.

This paper has the cleanest single story: **when does adding one logical observation change the homotopy type?**

## Paper 2 - Simultaneous refinement and interaction

**Working title:** *Simultaneous Logical Observation Refinement and Topological Interaction*

Core material:
- block order thinning;
- intersection theorem;
- coordinatewise versus sequential versus joint safety;
- destructive `010/101` example;
- compensating five-state example;
- coefficient-sensitive height-two relative matrix;
- translation to established higher-dimensional rooted forests;
- fitting orientations and Morse-safe criterion;
- eight-state example showing failure of one-bit direct-collapse equivalence;
- next development: Mayer-Vietoris interaction invariant.

This should probably wait until the Mayer-Vietoris interaction theory is developed one level further, because that would give the paper a central invariant rather than only examples plus structural theorems.

## Paper 3 - Observation design / dimension (potential short paper or algorithms paper)

**Working title:** *Minimum Observation Dimension for Logical Order Refinement*

Core material:
- same-vertex order-thinning universality;
- definition of `odim_P(Q)`;
- relation to classical 2-dimension;
- NP-completeness inheritance;
- new lower/upper bounds;
- exact algorithms for structured `P`;
- approximation or parameterized results if found.

Current status: promising but not yet mature enough for a full paper on its own unless additional bounds/algorithms are proved. It could presently be a short research note.

## Technical Report / Foundation Note

**Working title:** *Homological and Cohomological Foundations for Propositional Logical Topologies*

Keep together:
- canonical order-complex homology;
- functoriality;
- premise-relative homology;
- inference-gap groups;
- mapping-cone refinement defects;
- XOR as coboundary and `H^1` integration obstruction;
- repaired old exact sequence;
- Dowker distinction;
- Stanley-Reisner route;
- Rips/persistence layer;
- worked examples;
- research roadmap.

This is valuable as a citable technical foundation, but most ingredients are standard/adapted rather than standalone novelty claims. It should support the research papers rather than carry all of their new theorems.

## Future Paper - Premise/update persistence and evolving reasoning

Not ready yet. It should wait for at least one genuinely new theorem connecting premise-relative homology, refinement, and/or persistence. The bifiltration is a good skeleton, but by itself is mainly a natural application of standard persistence machinery.

## Future Paper - Compatibility algebra

Also not ready yet. Dowker + Stanley-Reisner machinery is useful, but a paper needs a ProLT-specific theorem, algorithm, or invariant beyond the standard encoding of jointly satisfiable/minimally unsatisfiable families.

---

# 10. Recommended priority order

1. Freeze the v0.1-v0.5 ledger and preserve all code/data.
2. Develop Paper 1 first; it already has the clearest theorem arc.
3. Run an adversarial novelty audit specifically against the chain classification, repair-map logical classes, and repair-forest theorem.
4. Develop the Mayer-Vietoris interaction invariant for Paper 2.
5. In parallel, investigate `odim_P(Q)` bounds/algorithms to see whether it becomes Paper 3 or remains a section/short note.
6. Keep premise homology, cohomology, compatibility algebra, and persistence as tracked research branches, not as material forced into Papers 1-3.
7. Only after the mathematical papers stabilize, return to continuous-threshold/evolving "mental space" interpretations.

---

# 11. Bottom-line assessment

There is enough material for **more than one manuscript**, but not all branches are equally mature.

- **Paper 1 is already structurally mature**, subject to novelty verification and a rigorous editorial/audit pass.
- **Paper 2 has enough substance for a serious manuscript skeleton**, but would become much stronger after one interaction invariant/theorem beyond the existing counterexamples and intersection theorem.
- **Observation dimension is a legitimate third research direction**, currently at short-note stage until new bounds/algorithms are added.
- **v0.1 should remain a foundation/report rather than being overloaded into the main theorem papers.**
- Premise homology, Boolean cohomology, compatibility algebra, persistence, and continuous/evolving interpretations should remain visible in the ledger but separate until each develops its own nonstandard results.

The key editorial principle is: **one paper, one central mathematical question.** The current program now contains several such questions, and splitting them will make the strongest results easier to understand, audit, and defend.
