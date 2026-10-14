# Fresh Adversarial Referee Pass
## An Elementary Finite-Jet Approach to Sign Laws on Hyperplane Arrangements
### Current 14-page version - 27 September 2026

## Executive verdict

**Recommendation: MINOR-TO-MODERATE REVISION before journal submission; preprint-ready after the targeted attribution/precision repairs below.**

I found no counterexample to the manuscript's main mathematical statements. The finite-`C^N` arrangement corollary is valid, the local-to-global parity propagation is sound, the Denjoy--Carleman normalization is sound, and the exact counts are correct.

The manuscript is now coherent as a **focused analysis/expository research note**, but a fresh adversarial comparison with the primary literature reveals four places where the historical boundary should be made still sharper:

1. Broglia--Tognoli's 1989 paper already uses the **first nonzero Taylor term / parity contradiction** in its motivating example. The note may claim a systematic, self-contained arrangement-level leading-jet treatment, but should not leave the impression that the leading-term mechanism itself originates here.
2. The manuscript's blanket sentence that the hypotheses of Broglia--Tognoli Theorem 4.2 “therefore apply” omits their explicit homology condition `[Y]=0 in H_{n-1}(M; Z_2)`. For `M=R^n` this is automatic when `n>=2`, but the manuscript includes `n=1`, which should be separated as an elementary case.
3. The citation to **Langenbruch Proposition 1 and (16)** is too specific for the generality claimed. Proposition 1 in that paper is stated under stronger weight assumptions. Rainer's Remark 3.13 is the cleaner authority for the general statement “for every nonquasianalytic weight sequence and every closed set there exists a class function flat on the set and positive real analytic off it.”
4. Rainer Remark 3.13 actually yields more than selector existence: it gives a direct route to **all nonquasianalytic chamber labelings** by multiplying the positive flat function by a chamberwise sign and extending by zero. This should be acknowledged explicitly. The manuscript's selector sum remains useful as a transparent explicit construction, but not as the only known route to the existence theorem.

There is also one mathematical wording issue in the new finite-order paragraph: saying that the `C^infinity` flatness result is the “simultaneous all-orders version” of the finite-`C^N` obstruction is potentially misleading. For each `N`, the point at which the `N`-jet vanishes can depend on `N`; the finite-order corollaries by themselves do not recover a **single flat point** by sending `N` to infinity. The smooth theorem is a stronger all-orders analogue, separately proved.

With these repairs, the note's honest contribution case is:

- a compact self-contained arrangement-level proof using leading homogeneous Taylor terms;
- explicit finite-order (`C^d` and `C^N`) formulations;
- a clean normalization of the Denjoy--Carleman transition;
- an explicit selector/chamber-sum construction even though stronger flat-function existence is known;
- exact realizability counts assembled in one language; and
- a bridge among signature theory, hyperplane-arrangement chamber functions, Boolean sign laws, and ultradifferentiable regularity.

That is a coherent contribution for a short/focused note. It is not a strong novelty case for a theorem-first research journal.

---

# 1. Mathematical audit of the 14-page version

## 1.1 Polynomial weak-sign lemma

**Verdict: correct.**

The divisibility/factor-parity proof works for arbitrary finite families of distinct proper affine hyperplanes, including parallel, nonessential, dependent, and multiply intersecting configurations.

The main ingredients all survive scrutiny:

- if `ell_j` does not divide the residual polynomial `Q_j`, then the restriction of `Q_j` to `H_j` is not identically zero;
- a generic point of a facet can be chosen outside all other hyperplanes and the residual zero set;
- the sign ratio across a generic crossing of `H_j` is therefore the parity of the maximal `ell_j` exponent;
- the chamber adjacency graph is connected;
- crossing a generic point of each hyperplane recovers each exponent bit, so uniqueness holds even when the arrangement realizes only a subset of the `2^m` formal sign vectors.

### Prior-art refinement

