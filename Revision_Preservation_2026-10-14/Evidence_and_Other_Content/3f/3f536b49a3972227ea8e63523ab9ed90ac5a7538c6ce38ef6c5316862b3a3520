# P01 reproducibility supplement

Canonical source: the hash-validated recovered CM_LM_RESEARCH_CONSOLIDATION archive. The supplied runner was executed unchanged in ../runs/canonical_01 with --all --historical --timeout 180. All 21 stages passed. See ../evidence/REPRODUCTION_ENVELOPE.json for exact interpreter, dependency versions, command, runtime, every input SHA-256 and output hash; see ../runs/canonical_01/RUN_MANIFEST.json for per-stage commands/status.

Relevant finite artifacts:
- ../runs/canonical_01/independent/resource_inventory_summary.json
- ../runs/canonical_01/independent/explicit_dense_decoders.json
- ../runs/canonical_01/independent/dual_number_contextuality.json
- ../runs/canonical_01/capability/ (original lab, phase and two-setting results)
- ../runs/canonical_01/bridge/ (symbolic interface tests)

Run generate_assets.py with the pinned verification environment to regenerate smith_table.tex and ANALYZER_CHECK.json. It tests both the invertibility of every effect reshape and the flattened analysis matrix, for dimensions 2,3,4 over Z/4Z, Z/8Z and Z/9Z. No random seed is used. All three figures are native LaTeX in main.tex; there are no placeholder artwork files.

Build: ../build_tex.py main.tex resolves an absolute task-local source; it runs installed pdflatex with automatic package installation and shell escape disabled, then BibTeX and two stabilizing TeX passes. BUILD_MANIFEST.json and build_history preserve results. Visual-review PNGs are QA intermediates; the manuscript PDF is the deliverable.

The supplement verifies finite implementations. General mathematical statements depend on the manuscript proofs. No fresh performance campaign was run.
