# Reproducibility bundle

This directory accompanies `binary_order_thinning_finite_posets_post_audit_v2.tex`.
It separates exact mathematical certificates from exhaustive finite evidence.

## 1. Seven-state exact certificate

`verify_two_bit_height_two_counterexample.py` reconstructs the seven-state poset,
two-bit labels, thinned order, deleted edges/triangles, integral relative boundary,
determinant, F2 rank, perfect matchings, deleted-edge triangle degrees, and beat-point
reductions of both endpoint posets.

Run:

```bash
python verify_two_bit_height_two_counterexample.py
```

The rerun is in `two_bit_7_rerun.out`; `two_bit_7_verified.out` is the supplied archive
output. Both end in `VERIFIED` and agree on the mathematical certificate.

## 2. Exhaustive two-bit search through six vertices

`two_bit_height2_exhaustive.cpp` enumerates naturally labelled transitive relations of
height at most two on `n` vertices and all `4^n` two-bit labels. Every finite poset has
a natural labelling after choosing a linear extension, so the search covers all
isomorphism types (with duplication).

For each case the checker constructs the relative F2 edge-triangle matrix. A homology-
neutral height-two pair must be square and full rank. It then tests uniqueness of the
perfect matching in the support graph. By the height-two matching theorem used in the
paper, direct relative collapse is equivalent to a unique perfect matching.

Compile and run:

```bash
g++ -O3 -std=c++17 two_bit_height2_exhaustive.cpp -o two_bit_height2_exhaustive
./two_bit_height2_exhaustive 6
```

The post-audit rerun produced:

- n=1: 1 poset, 4 profiles, no counterexample
- n=2: 2 posets, 32 profiles, no counterexample
- n=3: 7 posets, 448 profiles, no counterexample
- n=4: 39 posets, 9,984 profiles, no counterexample
- n=5: 330 posets, 337,920 profiles, no counterexample
- n=6: 4,117 posets, 16,863,232 profiles, no counterexample

Exact stdout is retained as `two_bit_n1_rerun.out` through `two_bit_n6_rerun.out`.
The supplied archive outputs for n=5 and n=6 are also retained.

**Status:** this establishes the vertex-minimality claim by exhaustive computation;
it is distinct from the analytic proof of the seven-state existence theorem.

## 3. Retained one-bit regression verifiers

The directory includes:

- `verify_homotopy_preserving_observations.py`
- `verify_refinement_subclasses.py`
- `verify_repair_forest_theorem.py`

The first two are retained as supplied. The original repair-forest script is preserved
as `verify_repair_forest_theorem_original.py`; it contained an absolute import path
(`/mnt/data/verify_homotopy_preserving_observations.py`). The runnable
`verify_repair_forest_theorem.py` differs only by replacing that absolute path with a
path relative to its own directory. Both forms were checked; the portable rerun is in
`verify_repair_forest_theorem_portable_rerun.out`.

The one-bit scripts are supplementary finite regression checks. They are not used as
substitutes for the proofs in the manuscript.

## 4. Convenience scripts

`run_two_bit_checks.sh` compiles the C++ checker, reruns the exact seven-state verifier,
and runs the exhaustive checker for n=1,...,6.

`run_one_bit_checks.sh` reruns the retained one-bit scripts.

## 5. Integrity

`SHA256SUMS` contains hashes for the reproducibility files. The build environment used
for this post-audit rerun was Linux with Python 3 and g++ supporting C++17.
