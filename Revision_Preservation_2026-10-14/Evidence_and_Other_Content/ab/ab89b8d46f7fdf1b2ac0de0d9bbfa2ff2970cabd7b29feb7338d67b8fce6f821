# Research viability assessment — GR

Observation Refinement Beyond a Fixed Carrier, with Constrained Observation Design

Assessment date: **2026-09-26**. Decision: **CONDITIONAL_RESEARCH**. Suggested review order: **6 of 16**.

**Recommended form:** One observation-selection/refinement research project.

**External novelty confidence:** Low for general normal forms; moderate potential for a genuinely constrained safety problem.

## Decision and contribution

Continue only with a sharply selected problem. The general fiber normal form, redundancy criteria and adjoint tests are useful organization, but mostly specialize established order/topology machinery. The promising question is **which observations can be selected or scheduled while preserving specified topology**, under a stated predicate library and cost model. This is broader than BT, which gives a precise one-bit height-two recognition theorem on a fixed carrier.

The historical equality between observation dimension and Boolean order dimension is false. If P=Q is any nontrivial chain, no added bit is needed, while a Boolean-lattice embedding of Q still needs a positive number of coordinates. A hardness argument depending on that equality therefore does not survive. Preserve the old note as history and explicitly supersede the claim in future research; this assessment does not edit it.

## A corrected starting lemma

Let P and Q be orders on the same finite carrier V with Q contained in P. Let B be an explicitly allowed family of Boolean predicates. A selected family refines P to

`x <=_new y iff x <=_P y and b(x) <= b(y) for every selected b`.

Every selected predicate must be Q-isotone to retain Q; equivalently, its true set must be a Q-upset. Put E=P\Q, the oriented pairs that must be deleted, and define

`C_b = {(x,y) in E : b(x)=1 and b(y)=0}`.

**Lemma.** A family of Q-isotone allowed predicates realizes exactly Q if and only if its C_b sets cover E. Consequently minimum cardinality, or additive minimum cost, is exactly the corresponding cover problem for this explicit family.

**Proof.** Isotonicity prevents deletion of any Q-pair. A P-pair outside Q disappears precisely when at least one chosen predicate has the forbidden 1-to-0 direction. Covering E is therefore necessary and sufficient. If every Q-upset is allowed, the principal upset above x separates x from any y with (x,y) in E; at most |V| such predicates suffice. When E is empty the empty family is optimal.

This corrects the target, but is an elementary reformulation, not a new hardness theorem. Special allowed families need their own reductions or algorithms. Exhaustively comparing direct bit-family search with the cover optimum for 382 naturally labelled pairs through four vertices passed. That bounded check supports the implementation and edge cases, not historical novelty.

## Why topology adds a real complication

Safe individual observations need not compose safely. On a three-chain, bits 010 and 101 each give a contractible thinned complex, whereas their joint refinement is disconnected. Conversely, the five-state example retained in the notes has two individual refinements with first Betti number one while their combination is acyclic in the checked degrees and is described by a contractible complex. The fresh F2 homology checks reproduce both patterns. Homology agreement is not generally a certificate of homotopy equivalence; those notions must remain distinct in algorithms.

