# Semantic contracts for compiling differentiable logic

Initial novelty and feasibility assessment for Brian, 13 October 2026, Asia/Bangkok.

## Recommendation

**Merge the established material into the existing CM compiler manuscript; reshape the independent-paper proposal before pursuing it.** A useful research question survives, but the present evidence does not justify a separate paper claiming a new general semantic compiler, a new dependence treatment, or a new classification of differentiable logic. Exact probability compilation, algebraic circuit contracts, typed differentiable-logic languages, and training/verification correspondence all have close and substantial antecedents.

The best immediate addition is a narrowly stated boundary: the existing compiler's Boolean soundness does not authorize replacing a recursive soft objective with the real expectation of its compiled truth token. Attach an exact diagnostic and conservative admission conditions. A standalone methods paper would require a scalable translation validator that handles shared context, parameter maps and actual derivative policies, together with compelling evidence of practical utility against ordinary expression DAGs and circuit tools.

Target readers are neuro-symbolic programming and compiler-verification researchers. A small explanatory addition belongs in *Operator-Level Boolean Computation with Correspondence Matrices*, after the pair-compiler soundness/admissibility boundary. The CM/LM calculus can receive a brief remark contrasting Boolean valuation with real expectation, but should not acquire a second compiler paper inside its foundations argument. Guarded dispatch contributes only an optional decision-preservation contract; whole-orthant regularity and guard-complexity research remain outside this dossier.

**Novelty assessment:** high confidence that the elementary bridges and broad architecture are already established; moderate confidence that the specifically proposed diagnostic integration is useful; low confidence that it is independently publishable without implementation and stronger evidence. These are judgments, not measured probabilities or historical-priority findings.

## Evidence, versions and research scope

The orientation material was read first: `output/pdf/palo_cm_relationships_2026-10-13/palo_cm_relationships.tex`, its README and inventory. The source report's 40,668 assertions were not rerun here and are not evidence for the new proposal. Decisive claims below were checked against original passages.

Local source fingerprints and complete paths are in [local_source_inventory.json](local_source_inventory.json). All four inspected PDFs match the handoff hashes exactly:

| Source | Version used | Decisive locators |
|---|---|---|
| PALO | Supplied 57-page author manuscript; journal JLAMP 124, 100719 (2022), DOI 10.1016/j.jlamp.2021.100719 | pp. 16–17; §§3.5–3.8, pp. 23–27; §4, pp. 28–29; p. 43 |
| CM/LM | 27 September 2026 revised final bundle, 32 pages | §§2.1–3.3, pp. 3–8; Theorems 4.4–4.5, p. 9 |
| Compiler | 26 September 2026 contract revision, 19 pages | Theorem 1, p. 3; §§4.1–4.3, pp. 4–6; Table 1/pseudocode, p. 7; baseline discussion, p. 10; empirical boundaries, pp. 12–15 |
| Guarded dispatch | 28 September 2026 reviewed package, 14 pages | Peripheral source; no new guard-complexity claim relies on it |

The LM and compiler folders' `README_FIRST.md` files explicitly select these versions. The LM final-bundle README confirms the 32-page revision. The compiler revision README and current-study navigation identify the contract revision as current and distinguish later natural-circuit evidence from a newer manuscript. Their scoped PDF inventories did not reveal a competing current manuscript. Modification time was not used as a version selector. The LM `CLAIMS_AND_UNIQUENESS.md` still points to September 22 material and has older outstanding-work wording; it is historical context, not authority over the explicit September 27 entry point.

The checked-out `cm_ir.py` was also inspected read-only. Its existing Boolean XOR duplicate cancellation and `make_eqv`/`make_imp` equal-child folds illustrate concrete surfaces that would need mode separation before any soft reuse. This is **not a bug report**: those functions implement Boolean semantics, and this dirty checkout is not the compiler paper's pinned implementation snapshot.

No applicable on-disk AGENTS.md was found at the project/output ancestors or within the two principal manuscript folders. Brian's supplied global instructions and this direction's exclusive-write restriction governed the work. Initial Git state is recorded in [git_status_initial.txt](git_status_initial.txt); extensive changes predated this research. All created files are in this exclusive folder. Source manuscripts and sibling outputs were untouched.

