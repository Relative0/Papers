# SAT-Based Four-Corner CM Factorization Algorithm

## 1. Goal

Given a CNF/circuit \(f\) and a fixed carrier-compatible cut \(A\mid B\), decide whether

\[
f(a,b)=g(a)\wedge h(b)
\]

without materializing the exponentially large correspondence flattening.

The CM theorem gives

\[
f=g\wedge h
\iff
\operatorname{rank}_{\mathbb F_2}[f]_{A\mid B}\le 1.
\]

The test therefore searches directly for a nonzero `2 x 2` minor.

## 2. Defect formula

Create two input copies per original variable. For a variable in `A`, corner `(i,j)` uses copy `i`; for a variable in `B`, it uses copy `j`. Compute the four outputs

\[
y_{00},y_{01},y_{10},y_{11}.
\]

Then constrain

\[
(y_{00}\wedge y_{11})\mathbin{\Updownarrow}(y_{01}\wedge y_{10})=1.
\]

- **SAT** gives a rank-defect certificate and proves the cut is not separable.
- **UNSAT** proves every `2 x 2` minor vanishes, hence rank at most one and exact AND-separability.

For a CNF, the implementation treats each clause as an OR gate and the formula as an AND gate and applies a Tseitin encoding. Only the two input copies are shared; internal gates are copied per corner.

## 3. Size

For `n` input variables and a circuit/CNF of size `s`, the encoding uses

- `2n` assignment-input variables;
- four copies of the semantic internal computation;
- a constant-size top defect gadget.

Thus the encoding size is `O(n+s)` with a modest constant factor, not `O(2^n)`.

## 4. Carrier-aware refinement baseline

The provided program also contains a recursive factor recovery baseline. Given the already-computed carrier blocks \(B_1,\ldots,B_k\), it enumerates only cuts that are unions of those blocks. When it finds an UNSAT defect cut, it recursively factors the two sides. Any sequence of valid splits eventually reaches the unique finest semantic grouping of the supplied carrier blocks.

Worst-case SAT calls remain exponential in `k`; this is deliberate. The baseline provides an exact practical comparator for the bounded-width/QBF route and directly quantifies how much the carrier prunes the search space:

\[
2^{n-1}-1 \quad\longrightarrow\quad 2^{k-1}-1
\]

possible unordered nontrivial cuts before recursive pruning.

## 5. Priority boundary

SAT- and QBF-based Boolean bi-decomposition are established logic-synthesis techniques, including AND bi-decomposition. Accordingly, the SAT use itself is **not claimed novel**. The present implementation is useful because it puts the project's CM rank condition into a transparent four-corner certificate, integrates carrier-block restrictions, exports ordinary DIMACS, and supplies exact witnesses that can be checked back against the original function.

The strongest future implementation step is **incremental SAT**: retain the four semantic circuit copies while changing only cut-control assumptions, allowing learned clauses to survive across related carrier-compatible cuts. That requires an industrial incremental SAT API; the bundled pure-Python DPLL is intentionally only a reproducibility validator.
