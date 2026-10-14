# ProLT master audit bundle — 24 September 2026

## Start here

Read `reports/ASTRA_MASTER_AUDIT_REPORT.md`, followed by `reports/CORRECTIONS_AND_PATCHES.md` and `reports/PAPER_SPLIT_AND_FREEZE_PLAN.md`.

The required deliverables are all in `reports/`:

- ASTRA_MASTER_AUDIT_REPORT.md
- CLAIM_AUDIT_TABLE.csv (114 rows, including all 82 named primary-note claims)
- NOVELTY_MATRIX.md
- PAPER_SPLIT_AND_FREEZE_PLAN.md
- CORRECTIONS_AND_PATCHES.md
- REPRODUCIBILITY_REPORT.md
- NEXT_RESEARCH_PROGRAM.md

Additional reports: `AUDIT_ADDITIONS_AND_PROOFS.md` gives complete proofs of six audit additions; `LITERATURE_SOURCES.md` supplies 22 bibliography/search records with access-scope limitations. The master report ends with direct answers to all fifteen requested questions.

## Source and correction status

`source_snapshot/` is extracted byte-for-byte from the supplied archive. No manuscript has been silently corrected. The v0.3 TeX is zero bytes in that archive; the readable PDF was audited. `SOURCE_MANIFEST.json` records the input archive hash and every member hash. `BUNDLE_SHA256.txt` records the delivered bundle files, excluding itself.

The principal correction is the false equality of relative observation dimension and classical poset 2-dimension. The related total-coarse-order NP-completeness proof is withdrawn, while a different general NP-completeness theorem is proved. These corrections do not invalidate the one-bit forest theorem.

## Reproduce the independent checks

Use Python 3.10 or later with assertions enabled and the dependency recorded in `verification/requirements.txt`. The audit ran Python 3.13.5; other versions were not independently tested here.

```sh
python -m pip install -r verification/requirements.txt
python verification/run_independent.py --output ./my_prolt_rerun --include-five-state
```

The wrapper copies scripts into a **new** directory and does not overwrite delivered reference outputs. The default without `--include-five-state` reruns the dimension checks, named examples, integer torsion examples, small two-bit search, chains through twelve, one-bit search through six, higher-height/edge checks, and exact named-example label minimization. The optional flag adds the completed five-state two-bit extension. No completed six-state two-bit result is claimed.

Reference outputs and original successful run logs are in `verification/`. Independent code imports none of the original supplied verifiers. New scripts share the audit's own helper routines; this is documented and is not presented as three wholly separate implementations.

The original supplied verifiers are preserved under `source_snapshot/03_VERIFICATION/`. They contain absolute `/mnt/data` dependencies and are not portable without preparing that location or editing a disposable copy. Their unchanged successful execution is recorded in `verification/original_runs/`; do not confuse the portable independent wrapper with a claim that the original packaging was portable.

## Reading the results correctly

Every finite count states its natural-labelling convention and range. A passing computation is supporting evidence, not a general proof. Formal proof-assistant verification and a complete novelty certification were not performed. The six-state two-bit timed-out attempt contributes no exhaustive coverage. Torsion examples are explicit witnesses, not globally proved minima.

The recommended active question is only the two-bit height-two collapse boundary. Standard foundations and additional speculative directions should remain frozen rather than being expanded in parallel.
