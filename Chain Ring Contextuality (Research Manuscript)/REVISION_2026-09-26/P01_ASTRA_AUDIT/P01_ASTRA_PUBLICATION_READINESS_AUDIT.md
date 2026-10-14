# P01 Astra Publication-Readiness Audit

## Contextuality and Exact Information Resources over Finite Chain Rings

**Audit date:** 26 September 2026.  
**Audited manuscript:** Brian Theory, research draft dated 19 September 2026.  
**Review mode:** independent read-only analysis, fresh bounded computations, primary-source comparisons, and simulated referee perspectives. This is one assistant's audit, not certification by six independent human referees or a proof assistant.

## 0. Archive inventory and source of record

The uploaded ZIP contains **34 files in 7 directory entries**, with no nested ZIP archive. It contains one designated manuscript source and one rendered manuscript, not several competing manuscript versions. The historical directory contains provenance records rather than another mathematical draft.

| Layer | Contents and treatment |
|---|---|
| Current manuscript | `01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/main.tex`, `main.pdf`, `references.bib`, and `smith_table.tex`. These define the actual object reviewed. The PDF has 11 pages and the source has 310 lines. |
| Current navigation/provenance | Root `README_FIRST.md`, `CLAIMS_AND_UNIQUENESS.md`, and `SOURCE_MANIFEST_SHA256.csv`. Used to identify the head and intended boundaries, not to certify the mathematics. |
| Earlier proof/priority reviews | `ADVERSARIAL_REVIEW.md`, `GATE_2_PRIORITY_PROOF_REPORT.md`, `CHANGED_CLAIMS.md`, `FINAL_CLAIMS.md`, the source/claim crosswalk, primary-source ledger, priority ledger, search log, and unresolved-issues register. Treated as assertions and search leads. |
| Supplied computational/build records | `generate_assets.py`, `ANALYZER_CHECK.json`, reproducibility notes, `BUILD_MANIFEST.json`, four build-stage logs, and `VISUAL_QA.json`. Code and actual certificates were inspected; status labels were not accepted as proof. |
| History | `HISTORY/PARTITION_BASELINE_20260925/` preserves an earlier context note and source manifest. Its relative paths describe a larger portfolio. |
| Later viability assessment | `RESEARCH_VIABILITY_REVIEW_2026-09-26/` contains an assessment, decision JSON, and two-file manifest. It is a later review, not a later manuscript. |
| Missing external dependencies | The archive points to a sibling program reproduction supplement, canonical run outputs, and other portfolio material that are **not inside this ZIP**. These were not presumed to exist locally or to be correct. |

All supplied files were accessible in the container. The ZIP itself was not text-indexed by the retrieval service, so archive inspection, extraction, source reading and PDF rendering were performed directly. Relevant text, code, ledgers and records were inspected recursively. External references and omitted sibling archives were not mistaken for supplied files.

The current source SHA-256 is:

`31f623fc8572d0d7cb2141d7971196176979dbd56ff40bd6a4d5ca318c3ac46f`

The supplied PDF SHA-256 is:

`f85a140ce21a2ff1e74b6b9f965d473f1430fee2c2464f867386f8f82720ba08`

All 30 entries in the current root manifest match their recorded sizes and hashes. Both entries in the later viability-review manifest also match. At the end of the audit, **all 34 extracted files still matched the original ZIP bytes**. Builds and experiments were performed in separate working directories. No `main.tex` edit was made.

## 1. Executive determination

**The mathematical core is substantially stronger than the publication package.** I found no counterexample to a principal theorem and no central proof gap after reconstructing the arguments. The all-lifts hyperplane argument, Smith trichotomy, exact `d*h` codebook, complete analyzer construction and raw-teleportation criterion withstand the checks described below.

The paper nevertheless should **not be submitted in its present packaged form**. Its main weaknesses are a non-self-contained reproduction package and an unfinished theorem-level contribution comparison. There is also a localized symbolic-ring proof clarification and a peripheral unsupported reference to a restricted construction. These are bounded repairs, not evidence that the research program needs to be restarted.

| Determination | Verdict |
|---|---|
| Principal mathematical results | Sound under the stated contracts, on this audit; not formally certified |
| External novelty | Moderate confidence for the complete chain-ring classification and matched-contract resource comparison; historical priority unresolved |
| Public preprint | **READY AFTER SPECIFIC MAJOR CORRECTIONS** |
| Journal submission | **MAJOR REVISION BEFORE SUBMISSION** |
| P0 publication blockers | **0 identified** |
| P1 major issues | **2** |
| P2 localized issues/recommendations | **7** |
| Need for further mathematical expansion | **Not established**; repair and positioning are the immediate work |

These judgments concern the current article and supplied evidence. They are not an acceptance prediction. Scores below are not probabilities, and were not averaged into the verdict.

## 2. Independence, coverage and limitations

The source was read against its PDF, not inferred from the abstract or earlier reviews. The main arguments were reconstructed by checking their quantifiers, ring assumptions, matrix types, zero/nonzero implications, and the distinction between a nonzero element and one with nonzero residue. Fresh calculations use a new standard-library Python implementation, without importing the author's code.

Three evidence levels are kept separate throughout:

1. A general argument in the manuscript, reconstructed and scrutinized here.
2. A finite calculation made directly from support definitions or exact matrix identities.
3. A historical assertion or generated classification table whose original runner is not supplied.

There is no exhaustive computation over all finite chain rings or all dimensions. There is no proof-assistant verification. Literature searching is bounded: an exact antecedent can remain undiscovered. The source comparisons below identify what was actually inspected and do not claim a complete reading of every external book, thesis or reference cited by those sources.

## 3. What the manuscript actually contributes

Let `r` be the number of nonzero Smith factors, `a` the least Smith exponent, and `h` its multiplicity. For a nonzero resource `M`, write `M = pi^a N`, using a preimage rather than an inverse of `pi^a`. Then `h = rank_k(N mod J)`.

The central structure is:

- **Support classification:** `r=1` is local; `r>=2, h=1` is logical but not strong; `h>=2` is strong, for the complete family of primitive projective local bases.
- **Exact orbit coding:** the maximum number of messages is `d*h` for a square resource and the particular full-GL encoding / invertible joint-readout contract.
- **Exact raw teleportation:** over a finite commutative local ring, a square resource works universally precisely when it is invertible, with complete analysis and unrestricted invertible branch corrections.

The hyperplane lemma and Hardy construction establish the support theorem. The invertible-matrix basis is an enabling algebraic fact. The coding/contextuality equivalence and nonprimitive separator are consequences that make the comparison conceptually useful, not additional unrelated classification projects.

The manuscript also includes a useful arbitrary-party two-setting obstruction, standard tensor/regular-representation boundaries, and a conditional Boolean interface. The first can remain as a boundary result. The last is not needed to understand or prove the core article.

## 4. Independent mathematical audit

### 4.1 Scalar foundations and leading layers

**Location:** Section 2, source lines 47-58.

The chain-ring and determinant assumptions are appropriate. Pivot clearing is valid because an entry of minimum valuation divides every entry in the remaining block. This is a divisibility statement, not an invocation of field elimination. The uniqueness of Smith exponents is classical module theory [S5, S6].

The leading-layer definition is valid. If two preimages satisfy `pi^a N = pi^a N'`, their difference has entries in

\[
\operatorname{Ann}(\pi^a)=(\pi^{s-a})\subseteq J.
\]

Consequently their residue matrices agree. This also handles `a=0`, since the annihilator is zero. In Smith coordinates, precisely the factors with exponent `a` survive after this preimage-and-reduction operation. Thus the rank is `h`.

The paper does **not** incorrectly identify `h` with `rank(M mod J)`. For example, `M=diag(u,u)` over `F2[u]/(u^4)` has `M mod J=0`, but its divided leading matrix is the identity and `h=2`. This example should appear early because it prevents a likely reader error.

Rectangular resources are allowed in the support theorem, while the communication theorems explicitly require square ones. The field case `s=1` is consistent: all nonzero exponents are zero, so `h=r`, and the logical-but-not-strong middle stratum disappears. Zero is explicitly excluded from the resource tasks and retained only as a bookkeeping row in the inventory.

**Verdict:** correct; no hidden field assumption found.

### 4.2 Support model and contextuality terminology

**Location:** Definition 2.1 and source lines 60-82.

Primitive rows, their unit-scaling classes, and complete bases are well-defined. Scaling an effect by a unit preserves zero/nonzero contraction. An invertible pair of local basis changes cannot annihilate nonzero `M`, so each context has at least one possible event.

