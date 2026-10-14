# Phase 5 T2 Master Report — Carrier- and CM-Defect-Aware Vtree Adaptation

**Date:** 29 September 2026  
**Final decision:** **G. MORE RESEARCH REQUIRED**

## Executive finding

Phase 5 did **not** establish a new general-purpose carrier/CM-guided vtree adaptation algorithm with a proved asymptotic advantage or a held-out industrial runtime win. It did establish several exact structural results that materially sharpen the next research gate:

1. **Global factor-exposure optimization is complete.** If `E_T(f)` is the exact finest factorization exposed by the compressed-SDD criterion on vtree `T`, then
   \[
   \max_T |E_T(f)| = |\Pi_f|.
   \]
   This follows because a vtree can be built around the semantic prime blocks. The point is not existence, but that **number of directly exposed blocks is an exact, ground-truth-free search objective**. Exhaustive search is, however, combinatorial and is not itself an efficient algorithm.

2. **Carrier hard-locking has an exact compatibility boundary.** A carrier partition `Pi_K` and semantic prime partition `Pi_f` can both have every block represented by a vtree subtree iff their block families are laminar. Crossing carrier/semantic blocks make simultaneous subtree alignment impossible. Thus carrier blocks are safe as *hard* vtree constraints only when this compatibility condition is certified; otherwise they should be soft evidence.

3. **CM defect localization has a sound support theorem but a sharp pairwise NO-GO.** If a four-corner witness varies only coordinates `U` on one side and `W` on the other, then at least one semantic prime block meets both `U` and `W`. Singleton/singleton support therefore gives a sound must-link edge. But the family
   \[
   f_n(x_1,\dots,x_n)=1 \iff x=0^n\text{ or }x=1^n
   \]
   is one semantic prime block, has no rank-two two-variable fixed-context slice at all, and on a balanced cut requires a witness varying all `n` coordinates. So universal pairwise localization by minimizing a four-corner witness is false.

4. **The strongest easy prime-alignment class is already close to standard component decomposition.** For an irredundant positive CNF, connected components of the clause/primal interaction graph coincide with semantic AND-prime blocks; building a vtree around those components is prime-aligned. This is useful as a correctness baseline, but its novelty is weak because independent component decomposition is standard SAT/knowledge-compilation preprocessing.

5. **The empirical signal is real but representation-dependent.** On all 65,535 nonfalse four-variable functions and all 15 labelled binary vtrees, a fixed balanced vtree fully exposed only 225 of 2,601 decomposable functions (8.65%). Uniformly averaging over all vtrees raises the decomposable-function alignment probability to about 21.94%. Exhaustive factor-exposure search over all 15 vtrees reaches the semantic optimum on all 65,535 functions, as the theorem predicts.

6. On the five-variable synthetic benchmark (540 instances, preregistered seed `20260929`), syntax-component vtrees are perfect on clean factorable CNFs but degrade when redundant cross-component clauses destroy syntactic separation. Hard carrier locking is perfect when the carrier is aligned, and fails sharply on deliberately crossing clean-factor instances. Global factor-exposure search is perfect by construction but is only an exponential upper/control procedure.

The net result is a **clearer architecture**, not yet a publishable new adaptation theorem:

> use certified syntactic/module decomposition first; treat carrier blocks as soft unless laminar compatibility is known; use CM defects as hyperedge/module evidence rather than automatically as pairwise edges; optimize direct factor exposure with local vtree moves; retain exact residual SAT so heuristics can only affect efficiency.

---

## 1. What was verified from Phase 4

The Phase 4 compressed-SDD cut criterion and the vtree-alignment limitation were taken as hypotheses and rechecked against the bundled exact truth-table machinery. The key Phase 4 empirical number is reproduced: for the fixed balanced four-variable vtree `((x0,x1),(x2,x3))`, 2,601 functions are semantically decomposable but only 225 are fully exposed by that fixed tree.

The Phase 4 incremental SAT and SDD code was inspected. The current environment has neither `pysdd` nor `python-sat`, so this phase does **not** claim actual compiled-SDD sizes, learned-clause speedups, SAT conflict reductions, or industrial runtime improvements. Small-universe SDD behavior is emulated exactly through semantic cut/cofactor criteria.

---

## 2. Exact theorem: exposure-optimal vtrees

