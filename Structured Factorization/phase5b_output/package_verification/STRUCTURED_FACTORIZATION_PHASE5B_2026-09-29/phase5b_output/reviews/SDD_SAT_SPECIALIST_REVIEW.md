# SDD and SAT specialist adversarial audit

This is a self-audit of the backend implementation, not an independent
external referee report. A separate agent should still inspect the benchmark
and aggregate claims. Validation counts below are stored in the machine-readable
test report rather than copied before the run completes.

Backend validation is now complete: 903 real SDD compilations, 113 dynamic
minimizations, 881 direct/semantic/carrier comparisons of each type, 1,390 SAT
cut comparisons, 46 witness checks, and 80 deletion-minimality queries; zero
discrepancies. The 22 false cases were correctly marked outside the nonfalse
factorization contract.

1. **Trimmed nodes can invalidate a naive extractor.** A literal or decision
   normalized below the queried vtree node is not the ancestor's decision
   partition. Resolution: the implementation descends the appropriate branch,
   splits the complementary true scope into free singleton factors, and checks
   the final partition against model projections, including after minimization.

2. **One exposed block is not automatically one proved prime.** A failed root
   split may conceal cross-vtree factors. Resolution: all nonsingleton direct
   blocks receive exact residual search. Objective terms based on exposed
   nonsingletons are labelled block exposure/residual estimates; any actual
   direct-prime statistic requires evaluation-only truth labels.

3. **False formulas have no claimed canonical nonfalse prime partition.**
   Resolution: the compiler returns an explicit false status; benchmark
   eligibility/censoring must preserve the preregistered rule and record them.

4. **Global residual queries can be unsound without certified outside
   factors.** Resolution: exact_refine requires a partition returned by sound
   extraction; the global-query argument uses nonfalsity and independently
   certified outside factors. An arbitrary heuristic partition must never be
   supplied as though it were a certificate.

5. **A reused encoding is not necessarily a reused solver.** Resolution: the
   new backend holds one PySAT g4 solver across all residual cuts, with complete
   cut assumptions. Clauses and auxiliary equivalences remain permanent. Solver
   counters are read directly. No fresh-versus-persistent speedup is claimed
   without a separate experiment.

6. **Full four-corner equivalence is essential.** One-direction Tseitin
   implications would admit spurious defects. Resolution: all clause,
   conjunction, ITE and formula outputs are equivalences, including empty
   clause/formula cases; validation compares queried cuts directly to finite
   relations rather than to another copy of the same encoder.

7. **Shrinking fixed assignments is not support minimization.** Resolution:
   the SAT session enforces clone equality outside a candidate support while
   allowing the witness context to change. Final supports are tested for
   deletion minimality. The claim is inclusion minimality, not smallest width.

8. **Hyperedges do not imply all-pairs dependence.** Resolution: U and W remain
   separate supports; only singleton/singleton records carry a must-link flag.
   Soft similarity derived from a larger hyperedge must not become a correctness
   constraint. All-equal n=3..8 test cases force higher-order witnesses.

9. **Dynamic baseline and recompilation search have different overheads.**
   Resolution: B2 uses actual manager minimization while custom candidate
   searches explicitly recompile. This favors the established baseline in a
   realistic way and limits conclusions about objective quality apart from
   implementation overhead. All such overhead belongs in total wall time.

10. **Carrier-constrained residual search is potentially stronger than this
    implementation.** Resolution: we first solve semantic primes then apply
    LCC, which is exact but may expend unnecessary work. Claims must name this
    pipeline and cannot assert dominance over all carrier-aware exact solvers.

11. **Oracle-query bounds are not runtime theorems.** Resolution: the stated
    bounds count queries only. The global CNF still contains all input variables;
    no parameterized time guarantee for this implementation follows merely
    from small direct blocks or narrow returned supports.

12. **Actual backends do not make tiny synthetic inputs industrial evidence.**
    Resolution: reserve industrial-performance claims for sufficiently large,
    representative held-out inputs and meaningful paired total-runtime gains.
    Tool availability establishes an implementation gate only.

## Independent audit of principal benchmark integration

The backend author separately reviewed the root agent's `code/benchmark.py`
(SHA256 `b377a3a8def9ddbcf426a5a5549313546160ff4faf55a8b57cde5ccdaad1d2b0`)
and frozen `BENCHMARK_PROTOCOL.md` before principal results. This is independent
of the benchmark implementation, though it is not an external review of the
backend author's own work.

