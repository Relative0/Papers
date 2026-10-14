# Review evidence and reproducibility

The manuscript and previous packages are read-only inputs. Outputs are confined to this folder.

- `PRELIMINARY_FINDINGS.md`: initial complete-source reconstruction, preserved before reading comparison reports.
- `REVIEW.md`: substantive independent verdict, source locators, repairs and limitations.
- `CLAIM_AUDIT.csv`: 39 audited claims, with correctness separated from priority and significance.
- `independent_diagnostics.py` / `diagnostics.json`: standard-library exact arithmetic, finite truth tables and source/version checks.
- `SUGGESTED_SCOPE_CLARIFICATIONS.patch`: two proposed wording edits only; not applied.
- `manuscript_layout.txt`: pypdf extraction with page markers; source for locators, not a substitute for rendering.
- `pdf_checks/page-01.png` through `page-18.png`: independent Poppler render, 1100-pixel long edge.
- `pdf_checks/contact_1.png` through `contact_3.png`: visual overview of all 18 pages. Pages 12–14 and 16 were also inspected individually.

## Exact diagnostics

PowerShell, from any directory:

```powershell
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Finite Jet Sign Rigidity (Research Manuscript)/INDEPENDENT_ADVERSARIAL_REVIEW_2026-10-13/independent_diagnostics.py'
```

This rewrites only `diagnostics.json` in this review folder. Python 3.10+ is sufficient and no third-party package is used by that checker. The program checks the requested source hashes and reads the September source for preserved blocks. It asserts exact statements on finite samples; it does not numerically infer universal analytic bounds, literature lower bounds, or novelty.

To rerender the PDF, use the existing `pdftoppm.exe` (resolved in this session to the bundled Poppler directory), with `-scale-to 1100 -png`, the unchanged current PDF, and an output prefix inside this review folder. No compilation or package installation is needed. The extraction used installed pypdf 6.10.0. The first PATH-resolved pdftotext was a MiKTeX program and failed on runtime-directory access; it was not used as successful verification.

## Primary-source locators independently verified

| Primary source | Passage | Evidence used |
|---|---|---|
| [Sherstov author PDF](https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf) | Theorem 1.10, p. 6; true=-1, p. 3; Theorem 2.4, pp. 11–12 | Read theorem statements and convention; matched the finite-cube reduction |
| [Shapiro institutional PDF](https://ftp.cs.wisc.edu/pub/users/prem/rfuns.pdf) | Section 3.3 equations (3.4)–(3.5), p. 14; Section 3.6, pp. 18–19 | Read exact root family and differentiability discussion |
| [Rainer survey](https://arxiv.org/pdf/2107.01061) | Definition 2.2; Theorem 3.6; Corollary 3.12; Remark 3.13; Section 7.2 | Read weight, series, cutoff, positive-flat and associated-function statements |
| [Kopotun–Prymak–Shevchuk guide](https://mathanalysis.knu.ua/wp-content/uploads/2020/07/at-study-guide-january-22-2018-1-1.pdf) | Theorem 21.1, PDF p. 56; Theorem 24.1, PDF p. 59; cover | Read Jackson special case, algebraic Bernstein inequality and bibliography metadata |
| [Broglia–Tognoli](https://aif.centre-mersenne.org/article/AIF_1989__39_3_611_0.pdf) | Definition 2.2; Proposition 2.4; Section 4 hypotheses; Theorem 4.2, printed p. 629 | Read admissibility, factor parity, connectivity and flat-point implication |

Web search/cache date labels were not used as publication dates. Article dates were taken from primary covers or publisher records. Source links and exact passages, rather than search snippets or previous judgments, support the decisive checks. Missing historical texts and screenshot-host failures are recorded in REVIEW.md.
