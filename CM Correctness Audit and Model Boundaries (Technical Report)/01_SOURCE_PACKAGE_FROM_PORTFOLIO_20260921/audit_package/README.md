# Boolean CM correctness audit -- verified baseline 1.0

**Date:** 18 September 2026. Start with `paper/CM_Correctness_Audit.pdf`.

This package audits the conversation's native CM, rotation-operator, shared-module, and literal independent-register models. It preserves successes and failures and **supersedes earlier conversational interpretations where they conflict with the final report**. Historical source snapshots remain unchanged for provenance; their documentation is not the final interpretation.

## Main findings

The Boolean rotation algebra, modal superposition/interference, tested Bell/GHZ contradictions, full-rank universal transfer, and 64-message dense coding are verified under explicit model assumptions. Important corrections are equally central:

- The 2x2 CM identity and its selected 4x4 square-zero operator are different objects.
- The shared module and literal tensor model are not tensor-equivalent. Some nonzero shared preparations tensor to zero. Their separability counts differ.
- Literal universal transfer needs a rank-eight resource including phase correlations, a complete 64-outcome analyzer, and gates beyond the commuting phase algebra. The old logical-only analyzer fails.
- The old no-finite-copy-activation theorem is restricted to rotation-linear maps and tensoring over the coefficient algebra. In the literal unrestricted model, two copies of a rank-six resource can heraldedly yield a full resource.
- The 15 Smith classes and 192-basis contextuality hierarchy are restricted-family results. Under full local GL(8,2), bipartite rank is the orbit invariant.
- Boolean-orthogonal corrections cannot supply a complete even-dimensional rank-one Bell scheme of the specified type. No nonzero bilinear form is preserved by both P and the added shear T.
- No-cloning concerns linear modal tensor-state maps, not copying ordinary coefficient memory or nonlinear Boolean coefficient processing.
- The tested Bell support cannot be reproduced faithfully by an ordinary no-signalling probability distribution. This is not just an unspecified Born rule.

## Evidence

The four historical suites pass 22 + 10 + 15 + 12 = **59** named tests. The new independent suite passes **31**, totaling **90** named tests. The calculation drivers additionally perform the explicitly recorded enumerations, including 4,194,304 resource/branch rank checks, two 16,384-case literal teleportation runs, 983,040 shared restricted fixed-space scans and 983,040 quotient-row scans.

Zero vectors occur in algebraic regression files but are not modal states. Each literal teleportation run has 16,320 nonzero-state/outcome cases and 64 null regressions.

`data/claim_ledger.csv` and the PDF identify the scope of every main check. Passing tests does not imply formal proof-assistant certification, physical quantum behavior, newness, or computational speedup.

## Reproduce

Use Python 3.11+ with the packages in `requirements.txt`. Exact tested versions are recorded in `data/artifact_validation.json`. The computation does not require internet access, a cloud account, or the user's Windows research folder.

```text
python -m pip install -r requirements.txt
python run_all.py --historical
```

Without `--historical`, `run_all.py` reruns the independent drivers, artifact checks, generated report tables, and 31 new tests. Logs supplied in this archive record what was actually run. Timings are not performance benchmarks.

### Compile the report

The modular report source has one included table file:

```text
cd paper
latexmk -pdf -interaction=nonstopmode CM_Correctness_Audit.tex
```

`CM_Correctness_Audit_Standalone.tex` includes the tables inline and can be compiled by itself using `latexmk -pdf CM_Correctness_Audit_Standalone.tex`. When using `pdflatex` directly, allow at least three passes from a clean directory until references and the two-page table of contents stabilize. Both sources have an embedded bibliography. No BibTeX run, fonts supplied by this archive, or Python execution is needed to compile the included source. A normal TeX Live/MiKTeX installation needs the packages named in its preamble.

## Contents

- `paper/`: PDF, modular LaTeX, generated table source, standalone LaTeX.
- `code/boolean_kernel.py`: independent packed AND/XOR matrix kernel, scalar cross-check, two rank implementations, inversion, tensoring, normal forms.
- `code/audit_models.py`: original CM checks, rotation algebra, all gates/resources, local stabilizers, contextuality, GHZ.
- `code/audit_protocols.py`: direct literal tensor circuits, two teleportation analyzers, dense coding, gate synthesis, rank checks, model-boundary witnesses, external probability LP.
- `code/audit_restrictions.py`: LM pairing, exhaustive shared restricted/quotient scans, orthogonal-row scan.
- `code/verify_artifacts.py`: historical manifest checks and fresh CSV cardinalities.
- `code/generate_report_tables.py`: tables, claim ledger, and standalone source.
- `tests/`: new independent tests, including the natural H-based analyzer's rank loss.
- `data/`: raw inventories, tables, explicit matrices, counterexamples, and numerical summaries.
- `logs/`: actual test, computation, and PDF build receipts.
- `source_snapshots/`: four preserved input packages, without caches.
- `MANIFEST_SHA256.txt`: hashes of the final package files other than this manifest.

The large resource/branch campaign saves one row per outcome giving its complete 65,536-resource count and mismatch total, plus a separate full resource inventory. It does not duplicate the same resource ranks in a four-million-row CSV; the source recomputes every comparison.

## Bit convention

Matrix rows are packed integers. Bit 0 is column 0; vector bit 0 is coordinate 0; flattened entry (i,j) is bit i*n+j. A printed binary string may display the opposite visual direction, so use the declared indexing. Integer arithmetic used to pack bits or count cases is not amplitude arithmetic. In every core state/operator calculation the scalar operations are AND and XOR. The real LP is a separately labeled external diagnostic.

## Source and claim boundaries

The new calculation modules do not import historical computational modules. Historical JSON/CSV and synthesis words are read to compare outputs, not to assume their correctness. The original CM/LM manuscript and revised operator-level manuscript were consulted through File Library excerpts; their full PDF bytes were not mounted and are not redistributed here. Input archive hashes and those provenance boundaries are recorded.

The package is a scientific audit and simulation, not a physical implementation. It makes no broad novelty claim and no claim to audit every possible CM theorem, arbitrary instrument, or every full-GL measurement context. See the report's final open-items section before extending the theory.
