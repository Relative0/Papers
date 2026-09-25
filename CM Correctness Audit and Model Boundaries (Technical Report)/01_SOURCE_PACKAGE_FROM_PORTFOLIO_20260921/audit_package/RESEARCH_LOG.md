# Audit research log

## 18 September 2026

1. Preserved the four available input archives under `source_snapshots`; recorded original archive hashes. No access to the Windows folder was claimed.
2. Reran all four historical suites: 59 tests passed. Checked three supplied manifests: 87 total listed files, no missing or changed entries.
3. Implemented a fresh packed Boolean kernel with a separate scalar contraction and a separate batch elimination algorithm; no earlier computational module imported.
4. Rebuilt the rotation algebra, all 65,536 gates/resources, Smith/rank profiles, local stabilizers, 192 measurement bases, and 24 permutation gate cases.
5. Recomputed restricted shared/literal contextuality by exact 2-SAT implication closure. Proved the Bob-conjugation setting relabeling that explains matching counts.
6. Rebuilt literal GHZ tables and the minimum-six-context search; preserved the family-dependent negative and weighted-lift results.
7. Constructed a simpler tensor-product Bell-effect basis from four explicit 2x2 Boolean effects. Independently replayed the old phase synthesis words and old teleportation outputs.
8. Used direct 512-dimensional tensor contractions to validate branch maps. Ran all 256 inputs x 64 outcomes for both old and new analyzers and all 65,536 resources x 64 branch ranks.
9. Explicitly computed and decoded all 64 dense-code messages. Separated modal basis-readout resource accounting from ordinary memory access.
10. Found and verified the nonzero-shared-tensor-to-zero counterexample, the literal local equivalence of classes (0,2) and (1,1), the enlarged exact-subspace capacities, and finite-copy literal activation witnesses.
11. Recomputed the shared restricted/quotient hierarchy with 983,040 scans each. Verified reversible corrections for the free-line construction.
12. Reran orthogonal-row restrictions and proved the broader even-dimensional hyperplane obstruction. Enumerated common P/T-invariant bilinear forms: only zero.
13. Verified the external no-signalling probability obstruction with LP and exact symbolic constraints; distinguished it from Boolean state evolution and from probabilistic physical theory.
14. Added 31 independent named tests and checked the original natural H-based analyzer's branch-rank loss.
15. Authored and compiled the LaTeX report; rendered the PDF and inspected all pages for layout and mathematical display issues. Final artifact checks and hash manifest accompany the release.

All failed interpretations are preserved in the report, rather than concealed by the passing arithmetic tests. Timing logs are execution receipts, not speed benchmarks.

## Execution and build notes

Several aggregate shell invocations reached the sandbox execution limit; their partial logs are labeled `interrupted_*`. All four historical suites have completed passing receipts, and the final independent drivers and tests were also run separately to completion. A cleanup edit briefly removed the empty normal-form dictionary initialization, producing the retained `corrected_cleanup_error.txt`; the initialization was restored and every independent driver and test then reran successfully. No result from that failed partial attempt is used as final evidence. Pytest plugin autoload is disabled in the reproducer to avoid unrelated environment plugins. The standalone and modular LaTeX sources were both compiled to convergence and their complete extracted PDF text agrees.
