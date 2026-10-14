# Phase 5B — Industrial SDD + Incremental SAT Validation of Factor-Exposure Vtree Adaptation

## Role

You are an independent research/engineering team specializing in:

- Sentential Decision Diagrams (SDDs) and structured d-DNNF;
- vtree construction, search, and local rotations;
- knowledge compilation;
- exact Boolean AND-factorization / bi-decomposition;
- incremental SAT with assumptions;
- graph/hypergraph partitioning and treewidth-guided compilation;
- Correspondence-Matrix (CM) four-corner rank certificates;
- experimental algorithmics and reproducibility;
- theorem verification and adversarial mathematical review.

This is a **focused continuation**, not a new broad survey. The purpose is to test whether the Phase 5 structural findings can be turned into a genuine practical improvement when using a real SDD implementation and a real incremental SAT backend.

Do not assume the previous results are correct merely because they are in the package. Reproduce and attack them first.

---

# 1. Materials

Read the complete attached handoff package before designing the experiment.

The two nested source packages are:

1. `02_COMPLETE_PACKAGES/STRUCTURED_FACTORIZATION_PHASE4_2026-09-29.zip`
2. `02_COMPLETE_PACKAGES/STRUCTURED_FACTORIZATION_PHASE5_T2_2026-09-29.zip`

Start with:

- `01_KEY_DOCS/PHASE5_PHASE5_T2_MASTER_REPORT.md`
- `01_KEY_DOCS/PHASE5_NEXT_RESEARCH_GATE.md`
- `01_KEY_DOCS/PHASE5_THEOREM_NOTE_DRAFT.tex`
- the Phase 4 `PHASE4_MASTER_REPORT.md` and `docs/SDD_DIRECT_EXTRACTION.md` inside the Phase 4 ZIP.

Treat all theorem claims and empirical numbers as hypotheses to verify.

---

# 2. Frozen Phase 5 findings to re-check

Phase 5 reported the following. Reconstruct each proof or computation independently before relying on it.

## F1 — Factor-exposure optimum

For the exact finest factorization `E_T(f)` exposed recursively by the compressed-SDD criterion on vtree `T`,

\[
\max_T |E_T(f)| = |\Pi_f|,
\]

where `Pi_f` is the canonical semantic prime AND-partition.

The intended significance is that direct factor count is a ground-truth-free objective for scoring a candidate vtree, although global search over vtrees is combinatorial.

## F2 — Carrier/semantic laminar obstruction

A carrier partition and semantic prime partition can simultaneously have all blocks represented as vtree subtrees iff the combined block family is laminar. Therefore crossing carrier blocks must not be hard-locked unless compatibility is certified.

## F3 — Defect-support theorem and pairwise NO-GO

A four-corner defect witness with varying supports `U` and `W` across a cut certifies that some semantic prime block intersects both supports. Singleton/singleton support gives a sound must-link edge.

However, the family

\[
f_n(x)=1 \iff x=0^n \text{ or } x=1^n
\]

was reported as a counterexample to universal pairwise localization: the whole variable set is one semantic prime block, yet fixed-context two-variable rank-two witnesses do not exist, and balanced-cut witnesses may require support on all variables.

## F4 — Small-universe baseline

For all 65,535 nonfalse 4-variable Boolean functions and all 15 labelled binary vtrees, Phase 5 reported:

- 2,601 semantically decomposable functions;
- fixed balanced vtree full alignment on 225/2,601 = 8.65%;
- mean full-alignment probability of a uniformly random vtree on decomposable functions about 21.94%;
- global exhaustive factor-exposure search reaches the semantic optimum for every function.

## F5 — Five-variable synthetic signal

Syntax-component initialization reportedly performs perfectly on clean factorable CNFs but degrades when syntactically crossing clauses are semantically redundant. Hard carrier locking fails sharply on deliberately crossing carrier/semantic partitions.

These findings are **not yet an industrial runtime result**.

---

# 3. Central Phase 5B question

Determine whether a real implementation of

> vtree adaptation for **direct semantic factor exposure**, optionally aided by soft carrier information and CM defect-support hyperedges,

can outperform established SDD-size/treewidth/syntactic baselines on the **total exact hybrid factorization task**, without compromising correctness.