**SDD/knowledge-compilation role:** no integration correctness blocker found.
Native B2 invokes actual SDD minimization, and custom methods use the reported
explicit rotations/child swaps and charge full recompilation. Actual
root-reachable element/node counts are used. The custom neighborhood budget is
modest and sorted deterministically; a failure cannot establish impossibility
for factor-exposure search in general. The size baseline's internal search
budget differs from custom recompilation budgets and remains a stated
comparison limitation.

**SAT/Boolean-decomposition role:** no integration correctness or semantic
leakage blocker found. Non-oracle worker payloads do not contain truth
partitions; their objectives never call the exhaustive baseline. All exposed
nonsingleton blocks enter the exact residual solver. Evaluation-only prime
counts are attached after the worker returns. M4/M5 retain raw U/W witnesses,
although the soft penalty uses their union. Such a union penalty is a heuristic
preference, not a theorem asserting all those variables belong together.

The worker's algorithm clock starts after imports/input parsing and ends after
exact residual and carrier assembly. This matches the registered definition.
The 15-second process watchdog also includes startup/imports, so the effective
algorithm-time limit is slightly smaller and environment-dependent; record the
separate process wall time and any censoring. No material consequence can be
assumed until failure counts are inspected.

Required follow-through: the principal worker records structural move deltas
and compilation/extraction costs but deliberately omits measured residual SAT
cost for each candidate. `code/move_diagnostics.py` supplies this separately
after all primary runs, with independent exact agreement checks, a per-work
item watchdog, complete mapping back to every source move, and explicit reuse
of one measured residual result per unique instance/partition. The resulting
timings are exploratory and cannot be fed back into frozen objectives or
presented as independent per-occurrence timing replicates.

Review recommendation before results: permit the frozen pilot to run after the
PASS backend gate; retain all listed limitations and require the registered
held-out stopping rule. Neither these finite tests nor the integration audit
supports an industrial-runtime or novelty claim by itself.

## Final outcome review

**Disposition: accept decision D for the reported bounded pilot; no unresolved
SDD/SAT correctness blocker identified.** The completed principal campaign has
2,100 trials, no timeouts/errors, and agreement with independent semantic and
simultaneous partitions. M5/B3 has held-out paired geometric runtime ratio
2.211513, with M5 slower on all 30 held-out instances. The registered runtime
and practical residual-work gates fail. These findings support an algorithmic
NO-GO for this implementation and campaign, not a universal impossibility
claim about defect/exposure objectives or native SDD search.

The final master/results/statistics/next-gate reports preserve that distinction.
They explicitly retain the recompilation cost, weak graph baseline, fixed
neighbor-prefix bias, small structurally repetitive families, and absence of
industrial-scale evidence. They do not recast factor counts, query counts,
or an oracle-aligned control as a runtime improvement. The separate surviving
mathematical note is correctly labelled a working note without publication-ready
novelty; omitting a new paper draft is consistent with that priority outcome.

The required post-primary move diagnostics are complete: 1,020 unique moves
map back to all 10,440 original move occurrences. The 174 distinct
instance/partition residual measurements have zero errors, timeouts, or
semantic/simultaneous disagreements. Timings are reused explicitly across
occurrences, with full mapping, and are not independent repeated timing
measurements. The separate diagnostic provides the previously missing actual
parent/candidate SAT costs without contaminating the frozen heuristic.

One illustrative observed tradeoff is `repeated_module_heldout_n6`: a candidate
increases SDD elements from 17 to 18, exposes two direct blocks instead of one,
and reduces residual calls from 7 to 5. Its single cached SAT-wall observation
is approximately 0.092 ms lower. This is an exact structural/count observation
and a tiny exploratory timing difference; it neither proves a relation between
globally optimal objectives nor rescues the failed end-to-end gate. Most
explored moves have unchanged exposure; the full negative distribution must
remain alongside this example.

The training-only solver-reuse diagnostic uses an archived Phase 4 controlled
encoding shared byte-for-byte by its persistent and fresh-solver arms, while
its third arm rebuilds the Phase 3 cut-specific encoding. This isolates a
useful implementation question more cleanly than attributing encoding-size
differences to persistence. It uses real counters and independent cut checks,
and never measures or infers a learned-clause count. Any advantage in this
fixed-cut training workload must stay separate from the held-out vtree-method
NO-GO; it cannot establish a carrier/defect-search benefit.

The public documentation examples are appropriately labelled smoke controls.
They do not meet the separate future requirement for a meaningful licensed
public industrial corpus. A future native-objective experiment needs new
preregistration and structurally distinct held-out data; none is authorized
merely by this review. No additional algorithm work is required to accept the
current negative result and complete its reproducibility archive.
