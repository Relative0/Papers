# Independent engineering, statistics and graph-baseline review

Date: 2026-09-29. Review performed by the frozen-reproduction agent, separate from the primary benchmark implementation. This is an internal adversarial review, not an external peer review. No held-out method was run for this review; findings below follow from source and protocol inspection before benchmarking.

Reviewed SHA-256 values at the final inspection:

| File | SHA-256 |
|---|---|
| BENCHMARK_PROTOCOL.md | c6a535c34ff11e67ed0056baa09f0d82c36cdeeee45ac13ca97a45052f6ff43a |
| code/make_benchmarks.py | 62a07cf7e66e6481f0cd395df595a8c758463c90c497db22aec1384b8d53ca8d |
| code/benchmark.py | 0b14e6fd55a05113a30b9f2ec886cc87fb787d8f5153f2867ade2c026e04ad25 |
| code/hybrid_core.py | c162c115fc8c97e82f5eaa6d05429ebf5b07a7ea61dc68e060875182b54c0abc |

## Verdict

The design is suitable for a **small maintained-backend implementation pilot**, subject to completing the preregistered analysis/selection checks below. It cannot support an industrial-performance GO under any observed result. No semantic-ground-truth leakage was found in the non-oracle objective or exact residual algorithm. The exactness argument appears sound under its stated nonfalse input and certified direct-partition contracts; backend tests remain necessary and are reported separately.

## Issues requiring action or explicit restriction

### E1 — Structural overlap makes held-out generalization weak [high; reporting restriction]

Most n=6/n=8 train, validation and held-out inputs are variable-renamed copies of one structure per family. Clean/aligned/crossing cases share the same conjunction-of-equalities semantics. The bounded-treewidth family is a directed implication path, the read-once family is an AND of binary OR clauses, and the indecomposable control is an equality chain. Redundant and repeated-module families add a fixed pattern of implied cross-clauses. Most variation is variable naming; n=10 introduces a size change, not a new structural family. Only the planted random-CNF family has substantially different clause structures across seeds.

**Required treatment:** report this as a fixed-generator/relabeling pilot. Instance-bootstrap intervals quantify variation within this specific finite mix and are not independent evidence of generalization to industrial circuits or unseen structural families. The primary split must remain unchanged now that registered; an expanded independently structured benchmark is a later gate, not a post-hoc substitution. A numerical pilot GO is at most authorization to investigate further. An industrial algorithmic claim remains NO-GO/not established regardless of the pilot ratio.

### E2 — Resume could silently mix source versions [high; repaired before runs]

Initial inspection found that `run_split` overwrote the split receipt while reusing existing result rows. A repair was requested immediately. The rechecked implementation now rejects changed source/protocol/manifest hashes, rejects existing rows without a receipt, retains the first receipt, and adds a `run_fingerprint` to each new row. This resolves the identified flaw for new runs. Correctness repairs after data collection must preserve old rows in an explicitly invalidated run directory; they cannot inherit the old successes.

**Analysis follow-through:** verify row fingerprints against the receipt and reject duplicate/missing `(instance, method, replicate)` cells. A receipt match by itself does not prove the JSONL is complete.

### E3 — Baseline selection and analysis must be frozen before held-out [high; operational check required]

The protocol correctly selects B2 or B3 on validation and names M5 as the sole primary challenger. At review time the runner accepts `heldout` without checking a saved baseline-selection artifact, and no aggregation script was part of the requested review.

**Required before held-out:** save the selected baseline, exact selection calculation, complete validation-row identifiers/fingerprints, tie rule, and analysis source hash. Guard the held-out entry point or otherwise record a verifiable chronological selection receipt. Do not switch to the better held-out baseline or the best M variant for the primary claim. Other comparisons remain exploratory.

### E4 — Residual-work rescue needs explicit zero/censoring rules [medium; define before held-out]

The registered rescue has three simultaneous thresholds, including a 5 ms absolute median SAT saving, which usefully prevents declaring tiny call-count changes meaningful. However, “median paired SAT-call/SAT-wall reduction” does not specify how zero baseline work, timeouts and missing SAT fields are handled.

**Required treatment:** predefine these cases before observing held-out. A both-zero pair supplies no improvement, and baseline-zero/method-positive cannot count as a favorable percentage. Censored/error pairs must not be silently discarded to improve the rescue statistic. Require all three repetitions or label the analysis incomplete. Show absolute SAT times and setup/probe overhead alongside ratios. Rescue is separate from, and cannot retroactively replace, a failed primary runtime criterion.

### G1 — B3 is a modest graph heuristic, not a full treewidth baseline [medium; reporting restriction]

