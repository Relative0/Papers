# Build, reproduction and final visual QA

Date: 29 September 2026. Final artifact: `01_CURRENT_MANUSCRIPT/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf`.

## Build result

PASS. The Windows PowerShell builder ran pdfLaTeX, Biber, and two further pdfLaTeX passes. Final output is a nine-page Letter-size PDF with 20 resolved bibliography entries. The generated `.bbl` is supplied alongside the `.tex` and `.bib`. No final undefined-reference/citation warnings, rerun requests, overfull boxes or underfull boxes were found in the final TeX log. The PDF is a standard untagged LaTeX PDF; no accessibility tagging is claimed.

Observed tooling: MiKTeX pdfTeX 1.40.25 / MiKTeX 24.1; LaTeX2e 2023-11-01 patch 1; Biber 2.19. Biber reported an environment locale fallback from C.UTF-8 to C, then completed successfully. The rendered accented author names and bibliography were checked. This nonfatal environment warning is retained in `build_logs/biber_output.txt`.

The initial sandboxed build could not create MiKTeX's per-user cache/configuration directory. A scoped escalated local build was approved and exposed a missing `logreq.sty`. The unmodified logreq 1.0 package was then downloaded from official CTAN into this workspace, and its `.sty`/`.def` were copied to the build directory. Automatic MiKTeX package installation stayed disabled. No global package installation was performed. The original upstream ZIP and README/license are in `latex_support/`; source: https://ctan.org/pkg/logreq and https://mirrors.ctan.org/macros/latex/contrib/logreq.zip.

The final PowerShell build was executed successfully. The POSIX shell equivalent is supplied for portability but was not executed on this Windows host. It expects an already installed TeX distribution and Biber. Build logs identify the exact final passes. The new builders resolve this package's manuscript path; the prior transfer's moved shell script did not.

## Visual QA

All nine final pages were rendered with Poppler using `pdftoppm -scale-to 1600 -png`. Pages 1–8 were inspected in two contact sheets; page 9 was inspected directly. The input v0.2 PDF was also inspected before revision. No clipped equations, missing glyphs, black replacement boxes, overlapping text or unreadable bibliography entries were found. Numbered theorem/proof continuations and the continued bibliography have normal page breaks. The final page contains references 17–20; it is not a blank extra page.

The justified additions expand the original eight-page note to nine pages including references. Font size and margins were not compressed merely to preserve the old page count. Own-manuscript QA images are included in `visual_qa/`. Copyrighted external source pages are excluded from this handoff.

## Original verification suite

Executed with bundled Python 3.12.14, standard library only. All checks passed. Both generated CSVs match the earlier evidence byte-for-byte. The JSON has Windows CRLF rather than original LF, and is equal both after newline normalization and after JSON parsing. Exact hashes and comparisons are in `REPRODUCTION_RECEIPT.json`. The original verifier is supplied unchanged as `verify_paper_u.py`.

The prior input archive was safely extracted into a new task directory; all 40 entries in its SHA-256 manifest matched. The complete original ZIP is preserved byte-for-byte in `04_PRIOR_TRANSFER/`, and its hash is recorded in the receipt.

## Independent extension

The tree reviewer authored and ran `02_INDEPENDENT_REVIEW/tree_review/check_mixed_ternary.py` independently of the supplied verifier. Its log reports Python 3.10.11. Generator closure, enumerated factor stabilizers, conjugation witnesses, mixed old-cell depths, relative height zero, ternary branching and pointwise/setwise distinctions were tested. Output: PASS. The proof-dependent product composition is explicitly disclosed rather than represented as enumeration of the entire product group.

The same folder contains JSON results and the run log. No redundant rerun was performed after the unmodified tests passed. No computational claim is a proof of an infinite theorem or empirical support for a model of mind.

## Other validation

Final package assembly checks citation keys, expected files, JSON readability, source-file hashes, generated unified diffs and all archive entries. Archive hashes and integrity results are recorded in the adjacent ZIP receipt. The workspace's existing unrelated untracked folders were left untouched; no commit, push, publication or external submission was made.
