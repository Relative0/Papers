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
