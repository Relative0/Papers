# CM vs. Bitset and Other Boolean Computation Methods: Comparative Tables and Interpretation

## Purpose

This document summarizes the practical comparison between **Correspondence Matrices (CMs)** and other Boolean-computation methods tested or discussed in the CM benchmarking work, including **bitset**, **Numba**, **BDD / ROBDD / dd**, **SymPy**, **Espresso**, and several CM variants.

The goal is not merely to rank methods by speed. The important lesson from the experiments is that different methods optimize different things:

- **Bitset** optimizes raw flat execution.
- **BDD / ROBDD** optimizes canonical symbolic decision-graph representation.
- **SymPy** optimizes symbolic manipulation and algebraic simplification.
- **Espresso** optimizes logic minimization.
- **Numba** optimizes compiled evaluator execution.
- **CMs** optimize structure preservation, decomposition, reusable representation, and problem reduction.

The strongest current interpretation is:

> **CM is most beneficial as a structure-preserving compiler / optimizer for Boolean computation. Bitset is the strongest flat execution kernel. The most promising architecture is CM IR / DAG reduction -> bitset execution -> avoid dense CM reinflation -> cache compiled IR when reuse is possible.**

---

# 1. High-Level Method Comparison

This table gives a qualitative comparison of each major method. It is intended to help readers understand why the project eventually moved away from “CM vs. bitset” as a pure speed race and toward “CM for structure, bitset for execution.”

Legend:

- ★★★★★ = excellent
- ★★★★☆ = strong
- ★★★☆☆ = moderate
- ★★☆☆☆ = weak
- ★☆☆☆☆ = poor

| Method | Raw Evaluation Speed | Large Structured Expressions | Reuse of Structure | Partial Evaluation | Canonical Representation | Memory Efficiency | Parallelization Potential | Human Interpretability | Best Use Case |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Bitset** | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★☆☆☆ | ★☆☆☆☆ | ★★★★★ | ★★★★★ | ★☆☆☆☆ | Fast flat truth-table evaluation |
| **Numba** | ★★★★☆ | ★★☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ | Fast compiled evaluator |
| **BDD / ROBDD / dd** | ★★★★☆* | ★★☆☆☆-★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★* | ★★☆☆☆ | ★★★★☆ | Canonical symbolic reasoning |
| **SymPy** | ★★☆☆☆ | ★★☆☆☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★☆☆☆☆ | ★★★★★ | Human-readable symbolic manipulation |
| **Espresso** | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | Logic minimization |
| **Dense CM / NumPy CM** | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | Structured Boolean representation |
| **CM lazy** | ★★☆☆☆-★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | Delayed CM materialization |
| **CM parallel** | ★★☆☆☆-★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | Experimental dense-work acceleration |
| **CM hybrid** | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | CM structure plus bitset execution |
| **CM partial hybrid** | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | Preserving more CM structure during hybrid execution |
| **CM no-reinflate** | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Current best CM execution path without dense CM output |
| **CM + persistent cache** | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | Compile-once / evaluate-many Boolean workflows |

\*BDD performance and memory efficiency can be excellent for favorable variable orderings and structured functions, but can degrade severely under unfavorable orderings or random expressions.

## Interpretation

This table makes the main architectural point clear: **bitset dominates raw execution**, but CM is competitive in a different category. CM is valuable when structure must be preserved, reused, transformed, decomposed, conditioned, or interpreted.

---

# 2. What Each Method Is Really Optimizing

This is one of the most important conceptual tables. It prevents unfair comparisons between methods that are solving different subproblems.

| Method | What It Primarily Optimizes | What It Does Not Primarily Optimize |
|---|---|---|
| **Bitset** | Fast packed execution over many truth assignments | Symbolic structure, decomposition, interpretability |
| **Numba** | Compiled execution of evaluator logic | Reusable symbolic / algebraic representation |
| **BDD / ROBDD / dd** | Canonical decision-graph representation | Robustness to all variable orderings and random-expression blowup |
| **SymPy** | Symbolic algebra and readable manipulation | Low-level packed truth-table execution |
| **Espresso** | Boolean logic minimization | Matrix/operator decomposition or repeated execution |
| **Dense CM** | Structured matrix/operator representation | Raw packed execution speed |
| **CM hybrid** | Structure-preserving reduction plus bitset execution | Eliminating all CM/bitset boundary overhead |
| **CM no-reinflate** | Structure plus execution without final dense CM matrix output | Removing all IR traversal / dispatch cost |
| **CM + persistent cache** | Reusable compiled structure and amortized execution | Being faster than bitset for every one-shot flat evaluation |