Broglia--Tognoli Proposition 2.4 is a closer **published** antecedent to the polynomial factor-parity mechanism than the 2014 MathOverflow discussion. Their proof factors out maximal powers of irreducible defining polynomials and concludes that the polynomial's signature is admissible according to the parity of those powers. For a hyperplane arrangement this specializes directly to the signed-parity form.

**Recommendation:** make Broglia--Tognoli Proposition 2.4 the primary historical comparison for the polynomial lemma. The MathOverflow citation may remain as an informal orthant-specific parallel, but it is no longer doing essential historical work and could be demoted to a footnote or removed.

---

## 1.2 Finite-jet orthant theorem

**Verdict: correct.**

The proof from a first nonzero homogeneous Taylor term is clean. The weak-sign transfer is valid even in directions where the leading polynomial vanishes, because the conclusion needed is only the weak inequality. The equivalence with affine Boolean functions over `F_2` is exact.

The finite-regularity corollary is also correct: if the first nonzero jet has order `d`, a `C^d` Peano/Taylor expansion is enough.

### Prior-art refinement

Broglia--Tognoli's motivating Example 1 already argues with the **degree of the first nonzero Taylor coefficient** and obtains incompatible parity requirements; their following remark states that the corresponding smooth function must be flat. Thus the leading-term parity mechanism itself is not historically new.

What the present note adds is a particularly transparent **general theorem package**: weak-sign polynomial lemma -> arbitrary orthants -> arbitrary finite affine arrangements -> explicit finite regularity.

Recommended language:

> “The first-nonzero-Taylor-term mechanism is already visible in Broglia--Tognoli's motivating crossing example. The purpose here is to isolate it as a general arrangement lemma, give a direct local-to-global proof, and record the finite-order consequences explicitly.”

This makes the manuscript stronger, not weaker, because it states exactly what the reader receives.

---

## 1.3 No-flat-point arrangement theorem

**Verdict: correct.**

The expanded overlap proof is now sufficient for publication.

At `p` the incident arrangement is central after translation. The first nonzero homogeneous term gives local crossing bits. For nearby `p'` on `H_j`, a generic point `q` on `H_j` can be chosen outside every other hyperplane; a tiny transverse pair near `q` lies in both local neighborhoods and computes both `e_j(p)` and `e_j(p')` from the same actual sign ratio. Local constancy follows, and connectedness of `H_j` globalizes the bit. Global chamber adjacency then determines one global constant sign.

No generic-position hypothesis is being used.

### Broglia--Tognoli comparison: one precision repair

The reduction

`G = F * product_j ell_j^2`

is valid: it makes the zero set exactly the arrangement, preserves chamber signs, and preserves nonflatness because the first nonzero Taylor term of `G` is the nonzero first term of `F` times a nonzero polynomial formed from the incident linear forms (and nonzero constants from nonincident factors).

However, Section 4 of Broglia--Tognoli assumes explicitly:

`[Y] = 0 in H_{n-1}(M; Z_2)`.

For `M=R^n`, this is automatic for `n>=2`; the manuscript's blanket statement that the hypotheses “therefore apply” should not silently cover the one-dimensional case. In dimension one the theorem here is elementary anyway.

Recommended replacement:

> “For `n>=2`, Broglia--Tognoli's homology hypothesis is automatic on `R^n`; each hyperplane component has a global affine equation and is arc-analytically connected. Thus their Theorem 4.2 applies to the squared-multiplier reduction. The one-dimensional case is elementary and is covered directly by the proof below.”

This is a citation-precision issue, not a failure of the theorem.

---

## 1.4 Finite-`C^N` arrangement corollary

**Verdict: correct and worth retaining.**

The statement is a genuine finite-order formulation:

- at each wall point `p`, choose the least `d(p)<=N` with a nonzero derivative;
- `C^{d(p)}` suffices for the local leading term;
- parity propagation requires only continuity and nonvanishing away from the arrangement.

