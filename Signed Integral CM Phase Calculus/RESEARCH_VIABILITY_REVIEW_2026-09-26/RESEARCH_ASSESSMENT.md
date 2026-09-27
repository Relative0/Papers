# Research viability assessment — SP

CM Phase Calculus Verified: Signed and Integral Lift

Assessment date: **2026-09-26**. Decision: **KEEP_TECHNICAL_COMPANION**. Suggested review order: **12 of 16**.

**Recommended form:** Signed-integral translation tutorial and correction note.

**External novelty confidence:** Low for core algebra/circuit novelty; useful explanatory boundary results.

## Decision and contribution

Keep as a technical companion or tutorial. Its most useful result is a disciplined explanation of **which scalar changes preserve which operations**. It does not establish a new physical quantum theory or a new efficient quantum algorithm. Recovering familiar circuits after mapping an integral group algebra to complex numbers is a representation result unless an additional algorithmic or verification benefit is demonstrated.

Z[C4] supplies a common source with different quotients, including F2[C4] and Z[i]. That is not an embedding of the characteristic-two phase algebra into the complex numbers. The characteristic obstruction is immediate. An intertwining identity such as Q P=J Q correctly transports the cyclic action through a quotient, but is standard linear/algebraic structure rather than a standalone novelty claim.

## What remains useful

| Material | Value | Scope limit |
|---|---|---|
| Native phase algebra versus signed/complex realization | Prevents scalar-domain confusion | No unchanged “Boolean quantum” interpretation |
| Global Hamming-preserver classification | Concrete consistency boundary | Standard permutation/commutant mechanism |
| Weight-four shell enumeration and no-fringe result | Reproducible finite architecture result | Does not quantify over every possible architecture |
| Failed masks, nilpotent splitter and Hadamard obstruction | Good minimal counterexamples | Not universal impossibility results for enriched models |
| Exact signed circuit translations | Educational and potentially verifiable | Established exact-synthesis and path-sum competition |

The bad conditional mask kills a coordinate rather than behaving like a reversible controlled gate. A nilpotent splitter cannot be treated as an invertible Fourier/Hadamard analyzer. These examples are useful because they expose specific mistakes, not because every failed construction deserves a separate no-go theorem. Counts such as 512 shell preservers belong to the declared finite search universe; the whole classification was not rerun for this review.

[Giles–Selinger](https://arxiv.org/abs/1212.0506) already gives exact Clifford+T synthesis over the relevant complex coefficient ring. [Amy’s path-sum verification](https://arxiv.org/abs/1805.06908) and [later equational theories](https://arxiv.org/abs/2306.16369) are direct comparators for any proposed symbolic translator. This review inspected their primary abstracts/records, not every algorithmic detail, so it does not claim an exhaustive implementation comparison.

## Local ownership

IP owns the intrinsic characteristic-two group algebra. SP explains an integral source and signed/complex images. BR owns the logical scalar-enrichment specification. AU should remain the single canonical home for model-boundary corrections and regression counterexamples; this document can explain the examples without claiming their discovery a second time. P02’s oracle bounds are not invalidated by transporting a different circuit model through a different quotient.

The earlier handoff is valuable provenance, but favorable reports and finite enumerations do not supply evidence of physical realizability, a Born rule or a speedup. The appropriate decision is to keep the accurate translation story while narrowing the research ambition.

## Possible extensions

1. **Checked cross-domain translation.** Specify an input circuit language, coefficient ring, quotient map and output semantics. Emit a certificate that a small checker verifies. Compare directly with existing path-sum/exact-circuit tools on the same task. Success is a new supported translation, clearer certificates, or a measured practical benefit. A reimplementation of standard complex simulation in different notation is not enough.
2. **A tutorial of failed analogies.** Show, with minimal examples, why support, signs, probabilities, reversible gates and quotient maps are distinct. This could be a useful technical article for readers of the CM program, even with no new theorem. Stop expanding it if the audience is only the already existing audit.
3. **Generalized native-isometry classifications.** Pursue only after formulating an infinite-family result not immediately implied by coordinate permutation and centralizer theory. Repeating another fixed-size shell enumeration is low value unless it resolves a precise conjecture.

The next gate is therefore a use-case decision, not a larger circuit demonstration. If no additional verification need is identified, preserve this as a concise companion and reuse the examples in the audit/tutorial material.

## Evidence and review limits

Verified signed-integral manuscript, including lines 408–552 and native-algebra/Hamming-shell boundary results; shared phase handoff and audit corrections.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [Signed Integral CM Phase Calculus/CURRENT_MANUSCRIPT/CM_Phase_Calculus_Verified.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Signed Integral CM Phase Calculus/CURRENT_MANUSCRIPT/CM_Phase_Calculus_Verified.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `ca00b5154e52493bda80e07ca573567ada9f9afcdeaec9c047e99bab5d43aed9`.

### Primary-source comparisons

- [Giles and Selinger — Exact synthesis of multiqubit Clifford+T circuits](https://arxiv.org/abs/1212.0506). Inspected: Abstract. Comparison: Exact circuit synthesis over Z[1/sqrt(2),i] is established.
- [Amy — Towards Large-scale Functional Verification of Universal Quantum Circuits](https://arxiv.org/abs/1805.06908). Inspected: Abstract/primary record. Comparison: Symbolic path-sum circuit verification is an existing comparator to signed-integral translations.
- [Amy — Complete Equational Theories for the Sum-Over-Paths with Unbalanced Amplitudes](https://arxiv.org/abs/2306.16369). Inspected: Abstract. Comparison: Exact path-sum equational reasoning is already developed; a new translation needs a specific additional use.
