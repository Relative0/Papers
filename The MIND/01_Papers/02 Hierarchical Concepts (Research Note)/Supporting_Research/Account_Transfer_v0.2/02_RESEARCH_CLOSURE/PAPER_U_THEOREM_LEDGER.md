# Paper U: theorem, definition, and substantive-claim ledger

**Inputs:** complete v0.1 LaTeX manuscript, supplied audit/model/example files, and relevant historical thesis passages. Source locations below use v0.1 labels or section headings; they are more stable than PDF page numbers. **Status language:** correct means correct under the stated contract, not novel. Source IDs Mxx/Cxx refer to the priority map. Proof reconstructions appear in v0.2 or the strengthening study.

## A. v0.1 mathematical core

| ID / claim | Status | Proof reconstructed? | Standard source/mechanism | Needed correction | Publication role |
|---|---|---|---|---|---|
| U01: Sigma_m^N, m>=2, ordered coordinates | Valid model definition | Definition | Full shift/tree boundary | State that ordering is a modeling choice | Retain |
| U02: common-prefix ultrametric, prop:ultrametric | Correct | Yes: prefix inequality | Tree boundary metric, M04/M06 | None; x=y handled separately | Background |
| U03: cylinder equals closed lambda^k ball, prop:ball | Correct | Yes: first differing digit | Prefix metric | Preserve closed/open distinction | Retain compactly |
| U04: length-k cylinder equals open lambda^(k-1) ball for k>=1 | Correct | Yes | Discrete distance scale | Do not use open lambda^k for same cylinder | Retain |
| U05: positive-radius balls clopen | Correct | Yes: smaller balls stay inside/outside | Ultrametric topology | A closed radius-zero singleton need not be open | Background |
| U06: balls laminar, prop:laminar | Correct | Yes: recenter intersecting balls | M04; strong triangle inequality | Intersecting unequal-radius balls need not be equal | Background |
| U07: balls ordered by reverse prefix specificity | Correct | Yes | Prefix tree | General feature order not canonical | Background |
| U08: primitive balls form Boolean algebra | Not actually asserted generally; avoid inference | Counterexample: union of two small cells may not be a ball | Set algebra | Separate balls from unions of cells | Retain distinction |
| U09: fixed-depth B_k is Boolean algebra | Correct | Yes: preimage of power set | Finite partition algebra | None | Retain |
| U10: observation pi_k and prefix equivalence, prop:fibers | Correct | Yes, definitional | C05 already uses fixed-prefix classes | No cognitive-priority claim | Core synthesis |
| U11: tau_k all unions of fibers | Correct | Yes | M01 Definition 1 | Call it partition/initial topology | Core synthesis |
| U12: fibers internally indiscrete, thm:coarsetop | Correct | Yes: intersect a union of cells with a cell | M01/M02 | This is not latent metric indiscreteness | Core correction |
| U13: tau_k non-T0 on unresolved states | Correct | Yes | M02 Lemma 3.5 | Singleton-cell finite models are exceptions to blanket non-T0 wording | Retain precisely |
| U14: tau_k increasing | Correct | Yes: each coarse cell is finite union of finer cells | Refinement | None | Background |
| U15: all resolutions recover latent topology | Correct for full prefix model | Yes: cylinders form a basis | M05 / product topology | Generated topology, not plain union equality | Retain and generalize |
| U16: truncated d^(k), definition and thm:pseudo | Correct | Yes: finite quotient pullback | M02/M03 | Name ultrapseudometric; d^0 identically zero | Core synthesis |
| U17: topology of d^(k) equals tau_k | Correct | Yes: finite positive quotient distances | M02 Theorem 5.3 | Finiteness important for discreteness argument | Retain |
| U18: zero-distance quotient genuine finite metric | Correct | Yes | M02 Theorem 5.3 | Distinguish metric identification from an unspecified quotient metric | Retain |
| U19: six-part resolution-equivalence, thm:equiv | Correct on defined full regular tree | Yes; orbit implication separately reconstructed | Set quotient + M06 | Several clauses are definitional, not six independent discoveries | Compress/unify |
| U20: every allowed observable agrees iff same prefix | Correct | Yes: pi_k or cell indicator separates cells | Set quotient universal property | "Every observable" means allowed, cell-constant observables | Retain |
| U21: G_k orbit equals boundary fiber | Correct with full Aut(T_m) | Yes: infinite ray portrait construction | M06 | False for arbitrary subgroup or nonregular hierarchy | Retain with counterexample |
| U22: distance/distinguishing depth, cor:distres | Correct | Yes: kappa=lcp+1 | Prefix scale calibration | General thresholds give inequalities, not this exact equality | Retain corrected generalization |
| U23: full prefix inverse limit, thm:inverse | Correct | Yes: compatible digit reconstruction | M05 | Totally bounded generalization recovers completion if incomplete | Retain |
| U24: p-adic digit map isometry, prop:padic | Correct | Yes: first differing digit valuation | Standard p-adic expansion | Least-significant digit first; m=p and lambda=1/p | Brief specialization |
| U25: pi_k is reduction modulo p^k | Correct | Yes: sum first k digits | Residue rings | None | Brief specialization |
| U26: Z_p versus Q_p remarks | Correct distinction | Algebraic check | Standard p-adic arithmetic | Z_p is not a field; arbitrary m-tree needs no field | Retain |
| U27: G_(k+1) proper subgroup of G_k, prop:symbreak | Correct | Yes: nonidentity child permutation at level k | M06 | Requires m>=2/full available permutations | Quantify via quotient |
| U28: XOR quotient under swap/complement, prop:xor | Correct | Yes; four-case enumeration | Elementary Klein-four action | Action is not free; complement alone already suffices | Remove from main |
| U29: anchored XOR bijective/self-inverse, prop:xoranchor | Correct | Yes: two applications cancel XOR | Reversible binary linear map | No relation to ultrametric geometry follows | Supplement only |
| U30: F_k=sigma(pi_k)=B_k | Correct for finite partition | Yes | Finite sigma-algebra | Do not confuse union of all B_k with full Borel sigma-algebra | Background |
| U31: uniform H(pi_k)=k log2 m | Correct | Yes: m^k equal outcomes | Shannon entropy | Uniform law is an extra assumption | One brief comparison |
| U32: conditional child self-information -log p | Correct on positive-probability events | Yes | Chain rule | Zero-probability realized-event language needs qualification | Supplement |
| U33: conditional expectation is coarse representation | Correct | Yes: cell averages, defined almost everywhere | M09 | Null-cell values arbitrary | Supplement |
| U34: L2 orthogonal projection | Correct for f in L2 | Yes: orthogonality to cell indicators | Hilbert-space conditional expectation | Do not claim for all L1 functions as L2 projection | Supplement |
| U35: M_k=E[f|F_k] martingale | Correct for f in L1 | Yes: tower property | M09 | It is a uniformly integrable/closed martingale | Supplement |
| U36: convergence statement | Correct direction but under-specified | Yes, exact M09 Theorem 4.6.8 contract | Levy upward theorem | State a.s. and L1 to E[f|F_infty]; to f only if measurable there; Lp requires f in Lp, p<infinity | Remove vague main-text aside |
| U37: finite complete prefix-free frontier | Correct | Definition checked | M07 | Prefix-free alone is not enough; require completeness | Retain |
| U38: repeat all constructions adaptively | Partly justified, too compressed | Yes: v0.2 Theorems 1.1, 2.2 | Ball quotient plus M06 | General refinement need not yield normal subgroup/quotient group | Strengthen |
| U39: four-attribute binary example | Correct as finite illustrative model | Recomputed depth-four hierarchy | Supplied script plus new independent code | Finite terminal leaves differ from infinite latent fibers | Evidence, not long main section |
| U40: cognitive appropriateness of adaptive attention | Modeling suggestion, not theorem | No empirical proof | No source supplies validation of this model | Label hypothesis, not conclusion | Limit |

