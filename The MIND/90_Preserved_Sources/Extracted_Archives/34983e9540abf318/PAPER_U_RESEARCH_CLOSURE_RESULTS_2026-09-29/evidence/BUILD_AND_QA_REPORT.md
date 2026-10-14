# Build, reproduction and visual QA

**Package audit reference date:** 29 September 2026

## Executed build

The manuscript was built with pdfLaTeX, Biber, and two further pdfLaTeX passes. The final combined output is preserved in `build_final.log`. Searching that final log found no `Warning`, `Overfull`, `Underfull`, or `Error` diagnostics. In particular, there are no unresolved citation/reference warnings in the final build.

The final PDF has **8 US-letter pages**. It is not encrypted. Its source and bibliography were checked for accidental control characters; none were found. The bibliography uses Biber, not BibTeX.

## Executed visual inspection

All eight final pages were rendered with `pdftoppm` and inspected in two contact sheets. The dense quotient-proof page and the final references page were additionally inspected at individual-page scale. No clipped equations, overlaps, broken glyphs, black squares, or spillover bibliography page were observed. The last revision removed an overfull inline entropy formula by giving it display space and adjusted reference spacing to keep the bibliography on one page. The rendered final document uses a restrained mathematical-article layout.

The contact sheets and intermediate render images are working QA artifacts, not source figures, and are not needed to reproduce the mathematics. They are not included in the final package.

## Executed finite-test rerun

The final `scripts/verify_paper_u.py` was run again in a separate output directory. All checks passed. The following three files matched the original recorded results byte for byte:

- `verification_results.json`
- `frontier_groups_m2_d3.csv`
- `frontier_groups_m3_d2.csv`

The rerun's console output is preserved as `verification_rerun.log`. This rerun used the same verification implementation; it is not a second independently written checker. Its evidence remains finite: 258 comparable frontier pairs across the two small group models, along with the metric, lattice, sample-separation, entropy and counterexample checks recorded in the JSON.

## Tool versions

- Python 3.13.5, GCC 14.2.0 build
- pdfTeX 3.141592653-2.6-1.40.26, TeX Live 2025/dev/Debian
- Biber 2.20
- pdftoppm 25.06.0

## Deliberate limitations

This is mathematical/source/layout QA, not PDF accessibility certification or a journal-specific production check. The PDF is not tagged. A clean build and passing finite tests do not establish novelty, empirical validity, or a publication-readiness verdict. Those questions are addressed separately in the closure report and reserved independent review prompt.
