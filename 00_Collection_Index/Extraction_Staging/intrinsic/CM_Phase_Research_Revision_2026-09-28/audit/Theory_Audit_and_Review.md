---
title: "Boolean CM Phase Algebra: Theory Audit and Publication Decision"
subtitle: "Proof reconstruction, adversarial review, overlap analysis, and revision record"
author: "Prepared for Brian Droncheff"
date: "28 September 2026"
---

# 1. Decision

**Retain and circulate the revised work as a focused technical companion. Do not present it as a newly founded quantum theory or, on the present evidence, as a strong standalone original-research paper.**

The supplied phase algebra has a sound mathematical core. I did not find a fatal error in the central ring identities, the correctly scoped phase-to-ANF construction, or the principal finite classifications. The inherited verification passed on a fresh execution. The weaknesses were principally contribution boundaries, an incompletely closed detector problem, reliance on enumeration for some readily provable classifications, and the temptation to transfer results between different gate, tensor, and readout models.

The revised manuscript, *Boolean CM Phase Algebra: Native Binary Realizations and Exact Detector Bounds*, is 14 pages, compared with the supplied canonical 26-page paper. It supplies an exact detector-width result, a complete analytic two-branch unitary normal form, and a sharp gate criterion for retaining the square-zero interaction obstruction. It also states precisely what eliminating a primitive convolution symbol does and does not change.

The most important priority finding is adverse to a strong novelty claim: the lower-bound engine for the detector theorem is already the forbidden-weight theorem of Enomoto, Frankl, Ito, and Nomura (1987) [1]. The revision explicitly credits that theorem. The application and construction are useful closure of this project's examples, not a new discovery in coding theory. Similarly, the underlying ring and Boolean Mobius transform are established mathematics [3,5].

**Submission decision:** mathematical circulation as a technical companion is supportable after author review. An unconditional recommendation to submit this as a substantial original-research article is not supportable. A specialist technical-note or expository form is plausible, but an actual venue and its expectations have not been selected or checked. Authorship, affiliation, disclosure, and submission-format decisions remain the author's responsibility. The numerical score below does not override these limitations.

# 2. What was actually audited

The canonical manuscript in `CURRENT_MANUSCRIPT` was read and its 13 theorem/proposition/corollary environments reconstructed. The source package, existing claim descriptions, September 26 viability assessment, review inventory, and executable evidence were inspected. The old and new verifiers were executed, rather than accepting historical success reports. The revised PDF was compiled and visually checked.

The related CM/LM manuscript was inspected for its operations, notation, and phase boundary. The supplied `main.tex` was examined for its characteristic-two modal access/readout contract and its ring-valued appendix. The six-row `phase_table.tex` was checked independently. These comparisons are not a new full publication-readiness audit of those other papers.

`CM Phase Calculus.tex` is only the root of *Signed and Integral Lifts of Correspondence Matrices*. Its seven included section files and `references.bib` were not supplied with that root. Its abstract and declared scalar transition can be compared; its missing proofs, complete novelty case, and detailed applications cannot be certified from this attachment. No unseen sections are represented as having been reviewed.

The archive records a prior viability assessment recommending a technical-companion form. Its separate review directory says no substantive independent referee artifacts are present. That does not prove no discussion ever occurred elsewhere, but the supplied package does not establish completed external peer review.

**Reviewer provenance:** the seven perspectives in Section 5 are analytical roles adopted by one assistant. They are not seven independent agents, external specialists, or journal referees. The new program is independently implemented relative to the inherited code, not independently authored or externally replicated. No proof assistant was used.

# 3. Mathematical findings and useful extensions

## 3.1 The ring is sound, classical, and not the original CM product

The cyclic coefficient algebra is

$$A=\mathbb F_2[C_4]\cong\mathbb F_2[t]/(t^4-1)\cong\mathbb F_2[u]/(u^4),\qquad u=1+t.$$

