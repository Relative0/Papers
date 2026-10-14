FINITE-JET SIGN RIGIDITY: 13 OCTOBER 2026 REVISION

Current manuscript:
  MANUSCRIPT/finite_jet_sign_laws_REVISED_2026-10-13.pdf
  MANUSCRIPT/finite_jet_sign_laws_REVISED_2026-10-13.tex

This 18-page revision integrates the useful results of the representational-limits
research branch into the September 27 final manuscript after adversarial review.
The prior manuscript was 14 pages. Its package remains intact in the collection.

Read REVIEW/REASSESSMENT_AND_CHANGE_LOG.txt for the publication judgment, changes,
proof audit, primary references, and remaining review limitations. The additions
are in Section 7 and Sections 8.3--8.4; the introduction, abstract, conclusion,
and bibliography have been updated accordingly.

Status: revised author-review candidate. An independent review on 13 October found no central mathematical error and recommended minor revision. Both requested scope clarifications were applied on 14 October. The September review verdict remains specific to that earlier version; no historical firstness is claimed.

Checks completed:
  - 24 existing theorem/lemma/corollary/proof blocks retained verbatim.
  - 41 labels and 18 bibliography entries checked; no unresolved references.
  - Existing diagnostic script: 23,962 exact rational and 32 floating assertions.
  - Four local pdflatex passes; final log has no LaTeX or box warnings.
  - All 18 pages rendered and checked in contact sheets; new mathematical pages
    12--14 and 16 also inspected individually.

Build from MANUSCRIPT with an existing LaTeX installation:
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error finite_jet_sign_laws_REVISED_2026-10-13.tex
Run twice to resolve references. The bibliography is embedded; no external files
are required. The QA log records the successful local MiKTeX build. The built-in
Codex compiler failed before reading the source because it could not find its
standard runtime directories. No new TeX installation or plugin was installed.

Run the standard-library diagnostics with Python:
  python QA/verify_candidates.py
This rewrites QA/verification_results.json, including interpreter provenance.
The finite checks supplement the mathematical arguments, not replace them.

PROVENANCE contains hashes of the 22 files in the earlier reviewed package and
copies of the three collection navigation files before this revision. The
package manifest records delivered bytes; it excludes itself.

Next before submission: author/proof review of the additions, then target-venue
formatting and author metadata. No publishing or submission was performed.