The no-signalling statement is correct at the possibility level. For a fixed Alice row `x`, the row `x M B^T` is zero exactly when `x M` is zero, because `B` is invertible. Thus existence of a possible Bob outcome is independent of Bob's basis. This does not produce a probability distribution or a probabilistic locality statement.

The global assignment is a choice per **setting**, with compatibility across Alice/Bob contexts. A ray appearing in two distinct local settings is not automatically identified as one context-independent hidden effect value. This is a legitimate Bell-style support scenario. It differs from an additional Kochen-Specker coloring constraint, and the hyperplane proof does not silently reintroduce that stronger constraint. The general support hierarchy is established background [S3]; the single-system modal coloring problem is another background comparison [S2].

**Verdict:** coherent and correctly limited. Improve the typing of joint effects for teleportation; do not change the intended setting-indexed model.

### 4.3 Residue-hyperplane lemma

**Location:** Lemma 3.1, source lines 85-93.

The forward direction survives the important all-bases/all-lifts test. Let `U_A` be the union of rays actually selected in some Alice setting by a global assignment. The complement cannot contain an entire basis. If its residue directions spanned the residue space, one could select a residue basis from that complement; lifting those selected rows gives an invertible ring basis, a contradiction. Therefore those residue directions lie in some hyperplane `H_A`.

It follows that **every primitive lift** outside `H_A` is selected somewhere, not merely that each residue direction has one convenient selected lift. Apply the same argument to Bob. Any chosen pair from the two unions occurs as the assignment's outcomes in the corresponding pair of settings, so its contraction is nonzero.

Conversely, every basis has a row outside any fixed residue hyperplane. Choosing such a row in each setting gives a global assignment when all cross-contractions between the prescribed lifts are nonzero.

This argument requires only the stated finite commutative local-ring setting, not Smith form. It does not assert that the complement equals a hyperplane or that one selected representative per residue is sufficient.

**Verdict:** complete and correct. Its elementary basis-complement ingredient should be separated from any novelty claim about the exact support criterion.

### 4.4 Hardy witness and higher-dimensional embedding

**Location:** Lemma 3.2, source lines 95-113; Theorem 3.3, line 134.

All three displayed basis matrices are invertible. With `p=pi^a`, `q0=pi^b`, and `c=pi^(b-a)`, the identity `pc=q0` holds without division by a nilpotent. The four displayed products have supports, in row-major order,

`1001, 0111, 1110, 0111`.

The seed `(F_A=0,F_B=0)` forces `X_B=1`, then `C_A=0`, then `F_B=1`, contradicting the seed. The negative coefficient in `C` is necessary outside characteristic two; direct checks over odd-characteristic and mixed-characteristic rings confirm the written sign.

The embedding argument is also valid. In Smith form, the relevant forcing rows have no coordinates outside the chosen two-factor block, so every additional standard outcome is zero in the forcing steps. Merely adding outcomes cannot evade the contradiction.

The new checker verifies all 36 selected ring/exponent instances directly. These checks corroborate the symbolic products; they do not replace the all-ring proof.

**Verdict:** correct, including unequal valuations and mixed characteristic. The general Hardy mechanism is prior art; the uniform ring formula is the claim requiring positioning.

### 4.5 Complete-basis Smith trichotomy

**Location:** Theorem 3.3, source lines 115-135.

All three parts have valid proofs.

For `r=1`, retain any supported seed. In every other basis choose a row with a unit in the relevant first coordinate. A supported seed gives both `p*x1 != 0` and `p*y1 != 0`, so all seed/new and new/new combinations remain supported. This proves locality in the paper's stronger sense that **every** supported event extends.

For `h=1`, choosing unit first coordinates in all settings makes the divided contraction a unit plus radical terms. That is a unit; multiplying it by the nonzero `pi^a` leaves a nonzero result. This constructs a global assignment, without claiming that every event extends.

For `h>=2`, suppose the hyperplanes existed. Write `H_B=ker(beta)`. Since vectors outside `H_A` span the Alice residue space and the leading matrix has rank at least two, some such vector `x` gives a row `w=x*Nbar` not proportional to `beta`. There is then `y` in `ker(w)` but outside `ker(beta)`. For chosen lifts, `xtilde*N` has a unit coordinate, while its pairing with `ytilde` lies in `J`. Subtract that pairing divided by the **unit coordinate** from the corresponding entry of `ytilde`. This preserves the residue and makes the ring pairing exactly zero. It contradicts the all-lifts conclusion of Lemma 3.1.

This last correction is crucial: reduction to a zero residue is not itself enough to prove a zero ring contraction. The manuscript supplies the additional cancellation step. Together with the Hardy witness whenever `r>=2`, the cases exhaust the nonzero resources.

**Verdict:** the strongest part of the manuscript. I found no missing converse or central gap. Direct support computations over the finite domains below agree throughout.

### 4.6 Invertible-matrix bases and complete analyzers

**Location:** Lemma 4.1, source lines 145-150.

The field proof is valid even over `F2`. Off-diagonal matrix units are differences of `I+E_ij` and `I`. For a diagonal matrix unit, choose a permutation taking `e_j` to `e_i`; then `P(I+E_ji)-P=E_ii`. Both matrices being subtracted are invertible.

After selecting a residue-field basis of invertible matrices, arbitrary entry lifts have two independently necessary properties: every reshaped effect matrix is invertible, and the matrix of flattened effect rows is invertible. The residue determinant criterion proves both. Thus this is genuinely a complete analyzer, not just a list of individually reversible effects.

The theorem states `d>=2`. The excluded `d=1` case is harmless and can be handled by the single matrix `[1]`; it is not a missing case that invalidates the stated result. The new checks included it as an additional boundary test.

**Priority:** units generating/spanning full matrix rings is classical, with substantially stronger results in the Wolfson-Zelinsky and Henriksen literature [S7, S8]. The local lifting step is standard. The manuscript already calls this elementary; adding the historical citation is the proper repair. Finding this antecedent does **not** invalidate the support classification or the exact resource comparison.

**Verdict:** correct; do not market the enabling lemma as a new general algebra theorem.

### 4.7 Exact `d*h` orbit coding

**Location:** Theorem 4.2, source lines 152-171.

Both the upper bound and achievability are valid under the written contract. The proof would benefit from one explicit inclusion.

Let `D` be the invertible joint decoder and `v_i=vec(U_i N)`. For each message,

\[
\operatorname{supp}(\overline D\,\overline v_i)
\subseteq
\operatorname{supp}(\pi^a Dv_i).
\]

A nonzero residue coordinate lifts to a unit, and a unit times nonzero `pi^a` is nonzero. The reverse inclusion need not hold and is not required. Exact decoding forces the right-hand supports for distinct messages to be disjoint, so the nonzero leading vectors on the left have disjoint supports and are linearly independent. They lie in the image under `Dbar` of

\[
V=\{X\overline N:X\in\operatorname{Mat}_d(k)\},\qquad \dim_k V=dh.
\]

The dimension count is rowwise: each of the `d` rows can be chosen in an `h`-dimensional row space. Therefore at most `dh` messages are possible.

For achievability, images of invertible residue matrices span `V`. Choose `dh` independent images, lift the encoders, and extend the resulting columns `vec(U_i N)` to a ring basis. The inverse basis matrix sends the actual codewords to `pi^a e_i`. These are nonzero and have distinct singleton supports. No branch is discarded and no projective identification is needed.

The independent finite optimization over `F2` checks all 20,160 invertible four-coordinate decoders for each of the 15 nonzero resources. It confirms two messages for the nine rank-one resources and four for the six invertible resources. The 52 ring certificates check achievability, not the upper bound over every ring decoder.

**Verdict:** correct. The theorem concerns an exact one-shot message count, not an entropy, stochastic channel capacity, or the cardinality of the GL orbit. The existence of modal field protocols is old [S1]; an identical full chain-ring `dh` theorem was not located in the bounded search.

### 4.8 Exact raw-vector teleportation

**Location:** Theorem 4.4, source lines 173-182.

The branch-transfer identity is correct. Write the unknown input as `x`, the resource as `sum M_jk e_j tensor e_k`, and the joint effect coefficients as `E_ij`. Bob's output has entries

\[
(Tx)_k=\sum_{i,j}E_{ij}x_iM_{jk},\qquad T=M^T E^T.
\]

The effect is a joint covector. Its reshaped `d` by `d` matrix can have full rank. Calling it rank-one analysis must not suggest that the reshaped matrix is a separable rank-one matrix.

For necessity, take any nonzero branch map `T` and suppose `z` is a nonzero kernel vector. There is `x` with `Tx != 0`. Both `x` and `x+z` are nonzero, produce that same possible branch output, and cannot both be recovered by a fixed correction. Thus a universally correct nonzero branch is injective; finiteness makes it bijective. Its inverse is linear. An invertible product `M^T E^T` forces `M` invertible, for example by the commutative determinant criterion. A complete effect basis with nonzero resource cannot make every branch map zero.

