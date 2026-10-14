---
title: "P02 Revision, Novelty, and Evidence Report"
subtitle: "Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation"
author: "Publication-readiness revision package"
date: "27 September 2026"
geometry: margin=1in
fontsize: 10pt
---

This report documents the 27 September 2026 revision of P02. It is a revision record and evidence/positioning assessment, not independent human peer review or a claim of historical priority.

\newpage
# Revision memo
## From `Exact Query Bounds in Characteristic-Two Modal Computation` to `Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation`

**Revision date:** 27 September 2026

## Purpose of this revision

The revision addresses the weakest parts of the publication-readiness audit: novelty/priority positioning, reproducibility, scientific significance, literature coverage, evidence quality, scope/focus, exposition, and submission hygiene.

The mathematics was not rebuilt from scratch because the prior audit found the core proofs sound. The revision instead makes the strongest theorem unmistakably central and repairs the evidence and positioning around it.

## Major manuscript changes

### 1. BV is now the headline theorem

The title was changed to:

> **Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation**  
> *Adaptive complete readout, oracle contracts, and related obstructions*

The abstract now leads with the exact BV theorem rather than presenting Deutsch, DJ, BV, and ring kickback at equal weight.

The BV section now appears before Deutsch/DJ and is explicitly labeled **Main result**.

### 2. Stronger theorem statement

The main theorem now explicitly states:

- any field of characteristic two;
- finite adaptive algorithms;
- arbitrary finite ancillas;
- complete recorded instruments;
- pointwise invertible actions fixed independently of the secret at each recorded query node;
- lower bound `q >= n`;
- matching QXOR upper bound `n`.

This eliminates ambiguity about which access model supplies the lower bound and which supplies the matching upper bound.

### 3. Added a complete two-bit worked example

For `n=2, q=1`, the recorded state has form

`Psi_s = c_empty + s_1 c_1 + s_2 c_2`.

Summing all four secret records gives zero in characteristic two, contradicting the linear independence required by exact recovery. This lets a reader see the obstruction before the general dimension count.

### 4. Added an alternative point-indicator proof

A nonzero coordinate in one output-label block is zero on every other secret. Its multilinear polynomial is therefore a scalar multiple of the Boolean point indicator

`prod_{s*_j=1} s_j prod_{s*_j=0} (1+s_j)`,

which has degree `n`. Since query degree is at most `q`, `q >= n`.

This is presented as a cross-check, not as a new general polynomial method.

### 5. Prior-art discussion substantially expanded

The revision now directly compares the theorem with:

- Beals et al. - polynomial method;
- Farhi et al. - binomial function-identification bound;
- Combarro et al. - one-query exact Boolean promise problems;
- Copeland--Pommersheim - oracle identification;
- Montanaro - finite-field-valued polynomial learning in ordinary quantum theory;
- Svozil 2026 - explicit oracle/access-model dependence and Deutsch response-unitary criterion;
- Schumacher--Westmoreland, James--Ortiz--Sabry, Diamond--Schumacher, and Willcock--Sabry - modal antecedents.

The manuscript explicitly says that the general access-model message is **not** a novelty claim.

### 6. Contribution language narrowed

The new publication-safe positioning is:

> A targeted comparison has not located a prior theorem with the full combination of characteristic-two amplitudes, exact BV secret recovery, arbitrary finite ancillas, finite adaptive complete recorded instruments, and the stated pointwise lower-bound interface. This supports treating the theorem as differentiated, but does not certify historical firstness.

The manuscript does not use “first” for the result.

### 7. Deutsch/DJ demoted to related obstructions

Deutsch and Deutsch--Jozsa now follow the BV theorem. The text explicitly credits:

- the qualitative Deutsch antecedent; and
- Svozil's modern access-model framing.

The DJ result remains only a **one-query obstruction**; no matching optimum is asserted.

### 8. Ring material moved to an appendix

The kickback section is retained because it explains a useful phase/readout boundary, but it no longer competes with BV for the paper's center of gravity.

The primitive-eigenvector wording was repaired. The revision explicitly notes the nonprimitive example

`eta = (u^2, u^2+u^3)^T`

with `X eta = R eta`, while proving that no **primitive** eigenvector can have eigenvalue `R`.

The compute--control--uncompute discussion was also narrowed: the two-QXOR charge is stated for that generic clean construction, not as a universal implementation lower bound.

### 9. Computational checks moved into a bounded-evidence appendix