The primary question is not whether a clever vtree can expose factors. The oracle control already answers that.

The question is whether useful alignment can be found automatically, cheaply enough to matter in an end-to-end exact solver/compiler workflow.

---

# 4. Required tooling gate

Before experiments, attempt to install or use maintained implementations for:

- an actual SDD compiler/library with explicit vtree control and, if possible, dynamic/local vtree operations;
- an assumption-capable incremental SAT solver/backend;
- graph/hypergraph partitioning or tree-decomposition tooling if useful.

Good candidates may include maintained PySDD/SDD tooling and PySAT-backed solvers, but choose based on what is current and actually available in the environment.

Record exact versions, installation commands, solver names, compiler configuration, machine/runtime information, and random seeds.

### Hard reporting rule

If an actual SDD compiler cannot be made available, do **not** report emulated quantities as SDD node counts or compiled sizes.

If a real incremental SAT backend cannot be made available, do **not** claim learned-clause, conflicts, decisions, propagation, or runtime advantages from a simulated oracle.

If either industrial tool is unavailable, complete whatever exact mathematical work remains possible and return a limitation verdict rather than manufacturing a positive result.

---

# 5. Reproduction gate

Before tuning a new method:

1. reproduce the Phase 4 exact cut criterion on bundled validation cases;
2. reproduce the Phase 5 4-variable exhaustive counts;
3. reproduce the laminar carrier obstruction theorem independently;
4. reproduce the defect-support lemma and the `f_n` counterexample computationally at least through the sizes in the package;
5. reproduce the five-variable benchmark summaries from the supplied seeds/data.

If any frozen result fails, stop and repair the theory/code before proceeding.

Document all discrepancies.

---

# 6. Exact hybrid pipeline to implement

The final solver must preserve exactness:

1. construct an initial vtree;
2. compile to a real compressed SDD, or use the closest exact maintained representation if the library exposes equivalent structure;
3. recursively extract all factors certified directly by SDD structure;
4. combine with any carrier partition only by an exact compatibility/refinement operation;
5. isolate unresolved residual blocks;
6. invoke persistent/incremental four-corner SAT only within unresolved blocks;
7. return the exact canonical simultaneous finest factor partition.

No heuristic is allowed to delete or merge an exact factor incorrectly. Heuristics may affect efficiency only.

---

# 7. Vtree methods to compare

Implement at least the following, subject to the capabilities of the real SDD library.

## B0 — Fixed balanced baseline

A deterministic balanced vtree with fixed variable order.

## B1 — Random vtree baseline

Multiple seeded random labelled binary vtrees.

## B2 — Standard SDD-size optimization

Use the library's established dynamic vtree search / local rotation / minimization method where available. This is a crucial prior-art baseline.

## B3 — Syntax/treewidth initialization

Construct a vtree from CNF primal/incidence structure, components, separators, tree decompositions, or hypergraph partitioning using a reasonable standard method.

## M1 — Factor-exposure-only local search

Use only ground-truth-free direct extraction information to score local vtree moves.

Primary candidate score:

- number of directly exposed blocks;
- or directly resolved variable volume;
- with deterministic tie-breaking.

Do not use the true `Pi_f` in this objective.

## M2 — Joint SDD-size + residual exact-work objective

Search using a preregistered objective combining quantities such as:

- real SDD size;
- direct exposed variable volume;
- number/size of residual blocks;
- estimated or measured residual SAT cost.

Tune only on training data.

## M3 — Soft carrier weighting

Carrier structure may bias clustering or rotations but must not hard-lock crossing carrier blocks unless laminar compatibility has been certified.

## M4 — CM defect-support hypergraph weighting

Represent failed-cut witnesses as support hyperedges/crossing constraints.

Only create a sound pairwise must-link when singleton/singleton localization is actually certified.

Investigate witness support minimization, repeated SAT queries, unsat/sat cores, and group testing only if mathematically sound.

## M5 — Hybrid carrier + defect + factor-exposure

Combine soft carrier evidence, defect-support hyperedges, and the direct factor-exposure objective.

## O — Oracle prime-aligned control

