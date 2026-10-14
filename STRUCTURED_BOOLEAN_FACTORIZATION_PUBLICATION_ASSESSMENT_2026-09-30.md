# Structured Boolean Factorization: publication decision memo

Assessment date: 30 September 2026. Internal AI editorial/research assessment, not external specialist review.

**Decision: no scholarly submission yet. The strongest current publication route is one tightly scoped negative-results/reproducibility report. A separate short theorem note is plausible only if a focused priority review identifies a substantive contribution. Do not commission three papers from the Phase 3, 4 and 5 drafts, or an algorithmic-speedup paper from the live-search result.**

There is enough evidence to justify a modest report about exact factor extraction, certification costs, and the difference between cheaper search and faster complete factorization. There is not yet evidence of a novel general factorization method, industrial benefit, or a novelty-cleared standalone theorem. An existing public evidence release already serves much of the archival function.

## 1. What actually exists

The requested “MIND” folder is named **The MIND** on disk. The collection index is at workspace-root **00_Collection_Index**, not inside The MIND.

| Stage | Actual starting artifact | Contribution and present status |
|---|---|---|
| Phase 3 | [Carrier-Aware Boolean Factorization at Bounded Incidence Width][P3], TeX working note; [underlying report and research package][P3R] | Combined carrier/CNF incidence-width FPT synthesis, pair-separation QBF, and fixed-cut four-corner SAT implementation. The width-lift remains a proof sketch needing detailed specialist scrutiny before a theorem submission. The experiments validate fixed-cut SAT and tiny factor recovery, not execution of a general QBF/FPT algorithm. |
| Phase 4 | [Direct and Residual Factor Extraction for Carrier-Constrained Boolean Structures][P4], TeX research draft; [master report][P4R] | Compressed-SDD cut criterion, finest vtree-clade factorization, signed read-once gate recursion, and persistent-encoding SAT fallback. Representation restrictions are essential. No general structured-d-DNNF extraction theorem was obtained. |
| Phase 5 | [Vtree Alignment and Higher-Order Four-Corner Defects in Exact Boolean Factorization][P5], TeX plus three-page PDF; [master report][P5R] | Exposure optimum, laminar obstruction, defect-support crossing and equality-family counterexample. Exact small-universe evidence; historical decision G, more research required. This is the latest manuscript note, not an integrated final paper. |
| Phase 5B | [master report][B], [corrected proofs][T], theorem ledger, real-backend implementation, frozen raw data, reviews and reproducibility ZIP | Mathematical working note survives; algorithmic NO-GO. No integrated Phase 5B TeX/PDF manuscript. Later proof corrections control interpretation of the older drafts. |
| Live tooling probe | [29 September report][Probe] | Supported live PySDD moves and restoration without recompiling every candidate. Tooling GO only. |
| First live integration | [original campaign][I1], then [separate audit][Audit] | Mechanism GO / algorithmic NO-GO. Audit finds no factor-exposure headroom in this dataset and identifies harness weaknesses. Saved numerical outcome remains valid; the dataset is an overhead control, not a decisive test of recoverable factor exposure. |
| Repaired prospective integration | [revision report][Rev], [new frozen protocol][Protocol], [final campaign][I2] | Development controls, integrity/resource repairs, Linux stress tests, then a separately frozen new 756-row campaign. Mechanism GO / algorithmic NO-GO again, this time with some observed factor recovery. |

These are an evolving research line, not three completed independent manuscripts. Copies in Supporting_Research, continuity archives, ZIPs and the sibling workflow are preservation/provenance layers, not additional contributions. The MIND snapshot is not the active runnable environment. Its current Phase 5B master/proof/status files are byte-identical to the sibling Phase 5B files; its Phase 5 PDF/TeX are byte-identical to the preserved Phase 5 originals.

The [collection crosswalk][Cross] keeps the separate CM structural-computation report distinct. The [linked-workspace guide][Links] is a dated snapshot that predates the final prospective outcome. The [publication scorecard][Score] correctly records that later outcome and unresolved priority, but its 5/10 is an editorial estimate, not a scientific gate. I would qualify its advice to integrate a manuscript: decide the contribution and publication form first. Integration alone cannot supply novelty.

