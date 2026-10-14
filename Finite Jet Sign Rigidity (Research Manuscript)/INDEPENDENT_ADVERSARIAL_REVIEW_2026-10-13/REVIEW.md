# Independent adversarial review — 13 October 2026

**Verdict: MINOR REVISION; retain the guarded-degree comparison in the same paper, with concise synthesis framing. No central mathematical error or mathematical submission blocker was found.** The current arguments support the stated finite-order, arrangement, Denjoy–Carleman, and quantitative conclusions. This is an informal independent machine-assisted review, not proof certification or an acceptance prediction.

The principal editorial risk is significance: this is a useful elementary synthesis with explicit finite-order formulations, not a paper whose principal mechanisms are newly discovered. The additions improve the account of what changes when walls are excluded, but do not establish new approximation machinery. For a venue accepting focused expository or synthesis notes, I would send a lightly revised version to human referees. For a venue requiring a substantial new theorem or technique, I would not represent this review as clearing that threshold. I recommend retaining Theorem 7.3, modestly compressing surrounding exposition, and not developing a second research paper from these additions alone.

## Scope, version, and independence

Reviewed source: `REVISED_PACKAGE_2026-10-13/MANUSCRIPT/finite_jet_sign_laws_REVISED_2026-10-13.tex`, 811 lines; matching PDF, 18 pages. All TeX line locators below refer to this file. PDF page numbers equal its printed page numbers.

| File | SHA-256 |
|---|---|
| Current TeX | `a9bb9bce6ab7aee4db9af72cc2b292386c5dd8ad47ddcec3e5c957e99513d079` |
| Current PDF | `3e574c5fea708bf599d5bcc4bf1b70bddce4c36e824684763a6944145d569bd3` |

Both match the supplied hashes. The complete manuscript was read and its argument reconstructed before any earlier assessment, review report, dossier, or package QA was consulted. `PRELIMINARY_FINDINGS.md` preserves that initial pass. Primary-source verification followed. Only afterward were the October reassessment/diff, September reports, and earlier research dossier/proof notes consulted. Their agreement with this review is corroboration, not a premise. No agents or additional chats were used.

The project is extensively dirty from pre-existing changes. Work here is confined to this review folder; no manuscript, prior package, navigation, register, commit, submission, or external communication was modified. The independent source comparison confirms preservation of all 24 older theorem/lemma/corollary/proof blocks. No additional applicable local AGENTS.md was found in the checked ancestors or manuscript subtree.

## Findings and minimal repairs

### F1 — Specify the margin endpoint in the abstract

**Category:** scope/presentation; minor. **Locator:** abstract, TeX line 52, PDF p. 1; compare Theorem 7.3(iii), lines 553–570, pp. 13–14, and Remark 7.4, line 627.

The abstract says “fixed positive margin” without giving the upper endpoint. The theorem correctly requires `0 < gamma < 1`; at `gamma = 1` there is no polynomial for a nonconstant law. Indeed, whole-cube amplitude at most one and guarded margin one make the polynomial identically +1 or -1 on an open box, hence everywhere. Margins greater than one are impossible even for constants. This is a compression ambiguity in the abstract, not a false theorem: the body already handles it correctly.

**Minimal repair:** write “fixed margin `0 < gamma < 1`.” The suggested patch includes precisely this change.

### F2 — Make the set for fixed derivative budgets explicit

**Category:** scope/presentation; minor clarification. **Locator:** Remark 7.2, TeX lines 531–539, PDF p. 12; contrast compactwise Roumieu definition, lines 151–156, p. 4.

The estimate is valid under the displayed fixed constants on the ball. A compactwise class membership statement does not supply one pair of constants uniformly on an entire open ball reaching the boundary of the domain, nor uniformly across all functions in the class. The sentence converting coordinate estimates “as in (2)” can be read too quickly as supplying that budget automatically. Its intended norm conversion is correct.

**Minimal repair:** specify coordinate estimates “with fixed constants on the same ball (or on a fixed compact subball).” No new hypothesis is needed for the displayed result; the hypothesis is already present. The patch makes the distinction explicit.

### F3 — Contribution size and length need editorial discipline