## Interpretation

The project’s strongest result is not that CM beats bitset at bitset’s own job. Rather:

> **CM creates reusable structure; bitset executes reduced structure.**

That is a different and more defensible thesis.

---

# 3. Speed Ranking Based on Reported Experimental Results

The approximate ranking below reflects the reported experimental evidence and interpretation from the CM benchmarking work. It is not a universal theorem; it describes the tested regimes and the project’s current best understanding.

| Approximate Rank | Method | Notes |
|---:|---|---|
| 1 | **Bitset** | Strongest one-shot flat execution baseline. |
| 2 | **Cached bitset** | Strongest repeated flat execution baseline. |
| 3 | **CM no-reinflate + persistent cache** | Best current CM-related path; narrows gap to bitset while preserving structure. |
| 4 | **CM no-reinflate** | Avoids dense final CM matrix output; major improvement over ordinary hybrid. |
| 5 | **CM hybrid** | Faster than NumPy-only CM, but still slower than bitset. |
| 6 | **Dense CM / NumPy CM** | Important baseline, but not final architecture. |
| 7 | **Numba** | Useful compiled-control baseline. |
| 8 | **SymPy** | Useful symbolic baseline; often degrades with depth. |
| 9 | **Espresso** | Useful minimization baseline, but not central execution winner. |
| 10 | **BDD worst-case random-expression regimes** | Can be excellent in favorable cases, but random expressions can cause blow-up. |

## Interpretation

BDD deserves a caveat: it can be extremely strong for the right functions and variable orderings. However, the reported project interpretation found BDD highly sensitive to variable count and random-expression structure. CM’s advantage was not universal speed, but relative stability and structure preservation.

---

# 4. Structure Preservation Comparison

This table compares whether a method preserves useful structure after or during computation.

| Method | Preserves Structure? | Type of Structure Preserved | Practical Meaning |
|---|---|---|---|
| **Bitset** | No | Flat packed truth table | Excellent for answers, weak for explanation or reuse. |
| **Numba** | No | Compiled evaluator program | Faster execution, but not a symbolic representation. |
| **BDD / ROBDD** | Yes | Canonical decision graph | Strong symbolic reasoning and equivalence checking. |
| **SymPy** | Yes | Symbolic expression tree | Strong for human-readable algebraic manipulation. |
| **Espresso** | Partially | Minimized Boolean expression / cover | Strong for minimization, less for operator decomposition. |
| **Dense CM** | Yes | Matrix/operator representation | Preserves row/column and operator structure. |
| **CM hybrid** | Yes | CM IR / DAG until reduced execution | Keeps structure while using bitset where appropriate. |
| **CM no-reinflate** | Yes | CM IR / DAG without dense output | Avoids expensive final dense matrix representation. |
| **CM + persistent cache** | Yes | Reusable compiled CMNode / structural hash | Best for repeated or related computations. |

## Interpretation

If a reader only cares about a final truth table, bitset is the obvious choice. If the reader cares about how the Boolean computation is structured, decomposed, reused, or transformed, CM becomes much more interesting.

---

# 5. Reuse Potential

This table asks: what happens if the same expression, structurally equivalent expression, or related expression is evaluated multiple times?

| Method | Reuse Capability | Explanation |
|---|---:|---|
| **Bitset** | Low to moderate | Can cache environments or outputs, but does not preserve higher-level operator structure. |
| **Numba** | Low to moderate | Can reuse compiled evaluator machinery, but not CM-like algebraic structure. |
| **BDD / ROBDD** | Very high | Canonical graph representation supports reuse and equivalence-style reasoning. |
| **SymPy** | High | Symbolic forms can be reused and transformed. |
| **Espresso** | Moderate | Minimized forms can be reused, but this is a different workflow. |
| **Dense CM** | Moderate | Matrix representation can be reused if output form is needed. |
| **CM hybrid** | High | CM structure remains useful before bitset execution. |
| **CM no-reinflate** | High | Avoids dense final output while retaining compiled structure. |
| **CM + persistent cache** | Very high | Structural hash cache and compiled expression reuse are central strengths. |

