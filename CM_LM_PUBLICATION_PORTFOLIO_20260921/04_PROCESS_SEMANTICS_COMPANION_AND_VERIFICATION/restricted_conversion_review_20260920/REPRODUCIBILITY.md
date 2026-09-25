# Reproducibility and scope

Python 3.10+; standard library only. Observed interpreter: Python 3.10.11 at `C:\Users\brian\AppData\Local\Programs\Python\Python310\python.exe`. No project virtual environment exists in this review package. No network access is used by the checks.

From the review folder, run:

```powershell
& 'C:\Users\brian\AppData\Local\Programs\Python\Python310\python.exe' -B code\run_review.py
```

The runner needs the frozen sibling `cm_lm_process_semantics_20260920` working package. It checks its manifest, copies only its checker and unit tests to `baseline_regression`, runs those copies plus the independent review checker, saves raw stdout and stderr, and rechecks the baseline. The copied checker can also run standalone in the delivered review folder. The new independent checker runs standalone with `python -B code/review_checks.py`.

Exact inputs and limits:

| Check | Universe | What it establishes computationally |
|---|---|---|
| A matrix classification | All 16^4 two-by-two matrices | Pivot Smith type agrees with four separately computed filtered binary ranks |
| A filters | Each of 65,536 matrices on the left and right of each of 15 Smith representatives: 1,966,080 checks | Both observed class downsets equal componentwise exponent order; not all two-sided pairs explicitly enumerated |
| Three-coordinate monotones | All 35 sorted triples over {0,...,4}, 1,225 ordered pairs | Threshold-count and componentwise orders agree; not an exhaustive scan of three-by-three A-matrices |
| Small nonchain test | All 65,536 two-by-two matrices over F_2[x,y]/(x^2,y^2) | Binary socle rank equals residue rank; explicit unit-minor extraction succeeds |
| Actual B_2 test | All 8^4 matrices over alphabet {0,1,u_1,u_2,u_1+u_2,u_1u_2,u_1^3u_2^3,1+u_1^3u_2^3} | Same checks in an explicitly bounded sample, not all 2^64 B_2 matrices |
| Resolved-disposal witness | Exact matrices in REVIEWED_THEOREMS.md R5 | Full binary output equals Phi_A(I_2); unresolved output has subspace dimension two |
| Baseline exhaustive rerun | Original checker and unchanged inputs | 65,536 matrices; 983,040 filters; 8,064 coarse support checks; 98,304 constructed normalizers; 368,640 orbit vectors |
| Baseline regression | Original 12 unittest tests | Operational/algebraic regressions pass |

The baseline normalizer count enumerates the constructed semilinear group; the upper bound is analytic, not an exhaustive search of GL(8,2). Neither implementation is a proof assistant. The new checker imports no baseline polynomial arithmetic, Smith routine or binary kernel. Its multiplication is implemented by explicit monomial exponent addition rather than the baseline's bit-shift formula.

All numerical inputs are deterministic. Integers encode polynomial coefficients: bit i is u^i over A; bit i+4j is u_1^i u_2^j over B_2. Binary matrices are stored as row bit masks. `data/review_checks.json` contains the filter matrices, disposal rows, all phase-measurement branch vectors, and exact target/output rows. Source hashes, environment, commands, UTC timestamps and exit codes are in `data/run_record.json` and the results JSON files.

The broad canonical audit's 31 tests were run in the previous phase; this review did not rerun them because the audit files were not changed. Its nine previously recorded manifest mismatches remain a separate historical provenance issue. No claim is made that this review repaired them.

`code/write_ledgers.py` serializes the queries and primary-source inspection record actually used during this review. The search was bounded and followed explicit backward citations and their later use; it was not a comprehensive citation-index search. A failed lookup is recorded as an access limit, never as evidence of novelty.

The workspace is not a Git repository. `git status --short` and `git diff --stat` were attempted and unavailable for that reason. SHA256 verification and an exact artifact inventory provide the change audit. Original papers and baseline files were not edited. The review adds a separate package and a separate delivery subfolder.
