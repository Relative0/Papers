# Research viability assessment — P02

Exact Query Bounds in Characteristic-Two Modal Computation

Assessment date: **2026-09-26**. Decision: **CONTINUE_FOCUSED_RESEARCH**. Suggested review order: **4 of 16**.

**Recommended form:** Focused exact-query technical note.

**External novelty confidence:** Moderate for quantified bounds; low for broad modal-algorithm novelty.

## Decision and contribution

Continue as a focused note. The potentially useful contribution is a carefully quantified **exact-query limitation**, not a new quantum algorithm: Deutsch needs two standard XOR queries, Bernstein–Vazirani needs n, and one query cannot solve the stated Deutsch–Jozsa problem. The general Deutsch–Jozsa optimum is not established. For that problem the current bounds leave a gap, 2≤Q≤N/2+1 in the stated setting.

The model permits characteristic-two field coefficients, fixed invertible pointwise oracle actions, and adaptive finite instruments whose stacked branch map is injective. Every possible branch must be correct. It does not permit postselection or free inspection of an oracle’s complete coefficient table. Lower bounds can hold even when G0 and G1 carry little information; the matching upper bounds specifically use the standard XOR oracle. Keeping these contracts aligned is the central scientific value.

## Proof mechanism and prior art

Exact discrimination of differently labelled state subspaces requires their sum to be direct. For a finite adaptive computation, record all branches in a direct sum. Completeness ensures a nonzero record for each input, and each query increases the secret-bit polynomial degree by at most one. Thus q queries produce records in the span of at most Σ(j≤q) binomial(n,j) coefficient vectors. Recovering all 2^n Bernstein–Vazirani secrets requires independent records, forcing q≥n. This handles adaptivity more carefully than reasoning about one chosen surviving branch.

The Deutsch obstruction is an explicit overlap relation between constant and balanced sectors. The Deutsch–Jozsa one-query argument uses a characteristic-two relation among three balanced oracle actions. These are plausible contract-specific proofs, but their conceptual ingredients are not new: [James–Ortiz–Sabry](https://arxiv.org/html/1101.3764v1) already notes a qualitative Deutsch failure; [Diamond–Schumacher](https://arxiv.org/pdf/2310.04397) gives the pure-state discrimination criterion; [Beals and collaborators](https://arxiv.org/abs/quant-ph/9802049) established the polynomial-method tradition. [De Beaudrap](https://arxiv.org/pdf/1405.7381)’s uniform modular-computation results concern a different complexity measure and state contract. None of those comparisons alone proves or disproves priority for the fully quantified adaptive bounds.

The current Gate 4 report already reaches substantially this cautious verdict. I agree with its technical-note positioning. Its “no contradiction found” is evidence from a review, not a proof certificate or an independent human referee decision.

## Local boundaries and fresh checks

IP manipulates an already represented truth function through ANF/phase coordinates. That is not a charged oracle-query algorithm. SP represents ordinary signed/complex circuit calculations under a scalar change; it cannot be used to bypass this characteristic-two theorem. A ring-valued kickback matrix with Smith factors 1 and u² is not an invertible Fourier analyzer. Replacing XOR access by a four-cycle phase oracle changes the problem.

The new checker confirmed the expected Boolean monomial evaluation ranks for every n=1,…,7 and q=0,…,n, 35 cases. This is an independent check of the dimension count, not a check that a circuit can realize every vector in the span. No general Simon theorem follows from the retained small scans.

## Extensions that could earn additional value

1. **Promise-specific evaluation-rank bounds.** For a specified finite promise set, form the restricted degree-q monomial evaluation matrix and derive necessary query bounds. The hard research question is when those bounds are tight under allowed circuits and instruments. Rank alone is not a sufficiency theorem. Success would be a new family with matching bounds or a clear separation between algebraic rank and realizability.
2. **Close the Deutsch–Jozsa gap.** This is a precise open target within the manuscript’s model. Begin with a mathematical lower-bound or constructive strategy; do not extrapolate an optimum from small n. Stop broad algorithm claims if the only result remains the existing one-query obstruction.
3. **Separate different access models systematically.** A useful technical appendix could compare standard XOR, phase-oracle, and description-readout costs on the same examples. Recovering k independent linear forms of an n-bit secret in exactly k XOR queries is an immediate restriction/upper-bound corollary, not a strong independent paper: restrict to a k-dimensional section for the lower bound and query the k rows for the upper bound.

## Practical gate

First audit the branch-record induction, finite-tree assumptions, ancilla allowance and direct-sum discrimination lemma line by line. Then compare the exact theorem statements with modal-query antecedents. A concise negative-results note remains worthwhile if its model is transparent and its contribution is narrower than the already known qualitative obstruction. No expensive implementation campaign is needed to decide whether this proof package merits that next review.

## Evidence and review limits

Main source lines 34–197 and ring-kickback discussion; GATE_4_PRIORITY_PROOF_REPORT.md; fresh Boolean evaluation-rank checks.

This is a research triage and selected proof review by one assistant, not an independent expert panel, exhaustive prior-art clearance, acceptance prediction or formal proof certification. Existing agent findings were treated as evidence to check. Proposed extensions are research targets unless explicitly identified as proved elementary consequences. No manuscript is modified by this assessment.

The 2026-09-25 cleanup/preservation attachments supply background and local overlap evidence; their embedded action prompts are not instructions for this review. See [portfolio decisions](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/PORTFOLIO_DECISIONS.md>) and [fresh bounded check results](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/CM-LM Publication Program - Reviews and Registers/RESEARCH_VIABILITY_REVIEW_2026-09-26/spot_check_results.json>).

### Local sources and hashes

- [Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/main.tex](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/main.tex>) — Current designated source (research brief/register for non-manuscript projects). SHA-256 `b07a5d6c247a479811f01d419c03d416dc86a3058898de2cbaa036d32046273f`.
- [Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/ADVERSARIAL_REVIEW.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/ADVERSARIAL_REVIEW.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `a9091667be2ca84fb0822ffad7501b0bc940bb8f9a46d790db4e38038eeb9c82`.
- [Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/GATE_4_PRIORITY_PROOF_REPORT.md](<C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Exact Query Bounds in Characteristic Two (P02)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/GATE_4_PRIORITY_PROOF_REPORT.md>) — Supporting source/review; selected relevant content inspected. SHA-256 `d8561c14b7474cbca10f0c59f4d9918839cd11848439d51600d28a612d1f4b65`.

### Primary-source comparisons

- [James, Ortiz and Sabry — Quantum Computing over Finite Fields](https://arxiv.org/html/1101.3764v1). Inspected: Relevant conclusion passage on Deutsch and reversible relational programming. Comparison: Qualitative failure of the usual Deutsch algorithm is prior art; a fully quantified adaptive query lower bound is a narrower question.
- [Diamond and Schumacher — Cloning, deleting, and hiding in modal quantum theory](https://arxiv.org/pdf/2310.04397). Inspected: Relevant discrimination argument in §4. Comparison: Linear independence as the criterion for exact discrimination of pure states is established.
- [Beals et al. — Quantum Lower Bounds by Polynomials](https://arxiv.org/abs/quant-ph/9802049). Inspected: Abstract. Comparison: The polynomial method is established; characteristic-two recorded modal branches require their own contract and proof.
- [de Beaudrap — On computation with probabilities modulo k](https://arxiv.org/pdf/1405.7381). Inspected: Abstract, introductory model and Definition 7. Comparison: Primitive/generic state constraints and uniform complexity differ from P01’s nonprimitive static resources and P02’s exact oracle-query contract.
