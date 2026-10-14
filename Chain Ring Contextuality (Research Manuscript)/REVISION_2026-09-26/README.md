# Revised P01 draft - 26 September 2026

**Author:** Brian Theory, B-Theory.

- Read [the revised article](manuscript/main.pdf); edit [main.tex](manuscript/main.tex).
- [Revision response](REVISION_RESPONSE.md) maps every audit issue to its repair.
- [Literature comparison and verification notes](LITERATURE_COMPARISON.md) identify the sources and the limits of the priority review.
- [Computational supplement](supplement/README.md) explains exactly what was rerun.
- [Optional Boolean note](supplement/boolean_interface.pdf) contains the corrected symbolic-projector argument.

The principal theorem set is retained. A primitive-resource corollary is added as an immediate consequence. The article now centers the classification, the exact orbit codebook and the raw-teleportation comparison. The original 19 September source is preserved in the parent project's historical source package. The received audit is preserved unchanged under P01_ASTRA_AUDIT/; it describes the old draft and is not a new assessment of this revision.

## Reproduce after extracting

Python 3.10 or later; standard library only:

    python supplement/run_reproduction.py

This creates supplement/reproduced/, refuses a nonempty output directory, and compares fresh substantive outputs with the included reference results. For another run choose a new directory:

    python supplement/run_reproduction.py --out another_run

The run includes the unchanged audit checker, the scoped companion cross-check, ten supplied companion regression tests, table generation and reference comparisons. It has no dependency on another project, a downloaded archive, a network service, or historical /mnt/data files. Do not use python -O, -OO, or PYTHONOPTIMIZE.

To rebuild both PDFs with an installed TeX distribution:

    python supplement/build_documents.py

This uses pdfLaTeX and BibTeX, disables shell escape, and disables automatic package installation for MiKTeX. Required TeX packages are listed in the document preambles. On this Windows host, MiKTeX required approved access to its own user configuration directory; mathematical reproduction does not require that access.

## Evidence and limitations

The release includes code, reference results, explicit analyzers and encoder/decoder certificates, source provenance, build logs, a clean-extraction receipt and a SHA-256 manifest. Finite checks are not formal proof certification. In particular, the 65,536-matrix length-four inventory is not a full direct support solve; the manuscript states this distinction explicitly.

Historical priority remains a bounded literature judgment. No journal submission, preprint upload, commit or push has been performed. Author name and affiliation were confirmed for this revision; no unprovided email address was invented.
