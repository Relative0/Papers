# Prompt: CM Computation and Benchmarking Research Thread

I want you to continue a rigorous research program based on Brian Droncheff's Correspondence Matrices (CMs), with the immediate goal of testing whether CM-specific operator normalization/folding can produce practical computational advantages in compressed Boolean computation.

## Files and working location

My local research folder is:

`C:\Users\brian\Documents\CM Quantum`

It contains (or I will place there) the original CM paper, the two generated research papers, the handoff notes, and all experiment CSV/JSON files. If you have local filesystem access, inspect that folder first. If you do not, tell me and work from files I upload; do not pretend to have accessed the path.

Also inspect the current public CM project and its evidence boundaries:

- https://relative0.github.io/Correspondence_Matrices/
- https://github.com/Relative0/Correspondence_Matrices

Preserve that project's discipline around correctness gating, artifact-equivalent comparisons, negative results, reproducibility, and avoiding cherry-picking.

## Core mathematical substrate

Use the original paper's CM ordering and terminology. XOR is the paper's `m`; ordinary Boolean coefficient multiplication is AND; quotient is `A \ B = A AND NOT B`.

The pure-Boolean phase branch defines a distinct cyclic-convolution product `star` on the four CM basis coefficients:

`E_r star E_s = E_(r+s mod 4)`

extended by XOR-linearity. This gives

`A_phase = F2[C4] ~= F2[u]/(u^4)`.

Do not confuse `star` with ordinary 2x2 matrix multiplication, pointwise Boolean operations, or the later signed/cyclotomic quantum lift.

A key exact CM-to-ANF rule for a two-input operator `Theta` is:

`P_(X Theta Y) = a XOR b P_X XOR c P_Y XOR d(P_X P_Y)`

with

`a = Theta_22`

`b = Theta_12 XOR Theta_22`

`c = Theta_21 XOR Theta_22`

`d = Theta_11 XOR Theta_12 XOR Theta_21 XOR Theta_22`.

Thus odd-feature/unit CMs are exactly the nonlinear two-input Boolean operators with a quadratic `XY` term; even-feature/nilpotent CMs are affine.

The original CM paper also has a composition theorem: when logical subexpressions share ordered operands, operations between them can be performed at the CM/operator level before operand evaluation. Rotations/transposes can sometimes align operands first. Quotienting and containment give additional structural simplifications.

## Research question

Test this hypothesis rather than assuming it:

**CM operator normalization can reduce the cost of compressed ANF/Boolean propagation by eliminating nonlinear polynomial operations before operand expansion.**

The goal is not merely to show that ANF can be computed without a truth table; Boolean Mobius transforms, Reed-Muller/FDD approaches, ZDDs and other symbolic methods already do that. The goal is to determine whether the CM operator layer creates a measurable advantage on appropriate workloads compared with strong artifact-equivalent baselines.

## Required work

First read the supplied papers/handoff and inspect existing code/results. Then research current literature and implementations before designing the benchmark. In particular compare against strong relevant methods rather than strawmen: direct sparse ANF propagation, fast truth-table Mobius transform, PolyBoRi/ZDD or equivalent ZDD Boolean polynomial manipulation, ROBDD/CUDD where artifact/query contracts are comparable, FDD/KFDD/Reed-Muller decision diagrams if practical, structural CSE/e-graph-like factoring, XOR-AND graphs/XAG optimization, and current Boolean-factorization or reversible/quantum-oracle synthesis work.

Implement a CM symbolic frontend/optimizer with at least these stages:

1. parse/retain a Boolean expression DAG with ordered operands and provenance;
2. normalize CM operand orientation with the original rotation/transpose relations where valid;
3. fold same-operand CMs before expanding subexpressions;
4. apply CM quotient/containment simplifications only when formally justified;
5. label each surviving CM node as affine or nonlinear from its feature parity;
6. propagate to a compressed ANF backend, preferably with a ZDD/FDD-style or otherwise canonical sparse representation in addition to a simple reference implementation;
7. preserve exact equivalence checks against an independent Boolean evaluator.

Build tests from small exhaustive cases upward. For every rewrite, maintain a checkable certificate or at minimum a deterministic equivalence test. Re-run decisive results rather than trusting old CSVs.

## Benchmark design

Pre-register the benchmark matrix and success criteria before looking at final timings. Include both favorable and unfavorable workload families. Good candidate axes include:

- semantic support/live_k;
- repeated same-operand operator structure;
- percentage of affine versus nonlinear CM nodes;
- shared-subgraph fraction;
- ANF sparsity and degree;
- edit locality/version reuse;
- repeated restrictions/partial assignments;
- factorization depth;
- random dense functions as an expected bad case.

Use real corpora where feasible, particularly existing CM project hardware/configuration corpora and public Boolean/reversible-circuit benchmarks. Keep synthetic mechanism tests separate from domain evidence.

Measure at least:

- correctness/equivalence;
- cold build time;
- warm/reuse time;
- peak memory/RSS where trustworthy;
- peak symbolic node count;
- peak explicit monomial count;
- number of polynomial multiplications avoided/performed;
- AND/multiplicative complexity of the resulting Boolean network;
- depth/AND-depth;
- serialization size/reload if relevant;
- for reversible/quantum-oracle compilation only when contracts are comparable: Toffoli/T count, depth and ancilla use.

Never convert a negative result into a positive narrative. A useful outcome may be a clear characterization of when CM folding helps and when it should abstain.

## Deliverables

Create a subfolder such as:

`C:\Users\brian\Documents\CM Quantum\Computation_and_Benchmarks`

if local access is available; otherwise return a downloadable ZIP with the same structure.

Maintain:

- `README.md` — reproducible run instructions;
- `RESEARCH_LOG.md` — dated decisions and findings;
- `BENCHMARK_PROTOCOL.md` — frozen workloads, metrics and success criteria;
- `RESULTS.md` — results with exact scope and limitations;
- source code and tests;
- raw CSV/JSON outputs;
- a machine-readable manifest with hashes/seeds/environment versions;
- a `NEGATIVE_RESULTS.md` section/file for failed approaches.

Do not edit or overwrite the original papers. Treat this as a new experimental branch.

At the end, answer these questions explicitly:

1. Does CM folding reduce symbolic work beyond a well-implemented generic structural optimizer?
2. Which structural properties predict benefit?
3. Does it reduce multiplicative/AND complexity, not just Python runtime?
4. Can the advantage survive against ZDD/FDD/XAG/BDD baselines on natural workloads?
5. If not, is CM still useful as a certificate/provenance layer or specialized compiler frontend?
6. What is the next falsifiable experiment?
