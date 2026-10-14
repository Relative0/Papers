# Hostile mathematical and priority review

Reviewer role: independent theorem/priority audit agent. Date 2026-09-29. The reviewer independently reconstructed proofs, wrote a separate finite checker without importing archived code, searched primary literature, and inspected `code/hybrid_core.py` and its SAT/defect documentation. This is an internal review, not external peer review. Benchmark outcome review is appended only after final result files exist.

## Hostile mathematical referee

| ID | Attack | Severity | Disposition |
|---|---|---|---|
| MAT-01 | A failed vtree cut is not a semantic-prime certificate. Are oracle labels being used to declare residual work empty? | Critical if present | Corrected interpretation explicitly in theorem audit; core refines every nonsingleton direct block. No shortcut based on known oracle alignment found in `exact_refine`. |
| MAT-02 | F1's lower-bound proof loosely says every internal split is between prime unions, which is false inside a prime block. | Proof exposition | Reconstructed proof separates the skeleton above prime roots from internal prime-block trees. The theorem survives. |
| MAT-03 | Does a support hyperedge mean every variable in it belongs to one prime? | Critical if present | No. The stored pair (U,W) certifies an existential crossing only. EQ3 AND EQ2 gives an explicit counterexample to whole-support merging. Core emits pair must-links only for singleton/singleton supports. |
| MAT-04 | Does greedy shrinking find the narrowest support? | High if claimed | No. Two incomparable minimal supports of widths 2 and 3 are independently checked; reports say inclusion-minimal only. |
| MAT-05 | Does deletion monotonically shrink a valid witness when SAT changes the context? | High | Yes, because equality assumptions restrict permitted support and all contexts may be re-solved. Earlier failed deletions remain infeasible. The stored prior SAT model is retained after UNSAT queries. |
| MAT-06 | Does a small defect-width parameter prove fast total factorization? | High if claimed | No. Query bounds do not bound the difficulty of each global CNF query. The two-point relation forces full support, and the pilot retains a global encoding. Reports explicitly deny FPT runtime. |
| MAT-07 | Are laminarity and carrier LCC applied to unknown semantic primes? | High if present | Core obtains exact semantic primes before LCC. Soft search weights may use carriers, but carrier/current-exposure compatibility is not promoted into certification of unknown prime compatibility. |
| MAT-08 | Is it sound to query a sub-block against the whole outside global formula? | High | Yes, conditional on the documented nonfalse function and certified direct partition. Outside factors are independent and nonfalse, so multiplication preserves the active-cut rank-one condition. |
| MAT-09 | Does the nonfalse theorem silently include UNSAT formulas or missing/free variables? | High | The proofs require nonfalse f. SDD pipeline detects false separately and normalizes skipped/free sides to singleton blocks. Caller must honor the documented `exact_refine` precondition. |
| MAT-10 | Does the CM theorem allow general shared DAGs? | High if claimed | No. Repeated-variable cancellation is an explicit counterexample; distinct leaves and support disjointness remain mandatory. |
| MAT-11 | Is the focused group-deletion bound circular or dependent on a unique minimum? | Medium | Bound uses the actual returned support width d, not the unknown smallest width. Every failed group intersects the final support, so the depth count is sound without uniqueness. Generic MSMP prior art limits novelty. |

Independent finite checker result: zero failures on 2,959 partition pairs through n=5, 246 all-equal nontrivial cuts through n=8, and 4,101 monotone-predicate/order pairs through n=4. These are checks, not substitutes for the mathematical proofs.

## Hostile novelty/priority referee

