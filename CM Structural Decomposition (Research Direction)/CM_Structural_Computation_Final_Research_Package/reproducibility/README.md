# Reproducibility guide

## Exact correctness replay

Run from the package directory:

```sh
python reproducibility/run_correctness.py --output replay_receipt_new.json
```

The runner copies current code, tests, dataset and recovered legacy source to a fresh temporary directory, removes inherited PYTHONPATH, and executes eight separate Python processes. It regenerates the dataset, runs core/exhaustive matrix/field/legacy/persistence/scope-limit suites, and reproduces six old-source contract observations. It never overwrites the original recorded results. The included actual receipt is `raw_results/clean_replay_v3.json`.

Requirements: Python 3.10 or later; tested with Python 3.13.5 on the recorded Linux runtime. Only standard-library modules are needed. No network is required. Do not disable assertions when reproducing tests.

## Actual persistence timing replay

```sh
python reproducibility/run_benchmark_copy.py --output benchmark_replay_new
```

The output directory must not already exist. The helper copies sources and data, then executes the recorded v3 complete replay in two sequential case-index chunks. These chunks are a runtime-management choice, not an outcome-based selection. All raw samples are saved. Timing results will vary with hardware, Python build and runtime noise; correctness and source hashes should not.

The measured endpoint starts from a truth integer. It includes discovery/build, needed source checks, serialization, actual reconstruction of a fresh loaded instance, rechecking, and an executed batch of 128 queries. Source extraction/query generation are outside this endpoint. Persistence is in-memory/same-process, not cold disk or an OS-process restart. Five repetitions rotate methods. No warm query batch precedes the measured final batch.

The artifact policy selects minimum actual SC-binary bytes among a bounded set of candidates. The packed baseline uses Python integer masks/popcount. The ROBDD is a fixed-order reference implementation, not CUDD. The failed `dd` installation log is retained. DSD/ACD/industrial KC/tensor comparators were not executed.

## Historical versions

`versions/v1` and `versions/v2` retain the exact code/test snapshots at those manuscript freezes; `versions/v3` preserves the final implementation. Use the matching snapshot in a separate copy when reproducing an old timing arm. Current code contains subsequent fixes and should not be represented as byte-identical to an earlier experiment.

`benchmark_v1.json`, `benchmark_v2_fused.json` and `benchmark_v2_binary.json` contain setup plus warm-query models. Their Q=1000 values are extrapolated from 128-query batches. The old packed/ROBDD paths parsed serialized data but queried original live objects. They do **not** establish new-instance replay. Only `benchmark_v3_replay.json` contains the corrected complete fresh-instance experiment.

A tool timeout interrupted the v2 binary run after 37 completed cases; only the remaining case was resumed. Earlier samples were retained. No selected reruns or best-of-run replacement were performed.

## Representation contract

First listed variable is the most significant assignment coordinate. Truth integer bit `a` is the function value on assignment `a`. Every artifact lists its declared universe; irrelevant but unassigned variables still contribute to model counts. The empty universe has one assignment.

`Artifact.condition(rho)` returns a new object over the remaining variables. A second condition cannot mention an already removed variable. `query_fused(rho)` is a scalar view of the object receiving it. JSON/binary decoding checks structure; exact source equivalence is a separate call to `checker.verify(artifact, expected_truth)`.

The checker does not import the producer/evaluator. That is a software separation, not a claim of independent human authorship or formal verification. Direct construction deep-freezes sequences and checks basic scope, but a directly constructed untrusted payload still needs shape checking and external verification before use. No secure hostile-input service is claimed.

## SC binary and JSON policies

`code/codec.py` defines SC bitstream version 1. Magic bytes are `SC`; packed fields include version, kind, scope, masks, lengths and payload. The declared universe is capped at 16 variables; variable identifiers must fit four bits (0..15). The factor-count field is five bits (up to 31), rank/prototype count fields are 17 bits, and the loader caps input at 4,000,000 bytes. These are implementation policies, not mathematical closure theorems. Arbitrary nonminimal constructed payloads may exceed a field limit. Ordinary discovered witnesses in the measured domain fit.

Factor scopes are canonicalized to the outer variable order; binary roundtrip guarantees semantic equality, not identical original factor ordering. Final padding is zero and trailing noncanonical data is rejected. No source certificate is embedded.

JSON uses decimal integers. With the tested Python default 4,300-digit conversion guard, dense truth integers at n=14 and n=16 fail JSON serialization in both artifact and packed paths. The guard is not disabled. The SC binary examples at both sizes round-trip correctly. Reported timing cases end at n=12. Supporting general larger JSON values would require an explicit hex/other schema change and new tests, not silently changing a global guard.

## Exported witnesses and data provenance

`data/selected_witnesses/INDEX.json` contains 76 selections (38 cases x JSON/binary selection), each exported as JSON and SC binary with hashes. The saved JSON has a terminal newline; that one byte is excluded from reported compact-JSON size. All exported witnesses were independently checked against their recorded external truth integers.

Pinned BLIF source:

```
commit: 0060e156826e733d69bf5b3322d1bdd0d03a1f9a
path: best_results/size/ctrl_size_2023.blif
SHA-256: 59b209caf863b2c6a9739777ae0a60a37cc4480c2e0d72fcbfcdddeb9a49be08
cases.json SHA-256: 04e0a7bd92b6a731a41472fbbd4e56b45d1c4e3387780ab7a3aa77cadb5ec41c
```

The input has seven primary inputs and 26 outputs. Each output's declared universe is its syntactic cone, not silently minimized essential support. Scalar and packed circuit evaluation agree, including off-set covers. The MIT notice is in `data/EPFL_LICENSE.txt`. The other 12 cases are intentional synthetic controls, not samples from an industrial population.

## Size and timing interpretation

Ideal payload bits exclude tags, variable IDs, indexes and object overhead. JSON and binary sizes measure actual serializations, with their exact format. Raw truth bytes are a packed payload floor without a container. None is a measured resident-memory value. Zero wins in this reference experiment do not prove that all structural methods fail or that no query count can amortize.
