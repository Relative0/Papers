# Next Research Gate — Phase 5 Candidates

**Date:** 29 September 2026

Phase 4 closes the first direct-extraction attack. The next phase should not broaden all three branches indiscriminately. It should test two targeted extensions and one implementation gate.

## T1 — Controlled repeated-support CM/LM DAGs

### Goal

Extend the exact read-once CM-rank recursion to a strict super-class in which variable support may repeat but the repetition is controlled.

### Candidate contracts

Investigate separately:

1. **read-\(r\)** operator DAGs for small fixed \(r\);
2. **module-shared DAGs**, where repeated support occurs only through named shared subfunctions whose truth function is canonicalized;
3. **bounded overlap graph/treewidth**, where each pair of child supports intersects in a small separator;
4. **deterministic shared modules**, where shared branches cannot cancel under XOR or be absorbed without a locally visible certificate.

### Success criterion

A theorem that outputs the exact semantic prime AND partition in

\[
f(r,w)\operatorname{poly}(|D|)
\]

or in polynomial time for a nontrivial canonical subclass, with an explicit obstruction/counterexample showing why weaker hypotheses fail.

### Required adversarial tests

Include at least:

- XOR duplicate cancellation: \(h\mathbin{\Updownarrow}h=0\);
- absorption: \(h\vee(h\wedge q)=h\);
- shared complement interactions;
- repeated support that is syntactically shared but semantically irrelevant;
- cases where every local gate CM is rank two but the global function factors after cancellation.

## T2 — Carrier-/defect-aware vtree adaptation

### Goal

Improve the fraction of semantic prime factors exposed directly by SDD structure.

### Baseline fact

For the fixed balanced 4-variable vtree, 2,376 of the 2,601 decomposable nonfalse Boolean functions had a full prime partition strictly finer than the finest vtree-laminar partition. Hence fixed-vtree alignment is the dominant limitation in the small exhaustive universe.

### Candidate algorithms

Compare:

1. vtree initialized from the carrier prime partition;
2. vtree initialized from the semantic variable-interaction graph;
3. vtree rotations driven by four-corner SAT witnesses/cores;
4. hybrid carrier + semantic interaction clustering;
5. an oracle vtree chosen from the known prime partition, as an upper-bound control.

### Success criterion

Either:

- prove that a specified construction guarantees prime alignment for a meaningful semantic class; or
- obtain a reproducible reduction in residual SAT cuts / compiled size on a benchmark set, without claiming a theorem unsupported by the data.

## C1 — Industrial incremental SAT benchmark

### Goal

Replace the validation DPLL with an assumption-capable CDCL solver while keeping exactly the same persistent base encoding.

### Required comparison

For each benchmark and identical cut order compare:

- fresh four-corner solver per cut;
- persistent base solver with selector assumptions;
- direct-extraction + persistent SAT residual hybrid.

Record at least:

- wall-clock time;
- SAT calls;
- variables/clauses emitted;
- decisions;
- propagations;
- conflicts;
- learned clauses retained if exposed by the API;
- peak memory;
- number/size of residual blocks after direct extraction.

### Gate

Do not make a speedup claim unless persistent solving improves a preregistered aggregate metric on held-out instances. Encoding reuse alone is already established and should not be conflated with solver speed.

## Convergence rule

Return to the master thread after T1 and T2 each produce either a theorem/counterexample boundary or a clearly documented NO-GO, and after C1 produces a reproducible comparator table. Do not expand to sheaf/cosheaf semantics before this gate closes.
