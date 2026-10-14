# Collection records

These records describe the 30 September 2026 organization and the 1 October revision cleanup. The September 30 reports below are dated snapshots; use the October 1 records for paths since retired into revision ZIPs. None claims complete recovery of every historical version or certifies mathematical novelty. Start with the [workspace index](<../README.md>) or [paper crosswalk](<PAPER_CROSSWALK.md>).

| Record | Purpose |
|---|---|
| [Publication-stage scorecard](<PUBLICATION_STAGE_SCORECARD_2026-09-30.md>) | Dated, genre-specific readiness judgments based on current manuscripts and review decisions; not acceptance probabilities |
| [Folder naming guide](<PAPER_FOLDER_NAMING_2026-10-01.md>) / [workflow audit](<PAPER_FOLDER_WORKFLOW_AUDIT_2026-10-01.md>) | Current short names, document types, Paper U review grouping and path-dependent workflow checks |
| [Folder relocation map](<PAPER_FOLDER_RELOCATION_MAP_2026-10-01.jsonl>) / [pre-rename source manifest](<PAPER_FOLDER_PRENAME_SOURCE_2026-10-01.jsonl>) | Per-file original/destination paths, sizes and SHA-256 for the 18 relocated folder trees |
| [Folder retirement record](<PAPER_FOLDER_PENDING_RETIREMENT_2026-10-01.md>) / [post-retirement receipt](<PAPER_FOLDER_POST_RETIRE_VERIFICATION_2026-10-01.json>) | User-authorized retirement of the 18 old names after fresh hash checks; destination files, directories and current links rechecked |
| [Revision archive index](<REVISION_ARCHIVES.md>) / [new-archive receipt](<REVISION_ARCHIVES_2026-09-30.json>) | Current unpacked heads, distinct older revision ZIPs, source/member hashes and retained original paths |
| [October 1 cleanup verification](<OTHER_PAPERS_CLEANUP_VERIFICATION_2026-10-01.json>) / [original-to-current relocation map](<OTHER_PAPERS_RELOCATION_MAP_2026-10-01.jsonl>) | 7,070 baseline paths reconciled against unchanged locations, edited navigation or verified archive members |
| [Postcleanup source inventory](<OTHER_PAPERS_POSTCLEANUP_SOURCE_2026-10-01.jsonl>) / [duplicate locations](<OTHER_PAPERS_DUPLICATE_LOCATIONS_2026-10-01.json>) | Current file paths, sizes and SHA-256; measured matching live locations for retired revisions |
| [October 1 archive-member manifest](<OTHER_PAPERS_ARCHIVE_MEMBER_MANIFEST_2026-10-01.jsonl>) | All 508 retired source files mapped to exact ZIP members with file and archive SHA-256 |
| [October 1 directory map](<OTHER_PAPERS_FILE_BEARING_DIRECTORY_MAP_2026-10-01.jsonl>) | Retained and retired folders containing baseline files, plus verified-empty temporary folders |
| [Preservation recheck and archive feasibility](<PRESERVATION_AND_ARCHIVE_FEASIBILITY_2026-09-30.md>) / [JSON receipt](<PRESERVATION_RECHECK_2026-09-30.json>) | Fresh hash/path check and a selective-archiving decision, including one changed live report |
| [Final verification](<FINAL_VERIFICATION.md>) / [JSON](<final_verification.json>) | Preservation, archive counts, checks, remaining limits |
| [Original source manifest — JSON](<source_manifest.json>) / [CSV](<source_manifest.csv>) | Every original workspace file and named external package; original path, size, SHA-256 and organized location |
| [Original folder manifest](<folder_manifest.json>) | Every original in-scope directory; all retained at original paths |
| [Archive catalog](<archive_catalog.json>) | Every member of each unique ZIP stream, with size, CRC, SHA-256 and original ZIP locations; recursively includes nested ZIPs |
| [Archive occurrences — JSONL](<archive_occurrence_manifest.jsonl>) / [CSV](<archive_occurrence_manifest.csv>) | Every member occurrence under each original ZIP path, including repeated/nested archives, mapped to retained bytes or an intact archive member |
| [Exact duplicate groups](<duplicate_groups.json>) | SHA-256 keyed file locations and archive member locations; identity of bytes does not imply exclusive scientific ownership |
| [Organization operations](<organization_operations.json>) | Verified copies, safe extractions and relocations; each new scientific file is traceable to an original member |
| [Baseline metadata](<snapshot_metadata.json>) / [sources](<baseline_sources.json>) | Original inventory before any original was changed or relocated |
| [Paper catalog](<paper_catalog.json>) / [manuscript evidence](<current_manuscript_evidence.json>) | Reading heads, version histories, identities, abstracts, local TeX dependency checks and boundaries |
| [Checksum claims](<checksum_claims.json>) / [summary](<checksum_summary.json>) | Existing manifest claims tested independently; preserves historical disagreements |
| [Receipt checks](<receipt_verification.json>) | Recorded archive hashes/counts and original partition report hash |
| [Project checks](<project_checks.json>) | Delivered bounded verifiers run in separate retained test copies; no source package outputs overwritten |
| [Chat evidence](<chat_evidence.json>), [historical decisions](<chat_evidence_historical.json>), [MIND links](<chat_evidence_mind_links.json>) | Selected relevant user/final messages, original titles and pagination limits; not a complete export of all historical chats |
| [Chat artifact access](<chat_artifact_access.json>) | Referenced local/remote artifacts and access limits; excluded MIND paths are not called missing |
| [MIND overlap map](<mind_overlap_map.json>) | Distinguishes earlier chat-verified exact duplicates from broader reported shared lineage |
| [Website PDF mapping](<website_delivery_map.json>) | All four delivery copies match selected reading heads |
| [README links](<readme_link_checks.json>) / [inherited missing links](<inherited_broken_links.json>) | New navigation checked separately from historical links preserved verbatim |
| [Folder tree](<FOLDER_TREE.txt>) | Final workspace tree, excluding The MIND and .git contents |
| [Git before](<git_status_before.txt>) / [after](<git_status_after.txt>) / [final diff stat](<git_diff_stat_after.txt>) | Existing working-tree changes distinguished from new organization files |
| [Unresolved and inaccessible](<UNRESOLVED_AND_ACCESS.md>) | Historical hash variants, unavailable session artifacts and workflow follow-ups |

