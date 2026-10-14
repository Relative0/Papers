# Revised manuscript build and visual QA

Review date: 29 September 2026. Revision keeps the v0.3 filename for a small referee patch; its separate directory and SHA-256 manifest distinguish it from the original.

Only three TeX paragraphs and one bibliography note changed. The focused unified patch records every change. Original manuscript and input ZIP were not modified.

Tools: MiKTeX pdfTeX 1.40.25 / MiKTeX 24.1, LaTeX2e 2023-11-01 patch 1; Biber 2.19; Poppler pdftoppm; pypdf for page/text inspection. The supplied logreq.sty and logreq.def were copied from the evidence bundle into the build directory. Automatic package installation was disabled.

The initial sandboxed pdfLaTeX run failed because MiKTeX could not initialize its normal user cache outside the workspace. The same local build succeeded with approved compiler access. Biber encountered the same sandbox initialization restriction, then succeeded with approved access; its Perl locale warning reported fallback to the C locale. No compiler setup, package installation or security configuration was changed. The first marker invocation used a nonexistent Node path; rerunning the required artifact-operation marker with the installed node command succeeded before source authoring.

Biber completed successfully, and the final PDF/log timestamps are later than the generated BBL. The final pdfLaTeX log has no undefined citations/references, required reruns, overfull boxes or underfull boxes. The PDF contains nine pages and twenty cited bibliography entries. Some unused entries remain in the supplied Bib file; unrelated bibliography cleanup was deliberately omitted.

Every final page was rendered with `pdftoppm -scale-to 1450 -png` and inspected as an image. Pages 1–3: title, abstract, theorem and quotient definitions readable. Pages 4–6: calibrated completion proof, new citation and clarified normality step readable. Pages 7–9: entropy, historical limits, appendix and references readable. No clipping, overlapping text, missing symbols or broken reference labels were seen. Page breaks within arguments and a partially filled last bibliography page are ordinary article layout, not defects.

The compiled PDF, TeX, Bib and BBL are in revised_manuscript/. Final compiler logs and page images are included in the complete ZIP. The Python checks are described in 04_PRIOR_COMPARISON_AND_REPRODUCTION.md and their fresh receipt is in rerun/. Textual explanation/citation edits do not change their mathematical contracts, so they were not redundantly rerun after compilation.

To rebuild, run scripts/build_revised.ps1 from PowerShell with pdfLaTeX and Biber installed. It resolves paths relative to itself, disables automatic package installation and stops on an unsuccessful compiler pass.
