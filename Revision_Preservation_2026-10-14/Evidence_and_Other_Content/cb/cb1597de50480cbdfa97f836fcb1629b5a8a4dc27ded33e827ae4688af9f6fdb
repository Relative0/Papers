# Boolean modal capability and dependency laboratory

Research dossier and independently implemented exact tests, 18 September 2026.

## Start here

- `reports/CAPABILITY_REPORT.md`: complete A-J research report, model contracts, capability/dependency tables, algorithm suite, resource hierarchy, proofs, prior-art matrix and paper recommendation.
- `reports/FORMAL_THEOREMS.md`: extracted 21-theorem set. The model contracts in the main report remain part of the statements.
- `reports/COMPUTATIONAL_LEDGER.md`: exact finite domains, algorithms, timings and output filenames.
- `data/capability_map.csv`, `data/dependency_matrix.csv`, `data/dependency_ablations.csv`, `data/prior_art_matrix.csv`: machine-readable report tables; matching JSON files are included.
- `data/resource_hierarchy.json` and `reports/resource_hierarchy.dot`: explicitly model-relative implications and counterexamples.
- `data/source_comparison.json`: all 65,536 encoded resources and associated classifications cross-checked against fresh supplied audit outputs.

## Reproduce

Python 3.10 or later is required. The delivered run used Python 3.13.5 and SymPy 1.14.0.

```bash
python -m pip install -r requirements.txt
python code/run_all.py
```

The command overwrites independent outputs and logs, regenerates tables and validates matched source comparisons. It does not rerun the supplied historical suite. The independent code imports no supplied implementation. All arithmetic is exact; SymPy is used only for a rational probability certificate. There is no random search or network dependency during a run. A failed assertion or timeout returns nonzero.

The last complete independent run is recorded in `data/run_summary.json`. Wall times are environment-specific and are not speedup benchmarks. Re-running changes timings and the artifact manifest will then no longer describe the modified files.

## Encoding and contracts

An A element is an integer 0..15 whose bit j is the coefficient of u^j, with u^4=0. This is not the historical R-power encoding. R=1+u has encoding 3; z=R^2 has encoding 5. The u-to-R change of basis has columns 1,3,5,15. Binary matrix rows are packed integers, with input bit j represented by bit j of a row.

F is ordinary finite-field modal theory. R names the rotation algebra, not a complete operational theory. S uses a shared A-module tensor. L uses literal independent F2 tensors, with either full field-linear or explicitly restricted A-linear/coarse operations. LM is the symbolic Boolean formula layer. None of these models is silently substituted for another.

Exact modal correctness means every possible outcome is correct. Full-support inspection, free truth-table access and postselection on a merely possible successful event are not allowed query readouts.

## Main conclusions

Finite-field tensor algebra already supports Bell support contextuality, no cloning, exact teleportation and dense coding. Zero divisors and CM rotation are not required for those existence results. The distinctive restrictions introduce valuation/Smith invariants, a logical-but-not-strong stratum and a separation between dense coding and universal teleportation for nonprimitive shared resources.

For a d-by-d chain-ring resource with lowest Smith multiplicity h, the exact shared invertible-orbit block codebook has d*h messages. Universal exact teleportation requires an invertible resource. In characteristic-two linear query models, Deutsch and Deutsch-Jozsa have no exact one-query algorithm and exact Bernstein-Vazirani requires n queries. Genuine A-module kickback does not supply an invertible Boolean Fourier transform. A known one-query modal UNIQUE-SAT circuit is reproduced as a positive control.

At most two binary basis measurements per site always admit a global assignment in the stated residue-F2 contracts. Thus the three-setting modal GHZ witness is not the conventional two-setting GHZ pattern.

## Limitations and provenance

The supplied archives and the primary manuscript text were read before conclusions were drawn. Paper B was read as complete Library text; no raw PDF is included. The entire historical runner and one supplied restriction sweep timed out. Completed supplied model/protocol stages and review extensions are separately identified in `provenance/`. Their old aggregate test totals are not counted as fresh.

The report does not certify novelty, a full operational completion for nonprimitive shared states, an efficient simulator for every native circuit, optimal multi-query Deutsch-Jozsa complexity or all-size Simon bounds. Mathematical proofs are provided but have not been checked in a formal proof assistant.

`MANIFEST_SHA256.txt` hashes the delivered files. `data/input_archives.json` identifies the user's three source archives.