The contrapositive is useful:

> a non-parity chamber labeling forces a point where the full `N`-jet vanishes.

### What it is, and what it is not

This is mathematically useful, but it is an **immediate finite-order extraction from the proof architecture**, not yet a deep quantitative theorem. It does not provide a bound depending on arrangement complexity, nor a minimal differentiability threshold, nor information about the size/topology of the high-order vanishing locus.

A targeted search did not locate an identical published `C^N` arrangement statement, but that is not evidence of historical firstness. The manuscript correctly avoids a firstness claim.

### Important wording fix

Current wording says roughly:

> “The `C^infinity` flatness statement is the simultaneous all-orders version of this finite-order obstruction.”

This can be read as claiming the smooth statement follows by taking all `N`. That is not logically valid: for each `N`, the point with vanishing `N`-jet may be a different point.

Recommended replacement:

> “The smooth theorem is the stronger all-orders analogue: it produces a single flat point. The finite-`C^N` corollaries alone do not recover that conclusion by letting `N` tend to infinity, since the point at which the `N`-jet vanishes may depend on `N`.”

### Optional strengthening

If the author wants the finite-order material to carry more of the note's distinctiveness, the cleanest strengthening is not more computation. It is a local formulation with point-dependent regularity:

> If `F` is continuous, nonzero off the arrangement, and at every arrangement point `p` is `C^{d(p)}` in a neighborhood of `p` with a nonzero `d(p)`-jet, then the chamber law is signed parity.

The present `C^N` corollary becomes a convenient uniform special case. This makes the actual mechanism - finite order pointwise, not globally `C^infinity` - especially clear.

---

# 2. Denjoy--Carleman and constructive side

## 2.1 Weight normalization

**Verdict: correct.**

With total weight `W_k=k! M_k`, the criterion

`sum M_k / ((k+1) M_{k+1})`

is exactly `sum W_k/W_{k+1}`. Rainer Theorem 3.6 gives the quasianalyticity criterion in the corresponding weight-sequence convention. The manuscript's use of products, affine pullbacks, translations, sums, and one-dimensional primitives does not require importing the stronger stability assumptions used for more general composition or Whitney extension theory.

Rainer Corollary 3.12 supports compactly supported functions for every nonquasianalytic weight sequence in the needed sense.

---

## 2.2 One-sided selector

**Verdict: correct.**

The squared-cutoff construction

`psi(t) = integral_0^t f(s)^2 ds`

works under the manuscript's stated assumptions. Translating a nonzero compactly supported function so the left endpoint of its support is zero yields `f=0` on `(-infinity,0]`, while every interval `(0,t)` contains a nonzero point. The primitive is therefore positive for every `t>0`.

### Citation issue: Langenbruch

The sentence citing Langenbruch “Proposition 1 and (16)” should be changed. In the 2003 paper, Proposition 1 is stated for an auxiliary sequence satisfying stronger conditions `(M1)` and `(M3')`; it is not the cleanest direct citation for the manuscript's full generality.

Rainer Remark 3.13 is stronger and exactly tailored to the claim:

> for every nonquasianalytic weight sequence and every closed subset `A`, there is a class function flat on `A` and positive and real analytic on its complement.

Rainer explicitly cites Langenbruch's 1999 and 2003 work for this result.

**Recommended repair:** cite Rainer Remark 3.13 directly for the general positive-flat statement. If Langenbruch is retained, describe it as historical source material cited by Rainer rather than pinning the manuscript's exact generality on Proposition 1.

---

## 2.3 A stronger prior-art implication: arbitrary chamber labelings

This is the most important finding of the fresh constructive-side audit.

Rainer Remark 3.13 does not merely imply a one-sided selector. Let `A` be the arrangement and let `g` be flat on `A` and positive on `R^n\A`. Given any chamber labeling `h(C) in {+1,-1}`, define

