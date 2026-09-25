# Research-paper preservation audit

**Audit date:** 25 September 2026. **Mode:** read-only manuscript inspection. No manuscript, research-data or archive bytes were changed or deleted. Subsequently, authorized repository-local Git metadata was configured and the publication files were committed and pushed; see Appendix G.

## Executive summary

**Do not treat Papers for Publication as a complete preservation copy of CM Quantum, or vice versa.** Most principal CM/modal papers are represented in both, but important historical sources, detailed proofs, evidence and newer publication material are not.

1. **The identically named publication portfolios really are mirrors:** all **350 non-ZIP files** under `CM_LM_PUBLICATION_PORTFOLIO_20260921` match by relative path and SHA-256 across the two roots. This verifies the copied portfolio, not the surrounding research archive.
2. The full scan covers **2,062 non-ZIP files**: 1,610 in CM Quantum and 452 in Papers for Publication. There are **49 PDF instances and 70 LaTeX instances**, collapsing to **53 distinct byte-level PDF/TeX objects** (22 PDFs, 31 TeX files). These include fragments, audits and planning documents; they are **not 53 independent papers**.
3. **CM-only preservation priorities:** the original 29-page *Correspondence Matrices; Algorithms for Propositional Logic* ([D232](#d232)); complete *LM Modal Bridge Report* ([D257](#d257)); canonical theorem bank ([D200](#d200)/[D201](#d201)) and claim registries; the 12-page findings consolidation ([D173](#d173)); original process-research stub ([D295](#d295)); historical P01/P02 skeletons and P01 version snapshots. Much of their subject matter migrated into publication papers, but these are not interchangeable copies.
4. **PUB-only preservation priorities:** *Finite-Jet Rigidity and Ultradifferentiable Realization of Boolean Sign Laws on Orthants and Hyperplane Arrangements* ([D331](#d331)/[D332](#d332)), a genuinely distinct paper; the editable LM-centered foundations source ([D325](#d325)); the Astra foundations audit ([D326](#d326)/[D327](#d327)); and ProLT v0.8.1 source, PDF and release record ([D336](#d336)/[D337](#d337)). ProLT is a newer version of a family already in CM, not a wholly unmatched topic.
5. **The master inventory is broader than the manuscripts.** Foundations/coherence, phase algebra, chain-ring contextuality, teleportation corrections, query obstructions and many negative results have substantial homes. The complete compact-CM spectral/dynamical classification is only partly preserved. The logical-Lie, simultaneous-diagonalization, complex-fuzzy-truth, Bector/B-module and time-evolving-LM investigations were not found as substantive treatments. Bibliographic occurrences of “fuzzy” and ordinary module terminology do not count as coverage.
6. **There are concrete packaging defects.** Both portfolio copies of Paper B refer to a missing `../04_figures/` directory containing notation macros and four PNG figures. Those assets survive in the original CM consolidation tree. The Astra audit refers to a bundled checker and spectral tables that are not present in either inspected root. The 20,873-check output survives, but its matching checker was not located. A saved PDF is therefore not enough to establish a reproducible source package.
7. **Nine old audit-manifest mismatches are real but mostly non-substantive:** eight changed JSON byte streams parse to equal JSON values; the ninth is changed timing data. The expected historical hashes are still represented in CM Quantum. Preserve both runs and document the manifest state rather than “repairing” the old manifest in place.
8. **The inventory itself needs a few status corrections.** P01 and P02 already contain written general proofs, rather than only conjectures/plans. The process companion gives a closed *binary* completion with changed operations, while unchanged nonzero-A independence remains obstructed. The intrinsic phase paper expressly corrects “degenerate Hermitian pairing” to **nondegenerate pairing with isotropic self-product**. Its 1,500 DAG check count means internal nodes in 50 DAGs.

This is a preservation and coverage audit, not independent certification of every mathematical proof, novelty claim or historic benchmark. “Full treatment” means a substantial written treatment was located; it does not mean the claim is externally verified or suitable for publication without review.

## Scope, evidence and limits

The requested inventory was found at:

`C:\Users\brian\Downloads\CM_LM_Research_Threads_Master_Topic_Inventory_2026-09-25.md`

The requested `/mnt/data` attachment/output mount is not available in this Windows session. Deliverables are saved in this task's `outputs` directory. The local inventory was read directly; the inaccessible conversation attachment was not invented or substituted with a reconstructed topic list.

Root abbreviations in this report:

| Code | Absolute root |
|---|---|
| CM | `C:\Users\brian\Documents\CM Quantum` |
| PUB | `C:\Users\brian\Documents\Math Latex etc\Papers for Publication` |

All discovered non-ZIP file types were inventoried and hashed; **29 ZIP instances were excluded and never opened**. All 22 distinct PDFs yielded text using `pypdf`, and all 31 distinct TeX objects were read as text. MiKTeX's `pdftotext` executable reported an unfinished installation, so extraction used the already-installed Python reader. No TeX setup changes or source compilation were attempted. Mathematical symbols in PDF extraction can be imperfect; available TeX was preferred for equations and source anchors. This was not a rendered-page typography or image-only figure audit. No PDF was wholly unextractable.

Evidence levels:

- **Exact copy:** equal SHA-256 of the complete file, not a filename inference.
- **Same family / revision:** aligned title, mathematical contract, section structure and actual additions/deletions. Where helpful, the report gives normalized five-word-shingle overlap. These are word-overlap diagnostics, not probabilities or mathematical-equivalence certificates. Formula extraction and layout lower cross-format scores, so they are never used alone to reject equivalence.
- **Substantively overlapping but distinct:** results distributed between a bank/report and more focused papers, with particular retained or omitted sections identified.
- **Absent / not located:** targeted phrase/concept searches plus manuscript/section review did not locate the stated result inside these roots. This is not a claim that it never existed in a conversation, other local folder, unexamined ZIP, figure or external repository.

The coverage matrix uses the inventory's original numbered sections. **F = full/substantial treatment; P = partial treatment or mention, with omitted subclaims stated; A = absent/not located.** Technical reports and theorem banks are identified as such, rather than counted silently as submission manuscripts. A source ID links to its file/hash ledger. TeX/Markdown locators are original source line numbers; PDF locators refer to extracted text or explicitly named sections/pages. Historical material can be fully covered but superseded: coverage and correctness status are different dimensions.

Read-only SHA comparisons, dependency resolution, text searches and generated-report consistency checks were executed for this audit. Inherited manuscript statements that “tests passed” are reported as inherited evidence, not as mathematical tests rerun now. No user research script was executed, because many write results into their source trees.

## Manuscript families and cross-directory equivalence map

| Family | Objects and identity | Cross-directory finding | Preservation conclusion |
|---|---|---|---|
| F01 Historical CM source | [D232](#d232), 29-page *Correspondence Matrices; Algorithms for Propositional Logic* | CM only; modern foundations/compiler works absorb selected content, not an exact replacement | Preserve historical derivations, quotient/decomposition examples and correction provenance |
| F02 LM-centered foundations | [D075](#d075) PDF; [D325](#d325) TeX | PDF is byte-identical despite different names; source exists only in PUB | Preserve PUB source and notes with PDF; source cannot be reconstructed losslessly from CM's PDF |
| F03 Operator-level computation / Paper B | [D233](#d233) 19-page; [D169](#d169) 21-page; [D110](#d110)/[D111](#d111) 24-page evidence-updated version, [D107](#d107) proof appendix | 19-page snapshot CM only; 21- and 24-page states both roots; PUB handoff “current.pdf” equals D110 | Same evolving family; keep evidence-updated version and historical snapshots; restore a complete archive copy of build assets later |
| F04 Signed phase/quantum encoding | [D165](#d165)/[D166](#d166), 33-page verified phase calculus | Exact copies both roots | Distinct signed/integral-lift branch, not superseded wholesale by pure-Boolean phase paper |
| F05 Intrinsic Boolean phase algebra | [D167](#d167)/[D168](#d168), 26-page manuscript | Exact copies both roots | Preserve unitary/splitter inventory, phase-ANF theorem, nilpotent bounds and correction appendix |
| F06 Pure modal addendum | [D074](#d074), TeX only | Exact copies both roots inside historical snapshots | Not safe current authority for unqualified finite-copy no-activation; retain with D034 corrections |
| F07 Correctness audit | [D033](#d033) 28-page PDF; [D034](#d034), [D035](#d035), [D036](#d036) | Exact manuscript copies both roots; some supporting JSON differs from old digest | Canonical correction history and model ledger; standalone TeX inlines generated tables, not another paper |
| F08 P01 chain-ring resources | [D086](#d086)/[D087](#d087), 11-page mature draft; [D214](#d214)/[D215](#d215) skeleton; [D307](#d307)/[D308](#d308) history | Mature draft both roots; skeleton/history CM only | General Smith/Hardy/coding/teleportation proof paper; preserve proof/priority revision trail |
| F09 P02 query bounds | [D098](#d098)/[D099](#d099), nine-page mature note; [D224](#d224)/[D225](#d225), six-page skeleton | Mature note both roots; skeleton CM only | Renamed “Obstructions” to “Bounds”; proof-bearing mature note, not a missing second query paper |
| F10 LM-modal bridge | [D257](#d257), full TeX report | CM only; short interface in P01 and related material in theorem bank | Full report not represented in PUB at comparable detail; preserve checks and proofs with it |
| F11 Theorem bank | [D200](#d200)/[D201](#d201), 18-page bank; [D203](#d203)/[D204](#d204)/[D205](#d205) support | CM only; central results split into P01/P02 and other papers | Preserve uncopied supporting propositions and 71-claim crosswalk |
| F12 Process semantics | [D149](#d149)/[D151](#d151) nine-page companion; [D128](#d128) verification note; [D295](#d295) earlier stub | Companion and later note both roots; original stub CM only | Three substantively overlapping documents, not equal versions merely because named main.tex |
| F13 Findings consolidation | [D173](#d173), 12-page status report | CM only | Broad synthesis, not independent theorem paper; keep as correction and research-history map |
| F14 ProLT | [D170](#d170) v0.6, 15 pages; [D324](#d324) v0.8, 18 pages; [D336](#d336)/[D337](#d337) v0.8.1, 19 pages | v0.6 both roots; v0.8 CM only; v0.8.1 source/PDF PUB only | Same family with substantial v0.6→v0.8 revisions and modest v0.8→v0.8.1 clarification; retain deferred historical material |
| F15 Finite-Jet Rigidity | [D331](#d331)/[D332](#d332), 13-page submission candidate | PUB only, no substantive CM counterpart located | Genuinely distinct paper beyond inventory's main CM/modal subjects; high-priority preserve |
| F16 Publication map | [D208](#d208)/[D209](#d209), one-page map | CM only | Planning/ownership record, not separate paper; useful history of splits and deferred topics |
| F17 Foundations Astra audit | [D326](#d326)/[D327](#d327), Markdown + 21-page PDF | PUB only | Substantive correction/novelty/finite-check record; not an independent foundations manuscript; linked checker/data missing |

All remaining TeX objects are accounted for in the object ledger: proof appendix, generated tables, evidence-update fragment, phase/Smith tables, macros, definitions and bibliography. They must not be inflated into separate paper counts.

## What is missing in each direction

### CM Quantum material not fully represented in Papers for Publication

**Distinct or materially fuller research documents:** D232 historical original; D257 bridge report; D200/D201 theorem bank; D173 consolidated report. These deserve preservation even where their headline results overlap newer papers.

**Same-family historical versions:** D214/D215 P01 skeleton, D224/D225 P02 skeleton, D307/D308 P01 snapshot, D233 19-page Paper B, D324 ProLT v0.8, D295 process stub. None should be called a wholly new paper just because its hash is absent from PUB. The version analysis below identifies what survives or changes.

**Supporting source/evidence:** D198 bibliography fragment, D203/D204/D205 model/definition/notation files, D209 publication map and D284 notation macros. The consolidation's claim registry, source snapshots, capability report, formal theorem list, adversarial reviews, raw S1/S2 material, earlier protocols and process development records also contain preserved research not duplicated by the portfolio. The complete manifest records **459 distinct CM-only file contents (611 file instances)**; the unmatched-object appendix inventories them without pretending every log or CSV is a paper.

### Papers for Publication material not fully represented in CM Quantum

There are **13 distinct PUB-only file contents**, with no extra repeated instances:

- F15's PDF and source: truly distinct finite-jet/orthant/hyperplane-arrangement mathematics.
- F02's editable source: mathematical content represented by the exact same PDF in CM, but the editable/buildable source is unique.
- F17's PDF and Markdown: audit text is unique; includes polarity-mask failure details, additional structural suggestions, historical-source counterexamples, prior-art review and verification scope.
- LM revision notes, verification output and handoff manifest: unique context/evidence files, not separate manuscripts.
- ProLT v0.8.1 PDF/source/README/release notes/hash file: newer same-family release, not a missing unrelated paper.

## Detailed version, split/merge and divergence findings

### V1. Two renamed PDFs are exact matches

The root CM foundations filename `CM_LM_Boolean_Operator_Calculus_LM_Centered_V1.pdf` and PUB's long `Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.pdf` are **D075**, SHA-256 `ca4c64497e29c40e7398746ef57550f5915e5ce7b5be480cc579dc13601bb4ca`.

PUB's `Operator-Level_Boolean_Computation_with_Correspondence_Matrices_current.pdf` is **D110**, SHA-256 `a02ba8aded23edd94b5f816bbf6b5f8afee881576762eb89371eb884613c4133`, equal to the 24-page portfolio/consolidation PDF. It is **not** the root CM's similarly named 21-page D169. This resolves a potentially consequential filename trap.

### V2. Paper B has three real content states

The 19-page D233 and 21-page D169 share 62.87% five-word-shingle Jaccard overlap; 82.63% of D233's distinct shingles occur in D169. The 21-page D169 and 24-page D110 share 81.12% Jaccard overlap; 96.49% of the older state's shingles occur in D110. This supports a revision family but is not a guarantee every formula/history note survived.

The 21-page state develops the typed S/R/H compiler contract and strategy/root outcomes more explicitly than the 19-page snapshot. The 24-page state adds the S1/S2 recount and P14-PY0 negative dispatcher study. D111 lines 1145–1167 preserve 10,500 generated/10,389 fully admitted cases and seven exact metric ties; lines 1184–1238 preserve the frozen corpus, decision threshold, ratios, amendments and P15 no-timing boundary. The 21-page abstract says no performance result before its broader campaign; the 24-page abstract distinguishes that unexecuted protocol from an independently completed negative ANF-dispatch campaign. These are evidentiary changes, not formatting.

The foundations/compiler split is substantive: D325 expands symbolic LM architecture and arbitrary arity, whereas D111 owns implementation contracts and empirical evidence. Do not replace the compiler paper with the foundations paper or infer that one broad title subsumes both.

### V3. P01 historical source is almost contained, with a meaningful later qualification

D308→D087 source comparison has **97.29% Jaccard overlap; 99.71% of old shingles occur in the current source**. The direct line diff changes the date from 18 to 19 September, adds the state-admissibility comparison with de Beaudrap and the nine-row-analyzer distinction from Varughese, and removes a page break before the resource map. The added paragraph explains why the nonprimitive nilpotent separator is excluded from a competing primitive-state model. This is an important assumption/priority qualification, even though the theorem core is unchanged.

D307 old PDF and D086 current PDF have 90.06% overlap. D215 skeleton is a different planning artifact, with drafting instructions and theorem-bank references; its mathematical center is represented in current P01. Preserve the skeleton as provenance, not as an additional completed article.

### V4. P02 matured and was renamed

D225's *Exact Query Obstructions* skeleton becomes D099's *Exact Query Bounds*. Both explicitly distinguish lower bounds for arbitrary fixed invertible pointwise gates from upper bounds available under informative standard XOR access. The mature note writes the adaptive recorded-branch proof and includes kickback/Fourier separation and known UNIQUE-SAT. Shared subject matter and exact theorem contracts establish family identity despite low literal overlap with the outline. Do not revive a blanket “Deutsch=2 for any G0,G1” statement when G0=G1 may convey no information.

### V5. The bank was split across papers, not preserved wholesale by them

D201 consolidates 71 claim IDs, proof provenance and exclusions. P01 inherits contextuality/Hardy/coding/resource comparisons; P02 inherits exact-query results; other material remains in the audit/phase/process manuscripts. Particularly easy-to-miss bank content includes:

- General regular N-cycle centralizer/rank and the distinction between cyclic valuation and elementary-abelian/Reed-Muller total-degree filtration (lines 76–129).
- Complement as translation, reversal versus inversion, and why the compact identity CM's lift cannot preserve the original product (132–154).
- Qualified deterministic no-deletion and exact retained-syndrome direct-sum criterion, with a noninjective deletion counterexample (700–724). These go beyond the inventory's simple no-cloning label.
- The finite six-context GHZ certificate and the 101,583 smaller-subset checks, with the warning that this is not universal six-context minimality (730–736).
- The weak 18-positive-event probability completion versus faithful completion distinction (738–745).

The corresponding full capability report/formal-theorem files [D264](#d264)/[D266](#d266) also survive only in CM. They should be retained even if no additional publication is pursued.

Another stronger bank statement deserves explicit retention: D201 lines 465–496 gives the transpose-orthogonal span dimension `(d-1)^2+1` for `d>=2` and hence dimension **50** at d=8, rather than only the older bound of 63. It also distinguishes this from a common-bilinear-form obstruction for the native shear/phase pair. The broader bank statement should not be reduced to the inventory's even-dimensional headline.

### V6. The full bridge report is not replaced by the short P01 appendix

D257 includes algebraic characterization of the restricted 16-LM family, the idempotent obstruction, scalar enrichment, support predicates, effect-family limitations, division-free updates, projective well-definedness and explicit verification tables. Its lines 934–936 record **144 of 256 ordinary Boolean matrix products leaving the restricted 16-LM family**. P01 lines 264–292 provide a short conditional interface; they do not reproduce the full update theory/check record. This is a materially fuller CM-only document even though “LM bridge” is mentioned in PUB.

### V7. Process research has successive dispositions and distinct operation contracts

D295 is the earlier *Independence, Conditioning, and Restricted Resources* stub; D151 is the 20 September *Process Closure and Restricted Conversion* companion; D128 is the later *Verification Note*. Their low literal shingle overlap (4.24% D295/D151; 1.94% D295/D128) does not make them unrelated: the sections track independent-success obstruction, closed field-modal completion, Frobenius/coarse support, marked normalizer, Smith filtering and collective resource conversion.

D151 contains the explicit distinction between retaining all phase registers and resolved phase disposal; its two-copy witness and mixed state after forgetting labels are not captured by a simplistic no-activation summary. D128 lines 199–212 explicitly says the results already occur in the companion and recommends a verification supplement rather than a fourth full paper. Keep all three as research history; the mature companion is the clearest current treatment, not a reason to erase the stub.

### V8. ProLT v0.8.1 is newer; v0.6 retains material deliberately removed

D324 v0.8→D336 v0.8.1 has **86.23% Jaccard overlap**, with 94.30% of v0.8 shingles retained. Content additions clarify the intended reader, define `Top`, distinguish indexed/weighted presentation data from the topology, expand the nerve triangle's intersections and add a Vickers reference. The release notes [D334](#d334) explicitly say no theorem/proposition/corollary/proof was replaced. Text comparison supports a modest clarification release; it is not an independent proof audit of that claim.

D170 v0.6→D324 v0.8 has only **44.72% Jaccard overlap**. The later text sharply separates positive certificates from complete profiles, topology from presentation, and nerve homology from topology homology; it includes a tautology/cone warning and more precise contextuality boundaries. The old v0.6 sections on cognitive interpretation, quantum interpretation, filters/limits and infinite languages are removed or compressed. They are exploratory ideas, not lost proved theorems, but preserving v0.6 is necessary to retain that history.

### V9. “Verified phase” and “intrinsic phase” are different branches

D166 develops the integral/signed lift, Gaussian integers, exact Clifford+T encoding and phase-path representation. D168 develops the intrinsic characteristic-two chain ring, unitary/splitter census, phase-ANF encoding and nilpotent interaction bound. Both are long manuscripts with distinct claims and appendices. A newer modal/resource paper does not subsume either entire branch. Preserve the signed-lift warning, unitary-versus-Hamming distinction and intrinsic norm correction with their original context.

### V10. Superseded modal claims coexist with corrected manuscripts

D074 still contains a theorem headed **“Postselection and finite-copy no activation”** (line 381). D034's literal heralded activation theorem (568) and D151's resolved-disposal witness (340) demonstrate why that headline cannot be used across changed tensor/filter contracts. This is not evidence that every restricted theorem is false. It is evidence that historical statement, permitted operations and later correction must travel together.

The two correctness-audit TeX forms are a different case: replacing D034's `input{generated_tables.tex}` with the complete D036 text produces D035 **exactly**, under the same decoded newline convention. The standalone source is therefore an inlined build convenience, not a substantively divergent audit.

## Integrity, source completeness and reproducibility risks

### Paper B build assets

D111 line 26 sets `graphicspath` to `../04_figures/`; line 27 unconditionally inputs `CM_PAPER_NOTATION_MACROS.tex`. The two portfolio copies lack that directory. Four figure includes (lines 266, 382, 533, 717) therefore also fail local resolution. In the original consolidation path, the same source hash still has its sibling `04_figures` folder and the dependencies resolve. Preserve that original folder structure, including D284, all four figure PNGs and bibliography. The source audit resolves declared `graphicspath`; these are not false positives from looking only beside `main.tex`.

The evidence-update fragment D120 refers to `p14_rows` as if used in the manuscript working directory; treated as a standalone document in `research_and_review`, it does not resolve. It is a fragment, not necessarily a broken standalone paper. D308's isolated historical source snapshot likewise needs its contemporary Smith table and bibliography restored beside it to compile. No build was attempted.

### Claimed verification files that were not located

D326 lines 698–703 says the audit includes spectral tables and a `verify_cm_lm.py` program. Neither that program nor the named spectral output package was found in the inspected roots. D328/D329 record a separate 20,873-check foundations run, but the associated executable checker was also not located in that handoff. This does not disprove the reported checks; it means these directories do not currently preserve their full runnable evidence. The handoff manifest D330 itself says implementation/raw benchmark material is not all included. Do not equate that prose with a complete supplement.

### Old manifest discrepancies

The two portfolio audit copies carry the same nine mismatches against their embedded `MANIFEST_SHA256.txt`: eight parse-equivalent JSON reserializations and one altered `audit_timing.json`. Historical byte versions matching all nine expected hashes were located in CM. Therefore **the old manifest is stale relative to the copied run**, and **the evidence of original byte identity is still recoverable**. Mathematical data corruption was not demonstrated by these mismatches. The companion verification note had already documented nine pre-existing mismatches; this audit independently checked them.

Some manifests refer to ZIPs (intentionally excluded), deleted build intermediates, or files copied to another path. These are separated from substantive absent files in the manifest appendix. For missing non-ZIP entries, expected hashes are searched throughout both roots, so a recoverable relocated copy is not mislabeled lost. In particular, several bridge input-snapshot data files have surviving exact copies elsewhere; the root-level companion PDF was relocated to `build/main.pdf` and another root filename.

## Prioritized “do not delete / archive carefully” list

| Priority | Preserve together | Why |
|---|---|---|
| P0 | Complete CM consolidation tree, especially D201/D257/D232, claims, model contracts, proof provenance and source snapshots | Publication portfolio is only a selection; proof/history/evidence not wholly represented there |
| P0 | PUB `Finite Jet Rigitity (Paper A)` PDF + TeX | Distinct manuscript absent from CM; strong independent mathematical subject |
| P0 | PUB LM-centered TeX, Astra audit Markdown/PDF and revision/verification records | Editable foundations source and full audit absent from CM despite duplicate foundations PDF |
| P0 | Original Paper B `04_figures` + `05_manuscript`, appendix, tables and bibliography | Copied portfolios omit required build dependencies; original tree is the recoverable complete source context |
| P1 | ProLT v0.8.1 source/PDF/release notes/hash file plus older v0.6/v0.8 PDFs | New release is PUB only; older version retains deferred cognitive/quantum/infinite-language discussion |
| P1 | Correctness audit + historical modal addendum + correction ledgers + original and copied JSON runs | Prevent regression to wrong tensor, no-activation, teleportation or probability claims; preserve provenance of stale manifest |
| P1 | Intrinsic and signed phase manuscripts, appendices and available verification packages | Different mathematical branches; phase-ANF/nilpotent and signed Clifford results are not replaced by P01/P02 |
| P1 | Process companion + both P03 stubs/notes + resolved-disposal data | Distinct operation classes and disposition history; “closure” or “activation” alone is insufficient indexing |
| P1 | Raw S1/S2 records, P14 evidence/reconciliation, negative results and old protocols | Failed speed/dispatcher claims and support-generator corrections are scientifically meaningful boundaries |
| P1 | Master topic inventory itself | It is the only located explicit record of several historical threads and detailed spectral claims; not all claims are yet manuscript-backed |
| P2 | P01/P02 skeletons, isolated P01 snapshots, publication map, broad consolidation report and handoff prompts | Preserve authorship/history/scope decisions; don't count them as additional completed papers |

Recommended preservation action, **not performed**: create a separate archival bundle that retains both roots' relative paths, all distinct content hashes, paper-family/version links, correction status and the original master inventory. Copy missing build assets into an archive copy, not into the untouched source tree. Retain exact byte copies before any normalization. Verify that archived files match this manifest and that the archive can restore the complete original Paper B source layout. Same-drive duplicate directories are not independent protection against device loss.

Next, recover the missing spectral/history conversation exports and foundations verification bundle into that archive, then update only the uncovered topic rows. This audit does not authorize deleting duplicates: exact-copy identity does not establish that a directory's dependencies, provenance or archival role are redundant.

The most efficient follow-up remains in this task, reusing the object IDs, hashes and evidence. A routine file-copy/hash-verify follow-up can use a low-reasoning coding-capable model; a substantive recovery/proof reconciliation should use a high-reasoning model. No measured model pricing comparison is available here. Creating an archive or changing source files requires a separately scoped request; no further action is required to use this report.

## Topic coverage matrix keyed to the master inventory

The following matrix treats the numbered topic units individually and names material subtopic gaps. Repeated checklists are cross-referenced afterward. Findings labeled F in a report/bank should not be mistaken for placement in a submission manuscript: the family map identifies document roles and each evidence ID identifies the actual file.

**193 individually assessed units:** 145 full, 43 partial, 5 absent. These counts include overview/open/correction rows and must not be interpreted as 193 independent new results.

| Inventory topic | Coverage | Located evidence | Assessment and material caveats |
|---|---|---|---|
| <a id="topic-2.1"></a>2.1 CM/LM foundations and Boolean operator calculus (inventory L41) | Full treatment | [D325](#d325) L290–1149 | Foundations paper develops symbolic lift, valuation, pairing, alignment, coherence, arbitrary arity and block/rank constructions; this is the fullest present home. |
| <a id="topic-2.2"></a>2.2 CM computation / compiler research (inventory L61) | Partial / mention | [D111](#d111) L795–1244; [D007](#d007) L1–520 | Compiler architecture and negative evidence are substantial; persistent-cache performance and the precise discarded-child implementation history are not fully retained in the manuscript. |
| <a id="topic-2.3"></a>2.3 Pure-Boolean phase / rotation algebra (inventory L82) | Full treatment | [D168](#d168) L279–520; [D201](#d201) L73–155 | Dedicated intrinsic-phase manuscript and theorem bank; keep cyclic convolution distinct from compact CM matrix multiplication. |
| <a id="topic-2.4"></a>2.4 Boolean modal / quantum-information laboratory (inventory L97) | Full treatment | [D034](#d034) L342–647; [D087](#d087) L84–254; [D099](#d099) L80–224 | Covered collectively across correctness audit, P01 and P02; each result has a different operation/measurement contract. |
| <a id="topic-2.5"></a>2.5 Canonical LM-to-modal bridge (inventory L117) | Full treatment | [D257](#d257) L84–137; [D257](#d257) L332–809 | Dedicated bridge report survives only in CM; abbreviated chosen scalar-extension interface is in P01. |
| <a id="topic-2.6"></a>2.6 Spectral/dynamical classification of the 16 compact CMs (inventory L128) | Partial / mention | [D325](#d325) L1340–1406; [D326](#d326) L423–447 | Representative spectra and a finite atlas summary survive. The complete similarity/functional-graph/frame-spectrum program is not a developed manuscript here. |
| <a id="topic-2.7"></a>2.7 Historical quantum-style CM/LM exploration (inventory L144) | Partial / mention | [D166](#d166) L506–812; [D168](#d168) L825–838 | Signed quantum lift survives, but most early fuzzy/cognitive/Bector/time-dependent investigations are not found. See 33.1-33.8 individually. |
| <a id="topic-3.1"></a>3.1 The 16 compact binary CMs (inventory L166) | Full treatment | [D325](#d325) L88–287; [D111](#d111) L167–338 | All compact binary kernels, true-first convention, XOR/XNOR and transformation notation are treated. |
| <a id="topic-3.2"></a>3.2 Bra-ket construction and contraction (inventory L196) | Full treatment | [D325](#d325) L88–287; [D107](#d107) L10–60 | One-hot bras/kets, elementary outer products, indexed XOR-AND contraction and selection proofs; physical interpretation explicitly bounded. |
| <a id="topic-3.3"></a>3.3 Matrix transformations corresponding to logical transformations (inventory L208) | Full treatment | [D325](#d325) L224–287; [D325](#d325) L1071–1120; [D111](#d111) L340–469 | Input flips, operand exchange, output complement and signed alignment treated. Output complement is distinguished from unchanged-outer-operation input actions. |
| <a id="topic-3.4"></a>3.4 General finite expressions and higher-dimensional CMs (inventory L223) | Full treatment | [D325](#d325) L643–791; [D325](#d325) L917–1120 | Arbitrary-arity truth tensors, ordered rectangular flattenings, conditional block lifts and rank/separability; no claim that every function has a given block decomposition. |
| <a id="topic-3.5"></a>3.5 Measurement / reconstruction / quotienting / conditioning (inventory L240) | Partial / mention | [D232](#d232) PDF, extracted L526–570 (around p. 10); [D325](#d325) L1018–1070; [D111](#d111) L795–846 | Historical feature quotient and later reconstruction/separability survive, but the full conditioning/reconstruction/partial-output experimental program is not developed together. |
| <a id="topic-4.1"></a>4.1 Formula-valued LM layer (inventory L257) | Full treatment | [D325](#d325) L290–358 | Formula Boolean algebra, polarity orbit and invertible symbolic frame normal form distinguish LM from numeric CM. |
| <a id="topic-4.2"></a>4.2 Canonical term lift (inventory L266) | Full treatment | [D325](#d325) L290–358; [D325](#d325) L643–725 | Canonical formula lift and arbitrary-arity definition are explicit. |
| <a id="topic-4.3"></a>4.3 LM to CM valuation (inventory L277) | Full treatment | [D325](#d325) L359–389; [D257](#d257) L302–331 | Coefficient valuation and naturality have statements/proofs. |
| <a id="topic-4.4"></a>4.4 Logical pairing (inventory L287) | Full treatment | [D325](#d325) L390–511; [D111](#d111) L713–794 | Agreement-bit pairing and labelled basis reconstruction are explicit, including dependent external formulas. |
| <a id="topic-4.5"></a>4.5 Pairing/valuation coherence (inventory L301) | Full treatment | [D325](#d325) L792–916 | Coherence theorem and higher-arity pairing explain commuting symbolic/numeric operations. |
| <a id="topic-4.6"></a>4.6 Operator-on-operator Boolean superposition (inventory L312) | Full treatment | [D325](#d325) L512–641 | Aligned symbolic operator superposition is central; numerical same-frame operation is a valued corollary with prior-art limits. |
| <a id="topic-4.7"></a>4.7 Signed-frame actions (inventory L326) | Full treatment | [D325](#d325) L321–358; [D325](#d325) L1071–1120 | Binary frame factorization and arbitrary signed-variable frame action are developed. |
| <a id="topic-4.8"></a>4.8 Polarity-mask correction (inventory L343) | Full treatment | [D325](#d325) L752–790; [D326](#d326) L58–58; [D326](#d326) L701–703 | Corrected action uses pi_delta, explicitly distinguished from rho indexed by valuation. The 48/64 failure history survives in the PUB-only Astra audit, not as a fresh failure in the revised paper. |
| <a id="topic-4.9"></a>4.9 All-true valuation / existence assumptions (inventory L352) | Full treatment | [D325](#d325) L290–290; [D325](#d325) L359–376 | Joint satisfiability is required for substituted all-true reference formulas; free generators have the specialization. |
| <a id="topic-5.1"></a>5.1 Boolean closure of operator superposition (inventory L363) | Full treatment | [D325](#d325) L512–641; [D325](#d325) L726–750 | Pointwise Boolean closure and the LM image as a Boolean subalgebra are proved. |
| <a id="topic-5.2"></a>5.2 Symbolic-to-numeric commuting diagrams (inventory L369) | Full treatment | [D325](#d325) L792–864 | Explicit coherence theorem and diagram. |
| <a id="topic-5.3"></a>5.3 Higher-arity closure (inventory L385) | Full treatment | [D325](#d325) L643–916; [D325](#d325) L917–1120 | General arity, pairing, flattenings and aligned frame compatibility treated. |
| <a id="topic-5.4"></a>5.4 ANF parity bridge (inventory L396) | Full treatment | [D325](#d325) L1121–1176; [D168](#d168) L537–596 | Top ANF coefficient/parity and the distinct phase-Mobius transform both have homes; do not identify them as the same map. |
| <a id="topic-6.1"></a>6.1 Rank and determinant (inventory L414) | Partial / mention | [D325](#d325) L1018–1070; [D326](#d326) L429–437 | Rank/separability theorem is full. The specific alpha_X alpha_Y XOR alpha_0 alpha_XY determinant identity was not located explicitly; retain it separately. |
| <a id="topic-6.2"></a>6.2 The six invertible matrices (inventory L425) | Partial / mention | [D326](#d326) L429–437; [D325](#d325) L1352–1377 | Six invertibles and OR/NAND spectral examples are recorded. Explicit GL_2(F_2)~S_3 and OR^2=NAND/OR^3=XNOR classification was not located in manuscript text. |
| <a id="topic-6.3"></a>6.3 Nilpotent / idempotent / involutive behavior (inventory L442) | Partial / mention | [D325](#d325) L1352–1388; [D326](#d326) L429–437 | Eight idempotents/four symmetric idempotents, XOR involution and tautology nilpotence recorded; full functional-graph/iteration atlas not preserved as a manuscript. |
| <a id="topic-6.4"></a>6.4 Polynomial and similarity classification (inventory L454) | Partial / mention | [D326](#d326) L429–447; [D325](#d325) L1340–1388 | Four characteristic-polynomial classes and splitting examples are in the audit. Six similarity/minimal-polynomial classes and six graph types were not located as explicit results. |
| <a id="topic-6.5"></a>6.5 Frame and valuation spectra (inventory L463) | Partial / mention | [D325](#d325) L1401–1406; [D326](#d326) L443–447 | Valuation spectral profile defined and left/right versus similarity caveat stated. Affine iff equal frame spectra and recovery of six orbits by minimal-polynomial multisets not found. |
| <a id="topic-6.6"></a>6.6 Pointwise superposition audit (inventory L471) | Partial / mention | [D325](#d325) L512–641; [D326](#d326) L684–701 | Exhaustive pointwise fusion/coherence is documented. Structural-subset closure claims, AND preserving singularity and full invertibility/idempotence counterexample census were not located explicitly. |
| <a id="topic-6.7"></a>6.7 Semigroup / Cayley / commutation questions (inventory L481) | Partial / mention | [D327](#d327) PDF, extracted L518–518 (around p. 12) | Semigroup dynamics is mentioned as deferred. No full multiplication/Cayley/centralizer/Green-relation paper for the 16 compact CMs found. The four-cycle centralizer is a different result. |
| <a id="topic-7.1"></a>7.1 The order-four rotation `R` (inventory L498) | Full treatment | [D168](#d168) L279–315; [D034](#d034) L184–207 | Literal four-cell rotation and faithful regular representation treated. |
| <a id="topic-7.2"></a>7.2 The 16-element centralizer / circulant algebra (inventory L506) | Full treatment | [D034](#d034) L200–207; [D201](#d201) L76–99 | Exact cyclic commutant with proof; 16 circulant operators for N=4. |
| <a id="topic-7.3"></a>7.3 Group algebra and chain-ring identification (inventory L514) | Full treatment | [D168](#d168) L279–298; [D201](#d201) L76–99 | Explicit group algebra/chain-ring identification with added convolution product. |
| <a id="topic-7.4"></a>7.4 Nilpotent filtration (inventory L528) | Full treatment | [D168](#d168) L317–351; [D201](#d201) L76–129 | Ideal filtration and binary rank N-a; cyclic valuation is explicitly separated from total-degree Reed-Muller filtration. |
| <a id="topic-7.5"></a>7.5 Units and nilpotents (inventory L539) | Full treatment | [D168](#d168) L317–351; [D168](#d168) L847–871 | Eight units, nilpotents and complete scalar classification. |
| <a id="topic-7.6"></a>7.6 Boolean degree versus lifted reversibility (inventory L549) | Full treatment | [D201](#d201) L102–129; [D168](#d168) L695–706 | Full-degree/parity iff invertibility of cyclic lift. This is about the lifted operator, not invertibility of the original 2x2 CM. |
| <a id="topic-7.7"></a>7.7 Operand reversal and phase reversal (inventory L561) | Full treatment | [D201](#d201) L132–154; [D168](#d168) L379–398 | Reversal conjugates R to R inverse; generally not inversion of every algebra element. |
| <a id="topic-7.8"></a>7.8 Complement and the deepest nilpotent layer (inventory L569) | Full treatment | [D201](#d201) L132–154 | Complement adds u^(N-1); translation, not multiplication by that element. |
| <a id="topic-7.9"></a>7.9 Transpose/conjugation analogue (inventory L577) | Full treatment | [D168](#d168) L379–398; [D201](#d201) L132–154 | Transpose/star and phase-reversal identities explicitly treated. |
| <a id="topic-7.10"></a>7.10 Degenerate norm (inventory L583) | Full treatment | [D168](#d168) L421–438; [D168](#d168) L934–934 | Preserve a correction to the inventory: self-product is isotropic/non-positive, while the free-module Hermitian pairing is nondegenerate. No Born norm follows. |
| <a id="topic-8.1"></a>8.1 Intrinsic star-unitaries (inventory L598) | Full treatment | [D168](#d168) L454–481; [D168](#d168) L877–890 | Intrinsic unitary classification, 512 count and restricted readout obstruction; not the same set as 512 shell preservers. |
| <a id="topic-8.2"></a>8.2 Mixer / splitter operators (inventory L611) | Full treatment | [D168](#d168) L482–520; [D034](#d034) L232–251 | Explicit reversible shears/splitters and detector profiles; 22,528 splitters overall, 8,192 with the specified profile. |
| <a id="topic-8.3"></a>8.3 Rotation is not itself the mixer (inventory L630) | Full treatment | [D168](#d168) L482–520; [D166](#d166) L449–505 | Rotation alone does not create the mixer; Hamming-isometry and ring-unitary notions are distinct. |
| <a id="topic-9.1"></a>9.1 Interference as characteristic-two cancellation (inventory L643) | Full treatment | [D034](#d034) L232–251; [D168](#d168) L482–520 | Explicit characteristic-two cancellation/interferometer constructions. |
| <a id="topic-9.2"></a>9.2 Shear / interferometer constructions (inventory L653) | Full treatment | [D201](#d201) L132–146; [D168](#d168) L482–520 | W D_k W construction and branch formula are stated/proved. |
| <a id="topic-9.3"></a>9.3 Zero-divisor cancellation (inventory L657) | Full treatment | [D034](#d034) L288–297; [D151](#d151) L88–119 | Nonzero nilpotent events/tensor factors can multiply to zero; concrete obstruction preserved. |
| <a id="topic-9.4"></a>9.4 Limitation (inventory L663) | Full treatment | [D168](#d168) L409–438; [D034](#d034) L623–647 | Possibility/cancellation is not a positive probability or physical interference law. |
| <a id="topic-10.1"></a>10.1 Phase-Mobius / ANF theorem (inventory L678) | Full treatment | [D168](#d168) L521–596 | Phase-ANF encoding, Boolean shear transform and subset-interval kernel treated with proofs. |
| <a id="topic-10.2"></a>10.2 Exhaustive verification (inventory L692) | Full treatment | [D168](#d168) L872–924 | 65,812 truth-function checks, 65,808 kernel pairs and 1,500 DAG internal nodes recorded. Inventory's '1,500 examples' should be read as nodes of 50 DAGs, not 1,500 independent DAGs. |
| <a id="topic-10.3"></a>10.3 Nilpotent interaction bound (inventory L702) | Full treatment | [D168](#d168) L634–651 | Shared-tag nilpotent interaction bound with proof and scoped regression evidence. |
| <a id="topic-10.4"></a>10.4 Workarounds (inventory L708) | Full treatment | [D168](#d168) L652–675 | Independent tags and Boolean conjunction/re-encoding workarounds explicitly separated. |
| <a id="topic-11.1"></a>11.1 Phase kickback (inventory L720) | Full treatment | [D099](#d099) L166–197; [D168](#d168) L521–536 | Ring-valued kickback construction retained. |
| <a id="topic-11.2"></a>11.2 Kickback without a Fourier transform (inventory L728) | Full treatment | [D099](#d099) L166–197; [D201](#d201) L575–617 | Singular H_z/Smith diagonal boundary distinguishes kickback from invertible analyzer. |
| <a id="topic-12.1"></a>12.1 What *is* canonical (inventory L743) | Full treatment | [D257](#d257) L205–331; [D325](#d325) L792–821 | Bare Boolean valuation/contraction/pairing naturality treated. |
| <a id="topic-12.2"></a>12.2 What is *not* generated by bare LM valuation (inventory L753) | Full treatment | [D257](#d257) L332–372; [D087](#d087) L264–292 | Idempotent obstruction: Boolean-ring maps into local A land in {0,1}; no nilpotent amplitudes from bare valuation. |
| <a id="topic-12.3"></a>12.3 CM coefficient vector to chain-ring element (inventory L761) | Full treatment | [D257](#d257) L373–406; [D201](#d201) L132–154 | Coefficient identification is linear and basis-dependent; chosen convolution is extra multiplication. |
| <a id="topic-12.4"></a>12.4 Symbolic `A`-enrichment (inventory L775) | Full treatment | [D257](#d257) L408–544; [D087](#d087) L264–292 | Chosen scalar enrichment and symbolic-support bridge have detailed proofs in CM-only report, shorter P01 appendix. |
| <a id="topic-12.5"></a>12.5 "Nonzero = possible" is an extra postulate (inventory L789) | Full treatment | [D257](#d257) L601–639; [D034](#d034) L154–181 | Nonzero possibility is an added modal contract; support is not a semiring homomorphism. |
| <a id="topic-12.6"></a>12.6 Effects and measurement bases (inventory L798) | Full treatment | [D257](#d257) L546–599; [D257](#d257) L641–676 | Bare LM effects only yield restricted coordinate family; full reversible A-bases require enrichment and choices. |
| <a id="topic-12.7"></a>12.7 Division-free updates (inventory L804) | Full treatment | [D257](#d257) L677–774; [D257](#d257) L922–938 | Division-free projectors, projective rescaling, symbolic compatibility, repeatability and exact finite counts retained. |
| <a id="topic-12.8"></a>12.8 Conditioning and process closure problems (inventory L825) | Full treatment | [D257](#d257) L775–809; [D151](#d151) L84–184 | Conditioning and tensor failures, plus later closed binary completion under changed operations; unchanged A-nonzero semantics still obstructed. |
| <a id="topic-12.9"></a>12.9 Final bridge conclusion (inventory L834) | Full treatment | [D257](#d257) L992–1029; [D087](#d087) L264–292 | Canonical Boolean layer versus chosen modal extension explicitly separated. |
| <a id="topic-13.1"></a>13.1 Shared-module tensor model (inventory L848) | Full treatment | [D034](#d034) L252–297; [D087](#d087) L193–223 | Shared/balanced A tensor and annihilation restrictions explained. |
| <a id="topic-13.2"></a>13.2 Literal independent-register model (inventory L858) | Full treatment | [D034](#d034) L299–341; [D151](#d151) L121–184 | Literal F_2 registers and broader linear operations developed. |
| <a id="topic-13.3"></a>13.3 Non-equivalence (inventory L868) | Full treatment | [D034](#d034) L299–341; [D087](#d087) L193–223 | No tensor/entanglement-preserving equivalence implied by coefficient embedding. |
| <a id="topic-13.4"></a>13.4 Tensor collapse examples (inventory L874) | Full treatment | [D034](#d034) L288–297; [D151](#d151) L88–119 | Explicit nonzero factors yielding zero; primitive-state conditioning counterexample. |
| <a id="topic-13.5"></a>13.5 Relabeling caveat (inventory L880) | Full treatment | [D034](#d034) L404–418 | Empirical-model isomorphism with Bob's transpose/relabeling explains matching restricted counts without tensor equivalence. |
| <a id="topic-14.1"></a>14.1 Exhaustive resource inventory (inventory L890) | Full treatment | [D087](#d087) L235–254; [D036](#d036) L1–104 | Complete 65,536 resource inventory, including zero, documented. |
| <a id="topic-14.2"></a>14.2 Projective rays and bases (inventory L896) | Full treatment | [D201](#d201) L256–271; [D257](#d257) L922–932 | 24 primitive rays and 192 unordered reversible projective bases; distinguish GL_2(A) count 24,576. |
| <a id="topic-14.3"></a>14.3 Smith/valuation classification (inventory L903) | Full treatment | [D087](#d087) L84–143 | Smith trichotomy has manuscript statement and proof; status stronger than only a finite conjecture, independent correctness/priority review still separate. |
| <a id="topic-14.4"></a>14.4 Counts in the `u^4` ring (inventory L914) | Full treatment | [D036](#d036) L22–41; [D087](#d087) L235–254 | 5,265 local + 34,056 logical-not-strong + 26,214 strong = 65,535 nonzero. |
| <a id="topic-14.5"></a>14.5 Fifteen Smith-type classes (inventory L924) | Full treatment | [D036](#d036) L1–21; [D074](#d074) L408–534 | 15 types include zero; tables and class interpretation preserved. |
| <a id="topic-14.6"></a>14.6 General finite-chain-ring conjecture/theorem candidate (inventory L930) | Full treatment | [D087](#d087) L46–143; [D201](#d201) L157–271 | General finite commutative chain-ring theorem is written, not merely proposed; full local basis and nonzero-state contract essential. |
| <a id="topic-14.7"></a>14.7 Uniform Hardy family (inventory L942) | Full treatment | [D087](#d087) L95–114; [D201](#d201) L183–208 | Uniform Hardy witness has construction and proof. |
| <a id="topic-14.8"></a>14.8 Same rank, different contextuality (inventory L948) | Full treatment | [D034](#d034) L333–341; [D087](#d087) L184–223 | Rank/operation dependence and primitive/nonprimitive separators treated; repair old example assumptions before reuse. |
| <a id="topic-14.9"></a>14.9 Restricted measurement dependence (inventory L959) | Full treatment | [D034](#d034) L333–418; [D087](#d087) L192–234 | Classification belongs to restricted basis/action contract and can change under enlarged access. |
| <a id="topic-15.1"></a>15.1 Bell-like nonseparable states (inventory L971) | Full treatment | [D034](#d034) L356–403 | Explicit Bell resource and support table. |
| <a id="topic-15.2"></a>15.2 Possibilistic Bell contradiction (inventory L975) | Full treatment | [D034](#d034) L373–385 | Modal contradiction with proof and possible/impossible contract; no CHSH probability inference. |
| <a id="topic-15.3"></a>15.3 Bell behavior does not require the chain ring (inventory L983) | Full treatment | [D034](#d034) L356–385; [D074](#d074) L135–175 | Embedded plain-F_2 Bell support shows phase ring is not necessary for broad existence. |
| <a id="topic-15.4"></a>15.4 No support-faithful no-signalling probability completion (inventory L992) | Full treatment | [D034](#d034) L623–647 | No support-faithful normalized no-signalling probability extension, with proof. |
| <a id="topic-15.5"></a>15.5 Historical signed-lift CHSH work (inventory L998) | Full treatment | [D166](#d166) L506–843 | Signed/integral lift reproduces standard quantum amplitudes/gates; a distinct branch, not intrinsic Boolean Born probabilities. |
| <a id="topic-16"></a>16. Hardy phenomena (inventory L1010) | Full treatment | [D087](#d087) L95–143 | Valuation-uniform Hardy construction and logical-versus-strong contextuality treated. |
| <a id="topic-17.1"></a>17.1 GHZ-like nonseparability (inventory L1026) | Full treatment | [D034](#d034) L420–435; [D074](#d074) L535–580 | GHZ nonseparability and support scenarios recorded. |
| <a id="topic-17.2"></a>17.2 Strong contextuality requires richer settings (inventory L1030) | Full treatment | [D087](#d087) L224–233; [D201](#d201) L430–464 | General two-complete-binary-setting obstruction has a written theorem. |
| <a id="topic-17.3"></a>17.3 Literal-register GHZ constructions (inventory L1037) | Full treatment | [D034](#d034) L420–435; [D201](#d201) L730–736 | Literal six-context witness retained as scoped finite evidence, not universal minimality. |
| <a id="topic-17.4"></a>17.4 Minimality and weighted variants (inventory L1041) | Partial / mention | [D201](#d201) L730–736; [D034](#d034) L420–435 | Finite check of 101,583 subsets of at most five contexts is preserved; full weighted-variant/minimality program is not developed. |
| <a id="topic-18.1"></a>18.1 Early conclusion: universal teleportation seemed impossible (inventory L1056) | Full treatment | [D034](#d034) L95–111; [D034](#d034) L509–513 | Failed restricted/old four-outcome conclusion is retained with correction boundary. |
| <a id="topic-18.2"></a>18.2 Corrected general Boolean-linear result (inventory L1064) | Full treatment | [D034](#d034) L437–507 | Corrected literal Boolean-linear construction and proof with allowed corrections explicit. |
| <a id="topic-18.3"></a>18.3 Large-outcome protocol (inventory L1072) | Full treatment | [D034](#d034) L464–507 | 64 outcomes and 16,384 successful branch/input checks recorded; not a four-outcome protocol. |
| <a id="topic-18.4"></a>18.4 Resource criterion (inventory L1080) | Full treatment | [D034](#d034) L455–462; [D087](#d087) L173–191 | Invertibility iff universal raw-vector transfer under declared complete analyzer/correction contract. |
| <a id="topic-18.5"></a>18.5 Singular resources (inventory L1090) | Full treatment | [D034](#d034) L529–565; [D074](#d074) L312–380 | Restricted subspace/quotient hierarchies for singular resources; older claims require tensor-model qualification. |
| <a id="topic-18.6"></a>18.6 Example singular resource (inventory L1096) | Full treatment | [D034](#d034) L529–583; [D151](#d151) L331–368 | diag(1,u^2) example and restricted/full transfer distinction survive. |
| <a id="topic-18.7"></a>18.7 Multi-copy activation (inventory L1100) | Full treatment | [D034](#d034) L567–583; [D151](#d151) L331–368 | Literal rank activation and resolved-phase-disposal example; do not carry old shared-model no-activation into enlarged operations. |
| <a id="topic-18.8"></a>18.8 Restricted models still have teleportation obstructions (inventory L1108) | Full treatment | [D034](#d034) L584–602; [D151](#d151) L284–368 | Orthogonal correction and retained-phase restrictions have separate obstructions; no blanket claim that every shared-ring protocol is impossible. |
| <a id="topic-19.1"></a>19.1 Dense-coding-like protocols (inventory L1125) | Full treatment | [D034](#d034) L514–527; [D087](#d087) L144–172 | Explicit protocols and exact invertible-orbit/readout task. |
| <a id="topic-19.2"></a>19.2 Resource formula (inventory L1129) | Full treatment | [D087](#d087) L152–172; [D201](#d201) L325–356 | N_max=dh theorem with leading Smith multiplicity h and matched complete readout. |
| <a id="topic-19.3"></a>19.3 Separation from teleportation (inventory L1137) | Full treatment | [D087](#d087) L173–223; [D036](#d036) L43–62 | Coding versus teleportation separations and model-dependent examples retained; P01 highlights a nonprimitive maximal separator. |
| <a id="topic-20"></a>20. No-cloning (inventory L1153) | Full treatment | [D034](#d034) L604–621 | Linear modal no-cloning proof, explicitly excludes arbitrary nonlinear Boolean cloning. |
| <a id="topic-21.1"></a>21.1 Binary orthogonal operator-basis obstruction (inventory L1168) | Full treatment | [D034](#d034) L584–602; [D201](#d201) L465–496 | Even-dimensional transpose-orthogonal span/correction obstruction retained. |
| <a id="topic-21.2"></a>21.2 Symplectic / orthogonal restrictions (inventory L1180) | Full treatment | [D034](#d034) L584–602; [D201](#d201) L465–496 | Separate symplectic alternating-form obstruction and gate/form assumptions recorded. |
| <a id="topic-21.3"></a>21.3 Restricted basis versus general linear basis (inventory L1186) | Full treatment | [D034](#d034) L437–507; [D034](#d034) L584–602 | General invertible analyzers exist despite orthogonal restrictions. |
| <a id="topic-22"></a>22. Stabilizer / Clifford / Pauli-like structures (inventory L1196) | Partial / mention | [D166](#d166) L714–843; [D151](#d151) L187–218 | Signed Clifford arithmetic and marked A-algebra normalizer have substantial homes. Full intrinsic Pauli/stabilizer simulation theory not established. |
| <a id="topic-22.1"></a>22.1 Signed-lift result (inventory L1207) | Full treatment | [D166](#d166) L714–843 | Exact Clifford+T phase-count encoding and quantum-algorithm reproductions belong to added signed lift. |
| <a id="topic-22.2"></a>22.2 Intrinsic Boolean subtheory (inventory L1224) | Full treatment | [D168](#d168) L279–520; [D151](#d151) L187–218 | Intrinsic ring, mixers and marked normalizer developed; do not imply a complete stabilizer formalism. |
| <a id="topic-23.1"></a>23.1 Deutsch (inventory L1239) | Full treatment | [D099](#d099) L80–96 | Deutsch lower bound; matching two-query upper bound specifically for informative XOR oracle, not arbitrary G0=G1. |
| <a id="topic-23.2"></a>23.2 Deutsch-Jozsa (inventory L1246) | Full treatment | [D099](#d099) L97–110 | Exact one-query DJ obstruction under complete recorded characteristic-two model. |
| <a id="topic-23.3"></a>23.3 Bernstein-Vazirani (inventory L1252) | Full treatment | [D099](#d099) L112–164 | Adaptive recorded-branch BV lower bound n; XOR upper bound qualified. |
| <a id="topic-23.4"></a>23.4 Simon (inventory L1258) | Full treatment | [D099](#d099) L198–224; [D264](#d264) L1–850 | Explicit finite scope: 65,535 preparations, dimension 16, one query, no ancilla, n=2, 36 oracles and three shifts. No exact preparation found; no general Simon theorem claimed. |
| <a id="topic-23.5"></a>23.5 Grover (inventory L1264) | Partial / mention | [D168](#d168) L619–633; [D099](#d099) L226–236 | Marked-pattern failure/accounting and Grover non-result retained; signed quantum reproduction kept separate. |
| <a id="topic-23.6"></a>23.6 UNIQUE-SAT / special oracle cases (inventory L1270) | Full treatment | [D099](#d099) L198–224 | Known modal UNIQUE-SAT positive control included and credited; finite scripts are corroboration, not new priority. |
| <a id="topic-23.7"></a>23.7 Main algorithmic lesson (inventory L1276) | Full treatment | [D099](#d099) L166–197 | Kickback with singular analyzer explicitly separates mechanisms from algorithmic speedup. |
| <a id="topic-24.1"></a>24.1 No intrinsic Born rule (inventory L1291) | Full treatment | [D168](#d168) L409–438; [D034](#d034) L623–647 | No intrinsic Born rule; explicit probability obstruction in selected supports. |
| <a id="topic-24.2"></a>24.2 Degenerate norms (inventory L1295) | Full treatment | [D168](#d168) L421–438 | Correct wording: isotropic self-product, non-positive norm candidate; nondegenerate Hermitian pairing. Inventory's blanket degeneracy phrasing needs correction. |
| <a id="topic-24.3"></a>24.3 Modal rather than probabilistic interpretation (inventory L1299) | Full treatment | [D087](#d087) L46–83; [D034](#d034) L343–354 | Nonzero-amplitude possibility semantics stated, not normalized probabilities. |
| <a id="topic-24.4"></a>24.4 No faithful probability completion in some Bell cases (inventory L1308) | Full treatment | [D034](#d034) L623–647 | Faithful no-signalling completion obstruction fully treated. |
| <a id="topic-24.5"></a>24.5 Signed/complex lifts are additional structure (inventory L1312) | Full treatment | [D166](#d166) L506–654; [D168](#d168) L825–838 | Signed/integral/complex-compatible lift explicitly additional structure. |
| <a id="topic-25"></a>25. Resource hierarchy and capability map (inventory L1318) | Full treatment | [D034](#d034) L167–181; [D036](#d036) L43–62; [D087](#d087) L294–306; [D151](#d151) L263–368 | Capability hierarchy assembled across model ledger, resource tables and later operation-dependent conversion companion; no single unqualified resource ordering. |
| <a id="topic-26.1"></a>26.1 Raw Boolean matrix logic has extensive antecedents (inventory L1356) | Full treatment | [D325](#d325) L1258–1293; [D111](#d111) L470–620 | Classical truth-table/Boolean/frame ingredients and scope of synthesis stated. |
| <a id="topic-26.2"></a>26.2 Bricken (inventory L1369) | Full treatment | [D325](#d325) L1390–1399; [D326](#d326) L713–713 | Bricken antecedent cited for bra-matrix-ket logic; source access/priority limits in audit. |
| <a id="topic-26.3"></a>26.3 Cheng et al. (inventory L1373) | Full treatment | [D325](#d325) L512–641; [D328](#d328) L7–10 | Cheng numerical same-frame truth-vector prior art expressly motivates LM-centered revision. |
| <a id="topic-26.4"></a>26.4 Mizraji / Eigenlogic / STP and related traditions (inventory L1382) | Full treatment | [D325](#d325) L1258–1293; [D325](#d325) L1390–1406; [D111](#d111) L470–620 | Mizraji, Eigenlogic, STP and distinct representation contracts discussed; not a new external literature audit here. |
| <a id="topic-26.5"></a>26.5 CM rotation algebra is mathematically classical in isolation (inventory L1393) | Full treatment | [D201](#d201) L76–99; [D168](#d168) L751–781 | Group/chain-ring algebra classical; chosen CM interpretation separated from novelty. |
| <a id="topic-26.6"></a>26.6 Modal Bell/GHZ/teleportation are prior-art heavy (inventory L1407) | Full treatment | [D087](#d087) L30–45; [D034](#d034) L652–661 | Modal Bell/communication precedents and priority limits present. |
| <a id="topic-26.7"></a>26.7 Strongest novelty candidates identified (inventory L1425) | Full treatment | [D201](#d201) L157–697; [D087](#d087) L84–234; [D099](#d099) L80–197 | Candidate theorem architecture materially present. Coverage is not independent proof or historical novelty certification. |
| <a id="topic-27.1"></a>27.1 Correct positioning of CM computation (inventory L1442) | Full treatment | [D111](#d111) L795–846; [D325](#d325) L1249–1257 | CM token/representation/IR artifacts distinguished from algorithms and dense execution. |
| <a id="topic-27.2"></a>27.2 Structural IR and DAGs (inventory L1452) | Full treatment | [D111](#d111) L795–846; [D168](#d168) L676–750 | IR/DAG, sharing, local substitution and pre-expansion folding developed. |
| <a id="topic-27.3"></a>27.3 No-reinflate execution (inventory L1464) | Partial / mention | [D111](#d111) L795–846; [D168](#d168) L676–750; [D007](#d007) L1–520 | Delayed materialization and symbolic execution are present; named no-reinflate architecture not fully documented as a separate manuscript result. |
| <a id="topic-27.4"></a>27.4 Persistent / structural caching (inventory L1472) | Partial / mention | [D111](#d111) L997–1080; [D007](#d007) L1–520 | Prepared reuse/cache costs discussed. Specific persistent-cache plateau and matched runtime conclusions not located as a complete results section. |
| <a id="topic-27.5"></a>27.5 Typed operand frames (inventory L1487) | Full treatment | [D111](#d111) L340–469; [D111](#d111) L918–946 | Typed row/column, signed order, fixed/layout and dense conversion conditions developed. |
| <a id="topic-27.6"></a>27.6 Structural, hybrid, retabulation, and fallback paths (inventory L1501) | Full treatment | [D111](#d111) L847–916 | Pure structural/hybrid/retabulate/ordinary fallback cases and root outcomes explicit. |
| <a id="topic-27.7"></a>27.7 Pair-root versus persistent rewriting (inventory L1512) | Partial / mention | [D111](#d111) L882–910; [D272](#d272) L1–190 | Recursive pair request and outer ordinary-IR fallback described. Explicit warning that successful child work is discarded and original root recompiled was not found in manuscript prose. |
| <a id="topic-27.8"></a>27.8 Provenance classes `S/T/H` (inventory L1523) | Partial / mention | [D111](#d111) L413–469 | Source uses S/R/H (R=retabulated), rather than inventory's S/T/H. Every non-S/S fusion is H; do not silently equate labels across releases. |
| <a id="topic-27.9"></a>27.9 Syntactic versus essential support (inventory L1533) | Partial / mention | [D111](#d111) L863–868; [D111](#d111) L934–944 | Live/support-discovery used, but explicit syntactic-versus-essential support contract was not found; preserve as an implementation clarification gap. |
| <a id="topic-27.10"></a>27.10 Dense API axes (inventory L1539) | Partial / mention | [D111](#d111) L918–946 | Broadcasting to requested layout described. Inventory's exact fixed-variable 4x2/eight-entry example and full ambient-axis caveat not located. |
| <a id="topic-27.11"></a>27.11 NoPair signaling (inventory L1545) | Partial / mention | [D111](#d111) L882–890 | No-pair returned to caller, which converts to ordinary IR. Exact named NoPair symbol is not in the inspected manuscript text. |
| <a id="topic-27.12"></a>27.12 Cost accounting (inventory L1551) | Partial / mention | [D111](#d111) L918–956; [D111](#d111) L1062–1080 | Construction, traversal, dense costs, endpoints and reuse accounting substantial; explicit discarded-child charging remains a gap. |
| <a id="topic-27.13"></a>27.13 Prepared versus one-shot use (inventory L1566) | Full treatment | [D111](#d111) L997–1080 | One-shot versus prepared endpoints and measured break-even costs distinguished. |
| <a id="topic-28.1"></a>28.1 S1/S2 study (inventory L1579) | Full treatment | [D111](#d111) L1142–1167; [D201](#d201) L748–765 | 10,500/10,389 and seven exact CM/generic metric ties retained; no unique-CM performance conclusion. |
| <a id="topic-28.2"></a>28.2 Mechanism counters (inventory L1594) | Full treatment | [D111](#d111) L1153–1159; [D111](#d111) L950–956 | Symbolic metric counts and strata, not one aggregated timing computation. |
| <a id="topic-28.3"></a>28.3 P14-PY0 dispatcher result (inventory L1603) | Full treatment | [D111](#d111) L1169–1236 | P14 negative frozen dispatcher result, thresholds, endpoints, amendments, corpus and ratios fully documented. |
| <a id="topic-28.4"></a>28.4 P15 semantic pass (inventory L1609) | Partial / mention | [D111](#d111) L1237–1238 | P15 has exposed-case correctness and no accepted timings/holdout. Inventory's exact hundreds-of-cases count not supplied here. |
| <a id="topic-28.5"></a>28.5 Large assertion counts (inventory L1613) | Partial / mention | [D326](#d326) L58–58; [D326](#d326) L680–703 | 1,536,530 assertion figure belongs to foundations Astra audit, not evidence of compiler speed. Compiler-specific million-comparison release not located. |
| <a id="topic-28.6"></a>28.6 Gate A: manuscript-source-protocol alignment (inventory L1619) | Partial / mention | [D111](#d111) L974–995; [D111](#d111) L997–1140; [D272](#d272) L1–190 | Freeze/correctness/comparator contract substantial. Named Gate A's full manuscript-source-protocol reconciliation details are not wholly in the paper. |
| <a id="topic-28.7"></a>28.7 Protocol v3/v4 (inventory L1643) | Partial / mention | [D111](#d111) L1136–1140; [D272](#d272) L174–174 | Protocol v3 present; v4 is a conditional future repair in protocol document, not a located completed v4 protocol. |
| <a id="topic-29"></a>29. Comparison with other Boolean methods (inventory L1654) | Partial / mention | [D111](#d111) L997–1080; [D168](#d168) L751–781 | Packed/bitset, sharing/DAG, ROBDD and AIG comparison contract plus ANF/STP prior art. Full Numba/CUDD/SymPy/Espresso comparative study not retained as a manuscript result. |
| <a id="topic-29.1"></a>29.1 Important correction to early speed claims (inventory L1669) | Full treatment | [D111](#d111) L1125–1264; [D168](#d168) L774–781 | No universal raw speedup; expensive dense output and generic ties/negative dispatcher preserved. |
| <a id="topic-30"></a>30. Quotienting experiments (inventory L1682) | Partial / mention | [D232](#d232) PDF, extracted L526–570 (around p. 10); [D325](#d325) L1018–1070; [D166](#d166) L930–968 | Feature subtraction and decomposition are present historically; exact containment/Jaccard/exhaustive quotient experiment and semantic-delta speed comparison not found as a full report here. |
| <a id="topic-31.1"></a>31.1 Foundations paper (inventory L1707) | Full treatment | [D075](#d075) PDF, extracted L1–65 (around p. 1); [D325](#d325) L512–641 | Distinct LM-centered foundations manuscript exists, with editable source only in PUB. |
| <a id="topic-31.2"></a>31.2 Computational/compiler paper (inventory L1723) | Full treatment | [D111](#d111) L44–80; [D111](#d111) L795–1244 | Distinct computational manuscript exists in 19-, 21- and 24-page states; preserve evidence-updated 24-page version. |
| <a id="topic-31.3"></a>31.3 Phase/modal/resource paper (inventory L1739) | Full treatment | [D168](#d168) L211–230; [D087](#d087) L25–45 | Intrinsic phase and P01 resource manuscripts are distinct homes, not interchangeable versions. |
| <a id="topic-31.4"></a>31.4 Canonical bridge paper/report (inventory L1752) | Full treatment | [D257](#d257) L84–137; [D257](#d257) L953–1029 | Full bridge technical report exists only in CM; P01 contains a shorter interface and program deliberately defers a separate bridge article. |
| <a id="topic-31.5"></a>31.5 Query-obstruction paper (inventory L1763) | Full treatment | [D099](#d099) L25–33 | P02 exists as nine-page proof-bearing technical note, beyond the six-page skeleton. |
| <a id="topic-31.6"></a>31.6 "Boolean Modal Laboratory for Quantum Information" (inventory L1774) | Partial / mention | [D173](#d173) PDF, extracted L1–62 (around p. 1); [D005](#d005) L1–200; [D209](#d209) L1–71 | Laboratory synthesis/report and planning record exist; no completed separate full paper with the proposed exact title was found. |
| <a id="topic-32"></a>32. Verification and reproducibility artifacts (inventory L1788) | Partial / mention | [D330](#d330) L22–26; [D168](#d168) L872–924; [D257](#d257) L904–950 | Many reproducibility artifacts exist, but copied packages and external code references have material gaps; see integrity/build findings. |
| <a id="topic-32.1"></a>32.1 Foundations verification (inventory L1805) | Partial / mention | [D325](#d325) L1473–1482; [D326](#d326) L680–703; [D329](#d329) L1–2 | Foundations 20,873-check output and separate 1,536,530 audit claims preserved. Referenced checker and spectral tables not found in supplied handoff tree. |
| <a id="topic-32.2"></a>32.2 Modal/resource verification (inventory L1815) | Full treatment | [D036](#d036) L64–104; [D257](#d257) L904–950; [D128](#d128) L199–205 | Resource, basis, projector and protocol checks documented with many local scripts/data. This audit checked files, not reran mathematical suites. |
| <a id="topic-32.3"></a>32.3 Astra handoff package (inventory L1828) | Partial / mention | [D004](#d004) L1–46; [D001](#d001) L1–260 | Extracted Astra handoff exists in CM. Its cited archive/package count does not guarantee unpacked completeness; six manifest entries are ignored ZIPs, not proof of lost papers. |
| <a id="topic-33.1"></a>33.1 Logical imaginary unit (inventory L1851) | Partial / mention | [D034](#d034) L208–230; [D166](#d166) L506–584 | Imaginary-number analogy and its correction survive; original historical proposed logical-i thread is not reproduced fully. |
| <a id="topic-33.2"></a>33.2 Hermiticity (inventory L1857) | Partial / mention | [D168](#d168) L421–438; [D325](#d325) L1340–1406 | Hermitian algebraic pairing and spectral cautions occur, but the original real-eigenvalue/observable/commutation tutorial is not substantively preserved. |
| <a id="topic-33.3"></a>33.3 Commutators and a logical Lie algebra (inventory L1871) | Absent / not located | No substantive matching text located | No substantive logical-Lie-algebra/commutator investigation located in manuscript or supporting text; ring commutants are not an equivalent topic. |
| <a id="topic-33.4"></a>33.4 Simultaneous diagonalization (inventory L1879) | Absent / not located | No substantive matching text located | No substantive simultaneous-diagonalization investigation or stated historical correction located; isolated diagonal/spectral discussion does not cover it. |
| <a id="topic-33.5"></a>33.5 Complex-valued fuzzy truth (inventory L1886) | Absent / not located | No substantive matching text located | Complex/fuzzy words occur in bibliography and signed-lift discussion, not the proposed unit-disk modulus/phase fuzzy-truth theory. |
| <a id="topic-33.6"></a>33.6 Bectors and B-modules (inventory L1895) | Absent / not located | No substantive matching text located | Bectors/B-modules historical construction not located. General vector/module language does not establish coverage of that named theory. |
| <a id="topic-33.7"></a>33.7 Evolutionary / time-dependent Logical Matrices (inventory L1904) | Absent / not located | No substantive matching text located | Time-evolving LMs, logistic activation, Heaviside threshold and coupled temporal model not located. |
| <a id="topic-33.8"></a>33.8 Cognitive / Matte-Blanco motivation (inventory L1916) | Partial / mention | [D170](#d170) §11.3 (historical cognitive interpretation) | ProLT v0.6 cognitive-interpretation paragraph preserves limited motivation. Matte-Blanco, p-adic/ultrametric and specific self-awareness program not located; later ProLT narrows/removes that paragraph. |
| <a id="topic-34.1"></a>34.1 Universal teleportation (inventory L1934) | Full treatment | [D034](#d034) L95–111; [D034](#d034) L437–513 | Universal teleportation no-go corrected with explicit enlarged-model boundary. |
| <a id="topic-34.2"></a>34.2 Four-outcome teleportation (inventory L1940) | Full treatment | [D034](#d034) L492–513 | Failed four-outcome claim distinguished from verified 64-outcome literal protocol. |
| <a id="topic-34.3"></a>34.3 No multi-copy activation (inventory L1946) | Full treatment | [D034](#d034) L567–583; [D151](#d151) L331–368 | Old no-activation cannot be exported to literal filtering/resolved disposal. |
| <a id="topic-34.4"></a>34.4 Shared tensor = literal tensor (inventory L1952) | Full treatment | [D034](#d034) L299–341 | Shared versus literal tensor distinction preserved. |
| <a id="topic-34.5"></a>34.5 Contextuality as gate-invariant absolute property (inventory L1958) | Full treatment | [D034](#d034) L333–418 | Contextuality class requires declared measurement/gate model. |
| <a id="topic-34.6"></a>34.6 Bell = CHSH probability violation (inventory L1964) | Full treatment | [D034](#d034) L373–385; [D034](#d034) L623–647 | Support contradiction is not a CHSH probability violation. |
| <a id="topic-34.7"></a>34.7 Born rule from CM phase algebra (inventory L1970) | Full treatment | [D168](#d168) L421–438; [D034](#d034) L623–647 | No intrinsic Born rule; retain nondegenerate-pairing/isotropic-self-product correction too. |
| <a id="topic-34.8"></a>34.8 LM valuation automatically yields chain-ring amplitudes (inventory L1976) | Full treatment | [D257](#d257) L332–372 | Idempotent obstruction to bare Boolean valuation generating A. |
| <a id="topic-34.9"></a>34.9 Nonzero = possible follows from LM semantics (inventory L1982) | Full treatment | [D257](#d257) L601–639; [D034](#d034) L154–181 | Modal nonzero rule is additional semantics. |
| <a id="topic-34.10"></a>34.10 CM pointwise superposition as uniquely novel (inventory L1988) | Full treatment | [D325](#d325) L512–641; [D328](#d328) L7–10 | Cheng antecedent and LM-centered novelty boundary explicit. |
| <a id="topic-34.11"></a>34.11 CM as "the compiler" (inventory L1994) | Full treatment | [D111](#d111) L795–846 | Representation, token, surrogate, IR and dense output separated from compiler algorithm. |
| <a id="topic-34.12"></a>34.12 Universal raw speed advantage (inventory L2000) | Full treatment | [D111](#d111) L1125–1264 | Generic ties and failed dispatcher threshold forbid universal speed claim. |
| <a id="topic-34.13"></a>34.13 Polarity-mask formula (inventory L2006) | Full treatment | [D325](#d325) L752–790; [D326](#d326) L701–703 | Corrected pi_delta/rho convention and 48/64 history retained. |
| <a id="topic-34.14"></a>34.14 Signed-lift quantum results as intrinsic Boolean results (inventory L2012) | Full treatment | [D166](#d166) L506–584; [D168](#d168) L825–838 | Signed/complex lift distinguished from intrinsic Boolean algebra. |
| <a id="topic-36.1"></a>36.1 General finite-chain-ring contextuality theorem (inventory L2047) | Full treatment | [D087](#d087) L46–143 | No longer merely an unwritten candidate: general finite-chain-ring theorem has proof. Broader multipartite generalization remains separate. |
| <a id="topic-36.2"></a>36.2 Uniform Hardy witness theorem (inventory L2059) | Full treatment | [D087](#d087) L95–114 | Uniform Hardy construction is written; global witness minimality is not thereby settled. |
| <a id="topic-36.3"></a>36.3 Resource monotones (inventory L2063) | Partial / mention | [D087](#d087) L144–223; [D151](#d151) L220–368 | Smith filter order, leading-layer coding and retained-phase criteria provide substantive monotones; not one universal monotone across all tasks/access models. |
| <a id="topic-36.4"></a>36.4 Multi-copy activation hierarchy (inventory L2073) | Partial / mention | [D034](#d034) L567–583; [D151](#d151) L284–368 | Literal rank and restricted retained/disposed-phase cases treated; minimum-copy hierarchy under every CM/orthogonal restriction remains open. |
| <a id="topic-36.5"></a>36.5 Closed process theory (inventory L2081) | Full treatment | [D151](#d151) L84–184; [D128](#d128) L55–134 | Closed binary instrument completion exists with changed tensor/conditioning. Faithful unchanged nonzero-A independence is obstructed, not solved by that completion. |
| <a id="topic-36.6"></a>36.6 Canonicality of the modal bridge (inventory L2092) | Partial / mention | [D257](#d257) L408–544; [D087](#d087) L264–292 | Canonical specialization after choosing A, but no universal property selecting the entire modal theory from bare LMs found. |
| <a id="topic-36.7"></a>36.7 Higher-arity CM rotation algebra (inventory L2096) | Partial / mention | [D201](#d201) L76–129; [D325](#d325) L1177–1248 | Power-of-two cyclic lift and degree/filtration distinction preserved, chiefly in CM-only bank; full higher-tensor cell-permutation/degree classification not completed. |
| <a id="topic-36.8"></a>36.8 Spectral/semigroup paper on the 16 compact CMs (inventory L2105) | Partial / mention | [D325](#d325) L1340–1406; [D327](#d327) PDF, extracted L518–518 (around p. 12) | Atlas/profile and deferred semigroup suggestion only; no complete spectral/semigroup paper located. |
| <a id="topic-36.9"></a>36.9 Restricted stabilizer-like subtheory (inventory L2118) | Partial / mention | [D151](#d151) L187–218; [D166](#d166) L714–843 | Marked algebra normalizer and separate signed Clifford reproduction; no intrinsic Gottesman-Knill simulation theorem found. |
| <a id="topic-36.10"></a>36.10 Query-complexity theorem paper (inventory L2122) | Full treatment | [D099](#d099) L34–224 | Unified exact-query proof manuscript already exists under explicit oracle/recording assumptions. |
| <a id="topic-36.11"></a>36.11 Compiler confirmatory benchmark (inventory L2126) | Partial / mention | [D111](#d111) L997–1140; [D111](#d111) L1240–1244 | Confirmatory token/packed protocol defined but unexecuted in manuscript; P14 is a different completed endpoint. |
| <a id="topic-36.12"></a>36.12 Compiler structural advantage (inventory L2130) | Partial / mention | [D111](#d111) L1142–1244; [D168](#d168) L676–750 | Structural mechanism and limited favorable cases survive; general matched structural advantage not established. |


## Inventory §35: every negative-result item

| ID | Inventory item | Finding / evidence crosswalk |
|---|---|---|
| 35.N01 | No intrinsic Born rule from the chain-ring norm. | [Full treatment: §24.1](#topic-24.1); [D168](#d168) L409–438; [D034](#d034) L623–647 |
| 35.N02 | Some Bell supports have no faithful no-signalling probability completion. | [Full treatment: §24.4](#topic-24.4); [D034](#d034) L623–647 |
| 35.N03 | Shared-module tensor/state classes are not closed under all conditioning/update operations. | [Full treatment: §12.8](#topic-12.8); [D257](#d257) L775–809; [D151](#d151) L84–184 |
| 35.N04 | Natural Boolean Fourier/character transforms can be singular. | [Full treatment: §11.2](#topic-11.2); [D099](#d099) L166–197; [D201](#d201) L575–617 |
| 35.N05 | Phase kickback can exist without an invertible analyzer. | [Full treatment: §23.7](#topic-23.7); [D099](#d099) L166–197 |
| 35.N06 | Standard one-query Deutsch advantage fails in the audited model. | [Full treatment: §23.1](#topic-23.1); [D099](#d099) L80–96 |
| 35.N07 | Exact one-query Deutsch-Jozsa fails. | [Full treatment: §23.2](#topic-23.2); [D099](#d099) L97–110 |
| 35.N08 | Bernstein-Vazirani loses the one-query advantage. | [Full treatment: §23.3](#topic-23.3); [D099](#d099) L112–164 |
| 35.N09 | Simon small cases did not yield the standard speedup. | [Full treatment: §23.4](#topic-23.4); [D099](#d099) L198–224; [D264](#d264) L1–850 |
| 35.N10 | No pure Boolean Grover advantage was established. | [Partial / mention: §23.5](#topic-23.5); [D168](#d168) L619–633; [D099](#d099) L226–236 |
| 35.N11 | Strict orthogonal/unitary operator-basis requirements create characteristic-two obstructions. | [Full treatment: §21.1](#topic-21.1); [D034](#d034) L584–602; [D201](#d201) L465–496 |
| 35.N12 | Singular single-copy resources do not universally teleport. | [Full treatment: §18.5](#topic-18.5); [D034](#d034) L529–565; [D074](#d074) L312–380 |
| 35.N13 | Two binary settings are insufficient for the targeted strong GHZ contextuality. | [Full treatment: §17.2](#topic-17.2); [D087](#d087) L224–233; [D201](#d201) L430–464 |
| 35.N14 | Dense CM materialization is not generally competitive with flat bitsets. | [Full treatment: §29.1](#topic-29.1); [D111](#d111) L1125–1264; [D168](#d168) L774–781 |
| 35.N15 | A generic support-aware optimizer matched CM folding in the S1/S2 symbolic metrics. | [Full treatment: §28.1](#topic-28.1); [D111](#d111) L1142–1167; [D201](#d201) L748–765 |
| 35.N16 | P14-PY0 did not establish a useful dispatcher win. | [Full treatment: §28.3](#topic-28.3); [D111](#d111) L1169–1236 |
| 35.N17 | Quotienting did not establish a semantic-delta speed advantage. | [Partial / mention: §30](#topic-30); [D232](#d232) PDF, extracted L526–570 (around p. 10); [D325](#d325) L1018–1070; [D166](#d166) L930–968 |
| 35.N18 | A fully closed chain-ring modal process theory remains unresolved. | [Full treatment: §36.5](#topic-36.5); [D151](#d151) L84–184; [D128](#d128) L55–134 |

## Inventory §37: complete easy-to-miss checklist crosswalk

Each original checklist line is retained here; compound lines also point to adjacent detailed rows in the matrix. These are cross-references, not fresh counted topics.

| ID | Inventory checklist item | Coverage and primary matrix row |
|---|---|---|
| 37.C01 | LM is symbolic/formula-valued; CM is its evaluated numeric shadow. | [Full treatment: §4.1](#topic-4.1) |
| 37.C02 | Canonical term-lift definition. | [Full treatment: §4.2](#topic-4.2) |
| 37.C03 | Logical pairing / agreement-bit semantics. | [Full treatment: §4.4](#topic-4.4) |
| 37.C04 | Valuation-pairing coherence. | [Full treatment: §4.5](#topic-4.5) |
| 37.C05 | Signed-frame and polarity transport. | [Full treatment: §4.7](#topic-4.7) |
| 37.C06 | Corrected polarity-mask convention. | [Full treatment: §4.8](#topic-4.8) |
| 37.C07 | Arbitrary-arity tensors/flattenings/block lifts. | [Full treatment: §5.3](#topic-5.3) |
| 37.C08 | Distinction between XOR-AND contraction and pointwise Boolean operator superposition. | [Full treatment: §4.6](#topic-4.6) |
| 37.C09 | Cheng et al. prior art for raw numerical same-frame combination. | [Full treatment: §26.3](#topic-26.3) |
| 37.C10 | Bricken bra-ket/logical-matrix prior art. | [Full treatment: §26.2](#topic-26.2) |
| 37.C11 | Spectral classification of the 16 compact CMs. | [Partial / mention: §2.6](#topic-2.6) |
| 37.C12 | `GL_2(F_2) ~= S_3` structure of the six invertible CMs. | [Partial / mention: §6.2](#topic-6.2) |
| 37.C13 | Rank-one/separability criterion. | [Partial / mention: §6.1](#topic-6.1) |
| 37.C14 | Valuation spectra / affine-function characterization. | [Partial / mention: §6.5](#topic-6.5) |
| 37.C15 | Literal four-cycle CM rotation `R`. | [Full treatment: §7.1](#topic-7.1) |
| 37.C16 | Centralizer = 16 circulant operators. | [Full treatment: §7.2](#topic-7.2) |
| 37.C17 | `F_2[C_4] ~= F_2[u]/(u^4)`. | [Full treatment: §7.3](#topic-7.3) |
| 37.C18 | Nilpotent filtration and rank sequence. | [Full treatment: §7.4](#topic-7.4) |
| 37.C19 | Boolean degree <-> lifted reversibility. | [Full treatment: §7.6](#topic-7.6) |
| 37.C20 | Operand reversal <-> `R^{-1}`. | [Full treatment: §7.7](#topic-7.7) |
| 37.C21 | Complement <-> deepest nilpotent layer. | [Full treatment: §7.8](#topic-7.8) |
| 37.C22 | Degenerate norm -> no Born rule. | [Full treatment: §7.10](#topic-7.10) |
| 37.C23 | Mixer/splitter is distinct from the rotation operator. | [Full treatment: §8.3](#topic-8.3) |
| 37.C24 | XOR cancellation as the intrinsic interference analogue. | [Full treatment: §9.1](#topic-9.1) |
| 37.C25 | Phase-Mobius / ANF bridge. | [Full treatment: §10.1](#topic-10.1) |
| 37.C26 | Nilpotent repeated-interaction limitation. | [Full treatment: §10.3](#topic-10.3) |
| 37.C27 | Phase kickback survives while the natural Fourier transform can be singular. | [Full treatment: §11.2](#topic-11.2) |
| 37.C28 | Bare LM valuation cannot create chain-ring amplitudes. | [Full treatment: §12.2](#topic-12.2) |
| 37.C29 | "Nonzero = possible" is extra modal semantics. | [Full treatment: §12.5](#topic-12.5) |
| 37.C30 | 24 rays / 192 reversible projective bases. | [Full treatment: §14.2](#topic-14.2) |
| 37.C31 | Division-free projectors and repeatability checks. | [Full treatment: §12.7](#topic-12.7) |
| 37.C32 | Conditioning/tensor non-closure. | [Full treatment: §12.8](#topic-12.8) |
| 37.C33 | Shared-module tensor != literal independent-register tensor. | [Full treatment: §13.3](#topic-13.3) |
| 37.C34 | Smith/valuation contextuality classification. | [Full treatment: §14.3](#topic-14.3) |
| 37.C35 | 5,265 local / 34,056 logical / 26,214 strong resource counts. | [Full treatment: §14.4](#topic-14.4) |
| 37.C36 | Uniform Hardy witness direction. | [Full treatment: §14.7](#topic-14.7) |
| 37.C37 | Same binary rank can hide different restricted resource power. | [Full treatment: §14.8](#topic-14.8) |
| 37.C38 | Bell support contradictions do not require CM rotation. | [Full treatment: §15.3](#topic-15.3) |
| 37.C39 | Bell support != CHSH probability violation. | [Full treatment: §15.2](#topic-15.2) |
| 37.C40 | No-support-faithful no-signalling completion for some tables. | [Full treatment: §15.4](#topic-15.4) |
| 37.C41 | GHZ strong-contextuality setting obstruction. | [Full treatment: §17.2](#topic-17.2) |
| 37.C42 | Earlier "teleportation impossible" conclusion is superseded. | [Full treatment: §18.1](#topic-18.1) |
| 37.C43 | Broad Boolean-linear teleportation iff invertible/full-rank resource, with model qualifications. | [Full treatment: §18.4](#topic-18.4) |
| 37.C44 | Failed four-outcome protocol versus successful larger/64-outcome protocol. | [Full treatment: §18.3](#topic-18.3) |
| 37.C45 | Multi-copy activation of singular resources under broader literal filtering. | [Full treatment: §18.7](#topic-18.7) |
| 37.C46 | Dense coding and teleportation are distinct resource capabilities. | [Full treatment: §19.3](#topic-19.3) |
| 37.C47 | Dense-coding `d h` style capacity result. | [Full treatment: §19.2](#topic-19.2) |
| 37.C48 | No-cloning is conditional on the allowed linear/modal dynamics. | [Full treatment: §20](#topic-20) |
| 37.C49 | Orthogonal/unitary operator-basis obstruction in characteristic two. | [Full treatment: §21.1](#topic-21.1) |
| 37.C50 | Restricted stabilizer/normalizer questions. | [Partial / mention: §36.9](#topic-36.9) |
| 37.C51 | Signed-lift quantum reproductions are additional structure / prior-art heavy. | [Full treatment: §22.1](#topic-22.1) |
| 37.C52 | Deutsch/DJ/BV negative query results. | [Full treatment: §23.1](#topic-23.1); also §§23.2, 23.3 |
| 37.C53 | Simon small-case negative and Grover unresolved. | [Full treatment: §23.4](#topic-23.4); also §§23.5 |
| 37.C54 | CM is structural representation/IR, not "the compiler". | [Full treatment: §27.1](#topic-27.1) |
| 37.C55 | No-reinflate architecture. | [Partial / mention: §27.3](#topic-27.3) |
| 37.C56 | Persistent structural cache / compile-once-evaluate-many. | [Partial / mention: §27.4](#topic-27.4) |
| 37.C57 | Pair-root implementation versus persistent rewriting. | [Partial / mention: §27.7](#topic-27.7) |
| 37.C58 | S/T/H provenance. | [Partial / mention: §27.8](#topic-27.8) |
| 37.C59 | Syntactic versus essential support. | [Partial / mention: §27.9](#topic-27.9) |
| 37.C60 | Fallback semantics and discarded child work. | [Partial / mention: §27.7](#topic-27.7) |
| 37.C61 | S1/S2 negative result: generic optimizer matched CM symbolic metrics. | [Full treatment: §28.1](#topic-28.1) |
| 37.C62 | P14-PY0 negative/non-decisive result. | [Full treatment: §28.3](#topic-28.3) |
| 37.C63 | Quotienting is structurally meaningful but not a demonstrated speed advantage. | [Partial / mention: §30](#topic-30) |
| 37.C64 | Gate A manuscript-source-protocol alignment. | [Partial / mention: §28.6](#topic-28.6) |
| 37.C65 | Strong competitors: bitset, CUDD/ROBDD, AIG, SymPy, Espresso, Numba. | [Partial / mention: §29](#topic-29) |
| 37.C66 | Historical logical imaginary unit idea. | [Partial / mention: §33.1](#topic-33.1) |
| 37.C67 | Hermiticity/commutator/simultaneous-diagonalization explorations. | [Partial / mention: §33.2](#topic-33.2); also §§33.3, 33.4 |
| 37.C68 | Complex-valued fuzzy truth direction. | [Absent / not located: §33.5](#topic-33.5) |
| 37.C69 | Bectors/B-modules. | [Absent / not located: §33.6](#topic-33.6) |
| 37.C70 | Evolutionary/time-dependent LMs. | [Absent / not located: §33.7](#topic-33.7) |
| 37.C71 | Matte-Blanco / cognitive motivation, clearly separated from mathematical claims. | [Partial / mention: §33.8](#topic-33.8) |

## Remaining master-inventory sections and duplicate topic lists

Sections 1 and 38 are status/register design, rather than substantive scientific claims. The existing CM-only claim registry D185 and model/claim/source crosswalks are useful predecessors to §38, but no assertion is made that they implement every suggested register field. Preserve them and this inventory together.

Section 39's proposed paper-home bullets are addressed by these matrix groups: Foundations §§3–6 and 26; Compiler §§27–30; Phase/modal §§7–11 and 13–25; LM bridge §12; Query §23; Historical §33. Its “avoid overloading” exclusions and choices of publication home are planning guidance, not missing mathematical results. The actual manuscript split/disposition is assessed in §31 and the family table. In particular, the historical essay and complete spectral/semigroup paper are not located as finished manuscripts; P01/P02 already exist; the process work is explicitly a companion/supplement.

Section 40 restates fourteen research clusters and eight correction priorities. All clusters map to the same numbered matrix groups, and all eight correction priorities are explicitly tested in §§34.1–34.14. Sections with numbered children are organizational parents; their substantive introductory statements (notably §§22, 29 and 32) also have matrix rows. Thus a mere parent heading is not counted as an additional proof or paper.

## Appendix A. Complete PDF/LaTeX object ledger

Each object groups **all byte-identical paths**, even when filenames differ. Distinct hashes stay separate even when they are the same paper family. Hashes below are full SHA-256. PDF page counts come from the PDF page tree. TeX objects may be standalones or fragments; the family map above distinguishes them.

<a id="d033"></a>
### D033 — CM_Correctness_Audit.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 4; PDF pages: 28.
- SHA-256: `602c8c82b8b0f09ce5e453d36f258821901bcb0bd654714ef500ca0c3835bc68`
- `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\paper\CM_Correctness_Audit.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\audit\paper\CM_Correctness_Audit.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit.pdf`

<a id="d034"></a>
### D034 — CM_Correctness_Audit.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `c7c861dd4d3f49a15b89ec9a030ccaec1fd9efce0c8306bd5058c5f0317560cc`
- `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\paper\CM_Correctness_Audit.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\audit\paper\CM_Correctness_Audit.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit.tex`

<a id="d035"></a>
### D035 — CM_Correctness_Audit_Standalone.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `0f1ebab450602f9382a5564cf7c46307950685aee7ec762c6a27862e64fbdd70`
- `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\paper\CM_Correctness_Audit_Standalone.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit_Standalone.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\audit\paper\CM_Correctness_Audit_Standalone.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\CM_Correctness_Audit_Standalone.tex`

<a id="d036"></a>
### D036 — generated_tables.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `0f3766e68e6b3b09d43c10c85834a2b75c00b3b26120b0473dfe69a9a126e184`
- `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\paper\generated_tables.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\generated_tables.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\audit\paper\generated_tables.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\paper\generated_tables.tex`

<a id="d074"></a>
### D074 — PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `1a58df56a9ebb04d413a62c0f900aaa32fcc627db9c4b26a639c1a9fe07c0ff1`
- `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\source_snapshots\Pure_Boolean_Modal_Quantum\paper\PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\source_snapshots\Pure_Boolean_Modal_Quantum\paper\PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\audit\source_snapshots\Pure_Boolean_Modal_Quantum\paper\PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\source_snapshots\Pure_Boolean_Modal_Quantum\paper\PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex`

<a id="d075"></a>
### D075 — CM_LM_Boolean_Operator_Calculus_LM_Centered_V1.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 2; PDF pages: 31.
- SHA-256: `ca4c64497e29c40e7398746ef57550f5915e5ce7b5be480cc579dc13601bb4ca`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_Boolean_Operator_Calculus_LM_Centered_V1.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\01_CURRENT_MANUSCRIPTS\Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.pdf`

<a id="d086"></a>
### D086 — main.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 3; PDF pages: 11.
- SHA-256: `f85a140ce21a2ff1e74b6b9f965d473f1430fee2c2464f867386f8f82720ba08`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\main.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P01\main.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\main.pdf`

<a id="d087"></a>
### D087 — main.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `31f623fc8572d0d7cb2141d7971196176979dbd56ff40bd6a4d5ca318c3ac46f`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\main.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P01\main.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\main.tex`

<a id="d088"></a>
### D088 — smith_table.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `96a4fcf96b5caa14208df4f84a8481dcccbf86e01c5c69d7e484131cfde9aa8d`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\smith_table.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P01\smith_table.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\01_P01_CHAIN_RING_CONTEXTUALITY_AND_RESOURCES\source_package\smith_table.tex`

<a id="d098"></a>
### D098 — main.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 3; PDF pages: 9.
- SHA-256: `ab8ee57575c186b86768b1ef2d6f42b62d1be15a3e33137710210363ee6dc89e`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\main.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P02\main.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\main.pdf`

<a id="d099"></a>
### D099 — main.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `b07a5d6c247a479811f01d419c03d416dc86a3058898de2cbaa036d32046273f`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\main.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P02\main.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\main.tex`

<a id="d100"></a>
### D100 — phase_table.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `e04c8a738b2317f930978d065a1c5eb25cd70c9e68dd345b51459b43f355db5f`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\phase_table.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\P02\phase_table.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\02_P02_CHARACTERISTIC_TWO_QUERY_OBSTRUCTIONS\source_package\phase_table.tex`

<a id="d107"></a>
### D107 — appendix_proofs.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `228a7e7fb69fed8acf311563c788a24f4381dbff1c53c9baeb34df4c53aee532`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\appendix_proofs.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\05_manuscript\appendix_proofs.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\appendix_proofs.tex`

<a id="d110"></a>
### D110 — main.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 4; PDF pages: 24.
- SHA-256: `a02ba8aded23edd94b5f816bbf6b5f8afee881576762eb89371eb884613c4133`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\05_manuscript\main.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\01_CURRENT_MANUSCRIPTS\Operator-Level_Boolean_Computation_with_Correspondence_Matrices_current.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.pdf`

<a id="d111"></a>
### D111 — main.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `70f302de93f2d42d698ec0d9b1d54ea983350264b04016e395062c0a2ed8ccdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\05_manuscript\main.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex`

<a id="d112"></a>
### D112 — p14_rows.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `ed6b1fc266956c9450f05adf370241a561cb49f8476608cfa80c0dc2d008add6`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\p14_rows.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\05_manuscript\p14_rows.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\p14_rows.tex`

<a id="d120"></a>
### D120 — evidence_update.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `5df3c633726ca0f1f3efdb6ec34fa09c2ee214e239907470f333646eea750f96`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\research_and_review\evidence_update.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\evidence_update.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\research_and_review\evidence_update.tex`

<a id="d128"></a>
### D128 — main.tex

- Type: `.tex`; roots: CM, PUB; copies: 3.
- SHA-256: `5b93d19dabb2d663440f7196fda8d905860f4485ffe757ffbac64810f5ca49f0`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\research_verification_20260921\P03_STUB\main.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\main.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\research_verification_20260921\P03_STUB\main.tex`

<a id="d149"></a>
### D149 — CM_LM_Technical_Companion_20260920.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 5; PDF pages: 9.
- SHA-256: `4fc0e6227a0f4532de126c6fb3dc0d033fe278031d253c4715b15faf56b81e80`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\CM_LM_Technical_Companion_20260920.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\CM_LM_Technical_Companion_20260920.pdf`
- `C:\Users\brian\Documents\CM Quantum\cm_lm_technical_companion_20260920\build\main.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_Technical_Companion_20260920.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\CM_LM_Technical_Companion_20260920.pdf`

<a id="d151"></a>
### D151 — main.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `b31f05d96415b11df98f6e2c0a5673210d70672172c1f2af49202d637cefebee`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\main.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\main.tex`
- `C:\Users\brian\Documents\CM Quantum\cm_lm_technical_companion_20260920\main.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\main.tex`

<a id="d165"></a>
### D165 — CM_Phase_Calculus_Verified.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 7; PDF pages: 33.
- SHA-256: `2a9aa28caa59da4e08f2705d3d3e08df05e1f6c155fd107c9e8ca11ba8740b01`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_Quantum_Handoff_2026-09-17\CM_Quantum_Handoff_2026-09-17\papers\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\CM_Phase_Calculus_Verified.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Modal Quantum CM-LMs\CM_Quantum_Handoff_2026-09-17\papers\CM_Phase_Calculus_Verified.pdf`

<a id="d166"></a>
### D166 — CM_Phase_Calculus_Verified.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `ca00b5154e52493bda80e07ca573567ada9f9afcdeaec9c047e99bab5d43aed9`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Verified.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_Quantum_Handoff_2026-09-17\CM_Quantum_Handoff_2026-09-17\papers\CM_Phase_Calculus_Verified.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Verified.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Modal Quantum CM-LMs\CM_Quantum_Handoff_2026-09-17\papers\CM_Phase_Calculus_Verified.tex`

<a id="d167"></a>
### D167 — Intrinsic_Boolean_CM_Phase_Algebra.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 4; PDF pages: 26.
- SHA-256: `e228fec6e98c9324cae30ebaae2e425e65ac8808c766d763afacf4ff86fa0c27`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Algebra.pdf`
- `C:\Users\brian\Documents\CM Quantum\CM_Quantum_Handoff_2026-09-17\CM_Quantum_Handoff_2026-09-17\papers\Intrinsic_Boolean_CM_Phase_Algebra.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Algebra.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Modal Quantum CM-LMs\CM_Quantum_Handoff_2026-09-17\papers\Intrinsic_Boolean_CM_Phase_Algebra.pdf`

<a id="d168"></a>
### D168 — Intrinsic_Boolean_CM_Phase_Algebra.tex

- Type: `.tex`; roots: CM, PUB; copies: 4.
- SHA-256: `3ea1b66845ac42b8dd0af22ef92e014b649d809fe080ec2338a52760915ca850`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Algebra.tex`
- `C:\Users\brian\Documents\CM Quantum\CM_Quantum_Handoff_2026-09-17\CM_Quantum_Handoff_2026-09-17\papers\Intrinsic_Boolean_CM_Phase_Algebra.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Algebra.tex`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Modal Quantum CM-LMs\CM_Quantum_Handoff_2026-09-17\papers\Intrinsic_Boolean_CM_Phase_Algebra.tex`

<a id="d169"></a>
### D169 — operator-level-boolean-computation-with-correspondence-matrices.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 3; PDF pages: 21.
- SHA-256: `6d726f96ebd446ac9228860cd1bd52e61bd49e2d3b1be7092f6310269a260136`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\operator-level-boolean-computation-with-correspondence-matrices.pdf`
- `C:\Users\brian\Documents\CM Quantum\operator-level-boolean-computation-with-correspondence-matrices.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\operator-level-boolean-computation-with-correspondence-matrices.pdf`

<a id="d170"></a>
### D170 — propositional-logical-topology-core-v0.6.pdf

- Type: `.pdf`; roots: CM, PUB; copies: 2; PDF pages: 15.
- SHA-256: `47efc49ee760778d0f6d01abf60f9638d3a0695672e973130a85a0373800924e`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\propositional-logical-topology-core-v0.6.pdf`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\root_pdfs\propositional-logical-topology-core-v0.6.pdf`

<a id="d173"></a>
### D173 — CM_LM_Quantum_Findings_Consolidated_Report_2026-09-22.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 12.
- SHA-256: `170d261fd7cdce5673f49cf80f86e365a2dfbcf75159d1f178bc405719f08923`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_Quantum_Findings_Consolidated_Report_2026-09-22.pdf`

<a id="d198"></a>
### D198 — references_static.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `4a0ae8a3c5310147821fddfc2d85b5fa3457a23e5bc0c117e62c8b64b8861b97`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\literature\references_static.tex`

<a id="d200"></a>
### D200 — THEOREM_BANK.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 18.
- SHA-256: `610a457a294ee338deadc81412b1e1df716efd2bdb25a2b1a473420f4596896b`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\THEOREM_BANK.pdf`

<a id="d201"></a>
### D201 — THEOREM_BANK.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `ea481a3b14d840b987a1c3937a943446da7fb2285a8e527342c25aa934a32d5c`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\THEOREM_BANK.tex`

<a id="d203"></a>
### D203 — definitions.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `4d299344b44343377e9da53fe1688233314da56272f4e9cddff36ed1785d4a47`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\definitions.tex`

<a id="d204"></a>
### D204 — model_contracts.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `914b6e4422016e414a7feac8898226d2fa2d523f962c89ffed0f6b127f24bd9f`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\model_contracts.tex`

<a id="d205"></a>
### D205 — notation.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `7c63dbc153a03cd0bcd642a684d23e98d3f5ade56b9ac1244363aa7ad548b5f3`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\notation.tex`

<a id="d208"></a>
### D208 — ONE_PAGE_PUBLICATION_MAP.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 1.
- SHA-256: `4f88bbb40e432f3b619ad10e07fa492cda5d34235a4afc10ffba8848041174c2`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\ONE_PAGE_PUBLICATION_MAP.pdf`

<a id="d209"></a>
### D209 — ONE_PAGE_PUBLICATION_MAP.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `02d9fcc00543de80523df88707db43053afe6bdee16c4c7b4cde726377d84b67`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\ONE_PAGE_PUBLICATION_MAP.tex`

<a id="d214"></a>
### D214 — PAPER_SKELETON.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 6.
- SHA-256: `5187f8910c382ee19ce7675b6ebfe9089cb80cc8408061f84a753f17cdeffb77`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P01_Chain_Ring_Resources\PAPER_SKELETON.pdf`

<a id="d215"></a>
### D215 — PAPER_SKELETON.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `15a3a6a5814c7aeaac2ba016b995a1ac384c59adc8ba627392e61106cf4ba173`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P01_Chain_Ring_Resources\PAPER_SKELETON.tex`

<a id="d224"></a>
### D224 — PAPER_SKELETON.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 6.
- SHA-256: `083c7811fa86f5c4f2cc9a035ec1253fade1d5dfce25270fb0b7f5a233037997`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P02_Exact_Modal_Queries\PAPER_SKELETON.pdf`

<a id="d225"></a>
### D225 — PAPER_SKELETON.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `c0fbb92e4c3a8082cb199077c68ecc782ac0a6e4c6b114108393ff2fba316659`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P02_Exact_Modal_Queries\PAPER_SKELETON.tex`

<a id="d232"></a>
### D232 — CorrespondenceMatrices (2).pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 29.
- SHA-256: `7a9958a2ec34e61318855a3e8054d668c7d9654de3316c4fe546f7db7a2503a9`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\inputs\CorrespondenceMatrices (2).pdf`

<a id="d233"></a>
### D233 — operator-level-boolean-computation-with-correspondence-matrices.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 19.
- SHA-256: `fa689c47df05ecf16014b83164e1457240926ae607aa4e59a9eaeb4ab5655c78`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\inputs\operator-level-boolean-computation-with-correspondence-matrices.pdf`

<a id="d257"></a>
### D257 — LM_Modal_Bridge_Report.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `8da0a88544332e2939e8ed99d1ad19bfb64e09aced2213258a79148250062170`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\bridge\report\LM_Modal_Bridge_Report.tex`

<a id="d284"></a>
### D284 — CM_PAPER_NOTATION_MACROS.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `d622a7aa81333f8b204d360bd5e47f20f039c2c2fcf283ef5a58cb0c7de7d6fa`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\04_figures\CM_PAPER_NOTATION_MACROS.tex`

<a id="d295"></a>
### D295 — main.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `32a415e193247799ac6ef40385587c10d90a2ae94d0e7a1b3141156da54bf94d`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\P03_STUB\main.tex`

<a id="d307"></a>
### D307 — main.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 10.
- SHA-256: `81ae94fd7e18deaa7ff1d5742ac12ae2de7d571d6e6ce36fa53f7de6e6bbb33a`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\81ae94fd7e18\main.pdf`

<a id="d308"></a>
### D308 — main.tex

- Type: `.tex`; roots: CM; copies: 1.
- SHA-256: `f3bb0b20de214b55075b9d2e2725ad85a21656c8da4ede279180e46388862927`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\f3bb0b20de21\main.tex`

<a id="d324"></a>
### D324 — propositional-logical-topology-core-v0.8.pdf

- Type: `.pdf`; roots: CM; copies: 1; PDF pages: 18.
- SHA-256: `acf6d1a70ce2c215f16b0323a1933cf52a1c60613995f646925f283881abe237`
- `C:\Users\brian\Documents\CM Quantum\propositional-logical-topology-core-v0.8.pdf`

<a id="d325"></a>
### D325 — Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.tex

- Type: `.tex`; roots: PUB; copies: 1.
- SHA-256: `86f2b8cb901c0af3f1a9c0a726f26aa65091d137d33bda21aa157c0985b6fb48`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\01_CURRENT_MANUSCRIPTS\Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.tex`

<a id="d327"></a>
### D327 — CM_LM_Audit_Astra.pdf

- Type: `.pdf`; roots: PUB; copies: 1; PDF pages: 21.
- SHA-256: `18ea905ba2b971dc7d1fe6fb56612e2cc272c7e128ec5c28d86b96beec70da11`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\02_REVIEWS_AND_AUDITS\CM_LM_Audit_Astra.pdf`

<a id="d331"></a>
### D331 — finite_jet_rigidity_boolean_sign_laws_submission_candidate.pdf

- Type: `.pdf`; roots: PUB; copies: 1; PDF pages: 13.
- SHA-256: `f1fab1ba8e31ffe54313f64aa99875ba8a95923b553c310c966649dcc80b2cb0`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Finite Jet Rigitity (Paper A)\finite_jet_rigidity_boolean_sign_laws_submission_candidate.pdf`

<a id="d332"></a>
### D332 — finite_jet_rigidity_boolean_sign_laws_submission_candidate.tex

- Type: `.tex`; roots: PUB; copies: 1.
- SHA-256: `e1da4d6605eb636f1f6481c487b14962702bfb0285afed9c12cfb2f856752e8b`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Finite Jet Rigitity (Paper A)\finite_jet_rigidity_boolean_sign_laws_submission_candidate.tex`

<a id="d336"></a>
### D336 — propositional-logical-topology-core-v0.8.1.pdf

- Type: `.pdf`; roots: PUB; copies: 1; PDF pages: 19.
- SHA-256: `662a8b576b1fb49d2c1379b97b8e12cc83f522c1162f23225cc3ef63d3bfdb0e`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\propositional-logical-topology-core-v0.8.1.pdf`

<a id="d337"></a>
### D337 — propositional-logical-topology-core-v0.8.1.tex

- Type: `.tex`; roots: PUB; copies: 1.
- SHA-256: `6ebaf9772297680c6c199f2184432ff3172d651744ca576e72a9aa3d846a7d2f`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\propositional-logical-topology-core-v0.8.1.tex`

## Appendix B. Supporting evidence and research records cited

These are reviews, logs, registries, notes or protocols; their presence is not by itself manuscript coverage.

<a id="d001"></a>
### D001 — ASTRA_CM_LM_MASTER_CONSOLIDATION_PROMPT_2026-09-18.md

SHA-256: `60b5a215ae82d025053e8ae380681e3205be06659bfa678f059417f20ab9e3e2`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\00_START_HERE\ASTRA_CM_LM_MASTER_CONSOLIDATION_PROMPT_2026-09-18.md`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\MASTER_CONSOLIDATION_PROMPT.md`

<a id="d004"></a>
### D004 — README_FIRST.md

SHA-256: `ab777df1aaef655637ff72bd17a0ab9a5279874cc38965caa289d96d1a4ba0d2`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\00_START_HERE\README_FIRST.md`

<a id="d005"></a>
### D005 — 01_BOOLEAN_MODAL_LABORATORY_CONCEPT_AND_RESEARCH_DIRECTIONS.md

SHA-256: `9a31c35045af6e7380ef903f70dae59671126e73ba29150c60777d27da8eafc5`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\03_PRIOR_THREAD_SYNTHESIS\01_BOOLEAN_MODAL_LABORATORY_CONCEPT_AND_RESEARCH_DIRECTIONS.md`

<a id="d007"></a>
### D007 — 03_CM_FOLDING_S1_S2_INTERPRETATION_AND_NEXT_BENCHMARKS.md

SHA-256: `afbe7dc860be190b21fec3a6bfaabf8012ffaa7fdcde1080aae51afe3fe37178`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\03_PRIOR_THREAD_SYNTHESIS\03_CM_FOLDING_S1_S2_INTERPRETATION_AND_NEXT_BENCHMARKS.md`

<a id="d185"></a>
### D185 — CLAIM_REGISTRY.md

SHA-256: `8901aea3421ad9df15bff0ba6ac76337ea40414f7d2d64a04aee717284b3d665`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\claims\CLAIM_REGISTRY.md`

<a id="d264"></a>
### D264 — CAPABILITY_REPORT.md

SHA-256: `265c3ebde1856d6cf03e2882116ec41753e91b5e8809da464cd6340d9104afaa`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\capability\reports\CAPABILITY_REPORT.md`

<a id="d266"></a>
### D266 — FORMAL_THEOREMS.md

SHA-256: `fdf2095256f82a00ff38839dc6360872db9689fd35103cd65b2159f71ea0a0f8`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\capability\reports\FORMAL_THEOREMS.md`

<a id="d272"></a>
### D272 — EVALUATION_PROTOCOL_V3.md

SHA-256: `54039d0c2ce26a8e9f81dbd6eb60cba6fa093335d1d049afbf6f8269182cdc1f`; roots: CM.

- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\01_audit\EVALUATION_PROTOCOL_V3.md`

<a id="d326"></a>
### D326 — CM_LM_Audit_Astra.md

SHA-256: `d178155618ece0c2ee7cd4fdfbc7fad8d1ac6bde39ba479cddbccddd2070ec3d`; roots: PUB.

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\02_REVIEWS_AND_AUDITS\CM_LM_Audit_Astra.md`

<a id="d328"></a>
### D328 — LM_Centered_Revision_Notes.md

SHA-256: `ed057ca11518abf562a58507f431e47d2e1faf671f80ede11711f94dbe361765`; roots: PUB.

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\03_VERIFICATION_AND_CONTEXT\LM_Centered_Revision_Notes.md`

<a id="d329"></a>
### D329 — LM_Foundations_Verification_Output.txt

SHA-256: `cf5800947eae0d2aed1259dcee0d4a713dcf33e1bd63f2318779b6ece0ac51a1`; roots: PUB.

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\03_VERIFICATION_AND_CONTEXT\LM_Foundations_Verification_Output.txt`

<a id="d330"></a>
### D330 — ARTIFACT_MANIFEST.md

SHA-256: `7d9148e70acbbbbb7b21c7c31f8c8c4232bcf46a3dfe22ecad92562e8ca6f891`; roots: PUB.

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\ARTIFACT_MANIFEST.md`

<a id="d334"></a>
### D334 — RELEASE_NOTES.md

SHA-256: `10c060c1cc5e0985392800acc356884cfa92c7a08d0624dc40e0b81e52d85c14`; roots: PUB.

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\RELEASE_NOTES.md`

## Appendix C. Directory totals and unmatched-file accounting

| Measure | CM | PUB |
|---|---:|---:|
| Non-ZIP file instances | 1610 | 452 |
| Distinct file hashes | 856 | 410 |
| PDF instances | 32 | 17 |
| TeX instances | 49 | 21 |
| Distinct PDF/TeX hashes | 47 | 32 |
| File instances with no opposite exact hash | 611 | 13 |
| Distinct contents with no opposite exact hash | 459 | 13 |

Detailed all-file paths, byte sizes, timestamps and full hashes are in the accompanying `Paper_Preservation_Audit_Evidence_2026-09-25.json`. That machine-readable ledger includes every scanned file, all 337 distinct extracted text objects, dependency checks, manifest discrepancies and the topic decisions. File modification times are recorded for provenance only; version direction was inferred from internal dates/release notes and content changes.

### Every PUB-only file

- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\01_CURRENT_MANUSCRIPTS\Correspondence_and_Logical_Matrices_Boolean_Operator_Calculus_LM_Centered.tex` — SHA-256 `86f2b8cb901c0af3f1a9c0a726f26aa65091d137d33bda21aa157c0985b6fb48`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\02_REVIEWS_AND_AUDITS\CM_LM_Audit_Astra.md` — SHA-256 `d178155618ece0c2ee7cd4fdfbc7fad8d1ac6bde39ba479cddbccddd2070ec3d`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\02_REVIEWS_AND_AUDITS\CM_LM_Audit_Astra.pdf` — SHA-256 `18ea905ba2b971dc7d1fe6fb56612e2cc272c7e128ec5c28d86b96beec70da11`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\03_VERIFICATION_AND_CONTEXT\LM_Centered_Revision_Notes.md` — SHA-256 `ed057ca11518abf562a58507f431e47d2e1faf671f80ede11711f94dbe361765`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\03_VERIFICATION_AND_CONTEXT\LM_Foundations_Verification_Output.txt` — SHA-256 `cf5800947eae0d2aed1259dcee0d4a713dcf33e1bd63f2318779b6ece0ac51a1`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM-LMs and lifting\CM_Computational_Paper_Handoff_2026-09-22\ARTIFACT_MANIFEST.md` — SHA-256 `7d9148e70acbbbbb7b21c7c31f8c8c4232bcf46a3dfe22ecad92562e8ca6f891`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Finite Jet Rigitity (Paper A)\finite_jet_rigidity_boolean_sign_laws_submission_candidate.pdf` — SHA-256 `f1fab1ba8e31ffe54313f64aa99875ba8a95923b553c310c966649dcc80b2cb0`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Finite Jet Rigitity (Paper A)\finite_jet_rigidity_boolean_sign_laws_submission_candidate.tex` — SHA-256 `e1da4d6605eb636f1f6481c487b14962702bfb0285afed9c12cfb2f856752e8b`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\propositional-logical-topology-core-v0.8.1.pdf` — SHA-256 `662a8b576b1fb49d2c1379b97b8e12cc83f522c1162f23225cc3ef63d3bfdb0e`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\propositional-logical-topology-core-v0.8.1.tex` — SHA-256 `6ebaf9772297680c6c199f2184432ff3172d651744ca576e72a9aa3d846a7d2f`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\README.md` — SHA-256 `aea7563e3b9210a417790279cb6c05ec12973b9f5b1c5cbbbb195fbb4eb3e434`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\RELEASE_NOTES.md` — SHA-256 `10c060c1cc5e0985392800acc356884cfa92c7a08d0624dc40e0b81e52d85c14`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\ProLT\SHA256SUMS.txt` — SHA-256 `6376300efb04b9d74b280638da88268f08c17cf3919a9503df0cf2a277999126`

### Every CM-only PDF/TeX object

- [D173](#d173) — `C:\Users\brian\Documents\CM Quantum\CM_LM_Quantum_Findings_Consolidated_Report_2026-09-22.pdf`
- [D198](#d198) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\literature\references_static.tex`
- [D200](#d200) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\THEOREM_BANK.pdf`
- [D201](#d201) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\THEOREM_BANK.tex`
- [D203](#d203) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\definitions.tex`
- [D204](#d204) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\model_contracts.tex`
- [D205](#d205) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\math\notation.tex`
- [D208](#d208) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\ONE_PAGE_PUBLICATION_MAP.pdf`
- [D209](#d209) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\ONE_PAGE_PUBLICATION_MAP.tex`
- [D214](#d214) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P01_Chain_Ring_Resources\PAPER_SKELETON.pdf`
- [D215](#d215) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P01_Chain_Ring_Resources\PAPER_SKELETON.tex`
- [D224](#d224) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P02_Exact_Modal_Queries\PAPER_SKELETON.pdf`
- [D225](#d225) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\papers\P02_Exact_Modal_Queries\PAPER_SKELETON.tex`
- [D232](#d232) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\inputs\CorrespondenceMatrices (2).pdf`
- [D233](#d233) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\inputs\operator-level-boolean-computation-with-correspondence-matrices.pdf`
- [D257](#d257) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\bridge\report\LM_Modal_Bridge_Report.tex`
- [D284](#d284) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\04_figures\CM_PAPER_NOTATION_MACROS.tex`
- [D295](#d295) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\P03_STUB\main.tex`
- [D307](#d307) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\81ae94fd7e18\main.pdf`
- [D308](#d308) — `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\f3bb0b20de21\main.tex`
- [D324](#d324) — `C:\Users\brian\Documents\CM Quantum\propositional-logical-topology-core-v0.8.pdf`

### CM-only supporting contents by extension

Counts are unique content hashes, excluding hashes found in PUB. This includes non-manuscript build/log/data records, not only research contributions.

| Extension | Distinct CM-only contents |
|---|---:|
| `.aux` | 3 |
| `.bbl` | 3 |
| `.bib` | 4 |
| `.blg` | 3 |
| `.csv` | 40 |
| `.dot` | 2 |
| `.json` | 142 |
| `.log` | 59 |
| `.md` | 121 |
| `.out` | 3 |
| `.pdf` | 9 |
| `.png` | 5 |
| `.ps1` | 1 |
| `.py` | 33 |
| `.svg` | 5 |
| `.tex` | 12 |
| `.toml` | 1 |
| `.txt` | 13 |

## Appendix D. Required source dependencies unresolved at their saved location

These are static local path checks, including declared graphics search paths. They do not certify a successful TeX build or installed package availability. Fragments and isolated historical source files may rely on a different intended working directory.

- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 27: `input{../04_figures/CM_PAPER_NOTATION_MACROS.tex}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 266: `includegraphics{figure_01_boolean_operator_contraction_preview.png}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 382: `includegraphics{figure_03_operand_alignment_and_fusion_preview.png}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 533: `includegraphics{figure_02_numeric_representation_map_preview.png}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 717: `includegraphics{figure_04_lm_valuation_and_pairing_preview.png}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\research_and_review\evidence_update.tex` line 55: `input{p14_rows}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Paper_B\evidence_update.tex` line 55: `input{p14_rows}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\f3bb0b20de21\main.tex` line 236: `input{smith_table}`
- `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\version_history\P01\f3bb0b20de21\main.tex` line 308: `bibliography{references}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 27: `input{../04_figures/CM_PAPER_NOTATION_MACROS.tex}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 266: `includegraphics{figure_01_boolean_operator_contraction_preview.png}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 382: `includegraphics{figure_03_operand_alignment_and_fusion_preview.png}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 533: `includegraphics{figure_02_numeric_representation_map_preview.png}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\manuscript\main.tex` line 717: `includegraphics{figure_04_lm_valuation_and_pairing_preview.png}`
- `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\03_PAPER_B_OPERATOR_LEVEL_BOOLEAN_COMPUTATION\research_and_review\evidence_update.tex` line 55: `input{p14_rows}`

## Appendix E. Existing SHA-256 manifest audit

ZIP references are excluded rather than reported as lost. Missing non-ZIP targets are searched by expected hash across both roots. Build intermediates and relocated PDFs are therefore distinguished from lost content.

### `C:\Users\brian\Documents\CM Quantum\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\ASTRA_PRO_CM_LM_CONSOLIDATED_HANDOFF_2026-09-18\SHA256SUMS.txt`

Matched in place: 7; byte mismatches: 0.

- L5 `./01_PRIMARY_RESEARCH_PACKAGES/CM_Capability_Dependency_2026-09-18.zip`: ZIP: deliberately excluded; no loss conclusion.
- L6 `./01_PRIMARY_RESEARCH_PACKAGES/CM_Quantum_Handoff_2026-09-17.zip`: ZIP: deliberately excluded; no loss conclusion.
- L7 `./01_PRIMARY_RESEARCH_PACKAGES/LM_Modal_Bridge_Research_Package_2026-09-18.zip`: ZIP: deliberately excluded; no loss conclusion.
- L8 `./02_AUDITS_AND_NOVELTY/Astra_CM_Novelty_Research_Package_2026-09-18.zip`: ZIP: deliberately excluded; no loss conclusion.
- L9 `./02_AUDITS_AND_NOVELTY/CM_Adversarial_Review_2026-09-18.zip`: ZIP: deliberately excluded; no loss conclusion.
- L10 `./02_AUDITS_AND_NOVELTY/CM_Final_Audit_2026-09-18.zip`: ZIP: deliberately excluded; no loss conclusion.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\research_verification_20260921\MANIFEST_SHA256.txt`

Matched in place: 44; byte mismatches: 0.

- L7 `P03_STUB/build/main.aux`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.aux`.
- L8 `P03_STUB/build/main.bbl`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.bbl`.
- L9 `P03_STUB/build/main.blg`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.blg`.
- L10 `P03_STUB/build/main.log`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.log`.
- L11 `P03_STUB/build/main.out`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.out`.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\MANIFEST_SHA256.txt`

Matched in place: 5; byte mismatches: 0.

- L6 `build/main.log`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\build\main.log`.
- L7 `build/main.bbl`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\build\main.bbl`.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\MANIFEST_SHA256.txt`

Matched in place: 154; byte mismatches: 9.

- L12 `data/audit_summary.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\audit_summary.json`.
- L13 `data/audit_timing.json`: BYTE MISMATCH; JSON values differ (timing record); expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\audit_timing.json`.
- L16 `data/bob_conjugation_basis_relabeling.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\bob_conjugation_basis_relabeling.json`.
- L17 `data/canonical_bell_basis.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\canonical_bell_basis.json`.
- L22 `data/equal_rank_class_equivalence.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\equal_rank_class_equivalence.json`.
- L23 `data/external_probability_LP.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\external_probability_LP.json`.
- L27 `data/literal_activation_witness.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\literal_activation_witness.json`.
- L33 `data/probability_exact_affine_constraints.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\probability_exact_affine_constraints.json`.
- L116 `source_snapshots/Native_Boolean_CM_Rotation_Phase/data/native_rotation_results.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\source_snapshots\Native_Boolean_CM_Rotation_Phase\data\console_output.txt`.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\INVENTORY_SHA256.txt`

Matched in place: 340; byte mismatches: 0.

- L327 `06_PROGRAM_LEVEL_REPORTS\REPRODUCTION_SUPPLEMENT.zip`: ZIP: deliberately excluded; no loss conclusion.
- L332 `07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.
- L338 `07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\bridge\inputs\CM_Adversarial_Review_2026-09-18(1)\CM_Adversarial_Review_2026-09-18\OUTPUT_MANIFEST_SHA256.txt`

Matched in place: 36; byte mismatches: 0.

- L23 `reproduction/data/all_resource_branch_rank_audit.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\all_resource_branch_rank_audit.csv`.
- L27 `reproduction/data/basis_permutation_entanglers.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\basis_permutation_entanglers.csv`.
- L29 `reproduction/data/bob_conjugation_basis_relabeling.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\bob_conjugation_basis_relabeling.json`.
- L32 `reproduction/data/class_inventory_audited.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\class_inventory_audited.csv`.
- L33 `reproduction/data/contextuality_audited_15_classes.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\contextuality_audited_15_classes.csv`.
- L34 `reproduction/data/dense_coding_64_messages.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\dense_coding_64_messages.csv`.
- L35 `reproduction/data/equal_rank_class_equivalence.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\equal_rank_class_equivalence.json`.
- L36 `reproduction/data/external_probability_LP.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\external_probability_LP.json`.
- L38 `reproduction/data/historical_test_rerun.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\adversarial\reproduction\data\historical_test_rerun.json`.
- L40 `reproduction/data/literal_activation_witness.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\literal_activation_witness.json`.
- L41 `reproduction/data/literal_finite_copy_activation.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\literal_finite_copy_activation.csv`.
- L42 `reproduction/data/literal_restricted_subspaces.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\literal_restricted_subspaces.csv`.
- L44 `reproduction/data/local_stabilizers_audited.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\local_stabilizers_audited.csv`.
- L45 `reproduction/data/measurement_bases_audited_192.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\measurement_bases_audited_192.csv`.
- L46 `reproduction/data/probability_exact_affine_constraints.json`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\probability_exact_affine_constraints.json`.
- L48 `reproduction/data/resource_inventory_audited_65536.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\resource_inventory_audited_65536.csv`.
- L49 `reproduction/data/shared_restricted_and_quotient_exhaustive.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\shared_restricted_and_quotient_exhaustive.csv`.
- L50 `reproduction/data/teleportation_direct_256x64.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\teleportation_direct_256x64.csv`.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\bridge\MANIFEST_SHA256.txt`

Matched in place: 70; byte mismatches: 0.

- L2 `./inputs/CM_Adversarial_Review_2026-09-18(1).zip`: ZIP: deliberately excluded; no loss conclusion.
- L52 `./prior_adversarial_review/CM_Adversarial_Review_2026-09-18/reproduction/data/shared_restricted_and_quotient_exhaustive.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\shared_restricted_and_quotient_exhaustive.csv`.

### `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\provenance\source_snapshots\bridge\prior_adversarial_review\CM_Adversarial_Review_2026-09-18\OUTPUT_MANIFEST_SHA256.txt`

Matched in place: 53; byte mismatches: 0.

- L49 `reproduction/data/shared_restricted_and_quotient_exhaustive.csv`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\shared_restricted_and_quotient_exhaustive.csv`.

### `C:\Users\brian\Documents\CM Quantum\cm_lm_technical_companion_20260920\MANIFEST_SHA256.txt`

Matched in place: 6; byte mismatches: 0.

- L1 `CM_LM_Technical_Companion_20260920.pdf`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\CM_LM_Technical_Companion_20260920.pdf`.

### `C:\Users\brian\Documents\CM Quantum\CM_Quantum_Handoff_2026-09-17\CM_Quantum_Handoff_2026-09-17\SHA256SUMS.txt`

Matched in place: 83; byte mismatches: 0.

- L6 `./papers/CM_Phase_Calculus_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.
- L12 `./papers/Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.

### `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\research_verification_20260921\MANIFEST_SHA256.txt`

Matched in place: 44; byte mismatches: 0.

- L7 `P03_STUB/build/main.aux`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.aux`.
- L8 `P03_STUB/build/main.bbl`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.bbl`.
- L9 `P03_STUB/build/main.blg`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.blg`.
- L10 `P03_STUB/build/main.log`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.log`.
- L11 `P03_STUB/build/main.out`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Research_Verification_20260921\P03_STUB\build\main.out`.

### `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\04_PROCESS_SEMANTICS_COMPANION_AND_VERIFICATION\technical_companion_20260920\MANIFEST_SHA256.txt`

Matched in place: 5; byte mismatches: 0.

- L6 `build/main.log`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\build\main.log`.
- L7 `build/main.bbl`: Missing at referenced path; exact expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research\Technical_Companion_20260920\build\main.bbl`.

### `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\05_CANONICAL_CORRECTNESS_AUDIT\audit_package\MANIFEST_SHA256.txt`

Matched in place: 154; byte mismatches: 9.

- L12 `data/audit_summary.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\audit_summary.json`.
- L13 `data/audit_timing.json`: BYTE MISMATCH; JSON values differ (timing record); expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\audit_timing.json`.
- L16 `data/bob_conjugation_basis_relabeling.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\bob_conjugation_basis_relabeling.json`.
- L17 `data/canonical_bell_basis.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\canonical_bell_basis.json`.
- L22 `data/equal_rank_class_equivalence.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\equal_rank_class_equivalence.json`.
- L23 `data/external_probability_LP.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\external_probability_LP.json`.
- L27 `data/literal_activation_witness.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\literal_activation_witness.json`.
- L33 `data/probability_exact_affine_constraints.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\data\probability_exact_affine_constraints.json`.
- L116 `source_snapshots/Native_Boolean_CM_Rotation_Phase/data/native_rotation_results.json`: BYTE MISMATCH; JSON values equal to historical exact-hash copy; expected bytes survive at `C:\Users\brian\Documents\CM Quantum\CM_Final_Audit_2026-09-18\CM_Final_Audit\source_snapshots\Native_Boolean_CM_Rotation_Phase\data\console_output.txt`.

### `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM_LM_PUBLICATION_PORTFOLIO_20260921\INVENTORY_SHA256.txt`

Matched in place: 340; byte mismatches: 0.

- L327 `06_PROGRAM_LEVEL_REPORTS\REPRODUCTION_SUPPLEMENT.zip`: ZIP: deliberately excluded; no loss conclusion.
- L332 `07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\CM_Phase_Calculus_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.
- L338 `07_LEGACY_AND_PRECONSOLIDATION_MATERIAL\handoff_20260917_papers\Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.

### `C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Modal Quantum CM-LMs\CM_Quantum_Handoff_2026-09-17\SHA256SUMS.txt`

Matched in place: 83; byte mismatches: 0.

- L6 `./papers/CM_Phase_Calculus_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.
- L12 `./papers/Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip`: ZIP: deliberately excluded; no loss conclusion.

## Appendix F. Verification of this audit

- All **2,062 scanned non-ZIP source files were rehashed after analysis**: zero changed, zero missing, zero added within the two source roots.
- All **119 PDF/TeX instances** map to one of the 53 ledger objects; every ledger reference and internal Markdown link resolves.
- All **193 matrix rows**, **18 §35 negative items**, and **71 §37 checklist items** are present; numbered leaf topics in §§2–36 are accounted for.
- The two 350-file portfolio trees match in both relative paths and SHA-256.
- The standalone audit source equals the modular source with its generated tables inlined.
- Git status/diff checks were attempted, but this task workspace is not a Git repository. Source SHA-256 verification supplies the relevant no-change evidence.
- No research verification suites, benchmark campaigns, TeX builds or ZIP contents were executed/examined. All quoted old test counts are inherited records.
- Verification completed: 2026-09-25T09:46:35.145422+00:00.


**Recommended next action:** preserve a verified archive before any cleanup. Use this task for that closely related follow-up; a low-reasoning coding-capable model is sufficient for a scoped copy/hash operation. Recover missing historical/spectral evidence before commissioning new papers on those topics. No additional task or model run is needed merely to read and use this report.

## Appendix G. Continued audit and completed GitHub preservation

Verified at **2026-09-25T13:05:30.035053+00:00** after the user's authorization to configure, commit and push.

- Repository: [Relative0/Papers](https://github.com/Relative0/Papers).
- Local folder: `C:\Users\brian\Documents\Math Latex etc\Papers for Publication`.
- Branch: `main`, tracking `origin/main`.
- Verified remote commit: [`8435cb66b9f69935ebfaff7f14612bb38296b7a2`](https://github.com/Relative0/Papers/commit/8435cb66b9f69935ebfaff7f14612bb38296b7a2).
- **452 original non-ZIP publication files** committed and pushed, comprising **19,304,969 source bytes**. Each staged Git blob matched the original audited file bytes, with no line-ending normalization. The remote branch equals the verified local commit.
- **11 publication ZIP files** remain local and untracked, intentionally excluded because the task identifies them as already unpacked. No other untracked files remain. There are no staged or unstaged changes to tracked files.
- Relative0 uses the existing credential manager account and a repository-local HTTPS remote. Commit identity is `Relative0 <949390+Relative0@users.noreply.github.com>`. The default GitHub CLI account remains **btheorystartups**; global authentication and Git identity settings were not changed. Browser and Git sessions remain separate.
- All **2,062 non-ZIP research files** were rehashed on continuation: **zero changed, missing or added research files**. Git metadata is excluded from this research-file count. The master inventory also matches its original audit hash.
- Revalidated **193 coverage rows (145 full, 43 partial, 5 absent)**, all **18 negative-result checklist rows**, all **71 easy-to-miss checklist rows**, **549 internal links**, and the exact **350-file** cross-directory portfolio mirror. The original topic assessments remain applicable because the inventory and all source bytes are unchanged.
- Rechecked cited preservation/correction details against the extracted sources, including Paper B's missing macro/figure paths, the nondegenerate-versus-isotropic pairing correction, theorem-bank dimension 50, and the older ProLT cognitive/infinite-language discussion.

**This upload preserves the publication directory, not the complete research archive.** The 459 distinct CM-only contents (611 file instances), the master inventory in Downloads, and this task's report/evidence outputs are outside the pushed directory. The CM-only full bridge report, theorem bank, historical manuscripts and original Paper B assets remain priority preservation items. Missing historical/spectral/checker material remains unlocated; a successful Git push does not repair those gaps.

The audit is complete within the requested local scope. Proof certification, compilation, external novelty review and recovery of material outside the two roots were not performed. The recommended next action is a separately scoped preservation copy of CM-only material, the master inventory and these audit deliverables, with hashes and original relative paths retained. Reuse this task and its evidence ledger; routine copy/hash work can use a low-reasoning coding-capable model, while new mathematical reconciliation merits higher reasoning. No source cleanup is recommended.
