# PALO / CM adversarial audit

Read `adversarial_audit.md` first, then `proposed_corrections.md` and the 73-row `claim_audit.csv`. `source_snapshot.json` records exact versions, source locators, initial completed dossier components, access limits and later unreviewed continuations. `reproduction_results.json` contains the actual bounded results and the replay-domain counterexample. `quality_checks.json` and `SHA256SUMS.txt` describe package integrity, not mathematical certification.

All outputs are confined to this folder. No original manuscript or sibling research output was changed by this audit. The live compiler source path was updated by another chat during the audit. The exact **19-page audited compiler PDF** was recovered by its original hash and retained in `audited_source_pdfs`; the newer **20-page October 13 addition** and active extraction/compilation continuations have separate coverage labels. The original three initial dossiers were all completed; this is not an audit of every later artifact.

The independent diagnostics use standard-library Python. From the project root:

```powershell
& .\.venv\Scripts\python.exe .\output\research\palo_adversarial_audit_2026-10-13\independent_checks.py
& .\.venv\Scripts\python.exe .\output\research\palo_adversarial_audit_2026-10-13\additional_checks.py
```

The first run takes roughly two minutes here; elapsed time is not a comparative benchmark. It records 12,288 exhaustive bounded identity decisions separately from 10,193 assertions. The second run records 797 assertions. Copied producer scripts and results are retained under `snapshots`, `dossier_snapshots` and immutable hash directories; all reruns performed in this task wrote within this audit folder. PDF extraction used the bundled runtime; standard-library artifact validation also used the existing project virtualenv.

`package_check.py` verifies required files, CSV/JSON structure, immutable dossier hashes, version changes and Git-state records. It deliberately reports later source hash changes without treating those new versions as audited. `snapshot_sources.py` records the initial inventory and is not a command to recreate historical versions after sources change. `refresh_dossiers.py` records new observations; it does not automatically extend proof coverage. Do not equate regenerated snapshots or large assertion counts with a new audit.

No further run is necessary to deliver the requested audit. Later theorem/manuscript extensions need their own frozen-version review; source edits, commits, publishing and paid compute remain outside this audit's authorization.
