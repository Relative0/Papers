# CM Structural Computation: completed three-draft research package

Start with `02_FINAL_EXECUTIVE_SUMMARY.md`, then `manuscripts/v3/paper_v3.pdf` and `01_FINAL_PUBLICATION_READINESS_AUDIT.md`.

**Final publication form:** a bounded methods / reproducibility technical report. A distinct, competitive research-paper novelty or performance claim is not established.

The manuscript is **Exact Boolean Decomposition Artifacts under Conditioning: Algebraic Contracts and a Reproducibility Audit**, prepared for Brian Theory's author review. Drafts v1, v2 and v3 are complete manuscripts with editable TeX and compiled PDFs. They are not three filenames for the same draft. The later versions add proofs, code, tests and corrected experiments. Earlier drafts remain preserved as review history and are not the recommended current text.

## Package navigation

- `manuscripts/`: three self-contained TeX/PDF projects, crosswalks and freeze hashes.
- `audits/`, `reviews/`, `responses_and_changelogs/`: two audit/review cycles, fourteen specialist-role reports, final audit and issue responses.
- `evidence/`, `prior_art/`, `research/`: recursive source inventory, ownership boundaries, handoff audit, research decisions, proofs/counterexamples and novelty ledger.
- `reproducibility/`: producer, independent scalar-checking logic, adapters, two codecs, baselines, tests, pinned source, raw timing samples, exported witnesses and clean-replay receipt.
- `historical_source_material/`: unchanged original ZIP, supplied protocol, old handoff, relevant extracted source and foundation reference. No original manuscript was overwritten.

The specialist reviews are same-assistant role-separated adversarial passes, **not external peer review or separate independent agents**. Mathematical arguments and code were actually checked, but formal verification and independent expert replication remain open.

## Reproduce the exact checks

From this package directory, with Python 3.10 or later (tested on Python 3.13.5):

```sh
python reproducibility/run_correctness.py --output replay_receipt_new.json
```

This copies code/data to a new temporary directory, runs eight commands in separate processes and leaves the preserved original results untouched. No network or third-party Python packages are required. See `reproducibility/README.md` for timing, schemas, source pins and version-specific replay.

## Compile a manuscript

```sh
cd manuscripts/v3
pdflatex -interaction=nonstopmode -halt-on-error paper_v3.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_v3.tex
```

The `references_formatted.tex` file is included directly, so BibTeX is not required to reproduce these PDFs. Editable `.bib` files are also provided. All included TeX inputs must remain together. Compile instructions apply analogously to v1 and v2. `build_manuscripts.py` automates all three builds.

## Integrity and provenance

`evidence/EVIDENCE_INVENTORY.json` records 3,668 original archive/nested-archive entries and 1,228 distinct content hashes. This is a complete inventory of those entries, **not a claim to have read every line of every neighboring project**. Targeted reading and audit scope are documented. Generated-package checksums appear in `05_MANIFEST_SHA256.json`; the manifest excludes itself and does not include its own checksum. `verify_package.py` checks it.

Prior source assertions are separated from new derivations, newly executed experiments and unresolved proposals. The original portfolio retains its own licenses and notices. The pinned EPFL input's MIT notice is included. No new blanket license is imposed on the author's manuscripts or original code.