## Interpretation

This is one of the areas where CM can be beneficial compared with bitset. If the computation is repeated, conditioned, or modified, then the compiled CM structure can become an asset. The reported persistent cache results support this.

---

# 6. Scalability and Failure Modes

Every method has a failure mode. Understanding these is more useful than asking which method is “best” in isolation.

| Method | Main Scaling Risk | Typical Failure Mode |
|---|---|---|
| **Bitset** | Truth-table size | Packed truth table eventually becomes too large. |
| **Numba** | Truth-table size / evaluator complexity | Compiled execution still faces exponential output size. |
| **BDD / ROBDD** | Variable ordering and function structure | Graph blow-up under unfavorable orderings or random expressions. |
| **SymPy** | Expression complexity | Symbolic expression swell and simplification cost. |
| **Espresso** | Cover / SOP complexity | Minimized representation can still become large or expensive. |
| **Dense CM** | Matrix materialization | Dense CM matrices become expensive. |
| **CM parallel** | Not enough large dense work after reduction | Multiprocessing overhead exceeds useful work. |
| **CM hybrid** | Boundary and reinflation overhead | Bitset helps, but result may still be converted back to dense CM-compatible forms. |
| **CM no-reinflate** | IR and execution scaffolding overhead | Avoids dense output, but still pays compilation / dispatch costs. |
| **CM + persistent cache** | IR growth or non-reusable workloads | Best when structure recurs or evaluation repeats. |

## Interpretation

The project’s progress can be summarized as a shift in CM’s failure mode:

```text
Early CM: dense matrix materialization was the bottleneck.
Modern CM: IR compilation and execution scaffolding are the remaining bottlenecks.
```

That is a major architectural improvement.

---

# 7. Numeric Speed Evidence: Hybrid vs. NumPy CM and Bitset

This table shows the reported hybrid comparison. The key point is that hybrid CM improved over NumPy-only CM, but bitset remained faster.

| n | CM_hybrid / NumPy-only CM | CM_hybrid / Bitset | Interpretation |
|---:|---:|---:|---|
| 4 | 0.93x | ~31.3x slower | Hybrid only slightly faster than CM; bitset much faster. |
| 8 | 0.73x | ~20.4x slower | Hybrid materially improves CM. |
| 12 | 0.68x | ~14.8x slower | Hybrid substantially improves CM. |
| 16 | 0.72x | ~8.2x slower | Gap to bitset narrows as size grows. |

## Interpretation

This is the first major turning point. Hybrid did not beat bitset, but it showed that CM could reduce a problem and then use bitset as the execution kernel. That suggests the right architecture is not CM *instead of* bitset, but CM *before* bitset.

---

# 8. Numeric Speed Evidence: Partial Hybrid vs. Full Hybrid

Partial hybrid was tested to see whether preserving more CM structure would improve performance. It did preserve structure, but did not consistently improve runtime.

| n | CM NumPy Time (s) | CM_hybrid Time (s) | CM_partial_hybrid Time (s) | Bitset Time (s) | Partial / CM | Partial / Hybrid | Partial / Bitset |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.000445 | 0.000213 | 0.000214 | 0.000009 | 0.48 | 1.01 | 24.63 |
| 8 | 0.000333 | 0.000213 | 0.000308 | 0.000009 | 0.92 | 1.44 | 33.85 |
| 12 | 0.000342 | 0.000233 | 0.000267 | 0.000012 | 0.78 | 1.14 | 22.23 |
| 16 | 0.000349 | 0.000320 | 0.000307 | 0.000024 | 0.88 | 0.96 | 12.89 |

## Interpretation

Partial hybrid answered an important question: preserving more structure is not automatically faster. Because partial hybrid converted bitset results back into NumPy / CM-compatible parent structures, it introduced extra boundary crossings and parent combine work.

The result is useful even though it is negative:

> **Full hybrid is usually preferable to threshold-only partial hybrid unless a future cost model identifies cases where preserving intermediate CM structure is worth the conversion overhead.**

---

