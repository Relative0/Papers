# DECISION AND GATE HISTORY

## Pre-Phase 4 baseline / Phase 3 inheritance

The project entered Phase 4 with an exact fixed-cut four-corner/CM rank criterion for Boolean AND-separability, a carrier-aware simultaneous finest-partition construction using the LCC of carrier and semantic partitions, and a fresh-SAT fixed-cut baseline. Phase 3 materials are preserved inside the Phase 4 package under `baseline_phase3/`.

## Phase 4 — direct extraction + persistent exact fallback

### Question

Can the semantic prime AND-partition be extracted directly from structured compiled/operator representations, reducing generic SAT/QBF work?

### Convergence

The unrestricted structured-d-DNNF route did **not** yield a universal theorem. Two useful exact subclasses survived:

1. compressed SDDs give exact factor extraction relative to the vtree, becoming full semantic prime extraction when prime-aligned;
2. support-disjoint/read-once CM/LM operator trees admit exact local CM-rank recursion.

The SAT branch was converted from rebuilt formulas to one persistent selector-controlled four-copy encoding, with candidate cuts represented as assumptions. Correctness/encoding reuse was established; industrial CDCL runtime gain remained untested.

### Phase 4 next gate

The gate proposed three targeted directions: controlled repeated-support operator DAGs, carrier/defect-aware vtree adaptation, and industrial incremental SAT benchmarking. Phase 5 pursued the vtree/defect direction first.

## Phase 5 T2 — carrier- and CM-defect-aware vtree adaptation

### Question

Can carrier information and/or CM four-corner defects be used to construct or adapt a vtree that exposes substantially more true semantic prime factorization directly, without already knowing the answer?

### Convergence

The phase established exact structural results and clear negative boundaries:

- direct factor exposure has an exact vtree optimum equal to semantic prime count;
- carrier and semantic block hard-locking is possible exactly under laminar compatibility;
- defect witnesses provide sound support-crossing information;
- singleton-pair localization is valid when it occurs;
- universal pairwise localization is false, with an explicit infinite counterexample family;
- small exhaustive/synthetic experiments show that alignment matters and hard crossing carriers can be harmful.

However, the phase did not have real industrial SDD and incremental SAT tooling. Therefore structural proxy improvement could not be called an end-to-end solver speedup.

### Phase 5 gate decision

**G. MORE RESEARCH REQUIRED.**

The next phase is deliberately narrow: run a real SDD + incremental SAT validation comparing established baselines with factor-exposure, soft carrier, and defect-support-hypergraph objectives under a frozen held-out protocol.

## Phase 5B — current task

The current task is fully specified in `NEXT_AGENT_PROMPT_PHASE5B.md`.

The primary decision sought is one of:

- a reproducible held-out end-to-end improvement that survives hostile review and priority checking;
- a meaningful parameterized theorem/complexity result tied to bounded defect support/carrier size/treewidth;
- a clean NO-GO showing that the new signals do not outperform established vtree/compilation methods sufficiently to justify an algorithm paper.

## Historical integrity rule

Past phase packages are frozen provenance. Corrections belong in new ledgers and new outputs. Do not silently rewrite an old phase to make later findings look inevitable.