Let `Pi_f={B_1,...,B_k}` be the canonical semantic prime AND-partition of a nonfalse Boolean function `f`. Let `E_T(f)` denote the finest partition exposed recursively by the exact compressed-SDD split criterion on vtree `T`.

### Theorem 2.1 — exposure optimum equals semantic prime count

For every nonfalse Boolean function,

\[
\max_T |E_T(f)|=|\Pi_f|.
\]

### Proof

`E_T(f)` is always a valid AND-factor partition, hence a coarsening of `Pi_f`, so `|E_T(f)|<=|Pi_f|`.

Conversely, construct a binary vtree in which every prime block `B_i` is a subtree and then combine those block subtrees arbitrarily into a binary tree. Every internal split is then a union of prime blocks versus its complementary union and is therefore a valid factor cut. Recursive direct extraction reaches all `B_i`. Hence equality is attained.

### Significance

The theorem is stronger than the bare oracle-alignment observation in one useful respect: it says that **direct block count itself is a complete optimization objective over vtrees**. One does not need the prime partition to *score* a candidate vtree; the compressed-SDD criterion scores it directly. But the vtree search space has `(2n-3)!!` labelled binary trees, so the theorem gives no polynomial-time search method.

---

## 3. Exact theorem: carrier-lock compatibility

Let `Pi` and `Sigma` be two partitions of the same variable set. Call the union of their block families *laminar* when any two blocks are disjoint or one contains the other.

### Theorem 3.1 — simultaneous subtree representation

There exists a binary vtree in which every block of `Pi` and every block of `Sigma` is the leaf set of a subtree **iff** the combined block family `Pi union Sigma` is laminar.

### Proof sketch

Subtree leaf sets in a rooted tree form a laminar family, proving necessity. For sufficiency, any finite laminar family can be represented as a rooted inclusion tree; binary refinement of nodes with more than two children preserves all required clusters.

### Corollary 3.2 — exact carrier hazard

A carrier-initialized method that *hard-locks every carrier block as a subtree* cannot be fully semantic-prime-aligned whenever `Pi_K` and `Pi_f` contain a crossing pair of blocks.

This is not merely an empirical warning. It is an exact obstruction. Carrier structure should therefore be treated as:

- a hard vtree constraint only when compatibility is known or guaranteed by the model class;
- otherwise a soft clustering weight or a source of residual-block information after semantic extraction.

---

## 4. Defect localization

### Lemma 4.1 — witness-support crossing

Take a failed cut `A|B` and a nonzero four-corner witness. Let `U subseteq A` be the coordinates on which `a0` and `a1` differ and `W subseteq B` the coordinates on which `b0` and `b1` differ. Then at least one semantic prime block intersects both `U` and `W`.

### Proof

Suppose no prime block intersects both varying sets. Restrict every prime factor to the fixed coordinates of the witness. Each factor then depends on row variation only, column variation only, or neither. Its 2x2 corner table is rank one. Entrywise multiplication of rank-one outer products is again rank one, so the whole four-corner determinant is zero, contradiction.

### Corollary 4.2 — sound pairwise must-link

If `U={x}` and `W={y}`, then `x` and `y` belong to the same semantic prime block.

This is the safe way to convert a CM defect into a pairwise edge: **only after** localization has reduced both witness supports to singletons.

### Theorem 4.3 — pairwise localization NO-GO family

For `n>=3`, let

\[
f_n(x)=1 \iff x=0^n \text{ or } x=1^n.
\]

Then:

- `Pi_{f_n}={V}` is a single semantic prime block;
- every two-variable restriction obtained by fixing all other variables has rank at most one;
- therefore the pairwise rank-two interaction graph is empty;
- for any nontrivial cut `A|B`, a defect witness exists, but it must vary all variables of `A` and all variables of `B`.

The bundled computation checks `n=3,4,5,6`; on a balanced cut the minimum total witness support is exactly `n` in each case.

### Consequence

A general algorithm cannot assume that a failed cut can be distilled to a sound pairwise must-link edge. CM defects should be represented as **support hyperedges / crossing constraints** unless singleton localization succeeds.

---

## 5. Positive prime-alignment baseline from positive irredundant CNF

### Proposition 5.1

For a positive irredundant CNF (no clause contains another), the connected components of its clause/primal interaction graph equal the semantic AND-prime blocks.