# 9. Numeric Speed Evidence: Boundary Cost Instrumentation

Boundary-cost instrumentation measured whether the CM/bitset conversion boundary was the dominant source of overhead.

## 9.1 Pre-Optimization Boundary Timing

| n | Mode | Total Time (s) | Bitset Eval (s) | Bitset -> Hypercube (s) | Align (s) | Dispatch (s) | Conversions | Elements Converted |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | CM_hybrid | 0.000302 | 0.000035 | 0.000020 | 0.000027 | 0.000004 | 1.0 | 8.0 |
| 4 | CM_partial_hybrid | 0.000280 | 0.000030 | 0.000022 | 0.000019 | 0.000006 | 2.0 | 12.0 |
| 8 | CM_hybrid | 0.000247 | 0.000042 | 0.000014 | 0.000040 | 0.000004 | 1.0 | 16.0 |
| 8 | CM_partial_hybrid | 0.000351 | 0.000031 | 0.000027 | 0.000040 | 0.000006 | 2.0 | 12.0 |
| 12 | CM_hybrid | 0.000269 | 0.000025 | 0.000011 | 0.000064 | 0.000003 | 1.0 | 8.0 |
| 12 | CM_partial_hybrid | 0.000215 | 0.000019 | 0.000026 | 0.000050 | 0.000006 | 2.0 | 8.0 |
| 16 | CM_hybrid | 0.000390 | 0.000045 | 0.000015 | 0.000185 | 0.000004 | 1.0 | 32.0 |
| 16 | CM_partial_hybrid | 0.000448 | 0.000033 | 0.000022 | 0.000024 | 0.000006 | 2.0 | 14.0 |

## 9.2 Post-Optimization Boundary Timing

| n | Mode | Before Total (s) | After Total (s) | Before Boundary (s) | After Boundary (s) | Boundary Reduction |
|---:|---|---:|---:|---:|---:|---:|
| 4 | CM_hybrid | 0.000302 | 0.000160 | 0.000087 | 0.000061 | 1.413x |
| 4 | CM_partial_hybrid | 0.000280 | 0.000174 | 0.000077 | 0.000048 | 1.605x |
| 8 | CM_hybrid | 0.000247 | 0.000205 | 0.000100 | 0.000072 | 1.394x |
| 8 | CM_partial_hybrid | 0.000351 | 0.000263 | 0.000104 | 0.000074 | 1.404x |
| 12 | CM_hybrid | 0.000269 | 0.000137 | 0.000103 | 0.000062 | 1.665x |
| 12 | CM_partial_hybrid | 0.000215 | 0.000162 | 0.000100 | 0.000051 | 1.972x |
| 16 | CM_hybrid | 0.000390 | 0.000393 | 0.000249 | 0.000234 | 1.065x |
| 16 | CM_partial_hybrid | 0.000448 | 0.000437 | 0.000084 | 0.000068 | 1.237x |

## Interpretation

The boundary optimizations helped, but did not solve the whole problem. The key insight was:

> **Boundary overhead is real, but not dominant.**

This led to the next major improvement: avoiding final dense CM reinflation entirely.

---

# 10. Numeric Speed Evidence: No-Reinflation Hybrid

No-reinflation avoids converting the final result back into a dense 2D CM matrix unless that matrix is actually required. This was one of the strongest improvements in the project.

## 10.1 Threshold = 5

| n | CM (s) | CM_hybrid (s) | No-Reinflate (s) | Bitset (s) | No-Reinflate / CM | No-Reinflate / Hybrid | No-Reinflate / Bitset | Final CM Materialized | Repr Code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003578 | 0.0001684 | 0.0001204 | 0.00000930 | 0.3365 | 0.7150 | 12.9463 | 0 | 2 |
| 8 | 0.0004026 | 0.0002254 | 0.0001716 | 0.0000113 | 0.4262 | 0.7613 | 15.1858 | 0 | 2 |
| 12 | 0.0003430 | 0.0001891 | 0.0001271 | 0.0000174 | 0.3706 | 0.6721 | 7.3046 | 0 | 2 |
| 16 | 0.0003229 | 0.0002508 | 0.0000915 | 0.0000381 | 0.2834 | 0.3648 | 2.4016 | 0 | 2 |

## 10.2 Threshold = 7

