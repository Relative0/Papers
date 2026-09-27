# Research viability assessment — CO

Operator-Level Boolean Computation with Correspondence Matrices

Assessment date: **2026-09-26**. Decision: **CONDITIONAL_RESEARCH**. Suggested review order: **7 of 16**.

**Recommended form:** Compiler artifact/methods report, possibly a negative-results report.

**External novelty confidence:** Low for elementary fusion algebra; conditional for a rigorously evaluated implementation contribution.

## Decision and contribution

Continue only after the implementation contract is reconciled. The algebra can support a useful compiler specification and reproducible engineering report. It does not currently establish a broadly faster Boolean compiler or a novel general theory of operator fusion. Pointwise Boolean operations on aligned truth tables are established; signed-frame/NPN normalization and small lookup-table rewriting are also familiar compiler techniques.

The structural, tabulated and hybrid modes form a sensible typed specification. Soundness is worth documenting. The stated fragment-completeness result, however, concerns a syntactically defined fragment closed under specified connectives; a structural-induction proof does not establish a maximal semantic class of all optimizable formulas. The same primitive may admit structural and tabulated derivations even if the deterministic strategy chooses one, so derivability should not be confused with unique strategy provenance.

## Implementation findings that affect publication

The most important audit is recovered under SC, not only in this folder. Its historical inspection of source revision `0ab8ffd...` records several limitations:

| Manuscript/benchmark risk | Consequence |
|---|---|
| Root compilation succeeds or the original root is passed through | Failed parent compilation does not imply optimized child folds persist |
| Support is tracked syntactically | A formula may retain variables on which its function no longer semantically depends |
| Fixed output axes may be retained and broadcast | Materialized size need not equal 2^(number of live semantic variables) |
| Multiple valid derivations, one chosen strategy | A sound inference system is not an exact account of strategy provenance |
| Protocol v3 is a design rather than an executed result | It cannot supply measured speedup evidence |

These are inherited source-audit findings, not claims about a newly fetched live repository. No performance campaign was rerun here. They are nevertheless more probative than a favorable high-level panel summary and must be addressed before an empirical publication claim. Preserve the current manuscript and audits as distinct dated artifacts.

## Local and external contribution boundaries

FO owns the general typed CM/LM semantics. CO should own one executable transformation and its correctness/performance contract. SC owns the broader decision about representations, decomposition and workload structure. A result cannot be counted once as “operator fusion,” again as “LM coherence,” and again as a generic decomposition speedup. The negative P14 dispatcher evidence is relevant to SC; it is not automatically a refutation of every pair-frame compiler transformation.

[Cheng’s Proposition 3.3](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/0224.pdf) is a direct antecedent for the raw numeric operation. [ABC](https://people.eecs.berkeley.edu/~alanmi/abc/abc.htm) and [equality-saturation systems](https://arxiv.org/abs/2004.03082) provide practical and architectural comparators, but this review did not benchmark them. [Darwiche–Marquis](https://arxiv.org/abs/1106.1819) gives the relevant principle: representation quality is relative to required queries and transformations. Comparing different output contracts can manufacture an apparent advantage.

## Extensions worth doing only after the gate

1. **One matched endpoint experiment.** Decide whether the task is scalar evaluation, repeated restriction, full truth-table materialization, or a serialized reusable artifact. Include generic small-function folding as a baseline and charge parsing, support discovery, compilation, reconstruction and validation consistently. Success is a repeatable benefit or a useful explained negative result on held-out families. Stop a speedup narrative if preprocessing and output costs erase the gain.
2. **Persistent typed intermediate representation.** If retained child rewrites are wanted, implement and specify them as a new version, not as behavior assumed of the root-only artifact. Connect a small independently checkable semantic certificate to every transformation. Four-row verification of a two-variable truth table is trivial; the engineering value would lie in composing those certificates across real inputs with reliable frame/support tracking.
3. **Amortization analysis.** For repeated queries, separate preparation and per-query costs and report the break-even reuse count when it exists. The elementary inequality based on those two costs is not itself new research; a validated workload regime could be.

## Practical gate

Before allocating another benchmark campaign, write one exact input/output/cost specification and resolve the table above against the selected implementation revision. A well-explained artifact or negative-results report can be worthwhile even without a universal speedup. If the only remaining mathematics is ordinary LUT composition, position it as implementation/exposition and avoid a separate theorem-paper claim.

## Evidence and review limits

Revised compiler source lines 169–414; compiler panel audit; CM_Compiler_Deep_Audit.md recovered in SC; retained protocol/source evidence.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [CM Computation/01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/Operator_Level_CM_Compiler_Revised_Draft.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Computation/01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/Operator_Level_CM_Compiler_Revised_Draft.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `5189ac98c826c54af4e291e0516216caffa93dc521e54bec679ee33a2e5e7fd4`.
- [CM Computation/01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/CM_Compiler_Panel_Audit_2026-09-22.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Computation/01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/CM_Compiler_Panel_Audit_2026-09-22.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `4af1ab1740d43e0673a29a8c486b156f4f1352f0e3b3d851f8248611b531f705`.
- [CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Compiler_Deep_Audit.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM Structural Computation and Decomposition (Research Direction)/01_RECOVERED_REPORTS_AND_PLANS/CM_Compiler_Deep_Audit.md>) — Cross-folder implementation audit; selected relevant content inspected. SHA-256 `f673f6e53ca106901a36bfcbcaf56bd48d7d2a4289c9f9a66e9217273d049a4d`.

### Primary-source comparisons

- [Cheng, Zhao and Xu — Matrix Approach to Boolean Calculus](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/0224.pdf). Inspected: Primary proceedings PDF, Proposition 3.3 inspected. Comparison: Pointwise outer Boolean operations on aligned truth vectors directly precede the numeric CM fusion law.
- [Willsey et al. — egg: Fast and Extensible Equality Saturation](https://arxiv.org/abs/2004.03082). Inspected: Abstract and authors’ explanatory material. Comparison: Equality saturation is an established implementation comparator, not evidence that it wins this particular workload.
- [Berkeley ABC — official project documentation](https://people.eecs.berkeley.edu/~alanmi/abc/abc.htm). Inspected: Official project description. Comparison: Logic synthesis and verification provide essential practical baselines for CM compiler claims.
- [Darwiche and Marquis — A Knowledge Compilation Map](https://arxiv.org/abs/1106.1819). Inspected: Abstract of the 2002 work. Comparison: Representation value depends on supported queries, transformations and succinctness; one endpoint must be fixed before benchmarking.
