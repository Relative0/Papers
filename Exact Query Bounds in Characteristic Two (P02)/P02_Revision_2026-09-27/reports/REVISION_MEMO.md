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
