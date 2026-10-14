# Pre-run review clarifications

2026-09-29, before any new benchmark runs. These clarify the frozen protocol without changing the objective or dataset.

1. Generated held-out cases often share an unlabelled module/path structure with training cases. Held-out here means a frozen new instance/label seed, not an unseen structure distribution. Bootstrap intervals are descriptive conditional on this fixed generator mixture, not population coverage guarantees. No pilot result establishes industrial-scale improvement.
2. B3 uses connected components and balanced trees on greedy min-fill variable orders; it is not a full tree-decomposition vtree constructor. The first six serialized neighbors per round create label/shape bias and constitute a small-budget search, not exhaustive local optimization.
3. All 70 x 10 x 3 trial cells must exist before the final primary analysis. Incomplete cells fail completeness; they are not dropped. Failures are explicitly PAR2=30 seconds.
4. Baseline selection is saved after validation and checked before held-out. Split receipts and source/protocol hashes cannot be overwritten on resume, and each row carries the fingerprint. Correctness repairs require preserving invalidated runs and restarting affected campaigns.
5. For residual-work percentage reduction, baseline=0 and method=0 means 0% improvement; baseline=0 and method>0 means negative infinity (failure of the rescue criterion). Positive denominators use 1-method/baseline. The absolute wall-time saving requirement applies to all paired held-out instances. Probe SAT work counts as work for M4/M5 and is added to residual SAT work, preventing a hidden preprocessing tradeoff.
6. The native solver/library defaults are recorded in environment.json; no claim of hardware isolation or measured learned-clause reuse counts is made.
