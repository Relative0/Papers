# Response to Round 1: implemented in Draft 2

These are responses to same-assistant, role-separated reviews, not a journal correspondence or independently commissioned review. Draft 1 remains unchanged.

| Issue | Response and evidence | Status |
|---|---|---|
| R1-B1: rank-count complexity | Section 7 proves the profile identity, specifies dense-transform cost and workspace, and gives a row-streaming bound polynomial in the explicit factor input. `walsh_count` crosschecked against every 4x4 Boolean matrix. | RESOLVED for report |
| R1-B2: encoding/fusion bias | Added `query_fused`, SC binary encoder/decoder, a recorded v2 protocol amendment, and two new timing arms. Both original and new samples are retained. Binary selection differs materially from JSON selection. | RESOLVED as a sensitivity analysis, not a competitive benchmark |
| R1-B3: legacy integration | Added `legacy_adapter.py`; 675 original artifacts across all four tags and 6,750 direct queries agree with the separate checker. Different discovery search spaces remain explicit. | RESOLVED in tested bounded scope |
| R1-B4: hierarchy | Section 8 proves complement-quotient bounds and the fixed-cut inner-product dictionary gap. It explicitly observes that another partition yields a small XOR representation. | RESOLVED; no priority claim |
| R1-B5: update and arithmetic tests | Added 3,020 sequential/fused checks, 2,000 recompressions, exact real-rank tests, and 151 compact-codec round trips. | RESOLVED in stated finite scope |
| Reviewer A: serious synthesis comparators | Literature includes DSD/ACD and the report distinguishes hardware and counting endpoints. Industrial tools were not executed. | OPEN for research-level comparison |
| Reviewer B: established KC paradigm | Scope, literature and publication posture explicitly reject a first-compiled-artifact claim. | RESOLVED as claim calibration |
| Reviewer C: minimum rank vs stored width | Factor-only recompression and a separate minimality check are now present. Standard linear algebra is not relabeled as a new principle. | RESOLVED |
| Reviewer D: confirmatory language | Same-data amendments are called sensitivity analyses; Q=1000 remains a modeled extrapolation from 128-query batches. | PARTIALLY RESOLVED; actual fresh-instance replay should be improved |
| Reviewer E: immutability and cold loading | Normal producer payloads use tuples; cold storage and process/RSS measurements remain unperformed. Arbitrary constructor input still warrants scrutiny. | PARTIALLY RESOLVED |
| Reviewer F: one contribution | The paper remains a bounded operational contract/audit report rather than a collection of decomposition discoveries. | RESOLVED for coherence; novelty still limited |
| Reviewer G: publication positioning | Report circulation rather than mature journal novelty is the explicit posture. | RESOLVED |

The second revision does not claim that missing optimized baselines have been replaced by discussion. They remain a submission blocker for a competitive performance paper.
