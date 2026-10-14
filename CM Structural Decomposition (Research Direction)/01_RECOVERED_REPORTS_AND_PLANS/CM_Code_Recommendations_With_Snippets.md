# Recommendations for Optimizing and Benchmarking Correspondence Matrices (CMs)

This document contains **actionable to-do’s, detailed code snippets, and reasoning** for improving the CM implementation, benchmarking methodology, and fair comparison to state-of-the-art Boolean computation methods.

---

## 1. Core Engineering Optimizations for CM Code

### 1.1 Broadcasting & Alignment
- ✅ Already implemented in `cm_build_lazy.py` with **broadcast-only alignment** and **single materialization**【24†cm_build_lazy.py】.
- 🔧 **To-do**: Ensure all `.repeat()` calls are replaced with `np.broadcast_to` where possible.

**Snippet Example** (in `cm_build_lazy.py` final expansion):

```python
# Replace manual repeats with broadcast
expand_shape = tuple(2 for _ in target_vars)
arr = np.broadcast_to(arr, expand_shape)  # zero-copy where possible
```

### 1.2 Cached Permutations
- ✅ Already cached row/col permutation indices in `cm_normalize.py`【26†cm_normalize.py】.
- 🔧 **To-do**: Extend caching to cover **bit-masks for fixed-variable selections**.

### 1.3 In-place Boolean Ops
- 🔧 **To-do**: Modify `combine_pointwise` in `cm_normalize.py` to use in-place bitwise ops.

**Snippet Example**:

```python
def combine_pointwise(M1, M2, op: str):
    a = M1.astype(bool, copy=False)
    b = M2.astype(bool, copy=False)
    if op == "AND": np.bitwise_and(a, b, out=a)
    elif op == "OR": np.bitwise_or(a, b, out=a)
    elif op == "XOR": np.bitwise_xor(a, b, out=a)
    elif op == "IMP": np.bitwise_or(np.bitwise_not(a), b, out=a)
    elif op == "EQV": np.bitwise_not(np.bitwise_xor(a, b), out=a)
    else: raise ValueError(op)
    return a
```

### 1.4 Packed Bits for Large Arrays
- 🔧 **To-do**: Use `np.packbits` to reduce memory 8× when storing large truth tables.

### 1.5 Parallelism
- 🔧 **To-do**: Integrate `numexpr` or `dask` for multicore logical ops.

---

## 2. Heuristics to Maximize CM Advantages

### 2.1 Pair-Node Tokens for Constant-Time Operator Algebra
Introduce **4-bit CM tokens** for operators and a `PairNode` IR to collapse aligned binary nodes.

**Snippet Example (`cm_token.py`):**

```python
TOK = { "AND": 0x8, "OR": 0xE, "XOR": 0x6, "IMP": 0xD, "EQV": 0x9 }
MASK = 0xF

def cm_not(t): return (~t) & MASK
def cm_transpose(t): return ((t & 0b1101) | ((t & 0b0010)<<1) | ((t & 0b0100)>>1))

def cm_compose(t1, t2, op):
    if op == "AND": return t1 & t2
    if op == "OR": return t1 | t2
    if op == "XOR": return t1 ^ t2
    if op == "IMP": return (~t1) | t2
    if op == "EQV": return ~(t1 ^ t2) & MASK
    raise ValueError(op)
```

**Snippet Example (`cm_pair.py`):**

```python
@dataclass(frozen=True)
class PairNode:
    xl: str; xr: str; tok: int

def compose_pair(p1, p2, op: str):
    if p1.xl == p2.xl and p1.xr == p2.xr:
        return PairNode(p1.xl, p1.xr, cm_compose(p1.tok, p2.tok, op))
    return None
```

This ensures `(X Θ₁ Y) Φ (X Θ₂ Y)` collapses in O(1) time.

### 2.2 Operand-Alignment Heuristic
- 🔧 **To-do**: Add a pass that reorders operands consistently (via transpose/rotation).

### 2.3 NOT-Pushing as Token Complement
- 🔧 **To-do**: Replace array-level DeMorgan with `cm_not(token)` for pair-nodes.

### 2.4 Memoization
- 🔧 **To-do**: Wrap `cm_compose` in `@lru_cache` for reuse across deep trees.

---

## 3. Benchmarking Against Other Algorithms

### 3.1 CNF + CDCL SAT Solvers
Use `tseitin_cnf`【25†cm_exprlib.py】 to generate CNF, then feed into PySAT or pycryptosat.

**Snippet Example (PySAT):**

```python
from pysat.solvers import Glucose4
from cm_exprlib import miter_equiv

def sat_equiv(expr1, expr2, n):
    nvars, clauses = miter_equiv(expr1, expr2, n)
    with Glucose4(bootstrap_with=clauses) as S:
        return not S.solve()  # UNSAT => equivalent
```

**Snippet Example (pycryptosat with XOR):**

```python
import pycryptosat
solver = pycryptosat.Solver()
for cl in clauses: solver.add_clause(cl)
solver.add_xor([1,2,3], True)
sat, model = solver.solve()
```

### 3.2 BDD Baseline
Use `dd.autoref` or `dd.cudd` for serious performance comparisons.

```python
from dd import autoref
mgr = autoref.BDD(); mgr.declare(*[f"x{i}" for i in range(n)])
```

### 3.3 Spectral / ANF
Apply Fast Walsh–Hadamard Transform to compute ANF.

```python
def fwht(a):
    h=1
    while h<len(a):
        for i in range(0,len(a),h*2):
            x,y=a[i:i+h],a[i+h:i+2*h]
            a[i:i+h]=(x+y)%2; a[i+h:i+2*h]=x
        h*=2
    return a
```

### 3.4 SymPy Simplification
Already implemented via `simplify_via_sympy`【27†expr_simplify.py】.

---

## 4. Benchmark Harness Enhancements

### 4.1 Independence from Globals
Fix `cm_bench.py` so functions don’t rely on `args` globals【22†cm_bench.py】.

### 4.2 Pair Collapse Metrics
Add `pair_collapses` and `pairable_ratio` fields to benchmark reports.

### 4.3 Report Extensions
Add side-by-side columns for CM, SAT, BDD, SymPy, Espresso, ANF runtimes.

---

## 5. Summary Checklist

- [ ] Replace repeats with `np.broadcast_to`.  
- [ ] Cache bit-masks for fixed-variable selections.  
- [ ] Add `cm_token.py` and `cm_pair.py` (operator tokens + pair-nodes).  
- [ ] Add pair-reduction pass in compiler.  
- [ ] Push NOTs as token complements.  
- [ ] Use `@lru_cache` for operator composition.  
- [ ] Add SAT backends (PySAT, pycryptosat).  
- [ ] Add BDD baseline (autoref + cudd).  
- [ ] Add ANF/FWHT transform backend.  
- [ ] Extend HTML report with pair metrics + multiple backends.  

---

## Closing Note

These changes implement the **operator-level O(1) algebra** promised by CMs, optimize large-matrix handling, and establish **fair, apples-to-apples benchmarks** against CNF-SAT, BDDs, ANF, and symbolic algebra systems.
