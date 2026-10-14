# Focused literature and priority audit

Search date and cutoff: **2026-09-29**. Scope: the claims in this Phase 5B implementation and the frozen structural results. This is a focused web audit, not a systematic review or proof that no antecedent exists. Primary publisher pages, author-hosted papers, author repositories, and author-deposited artifacts support the entries. Search queries and limitations are recorded in `data/literature_search_log.json`.

**Priority verdict:** dynamic vtree search, SDD minimization, graph/hypergraph-guided compilation, independent-component decomposition, SAT/QBF bi-decomposition, and monotone support deletion are established techniques. The Phase 5B contribution is a verified application and a bounded experimental evaluation of the factor-exposure objective. The proofs can survive even if the algorithmic result is a NO-GO, but their validity is not a novelty certificate. No firstness claim is made.

## Claim-by-claim matrix

| Claim or ingredient | Primary antecedent / evidence | Classification and safe claim |
|---|---|---|
| Dynamic vtree rotations and child swaps | Choi and Darwiche, AAAI 2013 [R1] | Established prior art; never claim the neighborhood itself is new |
| Optimize compressed SDD size by dynamic search | [R1] | Established baseline; must compare with the library's own minimizer |
| Treewidth/dtree/vtree-guided compilation | Bova and Szeider 2017 [R6]; de Colnet 2024 [R5]; TDD 2026 [R10] | Established theory and practice; a basic min-fill implementation is only a modest baseline |
| Dynamic hypergraph partitioning and components | Lagniez and Marquis 2017 [R4] | Established compiler design; carrier/defect inputs do not confer novelty on partitioning |
| Persistent SAT across Boolean bi-decomposition queries | Lee, Jiang and Hung 2008 [R2] | Established technique; selectors are a concrete encoding, not a new paradigm |
| QBF partition optimization for decomposition | Chen, Janota and Marques-Silva 2012 [R3] | Established technique and disjointness/balance objectives |
| Direct compressed-cofactor cut test | Mathematical proof in this package, grounded in SDD cofactor semantics | Valid elementary consequence; exact first appearance not determined |
| Global factor-exposure optimum F1 | Mathematical proof in this package | Valid project formulation; existence does not imply efficient search or new general decomposition theory |
| Laminar carrier/semantic obstruction F2 | Standard hierarchy/clade property, proof supplied | Known combinatorial fact applied to the project; do not market as discovery of laminarity |
| Defect support crosses some prime block F3 | Explicit rank/product proof supplied | Supported theorem; exact prior formulation unresolved; only existential crossing is certified |
| Pairwise localization NO-GO for the two-point equality relation | Explicit proof and checks supplied | Supported counterexample; elementary structure, no firstness claim |
| Read-once CM gate-rank recursion | Classical read-once functions [R14]; proof supplied | Compact CM formulation within a well-studied class; not a new efficient read-once factorization paradigm |
| Canonical Cartesian prime factorization | World-set relation factorization [R15] | Established broader concept; representation-sensitive complexity matters |
| Greedy equality-assumption support minimization | MSMP literature [R7,R8] | Known technique applied to a CM defect predicate |
| Output-sensitive group-deletion query bound | Generic monotone-predicate/group-deletion reasoning [R7,R8] | Proved here for clarity; not asserted novel, not a SAT-runtime/FPT result |
| Soft support hyperedges in a factor-exposure score | The concrete implementation and experiments | Potentially distinctive application; no comprehensive priority clearance, no correctness content beyond F3 |
| Compilation objectives beyond representation size | QBF decomposition quality [R3], query-dependent utility [R11], circuit-aware simplification [R9] | Broad novelty claim is untenable; distinguish the exact factor-exposure objective from adjacent objectives |
| Semantic vtree construction | 2026 NeSy author artifact [R12] | Closely adjacent recent work; paper-level comparison remains a publication prerequisite |
| Circuit graph/min-cut vtree initialization | 2026 TPM workshop [R13] | Direct recent antecedent for weighted interaction-graph/static construction |
| Industrial total-runtime improvement | Requires this package's preregistered held-out evidence | Empirical contribution only; maintained tools on small instances are not industrial-scale validation |

## Primary references and implications

