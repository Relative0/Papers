# Revision Memo — 27 September 2026

## Major changes made after specialist and hostile review

1. **Retitled and reframed the manuscript.** The paper is now *Signed and Integral Lifts of Correspondence Matrices*, explicitly a correction-oriented technical companion.
2. **Rewrote the abstract.** It now leads with the strict F2[C4] boundary result, the integral/signed quotient, and the exact limits of the contribution. It explicitly disclaims a new quantum theory, exact-synthesis algorithm, or speedup.
3. **Added an early contribution-status table.** Standard algebra, CM-specific results, validation results, and non-claims are separated before the technical development.
4. **Repositioned the global Hamming-isometry theorem.** Added MacWilliams/Wood/Greferath-Schmidt context and clarified that the coefficient weight is not standard ring-symbol Hamming weight. The theorem is presented as an elementary specialized classification.
5. **Sharpened the integral-lift section.** The quotient Z[C4]/(1+g^2) ≅ Z[i] is identified as standard algebra; the CM-specific contribution is the explicit coordinate intertwiner QP=JQ and the semantic bookkeeping.
6. **Downgraded standard circuit results to propositions.** Exact Clifford+T closure and the CM-specialized path-sum representation are explicitly tied to prior exact-synthesis and sum-over-paths literature.
7. **Expanded public provenance.** The foundational CM paper is now cited as a public May 2018 working paper with DOI 10.13140/RG.2.2.28036.37764 rather than as an undated supplied manuscript.
8. **Refreshed literature through 27 September 2026.** Added finite-ring Hamming-isometry context and acknowledged ongoing 2026 exact-synthesis progress.
9. **Narrowed the future-work section.** Removed broad human-benefit claims and retained one falsifiable next step: certified local CM phase rewrites compared against established exact backends.
10. **Removed four complete 16x16 tables from the manuscript body.** They remain in `data/interference_tables.json` and the source package for reproducibility.
11. **Added an independent adversarial implementation.** `code/independent_hostile_checks.py` reproduces the critical algebraic identities, counts, shell phase profiles, and no-fringe result without importing the main backend.
12. **Re-ran all computational checks.** Primary and independent scripts passed.
13. **Cleaned internal-process language and submission metadata.** Author metadata is Brian Droncheff; the PDF title and running heads now match the revised technical-companion framing.

## Criticisms intentionally not “fixed” by overclaiming

- No practical speedup is asserted because no comparative benchmark exists.
- No physical quantum implementation is asserted because the work is an exact classical representation/audit.
- No exhaustive novelty/priority claim is asserted; the literature review is targeted and the CM-specific priority question remains only partially resolved.
- No proof-assistant certification is claimed.

## Files added for this review cycle

- `REFEREE_PANEL_REPORT.md`
- `PUBLICATION_READINESS.md`
- `REVISION_MEMO.md`
- `code/independent_hostile_checks.py`
- `data/independent_hostile_checks.json`
- rerun logs under `data/*_revision.log` and `data/independent_hostile_run.log`