## B. Interpretive, provenance, and presentation claims

| ID / claim | Status | Proof reconstructed? | Standard source? | Needed correction | Publication role |
|---|---|---|---|---|---|
| U41: all ultrametrics make points indistinguishable | False historical thesis inference; v0.1 already rejects it | Counterexample: any nontrivial metric is Hausdorff | Elementary separation | Do not portray as an uncorrected v0.1 theorem | Correction motivation |
| U42: all intersecting ultrametric balls equal | False historical overstatement | Nested cylinder counterexample | Strong triangle inequality | Equal-radius qualification; arbitrary balls only laminar | Historical ledger only |
| U43: symmetry alone gives equivalence relation | False general inference | Symmetric relation need not be transitive | Elementary logic | Define equivalence from observations, not adjective "symmetric" | Interpretation limit |
| U44: conflicting cylinders intersect in common attributes | False as literal intersection | Incompatible cylinders disjoint | Set intersection | Common ancestor is a containing ball, not intersection | Historical ledger only |
| U45: p-adic distance from difference of individual norms | False general recipe | x=1,y=1+p: equal norms, positive distance | |x-y|_p, not ||x|_p-|y|_p| | Preserve correct distance | Historical ledger only |
| U46: Matte Blanco advocates only equivalence not literal identity | Misleading v0.1 abstract attribution | Primary pp.38-39 inspected | Primary text, not secondary gloss | State deliberate restriction of our model | Important repair |
| U47: observation equivalence formalizes full bi-logic | Not supported | Seven-part source audit | Primary pages and logical distinctions | No relation-converse rule, no absence of negation, no part/whole identity | Explicit limitation |
| U48: combined architecture potentially first | Not defensible on current evidence | C05/C13/C14 overlaps reconstructed | 2007, 2017, 2020 sources | Stronger prior-art acknowledgment | No novelty claim |
| U49: Paper F bridge as mathematical consequence | Not established by these results | Type/structure separation | No need to import companion machinery | Remove substantive bridge; one boundary sentence only | Scope reduction |
| U50: v0.1 source compiles cleanly | Source defect located | Literal double backslash before section at line 95 | Not mathematical | Replace malformed section command, remove working-draft language | Rebuilt and compiled |
| U51: prior audit Lauro-Grotto pages 52-62 | Bibliographically incorrect | Author PDF/publisher record checked | Correct 535-543 | Repair external source map | Audit correction |
| U52: no earlier topological unconscious treatment | Not supported | 2016/2017 sources located | C11/C12 | Full 2017 source still needed before any absence claim | Residual priority gap |

