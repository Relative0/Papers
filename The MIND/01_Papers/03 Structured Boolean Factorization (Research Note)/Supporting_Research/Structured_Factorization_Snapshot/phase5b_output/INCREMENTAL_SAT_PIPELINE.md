# Persistent exact four-corner SAT

`code/hybrid_core.py::FourCornerSession` constructs one fixed Tseitin CNF and
one PySAT `g4` (Glucose 4.1 binding) session. The construction independently
reimplements the logical encoding in archived Phase 4
`code/incremental_four_corner.py`; no archive file is modified or imported at
runtime. The new package is self-contained.

For each original variable there are assignment clones x0,x1 and a selector
s. Two ITE outputs supply the mixed corner coordinates. Every original CNF
clause output, formula output, ITE, and conjunction is defined by an
equivalence. In particular the encoder supports empty clauses and empty CNFs.
The four formula outputs F00,F01,F10,F11 satisfy the permanent defect assertion

    (F00 AND F11) XOR (F01 AND F10).

One complete selector assumption vector specifies a candidate cut. SAT
returns an explicit rank-two four-corner witness. UNSAT certifies that all
nonzero rows of the cut matrix agree, hence exact AND separability for the
nonfalse function. The persistent solver and base clauses are reused across
every residual query in one factorization, so learned clauses remain available
under normal assumption semantics. We measure solver counters directly through
`accum_stats()`; reuse is an implementation fact, not a claimed speed advantage
over fresh solving without a paired experiment.

The hybrid first obtains a certified direct partition from actual SDD
structure. Each singleton is complete. Every nonsingleton is recursively
tested across all unordered nontrivial bipartitions, with its least coordinate
on the first side and a fixed increasing-cardinality order. A successful UNSAT
cut produces two independently certified factors and recursion continues.
Exhausting the cuts certifies the block prime. There is no truth-partition
shortcut for a block which an evaluator happens to know is prime.

Queries use the original global function: the proposed sub-block is on side
A, and all other variables are on its complement. This is sound because all
outside residual blocks are already certified independent factors. Multiplying
by a nonfalse outside factor cannot change whether the active factor is
separable across the proposed cut. This argument requires nonfalsity and a
certified starting partition; `exact_refine` documents that precondition and
does not accept a guessed partition as a certificate.

The exact semantic result is assembled before applying carrier information.
The returned simultaneous partition is the least common coarsening of the
semantic prime partition and the supplied carrier partition. This is exact
but can spend more work than a comparator which directly restricts residual
cuts to unions of carrier blocks. We intentionally preserve this distinction:
the benchmark measures semantic factorization plus carrier assembly, and
does not claim an optimal carrier-constrained residual implementation.

Residual metrics include base construction time, SAT wall time, SAT calls,
variables/clauses, accumulated conflicts/decisions/propagations/restarts, and
complete residual wall time. No conflict, learned-clause, or solver speedup is
inferred merely from a reduced encoding or number of queries.

Worst-case enumeration is exponential in unresolved block size. If initial
block sizes are b_i, this implementation uses at most

    sum_i (2^b_i - b_i - 1)

four-corner oracle calls, counting recursive queries. The simpler sum of
`2^(b_i-1)-1` only bounds a single pass, not all recursive retesting. This is
an oracle-query bound, not an FPT runtime theorem: the global SAT encoding
still contains all original variables and clauses.

`code/validate_hybrid.py` compares the persistent backend to independent model
projection/cardinality criteria on every nontrivial cut of its small-function
and seeded CNF test subset. Complete semantic results and carrier LCCs are
also checked against separate brute-force relation/graph implementations.

The recorded backend validation passed 1,390 independent cut comparisons and
881 complete semantic-factorization comparisons, together with 881 carrier
LCC comparisons. There were zero discrepancies. These finite computations
support the implementation; the mathematical correctness argument remains
separate from empirical testing.

## Measured reuse diagnostic

Real Glucose4 comparisons completed 180 runs and 14,220 exact cut-answer checks. Persistent/fresh-same-base paired geometric end-to-end ratio is 0.124832; persistent/fresh-cut-specific-Phase3 ratio is 0.106228. This closes the archived claim's measurement gap only on a small training-only all-cuts workload. It is known incremental-SAT engineering, not a new vtree-search gain or a measured learned-clause count. Full scope and component times: SUPPLEMENTARY_DIAGNOSTICS.md.