The finite evidence table now states exact scopes. In particular, the 552 count is described as a bounded enumeration of degenerate oracle matrices for `n=1,2,3` with two shared target permutations, and explicitly not as an enumeration of all algorithms.

### 10. Reproducibility repaired

The new attachments recovered the original portfolio reproduction supplement. The revision package now includes:

- recovered original P02 outputs and provenance;
- recovered completed full-run manifest/log;
- a new P02-targeted rerun driver;
- fresh rerun outputs and hashes;
- original-vs-fresh semantic comparison;
- a new deterministic phase-table generator;
- current table provenance.

The missing historical `complete_p02.py` remains missing and is not falsely represented as recovered.

### 11. Submission hygiene improved

The inherited internal author footnote was removed. PDF metadata now identifies the author as `Brian Theory`, consistent with the existing manuscript label.

Before external submission, the author should still confirm the exact public author name, affiliation, email, ORCID (if any), acknowledgements, and target-venue formatting. Those details were not invented in this revision.

## Material intentionally not added

The prior audit derived a broader exact-identification rank characterization for a finite promise family. It remains in `RESEARCH_EXTENSION_CANDIDATE.md` and is **not** inserted into the manuscript because its theorem-level prior art has not been audited to the same standard. Keeping it separate protects the focus of the current paper.

Likewise, no attempt was made to manufacture a full DJ optimum or a general Simon theorem merely to make the paper larger.

\newpage

# Novelty and positioning report
## Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation

**Date:** 27 September 2026  
**Purpose:** Narrow the contribution to what the available evidence supports, identify the closest antecedents, and specify publication-safe novelty language.

## Executive conclusion

The paper should **not** claim novelty for any of the following broad ideas:

- modal quantum theory or finite-field amplitudes;
- exact distinguishability via linear independence/direct-sum structure;
- polynomial/degree-per-query lower bounds;
- oracle-identification dimension bounds;
- the fact that query complexity depends on the oracle/access interface;
- the qualitative failure of the standard Deutsch advantage over characteristic two;
- one-query modal UNIQUE-SAT;
- the ordinary complex-amplitude Bernstein--Vazirani algorithm.

The strongest differentiated theorem is narrower:

> **Characteristic-two exact BV theorem.** For any field of characteristic two, any finite adaptive algorithm satisfying the paper's complete recorded modal-readout contract, with arbitrary finite ancillas and pointwise invertible oracle actions fixed independently of the secret at each recorded query node, requires at least `n` queries to recover every `n`-bit Bernstein--Vazirani secret. Standard QXOR attains the bound with `n` queries.

After targeted searches and direct comparison with the closest sources listed below, I did **not** locate a prior theorem with this full combination of scalar domain, access class, finite adaptivity, complete modal readout, arbitrary finite ancillas, and exact `n`-query conclusion. That supports describing the theorem as a **differentiated exact specialization**. It does **not** prove historical firstness. The revised manuscript therefore uses “to our knowledge, a targeted comparison has not located...” rather than “first” or “novel.”

The one-query characteristic-two Deutsch--Jozsa obstruction also appears differentiated in the same targeted search, but its priority is less important to the paper and remains less certain. It should remain a secondary result.

## Claim-by-claim novelty classification

| Claim | Publication-safe classification | Why |
|---|---|---|
| Modal linear computation over characteristic-two fields | **Known background** | Schumacher--Westmoreland establish modal quantum theory over general fields. |
| Complete instrument / trivial common-kernel requirement | **Known antecedent** | `Almost quantum theory` gives the unconditional-operation common-kernel condition. |
| Exact modal discrimination from linear independence/direct sums | **Known principle / elementary label-span extension** | Diamond--Schumacher explicitly discuss distinguishability of linearly independent modal states. |
| Degree grows by at most one per oracle query | **Known architecture, specialized implementation** | Beals et al. establish the polynomial method; Farhi et al. give a closely related function-identification dimension bound. The paper's new work is the characteristic-two secret-bit specialization and recorded adaptive modal implementation, not the general technique. |
| Query complexity depends on oracle access | **Known** | Karl Svozil's 2026 preprint explicitly frames exact query complexity by answer partition plus oracle access and proves response-unitary dependence for Deutsch in the ordinary complex-unitary model. |
| Qualitative failure of the usual Deutsch speedup over `F_2` | **Known** | James--Ortiz--Sabry state the qualitative failure. |
| Exact Deutsch lower bound under the paper's full pointwise/adaptive modal contract | **Rigorous contract-level refinement** | Stronger quantified statement than circuit failure, but should not be the headline novelty. |
| One-query DJ obstruction under the same characteristic-two contract | **Apparently differentiated; priority not certified** | No equivalent theorem located in targeted search; only the one-query obstruction is proved. |
| Exact BV lower bound `q >= n` under finite adaptive complete modal readout, arbitrary finite ancillas, broader pointwise lower-bound interface | **Strongest apparently differentiated theorem** | Closest polynomial/oracle-identification antecedents use standard complex amplitudes and different variables/readout. No matching characteristic-two theorem located. |
| QXOR upper bound `n` for BV | **Elementary matching upper bound** | Querying unit vectors is straightforward; significance comes from matching the lower bound. |
| Ring-valued kickback with singular analyzer and rank `4+2n` | **Model-specific algebraic boundary / illustrative result** | Correct and useful, but elementary relative to the main exact-query theorem; not the paper's central novelty. |
| Modal UNIQUE-SAT positive control | **Known reproduced result** | Willcock--Sabry. |
| Small Simon scan / description-readout ablation | **Finite evidence only** | No general theorem or novelty claim should be attached. |

