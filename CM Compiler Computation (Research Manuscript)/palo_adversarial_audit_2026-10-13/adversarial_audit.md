# Adversarial audit of PALO and the Correspondence Matrices research

Prepared for Brian, 13 October 2026, Asia/Bangkok. This is a mathematical and comparative audit of identified snapshots, not a peer-review certificate or a portfolio-wide correctness guarantee. Original manuscripts, synthesis and sibling research outputs were preserved.

## Verdict and material findings

**The completed synthesis is substantially accurate within its declared scope. Its decisive elementary bridges and the reconstructed finite-jet and guarded-dispatch arguments withstand this audit. The evidence does not presently justify three separate new papers.** The completed or frozen dossier arguments favor focused additions to the existing Finite Jet, Guarded Dispatch and compiler manuscripts. The earlier ranking of extraction as the best practical direction remains a reasonable application judgment; it is not a novelty or publication-readiness finding.

The most consequential findings concern the proposed publication case rather than a false mathematical identity:

| ID | Severity / category | Finding | Consequence |
|---|---|---|---|
| N01 | Major; novelty unestablished | Certified continuous-to-symbolic rules predate this work. The 1994-conference/1995-proceedings Thrun paper already verifies continuous-region rules; Boolean-table extraction and modern verification add closer baselines. | A broad extraction paper needs a distinct theorem or useful implementation capability. |
| N02 | Major; close prior mechanism | Averkov–Bey treats polynomial degree versus inequality count using boundary factors and binary product codes. Polygon membership differs from multi-label dispatch, but the central mechanism is close. | Add an explicit comparison to GU; a larger star alone is weak standalone novelty. |
| N03 | Major; immediate corollaries / known inputs | Analytic-network whole-orthant impossibility follows from FJ. The fixed-arity logarithmic sign-degree and inverse-width bounded-margin results follow from Sherstov/Newman and Bernstein/Jackson. | Merge or place in a supplement; seek a genuinely additional resource theorem before a separate paper. |
| N04 | Major; established architecture | Syntax-independent probability losses, safe algebraic circuit evaluation and typed training/verification compilation already have substantial primary precedents. | Semantic compilation needs a specific, scalable context-and-gradient validator beyond the present elementary checker. |
| I01 | Minor; missing replay precondition | Extraction `replay` accepts a negative-magnitude contract that `extract` rejects. Exact ranges remain correct for the algebraic formula, but the declared positive-magnitude frame is not validated by replay. | Add the same domain and schema checks at the checker entry point; do not advertise a complete trust boundary yet. |
| I02 | Minor; false factual count | Representational dossier §6 reports 23,962 exact assertions. The frozen script and results produce 23,964, plus 32 floating checks. | Correct the count; no theorem or recommendation changes. |
| I03 | Minor; incorrect locator | Extraction dossier source table describes compiler negative evidence as §7. The selected compiler manuscript puts results in §8; §7 is the study protocol. | Repair the reference to §8, PDF pp. 12–15. |
| I04 | Minor; endpoint clarification | PALO permits threshold zero syntactically. Its crisp operator then sends Boolean false to true, so an ordinary Boolean-validation contract cannot include that endpoint without special treatment. | State `0 < tau <= 1` for Boolean-preserving propositional crispification; the default 1/2 examples are unaffected. |

No critical defect was found in the mathematical bridges checked. That statement does not certify all source theorems, all cited literature, current LIME software, training behavior or later artifact revisions. N01–N04 are publication-risk assessments, not allegations that the carefully qualified dossiers claim historical firstness. The dossiers themselves largely reach the same narrowed recommendation. Proposed exact replacements and repairs are in `proposed_corrections.md`; the row-level provenance is in `claim_audit.csv`.

## Versions and provenance

The synthesis reviewed is the 23-page PDF and its 62,018-byte LaTeX source. Source SHA-256: `772da774eaad0b7f6b934bd056784c54caa1b7031de2e03cf8b02cd4b14f6c39`. Initial available artifacts were frozen at 2026-10-13 15:32:45 UTC (22:32:45 Bangkok). Dossiers initially unavailable were recorded as unavailable, then separately captured as they appeared. `source_snapshot.json` preserves observation times, hashes, file paths, immutable dossier snapshots, navigation and completion observations. A hash identifies reviewed bytes; it does not prove authoritative status or mathematical validity. The ledger's `original_claim` column uses condensed claim formulations; immutable snapshots preserve the full original wording.

All seven original PDF hashes matched the synthesis inventory on initial capture and the first recheck. A subsequent final read detected a newer compiler PDF at the same path: **20 pages, with a semantic-boundary addition dated 13 October 2026**, SHA-256 `e47705280dd8e20038d6fd3e5fe779c8a9d6995e6f39cc59760e9302a608ca17`. The other six still matched. The compiler audit below concerns the **19-page September 26 version**, SHA-256 `453e845acd202035fa8ffcc1266f09c1e69ebf831dc08297583d5f26a81c6fa2`. The exact old PDF was recovered from the compiler-addition baseline backup, verified by that hash and preserved in `audited_source_pdfs`. The extracted old text, later text and their diff are retained; do not apply old page references to the new pagination. The new §4.4 was inspected as a post-cutoff passage and agrees with the audited semantic-boundary account, including the 3/8-versus-1/2 worked fusion and separately-affine criterion. Other changes in the new package have not received a complete review here.

