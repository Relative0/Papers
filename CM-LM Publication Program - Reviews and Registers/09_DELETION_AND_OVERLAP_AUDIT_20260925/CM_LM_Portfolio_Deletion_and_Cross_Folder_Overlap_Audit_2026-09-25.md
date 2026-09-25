# CM–LM Portfolio Deletion and Cross-Folder Overlap Audit

**Audit date:** 2026-09-25

## Decision

The folder CM_LM_PUBLICATION_PORTFOLIO_20260921 is now redundant at the file-content level: all 353 files, totaling 62,793,791 bytes, have at least one byte-identical SHA-256 match elsewhere under Papers for Publication.

I do not recommend deleting it yet. The newly organized folders are still untracked local repository content. Delete the portfolio only after the replacement folders have been committed and pushed, or after another verified backup has been made. At that point, deleting the portfolio will not remove the only copy of any file found in this audit.

This conclusion concerns preservation of the present bytes. The portfolio still has value as a historical package because its directory structure records the 2026-09-21 release arrangement. The root inventory and program reports preserving that context have now been copied to the publication-program register.

## Portfolio coverage

| Portfolio section | Files | Preserved home |
|---|---:|---|
| Root inventory, hashes and README | 3 | CM-LM Publication Program - Reviews and Registers / 07_PORTFOLIO_PROVENANCE_20260921 |
| 01 P01 chain-ring contextuality/resources | 23 | Chain Ring Contextuality and Exact Resources (P01) |
| 02 P02 characteristic-two query obstructions | 22 | Exact Query Bounds in Characteristic Two (P02) |
| 03 operator-level Boolean computation | 32 | CM Computation |
| 04 process-semantics companion and verification | 79 | Chain Ring Process Semantics (Technical Companion) |
| 05 canonical correctness audit | 165 | CM Correctness Audit and Model Boundaries (Technical Report) |
| 06 program-level reports | 15 | CM-LM Publication Program - Reviews and Registers / 08_PORTFOLIO_PROGRAM_REPORTS_20260921 |
| 07 legacy/preconsolidation material | 14 | Modal Quantum CM-LMs, CM Computation, ProLT, and the publication-program register |

Before the final preservation pass, 21 portfolio files had no exact copy outside the portfolio. Those files are now preserved as follows:

- Fifteen program-level architecture, citation, research-gap, QA, claim-change and reproduction-supplement files were copied into the program register.
- The portfolio inventories and root README were copied into the program register.
- The legacy-section README was copied into the program register.
- The older operator-level computation PDF was copied into CM Computation / 03_LEGACY_AND_PRECONSOLIDATION.
- ProLT core v0.6 was copied into ProLT / 03_LEGACY_VERSIONS.

The three ZIP files that Git previously left untracked inside the portfolio also have byte-identical copies elsewhere: the two phase-calculus packages are in Modal Quantum CM-LMs, and the reproduction supplement is now in the program register.

## Cross-folder uniqueness result

The organized folders are not uniformly unique. Most manuscript and companion folders have distinct central documents, but two research-direction folders currently contain only curated copies of material held elsewhere. Several other folders intentionally duplicate evidence so that their packages remain self-contained.

The exact-overlap scan covered 694 files across the 18 organized folders, excluding the source portfolio, generated publication-context notes and SHA-256 manifests. It found 53 SHA-256 groups occurring in more than one top-level folder.

| Folder | Exact duplicate files | Duplicate bytes | Assessment |
|---|---:|---:|---|
| Certified CM-LM Guard Synthesis (Research Direction) | 100% | 100% | Reference/index folder only; no unique research artifact yet |
| Compact CM Spectral and Dynamical Atlas (Research Direction) | 100% | 100% | Reference/index folder only; no unique atlas manuscript or result set yet |
| CM Computation | 25.5% | 67.7% | Revised compiler is unique; much of the large duplicated content is foundations and predecessor material |
| LM-Modal Bridge (Technical Companion) | 23.1% | 59.9% | Bridge report/package is distinct; large audit datasets are duplicated for provenance |
| CM-LMs and lifting | 75.0% | 52.9% | Foundations home; duplicates arose because the compiler package carried foundations and review files |
| Guarded Boolean Operator (Paper B) | 75.0% | 52.6% | Current paper is distinct; its release was copied wholesale into the guard-synthesis direction |
| CM Correctness Audit and Model Boundaries | 12.1% | 17.8% | Distinct audit; some evidence datasets also occur in the bridge package |
| ProLT Observation Design and Safe Refinement | 75.0% | 7.8% | Notes are distinct; small verification programs/results and ledger are shared |
| CM Structural Computation and Decomposition | 14.3% | 7.6% | Mostly distinct reports; one planning document is shared with guard synthesis |
| General ProLT Observation Refinement | 66.7% | 6.9% | v0.1/v0.2 notes are distinct; verification and ledger material is shared |
| ProLT | 9.1% | 3.5% | Core manuscript is distinct; ledger and historical version relationships remain |
| ProLT-Homology | 18.8% | 2.0% | Current homology paper is distinct; verification scripts/results are shared |
| Program reviews and registers | 9.4% | 1.1% | Intentional central index; theorem-bank files also appear in the atlas folder |
| P01 chain-ring paper | 4.3% | effectively 0% | Distinct paper; only a 146-byte build-stage record matches P02 |
| Process-semantics companion | 10.1% | effectively 0% | Distinct companion; repeated files are empty placeholders |
| P02 query-bounds paper | 4.5% | effectively 0% | Distinct paper; only a 146-byte build-stage record matches P01 |
| Finite-Jet Rigidity | 0% | 0% | Exact-file unique in the organized set |
| Modal Quantum CM-LMs | 0% | 0% | Exact-file unique in the organized set |

