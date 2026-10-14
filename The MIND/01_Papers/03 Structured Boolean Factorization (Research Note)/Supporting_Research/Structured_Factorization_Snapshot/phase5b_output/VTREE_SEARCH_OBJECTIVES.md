# Implemented vtree methods and objectives

All non-oracle methods receive original-variable CNF, carrier partition, and published seed. Semantic prime partitions are computed in a separate evaluator and supplied only to O. `code/benchmark.py` is the executable definition; `BENCHMARK_PROTOCOL.md` and `PROTOCOL_CLARIFICATIONS.md` were fixed before new runs.

| Method | Implementation |
|---|---|
| B0 | Deterministic balanced vtree over numeric variable order |
| B1 | Seeded random recursive split/shuffle tree, one per replicate; not uniform on all trees |
| B2 | B0 followed by PySDD's maintained native size minimization |
| B3 | Primal components, greedy min-fill order within each, balanced vtrees on those orders |
| M1 | B3 initialization, maximize direct exposed block count |
| M2 | B3, minimize log2(1+SDD size)+log2(1+residual cut-volume proxy) |
| M3 | M2 plus unit-weight soft carrier span penalty |
| M4 | M2 plus unit-weight minimized defect-support union span penalty |
| M5 | M2 plus both penalties |
| O | Build clades from independently evaluated semantic prime partition; upper/evaluation control only |

The span penalty is mean `(smallest containing clade size - support size)/n`. It is a heuristic cohesion preference. It asserts neither that a whole defect support is one prime block nor that a crossing carrier may be hard locked. U and W and witness assignments remain in the data. The union is used only as a soft feature. A singleton/singleton defect is flagged as a sound must-link, but this implementation does not use it to force tree constraints.

The residual proxy sums `2^(|B|-1)-1` over directly exposed nonsingleton blocks. It counts their first-pass cut universes, not exact recursive SAT cost or runtime. All coefficients were set to one before the experiment; no training or held-out tuning occurred. Serialization is deterministic tie-breaking. M1's tie break uses tree serialization, with no hidden size or prime-partition objective.

Every M method considers child swaps and binary rotations, including below the root. Each of at most two rounds evaluates the first six unseen serialized neighbors; at most twelve new trees are compiled. This intentionally bounded pilot policy is sensitive to variable labels and can miss improving moves. Native B2 does not have an equivalent candidate budget; the comparison measures implemented end-to-end workflows, not an isolated objective under equal search engineering.

Each trace stores actual SDD size, exposed count, residual variable volume, structural deltas, compilation/extraction overhead, candidate tree and parent tree. `move_diagnostics.py` measures residual SAT on recorded partitions afterward, outside the search objective and primary timer. Its separately stored costs are diagnostic observations. A size/exposure tradeoff observed on a candidate pair is not a theorem that one objective generally dominates another.

An exposed block is a valid factor, not necessarily a prime factor. Every nonsingleton exposed block is exact-refined, including in O, unless a separate prime certificate is supplied (none is supplied in this campaign). The evaluator's direct-prime count is attached only after a worker returns. Singleton fraction is the safe direct-resolution metric available to the algorithm.
