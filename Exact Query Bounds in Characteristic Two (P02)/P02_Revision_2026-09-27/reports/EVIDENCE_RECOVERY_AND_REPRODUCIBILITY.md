# Evidence recovery and reproducibility report
## P02 revision - 27 September 2026

## What the new attachments recovered

The newly supplied publication archives contain the portfolio-level `REPRODUCTION_SUPPLEMENT.zip` that was absent from the earlier standalone P02 ZIP. This materially changes the previous reproducibility assessment.

Recovered evidence includes:

- the canonical `reproduce.py` driver;
- pinned requirements;
- `REPRODUCTION_ENVELOPE.json` with environment and provenance;
- a completed Linux full-run manifest and log;
- the original P02 manuscript/provenance record;
- the P02 table provenance record;
- the original oracle-contract checker and output;
- original `new_algorithm_checks.json`;
- original `new_phase_fourier.json`;
- original `small_simon.json`;
- original `description_readout_ablation.json`;
- original `unique_sat_reproduction.csv`.

The recovered pinned environment is:

- Python 3.13.5
- NumPy 2.3.5
- SciPy 1.17.0
- SymPy 1.14.0
- pytest 9.0.2

The current execution environment matches those pinned package versions.

## Fresh P02-targeted rerun

A new targeted driver, `supplement/P02_TARGETED_RERUN_2026-09-27/reproduce_p02.py`, was created to make the P02 evidence portable without requiring the whole portfolio research tree.

It reruns:

1. the recovered oracle-contract checker;
2. the independent P02 publication-audit verifier;
3. all five recovered capability stages;
4. deterministic regeneration of the phase table from the fresh phase JSON.

The fresh run passed all four top-level stages. The generated `P02_RERUN_MANIFEST.json` records Python/platform data, stage times, output paths, file sizes, and SHA-256 hashes.

## Original-vs-fresh comparison

`SEMANTIC_COMPARISON.json` compares the recovered historical outputs with the fresh rerun.

The following JSON files are semantically identical after parsing:

- `oracle_contract_check.json`
- `new_algorithm_checks.json`
- `new_phase_fourier.json`
- `small_simon.json`
- `description_readout_ablation.json`

`unique_sat_reproduction.csv` is byte-for-byte identical.

Several JSON byte hashes differ even though parsed content is identical. The difference is serialization/line-ending level and is therefore recorded rather than hidden.

## The 552 count is now properly scoped

The recovered original checker establishes exactly what the manuscript's `552` number means:

- address-bit sizes `n = 1, 2, 3`;
- two shared target permutations;
- the degenerate interface `G_0 = G_1`;
- all corresponding Boolean truth tables in those bounded domains.

The original JSON explicitly says this is **not an enumeration of all algorithms**. The analytic unbounded observation is simply that `G_0=G_1` makes every oracle operator identical. The revised manuscript now states this scope directly.

## Historical table-generator gap and repair

The old P02 provenance refers to a historical script `complete_p02.py`. That script was **not located** in the supplied archives, even though the generated `phase_table.tex`, the source JSON, provenance record, and wider reproduction supplement were recovered.

This gap is repaired transparently rather than papered over:

- the old provenance is preserved as `original_evidence/TABLE_PROVENANCE_HISTORICAL.json`;
- a new deterministic `generate_phase_table.py` reads the package-local `new_phase_fourier.json` and regenerates `phase_table.tex`;
- the revised manuscript's `TABLE_PROVENANCE.json` records the new generator hash, input hash, output hash, fresh rerun manifest, and pointer to the historical provenance;
- the new generator explicitly says it is a reconstruction, not the missing historical script.

## Full portfolio run versus targeted rerun

The recovered supplement contains a previously completed Linux full-run manifest in which all recorded stages passed. During this revision session, the monolithic historical runner was started but exceeded the single-command execution window during a later historical stage after the independent, oracle-contract, and audit-test stages had already passed.

Rather than represent that interrupted attempt as a completed fresh full rerun, the final package distinguishes:

- **historical completed full-run evidence** (recovered manifest/log), and
- **fresh completed P02-targeted evidence** (new rerun manifest/logs).

This separation is more defensible than treating either one as the other.

## Reproducibility conclusion

The earlier score of 4.5/10 was driven mainly by a packaging failure: the standalone P02 archive referred to evidence that was not included. The new attachments recover most of that evidence, and the revision adds a self-contained P02 driver plus a transparent replacement for the missing table generator.

For the revised P02 package, reproducibility is now assessed at approximately **9.2/10**. The remaining limitation is archival rather than mathematical: the original historical `complete_p02.py` has not been recovered, and a completely fresh rerun of every unrelated portfolio stage was not necessary for P02-specific verification.
