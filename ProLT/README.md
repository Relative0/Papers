# Propositional Logical Topology core v0.8.1

Release date: 24 September 2026

This bundle is the release candidate for the paper's stated identity as an
expository synthesis of finite Boolean semantics, finite/Alexandrov topology,
observation signatures, and directed distance.

## Contents

- `propositional-logical-topology-core-v0.8.1.tex` — canonical LaTeX source.
- `propositional-logical-topology-core-v0.8.1.pdf` — compiled 19-page paper.
- `RELEASE_NOTES.md` — review history and changes from v0.8.
- `SHA256SUMS.txt` — integrity hashes for the release files.

## Build

The PDF was built with MiKTeX pdfTeX 1.40.25 using shell escape disabled:

```powershell
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error propositional-logical-topology-core-v0.8.1.tex
```

Run the command three times to settle the contents, citations, and internal
references.

## Release validation

- Three LaTeX passes completed without final warnings, unresolved citations,
  unresolved references, overfull boxes, or underfull boxes.
- The finite supporting verifier passed.
- The final PDF was reopened and its revised text extracted successfully.
- All 19 rendered pages were visually inspected for clipping, overlap, missing
  glyphs, broken tables, and pagination defects.
- The bundled TeX and PDF match the canonical v0.8.1 workspace copies by
  SHA-256.

The paper is release-ready for an expository or pedagogical submission. It does
not claim a new topology class, proof calculus, homology invariant, operational
measurement protocol, or contextuality result.
