# Research viability assessment — SC

Task-Matched CM Structural Computation and Decomposition

Assessment date: **2026-09-26**. Decision: **DEFER_UNTIL_ENDPOINT**. Suggested review order: **8 of 16**.

**Recommended form:** Empirical structural-computation study or reproducibility report.

**External novelty confidence:** Low now; potential depends on a distinct endpoint and measured value.

## Decision and contribution

Defer a new paper until one concrete computational task is chosen. This folder is a research direction supported by useful artifacts and cautionary evidence, not a completed new algorithmic result. The potential lies in selecting representations or decompositions for a workload with enough repeated work to repay discovery and conversion costs. “CM structure” by itself is not a distinct endpoint or an efficiency theorem.

The earlier performance READ_FIRST report explicitly warns that some headline numbers came from supplied reports without live repository access. A reported oracle headroom factor near 1.2841 corresponds to roughly 22.1% maximum total saving before selection overhead, not an achieved production speedup. A small headroom budget makes a more elaborate selector risky. Its relevance depends on the original workload and reconciliation of later evidence.

## What the recovered artifacts establish

The shared `REPRODUCTION_SUPPLEMENT.zip` contains three historical source copies labelled as fresh runs. Those labels identify archived work; they do not mean a new campaign was executed for this assessment. I inspected the GF2 decomposition implementation member and the original P14 execution report directly.

The decomposition code has exhaustive, screened, selected and advice-off arms, serializes a reconstruction-checkable best artifact, and charges analysis/dispatch, compilation, execution and exact artifact checking. It also bounds the variable count, candidate partitions and materialization budget. Thus it is an existing implementation with a **bounded candidate universe**, not proof of a globally best decomposition across every possible partition. The distinction between the included artifact check and an independent external semantic oracle must remain explicit.

The original P14 report says no-go for the unchanged dispatcher on its tested workloads: comparison with an instrumented observer and comparison with a direct evaluator lead to different impressions. A later reconciliation file exists, so the original speed ratios should not be promoted as final reconciled measurements. The qualitative warning is enough for this decision: selector overhead and scarce selection opportunities can erase gains. No timing result was reproduced in this review.

## Non-overlap and prior art

| Candidate | Keep here? | Reason |
|---|---|---|
| Choosing an execution representation for repeated tasks | Yes, if one costed workload is fixed | Distinct empirical question |
| Correctness of pair-frame formula compilation | No, belongs to CO | Avoid duplicating compiler results |
| Rank equals XOR-separation length across a split | Background in FO | Standard matrix-rank factorization |
| Sparse ANF/structure discovery | Possible comparator-driven direction | Compare actual access models and established sparse transforms |
| Generic dispatch-learning campaign | Defer | Existing headroom/overhead evidence does not justify it yet |

[Knowledge-compilation literature](https://arxiv.org/abs/1106.1819) already distinguishes succinctness, supported operations and query cost. [ABC](https://people.eecs.berkeley.edu/~alanmi/abc/abc.htm) and other conventional Boolean representations are essential baselines. The [2026 sparse Möbius work](https://arxiv.org/abs/2602.06246) concerns adaptive real-valued polynomial recovery; it is relevant to a proposed structure-discovery task but is not automatically an equivalent F2 implementation.

## Two worthwhile paths

1. **Reusable certified decomposition artifacts.** Specify the allowed partition family and required downstream operations. Determine whether one serialized, independently checked decomposition can be reused enough to amortize its construction. Compare against direct packed tables and an appropriate existing symbolic representation. Success is a reproducible cost/space advantage under identical output semantics, or a structural condition predicting when that advantage exists. Stop if it depends on excluding discovery, reconstruction or full output costs.
2. **A rigorous negative-results report.** Reconcile the historical campaigns, archive exact revisions/configurations, and explain why an oracle selector’s apparent benefit disappears after actual selection costs. This can be useful engineering knowledge if the experiment is complete and generalizable enough to guide others. It does not require a new dispatcher or a more elaborate learning model.

A first pilot should use a prespecified held-out workload and a plain baseline, with a decision rule set before inspecting results. Do not spend effort scaling a learned selector until a cheap oracle analysis shows recoverable headroom for the chosen endpoint. That is the next research gate, not an instruction to run new experiments now.

## Evidence and review limits

Recovered performance READ_FIRST_v2 and deep compiler audit; selected source/report members of the shared reproduction ZIP; current research brief.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [CM Structural Computation and Decomposition (Research Direction)/RESEARCH_BRIEF.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Structural Computation and Decomposition (Research Direction)/RESEARCH_BRIEF.md>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `96d95f506f9e5064a801566097c9badd25168cfb55d663abb5ee927d2bdffe80`.
- [CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Compiler_Deep_Audit.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Compiler_Deep_Audit.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `f673f6e53ca106901a36bfcbcaf56bd48d7d2a4289c9f9a66e9217273d049a4d`.
- [CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Performance_Audit_READ_FIRST_v2.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Performance_Audit_READ_FIRST_v2.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `dc93ed7db3497e1bb54c1732b0be214f47348e4110bc253f0413f25c133e7a7a`.

### Primary-source comparisons

- [Darwiche and Marquis — A Knowledge Compilation Map](https://arxiv.org/abs/1106.1819). Inspected: Abstract of the 2002 work. Comparison: Representation value depends on supported queries, transformations and succinctness; one endpoint must be fixed before benchmarking.
- [Berkeley ABC — official project documentation](https://people.eecs.berkeley.edu/~alanmi/abc/abc.htm). Inspected: Official project description. Comparison: Logic synthesis and verification provide essential practical baselines for CM compiler claims.
- [Willsey et al. — egg: Fast and Extensible Equality Saturation](https://arxiv.org/abs/2004.03082). Inspected: Abstract and authors’ explanatory material. Comparison: Equality saturation is an established implementation comparator, not evidence that it wins this particular workload.
- [Erginbas et al. — Adaptive Sparse Möbius Transforms for Learning Polynomials](https://arxiv.org/abs/2602.06246). Inspected: Abstract; submitted 2026-02-05. Comparison: Adaptive sparse real-valued polynomial recovery is a current comparator; it is not the same field or access model as IP.
