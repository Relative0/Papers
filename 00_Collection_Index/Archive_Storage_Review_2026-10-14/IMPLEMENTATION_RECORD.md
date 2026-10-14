# Archive replacement implementation — 14 October 2026

Authorization: the user stated that ZIPs are not needed as long as all revisions
have adequate Git coverage. This follows the prepared latest-commit amendment
proposal. The amendment replaces `96d8376067d67fe05ef563abc04570d881c72b87`
without changing its parent or any earlier history. No push is authorized.

## Included changes

- Exclude all 289 current tracked ZIP paths, listed in
  `executed_git_exclusions.txt`. Keep every original local ZIP and all 124
  checksum-verified working copies. No ZIP is deleted or repacked.
- Include revision source/PDF files, required evidence/assets/runtime contents,
  archive/member/revision maps and recovery tools as ordinary Git files.
- Check nested packages recursively: 139 distinct archive contents, 17,356
  required member occurrences and 5,908 distinct required contents. Twenty-one
  additional contents were preserved during recursive checking and validation
  of references against changed working files.
- Omit regenerable build intermediates from the recovery tree. No restricted
  archive members were encountered. Original local ZIPs retain all bytes.
- Preserve exact recovery-file bytes with a scoped `.gitattributes` rule.
- Add a root reading link and per-package source/PDF recovery index.

## Verification before amendment

- `recover_revision.py --verify-all`: PASS for all 139 archive contents and
  5,908 distinct required contents, using ordinary files without original ZIPs.
- `verify_git_coverage.py`: PASS for the staged index; all 5,908 contents have
  exact matching Git blobs, and the index contains zero ZIP paths.
- Actual directory recovery passed for the compiler pre-semantic/pre-audit
  package (20 files), Observation Refinement v0.1 (2 files), and Structural
  Computation draft v1 (9 files).
- Nested-ZIP compatibility recovery passed for a small nested package (9 files).
  This recreates packaging from retained files; it does not claim identical ZIP hashes.

Coverage checks verify files and original revision relationships, not universal
compilation or rerunning all historical experiments. Historical dependencies
and absolute paths can still need adaptation when reproducing a package.
Raw results, exact-check records, environment records and provenance are retained.

Newer finite-jet date-record edits and their QA/review outputs appeared during
this task. They are left unstaged and unchanged. Their ZIP removal paths are
included only as part of the explicitly scoped archive replacement.

Earlier ZIP blobs remain in earlier Git history. Superseded latest-commit
objects can remain locally through reflogs; no reflog expiration, pruning,
physical duplicate cleanup or forced push is performed.