Relevant chats checked: **Gluing** (01a0ec78-a0da-7a81-a512-33fce6be376d) and **Verify PySDD local vtree moves** (01a0ed4a-845f-7e31-b45b-2aa5be70ed6d), located through current chat inventory and collection chat evidence. Their conclusions agree with the saved reports. The latter records a completed public evidence release. I also fetched the [public prospective campaign report][PublicReport] and verified byte identity with the local report. Website publication is not external peer review or acceptance of a research paper; no new upload is needed merely to preserve these results.

## 2. What the evidence supports

### (a) Mathematical results with supplied proofs

The [Phase 5B proof audit][T] is the appropriate mathematical starting point. The core arguments are coherent under the stated hypotheses; their recorded “proved” status is not a priority certificate.

- **Canonical partition and carrier assembly:** for a nonfalse Boolean function on a declared variable universe, valid disjoint AND partitions have a unique finest common refinement. Free variables remain singleton true factors. The simultaneous carrier/semantic answer is the least common coarsening of the two exact partitions. This is a Cartesian-factorization/partition construction, not a new general decomposition principle.
- **P4-SDD and vtree-clade extraction:** a complete compressed decision at the specified cut is separable exactly when it has one nonfalse sub. Recursive extraction returns the finest factor partition whose blocks are clades of that tree. Trimmed nodes, free sides and compression must be handled explicitly.
- **F1:** the maximum number of exposed factors over all vtrees equals the semantic prime-factor count. This establishes an exact objective and existence of an aligned tree, not efficient search, convergence, or recognition of global optimality.
- **F2:** carrier and semantic blocks can simultaneously be clades precisely when their combined family is laminar. This is a standard hierarchy fact applied to the problem.
- **F3 and its limitations:** a nonzero four-corner witness with varying supports U and W certifies that some semantic prime meets both. Only singleton/singleton support gives a particular same-prime pair. EQ3 AND EQ2 refutes interpreting a whole support union as one prime.
- **Equality-family obstruction:** the relation containing only all-zero and all-one tuples is prime for n >= 3, while every fixed-context two-variable slice has rank at most one; every defect across a nontrivial cut varies all n coordinates. This refutes universal pairwise localization, not all conceivable localization algorithms.
- **Restricted positive classes:** irredundant positive-CNF interaction components equal semantic primes; essential binary read-once, support-disjoint trees admit the two-polarity gate-rank recursion. Neither result extends automatically to redundant CNFs or shared operator DAGs.
- **P5B support deletion:** at most m sequential deletion queries, or at most 1 + 2d ceil(log2 m) balanced-group queries, yield inclusion-minimal support, where d is the actual returned width. This is a generic monotone-predicate application; it is neither minimum-cardinality support nor an FPT SAT-runtime result.

The Phase 3 bounded-width statement belongs in the lineage/background, but its proof sketch is not covered by simply citing the later finite reproduction. Before promoting it, specify the complete QBF encoding, bag construction including clause-output/global gadgets and carrier constraints, nonfalse/output conventions, representation size, and exact invocation of the bounded-alternation theorem. This is a proof-completeness gate, not a finding that the theorem is false.

The Phase 5 PDF has no bibliography and is only a short working note. Necessary repairs include the skeleton-only wording in F1 (not every internal split inside a prime block), “rank at most one” for possibly zero restricted factors, full conventions, and the Phase 5B certification and ordered-support qualifications. Do not edit the archived copy.

### (b) Algorithmic claims

A real PySDD/Glucose exact pipeline exists and was extensively checked. Direct extraction followed by exact residual refinement and final carrier merging has a sound architecture. Every nonsingleton exposed block still needs prime certification unless an external theorem/certificate supplies it. A failed vtree cut is not such a certificate.

The live adapter supports matched local searches with one initial compilation, checking moves, undo/replay and retained roots. It implements established vtree operations. The later campaigns test live M1/M2, **not a native re-evaluation of the full Phase 5B carrier-plus-defect M5 objective**. They do not clear M5's original gate or test every proposed carrier/defect heuristic.

No current evidence supports a general polynomial-time extraction result, a practical global optimizer, unrestricted structured-d-DNNF factor recovery, or a superior complete factorization method.

### (c) Negative experimental results

Ratios below are challenger/baseline: greater than one means slower. Distinct campaigns, inputs, comparators and environments must remain separate.