For carrier-changing observations, the realized-signature fiber model Q={(p,a):a in B_p} is a useful representation. Singleton monotone fibers characterize an unchanged quotient. The “union of possible profiles belongs to the fiber” test for a greatest lower fiber element and the one-bit adjoint criteria are direct order-theoretic consequences. [Quillen/Barmak fiber theorems](https://arxiv.org/html/1005.0538) give sufficient homotopy conclusions using inverse images of principal ideals, not merely point fibers. None supplies a universal necessary-and-sufficient safe-refinement test.

## Research paths with stopping criteria

1. **Constrained safe cover.** Choose a motivated predicate library, cost and safety notion: for example, a literal collapse certificate in a restricted poset class. Determine whether the cover formulation admits a structural polynomial-time case, a parameterized algorithm, or a proved hardness result. Success must go beyond restating generic set cover. Avoid claiming arbitrary homotopy equivalence is an easy decidable subroutine.
2. **Safe schedules with a fixed observation set.** A subset dynamic program over 2^m states is an immediate exact baseline once safety certificates are available. A genuine contribution would improve this under a meaningful parameter or identify a structural obstruction to all schedules. The counterexamples above show why greedy “each observation is safe” reasoning fails.
3. **Carrier-changing certificate design.** Build explicit profile fibers and compare adjoint, beat-point and principal-ideal-fiber certificates on one application. A useful negative result could separate these sufficient criteria. Simply quoting Quillen under new notation is not enough.

Do not create separate papers for general normal forms, observation design and safe scheduling before one central result is established. The existing v0.2 and ledger are a foundation for this single project. The next gate is choosing the input and safety contract; the invalid dimension claim must not be used to justify funding or a publication plan.

## Evidence and review limits

v0.2 observation-refinement classification lines 144–260 and 377–534; homological foundations; historical v0.5 and research ledger; fresh 382-pair and safety-example checks.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [General ProLT Observation Refinement (Research Direction)/RESEARCH_BRIEF.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/General ProLT Observation Refinement (Research Direction)/RESEARCH_BRIEF.md>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `93077c5abdeb842a7a38329d9ec8061eca0352b26290bfd1523ddca8ed88fae0`.
- [General ProLT Observation Refinement (Research Direction)/01_RESEARCH_NOTES/ProLT_Observation_Refinement_Classification_v0.2.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/General ProLT Observation Refinement (Research Direction)/01_RESEARCH_NOTES/ProLT_Observation_Refinement_Classification_v0.2.tex>) — Supporting source/review; selected relevant content inspected. SHA-256 `82f88c86aa44094e1f12897924da268d85d86f4ba6483ced1de1fdb051d6e74c`.
- [General ProLT Observation Refinement (Research Direction)/01_RESEARCH_NOTES/ProLT_Homological_Foundations_v0.1.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/General ProLT Observation Refinement (Research Direction)/01_RESEARCH_NOTES/ProLT_Homological_Foundations_v0.1.tex>) — Supporting source/review; selected relevant content inspected. SHA-256 `17bb8af6ce8036e34a586a587b214f711d9e334e184894fae6796a0cc4bcf3e6`.
- [General ProLT Observation Refinement (Research Direction)/OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Simultaneous_Observation_Refinement_v0.5.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/General ProLT Observation Refinement (Research Direction)/OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/HISTORY/WORKING_NOTES/ProLT_Simultaneous_Observation_Refinement_v0.5.tex>) — Supporting source/review; selected relevant content inspected. SHA-256 `0ba09c718fb97b0c30f6720c55425480f822fcd7bd4ac39d9f4e659c2ac8982c`.
- [General ProLT Observation Refinement (Research Direction)/04_RESEARCH_LEDGER/ProLT_Research_Ledger_v0.1-v0.5.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/General ProLT Observation Refinement (Research Direction)/04_RESEARCH_LEDGER/ProLT_Research_Ledger_v0.1-v0.5.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `0c6f11a1c7647fe29155868741c72b297de300a6593f4df03774071c13025ede`.

### Primary-source comparisons

- [Barmak — On Quillen’s Theorem A for posets](https://arxiv.org/html/1005.0538). Inspected: Theorems 1.1–1.2 and comparable-map discussion. Comparison: Contractible inverse images of principal ideals imply simple homotopy equivalence; this is not a literal collapse criterion.
- [Vickers — author’s publications and Topology via Logic description](https://sjvickers.github.io/papersfull.html). Inspected: Author’s book description. Comparison: Observation-based topology is a mature antecedent to ProLT’s positive-observation interpretation.
- [Bonsangue, Jacobs and Kok — Duality beyond sober spaces: topological spaces and observation frames](https://ir.cwi.nl/pub/1395). Inspected: Institutional primary record and abstract/metadata. Comparison: Observation frames are relevant prior art; exact theorem correspondence needs full-text work before a novelty claim.
