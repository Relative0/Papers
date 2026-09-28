# Independent-role Audit 1: frozen Draft 1

**Process status:** a separate adversarial pass by the same assistant, not an independent model, human panel, or journal review. Draft 1 was frozen before this file; its hash is in manuscripts/v1/FREEZE.json. Nothing here certifies mathematical correctness formally.

## Overall decision

A coherent nine-page technical-report draft exists. The proofs of substitution closure and elementary counting are sound under the explicitly stated scopes. There is not yet a persuasive new theorem or competitive systems contribution. The strongest original material is the reproducible implementation-contract audit. Do not raise the publication verdict above technical-report status on this evidence.

## Ratings (0 absent/invalid, 5 partial, 10 strong for the stated report scope)

| Category | Rating | Evidence and reservation |
|---|---:|---|
| Mathematical correctness | 8 | Entrywise substitution and sign-sum proof checked; not formal verification |
| Hidden assumptions / completeness | 7 | Declared scope and scalars clear; arbitrary matrix selectors not covered |
| Algorithm correctness | 8 | 105,292 checks plus independent scalar evaluation; large cases not exhaustive |
| Experimental design | 5 | Frozen inputs and costs; JSON criterion and unfused artifact queries constrain inference |
| Measurement/statistics | 5 | Raw five-repetition data present; no CPU isolation or inferential generalization |
| Reproducibility | 8 | Stdlib code, exact source hash, raw data; optimized tools unavailable |
| Traceability | 8 | Crosswalk and source pins present; legacy-to-new conversion still missing |
| Novelty/priority | 3 | Elementary mathematics and established query paradigm |
| Literature coverage | 7 | KC/DSD/ACD/TT/certification represented; exact closest theorem priority not resolved |
| Portfolio separation | 9 | No compiler judgments/P14 speedups; rank theorem background only |
| Notation | 7 | V denotes both universe and matrix factor in nearby passages |
| Exposition | 8 | Clear unused-variable example; need a complete rank example |
| Scope/coherence | 8 | A report with one endpoint, not an atlas |
| Limitations | 9 | Natural corpus and missing CUDD explicitly disclosed |
| Abstract calibration | 8 | Restriction theorem is correct; 'no table construction' needs representation-size qualification |
| Publication readiness | 5 | Report circulation plausible; novel journal submission unsupported |

## Blocking issues before a stronger revised report

**R1-B1. Rank counting lacks a precise complexity contract.** Supply a coefficient/column-profile identity, a direct streaming bound, and explicitly distinguish polynomial time in listed factors from exponential dependence on a rank-parameter transform. A Walsh method alone must not create a false hardness impression.

**R1-B2. Negative timing/space conclusions can be encoding and implementation artifacts.** JSON metadata is not a compact binary representation. The artifact counts materialize a conditioned object while baselines count directly. Add a compact codec sensitivity and fused exact queries, retaining the old results rather than silently replacing them.

**R1-B3. Integration with original research is conceptual, not executable.** Add an adapter from every original artifact tag and verify it against an external source. Do not imply the new simple product recognizer reproduces the old Kronecker search.

**R1-B4. Quantitative hierarchy evidence is missing.** Give fixed-cut rank versus complement-prototype bounds and a separation example. Explicitly prohibit generalizing a fixed-cut gap to optimally reordered portfolios.

**R1-B5. Verification coverage should include repeated conditioning and field mismatch.** Add sequential-versus-merged restriction tests and examples where GF(2) rank and real rank differ. These tests cannot substitute for proof.

## Nonblocking observations

The source loader findings are useful only as contract boundaries, not a security vulnerability claim or evidence that producer outputs were wrong. The report already handles this reasonably. The first release can remain a report without industrial baselines; a research-paper claim cannot. Rank minimality should be proved from factors or explicitly not claimed. A record of binary download failure is appropriate. Remove V's notational collision. Do not add the 16-CM atlas or retrieval sections.

## Concrete counterexample / falsification checks

The factor x1*x2 XOR x3*x4 confirms the declared-universe issue numerically (count 6; after x1=0, count 2). Rank-factor sums cannot be multiplied over integers because two parity contributions can cancel. Source loader tests were actually executed; their six observed outcomes are in the immutable v1 evidence. No contradiction was found in the v1 closure or elementary counting statements.