| Frozen study | Primary complete-method result | Correct interpretation |
|---|---|---|
| Phase 5B: 70 synthetic instances, 10 methods, 3 repetitions; 30 held-out inputs, n <= 10 | M5/B3 = **2.211513**, descriptive 95% bootstrap interval **[2.008170, 2.427554]**; 0 wins / 30 losses; practical residual rescue also fails | Algorithmic NO-GO for this implementation and mixture. All 2,100 saved trials have successful status and correctness flags. The benchmark is small and structurally repetitive. |
| First live integration: 12 validation + 24 held-out inputs, 7 methods, 3 repetitions, n <= 14 | L2/B3 = **1.038179**; one-sided 95% upper **1.049606**; 1 win / 23 losses | Mechanism GO / algorithmic NO-GO. B3 already exposes the exact semantic partition on every input, so no exposure gain is available. |
| Revised prospective integration: new 12 + 24 inputs, same method/repetition counts, n <= 14 | L1/B2 = **1.037985**; one-sided 95% upper **1.141542**; 10 wins / 14 losses | Mechanism GO / algorithmic NO-GO. Some exposure gains occur, but not the registered complete-time benefit. This does not establish a statistically clear general slowdown either. |

Both live campaigns have 756 saved successful rows and no recorded method failure or correctness disagreement. The algorithmic gate required ratio <= 0.90 and upper bound < 1, plus correctness/failure conditions; neither passed.

In the revised campaign, live/fresh **search-stage** ratios are **0.180498** for M1 and **0.180870** for M2, with all 72 held-out pairs per objective matching. Thus matched search is about 5.5 times cheaper. That comparison is L1/F1 or L2/F2; the complete-method primary is L1/B2. Changing the denominator or timer would manufacture a speedup claim.

B3 misses the exact direct partition on 12/24 revised held-out cases; L1 misses on 8/24. The four recoveries are four sizes of one equivalence-ladder-bridge family, not four independent application families. This is a post-campaign diagnostic, relative to B3 rather than the selected B2 primary baseline. Keep it as explanatory evidence.

All uncertainty statements are conditional on small constructed sets. Repetitions and sizes from the same family are not independent real-world designs. Do not pool the three studies into one overall effect or regard their thousands of rows as thousands of independent problems. “Complete time” means the registered algorithm timer; process startup, parsing and serialization are separately recorded, not included in that primary timer.

### (d) Reproducibility and tooling

The [reproduction audit][Repro] records six frozen campaigns/eleven matching output artifacts and independently implemented relational checks. Crucially, Phase 5's historical exposure shortcuts used already-known prime partitions. Phase 5B verified their values independently; that does not transform them into scalable non-oracle search evidence.

The later artifact includes raw trials, frozen selections, source hashes, exactness checks, failure controls and bounded Linux stress evidence. The [first audit][Audit] and [repair][Rev] belong with the final campaign: they explain both the exposure-headroom defect and the subsequently tightened integrity checks. Preserve the n=32, 50-step watchdog timeout alongside the successful shorter walk. Stress success is bounded implementation evidence, not a proof of arbitrary-size memory safety.

Positive training-only persistent-SAT reuse and the recorded SDD-size/exposure tradeoff are useful supporting observations. They are not rescues of a failed primary endpoint or separate papers.

The [review ledger][Reviews] explicitly describes three AI agents acting in six roles; the SDD/SAT report includes self-audit. “Independent” here can mean a separate agent, checker or reconstruction. No external human specialist review is established by this record.

### (e) Open research, not current conclusions

Efficient exposure-optimal search; guaranteed favorable defect width; a SAT-runtime bound from structural assumptions; carrier-compatible early refinement; unrestricted representation-class extraction; and useful incidence in natural inputs remain open. A worthwhile future direction would need a new testable mechanism or sharper theorem. Merely enlarging the benchmark or searching for a positive result is not a research contribution.

## 3. Priority and positioning checked against primary sources

The following are focused comparisons, not a systematic novelty clearance.

