# Correspondence Matrix Computation Audit
## Prediction, Routing, Search Guidance, CM IR, and Performance Research

**Purpose:** This document is intended to be ingested by Codex / GPT Pro as a continuity and research brief for the `CM_Computation` project.

**Primary local project path:**

```text
C:\Users\brian\Documents\CM_Computation\
```

**Primary documentation path:**

```text
C:\Users\brian\Documents\CM_Computation\docs\
```

---

# Evidence status

The specified directory,

`C:\Users\brian\Documents\CM_Computation\`

was not mounted in the ChatGPT browser runtime that produced this audit. There were also no CM repository files attached to that conversation or present in its accessible file library.

Therefore, the producing agent did **not** reconstruct the repository call graph, inspect CM IR, rerun benchmarks, or independently reproduce C5 or C36. Doing so without the files would have required inventing evidence.

This document therefore contains:

1. a rigorous **provisional audit** of the supplied C5/C36 claims;
2. a fresh external-research analysis;
3. a concrete experimental roadmap;
4. one selected immediate experiment;
5. instructions for bringing the repository evidence into a Codex / GPT Pro session.

All project-specific numerical claims remain provisional until reproduced from repository artifacts.

---

# 1. Executive conclusion

The strongest present recommendation is:

> **Do not make the existing answer-predicting GNN deeper. Prospectively validate exact-backend routing first, then instrument exact search to determine whether partition ordering can actually reduce work.**

The priorities should be:

## 1.1 Run the frozen C36 routing rule prospectively

C36 is presently the only supplied result with an asserted positive end-to-end opportunity: `1.2841×` charged routing headroom.

If that number uses the conventional definition

\[
S=\frac{T_{\mathrm{default}}}{T_{\mathrm{oracle}}},
\]

then `1.2841×` corresponds to an oracle path taking approximately

\[
\frac{1}{1.2841}\approx 0.7788
\]

of baseline time, i.e. a maximum reduction of about **22.1%**.

That is meaningful, but not large enough to tolerate an expensive feature extractor or neural router.

The next experiment should therefore test the already-frozen family rule on entirely unseen circuit identities and an independent source. No architecture search and no adjustment after seeing the confirmation data.

## 1.2 Profile exact computation before introducing more prediction

The exact backends should be treated as the primary optimization targets:

- direct AST;
- flattened CSE;
- CM IR;
- compiled truth projection;
- exact ANF;
- any decomposition-assisted route.

The profile needs to separate parsing, support construction, IR conversion, ANF conversion, candidate generation, verification, allocation, hashing, and actual Boolean/GF(2) operations.

Until this exists, it is impossible to know whether CM IR, ANF, verification, Python object traffic, or repeated representation conversion is the meaningful bottleneck.

## 1.3 Investigate deterministic decomposition filters before a learned partition model

Older Boolean-decomposition literature may be unusually relevant here.

Published work describes disjoint bi-decomposition tests based on Boolean differential calculus and Walsh transforms, including filters using subsets of spectral coefficients to eliminate nondecomposable cases and identify AND-, OR-, or XOR-type decompositions.

The decisive project-specific question is:

> Is the repository's CM decomposition target mathematically equivalent to, reducible to, or strongly constrained by any known Boolean functional-decomposition form?

A cheap exact rejection test could be more valuable than increasing GNN accuracy, especially if most candidate partitions are negative.

## 1.4 Reformulate learning as search guidance — but only after proving search order matters

A partition ranker is promising only when changing the order changes the amount of exact work.

This is usually plausible for positive cases where search stops upon finding a witness. It may be false for negative cases where every candidate must ultimately be exhausted.

The exact search should therefore first be instrumented to answer:

- Does candidate order affect nodes explored?
- Does it affect cache reuse or pruning?
- What fraction of total time occurs on positive versus negative cases?
- How much oracle ordering headroom exists?

Only then should a tree, boosted ranker, or GNN be considered.

## 1.5 Retain answer-predicting neural work only if a perfect-predictor lower bound is profitable

For the C5-style route, measure

\[
T_{\mathrm{unavoidable}}
=
T_{\mathrm{features}}
+
T_{\mathrm{inference}}
+
T_{\mathrm{proposal}}
+
T_{\mathrm{verification}}.
\]

If this already equals or exceeds the best exact baseline, even a perfect model cannot help.

That direction should then be terminated.

---

# 2. Evidence manifest

## 2.1 Repository evidence actually available to the producing agent

| Evidence | Status | Use |
|---|---|---|
| `C:\Users\brian\Documents\CM_Computation\` | Not accessible | No repository claims reproduced |
| Current prompt and supplied C5/C36 summary | Available, but secondary | Used only as reported claims |
| Public originating CM paper | Available | Used for mathematical context |
| External primary research | Available | Used to assess alternative strategies |

No repository filename should be inferred from this report.

## 2.2 Claims that remain unverified

| Supplied claim | Audit status | Required evidence |
|---|---|---|
| C5 balanced accuracy ≈ `0.594` | Not reproduced | Predictions, labels, split manifest, metric code |
| Confirmation accuracy ≈ `0.75–0.78` | Not reproduced | Frozen checkpoint, confirmation identities, raw predictions |
| Model has `136,962` parameters | Not reproduced | Model definition and saved configuration |
| Training uses 48 pairs from five circuits | Not reproduced | Dataset manifest and provenance |
| Generated cases reached perfect accuracy | Not reproduced | Generator, split construction, raw results |
| Safe neural path was `6.3–9.2×` slower than exact ANF | Not reproduced | Per-phase timings and benchmark harness |
| C36 charged routing headroom was `1.2841×` | Not reproduced | Per-instance backend timing matrix and charging rules |
| C36 family rule | Not inspected | Rule implementation and frozen thresholds |
| CM IR semantics and implementation | Unknown | IR node definitions, construction, execution, tests |
| Verification duplicates exact discovery | Plausible but unmeasured | Verifier and fallback call graph plus phase timings |

---

# 3. What a Correspondence Matrix means

The originating paper presents a correspondence matrix as a **2×2 binary matrix representing a binary propositional operator**.

The rows and columns correspond to positive and negative forms of the two operands, and the paper enumerates the 16 possible matrices corresponding to the 16 binary Boolean operators.

The paper also generalizes the idea to logical measurement matrices, whose entries are logical expressions; a correspondence matrix is described as a positive valuation of such a logical matrix.

This establishes several distinct concepts that must not be conflated.

## 3.1 Mathematical CM

A 2×2 binary encoding of a binary logical relation.

## 3.2 Logical measurement matrix

The more general expression-valued measurement structure.

## 3.3 Repository CM artifact

Whatever concrete data structure the code uses to represent a CM or a larger composition of CMs.

This is currently unknown and must be determined from code.

## 3.4 CM IR

A project-specific intermediate representation.

It might encode:

- a DAG of CM operations;
- a compiled evaluation plan;
- a decomposition;
- a lowered Boolean form;
- or some combination.

Its meaning cannot be inferred from the paper.

## 3.5 Potential exact implementation implication

Because there are only 16 binary 2×2 CMs, a local CM can in principle be encoded in a four-bit integer rather than a general matrix object.

Under such a representation:

- negation can be a four-bit complement;
- transposition can be a fixed bit permutation;
- rotations can be fixed bit permutations;
- operator lookup can be a small table lookup;
- combinations of two CMs can often use precomputed tables;
- batches of truth assignments can potentially use packed machine words.

This is an inference from the mathematical representation, **not** a finding about the repository.

If CM IR already uses such encoding, there may be nothing to gain.

If the implementation currently allocates matrix or expression objects for many local CM operations, this should be benchmarked early.

Larger logical matrices should also not automatically be materialized merely because the mathematics permits their construction. A factorized, lazy, DAG-based, or otherwise compact representation may be essential.

---

# 4. Reported computational architecture

Only the following architecture can be inferred from the supplied material.

```text
circuit / expression / cone
          │
          ├────────────── exact ANF baseline
          │
          ├────────────── direct AST
          │
          ├────────────── flattened CSE
          │
          ├────────────── CM IR
          │
          └────────────── compiled truth projection