The eight units, chain of five ideals, nilpotent ranks, and two idempotents follow directly. The numerical $2\times2$ identity CM is $1+t^2=u^2$ in cyclic coordinates and is square-zero under the phase product. It is nevertheless an identity under ordinary CM matrix multiplication. This is an effective diagnostic against conflating the two products.

The intrinsic conjugation is $t\mapsto t^{-1}$. The standard free-module Hermitian pairing is nondegenerate but has nonzero isotropic vectors. The canonical supplied manuscript already distinguishes this from a positive norm; that distinction is retained, not claimed as a newly discovered repair. Algebraic self-product, literal coefficient inspection, and integer Hamming weight remain separate readouts.

The relevant group-algebra literature is substantial. Balogh and Laver reproduce an earlier general scalar-unitary order formula which gives eight scalar unitaries here [3]. That formula should not be confused with a classification of $2\times2$ matrices over the ring. Conversely, the local-ring unitary formulas in Cruickshank et al. cannot simply be applied: their assumptions include an element $b$ with $b+\bar b=1$, whereas this ring has no such element [4]. The revision uses direct proofs instead of importing an inapplicable theorem.

## 3.2 Star-free computation already exists, but has two meanings

Let $R$ be the binary permutation matrix of a four-cycle. Then

$$\rho(a)=a_0I+a_1R+a_2R^2+a_3R^3$$

is a faithful representation, with

$$\rho(a\star b)=\rho(a)\rho(b).$$

Thus every declared $A$-linear circuit can be implemented using ordinary binary matrices, XOR, and AND. The convolution symbol is not a necessary primitive. This route was already present in the supplied algebraic material; the revision makes it central and proves the more precise statement

$$\operatorname{Cent}_{M_4(\mathbb F_2)}(R)=\mathbb F_2[R].$$

For multiple blocks, commuting with the direct sum of copies of $R$ is exactly being a matrix over the represented ring. Removing the notation preserves the model. Allowing *all* binary linear gates enlarges it. These are different operations on a research program, and conclusions from the first do not automatically apply to the second.

A worked native-binary interferometer uses the block shear with lower-left block $I+R$. Its detector component is $(I+R)(I+R^j)e_0$, producing weights $(0,2,4,2)$. Those integers are pattern statistics, not Born probabilities.

## 3.3 The detector problem can be closed exactly

The revised contract fixes the following data: a finite-dimensional commutative unital binary algebra $B$, a nonzero tag $\tau$, fixed parallel $B$-linear output rows, zero-sum row weights, and the rule that the answer is constant exactly when every output pattern is zero. There is no adaptive row choice, nonlinear preprocessing, complete modal instrument, or free oracle-query claim.

Set $r=\dim_{\mathbb F_2}(\tau B)$. A row applied to the tagged input $1+\tau f_x$ produces

$$D_j(f)=\tau\sum_x w_{j,x}f_x,\qquad \sum_xw_{j,x}=0.$$

The combined detector is a binary linear map $H$ with $H\mathbf1=0$ and rank at most $rc$. Its kernel must contain no vector of weight $N/2$. The 1987 forbidden-weight theorem gives kernel dimension at most $N/2$ when $4$ divides $N$ [1]. Therefore $rc\ge N/2$.

The bound is attained explicitly. Choose $N/2+1$ addresses, compare their bits to one reference bit, and pack the resulting $N/2$ differences into a basis of $\tau B$, at most $r$ per channel. Vanishing forces too many equal bits for a balanced input. This gives

$$c_{\min}(N,\tau)=\begin{cases}1,&N\equiv2\pmod4,\\ \lceil N/(2r)\rceil,&N\equiv0\pmod4.\end{cases}$$

The first case is essential: for $N\equiv2\pmod4$, parity itself separates the promise, so a purported lower bound without the length hypothesis would be false.

For the original half-turn tag $\delta=u^2$, the ideal $\delta A$ has binary dimension two, not four. For $N=2^n$, $n\ge1$, the exact width is

$$c_{\min}(n)=\lceil 2^{n-2}\rceil,$$

giving $1,1,2,4,8,16$ channels for $n=1,\ldots,6$. A single row suffices at four addresses; two are necessary and sufficient at eight. The previous finite examples are therefore closed within their declared linear pattern-readout contract.