For sufficiency, the matrix basis from Lemma 4.1 gives a complete set of effects with every reshaped matrix invertible. Every branch transfer is invertible and can be corrected by its inverse. The identity remains an identity after tensoring with the identity on a reference. Hence the result proves raw-vector recovery and preservation of reference correlations, not merely recovery up to an unknown scalar.

**Verdict:** correct over the stated finite commutative local rings, including the broader non-chain domain of this theorem. The computation checks selected instances; the all-local-ring assertion rests on the proof. The mechanism has substantial algebraic/categorical antecedents [S1, S9, S10, S11]; the exact ring contract and full necessity/sufficiency statement require cautious novelty wording.

### 4.9 The separator and what it actually separates

**Location:** Corollary 4.5, source lines 184-190.

For `M=pi^a I_d`, `0<a<s`, the leading multiplicity is `d`, so the resource is strongly contextual and carries `d^2` exact orbit messages. It annihilates nonzero vectors in `pi^(s-a)K^d`, so it is not universally teleporting. This is a valid, transparent separation.

An important explanatory consequence should be added:

\[
\text{primitive square resource}\quad\Longrightarrow\quad
\bigl(N_{\max}=d^2\bigr)\Longleftrightarrow(h=d)
\Longleftrightarrow(M\text{ invertible})
\Longleftrightarrow\text{universal raw teleportation}.
\]

Indeed, primitivity makes the least exponent zero. Thus the **maximal-coding/nonteleportation separation specifically needs a nonprimitive resource** in this model. This is not a flaw; it tells the reader exactly which modeling choice creates the separation. The generic state convention in de Beaudrap's Definition 7 excludes that resource because its coordinates do not generate the unit ideal [S4].

A compact example sequence would be `diag(1,0)`, `diag(1,u^2)`, `diag(u,u)`, and `I_2`. The middle pair has the same regular binary rank six but different support type and codebook size. The nilpotent example is informative algebraically, not evidence of a physically stronger entanglement resource.

### 4.10 Two-setting obstruction and other boundaries

**Location:** Section 5, especially Theorem 5.1, source lines 224-233.

The arbitrary-party, local-dimension-two, two-setting theorem is correct. Over `F2`, two distinct bases share one nonzero row; write the alternatives as `a,b` and `a,a+b`. Choose an inclusion-minimal nonzero tensor coefficient in the corresponding `a,b` coordinates. Choosing the shared effect outside its support and the nonshared effect inside its support gives nonzero contractions in every context: all proper-subset coefficients vanish by minimality. Coincident bases create no difficulty.

For a finite local ring with residue `F2`, pass to a nonzero leading radical layer and a linear functional on that layer that detects a coefficient. The field argument gives a contraction detected by the functional, so the original ring contraction cannot be zero. This does not require a chain-ring Smith form.

The result proves existence of at least one global assignment. It **does not prove locality**, because some supported events can still fail to extend. The manuscript's formal theorem respects this distinction. Any shorthand in future summaries should do so too. Exact arbitrary-party/local-ring historical priority remains less well settled than the proof's correctness.

The balanced-tensor example `u^3 tensor_A u=0` versus `u^3 tensor_F2 u !=0` is correct. The binary-rank formula and explicit same-rank/different-resource examples are also correct. However, source line 212 invokes an unspecified restricted construction and an `R -> R^{-1}` comparison without a self-contained definition or local certificate. This peripheral assertion is **unverified as written**, not evidence against the central theorems. Delete it or supply its actual content.

### 4.11 Boolean appendix: valid construction, one scope repair

**Location:** Appendix A, source lines 263-292.

The Boolean-ring obstruction, coefficientwise scalar extension, and coefficient-OR support formula are valid. A unital map from a Boolean ring into a local ring can only produce idempotents zero and one, so it cannot generate the nilpotent `u`. In `B tensor_F2 A`, the four coefficients are unique, and an evaluated contraction is nonzero precisely when at least one coefficient evaluates to one. No additive or multiplicative nonzero-test homomorphism is implied.

The conjugate projectors `J_i=B0^{-1} P_i B0` are valid. The sentence explaining nonzero branches by saying that every relevant column has a unit coordinate needs a domain qualification. It is valid over the local ring `A`; it need not be valid over the symbolic ring `B tensor A`, which need not be local.

For an explicit counterexample to the overbroad intermediate assertion, let `t` be a nontrivial Boolean variable and set

\[
C=\begin{pmatrix}t&1+t\\1+t&t\end{pmatrix}.
\]

Then `C^2=I`. Neither `t` nor `1+t` is a unit in the Boolean coefficient ring, since each vanishes at one valuation. Each column is unimodular but has no individual unit entry. The same example sits inside the enriched coefficient ring.

The desired projector conclusion is still true, with a simpler proof:

\[
B_0J_i\psi=P_iB_0\psi.
\]

Invertibility of `B0` makes the left-hand side zero exactly when `J_i psi` is zero, and the right-hand side is zero exactly when the measured coordinate is zero. This proof works over any commutative coefficient ring and avoids the questionable unit-coordinate claim entirely.

**Verdict:** localized clarification, not a failed resource theorem. I recommend moving this appendix to an optional interface supplement or companion article, because it is not part of the central classification's publication case.


## 5. Fresh finite evidence: what was and was not checked

### 5.1 Independent implementation and decision procedure

The new `p01_independent_checks.py` implements ring operations, primitive projective rays, bases, contractions, matrix inversion, Smith elimination, support constraints and codebook tests independently of the supplied generator. It uses Python's standard library. Its recorded SHA-256 is `3dbe764ab388bf34d3f59329bd944dac5b36d002f6fa4d93b4d7b81e6c62b96a` and the deterministic sampling seed is `20260926`.

For two-outcome local bases, a global assignment is represented by one binary variable per basis on each side. Every forbidden joint outcome supplies a two-literal clause. Satisfiability tests whether any global assignment exists. Pinning each supported event tests whether every such event extends. Thus the decisions come from the support definition, not the Smith classification. Identical support tables are cached; their classifications are not guessed from invariants. The binary-field cases were additionally cross-checked by brute-force assignment enumeration.

The full run directly checked every nonzero 2-by-2 resource in nine rings, totaling **22,170 matrices**:

| Ring | Nonzero resources | Rays / bases per party | Local | Logical, not strong | Strong | Mismatches |
|---|---:|---:|---:|---:|---:|---:|
| F2 | 15 | 3 / 3 | 9 | 0 | 6 | 0 |
| F3 | 80 | 4 / 6 | 32 | 0 | 48 | 0 |
| F4 | 255 | 5 / 10 | 75 | 0 | 180 | 0 |
| F2[u]/(u^2) | 255 | 6 / 12 | 81 | 72 | 102 | 0 |
| Z/4Z | 255 | 6 / 12 | 81 | 72 | 102 | 0 |
| F2[u]/(u^3) | 4,095 | 12 / 48 | 657 | 1,800 | 1,638 | 0 |
| Z/8Z | 4,095 | 12 / 48 | 657 | 1,800 | 1,638 | 0 |
| F3[u]/(u^2) | 6,560 | 12 / 54 | 896 | 1,728 | 3,936 | 0 |
| Z/9Z | 6,560 | 12 / 54 | 896 | 1,728 | 3,936 | 0 |

An additional **38 resources over `A=F2[u]/(u^4)`** were checked against all 192 local bases: 14 nonzero Smith representatives and 24 deterministic random matrices. Their outcomes were 5 local, 17 logical-but-not-strong and 16 strong, again with no mismatch. This is not a claim to have run the full support solver on all 65,535 nonzero matrices over `A`.

These tests cover the smallest field, an extension field, equal-characteristic rings, mixed-characteristic rings, nilpotent resources and singular resources. They materially strengthen the finite evidence for the actual all-bases contract. They remain finite evidence, not a proof of the arbitrary-ring or arbitrary-dimension statement.

### 5.2 Separate exhaustive Smith inventory over A

A fresh exact elimination pass classified all **65,536** 2-by-2 matrices over `A`, including zero. The 15 Smith-class sizes agree with the supplied table. The resulting nonzero-category totals are:

| Category | Count |
|---|---:|
| Local | 5,265 |
| Logical but not strong | 34,056 |
| Strong | 26,214 |
| Zero, excluded from the resource task | 1 |

