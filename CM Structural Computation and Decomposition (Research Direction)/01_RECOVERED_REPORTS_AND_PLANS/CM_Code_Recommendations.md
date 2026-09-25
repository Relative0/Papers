# Recommendations for Optimizing and Benchmarking Correspondence Matrices (CMs)

This document summarizes **actionable to-do’s, code-level suggestions, and reasoning** for improving the CM implementation, benchmarking methodology, and fair comparison to other state-of-the-art Boolean computation methods.

---

## 1. Core Engineering Optimizations for CM Code

### 1.1 Broadcasting & Alignment (Implemented in `cm_build_lazy.py`)
- ✅ Already avoids unnecessary array repetition by using **broadcasted singleton axes**【24†cm_build_lazy.py】.
- 🔧 **To-do**: Ensure all downstream calls (e.g., in `cm_normalize.py`) maintain lazy expansion until final materialization. Double-check any `.repeat()` calls and replace with `np.broadcast_to` where possible.

### 1.2 Cached Permutations for Normalization
- ✅ Implemented with `@lru_cache` in `cm_normalize.py`【26†cm_normalize.py】.
- 🔧 **To-do**: Extend caching to cover not just permutations but also **bit-masks for variable fixing** (often repeated across runs).

### 1.3 Memory Layout & Data Types
- 🔧 **To-do**: Switch boolean storage to `np.uint8` or `np.packbits` when working with very large CMs (beyond 2^20 states). This will cut memory usage by ~8x.
- 🔧 **To-do**: Profile reshaping in `compile_expr_to_cm_lazy`. Consider using **NumPy views** rather than `.copy()` where safe.

### 1.4 Parallelism
- 🔧 **To-do**: Use `numexpr` or `dask.array` to distribute elementwise logical ops across cores. Especially relevant for `combine_pointwise` in `cm_normalize.py`【26†cm_normalize.py】.

---

## 2. Heuristics for Maximizing CM Advantages

### 2.1 Early Simplification
- ✅ Sympy simplifier already available in `expr_simplify.py`【27†expr_simplify.py】.
- 🔧 **To-do**: Integrate this into the random-expression benchmark loop (`cm_bench.py`) so both raw and simplified forms are tested. This will highlight how CMs benefit from reduced structure.

### 2.2 Structural Factorization
- 🔧 **To-do**: Implement a “factor detection” routine that checks whether an expression decomposes into independent sub-blocks of variables. These can be evaluated as smaller CMs and tensor-combined.

### 2.3 Quotienting & Composition
- Your paper highlights **quotienting and operator composition via CMs**【28†CorrespondenceMatrices.pdf】.
- 🔧 **To-do**: Add benchmark modes that stress-test these unique CM features, since standard solvers (SAT/CDCL) cannot exploit them directly.

---

## 3. Benchmarking Against Other Algorithms

### 3.1 Direct Truth-Table Expansion (Baseline)
- ✅ Already in `cm_exprlib.py` as `eval_expr_tt`【25†cm_exprlib.py】.
- 🔧 **To-do**: Use this as the “ground-truth” baseline for correctness checks.

### 3.2 Tseitin CNF + CDCL SAT Solver
- ✅ Encoding implemented in `tseitin_cnf`【25†cm_exprlib.py】.
- 🔧 **To-do**: Pipe CNF output into modern solvers:
  ```python
  import pycosat  # or subprocess to call Kissat/CaDiCaL
  sat = pycosat.solve(clauses)
  ```
- 🔧 **Benchmark Plan**: Compare CM evaluation vs. SAT solving time for equivalence checking and satisfiability.

### 3.3 BDDs (Binary Decision Diagrams)
- 🔧 **To-do**: Use `dd` (CUDD Python wrapper) or `buddy` to build reduced ordered BDDs for the same random formulas.
- 🔧 This allows an apples-to-apples comparison with a symbolic representation method.

### 3.4 Sympy Simplification / Canonical Forms
- ✅ Already prototyped (`simplify_via_sympy`, `bdd_sop`)【27†expr_simplify.py】.
- 🔧 **To-do**: Add runtime benchmarking for SymPy’s simplifier vs. CM computation.

### 3.5 Hybrid Approach
- 🔧 **To-do**: Test mixed pipelines:
  1. Simplify expression via SymPy.
  2. Encode into CNF → SAT solver.
  3. Encode into CM for equivalence check.
- Compare timings across all hybrid routes.

---

## 4. Benchmark Harness Enhancements

### 4.1 Randomized Workloads
- ✅ Already generating random expressions in `cm_exprlib.py::random_expr`【25†cm_exprlib.py】.
- 🔧 **To-do**: Add control over:
  - Clause density (like k-SAT benchmarks).
  - Operator distribution (bias toward AND/OR vs. XOR/IMP).

### 4.2 Reproducibility
- 🔧 **To-do**: Store seed + generated expressions in logs so runs are repeatable.

### 4.3 Multiple Backends
- 🔧 **To-do**: Extend `bench_sweep.html` reports to show *side-by-side comparisons* of:
  - CM runtime
  - Truth table runtime
  - SAT solver runtime
  - BDD runtime
  - SymPy simplifier runtime

---

## 5. Summary of To-Do’s

- [ ] Replace `.repeat()` with `np.broadcast_to` where possible.  
- [ ] Cache bit-masks for fixed-variable selections.  
- [ ] Explore `np.packbits` for memory savings.  
- [ ] Add `numexpr`/`dask` for multicore ops.  
- [ ] Integrate Sympy simplification into benchmarking.  
- [ ] Implement structural factorization heuristics.  
- [ ] Add CM-specific quotienting/composition benchmarks.  
- [ ] Integrate external SAT solvers (pycosat, Kissat).  
- [ ] Benchmark against BDD libraries.  
- [ ] Add reproducibility (seed + logs).  
- [ ] Expand HTML benchmark reports to include all methods.

---

## Closing Note

This roadmap balances **core engineering improvements** with **scientific benchmarking fairness**.  
Implementing even a subset will allow you to convincingly demonstrate where **Correspondence Matrices (CMs)** outperform, complement, or synergize with classical methods.