For recognizing constancy among *all* Boolean truth vectors, the exact width becomes $\lceil(N-1)/r\rceil$: the kernel must be exactly the span of the all-ones vector, and all $N-1$ reference differences attain this rank.

The revised paper includes a self-contained polynomial proof of the power-of-two, all-ones-containing specialization of the coding bound. It does not claim originality for that proof or for the already known theorem. The general all-multiples-of-four statement is attributed, not presented as a new self-contained discovery.

## 3.4 The square-zero obstruction has a sharp gate boundary

Let $V=A^m$ over $\mathbb F_2$, and let $\Delta$ multiply each block by $\delta=u^2$. Then

$$\operatorname{im}\Delta=\ker\Delta=K_m=\delta A^m.$$

Consequently, for every binary linear map $G$,

$$\Delta G\Delta=0\quad\Longleftrightarrow\quad G(K_m)\subseteq K_m.$$

This proves exactly which intervening gates preserve the obstruction. It is larger than the rotation centralizer. Circuits whose intervening gates and declared coefficient maps preserve $K_m$ have no terms with two selected square-zero activations. The statement concerns degree in the activation parameters, not the internal Boolean degree of each predicate.

There is a small, reversible counterexample outside this class. Swap cyclic basis vectors $e_1,e_2$ and fix $e_0,e_3$. This binary-orthogonal gate satisfies

$$\Delta G\Delta e_0=e_0+e_1+e_2+e_3\ne0.$$

The mixed coefficient of $(I+c\Delta)G(I+b\Delta)$ is therefore nonzero. This is not a counterexample to the original theorem with $A$-linearity retained. It is a counterexample to extending that theorem to arbitrary star-free binary gates. The exact criterion and explicit witness are a useful addition because they settle where the original reasoning stops applying.

The independent enumeration confirms, on one block, 16 binary maps commuting with $R$, but 4,096 preserving the tag ideal. Among invertible maps, the corresponding counts are eight and 576. Merely saying that a gate is Boolean, reversible, or orthogonal does not identify its model.

## 3.5 A normal form replaces some brute-force evidence

Every intrinsic two-branch unitary has the unique form

$$U=\operatorname{diag}(a,d)\begin{pmatrix}1&k\\k&1\end{pmatrix}S^e,$$

where $a,d$ are among the eight units, $k\in(\delta)$ has four choices, $S$ swaps the branches, and $e\in\{0,1\}$. This yields 512 unitaries, 128 monomial and 384 nonmonomial.

The involution count now has an analytic proof. Without the branch swap, $a^2=d^2=1$, giving 64 possibilities. With the swap, $d=a^{-1}$, giving 32. Thus there are 96 square-one matrices including the identity, of which 72 are nonmonomial. This explains the previously enumerated values instead of simply repeating them.

The same normal form proves the scoped self-product blind spot for $U^\dagger\operatorname{diag}(t^j,1)Ue_0$: the two branch self-products are always $(1,0)$. The second branch may nevertheless be a nonzero isotropic pattern. This does not rule out all interference, all binary gates, or all modal protocols.

## 3.6 The ANF construction is useful but not a new transform

The matrix $M_n=\left(\begin{smallmatrix}1&0\\1&1\end{smallmatrix}\right)^{\otimes n}$ is the established subset Mobius transform over characteristic two [5]. With a shared half-turn tag,

$$M_nP_fM_ne_{\varnothing}=e_{\varnothing}+\delta\,\operatorname{ANF}(f).$$

This identity explains the phase representation. It does not furnish an exact operational query algorithm with free access to every coefficient. An explicit state still has $4\cdot2^n$ binary coordinates, and the full butterfly uses $n2^{n-1}$ coefficient additions. Construction of the oracle or input and readout cannot be omitted from a resource comparison.

The local CM compiler formula is likewise ordinary Boolean polynomial substitution. Its augmentation identifies nonaffinity of the raw two-input predicate, not necessarily of the result after substituting dependent operands. For example, AND becomes the affine function $X$ when both operands are $X$. The revision states this qualification directly.

