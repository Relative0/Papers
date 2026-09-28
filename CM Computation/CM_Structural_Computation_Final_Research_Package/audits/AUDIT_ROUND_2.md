# Audit 2 of frozen Draft 2

**Method:** a separate adversarial pass by the same assistant. This is not an independent model evaluation, external peer review, or formal proof. The v2 TeX/PDF and code were frozen before this report. Mathematical proof checks, inspection of the actual benchmark, and constructor/codec inspection drive this audit.

## Mathematical reassessment

The profile identity follows entrywise from parity characters. The stated dense-transform complexity is correct after histogram construction; the polynomial row-streaming alternative prevents a misleading hardness inference. Minimal recompression through U=AB, BW=EF is sound because A is injective. Complement-quotient bounds are valid for occurring row classes, including zero matrices and all-ones row spaces. The fixed-cut inner-product example is correct; the real Gram matrix argument handles r>=2, with r=1 separated. None of this establishes historical novelty.

The most important remaining mathematical omission is persistence: a histogram adequate for one query is not automatically sufficient for later coordinate restrictions. Draft 2 says that assignment associations are retained but does not demonstrate why they are necessary. The report also needs a precise boundary between black-box truth verification and formula/proof-based certification. Finally, stored factor count and the number of rediscovered irreducible XOR components must not be conflated.

## Actual implementation and measurement findings

Inspection of benchmark.py shows that the v1/v2 baseline arms parse serialized JSON but continue querying the previously constructed baseline object. Thus these arms measure serialization/parse plus warm queries, not independently reconstructed persistent-state replay. Draft 2 acknowledges a proxy but its abstract and several 'full-lifecycle' phrases remain too broad. This is a methodological correction, not evidence that recorded timings are fabricated.

The new Artifact dataclass is frozen, but direct callers can pass nested lists; annotations alone do not make them immutable. Normal producer and JSON-decoder paths use tuples, so the reported tests are not invalidated. A claim covering arbitrary constructor inputs needs deep normalization or rejection. Likewise the compact codec supports only variable IDs 0..15; the semantic contract is more general. State that implementation limit.

## Ratings (0 absent/invalid, 5 partial, 10 strong within report scope)

| Category | Score | Reason |
|---|---:|---|
| Mathematical correctness | 8 | Proofs checked; no formal verification |
| Theorem completeness | 8 | Persistent histogram and source-access boundary still need treatment |
| Algorithm correctness | 8 | Large finite suites and adapters; constructor immutability gap |
| Experimental design | 6 | Encoding and fusion sensitivity added; one external design |
| Measurement validity | 5 | Parse-only baseline loading and extrapolated lifecycle language |
| Reproducibility | 8 | Frozen versions and stdlib sources; clean replay still needed |
| Traceability | 9 | Additions tied to executed tests and raw outputs |
| Novelty/priority | 3 | Useful synthesis/audit, not independently new principles |
| Literature | 8 | Correct arithmetic and fixed-cut distinctions; no exhaustive priority clearance |
| Portfolio separation | 9 | Foundations and compiler contributions remain excluded |
| Notation | 8 | Explicit scopes, fields and dimensions |
| Exposition | 8 | Good rank section; add tiny persistence counterexample |
| Coherence | 8 | One operational endpoint; additions remain relevant |
| Limitations | 8 | Most limits disclosed; abstract should match measurement contract |
| Abstract/conclusion calibration | 6 | 'Full lifecycle' stronger than actual loading path |
| Research-submission maturity | 5 | Technical report defensible; comparative novelty/evidence inadequate |

## Required v3 repairs

R2-B1: Add exact histogram insufficiency and declared-scope counterexamples. Preserve assignment indexing in all interfaces.

R2-B2: State and prove a deterministic zero-error black-box source-verification lower bound with its input model. Do not extend it to formula/proof-based verification or randomized approximation.

R2-B3: Implement actual fresh-instance serialization/load/reverification/query replay for all three backends, record a new protocol amendment, and directly time a complete finite query batch. Keep prior runs and label their Q=1000 extrapolations correctly. A new same-data run remains sensitivity evidence, not held-out generalization.

R2-B4: Deep-freeze direct constructor inputs, distinguish codec constraints from theorem scope, and add malformed/aliasing tests. Do not claim a hardened secure decoder.

R2-B5: Produce a clean replay receipt, complete claim/issue ledgers, and a final report-level readiness decision. Missing optimized baselines and broad natural data remain open rather than being 'resolved' by more prose.