`archive_catalog.json` retains **original** archive source paths. Resolve relocated paths using `source_manifest.json`; `archive_occurrence_manifest.*` already includes current organized archive paths. A `!/` locator identifies a member inside an intact ZIP, including nested ZIPs, rather than a file that must be extracted. Archive-only retention is deliberate for older snapshots, duplicate releases and broad research evidence that is unnecessary for current reading.

`Extraction_Staging/` retains the hash-checked staging copies used for exposure. `Verification_Work/` holds independent test copies and generated outputs; it is not a manuscript home. `90_Preserved_Sources/Verified_PreMove_Copies/` contains safety copies of the 11 original root ZIPs. The October 1 cleanup retired only older loose manuscript revisions verified in ZIPs; see the relocation map.

Snapshot/audit/organization scripts are an audit trail of a **one-time** operation against the captured baseline, not a general cleanup command. Do not rerun `snapshot.py` or `organize_sources.py` over the completed collection. `reconcile_collection.py`, `verify_current_sources.py` and `build_navigation.py` operate on the saved baseline and generated records. This directory is excluded from its own original-source inventory; its generated integrity manifest excludes only itself to avoid a circular checksum.

During the September 30 collection organization, The MIND's contents were not changed. On October 1, its older manuscript revision folders were separately archived and retired; current reading heads and shared research remain unpacked. The older overlap map attributes exact MIND-side hashes to a prior project chat; the October 1 duplicate-location map derives from fresh file hashes.

Concurrent live-workflow changes are recorded in [the recovery receipt](<concurrent_baseline_recovery.json>) and [observed new live files](<observed_new_live_workflow_files.json>). The [final workspace file inventory](<final_workspace_file_inventory.json>) includes their observed hashes without attributing them to organization. The Git baseline includes the newly initialized bookkeeping directory, created before any original was moved.
