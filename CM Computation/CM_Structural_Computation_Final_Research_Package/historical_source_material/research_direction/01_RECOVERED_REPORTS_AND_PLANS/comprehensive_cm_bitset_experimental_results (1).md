# Comprehensive CM + Bitset Experimental Results

**Purpose.** This document summarizes the computational experiments and architectural findings from the CM benchmarking work to date. It is intended as a standalone reference for writing, future paper planning, and deciding what additional experiments may be worth running.

**Core thesis that emerged:** CM is strongest as a **structure-preserving compiler / optimizer** for Boolean computation, while bitset is the strongest **flat execution kernel**. The best architecture found so far is:

> **CM IR / DAG for structure reduction -> bitset for execution -> avoid dense CM reinflation -> cache compiled IR when reuse is possible.**

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Overall Architecture and Benchmark Context](#overall-architecture-and-benchmark-context)
3. [Phase 0: Early Baselines and Conceptual Framing](#phase-0-early-baselines-and-conceptual-framing)
4. [Phase 1: Bitset and Numba Backends](#phase-1-bitset-and-numba-backends)
5. [Phase 2: Balanced Layout, Symbolic IR, and Hybrid Execution](#phase-2-balanced-layout-symbolic-ir-and-hybrid-execution)
6. [Phase 3: CM_parallel Validation and Stress Testing](#phase-3-cm_parallel-validation-and-stress-testing)
7. [Phase 4: Partial / Mixed Hybrid Execution](#phase-4-partial--mixed-hybrid-execution)
8. [Phase 5: CM-Bitset Boundary Cost Instrumentation](#phase-5-cm-bitset-boundary-cost-instrumentation)
9. [Phase 6: No-Reinflation Hybrid](#phase-6-no-reinflation-hybrid)
10. [Phase 7: IR Cost Decomposition and Reuse](#phase-7-ir-cost-decomposition-and-reuse)
11. [Phase 8: Persistent IR Cache and Reusable Compiled Expressions](#phase-8-persistent-ir-cache-and-reusable-compiled-expressions)
12. [What Worked vs. What Did Not](#what-worked-vs-what-did-not)
13. [Current Best Interpretation](#current-best-interpretation)
14. [Future Paper Ideas and Open Questions](#future-paper-ideas-and-open-questions)
15. [Appendix: Key Benchmark Tables](#appendix-key-benchmark-tables)

---

## Executive Summary

The project began as a benchmark comparison of **Correspondence Matrix (CM)** methods against other Boolean computation approaches, including bitset, Numba, BDD/ROBDD, SymPy, Espresso, and related baselines. The core correctness reference throughout was `eval_expr_tt(...)`, with correctness checks intended to stay outside timed windows for benchmark fairness. Source: cm_handoff_notes.md.

The strongest final result is not that dense CM beats bitset as a raw evaluator. Instead, the evidence supports a more interesting architectural result:

> **CM is an effective structural compiler / reducer. Bitset is the best execution kernel. Dense CM materialization is often unnecessary and expensive. Persistent IR caching converts CM into an amortizable compile-time artifact.**

The major empirical steps were:

- **Bitset was validated as a very strong flat execution baseline.** It uses packed Python integer bitmasks, full-mask semantics, and ordering checks against `eval_expr_tt(...)`.
- **Balanced layout and symbolic IR were major CM improvements.** Balanced layout reduced unnecessary ambient padding, and symbolic CM IR reduced live-variable subproblems substantially. In the handoff notes, balanced layout was reported as often giving roughly **1.3x-1.8x** improvement, and symbolic IR reduced live vars to around **3-5** with materializations around **7-11**.
- **Full hybrid materially improved CM**, often collapsing reduced subproblems into a single bitset materialization, but still remained slower than pure bitset in the flat benchmark setting.
- **CM_parallel was tested carefully and mostly ruled out as a high-value path.** The flat element-block scheduler worked technically, but optimized CM rarely produced large enough dense work for process-based parallelism to help. Stress testing found activation rate 0 under the main grid, and forced activation produced only intermittent, limited benefit.
- **Partial hybrid preserved more structure but did not improve runtime.** It avoided root collapse and used child/subnode bitset evaluation, but did not consistently beat full hybrid.
- **Boundary overhead was real but not dominant.** Instrumentation showed bitset conversion/alignment costs were meaningful and could be reduced, but they did not explain the full gap to bitset.
- **No-reinflation was a major win.** Avoiding dense 2D CM output and returning packed bitset or a 1D truth-table vector materially improved hybrid runtime; `final_cm_materialization_performed=0` and representation code `2` confirmed that dense CM reinflation was avoided.
- **IR compilation became the dominant remaining cost.** IR timing showed `hybrid_no_reinflate` was dominated by `ir_compile_time_s`, not bitset execution. Reuse/caching narrowed the gap to bitset substantially.
- **Persistent structural-hash caching and reusable compiled expressions made CM+bitset near-optimal in the intended compile-once/evaluate-many setting.** Persistent cache gave **1.51x-1.89x** end-to-end speedups for no-reinflate; cached execution at `n=16` was **2.42x** slower than cached bitset, much closer than earlier hybrid results.

---

## Overall Architecture and Benchmark Context

### Original benchmark task

The benchmark task was to generate Boolean expressions and evaluate them using multiple backends:

- CM
- CM lazy
- CM parallel
- CM hybrid
- bitset
- Numba
- BDD / ROBDD / `dd`
- SymPy
- Espresso
- BDD->SOP baseline

The reference correctness function was:

```python
eval_expr_tt(...)
```

Correctness was repeatedly treated as an external validation step, not as part of the timed execution window, to preserve fair comparisons.

### Conceptual distinction

A key conceptual distinction emerged:

| Method | Best interpretation |
|---|---|
| Bitset | Hardware-efficient packed flat evaluator; uses bitwise operations over many assignments at once |
| CM | Structured / algebraic / operator representation; supports decomposition, tensor composition, reuse, and structural optimization |

### Final architecture

The architecture that emerged is:

```text
Expr AST
  -> CM IR compiler / canonicalizing reducer
  -> CMNode / structured DAG
  -> hybrid_no_reinflate execution
  -> packed bitset or TT vector output
  -> optional persistent IR cache / reusable compiled expression
```

Final public-style API after the persistent cache work:

```python
compiled = compile_expr(expr, use_persistent_cache=True)
result = evaluate_compiled(compiled, mode="hybrid_no_reinflate", vars_all=[...])
```

---

## Phase 0: Early Baselines and Conceptual Framing

### Purpose / hypothesis

The initial aim was to compare raw CM evaluation against classical and symbolic Boolean computation baselines, including BDD, SymPy, and later bitset/Numba. The early working hypothesis was that CM might be unusually stable as variable count and depth increased.

### Observations

Early benchmark interpretation found:

- CM was **not universally fastest**.
- BDD could be fastest at very small sizes.
- BDD showed severe blow-up on random expressions.
- SymPy degraded with expression depth.
- CM appeared relatively stable and often gained ground as variable count or depth increased.

The right claim became:

> CM is not necessarily fastest overall; CM is unusually stable across increasing variable count and depth, especially on random/unstructured expressions.

### Verdict

The early result was a reframing:

> CM should not be pitched simply as the fastest evaluator. Its value is structural stability and compositional representation.

---

## Phase 1: Bitset and Numba Backends

### Purpose / hypothesis

Bitset and Numba were added to create stronger baselines. Bitset was expected to be especially difficult for CM to beat because it uses compact packed Boolean computation.

### Implementation summary

The bitset backend added:

- `build_bitset_env(vars)`
- `eval_expr_bitset(expr, env)`
- `bitset_to_bool_array(bits, n_vars)`

The bitset design used Python integer bitmasks, full-mask semantics for complement-producing operations, truth-table ordering aligned with `eval_expr_tt(...)`, and pure bitwise execution.

The Numba backend used a flattened postorder / stack-program style evaluator with `@njit`, primitive arrays, and separate compile/execution timing.

### Observations

Bitset quickly became the strongest flat execution baseline. Later validation added explicit mask semantics, environment caching, cache stats helpers, and ordering checks.

### Verdict

> Bitset is the strongest flat dense subproblem execution kernel. CM must either exploit structure that bitset does not see, or use bitset as its execution layer.

---

## Phase 2: Balanced Layout, Symbolic IR, and Hybrid Execution

### Purpose / hypothesis

The goal was to reduce unnecessary dense work in CM by improving representation before execution.

### Implementation summary

Important improvements included:

- Balanced CM layout instead of legacy padded square layout
- Shared symbolic CM IR / DAG
- Subtree memoization / structural reuse
- Canonical subtree hashing / CSE-style reuse
- Pruning / algebraic simplification
- Hybrid materialization with bitset fast path

The handoff notes state that balanced layout reduced unnecessary work and often gave roughly **1.3x-1.8x** improvement in cited examples. Symbolic IR reduced live variables to around **3-5** and materializations to around **7-11**, making CM behave like a structure optimizer.

### Hybrid benchmark results

A reported compare run used:

- `--sizes 4,8,12,16`
- `--trials 3`
- `--max-depth 4`
- `--cm-layout balanced`
- `--cm-compare-hybrid`
- `--cm-hybrid-threshold 7`
- `--cm-parallel`

Reported CM_hybrid vs NumPy-only CM:

| n | CM_hybrid / NumPy-only CM |
|---:|---:|
| 4 | 0.93x |
| 8 | 0.73x |
| 12 | 0.68x |
| 16 | 0.72x |

Reported CM_hybrid vs bitset:

| n | CM_hybrid / bitset |
|---:|---:|
| 4 | ~31.3x slower |
| 8 | ~20.4x slower |
| 12 | ~14.8x slower |
| 16 | ~8.2x slower |

Diagnostics showed median **1 bitset materialization** and **0 NumPy materializations** for CM_hybrid, implying the threshold often collapsed a reduced subproblem directly into one bitset evaluation.

### Verdict

Hybrid materially improved CM but still did not beat bitset in flat one-shot evaluation.

The critical interpretation became:

> Once CM reduces a problem to a small live-variable subproblem, bitset is the optimal execution kernel. CM's value is as structure optimizer, not primarily as final evaluator.

---

## Phase 3: CM_parallel Validation and Stress Testing

### Purpose / hypothesis

Earlier CM_parallel chunking was thought to be misaligned with the actual expensive data layout. The flat element-block redesign tried to parallelize contiguous flattened work rather than tiny leading-axis chunks.

### Validation grid

The validation grid used:

- `--sizes 8,12,16`
- `--max-depth 4`
- `--trials 10`
- `--cm-layout balanced`
- `--cm-parallel`
- `--cm-parallel-workers 4`
- `--cm-parallel-chunk-elems` in `{10000, 100000, 1000000}`
- `--cm-parallel-min-work-elems` in `{50000, 250000, 1000000}`
- `--cm-hybrid-threshold` in `{0,3}`

### Main validation results

In the validation grid:

- Activation rate was **0.000** for all `n=8,12,16`.
- `parallel_pool_starts` stayed at 0.
- Fallbacks were dominated by `small_total_work`.
- `live_vars_max` stayed small; max observed was 9.

The report concluded that CM_parallel behaved like CM plus scheduling checks, because no actual parallel combines activated.

### Stress test

A stress test tried to force large dense work:

- `--sizes 12,16,18`
- `--max-depth 6`
- `--cm-layout legacy_square`
- `--cm-hybrid-threshold 0`
- attempts to disable reductions were limited because no CLI flags existed for disabling memoization/pruning/canonical rewrites.

Stress-grid results:

- Activation rate: **0.000** (`activated_trials=0/135`)
- Fallback reason: `small_total_work` dominated
- Observed `live_vars_max`: **15**, implying up to about `2^15 = 32768` elements
- With `min_work >= 50000`, this was still below the activation gate

When min work was lowered to 10000:

- Activation occurred in **2/10** trials.
- Example chunk sizes: `10000,6384`.
- At `n=16`, the forced activation run gave `cm_time=0.003142`, `cm_parallel_time=0.002948`, ratio `0.938`; a small win, but intermittent.

### Representative stress table

| n | chunk_elems | min_work | cm_time | cm_parallel_time | ratio |
|---:|---:|---:|---:|---:|---:|
| 12 | 10000 | 50000 | 0.002568 | 0.003273 | 1.275 |
| 12 | 100000 | 250000 | 0.002711 | 0.002766 | 1.020 |
| 16 | 10000 | 50000 | 0.002393 | 0.004706 | 1.966 |
| 16 | 10000 | 1000000 | 0.004280 | 0.003410 | 0.797 |
| 16 | 10000 | 10000 | 0.003142 | 0.002948 | 0.938 |

### Verdict

> CM_parallel activates but provides limited benefit.

The deeper conclusion:

> Optimized CM removes most of the large dense work that process-based parallelism would accelerate. The issue is not just implementation; the workload is usually too small or too reduced for multiprocessing to help.

---

## Phase 4: Partial / Mixed Hybrid Execution

### Purpose / hypothesis

The hypothesis was that full hybrid might collapse too much structure too early. Partial hybrid was designed to preserve CM structure at the root while allowing child/subnode bitset evaluation.

### Implementation summary

`materialize_mode="partial_hybrid"`:

- never collapses the root into bitset
- allows child/subnode recursion to bitset-collapse when `k <= hybrid_threshold`
- converts bitset materializations back to NumPy hypercubes aligned to the parent's live vars
- adds diagnostics for bitset-vs-NumPy decisions, cache hits, root-forced behavior, and fixed-var threshold crossings

### Threshold 7 benchmark results

| n | cm (numpy) | cm_hybrid | cm_partial_hybrid | bitset | partial/cm | partial/hybrid | partial/bitset |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.000445 | 0.000213 | 0.000214 | 0.000009 | 0.48 | 1.01 | 24.63 |
| 8 | 0.000333 | 0.000213 | 0.000308 | 0.000009 | 0.92 | 1.44 | 33.85 |
| 12 | 0.000342 | 0.000233 | 0.000267 | 0.000012 | 0.78 | 1.14 | 22.23 |
| 16 | 0.000349 | 0.000320 | 0.000307 | 0.000024 | 0.88 | 0.96 | 12.89 |

Diagnostics:

- Hybrid: `bitset_materializations=1`, `numpy_materializations=0`, `full_collapse_occurred=1`
- Partial hybrid: approximately `bitset_materializations≈2`, `numpy_materializations≈1`, `full_collapse_occurred=0`, `decision_numpy_root_forced=1`

Partial hybrid preserved structure but did not consistently beat full hybrid.

### Verdict

> Partial hybrid does not improve on full hybrid.

Important nuance:

> Partial hybrid was not a failed implementation; it answered the question. A threshold-only policy with immediate conversion back to NumPy/CM-compatible arrays adds boundary crossings and parent combine work without enough saved computation.

---

## Phase 5: CM-Bitset Boundary Cost Instrumentation

### Purpose / hypothesis

After partial hybrid, the next question was whether CM/bitset boundary conversion was the dominant overhead: bitset eval, bitset-to-hypercube conversion, axis alignment, dispatch, and associated allocation.

### Instrumentation

Boundary timing fields added:

- `boundary_bitset_eval_time_s`
- `boundary_bitset_to_hypercube_time_s`
- `boundary_align_time_s`
- `boundary_dispatch_time_s`

Count/size fields added:

- `boundary_bitset_eval_calls`
- `boundary_bitset_to_hypercube_calls`
- `boundary_elements_converted`
- `boundary_align_calls`
- `boundary_align_transpose_calls`
- `boundary_align_insert_axes_total`
- `boundary_bitset_const_fastpath_calls`

### Pre-optimization measurements

| n | mode | total_time_s | bitset_eval_s | to_hypercube_s | align_s | dispatch_s | conversions | elements_converted |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | cm_hybrid | 0.000302 | 0.000035 | 0.000020 | 0.000027 | 0.000004 | 1.0 | 8.0 |
| 4 | cm_partial_hybrid | 0.000280 | 0.000030 | 0.000022 | 0.000019 | 0.000006 | 2.0 | 12.0 |
| 8 | cm_hybrid | 0.000247 | 0.000042 | 0.000014 | 0.000040 | 0.000004 | 1.0 | 16.0 |
| 8 | cm_partial_hybrid | 0.000351 | 0.000031 | 0.000027 | 0.000040 | 0.000006 | 2.0 | 12.0 |
| 12 | cm_hybrid | 0.000269 | 0.000025 | 0.000011 | 0.000064 | 0.000003 | 1.0 | 8.0 |
| 12 | cm_partial_hybrid | 0.000215 | 0.000019 | 0.000026 | 0.000050 | 0.000006 | 2.0 | 8.0 |
| 16 | cm_hybrid | 0.000390 | 0.000045 | 0.000015 | 0.000185 | 0.000004 | 1.0 | 32.0 |
| 16 | cm_partial_hybrid | 0.000448 | 0.000033 | 0.000022 | 0.000024 | 0.000006 | 2.0 | 14.0 |

The report found that bitset core time was **not** dominant; boundary alignment was often comparable to or larger than bitset eval+conversion, especially for `cm_hybrid` at `n=16`. It also found partial hybrid increased boundary crossings.

### Optimizations implemented

Two minimal optimizations:

1. **Alignment fast-path:** `align_to_vars(...)` / `align_to_vars_with_stats(...)` use a single `reshape` to insert multiple singleton axes when no transpose is needed and the input is C-contiguous.
2. **Avoid redundant uint8 copy:** `bitset_to_bool_array(...)` no longer calls `.astype(np.uint8)` on the result of `np.unpackbits(...)`.

Tests passed: `python -m pytest -q -> 30 passed`.

### Post-optimization results

| n | mode | before_total_s | after_total_s | before_boundary_s | after_boundary_s | boundary_reduction |
|---:|---|---:|---:|---:|---:|---:|
| 4 | cm_hybrid | 0.000302 | 0.000160 | 0.000087 | 0.000061 | 1.413 |
| 4 | cm_partial_hybrid | 0.000280 | 0.000174 | 0.000077 | 0.000048 | 1.605 |
| 8 | cm_hybrid | 0.000247 | 0.000205 | 0.000100 | 0.000072 | 1.394 |
| 8 | cm_partial_hybrid | 0.000351 | 0.000263 | 0.000104 | 0.000074 | 1.404 |
| 12 | cm_hybrid | 0.000269 | 0.000137 | 0.000103 | 0.000062 | 1.665 |
| 12 | cm_partial_hybrid | 0.000215 | 0.000162 | 0.000100 | 0.000051 | 1.972 |
| 16 | cm_hybrid | 0.000390 | 0.000393 | 0.000249 | 0.000234 | 1.065 |
| 16 | cm_partial_hybrid | 0.000448 | 0.000437 | 0.000084 | 0.000068 | 1.237 |

### Verdict

> Boundary overhead is real but not the dominant bottleneck.

Even after reducing boundary costs, hybrid remained slower than pure bitset, with significant time remaining in non-boundary NumPy/IR materialization scaffolding and the final CM materialization copy.

---

## Phase 6: No-Reinflation Hybrid

### Purpose / hypothesis

The boundary report suggested a deeper problem: even when bitset solved the reduced root cheaply, the result was forced back into a dense CM matrix. The no-reinflation hypothesis was:

> The remaining cost is not mostly computation, but re-expansion into the CM matrix representation.

### Implementation summary

`materialize_hybrid_no_reinflate(...)` was added. It returns:

- representation code `2`: packed bitset (`int`) in MSB-first variable order
- representation code `1`: 1D truth-table vector

It avoids dense 2D CM matrix construction. If `live_k <= hybrid_threshold`, it evaluates directly to packed bitset; otherwise it falls back to `materialize_ir(... materialize_mode="hybrid")` and produces a 1D truth-table vector, never a 2D dense CM matrix.

Diagnostics include:

- `final_cm_materialization_performed`
- `final_cm_materialization_time_s`
- `final_truth_table_materialization_time_s`
- `final_bitset_returned`
- `final_output_elements`
- `final_output_representation_code`

### Benchmark results

#### Threshold = 5

| n | cm | cm_hybrid | no_reinflate | bitset | no_reinflate/cm | no_reinflate/hybrid | no_reinflate/bitset | final CM materialized | repr code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003578 | 0.0001684 | 0.0001204 | 0.00000930 | 0.3365 | 0.7150 | 12.9463 | 0 | 2 |
| 8 | 0.0004026 | 0.0002254 | 0.0001716 | 0.0000113 | 0.4262 | 0.7613 | 15.1858 | 0 | 2 |
| 12 | 0.0003430 | 0.0001891 | 0.0001271 | 0.0000174 | 0.3706 | 0.6721 | 7.3046 | 0 | 2 |
| 16 | 0.0003229 | 0.0002508 | 0.0000915 | 0.0000381 | 0.2834 | 0.3648 | 2.4016 | 0 | 2 |

#### Threshold = 7

| n | cm | cm_hybrid | no_reinflate | bitset | no_reinflate/cm | no_reinflate/hybrid | no_reinflate/bitset | final CM materialized | repr code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003945 | 0.0001861 | 0.0001355 | 0.0000090 | 0.3435 | 0.7281 | 15.0555 | 0 | 2 |
| 8 | 0.0003766 | 0.0002222 | 0.0001286 | 0.0000094 | 0.3415 | 0.5788 | 13.6809 | 0 | 2 |
| 12 | 0.0002993 | 0.0001702 | 0.0001212 | 0.0000210 | 0.4049 | 0.7121 | 5.7714 | 0 | 2 |
| 16 | 0.0002750 | 0.0002405 | 0.0000963 | 0.0000391 | 0.3502 | 0.4004 | 2.4629 | 0 | 2 |

#### Threshold = 9

| n | cm | cm_hybrid | no_reinflate | bitset | no_reinflate/cm | no_reinflate/hybrid | no_reinflate/bitset | final CM materialized | repr code |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003422 | 0.0001625 | 0.0001118 | 0.0000082 | 0.3267 | 0.6880 | 13.6341 | 0 | 2 |
| 8 | 0.0004970 | 0.0002005 | 0.0001789 | 0.0000128 | 0.3600 | 0.8923 | 13.9766 | 0 | 2 |
| 12 | 0.0003236 | 0.0001796 | 0.0001273 | 0.0000284 | 0.3934 | 0.7088 | 4.4824 | 0 | 2 |
| 16 | 0.0002692 | 0.0002300 | 0.0000828 | 0.0000491 | 0.3076 | 0.3600 | 1.6864 | 0 | 2 |

### Observations

No-reinflate was consistently faster than baseline CM and usually faster than current hybrid. Improvements versus hybrid were roughly **1.1x to 2.7x**, and the gap to bitset narrowed but did not disappear. Diagnostics confirmed `final_cm_materialization_performed_median = 0` and representation code `2`, meaning dense CM output was avoided and packed bitset was returned.

### Verdict

> Avoiding reinflation helps, but substantial non-reinflation overhead remains.

This was one of the most important positive discoveries. It showed that dense CM output was a major representation cost and that CM should not always be forced to return a dense matrix.

---

## Phase 7: IR Cost Decomposition and Reuse

### Purpose / hypothesis

After no-reinflation, the remaining gap appeared to come from IR compilation and scaffolding. This phase decomposed `hybrid_no_reinflate` into IR build vs bitset execution.

### Instrumentation

IR timing fields included:

- `ir_compile_time_s`
- `ir_intern_time_s`
- `ir_canonicalize_time_s`
- `ir_rewrite_time_s`
- `ir_live_vars_time_s`
- `ir_other_time_s`

No-reinflate execution timing included:

- `nr_bitset_eval_time_s`
- `nr_fallback_materialize_ir_time_s`
- `nr_tt_vector_build_time_s`

### Pre-optimization measurements

| n | total_s | ir_compile | intern | canon | rewrite | live_vars | other | bitset_eval | ratio/bitset |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.000160 | 0.000107 | 0.000019 | 0.000006 | 0.000024 | 0.000011 | 0.000045 | 0.000037 | 18.44 |
| 8 | 0.000168 | 0.000120 | 0.000023 | 0.000006 | 0.000022 | 0.000017 | 0.000051 | 0.000032 | 16.27 |
| 12 | 0.000303 | 0.000212 | 0.000040 | 0.000009 | 0.000039 | 0.000032 | 0.000089 | 0.000067 | 7.88 |
| 16 | 0.000195 | 0.000113 | 0.000024 | 0.000006 | 0.000015 | 0.000014 | 0.000053 | 0.000065 | 3.71 |

Interpretation: `hybrid_no_reinflate` was dominated by IR compilation/build, not packed-bitset execution.

### Reuse/caching results

Compare-mode wall time:

| n | baseline_sum_s | compile_once_sum_s | speedup_compile_once | cache_sum_s | speedup_cache |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000950 | 0.000627 | 1.52x | 0.000724 | 1.31x |
| 8 | 0.001011 | 0.000627 | 1.61x | 0.000710 | 1.42x |
| 12 | 0.001704 | 0.000881 | 1.93x | 0.000852 | 2.00x |
| 16 | 0.001537 | 0.001161 | 1.32x | 0.001278 | 1.20x |

Hybrid no-reinflate with and without compiled-IR reuse:

| n | no_reinflate_total_s | ir_compile | bitset_eval | ratio/bitset | ir_cache_hit |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000160 | 0.000107 | 0.000037 | 18.44 | 0 |
| 8 | 0.000168 | 0.000120 | 0.000032 | 16.27 | 0 |
| 12 | 0.000303 | 0.000212 | 0.000067 | 7.88 | 0 |
| 16 | 0.000195 | 0.000113 | 0.000065 | 3.71 | 0 |

With `--cm-reuse-compiled-ir`:

| n | no_reinflate_total_s | ir_compile | bitset_eval | ratio/bitset | ir_cache_hit |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000070 | 0.000000 | 0.000042 | 7.57 | 1 |
| 8 | 0.000055 | 0.000000 | 0.000035 | 5.24 | 1 |
| 12 | 0.000075 | 0.000000 | 0.000057 | 2.71 | 1 |
| 16 | 0.000108 | 0.000000 | 0.000076 | 1.62 | 1 |

### Verdict

> IR compilation dominates `hybrid_no_reinflate`, and explicit reuse/caching meaningfully reduces redundant work and narrows the gap to bitset, while not fully eliminating it.

This phase established that CM should be treated as a compile-time optimizer whose cost should be amortized.

---

## Phase 8: Persistent IR Cache and Reusable Compiled Expressions

### Purpose / hypothesis

The previous phase showed that IR compilation dominated `hybrid_no_reinflate`. The next question was whether a persistent structural-hash cache and reusable compiled-expression API could turn CM into a reusable compile artifact.

### Implementation summary

Persistent cache design:

- Key: deterministic structural hash via `expr_structural_hash(expr)`
- Uses `hashlib.blake2b(digest_size=16)`
- Canonicalizes `AND/OR/XOR` by associative flattening and commutative sorting
- Sorts `EQV` children
- Preserves order for `IMP`

Cache value: compiled `CMNode`.

Cache behavior:

- process-level `OrderedDict[str, CMNode]`
- fixed max size
- LRU-ish update with `move_to_end` and `popitem(last=False)`

Diagnostics:

- `ir_persistent_cache_hits`
- `ir_persistent_cache_misses`
- `ir_persistent_cache_size`

Public API:

```python
compiled = compile_expr(expr, use_persistent_cache=True)
result = evaluate_compiled(compiled, mode="hybrid_no_reinflate", vars_all=[...])
```

Benchmark flags:

- `--cm-use-persistent-cache`
- `--cm-eval-repeat N`

### End-to-end persistent cache results

| n | baseline_no_reinflate_s | persistent_cache_no_reinflate_s | speedup |
|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000098 | 1.51x |
| 8 | 0.000144 | 0.000080 | 1.80x |
| 12 | 0.000203 | 0.000110 | 1.84x |
| 16 | 0.000219 | 0.000116 | 1.89x |

### Cached execution vs bitset

Baseline times are compile+execute once. Cached execution is per-eval execution-only using `--cm-eval-repeat 50`.

| n | baseline_no_reinflate_s | cached_exec_s_per_eval | bitset_s | bitset_cached_s_per_eval | cached/bitset_cached |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000024 | 0.000010 | 0.000003 | 8.12 |
| 8 | 0.000144 | 0.000027 | 0.000010 | 0.000005 | 5.54 |
| 12 | 0.000203 | 0.000047 | 0.000031 | 0.000009 | 4.90 |
| 16 | 0.000219 | 0.000066 | 0.000053 | 0.000027 | 2.42 |

### Tests

Coverage added:

- structural hash determinism and commutativity
- persistent cache hit behavior across distinct but equivalent Expr objects
- public `compile_expr` + `evaluate_compiled` correctness vs `eval_expr_tt`
- benchmark integration coverage for `--cm-eval-repeat`

### Verdict

> Persistent caching makes CM+bitset near-optimal.

This is the strongest current result: when CM's compile cost is amortized, and dense CM reinflation is avoided, CM+bitset becomes much closer to bitset performance while retaining the structural CM layer.

---

## What Worked vs. What Did Not

### What worked strongly

| Method / idea | Result |
|---|---|
| Bitset backend | Became strongest flat execution baseline |
| Balanced layout | Reduced unnecessary ambient work; cited ~1.3x-1.8x improvements |
| Symbolic CM IR / DAG | Major structural improvement; cited live vars ~3-5 and materializations ~7-11 |
| Full hybrid CM | Improved over NumPy-only CM; often 1 bitset materialization and 0 NumPy materializations |
| No-reinflation hybrid | Major runtime improvement; faster than CM and usually faster than hybrid |
| IR timing/decomposition | Identified true remaining bottleneck |
| Compiled IR reuse / persistent cache | 1.51x-1.89x end-to-end speedup; cached/bitset_cached ratio down to 2.42 at n=16 |

### What worked technically but did not become the main path

| Method / idea | Result | Why it was not the main path |
|---|---|---|
| CM_parallel flat element blocks | Technically correct; limited benefit | Optimized CM rarely produced enough dense work; activation usually zero or intermittent |
| Partial hybrid | Preserved structure; did not improve runtime | Added extra boundary crossings and NumPy parent combines; did not consistently beat full hybrid |
| Boundary micro-optimizations | Reduced boundary cost | Boundary overhead was real but not dominant; bigger issue was reinflation and IR cost |

### What likely should not be prioritized further for this paper

- More process-based CM_parallel tuning, unless a workload is specifically constructed to preserve large dense CM combines.
- Threshold-only partial hybrid tuning, unless paired with a real cost model.
- Low-level boundary micro-optimizations, unless no-reinflate is not available.
- Claims that CM is the fastest raw flat evaluator.

---

## Current Best Interpretation

The evidence supports the following layered model:

```text
Expression AST
    ↓
CM IR compiler / canonicalizer / reducer
    ↓
Reduced CMNode DAG
    ↓
Bitset execution of reduced form
    ↓
Packed bitset / TT vector result
```

The main conclusion:

> CM is not best framed as a competitor to bitset at raw flat evaluation. It is best framed as a structure-preserving compiler / optimizer that can reduce Boolean problems before handing execution to bitset.

### Important distinctions

1. **If the goal is one-shot flat truth-table evaluation**, pure bitset is usually simplest and fastest.
2. **If the goal includes structure, reuse, partial evaluation, conditioning, compositional workflows, or interpretability**, CM+bitset is valuable.
3. **If the output does not need to be a dense CM matrix**, no-reinflate should be used.
4. **If expressions are reused**, persistent IR caching should be used.

### Current best-performing CM-related path

```python
compiled = compile_expr(expr, use_persistent_cache=True)
result = evaluate_compiled(compiled, mode="hybrid_no_reinflate", vars_all=[...])
```

This path embodies the final discovered architecture:

> **Compile once, reuse many; execute reduced result with bitset; do not reinflate to dense CM unless a CM matrix is actually needed.**

---

## Future Paper Ideas and Open Questions

### Paper idea 1: CM as a structural compiler for Boolean computation

Potential thesis:

> Correspondence Matrices are most effective not as dense evaluators but as a structural optimization layer. When paired with bitset execution and no-reinflation output, CM becomes a reusable compiler for Boolean expressions.

### Paper idea 2: Representation cost vs computation cost

Potential thesis:

> The main overhead in structured Boolean computation may come not from logical evaluation but from representation conversion and output contracts.

### Paper idea 3: Compile-time amortization in structural Boolean evaluators

Potential thesis:

> Once dense output is avoided, IR compilation dominates; caching/reuse transforms CM from a per-call evaluator into an amortized compiler artifact.

### Paper idea 4: Limits of parallelism after structural reduction

Potential thesis:

> Parallel dense execution is less useful when the symbolic optimizer eliminates most dense work.

### Future experiment: n=32 scaling

Not yet run in the reports. This is still a valuable experiment.

Key safety condition:

- Avoid full truth-table allocation
- Avoid dense `(2,)*32` hypercube allocation
- Use `hybrid_no_reinflate`
- Use persistent cache
- Report `live_vars_max`, IR node counts, and whether representation code remains packed bitset

Potential outcome:

- If live vars stay small and no reinflation occurs, the system may scale beyond ordinary dense truth-table feasibility.
- If IR size explodes or a full dense path is triggered, this will identify the scaling boundary.

### Future architecture: packed-cell / block-encoded CM

A promising future direction is to let CM cells store bytes/words/bitsets rather than single Boolean values. This would create a **bit-packed or block-encoded CM**:

- fewer outer axes
- richer per-cell payload
- closer integration of CM structure and bitset execution
- potential reduction in broadcast/permutation/reinflation overhead

This is substantial enough to be a future paper or major architecture revision rather than a small optimization.

### Future optimization: IR execution specialization

Once compile and reinflation are controlled, the remaining cached-execution gap to bitset likely comes from:

- DAG traversal
- node dispatch
- variable alignment logic
- bitset invocation granularity

Potential next steps:

- flatten compiled CM IR into an execution program
- generate direct bitset code
- JIT or specialize evaluator for repeated compiled expressions
- cache reduced/fixed variants for partial evaluation workflows

---

## Appendix: Key Benchmark Tables

### Hybrid vs NumPy-only CM and bitset

Reported CM_hybrid vs NumPy-only CM:

| n | CM_hybrid / NumPy-only CM |
|---:|---:|
| 4 | 0.93x |
| 8 | 0.73x |
| 12 | 0.68x |
| 16 | 0.72x |

Reported CM_hybrid vs bitset:

| n | CM_hybrid / bitset |
|---:|---:|
| 4 | ~31.3x slower |
| 8 | ~20.4x slower |
| 12 | ~14.8x slower |
| 16 | ~8.2x slower |

### Partial hybrid, threshold 7

| n | cm | cm_hybrid | cm_partial_hybrid | bitset | partial/hybrid |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000445 | 0.000213 | 0.000214 | 0.000009 | 1.01 |
| 8 | 0.000333 | 0.000213 | 0.000308 | 0.000009 | 1.44 |
| 12 | 0.000342 | 0.000233 | 0.000267 | 0.000012 | 1.14 |
| 16 | 0.000349 | 0.000320 | 0.000307 | 0.000024 | 0.96 |

### No-reinflate, threshold 7

| n | cm | cm_hybrid | no_reinflate | bitset | no_reinflate/hybrid | no_reinflate/bitset |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.0003945 | 0.0001861 | 0.0001355 | 0.0000090 | 0.7281 | 15.0555 |
| 8 | 0.0003766 | 0.0002222 | 0.0001286 | 0.0000094 | 0.5788 | 13.6809 |
| 12 | 0.0002993 | 0.0001702 | 0.0001212 | 0.0000210 | 0.7121 | 5.7714 |
| 16 | 0.0002750 | 0.0002405 | 0.0000963 | 0.0000391 | 0.4004 | 2.4629 |

### IR cost decomposition, no-reinflate

| n | total_s | ir_compile | bitset_eval | ratio/bitset |
|---:|---:|---:|---:|---:|
| 4 | 0.000160 | 0.000107 | 0.000037 | 18.44 |
| 8 | 0.000168 | 0.000120 | 0.000032 | 16.27 |
| 12 | 0.000303 | 0.000212 | 0.000067 | 7.88 |
| 16 | 0.000195 | 0.000113 | 0.000065 | 3.71 |

### IR cache hit, no-reinflate

| n | no_reinflate_total_s | ir_compile | bitset_eval | ratio/bitset | ir_cache_hit |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000070 | 0.000000 | 0.000042 | 7.57 | 1 |
| 8 | 0.000055 | 0.000000 | 0.000035 | 5.24 | 1 |
| 12 | 0.000075 | 0.000000 | 0.000057 | 2.71 | 1 |
| 16 | 0.000108 | 0.000000 | 0.000076 | 1.62 | 1 |

### Persistent cache end-to-end no-reinflate

| n | baseline_no_reinflate_s | persistent_cache_no_reinflate_s | speedup |
|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000098 | 1.51x |
| 8 | 0.000144 | 0.000080 | 1.80x |
| 12 | 0.000203 | 0.000110 | 1.84x |
| 16 | 0.000219 | 0.000116 | 1.89x |

### Persistent cache cached execution vs bitset

| n | baseline_no_reinflate_s | cached_exec_s_per_eval | bitset_s | bitset_cached_s_per_eval | cached/bitset_cached |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.000147 | 0.000024 | 0.000010 | 0.000003 | 8.12 |
| 8 | 0.000144 | 0.000027 | 0.000010 | 0.000005 | 5.54 |
| 12 | 0.000203 | 0.000047 | 0.000031 | 0.000009 | 4.90 |
| 16 | 0.000219 | 0.000066 | 0.000053 | 0.000027 | 2.42 |

---

## Final Condensed Takeaway

The most useful result for future writing is:

> Dense CM is not the fastest raw evaluator. But CM IR is a valuable structural compiler. When CM reduces the Boolean problem, bitset executes the reduced form, dense CM reinflation is avoided, and compiled IR is cached, the system approaches bitset performance while preserving structure that pure bitset lacks.

This supports at least three strong research directions:

1. **CM as compiler / optimizer**
2. **Representation cost and no-reinflation**
3. **Compile-time amortization and reusable symbolic structure**
