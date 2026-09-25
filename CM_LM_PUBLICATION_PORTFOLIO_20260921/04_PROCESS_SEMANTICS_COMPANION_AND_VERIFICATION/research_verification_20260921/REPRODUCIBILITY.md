# Reproduction and verification

Research snapshot: 21 September 2026. Python checks use Python 3.10.11. The new mathematical kernel and unit tests need only the standard library. The unchanged canonical audit suite additionally needs its existing NumPy/pytest environment. No virtual environment was present at the workspace root; the installed Python was used. PDF source extraction used the bundled runtime's pypdf; it is not part of the mathematical proof.

## Exact commands

From the Paper-Workbench root:

```powershell
python -B output\process_semantics_research_20260921\code\run_verification.py
python -B output\process_semantics_research_20260921\code\finalize_release.py
```

The first command records exact argv, working directory, exit status and timings in data/run_record.json. Raw stdout/stderr for each stage are retained in logs/. It runs the new exhaustive checker, ten new regression tests, the 31-test canonical audit suite, and only the resolved-disposal witness from a byte-identical copy of the previous review checker. It does not claim to rerun that earlier review's entire nonchain-ring campaign. Source hashes are checked again at the end.

To run only the portable new checks after relocating the folder:

```powershell
python -B code\verify_semantics.py
python -B code\test_semantics.py
```

The combined runner and provenance collector intentionally retain the original Windows source paths. They require those source trees; the portable new checks do not. code/prior_review_checks.py is an unchanged copy of the earlier review source, with provenance in data/source_inventory.json. Its selected function has no external writes; the wrapper writes results in this new folder.

## Inputs and finite universes

There are no random seeds because no random sampling is used in the new checker. Scalars 0..15 are four-bit polynomials, bit j the coefficient of u^j; multiplication truncates at u^4. Matrices are row-major four-tuples. Zero Smith factors use exponent 4.

* All 16^4=65,536 matrices are checked against an independently computed binary rank.
* All 192^2=36,864 primitive-vector pairs have primitive balanced tensor.
* All 24 projective rows and their 192 unordered complementary bases are enumerated.
* All 15 Smith representatives, including zero, and 24^2 row pairs give 8,640 exact Frobenius-block contraction checks.
* All 65,536 filters on both sides of each of 15 representatives give 1,966,080 products. Class-graph transitive closure checks all 225 class pairs. Zero is included for algebraic verification but excluded as a successful preparation.
* All four ring automorphisms are verified on 256 scalar products each. Composing them with all 24,576 GL_2(A) matrices constructs 98,304 distinct normalizer matrices. The upper bound is analytic, not an enumeration of GL(8,2).
* All 15 Smith types and copy counts 1..4 give 60 unit-entry-count checks. The arbitrary-copy theorem is proved separately.
* The inherited resolved-disposal example is checked by full binary matrix multiplication. All coefficient outcomes are retained in its raw witness output, distinguishing selected and forgotten outcomes.

The unit suite checks scalar multiplication against polynomial convolution, tensor and conditioning counterexamples, rank collapse, nonseparability of the Frobenius map, unit detectability, complete binary instruments with a reference, and a small independent matrix-span check.

## LaTeX check

From P03_STUB:

```powershell
pdflatex -draftmode -interaction=nonstopmode -halt-on-error -disable-installer -output-directory=build main.tex
bibtex build/main
pdflatex -draftmode -interaction=nonstopmode -halt-on-error -disable-installer -output-directory=build main.tex
pdflatex -draftmode -interaction=nonstopmode -halt-on-error -disable-installer -output-directory=build main.tex
```

MiKTeX 24.1/pdfTeX 1.40.25 and BibTeX 0.99d completed successfully. The final log contains no undefined citations, unresolved references, LaTeX errors or overfull boxes. The expected pdfdraftmode warning says no PDF is written. No new PDF or visual-layout certification is claimed. The existing nine-page technical companion is preserved separately.

## Provenance and limitations

The supplied canonical manifest has 154/163 matches and nine existing mismatches. Both expected and actual hashes are retained; none of its entries is missing. The prior 20 September STATUS.md reports the same discrepancy set. Canonical and Downloads standalone TeX are byte-identical. A final run verified 122 tracked source files unchanged. No old data or manifest was regenerated.

This workspace is not a Git repository; git status --short and git diff --stat were attempted and returned that restriction. Release files are tracked by ARTIFACT_INVENTORY.txt and MANIFEST_SHA256.txt. The manifest covers every release file except itself. Empty scratch directories and any bytecode caches are not release artifacts. The copy script uses this exact inventory and refuses an existing destination, protecting the previous research.

Initial development checks caught a rectangular-transpose width error in the new encoding checker; it was fixed before final verification. Initial PDF text output hit Windows console encoding and succeeded with UTF-8. Initial MiKTeX/BibTeX checks were blocked from their user configuration directories by the workspace sandbox; the same checks succeeded with the tool's approved elevated access, with package installation disabled for LaTeX. These are tooling/development corrections, not a hidden proof failure.

No independent human review, formal proof certification, exhaustive citation-index coverage, paid source access or publication is claimed. Failed/full-text-inaccessible routes are marked in the literature and search ledgers.
