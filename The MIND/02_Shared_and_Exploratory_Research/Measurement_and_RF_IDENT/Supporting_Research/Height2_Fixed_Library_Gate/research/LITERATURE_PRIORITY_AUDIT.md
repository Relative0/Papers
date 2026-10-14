# Literature and priority audit

Audit date: 2026-09-29. This is a targeted primary-source search conducted during the transfer gate, with no asserted exhaustive coverage through 2026 and no proof of absence of earlier work. Source publication dates below come from the papers or publisher records; search-engine crawl dates are not publication dates. All claims of contribution remain provisional.

## Verdict

The adaptive formalism is a restricted decision tree with a support-dependent legal-action map. That formalism, its minimax recursion, and ordinary binary information bounds are established mathematics. The project cannot claim a new general adaptive-identification framework on that basis. The useful specialized content is the exact logical-to-incidence translation, its behavior under support restriction, and rigorously delimited consequences for supplied observation libraries.

The most defensible package is an exact repair-restriction theorem with explicit activation/deactivation mechanisms, together with examples and gap theorems showing what the topological legal-action predicate changes. Even that package has only low-to-moderate novelty confidence: much of its algebra is a short specialization of standard matrix and graphic-matroid facts. No publication-ready priority verdict has been established.

## Verified primary sources and what they do establish

