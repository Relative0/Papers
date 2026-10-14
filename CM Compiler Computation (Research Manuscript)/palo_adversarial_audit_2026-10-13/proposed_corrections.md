# Proposed corrections and narrow additions

13 October 2026, Asia/Bangkok. These changes are prepared separately. No original report, manuscript or producer dossier was edited. Apply only to the identified audited bytes, after checking for intervening changes. `source_snapshot.json` gives the exact paths and hashes. The publication-risk findings are not false-theorem errata.

## Synthesis: update the opportunity assessment (N01–N04)

**Target:** `palo_cm_relationships.tex`, Executive assessment, third concluding assessment and later staged-agenda / recommended-interpretation paragraphs; physical PDF pp. 4, 18–21. The existing report explicitly disclaims historical-priority review, so this is a post-audit addition, not a claim that its original source attribution was wrong.

**Insert after the three executive conclusions:**

> A targeted priority review narrows the publication opportunity. Certified continuous-region rule extraction, syntax-independent probability evaluation, algebraic circuit contracts, and typed training/verification compilation have substantial antecedents. The present bridges and small examples justify focused extensions to the existing manuscripts. A separate paper would need an additional theorem, algorithm, or useful application beyond these interfaces; neither CM reshaping nor elementary semantic correspondence establishes that contribution.

**Replace the final sentence “The recommended next research step is Stage 1 followed by a tightly scoped Stage 2 demonstrator.” with:**

> The semantic and extraction dossiers now provide small exact diagnostics and a restricted multi-affine demonstrator. The recommended next step is to consolidate their established boundary statements and selected corollaries into the existing compiler, guarded-dispatch, and finite-jet manuscripts. A separate integration or paper should follow only after a distinct theorem or motivated workload supplies a credible added contribution.

**Reason:** the preliminary agenda is partly completed, while separate-paper novelty remains unestablished. This does not authorize manuscript edits, integration or training.

## Synthesis: make the scalar algebra explicit (clarification)

**Target:** §4.1, physical PDF p. 7, paragraph beginning “One-hot Boolean state vectors…”.

**Replace the last sentence about native addition with:**

> The native coefficient algebra is the Boolean ring: addition is XOR and multiplication is AND. OR–AND contraction gives the same one-hot selection, but it differs on general vectors and matrices. Real expectation is a separately declared arithmetic interpretation and does not inherit the Boolean-ring reconstruction laws.

**Reason:** the existing wording is not false, but “Boolean semiring” must not silently mean both OR–AND and XOR–AND in future integrations. LM §2.2/Remark 2.3 provides the precise distinction.

## Synthesis: threshold endpoint and quantified limits (I04)

**Target:** §7.2, physical PDF pp. 11–12, after the tie-convention paragraph.

**Insert:**

> For an ordinary Boolean-preserving propositional validation contract, take a threshold (0<\tau\le1\). The allowed endpoint \(\tau=0\) maps Boolean false to true and therefore needs a separate interpretation. Crispification inside a batch interpretation also does not make an outer batch mean Boolean; quantified and batch-level validation require their own rules.

**Reason:** the default 1/2 example is correct. This specifies a missing endpoint qualification for any stronger compositional reading, without changing PALO's displayed definition.

## Synthesis: clarify product composition (scope refinement)

**Target:** §5.3, physical PDF p. 10, after the sufficient-independence paragraph.

**Insert:**

> This condition concerns expectations of the declared Boolean events. When the implementation evaluates a recursive soft expression, each child must first be shown to realize that event expectation. Disjoint supports at an outer node do not repair repeated-input discrepancies already present inside a child.

**Reason:** the covariance argument is correct. This guards against a broader future compiler admission rule than the text proves.

## Representational dossier: assertion count (I02)

**Target:** `representational_limits/research_dossier.md`, §6, sentence reporting 23,962; any matching row in its claim matrix or final summary. The audited `verify_candidates.py` and `verification_results.json` instead report 23,964 exact plus 32 floating assertions.

**Replace:**

> It passed **23,964 exact rational assertions** and **32 floating-point assertions**.

**Add if the earlier run is retained:**

> An earlier development update reported 23,962; the frozen script adds two diagnostic assertions. Counts are tied to the recorded script hash and are not proof-coverage measures.

**Impact:** bookkeeping only. The rational construction, asymptotic argument and merge recommendation survive.

## Representational dossier: retain normalization in shortened descriptions

**Target:** any future abstract or manuscript compression of Proposition P1. The present proof notes already include the needed hypotheses; this is mandatory preservation of scope, not a current false statement.

**Use this exact short statement:**

