# Response to Round 2: implemented in Draft 3

| Issue | Actual action / evidence | Final status |
|---|---|---|
| R2-B1: histogram persistence | Proved and tested xy versus (1-x)y; retained assignment-indexed factors; added all-query injectivity bound | RESOLVED |
| R2-B1: stored versus rediscovered components | Added xyz XOR x XOR y under z=0; explicit test records one retained versus two freshly discovered factors | RESOLVED |
| R2-B2: verification access model | Gave deterministic zero-transcript proof and rank<=1 spike example; expressly excluded formula/proof access, trusted aggregates and different models | RESOLVED for stated theorem |
| R2-B3: load proxy | Added real PackedTruth/ROBDD deserializers and a new exact replay protocol; 570 complete 128-query intervals measured on newly loaded objects | RESOLVED for in-memory reference replay |
| R2-B3: overbroad timing wording | Earlier Q=1000 values remain labeled modeled setup/warm-query proxies; final claim uses actual Q=128 intervals only | RESOLVED |
| R2-B4: caller aliasing | Constructor recursively freezes lists/tuples and rejects unsuitable payload elements; alias mutation test passes | RESOLVED in documented valid-input scope |
| R2-B4: codec limits | Documented 4-bit variable IDs, field widths and resource/format limits; structure/trailing-data tests included | RESOLVED as contract documentation; security audit OPEN |
| R2-B5: reproduction | Eight-command clean-directory replay passed; receipt, sources, raw data and selected witnesses included | RESOLVED; independent external replication OPEN |
| Review A: industrial synthesis relevance | No generic ACD/DSD superiority claim; latest don't-care ACD noted and excluded from total-function counting semantics | RESOLVED as scope, optimized evaluation OPEN |
| Review D: same-data status | Explicitly sensitivity/repair on the same 38 cases and seeds, not a new holdout population | RESOLVED |
| Review E/I: untrusted state | JSON/binary structure checks separate from external semantic verification; no formal/security certificate advertised | RESOLVED as narrow contract |
| Review H: elementary limits not new theory | No historical-first claim for injectivity or black-box lower bounds | RESOLVED |
| Review J: actual payloads | Exported 76 selected witnesses (38 cases x 2 selection policies), with both JSON and binary representations and hash index | RESOLVED |
| Review K: report positioning | Final verdict remains technical-report level; novelty/optimized baselines/external breadth unresolved | RESOLVED as calibration |

Open issues are not counted as resolved merely because a limitation paragraph was added. The final report makes only the narrower claims for which actual evidence is present.
