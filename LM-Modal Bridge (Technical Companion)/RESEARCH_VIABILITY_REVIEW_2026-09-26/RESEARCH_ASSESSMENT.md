# Research viability assessment — BR

Does the Symbolic LM Calculus Canonically Induce the Modal Measurement Theory?

Assessment date: **2026-09-26**. Decision: **KEEP_TECHNICAL_COMPANION**. Suggested review order: **14 of 16**.

**Recommended form:** Typed LM-to-modal bridge specification and worked examples.

**External novelty confidence:** Low for standalone algebraic novelty; useful prevention of model errors.

## Decision and contribution

Keep this as a bridge specification, not a separate foundational research paper. Its central value is to say exactly what must be added when passing from Boolean formula-valued matrices to a ring-valued modal construction. That prevents unjustified inferences about measurement, interference and resources. Most individual algebraic facts are standard or immediate, so a new research contribution would need to come from a useful verified translation or a genuinely new operational constraint.

## Mathematical assessment

Every Boolean-ring element is idempotent. A unital map into a local ring with only idempotents 0 and 1 consequently has a very restricted image. In A=F2[u]/u^4, this prevents a Boolean valuation alone from generating arbitrary phase coefficients. The fresh finite check found exactly those two idempotents. This is a clear obstruction, but a basic one.

The matrix algebra M2(F2) and the commutative algebra A cannot be isomorphic: one is noncommutative and the other commutative; their unit counts also differ. The fact that both have sixteen elements does not identify their products. An enrichment B tensor A followed by v tensor id is a legitimate scalar-extension construction. It adds structure rather than deriving it for free from the original Boolean calculus.

The symbolic support formula is exact once a coefficient zero-test is chosen. It does not determine an instrument, a state-update law or probabilities. Nonzero support is not an additive or multiplicative homomorphism; u u³=0 already defeats multiplicativity. Basis-conjugated projectors J_i=B^(-1) P_i B have the usual projection identities. Completeness follows under the stipulated invertible-basis/unimodularity assumptions, without dividing by arbitrary nonunits. These are useful checks on a specification, not new measurement axioms.

## Local overlap and antecedents

| Material | Owner / role |
|---|---|
| Formula-valued LM pairing and valuation | Imported from FO |
| Cyclic phase ring | Imported from IP |
| Symbolic scalar extension and effect typing | BR’s specification role |
| All-bases support/resource classification | P01 |
| Process closure, filtering and disposal | PC |
| Historical invalid model identifications | AU correction ledger |

The bridge’s own primary-source ledger correctly labels several LM identities as imported. It also records that the modal support rule is an additional contract. That is a sound boundary and should remain the organizing message. Its recovered older manuscript references should not be treated as the final corrected resource theory without consulting P01, PC and AU.

[Modal process and modular-computation literature](https://arxiv.org/html/1204.0701) already provides multiple algebraic state/effect contracts. Their existence makes it especially important to identify the bridge’s exact category of objects and maps. This review did not identify a new categorical equivalence here; the nonmonoidal binary-lift issue belongs in PC and prevents a casual equivalence claim.

## Extensions worth considering

1. **Symbolic instrument checker.** Encode finite ring coefficients and verify invertibility, completeness and event-support formulas, returning small counterexamples for invalid model transformations. Compare against ordinary bit-blasting/SAT/SMT or exhaustive finite algebra. Success is a useful reusable checker on actual LM/modal examples, with verified semantics or measurable simplification. Rewriting an exhaustive loop with new notation alone is insufficient.
2. **A precise translation contract.** State which symbolic formulas, effects and tensor products are preserved under each map and which require extra choices. This can become an accessible technical article with counterexamples. It is valuable exposition even if every component theorem is standard.
3. **A general finite-algebra extension only when needed.** Classifying idempotents or scalar maps in one more small algebra is unlikely to produce a strong paper. First identify an application whose behavior depends on that distinction.

The next gate is a user-facing verification need. If none exists, keep a concise bridge note and cite it from the other manuscripts rather than expanding it into another overlapping research program.

## Evidence and review limits

Recovered bridge source lines 332–445 and 585–741; PRIMARY_SOURCE_LEDGER.md; prior adversarial package references.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [LM-Modal Bridge (Technical Companion)/01_RECOVERED_BRIDGE_PACKAGE/report/LM_Modal_Bridge_Report.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/LM-Modal Bridge (Technical Companion)/01_RECOVERED_BRIDGE_PACKAGE/report/LM_Modal_Bridge_Report.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `8da0a88544332e2939e8ed99d1ad19bfb64e09aced2213258a79148250062170`.
- [LM-Modal Bridge (Technical Companion)/01_RECOVERED_BRIDGE_PACKAGE/research/PRIMARY_SOURCE_LEDGER.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/LM-Modal Bridge (Technical Companion)/01_RECOVERED_BRIDGE_PACKAGE/research/PRIMARY_SOURCE_LEDGER.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `e314db25eee498e666cfae99b5b42013ddcaad410f0045bd8e894d41b776faba`.

### Primary-source comparisons

- [Schumacher and Westmoreland — Almost quantum theory](https://arxiv.org/html/1204.0701). Inspected: Relevant full-text sections on states/processes and probabilistic resolutions, including §5.3. Comparison: Mixed subspace states and process semantics already exist; strong probabilistic resolution can fail.
- [de Beaudrap — On computation with probabilities modulo k](https://arxiv.org/pdf/1405.7381). Inspected: Abstract, introductory model and Definition 7. Comparison: Primitive/generic state constraints and uniform complexity differ from P01’s nonprimitive static resources and P02’s exact oracle-query contract.
