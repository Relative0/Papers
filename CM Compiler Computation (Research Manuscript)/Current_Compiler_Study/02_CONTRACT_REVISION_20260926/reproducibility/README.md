# Reproduction of the September 26 contract revision

Run from this folder with Python 3.10.11 (or a compatible environment):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip --isolated install -r requirements-checks-lock.txt
.venv\Scripts\python run_checks.py
```

This complete runner was additionally executed in a newly created virtual environment without system site packages. Direct dependencies are listed in `requirements-checks.txt`; all resolved runtime/test dependencies are pinned in `requirements-checks-lock.txt`. Bootstrap pip/setuptools versions and platform are recorded in `CLEAN_ENVIRONMENT.json`. The initial default pip invocation stalled and was cancelled; installation using pip isolated mode from public PyPI succeeded. No settings or security controls were changed. The check runner uses local files only, disables third-party pytest plugin autoload, and does not execute historical timing workers or paid services. NumPy, pytest, and requests versions are pinned in `requirements-checks.txt`; the current clean-environment result records optional packages as absent in `CHECK_RESULTS.json`. The checks require no external account.

## What is reproduced

`source/` is a 63-file import/test closure retrieved from public repository commit `0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b`. Each downloaded file was matched to its Git tree blob SHA-1 and recorded with SHA-256 in `SOURCE_SNAPSHOT.json`; files are unmodified. It includes the actual pre-freeze protocol-v3 plan. Some modules support upstream output-budget mocks; their presence does not mean that remote-worker services were used. This is a selected correctness closure, not the complete repository or historical timing execution environment.

The runner executes 90 upstream tests in `source/tests/test_cm_pair_alignment.py` and `source/tests/test_output_budget.py`, plus 33 cases in `test_contract.py`. One contract case checks 327,680 signed-frame fusion assignments over the five outer operations actually implemented by `cm_compose`. The original 1,048,576-case audit count covered all 16 abstract outer truth functions; it is a different check. The historical 116-test selection is also different and is not claimed to have been recreated.

`historical_evidence.zip` recovers 95 byte-identical members from the local portfolio reproduction supplement. It contains the corrected S1/S2 CSV, scripts, generators, metadata and historical reports, plus P14 raw rows, scripts, freezes, holdouts and amendments. Redundant superseded S2 records were not promoted into current evidence. `HISTORICAL_RECOVERY.json` maps every recovered member to its original archive path and hash, records the original ZIP hash, and verifies eight P14 freeze source/holdout hashes.

`check_historical.py` is an independent recount, reading that ZIP without extracting or running historical scripts. It checks all recovered member hashes, the 10,500 S1/S2 cases, 10,389 all-arm cases, seven-metric generic/CM equality, failure counts, fold counts and S2 medians. It recomputes all four P14 primary point estimates and their case ratios from 51,102 raw timing rows. The separate `../../03_STUDY_DESIGN_20260926/replay_p14_intervals.py` subsequently replayed all 17 archived bootstrap interval sets with the recorded 10,000-draw seed and resampling order. No historical elapsed-time observations were generated anew.

## Output records

- `TEST_STDOUT.txt`: exact selected pytest output.
- `CHECK_RESULTS.json`: command, environment, source revision, and all check results.
- `HISTORICAL_CHECKS.json`: independent raw-record recount results.
- `SOURCE_SNAPSHOT.json`: source file identity and scope.
- `HISTORICAL_RECOVERY.json`: preserved archive-member identity and freeze checks.

The manuscript's `BUILD_LOG.txt`, release manifest, and `VISUAL_QA.json` reside one directory above. Use the current runner instead of the preserved historical `check_manuscript.py`, whose old relative protocol dependency is absent from its historical folder.

## Still open

Recovery establishes the bytes used for this revision's checks. It does not prove that the public pinned commit produced the September 19 historical 116-test report or all historical timings. P14's imported compiler/dependency identity remains to be tied to its original freeze, although a compatible local runtime candidate was subsequently located and packaged under `../../03_STUDY_DESIGN_20260926/`. The narrower signed-formula primary pair-token cell was frozen and executed under protocol v4 with a negative result. A separate [natural admission/correctness gate](../../04_NATURAL_CIRCUIT_EXTENSION_20260926/README.md) and [descriptive secondary timing run](../../05_NATURAL_TIMING_20260926/README.md) now give bounded selected-cohort evidence, including one retained timing calibration failure. Full protocol-v3 circuit evidence remains unmeasured. A public archive identifier and release licensing/provenance review are still needed before a complete public artifact release. The failed primary endpoint has not been replaced.


## Supplied full-audit checks and separate commands

The later-supplied archive is stored unchanged at `../audit/CM_Publication_Audit_Evidence_2026-09-26.zip`. `check_audit.py` verifies its 21 manifest entries, runs the inspected unmodified standard-library checker in temporary space, and compares the resulting JSON exactly with the recorded audit results. `AUDIT_CHECK_RERUN.json` and `AUDIT_CHECK_STDOUT.txt` preserve the fresh execution separately. These reference-model counts are not added to the 123 implementation-test count.

From this directory, independent commands are:

```powershell
python -m pytest -p no:cacheprovider -q source/tests/test_cm_pair_alignment.py source/tests/test_output_budget.py test_contract.py
python check_historical.py
python check_audit.py
```

For the direct pytest command, set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and `PYTHONDONTWRITEBYTECODE=1` as the combined runner does, or use the clean environment. No command above performs new timing experiments. The prospective cold/warm cache policy is described in manuscript Section 7.1; these correctness checks are not cold/warm timing measurements.

The full finding-ID crosswalk is in `../FULL_AUDIT_RECONCILIATION.md`. The audit's five unmatched historical entries have all been located by hash in the companion-paper workspace; they represent four distinct contents, with one PDF listed twice. They are historical external references, not current build/runtime dependencies, and their source bytes remain in their canonical companion folder.