| Key | Reviewed source | Version and pages | Authority / audit role |
|---|---|---|---|
| PALO | Stehr, Kim, Talcott, *A Probabilistic Approximate Logic for Neuro-Symbolic Learning and Reasoning* | Supplied 57-page author manuscript, December 2020; 2021 publication notice | Supplied source for all semantic locators. Author publication list confirms JLAMP 124, 100719 (2022), DOI 10.1016/j.jlamp.2021.100719. |
| LM | *Correspondence and Logical Matrices: A Typed Boolean Operator Calculus* | Final September 27 revision, 32 pp. | September 30 collection guide selects this bundle. |
| COMP | *Operator-Level Boolean Computation with Correspondence Matrices* | September 26 contract revision, 19 pp. | Current compiler collection selects this manuscript; later study outputs are evidence extensions, not automatically new manuscript versions. |
| GU | *Guarded Boolean Operators: Exact Dispatch and a Polynomial Guard-Degree Tradeoff* | September 28 reviewed package, 14 pp. | Collection guide supersedes the older September 24 summary. |
| FJ | *Finite-Jet Sign Rigidity on Hyperplane Arrangements and Denjoy–Carleman Realization* | September 27 final submission candidate, 14 pp. | Final package / collection guide selects this source. |
| CTX | *Contextuality and Exact Information Resources over Finite Chain Rings* | September 26 revision, 12 pp. | Collection guide selects revised head. |
| PROC | *Process Closure and Restricted Conversion in a Chain-Ring Modal Model* | September 20 companion in September 21 package, 9 pp. | Collection guide selects the companion source, distinct from the verification supplement and historical stub. |

The six collection guides and their older `README_FIRST.md` records were read directly and copied into `navigation`. No superseding authoritative manuscript was identified at the initial navigation check; the later compiler addition is explicitly versioned in its cover/header and is recorded separately above. Modification times and older readiness summaries were not used to overrule explicit source selection. This is not a census of every historical ZIP or a promise that the versions will remain current.

PALO journal metadata and supplied-author semantics were kept separate. Publisher/DOI full-text access failed; no complete author-versus-version-of-record text diff was possible. The accessible publication metadata do not establish that every equation in the final journal PDF is byte-for-byte the same. The 2019 five-author technical report is a related earlier work, not silently substituted for the three-author supplied article. All PALO page references below concern the supplied PDF. Its p. 26 threshold equation and FJ p. 6 were visually inspected; extraction warnings and defective glyphs were treated as transcription issues, not mathematical evidence.

## Coverage and independence of the checks

Here “reconstructed” means an informal independent argument checked against the source, not machine-checked proof. “Faithful” means the synthesis reflects the specified source; it is weaker than independent theorem verification.

| Surface | Locators | Coverage | Limits |
|---|---|---|---|
| PALO primitives, dependence, quantifiers, crispification, prototype sampling | §§3.2–3.8, PDF pp. 16–27; §4 pp. 28–29 | Equations/prose compared, decisive examples independently checked | No full Bayesian framework proof, implementation audit or learning replication |
| LM Boolean arithmetic, one-hot selection, frame normal form and pairing | §§2–5, PDF pp. 4–12; Thms 3.1, 3.2, 4.1, 4.4, 4.5, 5.1, 5.4 | Algebra reconstructed; all 256 binary normal-form/pairing valuations checked | No full higher-arity, spectral or group-classification audit |
| Real contraction, joint-law formula and rewrite failures | Synthesis §§4–5, PDF pp. 7–10 | Independent derivation, exact checks; full bounded two-layer fold census | Not arbitrary PALO expressions or full quantification |
| GU geometry, degree/test and coordinate-query minima | GU Thm 2.2 pp. 3–4; Lemma 3.1/Thm 3.2 pp. 5–6; Prop. 5.1 pp. 9–10 | Proofs reconstructed; rational dispatcher checks | Coordinate-specific fixed binary language; no runtime/learning theorem |
| GU certification, representation and trajectories | Props 4.1–4.3 pp. 7–8; Prop. 5.2 p. 10; Appendix A.1 pp. 11–12 | Premises and elementary proofs checked | No general solver or trained trajectory experiment |
| FJ weak-sign, orthant and arrangement proofs | Lemma 3.1 p. 5; Thms 4.1/4.3 p. 6; 4.5/4.7 pp. 7–8 | Leading jet, factor parity and propagation reconstructed | General signature theory cited as prior work, not fully recertified |
| Denjoy–Carleman classification | FJ §2.3 p. 4; Lemma 5.1 and Thms 5.3/6.1 pp. 8–10 | Normalization, elementary closures, selectors and counts checked against Rainer | No full independent proof of classical DC/cutoff theorem |
| Representational extensions | Dossier and proof notes P1–P3 | Arguments checked; cited majority lower bound verified; exact construction rerun | Sherstov's entire lower-bound proof not independently re-proved; optimal growing-arity bounds remain open |
| Extraction weighted star, box range and composition | Dossier §§5–7; demo/replay | Conditional proof reconstructed, replay inspected/rerun, domain-gap reproduced | No unsaturated/non-star optimum, full neural verifier or floating-point kernel |
| Semantic polynomial/gradient contracts | Dossier results A–E and checker | Polynomial criterion, residual ideal, contextual-law argument and chain-rule bounds checked; independent counts | No complete IR integration, custom-backward audit or scalable DAG algorithm |
| Compiler empirical comparisons | COMP §8, PDF pp. 12–15 | Synthesis checked against reported study numbers | Timing workers, raw historical runtimes and source test suite not rerun |
| Chain-ring comparison | CTX §§2–3 pp. 3–7; PROC §§2–4 pp. 2–4 | Contract definitions / key support obstruction checked; small scalar calculations | Full CTX classification, coding, teleportation and PROC normalizer/conversion theorems not independently proved |
| Literature | Primary passages identified below | Targeted proof/definition/priority comparisons | No exhaustive citation census, absence-based novelty guarantee or full specialist review |

