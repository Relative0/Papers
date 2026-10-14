# Adversarial audit of the compiler semantic-boundary addition

Date: 13 October 2026. Scope: the current compiler manuscript, with detailed mathematical and source checking of Section 4.4 and consistency checks of its Boolean theorems, discussion and artifact claims. Brian authorized an adversarial audit and manuscript updates for legitimate findings. This is a second-pass audit in the same chat, not an independent external referee report.

## Disposition

One substantive mathematical wording error was confirmed and corrected. Three related specification gaps were clarified. The real-contraction formula, Boolean fusion theorem, displayed soft counterexample and full-cube multilinearity criterion survive the audit. No new performance, training, implementation or novelty claim is warranted. The separate-paper direction remains deferred.

## Accepted findings and revisions

| ID | Finding and evidence | Disposition |
|---|---|---|
| A01 | The old sentence said gradient preservation "requires" function equality. This is too strong: `t` and `t + 1/4` have identical derivatives. It also failed to specify the domain needed to infer derivatives from equality: `p` and `pq` agree on `q=1`, but their ambient gradients there are `(1,0)` and `(1,p)`. | Corrected. Equality of the pullback functions on an open parameter domain is stated as sufficient for equality of their mathematical parameter gradients. A common parameterization is an explicit comparison contract, not a purported logically necessary condition for every coincidental equality. Pointwise and lower-dimensional equality, custom backward rules and floating-point evaluation are distinguished. |
| A02 | "Whole-table extension" and "base variables" were implicit in a manuscript centered on binary tokens. The full-cube iff criterion concerns free event coordinates; applying the degree test after tying parameters would reject an exact product-model probability `t^2`. Distinct events with equal marginals must not be identified. | Clarified. Define `B_e` as the unique multilinear interpolant of the Boolean truth table over distinct event identities. State the product model and separate correlated model sum. Explicitly separate parameter identity from event identity, and restrict necessity of the criterion to the full cube. This does not repair a false criterion; it makes its assumptions operational. |
| A03 | The old text distinguished event equivalence from equal marginals but did not define the contextual replacement guarantee; its crispification claim lacked a numerical example or threshold/tie placement. | Clarified. State almost-sure event equality under the same joint model, and give the recursive-crisp versus final-threshold conjunction at `p=q=3/5`, threshold `1/2`, tie rule `>=`. PALO's author manuscript p. 26, Section 3.7, supports the placement and tie rule. |
| A04 | The later discussion called frame metadata a certificate of "legality" without restating the Boolean scope. The preceding invariant supplied that scope, but the new numerical section made an unqualified reading avoidable. | Clarified. For valid child tokens, matching metadata certifies same-frame **Boolean** fusion; the numerical contracts require additional checks. No Boolean rule or compiler implementation changed. |

The source attribution was also tightened: PALO's listed operations belong to its approximate propositional semantics; this audit does not analyze quantified/batched learning semantics. Weighted model counting supplies the model sum; semantic loss applies a negative logarithm to the satisfying-assignment probability. The manuscript retains its existing three primary citations.

## Challenges that did not justify changes

- **The real-contraction coefficients are reversed:** rejected. True-first row/column order gives `a*p*q + b*p*(1-q) + c*(1-p)*q + d*(1-p)*(1-q)`, hence the displayed expansion. All 16 tables were checked at corners and rational interior points.
- **The worked Boolean fusion is invalid:** rejected. Its children are `not(X and Y)` and `X or Y`. Their XOR is true exactly on equal Boolean inputs. At the soft midpoint both children instead equal `3/4`; the declared XOR kernel gives `3/8`, while primitive equivalence gives `1/2`. These exact numbers are now directly asserted, rather than merely covered by a different rational witness.
- **Multilinearity is insufficient or unnecessary on the full cube:** rejected. Each primitive kernel agrees with its Boolean table at corners, so the recursive polynomial and `B_e` have equal corner values. Uniqueness of multilinear interpolation proves sufficiency; polynomial identity on a cube with nonempty interior proves necessity. The zero/constant case is included. Restrictions or parameter ties change the domain and are now explicitly excluded from the iff's necessity direction.
- **Disjoint support must be necessary:** rejected. It is only a sufficient syntactic condition; coefficient cancellation or ignored operands can preserve multilinearity even with repeated syntax. The necessary-and-sufficient condition is stated on the final polynomial after cancellation. Expansion is potentially exponential.
- **Equal probabilities suffice for contextual replacement:** rejected by the already valid fair-event example. Additional exact cases show that marginal pair `(1/2,1/2)` permits conjunction probabilities `0`, `1/4` or `1/2`, depending on the joint model. Almost-sure equality under the same model does suffice for Boolean contexts, even when syntactic event names differ.
- **The addition establishes a CM-specific differentiable compiler or a new calculus:** rejected. Its algebra is standard, ordinary framed tables support the same checks, and the manuscript expressly limits implementation and novelty claims. Existing negative empirical findings are retained.