- `F(x)=h(C) g(x)` for `x` in chamber `C`;
- `F(x)=0` for `x in A`.

Because every derivative of `g` vanishes on `A`, the chamberwise sign changes glue smoothly across `A`. Off `A`, derivatives are just `+/- D^alpha g`; on `A` they are zero. Thus the same ultradifferentiable bounds hold. Consequently the arbitrary-labeling existence half of the nonquasianalytic arrangement theorem is already a direct corollary of the known positive-flat-function result.

The same observation realizes every whole-orthant Boolean law.

### Consequence for the paper

Do **not** remove the selector construction. It is more elementary and explicit, and the finite product/sum formula is valuable. But the manuscript should say plainly:

> “The existence direction also follows immediately from the general positive-flat-function theorem by changing the sign chamberwise; the selector formula below is retained as an explicit elementary realization adapted to the hyperplane coordinates.”

This closes a likely referee objection before it is made.

---

# 3. Literature-positioning audit

## 3.1 Broglia--Tognoli is now correctly central - but can be made more exact

The present revision is a major improvement over the original because it makes the 1989 signature-flatness result central rather than peripheral.

Still, two details should be added:

1. Their motivating Example 1 already exhibits the first-nonzero-Taylor-term parity contradiction.
2. Their Proposition 2.4 is a better peer-reviewed antecedent for the polynomial factor-parity lemma than the MathOverflow discussion.

These two additions prevent the reader from interpreting “leading-jet proof architecture” or the polynomial lemma as more original than intended.

---

## 3.2 Sign-distribution/signature cluster

The inclusion of Fortuna 1991, Acquistapace--Broglia 1992 plus the 1993 correction, Acquistapace--Broglia--Fortuna 1994, and Acquistapace--Broglia 1994 is appropriate and materially improves the literature review.

The note does not need to reproduce that literature's full algebraic program. Its current use - locating the terminology and broader historical problem - is proportionate.

One optional bibliographic addition is Broglia--Tognoli's shorter 1989 announcement/preliminary note on approximation of non-flat smooth functions. It is not necessary if the full Annales de l'Institut Fourier article is cited.

---

## 3.3 Hyperplane arrangements and oriented matroids

Varchenko--Gelfand and Moseley are appropriate. Moseley's published abstract explicitly says the results extend to arbitrary real hyperplane arrangements and oriented matroids.

For a reader from arrangement theory, adding the standard reference

> Björner, Las Vergnas, Sturmfels, White, Ziegler, *Oriented Matroids*, 2nd ed., Cambridge University Press, 1999

would help anchor the chamber/sign-vector/topes language. This is a **P2 completeness improvement**, not a blocker.

A very recent 2026 paper by Yagi and Yoshinaga on reconstruction of oriented matroids from Varchenko--Gelfand algebras confirms that this chamber-function viewpoint remains active, but it is not needed for the mathematical claims here. It may be added only if the author wants the literature paragraph to be current through 2026.

---

## 3.4 MathOverflow and finite-grid sign representation

The MathOverflow and Basu et al. references are not wrong, but they are peripheral after the direct signature literature is acknowledged.

For a short note, the strongest editorial choice may be:

- replace the MathOverflow paragraph's historical role with Broglia--Tognoli Proposition 2.4;
- retain MathOverflow only as an optional informal orthant-specific pointer;
- retain Basu et al. only if the Boolean-function comparison is useful to the intended audience.

Removing one or both would make the literature section look **less defensive and more authoritative**.

---

# 4. Is the paper coherent as a short note?

**Yes, with the targeted changes above.**

The paper now has one coherent question:

> How does finite-order/nonquasianalytic regularity constrain which chamber sign functions can be realized by a single real function?

The sequence is natural:

1. polynomial parity;
2. finite Taylor jets;
3. local-to-global arrangement propagation;
4. finite-`C^N` obstruction;
5. quasianalytic exclusion of flatness;
6. nonquasianalytic explicit realization;
7. exact counts and examples.