No chat or subagent was created and no messages were sent to other chats. Producer status was read through compact bounded `wait_threads` snapshots. Research still in progress was treated as provisional. All three initial research turns completed and their dossier/reference/claim-matrix files were captured. The final status check at **16:08:12 UTC / 23:08:12 Bangkok** showed later extraction and semantic-compilation continuations active. Brian subsequently requested a Guarded Dispatch extension in the extraction chat. Preliminary `guarded_dispatch_extension_2026-10-13/extension_sections.tex` and `region_sections.tex`, plus any resulting revised manuscript, are **outside completed proof coverage**. In particular, a proposed general chamber-constant non-star theorem is not verified by this audit. Review its precise hypotheses, factor-parity proof, examples and replay behavior once its package is frozen; the current weighted-star finding must not be presented as approval of that extension. Likewise, review any new semantic-compilation manuscript or implementation against the event/context/gradient contract before treating it as validated. These are follow-up coverage obligations for later work, not unfinished obligations within the initial-dossier audit. Current observed pending paths/hashes and initial-turn completion times are recorded in `source_snapshot.json`.

## Corrected semantic synthesis

### Arithmetic and frames

The native LM coefficient algebra is the Boolean ring over F2: addition is XOR and multiplication is AND. OR–AND and XOR–AND give the same one-hot selection because only one summand survives. They disagree for arbitrary vectors: `(1,1) dot (1,1)` is zero with XOR reduction and one with OR reduction. Ordinary real contraction is a separate interpretation, not substitution into every LM identity.

For true-first axes `(11,10,01,00)` and `C=[[a,b],[c,d]]`,

`B_C(p,q) = a pq + b p(1-q) + c(1-p)q + d(1-p)(1-q)`.

It is the expected Boolean table under independent Bernoulli base events. The native one-hot corner law and true-first convention are correct. Input swaps and polarity flips commute with real expectation when both table and distribution coordinates are transported. General Boolean identities do not survive: `S(p)=[[p,1-p],[1-p,p]]` has determinant `2p-1`, is singular at 1/2 and is involutory only at the Boolean endpoints. This confirms the report's warning; it does not invalidate the original Boolean frame theorem.

The symbolic normal form `M = S_X C S_Y`, its valuation by frame permutations, and logical pairing were checked under Boolean valuations. Compound references need not be independent for these Boolean identities. An all-true specialization of substituted reference formulas requires joint satisfiability; arbitrary existing valuations remain valid. Matched-intermediate-frame matrix multiplication is an XOR–AND parity contraction, distinct from functional cascade and OR–AND relational composition.

### Dependence and repeated inputs

For marginals `p=P(X=1)`, `q=P(Y=1)` and `r=P(X=1,Y=1)`, joint masses are

`(r, p-r, q-r, 1-p-q+r)`, with `max(0,p+q-1) <= r <= min(p,q)`.

Directly summing coefficient times mass gives exactly

`E_C = d+(b-d)p+(c-d)q+(a-b-c+d)r`,

and `E_C-B_C = (a-b-c+d)(r-pq)`. This is an elementary identity, not a new probability calculus. The coefficient is 1 for AND, -1 for OR, 2 for equivalence and 0 for projections. Fréchet endpoint evaluation gives sharp binary bounds because the expression is affine in r and both endpoints are feasible.

Binary sharpness does not imply global sharpness for shared networks. Three fair bits can each have a feasible pairwise law requiring anticorrelation, but they cannot all be pairwise unequal in one Boolean world. A table with a joint law supplies additional information; the representation does not infer that law. Event identity is distinct from equality of probability parameters.

PALO's recursive rules yield `P and P = p²` and `P and not P = p(1-p)`. At p=1/2 both equal 1/4; the corresponding event probabilities are 1/2 and zero. Primitive equivalence at p=q=1/2 is 1/2, while the conjunction of both material implications is 9/16. PALO explicitly explains these approximations and its substructural laws on pp. 17, 23–25. These are intended semantic choices, not newly discovered PALO bugs.

Independent output events permit product expectation composition. Disjoint sets of independent base events are a sufficient way to establish that fact. Recursive child expressions must themselves have the selected faithful event interpretation before that condition licenses replacing the entire numerical graph. Disjoint child supports at a single outer node do not repair hidden repetitions inside a child.

