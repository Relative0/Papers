# Response to the attached publication-readiness review

**Revision:** 26 September 2026. **Disposition:** contract/specification corrections completed; synthetic pair-token primary test failed; natural/circuit and submission gates remain open.

This response now addresses both the pasted summary and the subsequently supplied full audit/checker bundle. The full report was read, its 21 manifest entries were verified, and its unmodified reference checker was rerun with results identical to the supplied record. [FULL_AUDIT_RECONCILIATION.md](FULL_AUDIT_RECONCILIATION.md) maps every P1/P2/P3 finding to current evidence and remaining work. The September 22 manuscript, prior audits, and first revision delivery ZIP are preserved. The compiler source remains unmodified.

| Review concern | Change / evidence | Status |
|---|---|---|
| Dense output incorrectly described as unfixed-axis output | Sections 5.1–5.4 now retain every ambient row/column axis, distinguish syntactic/essential/ambient counts, give exact shape and the 4-by-2 fixed-Z example, and charge NumPy Boolean bytes. Tests cover both fixed values, all three strategies, irrelevant axes, ownership and budget refusal. | Resolved in draft and executable regressions |
| Valid derivations confused with selected strategy | Section 4 treats inference as an admissibility relation. Section 5.2 gives ordered case selection, S/T/H outcome mapping, and the legacy `structural` alias. `X AND Y` can derive S and T; pure compilation of `X OR (Y AND Y)` still fails. The theorem's fallback clause now explicitly concerns selected failure. | Resolved |
| Support ambiguous | Explicit recursive `Vars(e)` minus `dom(F)` definition, with cancellation examples. No essential-dependence minimization is assumed. | Resolved |
| Child folds assumed to survive root failure | Section 5.2 states original-AST fallback and distinguishes attempted counters from committed results. A spy regression verifies the identical original AST is passed to the real builder after child success. Root retabulation can also supersede earlier work. | Resolved; no different persistent-rewrite algorithm introduced |
| Token failure, invalid input and actual fallback conflated | Duplicate/overlapping layouts are errors; token `None` with `ordinary_fallback` is a diagnostic; only the dense wrapper executes fallback. Budget checking occurs before token compilation. | Resolved |
| Novelty too close to classical operations | Abstract and contribution language narrowed; Proposition 3.3 attribution, kitty operations, mockturtle's ordered leaf interface, and AIG candidate/gain/commit behavior compared explicitly. No claim of novel truth-table algebra, unprecedented operand metadata, or measured engineering advantage. | Positioning corrected; research significance remains for reviewers to assess |
| No current implementation artifact/check chain | Recovered 63 source/import/test files at the pinned commit, checked Git blobs and SHA-256, added a portable runner, 33 contract cases and current manifest. 90 upstream tests plus the 33 new cases pass. | Current contract chain closed; historical 116-test identity remains unestablished |
| Historical evidence merely reported | Recovered 95 byte-identical S1/S2/P14 archive members. Recounted S1/S2 observations and all P14 primary point estimates; reproduced all 17 P14 bootstrap interval sets from 51,102 raw rows. Eight P14 freeze hashes match. | Analysis closure improved; historical imported-runtime identity is not certified by its freeze |
| Missing/obsolete package-relative checker | Current runner uses only packaged dependencies and data. Historical broken checker is retained as history and clearly not the current entry point. | Resolved for this revision |
| Confirmatory pair study missing | Preserved protocol v3. A disclosed synthetic-only protocol v4 retained its primary cell and thresholds, froze 64 held-out formulas, and executed 30 paired repetitions per formula. Direct packed/CM median time ratio was 0.2479 (95% interval 0.2462–0.2495), so primary utility failed. | Synthetic cell answered negatively under a post-import cache-reset regime; full v3 circuit scope remains open |
| Natural applicability unknown | Calls for root admission by strategy and attempted work discarded at root failure, distinct from timing evidence. | Open empirical work; v4 synthetic cases cannot establish prevalence |
| Other useful editorial/evidence corrections | Removed detailed later-project results from abstract; kept P14 table with its subsection; corrected 98.75% marginal versus 95% familywise interpretation after inspecting frozen analyzer quantiles; restored P14 environment/amendments; corrected AIG page range and Lee first author. | Resolved in revision |

## Verification actually performed

- All 123 selected tests pass under Python 3.10.11 / NumPy 2.2.6 / pytest 9.0.2, including 327,680 signed-fusion assignment comparisons across all five implemented outer operations.
- 63 pinned source files have verified Git blob identities and current SHA-256 checks. They are not edited to make the tests pass.
- Recovered S1/S2: 10,500 rows, 10,389 all-arm completions, zero differences in the seven stated CM/generic symbolic metrics, and the reported failure patterns and medians confirmed.
- Recovered P14: 51,102 timing rows; four primary case-balanced ratios and all 17 archived interval sets reproduced with 10,000-draw bootstrap replay; eight frozen source/holdout hashes verified. This did not rerun historical timing workers.
- Frozen v4 primary cell: 64 held-out formulas, 3,840 timing rows, 128 memory rows, zero correctness disagreements or recorded failures. The independent recount matches the frozen analyzer. Median packed/CM ratio 0.2479, 95% interval [0.2462, 0.2495], so primary success is false.
- The PDF build and visual QA records are packaged separately. A successful build is not a mathematical proof or a publication-readiness certificate.

One initial new checker attempted to pass an arbitrary outer truth-table integer to the implementation's string-only five-operation `cm_compose` API. The checker was corrected to test the five implemented operations, giving the explicitly reported 327,680 comparisons. No implementation behavior was changed. The first LaTeX build encountered a sandbox denial for MiKTeX's user cache; the build was subsequently run with the required tool access.

## Remaining submission work, in priority order

1. Complete a prospectively selected natural-input root-admission survey and applicable ABC/AIG, ROBDD and generic-folding comparisons. Map sharing, reuse, output and process-start regimes without replacing the failed v4 primary cell.
2. Establish which imported compiler/runtime bytes produced historical P14 timings, then prepare a public versioned archive with corpus provenance and a stable identifier. Bootstrap analysis replay is complete; new timing workers are not needed for that analytical step.
3. Reassess venue and contribution significance using the resulting evidence. The contract suite is a useful methods artifact but does not alone prove journal-level novelty or performance.

These are separate research/release requirements. The authorized draft revision, full-audit reconciliation, source recovery, regression checks, historical bootstrap replay and synthetic-only v4 timing campaign are complete. The audit's original readiness score is a historical assessment of the September 22 draft; it has not been silently recalculated or presented as a new independent verdict on this revision. No production compiler code change, external publication, commit, or push was performed.
