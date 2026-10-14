# Current compiler manuscript and archived baselines

Collection updated on 13 October 2026 at Brian's request.

- Current editable manuscript: [Current_Compiler_Study/02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.tex](Current_Compiler_Study/02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.tex).
- Current 20-page PDF: [Current_Compiler_Study/02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.pdf](Current_Compiler_Study/02_CONTRACT_REVISION_20260926/Operator_Level_CM_Compiler_Revised_Draft.pdf).
- Older main manuscript revisions: the existing dated root ZIPs, preserved unchanged.
- Newly zipped older manuscript folders: [CM_Compiler_Pre_Semantic_Addition_and_Pre_Audit_2026-10-13.zip](CM_Compiler_Pre_Semantic_Addition_and_Pre_Audit_2026-10-13.zip). It contains the pre-semantic-addition and pre-adversarial-audit `baseline/` directories, preserving their complete original paths. Those two unzipped folders were removed only after archive-member hashes were verified.

The newest `Current_Compiler_Study` stays unpacked with its study and reproducibility files. The separate `Current_Compiler_Audit_Report` is a publication-readiness report, not an older manuscript; its existing unpacked/ZIP pairing remains intact.

The ZIP also preserves the root source manifest, study bundle manifest, revision manifest and navigation files as they existed immediately before this collection update. `ARCHIVE_MEMBERS_SHA256.json` inside it records every preserved member's SHA-256 and size. To recover an old manuscript, extract the relevant baseline path into a separate working directory; avoid overwriting the current manuscript.

`SOURCE_MANIFEST_SHA256.csv` covers actual current collection files, including existing and new ZIPs, using real root-relative paths. `BUNDLE_MANIFEST_SHA256.csv` covers current study files using study-relative paths. The revision JSON covers its current files. Each excludes itself and generated Python cache files. Earlier inventories and frozen study records are preserved as historical evidence.

Verify the collection with `python build_source_manifest.py --verify`. The current semantic/manuscript diagnostic evidence remains under the two semantic supplements; no manuscript content, compiler implementation or frozen empirical data changed during this archival update.