Percentages describe exact file identity across top-level folders, not thematic similarity.

## Substantive overlap map

### CM Computation and CM-LMs and lifting

These are different paper families, but the compiler audit package carries an exact copy of the LM-centered foundations PDF/LaTeX, the foundations audit, and several review responses. CM Computation also preserves the older 24-page compiler predecessor beside the revised 14-page compiler.

The working distinction should remain:

- CM-LMs and lifting owns the foundations/operator-calculus paper.
- CM Computation owns the compiler, normalization/tabulation rules, S/T/H provenance and scoped completeness result.
- Foundations files inside CM Computation are supporting references, not a second compiler manuscript.

### Guarded Boolean Operator and Certified CM-LM Guard Synthesis

The guard-synthesis folder duplicates the current guarded release: PDF, LaTeX, referee report, revision notes, case-study results and verifier. Its planning document is also duplicated in the structural-computation folder.

Therefore, Certified CM-LM Guard Synthesis is not presently a separate paper package. It is a placeholder for a future synthesis algorithm, certificate system or application. Its only unique item is the generated context/status note, which was excluded from the overlap percentages.

### Compact CM Spectral and Dynamical Atlas

All substantive files in this folder are exact copies from the foundations folder or program register: the audit, master inventory and theorem bank.

Therefore, the atlas is not presently a unique paper or result package. It is a research-direction index. It becomes a distinct project only after classification outputs, traceable generation code, tables, proofs or an atlas manuscript are added.

### General ProLT Refinement, Observation Design and ProLT-Homology

The v0.1/v0.2 general-refinement notes and v0.3–v0.5 observation-design notes are substantively different starting drafts, but the two direction folders share fourteen verification/ledger files. Five verification files also occur in the ProLT-Homology reproducibility package.

There is also a very close version relationship between the v0.8 core PDF copied into the general-refinement folder and the v0.8.1 manuscript in ProLT. The v0.8.1 file should be treated as the current core version.

The paper boundaries remain defensible:

- ProLT owns the core observation/distinguishability/inference framework.
- ProLT-Homology owns binary order thinning and its sharp limits.
- General ProLT Observation Refinement concerns refinements that can change the quotient carrier.
- Observation Design and Safe Refinement concerns constrained observation choice and joint-versus-sequential safety, but it is not submission-ready and contains a corrected false observation-dimension claim.

### LM-Modal Bridge and the canonical correctness audit

The bridge package and correctness-audit package share eighteen exact evidence datasets, including the large 65,536-row resource inventory and teleportation, coding, contextuality and branch-rank tables.

The documents themselves serve different purposes. The bridge preserves the scalar-enrichment and support/satisfiability construction; the correctness audit owns model contracts, corrections and program-wide validation. Keeping the repeated evidence in both self-contained archival packages is reasonable.

### P01 and the process-semantics companion

P01 is a distinct research paper. The process-semantics material is a technical companion that supplies closure, conditioning, normalizer, filter-order and disposal analysis. It supports P01 but does not duplicate P01’s main chain-ring classification and exact resource-comparison results.

### Finite-Jet Rigidity and the guarded-operator paper

These papers descend from the same continuous-score parent draft. Finite-Jet Rigidity owns finite-jet/sign-law rigidity. The guarded paper owns quotient-by-sign semantics, zero handling, restricted dispatch and minimum probes. No exact current manuscript files overlap, but their shared lineage should be disclosed and cross-cited.

### Modal/phase papers, P01 and P02

They share Boolean, modal and CM/LM foundations, but their principal results differ:

- The signed/integral phase paper and intrinsic Boolean phase-algebra paper study phase models and pattern algebra.
- P01 studies chain-ring contextuality, coding and teleportation resources.
- P02 studies exact charged-oracle query bounds in characteristic two.

References to teleportation, ANF, modal computation or finite rings do not make these the same paper.

## Recommended cleanup

No deletion or deduplication was performed during this audit.

After the new organization is committed and pushed:

1. The old portfolio may be deleted if retaining its release layout is no longer useful.
2. Convert Certified CM-LM Guard Synthesis into a lightweight research brief with references to the guarded-paper folder, unless a unique algorithm or manuscript is added.
3. Convert Compact CM Spectral and Dynamical Atlas into a lightweight research brief with references to the foundations/register files, unless unique generated outputs or a manuscript are added.
4. Keep the duplicated correctness/bridge datasets and ProLT verification files when self-contained reproducibility packages are desired.
5. In CM Computation, clearly mark foundations copies as references and the revised compiler as the working manuscript head.

## Verification limits

SHA-256 establishes exact preservation and exact duplication. Near-version screening used extracted PDF text and LaTeX/Markdown text to identify materially related drafts. It confirmed the known ProLT v0.8/v0.8.1 and compiler predecessor/revision relationships. Topic-level boundaries rely on the detailed manuscript audit and theorem/claim comparison already preserved in the publication-program register.

The audit does not authorize or perform deletion. It establishes the condition under which deletion is preservation-safe.