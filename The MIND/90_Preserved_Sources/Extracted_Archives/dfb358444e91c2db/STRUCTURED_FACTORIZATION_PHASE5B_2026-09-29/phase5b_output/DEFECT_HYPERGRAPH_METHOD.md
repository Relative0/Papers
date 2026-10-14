# Defect supports as soft structural evidence

`probe_defects` probes fixed candidate cuts using the same real persistent SAT
backend as exact refinement. An UNSAT cut is a separability certificate. A SAT
cut yields clone assignments x0,x1 and supports U on one side and W on the
other. The stored object is `(U,W)`, not just their unlabelled union and not a
clique of asserted pairwise dependencies.

The reproduced support lemma proves only that some semantic prime factor
intersects both U and W. It does not prove that all variables in either support
belong together. The code emits `singleton_must_link` only when both supports
are singletons. Larger supports may bias a vtree objective softly; they may
never be used to impose exact variable merging or prune possible factor cuts.
Even a certified singleton pair is merely optional search evidence: final
correctness still comes from SDD certificates and exact residual SAT.

Each variable has a permanent gated equality

    e_v -> (x_v^0 == x_v^1).

For one current witness of support D, setting e_v for every coordinate outside
D ensures a future witness uses only D. The deletion test for v adds e_v as
an assumption. On SAT, the decoded smaller support replaces D. On UNSAT, v
is retained. Repeating for the initial coordinates yields an inclusion-minimal
support. Assignments and contexts may change after each SAT query; merely
editing a previous assignment would not implement this search.

If the initial support width is d, at most d deletion queries follow the
initial witness query. The proof is elementary: every coordinate is considered
at most once; each successful test permanently tightens the equality set;
an earlier UNSAT deletion remains UNSAT under further equality constraints.
Thus every remaining coordinate is necessary relative to the final permitted
support. This is not minimum-cardinality support, a bound on d, a pairwise
localization theorem, or a runtime bound independent of SAT difficulty.

For each failed deletion the implementation records the equality assumptions
appearing in the solver's UNSAT core. These cores also depend on the complete
cut-selector assumptions and the permanent defect formula; the stored subset
is diagnostic only. No minimal-core claim, pairwise inference, group-testing
speedup, or additional use of cores in the objective is made. Deterministic
coordinate deletion was chosen to keep the query accounting and evidence
sound and reproducible.

The all-equal relation with models `0^n` and `1^n` is implemented as a CNF
equating every variable with x1. For n=3 through 8, the real backend confirms
that balanced-cut shrinking retains all n coordinates. No singleton pair is
emitted. Additional seeded random cases verify the four decoded truth values,
support crossing of an independently computed semantic prime, and deletion
minimality with fresh equality assumptions. Raw witnesses and counters are in
`data/hybrid_validation.json`.

The real-backend run completed 46 witness checks and 80 fresh support-deletion
minimality queries with zero discrepancies, including all six all-equal
instances n=3..8. These are finite implementation checks, not an extension of
the infinite-family proof by experiment.

Defect extraction incurs encoding, SAT probing, shrinking, and support
processing costs. The benchmark must charge all of them to M4/M5 even when
the resulting hyperedges do not change the selected vtree. A reduction in
residual work alone does not establish a total-runtime improvement.
