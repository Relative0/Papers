# CM Quantum Research Handoff

Prepared: 2026-09-17

This package is intended to be extracted into:

`C:\Users\brian\Documents\CM Quantum`

The chat environment cannot write directly to that Windows path, so this archive is the portable handoff. It contains the two research papers, editable LaTeX/source-verification bundles, every machine-readable test result currently present in the working session, two ready-to-paste prompts for new research threads, and a concise state-of-research handoff.

## Recommended folder layout after extraction

- `papers/` — the two consolidated papers and source/verification bundles.
- `test_runs/all/` — all CSV/JSON experiment outputs from the current research sequence.
- `prompts/` — two independent prompts for separate threads.
- `CURRENT_STATE.md` — definitions, confirmed results, caveats, and next questions.
- `TEST_RUN_GUIDE.md` — which result files matter most and which older files record superseded intermediate hypotheses.

## Strong recommendation: use two new threads

Use one thread for **Computation and Benchmarking** and a second for **Pure-Boolean Modal / Quantum-like Investigations**. They share the same algebraic foundation, but their success criteria and literature are sufficiently different that separating them should reduce confusion and make reproducibility easier.

The computational thread should not assume that the CM method is faster. It should test that proposition against strong incumbent representations and retain negative results.

The modal/quantum-like thread should stay inside the pure Boolean CM coefficient algebra unless a comparison section explicitly discusses the signed/cyclotomic lift. It should not call modal possibility patterns Born probabilities or claim physical quantum behavior without evidence.