| ID | Attack | Severity | Disposition |
|---|---|---|---|
| PRI-01 | Rotations, swaps, dynamic SDD minimization and graph/hypergraph decomposition are being renamed as new methods. | High if claimed | Explicitly classified as prior art with Choi/Darwiche 2013, d4 2017, and newer graph/treewidth work. |
| PRI-02 | Incremental assumption solving for Boolean decomposition is supposedly new. | High if claimed | Lee/Jiang/Hung 2008 and Chen/Janota/Marques-Silva 2012 are cited; implementation is an application. |
| PRI-03 | A small oracle-query theorem is being used to rescue an algorithmic NO-GO. | High | Rejected. MSMP work from 2013/2016 is direct antecedent; the proof is useful documentation, not sufficient novelty or practical benefit. |
| PRI-04 | The priority audit stopped at old papers and missed 2025/2026 semantic/circuit structure work. | High | Current search added Circuit-Aware d-DNNF 2025; TDD 2026; semantic-vtree NeSy 2026 artifact; circuit-interaction vtree TPM 2026; query-oriented AAAI 2026 and distributed 2026 preprint. |
| PRI-05 | The 2026 semantic-vtree paper is dismissed based on its title alone. | High for submission | Not dismissed. Metadata and conference listing were verified; full theorem-level comparison remains an explicit publication prerequisite. No firstness claimed. |
| PRI-06 | A true elementary laminarity/cofactor theorem is automatically publication-ready. | Medium | Rejected. Mathematical validity and originality are tracked separately. No new paper is justified solely by repackaging these facts. |
| PRI-07 | Public toy examples constitute industrial benchmark validation. | High if claimed | They are smoke controls only. A maintained-library pilot on small synthetic instances must be described at that scale. |

No unambiguous new, publication-ready theorem is established by this priority audit. A transparent negative pilot and reusable exact implementation can remain useful research artifacts. Any later publication claim requires the narrowly identified theorem-level comparisons, not an unrestricted literature restart.

## Final outcome review and acceptance

After principal execution, this reviewer read `PHASE5B_MASTER_REPORT.md`, `BENCHMARK_RESULTS.md`, `STATISTICAL_ANALYSIS.md`, `NEXT_RESEARCH_GATE.md`, and `data/statistical_summary.json`. A separate read-only calculation over all principal JSONL rows independently confirmed 600 training, 600 validation, and 900 held-out rows; all 2,100 trial cells are unique, status `ok`, and marked correct for both semantic and simultaneous partitions. Recomputing median-of-three paired M5/B3 times gives geometric ratio **2.211513105083704**, with **0 wins, 30 losses, 0 ties**. This reproduces the reported point estimate directly from raw data. The reported 10,000-draw bootstrap interval is **[2.008170496336859, 2.4275540473614283]**; this final review read that interval and the analysis description, rather than presenting it as a second independently executed bootstrap.

The registered residual-work rescue also fails in the saved summary: median paired call reduction -0.9308035714285714, SAT-wall reduction -1.5713347709770238, and absolute SAT-wall saving -0.0006111500842962414 seconds. Negative reductions are additional work, not improvements. There is no basis for substituting a more favorable secondary metric or claiming fewer SAT calls established an overall speedup.

**Final mathematical acceptance:** the reports accurately separate structural proofs from empirical observations. The semantic-prime certification correction remains visible and prevents an oracle-alignment shortcut. Neither the empirical success of exactness checks nor the support-query bound is promoted into an unrestricted correctness proof or runtime theorem. The negative campaign does not refute F1–F3, and those proofs do not overturn the negative campaign.

**Final priority acceptance:** category **D. MATHEMATICAL NOTE SURVIVES; ALGORITHMIC NO-GO** is defensible as a project disposition because the reports explicitly call the surviving note a *working note* and explicitly state that publication-ready novelty is not established. Category D must not be read as certifying an original publishable mathematical contribution. The MSMP application is not used to justify category B, and no firstness, industrial speedup, or general impossibility claim is made. Omitting a new LaTeX submission draft is appropriate under the user's conditional deliverable.

The scope limitations are materially important and adequately disclosed: small related synthetic structures, a modest graph baseline, an orientation/candidate-prefix search restriction, native B2 versus recompilation-based custom search, and no industrial benchmark corpus. The bootstrap is correctly described as conditional descriptive resampling, not independent population evidence. Oracle O remains an evaluation control. The next gate correctly defers further experiments and requires a new scientific mechanism and preregistration before any later campaign.

**Disposition: accepted for delivery as a reproducibility package and negative bounded pilot.** No further mathematical/priority wording repair is required in the inspected final reports. Remaining limits are research/publication limitations, not unfinished work within this phase. No additional model run, benchmark, or optional experiment is recommended now.
