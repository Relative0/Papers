# PROJECT STATE SNAPSHOT — Structured Factorization

**Snapshot date:** 29 September 2026  
**Current gate:** **G. MORE RESEARCH REQUIRED**  
**Immediate next phase:** **Phase 5B — real SDD + incremental SAT validation of factor-exposure vtree adaptation**

## A. Core exact problem

The project studies exact semantic AND-factorization of Boolean functions, together with a simplicial/carrier partition and Correspondence-Matrix (CM) four-corner rank certificates. The exact combined target is the canonical simultaneous finest partition obtained by reconciling carrier structure with the semantic prime AND-partition.

A recurring design discipline is:

> certify whatever can be extracted directly from structure; split into independent residual blocks; use exact four-corner SAT only where structure leaves uncertainty.

## B. Phase 4 results that survived

### B1. Fixed-cut CM criterion

For a cut `A | B`, conjunctive separability is equivalent to rank at most one of the Boolean flattening over `F_2`. This is the semantic four-corner basis for the exact SAT oracle.

### B2. Compressed-SDD cut criterion

For a compressed SDD decision at vtree split `X | Y`, a nonfalse function factors as `g(X) AND h(Y)` iff the compressed decision has at most one nonfalse sub. Recursive use gives the exact finest factorization whose blocks are vtree subtrees. Full semantic prime factorization follows when the vtree is prime-aligned.

The fixed balanced four-variable vtree exposed the full semantic prime partition for only 225 of 2,601 decomposable nonfalse functions; 2,376 had a strictly finer unrestricted prime partition. This identified **vtree alignment** as the dominant limitation of that direct route.

### B3. Read-once/support-disjoint CM/LM operator-tree theorem

For operator trees whose child supports are disjoint, a local two-state rank recursion computes the exact semantic prime AND-partition. Rank-one gate states split into signed conjunction factors; rank-two essential gates fuse the two child supports into one semantic prime block. The bundled validation checked 35,210 instances with zero discrepancies.

This is not a claim that read-once factorization itself is new. The potentially project-specific content is the exact CM-rank/four-corner formulation and proof discipline.

### B4. Persistent four-corner SAT encoding

Phase 4 built one permanent four-copy semantic CNF with carrier-block selectors. Candidate cuts are expressed as selector assumptions rather than by rebuilding the whole formula. Logical assumption-equivalence was validated. The environment did not have an industrial assumption-capable CDCL backend, so **encoding reuse was established but runtime/learned-clause speedup was not**.

## C. Phase 5 results that survived

### C1. Exposure-optimum theorem — PROVED

If `E_T(f)` is the exact finest factorization directly exposed by vtree `T`, then

`max_T |E_T(f)| = |Pi_f|`,

where `Pi_f` is the semantic prime AND-partition.

Interpretation: direct factor count is a ground-truth-free objective for scoring a candidate vtree. This theorem does **not** provide an efficient global vtree search algorithm; an oracle-aligned tree makes the optimum existence unsurprising.

### C2. Carrier/semantic laminar compatibility — PROVED

All carrier blocks and semantic prime blocks can simultaneously be represented as vtree subtrees iff their combined block family is laminar. Therefore a crossing carrier partition must not be hard-locked into the vtree unless compatibility is certified.

### C3. Defect-support crossing lemma — PROVED

A nonzero four-corner witness whose assignments vary on support `U` on one side of a cut and support `W` on the other certifies that at least one semantic prime block intersects both `U` and `W`.

Singleton/singleton support yields a sound pairwise must-link corollary.

### C4. Universal pairwise defect localization — REFUTED

For the family

`f_n(x) = 1 iff x = 0^n or x = 1^n`,

the complete variable set forms one semantic prime block, yet no fixed-context two-variable rank-two witness exists. On the balanced cuts checked for `n = 3,4,5,6`, minimum total defect support equals `n`.

Consequently, failed cuts should generally be represented as **support hyperedges/crossing constraints**, not automatically collapsed to pairwise interaction edges.

### C5. Positive irredundant CNF component theorem — PROVED, PRIOR-ART-DOMINATED BASELINE

For positive irredundant CNF, connected clause/primal interaction components match semantic AND-prime blocks. This is useful as a positive control, but independent-component decomposition is established preprocessing and is not positioned as the main novelty.

## D. Completed computation

### D1. Complete four-variable vtree universe

All 65,535 nonfalse four-variable functions and all 15 labelled binary vtrees were evaluated.

Key numbers:

- semantically decomposable functions: **2,601**;
- fixed balanced vtree full alignment on decomposable functions: **225 / 2,601 = 8.65%**;
- mean full-alignment probability of a uniformly random vtree on decomposable functions: **21.94%**;
- exhaustive exposure optimization reaches the semantic optimum for **65,535 / 65,535** functions.

The Phase 5 implementation corrected a label-order issue that would arise if the Phase 4 small validator were reused unchanged on arbitrary leaf permutations. The original Phase 4 fixed-balanced experiment was unaffected.

### D2. Five-variable synthetic campaign

Seed: `20260929`; 540 total instances over three families. On clean factorable CNFs, syntax-component initialization achieved 100% full alignment. Hard carrier locking failed completely on deliberately crossing carrier/semantic regimes. Semantically redundant syntactic crossings degraded syntax-component alignment, illustrating the difference between syntax and semantic dependence.

These are structural small-universe results, **not industrial runtime evidence**.

## E. Novelty/priority boundary currently frozen

The literature/priority work found substantial antecedents for:

- dynamic vtree search and local rotations;
- SDD-size minimization;
- graph/treewidth/hypergraph-guided compilation;
- independent-component preprocessing;
- SAT/QBF Boolean bi-decomposition.

Therefore the strongest project-specific candidates are narrower:

1. factor-exposure as a vtree-search objective distinct from ordinary SDD-size minimization;
2. the exact carrier/semantic laminar obstruction;
3. CM defect-support hyperedges/crossing constraints and their sound localization theorem;
4. the exact hybrid combination of direct exposure with persistent residual four-corner SAT.

Any future paper must re-check priority through the publication date.

## F. What has NOT been established

- No practical algorithm is yet proved to find an exposure-optimal vtree efficiently.
- No unrestricted pairwise defect-localization theorem survives.
- No actual SDD node-count/runtime rotation benchmark has been completed with maintained SDD tooling.
- No industrial incremental-SAT runtime or learned-clause advantage has been demonstrated.
- No held-out end-to-end result yet shows that carrier/defect-aware adaptation beats standard SDD-size/treewidth/syntax baselines.

## G. Immediate next work — Phase 5B

The next agent must run a focused industrial validation, not another broad survey. It should:

1. obtain a maintained SDD implementation with explicit vtree control/local optimization if possible;
2. obtain an assumption-capable incremental SAT backend;
3. reproduce Phase 4/5 frozen results before tuning;
4. implement exact direct-extraction + residual persistent-SAT factorization;
5. compare fixed/random, standard SDD-size, syntax/treewidth, factor-exposure, joint size+residual-work, soft-carrier, and CM defect-support-hypergraph methods;
6. freeze train/validation/held-out splits and tuning rules before seeing held-out results;
7. use total exact hybrid runtime as the primary held-out metric;
8. return either a reproducible improvement, a theorem/parameterized result, or a clean NO-GO.

See `NEXT_AGENT_PROMPT_PHASE5B.md` for the exact protocol and deliverables.