## Source verification

The audit reread the cached, fingerprinted primary texts already used for the addition. No new publication-status or current-software assertion was introduced.

- PALO: supplied 57-page author manuscript, DOI `10.1016/j.jlamp.2021.100719`; pp. 16-17 (Section 3.2) give the approximate kernels and failure of classical laws; pp. 23-25 (Sections 3.5-3.6) discuss dependence, bounds and classical abstraction; p. 26 (Section 3.7) places crispification in each propositional interpretation. The cached page-26 render confirms `>=`, which text extraction loses. Its PDF SHA-256 remains `8afb448071a9e79091bfe5d692e24c84a518969d57f9f9eed8cf2b2d3fb0abd7`.
- Kimmig, Van den Broeck and De Raedt: 22-page author version of *Algebraic Model Counting*, pp. 3-4, Definitions 1-3 and the probability instance. Literal-product WMC with complementary probabilities is the independent-base-event model; richer joint models require their supplied model/factor representation.
- Xu et al.: PMLR 80, pp. 5502-5511; PDF pp. 2-3, Definition 1 and Proposition 2. Semantic loss is proportional to negative log of a product-model satisfying-assignment sum and is syntax invariant under logical equivalence. This audit does not repeat the paper's unrestricted differentiability wording at probability-zero boundaries.

The existing source inventory files retain exact source paths/URLs and hashes. The pre-audit manuscript and revision manifest are preserved under `baseline/`; the earlier pre-addition baseline remains intact in the preceding supplement.

## Verification and limits

- `exact_audit_checks.py`: 1,023 passing exact assertions. Includes a separate weighted-outcome scalar evaluator, the actual displayed fusion values, event/parameter distinctions, restricted-domain and gradient counterexamples, recursive crispification, correlated models and almost-sure contextual substitution examples. Sparse polynomial operations reuse the preceding checker; this is not claimed to be a fully independent implementation or machine-checked general proof.
- `replay_original_checker.py`: reproduces all 42,918 assertions and all substantive output fields of the preceding checker, excluding elapsed time, over 12,288 bounded compositions. Writes a new replay record without changing the prior evidence.
- Manuscript validation: reference/label resolution, scoped diff, canonical and archived hashes, revision and changed enclosing-manifest entries, PDF build and rendered-page inspection are recorded after installation in `compiler_audit_20261013/verification.json` in the workspace research package. The manuscript supplement retains the audit, exact results, replay and before/after patch.
- The built-in LaTeX compiler fails before source processing with `Unable to find standard directories for platform`. The existing MiKTeX fallback builds with automatic package installation disabled; its log is preserved. This environment failure is not a source error.
- The pinned compiler implementation and frozen empirical data were not edited. Their 123-test suite and timing campaigns were not rerun: this pass changes explanatory text and supplies semantic diagnostics, not implementation behavior or empirical estimates. The audit reviewed those manuscript claims for consistency but does not constitute a new independent replication of them.

## Recommendation

Complete the bounded corrections and stop. A further semantic-compilation paper or backend should wait for a realistic workload and a distinct, measured capability beyond established framed-table/circuit methods. No further thread or model run is needed for this audit. Existing submission gates in the compiler manuscript remain separate work requiring their own scope.