# 4. Completeness and closure

The finite scalar algebra, two-branch unitary classification, specified native representation, exact parallel detector widths, and shared square-zero gate criterion are now closed at their stated level. Their proofs do not depend on extrapolating a bounded search. The finite enumeration remains valuable as cross-checking and as an inventory of explicitly bounded properties.

This does not mean that every model expressible using Boolean matrices has been classified. The paper does not establish a general Born rule, universal exact teleportation under rotation restrictions, contextuality classification for arbitrary extensions, general Simon/search lower bounds, optimal modal Deutsch--Jozsa query complexity, or superiority to a matched Boolean compiler. These are not silently advertised as completed topics.

The delivered revision preserves the original data even where a broad application discussion or an enumeration table is no longer typeset in the main paper. Closing a focused contract and declining unrelated claims is preferable to adding more modalities merely to make the paper appear larger.

# 5. Specialist and hostile review perspectives

The following reports are intentionally different tests of the work, not claims of independent authorship or external peer review.

## R1. Modular algebra and finite-ring specialist

**Verdict: sound specialized algebra; restrain novelty.** The identification with a truncated polynomial ring is classical. A claim of a new number system would fail immediately. The scalar filtration and conjugation should be proved in one place, and the matrix counts should have structural explanations where available. Do not confuse a nondegenerate pairing with an anisotropic positive norm. Do not import local-ring formulas whose trace or characteristic assumptions fail.

**Response and revision:** accepted. Sections 2 and 4 now supply direct arguments, the complete normal form, analytic involution counts, and a specific hypothesis comparison to the literature. No historical firstness is claimed for the small matrix group. The existing nondegeneracy/isotropy distinction was retained. Residual issue: the specialized matrix-group normal form has not been certified historically new, and the paper does not need to assert it is.

## R2. Coding-theory and exact-resource specialist

**Verdict: close the finite examples by a theorem, then attribute its engine.** The resource must be the number of fixed parallel algebra-valued channels, not an undefined amount of information or an oracle-query count. Outputs lie in the tag ideal, so its dimension, rather than the full scalar dimension, bounds rank. Balanced avoidance is a forbidden-weight problem; ordinary minimum-distance bounds are not the right comparison. The address-length exception must not be hidden.

**Response and revision:** accepted. Definition 6.1 freezes the contract. Theorem 6.3 proves the exact general even-length formula, credits Enomoto et al., and supplies explicit optimal weights. Corollary 6.4 treats unpromised constancy. The power-of-two proof is supplied separately. The novelty claim was reduced when the 1987 antecedent was found; it was not concealed as merely a related citation.

## R3. Modal computation and operational-model specialist

**Verdict: algebraic pattern separation is not an operational exact algorithm.** A detector can vanish on a constant input without making a possible measurement outcome that announces constancy. A complete recorded modal instrument must retain enough maps to avoid annihilating every possible branch. Literal pattern inspection and complete recorded readout cannot be interchanged. Balanced tensor products over $A$ also differ from independent binary tensor factors.

**Response and revision:** accepted. The abstract and Sections 1, 6, and 8 explicitly exclude a Deutsch--Jozsa query-advantage interpretation. The related BV manuscript is used only to delimit its own stronger operational contract, not assumed to validate this paper. The analyzer rank table is independently reproduced. No Bell/GHZ/teleportation claims were imported to enlarge the manuscript.

## R4. Native binary implementation and Boolean compiler specialist

**Verdict: replacing a primitive is not the same as enlarging a gate set.** A faithful regular representation is enough to eliminate star notation, but all consequences of the algebra survive that translation. An arbitrary binary gate need not commute with scalar multiplication. A no-go statement should identify the invariant subspace it actually needs. A local Boolean compiler identity is not automatically a practical compiler advantage.