| Closest literature | Consequence for this project |
|---|---|
| [Olteanu, Koch and Antova, World-set Decompositions][LRel], Section 6, Proposition 10 and Theorems 11–12 | Explicit relational prime-factorization uniqueness and algorithms predate the project. Their explicit-relation input size differs from succinct CNF/SDD size; acknowledge both the antecedent and that representation distinction. |
| [Darwiche, SDD semantics][LSDD] and [Choi–Darwiche, dynamic minimization, 2013][LDyn] | Compressed cofactor structure and rotations/swaps are established. The local cut characterization and F1 should be presented as derived structural facts unless a stronger difference is established. |
| [Lee–Jiang–Hung, DAC 2008][LSat]; [Chen–Janota–Marques-Silva, QBF bi-decomposition][LQBF]; [Capelli–Mengel, STACS 2019][LWidth] | SAT/QBF partition search and bounded-width/fixed-alternation tractability are antecedents. Phase 3 needs more than a carrier-aware restatement to justify its own research paper. |
| [Marques-Silva–Janota–Belov, CAV 2013][LMSMP]; [Janota–Marques-Silva, 2016][LQuery] | Monotone-predicate minimal-set algorithms/query analysis are established. The support predicate is a useful application; a generic deletion bound is not a standalone novelty claim. |
| [de Colnet–Szeider semantic-vtree artifact, 2026][LSem] | I inspected its five-page supplementary proof. Its Lemma 1 concerns relocating functionally defined auxiliary variables to vtree LCAs with O(|Y| |Sigma|) d-SDNNF size; that statement differs from the exposure optimum and defect-support claims. This narrows, but does not complete, the priority comparison. The main-paper PDF was blocked by an OpenReview browser challenge in the web tool; no full-paper clearance is claimed. |
| [Circuit-Aware d-DNNF Compilation, IJCAI 2025][LCircuit]; [A Canonical Generalization of OBDD, SAT 2026][LTDD] | Semantic/circuit-aware compilation and alternative structured representations are active prior work. Broad “semantic-aware vtree” or new representation-tractability claims would be too broad. Neither source by itself establishes that the exact F3 statement has appeared before. |

