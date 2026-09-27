# P01 Publication Blockers and Revision Register

Audit date: 26 September 2026. Source: research draft of 19 September 2026.

**0 P0 theorem-level blockers; 2 P1 major issues; 7 P2 localized issues/recommendations.** These counts are issue records, not failed-gate counts. Gate D and Gate G share the same missing-evidence issue.

**Current verdict:** preprint READY AFTER SPECIFIC MAJOR CORRECTIONS; journal MAJOR REVISION BEFORE SUBMISSION.

No source manuscript was modified. A P2 recommendation is not automatically a prerequisite for preprint release.

## P1-01: Reproduction dependencies missing from the submitted archive

**Severity:** P1  
**Location:** Section 6, source_package/REPRODUCIBILITY.md, generate_assets.py:6-7, root REPRODUCIBILITY/README.md

The generator fails on a missing inventory input. The canonical runner, envelope, run manifest, historical suites, and certificates referenced as supplied are outside this ZIP. Hashes of present files do not establish reproducibility of absent files.

**Repair:** Create a self-contained supplement with the actual dependencies and a clean-directory command, or prune/replace the unsupported availability and execution claims. Distinguish direct SAT, invariant-class aggregation, proof-generated tables, and historical checks. Archive the replacement run with source/output hashes.

**Effect on claims:** No theorem change expected. Changes the factual evidence/availability statements.

**Timing:** Essential before preprint and journal submission.

## P1-02: Contribution positioning is not yet a submission-quality theorem comparison

**Severity:** P1  
**Location:** Introduction, Section 4, references.bib, priority ledgers

The core classification looks differentiated, but the paper does not yet give a compact theorem-level comparison with close algebraic and information-theoretic antecedents. Invertibles spanning matrices is classical; the field modal protocols are old; ring matrix-channel coding solves a distinct problem that should be compared rather than ignored.

**Repair:** Add a source-based comparison of domains, admissible resources, settings, encoders, readout, exactness and conclusions. Cite the units literature and appropriate chain-ring coding/geometry sources. Identify the classification and matched-contract comparison as the contribution. Retain bounded-priority language, not historical-firstness assertions.

**Effect on claims:** May change the contribution paragraph and novelty classification; no contradiction of the main theorems found.

**Timing:** Essential before journal submission; add key attribution and conservative claims before preprint.

## P2-01: Symbolic projector proof uses a local-ring property without fixing its domain

**Severity:** P2  
**Location:** Appendix A; main.tex:282

A symbolic invertible matrix over B tensor A need not have a unit entry in each column. The projector conclusion survives, but that justification does not apply at the symbolic level.

**Repair:** State the coefficient ring and replace the argument by B0 J_i psi=P_i B0 psi. Since B0 is invertible, either side is zero exactly when the measured coordinate is zero.

**Effect on claims:** No change to projector theorem. Explicit counterexample to the overbroad intermediate assertion is in the report.

**Timing:** Before either release, if Appendix A is retained.

## P2-02: Joint effect versus reshaped matrix should be typed explicitly

**Severity:** P2  
**Location:** Section 2 task table; Theorem 4.4

Rank-one effect could be misread as a separable/rank-one reshaped d x d matrix, which is not the intended analyzer. The proof permits full-rank reshapes.

**Repair:** Define the effect as a primitive covector e on K^d tensor K^d; define E_ij=e(e_i tensor e_j), then display (T x)_k=sum_ij E_ij x_i M_jk. Distinguish this from a decomposable local effect.

**Effect on claims:** Clarifies existing contract; no change under the intended reading.

**Timing:** Before either release.

## P2-03: A peripheral restricted-model equivalence is not self-contained

**Severity:** P2  
**Location:** Section 5.1; main.tex:212

An audited restricted construction, regular blocks and R-to-R-inverse involution are invoked without enough local definitions or an accessible certificate. This is not used by the core proofs.

**Repair:** Delete the assertion, or supply the exact construction and self-contained derivation/certificate. Do not infer validity from a historical review label.

**Effect on claims:** Removes or supports a peripheral claim only.

**Timing:** Before either release.

## P2-04: A few short proofs need one more explanatory step

**Severity:** P2  
**Location:** Theorem 4.2, Theorem 3.3 and introductory examples

Correct arguments are compressed at residue-support inclusion, dimension of the orbit span, and why extra outcomes do not defeat Hardy forcing. Readers can confuse h with rank of M mod J.

**Repair:** Add the support-inclusion formula used in this report, one leading-layer example such as diag(pi,pi), and a forcing diagram/table. Explicitly distinguish ordinary reduction from division-preimage followed by reduction.

**Effect on claims:** No theorem change.

**Timing:** Strongly recommended before journal submission.

## P2-05: Portfolio-specific appendix obscures the article center

**Severity:** P2  
**Location:** Appendix A, Section 5.1 and Appendix B

The Boolean-interface material is largely standard and belongs to a different explanatory story. The resource map, which does explain this article, appears too late.

**Repair:** Keep classification, coding, teleportation and the two-setting boundary in one paper. Move the resource map forward. Move Appendix A to a companion/supplement, or reduce it to a short optional note.

**Effect on claims:** Scope change only; not a mathematical repair requirement.

**Timing:** Strongly recommended, not a prerequisite for correctness.

## P2-06: Published bibliographic metadata should replace provisional arXiv-only entries

**Severity:** P2  
**Location:** references.bib

Several identifiable published articles are formatted as miscellaneous preprints. A lecture source can be supplemented by the original chain-ring geometry paper. Existing years are not necessarily false but publication metadata is incomplete.

**Repair:** Update verified journal/volume/page/DOI fields; retain arXiv IDs as access links. Distinguish original preprint year from publication year. Check every new source against its primary record.

**Effect on claims:** No theorem change.

**Timing:** Before journal submission.

## P2-07: Submission metadata and several interpretive phrases remain draft-like

**Severity:** P2  
**Location:** Title footnote, abstract, Section 7, historical-versus-current review wording

Author metadata is explicitly provisional. The discussion says nonzero rank permits a logical obstruction, although the actual criterion is at least two nonzero Smith factors. Historical evidence labels should not sound like current independent certification.

**Repair:** Finalize authorship/contact metadata; use r>=2 in that summary sentence; preserve the setting-indexed and raw-vector qualifications in abstract/conclusion; label simulated/internal review as such.

**Effect on claims:** No change to formal theorem statements.

**Timing:** Before journal submission; correct the rank summary before preprint.
