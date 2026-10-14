# Incremental-Control Four-Corner SAT Comparator

**Phase 4 — 29 September 2026**

## 1. Objective

Phase 3 rebuilt a fresh four-corner SAT instance for every candidate carrier-compatible cut. Phase 4 builds **one fixed CNF** and makes the cut itself a set of solver assumptions.

This is deliberately a comparator, not a novelty claim: incremental SAT for Boolean bi-decomposition is established prior art. The project-specific content is the combination of carrier-block selectors with the CM four-corner rank defect.

---

## 2. One selector per carrier block

Let

\[
\Pi_K=\{B_1,\dots,B_k\}
\]

be the carrier prime partition. Introduce one Boolean selector \(s_j\) for each block \(B_j\):

- \(s_j=1\): the block is on the \(A\) side of the queried cut;
- \(s_j=0\): the block is on the \(B\) side.

Every variable inside one carrier block uses the same selector, so carrier compatibility is enforced by construction rather than by extra per-query clauses.

For each original variable \(x_v\), create two assignment copies

\[
x_v^{(0)},\qquad x_v^{(1)}.
\]

The pure corners need no multiplexing:

\[
F_{00}:x_v\mapsto x_v^{(0)},
\qquad
F_{11}:x_v\mapsto x_v^{(1)}.
\]

For the mixed corners introduce

\[
z_v^{01}=\operatorname{ITE}(s_{B(v)},x_v^{(0)},x_v^{(1)}),
\]

\[
z_v^{10}=\operatorname{ITE}(s_{B(v)},x_v^{(1)},x_v^{(0)}).
\]

Thus one semantic four-copy circuit works for *every* carrier-block cut.

---

## 3. Defect condition

As before, the base encoding asserts

\[
P=F_{00}\wedge F_{11},
\qquad
Q=F_{01}\wedge F_{10},
\]

and

\[
P\mathbin{\Updownarrow}Q=1.
\]

For a requested cut, only selector assumptions change.

### Theorem 3.1 — assumption equivalence

Fix any nontrivial union \(A\) of carrier blocks and set the selector assumptions accordingly. The controlled base CNF is satisfiable under those assumptions iff the Phase-3 independently constructed four-corner defect CNF for cut \(A\mid\bar A\) is satisfiable.

### Proof

Under the assumptions, every mixed-corner multiplexer simplifies to exactly the clone used by the independent encoding:

- variables in \(A\) take row index \(i\);
- variables in \(\bar A\) take column index \(j\).

The four semantic outputs and final XOR/AND defect therefore compute the same Boolean formula as the independent construction. Auxiliary Tseitin variables are definitional, so satisfiability is preserved in both directions. ∎

Consequently:

- SAT gives a concrete rank-two CM minor witness;
- UNSAT certifies rank at most one and exact AND-separability across that cut.

---

## 4. Why this is genuinely incremental

The clause database is fixed across all candidate cuts. In an assumption-capable CDCL/IPASIR solver, a query consists only of literals

\[
\{s_j\text{ or }\neg s_j:1\le j\le k\}.
\]

Learned clauses derived from the permanent base formula remain available across queries; assumptions are temporary decisions. This is the standard setting in which incremental SAT can amortize related decomposability tests.

`code/incremental_four_corner.py` includes:

- the fixed control-variable encoder;
- assumption generation;
- witness decoding;
- exact recursive factor recovery using the shared base encoding;
- an optional `PySATSession` adapter for a real assumption-capable CDCL backend;
- export of a base DIMACS file plus JSON assumption stream.

The execution environment used for this phase did **not** contain `python-sat`, CaDiCaL, Kissat, MiniSat, or another industrial incremental solver. Therefore the validation backend reuses the fixed base formula but restarts the bundled DPLL search. **No learned-clause speedup is claimed from the present timing environment.**

---

## 5. Correctness validation

`code/validate_incremental.py` generated 120 random carrier/CNF instances and checked **516 carrier-compatible cuts**.

For every cut it compared:

1. the controlled base encoding under selector assumptions;
2. a freshly built Phase-3 independent-cut SAT encoding;
3. direct exhaustive CM rank-one computation.

It also compared complete recursive factor recovery from the controlled encoding against the independent Phase-3 recovery.

Result:

\[
\boxed{0\text{ discrepancies in }516\text{ cut queries}.}
\]

The exact records are in `data/incremental_validation.json`.

---

## 6. Encoding-amortization experiment

A separate deterministic size experiment used \(k=2,\dots,8\) carrier blocks with two variables per block and compared:

- emitting a fresh independent CNF for every unordered block cut;
- emitting the controlled base CNF once.

| carrier blocks \(k\) | cuts | controlled clauses | clauses emitted by independent rebuilds | rebuild/base ratio |
|---:|---:|---:|---:|---:|
| 2 | 1 | 284 | 252 | 0.89 |
| 3 | 3 | 420 | 1,116 | 2.66 |
| 4 | 7 | 556 | 3,444 | 6.19 |
| 5 | 15 | 692 | 9,180 | 13.27 |
| 6 | 31 | 828 | 22,692 | 27.41 |
| 7 | 63 | 964 | 53,676 | 55.68 |
| 8 | 127 | 1,100 | 123,444 | 112.22 |

This is an **encoding-reuse** result, not a solver-runtime result. With one query the selector/multiplexer overhead can make the controlled base larger; its benefit appears when many related cuts are queried.

Raw data: `data/incremental_amortization_sizes.json`.

---

## 7. Best role in the combined research program

The incremental SAT engine should now be treated as the exact semantic oracle used only where direct structure cannot decide the factorization:

- SDD/compiled route: resolve vtree-exposed factors directly, SAT-test unresolved crossing cuts;
- CM/LM read-once route: no SAT needed inside the theorem class; SAT becomes the fallback once repeated support/sharing is introduced;
- general carrier/CNF route: use the same controlled base as the practical exact comparator against the Phase-3 bounded-width QBF theorem.

This gives one common correctness oracle across all three branches.