**[R1] Arthur Choi and Adnan Darwiche. Dynamic Minimization of Sentential Decision Diagrams. AAAI 2013.** The paper explicitly navigates vtrees using rotations and child swaps and evaluates a dynamic size-minimization heuristic. Both operations and the search paradigm predate this project. [Publisher and DOI](https://ojs.aaai.org/index.php/AAAI/article/view/8690).

**[R2] Ruei-Rung Lee, Jie-Hong Roland Jiang and Wei-Lun Hung. Bi-Decomposing Large Boolean Functions via Interpolation and Satisfiability Solving. DAC 2008.** Incremental SAT and interpolation are used to explore decompositions and variable partitions. A four-corner implementation cannot claim priority for incremental SAT bi-decomposition. [Author-hosted paper](https://alcom.ee.ntu.edu.tw/assets/publications/dac08-bd.pdf).

**[R3] Huan Chen, Mikoláš Janota and João Marques-Silva. QBF-Based Boolean Function Bi-Decomposition. DATE 2012; preprint 2011.** It optimizes disjointness and balancedness of variable partitions. This is relevant both to decomposition machinery and to objectives other than representation size. It does not by itself establish antecedence for the exact SDD-exposure objective here. [Author preprint](https://arxiv.org/abs/1112.2313).

**[R4] Jean-Marie Lagniez and Pierre Marquis. An Improved Decision-DNNF Compiler. IJCAI 2017.** d4 combines disjoint-component analysis, component caching, and dynamic hypergraph partitioning. These are essential prior-art boundaries for syntax and hypergraph baselines. [Publisher](https://www.ijcai.org/proceedings/2017/93).

**[R5] Alexis de Colnet. On the Relative Efficiency of Dynamic and Static Top-Down Compilation to Decision-DNNF. SAT 2024.** It studies dynamic graph partitioning versus static tree-decomposition guidance, showing separations in both directions for the modeled strategies. Therefore this pilot cannot claim one broad strategy universally dominates the other. [Publisher](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2024.11).

**[R6] Simone Bova and Stefan Szeider. Circuit Treewidth, Sentential Decision, and Query Compilation. PODS 2017.** This is an established connection between treewidth, SDD structure and compilation parameters; factor-width terminology already has an independent technical meaning. [DOI](https://doi.org/10.1145/3034786.3034787). The citation and topic were cross-checked in the current SAT 2026 TDD reference list [R10]; no uninspected theorem details from this paper are relied upon.

**[R7] João Marques-Silva, Mikoláš Janota and Anton Belov. Minimal Sets over Monotone Predicates in Boolean Formulae. CAV 2013.** This is direct prior art for reducing many minimal-set tasks to a common monotone-predicate problem. Equality-limited defect existence is another such predicate. [Author-hosted paper](https://sat.inesc-id.pt/~mikolas/cav13.pdf). See also the expanded reductions discussion in [Marques-Silva and Janota, 2014](https://arxiv.org/abs/1402.3011).

**[R8] Mikoláš Janota and João Marques-Silva. On the Query Complexity of Selecting Minimal Sets for Monotone Predicates. Artificial Intelligence 233, 2016.** It studies oracle-query bounds, including stronger witness-oracle results under structural restrictions on minimal sets. This makes a generic deletion or group-testing query bound a poor standalone novelty claim. The package's simple proof does not purport to reproduce all results of this paper. [Publisher/DOI](https://doi.org/10.1016/j.artint.2016.01.002).

**[R9] Vincent Derkinderen and Jean-Marie Lagniez. Circuit-Aware d-DNNF Compilation. IJCAI 2025.** It uses original circuit structure and identifies/eliminates don't-care variables during compilation, with empirical benefits in solved instances and circuit size. Decomposition-aware use of semantics and original structure is an active area; the current project must identify its precise objective and certificate rather than claim generic semantic awareness. [Publisher](https://www.ijcai.org/proceedings/2025/496).

**[R10] Florent Capelli, YooJung Choi, Stefan Mengel, Martín Muñoz and Guy Van den Broeck. A Canonical Generalization of OBDD. SAT 2026, published 2026-07-16.** It introduces Tree Decision Diagrams as structured d-DNNFs and relates compilation to treewidth and factor width. This is a nearby alternative representation, not evidence that arbitrary structured d-DNNFs support all SDD operations. [Publisher](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.10).

**[R11] Kengo Nakamura, Masaaki Nishino and Norihito Yasuda. Variance Computation for Weighted Model Counting with Knowledge Compilation Approach. AAAI 2026, publisher date 2026-03-14.** It studies a downstream query that is tractable on structured d-DNNF but harder on several neighboring languages. It illustrates why query utility can matter beyond raw circuit size; it is **not** a direct antecedent for the factor-exposure search score. [Publisher](https://ojs.aaai.org/index.php/AAAI/article/view/39007).

**[R12] Alexis de Colnet and Stefan Szeider. LLM-guided Semantic Vtrees for SDD Compilation. NeSy 2026.** The author-deposited artifact, published 2026-08-12, contains implementation, prompts, experimental data and a supplementary proof, and is independently listed in the NeSy program. Its semantic-vtree focus is close enough that an exact comparison is required before a submission. This audit inspected artifact metadata and conference listing, not the complete paper and supplement; no inference about an identical factor-exposure theorem is made. [Author artifact](https://zenodo.org/records/21900606), [conference program](https://2026.nesyconf.org/program/).

**[R13] Sander Verwimp, Annegret Seibt and Vincent Derkinderen. Growing Vtrees from Variable Orderings: Novel Static Heuristics for SDD Compilation. TPM 2026 workshop.** The workshop abstract describes a fan-in heuristic and a weighted interaction graph recursively partitioned by minimal cuts. This is directly relevant to graph-guided vtree initialization. Treat workshop status separately from archival publication. [Workshop abstract](https://tractable-probabilistic-modeling.github.io/tpm2026/papers/), [author dataset, published 2026-08-03](https://doi.org/10.48804/MQYNKZ).

**[R14] Functions That Are Read-Once on a Subset of Their Inputs. Discrete Applied Mathematics 46, 1993.** This primary paper builds on classical read-once characterizations. It is evidence of the established theory, not a theorem-by-theorem match for the arbitrary essential-binary-gate CM recursion. That exact match remains unresolved. [Publisher](https://www.sciencedirect.com/science/article/pii/0166218X9390105W).

**[R15] Dan Olteanu, Christoph Koch and Lyublena Antova. World-Set Decompositions: Expressiveness and Efficient Algorithms.** The 2007 preprint and later journal treatment include efficient factorization of explicit relation-based representations. They undermine any broad novelty claim for Cartesian prime decomposition; they do not turn a compact arbitrary CNF into an explicit relation at polynomial cost. [Author preprint](https://arxiv.org/abs/0705.4442), [institutional publication record](https://ora.ox.ac.uk/objects/uuid%3Af3203a80-a683-4f37-b700-e7ef1f8bb779).

**[R16] Harry Vinall-Smeeth. Structured d-DNNF Is Not Closed under Negation. IJCAI 2024.** It establishes limitations for negation, disjunction and existential quantification and a succinctness separation from SDD. These support the archive's decision not to assume cheap arbitrary structured-d-DNNF normalization. They do **not** prove that every possible direct factorization algorithm is impossible. [Publisher](https://www.ijcai.org/proceedings/2024/398).

**[R17] Zhenghang Xu, Minghao Yin, Jianan Wang and Jean-Marie Lagniez. A Distributed Framework for Compiling and Reasoning with d-DNNF. 2026 preprint, 2026-07-15.** This recent work explicitly considers compilation plus subsequent model counting/direct access/sampling and distributed decomposition. It is adjacent context for end-to-end workload objectives; the audit does not adopt its priority claims or treat a preprint as a verified industrial baseline. [Author preprint](https://arxiv.org/abs/2607.13642).

## Corrections and unresolved priority work

The search also returned *Compilation and Fast Model Counting beyond CNF* under a February 2025 arXiv date. The primary SAT 2026 reference list identifies its conference publication as **IJCAI 2024**, so it must not be counted as newly published 2025 conference work just because of a later preprint posting. [Conference reference](https://www.ijcai.org/proceedings/2024/367).

The exact F1/F3/CM formulation may be useful as a concise note, but the current audit does not establish that these elementary statements are publishably novel. In particular, compare relational-factorization and Boolean-decomposition theorems at theorem level, inspect the full 2026 semantic-vtree paper, and compare its representation/compilation objective with E_T before claiming a new semantic-vtree principle. The pilot's negative or null runtime result must not be rebranded as a new algorithmic contribution.

No broad survey expansion is required to execute the pilot. The remaining priority tasks are publication prerequisites only. A safe present posture is a reproducibility package and mathematical working note, with established ingredients cited and algorithmic claims restricted to the preregistered measurements.
