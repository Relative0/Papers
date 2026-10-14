# Draft 3 final claim crosswalk

Earlier crosswalks remain preserved and identify v1/v2-specific results. Final additions and corrections:

| ID | Claim | Proof / executable evidence | Scope |
|---|---|---|---|
| C17 | Histograms alone do not support all named-variable restrictions | `persistence_limits.tex`; persistence_v3.json | Explicit two-variable rank-one example |
| C18 | Exact all-query states distinguish supported functions | Proposition in persistence_limits.tex | Deterministic exact answers, full assignments included, fixed-width bound |
| C19 | Zero-source verification needs all value queries | Proposition in persistence_limits.tex; 510 spike-rank checks | Deterministic zero-error black-box model only |
| C20 | Finest XOR factor count can increase after restriction | Explicit ANF example and persisted JSON | Retained list versus rediscovery distinguished |
| C21 | Final constructor resists caller list aliasing | artifacts.__post_init__; persistence_v3.json | Deep normalization, not hardened input service |
| C22 | Complete reload experiment shows zero per-case median wins | benchmark_v3_replay.json; protocol v3; 570 full trials | Actual Q=128, in-memory, one design + synthetic controls |
| C23 | All exact suites rerun cleanly | clean_replay_v3.json; run_correctness.py | Seven actual subprocess commands, stdlib, not independent external replication |
| C24 | Actual selected witnesses preserved | selected_witnesses/INDEX.json and 152 serialized files | 76 selections, each JSON and SC binary |
| C25 | Standalone technical report, not mature novel paper | Final audit and novelty ledger | Editorial inference, not a theorem or acceptance forecast |

C07/C14 in earlier drafts must be read with their timing-model limitations: Q=1000 values were extrapolated from warm batches and baseline parsing did not constitute new-instance loading. Only C22 is a directly measured complete reload claim.
