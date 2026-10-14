# Boolean CM Phase Algebra - revised research package

Prepared for Brian Droncheff, 28 September 2026.

## Decision and canonical files

**Retain as a focused technical companion.** The core algebra and the declared finite checks pass this audit. The revised work does not establish a new quantum theory, a new coding-theory lower bound, or a practical speedup. A substantial standalone original-research submission is not recommended on the present novelty/significance evidence. Author review and actual venue/form decisions remain open.

- `manuscript/CM_Phase_Algebra_Revised.tex`: canonical revised manuscript; standalone source with embedded bibliography.
- `manuscript/CM_Phase_Algebra_Revised.pdf`: 14-page compiled manuscript.
- `audit/Theory_Audit_and_Review.pdf`: 12-page theory audit, seven review perspectives, overlap analysis, scorecard, and decision.
- `audit/Theory_Audit_and_Review.md`: editable audit report.
- `audit/Claim_Crosswalk.md` and `.json`: all 13 original formal-result environments, plus examples and new additions.
- `audit/Manuscript_Changes.diff`: whole-document original-to-revised diff; this is a substantial rewrite, not a minimal patch.
- `audit/readiness_scorecard.json`: all supplied weights, original/revised scores, confidence, and findings.

The weighted assessment is 7.146/10 for the original and 8.222/10 for the revision **as a technical companion**. A numerical average does not override the original-research contribution gate. The scores are judgments, not acceptance probabilities.

## Main mathematical changes

The native binary representation is identified exactly with the rotation centralizer. The detector contract is explicit and its width is closed by an optimal construction plus the classical Enomoto--Frankl--Ito--Nomura forbidden-weight theorem. The shared square-zero obstruction is characterized precisely by preservation of the tag ideal, with a reversible binary counterexample outside that class. A complete two-branch unitary normal form proves the involution counts analytically. The standard Boolean Mobius transform and all readout/tensor distinctions are credited and scoped.

## Reproduce the calculations

The inherited inventory requires NumPy. This package was executed with Python 3.13.5 and NumPy 2.3.5; the retained compatible requirement is `numpy>=1.24,<3`. The new verifier and inherited report cross-check use the standard library only. The runner and new verifier require Python 3.10 or later.

From the package root:

```sh
python -m pip install -r reproducibility/legacy/requirements.txt
python reproducibility/RUN_ALL.py
```

The runner does not install packages or contact a network. It executes the inherited inventory, inherited independent report checker, and new verifier, stopping with a nonzero exit status on failure. The optional pip command is the only network-dependent setup command above. Each verifier overwrites its own generated results; elapsed-time fields may differ on rerun.

To execute only the new implementation:

```sh
python reproducibility/code/verify_revision.py
```

Outputs are in `reproducibility/data/revision_verification.json` and `reproducibility/legacy/data/`. Logs are retained under `reproducibility/logs/`. The inherited full `operators.csv` is included, not merely summary counts. Separate old and new code paths are implementation cross-checks, not external replication.

## Build the manuscript and audit

A standard TeX Live or compatible LaTeX installation with the packages named in the source is required. No external bibliography processor is needed for the manuscript.

```sh
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error CM_Phase_Algebra_Revised.tex
pdflatex -interaction=nonstopmode -halt-on-error CM_Phase_Algebra_Revised.tex
```

The audit PDF additionally uses Pandoc. From the package root:

```sh
pandoc audit/Theory_Audit_and_Review.md --from markdown --standalone --pdf-engine=pdflatex --lua-filter=audit/table_widths.lua -V geometry:margin=24mm -V fontsize:11pt -V documentclass:article -H audit/pdf_header.tex -o audit/Theory_Audit_and_Review.pdf
```

The audit table-width filter and header are provided so the PDF is reproducible without hand edits.

## Provenance, limitations, and author review

`provenance/original_uploads/` preserves all five original uploads, including the original ZIP intact. `input_manifest.json` records their SHA-256 hashes. The original canonical paper, available prior viability assessment, and original review inventory are separately convenient to inspect. No files in the user's external accounts or repositories were edited.

The supplied signed-integral companion root references missing section files; its abstract and declared scalar transition were compared, but unseen proofs were not reviewed. The other attached papers were compared where relevant, not newly certified in full.

The specialist and hostile reports are seven analytical perspectives from one assistant. They are not independent external peer reviews. The revision is AI-assisted and prepared for author review; the byline is not an assertion of author approval. The original modal source's byline differs from the other project manuscripts, and this package does not silently resolve that authorship issue.

All declared checks passed after relocation into this final package directory. PDF pages were rendered and inspected. No formal proof-assistant certification, historical-firstness certificate, independent external replication, or practical benchmark advantage is claimed.

`MANIFEST_SHA256.json` hashes all deliverable files except itself. Generated timing and build metadata can change after a rerun. Original-input hashes remain the provenance reference.
