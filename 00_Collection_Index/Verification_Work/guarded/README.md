# Guarded Boolean Operator (Paper B): reviewed revision

Audit date: 28 September 2026.

## Start here

`manuscript/guarded_boolean_dispatch_revised.pdf` is the revised 14-page manuscript. Its editable LaTeX source is next to it. This is an update of the uploaded restricted-dispatch Paper B, not the separate CM/LM foundations manuscript.

`audit/REVIEW_AND_REVISION_REPORT.pdf` gives the specialist passes, two hostile passes, findings, proof ledger, before/after scorecard, and conditional submission decision. The Markdown source and machine-readable scorecard are included. All passes were conducted by the same assistant, not independently recruited external referees.

**Verdict:** conditionally ready as a focused mathematical methods/expository note, after author and venue checks. Not an unqualified new-theory or general algorithms submission. The weighted readiness assessment is 8.42/10; novelty and significance remain the limiting categories.

## New main result

For the exact four-operator model induced by real F(x,y)=x+y+xy, in the original positive magnitude coordinates, the minimum number m_d of fixed binary polynomial-sign tests of degree at most d is:

- d=1: no finite library works;
- d=2 or 3: exactly three tests;
- d>=4: exactly two tests, and both polynomials in any two-test solution must have degree at least four.

This is a promised-zero-free, fixed-library result. The implementation uses exact trichotomy for boundary rejection. Reciprocal coordinates linearize the boundaries, so the degree restriction is coordinate-dependent. Fewer sign observations are not a demonstrated runtime speedup.

## Run the exact reference dispatcher

Requirements: Python 3.10 or later. The recorded run used Python 3.13.5 on Linux. Cross-platform compatibility was not exhaustively tested. The dispatcher itself uses the standard library only.

From the extracted bundle root:

```sh
python code/guarded_dispatch.py 2 1/2 --mode coordinate
python code/guarded_dispatch.py 2 1/2 --mode quartic
python code/guarded_dispatch.py 1 1/2 --mode quartic
```

The first two commands return projection X with true-first truth vector [1,1,0,0]. The last returns BOUNDARY and no truth vector. Integers and rational strings are exact inputs. Python float inputs are deliberately rejected; the program is not a measurement-uncertainty solver.

## Reproduce the verification evidence

```sh
python -m pip install -r code/requirements.txt
python code/verify_guarded_dispatch.py --out reproduced_results
```

This uses SymPy 1.14.0 and standard-library exact rational/integer arithmetic. Six modules verify symbolic prerequisites, the rational grid and boundary cases, finite test-set equivalence, actual LM substitution, Walsh witnesses, and adversarial regressions. The output `verification_results.json` is deterministic semantic evidence. The separate `environment_and_run.json` contains versions, source hashes, and non-benchmark timings.

Compare the reproduced semantic file with `evidence/fresh_run/verification_results.json`. A second recorded run from an unrelated working directory and a relocated path containing spaces produced a byte-identical semantic file; see `evidence/portability_check.json`. This is not a formal proof assistant or a cross-platform certification. The universal lower bounds and connectedness are justified by manuscript proofs, not finite enumeration.

The original historical nonlinear script failed because of a hardcoded output directory. Only that output path was repaired for its rerun, and the parsed JSON matched the archived output. A portable replay is included:

```sh
python code/reproduce_historical.py --out historical_replay
```

This executes the supplied historical script after validating a single filename replacement. Do not use it with an unreviewed arbitrary archive. The old Walsh script's separate rerun is logged; it uses NumPy and includes a tautological LM self-comparison. Neither weakness is inherited by the new verifier.

## Rebuild the manuscript

A normal TeX Live installation with latexmk, pdflatex, Latin Modern, amsmath, amsthm, mathtools, microtype, geometry, booktabs, tabularx, enumitem, and hyperref is sufficient.

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error guarded_boolean_dispatch_revised.tex
```

Without latexmk, run pdflatex twice (and once more if labels changed). The recorded final build has no unresolved references, undefined citations, overfull boxes, or underfull boxes. The report PDF can be rebuilt using the included report LaTeX source and `audit/report_style.tex` in the same directory.

## Package map

`manuscript/`: revised PDF and LaTeX.

`audit/`: full review PDF/Markdown/LaTeX, scorecard JSON/Markdown, proof and revision crosswalk, priority search ledger, submission checklist, and source diff.

`code/`: exact rational dispatcher, deterministic verifier, historical output-path replay, and dependency requirement.

`evidence/`: fresh and relocated result files, source inventory, historical logs/comparisons, build logs, and document quality checks.

`history/`: untouched original uploaded ZIP plus its current manuscript source, retained for provenance rather than as the version to submit.

`MANIFEST_SHA256.txt`: final bundle file checksums, excluding the manifest itself.

## Author-controlled steps

Confirm the inherited byline "Brian Theory," affiliation or independent-researcher designation, contact address, venue-specific declarations and AI-assistance disclosure, and code licensing. No affiliation, email, permission, publication acceptance, external referee endorsement, or repository DOI was invented. The new code is supplied for author review; no license has been assigned without the author's authorization.

For submission, use the revised manuscript and relevant supplementary evidence, not the internal review report as if it were independent peer review.
