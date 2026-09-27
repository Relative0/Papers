# P01 independent publication-readiness audit package

Audit date: 26 September 2026. Audited source: research draft dated 19 September 2026.

## Read first

`P01_ASTRA_PUBLICATION_READINESS_AUDIT.md` is the full report, including the mathematical reconstruction, evidence limits, primary-source comparisons, six simulated referee perspectives, scorecard, gates and final determination.

`P01_CLAIM_BY_CLAIM_AUDIT.csv` has 18 claim records.
`P01_PUBLICATION_BLOCKERS.md` has 0 P0, 2 P1 and 7 P2 issue records.
`P01_SCORECARD.json` contains 19 scores and eight gates.
`audit_data.json` contains the structured claim/issue/score/gate records used to prepare the report.
`LITERATURE_SEARCH_NOTES.md` records representative actual queries and search limitations.

## Reproduce the NEW audit calculations

Run from this extracted directory with Python 3.10 or later:

```bash
python p01_independent_checks.py --out new_results
```

Only the Python standard library is used. Do not run with `python -O`, which disables the assertion-based checks. The default exhaustive order cutoff is 9; reducing it changes the tested population. Avoid overwriting the supplied evidence directory. The tested environment was Python 3.13.5 on Linux.

Expected scope: 22,170 nonzero 2-by-2 resources across nine small rings, 38 A4 resources, all 65,536 A4 matrices for the separate Smith inventory, 36 Hardy cases, 28 analyzer configurations, 52 coding certificates, exhaustive binary-field coding optimization, and 255 three-party two-setting tensors. Exact category counts appear in the report and result JSON.

Deterministic substantive outputs should agree. Runtime and platform fields will differ. Direct support decisions use contraction tables and implication graphs, not the analytic Smith criterion; the Smith-inventory category aggregation DOES use the invariance proof and separately tested representatives.

This new checker is NOT the author's unchanged historical runner. The original supplied generator failed because input dependencies are missing; the exact failure log is preserved in `evidence/original_runner_attempt.log`. Historical stages, missing reproduction-envelope inputs and the 112/144 LM split were not certified by this audit.

## Evidence

`evidence/independent_full/` contains the new support cases, summary, analyzer/coding certificates and Smith inventory. The evidence root contains source inventory/hash checks, original-run failure, clean LaTeX build logs, a text-equivalence comparison and rendered contact sheets. Empty `pdf_text_diff.txt` indicates no text difference after whitespace normalization.

All 34 original archive files were left unchanged. The source manuscript is not repackaged here as a revised draft. There is no proof-assistant certification and no definitive historical-priority certification.

## Verdict

Preprint: READY AFTER SPECIFIC MAJOR CORRECTIONS.
Journal: MAJOR REVISION BEFORE SUBMISSION.
Main recommendation: preserve the principal theorem set, repair reproduction/availability claims, strengthen theorem-level positioning, and apply the localized corrections. Additional mathematical scope is not required by this audit.