**Response and revision:** accepted. Theorem 3.1 identifies the exact rotation centralizer. Theorem 7.1 identifies the larger ideal-preserving class and provides a reversible witness outside it. Appendix B restricts the raw two-input nonlinearity test and retains local compiler identities without making performance claims. A matched implementation benchmark has not been delivered, so practical superiority is not asserted.

## R5. Reproducibility and evidence specialist

**Verdict: strong finite evidence only after fresh execution and exact scope labels.** All matrices, all states in a fixed shell, seeded circuit regressions, and selected task examples are different evidence universes. A count of internal DAG nodes is not a count of independent programs. Agreement between two scripts by the same author is not external replication. Historical test claims should not be accepted without running the available source.

**Response and revision:** accepted. The inherited inventory and its separate report checker pass on fresh execution. A new standard-library program checks the new normal form, gate boundary, subspace kernels, detector constructions, and analyzer ranks without importing inherited code. Logs, input hashes, original sources, full finite data, and run instructions accompany the revision. This remains computational corroboration, not formal proof or independent laboratory replication.

## R6. Hostile novelty referee

**Attack:** "This is a small classical group algebra, an established Mobius transform, an old forbidden-weight theorem, and a finite matrix catalog. Calling the package intrinsic, phase-like, or Boolean does not create a new quantum theory. A narrow synthesis must not be sold as a fundamental computational breakthrough."

**Assessment:** substantially correct as an attack on an inflated research claim. The priority investigation confirms the decisive coding antecedent, while the ring and transform are standard. The paper's genuine utility lies in explicit interfaces, sharp boundaries, complete constructions, and reproducible classifications. That is a defensible technical-companion contribution, not evidence of a broad breakthrough.

**Response and revision:** accepted the attack on novelty inflation. Removed broad speculative applications and general computation-advantage framing; placed attribution beside the relevant theorem, rather than only in a distant bibliography. Rejected only the conclusion that a carefully typed and reproducible companion has no value at all. Residual verdict: a hostile originality-focused journal referee could still reasonably recommend rejection. The scorecard records that risk rather than averaging it away.

## R7. Hostile handling editor and portfolio-overlap reviewer

**Attack:** "The portfolio appears to have several papers sharing the same four-coordinate algebra. The original phase manuscript reads partly as a research notebook and partly as a promise of future applications. Who is the intended reader, what belongs in this paper, and why should an editor treat it as a standalone research article? A readiness average cannot answer these questions."

**Assessment:** the concern is justified. The foundational paper owns the CM/LM calculus; the modal query paper owns its explicit exact-query results; the signed-integral companion changes scalars. Repeating all of those theories here would weaken focus and create redundant novelty claims. The signed companion's supplied root does not allow a complete overlap audit of its missing sections.

**Response and revision:** accepted. The revision is reduced from 26 to 14 pages and focused on native representation, exact detector widths, and nilpotent/gate boundaries. A title-level reference to the supplied BV companion avoids inventing a harmonized author byline: its supplied source uses "Brian Theory," while other sources use "Brian Droncheff." The revised phase document remains explicitly prepared for author review. Residual verdict: circulate as a companion; withhold a blanket original-research submission recommendation until the intended form and author-approved submission metadata are settled.

# 6. Relation to the other supplied manuscripts

**CM/LM Boolean operator calculus.** Its core is the typed correspondence/logical-matrix construction, signed frames, pairing, superposition, and higher-arity structure. Its supplied text explicitly says cyclic convolution is a separate additional multiplication, not ordinary CM multiplication or LM pairing. The present phase companion should begin at that boundary and should not repeat foundational novelty claims.

**Characteristic-two modal computation (`main.tex`).** Its main object is exact query complexity under complete recorded linear instruments and specified pointwise oracles. The shared ring appendix and nilpotent analyzer are genuine overlaps, but not identical contributions. The present detector-width theorem counts fixed output channels after a tagged pattern is given; the supplied modal paper counts oracle calls with every possible terminal branch correct. The two results do not conflict merely because both mention constant/balanced functions.

