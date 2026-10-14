# Phase 4/5 frozen-claim reproduction audit

Date: 2026-09-29. Status: **PASS for the specified frozen campaigns, with scope qualifications below.**

## Execution and archive preservation

`code/reproduce_frozen.py` copied the eight archived Python sources byte-for-byte to `reproduction/frozen_original/`. It then wrote executable copies under `reproduction/relocated/` with only the archived Linux absolute import/output paths replaced by paths in this Phase 5B directory. No algorithm or random-number call was changed. The transformation manifest records every replacement and original/relocated SHA-256. Archived source hashes were checked again after execution and remained unchanged. Python bytecode generation was disabled.

All six campaigns exited successfully. Eleven frozen output artifacts match after parsing JSON/CSV or comparing text lines. The sole ignored JSON key is the archived `runtime_seconds`; platform newline differences are ignored. The JSON comparison retains all counts, examples, partitions, records, seeds and other values. Raw logs and machine-readable comparison results are in `reproduction/logs/` and `reproduction/frozen_comparison_report.json`.

The runtime was Python 3.10.11, Windows 10 build 19045, standard-library validation paths. The frozen subprocesses used `PYTHONHASHSEED=0` and `-B`. These reproductions make no industrial SAT or SDD runtime claim. Versions and commands are preserved in `reproduction/runtime.json` and the comparison report.

## Frozen campaign results

| Campaign | Reproduced result | Measured wall seconds |
|---|---|---:|
| Phase 4 compressed-cofactor/direct extraction | 65,535 nonfalse functions; 0 root-cut failures; 0 laminar-extraction failures; 2,601 decomposable; 2,376 hidden by the fixed balanced vtree | 19.419 |
| Phase 4 read-once operator trees | 10 essential binary connectives; 35,210 instances; 0 failures | 11.869 |
| Phase 4 controlled SAT comparator | 120 instances; 516 cut queries; 0 discrepancies; example DIMACS and assumption stream match | 3.197 |
| Phase 5 exhaustive n=4 | 65,535 functions; 15 non-plane labelled rooted binary vtrees; 225 fixed-balanced alignments among 2,601 decomposable functions; 65,535 global optima reach the prime partition | 14.029 |
| Phase 5 defect family | n=3,4,5,6; empty pairwise rank-two graph; one semantic prime; minimum balanced-cut witness support n | 0.187 |
| Phase 5 n=5 benchmark | Seed 20260929; 540 accepted instances, 180 per family; all 2,700 method records and 15 summary rows match | 1.857 |

The n=4 random-vtree alignment probability among decomposable functions is `0.2193771626297578`. The operator campaign is exhaustive for the frozen ordered-leaf tree families through n=4 and samples 30,000 n=5 draws with seed 123; sampling is with replacement and is not a claim of 30,000 distinct trees. The incremental seed is 41.

## Independent checks against circular scoring

Merely rerunning Phase 5 would be insufficient: its n=4/n=5 exposure scores are computed from the already known semantic prime partition. The new audit therefore implemented independent relational-projection computations.

For a nonempty relation R and disjoint L,R covering a variable set U, Cartesian factorability is checked by

`|projection_U(R)| = |projection_L(R)| * |projection_R(R)|`.

Projection sets are constructed directly from satisfying assignments. Factor extraction recursively applies this product-cardinality check and never receives the prime partition as an input. To compute the n=4 reference prime partition independently, all 15 set partitions are enumerated and their projection-product cardinalities checked; the unique valid partition with most blocks is selected. This implementation is separate from the archive's rank-cut intersection construction.

- All 65,535 independently derived n=4 prime partitions agree with the archive.
- All 458,745 unordered n=4 cut checks agree between directly constructed compressed nonzero cofactor sets and the projection-product criterion.
- All 983,025 n=4 function/vtree direct-exposure partitions agree with the archive's prime-derived shortcut.
- All 952,569 prime-aligned n=4 function/vtree pairs return the full prime partition under the independent extraction.
- During an instrumented replay of the frozen n=5 seed, all 121,500 exposure calls agree with independent direct projections; frozen outputs still match. Instrumentation consumes no random numbers.