The class-size computation is independent. Converting class sizes to contextuality totals uses the proved invariance under invertible basis changes and the separately support-tested representatives. This is stronger than merely copying a formula, but it must not be described as an exhaustive direct support decision on every matrix. `A2_smith_inventory.csv` records the actual class sizes.

### 5.3 Additional exact checks

| Test | Actual coverage | Result and evidentiary limit |
|---|---|---|
| Hardy witness | 36 nonzero exponent pairs across nine chain rings (including F2 and F3) | All four support patterns agree with the argument, including odd and mixed characteristic. Not a proof for every ring. |
| Complete analyzers | Seven rings, dimensions 1, 2, 3, 4: 28 configurations | Both the flattening basis and each reshaped matrix are invertible. Branch correction identities were checked for one explicitly invertible resource per configuration. |
| Orbit-code lower bound | 52 nonzero Smith representatives across seven rings | Explicit encoders and a complete decoder give the claimed sparse outputs. These are achievability certificates, not an exhaustive upper-bound search over ring decoders. |
| Binary-field coding optimum | All 15 nonzero resources; all 20,160 invertible 4-by-4 decoders per resource | Optimizing pairwise disjoint decoded supports gives two messages for each of the nine rank-one resources and four for each of the six invertible resources. |
| Two-setting obstruction | All 255 nonzero three-party binary tensors, a representative pair of distinct settings per party | Every instance has a global assignment. Distinct setting pairs are related by local `GL2(F2)` changes. This does not establish locality or arbitrary-party validity computationally. |
| Supplied analyzer certificates | Nine stored examples over Z/4, Z/8, Z/9, dimensions 2, 3, 4 | Independently rechecked both required invertibilities. These supplied certificates are genuine checkable evidence. |

No singular teleportation counterexample emerged in these checks, but there was not a comprehensive enumeration of all possible teleportation protocols. The necessity proof is the evidence for the unrestricted general impossibility statement.

The checker is an audit deliverable, not a retroactive substitute for the manuscript's purported unchanged canonical runner. Its outputs identify the environment, seed, source hash, test scope and exact results. Reported runtime is merely execution provenance, not a benchmark claim.

## 6. Reproducibility and manuscript production

### 6.1 Definite failure of the supplied entry point

Running the supplied `generate_assets.py` from an isolated working copy fails before its analyzer generation, with `FileNotFoundError` for:

`runs/canonical_01/independent/resource_inventory_summary.json`

The expected input is resolved relative to the portfolio-style output directory and is not present in the uploaded archive. The generator hash matches the stored manifest; the missing input's recorded hash cannot be checked without the file.

Other references lead to missing artifacts, including the reproduction envelope, run manifest, explicit decoders, historical suites, and the sibling program reproduction supplement. Section 6 says that a canonical runner, a 14-resource decoder set, historical stages and other checks are supplied. That is not true of this standalone ZIP. The larger portfolio may contain them, but their existence, bytes and reproducibility were not established by this audit.

The reproduction wrapper explains the partition and duplicate policy; it does not make the present archive self-contained. I therefore distinguish an understandable packaging omission from a mathematical falsification. Nevertheless, it is a real publication-readiness issue.

**Repair:** either include the actual dependencies and an independently repeatable clean-directory command, or revise Section 6 to remove unsupported availability claims and replace them with the actual available evidence. If the new audit checker is adopted, label it a new independent checker, preserve its scope and hashes, and do not describe it as the unchanged historical runner.

### 6.2 Which evidence is circular or weaker than its label suggests?

A table that applies the analytic Smith criterion to every class is an illustration of that criterion. It is not independent support for the criterion. A JSON file with explicit matrices can be independent evidence if those matrices are checked from definitions. A status string such as `verified` or `PASS` without the runner and inputs is not equivalent evidence.

The supplied material mixes these levels. The corrected supplement should have an evidence column distinguishing direct support solving, exact identity/certificate checks, invariant-based aggregation and proof-generated tables. The 256-product Boolean/LM statement, including the reported 112/144 split, was not freshly reproduced from the absent historical suite and should not acquire a new certification label from this audit.

### 6.3 Build and visual results

A separate clean working copy was built with shell escape disabled, using LaTeX, BibTeX and two subsequent LaTeX passes. The system's default BibTeX launcher had an environment problem; invoking the installed `bibtex.original` executable resolved it. That launcher problem is not a defect in the manuscript.

The final output has 11 pages. Extracted text agrees with the supplied PDF after whitespace normalization. The final build contains no unresolved reference/citation warning or overfull/underfull box report. The original 11 pages and a fresh-build contact sheet were visually inspected; no clipping or overlapping equations/tables was found. This is useful submission-production evidence, not proof validation.

The author footnote still says that metadata will be completed before submission. Several bibliography records should be upgraded from preprint-style entries to verified published metadata. These are localized professional-preparation issues.

## 7. Fresh primary-source and novelty audit

### 7.1 Search method and limits

The literature search was run on 26 September 2026. It used the manuscript's terms and translations into module geometry, invertible matrix bases, finite-ring channels, modal protocols, generalized teleportation and support/global-section language. Existing ledgers supplied leads but not verdicts.

The principal sources and inspected locations are documented in Section 17. Some are fully accessible papers; some are selected thesis sections or primary author-repository abstracts. The original Zelinsky PDF was not retrievable through its publisher, and is not represented here as fully read. Its result is explicitly recorded in later primary research, and Henriksen's author repository supplies a further primary antecedent for the relevant units-span fact.

No exact antecedent for the full complete-basis chain-ring trichotomy or the identical `d*h` communication contract was located. That establishes a **bounded-search result**, not historical uniqueness. The appropriate novelty confidence is moderate, not certified firstness.

### 7.2 Closest sources and actual relationships

| Prior source | Established overlap | Distinction relevant to P01 | Audit consequence |
|---|---|---|---|
| Schumacher and Westmoreland, *Modal quantum theory* [S1] | Finite-field states, basis measurements, possibility from nonzero amplitudes, reversible linear maps, dense coding and teleportation | The inspected field examples do not state P01's all-chain-ring Smith trichotomy or exact identical-contract `d*h` theorem | Protocol existence and modal vocabulary are prior art; the classification/comparison needs its own contribution statement |
| Schumacher and Westmoreland, *Non-contextuality and free will in modal quantum theory* [S2] | Modal contextuality/nonlocality, including shared-effect consistency questions | P01's choices are indexed by whole local settings, not an additional identification of every repeated effect ray | Explain the contract difference without dismissing all previous bipartite nonlocality as merely single-system KS |
| Abramsky and Brandenburger [S3] | Global sections and a hierarchy of possibilistic/logical/strong contextuality | These provide the conceptual framework, not the chain-ring classification | Credit the framework; do not rename an established hierarchy as a new one |
| de Beaudrap [S4] | Algebraic/modal computation over rings and an explicit admissibility condition for states | Definition 7 requires coordinate ideal equal to the unit ideal; over a local ring this is primitivity | The nonprimitive separator lies outside that state class. This is an important boundary, not a disproof of P01 |
| Honold and Landjev [S5]; Byrne et al. [S6] | Chain-ring modules, shape/type, decomposition and finite geometry | These are the algebraic foundation; the inspected statements do not address the same support or analyzer tasks | Strengthen primary attribution and separate classical invariant theory from the application |
| Wolfson/Zelinsky as recorded in later primary research [S7]; Henriksen [S8] | Matrix/endomorphism rings generated additively by their units, with stronger decomposition statements | A basis of invertibles over a field follows from spanning; local-ring lifting is elementary | Treat Lemma 4.1 as a classical enabling fact, not a new theorem-level contribution |
| Varughese [S9] | Finite-field categorical teleportation and coding examples | The inspected examples use a different categorical/measurement setup; the displayed qutrit construction has three chosen states, not P01's full nine-row analyzer | The historical comparison is relevant but not an equivalence of contracts |
| Thas [S10] | A broad quantum-like formalism over division rings with involution and protocol constructions | Division-ring/Hermitian structure excludes the nilpotent chain-ring mechanism at issue here | An adjacent predecessor, not an identified exact antecedent to the zero-divisor classification |
| Verdon [S11] | Entanglement-invertible channels and teleportation-related classifications | Complex operator-algebra/channel assumptions differ from raw vectors over finite local rings and unrestricted GL corrections | Do not claim the general invertibility intuition is new; compare the exact formal statement |
| Feng, Nobrega, Kschischang and Silva [S12] | Communication over finite-chain-ring matrix channels, module-shape descriptions and capacities | Their stochastic transfer/noise channel is not the P01 jointly decoded orbit-support problem | This is a missing useful comparison, not evidence that the `d*h` statement is already proved there |
| Ben-Zvi, Ma and Reyes [S13]; Cortez, Morales and Reyes [S14] | Kochen-Specker obstructions for matrix/partial-ring structures | Compatible-idempotent colorings are not a fixed resource's setting-indexed bipartite support | Credit ring-valued contextuality precedents without conflating their theorem with the present one |
| Schumacher and Westmoreland, *Almost quantum theory* [S15] | Further modal mixtures/processes and possible/probable relationships | P01 intentionally does not establish such a complete process/probability theory | Keep the stated static support and algebraic protocol boundaries |

