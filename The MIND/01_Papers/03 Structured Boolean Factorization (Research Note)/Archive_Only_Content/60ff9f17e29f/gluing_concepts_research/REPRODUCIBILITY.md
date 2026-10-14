# Reproducibility Notes

## Environment

The computation uses only the Python standard library and has no third-party package dependency. It was rerun successfully with `python3` on 28 September 2026.

## Command

```bash
cd gluing_concepts_research
python3 code/gluing_audit.py
```

The script prints a JSON summary and writes the exact finite examples, diagnostic assertions, enumeration counts, and structured-factorization example under `data/`.

## Exhaustive domain

For labelled vertex sets of size `n <= 5`, the script enumerates every downward-closed family of subsets, filters to complexes that use every named vertex, computes minimal nonfaces, finds the connected components of the minimal-nonface interaction hypergraph, reconstructs the putative finest join decomposition, and checks every unordered bipartition against the exact induced-subcomplex join condition.

The resulting labelled-complex counts are:

| n | all downsets | use every vertex | join-decomposable | join-indecomposable | bipartition checks | failures |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 1 | 0 | 1 | 0 | 0 |
| 2 | 6 | 2 | 1 | 1 | 2 | 0 |
| 3 | 20 | 9 | 4 | 5 | 27 | 0 |
| 4 | 168 | 114 | 30 | 84 | 798 | 0 |
| 5 | 7581 | 6894 | 546 | 6348 | 103410 | 0 |

Total: **7,020** complexes using all vertices; **104,237** partition checks; **0** partition-criterion failures; **0** finest-factor reconstruction failures.

## Exact examples

The script reproduces Examples A–G and the additional cross-layer Example H. Important assertions include:

- four triangular faces union to the tetrahedral boundary, not the filled tetrahedron;
- the boundary has Betti vector `(1,0,1)` over `F2`, while the filled tetrahedron has `(1,0,0,0)`;
- flag completion of the complete graph `K4` yields the filled tetrahedron;
- the chosen clean-factorization example reconstructs exactly from its finest join factors;
- the chosen irreducible example has a connected minimal-nonface interaction hypergraph;
- the cross-layer Example H has nontrivial structural and semantic prime partitions whose least common coarsening is the one-block partition.

## Interpretation limits

These computations verify finite combinatorics and implementation contracts only. They do not establish psychological validity, general novelty, or complexity results beyond the enumerated range.
