# Integrated manuscript v0.4

This directory contains the separate manuscript created after the completed interaction-core gate and its proof/priority/editorial convergence review on 29 September 2026.

- `Observation_Refinement_Descent_and_Cone_Draft_v0.4.pdf` — reading copy.
- `Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex` — integrated LaTeX source.
- `CONVERGENCE_REVIEW.md` — substantive descent correction, theorem hierarchy, preserved counterexamples, priority boundaries, and review disposition.
- `HANDOFF_TO_MASTER.md` — current status and continuation boundaries.
- `INTEGRATION_RECEIPT.json` — 27 explicit transformations and source hashes.
- `VERIFICATION_RECEIPT.json` — preserved-input checks and targeted integer reruns.
- `PDF_QA_RECEIPT.json` — final PDF build and visual review.
- `v0.3_to_v0.4.patch` — reviewable source diff against the frozen manuscript.
- `build/` — organized compiler logs, auxiliary files, page renders, and fresh certificate outputs.

The original handoff and v0.3 under `../Transferred Research/` are unchanged. The earlier two unmerged section files also remain unchanged; their integration status is superseded for **v0.4 only**. Previous reports saying they were unmerged accurately describe those earlier gates.

## Reproduction

Run in this directory, using the installed Python 3.10 environment with SymPy:

```powershell
python build_manuscript.py
python verify_convergence.py
```

Then run the following compiler invocation twice. MiKTeX requires normal access to its existing per-user configuration/cache, which the restricted Codex sandbox does not provide without an approved escalation.

```powershell
& 'C:\Users\brian\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe' --disable-installer --disable-write18 --interaction=nonstopmode --halt-on-error --output-directory=build Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex
```

`finalize_artifacts.py` uses the bundled Python environment with pypdf and Pillow to check the final log, extract text, copy the PDF to this directory, prepare contact sheets, and write the build receipt. PDF visual review must be repeated after future source changes; a script cannot certify visual quality.

For future edits, change `build_manuscript.py` or retire the generator explicitly. Re-running it overwrites the generated v0.4 source, so do not make unrecorded edits only to that source. Do not alter v0.3.