### Reason

Positive irredundancy makes each clause a prime implicate: with no negative literals there is no cross-clause resolution mechanism that creates a stricter positive clause, and a positive clause is entailed only when some input clause is contained in it. If the function factors across disjoint variable sets, a prime implicate cannot straddle the two factors: otherwise choose a model of each factor falsifying its own side of the clause and combine them. Hence every prime clause lies within a semantic factor; conversely disconnected clause components are explicit conjunctive factors.

### Status

The statement is mathematically useful, but the algorithmic idea is not a novelty claim. Detecting disconnected CNF components and compiling/solving them independently is established preprocessing and knowledge-compilation practice. This proposition is best used as a **positive control class** for vtree construction.

---

## 6. Exhaustive four-variable campaign

All 65,535 nonfalse functions and all 15 unordered labelled rooted binary vtrees were evaluated.

| Metric | Result |
|---|---:|
| Nonfalse functions | 65,535 |
| Semantically decomposable | 2,601 |
| Labelled binary vtrees | 15 |
| Fixed balanced tree fully aligned on decomposable functions | 225 / 2,601 = 8.65% |
| Mean alignment probability of a uniformly random vtree on decomposable functions | 21.94% |
| Global exposure optimum reaches full semantic prime partition | 65,535 / 65,535 |

Number of vtrees that are fully aligned for each function:

- exactly 1 aligned vtree: 108 functions;
- exactly 3 aligned vtrees: 2,412 functions;
- all 15 aligned: 63,015 functions.

The `all 15` category includes the 62,934 indecomposable functions, for which every vtree correctly returns the one-block partition, plus highly factorable cases whose prime blocks are all singletons.

The corrected exhaustive code deliberately computes the vtree-laminar coarsening from the exact prime partition for *evaluation*. This avoids a label-order bug that appears if the Phase 4 small validator is applied unchanged to arbitrary leaf permutations; the original Phase 4 fixed balanced experiment is unaffected because it used its fixed local ordering.

---

## 7. Five-variable benchmark campaign

### Protocol

- seed: `20260929`;
- 5 variables;
- 180 instances per family, 540 total;
- all 105 labelled binary vtrees available for the global exposure-search control;
- families:
  1. clean factorable CNFs;
  2. factorable CNFs with semantically redundant but syntactically crossing clauses;
  3. random CNFs;
- methods:
  - fixed balanced tree;
  - one uniform random tree;
  - syntax-component tree;
  - carrier-hard-locked tree;
  - exhaustive global exposure-search control.

`Residual cut volume` is the number of nontrivial bipartitions inside unresolved blocks under a naive exhaustive residual-cut accounting. It is a structural workload proxy, **not** a measured SAT runtime or solver speedup.

### Selected results

#### Clean factorable CNF

| Method | Full alignment | Mean direct blocks | Mean residual cut volume |
|---|---:|---:|---:|
| Fixed | 5.0% | 1.13 | 13.84 |
| Random | 8.33% | 1.20 | 13.34 |
| Syntax components | 100% | 2.49 | 3.67 |
| Carrier locked (mixed carrier regimes) | 36.11% | 1.60 | 10.46 |
| Global exposure search | 100% | 2.49 | 3.67 |

Carrier-lock stratification on the clean family:

- aligned carrier: 100% full alignment;
- crossing carrier: 0% full alignment;
- singleton carrier: 8.33% full alignment.

The zero for deliberately crossing carriers is the empirical manifestation of Theorem 3.1.

#### Redundant-cross factorable CNF

Syntactic crossing clauses connect components even though they are semantically redundant. Syntax-component alignment falls to 80%, while global semantic exposure search remains 100%. This is the expected boundary between syntactic interaction and semantic dependence.

#### Random CNF

No simple heuristic dominates. Fixed, random, syntax-component and mixed carrier locking range from roughly 48% to 63% full alignment in this tiny regime; the global exposure control remains 100%. These are small synthetic results only and should not be generalized to industrial formulas.

---

## 8. Literature/priority outcome

The literature audit changes the novelty posture in four ways.

1. **Dynamic vtree search and local rotations are established.** Choi and Darwiche (AAAI 2013) explicitly navigate vtree space using rotations and child swaps to minimize SDD size. A Phase 5 paper cannot claim vtree rotation/search itself as new.

