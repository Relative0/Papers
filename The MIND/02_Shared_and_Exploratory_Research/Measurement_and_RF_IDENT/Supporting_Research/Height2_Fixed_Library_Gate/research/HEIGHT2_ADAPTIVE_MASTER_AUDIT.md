# Height-two fixed-library adaptive identification: master audit

Date: 2026-09-29. Status: completed bounded research gate, with proved structural results, reproducible finite checks, and explicitly unresolved priority/complexity questions.

## Transfer reconstruction

Both supplied archives were safely extracted into this gate directory without modifying the source files or the existing research folders. TRANSFER_VERIFICATION.json records 109 verified full-package manifest entries and 62 verified core entries, no hash failures, and identical content for all 62 shared files. The full archive is the working source; the core is a verified duplicate subset. Nested historical backup archives were retained, not recursively executed or treated as current instructions.

The user-requested handoff, reading order, hostile-audit report/status/handoff, A1 and full v0.4/v0.5 TeX sources were read, with v0.3's height/chain sections, the unification model, ledger and claim-audit entries cross-checked. Original PDFs are preserved; mathematical inspection used their matching TeX. Instructions inside historical documents are research context and do not supersede the current user's scope.

The inherited status remains:

| Result | Preserved status |
|---|---|
| U1 | Valid, standard preorder intersection/restriction |
| U2 | Valid with repair: splitting may reveal internal strict fiber order; no new comparison between descendants of distinct coarse-incomparable points |
| U3 | Valid canonical lexicographic factorization; lexicographic machinery itself standard |
| U4 | Standard octahedral cone triangle / long exact defect sequence, not an unconditional direct sum |
| U5 | Valid pullback iff surviving coarse fibers retain their full fine-label profiles |
| U6 | Valid ONLY with fine measurability explicitly assumed |
| A1 | Chain safe depth ceil(log2 n); some path requires a redundant query; an optimal tree has maximum one redundant query per path; forbidding redundancy prevents identification |

A1's statement survives. Its construction can have singleton branches using no redundant query, so the informal phrase "every path exactly one" is not retained.

The older v0.5 dimension equality and its inherited hardness proof are not used. The transferred claim table ALREADY flags V5-06 false and V5-07 in need of major repair. Its V5-09 ambient-complex repair, preserving unsupported deleted-edge rows, is also retained. These are existing corrections, independently confirmed here. The older exact chain trichotomy is tagged prior-art-equivalent in that table, with an unlocated Ehrenborg-Kitaev proof caution; A1's later narrow novelty assessment is not promoted to a broad chain-classification claim.

## Current theorem results

| ID | Result | Status and scope |
|---|---|---|
| H1 | Branch cancellation; current order is P0 restricted to the current support | Proved, elementary |
| H2 | Exact cell-provenance graph restriction and relative boundary submatrix; removed rows are zero on retained columns | Proved |
| H2a | Child relative H2 injects into parent relative H2; actual column matroid undergoes deletion | Proved |
| H2b | If parent query is safe, child safety iff surviving deleted-edge and deleted-triangle counts agree; failure is lost anchoring | Proved |
| H2c | Augmented [B,I] graphic matroid evolves by an explicit deletion/contraction minor | Proved, standard matroid specialization |
| H3 | Useful activation and deactivation both occur minimally on three states, through legal conditioning | Proved, exhaustive checks agree |
| H4 | Support-only exact DP and feasibility recursion | Proved, standard planning specialization |
| H5 | Maximal finite penalty n-1-ceil(log2 n), attained on connected actual-height-two posets | Proved for an explicit oriented library |
| H6 | Complement-closed parity complete-bipartite family: safe depth n/2+log2 n-1 versus ordinary log2 n | Proved for n=2^k; actual height one |
| H7 | RF-SAFE polynomial; RF-DEPTH NP-complete; RF-IDENT polynomial at height <=1 and in NP at height <=2 | Proved; general height-two RF-IDENT complexity remains open |
| H8 | Main synthesis of exact restriction, lost-anchor deactivation and adaptive consequences | Proved; novelty provisional |

Safety always means one-bit refinement BEFORE conditioning. Height two means chains of at most three elements. The topology is carried by the order complex. Tests are supplied oriented Boolean functions; no complement or formula is synthesized unless it belongs to the fixed library.

The original ProLT coordinate family determines structural distinguishability; its hidden-state values are not a free run-time oracle. Otherwise an initial T0 signature would make the identification task vacuous. Query activation here concerns admissibility, not the U6 measurability obstruction, which vanishes after T0.

## Verification performed

Two implementations independently construct (A) the rooted repair graph and (B) the relative F2 matrix. Neither calls the other.