### 7.3 The invertible-matrix issue is resolved, not merely suspected

The field span lemma is definitely not a novel general algebraic phenomenon. Classical results on sums of nonsingular transformations are stronger than the spanning assertion. Henriksen's result that matrix rings of size greater than one are generated by sums of units gives another direct antecedent. The exceptional one-dimensional binary case in the two-summand theorem does not obstruct the basis claim: the 1-by-1 identity is itself a basis.

P01 already presents its construction as elementary. The required repair is therefore attribution and hierarchy: retain a short self-contained proof as a tool, cite the established phenomenon, and make clear that the publication contribution rests elsewhere. This does not erase the complete-basis contextuality result.

### 7.4 Why the finite-ring channel comparison matters

It would be misleading to dismiss finite-chain-ring coding literature just because it does not use the word contextuality. Module shapes, orbit ideas and decoding constraints are central there. It would be equally misleading to equate those papers' channel capacities with P01's exact message count.

For example, in a noiseless version of the uniform unknown square-transfer model `Y=A X`, replacing `X=M` by `X=U M` leaves the distribution invariant when `A` is uniform over the invertible group: `AU` has the same distribution as `A`. That elementary observation explains why P01's controlled local encoder plus complete joint readout is a different task. This comparison is an inference from the explicit channel model, not a claim that the source discusses P01.

A compact in-paper contract table should list the scalar system, state admissibility, local reversible maps, measurement/readout rule, exactness notion and conclusion. This would make the distinction informative rather than defensive.

### 7.5 Novelty types, rather than a single uniqueness number

| Novelty type | Assessment |
|---|---|
| Theorem novelty | The full chain-ring trichotomy and matched-contract `d*h` statement are plausible original results at moderate confidence. Historical priority is unresolved. The matrix-span fact is classical. |
| Proof novelty | The all-lifts hyperplane formulation and radical cancellation are useful mechanisms, but this search does not establish that their underlying algebra is new. |
| Classification novelty | The strongest candidate: a complete, concise partition by `r` and `h` under a clearly stated measurement family. |
| Unification novelty | Substantial value: support obstruction, exact message count and raw teleportation are organized by related but different invariants. |
| Contract novelty | Material. Full bases, arbitrary invertible readout, all nonzero resources and exact raw recovery determine what the theorems mean. Contract specificity is not automatically triviality. |
| Application novelty | A useful application of standard chain-ring structure to modal support/information tasks. |
| Expository novelty | Potentially valuable if the paper foregrounds the resource map and explains primitive versus nonprimitive behavior. An appendix from another program should not carry this burden. |

## 8. Completeness, scope, significance and exposition

### 8.1 Is the central mathematics self-contained?

For the principal theorems, substantially yes. A competent reader can reconstruct the arguments from the article. The supplied audit notes are not needed to make a missing central proof true. The article would nevertheless benefit from a few displayed intermediate steps: the leading-layer well-definedness, residue-support inclusion, matrix types in the transfer formula and why extra outcomes do not evade the embedded Hardy forcing.

The unsupported restricted-construction sentence in Section 5.1 is an exception to self-containment, but is unused by the central proofs. It should be deleted or made explicit rather than defended by pointing to an unnamed audited construction. The computational availability statements also cannot be verified from this ZIP.

### 8.2 One paper or several?

**Keep the three main resource questions in one paper.** They are not merely three examples with a common vocabulary. Their comparison is organized by the same Smith profile, and the contrast between `h`, `r` and full invertibility produces a useful classification diagram.

The two-setting theorem is a relevant boundary result and can stay if clearly distinguished from the complete-basis classification. Move the resource map currently in Appendix B toward the end of the introduction or the start of the comparison section. Move the Boolean-interface appendix to an optional supplement/companion discussion, or sharply reduce it. Splitting the three central results now would likely weaken the unification claim and repeat foundational material.

### 8.3 What makes the separation meaningful, and what limits it?

The cleanest interpretive addition is the primitive-resource comparison. If `M` is primitive, the least exponent is zero. Hence

\[
\text{maximum codebook}=d^2
\quad\Longleftrightarrow\quad h=d
\quad\Longleftrightarrow\quad M\text{ is invertible}
\quad\Longleftrightarrow\quad\text{universal exact raw teleportation}.
\]

Thus the particular maximal-coding/nonteleportation separation genuinely uses nonprimitive resources. This observation follows directly from the audited theorems and should be stated, rather than leaving a referee to discover it. It does not say that every primitive strongly contextual resource teleports: for dimension larger than two, `2<=h<d` remains possible.

The mathematical significance is a transparent classification and comparison, not a proposed physical replacement for quantum theory. Standard ingredients do not invalidate that significance; they require accurate framing. Conversely, terminology such as quantum or universal must not be used to inflate a task-specific algebraic result.

### 8.4 Specific editorial changes

Begin with one worked table over `F2[u]/(u^4)`: a rank-one resource, `diag(1,u^2)`, `diag(u,u)`, and `I2`. Display `r`, least exponent, `h`, support class, exact message count and teleportation status. This gives both target audiences a common point of reference before the proofs.

For finite-ring readers, define the support/global-assignment task using one two-party context table. For foundations readers, explain unit, primitive row, annihilator and why ordinary residue reduction loses the leading layer. Keep the distinction between basis-indexed locality and additional shared-ray identifications visible.

Replace ambiguous rank-one-effect language with typed covectors and a reshape definition. In the conclusion, replace the phrase suggesting that mere nonzero rank creates a logical obstruction by the actual threshold `r>=2`. The title is defensible. The abstract should state the complete-basis and raw-vector restrictions once, and foreground the comparison instead of listing all secondary interface material.

## 9. Simulated referee perspectives

The following are deliberately different critical perspectives within this single audit. They are **not reports obtained from six independent people**.

### Referee A - finite-ring algebra and modules

**Strongest positive:** the leading-layer construction respects annihilators, and the strong-contextuality proof converts residue cancellation into exact ring cancellation using a unit coordinate. No inappropriate division by a nilpotent is needed.

**Strongest objection:** classical module structure and units-span results need more precise attribution; Appendix A momentarily transfers a local-ring property to a potentially nonlocal symbolic coefficient ring.

**Questions to the author:** Can the leading preimage's independence be stated explicitly? Is every use of primitive/unimodular tied to its coefficient ring? Which algebraic lemmas are background rather than contributions?

**Severity:** P2 mathematical clarification; P1 contribution-positioning concern. No principal-theorem rejection on this audit.

### Referee B - contextuality and foundations

**Strongest positive:** the all-lifts quantifier is handled correctly, and the three support strata have explicit mechanisms rather than only computational labels.

**Strongest objection:** readers may silently add shared-ray noncontextuality or confuse logical locality with probabilistic locality. Those would change the problem.

**Questions:** Why is the entire basis the setting? Which conclusions survive restricted settings? Can a small middle-stratum example be worked through? Does the two-setting result claim only one global assignment, as it should?

**Severity:** predominantly P2 exposition and contract clarity. Restricted-settings classification is optional future research, not a prerequisite for this theorem.

### Referee C - algebraic information protocols

**Strongest positive:** the codebook proof has matching upper and lower bounds, and exact branch inverses explain reference-system preservation without hidden postselection.

**Strongest objection:** effect reshaping is insufficiently explicit, and the maximal-coding/nonteleportation example is meaningful only after stating which nonprimitive states are admitted.

**Questions:** What exactly is a rank-one effect here? Can the transfer matrix be derived with indices? Does maximal coding coincide with teleportation for primitive resources? What is the unassisted `d`-message comparison task?

**Severity:** P2 typing/interpretation; P1 if the broader protocol novelty is overstated in revision. No new physical resource theory is required.

### Referee D - coding theory and finite geometry

**Strongest positive:** residue orbit spans give a sharp and economical resource invariant, and the complete-readout construction realizes the upper bound.

**Strongest objection:** the author should not ignore module-shape coding literature or advertise a message-count theorem as a general channel-capacity theorem.

**Questions:** Which hypotheses distinguish this task from finite-chain-ring matrix channels? Is unit rescaling consistently treated? Which parts are immediate from known orbit/span theory, and what is the new operational identification?