**Signed and integral phase calculus.** Its supplied abstract changes scalars to $\mathbb Z[C_4]$ and then quotients by $1+g^2$ to reach $\mathbb Z[i]$. That is not a star-free implementation of the same characteristic-two ring. It is a different scalar construction. The abstract's Hamming-isometry boundary overlaps this paper; its missing sections prevent a complete theorem-by-theorem comparison.

**The phase table.** It is derived evidence for the balanced-$A$ analyzer $H_z$. Invertible row and column operations reduce $H_z$ to $\operatorname{diag}(1,u^2)$. Its $n$-fold tensor over $A$ has binary rank $4+2n$, because only terms with zero or one factor $u^2$ survive. The six supplied values, $6,8,10,12,14,16$, all match the new calculation. This is row/column equivalence, not an assertion of conjugacy or a probability distribution.

**Portfolio recommendation:** retain these divisions. The phase manuscript should be the algebra-and-interface companion, not a fifth place to re-prove the main query theorem or a second signed-quantum construction. The missing signed sections should be checked before making any future claim that the entire portfolio is free of detailed overlap.

# 7. Fresh verification and limits of the evidence

The inherited program enumerated all 65,536 two-branch matrices, reporting 24,576 invertibles, 512 intrinsic unitaries, 96 involutions, and 72 nonmonomial involutions. It confirmed 32 global Hamming isometries, 512 weight-four-shell preservers, and a 256-element intersection between that shell class and the unitaries. It also reproduced 22,528 invertible splitters and 8,192 examples with the specified four-phase target profile. These are fixed finite architectures, not all possible algorithms.

The separate inherited report checker independently checked binary orthogonality for all 65,536 matrices and verified 17 manuscript count claims. Additional inherited checks covered 256 scalar products, 4,096 triples, 65,812 Boolean phase/ANF cases, 65,808 kernel-product pairs, 200 seeded nilpotent-regression circuits, and the specified local compiler tests. The 1,500 internal nodes belong to 50 seven-variable DAGs. The bounded marked-coordinate-peak scan remains a local negative result, not a general search impossibility theorem.

The new verifier uses a separate standard-library implementation. Its principal universes are:

- All 65,536 binary $4\times4$ maps for the centralizer/ideal-boundary equivalence, and all 65,536 ring $2\times2$ matrices for normal-form comparison.
- All 29,230 binary subspaces containing the all-ones vector at lengths two, four, and eight; the respective totals are 2, 16, and 29,212, with maximal balanced-avoiding dimensions 1, 2, and 4.
- 52,776 promised detector cases and 262,140 unrestricted-constancy cases, over every even length from two through sixteen and all three tags $u,u^2,u^3$; repeated inputs under different tags are counted separately.
- Six independently expanded analyzer ranks and exact tensor/gate counterexamples, together with checks of the elementary-symmetric parity identity used in the power-of-two proof.

Every declared check passed. The general proofs, not those finite counts, establish unbounded statements. Execution time is retained in logs as a reproducibility observation; it is not a fair benchmark or a claim of performance advantage. Verification does not establish historical novelty, physically realizable readout, author approval, or publication acceptance.

# 8. Publication-readiness scorecard

Scores assess the manuscript as a focused technical companion. "Original" is a retrospective assessment of the supplied canonical phase manuscript, not a previous panel's score. "Revised" assesses the delivered document. Confidence is confidence in this audit judgment, not probability of journal acceptance.

| Category | Weight | Original | Revised | Confidence |
|:--|--:|--:|--:|:--|
| Mathematical correctness | 20% | 8.7 | **9.1** | High |
| Completeness of proofs/results | 8% | 8.0 | **9.0** | High |
| Model and assumption discipline | 8% | 7.9 | **9.2** | High |
| Novelty and priority | 12% | 4.5 | **5.3** | Moderate |
| Scientific significance | 8% | 5.8 | **6.8** | Moderate |
| Literature coverage and positioning | 8% | 6.4 | **8.2** | Moderate-high |
| Reproducibility | 7% | 8.8 | **9.3** | High |
| Internal consistency | 6% | 7.8 | **9.0** | High |
| Resolution of prior reviewer concerns | 5% | 7.0 | **8.5** | Moderate |
| Exposition and readability | 5% | 7.0 | **8.4** | Moderate |
| Scope and structural focus | 4% | 5.8 | **8.8** | High |
| Evidence and citation quality | 4% | 7.5 | **8.6** | High |
| Submission hygiene | 3% | 6.2 | **7.8** | High |
| Venue/form fit | 2% | 5.8 | **7.2** | Moderate |

