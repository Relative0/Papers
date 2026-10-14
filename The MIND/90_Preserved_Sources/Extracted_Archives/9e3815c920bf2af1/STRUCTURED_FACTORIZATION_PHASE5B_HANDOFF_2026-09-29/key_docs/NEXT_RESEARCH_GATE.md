# Next Research Gate

## Gate decision

Proceed only with a focused **Phase 5B industrial adaptation test**, not another broad theorem sweep.

## Required next experiment

Install/use a maintained SDD implementation and an assumption-capable SAT backend. Freeze a benchmark split before tuning.

Compare:

1. standard SDD dynamic size minimization;
2. factor-exposure-only local rotations;
3. combined SDD-size + residual-SAT objective;
4. syntax-component initialization;
5. soft carrier weighting;
6. defect-support-hypergraph weighting;
7. oracle aligned upper bound on instances where exact prime partition is independently computable.

Primary held-out metric: total exact hybrid runtime. Secondary: residual SAT calls, residual variable volume, SDD size, peak memory.

## Theorem target

Do not target unrestricted pairwise defect localization. Instead target one of:

- bounded defect-support width `d`;
- bounded carrier block size `b`;
- bounded interaction/treewidth `w`;
- a class where witness support can be shrunk monotonically.

Prove either a localization query bound or a bound on residual block size after adaptation.

## Stop rule

If defect/carrier-aware objectives do not beat standard syntax/treewidth/size baselines on held-out total runtime or residual work, record a NO-GO and keep the carrier/defect theorems as a mathematical note rather than forcing an algorithm paper.