## Closest prior art and exact overlap

### 1. Beals et al. (2001) - polynomial method

**Source:** Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, Ronald de Wolf, *Quantum Lower Bounds by Polynomials*, JACM 48(4), 778--797. DOI: https://doi.org/10.1145/502090.502097  
Preprint: https://arxiv.org/abs/quant-ph/9802049

**Overlap:** Query amplitudes can be represented by low-degree polynomials in oracle variables, with degree increasing in a controlled way per query.

**Difference:** Their setting is ordinary complex-amplitude quantum computation and standard black-box variables. P02 uses characteristic-two amplitudes, exact all-branches modal readout, and the BV promise to express each pointwise oracle call as affine degree one in the `n` secret bits themselves.

**Effect on novelty:** Do not claim a new polynomial method. Claim the characteristic-two specialization and adaptive modal theorem.

### 2. Farhi, Goldstone, Gutmann, Sipser (1999) - function-identification dimension bound

**Source:** *Bound on the number of functions that can be distinguished with k quantum queries*, Physical Review A 60, 4331--4333. DOI: https://doi.org/10.1103/PhysRevA.60.4331  
Preprint: https://arxiv.org/abs/quant-ph/9901012

**Overlap:** If a standard complex quantum algorithm distinguishes a family of Boolean functions with `k` queries, the number distinguishable is bounded by a binomial sum. This is structurally very close to P02's coefficient-span count.

**Difference:** Farhi et al. parameterize polynomials by the truth-table entries over an address set of size `N`. For BV, that bound does not rule out the standard one-query quantum algorithm. P02 exploits the characteristic-two identity `f_s(x)=sum_j s_j x_j` inside the amplitude field, collapsing the oracle dependence to only `n` secret variables and producing `sum_{j<=q} C(n,j)`.

**Effect on novelty:** This source should be cited prominently as a closest methodological antecedent. The revised paper now does so.

### 3. Combarro et al. (2021) - exact one-query promise problems

**Source:** Elías F. Combarro et al., *On a poset of quantum exact promise problems*, Quantum Information Processing 20, 214 (2021). DOI: https://doi.org/10.1007/s11128-021-03156-3

**Overlap:** Standard complex exact one-query promise problems include Deutsch--Jozsa and Bernstein--Vazirani and are studied in a common framework.

**Difference:** Ordinary Hilbert-space amplitudes and measurement; their one-query BV result is the familiar complex-amplitude result, not a characteristic-two modal theorem.

### 4. Copeland and Pommersheim (2021) - oracle identification

**Source:** Daniel Copeland and Jamie Pommersheim, *Quantum query complexity of symmetric oracle problems*, Quantum 5, 403 (2021). DOI: https://doi.org/10.22331/q-2021-03-07-403

**Overlap:** General exact/probabilistic oracle-identification questions and group-character methods.

**Difference:** Complex unitary oracle groups and character theory; not the characteristic-two complete-modal-readout contract.

### 5. Montanaro (2012) - finite-field-valued functions

**Source:** Ashley Montanaro, *The quantum query complexity of learning multilinear polynomials*, Information Processing Letters 112(11), 438--442 (2012). DOI: https://doi.org/10.1016/j.ipl.2012.03.002

**Overlap:** Exact quantum learning of unknown polynomials over finite fields, including `q=2` Reed--Muller structure.