The Boolean language does not need to be removed. It is most convincing when presented as a translation layer between chamber sign functions and affine parity, rather than as the source of novelty.

### Editorial limitation

The paper is not a strong theorem-novelty manuscript. Both halves of the `C^infinity`/Denjoy--Carleman dichotomy can be routed through prior work:

- nonadmissible smooth signature -> flat point: Broglia--Tognoli;
- positive flat class function on any closed set: Rainer's Remark 3.13 citing Langenbruch;
- chamber functions/Heaviside algebra: Varchenko--Gelfand.

The paper's value is therefore **proof economy + finite-order extraction + normalization + synthesis + explicit formulas/counts**.

For a venue that publishes concise notes or expository research articles, that is coherent. For a venue expecting a substantial new theorem, it is likely too modest unless the finite-order direction is strengthened beyond the present immediate corollary.

---

# 5. Four adversarial referee perspectives

## Referee 1 - real/functional analyst

**Recommendation: minor revision.**

### Strongest aspect
The local-to-global proof is genuinely clean. The `C^N` formulation makes explicit that smoothness is more than is needed at each wall point.

### Main concern
The sentence calling the smooth flatness result the “simultaneous all-orders version” of the finite-order obstruction should be corrected. It hides a quantifier issue: `exists p_N for every N` is not `exists p for every N`.

### Required changes
- repair that sentence;
- optionally formulate the pointwise finite-order theorem, with `d(p)` varying along the arrangement;
- retain the current proof of parity propagation.

### Assessment
Mathematics is publishable in note form; novelty is modest but the exposition is useful.

---

## Referee 2 - Denjoy--Carleman/quasianalytic specialist

**Recommendation: minor revision.**

### Strongest aspect
The `W_k=k!M_k` normalization is explicit and correct; the paper avoids importing stronger closure hypotheses than it needs.

### Main concern
The Langenbruch citation is too specific. Proposition 1 is not the clean authority for the full generality stated. Rainer Remark 3.13 should carry the general positive-flat claim.

### Additional concern
The manuscript should acknowledge that Rainer Remark 3.13 directly produces arbitrary chamber sign patterns by flat gluing. The selector construction is still worth giving as an explicit elementary alternative.

### Required changes
- change the Langenbruch citation;
- state the direct positive-flat gluing route;
- keep the selector proof but label it as an explicit construction rather than a new existence mechanism.

---

## Referee 3 - hyperplane arrangements/oriented matroids

**Recommendation: minor revision.**

### Strongest aspect
The chamber-crossing parity formulation is transparent and works without general position.

### Main concern
The combinatorics should be tied slightly more explicitly to standard oriented-matroid language. The `2^{m+1}` family is the multiplicative family generated by the oriented hyperplane sign coordinates and a global sign. This is elementary and should not be sold as a new combinatorial classification.

### Required/optional changes
- Broglia--Tognoli Proposition 2.4 should precede MathOverflow as the polynomial antecedent;
- optionally cite *Oriented Matroids* (Björner et al.) for sign vectors/topes/chambers;
- no need to expand the note into an oriented-matroid paper.

---

## Referee 4 - novelty/editorial positioning

**Recommendation: revise before submission; then suitable for a focused note venue.**

### Strongest aspect
The revised manuscript is honest about the known smooth obstruction and succeeds as a bridge across literatures that do not usually speak the same language.

### Main concern
The contribution boundary still has a few phrases that could be read too generously:

- “leading-jet proof architecture” needs the qualification that Broglia--Tognoli already use the first nonzero Taylor term in their basic crossing example;
- the positive-flat theorem already gives arbitrary nonquasianalytic labelings, not merely a selector;
- the finite-`C^N` corollary is useful but currently immediate rather than deep.

### Editorial judgment
After these repairs, I would be comfortable sending the manuscript to referees **if the journal has an appropriate note/expository-research format**. I would not position it as a major original theorem paper.

