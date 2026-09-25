# Restricted-conversion proof and priority review

20 September 2026. Review of T07–T12 in the frozen `cm_lm_process_semantics_20260920` package. This is an additional analytic and computational review by the same assistant, not independent human refereeing or formal proof certification.

The restricted one-copy results survive. The fixed-phase multi-copy theorem survives within its stated contract, but its mathematics reduces to an exact residue-rank criterion. Its novelty weight should be reduced. A concrete two-copy activation protocol exists once resolved phase measurements followed by disposal are permitted. The earlier statement that general phase disposal needs a more precise contract was correct; the broadly phrased next research target was too weak to be a publication milestone.

## Findings that affect the research decision

1. **T09 is correct, with explicit dimensions and nonzero-target qualifications.** A structured target is reachable by local A-linear filters exactly when each padded target Smith exponent is at least the corresponding source exponent. The proof using image subquotients and socle counts is valid. Finite classical feed-forward does not enlarge the pure heralded preorder. Zero is an impossible branch, even though it belongs to the algebraic downset.

2. **T12 can be strengthened, but should be downgraded as a novelty candidate.** For any matrix N over a commutative local ring B, there are rectangular L,Q with LNQ=I_d exactly when rank(N modulo the maximal ideal) is at least d. A unit minor proves sufficiency; reduction proves necessity. In the Frobenius lift over B_k this gives an exact free-target conversion criterion. For k identical copies it is r_0^k >= d. The old socle-rank obstruction is the same residue rank in a binary representation. This is elementary local-ring matrix algebra, not a new distillation principle. The proof is in the companion theorem file; standard minor behavior is documented in [Stacks, Lemma 15.8.1](https://stacks.math.columbia.edu/tag/07Z6).

3. **A resolved-disposal boundary is now settled constructively.** Two copies of Phi_A(diag(1,u^2)) can yield Phi_A(I_2) if the operation class permits B_2-linear filters followed by a resolved coefficient measurement of the second phase register on each side. Explicit filters and the selected binary output are provided. Only one A phase register remains. The same witness works using the unit sectors of two copies of Phi_A(diag(1,0)); it therefore does not exploit the nilpotent sector. Unobserved disposal of the witness gives a two-dimensional mixed-state subspace, not the desired pure target. No general impossibility for unobserved disposal is inferred.

4. **The filtering relation and filtered ranks have closer antecedents than the baseline ledger recorded.** Matrix comparison by X=LYR appears explicitly in Aranda Pino–Goodearl–Perera–Siles Molina, Definition 2.1 (2008 preprint; 2010 publication), and Antoine–Ara–Bosa–Perera–Vilalta, section 2.5. Thus the relation itself is established. [Original definition](https://arxiv.org/pdf/0806.4156), [later treatment](https://arxiv.org/html/2307.07266v1).

5. **Do not substitute Malcolmson comparison for physical filtering.** Hung–Li, Definition 3.1, permits an additional triangular-block erasure. Their Proposition 3.7 classifies that broader order for the relevant ring family. It is not the local-filter preorder. For example, diag(u,u) is below diag(1,u^2) in their order, but cannot be obtained from it by A-linear local filters. [Hung–Li, pp. 8–11](https://www.math.buffalo.edu/~hfli/malcolmson14.pdf).

6. **The one-variable filtered ranks are already standard rank functions after normalization.** With rho_t(M)=sum_i max(4-a_i-t,0), rho_t/(4-t) is the quotient-regular Sylvester rank for A/(u^(4-t)). These functions and their extreme-point classification appear in Jaikin-Zapirain–López-Álvarez, Proposition 2.2. The complete filter monotones are the Smith threshold counts; inequalities between the rho_t alone are weaker. [Primary source, section 2.1](https://arxiv.org/pdf/2012.15844).

## Claim disposition

| Baseline claim | Review outcome | Priority disposition |
|---|---|---|
| T07 coarse support realization | Algebraic identities and local intertwining retained; no monoidal or entanglement-preservation inference | Frobenius realization is classical machinery; exact CM/LM comparison remains a synthesis claim with unresolved historical priority |
| T08 normalizer and measurement stabilizer | Retained; make the dual/state action explicit, and distinguish group size from the induced permutation group | Elementary centre/commutant and projective-line specialization; exact ambient-linear antecedent not certified |
| T09 Smith classes and selected filters | Retained; add rectangular padding, target nonzero and adaptive-branch lemmas | Standard chain-ring algebra; underlying comparison predates this project |
| T10 d*r_B code size | Retained under fixed orbit and full binary decoder; no broad capacity claim | Elementary orbit-span and modal distinguishability argument |
| T11 h/contextuality increases | Retained as an explicit selected-filter counterexample | Direct consequence of P01's already established static classification |
| T12 retained-phase obstruction | Retained and strengthened to an iff for free structured targets | Residue-rank/unit-minor corollary; withdraw its designation as the strongest prospective novelty claim |
| O01 partial phase disposal | Resolved positively for coefficient-resolved disposal by an explicit witness; unspecified/coarser operation classes remain unclassified | Boundary example, not a general new resource theory |
| O02 combined priority | Still unresolved, with substantially stronger classical antecedents | No claim of being first |

For T08, the binary state group has order 98,304, while its action on the 24 projective points has kernel the eight scalar units and hence image order 12,288. The original order was for the linear group, so this is a clarification rather than a counterexample. Neither number is the full automorphism group of the distant graph.

## Proof qualifications to carry into any manuscript

- State a positive-dimensional, nonzero target. For the zero matrix, exponent inequalities describe an algebraic zero output, not a successful preparation.
- Fix the operational equivalence relation. Full binary effects distinguish some A-unit multiples; invertible A-linear transformations still relate them. Algebraic orbit equivalence is not equality of all full binary measurement statistics.
- Pad Smith lists by exponent four to the maximum of the source and target smaller dimensions. The actual local filter shapes must be declared.
- A successful adaptive transcript is a product of local linear maps. A coarse outcome with a pure final state has at least one nonzero constituent trajectory producing that state. This justifies extending the obstruction to generalized process subspaces and incoherent classical outcomes.
- Only local logical product ancillas are free in the fixed-phase theorem. Retain every phase register, and do not supply a correlated phase resource or resolve/dispose of a phase register inside that theorem.
- B_k for k>1 is local and Frobenius, but is not a chain ring. Do not use a general Smith classification over it. The free-target theorem needs only a unit minor.
- Describe “possible selected branch,” not a success probability, deterministic protocol, or Born-rule prediction.

## Verification and limits

The new independent implementation passed 65,536 classifications over A, 1,966,080 one-sided filter checks counting both sides, and 1,225 three-entry comparisons of threshold versus componentwise order. It also checked socle/residue rank equality and explicit free extraction for all 65,536 two-by-two matrices over F_2[x,y]/(x^2,y^2), and a declared 4,096-matrix sample over actual B_2. The two-copy boundary witness was verified by full binary matrix multiplication; the output rows equal the target rows exactly.

The original exhaustive checker and its 12 unit tests were rerun from byte-identical copies. Raw stdout/stderr and exact commands are preserved. The frozen baseline manifest is verified before and after. These are finite checks, not universal proofs; the written proofs supply the arbitrary-dimension and arbitrary-copy claims. No new human review occurred, no historical audit was rewritten, and no PDF typesetting or visual verification is claimed.

The most direct additional chain-ring lead is Yonglin Cao, *On the Multiplicative Monoid of n×n Matrices Over Artinian Chain Rings* (2010), DOI 10.1080/00927870903133946. Its primary publisher abstract confirms Green-relation coverage, but the full text was inaccessible through the available route. No theorem number or exact order-classification equivalence is attributed to it. That access limit prevents a definitive historical attribution, not the mathematical conclusion that T09 is elementary established machinery.

## Revised publication decision

**No-go for a separate fourth full paper. Preserve the work as a technical companion.** The review strengthens correctness and reduces the remaining novelty case. T12 and the resolved-disposal witness are not sufficient publication milestones. An independently useful note remains an editorial possibility for the closure/support comparison as a whole, but should not be marketed around new Smith conversion, new rank monotones, or a general no-activation theorem.

No work remains required to complete this review. Defer further research until there is an operational reason to choose a particular phase-access contract; do not invent a narrower restriction merely to produce a theorem. If that question becomes relevant, continue in this thread to retain the contracts and evidence, using GPT-6 Astra at high effort for the mathematical analysis. This is the conservative reliability choice among the exposed models, not a measured cost comparison. Reconcile the older audit-manifest differences only before public archive preparation. Publication, author contact and external submission remain unauthorized.