**Weighted assessment: 7.15/10 original; 8.22/10 revised.**

**Mathematical correctness:** Reconstructed core; exact scoped proofs; no formal verification.

**Completeness of proofs/results:** Detector widths closed; involution counts proved analytically.

**Model and assumption discipline:** Gate algebra, tensor base, detector contract, and readout separated.

**Novelty and priority:** Main algebra and coding engine are classical; no certified firstness.

**Scientific significance:** Useful exact interface/boundary companion; no demonstrated speedup.

**Literature coverage and positioning:** Decisive 1987 theorem credited; local-ring hypotheses checked.

**Reproducibility:** Inherited full rerun and a separate new implementation pass.

**Internal consistency:** Native binary and ring claims use explicit compatible contracts.

**Resolution of prior reviewer concerns:** Available viability concerns addressed; no unseen reviews certified.

**Exposition and readability:** Reduced to 14 pages, explicit examples and proof boundaries.

**Scope and structural focus:** Broad speculative applications removed; companion role fixed.

**Evidence and citation quality:** Finite universes labeled; primary theorem statement located.

**Submission hygiene:** Buildable source/PDF; author approval and venue metadata pending.

**Venue/form fit:** Technical/expository companion plausible; no venue selected.

The correctness and reproducibility gates pass within the declared scope. The originality/significance gate for a substantial standalone research article does not. The prior-concerns score covers the available viability assessment and issues reconstructed here; it does not certify closure of external reports that were not supplied. The submission-hygiene score does not imply that the author has approved a byline, affiliation, disclosure, or journal format.

# 9. How to proceed

Freeze this revision as the canonical algebra-and-interface companion, retaining the original source and full data as provenance. Do not replace the modal query paper's operational contract with the weaker pattern-inspection contract. Do not describe removal of the star symbol as removal of the algebra's nilpotence. Those two mistakes would undo the principal benefit of the revision.

For public mathematical circulation, the author should approve the text, byline, and AI-assistance disclosure, then circulate the focused companion alongside the appropriate foundational manuscript. For a journal submission, first settle whether the target accepts a compact expository/technical synthesis of this kind. That is a form-and-contribution decision, not a reason to perform unlimited additional hostile passes on the same elementary identities. This audit does not identify or endorse a particular journal.

A targeted external reader would be most useful on the sufficiency and originality of the synthesis, rather than another unchecked global score. The strongest exact theorem is now deliberately attributed at its coding-theory core. An external reader could also compare the complete signed-integral manuscript once its missing sections are available. Such a reading would be genuine external feedback; the seven perspectives in this report are not a substitute for it.

For further original research, there are two defensible directions. One is a classified restricted gate family between the rotation centralizer and the tag-ideal stabilizer, with a specific retained-information task. The other is an actual matched implementation study against Boolean or symbolic baselines given the same inputs, output contract, and local simplifications. Neither a larger small-matrix census nor an uncharged oracle layer would by itself make a stronger computational contribution. No practical advantage is claimed in advance.

**Bottom line:** the work need not be discarded, and the mathematics need not be expanded indiscriminately. The supplied finite examples have been turned into sharper, more complete statements. Retain the revised companion; reserve a standalone-original-research claim for a contribution beyond the classical algebra and coding theorem already identified.

# 10. Literature and access record

The priority check was refreshed on September 28, 2026. Search absence is not proof of historical novelty. The following records distinguish what was accessible from what is merely cited as nearby context.