| n | CM (s) | CM_hybrid (s) | No-Reinflate (s) | Bitset (s) | No-Reinflate / CM | No-Reinflate / Hybrid | No-Reinflate / Bitset | Final CM Materialized | Repr Code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003945 | 0.0001861 | 0.0001355 | 0.0000090 | 0.3435 | 0.7281 | 15.0555 | 0 | 2 |
| 8 | 0.0003766 | 0.0002222 | 0.0001286 | 0.0000094 | 0.3415 | 0.5788 | 13.6809 | 0 | 2 |
| 12 | 0.0002993 | 0.0001702 | 0.0001212 | 0.0000210 | 0.4049 | 0.7121 | 5.7714 | 0 | 2 |
| 16 | 0.0002750 | 0.0002405 | 0.0000963 | 0.0000391 | 0.3502 | 0.4004 | 2.4629 | 0 | 2 |

## 10.3 Threshold = 9

| n | CM (s) | CM_hybrid (s) | No-Reinflate (s) | Bitset (s) | No-Reinflate / CM | No-Reinflate / Hybrid | No-Reinflate / Bitset | Final CM Materialized | Repr Code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003422 | 0.0001625 | 0.0001118 | 0.0000082 | 0.3267 | 0.6880 | 13.6341 | 0 | 2 |
| 8 | 0.0004970 | 0.0002005 | 0.0001789 | 0.0000128 | 0.3600 | 0.8923 | 13.9766 | 0 | 2 |
| 12 | 0.0003236 | 0.0001796 | 0.0001273 | 0.0000284 | 0.3934 | 0.7088 | 4.4824 | 0 | 2 |
| 16 | 0.0002692 | 0.0002300 | 0.0000828 | 0.0000491 | 0.3076 | 0.3600 | 1.6864 | 0 | 2 |

## Interpretation

No-reinflate gives the clearest numeric evidence that representation cost matters. The result was not just faster Boolean computation; it was faster because the system stopped forcing the answer back into a dense CM matrix.

The important diagnostic columns are:

| Field | Meaning |
|---|---|
| `Final CM Materialized = 0` | The final dense CM matrix was not constructed. |
| `Repr Code = 2` | The result was returned as packed bitset output. |

This supports the practical rule:

> **Use dense CM output only when the dense CM matrix itself is needed. Otherwise, use no-reinflate.**

---

# 11. Numeric Speed Evidence: IR Cost Decomposition

After no-reinflation, the next bottleneck was not bitset execution. It was CM IR compilation and execution scaffolding.

| n | Total No-Reinflate Time (s) | IR Compile (s) | Intern (s) | Canonicalize (s) | Rewrite (s) | Live Vars (s) | Other IR (s) | Bitset Eval (s) | Ratio / Bitset |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.000160 | 0.000107 | 0.000019 | 0.000006 | 0.000024 | 0.000011 | 0.000045 | 0.000037 | 18.44 |
| 8 | 0.000168 | 0.000120 | 0.000023 | 0.000006 | 0.000022 | 0.000017 | 0.000051 | 0.000032 | 16.27 |
| 12 | 0.000303 | 0.000212 | 0.000040 | 0.000009 | 0.000039 | 0.000032 | 0.000089 | 0.000067 | 7.88 |
| 16 | 0.000195 | 0.000113 | 0.000024 | 0.000006 | 0.000015 | 0.000014 | 0.000053 | 0.000065 | 3.71 |

## Interpretation

This table is crucial because it shows that bitset execution inside CM was not the dominant remaining cost. At several sizes, IR compilation was larger than bitset execution.

That supports the central architecture:

> **CM should be treated like a compiler. Compilation cost should be reused or cached.**

---

# 12. Numeric Speed Evidence: Compiled IR Reuse

Compiled-IR reuse removed the IR compilation cost from repeated evaluations.

| n | No-Reinflate Total (s) | IR Compile (s) | Bitset Eval (s) | Ratio / Bitset | IR Cache Hit |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000070 | 0.000000 | 0.000042 | 7.57 | 1 |
| 8 | 0.000055 | 0.000000 | 0.000035 | 5.24 | 1 |
| 12 | 0.000075 | 0.000000 | 0.000057 | 2.71 | 1 |
| 16 | 0.000108 | 0.000000 | 0.000076 | 1.62 | 1 |