**Difference:** The unknown function's algebra is over a finite field, but the quantum amplitudes and measurement theory remain ordinary complex quantum mechanics. This is not a finite-field-amplitude/modal result.

### 6. Svozil (2026) - access-model dependence

**Source:** Karl Svozil, *Answer Partitions and Oracle Access Determine Quantum Query Complexity*, arXiv:2605.12675v4. https://arxiv.org/abs/2605.12675

**Overlap:** Very important contemporary antecedent. It explicitly says that an answer partition does not determine exact query complexity without its access model. For Deutsch, a controlled response unitary admits a one-query exact solution iff the response unitary has the needed `-1` eigenvalue; alternative response dimensions can raise the exact cost.

**Difference:** Ordinary complex-unitary quantum theory, Hilbert-space block discrimination, and response-unitary spectra. It does not supply the characteristic-two adaptive BV theorem or the modal complete-instrument proof.

**Effect on novelty:** The broad “oracle choice matters” rhetoric is no longer defensible as a contribution. The revised manuscript explicitly treats it as background and cites Svozil.

### 7. Modal antecedents

- Benjamin Schumacher and Michael Westmoreland, *Modal Quantum Theory*, Foundations of Physics 42 (2012), 918--925. https://doi.org/10.1007/s10701-012-9650-z
- Benjamin Schumacher and Michael Westmoreland, *Almost quantum theory*. https://arxiv.org/abs/1204.0701
- Roshan P. James, Gerardo Ortiz, Amr Sabry, *Quantum Computing over Finite Fields: Reversible Relational Programming with Exclusive Disjunctions*. https://arxiv.org/abs/1101.3764
- Jeremiah Willcock and Amr Sabry, *Solving UNIQUE-SAT in a Modal Quantum Theory*. https://arxiv.org/abs/1102.3587
- Phillip Diamond and Benjamin Schumacher, *Cloning, deleting, and hiding in modal quantum theory*. https://arxiv.org/abs/2310.04397

These sources delimit the model background, qualitative Deutsch antecedent, positive modal algorithm, and distinguishability principle. None was found to contain the fully quantified P02 BV theorem.

## Searches performed

Targeted searches included combinations and synonyms of:

- `Bernstein-Vazirani modal quantum theory`
- `Bernstein Vazirani characteristic two amplitudes query`
- `Bernstein-Vazirani finite-field quantum computing`
- `adaptive Bernstein-Vazirani query lower bound modal`
- `Deutsch-Jozsa characteristic-two modal quantum`
- `finite field quantum amplitudes Bernstein Vazirani query complexity`
- `exact oracle identification polynomial dimension query`
- `answer partitions oracle access query complexity`
- citation chaining from Beals, Farhi, Combarro, Copeland--Pommersheim, Montanaro, Schumacher--Westmoreland, James--Ortiz--Sabry, and Svozil.

No search result by itself proves absence. The correct conclusion remains “no equivalent theorem located in the targeted search,” not “the theorem is the first.”

## Recommended novelty wording

### Safe abstract/introduction wording

> The general polynomial method and the dependence of exact query complexity on oracle access have substantial prior antecedents. The contribution here is narrower: an exact characteristic-two Bernstein--Vazirani lower bound that remains valid for arbitrary finite ancillas and finite adaptive complete recorded modal readout under the stated pointwise access contract.

### Safe priority wording

> To our knowledge, a targeted comparison with the closest modal, polynomial-method, and exact oracle-identification literature has not located a prior theorem with this full combination of scalar domain, access class, adaptivity/readout model, and exact conclusion. We do not claim historical firstness.

### Wording to avoid

- “first proof that oracle choice matters”
- “new polynomial method”
- “first finite-field Bernstein--Vazirani result” without qualification
- “Deutsch fails in characteristic two” as a new observation
- “Deutsch--Jozsa exact complexity is 2” (not proved)
- any claim that the finite Simon scan establishes a general lower bound

## Publication positioning

The paper is strongest as a **focused exact-query technical note/research article** centered on Theorem 3.2 in the revised manuscript. The revised title and abstract now make BV the headline, move Deutsch/DJ to related obstructions, place the ring calculation in an appendix, and make the novelty boundary explicit.

\newpage

# Evidence recovery and reproducibility report
## P02 revision - 27 September 2026

## What the new attachments recovered

The newly supplied publication archives contain the portfolio-level `REPRODUCTION_SUPPLEMENT.zip` that was absent from the earlier standalone P02 ZIP. This materially changes the previous reproducibility assessment.