`syntax_tree` builds primal-graph components, performs greedy min-fill elimination within each component, and then makes a balanced vtree over the elimination order. It does not construct an elimination tree, junction tree, branch decomposition, or a vtree with a proved width guarantee. This distinction matters: a min-fill ordering followed by balancing need not preserve the decomposition structure that made the ordering attractive.

**Required wording:** “syntax-component, min-fill-ordered balanced vtree baseline.” Do not describe it as a state-of-the-art treewidth compiler or infer superiority over treewidth methods. The protocol already calls it modest, and the explicit component factoring is an appropriate strong baseline on the clean planted families. A serious industrial follow-up should include a standard decomposition-to-vtree construction and broader baseline portfolio.

### G2 — Six-neighbor serialized prefix is a strong label/shape bias [medium; exploratory limitation]

The neighborhood contains child swaps and binary rotations recursively. Only the first six unseen trees in `repr` order are compiled each round, with at most two rounds. Numeric variable labels and tuple serialization therefore determine which local regions get attention. Equivalent renamings can change the candidate prefix. Child swaps and symmetric moves can consume much of the budget, and the two-round search can stop without considering all improving moves in the full neighborhood.

This is a reproducible and semantic-free bounded heuristic, not a correctness error. The fixed budget must not be retuned from held-out results. **Required reporting:** identify the prefix policy and avoid attributing failure or success to the intrinsic quality of exposure/carrier/defect objectives. Save move traces as planned. Balanced move-type coverage or seeded candidate sampling belongs to a new preregistered experiment.

### E5 — Native minimization versus full recompilation confounds objective quality [medium; already disclosed]

B2 uses PySDD's native minimizer; each M candidate recompiles the CNF in a new manager. End-to-end comparison remains legitimate because that overhead is real and included. It does not isolate whether a different objective would work well when integrated into the native dynamic optimizer. One must not report an M loss as a theorem that factor-aware objectives are ineffective, nor an M gain as equal-budget search superiority.

### E6 — Carrier information is used after semantic refinement [medium; already disclosed]

The exact routine refines semantic factors first and applies carrier LCC afterward. This is exact but can spend SAT work distinguishing semantic factors that the carrier will immediately merge. All methods share that routine, so the comparison is internally consistent. It does not compare against the potentially cheaper carrier-compatible residual algorithm in the Phase 4 architecture. Crossing-carrier controls can be especially affected. Claims must name this implemented pipeline.

## Ground-truth and correctness audit

- Parent-side enumeration computes semantic ground truth for evaluation; only method O receives an `oracle_partition` payload. Other workers receive input metadata, CNF, carrier and seeds. No non-oracle objective branch reads stored semantic truth, family labels or planted semantic factors.
- M objectives use actual compiled SDD size, certified direct partitions, carrier sets and SAT-derived support sets. Unioning U and W for a soft span score does not impose an unsound all-pairs must-link constraint.
- All nonsingleton direct blocks remain unresolved and receive exact SAT refinement, even for O. This avoids confusing a failed vtree cut with semantic primeness and avoids granting oracle labels as a hidden certificate to ordinary methods.
- The SDD extraction handles true/free variables, literals and trimmed descendant nodes separately. False input yields no claimed prime partition. The finite backend test suite must cover these paths, permutations and post-minimization trees.
- Residual queries keep variables outside the active certified factor on the complement side. Nonfalsity and the certified product decomposition justify equivalence with refinement inside that block. Arbitrary heuristic partitions must not be substituted for these certificates.
- The four-corner encoding uses equivalences for clause outputs, conjunctions and muxes; the asserted product XOR is appropriate. Equality assumptions for shrinking restrict varying support while permitting contexts to change. This supports inclusion minimality, not minimum cardinality.
- Original variables only are included in the benchmark factorization universe; no Tseitin variables are mistakenly treated as semantic coordinates. The planted random family is satisfiable because every clause has at least one positive literal and the all-true assignment satisfies it.

## Timing, memory and censoring audit

The worker's outer timer starts after worker-module imports and input parsing, but before tree construction, probing and compilation. It includes later PySDD/PySAT imports, temporary-vtree I/O, every candidate compilation, extraction, objective processing, residual solver setup/search, and carrier LCC. Component timers omit some overhead included by the outer timer, so they need not sum to total. This is acceptable if reported plainly. Diagnostics must remain outside this primary timer as registered and must not feed back into objectives.