## Interpretation

This table is one of the strongest pieces of evidence in favor of CM. It shows that once CM compilation is reused, CM+bitset moves much closer to bitset.

The remaining gap is likely not “CM computation” in the old dense sense, but execution scaffolding:

- dispatch,
- result wrapping,
- variable-order handling,
- DAG traversal,
- fixed-variable handling,
- bitset invocation overhead.

---

# 13. Numeric Speed Evidence: Persistent Cache

Persistent structural-hash caching made CM reusable across equivalent expression objects.

## 13.1 End-to-End No-Reinflate Persistent Cache

| n | Baseline No-Reinflate (s) | Persistent Cache No-Reinflate (s) | Speedup |
|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000098 | 1.51x |
| 8 | 0.000144 | 0.000080 | 1.80x |
| 12 | 0.000203 | 0.000110 | 1.84x |
| 16 | 0.000219 | 0.000116 | 1.89x |

## 13.2 Cached Execution vs. Cached Bitset

| n | Baseline No-Reinflate (s) | Cached CM Exec / Eval (s) | Bitset (s) | Cached Bitset / Eval (s) | Cached CM / Cached Bitset |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000024 | 0.000010 | 0.000003 | 8.12 |
| 8 | 0.000144 | 0.000027 | 0.000010 | 0.000005 | 5.54 |
| 12 | 0.000203 | 0.000047 | 0.000031 | 0.000009 | 4.90 |
| 16 | 0.000219 | 0.000066 | 0.000053 | 0.000027 | 2.42 |

## Interpretation

This is probably the most important performance table for explaining why CM remains interesting.

For one-shot flat evaluation, bitset wins. But with persistent cache and repeated evaluation, CM becomes much more competitive while retaining structure.

At `n=16`, cached CM execution was reported as **2.42x** cached bitset. That is still slower, but far closer than the earlier full hybrid result of about **8.2x** slower than bitset.

---

# 14. Numeric Speed Evidence: CM_parallel Stress Results

CM_parallel was tested because CM operations can involve large matrix / tensor-style work. However, optimized CM often removed that dense work before multiprocessing could help.

| n | Chunk Elements | Min Work | CM Time (s) | CM_parallel Time (s) | Ratio |
|---:|---:|---:|---:|---:|---:|
| 12 | 10000 | 50000 | 0.002568 | 0.003273 | 1.275 |
| 12 | 100000 | 250000 | 0.002711 | 0.002766 | 1.020 |
| 16 | 10000 | 50000 | 0.002393 | 0.004706 | 1.966 |
| 16 | 10000 | 1000000 | 0.004280 | 0.003410 | 0.797 |
| 16 | 10000 | 10000 | 0.003142 | 0.002948 | 0.938 |

## Interpretation

CM_parallel sometimes helped, but not consistently. The larger finding was that activation was often zero in optimized grids because structural reduction left too little dense work.

This is an important negative result:

> **Parallel CM is not currently a strong selling point. Structural reduction made the dense parallel workload too small or too intermittent.**

Future parallel work should focus on data-layout-aligned work units such as flattened buffers, post-lift matrix blocks, or large contiguous slices.

---

# 15. Recommendation Table: Which Method Should Be Used?

| Goal | Recommended Method | Why |
|---|---|---|
| Fastest one-shot flat Boolean evaluation | **Bitset** | Strongest raw execution kernel. |
| Fast repeated flat evaluation | **Cached bitset** | Minimal execution overhead. |
| Structure-preserving computation | **CM IR / DAG** | Preserves decomposition, row/column structure, and operator semantics. |
| Compile-once / evaluate-many with structure | **CM no-reinflate + persistent cache** | Amortizes compilation while preserving CM structure. |
| Symbolic equivalence / canonical decision reasoning | **BDD / ROBDD** | Canonical graph representation when variable ordering is favorable. |
| Human-readable symbolic manipulation | **SymPy** | Best suited for algebraic readability and symbolic transformations. |
| Logic minimization | **Espresso** | Designed for minimization workflows. |
| Dense CM matrix required as output | **Dense CM or hybrid with reinflation** | Necessary when the actual CM matrix is the required product. |
| Partial evaluation / conditioning workflows | **CM + cached IR** | CM structure can be reused under related variable settings. |
| Future research architecture | **CM IR -> bitset execution -> no-reinflate -> persistent cache** | Best-supported architecture from the experiments. |