**Severity:** P1 positioning. This concern is addressable with a precise comparison rather than a new theorem.

### Referee E - journal referee and novelty specialist

**Strongest positive:** there is one plausible, focused article with a concrete organizing invariant and clear nonclaims.

**Strongest objection:** internal portfolio uniqueness is not external originality; the in-paper contribution comparison is weaker than the private ledger. The Boolean appendix dilutes the strongest story.

**Questions:** What exact theorem should an expert cite this paper for? Which result remains interesting after the classical ingredients are credited? Can the resource map be moved forward and the peripheral interface removed?

**Severity:** P1 literature/contribution revision, P2 structure. No evidence-based prediction of acceptance is made.

### Referee F - reproducibility and computational mathematics

**Strongest positive:** the manuscript compiles, hashes match, stored analyzer matrices validate, and the new independent support calculations are substantial.

**Strongest objection:** the supplied canonical generator does not run from the package, while the article says its dependencies and supporting suites are provided. Some displayed classifications use the criterion they ostensibly corroborate.

**Questions:** Can an unrelated reader unzip into a clean directory and run the stated command? Which outputs are direct support decisions, and which are theorem-generated? Where are the explicit decoders and historical run inputs?

**Severity:** P1, essential before release of the current evidence claims.

**Panel synthesis:** the perspectives converge on preserving the main article, repairing evidence access, clarifying a few short arguments and strengthening attribution. They differ about how much interpretive or optional material to retain, not about an identified false central theorem. The computational concern is not neutralized by the algebraists' confidence; the algebraic results are not falsified by the packaging failure.


## 10. Claim-by-claim verdict summary

The accompanying CSV contains 18 claim records with source locations, assumptions, proof status, finite evidence, closest prior art and required actions. The central verdicts are summarized below. "Correct" here means supported by this reconstruction, not formally certified.

| Claim | Manuscript | Correctness / completeness | Novelty and publication treatment |
|---|---|---|---|
| Leading layer and Smith invariants | Section 2 | Correct; no illicit nilpotent division | Classical background; improve primary attribution |
| Residue-hyperplane criterion | Lemma 3.1 | Correct, including all primitive lifts | Useful exact formulation; priority unresolved |
| Uniform Hardy witness | Lemma 3.2 | Correct; signs and embedded extra outcomes work | Known argument type with a ring-specific uniform implementation |
| Complete-basis trichotomy | Theorem 3.3 | Correct under the written setting-indexed contract | Strongest apparently new classification, moderate confidence |
| Invertible-matrix analyzer basis | Lemma 4.1 | Correct, including F2 and lifting | Classical enabling algebra, not a new matrix theorem |
| Exact `d*h` codebook | Theorem 4.2 | Upper and lower bounds both survive | Apparently differentiated matched-contract result, moderate confidence |
| Coding advantage iff strong contextuality | Corollary 4.3 | Correct for the stated unassisted threshold | Direct consequence of the two main classifications |
| Universal exact raw teleportation iff invertibility | Theorem 4.4 | Correct necessity, sufficiency and reference preservation | Contract-specific theorem from familiar algebraic mechanisms; priority unresolved |
| Maximal coding without teleportation | Corollary 4.5 | Correct for allowed nonprimitive resources | Useful separation, explicitly outside primitive-only conventions |
| Two-setting obstruction | Theorem 5.1 | Correct absence-of-strong-contextuality statement | Retain as a boundary; do not call it a full locality theorem |
| Restricted-construction equivalence | Section 5.1, line 212 | Insufficiently defined to verify as written | Remove or provide construction; not used in main results |
| Boolean scalar/interface results | Appendix A | Main results correct; symbolic unit-coordinate explanation needs repair | Standard/interface material; optional scope reduction |
| Historical verification/availability claims | Section 6 | Not reproducible from the furnished archive | Correct the package or narrow the claims before release |

## 11. How this audit changes the previous internal assessments

| Earlier assessment | Independent outcome here |
|---|---|
| Gate 2 says the all-lifts, cancellation, codebook and teleportation arguments survive | **Agree for reconstructed reasons.** The report gives those arguments and fresh direct support checks, rather than adopting the word cleared. |
| Earlier reviews call the analyzer extension elementary rather than a novel matrix theorem | **Agree and strengthen attribution.** The classical units literature supplies definite antecedents. This is not a newly discovered retraction of a claim the manuscript actually made. |
| The viability review reports five direct Z/4 Smith-representative checks | **Substantially strengthen finite evidence.** This audit directly classifies every nonzero 2-by-2 resource in nine rings and additional A4 cases. |
| Reproducibility concern marked resolved because 21 supplied stages passed | **Do not carry that clearance into the present package.** The required runner/dependencies are absent here and the supplied generator fails. This does not establish that an earlier larger package never ran. |
| Viability table uses the shorthand two-setting locality | **Correct the shorthand.** The theorem establishes existence of a global assignment, hence no strong contextuality, not extension of every supported event and hence not full possibilistic locality. |
| Priority remains moderate and submission positioning unfinished | **Agree, with a more specific literature comparison.** No exact antecedent was located, but units, modal protocols, admissibility and matrix-channel coding must be distinguished explicitly. |
| Research should continue in a focused way | **Narrow the immediate next step.** Bounded repair and positioning are justified. Additional restricted-setting, encoder-group or non-chain-ring theorems are optional research, not prerequisites imposed by this audit. |
| No localized projector concern previously recorded | **Add a new local issue.** The symbolic coefficient ring need not be local; the desired conclusion admits a direct invertibility proof. |

## 12. Publication-readiness scorecard and hard gates

Scores use the requested 0-10 scale. They are expert-style judgments, not measurements, acceptance probabilities or independent panel votes. In particular, the originality score reflects a bounded, moderate-confidence search. No arithmetic mean is used.

| Category | Score | Principal evidence | Most important remaining weakness |
|---|---:|---|---|
| Mathematical correctness | 8/10 | Central proofs survive reconstruction and bounded counterexample searches. | Localized symbolic justification requires repair; not formal proof certification. |
| Proof completeness | 8/10 | Main theorems are derivable from manuscript arguments. | Expose support inclusion and effect reshaping; remove unsupported peripheral assertion. |
| Precision of assumptions and contracts | 8/10 | All-bases, full GL, balanced tensors and raw recovery are explicit. | Clarify rank-one effect typing and symbolic coefficient ring. |
| Internal logical consistency | 8/10 | Classification, codebook and teleportation map agree. | Evidence-availability wording and the discussion rank summary need correction. |
| External originality / theorem-level uniqueness | 7/10 | No equivalent full chain-ring trichotomy or identical orbit theorem located. | Provisional, moderate-confidence assessment; not historical priority clearance. |
| Quality of novelty substantiation | 6/10 | Existing ledgers and explicit nonclaims are useful. | Close antecedents need an in-paper hypothesis/conclusion comparison. |
| Mathematical significance | 7/10 | A common invariant organizes a clean three-resource comparison. | Standard ingredients; significance is classification/unification, not new general matrix algebra. |
| Completeness of literature review | 6/10 | Core modal, sheaf and state-admissibility references are present. | Units literature and finite-chain-ring information/coding comparisons need improvement. |
| Reproducibility | 4/10 | PDF builds and supplied analyzer certificates validate. | The unchanged generator fails; much of the claimed supplement is absent. |
| Independence of computational evidence | 5/10 | Some supplied certificates contain checkable matrices. | Other tests depend on absent runners or use the analytic classification. New audit checks are separate. |
| Expository clarity | 7/10 | Short coherent arguments and a useful resource map. | Dense leading-layer and operational steps deserve worked examples. |
| Accessibility to adjacent specialists | 6/10 | The required algebra is modest. | Algebra readers need support-model motivation; foundations readers need ring/annihilator examples. |
| Scope and conceptual coherence | 7/10 | Three resource questions share the same Smith data. | Boolean-interface appendix and portfolio remnants dilute the center. |
| Appropriate claim calibration | 8/10 | No physical model, priority certificate or computational speedup is asserted. | Availability claims overreach this ZIP; separator significance needs primitive-state comparison. |
| Quality of references and attribution | 6/10 | Major relevant authors are credited. | Missing classical units citation and incomplete published metadata. |
| Reviewer resilience | 6/10 | Main proof objections have concrete answers. | A referee can still object to evidence access and insufficient differentiation of known ingredients. |
| Technical manuscript preparation | 8/10 | Fresh 11-page build; text matches supplied PDF; no final unresolved citations/overfull boxes. | Author metadata and bibliography remain draft-like. |
| Overall preprint readiness | 6/10 | The core can responsibly be released after bounded repairs. | Repair evidence claims, symbolic explanation and peripheral unsupported assertion first. |
| Overall journal-submission readiness | 5/10 | One viable focused article; no fundamental rework identified. | Major pre-submission revision of evidence packaging and contribution positioning. |