---

# 6. Updated scorecard after this fresh pass

These scores deliberately reassess the previous optimistic post-revision scorecard.

| Category | Fresh score /10 | Comment |
|---|---:|---|
| Mathematical correctness | 9.0 | No central error found. |
| Proof completeness | 9.0 | Arrangement propagation and finite-order proof are complete. |
| Precision of hypotheses/statements | 8.5 | Fix the all-orders wording and BT applicability sentence. |
| Internal consistency | 9.0 | The note now tells one coherent story. |
| Denjoy--Carleman conventions | 9.0 | Correctly normalized. |
| Arrangement arguments | 9.0 | Sound without generic-position assumptions. |
| Novelty / differentiation | 4.5-5.0 | Finite-order formulation and synthesis are useful; core mechanisms/results have stronger antecedents than even the revision fully spells out. |
| Completeness of literature review | 8.0 | Strong improvement; add BT Example 1/Prop. 2.4 and optionally oriented-matroid standard reference. |
| Citation accuracy / attribution | 7.5 | Main remaining issues are BT Section 4 hypotheses and the Langenbruch pinpoint citation. |
| Resolution of prior concerns | 8.5 | Major priority problem repaired; a few second-order attribution issues remain. |
| Version/provenance reconciliation | 9.0 | Strong. |
| Expository clarity | 8.5 | Good, with a few historical-boundary refinements needed. |
| Accessibility | 8.5 | Good bridge among analysis, arrangements, and Boolean language. |
| Examples/counterexamples | 8.0 | Adequate for a note. |
| Scope discipline / focus | 9.0 | Still focused despite literature additions. |
| Reproducibility / verifiability | 9.0 | Strong for a theorem paper. |
| Title/abstract/claim calibration | 8.5 | Good; one more pass on “leading-jet” contribution language recommended. |
| Journal positioning | 7.0 | Plausible note, not theorem-heavy article. |
| Preprint readiness | 8.0 | Ready after the P1 wording/citation repairs. |
| Peer-reviewed submission readiness | 6.5-7.0 | Targeted revision first; then about 7.5 for an appropriate note venue. |

No arithmetic average is recommended; novelty/positioning is the editorial gate.

---

# 7. Readiness gates

## Gate A - mathematical validity

**PASS.**

No central theorem needs retraction or repair.

## Gate B - priority / novelty

**PASS FOR A REFRAMED NOTE, after the additional attribution repairs.**

The paper should state even more explicitly that:

- BT already contains the leading-term parity idea in a local example;
- BT Proposition 2.4 is a direct polynomial-signature antecedent;
- Rainer Remark 3.13 already implies arbitrary nonquasianalytic sign distributions by flat gluing.

The finite-`C^N` statement remains a defensible finite-order formulation with no historical firstness claim.

## Gate C - preprint readiness

**READY AFTER MINOR REPAIRS.**

The necessary changes are citation/framing/quantifier precision, not new mathematics.

## Gate D - journal readiness

**MINOR-TO-MODERATE REVISION; THEN SUBMIT AS A FOCUSED NOTE.**

Venue selection matters. A journal that expects substantial new theorem content may reject on significance even if every proof is correct.

---

# 8. Prioritized repair plan

## P0 - correctness blockers

**None.**

## P1 - fix before submission

### P1.1 - Broglia--Tognoli applicability sentence

**Current location:** introduction, prior-work paragraph.

**Problem:** omits the Section 4 homology hypothesis and silently includes `n=1`.

**Fix:** state automatic applicability for `R^n`, `n>=2`, and treat `n=1` as elementary separately.

### P1.2 - acknowledge BT's leading-Taylor-term example

**Current locations:** abstract, introduction, conclusion phrases about “leading-jet proof/architecture.”

**Problem:** could imply more originality in the proof mechanism than the 1989 paper permits.