```

Two learned pathways appear to exist conceptually.

## 4.1 C5-style proposal path

```text
input
  │
feature and graph construction
  │
GNN inference
  │
candidate mathematical proposal
  │
exact verification
  ├── accepted ──> exact result
  └── rejected / abstained ──> exact fallback
```

## 4.2 C36-style routing path

```text
input
  │
cheap routing features
  │
backend selection
  │
one exact backend
  │
exact result
```

The critical economic difference is that the C36 selector cannot make the mathematical answer wrong when every backend is exact.

A poor decision costs time but does not require a second computation to verify the selector.

The appropriate expected-cost expression for a proposal path is approximately

\[
\begin{aligned}
E[T_{\mathrm{proposal\ path}}]
={}&E[T_{\mathrm{features}}]
+E[T_{\mathrm{inference}}]
+E[T_{\mathrm{proposal}}] \\
&+E[T_{\mathrm{verification}}]
+P(\mathrm{fallback})
E[T_{\mathrm{fallback}}\mid\mathrm{fallback}].
\end{aligned}
\]

The corresponding routing cost is

\[
E[T_{\mathrm{route}}]
=
E[T_{\mathrm{routing\ features}}]
+
E[T_{\mathrm{decision}}]
+
E[T_{\mathrm{selected\ exact\ backend}}].
\]

Accuracy is not the primary objective in either case.

The real objective is end-to-end charged runtime.

---

# 5. Provisional C5 diagnosis

## 5.1 Reproduction status

None of the numerical C5 claims could be reproduced without the repository artifacts.

## 5.2 What the supplied numbers would imply

A balanced accuracy of `0.594` is only `0.094` above the binary chance level of 0.5.

That is modest performance, but it should not be judged alone.

The economically relevant questions include:

- Were false positives much more expensive than false negatives?
- Did confidence correlate with profitability?
- Was verification cheaper for accepted correct proposals?
- Did positive and negative circuit families have different costs?
- Was the confirmation set easier or structurally related to training data?

The difference between `0.594` and approximately `0.75–0.78` does not by itself prove instability, but it requires an identity-level explanation.

Performance should be reported separately by:

- source;
- circuit;
- cone family;
- support width;
- target class;
- generated versus natural origin.

## 5.3 Parameter count versus data

The comparison between approximately `136,962` parameters and 48 training pairs is suggestive but should not be overinterpreted mechanically.

A graph model can receive node-level, variable-level, or partition-level supervision from one circuit.

The more serious concern is the reported presence of only **five independent training circuits**.

Generalization to unseen circuit families is controlled by the number and diversity of independent circuit/source groups, not simply by the number of graph nodes or candidate pairs.

Five independent groups cannot provide a stable estimate of broad transfer.

## 5.4 Ranked diagnosis, assuming the supplied summary is accurate

### 1. Economic headroom and verification duplication

This is the most serious issue.

A safe path that is reportedly `6.3–9.2×` slower than exact ANF must remove an enormous amount of verification or fallback work before it can break even.

Better classification accuracy does not automatically remove feature construction or verification.

### 2. Target mismatch

Predicting a complete mathematical answer is likely the wrong target when the answer must subsequently be rediscovered or nearly rediscovered by verification.

More suitable targets may be:

- which exact backend to use;
- which candidate partition to test first;
- which variable to branch on;
- which rewrite to attempt;
- whether an inexpensive exact filter should be run;
- expected runtime difference between exact paths.

### 3. Insufficient independent natural data

Perfect performance on generated motifs combined with weak natural-circuit transfer would be a strong sign that the generator exposes a shortcut or lacks deployment-distribution diversity.

### 4. Representation mismatch

The graph may omit algebraic information required to recognize the target, including:

- cofactor relationships;
- variable interactions in ANF;
- long-range reconvergence;
- support structure;
- algebraic interaction structure.

### 5. Model capacity and activation choice

This should be last.

Additional depth, GELU, SiLU, normalization, or residual connections might improve optimization, but nothing in the supplied result indicates insufficient neural capacity is the principal failure.

## 5.5 Perfect-predictor test

Break the accepted path into:

\[
T_{\mathrm{accepted}}
=
T_{\mathrm{features}}
+
T_{\mathrm{inference}}
+
T_{\mathrm{proposal}}
+
T_{\mathrm{verification}}.
\]

Then measure it using a known-correct proposal, bypassing model errors entirely.

Terminate answer prediction when either condition holds:

1. median \(T_{\mathrm{accepted}}\) is not meaningfully below the fastest safe exact baseline; or
2. upper-tail cost eliminates the savings after accounting for eligible-case frequency.

This experiment is much more informative than another activation-function sweep.

---

# 6. Provisional C36 diagnosis

## 6.1 Why C36 is more promising

Per-instance algorithm selection is a well-established systems strategy.

The important architectural property for this project is that every backend can remain exact while the selector predicts only which exact method is likely to be cheapest.

This avoids the correctness/verification burden of answer prediction.

The appropriate metric is not backend classification accuracy.

For instance \(x\), define runtime regret as

\[
R(x)
=
T_{\mathrm{chosen}}(x)
-
\min_j T_j(x).
\]

The total charged objective should be based on the runtime of the complete policy.

## 6.2 Interpretation of reported `1.2841×`

Assuming the reported number is an oracle-versus-default speedup,

\[
\frac{T_{\mathrm{oracle}}}{T_{\mathrm{default}}}
=
\frac{1}{1.2841}
\approx 0.7788.
\]

Thus the entire selector, including extra routing features, has at most about 22.1% of baseline time available as gross savings.

This argues against a GNN router unless:

- its graph representation is already needed downstream;
- inference is extremely cheap;
- or simple models leave a substantial fraction of oracle opportunity uncaptured.

A shallow deterministic rule or small tree may be the correct final solution.

## 6.3 Break-even decision

For candidate backend \(j\) versus default backend \(d\), route only when

\[
\widehat{T_d-T_j}
>
T_{\mathrm{route-only\ features}}
+
T_{\mathrm{decision}}
+
\delta,
\]

where \(\delta\) is a safety margin for timing noise and distribution shift.

When that condition is not met, use the exact default.

---

# 7. External research implications

## 7.1 Exact backend selection

Algorithm-selection systems such as SATzilla demonstrate the value of selecting among complementary exact solvers on an instance-by-instance basis.

The relevant transfer to CM computation is:

- predict runtime or regret, not mathematical output;
- charge feature computation;
- compare against the best single backend;
- calculate oracle headroom first;
- prefer simple models when headroom is modest.

Candidate models should include:

1. frozen family rule;
2. depth-limited decision tree;
3. regularized linear or pairwise model;
4. gradient-boosted trees;
5. separate runtime regressors;
6. neural router only if simpler methods leave material headroom.

## 7.2 Learned guidance of exact solvers

Research such as NeuroCore demonstrates an important pattern:

> A learned model can guide an exact solver without replacing it.

A crucial detail is that frequent neural inference can be too expensive.

For CM search, a promising architecture is therefore:

```text
one graph encoding
       │
