# CM adversarial research review

Review date: 18 September 2026.

## Start here

`COMPLETE_RESEARCH_DOSSIER.md` combines the research report, the full nine-column novelty matrix, annotated bibliography, and search-scope statement. It is the best single file to give to another researcher or model. `SEARCH_LOG.csv` is the accompanying detailed query record.

The principal conclusion is a candidate general classification theorem for bilinear support models over finite commutative chain rings. The CM rotation algebra and most individual diagnostics are classical or elementary. Candidate priority is explicitly bounded; the proofs are research arguments, not proof-assistant or referee certification.

## Files

| File or directory | Purpose |
|---|---|
| `RESEARCH_REPORT.md` | Deliverables A-M, with proofs, scope boundaries, publication architecture, applications and final synthesis |
| `FORMAL_THEOREMS.md` | Extracted definitions and corrected theorem/proof set |
| `PAPER_BLUEPRINT_AND_RELATED_WORK.md` | Extracted paper plan, contribution paragraph, related-work draft and safe-claim table |
| `NOVELTY_MATRIX.csv` and `.md` | All T1-T15 in the nine requested columns |
| `ANNOTATED_BIBLIOGRAPHY.md` and `BIBLIOGRAPHY.json` | 46 annotated records, with identifiers and explicit access qualifications |
| `SEARCH_LOG.csv` | 89 actual query strings and 16 important primary-source follow-ups |
| `SEARCH_SCOPE.md` | What the search does and does not establish |
| `checks/` | New independent verification code, exact outputs and timings |
| `reproduction/` | Successful supplied-audit rerun status, logs and regenerated data |
| `source_audit/input_hash_audit.json` | Verification of all 176 manifest-listed input paths |
| `reproduce_supplied.py` | Portable helper to rerun the original corrected audit |
| `OUTPUT_MANIFEST_SHA256.txt` | Hashes of final deliverable files, excluding the manifest itself |

## Reproduce the new checks

The new scripts require Python 3 and NumPy. They were run with Python 3.13.5 and NumPy 2.3.5. They do not import code from the supplied archive.

```text
python checks/independent_extensions.py
python checks/additional_boundaries.py
```

Running them regenerates JSON files next to the scripts, including new runtime values. Preserve the delivered files before rerunning if byte-for-byte evidence preservation matters.

The main campaign checks 22 ring/dimension cases, 65,812 Boolean functions, and all binary matrices through dimension four for the orthogonal span. The additional run verifies form-preserving group counts and two unimodular equal-rank examples. Higher-dimensional existence checks rely on the hyperplane lemma proved in the report; they are not independent tests of that lemma.

## Reproduce the supplied baseline

Unpack the original user-supplied archive. Locate its authoritative `02_FINAL_AUDIT/CM_Final_Audit` directory. Work on a fresh copy: the audit scripts regenerate their own tables. Install that directory's requirements, then run:

```text
python reproduce_supplied.py "PATH/TO/02_FINAL_AUDIT/CM_Final_Audit"
```

The delivered baseline was run with Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and pytest 9.0.2. All 31 independent and 59 historical tests passed. The original source ZIP is not duplicated in this output bundle; it remains the source of the baseline implementation. The new checks are self-contained within this bundle.

## Important boundaries

Paper B, the original CM manuscript and the older phase paper were not bundled in the source ZIP. Relevant File Library excerpts were consulted; a full byte-level or exhaustive rereading of those separate manuscripts is not claimed. The corrected audit PDF/code/data were available directly and were inspected and rerun.

The exact nine-page Bricken matrix-techniques note was listed in an author index but not recovered. Some historical sources were checked through metadata or later primary citations rather than complete original texts. These gaps are named in the bibliography and report.

The complete-basis theorem uses an explicit support model, not a physical quantum theory or a proven closed sequential process theory. Same-rank equivalence under larger field-linear groups does not preserve the restricted measurement contract automatically. The particular archived shared and literal restricted bipartite tables agree up to an involution relabeling.
