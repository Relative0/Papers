# Handoff README — Structured Factorization Phase 5B

This package is intended for a fresh **ChatGPT Work** thread running a strong research model.

## Recommended execution

Upload this ZIP to the new Work thread and instruct the agent to open and follow:

`NEXT_AGENT_PROMPT_PHASE5B.md`

The prompt is self-contained, but the nested Phase 4 and Phase 5 packages are authoritative source material.

## Package layout

- `NEXT_AGENT_PROMPT_PHASE5B.md` — main task specification.
- `key_docs/` — the most important Phase 5 documents for fast orientation.
- `source_packages/STRUCTURED_FACTORIZATION_PHASE4_2026-09-29.zip` — Phase 4 code, data, proofs, and exact SAT/SDD baseline.
- `source_packages/STRUCTURED_FACTORIZATION_PHASE5_T2_2026-09-29.zip` — complete Phase 5 T2 output package.
- `SHA256SUMS.txt` — checksums for handoff contents.

## Continuity rule

The new agent should reproduce the core Phase 4/5 claims before tuning Phase 5B. It should not use semantic ground truth in heuristic vtree objectives except in explicitly labelled oracle controls/evaluation.

The primary next question is whether **factor-exposure-aware vtree search, soft carrier information, and CM defect-support hyperedges** improve the total exact hybrid factorization workflow when evaluated with a real SDD compiler and real incremental SAT backend.