one batched score for all partitions / variables
       │
initialize exact search order
       │
continue with cheap native heuristics
```

Do not invoke an expensive GNN inside every small branch decision unless measurements prove it profitable.

## 7.3 Learned compiler cost models and autotuning

Compiler/autotuning systems such as TVM/Ansor use learned cost models to rank exact implementation alternatives rather than predict program outputs.

A possible CM analogue is:

```text
equivalent exact representations / rewrites
                │
cheap structural cost model
                │
small selected candidate set
                │
measure or execute exact candidates
```

The important difference is amortization.

Compiler autotuning may spend substantial search time because a kernel executes many times later.

If CM instances are mostly one-shot, per-instance tuning must be extremely cheap or trained offline.

## 7.4 Exact algebraic and spectral pruning

ANF computation is connected to Möbius transforms.

Depending on width and sparsity, bit-packed and word-parallel implementations may substantially reduce constant factors.

For decomposition specifically, Boolean functional-decomposition literature suggests possible exact filters based on:

- cofactors;
- Boolean derivatives;
- ANF interaction structure;
- Walsh/spectral signatures;
- disjoint-support constraints.

The key project-specific research question is:

> Does the CM decomposition being searched for imply any cheap necessary condition that can reject most candidate partitions without performing full discovery?

If so, a deterministic filter could:

1. eliminate impossible partitions;
2. identify likely decomposition type;
3. provide stronger labels;
4. shrink the exact search before any learned method is considered.

## 7.5 BDDs and variable ordering

BDD performance can vary catastrophically with variable order.

Therefore BDDs should be investigated only as a conditional representation/backend.

Potential eligibility signals include:

- moderate support width;
- repeated cofactor queries;
- bounded expected node growth;
- reuse across many related queries.

The benchmark must charge:

- build time;
- ordering time;
- peak node count;
- memory;
- amortization count.

A learned variable-order predictor is worth considering only after establishing that a BDD backend itself has useful oracle headroom.

## 7.6 Equality saturation and constrained rewrite search

Unguided equality saturation can suffer severe combinatorial growth.

The more plausible use for CM computation is bounded local rewrite exploration:

1. run existing exact rewrites;
2. retain alternatives only at bounded cuts or motifs;
3. canonicalize equivalent local forms;
4. extract using a measured downstream CM/ANF cost;
5. impose strict node, iteration, memory, and time budgets.

Do not begin with unrestricted e-graph saturation of entire expressions.

---

# 8. Bottleneck and opportunity analysis

## 8.1 Likely C5 bottleneck hierarchy

Based only on the supplied summary:

1. verification and fallback duplication;
2. feature/graph-construction cost;
3. target misalignment;
4. insufficient independent data;
5. representation;
6. network architecture.

## 8.2 Important limitation of partition ranking

Suppose an exact algorithm tests \(N\) independent candidate partitions.

For a positive case, good ranking may reduce expected work from roughly \(N/2\) tests toward one test.

For a negative case, merely permuting candidates still requires all \(N\) tests.

The ranker then adds cost while saving nothing.

Partition guidance therefore needs at least one of:

- high enough positive-case rate;
- branch-dependent pruning;
- improved cache reuse;
- exact filters eliminating candidates;
- a certificate-producing positive proposal;
- a cascade avoiding the ranker on likely negatives.

This should be established empirically before training.

## 8.3 Feature piggybacking

Routing features should be collected during work already required by all backends wherever possible.

Candidate nearly-free features include:

- support width;
- node count;
- logical depth;
- operation histogram;
- fan-out statistics;
- number of unique nodes versus references;
- CSE reuse ratio;
- reconvergence counts;
- estimated truth-table storage;
- number of requested outputs;
- repeated-query count.

A separate graph construction solely for routing is unlikely to fit within a 22% gross headroom unless baseline instances are expensive.

## 8.4 CM-specific exact opportunities to inspect

Repository inspection should answer:

- Are local CMs stored as four-bit values or heavyweight objects?
- Are transforms implemented as constant-time bit permutations?
- Are support sets recomputed?
- Are identical sub-CMs hash-consed?
- Does CM IR repeatedly convert to AST, ANF, or truth-table form?
- Are truth vectors packed into machine words?
- Is there a sparse/dense ANF crossover?
- Are cofactor results cached across candidate partitions?
- Are sibling cones recomputing identical subgraphs?
- Is feature extraction traversing the graph separately from exact preprocessing?
- Are compiled artifacts reused when the same cone is queried repeatedly?

---

# 9. Opportunity matrix

The speedup entries below are research expectations or ceilings, not claims of achieved project performance.

| Strategy | Class | Exact result? | Potential | Confidence | Added overhead | Engineering effort | Main risk |
|---|---|---:|---|---|---|---|---|
| Frozen C36 family rule | I | Yes | Up to reported `1.2841×` development ceiling | Medium-low pending confirmation | Very low | Low | Headroom may not transfer |
| Shallow tree / boosted runtime router | II with exact backends | Yes | Limited by routing oracle | Medium-low | Low | Low–medium | Overfitting small circuit groups |
| Confidence-gated routing cascade | II with exact backends | Yes | Better overhead/safety trade-off | Medium | Low on easy cases | Medium | Calibration shift |
| CM IR/exact-backend profiling and optimization | I | Yes | Unknown; possibly substantial | Medium | None at runtime if successful | Medium | Optimizing a non-hot phase |
| Packed/bit-parallel ANF/truth operations | I | Yes | Workload-dependent | Medium | Low | Medium | Support width or sparsity may dominate |
| Walsh/cofactor decomposition filters | I | Yes | Potentially high rejection savings | Medium-low | Low–moderate | Medium–high | Decomposition notion may not match CM target |
| Hand-engineered partition ordering | I | Yes | High only when order changes work | Medium-low | Very low | Low | Negative cases may remain exhaustive |
| Boosted-tree partition ranker | II | Yes | Unknown | Medium-low | Low | Medium | Saves search nodes but not wall time |
| GNN partition/order scorer | II | Yes | Unknown | Low until dataset grows | Moderate–high | High | Inference and data independence |
| Certificate-carrying decomposition proposal | III | Yes after check | High if checking is much cheaper | Low pending measurements | Verification | Medium–high | Verification duplicates discovery |
| BDD conditional backend | I/II | Yes | Potentially high on selected families | Low–medium | Build and ordering | Medium–high | Catastrophic BDD growth |
| Bounded cut-tracing/e-graph exploration | I/II | Yes | Speculative but plausible | Low | Bounded rewrite/extraction | High | Search-space growth |
| SAT/SMT decomposition formulation | I/II | Yes | Unknown | Low | Encoding / solver startup | High | Encoding exceeds specialized search |
| Deeper C5 answer GNN | III | Yes only after verification | Present evidence negative | Low | High relative to baseline | Medium | Accuracy improves without profitability |

---

# 10. Immediate next experiment

## C37 — Prospective confirmation of the frozen exact-backend family rule

This should be the next experiment because it has the highest information value per engineering hour.

It answers three questions at once:

1. Does the reported C36 opportunity generalize?
2. Is the family rule sufficient?
3. Is there enough remaining oracle headroom to justify any learned router?

## 10.1 Pre-registration

Before examining the new circuits, freeze and record:

- exact C36 rule source code;
- all thresholds and family definitions;
- fallback/default backend;
- eligible exact backends;
- features used by the rule;
- current Git commit;
- benchmark command;
- primary metric;
- success and termination criteria.

Store this in:

```text
C37_PROTOCOL.md
```

The independent corpus must not be used to revise the rule.

## 10.2 Dataset

Use an entire natural-circuit source not previously used in C36.

Requirements:

- no generated variants;
- no transformed copies of C36 circuits;
- no sibling cones split across development and confirmation;
- provenance recorded at repository, source file, parent circuit, and cone levels;
- all eligible instances selected by a rule fixed before timing;
- exclusions and failures retained in the result table.

The statistical unit for confirmation should be the parent circuit or source, not the individual cone.

## 10.3 Timed policies

Measure:

1. current production/default backend policy;
2. frozen C36 family rule;
3. every exact backend independently, solely to calculate the oracle;
4. optionally a uniform best-single-backend determined on C36 development data, not selected using C37.

Do **not** fit a decision tree or boosted model to C37 before reporting the frozen-rule result.

## 10.4 Complete charged time

For the frozen policy:

\[
T_{\mathrm{policy},i}
=
T_{\mathrm{common},i}
+
T_{\mathrm{route-only\ features},i}
+
T_{\mathrm{decision},i}
+
T_{\mathrm{selected\ backend},i}.
\]

For the default:

\[
T_{\mathrm{default},i}
=
T_{\mathrm{common},i}
+
T_{\mathrm{default\ backend},i}.
\]

Common preprocessing should be charged identically and should not be performed separately for routing and execution.

## 10.5 Measurement protocol

For each instance:

- verify every backend produces the same canonical result;
- measure cold one-shot execution as the primary mode;
- report a warm/reused mode separately only when repeated use is realistic;
- randomize backend execution order;
- execute policies in separate process runs so oracle measurement does not warm policy runs;
- use repeated measurements;
- for very short cases, execute batches long enough to exceed timer-resolution and scheduler noise;
- report median instance time rather than minimum;
- record peak memory and timeout status;
- record CPU, OS, interpreter/compiler, dependencies, power mode, and commit.

## 10.6 Primary metric

\[
S_{\mathrm{frozen}}
=
\frac{\sum_i T_{\mathrm{default},i}}
{\sum_i T_{\mathrm{frozen},i}}.
\]

Bootstrap confidence intervals by parent circuit, not by individual cone.

## 10.7 Secondary metrics

Report:

- oracle total speedup;
- best-single-backend speedup;
- geometric mean per-instance speedup;
- median, p90, p95, and p99 runtime regret;
- worst absolute regret;
- fraction of cases slower than default;
- fraction more than `1.25×`, `1.5×`, and `2×` slower than default;
- route-only feature cost;
- fraction of oracle savings captured:

\[
C
=
\frac{T_{\mathrm{default}}-T_{\mathrm{frozen}}}
{T_{\mathrm{default}}-T_{\mathrm{oracle}}}.
\]

## 10.8 Proposed decision rules

These thresholds must be frozen before seeing results.

### Terminate routing research

Do so when independent oracle speedup is no greater than approximately `1.05×`.

### Retain the frozen rule

Retain it when:

- all correctness comparisons pass;
- total point speedup is at least `1.05×`;
- the circuit-group bootstrap lower bound exceeds `1.00×`;
- tail regressions satisfy the predeclared operational guard.

### Strong positive result

Treat the rule as a production candidate when:

- total speedup is at least `1.10×`;
- it captures at least 40% of the independent oracle saving;
- feature cost remains a small portion of realized saving;
- there is no unacceptable expensive-tail regression.

### Justify a simple learned router

Proceed to a tree or boosted model only when:

- independent oracle speedup remains at least approximately `1.15×`;
- the frozen rule leaves substantial oracle opportunity;
- inexpensive static features are available;
- enough independent circuit groups exist for source-held-out evaluation.

## 10.9 Required output artifacts

```text
C37_PROTOCOL.md
C37_INSTANCE_MANIFEST.csv
C37_TIMINGS_LONG.csv
C37_OUTPUT_EQUIVALENCE.csv
C37_ENVIRONMENT.json
C37_SUMMARY.json
C37_REPORT.md
```

Every timing row should include:

```text
source_id
circuit_id
cone_id
backend
repeat
mode
common_time
route_feature_time
decision_time
backend_time
total_time
result_hash
status
peak_memory
```

---

# 11. Subsequent experimental roadmap

## Experiment 2 — Routing headroom decomposition

**Hypothesis:** Most of C36's oracle opportunity can be captured with very cheap static features.

Compare:

- best single backend;
- frozen rule;
- depth-2 through depth-5 CART;
- regularized multinomial or pairwise logistic model;
- histogram gradient boosting;
- one log-runtime regressor per backend;
- oracle.

Use nested group-held-out evaluation.

Optimize charged runtime or regret, not winner accuracy.

**Kill criterion:** no model beats the frozen rule by a predeclared practically meaningful margin on a second untouched source.

---

## Experiment 3 — Confidence-gated routing cascade

**Hypothesis:** Expensive features are useful only for ambiguous cases.

Use:

```text
Level 0: free metadata
    ↓ decisive?
