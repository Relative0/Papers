# CM Computation: one unpacked current-study folder

**Execution update:** The cleanup was completed on 1 October 2026. The final layout has two unpacked current folders because the publication-readiness audit is a distinct report: `Current_Compiler_Study` and `Current_Compiler_Audit_Report`. This document records the initial plan; see the [completion and validation record](CM_COMPUTATION_CLEANUP_COMPLETION_2026-10-01.md) for the actual final state.

Read-only assessment on 1 October 2026. This is a cleanup plan, not a record of removal. The source-by-source SHA-256 comparison is in [CM_COMPUTATION_ZIP_COVERAGE_2026-10-01.json](CM_COMPUTATION_ZIP_COVERAGE_2026-10-01.json). It checks the 19 immediate folders under `CM Computation` against direct members of the five ZIPs beside them and the September 22 revision ZIP. All six ZIPs passed a full member CRC check. SHA-256 equality proves byte preservation, not that two papers have the same scientific role.

## What is current

There is one compiler manuscript here: **Operator-Level Boolean Computation with Correspondence Matrices**. Its current source and PDF are `02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.tex` and `.pdf`. The later evidence is in `03_STUDY_DESIGN_20260926`, `04_NATURAL_CIRCUIT_EXTENSION_20260926`, and `05_NATURAL_TIMING_20260926`. The last two studies do not establish a speedup; the negative results and limits must remain visible.

The one unpacked folder to retain is the present `CM_Compiler_Study_Artifacts_2026-09-26/CM_Compiler_Study_Artifacts_2026-09-26/`. It contains the current manuscript, all four numbered study directories, reproducibility and review guides, a bundle README, and a hash manifest. The four outer numbered directories and the two outer guides match its corresponding scientific files by SHA-256. Their differing files are generated `.pyc` bytecode only. The matching `CM_Compiler_Study_Artifacts_2026-09-26.zip` contains all 342 non-cache files from this unpacked bundle.

The similarly named **CM Structural Computation** package is a separate Draft 3 research direction, with a sibling [paper home](<../CM Structural Decomposition (Research Direction)/COLLECTION_README.md>). Its copy here is a reference copy; it is not the compiler manuscript head. The publication-audit folders are delivery evidence, not a second manuscript. `HISTORY` contains superseded and predecessor material; the viability-review folder is a review.

## Proposed disposition of every visible folder

| Folder(s) now visible in `CM Computation` | Evidence and proposed disposition |
| --- | --- |
| `CM_Compiler_Study_Artifacts_2026-09-26` | **Keep unpacked** as the single current-study folder. Its nested same-name level can be collapsed during the transition, after path checks. |
| `02_CONTRACT_REVISION_20260926`, `03_STUDY_DESIGN_20260926`, `04_NATURAL_CIRCUIT_EXTENSION_20260926`, `05_NATURAL_TIMING_20260926`, `REPRODUCIBILITY`, `REVIEWS_AND_RECOMMENDATIONS` | Retire outer copies after relinking. All 337 non-cache files across these six folders match the current-study ZIP and their corresponding files inside the kept unpacked bundle. The 88 differing bytecode files are generated caches. |
| `01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922` | Retire loose copy after relinking historical references. All 13 files match both the full-evidence ZIP and the dedicated `Revision_Archives/CM_Compiler_2026-09-22.zip`. Keep that distinct revision ZIP. |
| `CM_Compiler_Contract_Revision_2026-09-26`, `CM_Compiler_Full_Evidence_2026-09-26` | Retire loose extracted bundles. Their 96 and 144 non-cache files respectively match same-named ZIPs. Retain both ZIPs as distinct snapshots. |
| `CM_Structural_Computation_Final_Research_Package` | Retire this loose reference copy only after checking external links. Its 630 non-cache files match `CM_Structural_Computation_Three_Draft_Research_Package_2026-09-26.zip`. The sibling SC home is related but is **not** byte-for-byte the whole loose copy: 160 non-cache files in this copy are absent from the sibling loose tree, so the ZIP is necessary. |
| `build`, `evidence`, `report`, `verification` | Retire loose audit output once no audit rerun depends on these exact paths. All 20 non-cache files across them match `CM_Publication_Audit_Evidence_2026-09-26.zip`. Keep the audit ZIP. |
| `HISTORY` | **Do not retire merely on same-directory ZIP coverage.** Only 6 of its 38 non-cache files occur in the five adjacent ZIPs. All 38 match the preserved original [CM Computation.zip](<../90_Preserved_Sources/Former_Root_ZIPs/CM Computation.zip>), but it also holds two original historical ZIPs. Make a distinct history ZIP with a verified manifest, retain those original ZIP bytes, then relink history references before retiring the loose folder. |
| `RESEARCH_VIABILITY_REVIEW_2026-09-26` | Its three files are absent from adjacent ZIPs but match the preserved original root ZIP. Give the review its own verified ZIP or include it explicitly in a labeled historical-review ZIP before retiring it. |
| `Revision_Archives` | Retain the September 22 ZIP; move that ZIP to the `CM Computation` root after a hash check if the aim is literally one top-level folder. The one ZIP is not inside another adjacent ZIP. |
| `__pycache__` | Generated cache; not a research artifact. Remove only as part of approved cleanup. |