### Thresholds, quantifiers and objectives

The supplied PALO definition on p. 16 uses maximum for existence, geometric mean for universality and arithmetic mean for the many/mean quantifier on finite batches; §3.3 averages over batch views. These are not universal certificates. One value 0.1 and 99 values one have geometric mean approximately 0.977, without making the weak instance true. The source's bound semantics and abstract/concrete classical modes must remain separate.

PALO §3.7 inserts `crisp_tau` in propositional interpretation equations, with equality assigned true. At p=q=3/5 and tau=1/2, crisp atoms conjoined give one; final threshold of pq=9/25 gives zero. The report gets this distinction right. Strict guarded dispatch abstains at a zero by its own contract; it is not PALO's tie convention. Threshold zero is a degenerate endpoint for Boolean validation; use an interior/default threshold or state the endpoint behavior explicitly. Crisp batch means need not be Boolean, so a propositional substitution theorem is not a quantifier theorem.

The source already uses classical Maude preprocessing, symbolic deduction and numerical compilation. Adding implied axioms can deliberately change the approximate objective. A validator must label such a reformulation rather than pretending it is an invisible objective-preserving optimization. CSE that shares a deterministic value can preserve p²; Boolean idempotence that removes a factor does not. Reverse-mode derivatives must accumulate every consumer.

The prototype on p. 28 describes approximate posterior-mode behavior with repeated SGD synthesis; note 29 explicitly says full posterior-distribution semantics had not been implemented. Empirical operator frequencies from that procedure are not automatically posterior masses. A genuine parameter measure can be pushed forward through measurable operator fibers, with boundary and unresolved mass retained. The averaged table loses cross-entry dependence and is generally not a Boolean CM. No current-software or posterior-calibration claim was verified.

## Representational limits: reconstructed proof and quantitative scope

The crucial FJ argument survives:

1. Nonvanishing on each entire open orthant within a centered ball makes its sign constant by connectedness.
2. A least nonzero derivative order d gives a nonzero homogeneous Taylor polynomial `P_d`; d=0 is allowed. Along each fixed ray, `F(tv)/t^d -> P_d(v)`. Thus the inherited chamber sign is **weak**, including directions where `P_d(v)=0`.
3. Factor a polynomial maximally by each coordinate/hyperplane form. At a generic facet point the residual factor is nonzero. Crossing that facet changes sign by the parity of the factor's multiplicity.
4. The same multiplicity governs every facet of that hyperplane. Connected chamber adjacency leaves one common sign times a product of hyperplane signs.

This yields affine Boolean parity. For C^d the corresponding finite Taylor expansion suffices; for C^k non-affine realization the entire k-jet vanishes. Infinite-order flatness requires smoothness. The theorem does not say every parity realization is nonflat or that every finitely differentiable realization must be parity.

For arbitrary affine arrangements, nonflatness must hold at every wall point. The local incident arrangement determines crossing bits; a generic transverse pair in overlapping neighborhoods equates nearby bits. Connectedness of each affine hyperplane propagates them globally. Merely having a nonzero jet at one chosen corner is insufficient. The finite-N theorem forces a zero N-jet somewhere for a non-parity labeling; that location may depend on N. Letting N grow does not replace the separate smooth argument.

The DC convention is `|D^alpha F| <= C rho^|alpha| |alpha|! M_|alpha|`, with normalized positive nondecreasing log-convex M. Total weight `W_k=k!M_k` gives the series `sum M_k/((k+1)M_(k+1))`. Products use log-convexity; primitives use monotonicity. No unstated general composition or differentiation closure is needed. In the non-quasianalytic case a compactly supported cutoff f translated to start at zero yields `psi(t)=integral_0^t f(s)² ds`: zero for t<=0, positive for every t>0. The selector products activate only the intended chamber. Parity sufficiency uses polynomials. Generic facets distinguish all m parity bits, yielding exactly `2^(m+1)` versus `2^r` laws for the **full classes**, not finite neural networks. Unary/parallel cases can have equal counts.