The 15-second parent subprocess watchdog measures full worker process time, including interpreter startup and parsing, whereas successful `total_seconds` excludes those. This is a resource cap on the whole trial, not precisely a 15-second algorithm timer. Report both quantities and this difference. PAR2=30 seconds is a fixed penalty for censored/error rows, not an estimate of their completion time. Median-of-three aggregation can hide one failed replicate in the timing median; the separate failure-count gate therefore matters and must use all raw repetitions.

Peak working set is an OS process high-water value on the recorded Windows platform and includes dependencies/interpreter. On platforms without `peak_wset`, the fallback is endpoint RSS and must not be labelled peak memory. Failed/time-out workers have missing in-worker memory measurements; do not report survivor-only memory as though complete.

## Before-data checklist and final claim boundary

1. Keep the repaired immutable receipts and validate all expected rows/fingerprints.
2. Complete backend correctness checks before runtime trials.
3. Freeze validation baseline selection and all aggregation/zero/censoring rules before held-out.
4. Preserve the registered manifest and candidate budget; do not tune from held-out.
5. Report the small relabeling-heavy generator, limited graph baseline, biased prefix neighborhood and recompilation asymmetry with the results.
6. An industrial superiority claim is not established by this pilot, regardless of its primary GO/NO-GO arithmetic. The immediate result is a reproducible implementation gate and a decision about whether this specific small campaign justifies a larger independently structured test.

## Final principal-outcome disposition

The completed principal results, `BENCHMARK_RESULTS.md`, `STATISTICAL_ANALYSIS.md`, `PHASE5B_MASTER_REPORT.md`, and the final analysis source were reviewed after principal timing. This follow-through inspected existing data and independently recomputed the primary statistics; it did not execute any benchmark method or alter raw results. Supplementary move/SAT-reuse/public diagnostics were still being handled separately and are outside this principal-outcome arithmetic review.

**Accounting and provenance: PASS.** Independent raw-row checks found exactly 600 train, 600 validation and 900 held-out records, with every required `(instance, method, seed)` cell present once. All 2,100 rows have successful status, correct semantic and simultaneous partitions, and the expected receipt fingerprint. The algorithm/protocol/manifest maps agree across all three split receipts. The current validation bytes and analysis source match the baseline-selection hashes. Selection timestamp `2026-09-29T10:27:31.388585+00:00` precedes the held-out receipt timestamp `2026-09-29T10:27:45.601149+00:00`.

**Baseline selection: PASS.** Independent recomputation gives validation geometric means of `0.040818944317991795` seconds for B2 and approximately `0.0395112332782700` seconds for B3, so the recorded B3 selection follows the registered rule. No held-out method is substituted as the baseline.

**Primary arithmetic: PASS; improvement criterion: FAIL.** The independently recomputed M5/B3 ratio is `2.211513105083704`. Repeating the registered 10,000-draw paired log-ratio bootstrap from the stored times and seed gives `[2.008170496336859, 2.4275540473614283]`. M5 has 0 faster, 30 slower and 0 tied instance medians. Report rounding and the interpretation that a ratio above one is slower are correct. The negative decision does not depend on a borderline interval or a tiny winning subset.

**Practical residual rescue: FAIL.** Independent recomputation, including probes, gives median paired SAT-call reduction `-0.9308035714285714`, SAT-wall reduction `-1.5713347709770238`, and absolute SAT-wall saving `-0.0006111500842962414` seconds. All three go in the unfavorable direction, so none reaches its registered positive threshold. No preprocessing cost is hidden in the rescue calculation.

**Earlier issue dispositions.** E2 is resolved by immutable receipts and row fingerprints. E3 is resolved for the final evidence: the analysis now rejects differing split source maps, rechecks validation and analysis hashes, and selection demonstrably preceded held-out. E4 has explicit zero and censoring rules and incorporates probe work; zero failures means censoring rules were not empirically exercised in this campaign. E1, G1, G2, E5 and E6 remain substantive scope limits and are properly retained in the reports rather than presented as repaired performance shortcomings.

The benchmark report distinguishes per-instance median runtime summaries from completed raw-trial SAT-count summaries. Family strata are descriptive, all ten have zero M5 wins, and no exploratory method or stratum changes the primary result. The reports correctly retain the relabeling-heavy generator, modest min-fill-balanced graph baseline, prefix-neighborhood bias, full-recompilation overhead and semantic-first residual limitation.

**Final engineering/statistics and graph/vtree disposition:** accept the principal computational accounting and the scoped **algorithmic NO-GO for this implementation and campaign**. No further arithmetic or graph-baseline claim correction is required for the reviewed principal reports. This is neither an industrial superiority result nor a refutation of every native implementation of factor-aware objectives. Supplementary diagnostics cannot rescue or revise the frozen primary decision.
