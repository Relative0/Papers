# LM-to-Modal Bridge Research Package

Date: 2026-09-18

This package collects the complete findings from the investigation of whether the formula-valued Logical Matrix (LM) calculus canonically induces the later modal/effect/measurement framework over the CM-derived chain ring.

## Main result

The later modal theory is **not** a direct semantic consequence of the original LM calculus. The strongest mathematically defensible bridge is:

1. Paper B supplies a Boolean symbolic matrix calculus and valuation-natural contraction.
2. The later amplitude ring `A = F2[u]/(u^4)` must be chosen independently; direct Boolean valuation cannot generate its non-Boolean elements.
3. The canonical enriched symbolic layer is `B tensor_F2 A`, where `B` is the Boolean/Lindenbaum algebra of formulas.
4. Boolean valuation extends canonically to `v_A = v tensor id_A`.
5. Every symbolic ring-valued amplitude has a Boolean support predicate whose satisfying valuations are exactly the valuations for which the concrete ring amplitude is nonzero.
6. The choices "effects are rows of reversible A-bases" and "nonzero = possible" remain additional modal measurement structure.
7. A clean division-free branch update exists for reversible bases: `J_i^B = B^{-1} P_i B`.
8. Zero divisors still obstruct a closed unrestricted process theory.

## Most important files

- `report/LM_Modal_Bridge_Report.tex` - full LaTeX research report, including definitions, type map, theorem statements and proofs, failure results, prior art, computational checks, paper implications, and bibliography.
- `tests/lm_modal_bridge_checks.py` - expanded independent finite checker.
- `tests/lm_modal_bridge_checks_output.json` - exact output from the expanded checker.
- `research/PRIMARY_SOURCE_LEDGER.md` - line-level primary-source map used in the investigation.
- `research/PRIOR_ART_MATRIX.csv` - novelty/prior-art classification of the bridge claims.
- `research/SEARCH_LOG.csv` - reproducible literature-search ledger.
- `research/references.bib` - BibTeX bibliography.
- `inputs/CM_Adversarial_Review_2026-09-18(1).zip` - the supplied adversarial-review archive, preserved unchanged.
- `prior_adversarial_review/` - unpacked contents of that archive.
- `MANIFEST_SHA256.txt` - SHA-256 manifest for every file in this package.

## Computational headline results

The expanded checker independently verifies:

- ring order: 16
- units: 8
- idempotents: exactly 0 and 1
- `|GL_2(A)| = 24,576`
- unordered reversible projective two-outcome bases: 192
- branch nonzero iff measured coefficient nonzero: 98,304 checks
- same-basis repeatability: 98,304 checks
- row-unit projective invariance: 24,576 checks
- symbolic-support fibers: 262,144 checks
- Paper-B LM ordinary Boolean-ring matrix products: 112 remain in the 16-LM family and 144 leave it
- explicit nonzero tensor annihilation from zero divisors
- explicit unimodular-preparation / nonunimodular-conditional example

## Reproducing the new finite checks

From the package root:

```bash
python tests/lm_modal_bridge_checks.py
```

The result should match `tests/lm_modal_bridge_checks_output.json` apart from the environment string.

## Source-material note

The original Paper B PDF and several other primary files were read from the ChatGPT File Library during the research, but raw-byte export of those Project files was not authorized in the working environment. They are therefore identified precisely in `research/PRIMARY_SOURCE_LEDGER.md` rather than duplicated here. The supplied adversarial-review archive is included in full.

For handoff to another researcher or agent, provide Paper B alongside this ZIP if available.
