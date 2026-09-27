# P02 targeted reproducibility package - 27 September 2026

This directory accompanies the revised manuscript **Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation**.

It has two evidence layers:

1. `original_evidence/` contains the recovered P02-relevant artifacts from the portfolio reproduction supplement: original JSON/CSV outputs, the reproduction envelope, the original P02 provenance records, and the previously completed Linux full-run manifest/log.
2. `reproduce_p02.py` performs a fresh P02-targeted rerun using the recovered oracle-contract checker, the independent publication-audit verifier, the recovered capability scripts, and a deterministic phase-table generator.

The recovered portfolio runner referred to a historical table generator named `complete_p02.py`; that script was not located in the supplied archives. `generate_phase_table.py` is therefore a **new reconstruction**, not a recovered historical script. It consumes `capability/data/new_phase_fourier.json` and deterministically regenerates the table used by the revised manuscript.

## Environment

Pinned package requirements are in `requirements.txt`. The recovered full-run manifest used Python 3.13.5. The fresh rerun manifest records the actual environment used for this package.

## Reproduce

From this directory:

```text
python reproduce_p02.py
```

The run writes logs and fresh outputs under `fresh_outputs/` and creates `P02_RERUN_MANIFEST.json` with SHA-256 hashes.

## Scope

The finite checks validate bounded instances, algebra identities, data generation, and implementation behavior. They do not replace the manuscript's general proofs. In particular, the 552 oracle-contract count is a bounded enumeration of degenerate oracle matrices for address-bit sizes 1 through 3 with two shared target permutations; it is not an enumeration of all algorithms.