The search covered primary papers and publication records available through 13 October 2026. It followed backward references from SPL and the 2024 semiring paper to AMC, and forward connections from AMC and semantic loss to Scallop, circuit atlases, and algebraic gradients. It also followed the 2026 QLL paper to its foundations and Vehicle. This was a focused full-passage review, not an exhaustive citation-index census. Exact searches and access limitations are in [research_log.md](research_log.md). Author/current-version arXiv PDFs are cached privately with SHA-256 hashes in [external_source_inventory.json](external_source_inventory.json); they are research inputs, not a redistribution package.

## Closest primary work and precise overlap

Each comparison distinguishes what was actually established from what remains available to this project. Bibliographic records are in [references.bib](references.bib).

### PALO itself

PALO defines the recursive product/probabilistic-sum semantics on pp. 16–17, explicitly states the independence approximation, and acknowledges the failure of idempotence, absorption and distributivity. Its primitive equivalence deliberately differs from the conjunction of two material implications. Sections 3.5–3.6 already discuss repeated-variable examples, probability bounds and changes to objectives caused by classically equivalent theories. Page 28 describes Maude preprocessing using classical semantics. A compiler contract is therefore a possible additional engineering discipline, not a discovery of an unrecognized logical inconsistency. The journal metadata are confirmed by the [author's SRI publication list](https://www.csl.sri.com/users/mkim/pub.html).

PALO's crisp operator is applied inside the interpretation, with the convention `value >= threshold`; this was visually verified on PDF p. 26. It is not final-only thresholding. Page 28, note 29, says the prototype had not implemented full posterior-distribution semantics. No present-day LIME implementation audit or training replication was performed.

### Xu et al., semantic loss, ICML 2018

[Full paper](https://proceedings.mlr.press/v80/xu18h/xu18h.pdf), [publication record](https://proceedings.mlr.press/v80/xu18h.html); PMLR 80, 5502–5511. Definition 1 (§3.1, PDF pp. 2–3) is negative log weighted model count under independent base variables. Proposition 2 (§3.2, p. 3) establishes syntax independence. Section 5 discusses compiled constraint evaluation; p. 5 contrasts syntax-sensitive fuzzy encodings. Thus a CM truth tensor followed by product-distribution evaluation and a logarithm does not supply a new semantic loss or a new syntax-independent learning objective. Our proposed validator instead compares this event semantics with a separately declared recursive soft objective; it should preserve either when requested rather than automatically replacing one by the other.

### Kimmig, Van den Broeck and De Raedt, AMC

[22-page author manuscript](https://starai.cs.ucla.edu/papers/KimmigJAL16.pdf), [repository record](https://escholarship.org/uc/item/2w76d6hr). Journal of Applied Logic 22, 46–62 (2017), DOI 10.1016/j.jal.2016.11.031; the inspected author PDF is dated 28 July 2016. Theorem 2 (§3.1, p. 12), Theorems 3–7 (§§3.2–3.3, pp. 13–15), and Table 2 already classify safe circuit evaluation using determinism, decomposability, smoothness and semiring properties. Section 3.5 (pp. 17–19) distinguishes sums over models from sums over derivations with repeated variables. This is decisive overlap with broad dependence-aware compilation and occurrence tracking. Those theorems concern AMC evaluation, not PALO's recursive probabilistic-sum connective; the latter's conjunction does not distribute over its disjunction, so those two operations cannot simply be called the AMC semiring.

### Derkinderen et al., semirings for PLP and NeSy, 2024

[Full version](https://arxiv.org/pdf/2402.13782v1), [arXiv/publication metadata](https://arxiv.org/abs/2402.13782). IJAR 171, 109130 (2024), DOI 10.1016/j.ijar.2024.109130. Sections 3.2–3.3, Definitions 10–12 and the sd-DNNF-to-arithmetic-circuit construction explain the logical, compilation and algebraic evaluation stages. Section 4.1, Equations 10–16, gives gradient-semiring evaluation. This subsumes a proposal whose main result is merely a typed Boolean/probability/gradient pipeline. The legitimate distinction is a tool checking transformations between *different selected* interpretations, including an interpretation that is intentionally not an AMC evaluation.

### Scallop, PLDI 2023

[44-page author paper](https://www.cis.upenn.edu/~jianih/res/papers/pldi23_scallop.pdf), [conference record](https://pldi23.sigplan.org/details/pldi-2023-pldi/61/Scallop-A-Language-for-Neurosymbolic-Programming). Li, Huang and Naik, PACMPL 7, PLDI, article 166. Section 4 gives a provenance framework; §4.5, PDF pp. 13–14, gives differentiable provenances. The top-k proof mode retains Boolean formulas and evaluates them by differentiable WMC; duplicate/conflicting literals are handled during proof combination. Therefore dependency IDs, formula provenance and dual-number propagation are strong baselines. Figure 12 and §4.5.2 also explicitly keep the derivative unchanged through clamping in the additive mode. That chosen derivative policy illustrates why forward-function equality alone cannot certify the actual backward computation. A proposed checker must declare whether it verifies mathematical derivatives, library tie rules or surrogate gradients. No Scallop execution was performed.

### SPL, NeurIPS 2022

[Full author version](https://arxiv.org/pdf/2206.00426), [proceedings](https://proceedings.neurips.cc/paper/2022/hash/c182ec594f38926b7fcb827635b9a8f4-Abstract.html). Ahmed, Teso, Chang, Van den Broeck and Vergari. Sections 3.1–3.3, Definition 3.7 and Theorem 3.1 (PDF pp. 4–6), plus Appendix A (p. 15), give correlation-capable probabilistic circuits, constraint circuits and compatibility requirements for efficient products/normalization. Exact inference is O(|q||c|) under the stated conditions; MAP additionally requires determinism. Appendix B explains compilation, with possible exponential size. A CM library adds neither this correlated distribution model nor these constraint guarantees. SPL is a probability-mode baseline; replacing a recursive soft loss with SPL is a model change, not an optimization preserving that loss.

### Circuit atlases, 2021 and 2024

Vergari et al., [NeurIPS 2021 paper](https://papers.nips.cc/paper/2021/file/6e01383fd96a17ae51cc3e15447e7533-Paper.pdf), §3, Table 1, Theorems 3.1–3.2 (PDF pp. 4–5), gives sufficient structure and hardness boundaries for circuit products and other operations. Wang, Mauá, Van den Broeck and Choi, [NeurIPS 2024 record](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ff9c70659c39cdd801dd5f5a1201c29e-Abstract-Conference.html), [current arXiv v2](https://arxiv.org/pdf/2412.05481v2), extends this to algebraic circuits. Theorem 4, PDF p. 6 and Appendix A.3, pp. 19–20, gives mapping conditions using homomorphisms or structural restrictions; Theorem 5 carries properties through compositions. Generic compositional semantic contracts and mappings across algebras are therefore occupied territory. The prospective contribution must handle the narrower soft-objective and actual-gradient validation problem with demonstrated benefit.

### Vehicle, FSCD 2025

[Published full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol337-fscd2025/html/LIPIcs.FSCD.2025.2/LIPIcs.FSCD.2025.2.html), [record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSCD.2025.2). Daggitt et al., LIPIcs 337, 2:1–2:20, invited talk paper. Sections 4.1–4.2 describe dependent typing and backend-specific compilation. Section 4.2.4 reports Agda formalization of compilation soundness for training and verification targets and a logical correspondence between them. Section 5 identifies remaining certificate and quantization issues. A typed IR plus multiple backends and a generic soundness claim is not sufficient novelty. Vehicle does not, in these inspected passages, assert arbitrary real-objective equality or identical gradients across every classically equivalent source rewrite. That narrower translation-validation target remains a question, not an established absence from its full codebase.

### Differentiable-logic foundations and QLL, 2026

Affeldt et al., [v1, 27 February 2026](https://arxiv.org/abs/2602.23878), submitted to JAR according to its record: §5, PDF p. 17, has intrinsically typed generic syntax; §§6–8 formalize algebraic, analytic and proof-theoretic properties, including Theorem 8.1 (p. 33). Flinkow et al., [QLL v2, 14 May 2026](https://arxiv.org/pdf/2605.13845v2): §3, Tables 2–3, pp. 6–7, distinguishes law preservation, bounded idempotence defect and gradients; Theorem 3.7 concerns the infinite-hardness Boolean limit, not unrestricted finite-hardness equality. Its evaluation (§4, p. 8 onward) separates attacks from verification. Neither a generic law/gradient tradeoff nor approximate idempotence is new here.

Capucci et al., [*Adequate Losses via Quantitative Linear Logic*, current v3, 16 July 2026](https://arxiv.org/pdf/2605.13348v3), §§5.1, 6.3, Theorem 6.4 (pp. 34–35), connects quantitative satisfaction and provability. Pages 35–36 connect it explicitly with Vehicle. This is a major forward-literature constraint on an ambitious “first semantic foundation” framing. The present dossier does not independently validate all QLL proofs or experimental claims, and records these two QLL works as preprints rather than assuming journal acceptance.

### Gradients, conditional rewrites and numerical verification

Maene and De Raedt, [AAAI 2025 record](https://ojs.aaai.org/index.php/AAAI/article/view/34132), [full paper](https://arxiv.org/pdf/2502.18406v1), §3 and Theorem 2/Algorithm 1 (§4, p. 4), already generalize gradients and algebraic backpropagation. van Krieken, Acar and van Harmelen, [full paper](https://arxiv.org/pdf/2002.06100), *Artificial Intelligence* 302, 103602 (2022), §4 and §§7–8, distinguishes recursive semantics and analyzes gradient behavior. These defeat a standalone claim based on differentiating compiled probability polynomials or noticing syntax-dependent gradients.

[egg, POPL 2021](https://cnandi.com/docs/popl21-cr.pdf), §§4.1–4.3 (PDF pp. 13–16), provides analyses, conditional/dynamic rewrites and extraction. It is an appropriate infrastructure baseline, not a source of automatic soundness for user-supplied rewrite rules. Daisy's [author repository](https://github.com/malyzajko/daisy) documents sound roundoff analysis and rewriting/mixed-precision work; the selected full-paper fetch failed, so no theorem-level priority conclusion is drawn from its search excerpt. Numerical certification remains an explicit obligation for an implemented floating-point backend.

## Preferred question and concrete candidate algorithm

**Preferred question:** Can a bounded-cut translation validator for differentiable-logic optimizers carry semantic-mode, context and parameter metadata, then accept an optimization only when an exact or bounded value/gradient/decision contract survives composition through a shared DAG?

Prefer an add-on checker over a replacement compiler. Preserve the existing Boolean pipeline, but give each candidate transformation a request such as `Boolean`, `RecursiveSoft(PALO-polynomial)`, `Event(mu)`, `Gradient(parameterization, derivative_policy)` or `Decision(domain, threshold, placement)`. A request can contain several contracts. Satisfying one must not silently discharge the others.

Candidate certificate fields are source/target fingerprints, primitive semantics ID, truth-state order and frame, variable/occurrence IDs, **separate event IDs and parameter IDs**, event-model ID, boundary-context variables, domain assumptions, sample/batch identity where relevant, threshold placement and tie rule, arithmetic model, derivative policy, residual evidence, and provenance for every composed step. This specification is proposed; the supplied Python checker is an executable mathematical core, not a complete typed IR or certificate security layer.

Candidate algorithm:

1. Obtain a bounded local cut from an expression DAG without changing the source objective. Record sharing and all consumers. Validate axis/polarity transport.
2. Check Boolean equality using a small table/BDD/circuit. In event mode, also establish contextual event equivalence or a sufficient joint-boundary signature; equal node marginals alone are insufficient.
3. For the declared polynomial recursive semantics, build exact rational sparse normal forms after the declared parameter/alias substitution. Compute the residual `Delta = source - target`. Zero coefficients certify universal value equality. A nonzero residual produces an exact rational counterexample on a degree-complete interior grid.
4. For permitted approximations on a rational box, bound both Delta and its input derivatives, then lift them through declared parameter Jacobian and downstream-context bounds. Bernstein coefficients are one conservative mechanism. Reject or return unknown if the required assumptions cannot be discharged.
5. Check final-threshold margins separately, or use the recursive-crisp contract with its own threshold locations. Store intentional semantic changes as reformulations, never as objective-preserving optimizations.
6. Account for checking, recognition, expansion, fallback and certificate replay costs. Cap cut size, degree and coefficient growth. A rejected/unknown rewrite retains the original expression.

This combines known mechanisms. The possible methods contribution is their careful integration and usefulness under realistic shared objectives. It is not yet established that this combination offers a publishable capability unavailable through existing tools.

Alternatives: (a) a restricted Boolean-token folding admission theorem and diagnostics, suitable for the existing compiler; (b) a PALO/LIME preprocessing audit with objective-change manifests, requiring an accessible current implementation and source-level examples; (c) approximate C1-preserving rewrite extraction, requiring sound nonlinear/Jacobian bounds; (d) context-aware joint-probability cut replacement, likely best built on existing circuit compilers. Do not pursue all four as simultaneous paper claims.

## Assumptions and exact results reconstructed here

The exact checker covers **finite propositional pure expressions** with constants, negation `1-p`, and bilinear extensions of Boolean binary tables. Variables are named soft inputs in [0,1]. Coefficients use exact rationals and arithmetic denotes real arithmetic. There are no quantifiers, neural attachments, stochastic/stateful evaluations, sampled training, logs, min/max, division or floating-point kernels in this prototype. PALO's geometric mean, maximum and batch semantics require separate rules. A symbolic polynomial counterexample in free inputs need not be attainable by a particular neural parameterization.

The following are proved derivations/baselines, **without novelty claims**. They explain what a checker can certify and where a proposed theorem would still need work.

### A. Universal soft-preserving Boolean table folding

Let `s_E(p)` be the recursively computed polynomial for expression E. Let `b_E` be its Boolean function and `B_E` its independent-base-variable multilinear extension. Define M on polynomials by replacing every positive exponent in each monomial by 1 and combining coefficients. Then

`M(s_E) = B_E`, and `s_E = B_E on [0,1]^n` iff `s_E` is affine separately in every distinct base input.

Proof: M(s_E) agrees with s_E at every Boolean corner and is multilinear. Bilinear kernels agree with their declared Boolean tables at corners. A multilinear polynomial is determined by its corners. Conversely, equality on the full cube gives polynomial identity, so s_E has no higher coordinate degree after cancellation. This is an arbitrary-arity criterion, not enumeration of sixteen gates. It is an elementary consequence of Boolean polynomial reduction and interpolation, not a new classification theorem.

Read-once/disjoint-support compositions satisfy the criterion inductively. This is sufficient, not necessary: ignored operands or algebraic cancellation may remove apparent support. A four-bit token cannot represent every recursive soft polynomial over two variables: Boolean corners discard the higher-degree part. Event-table contraction changes the objective precisely when that discarded part is nonzero.

### B. Residual certificates and counterexamples

For Boolean-equivalent E,F, their soft residual vanishes on corners, and admits

`Delta = sum_i (p_i^2 - p_i) H_i(p)`.

The script constructs H_i by telescoping monomial reductions and checks the resulting exact identity. This explains why a Boolean test suite can miss the entire soft discrepancy. It is ordinary ideal membership in the Boolean cube's vanishing ideal; it is not a new algebraic result.

If Delta has coordinate degrees d_i and is nonzero, an interior tensor grid containing d_i+1 distinct rational values in coordinate i must contain a witness. Induct on the number of variables using the univariate root bound. The script chooses `(j+1)/(d_i+2)` for j=0,…,d_i. This gives a **complete rejection procedure for explicit bounded-degree polynomials**. It is not a generally efficient circuit-identity algorithm: polynomial expansion and the grid may both be exponential, and rational coefficient bit length matters.

### C. Probabilistic equivalence and the contextual trap

Boolean equality E=F implies equal expectations under every specified joint model on the same base events. Conversely, equality under every joint model implies Boolean equality by choosing point masses. Fixed-model expectation equality is much weaker and is not a contextual congruence.

For fair independent X,Y, `P(X)=P(Y)=1/2`, but the contexts `X and X` and `X and Y` have probabilities 1/2 and 1/4. A safe fixed-model rule can require E=F almost surely. More generally, for a declared boundary random vector Z, equality of the joint laws `(E,Z)` and `(F,Z)` is necessary and sufficient to preserve `E[h(E,Z)]` for **all** Boolean boundary contexts h. Sufficiency follows by integration; necessity follows by testing indicators of each joint state. This is a standard finite-probability characterization, not a novel theorem. Efficiently constructing/checking such signatures is the research obligation.

For a parameterized model mu_theta, equality at one theta does not certify gradients or training. Require equality over the parameter domain and differentiability, with identical evidence/conditioning and normalization. Distinct independent Bernoulli events can have the same parameter p without becoming the same event. Event IDs, source sharing and parameter tying therefore need distinct metadata.

### D. Gradients, parameter maps and composition

Exact C1 function equality on an open neighborhood, followed by the **same** differentiable parameter map p(theta), implies equal mathematical parameter gradients by the chain rule. Equality only at sampled values, only on a lower-dimensional set without checking the actual pullback, or only after Boolean corner restriction does not. Polynomial parameter maps can be substituted and checked exactly; generic neural maps require a different validation method.

Equal forward functions are not enough for arbitrary library/custom backward rules. Clamp straight-through derivatives and min/max tie rules must be included in the gradient contract. CSE of a pure shared expression preserves its value, but reverse-mode differentiation must accumulate contributions from every consumer. Deduplicating repeated operands through Boolean idempotence is a different transformation.

For approximate composition, let downstream scalar K be C2 on a convex domain containing u(theta) and v(theta). Suppose `||u-v|| <= epsilon_v`, `||J_u-J_v|| <= epsilon_J`, `||J_v|| <= B`, `||grad K|| <= M`, and `||Hessian K|| <= H` in compatible induced norms. Then

`|K(u)-K(v)| <= M epsilon_v`,

`||grad_theta K(u)-grad_theta K(v)|| <= M epsilon_J + H B epsilon_v`.

Proof: use the mean-value bound for K and its gradient, and split `J_u^T grad K(u) - J_v^T grad K(v)` into `(J_u-J_v)^T grad K(u) + J_v^T(grad K(u)-grad K(v))`. Sharing multiplicity must be represented in u,v and their Jacobians. These standard sensitivity bounds are not implemented as a general DAG algorithm here. Nonsmooth K needs branch/tie analysis; log losses need a positive lower probability bound. No claim about identical optimization trajectories or final learned models follows from a local tolerance alone.

### E. Decision contracts

For final threshold `1[value >= tau]`, `|source-target| <= epsilon` and a uniform source margin strictly greater than epsilon suffice for identical decisions. Equality of Boolean corners alone does not. Alternatively, bound both functions entirely on the same side of tau in each certified box.

PALO's recursive crisp interpretation is a different contract. In the propositional fragment, with `0 < tau < 1`, crispify atomic inputs and retain Boolean intermediate operations; Boolean-equivalent formulas then agree. Do not transfer this statement to PALO's quantified/batch-mean semantics without checking its aggregation rules. The endpoint tau=0 is excluded because it maps Boolean false to true.

## Falsification attempts and exact checks

[semantic_contract_checker.py](semantic_contract_checker.py) is a self-contained standard-library prototype. [checker_results.json](checker_results.json) records **42,918 passing assertions**, **12,288 operator compositions**, 17 named rewrites and 17 correlated-expectation examples. The last run used the existing project `.venv/Scripts/python.exe`; measured runtime was approximately 11.4 seconds on this machine. That timing is merely a diagnostic run duration, not a benchmark comparison.

| Composed circuit family | Enumerated | Soft-preserving whole-table folds | Rejected |
|---|---:|---:|---:|
| Two children on the same two-variable frame | 4,096 | 2,216 | 1,880 |
| Children with one shared base variable | 4,096 | 2,656 | 1,440 |
| Children with disjoint two-variable supports | 4,096 | 4,096 | 0 |

Each family enumerates every outer Boolean binary table and both inner tables. The checker compares polynomial reduction with an independent Boolean evaluator and direct corner interpolation. The families include constant and projection gates, so these counts do not estimate failure rates in natural workloads. They confirm the criterion on bounded examples and disprove blanket admission by frame equality.

Serious attempted counterexamples:

- **Idempotence:** recursive AND(p,p)=p² versus p. Boolean/event equality passes; soft equality fails. On [0,1/100], Bernstein bounds give value error <=99/10000 and derivative error <=1. Small value error does not entail a small gradient error.
- **Implication expansion versus equivalence expansion:** implication equals `not p or q` exactly under PALO kernels. Primitive equivalence versus the product of two material implications fails: at p=q=1/2 the values are 1/2 and 9/16. The checker generates an exact witness and coefficient residual.
- **The existing compiler's own worked fusion:** `(X implies not Y) xor (not Y implies X)` compiles to Boolean equivalence (compiler p. 6). Under recursive bilinear soft kernels, at p=q=1/2 its value is 3/8 versus 1/2 for primitive equivalence. Correct Boolean fusion does not certify the relaxed objective.
- **Distribution:** `p and (q or r)` minus `(p and q) or (p and r)` is `-p(1-p)qr`. It vanishes at every Boolean corner but can reach -1/4.
- **Parameter restrictions:** equivalence expansion becomes exact on q=1. The polynomial pullback verifies this. A universal free-input checker can reject a rewrite that is safe for a restricted parameter map; it must distinguish rejected-universal from rejected-on-this-model.
- **Parameter tying versus event aliasing:** substitute independent event probabilities p=q=t and obtain t² for conjunction; identify both occurrences as the same event and its probability is t. Equal numeric labels are not dependence information.
- **Contextual marginal equality:** the fair-event example above defeats a scalar fixed-model equality certificate used inside a correlated context.
- **Decision versus value:** p and p² are both above 1/2 throughout [3/4,1], certified by exact Bernstein ranges, even though their values and gradients differ. At p=3/5 they fall on opposite sides. A decision certificate is domain-dependent.
- **Crisp placement:** p=q=3/5 gives recursive crisp AND=1, while final threshold of pq=9/25 gives 0. This reproduces the handoff example with the source's threshold rule.
- **LM frame relaxation:** the real matrix `[[p,1-p],[1-p,p]]` has determinant 2p-1 and is singular at 1/2; it cannot carry the Boolean involution/reconstruction proof unchanged.
- **False novelty:** replacing CMs with framed truth vectors leaves every result and checker algorithm in this dossier intact. Existing AMC and atlas theorems already cover substantial circuit-property contracts. No mathematical exclusivity for CM/LM was found.

The checker additionally verifies the joint-probability covariance identity for all 16 tables at bounded rational marginals and feasible joint probabilities, checks residual ideal decompositions, and validates Bernstein enclosures at rational points. Interval sampling is supplementary: the bound's soundness derives from the Bernstein convex-hull property, not from those samples. The script does not verify arbitrary learned domains, deployed numerical derivatives, a full PALO grammar, or a complete certificate checker in an ITP.

## CM/LM's actual role and reciprocal value

The CM token and signed-frame conventions are a convenient finite representation of b_E. LMs give a formula-valued organization and a native Boolean valuation/coherence story. The source's Theorem 4.5 identifies partition selectors as Boolean-algebra homomorphisms; an expectation with fractional distribution weights generally does not preserve conjunction. This helps explain the semantic boundary. It does not make real expectation a Boolean valuation.

If ordinary framed truth tables replace CMs, **no theorem, admission algorithm, compositional guarantee or capability established here is lost**. Matrix notation, uniform small-kernel storage and continuity with Brian's calculus are the actual benefits. The proposed additional capability would come from contract metadata, residual certificates and compiler enforcement. They can be attached to a DAG, BDD or probabilistic circuit just as well. CM-specific novelty must not be inferred from an implementation choice.

For PALO, an optional checker could make preprocessing effects inspectable: safe soft laws pass, intentional derived-theory changes are labeled, and Boolean simplification does not masquerade as an unchanged numerical objective. PALO might supply realistic formulas and objectives for testing the portfolio. For the portfolio, this motivates a precise boundary and a new use case without changing Boolean expressiveness claims. It supplies no proven speedup or training improvement.

The compiler source reports an exact generic-optimizer tie on its exploratory reductions, a negative synthetic pair-token study, and direct packed full-bitset evaluation faster in all 70 complete natural timing cases. These source results were read, not rerun. A soft-contract prototype must charge semantic checking and fallback costs and cannot inherit a broad performance claim from constant-size token fusion.

## Minimum credible paper package

**Conditional standalone title:** *Context-Aware Translation Validation for Differentiable Logic*. Keep *Semantic Contracts for Compiling Differentiable Logic* as a program title; avoid claiming that CM supplies the unique semantics.

**Provisional abstract, describing a target paper rather than completed results:**

> Differentiable-logic systems combine Boolean specifications, recursive real-valued objectives and probability models whose compiler transformations obey different equivalence relations. We study translation validation for a finite propositional fragment with shared expressions. A mode-indexed checker records event identity, parameterization, derivative policy and boundary context. Exact polynomial residuals certify objective-preserving rewrites or produce rational counterexamples; contextual probability signatures and separate value, gradient and threshold contracts support restricted replacements. We aim to establish compositional soundness and evaluate admission, certificate cost and numerical execution against ordinary expression DAGs and probabilistic-circuit baselines. Correspondence matrices provide one framed truth-function representation, while the validation method is representation-independent.

The abstract's compositional implementation and evaluation sentences are **uncompleted obligations**. Do not submit it as a results abstract now.

Proposed outline: (1) task and selected semantic contracts; (2) closest-work distinctions; (3) typed DAG/cut representation and event/parameter/context separation; (4) exact validation and counterexample generation; (5) bounded C1 and decision propagation, with unknown/fallback rules; (6) artifact evaluation; (7) boundaries, negative findings and relation to the Boolean compiler.

Needed proof package:

1. A precise judgment whose conclusions state each requested contract independently, plus compositional preservation across sharing and scope changes.
2. A small trusted certificate-replay kernel with proof or independently audited arithmetic; exact residual equality alone is only a building block.
3. Correct pullback rules for declared parameter maps and mathematical/custom derivative policies. Quantifiers, losses and nonlinear gates must be either proved or excluded by types.
4. Contextual event replacement conditions, including support restrictions and normalization. A scalar probability certificate must be rejected when the caller requests a context contract.
5. Sound approximation and gradient propagation with explicit norms, domain and regularity assumptions; decision margins and floating-point realization need separate evidence.
6. Complexity bounds in cut size, degree, coefficient bit length and DAG sharing. No polynomial-time claim for unrestricted expansion or compilation.

Minimum experiments, kept local and small until justified: realistic formulas extracted from an accessible PALO or differentiable-logic example; paired original and transformed objectives; same parameter maps and derivative policies; measured admission and fallback; value/gradient discrepancies and certificate replay; exact-model-counting cases with shared variables; supported query reuse and costs. Training is secondary to proving and measuring semantic correctness. Do not spend on large training merely to decorate the methods result.

Meaningful baselines: original expression DAG with automatic differentiation; the same DAG with algebraic safe rewrites; generic sparse-polynomial/CAS identity checking; cut truth tables and ROBDDs with the same frames; d-DNNF/SDD weighted model counting for probability mode; Scallop provenance and Vehicle language/backend boundaries where integration is feasible; conservative interval/automatic-differentiation bounds. Compare identical endpoints, preparation/reuse rules and requested contracts. The matrix/table ablation is mandatory: any claimed CM advantage must survive a framed-table comparator.

Stopping criteria:

- Merge the explanatory boundary and checker appendix if all contribution claims reduce to known multilinearization, AMC or generic conditional rewrites.
- Do not launch a separate paper if realistic objectives admit too few useful transformations, polynomial expansion dominates, or the generic-table/DAG checker gives the same capability and cost with no meaningful methodological distinction.
- Retain conservative rejection when feasible neural parameter domains cannot be certified; do not count free-input counterexamples as attainable model failures.
- Stop approximation claims if gradient bounds become vacuous after shared-context propagation or if actual backward policies cannot be characterized.
- A methods paper can still be credible with negative performance results, but must demonstrate a useful verification/diagnostic capability or a nontrivial general theorem, not merely exhibit familiar counterexamples.

## Established, unimplemented and next steps

Established in this investigation: current local source selection; documented primary-literature overlap; a written proof of the bounded polynomial admission/witness mechanism; exact checker results; concrete failures of blanket Boolean-to-soft folding, marginal-only contextual replacement and value-only gradient reasoning. These are research evidence and derivations, not a finished formalized compiler.

Unimplemented/unproved as a system: full typed IR; PALO/LIME integration; model-feasible neural counterexamples; scalable cut extraction; general joint-model compilation; contextual C1 budget propagation; formal certificate replay; floating-point/actual-AD preservation; performance advantage and training effects; standalone novelty/priority.

Priority recommendation after this completed initial assessment:

1. **Merge proposal, if Brian wants a manuscript revision:** add the semantic boundary and one worked counterexample to the existing compiler manuscript, with this checker as supporting research evidence. The present authorization allowed research artifacts only, so no source revision has been made. A same-chat follow-up preserves the source decisions and reduces rediscovery; gpt-6.1-sol with medium reasoning is a suitable available model for a bounded draft edit and verification.
2. **Defer independent prototype expansion** until there is a concrete shared-objective workload and a clear distinction from Vehicle/Scallop/AMC/atlas coverage. If that gate is met, continue here while source decisions remain useful; gpt-6.1-sol with high reasoning is suitable for the implementation, with a more capable mathematical review only if proof difficulties justify it. No additional training spend is needed for that first gate.
3. **Skip a standalone paper draft now.** No new chat or model run is required to finish this assessment. If the later implementation becomes an independent project, use a fresh chat with the compact handoff in the README rather than copying this whole history. Model recommendations are capability judgments using session availability, not measured price or cache savings.

All required initial deliverables are complete. No commits, pushes, publication, external messages, secrets access, paid compute or changes to permissions were performed.