**Category:** significance/coherence, not correctness. **Locators:** contribution language, TeX lines 84–94, PDF p. 2; Section 7, lines 503–628, pp. 12–14; Sections 8.3–8.4, lines 664–680, pp. 15–16; conclusion, lines 696–698, p. 17.

The quantitative classification is a useful complete statement, but its difficult lower-bound input is Sherstov's theorem. The corner and associated-function estimates are routine Taylor consequences; the R-function construction is explicitly classical; the analytic-composition consequence is immediate once the full-domain hypothesis is specified. Adding these does not transform the novelty level of the underlying paper. Its abstract and introduction largely acknowledge this accurately.

**Minimal editorial repair:** retain Theorem 7.3 and its actual reductions, retain the short corner estimate and R-function/domain examples, and compress repeated historical disclaimers or neighboring-theory summaries if aiming at a strict note format. Keep the finite-jet/realization classification as the main arc and present guarded degree as a comparison under a changed domain specification. Do not advertise Theorem 7.3 as an application of the finite-jet obstruction: Remark 7.4 already correctly says it is not. No prescribed page limit or mandatory deletion is inferred.

**Separate-paper judgment:** the guarded-domain taxonomy has a coherent standalone *expository* short-note case for an approximation/threshold-degree audience. That case rests on transparent synthesis, not priority or a new lower-bound technique. A second research manuscript repeating this framework is not presently justified. A separate project becomes worth reconsidering only with a concrete theorem about growing dimension, margin dependence, conditioning, or coefficient/evaluation resources that goes materially beyond the stated fixed-parameter rates. This is an editorial judgment, not a demand that every publishable synthesis contain new machinery.

No other substantive repair is required by this audit. In particular, I did not manufacture missing assumptions about derivative stability, generic arrangement position, coefficient bounds, network optimization, or uniformity in growing dimension: the stated proofs either avoid them or explicitly exclude such claims.

## Mathematical reconstruction and stress tests

### Earlier dependencies: Lemma 3.1 and Section 4

**Locators:** TeX lines 198–229, PDF p. 5; lines 239–342, pp. 6–8.

The weak-sign polynomial lemma survives interior chamber zeros: a nonzero polynomial cannot vanish on an open chamber, and the residual after extracting a maximal hyperplane factor is nonzero at some generic facet point. There the crossing ratio is the parity of that factor's multiplicity. The connected chamber graph globalizes it; a generic crossing of each distinct hyperplane proves uniqueness. Parallel, dependent, nonessential, and multiple-intersection arrangements do not invalidate this argument. In dimension one each hyperplane is a point and the generic-crossing argument still works.

For a least nonzero derivative order `d`, the ray expansion `F(tv)/t^d -> P_d(v)` gives the required weak inequality, including directions where `P_d(v)=0`. A `C^d` Peano expansion suffices, including `d=0`. The arrangement overlap argument uses the same transverse sign pair inside two balls to identify their local bits. This makes the bits locally constant along each connected hyperplane, without requiring a uniform Taylor order. The uniform `C^N` version then follows. The manuscript correctly distinguishes an N-dependent vanishing point from a single smooth flat point (Remark 4.8, lines 333–334).