**Fix:** add one sentence noting that their motivating example already uses the first nonzero Taylor coefficient and a parity contradiction; describe the present value as systematic arrangement-level packaging and finite-order extraction.

### P1.3 - replace Langenbruch Proposition 1 pinpoint

**Current location:** “Classical constructive antecedent.”

**Problem:** Proposition 1 uses stronger auxiliary weight hypotheses than the general claim as written.

**Fix:** cite Rainer Remark 3.13 directly for the general positive-flat statement. Retain Langenbruch as the historical source cited by Rainer, without the misleading pinpoint.

### P1.4 - acknowledge direct positive-flat gluing for arbitrary labels

**Current location:** immediately after the constructive antecedent paragraph or before Theorems T5/T6.

**Problem:** the manuscript currently understates the strength of the prior theorem and makes the selector formula look more essential to existence than it is.

**Fix:** add a short paragraph proving the chamberwise sign-flip construction and explaining that the selector is retained for explicitness.

### P1.5 - repair the “simultaneous all-orders” sentence

**Current location:** finite-`C^N` arrangement remark.

**Problem:** quantifier ambiguity/overstatement.

**Fix:** explicitly say the smooth theorem is stronger and the points of `N`-jet vanishing may depend on `N`.

### P1.6 - make BT Proposition 2.4 the main polynomial antecedent

**Current location:** scope subsection on polynomial signs.

**Problem:** MathOverflow is currently given more prominence than the closest peer-reviewed published argument.

**Fix:** cite BT Proposition 2.4 first; demote or remove MathOverflow.

## P2 - high-value improvements

### P2.1 - standard oriented-matroid reference

Add Björner--Las Vergnas--Sturmfels--White--Ziegler, *Oriented Matroids*, 2nd ed. (1999), for the chamber/sign-vector/topes framework.

### P2.2 - optional 2026 VG update

Yagi--Yoshinaga (IMRN 2026) may be mentioned as current evidence that VG chamber algebras and oriented-matroid reconstruction remain active. This is not needed for correctness or priority.

### P2.3 - strengthen finite-order statement locally

Consider stating the point-dependent regularity theorem before the uniform `C^N` corollary. This better expresses the real mathematical mechanism and gives the finite-order contribution more conceptual substance.

### P2.4 - trim peripheral comparison if targeting a strict note format

MathOverflow and/or finite-grid sign-representation discussion could be shortened. The paper is strongest when centered on signatures, finite jets, DC classes, and chamber functions.

## P3 - optional polish

- Add one sentence translating signed-parity laws into products of oriented hyperplane sign coordinates in standard arrangement language.
- Consider changing “short note” to “focused note” if a venue has a formal short-note page limit.
- Add a one-line “Known / supplied here” summary at the end of the introduction.

---

# 9. Suggested exact replacement text

## 9.1 Prior-work paragraph patch

> The smooth arrangement conclusion below is a consequence of the signature-flatness theorem of Broglia and Tognoli. Given a function nonzero off the arrangement, multiplication by the square of every defining affine form produces a function with zero set exactly the arrangement while preserving chamber signs and nonflatness. For `n>=2`, their homology hypothesis is automatic on `R^n`; hyperplane components have global affine equations and are arc-analytically connected, so their theorem applies. The one-dimensional case is elementary and is covered directly below. For a hyperplane arrangement their admissible signatures are precisely the signed-parity laws. Their motivating crossing example already uses the first nonzero Taylor coefficient to force an even/odd parity contradiction; the purpose here is to isolate that mechanism systematically for arbitrary arrangements and finite regularity, not to claim its invention.

## 9.2 Positive-flat antecedent patch

> A stronger existence statement is classical. Rainer's Remark 3.13, citing work of Langenbruch, states that for every nonquasianalytic weight sequence and every closed set `A` there exists an ultradifferentiable function flat on `A` and positive real analytic on its complement. Taking `A=(-infinity,0]` gives a one-sided selector. More generally, taking `A` to be the arrangement and multiplying this positive flat function by an arbitrary locally constant sign on the chambers, then extending by zero on `A`, directly realizes every chamber labeling in the same class. We nevertheless retain the squared-cutoff selector and finite chamber sum because they give an explicit elementary formula adapted to the defining affine forms.