### Hard gates

| Gate | Status | Reason |
|---|---|---|
| A - Principal-theorem correctness | PASS | No counterexample or central proof gap found; Appendix A has a localized justification issue, not a failed principal theorem. |
| B - Proof completeness | PASS WITH MINOR REPAIR | Add the explicit typing/support steps and fix Appendix A; remove or substantiate the peripheral restricted-construction statement. |
| C - Novelty / positioning | UNRESOLVED | The full classification is apparently differentiated at moderate confidence. Historical-firstness claims are not cleared; a conservative contribution is defensible. |
| D - Reproducibility | FAIL | The submitted archive is not a self-contained executable reproduction package, despite a successful PDF build. |
| E - Scope coherence | PASS | Classification, coding and teleportation form one article. Relocating the Boolean appendix is recommended, not mandatory. |
| F - Literature completeness | UNRESOLVED | Several close domains now have identified primary sources; the in-paper comparison must be finalized before submission. |
| G - Claim calibration | FAIL | Mathematical nonclaims are good, but Section 6 says evidence is supplied that is absent from this ZIP. Fix together with D. |
| H - Submission professionalism | PASS WITH MINOR REPAIR | Complete metadata, published references, accessible supplement and final targeted layout check. |

Gate D and Gate G fail for the same principal evidence-availability issue; they are not two independent mathematical failures. The principal-theorem correctness gate does not certify the peripheral undefined assertion. The bibliography/priority gates are unresolved because theorem-level positioning remains unfinished, not because a known source was found to refute the whole article.

## 13. Prioritized issue register

**Counts: 0 P0; 2 P1; 7 P2.** P2 entries include recommendations as well as localized corrections. The companion `P01_PUBLICATION_BLOCKERS.md` gives exact locations, repairs, timing and effects on central claims for every item.

| ID | Severity | Issue | Claim impact |
|---|---|---|---|
| P1-01 | P1 | Reproduction dependencies missing from the submitted archive | No theorem change expected. Changes the factual evidence/availability statements. |
| P1-02 | P1 | Contribution positioning is not yet a submission-quality theorem comparison | May change the contribution paragraph and novelty classification; no contradiction of the main theorems found. |
| P2-01 | P2 | Symbolic projector proof uses a local-ring property without fixing its domain | No change to projector theorem. Explicit counterexample to the overbroad intermediate assertion is in the report. |
| P2-02 | P2 | Joint effect versus reshaped matrix should be typed explicitly | Clarifies existing contract; no change under the intended reading. |
| P2-03 | P2 | A peripheral restricted-model equivalence is not self-contained | Removes or supports a peripheral claim only. |
| P2-04 | P2 | A few short proofs need one more explanatory step | No theorem change. |
| P2-05 | P2 | Portfolio-specific appendix obscures the article center | Scope change only; not a mathematical repair requirement. |
| P2-06 | P2 | Published bibliographic metadata should replace provisional arXiv-only entries | No theorem change. |
| P2-07 | P2 | Submission metadata and several interpretive phrases remain draft-like | No change to formal theorem statements. |

## 14. Strongest defensible contribution and claims to avoid

### 14.1 Recommended contribution paragraph

> We classify complete-basis possibilistic contextuality for nonzero bipartite resources over finite commutative chain rings. The number of nonzero Smith factors and the multiplicity of the least Smith exponent distinguish local, logically contextual but not strongly contextual, and strongly contextual resources. Under a specified full-invertible-orbit encoding and complete joint-readout contract, the same leading multiplicity gives the exact maximal codebook size `d*h`. Comparing this with universal exact raw-vector teleportation over finite commutative local rings yields a separation realized by nonprimitive resources. The contribution is the classification and matched-contract comparison; the underlying module theory, modal framework and elementary analyzer algebra are established ingredients.

This is a contribution statement, not a historical-firstness declaration.

### 14.2 More conservative alternative

> Using standard finite-chain-ring module structure and an explicitly fixed possibilistic measurement model, we present a unified classification of support contextuality and exact orbit coding, and compare these with raw-vector teleportation. The results organize the three tasks by related Smith and invertibility data, make the role of nonprimitive resources explicit, and provide self-contained proofs and bounded computational checks. We distinguish this setting from primitive-state models, shared-effect Kochen-Specker colorings and stochastic finite-ring matrix channels.

### 14.3 Claims the author should avoid unless additional evidence is obtained

Do not claim that modal nonlocality, Hardy arguments, finite-field teleportation, the contextuality hierarchy, Smith theory or invertibles spanning a matrix algebra originate here. Do not claim universal priority for the full trichotomy merely because this search found no equivalent source.

Do not describe `d*h` as a general Shannon capacity, a physical dense-coding advantage or a computational speedup. Do not generalize the theorem to arbitrary measurement families, restricted encoder groups or non-chain rings without new work. Do not describe the raw-teleportation theorem as valid under only rotation-restricted corrections.

Do not claim a tensor-closed multi-round probabilistic process theory. Do not portray the nonprimitive separator as a counterexample inside primitive-only frameworks. Do not call a no-strong-contextuality theorem a locality theorem. Do not describe omitted historical scripts/certificates as currently supplied or freshly reproduced by this audit.

## 15. Revision plan and whether more mathematics is required

### Essential before a public preprint

Resolve P1-01 by furnishing an actual runnable supplement or pruning/replacing the evidence-availability claims. Preserve a clean distinction between fresh independent tests and historical reports. Correct the symbolic-projector justification if Appendix A stays. Type the joint effects and transfer matrices explicitly. Remove or prove the undefined restricted-construction sentence. Correct the `r>=2` and no-strong-versus-local summary language. Add the classical units attribution and use a conservative contribution statement.

A responsible preprint need not wait for proof that no equivalent result exists anywhere in the literature. It does need truthful evidence claims, appropriate credit for identified predecessors, complete main arguments and clear limitations.

### Essential before journal submission

Complete P1-02: a concise source-based comparison of the nearest contracts and theorem statements. Make the article's distinctive citation target unmistakable. Finalize author/contact metadata and published bibliography records. Confirm that the final supplement, manuscript descriptions and generated outputs agree from a clean extraction. Rebuild the final source and inspect the changed pages.

### Strongly recommended

Move the resource map earlier, provide a worked chain-ring example, expand the residue-support step and the role of primitive resources, and reduce the Boolean appendix. These changes improve reviewer resilience without lengthening the paper through unrelated research.

### Optional future research

Restricted-setting witness complexity, restricted encoder groups, non-chain rings, and process-theoretic closure are real research directions. They should not be silently added to the current submission requirements. A new theorem in those directions could justify a subsequent article, but its absence does not invalidate the present classification.

### Does this manuscript need additional mathematics?

**No major new theorem is shown to be necessary by this audit.** The current core has reconstructed proofs. A localized replacement justification and explicit typing/edge-case exposition are needed. The peripheral restricted-construction assertion needs a derivation only if the author insists on retaining it; deleting it is a valid repair. Historical priority still needs a more careful comparison, but that is not the same as demanding further mathematical scope.

The most valuable immediate operation is a controlled repair pass against the issue register, followed by a clean-package verification. Do not expand the article merely to raise a significance score.

## 16. Audience and venue positioning

The natural primary audience is **algebraic quantum foundations / contextuality with finite-ring methods**, with secondary interest from finite geometry and coding theory. This is a positioning judgment about the audited content, not a claim about any particular journal's current editorial policy.

For a foundations audience, explain the setting/outcome model, primitive-state distinction and operational contracts first; make clear that no probability model or physical realization is asserted. For an algebra audience, foreground the invariant classification and distinguish it from classical Smith/module results. For an information-theory audience, specify the exact decoder task and compare it directly with finite-chain-ring matrix channels instead of using the word capacity loosely.

The current manuscript is less naturally a broad mathematical-physics or general quantum-computing article because it deliberately omits dynamics, probabilities and complexity advantage. No journal-specific acceptance odds, prestige ranking or current-scope verification is supplied. Select a specific venue after the contribution and supplement are finalized.

## 17. Primary references and inspection notes

The identifiers below support the literature comparisons in this report. They are not a claim to have read every page of every cited source. PDF passages used for mathematical comparisons were rendered/screenshot-inspected; primary metadata records were used for dates and publication details. No long quotations are reproduced.