| n | Naturally labelled posets, height <=2 | Boolean query cases |
|---:|---:|---:|
| 1 | 1 | 2 |
| 2 | 2 | 8 |
| 3 | 7 | 56 |
| 4 | 39 | 624 |
| 5 | 330 | 10,560 |
| 6 | 4,117 | 263,488 |
| Total | 4,496 | 274,738 |

There were zero graph/matrix disagreements. Natural labelling includes every isomorphism class, often multiple times; these are not unlabelled counts or counts of all labelled orders. The exact-height-two slice reproduces the v0.4 totals of 184,088 query cases and 38,067 nonredundant safe observations.

Fixed-library enumeration covered all 639,433 effective oriented libraries through four states. Constants were omitted because they are useless, while complements remained distinct. Larger reconnaissance covered 6,600 seeded cases at n=5 and 4,000 at n=6, not all libraries. Independent uncached matrix-based tree search checked 1,730 instances. All 94 reported protocol nodes were checked against actual original library queries.

A third standalone implementation checked exact boundary restriction, zero removed-row blocks, kernel monotonicity and the safe-parent count criterion in 337,138 poset/query/support cases through five vertices, including 187,015 with safe parent. All assertions passed.

The extremal star and genuine-height-two families were checked through n=12. The complement-closed parity family has independently computed depths:

| n | Ordinary depth | Safe depth | Proved formula |
|---:|---:|---:|---:|
| 4 | 2 | 3 | 3 |
| 8 | 3 | 6 | 6 |
| 16 | 4 | 11 | 11 |

Scripts, seeds, logs, CSV/JSON, original-query protocols and hashes are in ../computations/. Enumeration supports the proofs; it is not used to infer universal statements.

## Explicit answers to the requested final questions

1. **Branch cancellation?** Yes, exactly on each answer fiber.
2. **Safety hereditary?** No at height two. Safety on all induced supports is equivalent to isotonicity.
3. **Unsafe to safe?** Yes, including informative legally reachable activation.
4. **Safe to unsafe?** Yes, through loss of anchors; no new relative H2 cycle is created.
5. **Smallest examples?** Three states for useful activation and deactivation; two-state activation is possible only with a constant singleton restriction.
6. **Ordinary feasible, safe impossible?** Yes: descending test 10 on a two-chain is minimal.
7. **Finite strict depth penalty?** Yes, first possible at four states; universal finite gap bound is sharp.
8. **Unbounded penalty?** Yes; even complement-closed libraries have exact gap n/2-1 in a connected family.
9. **Exploit initially unavailable tests?** Yes: the three-state fork activation protocol requires one.
10. **Genuine adaptive advantage over nonadaptive safe protocols?** Yes relative to precisely defined initially-safe sublibraries, full-carrier safe-prefix sequences, and jointly safe separating blocks. No separation from all predetermined schedules with branchwise conditioning is claimed.
11. **Graph/matroid explanation?** Yes: provenance-aware graph deletion/root splitting, actual column-matroid deletion, augmented graphic-matroid minor, and lost-anchor cokernel.
12. **Strongest exact natural family?** The complement-closed parity complete-bipartite depth formula; arbitrary-library stars also have an exact feasibility criterion. These occur at height one; genuine-height-two general feasibility remains open.
13. **Different from standard restricted decision trees?** Planning is exactly a support-dependent legal-action decision tree. Specialized content lies in the legal-action geometry, not the recurrence.
14. **Best publication candidate?** A compact package centered on exact restriction/anchor-loss dynamics, supported by the exact complement-closed family and the height-one/height-two feasibility boundary.
15. **Novelty confidence?** Low-to-moderate pending theorem-level priority review. Generic dynamic programming, graph incidence and matroid machinery are standard.
16. **Single highest-value next step?** Resolve general height-two RF-IDENT feasibility complexity or a sharply specified natural height-two subclass, using the minimal deactivation obstruction; do not broaden the framework.

## Deliverable map and limits

MAIN_THEOREM.md is the concise proof roadmap. REPAIR_GRAPH_DYNAMICS.md and ADAPTIVE_DEPTH_THEORY.md contain the principal proofs. FORMAL_ADAPTIVE_MODEL.md, BRANCH_CANCELLATION.md, QUERY_ACTIVATION_DEACTIVATION.md, FIXED_LIBRARY_IDENTIFICATION.md, MATROID_INTERPRETATION.md, STRUCTURED_LIBRARY_RESULTS.md and COMPLEXITY_AUDIT.md isolate their assumptions. LITERATURE_PRIORITY_AUDIT.md, HOSTILE_REFEREE_REPORTS.md, COUNTEREXAMPLES.md, OPEN_PROBLEMS.md and HANDOFF_TO_MASTER.md record scope and next steps.

The independent structural and complexity reports are retained as supporting audits. No publication, remote write, commit or push was performed. Existing unrelated working-tree changes were not modified.

This bounded gate is complete. A general solution to every open question, an exhaustive search of all larger libraries, and a certified exhaustive literature review are not claimed.
