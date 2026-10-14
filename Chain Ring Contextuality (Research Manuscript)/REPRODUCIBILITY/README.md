# Reproducibility

The current draft has a [standalone computational supplement](../REVISION_2026-09-26/supplement/README.md).

After extracting the revised package, run:

    python supplement/run_reproduction.py

Python 3.10+ and the standard library suffice. The wrapper reruns the unchanged audit checker, a scoped companion comparison and ten supplied tests; compares substantive outputs; regenerates the manuscript table; and writes commands, timings, exit codes and hashes. No original portfolio dependencies are needed. Do not disable assertions.

The [revision response](../REVISION_2026-09-26/REVISION_RESPONSE.md) states coverage and limits. The historical generator in the preserved 19 September source package depended on absent inputs and is not the current entry point. Old canonical-runner or LM-product assertions describe historical snapshots and are not evidence claims of the revised article.

Build PDFs with python supplement/build_documents.py using an installed TeX distribution. The [revision README](../REVISION_2026-09-26/README.md) gives details.
