# Paper U: research-closure results

**Audit reference date:** 29 September 2026  
**Verdict:** READY ONLY AS A SHORT SYNTHESIS/CORRECTION NOTE

## Start here

Read `PAPER_U_RESEARCH_CLOSURE_REPORT.md` for the decision and the explicit answers to all eleven closure questions. The revised manuscript is the eight-page `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.pdf`; its editable source and bibliography are adjacent. The narrowed contribution is a synthesis and correction, with an exact adaptive stabilizer index and normality criterion as the strongest mathematical sharpening. No theorem is certified original, and this package is not an immediate-submission clearance.

## Package guide

| File or directory | Purpose |
|---|---|
| `PAPER_U_RESEARCH_CLOSURE_REPORT.md` | Decision, major findings, disposition, eleven answers and remaining limitations |
| `PAPER_U_THEOREM_LEDGER.md` | 52 original-draft claim entries and 16 revision/study entries, with proof status and attribution |
| `PAPER_U_PRIORITY_AND_LITERATURE_MAP.md` | Theorem-level overlaps, chronology, recent work, source links and access grades |
| `PAPER_U_MATTE_BLANCO_SOURCE_AUDIT.md` | Seven interpretive themes, exact printed-page locators and source-access caveats |
| `PAPER_U_GENERALIZATION_AND_STRENGTHENING_STUDY.md` | Proofs, generalizations, counterexamples, adaptive frontiers and bounded noisy-channel study |
| `PAPER_U_ADVERSARIAL_ATTACKS.md` | Explicit attacks on correctness, contribution, interpretation, p-adics, scope and priority |
| `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.tex` | Authoritative revised manuscript source |
| `paper_u_refs_v0.2.bib` | Revised BibLaTeX bibliography |
| `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.pdf` | Compiled and visually checked manuscript |
| `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.bbl` | Generated bibliography cache; rebuild from the `.bib` with Biber |
| `scripts/` | Standard-library finite checks and LaTeX build script |
| `evidence/` | Actual JSON/CSV results, reproduction log, build log and QA report |
| `HANDOFF_TO_REVIEW_GATE.md` | Exact surviving contract and priority questions for independent reviewers |
| `NEXT_THREAD_REVIEW_PROMPT.md` | Ready-to-use prompt for the next review thread |
| `inputs/` | Unmodified uploaded package and task brief for historical comparison |
| `MANIFEST_SHA256.json` | SHA-256 hashes of package files, excluding the manifest itself |

## Reproduce the checks

From this directory, with Python 3.10 or later:

```sh
python scripts/verify_paper_u.py --out evidence_rerun
```

The script has no third-party Python or network dependency. Compare its JSON and two CSVs against `evidence/`. The final verification was independently re-executed within this session, and all three output files were byte-identical. This is a fresh execution of the same checking program, not an independently authored second implementation. Exact arithmetic is used for the finite metric checks; entropy comparisons use stated floating-point tolerances. These are bounded regression tests, not substitutes for the infinite proofs.

## Rebuild the manuscript

Install a TeX distribution providing pdfLaTeX, BibLaTeX, Biber, Latin Modern and the usual AMS/geometry/hyperref packages. Then run:

```sh
bash scripts/build_manuscript.sh
```

On Windows, the same four build steps can be run in a terminal with the TeX tools on its PATH: pdfLaTeX, Biber, pdfLaTeX, pdfLaTeX, using the manuscript basename. The included PDF does not require a TeX installation to read.

## Next independent review

Use `NEXT_THREAD_REVIEW_PROMPT.md` with this complete ZIP. Review v0.2 as a **short synthesis/correction note**, not as a pre-certified original research paper. A fresh referee should focus on the exact adaptive normality criterion, source attribution and the constrained psychological interpretation. The final publication-readiness scorecard was deliberately not performed during this research-closure phase.

## Source and provenance boundaries

The uploaded original bundle is preserved unchanged, including its user-supplied historical thesis. No externally retrieved full book scans or font files are redistributed. External sources are referenced in the literature map and bibliography. Primary Matte-Blanco passages were checked in existing OCR with printed-page markers, not collated against the corresponding original page images. Some relevant cognitive sources were available only at abstract, metadata or contents level. These limitations are recorded individually in the source map.

The specialist and hostile-review perspectives were conducted by one model. No independent human reviewers were recruited, and no empirical psychological validation was performed.
