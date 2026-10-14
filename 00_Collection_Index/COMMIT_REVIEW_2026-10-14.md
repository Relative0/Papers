# Local commit review — 14 October 2026

Scope: preserve the pending paper-centered collection reorganization, current
manuscript revisions, research evidence, navigation and preservation records.
Embedded website repositories retain separate Git histories and are excluded
from the parent index. No push, deployment or publication was requested.

## Verification

- `verify_git_preservation.py`: PASS. All 3,317 retired tracked paths have
  matching Git blob contents in current files or preservation ZIP members.
  Text comparisons also recognize CRLF-to-LF normalization. All 289 ZIPs were
  read successfully, including 25,911 file members. See the JSON receipt.
- `verify_folder_retirement.py`, with its output redirected to a temporary
  receipt: all 18 old folders absent, no missing destinations/directories and
  no broken primary links (842 checked). Its dated October 1 hash comparison
  fails for later compiler and finite-jet revisions and guide edits; 16 files
  differ from that snapshot. The historical receipt was left intact.
- Current compiler revision `verify_manifest.py`: PASS, 109 entries.
- Compiler collection `build_source_manifest.py --verify`: FAIL because the
  later `palo_adversarial_audit_2026-10-13` folder is outside the saved inventory.
  No listed files are missing or changed. The inventory was left intact.
- Website `verify_structured_factorization_release.py`: PASS, 109 artifacts.
  The embedded website repository's staged whitespace check passed.
- The embedded `sf-site-release` documentation whitespace check passed.
- Parent whitespace diagnostics include existing CRLF/trailing-space content
  and historical artifacts. Scientific and frozen package bytes were not
  reformatted to silence those diagnostics.

Preservation ZIPs are intentionally tracked rather than globally ignored.
Python bytecode and LaTeX auxiliary files remain ignored. Large local archive
files are retained; remote hosting size limits have not been assessed because
this task is limited to local commits.

This review checks preservation and delivered integrity records; it does not
certify mathematical claims or rerun historical performance campaigns.
