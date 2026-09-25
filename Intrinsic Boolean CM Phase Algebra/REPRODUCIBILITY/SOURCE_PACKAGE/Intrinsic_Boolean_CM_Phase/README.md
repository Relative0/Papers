# Intrinsic Boolean Phase Algebra of Correspondence Matrices

Research draft II, version 1.0, 17 September 2026. Prepared for Brian Droncheff.

This package consolidates the intrinsic Boolean branch of the CM exploration.
It is an AI-assisted mathematical research draft, not peer reviewed and not a
claim of new physical laws, a quantum device, or a computational speedup.

## Start here

Read `paper.pdf`. Sections 2-4 define the objects and their different products.
Sections 6-9 explain intrinsic unitaries, reversible shears, kickback, and the
phase-to-ANF transform. Section 10 proves the shared-tag interaction bound and
two ways to retain an AND interaction. Section 11 gives the local CM-to-ANF
compiler. Sections 12-14 cover prior work, applications, and falsifiable tests.
Appendices contain the full scalar classification, verification scope, and
correction ledger.

## Reproduce the mathematical checks

Python 3.10+ and NumPy are required. The execution retained here used Python
3.13.5 and NumPy 2.3.5; other compatible versions have not all been tested.
From the extracted directory:

```text
python -m pip install -r requirements.txt
python code/verify_intrinsic.py data
python code/build_tables.py
python code/check_report.py
```

The first script overwrites the generated files in `data/`. It makes no network,
cloud, account, or repository calls. Package installation, when needed, is a
separate user action. The randomized regression tests use seed 17092026.
The runtime field and environment string naturally vary by machine.

`verify_intrinsic.py` compares independent scalar multiplications, checks ring
identities, enumerates the complete 65,536-operator space, independently checks
binary rank, tests every truth function through four variables, and executes
the reported compiler and interaction regressions. It finishes with
`ALL CHECKS PASSED` only if its assertions hold.

`check_report.py` does not import the experiment implementation. It reaggregates
the CSV inventory, checks all 65,536 unitary flags by direct 8-by-8 binary
orthogonality, checks the report totals, and checks the recorded script hash.
Its results are stored in `data/report_check.json`. This is an independent
implementation check within this work, not external third-party replication.

## Rebuild the PDF

Use a TeX distribution with latexmk, pdfLaTeX, Biber, biblatex, newtx, and tikz-cd:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```

The working LaTeX source uses `references.bib`, `scalar_table.tex`, and
`audit_table.tex`. A separate downloadable standalone `.tex` edition embeds its
bibliography and both tables, so it can be compiled without this directory tree.
The generated tables should be refreshed with `build_tables.py` after a rerun.

## Data files

- `verification.json`: authoritative execution summary, environment, seed,
  and verification-script hash.
- `report_check.json`: independent aggregation and orthogonality check.
- `operators.csv`: all 65,536 four-entry CM-ring matrices, including failures;
  invertibility, rank, intrinsic unitary, involution, Hamming, and fringe flags.
- `elements.csv`: all 16 scalar CMs, inverses, orders, nilpotency, and self-products.
- `star_table.csv`: complete convolution table; `interference_0.csv` through
  `interference_3.csv`: all pairwise XOR/relative-rotation tables.
- `transformations.csv` and `division.csv`: transformation and division checks.
- `shear_fringe.csv`: the reversible-shear four-phase detector profile.
- `DJ_n2_examples.csv`: scalar-detector examples under the two-bit promise.
- `phase_anf_exhaustive.csv`, `affine_hidden_strings.csv`, and
  `marked_pattern_decoding.csv`: algorithm checks with exact mismatch counts.
- `synthetic_folding_operations.csv`: deterministic operation counts for a
  deliberately simple sparse backend, not state-of-the-art timing comparisons.
- `nilpotent_interaction_tests.csv`: finite regressions of a theorem proved in
  the paper, not a substitute for that proof.

## Conventions that matter

Original CM rows and columns are indexed by truth values 1,0. Phase coordinates
are clockwise: a0,a1,a2,a3 represent [[a0,a1],[a3,a2]]. Storage codes are
`a0 + 2*a1 + 4*a2 + 8*a3`; codes are not numerical amplitudes.
Computational-register basis vectors use ascending bitstrings. A register
coefficient is one CM-ring element. All update arithmetic in the intrinsic
model is AND/XOR and fixed rewiring; the support quotient can be implemented
with Boolean NOT, itself `1 XOR x`.

Pointwise conjunction, contracted matrix multiplication, cyclic phase
convolution, and Boolean-polynomial multiplication are different typed
operations. The added convolution is not silently attributed to the original
CM paper. Integer counts and Hamming statistics are external readouts, not
amplitudes or Born probabilities.

## Provenance and limits

The original CM manuscript and the earlier phase-count paper are referenced,
not redistributed. Third-party research is cited in `references.bib`; this
package contains no copies of those papers, no external repository clones,
no credentials, and no font files. The user's existing repository evidence is
cited at a pinned commit, not claimed as rerun by this package.

See `RESEARCH_NOTES.md` for source boundaries and the main correction record.
`MANIFEST.json` records SHA-256 hashes of the release files. Rerunning the
experiment changes environment/runtime metadata; regenerate a manifest for a
new release rather than treating it as the same frozen artifact.