---

# 16. Where CMs May Be Beneficial

CMs are most beneficial when the computation is not just “evaluate this Boolean expression once.”

## 16.1 Repeated and related computations

If a Boolean expression or structurally similar expression will be evaluated repeatedly, CM’s compiled IR can be reused. Persistent caching and compile-once / evaluate-many were among the strongest results.

## 16.2 Structured expressions

CMs can exploit repeated subtrees, common subexpressions, and algebraic simplifications before execution.

## 16.3 Partial evaluation and conditioning

CMs are promising when variables are fixed, conditioned, or queried under multiple scenarios. The representation can preserve structure across related evaluations.

## 16.4 Compositional Boolean workflows

If the system needs to build larger Boolean computations out of smaller parts, CM’s operator / matrix structure is more useful than a flat bit vector.

## 16.5 Interpretability and analysis

CMs provide a representation that can be inspected, decomposed, and related back to the original logical structure. Bitset gives answers quickly but does not preserve much explanatory structure.

## 16.6 Avoiding dense final output

No-reinflation showed that a major cost was forcing results back into dense CM matrices. If the final dense CM matrix is not needed, CM can keep its structural role without paying that output cost.

---

# 17. Where CMs Are Not Beneficial

CMs are not the best choice for every Boolean computation.

| Scenario | Better Choice | Why |
|---|---|---|
| One-shot flat truth-table evaluation | Bitset | CM overhead is not amortized. |
| Very small dense evaluations | Bitset | Bitset has extremely low overhead. |
| Pure symbolic simplification for human algebra | SymPy | SymPy is built for symbolic manipulation. |
| Canonical Boolean equivalence checking | BDD / ROBDD | BDDs provide canonical decision representations under a variable order. |
| Logic minimization | Espresso | Espresso is designed for minimization. |
| Dense output required every time | Depends | CM may be necessary, but dense matrix output is expensive. |
| No structure, no reuse, no conditioning | Bitset | CM’s main strengths are not used. |
| Multiprocessing expected to save small workloads | Bitset or single-process CM | CM_parallel overhead may exceed useful work. |

---

# 18. The Most Important Takeaway Table

| Question | Best Answer from the Experiments |
|---|---|
| Fastest raw evaluator? | **Bitset** |
| Best symbolic canonicalizer? | **BDD / ROBDD**, when variable ordering is favorable |
| Best algebra system? | **SymPy** |
| Best minimizer? | **Espresso** |
| Best structure-preserving representation? | **CM** |
| Best current CM implementation path? | **CM no-reinflate + persistent cache** |
| Best hybrid architecture? | **CM IR -> bitset execution** |
| Biggest CM improvement? | **Symbolic IR + no-reinflate + persistent cache** |
| Most important negative result? | **CM_parallel did not meaningfully help in optimized regimes** |
| Strongest paper thesis? | **CM is a compiler / optimizer, not merely an evaluator** |

---

# 19. Final Interpretation

The CM experiments should not be framed as a failed attempt to beat bitset. They should be framed as a discovery about the proper role of CM.

The strongest interpretation is:

> **Bitset is the right execution kernel. CM is the right structure-preserving optimization layer.**

A skeptical reader may look at the raw speed tables and conclude that bitset wins. That is true for one-shot flat evaluation. But the broader tables show why CM still matters:

- CM preserves structure.
- CM supports decomposition.
- CM reduces live-variable subproblems.
- CM enables reuse through compiled IR and structural hashing.
- CM can avoid dense output through no-reinflation.
- CM becomes much more competitive when compile cost is amortized.
- CM provides a representation that bitset does not.

The most defensible final architecture is therefore:

```text
Expression
  -> CM IR / DAG compiler
  -> structural reduction, pruning, reuse
  -> bitset execution of reduced subproblem
  -> no dense CM reinflation unless needed
  -> persistent compiled-IR cache for repeated or related evaluations
```

That is where CMs may be beneficial: not as a replacement for bitset, but as the structure-preserving layer that makes bitset execution more meaningful, reusable, and compositional.
