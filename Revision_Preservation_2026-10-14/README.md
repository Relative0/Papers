# Revision preservation without tracked ZIP packaging

This is a replacement for source files, revision PDFs and evidence
whose exact bytes existed only inside tracked ZIPs. Existing paper collections
remain unchanged. ZIPs are excluded from the amended current Git tree; original
local archives and verified working copies have not been deleted or modified.

- `Sources_and_PDFs/`: ordinary source/configuration files and PDFs, grouped
  by the first 16 characters of the original archive's SHA-256 and retaining
  the original archive member paths. `SOURCE_AND_PDF_INDEX.json` identifies
  their original paper/archive and revision context.
- `Evidence_and_Other_Content/`: one file per distinct SHA-256 for the
  remaining archive-only evidence, documentation, assets and runtime files.
  Hash-based filenames avoid multiple copies and accidental claims that
  different historical versions are interchangeable.
- `ARCHIVE_MEMBER_MAP.csv`: every file member of 139 distinct archives, including
  nested archives, its original name, size, SHA-256 and preservation classification.
- `CONTENT_LOCATIONS.json`: maps preserved member hashes to these retained
  files or byte-identical files already in the paper collections.
- `ARCHIVE_INDEX.json`: full archive hashes, original local paths and verified
  local working copies. Original ZIP bytes and package structure remain intact
  in that local vault, including nested archives and build intermediates.

Source/PDF copies preserve original filenames and directory relationships
for the archive-only files. They are not a claim that every source directory
is a standalone runnable or compilable package: unchanged dependencies may
remain in the original paper collection. The recovery tool rebuilds each
revision's layout from retained Git files without requiring original ZIPs.
Verify the documented environment before rebuilding. Raw historical runs, logs and result tables
are evidence; rebuilding source does not reproduce their observations exactly.

The preparation folder `95_Archive_Storage_Preparation_2026-10-14` is ignored
by Git and is on the same disk. The archive index is a retrieval record, not a
promise that that folder is present in a future clone.

## Recovery from a clone

Run `python Revision_Preservation_2026-10-14/recover_revision.py --verify-all`
to verify coverage. `PAPER_REVISION_INDEX.md` identifies the archived revisions.
Choose the full SHA-256 from `ARCHIVE_INDEX.json`, then run
`python Revision_Preservation_2026-10-14/recover_revision.py --archive SHA256 --output PATH`.
The command restores the original member paths in a separate directory and
refuses to overwrite different existing files. Nested archives become folders
ending in `.zip.contents`. Use `--restore-nested-zips` only when an original
program requires those ZIP filenames; it creates new ZIPs from retained files,
not byte-identical historical packaging. Recreated packages omit build caches.

`verify_git_coverage.py --ref HEAD` checks that every required preserved content
has an exact matching Git blob. 5,908 distinct required contents were verified
before the amendment. Build intermediates are omitted from Git recovery; no
restricted archive members were encountered. Earlier Git history remains intact.