2. **Graph/tree-decomposition-guided compilation is established.** Structured d-DNNF/SDD compilation has long used dtrees, treewidth, hypergraph partitioning and related decompositions; recent work continues to compare static tree decompositions with dynamic graph partitioning.

3. **Independent components are established preprocessing.** SAT and decision-DNNF/model-counting systems routinely detect disconnected components and solve/compile them independently.

4. **SAT/QBF Boolean bi-decomposition is established.** Earlier work already uses SAT/QBF to discover AND/OR/XOR decompositions and optimize variable partitions. The CM four-corner formulation remains a useful exact certificate, but generic “use SAT/QBF to find a cut” is not novel.

The most distinctive surviving mathematical content of this phase is therefore the **carrier/semantic laminar obstruction** and the **defect-support localization theorem plus higher-order counterexample**, together with the factor-exposure objective as a vtree-search target distinct from ordinary SDD-size minimization.

---

## 9. Hostile review synthesis

### SDD/knowledge-compilation reviewer

**Attack:** The global exposure theorem is nearly tautological because an oracle-aligned vtree exists. The empirical optimum over all vtrees is therefore not evidence of a practical algorithm.

**Accepted.** The report explicitly treats global search as an upper/control result. The next phase must test local rotations with a factor-exposure objective and compare against standard size minimization on real SDDs.

### Boolean-decomposition reviewer

**Attack:** Syntax components and positive-CNF component theorems are standard decomposition dressed in new language.

**Accepted.** They are retained only as baselines/controls, not novelty claims.

### Graph/vtree reviewer

**Attack:** Hard-locking carrier blocks is unjustified when carrier and semantic partitions cross.

**Accepted and strengthened to an exact theorem.** Crossing partitions are incompatible as simultaneous vtree clusters.

### Hostile empirical reviewer

**Attack:** Five variables and synthetic CNFs cannot support claims of runtime improvement; exhaustive vtree search leaks semantic difficulty into the method; no actual SDD or industrial SAT backend was used.

**Accepted.** No solver-speed or industrial-runtime claim is made. The global search is an upper bound/control. A proper held-out industrial campaign remains required.

---

## 10. Final status table

| Item | Status | Strength |
|---|---|---|
| Exposure-optimum theorem | PROVED | exact, but not an efficient search theorem |
| Carrier/semantic laminar compatibility theorem | PROVED | exact and directly useful |
| Witness-support crossing lemma | PROVED | exact |
| Singleton defect => must-link corollary | PROVED | exact |
| Universal pairwise defect localization | REFUTED | explicit infinite counterexample family |
| Positive irredundant CNF prime alignment | PROVED | useful, likely prior-art dominated |
| Four-variable all-vtree experiment | COMPLETE | exhaustive |
| Five-variable benchmark | COMPLETE | synthetic, exact small-universe |
| Actual SDD size/rotation benchmark | NOT DONE | tooling absent |
| Industrial incremental SAT runtime benchmark | NOT DONE | tooling absent |
| New general prime-alignment heuristic theorem | NOT ESTABLISHED | open |
| Useful query bound for defect localization | NOT ESTABLISHED | open |

---

## 11. Decision

# G. MORE RESEARCH REQUIRED

### Mathematically proved

- exposure optimum equals semantic prime count;
- exact laminar compatibility criterion for carrier and semantic subtree constraints;
- defect-support crossing lemma and singleton must-link corollary;
- pairwise-localization impossibility family;
- positive irredundant-CNF component alignment baseline.

### Computationally observed

- exhaustive n=4 all-function/all-vtree statistics;
- exact n=3..6 localization counterexamples;
- synthetic n=5 benchmark trends.

### Known prior art

- dynamic vtree rotations/search;
- SDD-size minimization objectives;
- treewidth/dtree/hypergraph-guided compilation;
- independent component preprocessing;
- SAT/QBF bi-decomposition.

### Conjectural / open

- whether local vtree search using factor exposure rather than SDD size materially reduces residual SAT work on real held-out benchmarks;
- whether CM support-hyperedges can guide rotations better than standard graph/hypergraph signals;
- whether a useful parameterized query bound exists for localization when defect support width is small;
- whether carrier information helps as a soft prior after correcting for crossing/laminar incompatibility.
