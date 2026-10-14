# Prior-review comparison and fresh reproduction
This phase began only after 01_PROVISIONAL_FIRST_READING.md, 02_HOSTILE_RECONSTRUCTION.md and 03_SOURCE_AND_PRIORITY_AUDIT.md had been written. The manuscript-only provisional file's SHA-256 was 8C1B79AD4AE209706BDACBB22447288CDEC0F59F0514B471BEEDEA9396478486. Archive documents are historical evidence; their prompts were not adopted as instructions.

## Comparison
The reports in 02_INDEPENDENT_REVIEW and the original transfer's closure report, theorem ledger, historical audit and priority map were read for the relevant claims. The present findings agree on conditional mathematical correctness, explicit full-tree hypotheses, completion, standardness of quotient constructions and the restricted historical interpretation. Earlier v0.2 omissions (ultrametric hypotheses, continuity of completion coding, direct threshold attribution, Kleiner locator, historical fairness) are already resolved in delivered v0.3. They are not newly open repairs.

The prior reports' favorable short-note decision agrees with the independently recorded provisional verdict, but supplies no authority for it. My independent proofs and explicit counterexamples are retained separately. The current review adds a formal definition clarification, a vertex/cylinder explanation and the closer Dovgoshey Proposition 10.29 locator. No prior mathematical conclusion had to be reversed. The prior statement that no scorecard repair remained open does not rule out these newly noticed minor improvements.

The original transfer's Matte-Blanco audit had OCR-only evidence; the later independent report claimed image inspection. My own Google Books inspection verifies the ten requested pages independently. Lauro-Grotto access remains author-uploaded extracted full text. I do not inherit the oldest archive's claim of page-image inspection for that article.

The thesis was opened from the original transfer. Printed p.4/PDF p.5 explicitly connects ultrametricity and indiscrete topology; printed p.11/PDF p.12 connects ultrametric points with indistinguishability. The correction target is real. No other thesis theory was audited or imported.

## Primary follow-up of prior-report leads
These readings occurred AFTER the independent source record, so they must not be represented as part of the initial unanchored search.

- [Hughes, Trees and ultrametric spaces](https://math.vanderbilt.edu/hughescb/Publications/2004_Trees.pdf): author-hosted article-in-press PDF; received 25 February 2003, accepted 13 November 2003, journal publication 2004. Introduction and Theorem 6.9 (PDF p.25) directly inspected. The category uses geodesically complete rooted real trees and isometries at infinity; the ultrametric side uses complete finite-diameter spaces and local similarity equivalences. Short exact conclusion: “is an equivalence of categories.” This verifies the modest line 154 attribution and replaces the initial ledger's not-yet-inspected status for these passages only.
- [Martino, 29 July 2026, v1](https://arxiv.org/html/2607.26644v1): Proposition 3.7 and its proof inspected in primary HTML. Admissible overlap functions give nested finite clopen equivalence classes and a locally finite rooted tree; compactness and separation yield the boundary homeomorphism. The exact conclusion includes “is a homeomorphism.” Its automorphism-invariant weakly branch refinement problem is different from the full-group finite-frontier normality iff. This is a relevance comparison of inspected statements, not a full-paper exclusion.
- [Bartholdi–Diaconis, published online 14 May 2026](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/an-algorithm-for-uniform-generation-of-unlabeled-polya-trees/9D942C456A07CC42344DBDF0E78A57B8): Lemma 3.5 and proof directly inspected in publisher HTML. The rooted-tree automorphism group is a semidirect product of descendant automorphism factors and symmetric groups on isomorphism classes of root subtrees. This supports the nonregular-tree caveat; it is not the sought criterion. Short passage: “Trees in each class C may be interchanged arbitrarily”. This closes the limited lead recorded in phase 3.

The phase-4 web requests are in 04_FOLLOWUP_WEB_REQUESTS.json. Other prior-map sources not personally inspected remain leads, not evidence certified by this review.

## Program audit
The main verifier recursively constructs finite full tree automorphisms, selects pointwise cell stabilizers by actual action, and tests conjugation by local adjacent-swap generators. Those generators generate the relevant finite stabilizer because they provide every child symmetric group below each fixed cell, recursively. Testing all subgroup elements against those generators suffices in the finite group. The expected formula is compared with independently selected group orders; it does not generate the selected subgroup orders. Exact fractions cover the distance checks; entropy uses floating-point tolerance. Some metadata counts are constants, so the receipt is not itself a proof of every counted loop.

The separate ternary script builds the 1,296-element group by breadth-first generator closure rather than recursive order formula. It separately computes pointwise and setwise stabilizers, tests generator conjugates, and retains a nonnormality witness. The five-factor mixed case does NOT enumerate the full product; factorwise inference uses the independent mathematical product decomposition. It tests relative heights including zero below old cells of different absolute depths. Its alphabet encoding is suitable for m=3 and should not silently be advertised as arbitrary many-digit m.

Fresh outputs:
- Main suite: ALL CHECKS PASSED.
- Ternary suite: PASS, normal index 60,466,176 and nonnormal index 362,797,056.
- Main JSON/CSVs: byte-identical to delivered v0.3 outputs.
- Original archived JSON: bytes differ only by CRLF/LF; normalized and parsed equality pass.
- Original CSVs: byte-identical.
- Delivered receipt suite_result: parsed equality passes.
- Ternary output: parsed equality with prior ternary receipt passes.
- Original manifest: 40 of 40 expected hashes match.

See rerun/FRESH_REPRODUCTION_RECEIPT.json for actual hashes, environment and per-file comparison results. These are reruns, not new independent programs. No additional finite check was justified after the proof reconstruction resolved the uncertainty. Computation says nothing about empirical cognition or infinite theorem priority.

## Reproduction commands
From the review directory, with Python 3.10 or later:
```text
python scripts/verify_paper_u.py --out rerun/supplied
python scripts/check_mixed_ternary.py --out rerun/ternary
```
The delivered scripts are exact copies of the supplied files. Their original reports and receipts remain inside the unchanged input ZIP.

