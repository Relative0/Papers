# Five-Variable Benchmark Results

See `data/n5_benchmark_summary.csv`, `data/n5_benchmark_records.csv`, and `benchmarks/MANIFEST.json`.

The campaign uses 540 five-variable CNFs with seed 20260929 and three families: clean factorable, factorable with redundant cross-syntax, and random CNF.

Main conclusions:

- clean syntactic components are an excellent vtree signal when the representation faithfully exposes semantic independence;
- redundant cross-component syntax can hide independence;
- hard carrier constraints are perfect when aligned but can be maximally damaging when crossing;
- exhaustive factor-exposure search is a valid upper/control and always reaches prime alignment, but is not a scalable algorithm;
- no industrial runtime claim is made.
