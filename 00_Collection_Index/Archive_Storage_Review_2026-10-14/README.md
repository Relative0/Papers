# Prepared archive storage reduction — 14 October 2026

**Implementation update:** the user clarified that ZIP packaging is not needed
provided revisions remain adequately covered in Git. The authorized amendment
therefore excludes all 289 current ZIP paths (not only the 287 in the original
proposal) while preserving their original local files and earlier Git history.
Recursive checks cover 139 distinct archives including nested packages and
5,908 distinct required contents. See `IMPLEMENTATION_RECORD.md`. The original
proposal and estimates below are retained as preparation history.

Baseline: `96d8376067d67fe05ef563abc04570d881c72b87`. This preparation does
not amend that commit, remove files from Git, delete originals or repack ZIPs.

## Concrete proposed amendment

1. Remove only the 287 ZIP paths listed in `proposed_git_exclusions.txt` from
   the latest commit's index. Leave their local files untouched and leave the
   parent commit and earlier history unchanged. Two ZIP paths already present
   in the parent retain their tracking.
2. Include the prepared `Revision_Preservation_2026-10-14` tree and these review
   records in the amended commit. That tree supplies archive-only revision
   sources/PDFs and evidence as ordinary files, with source/member/revision maps.
3. Include the prepared ignore rules for future ZIPs and the local working vault.
4. Verify all source/PDF/evidence mappings, confirm original ZIP hashes and
   verify the expected index contents before committing. Verify the resulting
   Git tree and ordinary-file preservation after committing. Do not push.

Amending changes the latest commit's identity and requires separate approval.
The initial request authorized creating commits; this storage change replaces
an existing commit. The user authorized the local preparation folder.

## Prepared protection and preservation

`local_vault_receipt.json` records 124 checksum-verified original ZIP copies
under `95_Archive_Storage_Preparation_2026-10-14/Original_Archives`, one per
distinct archive. All original ZIP files remain at their existing paths.
This is a working copy on the same disk, not an independent off-machine backup.

`git_retention_verification.json` reports PASS for 15,992 required archive
member occurrences and 5,887 distinct required contents. The prepared ordinary
files include 1,934 source/PDF paths, representing 348 archive-only distinct
source/configuration contents and 26 archive-only distinct PDFs. The other
required contents either already exist in the collections or are preserved
in the new evidence/content store. The prepared archive-only retained contents
total 3,420 distinct contents and 308,279,856 uncompressed bytes.

The preservation preview is not a compilation or runnable-package certificate.
Some unchanged dependencies stay in the original paper collections. Full
original archives remain recoverable from the vault, including their package
structure, nested ZIPs and build intermediates.

## Size estimate and later cleanup

New ZIP objects contribute 441,321,874 bytes to current Git object storage.
Of the retained archive-only contents, 480 already exist in Git history; the
remaining 2,940 individually compress to approximately 64,440,607 bytes using
zlib. Thus a rough Git-storage estimate is about 415 MB rather than today's
792 MB, before allowing for metadata, references and Git's actual delta packing.
This is an estimate, not a measured post-amendment pack size or a guaranteed
immediate reduction of local `.git` storage. Old objects can remain reachable
through reflogs or other refs. No pruning or reflog expiration is proposed.

Removing build intermediates from the original archives is not part of this
proposal: their combined compressed member size is only 3,549,627 bytes.
Repacking would change original archive checksums for a modest saving. If lean
delivery packages are later needed, create separately named derivatives while
preserving original provenance.

Keep every manuscript revision PDF, project source, bibliography, inputs,
protocol, exact-check output, raw empirical result, environment record and
checksum ledger. Review regenerable previews, temporary extraction folders,
runtime downloads and dependency binaries individually. Timing observations
and other historical outputs cannot be replaced by a later rerun.

The preparation temporarily increases local disk usage because it keeps both
originals and verified copies. Consolidating duplicate local ZIP paths could
later save 541,824,770 bytes, but requires dependency/link updates and approval
for the exact removals. It is separate from reducing Git history size.

## Files

- `archive_paths.csv`: every tracked ZIP, SHA-256, identity group and proposed action.
- `proposed_git_exclusions.txt`: exact ZIP paths to untrack while retaining locally.
- `archive_members.csv`: complete direct-member inventory and matching tracked files.
- `archive_only_retention.csv`: required archive-only contents and their provenance.
- `storage_plan.json`: classification counts and storage measurements.
- `local_vault_receipt.json`: verified original copies and retained source/PDF previews.
- `retention_storage_estimate.json`: new-content compression estimate.
- `git_retention_verification.json`: verified source/PDF/evidence preservation.
- Python preparation scripts: idempotent copies and checks; no deletion routines.

The original inventory script requires its unchanged tracked baseline. The
prepared ignore change is intentionally a working edit; inspect the existing
reports rather than rerunning that initial baseline capture over preparation.