Recovered evidence includes:

- the canonical `reproduce.py` driver;
- pinned requirements;
- `REPRODUCTION_ENVELOPE.json` with environment and provenance;
- a completed Linux full-run manifest and log;
- the original P02 manuscript/provenance record;
- the P02 table provenance record;
- the original oracle-contract checker and output;
- original `new_algorithm_checks.json`;
- original `new_phase_fourier.json`;
- original `small_simon.json`;
- original `description_readout_ablation.json`;
- original `unique_sat_reproduction.csv`.

The recovered pinned environment is:

- Python 3.13.5
- NumPy 2.3.5
- SciPy 1.17.0
- SymPy 1.14.0
- pytest 9.0.2

The current execution environment matches those pinned package versions.

## Fresh P02-targeted rerun

A new targeted driver, `supplement/P02_TARGETED_RERUN_2026-09-27/reproduce_p02.py`, was created to make the P02 evidence portable without requiring the whole portfolio research tree.

It reruns:

1. the recovered oracle-contract checker;
2. the independent P02 publication-audit verifier;
3. all five recovered capability stages;
4. deterministic regeneration of the phase table from the fresh phase JSON.

The fresh run passed all four top-level stages. The generated `P02_RERUN_MANIFEST.json` records Python/platform data, stage times, output paths, file sizes, and SHA-256 hashes.

## Original-vs-fresh comparison

`SEMANTIC_COMPARISON.json` compares the recovered historical outputs with the fresh rerun.

The following JSON files are semantically identical after parsing:

- `oracle_contract_check.json`
- `new_algorithm_checks.json`
- `new_phase_fourier.json`
- `small_simon.json`
- `description_readout_ablation.json`

`unique_sat_reproduction.csv` is byte-for-byte identical.

Several JSON byte hashes differ even though parsed content is identical. The difference is serialization/line-ending level and is therefore recorded rather than hidden.

## The 552 count is now properly scoped

The recovered original checker establishes exactly what the manuscript's `552` number means:

- address-bit sizes `n = 1, 2, 3`;
- two shared target permutations;
- the degenerate interface `G_0 = G_1`;
- all corresponding Boolean truth tables in those bounded domains.

The original JSON explicitly says this is **not an enumeration of all algorithms**. The analytic unbounded observation is simply that `G_0=G_1` makes every oracle operator identical. The revised manuscript now states this scope directly.

## Historical table-generator gap and repair

The old P02 provenance refers to a historical script `complete_p02.py`. That script was **not located** in the supplied archives, even though the generated `phase_table.tex`, the source JSON, provenance record, and wider reproduction supplement were recovered.

This gap is repaired transparently rather than papered over:

- the old provenance is preserved as `original_evidence/TABLE_PROVENANCE_HISTORICAL.json`;
- a new deterministic `generate_phase_table.py` reads the package-local `new_phase_fourier.json` and regenerates `phase_table.tex`;
- the revised manuscript's `TABLE_PROVENANCE.json` records the new generator hash, input hash, output hash, fresh rerun manifest, and pointer to the historical provenance;
- the new generator explicitly says it is a reconstruction, not the missing historical script.

## Full portfolio run versus targeted rerun

The recovered supplement contains a previously completed Linux full-run manifest in which all recorded stages passed. During this revision session, the monolithic historical runner was started but exceeded the single-command execution window during a later historical stage after the independent, oracle-contract, and audit-test stages had already passed.

Rather than represent that interrupted attempt as a completed fresh full rerun, the final package distinguishes:

- **historical completed full-run evidence** (recovered manifest/log), and
- **fresh completed P02-targeted evidence** (new rerun manifest/logs).

This separation is more defensible than treating either one as the other.

## Reproducibility conclusion

The earlier score of 4.5/10 was driven mainly by a packaging failure: the standalone P02 archive referred to evidence that was not included. The new attachments recover most of that evidence, and the revision adds a self-contained P02 driver plus a transparent replacement for the missing table generator.

For the revised P02 package, reproducibility is now assessed at approximately **9.2/10**. The remaining limitation is archival rather than mathematical: the original historical `complete_p02.py` has not been recovered, and a completely fresh rerun of every unrelated portfolio stage was not necessary for P02-specific verification.

\newpage

# Updated publication-readiness scorecard
## Post-revision assessment - 27 September 2026

This scorecard evaluates the **revised package**, not the earlier standalone archive. Scores remain editorial judgments, not acceptance probabilities.

