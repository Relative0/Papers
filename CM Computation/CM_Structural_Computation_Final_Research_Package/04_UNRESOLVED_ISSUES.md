# Unresolved issues and exclusions

## Material research-submission blockers

**U01 - Differentiated novelty.** No precise historical-first theorem/algorithm claim has been established. The work integrates known structures with a concrete source audit and data. A rigorous future novelty comparison must identify what standard KC/decomposition systems do not already provide.

**U02 - Optimized comparators.** CUDD installation/download attempts failed; no optimized CUDD, DSD, ACD, industrial KC or tensor-train implementation was benchmarked. The Python ROBDD is explicitly a reference baseline. Discussion is not a substitute for these runs.

**U03 - External breadth.** All 26 external functions are outputs of one control circuit, not independent families. There is no heldout industrial multi-design study or natural prevalence estimate.

**U04 - Independent assurance.** Reviews are same-assistant role-separated passes, not independent models or human peer reviewers. Proofs and code still need external expert scrutiny. The checker is not formally verified.

## Bounded limitations, not hidden completed tasks

**U05 - Scale/input model.** Discovery is capped at sixteen declared variables; timed synthetic cases reach twelve. Source input is an explicit truth integer, with extraction outside the comparison. No scalable formula-to-artifact compiler claim is made.

**U06 - Physical persistence and memory.** The v3 replay reconstructs fresh in-memory instances, but does not measure cold disk, new processes, CPU isolation, resident memory or multi-machine performance. Binary byte counts cannot stand in for RSS.

**U07 - Historical performance.** Source and logs are retained, but no complete historical C35/C36/P14 campaign was rerun and reconciled here. Historical speedups are not current findings or new-paper evidence.

**U08 - Security and API totality.** Constructor aliases and malformed examples are checked, but there is no hostile-input/resource-exhaustion/security audit. Serialization supports documented field limits, not every arbitrary mathematical payload. A directly constructed payload requires shape checking and external verification before it is trusted.

**U09 - Search/global optimality.** Both old and new searches are bounded; the new search uses a 16-candidate budget. No globally optimal decomposition, variable order or encoding is claimed.

**U10 - Weighted/care-set queries.** These are not implemented/evaluated in the paper. A don't-care completion cannot silently replace the original total function in an exact unrestricted count.

**U11 - Current literature coverage.** Primary sources were searched and key results inspected. This is not exhaustive priority clearance. Recent sparse-transform and tensor-network classification papers are triaged with their different arithmetic/access models, not fully audited or imported.

## Internal issues that were actually repaired

The earlier parse-only reload proxy is corrected in the v3 replay and still labeled in historical arms. Direct caller-owned mutable lists are deep-frozen in v3. Histograms are not substituted for assignment-indexed factors. All three manuscript versions are preserved. See issue-response matrices for exact evidence rather than treating these assertions as independent certifications.


## Final QA: additional codec-policy boundary

A numerical cap of n<=16 is not a universal JSON-serialization guarantee. With this runtime's default 4,300-decimal-digit conversion guard, dense truth integers at n=14 and n=16 are rejected by the artifact and packed JSON paths. The guard was not globally disabled. The SC binary format round-trips both examples successfully. All reported timing cases stop at n=12, so those measurements are not invalidated. A hex-integer JSON schema or a consistently binary persistence path is required before claiming broad JSON support through the numerical cap. See `reproducibility/raw_results/scope_limits_v3.json`.