> Fix arity and a Boolean sign law. On the cube with all coordinate magnitudes at least \(\delta\), non-affine sign-only polynomial realization with unrestricted coefficients has degree \(\Theta(\log(1/\delta))\). With amplitude bounded by one on the entire cube and fixed output margin \(0<\gamma<1\), every nonconstant law instead requires degree \(\Theta(1/\delta)\). The constants can depend on the fixed law, arity and margin. These are consequences of existing approximation and threshold-degree results, and impose no coefficient-bit, network-size or training guarantee.

**Impact:** prevents confusing the two resource regimes or marketing the corollaries as new.

## Extraction dossier: compiler source locator (I03)

**Target:** `certified_boolean_extraction/research_dossier.md`, §2 source table, COMP row.

**Replace “negative evidence Section 7 and current navigation” with:**

> Negative evidence in Section 8, PDF pp. 12–15, and current study navigation. Section 7 specifies the frozen empirical protocol.

**Impact:** reference precision only; the negative-result interpretation is correct.

## Extraction replay: enforce the producer's domain (I01)

**Target:** `certified_boolean_extraction/exact_extraction_demo.py`, `replay`, before certificate arithmetic. This patch is suggested, not applied to that source.

The current `extract` rejects nonpositive a/b, while `replay` does not. `independent_results.json` contains an accepted negative-magnitude contract with a=-1/2 and b=1/2. Its algebraic range is correct but its positive-magnitude interface is invalid. No positive-box certificate from the demo was shown false.

**Minimal entry validation, under the prototype's existing rational caller contract:**

```python
if set(expected_bounds) != set(AXES):
    return False
if any(len(expected_bounds[k]) != 2 for k in AXES):
    return False
if any(expected_bounds[k][0] > expected_bounds[k][1] for k in AXES):
    return False
if expected_bounds['a'][0] <= 0 or expected_bounds['b'][0] <= 0:
    return False
```

**A production checker additionally needs** explicit rational types, field/row/witness shape validation and controlled rejection of malformed data. A hash is not a domain validator. These defensive obligations are separate from the multi-affine range theorem; this audit does not propose a production parsing system.

**Replace the dossier §6 replay sentence with:**

> The replay path recomputes all vertex ranges using direct F and verifies frames, domains, witnesses, ranges and labels under the declared rational-box contract. Its current entry point still needs explicit enforcement of the producer's positive-magnitude precondition and input schema before it can be treated as a complete certificate boundary.

**Impact:** modest prototype repair; mathematical and publication recommendations are unchanged.

## Extraction: preserve weighted-star quantifiers (no current theorem correction)

**Target:** a future shortened theorem / abstract derived from dossier §§5.1–5.3.

**Use:**

> The weighted-code formula is exact for tests constant on each operator label, under the stated irreducible determining-boundary hypotheses. At \(2^k\) labels and k binary tests, signature saturation forces label constancy, giving the sharp equal-boundary-degree threshold \(e2^{k-1}\). The unsaturated and non-star unrestricted optima remain open.

**Impact:** prevents transferring saturation to spare-signature cases or to arbitrary neural dictionaries. Add Averkov–Bey as the close factor/coding precedent, while retaining the membership-versus-multi-label distinction.

## Semantic dossier: freeze counts and limit the gradient claim

**Target:** a future synthesis update using the initial handoff's 42,881 count. The completed dossier's 42,918 count is correct and reproduced.

**Use:**

> The final frozen semantic checker passed 42,918 exact assertions over 12,288 two-layer operator compositions. An independent table/grid reproduction found 1,880 rejected same-frame folds, 1,440 rejected one-shared-variable folds and zero rejected disjoint-support folds. These are bounded composition counts, not natural-workload failure rates or general compiler verification.

**For p² -> p, use:**

> On the closed free-input interval [0,1/100], the maximum value error is 99/10000 and maximum ordinary input-derivative error is one. The parameter-gradient discrepancy also contains the actual parameter Jacobian. Value tolerance alone therefore does not certify a gradient tolerance or a training trajectory.

**Reason:** the current dossier already distinguishes these contracts. Preserve that distinction when condensing its results; do not mislabel a provisional count as a false final claim.

## Publication language across all artifacts

Do not insert “first,” “new general extraction,” “new probability semantics,” “neural impossibility” without its whole-orthant hypothesis, “faster,” “compression,” “sample-complexity,” “posterior sampling,” or “quantum applicability” based on the current diagnostics. The dossiers largely already avoid these claims.

**Recommended joint replacement description:**

> The portfolio offers typed Boolean representations and several explicit contracts for interpreting continuous scores. PALO supplies a relevant learning setting. The present results establish small semantic boundaries, conditional realization restrictions and restricted certificates. Their analytical conclusions survive replacement of CMs by equivalently framed truth tables. A distinct publication contribution must therefore come from additional theory, an implemented validation capability, or demonstrated application value.

Applying these suggestions requires a source-edit scope beyond this audit's exclusive output folder. No new paper, training purchase, publication, commit or external message is needed to complete the audit.
