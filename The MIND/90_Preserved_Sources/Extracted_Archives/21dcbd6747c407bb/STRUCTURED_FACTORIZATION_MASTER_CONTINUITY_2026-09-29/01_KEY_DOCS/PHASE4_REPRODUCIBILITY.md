# Reproducibility — Phase 4

All scripts use only Python's standard library for their required validation paths. Optional PySAT support is detected at runtime by `incremental_four_corner.py` but was not available in the research environment.

Run from the package root.

## Incremental comparator validation

```bash
python code/validate_incremental.py
```

Expected summary for the frozen seed/campaign:

```text
trials: 120
total_queries: 516
failure_count: 0
```

The script rewrites `data/incremental_validation.json`.

## SDD/vtree extraction validation

```bash
python code/sdd_direct_extraction.py
```

Expected key values:

```text
functions_tested: 65535
root_cut_failures: 0
laminar_extraction_failures: 0
full_decomposable_functions: 2601
full_factorization_strictly_finer_than_t_aligned: 2376
```

It writes `data/sdd_extraction_validation.json`.

## CM/LM operator-tree validation

```bash
python code/cm_operator_tree_factor.py
```

Expected key values:

```text
essential_binary_connectives: 10
total_tested: 35210
failure_count: 0
```

The frozen campaign is exhaustive through the tested ordered 4-variable family and samples 30,000 of 140,000 5-variable instances. It writes `data/operator_tree_validation.json`.

## Incremental example

`code/incremental_four_corner.py` can export one permanent DIMACS formula and a JSON stream of cut assumptions. The frozen example is included as:

- `data/incremental_example_base.cnf`
- `data/incremental_example_queries.json`

## Interpretation warning

The clause-emission ratios in `data/incremental_amortization_sizes.json` measure how many clauses would be emitted by repeated fresh encodings relative to one controlled base encoding. They are **not wall-clock SAT speedups**. An industrial incremental CDCL benchmark remains a separate Phase-5 task.
