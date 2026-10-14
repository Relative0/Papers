# Signed and Integral Lifts of Correspondence Matrices

**Submission revision — 27 September 2026**

This package contains the revised 30-page technical companion, source, bibliography, reproducibility code/data, independent adversarial checks, and the full referee/revision record produced for the latest audit.

## Main files

- `paper.pdf` — revised submission manuscript.
- `paper.tex`, `sections/`, `references.bib` — modular LaTeX source.
- `standalone.tex` — self-contained manuscript source with embedded bibliography.
- `REFEREE_PANEL_REPORT.md` — five specialist passes plus two hostile referee attacks.
- `REVISION_MEMO.md` — changes made in response to the review.
- `PUBLICATION_READINESS.md` — weighted scorecard and submission decision.
- `code/` — exact arithmetic and verification scripts.
- `data/` — generated summaries, classification data, tables, and rerun logs.

The referee reports are role-based AI reviews, not external human peer review. They were separated by specialty and followed by independent computational reconstruction where possible.

## Scientific scope

The paper is framed as a correction-oriented mathematical/computational companion. It does **not** claim a new physical quantum theory, a new exact-synthesis algorithm, a Born-rule derivation from Boolean logic, or a simulation speedup.

The central contribution is the explicit separation of:

1. strict Boolean F2[C4] rotation/convolution and its finite no-go audit;
2. the integral lift Z[C4] and quotient by 1+g^2 giving signed Gaussian phase coordinates;
3. the exact intertwiner QP=JQ and XOR carry/overlap correction;
4. typed translation of predicate CMs to reversible and phase oracles;
5. validation against established exact Clifford+T and Boolean path-sum semantics.

## Reproduce the checks

Python 3.10+ is recommended. The latest run used Python 3.13.5 and NumPy 2.3.5.

```sh
python -m pip install -r requirements.txt
python code/verify_finite.py
python code/verify_quantum.py
python code/verify_bridges.py
python code/independent_hostile_checks.py
python code/make_tables.py
```

Headline reproduced results include:

- 65,536 two-by-two F2[C4]-linear operators tested on all 256 states;
- 32 global coefficient-Hamming isometries;
- 512 weight-four shell preservers and 128 distinct shell actions;
- zero target four-phase fringe hits in the stated shell experiment;
- 240 exact random circuit tests and 5,760 intermediate norm checks;
- 120 exact path-sum/state-vector comparisons;
- 8,192 predicate/phase correction checks;
- independent reproduction of QP=JQ, carry, global/shell counts, phase profiles, no-fringe, and oracle identities.

## Build

```sh
latexmk -pdf -interaction=nonstopmode paper.tex
```

The final PDF has no unresolved references. Full 16x16 interference tables are retained in `data/interference_tables.json` and `sections/08_tables.tex` but are intentionally omitted from the submission body.

## Readiness conclusion

The review package rates the revised manuscript **8.48/10 weighted publication readiness**. It is considered ready for public preprint and targeted journal submission as a technical/correction note, subject to venue-specific formatting and disclosures. Novelty/priority remains the principal residual weakness for venues that require a major new quantum algorithm or formalism.