Build a vtree directly from independently computed ground-truth prime blocks when feasible.

This is an upper bound only, never an algorithmic competitor.

---

# 8. Local-search protocol

Where possible, use the same elementary vtree neighborhood as established dynamic SDD search (e.g. rotations and child swaps) so comparisons are fair.

For every local move, separately record:

- change in real SDD size;
- change in direct factor exposure;
- change in residual block volume;
- change in measured residual SAT cost;
- compilation/search overhead.

Investigate whether factor-exposure and SDD-size objectives are aligned, orthogonal, or antagonistic.

A particularly valuable result would be a Pareto analysis showing when reducing SDD size hides factors, or exposing factors enlarges the SDD but reduces total hybrid runtime.

---

# 9. Benchmark protocol — freeze before tuning

Create a benchmark manifest and train/validation/held-out split **before tuning any weights**.

Include at least:

- clean factorable CNFs;
- partially factorable CNFs;
- factorable formulas with redundant syntactic cross-links;
- bounded-treewidth CNFs;
- random CNFs;
- read-once/operator-tree functions;
- repeated-module functions;
- carrier/semantic aligned instances;
- deliberately crossing carrier/semantic instances;
- indecomposable controls;
- public knowledge-compilation/model-counting/SAT benchmark instances when feasible and licensing permits.

The held-out set must not influence parameter tuning, objective weights, or algorithm design decisions.

If exact ground-truth prime partitions become too expensive at industrial sizes, use them only on a separately marked evaluable subset. The end-to-end exact hybrid solver itself can still be measured without exposing ground truth to the heuristic.

---

# 10. Primary and secondary metrics

## Primary held-out metric

**Total exact hybrid runtime**, including:

- vtree construction/search;
- SDD compilation/recompilation;
- direct extraction;
- carrier/defect processing;
- residual incremental SAT;
- final exact partition assembly.

## Secondary metrics

Record at least:

- real SDD node/edge size as exposed by the library;
- vtree search time;
- direct prime-factor count;
- fraction of variables resolved directly;
- number of residual blocks;
- residual variable volume;
- residual block-size distribution;
- number of four-corner SAT calls;
- SAT conflicts/decisions/propagations where available;
- SAT wall time;
- total wall time;
- peak memory;
- compilation failures/timeouts;
- correctness agreement with an independent exact baseline on instances where both finish.

Do not call a reduction in encoding size a solver speedup.

---

# 11. Statistical discipline

For stochastic methods:

- use fixed published seeds;
- run enough replicates to estimate variability;
- report median, mean where meaningful, robust spread, and paired comparisons;
- keep timeouts and censoring rules fixed in advance;
- report negative and null results.

Do not cherry-pick benchmark families or successful seeds.

For the held-out comparison, emphasize effect sizes and paired per-instance outcomes rather than only aggregated averages.

---

# 12. Focused theorem program

Do **not** restart an unrestricted theorem hunt.

Attack only theorem targets that are directly motivated by the implementation.

Preferred parameters:

- defect-support width `d`;
- maximum carrier block size `b`;
- interaction/treewidth `w`;
- monotone-shrinkable witness support;
- number/size of semantic blocks crossing a candidate cut.

Aim for one of:

### T1 — Defect localization bound

A proved query bound for shrinking a failed-cut defect to a certified support hyperedge under a meaningful structural assumption.

### T2 — Residual-size bound

A proved bound on unresolved residual block size or volume after a specified adaptation procedure under a useful parameter.

### T3 — Hybrid complexity bound

A bound showing that the cost of direct exposure plus residual exact SAT is fixed-parameter tractable or otherwise improved under a stated parameter.

### T4 — Objective relation theorem

A theorem or counterexample clarifying the relationship between SDD-size-optimal vtrees and factor-exposure-optimal vtrees.

A clean impossibility theorem is acceptable and may be more valuable than a weak positive statement.

---

# 13. Literature and priority audit through the current date

Perform a current web/literature search before making novelty claims.

At minimum cover:

