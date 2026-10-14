# Reproduce the checks and manuscript

Use Python 3.10 or later for the standard-library checks. From the package root:

```powershell
python .\03_EVIDENCE_AND_REPRODUCIBILITY\verify_paper_u.py --out .\rerun_original
python .\02_INDEPENDENT_REVIEW\tree_review\check_mixed_ternary.py --out .\rerun_independent
```

Compare the first run with `03_EVIDENCE_AND_REPRODUCIBILITY/supplied_rerun/` and the second with `02_INDEPENDENT_REVIEW/tree_review/mixed_ternary_results.json`. JSON newline bytes may vary by operating system; compare parsed values as well as hashes. CSV byte identity was observed for the current run. Output folders above are new convenience locations, so canonical evidence is not overwritten.

For the manuscript, install/use pdfLaTeX and Biber, then run:

```powershell
.\03_EVIDENCE_AND_REPRODUCIBILITY\build_manuscript.ps1
```

On a POSIX system:

```sh
sh 03_EVIDENCE_AND_REPRODUCIBILITY/build_manuscript.sh
```

The PowerShell builder was tested; the POSIX equivalent was not run on this Windows host. Both use the actual manuscript folder and copy the small supplied logreq dependency into a separate build folder. They write the rebuilt PDF and `.bbl` back beside the TeX. To preserve the exact delivered PDF bytes, work in a copy of the package. PDF timestamps and TeX-version differences can change output hashes without changing content.

The original source material, research-closure findings, original manifests and older code are all recoverable by extracting `04_PRIOR_TRANSFER/PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29.zip`. They are historical inputs; v0.3 and the new independent review are the current state.