The six adjacent ZIPs now total five at the root plus one in `Revision_Archives`. All 1,624 non-cache files in the 19 immediate folders are accounted for: 1,588 have a SHA-256 match in an adjacent ZIP; the other 36 are 32 in `HISTORY`, three in the viability review, and the distinct revision ZIP itself. The first 35 also match the preserved original root ZIP. This does **not** imply every loose folder is safe to remove yet; scripts and guides still name their current paths.

## Target layout

```text
CM Computation/
  COLLECTION_README.md                 # updated navigation and provenance
  Current_Compiler_Study/              # the sole unpacked artifact folder
    README_BUNDLE.md
    BUNDLE_MANIFEST_SHA256.csv
    02_CONTRACT_REVISION_20260926/
    03_STUDY_DESIGN_20260926/
    04_NATURAL_CIRCUIT_EXTENSION_20260926/
    05_NATURAL_TIMING_20260926/
    REPRODUCIBILITY/
    REVIEWS_AND_RECOMMENDATIONS/
  CM_Compiler_Study_Artifacts_2026-09-26.zip
  CM_Compiler_Contract_Revision_2026-09-26.zip
  CM_Compiler_Full_Evidence_2026-09-26.zip
  CM_Compiler_2026-09-22.zip
  CM_Compiler_History_2026-10-01.zip    # to create and verify
  CM_Compiler_Viability_Review_2026-10-01.zip # to create and verify
  CM_Publication_Audit_Evidence_2026-09-26.zip
  CM_Structural_Computation_Three_Draft_Research_Package_2026-09-26.zip
  [other small provenance files kept or linked from COLLECTION_README.md]
```

Keep all five existing root ZIPs, the dedicated September 22 ZIP, the original historical ZIPs, and the original preserved root ZIP. The current-study ZIP is a frozen counterpart to the unpacked current folder, not a second editing location. The source manifest and ZIP checksum file remain historical evidence; do not silently rewrite their original-path claims.

## Transition gates before removing any loose folder

1. Record a fresh source manifest with original path, size and SHA-256. Create and CRC/hash-check the two missing historical/review ZIPs; include the original historical ZIPs as bytes, and map each retired path to an archive member or kept live path. Verify the copied current folder before relocating an original.
2. Update `CM Computation/COLLECTION_README.md`, `README_FIRST.md`, `CANONICAL_REFERENCES.md`, `CLAIMS_AND_UNIQUENESS.md`, root `README.md`, the paper crosswalk, and affected local READMEs to navigate the single kept folder or labeled ZIPs. Preserve the old manifests as historical snapshots and add a separate relocation map.
3. Update and test `publication_audit_2026-09-30/build_release.py`: it currently bundles outer `01`–`05`, `report`, `evidence`, and `verification`, and reads the outer `02` PDF. Preserve its release contents from the new current folder and appropriate ZIPs, or freeze the script as a historical recipe with a tested new recipe. Scan other project scripts and links for outer-path assumptions.
4. Perform a dry-run removal list. Recheck archive SHA-256, ZIP CRC, a one-to-one reconciliation for every non-cache file, README links, relevant paper/release checks, and `git status --short` / `git diff --stat`. Only then remove the specifically approved redundant loose directories. Leave The MIND and the sibling SC home unchanged.

No folders were removed in this assessment. The earlier preservation instruction explicitly forbade deleting originals, and this request asks for a plan. The final removal is a separate, concrete step after these gates.