The n=5 accepted CNFs, truth-table integers, family and instance identifiers are now saved explicitly in `reproduction/frozen_n5_accepted_instance_manifest.json`. The archive supplied a generator and seed but did not preserve these per-instance CNFs. The new manifest is a reconstruction, not an original archived artifact.

Machine-readable evidence is in `reproduction/independent_n4_audit.json` and `reproduction/independent_n5_audit.json`. These checks validate the frozen shortcut's values. They do **not** convert exhaustive oracle-assisted search into a scalable, non-oracle heuristic. The frozen n=5 carrier modes also consult the known prime partition to construct aligned/crossing cases; that is labelled benchmark generation/control, not information a production objective may consume.

## Assumptions and limitations carried forward

1. **Nonempty relations.** The SDD and prime-partition theorem statements exclude the false function. All exhaustive n=4 and accepted n=5 campaigns obey this. A replay of the frozen incremental generator finds 16 false formulas among its 120 trials (IDs saved in `reproduction/assumptions_audit.json`). Four-corner encoding equivalence still holds on them, but they cannot establish uniqueness of a nonempty-relation prime factorization. New pipelines should handle false inputs explicitly before using prime-factor claims.

2. **Prime alignment is a promise or certificate.** If all semantic prime blocks are vtree clades, direct extraction returns the full partition; this mathematical implication is correct. However, a failed root SDD cut says only that this particular cut fails. It does not certify that the resulting unresolved block is semantically prime. On the balanced tree `((0,1),(2,3))`, both `(x0=x2) AND (x1=x3)` (truth bits 33825) and the all-equal function (truth bits 32769) return one direct block, although the former has two crossing semantic primes. Thus a measured zero-residual shortcut requires independently certified primeness or an explicit theorem-class/prime-alignment promise. An oracle-aligned control must not silently supply that certificate to heuristic runs.

3. **Local truth-table coordinate order.** The Phase 4 `row_patterns` routine expects truth bits in the order `leaves(tree)` and does not remap global variable indices. Its frozen fixed-order use is correct. Reusing it on arbitrarily permuted vtrees requires a truth-table permutation. The independent audit uses original-coordinate projection masks and avoids this issue.

4. **Representation restrictions.** The compressed-SDD criterion assumes a complete compressed partition with exhaustive, disjoint, nonfalse primes; “at most one nonfalse sub” relies on compression. Uncompressed or arbitrary structured d-DNNF syntax does not inherit this syntactic test. True/free variables require singleton handling; false functions require a separate convention. The operator result assumes essential connectives and support-disjoint, read-once leaves, not general shared DAGs.

5. **Correctness versus performance.** The archived controlled comparator restarts its bundled DPLL search. It verifies the encoding and witness semantics; it does not demonstrate learned-clause amortization. Frozen n=4/n=5 scripts manipulate exact tables/prime partitions and do not measure maintained-library SDD size or an end-to-end industrial runtime. The separate archived clause-emission table has no bundled standalone generator; this audit does not present it as newly reproduced timing evidence.

6. **Proof versus finite evidence.** Finite exhaustive checks support implementations and discover counterexamples; they do not replace general proofs. The n=3..6 defect computations instantiate the archived all-equal counterexample family. The general family argument remains a mathematical statement, not a conclusion inferred solely from those four computations.

## Reproduce

From the Phase 5B directory, with its sibling `continuity_archive/` present:

```powershell
python -B code/reproduce_frozen.py
```

Use `--mode frozen` to run only the archived campaigns, or `--mode independent` to rerun the independent audit using the relocated copies. The script writes only inside `phase5b_output/reproduction/`; a rerun replaces its own reproduction outputs. Approximate complete wall time on the recorded machine was under two minutes. No external package installation is required.

The frozen-result gate is satisfied. Subsequent adaptation claims must use the new non-oracle pipeline and its separately frozen benchmark split; the archived oracle scores remain explicit controls/evaluation only.
