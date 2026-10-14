# Research viability assessment — IP

Intrinsic Boolean CM Phase Algebra

Assessment date: **2026-09-26**. Decision: **KEEP_TECHNICAL_COMPANION**. Suggested review order: **11 of 16**.

**Recommended form:** Algebra/computation technical note, coordinated with FO and PC.

**External novelty confidence:** Low for the underlying algebra and ANF transform; finite specialized classifications need priority work.

## Decision and contribution

Retain the work, but downgrade the presumption of a standalone major research paper. The basic algebra is the familiar modular group algebra F2[C4], isomorphic to F2[u]/(u^4). Its units, nilpotent ideal chain, regular representation and cyclic coefficient action are concrete and useful, but not a newly discovered number system. The Boolean phase encoding supplies a compact way to organize familiar ANF/Möbius identities. A technical note or companion is a more realistic current form.

The manuscript has material worth preserving beyond notation: exact small group counts, the distinction between nondegenerate pairings and isotropic self-products, limits of shared nilpotent tags, and failed detector constructions. Those require careful boundaries and attribution, not automatic dismissal. The unresolved question is whether a specialized finite classification is sufficiently new and useful to support its own short article.

## Claim analysis

| Material | Assessment |
|---|---|
| F2[C4] ≅ F2[u]/u^4 and eight units | Standard group/local algebra |
| GL2 size 24,576; unitary group size 512, with monomial/nonmonomial split | Specific finite classification; retain certificates and compare relevant unitary literature |
| Global Hamming isometries | Coordinate-permutation/centralizer mechanism is standard |
| Phase encoding followed by Möbius transform | ANF in different coordinates; no free algorithmic advantage |
| Shared versus independent nilpotent tags | Useful resource distinction; truncation follows directly from ideal nilpotence |
| Small balanced-function detectors | Bounded finite findings; no general oracle algorithm established |

The identity z^b=1+δ b for a Boolean b explains why a phase transform exposes ANF coefficients. The interval transform K_f is a conjugated multiplication operator, so K_f K_g=K_(fg) follows by similarity. If a shared tag is u^p, high products vanish once their total u-degree reaches four. Replacing four by a general nilpotence index is an immediate algebraic extension, not a new theorem program. Independent tags retain interactions but their full tensor algebra grows as 4^m.

The [group-algebra unit literature](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/abs/unitary-and-symmetric-units-of-a-commutative-group-algebra/0295D70C2F7BD25DEA0CBD468614D33C) is a direct priority comparison, but the inspected abstract does not settle the exact matrix unitary classification. [Boolean Möbius transforms are established](https://arxiv.org/abs/1507.05316). The [2026 adaptive sparse Möbius paper](https://arxiv.org/abs/2602.06246) is a useful future algorithm comparator, while using real-valued coefficients and a different access model; neither equivalence nor superiority follows from the shared transform name.

## Local overlap and audit status

FO owns the Boolean CM/LM framework; IP adds convolution and phase coefficients. BR owns the typed extension from Boolean scalars, PC the process/filter/disposal contracts, and P01 the general static resource classification. P02 explicitly charges oracle access, so inspecting an already built 2^n-entry ANF here cannot be advertised as a query speedup against it. SP changes to a signed/integral source and must not be conflated with this characteristic-two algebra.

The older current manuscript predates later model-boundary corrections. Before circulation, reconcile its operational language against AU and PC. Existing finite counts are inherited reproducibility evidence; this task did not independently rerun the entire unitary or detector enumeration. The fresh ring check confirms only selected structural facts such as zero divisors and the idempotents.

## Extensions with a defensible gate

1. **Truncated dependency tracking.** Find an actual symbolic calculation where nilpotent tags intentionally discard high-order interactions while preserving exactly the requested output. Compare against ordinary truncated polynomial/automatic-differentiation representations. Success requires a theorem about information retained or measured implementation value; nilpotence alone is already understood.
2. **General detector combinatorics.** The three-variable single-detector failure and two-channel cover of the 70 balanced functions could motivate a precise covering problem. Define the allowed detectors and cost, then seek asymptotic bounds or a structural characterization. Larger brute-force tables alone are unlikely to justify another paper.
3. **A certified finite-algebra reference artifact.** Publish reproducible group and measurement tables with explicit contracts if they are useful to the companion projects. This can be valuable without a historical-firstness claim, particularly if it replaces inconsistent earlier counts.

The immediate task is selecting one of these uses and reconciling the existing manuscript, not expanding all three. If none has a clear audience or unmet need, keep IP as an attributed companion and shared computational appendix.

## Evidence and review limits

Current source lines 409–750 and phase/ANF sections; retained exhaustive classifications; shared phase handoff and AU model corrections.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [Intrinsic Boolean CM Phase Algebra/CURRENT_MANUSCRIPT/Intrinsic_Boolean_CM_Phase_Algebra.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Intrinsic Boolean CM Phase Algebra/CURRENT_MANUSCRIPT/Intrinsic_Boolean_CM_Phase_Algebra.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `3ea1b66845ac42b8dd0af22ef92e014b649d809fe080ec2338a52760915ca850`.

### Primary-source comparisons

- [Barbier, Cheballah and Le Bars — Properties and constructions of coincident functions](https://arxiv.org/abs/1507.05316). Inspected: Abstract. Comparison: Boolean Möbius/ANF transforms and structural identities predate the phase encoding.
- [Unitary and Symmetric Units of a Commutative Group Algebra](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/abs/unitary-and-symmetric-units-of-a-commutative-group-algebra/0295D70C2F7BD25DEA0CBD468614D33C). Inspected: Publisher abstract. Comparison: Characteristic-two unitary group-algebra units are a direct comparison area; the abstract alone does not settle the matrix-group count.
- [Erginbas et al. — Adaptive Sparse Möbius Transforms for Learning Polynomials](https://arxiv.org/abs/2602.06246). Inspected: Abstract; submitted 2026-02-05. Comparison: Adaptive sparse real-valued polynomial recovery is a current comparator; it is not the same field or access model as IP.
- [Schumacher and Westmoreland — Almost quantum theory](https://arxiv.org/html/1204.0701). Inspected: Relevant full-text sections on states/processes and probabilistic resolutions, including §5.3. Comparison: Mixed subspace states and process semantics already exist; strong probabilistic resolution can fail.