The historical reduction in Remark 4.6 is adequate. For `G=F product ell_j^2`, signs are unchanged off the walls, the zero set is exactly the arrangement, and nonflatness persists because the first nonzero term is multiplied by a nonzero polynomial. Theorem 4.2 of [Broglia–Tognoli](https://aif.centre-mersenne.org/article/AIF_1989__39_3_611_0.pdf), printed p. 629, supplies the nonadmissible-signature flat-point consequence; its Section 4 hypotheses and arc-analytic connectivity requirement are addressed. Definition 2.2 and Proposition 2.4, printed pp. 615–617, identify the factor-parity antecedent. The special case `n=1` is separated. This verifies the particular historical implication used here, not all subsequent signature-flatness literature.

### Denjoy–Carleman realization and counts

**Locators:** TeX lines 146–191, 349–430, 441–482; PDF pp. 4–5, 8–11.

Writing `W_j=j! M_j` respects the total-weight convention: W is log-convex, normalized, and has unbounded jth-root growth. Its reciprocal quotient series is the one in the manuscript. The cutoff input is valid for the assumed normalized weights; stronger derivative-stability or moderate-growth conditions are not smuggled in. Product closure follows from log-convexity and Leibniz; primitive closure uses monotonicity.

The selector proof does not require a bump positive throughout the interior of its support: translating its left support endpoint to zero ensures every `(0,t)` contains a nonzero point, and the integral of its square is therefore strictly positive for every positive t. Exactly one product selector contributes off the walls. Distinct chamber sign vectors follow from convexity of fixed sign cells. Generic crossings recover each exponent bit, so all `2^(m+1)` parity restrictions are distinct even when sign vectors form only a proper subset of the formal Boolean cube. The parallel arrangement/count-coincidence observation is correct.

The governing primary passages are [Rainer](https://arxiv.org/pdf/2107.01061), Definition 2.2, Theorem 3.6, Corollary 3.12 and Remark 3.13, author PDF pp. 6, 13–15. The manuscript appropriately acknowledges stronger positive-flat existence and chamberwise gluing. Its explicit selectors remain useful but are not a newly necessary existence method.

### Proposition 7.1 — zero jets and Hölder constants

**Locator:** TeX lines 509–527; equation (10), PDF p. 12.

Any surviving derivative of order at most k has a least order d and triggers Theorem 4.3, contradicting non-affinity. Thus the entire k-jet is zero. For `k=0`, continuity would force a constant sign near zero if `F(0)` were nonzero; the estimate is simply Hölder continuity from zero.

For `k>=1`, along a unit Euclidean ray, the scalar kth derivative is bounded by `H t^alpha`, because the multilinear operator norm dominates evaluation on k copies of a unit vector. Repeated integration gives

`H/(k-1)! integral_0^r (r-t)^(k-1) t^alpha dt = H Gamma(alpha+1)/Gamma(k+alpha+1) r^(k+alpha)`.

The segment stays in the centered ball. No factorial or dimension factor is missing. At balanced corners the radius is `sqrt(n) delta`; the strict condition `sqrt(n) delta < R` is the right one. The result is necessary under the fixed Hölder budget; it claims neither sufficiency for a specified H nor sharpness of its numerical constant for every truth law. Section 8.3 establishes sharpness of the exponent for alpha=1, as stated.

### Remark 7.2 — associated function and Gevrey behavior

**Locator:** TeX lines 530–540; equation (11), PDF p. 12.

Flatness removes every Taylor coefficient. Remainder of order j is at most the displayed derivative budget times `r^j/j!`; hence it is `A M_j(Br)^j`. The j=0 term is the amplitude bound. Taking the infimum gives the claimed estimate, using the factorial-out M, not the total weight W.

If every coordinate partial of order j has the same budget, expansion of the j-linear form bounds it by `A B^j j! M_j product_l ||v_l||_1`. Since `||v_l||_1 <= sqrt(n)||v_l||_2`, replacing B by `B sqrt(n)` is sufficient. The dimensional factor is correctly exponential in derivative order and absorbed in B, not in one order-independent amplitude constant.

For `M_j=(j!)^(s-1)`, taking j of order `t^(-1/(s-1))` gives the stated exponential upper bound. At the analytic endpoint M=1, the infimum is zero for `0<t<1`, consistently excluding a nonzero exact non-affine analytic germ. The reference to [Rainer Section 7.2](https://arxiv.org/pdf/2107.01061), equation (7.3) and Example 7.1, PDF p. 27, is consistent under the weight translation. The claim does not require the stronger assumptions used for optimal cutoff constructions, and does not concern parameter gradients or learning dynamics. F2 concerns only clarity about the fixed set and budget.

### Theorem 7.3 — all three degree assertions

**Locators:** definitions, TeX lines 544–558, PDF pp. 12–13; theorem/proof, lines 560–624, pp. 13–14; endpoint remark, lines 626–627, p. 14.

**Parity.** The product polynomial has degree |S|. On Boolean vertices, fixing coordinates outside S, every monomial of degree below |S| misses at least one parity coordinate, giving zero correlation. Strict sign agreement gives positive correlation instead. Constants have degree zero. This works for every `0<delta<1`, not merely asymptotically.

**Rational upper bound.** With `m=ceil(log_2(1/delta))`, the smallest node is no larger than delta. The negative and positive real zero sets of the two even-power products are disjoint; their sum is everywhere positive. For every positive guarded t, one node u satisfies `u<=t<=2u`. Its factor has absolute ratio at most 1/3; all other factors have ratio at most one. Thus the stated error bound holds on the entire guarded interval, not just on nodes. Oddness handles negative t. No poles or denominator-sign changes are left unresolved.

The expectation extension is a convex average of the signs throughout `[-1,1]^n`. With coordinate error epsilon, the probability of any changed coordinate is at most `n epsilon/2`, so sign-weighted expectation is at least `1-n epsilon`. Choosing fixed L makes it strictly positive. After substitution, each coordinate occurs multilinearly in the a/q representation; multiplying by one q per coordinate therefore yields total degree at most `2Ln(m+1)`. There is no extra denominator power or implicit amplitude guarantee. [Sherstov Theorem 2.4](https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf), author PDF pp. 11–12, verifies the Newman-type comparison, although the manuscript proves its own dyadic version.

**Non-affine lower bound.** In the F_2 algebraic normal form, all second coordinate differences vanish identically exactly when every coefficient of degree at least two vanishes. A non-affine law therefore has a binary non-affine face. Binary affine laws have an even number of true corners; the eight other tables have one or three true corners, and input flips plus output negation turn each into AND. Fixing other coordinates at +/-1 preserves the guarded-domain inclusion and cannot increase degree.

For sufficiently small delta, take the largest odd integer `N<=1/delta`. Then `N` is comparable to `1/delta`. Every odd signed sum has magnitude at least one, so both normalized majority sums lie in the guarded square. Linear substitution into a continuous-domain AND polynomial preserves total degree and gives a sign representation on an actual finite cube. To align conventions explicitly, for a manuscript polynomial P positive only when both inputs are positive, `-P(-sum(z)/N,-sum(w)/N)` is negative only when both sums are negative. This matches Sherstov's true=-1 conjunction on disjoint variable blocks. [His Theorem 1.10](https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf), author PDF p. 6, gives `Omega(log N)`. The source is not about arbitrary two-halfspace thresholds in this step, and a finite-set theorem is not being directly applied to an infinite interval.

**Bounded margin lower bound.** A changing Boolean edge exists for every nonconstant law. Its slice is bounded on the whole interval, including the excluded gap. The two values differ by at least `2 gamma`, giving a mean-value derivative of magnitude at least `gamma/delta`. Bernstein's interior inequality bounds it by `d/sqrt(1-xi^2) <= d/sqrt(1-delta^2)`. This proves the displayed constant and the asymptotic lower bound. Replacing the whole-cube amplitude condition by a guarded-domain condition would invalidate this argument; the manuscript expressly does not do so.

**Bounded margin upper bound.** The clipped ramp has Lipschitz constant `1/delta`. Its cosine pullback is even, continuous and periodic with the same Lipschitz bound. Jackson approximation followed by even symmetrization leaves a cosine polynomial; Chebyshev substitution gives algebraic degree at most k with error `C/(k delta)`. Dividing by `1+eta` keeps its whole-interval amplitude at most one and guarded sign error at most `2eta/(1+eta)`. Taking `eta <= (1-gamma)/(2n)` is one sufficient fixed choice. The same expectation extension then supplies both the full-cube amplitude and guarded margin. Total degree is at most nk, with constants allowed to depend on fixed n and gamma.

The [Kopotun–Prymak–Shevchuk study guide](https://mathanalysis.knu.ua/wp-content/uploads/2020/07/at-study-guide-january-22-2018-1-1.pdf), Theorem 21.1 (k=1) and Theorem 24.1, PDF pp. 56 and 59 / printed pp. 53 and 56, contains the required inequalities. Its cover confirms the bibliography's title/authors/date. No uniform claim in growing dimension, gamma approaching one, coefficients, or evaluation cost follows. The gamma=1 impossibility and constants are correctly separated in Remark 7.4.

### Section 8.3 — classical R-functions, every k

**Locator:** TeX lines 664–670; PDF pp. 15–16.

For `r>0`, `F_k=r^k(x+y-r)` has a smooth angular part and positive homogeneity of degree k+1 for every integer k>=0. Its derivative of order j is `O(r^(k+1-j))`, so induction gives a `C^k` extension with zero k-jet. To check Lipschitz continuity of `D^k`, take the larger endpoint radius rho. If endpoint separation is at least rho/2, the `O(rho)` size bounds suffice; otherwise the connecting segment stays at radius at least rho/2 and the bounded next derivative suffices. This also handles k=0. Odd powers of r cause no angular singularity away from zero.

A direct independent check of failure of `C^(k+1)` is especially simple:

`F_k(t,0)=0 (t>=0), and F_k(t,0)=-2(-t)^(k+1) (t<0)`.

The one-sided derivatives of order k+1 differ for every k, including zero and odd k. The manuscript's homogeneous-Taylor-polynomial proof is also valid; no repair is required. On the positive diagonal its coefficient is `2^(k/2)(2-sqrt(2))>0`, so no higher exponent can uniformly replace k+1 as the corner tends to zero. This establishes exponent sharpness, not an optimal numerical Hölder constant.

[Shapiro](https://ftp.cs.wisc.edu/pub/users/prem/rfuns.pdf), Section 3.3, equations (3.4)–(3.5), author PDF p. 14, gives the same root family; Section 3.6, pp. 18–19, discusses vanishing derivatives. The manuscript correctly labels the construction classical. The `C^{k,1}` and non-`C^{k+1}` observations are elementary regularity elaborations, not grounds for reclaiming novelty of the family.

### Section 8.4 — analytic formulas and domain restrictions

**Locator:** TeX lines 672–680; PDF p. 16.

Finite compositions are analytic where all constituent maps are analytic and defined. The local obstruction requires a scalar score defined and correct on an entire neighborhood of the common corner, with independently variable coordinates. Fitting finite representatives, reachable inputs on a submanifold, or guarded boxes does not satisfy it. The text includes these qualifications and asserts no training impossibility or neural resource lower bound.

For fixed positive delta the rounded square root is globally analytic. Its two partial derivatives are positive, so the positive-positive guarded minimum occurs at `(delta,delta)` and is `(2-sqrt(3))delta`. With a negative guarded input, the strict comparison with `|y|` gives value less than `-delta` (symmetrically for y). This establishes the claimed guarded margin on the entire stated domain, including its boundaries. The value `-delta` at zero gives wrong signs at sufficiently small positive inputs. Formula dependence on delta and lack of whole-cube amplitude normalization are acknowledged; there is no conflict with Section 7. The min/ReLU identity is correct and is used only as a nonsmooth alternative.

## Novelty, attribution, and comparison with previous judgments

The present manuscript establishes a valid package in its own text: explicit finite-order orthant/arrangement statements, elementary parity propagation, exact realization counts, and the fixed-dimensional guarded-degree taxonomy. “Established here” means proved in this manuscript, not proved historically for the first time.

The polynomial multiplicity mechanism, smooth signature-flatness obstruction, positive-flat existence, R-function family, and rational/Bernstein/Jackson inputs are antecedent material. The finite-order statements are economical consequences of the leading-term proof. Exact counts and selectors give a useful common language but are elementary once the rigidity and positive-flat input are available. The guarded classification's non-affine two-face reduction is a clean synthesis step; its publication value is the complete contrast between domain and normalization regimes. I located no decisive counterexample or demonstrable omitted identical-statement reference in the targeted search, but that does not prove originality.

The abstract, prior-work paragraph, and conclusion generally track this boundary. F1 and F2 sharpen two scope compressions. The title remains appropriate to the paper's principal arc; it need not enumerate every comparison. Repeated disclaimers are better compressed than multiplied. The historical citations are adequate for the actual modest claims, subject to the access limitations below.

The September editorial reports assess the 14-page source, not this 18-page revision. Their stronger “ready” language and numerical scores are not carried forward as certification. The October reassessment's mathematical outline agrees with the independently saved initial reconstruction and verified sources. Its inference against a separate research manuscript is reasonable; I add that a deliberately expository standalone note could have a credible audience, while still preferring integration here. No old repair request remains silently unresolved in the current text: the first-Taylor antecedent, squared-multiplier/homology explanation, positive-flat gluing, and N-dependent-point quantifier correction are present.

## Verification, diagnostics, and limits

- `independent_diagnostics.py` ran successfully under the bundled Python interpreter, using only its standard library and read-only manuscript inputs. It verifies hashes, 24 preserved older blocks, 41 unique labels, 18 bibliography entries, and no missing referenced labels/citations.
- It exhaustively checks the affine/two-face equivalence for all 65,812 Boolean truth tables of arities 1–4, the eight-member binary AND flip orbit, 40 exact rational bounds, 1,216 exact cleared-AND signs across seven widths (including nondyadic widths and delta close to one), and 2,048 expectation-extension cases. It records R-function axis derivative jumps and odd-majority guard examples. See `diagnostics.json` for exact scope. These computations are bounded sanity checks; the universal conclusions rest on the arguments above and primary cited results.
- All 18 PDF pages were rendered and inspected in three contact sheets; pp. 12–14 and 16 were also inspected individually. No visible clipping, equation corruption, overlap, unresolved reference, or unexpected blank page was found. The current package's compiler log has its 18-page output line and no actual LaTeX warning/overfull/underfull diagnostic. No recompilation was needed to resolve a mathematical or layout issue.
- The initial `pdftotext` command resolved to MiKTeX and failed on runtime-directory access; no software or permission change was attempted. Bundled pypdf successfully extracted all pages, and available Poppler rendered them. These read/QA limitations did not affect source review.
- Primary full texts of the decisive Sherstov, Shapiro, Rainer, approximation-guide, and Broglia–Tognoli passages were accessed. The first Shapiro host returned an unusable response; the institutional `ftp.cs.wisc.edu` HTTPS copy worked. Several web PDF screenshot fetches failed; readable full-text extraction remained available.
- Full texts of **Acquistapace–Broglia (1992), “Signatures and flatness,” and its 1993 correction were not obtained**. A publisher DOI access attempt failed and the institutional correction record exposed metadata but no paper. A related [1994 primary paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/ABB8E3FDA7D97595D28F39E905E63EB8/S0008414X00045910a.pdf/when-is-a-distribution-of-signs-locally-completable.pdf) corroborates the broader sign-completability context, not the contents of those missing texts. Russian R-function originals and every neighboring-theory reference were not independently fully audited. Therefore historical exhaustion and the effect of the 1993 correction on the broader literature remain unresolved; no indispensable current proof relies on an unverified theorem from those two texts.
- Search coverage was targeted, not exhaustive backward/forward citation mining. No failed search is treated as proof of priority. This report supplies neither formal proof-assistant verification nor a guarantee of journal suitability.

## Prioritized recommendation to Brian

1. **Before the next circulation:** make F1's margin range explicit and F2's same-set fixed-budget wording explicit. `SUGGESTED_SCOPE_CLARIFICATIONS.patch` contains only those two proposed edits and has not been applied.
2. **Before journal submission:** keep Theorem 7.3, streamline repeated exposition if the chosen venue's note format needs it, and present the article as a finite-order/expository synthesis. Author metadata and journal style remain venue-dependent; no submission is authorized here.
3. **Before any stronger originality claim or second research paper:** obtain the missing signature paper/correction and identify a concrete extension beyond the fixed-dimensional classification. Defer that project until such an extension is selected; more finite-grid checks will not supply it.

The authorized independent review is complete. For the two specified wording edits and routine source/PDF checks, reuse the authoring chat or this review chat with these files; the available gpt-6-luna at medium reasoning should suffice, subject to authorization to edit the manuscript. No model change is made here and no measured cost saving is claimed. A separate-paper research project, if later selected, belongs in a fresh chat with a specific theorem objective and its own authorization; use a mathematical reasoning model at high effort for that substantially more uncertain work. No further review run is needed solely to repeat the completed checks.