## 9.3 Finite-order remark patch

> Equivalently, a non-parity chamber labeling realized by a `C^N` function forces the full `N`-jet to vanish at some arrangement point. The smooth theorem is a stronger all-orders analogue: it yields a single flat point. The finite-order statements alone do not imply that conclusion by letting `N` tend to infinity, because the vanishing point may depend on `N`.

## 9.4 Polynomial antecedent patch

> The factor-parity mechanism is classical. In Broglia--Tognoli Proposition 2.4, maximal powers of irreducible defining polynomials determine whether a polynomial-induced signature changes sign along each component; for hyperplanes this is exactly the parity-bit argument used here. A later MathOverflow discussion gives the same observation in the coordinate-orthant language.

---

# 10. Final editorial judgment

If I were the handling editor, I would **not reject the note for mathematical correctness**. I would ask for the targeted historical and quantifier repairs above before sending it to external referees. Once repaired, I would regard it as a plausible focused note whose value is transparency, finite-order formulation, and synthesis.

The decisive editorial question would be significance, not validity:

> Does this journal publish short notes in which the principal `C^infinity` theorem is known but the author supplies a very clean proof, finite-regularity consequences, and an exact ultradifferentiable realization package?

For an appropriate venue, the answer can reasonably be yes. For a journal that requires a substantial new theorem as the main result, the finite-`C^N` material in its current form is probably not enough on its own.

## Single highest-value next action

Apply the six P1 repairs and then run one final **claim-by-claim red-team read of the revised introduction/abstract/conclusion only**. The mathematics does not need another wholesale rewrite.

---

# Sources checked in this pass

- F. Broglia and A. Tognoli, “Approximation of C-infinity-functions without changing their zero-set,” *Annales de l'Institut Fourier* 39 (1989), 611-632. DOI: 10.5802/aif.1178. Primary checks: Example 1 and following flatness remark; Definition 2.2; Proposition 2.4; Section 4 hypotheses; Theorem 4.2; Remark 4.6.
- A. Rainer, “Ultradifferentiable extension theorems: A survey,” *Expositiones Mathematicae* 40 (2022), 679-757. DOI: 10.1016/j.exmath.2021.12.001. Primary checks: Theorem 3.6, Corollary 3.12, Remark 3.13, bibliography entries [55]-[56].
- M. Langenbruch, “A general approximation theorem of Whitney type,” RACSAM 97 (2003), 287-303. Check: Proposition 1 and surrounding hypotheses; comparison with Rainer's general formulation.
- A. N. Varchenko and I. M. Gel'fand, “Heaviside functions of a configuration of hyperplanes,” *Functional Analysis and Its Applications* 21 (1987), 255-270. DOI: 10.1007/BF01077800.
- D. Moseley, “Equivariant cohomology and the Varchenko--Gelfand filtration,” *Journal of Algebra* 472 (2017), 95-114. DOI: 10.1016/j.jalgebra.2016.10.010.
- F. Acquistapace, F. Broglia, E. Fortuna, “When is a Distribution of Signs Locally Completable?”, *Canadian Journal of Mathematics* 46 (1994), 449-473. DOI: 10.4153/CJM-1994-024-2.
- A. Björner, M. Las Vergnas, B. Sturmfels, N. White, G. M. Ziegler, *Oriented Matroids*, 2nd ed., Cambridge University Press, 1999.
- Y. Yagi and M. Yoshinaga, “Reconstruction of oriented matroids from Varchenko--Gelfand algebras,” *International Mathematics Research Notices* (2026), rnag109. DOI: 10.1093/imrn/rnag109. Optional current-context source only.
