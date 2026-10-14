# Research viability assessment — GU

From Continuous Scores to Guarded Boolean Operators: Exact Sign Quotients, Minimal Dispatch, and Fixed-Frame CM/LM Lifts

Assessment date: **2026-09-26**. Decision: **CONDITIONAL_RESEARCH**. Suggested review order: **5 of 16**.

**Recommended form:** Restricted-guard methods article or application report.

**External novelty confidence:** Moderate for the concrete separation; low for a general new abstraction framework.

## Decision and contribution

There is a useful core, but the current four-operator example is not enough to presume a substantial standalone research paper. Continue conditionally around **restricted dispatch**, where the cost and expressiveness of the permitted guard language are explicit. The general idea of quotienting parameters by the induced Boolean operator is a kernel partition, and a zero-aware collecting interpretation is standard semantic machinery. Naming these objects does not create a new abstraction theory.

The concrete example has more content. In the positive parameter quadrant, the g11 score is positive and pairwise sums constrain the other signs, leaving AND, X, Y and XNOR. The transition curves include b=a/(1+a) and b=a/(a−1), with the symmetric counterpart. A finite Boolean combination of affine guards has boundary contained in finitely many lines, so it cannot represent these curved operator boundaries exactly. Three particular polynomial/entry tests do suffice. The star of four sign patterns explains the worst-case requirement for those entry probes.

## What the theorem does and does not say

| Claim | Verdict |
|---|---|
| Four realizable operators and connected regions | Sound-looking concrete classification; independently checked interior witnesses |
| Finite affine-guard impossibility in the original coordinates | Useful restricted-language separation |
| Three chosen CM-entry probes are necessary and sufficient | Library-specific query result, not unrestricted information complexity |
| Any exact atlas needs at least three arbitrary binary predicates | Not justified: two arbitrary predicates can encode four labels |
| Generic sign cells, CAD, guard synthesis and quotienting | Established methods; need a new restriction, theorem or application |

Coordinate choice is crucial. Introducing the nonlinear feature a b can make the relevant tests linear in the lifted feature coordinates. That does not defeat the stated original-coordinate lower bound, but it prevents interpreting it as a coordinate-free impossibility. Likewise, worst-case adaptive cost at the central star pattern remains three for the permitted probes, while expected cost can depend on the parameter distribution.

[DSGRN already](https://arxiv.org/abs/1512.04131) relates finite combinatorial parameter information to regulatory dynamics, and [semialgebraic sign-condition theory](https://arxiv.org/abs/math/0603256) is mature. The [June 2026 Boolean/multilevel DSGRN preprint](https://arxiv.org/abs/2606.14925) is an especially relevant current comparison for proposed regulatory-network applications. It is a neighboring program, not evidence that its abstract contains the exact curved-boundary example here.

## Relation to prior reviews and local work

The earlier adversarial report correctly discouraged novelty claims based on Walsh expansions and generic hyperplane counting. The current nonlinear example makes a narrower, more defensible claim. Its n=1 and guard-language caveats must remain. The fresh checker verified the scores at rational witnesses for AND, X, Y and XNOR; it did not prove connectedness of every region or global minimality beyond the specified probes.

FJ owns analytic sign realizability and finite-jet rigidity. GU owns parameter-to-operator dispatch under a guard contract. CO owns execution of Boolean formulas; it should not claim this continuous-parameter guard separation as a second compiler theorem. The old guard-synthesis research brief is already part of this folder and should remain one project.

## Extensions and decision gates

1. **Certified synthesis under a priced guard library.** Fix permitted polynomial features, degrees, evaluation costs and a zero policy. Produce a method yielding an exact atlas plus a checker, and compare with general sign decomposition and decision-tree/set-cover baselines. A worthwhile result is a lower/upper cost bound for an infinite family or a documented practical improvement on a relevant application. Generic CAD followed by generic set cover is an implementation recipe, not automatically a new theorem.
2. **Robust dispatch away from boundaries.** A bound of the form min|g_i|/L_i from Lipschitz constants is elementary. The substantive target is a sharp tradeoff between cheap approximate tests, certification effort and robust regions under a fixed perturbation model. Success requires more than plotting margins for the same four regions.
3. **Application with repeated parameter queries.** Choose one actual family where operator-level compilation is reused across many parameter values. Charge feature construction and certification, compare with direct evaluation, and stop if those costs erase the reuse benefit. Keep dynamic-system claims separate from a static operator atlas unless a dynamics theorem is supplied.

The next decision should be whether such a motivated family exists. Without it, retain the current result as a compact methods note or worked example in the foundations material; do not expand it into several small papers.

## Evidence and review limits

Current source lines 494–615 and surrounding extraction definitions; prior and unpacked fresh adversarial reviews; four rational region witnesses checked anew.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [Guarded Boolean Operator (Paper B)/01_CURRENT_MANUSCRIPT_AND_REVIEW_20260924/guarded_boolean_operator_atlases_restricted_dispatch.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Guarded Boolean Operator (Paper B)/01_CURRENT_MANUSCRIPT_AND_REVIEW_20260924/guarded_boolean_operator_atlases_restricted_dispatch.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `9bd663f95fb8505bd9dd0d9cadf30b4fb1ca4e319b1547da78a084c456c4d198`.
- [Guarded Boolean Operator (Paper B)/01_CURRENT_MANUSCRIPT_AND_REVIEW_20260924/PRIOR_ADVERSARIAL_REFEREE_REPORT.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Guarded Boolean Operator (Paper B)/01_CURRENT_MANUSCRIPT_AND_REVIEW_20260924/PRIOR_ADVERSARIAL_REFEREE_REPORT.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `a2fc83811b9bc4134e0bbb7d9394a94d80584b216f4f6d5f6afbb34d68634387`.

### Primary-source comparisons

- [Cummins et al. — Combinatorial Representation of Parameter Space for Switching Networks](https://arxiv.org/abs/1512.04131). Inspected: Abstract and primary-source excerpts. Comparison: Finite combinatorial parameter regions for regulatory dynamics predate GU.
- [Cummins et al. — Boolean models coarsely sample continuous dynamics of regulatory networks](https://arxiv.org/abs/2606.14925). Inspected: Abstract; submitted 2026-06-12. Comparison: A current comparison for Boolean/multilevel regulatory model extensions, not an exact duplicate of GU’s guard-library theorem.
- [Basu, Pollack and Roy — An asymptotically tight bound on the number of connected components of realizable sign conditions](https://arxiv.org/abs/math/0603256). Inspected: Abstract. Comparison: Semialgebraic sign conditions and cell counts are established machinery.
