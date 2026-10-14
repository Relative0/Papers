# Manuscript v0.5 — bounded referee repairs

`Observation_Refinement_Descent_and_Cone_Draft_v0.5.pdf` is the reading copy; the matching `.tex` is generated from the immutable v0.4 by `build_v05.py`. The change scope is the independent referee's finite corrections: Theorem 2.4, the proof detail in Theorem 4.2, Theorem 11.2 cover/site hypotheses, Section 11.1 homological wording, Section 18 priority positioning, and a signed seven-state witness.

Read `RESPONSE_TO_REFEREE.md` for the point-by-point disposition, `SIGNED_WITNESS_SUPPLEMENT.md` for the integral paths, and `REPAIR_RECEIPT.json` for the source hash and exact transformation list. The original referee report is at `../Independent Expert Review/INDEPENDENT_EXPERT_REPORT.md`. `build/` contains compiler, rendering, and verification intermediates.

The mathematical core and counterexamples in v0.4 are retained. v0.3 and v0.4 remain separate and unchanged. To regenerate, run `python build_v05.py`, then compile with installed MiKTeX twice using `--disable-installer --disable-write18 --interaction=nonstopmode --halt-on-error --output-directory=build`. The existing MiKTeX cache requires normal user-profile access, which may need sandbox escalation. Run `verify_v05.py` after compiling; re-render the PDF and inspect pages after future edits.
