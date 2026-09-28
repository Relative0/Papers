# Final publication-readiness audit: Draft 3

**Date:** 26 September 2026.  
**Manuscript:** *Exact Boolean Decomposition Artifacts under Conditioning: Algebraic Contracts and a Reproducibility Audit*.  
**Status:** **TECHNICAL REPORT / WORKSHOP-LEVEL RESULT ONLY AT PRESENT.** This is an assessment of the material's present scope, not an acceptance prediction. Technical-report circulation is defensible after author checking; readiness as a novel competitive research submission is not established.

## What was completed

The original archive was recursively inventoried and selected primary source, theory and historical materials were inspected. The handoff was challenged rather than treated as authority. A complete manuscript v1 was frozen, audited and reviewed through seven separate specialist-role reports. Actual additional proofs, implementation work and experiments produced v2, which was then frozen and subjected to a second audit and seven reports, including four new roles. The resulting repairs produced v3 and a clean-directory correctness replay. All three TeX/PDF versions, raw results, response matrices, source snapshots and original portfolio are preserved.

These are **same-assistant, role-separated adversarial analyses**, not independently recruited human reviewers, separately executed models, or external peer review. Neither the reviews nor the finite tests constitute formal certification.

## Correctness assessment

The final mathematical statements have explicit domains and supplied proofs. Conditioning closure is substitution within disjoint scopes or Cartesian row/column selections. Counts retain unused declared variables. XOR counting uses an integer sign sum, not a Boolean-semiring product. Rank-profile counting is parity-aware; row streaming is polynomial in the listed factor-table input, while a dense rank transform can require excessive workspace. Minimal factor recompression, the complement-quotient bounds and the fixed-cut field/dictionary example were checked algebraically and computationally.

The persistence counterexamples are concrete and executed. The all-query state bound is a fixed-bit-state counting argument. The exact-verification bound is expressly limited to deterministic zero-error value-oracle access; it is not a statement against trusted integer metadata, formula proofs or certified KC. The report distinguishes stored-factor monotonicity from fresh ANF-component discovery.

No counterexample was found to these explicitly stated mathematical claims. That is not an unconditional guarantee of correctness. The main surviving mathematical concern is external independent checking and historical priority, not an identified false theorem.

## Executed evidence

| Evidence | Actual coverage |
|---|---|
| Original core suite | All 278 Boolean functions for 0 <= n <= 3; 3,988 artifacts; 105,292 conditioning/count checks |
| Rank/prototype/profile suite | All 65,536 binary 4x4 matrices |
| Persistence/recompression extensions | 3,020 sequential/fused checks; 2,000 recompressions; 151 binary round trips and trailing-data rejections |
| Legacy compatibility | 675 artifacts across the four old tags; 6,750 query comparisons |
| Exact field ranks | Rational elimination for inner-product matrices r=1..5 |
| Final loaded-state suite | 278 three-backend round trips; 7,070 three-backend query comparisons; 510 single-spike rank checks; explicit counterexamples and interface rejections |
| Final fresh-instance timing | 38 cases, three backends, five repetitions: 570 complete 128-query trials |
| Clean correctness replay | Eight commands in a fresh copied directory; all passed; original results not overwritten |

Do not sum these counts as independent statistical samples: suites overlap and test different properties. All 26 external functions come from one related design. The other 12 are deliberately synthetic. No industrial prevalence estimate or multi-family confidence interval follows.

## Ratings

Scores are editorial judgments on a 0--10 scale, not probabilities or peer-review votes. A score of 10 would mean strong evidence for the explicitly limited report scope, not absolute assurance.

| Area | Score | Reason / remaining limitation |
|---|---:|---|
| Mathematical correctness | 8 | Explicit proofs and extensive finite checks; no formal or independent proof review |
| Completeness for this report | 8 | All chosen semantic families, boundaries and versions covered; not the entire original research program |
| Novelty / differentiation | 3 | New integration, source audit and data in this pass; core mathematics is elementary or established and priority is not cleared |
| Prior-art coverage | 8 | KC, BDD, DSD/ACD, certified KC, tensor counting/trains, rank notions and transforms represented; not an exhaustive systematic review |
| Theorem quality | 7 | Useful exact formulations and counterexamples; not substantial new general theory |
| Experimental validity | 7 | Final actual reload replay repairs a real proxy issue; raw five-repetition data retained |
| Experimental generalization | 3 | One small external design, synthetic n<=12, no optimized industrial comparators or heldout second corpus |
| Reproducibility | 9 | Standard-library sources, pinned data, source snapshots and actual clean replay; independent external replication remains absent |
| Overlap control | 9 | FO calculus and CO compiler/P14 claims are explicitly excluded |
| Exposition | 8 | Worked irrelevant-variable, cancellation and histogram examples; full proofs and explicit scope |
| Limitations | 9 | No cold-disk/RSS claim, no CUDD comparison, no formal certification or historic timing promotion |
| Artifact traceability | 9 | Version crosswalks, issue ledger, raw records and hashes; publication decisions remain judgments |
| Public technical-report suitability | 8 | Coherent and transparent after author review |
| Mature competitive research submission | 4 | A differentiated theorem/algorithm or broader optimized empirical result is still needed |

## What the final review changed

The second audit did not merely approve v2. It found that earlier baseline loads parsed JSON but queried old live objects. The v3 benchmark constructs actual new instances from serialized data, rechecks them and times a complete batch. It also found that a frozen dataclass did not by itself protect arbitrary caller-owned lists; v3 deep-copies nested sequences into tuples and tests aliasing. The paper now explicitly rejects treating a one-query histogram as an all-query persistent representation.

## Final decision and unresolved issues

A standalone report exists with little substantive duplication of the neighboring CM-LM calculus or pair compiler. It is a focused combination of exact operational contracts, executable historical-boundary observations, and deliberately limited measurement. There is no basis here to advertise the four decomposition primitives, conditioning, model counting or certified compilation as new inventions.

The strongest remaining objections are: uncertain research novelty; missing optimized CUDD/DSD/ACD/KC/tensor baselines; only one external benchmark family; no measured resident memory; no independent external reviewers; and no formal verification. See `04_UNRESOLVED_ISSUES.md`. None is hidden behind a positive publication label.

The final result should be retained as a technical report and a reproducible foundation for a stronger follow-on experiment, rather than stretched into a general CM computational-superiority paper.


## Final QA: additional codec-policy boundary

A numerical cap of n<=16 is not a universal JSON-serialization guarantee. With this runtime's default 4,300-decimal-digit conversion guard, dense truth integers at n=14 and n=16 are rejected by the artifact and packed JSON paths. The guard was not globally disabled. The SC binary format round-trips both examples successfully. All reported timing cases stop at n=12, so those measurements are not invalidated. A hex-integer JSON schema or a consistently binary persistence path is required before claiming broad JSON support through the numerical cap. See `reproducibility/raw_results/scope_limits_v3.json`.