- dynamic SDD vtree search;
- vtree rotations / child swaps;
- SDD minimization;
- structured d-DNNF;
- treewidth/dtree/vtree construction;
- hypergraph partitioning for compilation;
- component decomposition in SAT/model counting;
- Boolean bi-decomposition via SAT/QBF;
- decomposition-aware knowledge compilation;
- recent work on compilation objectives other than representation size;
- witness/core-guided structural search;
- 2025–2026 work relevant to dynamic decomposition and compiler structure.

Produce a claim-by-claim priority matrix distinguishing:

- established prior art;
- known technique applied to a new objective;
- theorem genuinely supported here;
- empirical contribution only;
- conjecture/open direction.

Do not claim novelty for dynamic vtree search, rotations, graph-guided compilation, or independent-component decomposition merely because they appear in this implementation.

---

# 14. Adversarial review

After the strongest result is obtained, run at least these internal reviewers:

1. SDD/knowledge-compilation specialist;
2. SAT/Boolean-decomposition specialist;
3. graph/treewidth/vtree specialist;
4. algorithm-engineering/statistics reviewer;
5. hostile novelty/priority referee;
6. hostile mathematical referee focused on any new theorem.

They must attack:

- leakage of ground-truth prime factors;
- held-out contamination;
- unfair baselines;
- hidden recompilation costs;
- timeout bias;
- conflating SDD-size improvement with factorization improvement;
- conflating fewer SAT calls with faster SAT;
- unsound conversion of defect witnesses into pairwise constraints;
- carrier hard-locking;
- theorem assumptions and quantifiers;
- reproducibility;
- priority over existing vtree and bi-decomposition literature.

Revise the work based on valid criticism and preserve a review ledger.

---

# 15. Stop rule

If carrier/defect-aware objectives do not beat standard syntax/treewidth/SDD-size baselines on held-out **total exact hybrid runtime** or on a clearly preregistered residual-work metric with meaningful practical benefit, record a NO-GO.

Do not rescue a negative runtime result by changing the primary metric after seeing the held-out data.

If the algorithmic result is negative but the carrier/defect theorems survive, preserve them as a separate mathematical note.

---

# 16. Deliverables

Produce one complete ZIP containing at minimum:

1. `PHASE5B_MASTER_REPORT.md`
2. `TOOLING_AND_ENVIRONMENT.md`
3. `REPRODUCTION_AUDIT.md`
4. `INDUSTRIAL_SDD_PIPELINE.md`
5. `INCREMENTAL_SAT_PIPELINE.md`
6. `VTREE_SEARCH_OBJECTIVES.md`
7. `DEFECT_HYPERGRAPH_METHOD.md`
8. `BENCHMARK_PROTOCOL.md`
9. `BENCHMARK_RESULTS.md`
10. `STATISTICAL_ANALYSIS.md`
11. `THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md`
12. `LITERATURE_PRIORITY_AUDIT.md`
13. `HOSTILE_REVIEW_LEDGER.md`
14. `THEOREM_STATUS.csv`
15. benchmark manifests and all random seeds
16. machine-readable per-instance CSV/JSON results
17. complete reproducible code
18. dependency lockfile / environment specification
19. stdout/stderr logs for the principal runs
20. `NEXT_RESEARCH_GATE.md`
21. a paper/theorem-note LaTeX draft **only if** the surviving contribution warrants one.

Also include checksums for the final package.

---

# 17. Final decision categories

End with exactly one primary decision:

A. **INDUSTRIAL HYBRID IMPROVEMENT ESTABLISHED**

B. **USEFUL PARAMETERIZED THEOREM + SUPPORTING EMPIRICS**

C. **STRONG FACTOR-EXPOSURE RESULT, RUNTIME BENEFIT NOT ESTABLISHED**

D. **MATHEMATICAL NOTE SURVIVES; ALGORITHMIC NO-GO**

E. **PRIOR-ART-DOMINATED**

F. **NO-GO**

G. **MORE RESEARCH REQUIRED**

Then state separately and unambiguously:

- what is mathematically proved;
- what is computationally reproduced;
- what is newly observed on held-out instances;
- what is known prior art;
- what failed;
- what remains conjectural;
- whether the result is publication-ready, and if so in what form.

Do not let an attractive benchmark result be described as a theorem, and do not let a theorem about structure be described as an industrial speedup without measured evidence.
