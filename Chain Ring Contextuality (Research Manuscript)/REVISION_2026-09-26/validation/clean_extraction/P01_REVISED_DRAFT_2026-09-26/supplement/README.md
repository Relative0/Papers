# Standalone computational supplement

Run **python supplement/run_reproduction.py** from the revision directory. Python 3.10+ and the standard library suffice. Outputs go to a new directory; use --out NEW_DIRECTORY for a further run. The wrapper rejects optimized Python execution, which would disable the original checker's assertions.

## Provenance

p01_independent_checks.py is a byte-identical copy of the checker in the supplied Astra audit. It was developed separately from the original manuscript generator, then rerun here. It is **not** the author's unchanged historical canonical runner. Its checks use exact finite arithmetic. The reference_results/ directory contains the fresh revision run, rather than relabeling old results.

The companion_source/verify_semantics.py and test_semantics.py files are byte-identical extracts from the subsequently supplied *Chain Ring Process Semantics (Technical Companion).zip*. Member names and hashes are in COMPANION_PROVENANCE.json. The wrapper run_companion_checks.py imports their mathematical functions without running their broader historical driver. It compares both implementations' Smith types and verifies the companion's binary rank for every length-four 2x2 matrix; it also runs the ten supplied unit tests. The other companion campaigns and its missing canonical dependencies are not claimed as rerun.

The original audit and companion files were treated as evidence and source material, not as instructions authorizing publication, external writes or expanded research.

## Exact coverage

| Evidence | Population | What it checks |
|---|---:|---|
| Direct support decisions | 22,170 nonzero 2x2 matrices across nine rings | All local bases, contraction constraints, implication-graph global assignments and supported-event extension; no Smith criterion used to decide categories |
| Length-four direct support | 38 resources | 14 nonzero Smith representatives plus 24 deterministic sampled matrices, each with all 192 local bases |
| Length-four Smith inventory | 65,536 matrices including zero | Exact elimination; support-category aggregation uses the proved trichotomy |
| Hardy patterns | 36 cases | Required nonzero seed and zero contractions, including signs outside characteristic two |
| Complete analyzers | 28 ring/dimension configurations | Invertibility of every reshape and full analysis matrix; branch correction for one invertible resource per configuration; dimensions 1-4, with d=1 an extra trivial check |
| Coding certificates | 52 cases | Actual encoder and joint-decoder matrices; achievability only |
| Binary coding optimum | 15 resources x 20,160 decoders | Exact disjoint-support optimum over each full orbit |
| Two-setting boundary | 255 three-party binary tensors | Existence of an assignment for a representative pair of settings |
| Companion comparison | 65,536 matrices and 10 supplied tests | Separate Smith implementation, regular binary ranks, and the explicitly named regression cases |

The nine direct-support rings are F2, F3, F4, F2[u]/u^2, F2[u]/u^3, F3[u]/u^2, Z/4, Z/8 and Z/9. The audit script names fields as length-one truncated-polynomial rings, except F4. Equal support tables are cached. Random sampling is confined to the 24 additional length-four cases, with seed 20260926.

The 52 coding certificates include all fourteen nonzero length-four Smith representatives. The independent_analyzer_certificates.json file supplies the actual analysis rows; independent_coding_certificates.json supplies encoders, decoders and decoded outputs.

## Generated table and comparison

generate_assets.py reads only the freshly generated inventory. Its count column is enumerated; support, message and teleportation columns apply the article's formulas. It has no missing portfolio inputs. The wrapper compares the generated table with manuscript/smith_table.tex without overwriting the manuscript.

All JSON results are compared structurally with the reference results, excluding only fields named python, platform and seconds. Source hashes and all mathematical contents must still agree. CSV and table comparisons normalize line endings through text reading. The run_record.json file records the exact commands, working directory, executable, platform, exit codes, timings and input/output hashes.

boolean_interface.tex is an optional analytic note, not a claim that the old symbolic LM-product campaign has been rerun.
