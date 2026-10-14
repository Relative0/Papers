# File map and authority order

## 00_READ_FIRST

- `START_HERE.md` — first file to read.
- `MASTER_HANDOFF.md` — canonical compact state summary.
- `SIMPLE_PROMPT_FOR_GPT_ASTRA.md` — copy/paste prompt for a fresh account.
- `RECOVERY_CHECKLIST.md` — quick integrity/read-order checklist.

## 01_CURRENT_MANUSCRIPT — authoritative publication text

- `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.tex` — **authoritative source**.
- `paper_u_refs_v0.2.bib` — authoritative bibliography.
- `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.pdf` — compiled eight-page manuscript.
- `.bbl` — generated bibliography cache.

If there is a conflict between v0.1 source material and v0.2, v0.2 controls unless the next independent review proves v0.2 wrong.

## 02_RESEARCH_CLOSURE — the research record

- `PAPER_U_RESEARCH_CLOSURE_REPORT.md` — full decision and remaining limitations.
- `PAPER_U_THEOREM_LEDGER.md` — claim-by-claim status, proof and standardness record.
- `PAPER_U_PRIORITY_AND_LITERATURE_MAP.md` — prior art, chronology, links/access status.
- `PAPER_U_MATTE_BLANCO_SOURCE_AUDIT.md` — historical/interpretive source audit.
- `PAPER_U_GENERALIZATION_AND_STRENGTHENING_STUDY.md` — proofs, counterexamples, generalizations, adaptive results.
- `PAPER_U_ADVERSARIAL_ATTACKS.md` — explicit attempts to kill/trim the paper.

## 03_EVIDENCE_AND_REPRODUCIBILITY

- `scripts/verify_paper_u.py` — finite verification/regression script.
- `scripts/build_manuscript.sh` — LaTeX build helper.
- `evidence/` — actual JSON/CSV results and logs from the closure phase.
- `CLOSURE_PACKAGE_MANIFEST_SHA256.json` — original closure archive integrity record.
- `ORIGINAL_CLOSURE_README.md` — original package guide.

## 04_ORIGINAL_INPUTS — provenance, not authority

This directory preserves the user's research-closure request, the original v0.1 bundle, the prior p-adic/ultrametric audit, and the 2015 thesis. The thesis is historical provenance and can contain mathematical errors or undeveloped conjectures.

`unpacked_source_bundle/` exposes the uploaded source archive without requiring another unzip step.

## 05_NEXT_REVIEW

- `HANDOFF_TO_REVIEW_GATE.md` — detailed gate and high-value attacks.
- `NEXT_THREAD_REVIEW_PROMPT.md` — full next-stage prompt.

## 06_IMMUTABLE_ARCHIVES

- exact prior closure result ZIP;
- exact uploaded research-closure source ZIP.

These are included so that a future agent can recover the pre-transfer state even if files elsewhere are accidentally changed.