**[1] H. Enomoto, P. Frankl, N. Ito, K. Nomura (1987), "Codes with given distances," Graphs and Combinatorics 3, 25--38. DOI: 10.1007/BF01788526.** The primary publisher abstract was read. It explicitly states the sharp length-$4t$, dimension-greater-than-$2t$, weight-$2t$ theorem. The full subscription article was not accessible in this session. The abstract is nevertheless enough to establish that the detector lower-bound engine is prior art. The supplied revision gives a separate proof of the power-of-two specialization needed for its original CM use case.

**[2] L. Bassalygo, G. Cohen, G. Zemor (2000), "Codes with forbidden distances," Discrete Mathematics 213, 3--11. DOI: 10.1016/S0012-365X(99)00161-2.** Indexed paper text identifies Proposition 2 as the corresponding forbidden-weight result. Attempts to fetch a full CORE copy were blocked. This is corroborating context; the decisive priority attribution does not rest on an inaccessible proof or an automatically generated summary.

**[3] Z. Balogh and V. Laver (2020), "Unitary subgroups of commutative group algebras of characteristic two," arXiv:2007.05819.** Full HTML was inspected, particularly Lemma 1 and its attribution of the scalar unitary-order formula to earlier work. The lemma applies to the scalar $\mathbb F_2[C_4]$ case. The paper's later assumption $n>2$ must not be ignored when discussing its different main classification. This source does not by itself establish priority of the present $2\times2$ normal form.

**[4] J. Cruickshank, A. Herman, R. Quinlan, F. Szechtman (2013), "Unitary groups over local rings," arXiv:1303.5106.** Full HTML was inspected. Its trace-surjectivity assumption, and later odd residue characteristic, are material. They were checked rather than silently transferred to this characteristic-two involution.

**[5] M. Barbier, H. Cheballah, J.-M. Le Bars (2020), "On the computation of the Mobius transform," arXiv:2004.11146.** The paper and relevant PDF page images were inspected for the truth-table/ANF transform and butterfly context. Its auxiliary nilpotent polynomial notation is not the same multiplication as the Boolean-function quotient $X_i^2=X_i$ used in this manuscript's local compiler identity.

**[6] B. Schumacher and M. D. Westmoreland, "Modal quantum theory," Foundations of Physics 42 (2012), 918--925; and "Almost quantum theory," arXiv:1204.0701, later a 2016 book chapter.** Full HTML of the latter was inspected for states, effects, and unconditional operations. These works supply operational background, not a justification for inspecting a full coefficient description for free.

**[7] Y. E. Erginbas, J. S. Kang, E. Polito, K. Ramchandran (2026), "Adaptive sparse Mobius transforms for learning polynomials," arXiv:2602.06246.** The current abstract was inspected as an example of nearby algorithmic work. Its real-valued, additive-query formulation is not treated as an automatically matched baseline for XOR-valued computation. No theorem-level comparison or performance benchmark against it is claimed.

Project companions are cited as unpublished supplied manuscripts, not as peer-reviewed sources. The foundations and modal paper were available as substantial standalone sources; the signed-integral root was incomplete. No source search has certified the specialized normal form, elementary gate criterion, or their synthesis to be historically first.

# 11. Delivered materials and audit trace

The package contains the standalone revised LaTeX manuscript and compiled PDF; this report in Markdown and PDF; all 14 readiness entries in JSON; the original-to-revised claim crosswalk; a full source diff; the inherited reproducibility code and data; the new verifier and generated JSON; execution logs; original uploads and hashes; and a manifest of the delivered files. The old uploaded ZIP remains intact in the provenance directory, so removed exposition and historical material are recoverable.

The canonical paper is `manuscript/CM_Phase_Algebra_Revised.tex`. The report and provenance files are not part of the submission manuscript. The root README supplies commands for rerunning the checks and compiling the paper. Results are generated locally; the verification scripts do not access accounts, remote services, or private external data.

The final PDF was inspected for page layout and mathematical/table rendering. This is a typesetting check, not another source of mathematical independence. Any future substantive change to the theorem contracts should trigger corresponding changes in the verifier and this audit record rather than leaving the present scorecard attached to a different manuscript.
