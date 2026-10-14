# CM compiler publication-readiness audit - 26 September 2026

This is the audit deliverable, not a replacement manuscript or a claim that the complete author repository and timing campaigns have been reproduced.

## Start here

- `report/CM_Publication_Readiness_Audit_2026-09-26.pdf`: 26-page audit.
- `report/CM_Publication_Readiness_Audit_2026-09-26.md`: editable report, source locators, and primary-source links.
- `report/readiness_scorecard.json`: scores and release gates.
- `verification/independent_finite_checks.py`: standalone fresh mathematical/reference-model checker.
- `verification/independent_finite_results.json`: recorded check results.
- `evidence/`: archive inventory, integrity records, historical-content reconciliation, and manuscript build comparison.

## Rerun the independent checks

With Python 3.10 or newer, from this bundle's root:

    python verification/independent_finite_checks.py

This uses only the Python standard library. It writes `verification/independent_finite_results.json` and prints its results. It does not install or import the author's implementation, benchmark runtime, or validate the author's historical raw measurements. See the report for exact counts and limits.

## Rebuild this audit report

With Pandoc and a LaTeX installation:

    pandoc report/CM_Publication_Readiness_Audit_2026-09-26.md --lua-filter=report/break_code.lua --pdf-engine=pdflatex -o audit.pdf

The Lua filter only enables line breaks in long inline code/path strings for PDF layout.

## Interpretation

Overall structured assessment: 65.3/100. Preprint: GO AFTER SPECIFIED CORRECTIONS. Serious submission: MAJOR REVISION BEFORE SUBMISSION. Complete paper artifact: NOT YET REPRODUCIBLE.

The manuscript build and the independent local mathematics are reproducible from their respective recorded evidence. The author's 116-test run, raw S1/S2 and P14 statistics, and designated unexecuted confirmatory campaign were not rerun in this audit. Public implementation source was inspected at commit 0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b; source URLs and blob identifiers are in the report.

The original supplied ZIP remains the source for manuscript/review inputs. No manuscript edits were made. `verification/inventory.py` records the archive-inspection procedure and includes the audit runtime's input paths; those paths must be adjusted to rerun it against a locally extracted original archive. The historical checker failure is recorded as a packaging limitation, not as failure of the current manuscript build.

`AUDIT_BUNDLE_SHA256.json` records the included file contents before ZIP packaging. It excludes itself.