The qualitative smooth obstruction and leading-term idea have direct [Broglia–Tognoli antecedents](https://www.numdam.org/item/AIF_1989__39_3_611_0.pdf), notably the opening AND example and Theorem 4.2, printed pp. 629–630. FJ already acknowledges this. Multiplication by squared wall equations reconciles its nonvanishing-off-walls hypothesis with that source's exact zero-set hypothesis; affine hyperplanes meet its connectivity requirements. The normalization, cutoff and positive-flat inputs match [Rainer's survey](https://arxiv.org/pdf/2107.01061v2), Thm 3.6 and Cor. 3.12/Remark 3.13, PDF pp. 13–15. Those classical theorems were checked for hypotheses, not independently proved in full.

The new dossier's fixed-arity bounds are correct conditional derivations. On `D_delta,n={x in [-1,1]^n: |x_i|>=delta}`, parity needs degree equal to its support size; a non-affine law needs degree `Theta_h(log(1/delta))` with unrestricted coefficients and no normalized output margin. Every nonconstant law needs `Theta_(h,gamma)(1/delta)` when amplitude is bounded by one on the **whole cube** and fixed `0<gamma<1` is required on the guard. Constants depend on fixed n, h and gamma.

The non-affine lower bound fixes a non-affine two-face, reduces it by sign flips to AND, and substitutes normalized sums of two odd-N groups of Boolean variables, with N comparable to 1/delta. [Sherstov's Theorem 1.10](https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf), PDF p. 6, supplies the logarithmic majority-intersection bound on that finite cube. The dossier does not incorrectly apply a finite-set theorem directly to an infinite interval. Its dyadic positive-denominator rational construction gives the matching upper bound after denominator clearing. Bernstein's derivative bound plus a changing Boolean edge gives the bounded-margin lower bound; Jackson approximation of a clipped ramp gives the upper bound. These are useful consequences, not independent historical novelty.

Finite fitting, whole-orthant realization, bounded guarded approximation and certified extraction remain different problems. Min/ReLU realizes AND exactly with a nonsmooth corner. Classical [R-functions](https://ftp.cs.wisc.edu/pub/users/prem/rfuns.pdf), §§3.3/3.6, already supply off-corner analytic and finite-regularity alternatives. Rounded roots and soft minimum can be analytic and sign-correct outside a shrinking excluded region while failing near the common corner. Smooth flat selectors can realize every law but their existence does not establish an efficient network or learning algorithm.

P2's Hölder Taylor estimate and homogeneous angular-cutoff sharpness argument survive with its operator norm and fixed cutoff constants. P3's associated-function bound survives a fixed derivative budget; coordinate partial norms require dimension factors when converted to operator norms. Optimal cutoff rates for arbitrary weights require stronger hypotheses than bare non-quasianalyticity. Spatial flatness is not a weight-gradient, sample-complexity or training-failure theorem. Scaling a score preserves signs while changing margins and derivative budgets, so normalization is indispensable.

## Guarded extraction, coding, composition and dynamics

For F=x+y+xy and positive a,b, `g11=a+b+ab>0` and the three other scores h1,h2,h3 have pair sums -2ab,-2b,-2a. At most one can be positive; two cannot vanish together. The four zero-free patterns are AND, X, Y and XNOR. Reciprocal coordinates `(u,v)=(1/a,1/b)` turn the regions into convex half-plane intersections, proving connectedness and the three-leaf adjacency star.

The degree/test theorem is correct for fixed binary polynomial indicators `1{H>0}` in original magnitude coordinates, over the full promised zero-free domain. Every discriminant arc must be covered by test zeros; substitution along its rational parametrization forces an irreducible quadratic boundary factor. Degree <=3 cannot contain two such factors, so three tests are needed. Two quartic products suffice; four labels require at least two bits. At two-bit saturation each label has exactly one signature and each bit cuts two leaf boundaries, forcing degree >=4 in **both** tests. This verifies `m1=infinity`, `m2=m3=3`, `md=2` for d>=4. Three truth-coordinate probes remain necessary, even adaptively on the AND input. These are different observation oracles.

Zero rejection changes the alphabet: the binary tests alone can confuse an AND chamber with a boundary point. Exact trichotomy of the two products rejects boundaries. The original theorem counts neither that promise verification nor arithmetic, coordinate/feature construction, coefficient precision or runtime. Introducing ab as a feature or reciprocal coordinates changes the language and its lower bounds. No sample-complexity or neural-training bound follows.

The extraction dossier's weighted-star theorem is sound under its explicit assumptions: mutually exclusive positive leaves, nonempty labels, distinct irreducible boundary forms, and real regular boundary patches that determine polynomial divisibility. For tests constant on each label, a code row must contain every factor whose leaf changes that bit, and product tests attain the weighted row load. With `2^k` labels and k bits, signature saturation forces constancy even without that requirement; equal boundary degree e gives the sharp per-test threshold `e*2^(k-1)`. The disjoint-circle construction satisfies the hypotheses. Spare signatures break the constancy inference; the unsaturated/non-star optimum remains unproved. The proof is a conditional extension of GU and classical coding, not a general network extraction algorithm.

[Averkov–Bey](https://arxiv.org/pdf/1002.0941v1), Prop. 2.1 and §§2–3, is a materially closer antecedent than a generic semialgebraic reference: boundary divisibility and products encode binary cuts under degree constraints. Its problem describes polygon membership; GU decodes several labels on a promised domain. That is a real difference in specification, but it does not make the mechanism novel. The publisher confirms online April 2010 and issue January 2011, [Monatshefte 162, 19–27](https://link.springer.com/article/10.1007/s00605-010-0224-x). Later regenerated PDF dates are not deposit/publication dates. Averkov–Bröcker is a related cardinality precedent, not a proof of the specific fixed-degree multi-label theorem.

The newer extraction continuation identified [Averkov 2009](https://emis.de/ft/11056), *Notes on the Algebra and Geometry of Polynomial Representations*, pp. 271–282. This audit directly checked Lemma 2.1 and Theorem 2.2, PDF pp. 4–5: regular real irreducible boundary portions force factors, and local one-sided descriptions force odd multiplicity. This is a closer curved-boundary precedent for GU's factor mechanism. It strengthens N02 without proving that the exact multi-label or weighted-star statement was previously published. Any new non-star extension must make this comparison explicitly.

The exact demo's six-variable score `D+A*x+B*y+C*x*y` after signed-magnitude substitution is multi-affine in D,A,B,C,a,b. On a compact nonempty independent box, interpolation makes its range extrema vertex values; continuity and connectedness give every intermediate value. This is a universal range certificate based on a theorem, not arbitrary corner sampling. It certifies the two continuous AND boxes and correctly distinguishes ties/mixed/empty/unsupported cases. Its comparison to natural intervals is a precision result. All sixteen coefficient-perturbation certificates use singleton input representatives; they do not certify full orthants.

The replay gap I01 is confined to interface validation. A certificate with a=-1/2, b=1/2 and fixed unit A,B,C can have exact formula ranges and pass `replay`, although `extract` returns UNKNOWN because a must be positive. The polynomial theorem remains valid; the frame claim does not. No delivered positive-box certificate was shown false. Matching positivity, interval-order and schema checks in both entry points repairs the issue. Hashes bind bytes but do not establish admissibility or prove mathematics.

Boolean certificate composition is pointwise substitution on the intersection of certified domains, with the same actual inputs, frames and threshold conventions. Check intersection nonemptiness and reachability before presenting a realized total operator. A continuous cascade additionally needs certified intermediate-range inclusion and a second module constant on the appropriate abstraction cells. Two modules can have the same sign output but magnitudes x and 100x; `z-10` distinguishes them at x=1. CM/LM coherence does not remove that obligation or correlations/shared-input dependence.

Trajectory constancy on components outside zeros is elementary continuity. Polynomial root counts apply to nonzero **composed scores along the path**; polynomial scores with an arbitrary oscillatory path need not give a polynomial time signal. Isolated zeros are finite on a compact interval only with the closedness assumptions used in GU. Tangencies, simultaneous crossings, endpoint zeros and identically-zero scores need separate handling. Equal endpoint tables do not prove persistence. Logged SGD checkpoints do not certify the interpolating path. Margin/Lipschitz persistence needs a uniform bound on the containing region, not a measured gradient at one point. No new dynamics or trained-model stability result was established.

## Semantic compilation and gradient contracts

For the finite pure propositional bilinear-kernel fragment, recursively evaluated scores are polynomials. Multilinear reduction M replaces each positive exponent by one and combines coefficients. It agrees on Boolean corners, so `M(s_E)` is exactly the whole Boolean function's multilinear expectation. Universal full-cube equality to that expectation holds iff the recursive polynomial is separately affine in every distinct base input after cancellation. This elementary criterion is correct; read-once compositions suffice but are not necessary.

A Boolean-equivalent soft residual lies in the ideal generated by `p_i²-p_i`. The checker's telescoping reconstruction is correct. A tensor grid with d_i+1 distinct points in coordinate i decides an explicit polynomial identity of known coordinate degrees, and produces a rational witness if it fails. Expansion, grid size, degree and coefficient bit length can be exponential. The checker is not a generally efficient circuit-identity algorithm or a production compiler.

The independent reproduction evaluates the 12,288 two-layer circuits using direct Boolean tables and an unisolvent rational grid, without importing the dossier's polynomial class. Coordinate degree is at most two, so the three-point tensor grid is decisive for this bounded family:

| Family | Circuits | Preserved soft function | Changed soft function |
|---|---:|---:|---:|
| Same two-variable frame | 4,096 | 2,216 | 1,880 |
| One shared variable | 4,096 | 2,656 | 1,440 |
| Disjoint two-variable supports | 4,096 | 4,096 | 0 |

These counts reproduce the dossier. Constant/projection gates are included, so 1,880/4,096 is not an empirical natural-workload failure rate. The copied final checker produces **42,918**, superseding the handoff's provisional 42,881. Count changes during development were not treated as false final claims.

Fixed-model equality of scalar expectations is not a contextual congruence. Fair independent events X,Y each have probability 1/2, but replacing the second X in X AND X by Y changes the expectation from 1/2 to 1/4. Equality almost surely is sufficient. Equality of the joint law with all declared boundary variables is necessary and sufficient for all finite Boolean boundary contexts; the indicator proof is correct. Choosing all joint distributions including point masses recovers Boolean equality, a different quantifier.

Exact C1 function equality under the same differentiable parameter map preserves mathematical gradients. Equality on a constrained set should be checked after pullback for parameter gradients; it need not preserve all free-input gradients. Forward equality does not settle custom backward, straight-through clamp, nonsmooth tie or stochastic policies. For p² -> p on [0,1/100], maximum value error is 99/10000 and maximum input-derivative error is one (attained at zero); on the open interval the latter is a supremum. Parameter-gradient error includes the parameter Jacobian and can shrink or grow. These observations do not prove any training outcome.

The dossier's downstream value/Jacobian bounds follow from the mean-value theorem and chain rule under its C2 convex-domain and compatible-norm assumptions. A value error plus source margin strictly exceeding that error preserves final threshold decisions. Logs or divisions need a positive denominator bound, and nonsmooth contexts need branch/tie analysis. Shared consumers belong in the output vector/Jacobian; scalar certificates cannot silently ignore them.

[Semantic Loss](https://proceedings.mlr.press/v80/xu18h/xu18h.pdf), Definition 1 / Proposition 2, already supplies syntax-independent independent-base probability loss. AMC's Theorems 2–7 and Table 2 classify evaluation under circuit structure and semiring hypotheses; PALO multiplication/probabilistic OR is not that semiring because distributivity fails. [SPL](https://arxiv.org/pdf/2206.00426) adds correlated conditional distributions and compatible constraint circuits with structural tractability assumptions. These are exact or partial conceptual overlaps, not interchangeable semantics.

[Vehicle](https://drops.dagstuhl.de/storage/00lipics/lipics-vol337-fscd2025/html/LIPIcs.FSCD.2025.2/LIPIcs.FSCD.2025.2.html), §4.2.4, is a close typed multi-backend compilation/soundness precedent. [Semirings for PLP/NeSy](https://arxiv.org/pdf/2402.13782v1) already discusses compilation and gradient semirings. [QLL v2](https://arxiv.org/pdf/2605.13845v2) and its [adequate-loss foundations v3](https://arxiv.org/html/2605.13348v3) are current 2026 preprints addressing law/analytic/verification tradeoffs. QLL Theorem 3.7 uses infinite hardness. Adequate Losses Theorem 6.4 instead gives quantitative adequacy at every hardness under its specified pQLL theory and propositional premises; its finite-temperature result must not be erased by summarizing all this work as a Boolean-limit theorem. Neither result automatically applies to PALO's different semantics. No claimed gap was inferred from the absence of an identical paper title. The dossier's broader Scallop/atlas comparisons are useful leads; full implementation equivalence to those systems was not established here.

## Chain-ring comparisons and empirical boundaries

CTX uses nonzero bipartite resources, balanced tensors, all primitive projective local bases, setting-indexed outcomes and support defined by nonzero contraction. Its local/logical/strong classification is faithfully reported for that contract. “Local” means every supported event extends to a global support assignment; it does not assign probabilities. Strong contextuality excludes a probability distribution over compatible deterministic global sections because there are none. It does not forbid every context-indexed empirical probability model, nor reduce to covariance.

PROC's independent-success obstruction is directly verified in `F2[u]/(u^4)`: u³ and u are each nonzero and their product is zero. Primitive vectors can therefore have locally possible selected outcomes whose joint outcome is impossible; selection need not preserve primitive preparations. The unit predicate is multiplicative and discards nilpotent support. The binary modal completion uses F2 subspaces, spans and F2 tensors; forgetting is an incoherent span, not XOR cancellation of branches. It changes the tensor/process contract. These are not probabilistic semantics or physical quantum predictions.

The comparison with PALO is methodological: declare composition, support and global-consistency contracts. The ring obstruction is not PALO's independence approximation in another notation. The chain-ring papers are optional separate support-model examples, not necessary machinery for extraction or soft compilation. Their main specialist theorems remain outside independent proof coverage here.

The compiler's reported generic-optimizer tie and negative studies are accurately presented. The synthetic median direct/CM producer ratio 0.248 favors direct packed evaluation. The natural secondary ratio is 0.0376 across 70 complete cases, all favoring direct packed, with one retained calibration failure. These results have specified endpoints, admission/fallback and cache regimes. They neither establish universal inferiority nor authorize acceleration claims for a future PALO integration. Historical timing/runtime closure was not reproduced. No learning benchmark, trained extraction study or end-to-end PALO implementation appears among the audit's completed results.

## Literature/priority decisions

The strongest primary comparisons were made at definitions/theorems, not just abstracts:

| Prior work | Classification of overlap | What does not follow |
|---|---|---|
| Broglia–Tognoli 1989, opening example, Prop. 2.4, Thm 4.2 | Direct qualitative / special-case overlap with smooth signature-flatness | No new smooth-flatness priority from neural wording |
| Rainer 2021 author / 2022 journal survey, DC theorem and flat cutoffs | Exact classical inputs and quantitative machinery | Optimal weight-specific cutoff estimates need extra hypotheses |
| Shapiro 2007 R-functions, §§3.3/3.6 | Direct constructive and finite-regularity precedent | Russian original priority and every neural architecture remain unreviewed |
| Sherstov 2009 preprint / 2013 journal, Thm 1.10 and Newman construction | Known lower-bound input and rational-composition mechanism | Derived fixed-arity result is not automatically an original theorem |
| Averkov–Bey 2010/2011, factor and binary coding arguments | Close degree/cardinality mechanism; different membership specification | No automatic proof that the exact GU multi-label statement was previously printed |
| Thrun NIPS 7, §§2–3, pp. 506–509 | Direct certified continuous-region rule precedent | Source algorithm is sound/incomplete; absence of contradiction is not a certificate |
| Xu 2018 / AMC 2017 / SPL 2022 | Exact probability/loss and circuit-contract precedents | They do not preserve every PALO recursive soft objective |
| Vehicle 2025 / semirings 2024 / QLL 2026 | Typed, algebraic, gradient and adequacy precedents | No codebase-level claim that they already implement the proposed exact checker |
| Neural Abstractions NeurIPS 2022, Thm 1 / learner-certifier loop | Conceptual verification architecture, different trajectory target | Not an exact Boolean extraction theorem |
| AAAI 2026 neural-policy predicate abstraction, Thms 7–8 | Reachability/CEGAR precedent with finite bounded-integer states | Finite-state termination does not transfer to arbitrary continuous input |

[Thrun's bibliography](https://web.stanford.edu/~thrun/papers.html) lists IAI-TR-93-5. The downloaded author link is a differently titled 48-page work; its identity was not conflated with the exact 1993 report. The accessible [NIPS full text](https://proceedings.neurips.cc/paper/1994/file/bea5955b308361a1b07bc55042e25e54-Paper.pdf) independently establishes the prior verification idea. This refutes a broad reading of [Wurm's arXiv v1](https://arxiv.org/html/2509.16547v1) assertion that there had been no verification attempts. Wurm's specified complexity results were read for scope, not independently proof-audited. Its IJCNN 2025 publication is recorded in the dossier's Crossref response; the publisher full text was unavailable, so only the arXiv text was audited. Do not infer conference-text identity from metadata.

Searches through the task date and backward references found meaningful antecedents; failure to find a closer exact theorem is not novelty clearance. Unretrieved 1992 signature/flatness and 1993 correction texts, original R-function literature, full publisher comparisons and specialist priority review remain genuine limits. No subscriptions, paid tools or access safeguards were bypassed.

## Reproduction results and evidential weight

All reruns wrote inside this exclusive folder. Scripts were read first; source scripts/data were copied before execution. Results and script hashes are collected in `reproduction_results.json`:

| Run | Result | What it establishes |
|---|---|---|
| Frozen synthesis `verify_bridges.py` | 40,668 exact assertions pass | Its reported bounded calculations and count reproduce |
| Frozen representational checker | 23,964 exact + 32 floating checks pass | Construction samples/corner identities reproduce; dossier count needs correction |
| Frozen extraction demo | 3,587 exact assertions pass | Restricted certificates and diagnostic examples reproduce |
| Frozen semantic checker | 42,918 exact assertions pass | Final bounded polynomial diagnostics reproduce |
| Independent audit checker | 10,193 meaningful assertions; 12,288 separately recorded identity decisions | Independently recovers fold counts, joint-law identities and guard decoding; reproduces replay gap |
| Additional algebra/domain checker | 797 assertions pass | Boolean LM valuations, real switch domain, ring scalar obstruction and concrete counterexamples |

Counts are not additive proof coverage. Many checks share an identity, grid endpoints repeat feasible laws, and copied reruns are not an independent derivation. The independent fold grid is exhaustive for its declared bounded-degree family because of interpolation, not simply because it is large. Finite grids do not prove FJ, arbitrary guard lower bounds, solver completeness, historical novelty, sample complexity or training performance. Floating illustrations are separated from exact arithmetic. Runtime here is diagnostic overhead, not a comparative benchmark.

The project implementation was not edited, so unrelated repository tests were not run. Git status/diff statistics were recorded before and after; existing tracked changes remained, and concurrent work is not attributed to this audit. All writes attributable to this task are under the exclusive audit folder. No commits, pushes, publication, other-chat messages, credential access or paid compute occurred.

## Per-direction recommendation and corrected joint account

**Representational limits:** merge a concise R-function comparison and normalized resource discussion into FJ, subject to Brian authorizing source edits. P1–P3 are mathematically useful supporting consequences. A separate paper needs a matched growing-arity/conditioning theorem that survives comparison to existing approximation and composition results. Defer architecture/training claims until the score family, domain and resource normalization are fixed.

**Certified extraction:** merge the weighted/saturated-star extension and small replayable multi-affine example into GU or its supplement. Repair replay entry validation and distinguish finite representative certificates from continuous cells. A stronger unsaturated/non-star theorem or useful, cost-measured application could justify a separate methods paper; neither is completed. Generic extraction, certificate reuse and transition graphs already have strong antecedents.

**Semantic compilation:** add the objective-preservation boundary and a small exact diagnostic to COMP. The strongest surviving practical capability is explicit rejection of invalid soft rewrites, including the original compiler's Boolean worked fusion. A separate context-aware translation-validation paper remains plausible only after sound shared-context/parameter/backward-policy integration and task-matched measurements. No notation-specific speed or information advantage is established.

The reliable combined thesis is: **a learned numerical model can support a justified Boolean interpretation only relative to a declared abstraction, reachable domain, arithmetic and threshold policy; constructing, certifying, composing and maintaining that interpretation consume additional resources.** This is a substantive specification question and an established formal-methods theme. PALO supplies a motivated learning setting; GU/FJ/LM/COMP supply particular contracts and examples. Their connection is useful without being a new universal logic or a demonstrated learning system. CM/LM contributes typed symbolic organization; ordinary framed tables preserve the analytical and extraction results, so novelty must come from additional theorems, algorithms or measured utility.

The requested audit is complete at the frozen versions and coverage recorded here. Optional next step: apply the specific errata and narrow manuscript additions after source-edit scope is authorized, in this chat because the evidence and version decisions are reusable; gpt-6.1-sol with medium reasoning is a proportionate available choice for that bounded editing pass. Defer separate-paper development and integration until a concrete new theorem or useful workload is selected. No further thread or model run is required merely to deliver this audit; no price or cache-saving measurement is claimed.
