# Priority and Tractability Frontier — Phase 3

## Established external barriers

1. **SAT bi-decomposition is prior art.** Lee, Jiang, and Hung (DAC 2008) use interpolation and incremental SAT for Boolean bi-decomposition and automatic variable partitioning.
2. **QBF unknown-partition bi-decomposition is prior art.** Chen, Janota, and Marques-Silva (DATE 2012) explicitly treat OR, AND, and XOR bi-decomposition and use existential partition controls plus universal functional variables to obtain exact/optimal partitions.
3. **Bounded-width QBF is FPT.** Capelli and Mengel show fixed-parameter algorithms for bounded-treewidth quantified CNF with bounded quantifier alternation, via structured d-DNNF/knowledge compilation; their runtime is an iterated-exponential function of width whose tower height depends on the number of quantifier blocks, times linear/polynomial input size.
4. **Bounded-treewidth circuits/CNFs compile efficiently.** Multiple knowledge-compilation results convert bounded-treewidth Boolean circuits/CNFs to structured deterministic DNNF with singly-exponential dependence on treewidth in the unquantified case.

## What therefore survives as project-specific

- the use of the **simplicial carrier prime partition** as a hard admissibility constraint on cuts;
- the exact **CM rank-one/four-corner** interpretation of AND-separability;
- the **simultaneous finest partition** rather than an arbitrary good bi-decomposition;
- the combined incidence-width formulation involving both semantic clauses and carrier minimal nonfaces;
- explicit exact certificates and a carrier-aware implementation pipeline.

## Current sharp frontier

| Regime | Status |
|---|---|
| General CNF, fixed cut | coNP-complete (Phase 2 / prior AND-decomposition results) |
| General CNF, only carrier-block count `k` bounded | still coNP-hard already at `k=2` |
| Positive irredundant CNF + minimal-nonface carrier | polynomial via combined interaction hypergraph |
| General CNF + bounded combined incidence treewidth `tau` | FPT by the carrier-aware QBF theorem (Phase 3; synthesis/corollary-level novelty) |
| Fixed cut + arbitrary succinct circuit | exact SAT four-corner test; worst-case coNP-complete |
| ANF / multilinear Boolean polynomial | polynomial factorization already well developed; low novelty priority |

## Best next theorem target after this phase

The next target should **not** be another generic treewidth corollary. Better possibilities are:

- an explicit low-tower or singly-exponential algorithm for the *simultaneous finest partition* on a narrower but useful representation (e.g. structured d-DNNF / bounded decision width), improving materially over generic bounded-alternation QBF;
- a conditional lower bound showing that the tower/exponential width dependence is unavoidable for carrier-aware exact recovery;
- an incremental-SAT theorem/empirical result showing provable or reproducible amortized savings from carrier-constrained cut families and CM defect-core reuse;
- a CM/LM-specific syntactic subclass where separability can be recovered directly from the operator DAG faster than general Boolean bi-decomposition.