Bibliographic caution: the semantic-vtree Zenodo metadata/supplement names PMLR volume 284, but the [publisher's volume 284][L284] is NeSy **2025**. The [2026 program][LProgram] and [author publication list][LAuthor] confirm the 2026 contribution, with the author list marking proceedings “to appear.” Cite the verified artifact/program and confirm final proceedings metadata before submission; do not copy the inconsistent volume citation.

The strongest possible short-note center is **the exact information and limitations of factor-exposure/defect certificates**, particularly F3 with its two distinct obstructions. Its elementary nature is a real editorial risk. A specialist must identify a nontrivial new statement or a concrete new use, not merely confirm that the proofs are correct. This assessment neither proves novelty nor proves that every formulation is already known.

## 4. Publication options and concrete gates

### Recommended: one negative-results/reproducibility report

**Possible focus:** “Cheaper Vtree Search Does Not Establish Faster Exact Factorization: A Reproducibility Study.”

**Central claim:** in these registered bounded studies, exact live SDD transformations preserve matched search decisions and reduce search cost, but the selected complete methods fail the preregistered improvement gates. Certification and benchmark headroom must be accounted for when evaluating exposure objectives.

**Start from:** [Phase 5B report][B], [reproduction audit][Repro], [first integration audit][Audit], [revision][Rev] and [final campaign][I2], with short corrected mathematical preliminaries from [T][T].

**Keep together:** all three campaigns, the tooling mechanism, the first dataset's limitation, the repair history and the prospective test. They answer one evolving empirical question. Keep raw trials, environment locks, move traces, public toy controls, SAT-reuse study, proof checkers and detailed stress results in one shared supporting artifact.

**Missing work:** a readable integrated methods/results narrative; exact timer/method definitions; explicit separation of registered and post-hoc analyses; citations and prior-public-release disclosure; external SAT/knowledge-compilation and experimental-method review. If the target expects a reusable software contribution, document a portable read-only analysis entry point and artifact scope in a new working copy. No additional performance campaign is necessary for this narrowly bounded report.

**Readership/form:** knowledge-compilation, SAT/decomposition and experimental algorithm-engineering researchers; a technical report or short workshop/reproducibility contribution is more plausible than a broad algorithms paper. Venue acceptance and current submission rules have not been checked.

**GO gate:** an external specialist finds the documented failure mode and auditable artifact informative beyond an implementation diary; every headline maps to a frozen endpoint; proof/certification and dataset limitations remain explicit; a reviewer can reconstruct reported decisions from saved rows without rerunning a held-out campaign. **NO-GO:** reviewers find the result too narrow for the chosen outlet, or the paper needs unsupported generalization to seem significant. Then retain the existing public artifact and do not manufacture a journal submission.

### Conditional alternative/addition: one focused theorem note

**Central claim:** characterize what vtree cuts and four-corner supports certify, together with an infinite family proving that fixed-context pairwise evidence can completely miss semantic primeness.

**Start from:** [Phase 5 draft][P5] plus [Phase 5B corrected proofs][T], not from concatenating all historical drafts.

**Missing work:** complete self-contained statements/proofs; exact relational/Boolean/SDD antecedent mapping; full recent semantic-vtree comparison; external theorem-level and priority review. Add an explicit novel corollary or application only if actually proved and useful. More finite enumeration cannot substitute for these tasks.

**Readership/form:** Boolean decomposition, knowledge representation and finite relational-factorization specialists; short theory note or an expository/application note if the contribution is pedagogical.

**GO gate:** a reviewer can state precisely which result or application is new, why it is nontrivial, and which closest prior theorem does not already yield it at the same scope. **NO-GO:** only elementary restatements and useful exposition remain. Then use the proofs as preliminaries/appendix of the report or as an openly labelled working note; do not force a second paper.

If both outputs survive their gates, the theorem note owns the full novel proofs; the empirical report cites it and supplies only necessary definitions. Both cite the same versioned artifact. No duplicate theorem novelty claims or repeated campaign “contributions.” If the note cannot stand without the same experiment story, merge it into the report.

### Defer: a genuinely new algorithm or complexity paper

**Central claim would have to be new:** either a stronger representation-sensitive theorem with a useful bound, or a new mechanism that improves complete exact factorization under a prospectively defined workload.

**Start from:** the preserved Phase 3 width argument / Phase 4 restricted classes for theory, or the repaired live implementation for computation.

**Missing work:** the actual new theorem/mechanism; credible comparators; natural/design-disjoint inputs where appropriate; full lifecycle accounting; external review. A new campaign requires separate authorization, a new frozen dataset/protocol and an explicit budget. Existing held-out sets remain historical evaluation data.

**Readership:** parameterized complexity/knowledge compilation for a new bound, or SAT/algorithm engineering for a complete-method result.

**GO gate:** a nontrivial theorem beyond the cited generic mechanisms, or a separately preregistered primary complete-method gate cleared with exactness and fair baselines. **Current decision: NO-GO for drafting this paper.** The earlier <=0.90/upper<1 rule is an example of a clear gate, not a guarantee that passing it on synthetic inputs would establish industrial relevance.

Do not split off independent papers for laminarity, read-once recursion, support shrinking, persistent SAT reuse, live moves, or harness repair on the current evidence. Their value is as assumptions, baseline facts, methods or supporting material.

## 5. Recommended order and stopping rule

1. **Choose the bounded-report claim as the default; preserve the existing evidence release.** Do not begin a broad “new factorization algorithm” manuscript.
2. **Prepare a short external review packet** containing the corrected theorem statements, precise antecedent differences, campaign table and artifact links. Ask specifically whether the theorem bundle has independent novelty and whether the negative experimental lesson merits a short report. This is the next useful work; a local packet can be prepared without external writes, but contacting reviewers requires authorization.
3. **Draft in a new local working copy only after that scope decision.** Default to one report. Split a theorem note only when its separate gate passes. Resolve author metadata, AI-use disclosure, citations, licensing and target-specific requirements before release.
4. **Defer further computation.** Reopen only for a distinct justified theorem/mechanism, not to improve the appearance of these frozen outcomes. If specialist review finds neither novelty nor sufficient empirical value, stop at the existing public artifact.

Closely related packet preparation belongs in this chat because it reuses the evidence map and claim boundaries; **gpt-6-sol/high** is a reasonable economical choice for bounded synthesis and citation checking. A difficult new proof would justify **gpt-6-astra/high**, but no such run is recommended now. These are suitability judgments, not measured savings. External review requires a human specialist; another AI reviewer does not satisfy that gate. No new thread or model run is needed merely to preserve the completed work.

## 6. Assessment verification and limits

This assessment read the three manuscript sources, extracted and visually inspected all three Phase 5 PDF pages, read the controlling proof/reproduction/review records, inspected campaign protocols and relevant timer/analysis code, checked project chats, and consulted primary literature.

Read-only calculations over saved rows independently reproduced:
- Phase 5B: 600/600/900 unique trial cells, successful status/correctness flags, M5/B3 2.211513 and 0/30 wins.
- Both integrations: 252 validation and 504 held-out unique keys, successful status/correctness flags, primary ratios and wins/losses; frozen source hashes matched their receipts.
- Matched live/fresh search ratios using the registered **median of paired repetition ratios**, not a ratio of medians; checked matching tree/partition/selected trace fields with zero mismatches.
- Revised primary bootstrap upper 1.1415416326549648 using the recorded seed and 10,000 resamples; saved raw-file hashes agree with the reports.
- Byte identity of the key current-status/manuscript copies and the public prospective campaign report.

Correctness flags are not a fresh independent proof of every trial: this assessment relies on the preserved independent exactness audits for that stronger claim. It did not rerun solvers, frozen campaigns, stress suites or scientific reproduction scripts. No complete formal proof audit or systematic literature review is claimed.

Only this new Markdown assessment and a disposable PDF-reading image outside the research folders were written. The MIND and all archived/live research files were left unchanged. The repository already had substantial organization-related deletions and untracked files; those were not this assessment's work. No commit, push, message to another person, deployment or publication was performed.

[P3]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Manuscript_Versions/Phase3/THEOREM_NOTE_DRAFT.tex>
[P3R]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Supporting_Research/Original_Theme_Gluing/STRUCTURED_FACTORIZATION_PHASE3_2026-09-29/structured_factorization_phase3/PHASE3_MASTER_REPORT.md>
[P4]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Manuscript_Versions/Phase4/THEOREM_NOTE_DRAFT.tex>
[P4R]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Supporting_Research/Structured_Factorization_Snapshot/continuity_archive/03_UNPACKED_PHASE4/structured_factorization_phase4/PHASE4_MASTER_REPORT.md>
[P5]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Manuscript_Versions/Phase5/THEOREM_NOTE_DRAFT.pdf>
[P5R]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Supporting_Research/Structured_Factorization_Snapshot/continuity_archive/04_UNPACKED_PHASE5/phase5_output/PHASE5_T2_MASTER_REPORT.md>
[B]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Current_Research_Status/PHASE5B_MASTER_REPORT.md>
[T]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/The MIND/01_Papers/03_Structured_Boolean_Factorization/Current_Research_Status/THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md>
[Probe]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_vtree_probe_2026-09-29/REPORT.md>
[I1]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_integration_2026-09-30/CAMPAIGN_REPORT.md>
[Audit]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_integration_audit_2026-09-30/AUDIT_REPORT.md>
[Rev]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_integration_revision_2026-09-30/REVISION_REPORT.md>
[Protocol]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_integration_revision_2026-09-30/CAMPAIGN_PROTOCOL.md>
[I2]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/live_integration_revision_2026-09-30/CAMPAIGN_REPORT.md>
[Cross]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/00_Collection_Index/PAPER_CROSSWALK.md>
[Links]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/00_Collection_Index/LINKED_MIND_WORKSPACES.md>
[Score]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/00_Collection_Index/PUBLICATION_STAGE_SCORECARD_2026-09-30.md>
[Repro]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/REPRODUCTION_AUDIT.md>
[Reviews]: <C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/HOSTILE_REVIEW_LEDGER.md>
[PublicReport]: <https://relative0.github.io/Correspondence_Matrices/results/2026-09-30/structured-factorization/prospective-campaign/CAMPAIGN_REPORT.md>
[LRel]: <https://arxiv.org/pdf/0705.4442>
[LSDD]: <https://www.ijcai.org/Proceedings/11/Papers/143.pdf>
[LDyn]: <https://ojs.aaai.org/index.php/AAAI/article/view/8690>
[LSat]: <https://alcom.ee.ntu.edu.tw/assets/publications/dac08-bd.pdf>
[LQBF]: <https://arxiv.org/abs/1112.2313>
[LWidth]: <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2019.18>
[LMSMP]: <https://sat.inesc-id.pt/~mikolas/cav13.pdf>
[LQuery]: <https://www.sciencedirect.com/science/article/pii/S0004370216000035>
[LSem]: <https://zenodo.org/records/21900606>
[LCircuit]: <https://www.ijcai.org/proceedings/2025/496>
[LTDD]: <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.10>
[L284]: <https://proceedings.mlr.press/v284/>
[LProgram]: <https://2026.nesyconf.org/program/>
[LAuthor]: <https://ac.tuwien.ac.at/publist/sszeider-publications/>

