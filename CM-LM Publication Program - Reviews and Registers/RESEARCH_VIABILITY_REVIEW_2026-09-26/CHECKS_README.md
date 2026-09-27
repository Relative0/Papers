# Fresh checks

Run `python -X utf8 spot_checks.py` in a writable copy of this directory. The script uses only the Python standard library and writes `spot_check_results.json` next to itself. It imports no manuscript implementation. A rerun changes elapsed time and hence the results-file hash; regenerate a manifest in that copy if needed. The delivered manifest describes the delivered snapshot.

The script checks finite instances only. Z/4 global assignments are enumerated directly, independently of the Smith criterion. Unordered local bases suffice because ordering only relabels outcomes. The poset cover check ranges over naturally labelled transitive orders Q contained in P through four vertices. Homology is computed over F2 and is not generally a homotopy test. Polynomial evaluation ranks do not establish circuit reachability. Guard checks are interior witnesses, not a proof of all region boundaries. Zero-divisor/idempotent checks do not certify every group classification.

No performance benchmark, full six-vertex minimality enumeration, complete phase-unitary enumeration or exhaustive historical archive replay was run in this assessment.