| Source | Exact relevance checked | Boundary of the comparison |
|---|---|---|
| [Hyafil and Rivest, Constructing Optimal Binary Decision Trees is NP-Complete (1976)](https://people.csail.mit.edu/rivest/pubs/HR76.pdf) | Explicit finite objects, fixed Boolean tests, identification trees; principal cost is total external path length. | Do not quote its main result as if it proved minimum worst-case height. |
| [Laber and Nogueira, On the hardness of the minimum height decision tree problem (2004)](https://www2.ic.uff.br/~loana/decisiontree.pdf) | Explicitly minimizes worst-case test count; Theorem 1 gives a set-cover-based approximation-hardness reduction. | Appropriate source for the ordinary depth problem, not RF-IDENT feasibility hardness. |
| [Karbasi and Zadimoghaddam, Constrained Binary Identification Problem (STACS 2013)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2013.550) | Constrained Twenty Questions with graph, cost, and submodular query restrictions; adaptive identification and approximation bounds. | Different concrete restrictions and principally expected-cost objectives; no checked repair-forest predicate. |
| [Hoffmann and Brafman, Contingent Planning via Heuristic Forward Search with Implicit Belief States (ICAPS 2005)](https://cdn.aaai.org/ICAPS/2005/ICAPS05-008.pdf) | Belief states are sets of worlds; sensing actions split them; action applicability and AND/OR search are explicit. | Its universal pointwise preconditions are hereditary under pure support restriction; that special mechanism cannot produce repair-safety deactivation without changing the model. |
| [Kohler, Akrour, and Preux, Interpretable Decision Tree Search as a Markov Decision Process, v3 (2024), Sec. 5.1](https://arxiv.org/html/2309.12701v3#S5.SS1) | Explicit map phi:S->P(F) specifies a state-dependent admissible-test set, and dynamic programming solves the resulting state graph. | This is a classification/regularized-loss setting using heuristic test generation, not the same topological predicate. The generic state-dependent decision-tree architecture nevertheless predates this project. |
| [The later version, Breiman meets Bellman: Non-Greedy Decision Trees with MDPs (KDD 2025)](https://arxiv.org/html/2309.12701v5) | Confirms the same work's later title and publication version. | Distinguish the 2024 version title from the 2025 publication title. |
| [Cheraghchi, Karbasi, Mohajer, and Saligrama, Graph-Constrained Group Testing (2010 preprint)](https://arxiv.org/abs/1001.1445) | Pools satisfy graph connectivity restrictions; nonadaptive multi-defective identification is studied. | Connectivity of a queried pool is different from preserving an order complex before conditioning. |
| [Golovin and Krause, Adaptive Submodular Optimization under Matroid Constraints (2011)](https://www.cs.cmu.edu/~dgolovin/papers/1101.4450v1%20adapt_matroids.pdf) | Adaptive selection under fixed matroid/independence constraints has established approximation theory. | A repair matrix has a matroid on triangle columns, not automatically on supplied observations. No adaptive-submodularity or greedy-approximation theorem is transferred here. |
| [Bernardi and Klivans, Directed Rooted Forests in Higher Dimension (2016)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v23i4p35), [author manuscript](https://www.dam.brown.edu/people/cklivans/Forests.pdf) | Lemma 14 identifies rooted forests with square nonsingular boundary submatrices; fitting orientations and homological weights are already developed. | General rooted cellular-forest and determinant terminology is prior art, as v0.5 already acknowledges. |
| [Duval, Klivans, and Martin, Simplicial and Cellular Trees (2015 preprint; 2016 chapter)](https://arxiv.org/abs/1506.06819) | Cellular-matroid, higher-tree, and torsion background. | Supports the standard framework, not a new fixed-library adaptive theorem. |
| [Barmak and Minian, Simple Homotopy Types and Finite Spaces (2006 preprint)](https://arxiv.org/abs/math/0611158) | Finite-space collapses and their correspondence with simplicial collapses. | Finite posets and order-complex/simple-homotopy methods are established foundations. |

The source comparisons above are verified from primary documents or their primary records. Statements about how the ProLT model embeds or fails to embed into them are deductions of this audit, not claims made by those authors.

## Corrections already recorded in the transferred audit

The local `03_PROLT_PRIMARY_SOURCES/CLAIM_AUDIT_TABLE.csv` must accompany the source papers. Its V5-06 already marks the asserted total-order relative observation dimension / classical 2-dimension equality `FALSE/COUNTEREXAMPLE`; V5-07 marks its inherited complexity claim `NEEDS_MAJOR_REPAIR`. The two-chain check in the independent complexity audit confirms this known correction and is not a new discovery.

V5-09 already marks the block-to-rooted-forest translation `NEEDS_MINOR_REPAIR`: generating the auxiliary complex only from deleted triangles may omit unsupported deleted edges and their zero boundary rows. Use G=K^(1) union the deleted triangles, with retained edges as the root, or explicitly retain and handle the omitted rows. The present one-bit matrix/repair graph construction includes every descent edge, including isolated graph vertices.

V3-13 classifies the chain trichotomy as `PRIOR_ART_EQUIVALENT` and calls for disclosure of the unlocated Ehrenborg-Kitaev proof cited by the transferred audit. This audit has not located or independently checked that cited proof. The later hostile-audit theorem A1 remains preserved with its narrower ProLT-specific adaptive statement and moderate novelty assessment; it does not make the underlying chain classification new.

## The hostile reduction test

For fixed P0 and Q define A(S) to be the nonconstant supplied tests whose one-bit refinements are repair-safe on P0[S]. Branch cancellation implies that S is a complete state for future decisions. The resulting task is exactly deterministic identification with state-dependent available actions. A test has two successor supports, and a successful policy is an AND/OR solution tree ending in singletons.

This reduces the planning aspect to established decision-tree/belief-state ideas. It does not make the legal-action geometry vacuous: a general support-dependent map can be arbitrary, whereas here it comes from deleted chains and a particularly sparse relative boundary. The contribution must be a theorem exploiting that restriction, not renamed dynamic programming.

Standard contingent planning with preconditions holding in every possible world permits activation as the belief set shrinks. Such applicability is hereditary: once all surviving worlds satisfy a precondition, all subsets do too. Repair-safety can deactivate. This separates the concrete predicate from that particular simple sensing model; it does not establish priority over all epistemic planning or all state-dependent action models.

## Claim-by-claim novelty classification

| Proposed result | Classification | Reason |
|---|---|---|
| Branch cancellation | Definition-level specialization | Every previously observed coordinate is constant on the conditioned support. |
| Support-only DP and exact feasibility recursion | Standard algorithmic specialization | Ordinary Bellman / AND-OR recursion with a computable legal-action predicate. |
| RF-SAFE polynomial time | Direct source-theorem algorithm | Build the existing one-bit repair graph and test the forest condition. |
| RF-DEPTH NP-complete | Standard hardness transfer | Antichains recover unrestricted fixed-library depth; no repair geometry is needed. |
| Height-one polynomial RF-IDENT | Generic hereditary-action lemma plus ProLT specialization | Safety becomes isotonicity; a legal split cannot destroy feasibility. |
| Root splitting and exact retained-cell boundary formula | Useful ProLT structural synthesis | The graph representation must track support of every edge/triangle and coarse component. |
| Column-matroid deletion under conditioning | Elementary but important exact fact | Every retained triangle retains every incident descent row, so removed rows are zero on retained columns. |
| Minimal activation/deactivation examples | Concrete separating examples | Value lies in correctness and minimality, not in the word “activation.” |
| Sharp finite gap n-1-ceil(log2 n) | Elementary ProLT-specific extremal corollary | Star examples already realize it at height one with oriented libraries. |
| Exact complement-closed parity-family depth D_k=2^(k-1)+k-1 | Stronger structured-family result; provisional contribution candidate | Gives exact penalty n/2-1 even with complements supplied. It still occurs at height one. |
| A1 from the transferred audit | Preserved, no new claim | Arbitrary Boolean query profiles on chains differ from a fixed supplied library. |

The classifications are judgments, not bibliographic proofs. A correct elementary result may still be useful, but should not be described as a new general theory merely because its application vocabulary differs.

## Exact matroid boundary of novelty

Fix one observation r. Let B_S have rows E_r(S) (descent edges) and columns F_r(S) (deleted triangles). For T subset S,

    B_T = B_S[E_r(T), F_r(T)].

Every triangle in F_r(T) has all three vertices in T, hence every descent in its column lies in E_r(T). Therefore the removed rows in B_S[:,F_r(T)] are zero. All column dependences are unchanged, giving

    M(B_T) = M(B_S) restricted to F_r(T).

Thus the represented matroid evolves by deletion. A blanket claim of “no clean matroid-minor operation” is false. Graphically the formal roots may split, but identifying all formal roots gives an ordinary graphic representation with exactly this column matroid. Safety additionally demands spanning all remaining descent rows; matroid independence alone omits this condition. If B_S is invertible, B_T is injective and safety is equivalent to |F_r(T)|=|E_r(T)|. Conditioning cannot create a new column cycle; loss of anchoring/full row rank explains deactivation.

This argument is an elementary consequence of standard represented-matroid restriction. Its value here is preventing incorrect claims about rank updates, root changes, and newly created cycles.

## Depth-gap caveats and a stronger family

The extremal oriented-library gap supplied elsewhere in the gate is mathematically useful, but it does not require height-two triangles. A height-one star already suffices. Moreover, complementing its antitone code queries makes them isotone, eliminating that family's penalty. That dependence must be stated.

Complement closure does **not** eliminate all gaps. The independently audited family in `COMPLEXITY_INDEPENDENT_AUDIT.md`, C6, uses all k-bit words, with every even-parity word below every odd-parity word. Supply coordinates and singleton indicators, including all complements. For k>=2, coordinate safety forces deletion of a whole layer/bit cell of n/4 vertices. The untouched opposite bit half is a smaller instance; charging any earlier deletions in that half gives the exact recurrence D_k=n/4+1+D_(k-1), with D_1=1. Consequently d_RF=n/2+k-1, d_ad=k, and the exact penalty is n/2-1. This structured-family theorem is stronger than a mere unbounded-gap example. It remains a height-one construction and leaves the special value of height-two deactivation to be justified separately. Its exact statement has not received an exhaustive priority audit.

## Search coverage and unresolved priority

Queries covered restricted Twenty Questions, minimum-height decision trees, constrained binary identification, state-dependent test sets, contingent sensing, graph-constrained group testing, adaptive matroid constraints, rooted cellular forests, and finite-space simple homotopy. Strong exact matches were found for the general decision process and for the rooted-boundary algebra. No exact fixed-library ProLT repair-safety theorem was located in this targeted search.

That last observation is not an originality certificate. Detailed citation chasing for adaptive test cover, epistemic action preconditions beyond universal pointwise conditions, and poset-search variants remains incomplete. A public “first” claim or high-confidence priority claim would exceed the evidence.

## Recommended publication gate

Keep the focus on the exact restriction theorem and a structural result that needs nonhereditary legality at height two. General RF-IDENT complexity, or an efficient complete algorithm on a natural height-two class, would add more substance than another decision-tree restatement. The complement-closed gap is a useful supporting theorem. Before drafting a principal novelty claim, perform a targeted second audit against those precise statements and have an independent referee reconstruct their proofs.

## Final narrow priority check: exact parity-family theorem

After the exact recurrence was proved, five additional targeted web searches were run on 2026-09-29. These are the exact query strings:

1. `"decision tree" "poset" "parity" "monotone"`
2. `"decision tree" "complete bipartite" "coordinate" "singleton"`
3. `"identification" "isotone" "queries"`
4. `"decision tree" "2^{k-1}" "k-1" "parity"`
5. `"search" "posets" "queries" "two-level" monotone`

The target was the conjunction of a two-level complete bipartite order defined by Boolean parity classes, a supplied coordinate-plus-singleton library with complements, support-relative isotone admissibility, and exact depth 2^(k-1)+k-1. No returned source inspected in this narrow pass gave that construction, recurrence, or exact theorem.

The principal apparent matches were different problems, checked at their primary sources:

- [Besselman et al., Direct Sums for Parity Decision Trees (CCC 2025)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol339-ccc2025/html/LIPIcs.CCC.2025.16/LIPIcs.CCC.2025.16.html) permits linear parity queries to compute functions and proves direct-sum results. Here parity defines the two poset layers; parity queries are not part of the supplied library. The models must not be conflated.
- [Blanc et al., Decision Tree Heuristics Can Fail, Even in the Smoothed Setting (2021)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol207-approx-random2021/LIPIcs.APPROX-RANDOM.2021.45/LIPIcs.APPROX-RANDOM.2021.45.pdf) studies failure of greedy learning heuristics. It does not provide the checked support-relative isotone identification model or the exact parity-family depth formula.
- [Canonne et al., Testing k-Monotonicity: The Rise and Fall of Boolean Functions (2019)](https://theoryofcomputing.org/articles/v015a001/) concerns property testing of an unknown Boolean function on a poset. In the present theorem the functions are supplied and monotonicity restricts which test may be asked on the surviving support. This is a different role for monotonicity.

**Result and limitation.** The exact theorem survives this small targeted search in the limited sense that no direct prior theorem was located. Five search strings and inspection of the apparent primary-source matches do not exhaust differently named models, unpublished work, or citation networks. The audit therefore retains provisional low-to-moderate novelty confidence and does not make a “first” claim. Mathematical verification of the recurrence is substantially stronger than the present evidence about priority.