| Category | Weight | Prior score | Revised score | Principal change |
|---|---:|---:|---:|---|
| Mathematical correctness | 20% | 9.0 | **9.2** | Core proofs retained; theorem scope made more explicit; ring wording corrected. |
| Completeness of proofs/results | 8% | 8.8 | **9.2** | Added two-bit example and independent point-indicator proof of the BV lower bound. |
| Model and assumption discipline | 8% | 8.8 | **9.4** | Node-wise oracle scope, query-vs-gate count, QXOR matching interface, and limitations are explicit. |
| Novelty and priority | 12% | 6.0 | **7.6** | Closest antecedents are now directly compared; Svozil 2026 narrows broad access novelty; exact BV theorem remains differentiated but firstness unclaimed. |
| Scientific significance | 8% | 6.5 | **8.1** | Paper now centers the sharp reversal: ordinary complex BV uses one query, while exact modal QXOR needs `n` under the stated characteristic-two model. |
| Literature coverage and positioning | 8% | 7.0 | **9.2** | Added Farhi, Combarro, Copeland--Pommersheim, Montanaro, Svozil, published metadata, and explicit overlap/difference table. |
| Reproducibility | 7% | 4.5 | **9.2** | Recovered original 46 MB supplement; fresh P02-targeted rerun; semantic comparison; deterministic table generator; provenance. |
| Internal consistency | 6% | 8.0 | **9.2** | Title, abstract, theorem wording, tables, evidence scope, and appendices now align. |
| Resolution of prior reviewer concerns | 5% | 8.0 | **9.1** | Adaptive proof highlighted; evidence restored; priority language narrowed; lower/upper interfaces separated. |
| Exposition and readability | 5% | 7.2 | **8.8** | Main theorem moved forward; worked `n=2` example; alternative proof; secondary material moved to appendices. |
| Scope and structural focus | 4% | 7.0 | **9.0** | BV is the core; Deutsch/DJ are secondary; ring and finite scans are appendices. |
| Evidence and citation quality | 4% | 6.0 | **9.1** | Claim-level antecedents and executable evidence are now available and scoped. |
| Submission hygiene | 3% | 5.5 | **8.1** | Internal author footnote removed, PDF metadata fixed, references repaired; final public author/affiliation/ORCID still require confirmation. |
| Venue/form fit | 2% | 7.0 | **8.2** | The revised manuscript is now clearly a focused exact-query technical note/research article. |

**Weighted revised score:** **8.85 / 10** (approximately **8.8 / 10**).

The numerical increase does not certify acceptance or priority. The remaining substantive uncertainty is theorem-level historical priority, not mathematical correctness.

## Updated gates

- **Gate A - Mathematical integrity:** **PASS WITH MINOR REPAIRS**  
  No fatal mathematical issue found; final independent human/specialist proof review remains prudent.

- **Gate B - Novelty/priority integrity:** **DIFFERENTIATED BUT PRIORITY WORDING MUST BE CAUTIOUS**  
  The broad access-model and polynomial ideas are known. The exact characteristic-two adaptive BV theorem remains differentiated in the targeted search, but firstness is not certified.

- **Gate C - Evidence/reproducibility:** **PUBLICATION-GRADE FOR THE P02-SPECIFIC PACKAGE**  
  Original evidence was recovered and fresh targeted reruns pass. The missing historical table-generator source is transparently replaced by a new deterministic reconstruction.

- **Gate D - Preprint readiness:** **READY AFTER FINAL METADATA CONFIRMATION**  
  The remaining preprint item is principally author/public metadata and one final proof/citation read-through.

- **Gate E - Peer-reviewed submission readiness:** **READY AFTER TARGETED FINAL REVIEW**  
  Recommended remaining gate: an independent specialist checks the main theorem and closest-prior-art table, followed by venue formatting and confirmed author metadata.

## Remaining blockers

### No fatal blockers identified

### Submission blockers

1. Confirm the exact public author name, affiliation, email, ORCID if desired, acknowledgements, and conflicts/funding statements.
2. Obtain a final independent specialist review of Theorem 3.2 and Lemma 3.1 under exactly the stated adaptive contract.
3. Perform one last theorem-level prior-art check immediately before submission, especially for work appearing in 2026.
4. Format references and manuscript style to the chosen venue.

### Nonblocking research opportunities

- close or improve the DJ multi-query gap;
- audit the broader promise-family evaluation-rank characterization as a separate paper/lemma;
- study realizability versus rank for many-to-one exact classification tasks.
