# Provenance and verification index

Start with [The MIND index](../README.md), [THEME_CROSSWALK.md](THEME_CROSSWALK.md), and [UNRESOLVED_AND_ACCESS.md](UNRESOLVED_AND_ACCESS.md). [FINAL_VERIFICATION.md](FINAL_VERIFICATION.md) is the dated September 30 snapshot; its former loose manuscript-version paths were archived on October 1. Use the [revision receipt](../../00_Collection_Index/OTHER_PAPERS_REVISION_ARCHIVES_2026-10-01.json) and [source relocation map](../../00_Collection_Index/OTHER_PAPERS_RELOCATION_MAP_2026-10-01.jsonl) for current locations.

The [collection records ZIP](MIND_Collection_Records_2026-09-30.zip) contains the four requested entry files and their supporting manifests, including the [next-agent theme-analysis brief](NEXT_AGENT_ORIGINAL_THEMES_ANALYSIS_PROMPT.md). The original fresh Paper U referee folder and ZIP were found on 30 September 2026; `Before_Fresh_Referee_Restore/` preserves the earlier index state for comparison.

Machine-readable deliverables:
- `source_manifest.json` / `.csv`: each original filesystem source, size, SHA-256, organized and preserved locations, disposition and reason.
- `original_directory_map.json`: every original The MIND directory, including cache/empty directories, mapped to preserved location.
- `archive_members_final.json`: each canonical ZIP member, hash, extracted location and organized location.
- `archive_occurrence_manifest.json`: source-specific member rows for every original ZIP occurrence and nested ZIP; identical ZIPs expand against the verified canonical payload.
- `linked_related_archive_members.json`: members of peripheral publication ZIPs left in place.
- `duplicate_groups.json`: hashes mapped to all original source paths, archive occurrences and current collection locations.
- `manuscript_version_catalog.json`: distinct manuscript TeX byte versions and provenance.
- `final_content_inventory.json`: all delivered scientific/source/copy files in the collection.
- `final_verification.json`: reconciliation counts and issues.
- `reference_register_final.json`: named referenced packages, their sources and availability.
- `paper_theme_crosswalk.json`: evidence for classification.

`chat_evidence/` retains retrieved user messages and final responses from ten relevant chats; these are historical data, not new instructions. Pre-move inventories, copy checks, receipts and relocation plan are retained. Scripts here document the organization, but are **not idempotent rerun commands**: they intentionally refuse output overwrites and reference the original layout. Do not rerun them against the finished collection.

The old `staging` paths in pre-move audit records refer to what is now `../90_Preserved_Sources/Extracted_Archives`. Use `archive_members_final.json` for current paths. `checksum_verification_final.json` plus `embedded_hash_verification.json` supersede the preliminary checksum diagnostic.

`audit_metadata_checksums.json` was sealed before the newly found fresh Paper U review was added. Use `audit_metadata_checksums_2026-09-30.json` for the updated metadata.