**[S1] Benjamin Schumacher and Michael D. Westmoreland.** *Modal quantum theory*. arXiv:1010.2929, submitted 2010, version 2 (2011); published in *Foundations of Physics* 42, 918-925 (2012), DOI `10.1007/s10701-012-9650-z`. Primary record: https://arxiv.org/abs/1010.2929. Inspected finite-field definitions and the dense-coding/teleportation discussion near the end of the paper; PDF page 9 was visually checked. This is not *Almost quantum theory*.

**[S2] Benjamin Schumacher and Michael D. Westmoreland.** *Non-contextuality and free will in modal quantum theory*. arXiv:1010.5452 (2010). https://arxiv.org/abs/1010.5452. Inspected modal noncontextuality and bipartite nonlocality arguments; the paper is not exclusively a single-system KS result.

**[S3] Samson Abramsky and Adam Brandenburger.** *The Sheaf-Theoretic Structure of Non-Locality and Contextuality*. *New Journal of Physics* 13, 113036 (2011), DOI `10.1088/1367-2630/13/11/113036`; arXiv:1102.0264v7. https://arxiv.org/abs/1102.0264. Inspected the support/global-section hierarchy, including Section 6.

**[S4] Niel de Beaudrap.** *On computation with 'probabilities' modulo k*. arXiv:1405.7381 (2014). https://arxiv.org/abs/1405.7381. Inspected the ring-valued model and Definition 7, especially coordinate generation of the unit ideal. This is the basis for the primitive-state comparison.

**[S5] Thomas Honold and Ivan Landjev.** *Linear Codes over Finite Chain Rings*. *Electronic Journal of Combinatorics* 7, R11 (2000), DOI `10.37236/1489`. Primary journal mirror: https://www.maths.tcd.ie/EMIS/journals/EJC/Volume_7/PDF/v7i1r11.pdf. Inspected Section 2, including module structure and basis results, and the code/geometry setup. The issue year is 2000; the publisher also exposes a late-1999 online date. The manuscript's Honold 2009 lecture source was also inspected in selected relevant portions, not all 116 pages: https://www.geometrie.tuwien.ac.at/zif-cg09/pdf/lecture_honold.pdf.

**[S6] Eimear Byrne, Anna-Lena Horlemann, Karan Khathuria and Violetta Weger.** *Density of Free Modules over Finite Chain Rings*. arXiv:2106.09403v2 (2022; first preprint 2021). https://arxiv.org/abs/2106.09403. Inspected module-structure/counting background and the primary record. This source is not an identified proof of P01's operational theorems.

**[S7] Feroz Siddique and Ashish K. Srivastava.** *Decomposing elements of a right self-injective ring*. arXiv:1211.5383 (2012). https://arxiv.org/abs/1211.5383. The primary research record explicitly identifies the Wolfson/Zelinsky nonsingular-summand theorem and its one-dimensional binary exception. Historical antecedent: Daniel Zelinsky, *Every linear transformation is a sum of nonsingular ones*, *Proceedings of the AMS* 5, 627-630 (1954), DOI `10.1090/S0002-9939-1954-0062728-7`. The original publisher PDF was not accessible during this audit; its full proof was not independently read here.

**[S8] Melvin Henriksen.** *Two Classes of Rings Generated by Their Units*. *Journal of Algebra* 31(1), 182-193 (1974), DOI `10.1016/0021-8693(74)90013-1`. Primary author repository: https://scholarship.claremont.edu/hmc_fac_pub/45/. Inspected the author's deposited abstract and bibliographic record, which explicitly state the stronger sum-of-three-units result for matrix size greater than one. The complete article proof was not accessed.

**[S9] Matthew Varughese.** *Categorical Quantum Computing with Finite Fields*. MSc thesis, University of Oxford (2009). https://www.cs.ox.ac.uk/people/aleks.kissinger/theses/bob/Varughese.pdf. Inspected and visually checked Examples 8.3-8.4, printed pages 50-51. These are protocol precedents under a different categorical setup.

**[S10] Koen Thas.** *General Quantum Theory*. arXiv:1712.04669 (2017). https://arxiv.org/abs/1712.04669. Inspected the division-ring/involution setting and Section 14 on protocols, including the characteristic-two discussion. This is not a full re-audit of that paper's proofs.

**[S11] Dominic Verdon.** *Entanglement-invertible channels*. *Journal of Mathematical Physics* 65, 062203 (2024), DOI `10.1063/5.0159504`; arXiv:2204.04493v4. https://arxiv.org/abs/2204.04493. Inspected the primary record and framework/results on entanglement-invertibility and teleportation correspondences. Its operator-algebraic assumptions differ from P01's finite-ring raw-vector task.

**[S12] Chen Feng, Roberto W. Nobrega, Frank R. Kschischang and Danilo Silva.** *Communication over Finite-Chain-Ring Matrix Channels*. arXiv:1304.2523v2 (2014; first preprint 2013), DOI `10.1109/TIT.2014.2346079`. https://arxiv.org/abs/1304.2523. Inspected the channel definition and capacity setting, including Section VII. The stochastic transfer/noise assumptions are material to the comparison.

**[S13] Michael Ben-Zvi, Alexander Ma and Manuel Reyes, with an appendix by Alexandru Chirvasitu.** *A Kochen-Specker theorem for integer matrices and noncommutative spectrum functors*. arXiv:1509.03618v3 (2017; first preprint 2015). https://arxiv.org/abs/1509.03618. Inspected the matrix/idempotent KS framework and principal theorem statements. P01 already cites this relevant but different contextuality setting.

**[S14] Ida Cortez, Camilo Morales and Manuel Reyes.** *Minimal ring extensions of the integers exhibiting Kochen-Specker contextuality*. arXiv:2211.13216v4 (2025; first preprint 2022). https://arxiv.org/abs/2211.13216. Inspected the primary record and relevant partial-ring theorem statements. No claim is made that this supplies the complete-basis resource classification.

**[S15] Benjamin Schumacher and Michael D. Westmoreland.** *Almost quantum theory*. arXiv:1204.0701 (2012). https://arxiv.org/abs/1204.0701. Inspected the model/process discussion and probability-resolution material, including the late-paper comparison of resolutions. This supports the distinction between a static support model and a richer modal process theory.

## 18. Audit artifacts and verification boundaries

`P01_CLAIM_BY_CLAIM_AUDIT.csv` has 18 rows. `P01_PUBLICATION_BLOCKERS.md` has the complete nine-record issue register. `P01_SCORECARD.json` records the 19 scores, eight gates and verdict counts. `p01_independent_checks.py` regenerates the new finite checks without the author's missing dependencies.

The bundled evidence directory includes the archive inventory, manifest checks, failed original-run log, clean-build logs, text comparison, support results, exact analyzer/coding certificates, Smith inventory and supplementary preservation checks. The literature-search notes record representative actual queries and inspected sources, not a fictitious exhaustive query history.

The original manuscript was not edited. The fresh PDF was a build-verification artifact, not a revised manuscript. No report here certifies unobserved historical runs, absent portfolio files, exhaustive higher-dimensional search, formal proof checking, or definitive historical novelty.

## 19. Final publication-readiness determination

**Current strongest contribution:** A complete chain-ring support-contextuality classification, combined with an exact orbit-codebook formula under the same explicit algebraic resource setting, and a comparison with raw-vector teleportation. The distinction between nonzero Smith rank, leading multiplicity and invertibility is the central conceptual result. The nonprimitive separator is a useful consequence once state admissibility is made explicit.

**Mathematical correctness:** Principal results survive independent reconstruction and bounded direct checks. No central false theorem or unresolved central proof gap identified. A localized symbolic justification and a peripheral unsupported sentence need repair/removal.

**Novelty confidence:** Moderate for the full classification and matched-contract comparison; established background for several ingredients; historical priority unresolved. No firstness certification.

**Principal publication risk:** The submitted evidence package is not self-contained, and contribution positioning is less mature than the mathematics. These are actionable major issues, not reasons to abandon the article.

**Preprint readiness:** **READY AFTER SPECIFIC MAJOR CORRECTIONS.**

**Journal-submission readiness:** **MAJOR REVISION BEFORE SUBMISSION.**

**Number of P0 blockers:** **0 identified.**

**Number of P1 major issues:** **2.**

**Number of P2 localized issues/recommendations:** **7.**

**Most important next action:** Produce a self-contained, truthfully described reproduction supplement and reconcile Section 6 against a clean-directory run, while keeping the mathematical source unchanged until the listed repair pass is applied.

**Senior-author decision:** Provisionally freeze the scope and principal theorem set, not the release. Enter a bounded repair-and-positioning phase rather than continuing open-ended theorem expansion. The evidence does not justify submitting the present package unchanged, but it also does not establish a need for fundamental mathematical rework. Final submission preparation should follow closure of the two P1 issues and the essential localized corrections.