## C. New-to-this-revision statements (not automatically new to mathematics)

| ID / claim | Status | Proof reconstructed? | Standard source/mechanism | Needed correction | Publication role |
|---|---|---|---|---|---|
| R01: inter-ball distances constant | Correct | v0.2 Lemma 2.1 | Strong triangle inequality | Finite clopen partition used in theorem | Coordinate-free core |
| R02: finite-ball quotient universal package | Correct | v0.2 Theorem 2.2 | M01-M03 plus factorization | Different target categories explicitly distinguished | Synthesis |
| R03: greatest dominated collapsing pseudometric | Correct | Pointwise domination argument | Immediate extremal characterization | Not a deep optimization theorem | Useful clarification |
| R04: arbitrary partition can violate triangle | Correct counterexample | Binary depth-two calculation and script | Direct | Balls sufficient, not necessary | Boundary of geometry claim |
| R05: total bounded threshold partitions finite | Correct | Finite small-ball cover | Total boundedness | Noncompact spaces need completion | Coordinate-free extension |
| R06: uniform error <=r_k | Correct | Collapse case split | Direct | Numeric radius arbitrary; no uncalibrated equality | Useful estimate |
| R07: completion equals threshold inverse limit | Correct | v0.2 Proposition 3.1 | M05, M04/M05 completion setting | Compactness required to identify with original X | Important scope boundary |
| R08: adaptive exact index (m!)^N | Correct | Successive index multiplication | M06 section theory | Does not imply normality | Strongest quantitative statement |
| R09: adaptive normality iff per-old-cell full level | Correct under full regular Aut contract | Orbit-invariance proof plus kernel converse | Standard mechanisms; exact priority unresolved | No new-theorem marketing | Strongest sharpened statement |
| R10: normal quotient product finite-tree groups | Correct | Restriction homomorphism kernels | M06 | h_s=0 allowed; do not replace all finite-tree groups by symmetric groups | Retain |
| R11: nonregular orbit failure | Correct | Three-point isometry classification | Direct | No blanket orbit equivalence | Retain |
| R12: frontier lattice and Kraft equality | Correct | Prefix-closed ideals and cylinder measure | M07 / standard codes | Finite frontiers have no global top | Short appendix |
| R13: least sample-separating frontier | Correct | Split every prefix shared by two samples | Uncompressed trie | Fixed feature order; not arbitrary optimal decision trees | Appendix/study |
| R14: adaptive entropy increment formula | Correct | Telescoping one-split chain rule | M08 | Null masses contribute zero | Short caution |
| R15: equal symmetry index, unequal entropy | Correct | Balanced vs comb, 2 versus 7/4 bits | Direct | No index=information slogan | Retain |
| R16: noisy TV pullback need not be ultrametric | Correct counterexample | Bernoulli(0), (1/2), (1) | Elementary probability | Exact row equality still meaningful | Deferred extension |

## 4. Audit scope

All numbered v0.1 mathematical environments and the substantive claims listed above were reconstructed or classified. The entire 2015 thesis was not independently re-proved: relevant ultrametric/topological/interpretive passages were audited as historical input. Other thesis machinery was deliberately excluded. This ledger is a research-closure ledger, not the later publication-readiness scorecard.
