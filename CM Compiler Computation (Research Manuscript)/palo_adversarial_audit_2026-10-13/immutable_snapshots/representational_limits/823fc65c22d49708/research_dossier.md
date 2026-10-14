# Exact Boolean interpretation, regularity limits, and constructive alternatives

**Assessment date:** 13 October 2026, Asia/Bangkok.  
**Disposition:** **Merge with the existing Finite Jet manuscript; reshape the extension around normalized resources. Defer a separate paper.**  
**Evidence level:** primary-source investigation, direct proof audit, complete arguments for derived corollaries, and small reproducible diagnostics. No historical-priority guarantee, formal proof certification, neural training, or integrated PALO implementation.

## 1. Decision and significance

The proposed direction has mathematical substance, but its obvious headline is already covered by Brian's Finite Jet manuscript and older signature/flatness and R-function literature. Applying the obstruction to finite analytic neural models is an immediate corollary under the exact whole-orthant specification. Exact Boolean operations built from continuous or finitely differentiable scores are a long-standing topic in R-function theory. A standalone paper consisting of those connections would overlap heavily with the existing manuscript.

The investigation produced a more useful resource comparison. On a fixed-dimensional bounded cube, excluding a coordinate-wall region of width \(\delta\):

| Requirement on a polynomial score | Derived degree conclusion |
|---|---|
| Signed parity; only strict sign correctness | Exactly the parity support size |
| Non-affine Boolean law; only strict sign correctness | \(\Theta_h(\log(1/\delta))\) as \(\delta\to0\) |
| Any nonconstant law; score bounded by one on the entire cube; fixed margin \(0<\gamma<1\) | \(\Theta_{h,\gamma}(1/\delta)\) |
| Non-affine law on every local open orthant, with the common corner included in the analytic domain | No polynomial/analytic realization |

Full definitions and arguments are in [proof_notes.md](proof_notes.md), Proposition P1. The logarithmic lower bound uses a finite majority-function reduction to Sherstov; the upper bound uses a Newman-style rational construction and positive denominator clearing. The bounded-margin result uses Bernstein and Jackson inequalities. These are **derived consequences of existing results**, rather than demonstrated original contributions.

Two further consequences clarify what regularity buys. A non-affine \(C^{k,\alpha}\) exact orthant score has corner magnitude bounded by a constant times \(r^{k+\alpha}\), and this rate can be attained by standard angular cutoffs. A smooth exact score with a fixed Denjoy-Carleman derivative budget has margin controlled by the standard associated function of its weight. Neither result by itself clears a novelty threshold.

The best immediate use is an R-function prior-work comparison and a short normalized-resource discussion in **Finite-Jet Sign Rigidity on Hyperplane Arrangements and Denjoy-Carleman Realization**. The growing-arity, conditioning-aware resource problem could support a later paper if it yields a theorem beyond established threshold-degree and approximation composition results.

**Readership:** approximation theory and real geometry first; learning theory for resource lower bounds; formal methods for the domain/abstraction contract. A general neural-network audience would need architecture-specific consequences and substantive experiments beyond a two-input illustration.

## 2. Sources, versions, and workspace provenance

The handoff report was read first as orientation. Its source claims were checked against originals for the decisive points. Its 40,668 exact rational assertions are unrelated to the new checker and are not evidence for the proofs or novelty assessed here.

The checkout was already substantially dirty. Initial Git status and diff statistics were saved as **initial_git_status.txt** and **initial_git_diff_stat.txt**. Work in this investigation is confined to this folder. No manuscripts, shared comparative report, sibling folders, tracked implementation files, commits, or external services were changed.

No project AGENTS.md was found at the applicable root/output ancestors; Brian's supplied global instructions and this research handoff govern the work. Navigation within the manuscript collections explicitly selects the following sources:

| Key | Exact selected version | Locators used |
|---|---|---|
| FJ | September 27 final source-of-record package; 14-page PDF and matching final .tex | Sections 2-7; Lemma 3.1; Theorems 4.1, 4.3, 4.5, 4.7, 5.3, 6.1 |
| GU | September 28 reviewed package; 14-page PDF | Theorem 3.2, pp. 5-6; Section 3.3; Propositions 4.1-4.3; Proposition 5.2 |
| LM | September 27 final adversarial revision; 32-page PDF | Typed Boolean representation/frame distinction; used as context, not a full proof audit |
| PALO | Supplied 57-page author manuscript, first page dated December 2020 and carrying a 2021 notice | Section 3.1, pp. 12-14; Section 3.7, p. 26; primitive semantics and dependence discussion |

The matching PDFs have the same SHA-256 hashes as the parent inventory. Exact paths, observed page counts, and hashes are recorded in [local_source_versions.json](local_source_versions.json). FJ's hash is **34de9849f40be2775d70f9c4b16fc3d011622e029987833f513f933c94dfca94**. Its final-package README explicitly names both final source and candidate PDF as source of record. Collection navigation updated September 30 points to this same package. Older root readiness language mentioning divergent page counts is not a newer scientific version.

The Guarded and CM/LM collection guides likewise point to the handed-off revisions. Modification times were not used to choose versions. PALO bibliographic metadata identifies the journal record as JLAMP 124, article 100719 (2022), DOI [10.1016/j.jlamp.2021.100719](https://doi.org/10.1016/j.jlamp.2021.100719). Page references here use the supplied author manuscript.

FJ PDF pages 3, 4, 6, 7, and 8 were rendered with bundled Poppler; pages 3, 4, 6, and 7 were visually inspected, including the exact weight convention and parity-propagation argument. The full extracted text and authoritative .tex were also read. This checks interpretation and transcription; it is not an independent peer-review certificate.

## 3. Hypothesis and proof audit of the existing results

### 3.1 Finite-order orthant rigidity

FJ Theorem 4.1, PDF p. 6, requires \(C^\infty\) regularity on a neighborhood of zero, nonvanishing at every point with nonzero coordinates in a centered ball, and a nonzero derivative of some finite order at zero. The sign on each local open orthant is then constant. A least nonzero homogeneous Taylor polynomial inherits those signs **weakly**, including directions where that polynomial vanishes. Lemma 3.1 concerns weak signs; it does not incorrectly require a strictly nonvanishing leading polynomial.

The argument was reconstructed: for each fixed direction \(v\), divide \(F(tv)\) by \(t^d\) and take \(t\downarrow0\). This yields \(h(\operatorname{sgn}v)P_d(v)\ge0\). The polynomial lemma uses maximal multiplicity of each hyperplane factor, a generic facet point at which the residual factor is nonzero, and connected chamber adjacency. Factor parity is therefore fixed across each hyperplane. No uniform-in-direction Taylor estimate is needed for this qualitative step.

Theorem 4.3 states the finite version: \(F\in C^d\), all lower derivatives vanish, and some derivative of order \(d\) is nonzero. It covers \(d=0\). Consequently a non-affine \(C^k\) realization has a zero \(k\)-jet; it need not be flat in the infinite-order sense unless it is smooth. This distinction is essential for the classical finitely differentiable R-function alternatives.

No gap was found in this direct orthant argument. This is an informal mathematical audit, not exhaustive independent certification of the manuscript.

### 3.2 Arrangement rigidity and its global assumptions

FJ Theorem 4.5, pp. 7-8, concerns a finite set of **distinct proper affine hyperplanes**, \(F\in C^\infty(\mathbb R^n)\), nonvanishing off their union, and **no flat point anywhere on that union**. Nonflatness at a chosen common corner alone is insufficient for the global conclusion.

At a wall point \(p\), choose a ball avoiding hyperplanes not incident to \(p\). Translate its incident arrangement to a central one and apply the leading-polynomial argument. A sufficiently nearby point \(p'\) on a given hyperplane has a ball inside the first ball. A generic transverse pair on that hyperplane lies in both balls and off all other hyperplanes, so the ratio of actual signs determines the same local parity in both. Local constancy propagates along the connected affine hyperplane, including intersections. Chamber-graph connectedness supplies the final common sign.

Theorem 4.7, PDF p. 8, requires \(F\in C^N(\mathbb R^n)\) and a nonzero \(N\)-jet at **every** wall point. The first nonzero order may vary with the point but is bounded by \(N\). It follows that a non-parity chamber law forces a zero \(N\)-jet somewhere. The point can depend on \(N\); a limit of these finite-order statements does not establish one flat point. The smooth proof separately supplies that conclusion.

The direct propagation argument was checked and appears sound under these assumptions. It should not be replaced by a theorem on a unit times a normal-crossing monomial: \(xy(x^2+y^2)\) has the same real zero support and parity signs but a residual factor vanishing at the origin.

The manuscript's Broglia-Tognoli reduction is appropriate: \(G=F\prod_j\ell_j^2\) has exactly the arrangement as zero set, preserves signs, and preserves a nonzero leading jet because the product of nonzero polynomials is nonzero. For \(n\ge2\), the relevant homology of \(\mathbb R^n\) vanishes; hyperplane components have global equations and analytic-arc connectivity. Dimension one is handled directly. This is historical overlap, not an additional novel theorem.

### 3.3 Denjoy-Carleman dichotomy

FJ Section 2.3, PDF p. 4, fixes the **compactwise Roumieu**, factorial-out convention:

\[
M_0=1,\quad M_k>0,\quad M\text{ nondecreasing and log-convex},\qquad
|D^\alpha F(x)|\le C_K\rho_K^{|\alpha|}|\alpha|!M_{|\alpha|}.
\]

With total weight \(W_k=k!M_k\), the criterion becomes

\[
\sum_{k\ge0}\frac{M_k}{(k+1)M_{k+1}}
=\sum_{k\ge0}\frac{W_k}{W_{k+1}}.
\]

This agrees with the total-weight convention in the inspected Rainer text. There is no missing factorial. The proofs need finite sums/products, affine precomposition, and one-variable primitives; log-convexity and monotonicity suffice for these operations. General composition or derivative stability is not silently assumed.

On the divergent side, Taylor injectivity excludes a flat germ nonzero on all local cells; parity polynomials provide sufficiency. On the convergent side, a compactly supported nonzero function \(f\) can be translated so its support begins at zero. The primitive of \(f^2\) is zero on the negative half-line and positive at every positive argument; every interval to the right of its support endpoint contains nonzero values. This verifies the selector mechanism without assuming a positive cutoff was provided initially.

For arrangements, a fixed sign cell is an intersection of open half-spaces and therefore convex. Distinct chambers have distinct realized sign vectors. Each chamber selector is active only in its own chamber, so there is no cancellation. Crossing a generic facet recovers each parity bit and then the global sign, yielding \(2^{m+1}\) distinct laws; the arbitrary-label side has \(2^r\). The counts concern the **full classes**, not finite neural architectures. Parallel hyperplanes have \(r=m+1\), so the two counts can coincide.

Gevrey \(s=1\) is analytic in these conventions; \(s>1\) is non-quasianalytic. Existence of selectors in a class does not establish a network representation, efficient formula, uniformly bounded derivative constants, or trainability.

## 4. Closest works and precise overlap

Bibliography details and primary links are in [references.bib](references.bib). Annotations distinguish inspected results from material still unavailable.

### A. Broglia and Tognoli (1989): direct qualitative antecedent

[Published paper](https://www.numdam.org/item/10.5802/aif.1178.pdf), AIF 39(3), 611-632, DOI 10.5802/aif.1178. Inspected Proposition 2.4, printed pp. 616-617; Section 4 hypotheses, p. 628; Theorem 4.2 and proof, pp. 629-630; Remark 4.6, p. 631. The result links non-admissible signatures to flatness under zero-set, homology, and component conditions. The affine-arrangement reduction above is substantive overlap. This source already motivates leading-term detection. Analytic-network impossibility is not historically new merely because the application vocabulary changes.

### B. Rvachev/Shapiro R-functions: constructive alternatives and regularity

[Shapiro's 2007 author PDF](https://ftp.cs.wisc.edu/pub/users/prem/rfuns.pdf), Acta Numerica 16, 239-303, DOI [10.1017/S096249290631001X](https://doi.org/10.1017/S096249290631001X). Decisive author-PDF locators: Section 3.3, pp. 12-14, equations (3.3)-(3.5); Section 3.6, pp. 18-19; zero conventions, Section 3.7, p. 19. These include min/max, root-based AND/OR analytic off the common zero, and finite-regularity upgrades with vanishing corner derivatives. The [1991 Cornell primer](https://hdl.handle.net/1813/7059) establishes an older English-language entry point; its full text was not independently audited. Generic exact sign construction, finite regularity, and the punctured-plane example require this comparison. Russian original priority was not resolved.

### C. Rainer and Langenbruch: class conventions and quantitative machinery

[Rainer's December 30, 2021 author version](https://www.mat.univie.ac.at/~armin/publ/survey-UET.pdf), published Expositiones Mathematicae 40(3) (2022), 679-757. Inspected Theorem 3.6, p. 13; Corollary 3.12 and Remark 3.13, p. 15; Section 7, pp. 26-30. The source verifies the quasianalytic criterion and positive-flat/cutoff inputs. Its associated-function lower bounds and optimal-cutoff discussion overlap the proposed quantitative extension. Strong non-quasianalyticity is needed for the optimal-cutoff equivalence, beyond ordinary non-quasianalytic existence. Its references lead to [Langenbruch (2003)](https://rac.es/ficheros/doc/00128.pdf); that paper's conventions and approximation setup were inspected, but its full extension machinery was not independently re-proved.

### D. Sherstov/Newman: the strongest resource candidate already has a close antecedent

[Sherstov's author manuscript](https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf), published SIAM J. Comput. 42(6) (2013), 2329-2374, DOI 10.1137/100785260. Inspected Theorems 1.4 and 1.10, author pp. 4 and 6, and the full Newman construction in Theorem 2.4, pp. 11-12. The finite majority lower bound and rational construction give Proposition P1 via an explicit reduction. The general composition statements also constrain novelty for growing-arity extensions. A superficially new degree-versus-boundary theorem must be compared to these results.

### E. Classical approximation: normalization changes the problem

[Kopotun, Prymak, and Shevchuk's 2018 study guide](https://mathanalysis.knu.ua/wp-content/uploads/2020/07/at-study-guide-january-22-2018-1-1.pdf), Theorem 24.1, printed p. 56 / PDF p. 59; Sections 20-21 for Jackson kernels. A directly inspected Lipschitz approximation statement is [Bizeul and Klartag, Section 2.3, equation (35), PDF p. 12](https://www.weizmann.ac.il/math/klartag/sites/math.klartag/files/uploads/lipschitz_regression.pdf). These standard inequalities supply the bounded-margin argument. [Eremenko and Yuditskii's two-interval sign approximation](https://math.purdue.edu/~eremenko/dvi/sgn2.pdf), Theorem 1.1 and Section 8, gives closer extremal context, but fixed-interval asymptotics were not extrapolated uniformly to shrinking gaps.

### F. Chen, De, Servedio, and Tan: standard smooth orthant cutoffs

The supplied [IAS PDF](https://www.ias.edu/sites/default/files/math/csdm/14-15/ChenDeSerTan.pdf) is a December 2014 preprint of **Boolean function monotonicity testing requires (almost) \(n^{1/2}\) non-adaptive queries**, later [STOC 2015, pp. 519-528](https://www.cs.columbia.edu/~rocco/papers/stoc15.html). Inspected Proposition 4.3, pp. 12-13, Proposition 4.4, Claim 4.5, and their proofs. It constructs union-of-orthants cutoffs with \(\delta^{-k}\) derivative estimates and derivative-support control. The paper itself calls the basic cutoff properties standard. Generic cutoffs with this scaling are not a new contribution.

### G. Differentiable-logic and neural connections

[Varnai and Dimarogonas, 2020](https://arxiv.org/pdf/2003.06041), Section IV.B, Proposition 1, PDF p. 4, proves incompatibility of soundness, idempotence, and smoothness for an AND robustness operation; its first-order proof was inspected. These assumptions differ from finite-jet rigidity, which does not require idempotence.

[Flinkow et al., QLL v2, May 14, 2026](https://arxiv.org/html/2605.13845v2), Section 3, equation (3), Theorem 3.7, Appendix A.2, and Section 4.4 were read. Soundness in Theorem 3.7 is for the \(p=\infty\) lattice limit; finite-temperature semantics need not have that exact Boolean property. QLL studies logical laws, gradients, losses, and verification, rather than this full orthant sign classification. Generic smoothness/logic tension is already active work.

[Kucherenko and Shah, GRS-KAN v1, July 1, 2026](https://arxiv.org/html/2607.01449v1), Section 2.2 equations (5)-(6), Section 2.3, and Section 3 equations (18)-(21) were read. It integrates R-functions with neural branches and sigmoid gates. This is a current counterexample to a broad novelty claim about combining those ideas. No publication beyond the preprint was verified.

[Sukumar and Srivastava, arXiv v2, November 7, 2021](https://arxiv.org/abs/2104.08426), is a neural boundary-condition application of R-functions. The full PDF retrieval failed; its bibliographic/abstract evidence is background only, not a theorem supporting this assessment.

### H. Signature literature beyond the main antecedent

The [1994 Acquistapace-Broglia-Fortuna paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/ABB8E3FDA7D97595D28F39E905E63EB8/S0008414X00045910a.pdf/when-is-a-distribution-of-signs-locally-completable.pdf), CJM 46(3), 449-473, has an algorithmic local-completability/separation setting for algebraic surfaces. Its introduction, type-changing discussion, and concluding separation procedure were inspected. This is broader real-geometry context, not the quantitative theorem proposed here. The 1992 **Signatures and flatness** and its 1993 correction were identified, but full texts were not retrieved; the [Pisa correction record](https://arpi.unipi.it/handle/11568/175441) has no associated file. Those remain explicit priority-audit dependencies.

## 5. Preferred question and alternatives

**Preferred question:** For an explicitly chosen family of Boolean laws with growing arity, what is the sharp joint tradeoff between excluded boundary width, bounded score margin, polynomial degree, and coefficient/evaluation conditioning?

Begin with \(D_{\delta,n}\) and \(\|P\|_{[-1,1]^n}\le1\), \(hP\ge\gamma\), fixing an explicit coefficient norm or rational coefficient-bit convention. The model family should be declared before choosing a baseline: ordinary polynomials, positive-denominator rational scores, and a specified circuit basis are different resources.

**What is already derived:** Proposition P1 settles fixed arity at the asymptotic level. There is also a direct compactness argument that bounded-degree polynomials cannot realize a non-affine law on a sequence of shrinking guards: normalize coefficient vectors, take a nonzero limiting polynomial, inherit weak orthant signs, and apply the polynomial lemma. P1 strengthens this qualitative divergence with an existing lower-bound reduction.

**What remains unproved:** a matched theorem uniform in \(n,\delta,\gamma\), a useful additional conditioning/bit-cost bound, and any separation from known threshold/rational approximation composition theorems. Candidate families include AND, parity, and bounded-depth read-once formulas; the last two must be compared directly to Sherstov's Section 3.4. There is no asserted formula for the general joint tradeoff.

**Alternative 1:** corner margin under \(C^{k,\alpha}\) or Gevrey budgets. P2 and P3 give precise, normalized consequences with proofs. Their ingredients are standard, and R-function/cutoff examples attain the basic finite-regularity rate. This is good explanatory manuscript material, weak standalone novelty.

**Alternative 2:** a necessity/sufficiency classification for an actual architecture. A finite analytic tanh/sigmoid score cannot realize non-affine whole-orthant signs; min/max and the \(R_0^k\) families can. A new architecture theorem needs restrictions beyond this immediate regularity application, for example fixed width, bounded parameter norms, fixed input features, and an explicit margin. No such sharp architecture theorem was proved here.

**Alternative 3:** connect a regularity obstruction to the complexity of a guarded alternative. A universal connection is false without a fixed guard language and charges for derived features. The guarded domain is defined by \(n\) input sign tests; an unrestricted final Boolean lookup changes the cost model. The current GU theorem concerns polynomial tests in magnitude-parameter coordinates, rather than polynomial score degree on a shrinking input domain. Its degree-cardinality theorem does not transfer merely because both problems involve signs.

## 6. Falsification and diagnostic results

The serious falsification attempts were conceptual as well as computational:

1. **Dropped the corner:** the punctured-plane R-function realizes OR analytically. Hence connectedness alone is insufficient.
2. **Dropped whole-cell quantifiers:** polynomial interpolation realizes every finite table, including AND. This invalidates a general claim that analytic networks cannot learn AND.
3. **Dropped infinite differentiability:** the classical homogeneous \(R_0^k\) score realizes AND in \(C^{k,1}\), with no nonzero \(k\)-jet. Finite regularity is not a parity-only expressiveness class.
4. **Kept analytic regularity but excluded walls:** rounded root and soft-minimum scores realize guarded AND with explicit shrinking margins. Flatness estimates cannot be applied to them.
5. **Removed normalization:** positive scalar multiplication changes any claimed margin-resource tradeoff. The bounded polynomial theorem therefore normalizes amplitude on the entire cube.
6. **Tried a logarithmic degree theorem as new:** the majority reduction and Newman construction supply the same scale from known results. This attempt strengthened the mathematical dossier while weakening the distinct-paper case.
7. **Tried to identify regularity with Boolean complexity:** flat angular selectors can use the same pointwise derivative bounds for all labelings of fixed dimension, while their explicit table size can be exponential. Regularity norms do not alone measure representation/evaluation complexity.
8. **Tried a CM-specific advantage:** replacing CM coefficients by ordinary truth-table coefficients leaves every proof intact. No unique expressiveness or complexity result was found.

The reproducible [verify_candidates.py](verify_candidates.py) uses standard-library exact fractions. It passed **23,962 exact rational assertions** and **32 floating-point assertions**. The exact checks include all binary and ternary finite truth tables, all affine counts/two-face witnesses, and six dyadic rational constructions with \(\delta=1/2,\ldots,1/64\). The float checks illustrate four soft-minimum choices.

The explicit degree upper bounds for binary AND were 8, 12, 16, 20, 24, and 28. After safe whole-cube amplitude normalization, this simple construction's certified margin lower bounds range from about \(10^{-1.9}\) to \(10^{-26.0}\). These are conservative **construction-specific lower bounds**, not optimal margins or universal impossibility bounds. Exact fractions and actual balanced-corner margins are in [verification_results.json](verification_results.json).

The universal sign upper bound comes from the written interval argument, not the sample grid. The script does not certify the manuscript proofs, best approximation constants, optimum degree, Gevrey membership, training, or numerical implementation stability. No project implementation surface was changed, so the repository's unrelated test suite was not run.

## 7. CM/LM's role and value in both directions

CMs give ordered Boolean coefficients; the fixed-frame LM lift supplies a formula-valued, compositional Boolean representation. Those are legitimate endpoints for an exact sign abstraction. In this investigation, the numerical extension \(H_h\) is ordinary multilinear interpolation/expectation with those coefficients. It uses real arithmetic, whereas the native Boolean-ring operations use XOR. These semantics must remain distinct.

**Truth-table replacement test:** no theorem, sign obstruction, degree bound, cutoff construction, lower-bound reduction, or guarded realization in this dossier is lost if the CM/LM encoding is replaced by an ordinary truth table. The LM layer contributes the portfolio's existing typed symbolic coherence when an implementation needs it; it is not responsible for the new analytical capability. No compression or speedup is inferred.

**Value for PALO:** the source's finite tanh/sigmoid tensor predicate examples are analytic functions of their real inputs, so the exact whole-orthant specification can be screened for impossibility. This requires that the sign coordinates describe a full neighborhood containing the common corner. A learned embedding, unreachable polarity cells, or a different predicate abstraction need not satisfy that premise.

PALO's Section 3.7 crispifies within interpretation. That insertion can create a nonsmooth/discrete intermediate computation and therefore support classical Boolean composition without asking one analytic final score to implement the same whole-orthant law. Merely thresholding the final soft output is a different contract. The regularity theorem reveals this design distinction; it does not show that PALO's stated semantics is defective.

**Reciprocal portfolio value:** PALO supplies a motivated use case for specifying input features, reachable cells, thresholds, excluded regions, and margins. It does not establish a training failure caused by corner flatness. Spatial derivatives at one point do not determine parameter gradients or optimization on data supported away from that point.

**Manuscript placement:** Finite Jet should receive the R-function comparison and carefully bounded resource corollaries. GU should only receive a short cross-reference if authorized later: its existing Theorem 3.2 already fixes original coordinates and a polynomial guard library, and Proposition 5.2 already states representation invariance. No new compiler contribution is claimed here. Chain-ring sources were kept peripheral because no necessary link emerged.

## 8. Minimum credible package and stopping criteria

**Immediate package for the existing manuscript:** a concise R-function prior-work paragraph; one proposition or remark contrasting whole-orthant realization with \(D_{\delta,n}\); exact normalization of margin/resource claims; and the derived P1/P2 results only if they fit the short-note scope. The longer approximation/threshold-degree argument may belong in supplementary notes instead of expanding a focused analysis article. No source manuscript was edited.

**Conditional future title:** *Boolean Sign Laws with Excluded Boundaries: Degree, Margin, and Conditioned Realization*.

**Provisional abstract, contingent on additional results:**  
“We study polynomial and rational scores that induce a prescribed Boolean law on a cube after an explicit neighborhood of the coordinate walls is excluded. We distinguish sign correctness from bounded-margin correctness and account separately for degree and numerical resources. Building on exact sign-rigidity and classical approximation results, we seek matching bounds for specified families as arity and boundary width vary, together with constructions whose coefficients and evaluation costs are controlled. Exact nonsmooth and flat smooth realizations provide alternative resource regimes.”

This is a research aim, not a completed-publication abstract claiming the missing theorem.

**Outline:** domain and resource contracts; closest-work comparison; fixed-arity corollaries as background; one genuinely new joint theorem; explicit constructions and their conditioning; comparison to min/max/R-functions and analytic guarded approximations; limits and relation to crisp interpretation.

**Required proof work:** a sharp growing-arity lower bound; a matched constructive upper bound with the same normalization; actual coefficient/bit/evaluation guarantees; exact scope of any guard comparison; and an explicit argument that the result is not a restatement of known rational/threshold-degree composition or optimal-cutoff theory.

**Meaningful baselines:** parity product; ordinary multilinear interpolation at finite representatives; Newman/dyadic rational construction; appropriate Zolotarev approximants if conditioning is studied; bounded Jackson construction; exact min/max or ReLU realization; classical \(R_0^k\); analytic rounded root/soft minimum; flat selectors. Compare like-for-like domains and margins. A truth-table implementation is mandatory if CM encoding is used.

**Experiments:** for a mathematical paper, proofs are central and diagnostic examples are sufficient support. If architecture claims are made, add modest controlled experiments separating finite representatives, guarded whole regions, and near-corner behavior. Measure certified margin, declared norm, parameter/degree resources, arithmetic cost, and conditioning. A dense grid alone does not certify whole-region correctness; a neural-training benchmark without a new theorem would change this into a different project.

**Stop a separate-paper effort if:** the candidate theorem reduces to Sherstov/Newman plus Bernstein/Jackson; the “new” construction is an \(R_0^k\) or standard cutoff; normalization makes the proposed advantage disappear; complexity relies on uncharged features/guards; or no result remains after replacing CM/LM by ordinary tables. Most of these stopping criteria already apply to the initial broad direction.

## 9. Search reach, remaining limits, and next steps

Searches were made through the current task date, October 13, 2026. They followed backward citations from the final FJ bibliography and Shapiro/Rainer/Sherstov, and searched forward connections to QLL, R-functions in neural architectures, PINNs, and current sign/orthant work. The July 2026 GRS-KAN preprint was found and read beyond its abstract. Search-result crawl dates were not treated as publication dates. Direct links and locators, rather than search snippets, support the decisive comparisons.

This was a focused first investigation, not an exhaustive citation-network export. Full texts of the 1992 signature paper and 1993 correction, some Russian R-function originals, and the neural PINN PDF remain unavailable in this run. Cambridge/SRI/publisher metadata and accessible author copies were used where available; some publisher/author-host downloads failed. No subscription bypass, paid database, or historical-priority guarantee was attempted.

**Established/source-audited:** the exact hypotheses and direct mechanism of the supplied finite-order/arrangement results; the normalization and selector input; older R-function alternatives; existing threshold-degree and approximation inputs.

**Derived with complete arguments:** P1's fixed-arity resource classification, P2's finite-Hölder corner estimate/construction, and P3's associated-function margin implication. These remain appropriate for independent mathematical review before manuscript insertion.

**Unproved/unimplemented:** historical originality, a growing-arity/conditioning theorem, network resource minima, an integrated PALO/CM system, neural optimization consequences, and runtime gains.

Priorities are:

1. **Optional, highest value:** author review of the R-function overlap and normalized corollaries, then decide whether to add a small section/supplement to Finite Jet. This stays in this chat because the version audit and proof decisions are useful. A focused independent review with **gpt-6.1-sol, high reasoning** is a proportionate available model choice; exact pricing or app savings were not measured. Actual source edits require an expanded target scope, since this investigation was authorized only to write here.
2. **Before any distinct-paper decision:** obtain the missing signature/correction texts and audit the proposed growing-arity theorem against threshold/rational approximation literature. This can continue here for the review; if a distinct resource-theory project is selected, it becomes a self-contained new research chat with the handoff below. High mathematical uncertainty would justify **gpt-6-astra, high reasoning** for that narrow theorem effort.
3. **Defer neural training and system integration** until a precise added theorem or application contract survives. No further compute, publication, or external action is presently required.

**Thread decision at completion:** finish this initial assessment here. The work is documented and reviewable; creating a fresh chat now would duplicate setup without a selected new theorem.

**Starter prompt only if Brian later chooses the distinct project:**  
“Investigate a sharp growing-arity, conditioning-aware polynomial/rational realization theorem on \(D_{\delta,n}\), with amplitude bounded by one on the whole cube and fixed guarded margin. Read the representational-limits dossier and proof_notes.md at C:/Users/brian/Documents/CM_Computation/output/research/palo_paper_directions_2026-10-13/representational_limits. Fixed-arity sign-only parity/non-affine degree and bounded-margin rates are already derived corollaries, not novelty claims. Audit Sherstov's composition results, Newman/Zolotarev approximation, Bernstein/Jackson bounds, and R-functions before proposing a new theorem. Preserve manuscript versions and unrelated checkout changes; source edits, commits, external writes, and paid compute are not authorized by this handoff.”