yes → exact backend
no
    ↓
Level 1: one cheap structural pass
    ↓ decisive?
yes → exact backend
no → robust default
```

Compute richer features only when

\[
E[\text{additional saving}\mid x]
>
T_{\text{additional features}}+\delta.
\]

**Kill criterion:** the cascade's feature savings do not improve complete runtime over the best one-stage policy.

---

## Experiment 4 — Exact-backend phase profiler

**Hypothesis:** duplicated preprocessing, allocation, hashing, or representation conversion accounts for a meaningful portion of runtime.

Instrument:

- parsing;
- support calculation;
- AST traversal;
- CSE flattening;
- CM IR construction;
- ANF transformation;
- truth compilation;
- candidate generation;
- verification;
- fallback;
- result canonicalization.

Also collect counts:

- nodes allocated;
- support-set computations;
- hash calls;
- cache hit rates;
- unique versus referenced nodes;
- IR conversions;
- ANF monomial counts;
- truth-vector bytes.

**Success criterion:** identify one or more phases comprising at least 15–20% of end-to-end time and a change that reduces complete runtime.

**Kill criterion:** CM IR or another proposed optimization target is below approximately 5–10% of total time.

---

## Experiment 5 — Exact decomposition-filter study

**Hypothesis:** CM decomposability entails a known cofactor, Boolean-differential, ANF-interaction, or Walsh-spectral condition that rejects candidates cheaply.

Steps:

1. Formalize the exact repository decomposition condition.
2. Map it against disjoint bi-decomposition and Ashenhurst-Curtis-style decomposition.
3. Derive necessary conditions.
4. Implement exact filters in increasing cost order.
5. Measure rejection rate and false-negative rate.
6. Charge filter cost.

Candidate filter classes:

- support separability;
- variable-interaction hypergraph components;
- cofactor equality/complement patterns;
- Boolean derivatives;
- selected Walsh coefficients;
- ANF mixed-monomial tests;
- rank/signature tests.

**Required correctness:** a pruning filter must have zero false negatives, supported by a proof or exhaustive validation over bounded supports.

**Kill criterion:** filter computation costs more than the exact candidates it eliminates.

---

## Experiment 6 — Search-order sensitivity before learning

**Hypothesis:** partition order materially changes exact-search work.

Run identical instances under:

- current order;
- random orders;
- size-balanced order;
- support-based order;
- cofactor-similarity order;
- oracle hindsight order.

Measure:

- candidates visited;
- recursive nodes;
- pruning events;
- cache hits;
- time to first witness;
- total time;
- positive and negative cases separately.

**Kill criterion:** ordering changes candidate count but not wall time, or negative exhaustive cases dominate total runtime.

---

## Experiment 7 — Modest partition ranker

Proceed only if Experiment 6 establishes headroom.

Start with:

- deterministic score;
- pairwise logistic ranker;
- boosted ranking trees.

Use a GNN only after those baselines.

Train against a cost label such as

\[
y(p)
=
-\text{exact work incurred when }p\text{ is explored next},
\]

rather than simply `valid/invalid`.

Report top-\(k\), MRR, and ranking accuracy, but use end-to-end exact runtime as the primary metric.

**Kill criterion:** ranking improves top-\(k\) metrics without improving complete wall-clock time.

---

## Experiment 8 — Certificate economics

For each correctly proposed decomposition, measure

\[
\rho
=
\frac{
T_{\mathrm{certificate\ construction}}
+
T_{\mathrm{verification}}
}{
T_{\mathrm{baseline\ discovery}}
}.
\]

Possible witnesses include:

- partition plus explicit factors;
- decomposition tree;
- rewrite plus substitution;
- canonical motif and instantiation map;
- exact ANF identity;
- SAT miter proof where appropriate.

A useful initial engineering target would be median \(\rho<0.2\), with the upper tail still below break-even.

**Kill criterion:** verification normally repeats a substantial fraction of discovery or requires the full baseline representation.

---

## Experiment 9 — Conditional representation portfolio

Add BDD, sparse ANF, dense packed ANF, or other representations only behind strict eligibility limits.

Candidate routing features:

- support width;
- truth-table memory estimate;
- ANF density;
- reconvergence;
- CSE reuse;
- repeated cofactor-query count;
- expected number of downstream queries.

Measure construction plus use.

Report the break-even reuse count.

**BDD kill criterion:** node/memory growth exceeds a predeclared cap or build time is not amortized by repeated queries.

---

## Experiment 10 — Bounded rewrite-alternative tracing

Do not begin with unrestricted equality saturation.

Instead:

- record equivalent alternatives discovered by current rewrites;
- retain them only at bounded cuts;
- canonicalize local alternatives;
- set node and time budgets;
- extract using measured downstream backend cost.

**Kill criterion:** rewrite recording and extraction consume more time than the selected representation saves, or memory growth becomes heavy-tailed.

---

## Experiment 11 — Neural guidance

Only after earlier experiments establish:

- meaningful independent oracle headroom;
- at least hundreds of independent natural circuits or source groups;
- a stable exact search target;
- cheap batched inference;
- strong non-neural baselines.

Then evaluate:

- small hierarchical GNN;
- residual message passing;
- graph transformer only when long-range structure is demonstrably missing;
- one-shot candidate scoring;
- distillation into a cheap MLP/tree for deployment.

Depth, activation, dropout, and normalization become relevant here — not before.

---

# 12. Pre-registered kill criteria

## Answer-predicting GNN

Stop when the known-correct-proposal path, including features and verification, cannot beat the best exact baseline by a useful margin.

## Exact-backend routing

Stop when independent oracle headroom disappears or route-only features consume most of the available saving.

## Partition ranking

Stop when ordering does not alter total exact work, particularly on negative cases that dominate runtime.

## Certificate proposals

Stop when checking the witness is comparable in cost to discovering the result.

## CM IR optimization

Deprioritize when CM IR construction and execution are not material hotspots.

## BDD/ZDD

Stop on unacceptable node growth, memory tails, or insufficient query reuse.

## SAT/SMT encoding

Stop when encoding construction or solver startup dominates the specialized baseline, or when encoding scales badly before the current method does.

## Equality saturation

Stop when e-graph construction, saturation, or extraction exceeds the saved downstream computation.

Use bounded alternatives rather than increasing limits indefinitely.

---

# 13. Final judgment

Based on the information presently available:

> **The existing C5 result is not a strong argument for a larger GNN. It is an argument that answer prediction is probably occurring at the wrong layer of the system.**

The most defensible current order is:

1. prospectively validate the frozen exact-backend rule;
2. establish independent routing oracle headroom;
3. profile and improve exact representations and shared preprocessing;
4. reconcile CM decomposition with established Boolean decomposition theory;
5. measure whether candidate order changes exact search;
6. use deterministic or boosted search guidance;
7. investigate cheap certificates;
8. reserve neural guidance for a larger, independently sourced dataset.

C36-style routing is presently the leading strategy because it offers reported measurable value without creating a correctness burden.

The most promising genuinely mathematical direction is the search for exact cofactor, differential, ANF, or spectral filters that exploit the particular CM decomposition condition.

---

# 14. Repository ingestion instructions for Codex / GPT Pro

## 14.1 Why `C:\...` was "not mounted"

A ChatGPT browser conversation does **not automatically have permission to read arbitrary files on the local Windows filesystem**.

Writing a path such as

```text
C:\Users\brian\Documents\CM_Computation\
```

in a prompt does not expose those files to the model.

The path is meaningful to software running on the local computer, but a browser-based ChatGPT session generally sees only:

- files explicitly uploaded to the conversation/workspace;
- files available through connected storage/tools;
- files available in a local coding environment that has actually been granted filesystem access.

Therefore the earlier audit could see the path string but not the underlying repository.

## 14.2 Best option when Codex is running locally with filesystem access

If Codex is operating in an environment that can directly access local files, point it at:

```text
C:\Users\brian\Documents\CM_Computation\
```

and give it this Markdown file as the research brief.

Then instruct it:

> Do not recursively ingest the repository. First inventory filenames, sizes, Git state, and targeted `rg` matches. Build a 12–30-file evidence manifest before reading deeply.

This is preferable to uploading a ZIP because the agent can selectively inspect files and execute benchmarks in place.

## 14.3 Best option for a browser-based GPT Pro session

If the Pro session cannot directly access the local filesystem, then **uploading a ZIP is the practical route**.

However, do not begin by zipping the entire repository unless necessary.

Preferred sequence:

### Package A — targeted audit bundle

Include approximately 20–40 high-value files:

- originating CM paper or canonical mathematical source;
- C5 experiment code;
- C5 result summaries/raw predictions;
- C5 dataset/split manifest;
- verifier/fallback code;
- C36 experiment code;
- C36 timing results;
- C36 frozen family rule;
- exact backend implementations;
- CM IR implementation;
- benchmark/timing harness;
- dataset construction/provenance code;
- relevant environment/requirements file;
- Git commit/state information.

### Package B — broader docs/results only if needed

If Package A reveals missing dependencies, upload a second ZIP containing:

- `docs/` sections related to computation/experiments;
- compact benchmark result tables;
- profiling output;
- relevant tests.

Avoid media, generated videos, caches, environments, build artifacts, and unrelated documentation.

## 14.4 If uploading a larger repository ZIP

It is acceptable to ZIP:

- the relevant `docs/` tree;
- source code;
- tests;
- compact result artifacts;

and attach it.

But tell the agent explicitly:

> The ZIP is a filesystem container, not permission to ingest every file into context. Inventory first; use targeted search; select a small evidence set; expand only to resolve dependencies.

This avoids context pollution.

## 14.5 Recommended ZIP exclusions

Exclude:

```text
.git\objects
.venv
venv
node_modules
__pycache__
.pytest_cache
.mypy_cache
build
dist
coverage
large generated media
video_factory output
duplicate archives
temporary benchmark dumps
large raw datasets that have compact summaries
```

Include `.git` metadata only if needed for history and if reasonably sized; otherwise include:

```text
git rev-parse HEAD
git status --short
git log --oneline -n 30
```

as text files.

## 14.6 Strong recommended upload structure

```text
CM_Codex_Audit_Package/
│
├── READ_FIRST_CM_PERFORMANCE_AUDIT.md
│
├── EVIDENCE_MANIFEST.md
│
├── git_state.txt
│
├── paper/
│   └── originating_cm_paper.*
│
├── c5/
│   ├── code/
│   ├── results/
│   └── dataset_manifest/
│
├── c36/
│   ├── code/
│   ├── results/
│   └── frozen_rule/
│
├── exact_backends/
│   ├── anf/
│   ├── ast/
│   ├── cse/
│   ├── cm_ir/
│   └── truth_projection/
│
├── verification/
├── benchmark_harness/
├── dataset/
└── relevant_docs/
```

The file you are reading should be renamed or copied to:

```text
READ_FIRST_CM_PERFORMANCE_AUDIT.md
```

## 14.7 Opening instruction for the next Codex / Pro session

Use:

> Read `READ_FIRST_CM_PERFORMANCE_AUDIT.md` first.
>
> Then inspect the uploaded project package, but do **not** recursively ingest every file. Begin with directory inventory and targeted searches for C5, C36, C37, CM IR, exact ANF, direct AST, flattened CSE, compiled truth projection, verification, fallback, routing, decomposition, partition, benchmarks, dataset splits, and provenance.
>
> Build an evidence manifest of approximately 12–30 primary files before performing the substantive audit.
>
> Reproduce project-specific numerical claims from primary artifacts before relying on them.
>
> Where executable access is available, inspect and run the benchmark harness rather than reasoning only from documentation.
>
> Treat this audit file as a hypothesis and research plan, not as ground truth.

---

# 15. Recommended practical next step

For a browser-based Pro session:

1. Create a ZIP containing the **targeted evidence bundle** first.
2. Include this Markdown file at the root as `READ_FIRST_CM_PERFORMANCE_AUDIT.md`.
3. Attach the ZIP to the new Pro/Codex session.
4. Paste the opening instruction from section 14.7.
5. Allow the agent to request a second, broader ZIP only if a dependency is genuinely missing.

If it is easier operationally to ZIP the entire relevant source/docs/results area, that is also workable, provided the prompt explicitly instructs the agent to **inventory and selectively read rather than ingest everything**.

The key distinction is:

> **Upload access can be broad; context ingestion should remain selective.**

