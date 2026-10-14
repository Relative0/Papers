# Interaction Core Gate -- 29 September 2026

Start with **INTERACTION_CORE_RESEARCH_GATE.md** for the verdict and answers to all eleven research questions. **HANDOFF_TO_MASTER.md** is the compact continuation record.

The authoritative incoming package is preserved at:

    ../Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29/

The source ZIP remains in the user's Downloads directory. The extracted archive and its frozen v0.3 manuscript are not overwritten by this gate. The pre-existing matching section remains unmerged; MANUSCRIPT_INTERACTION_SECTION.tex is an additional, separate candidate insertion. It is source only, not a compiled/integrated manuscript.

## Reports

* SPECTRAL_SEQUENCE_CONSTRUCTION.md -- definitions, signs, pages, convergence, exact two-column theorem.
* MAX_DEGREE_TWO_CLASSIFICATION.md -- path/cycle blocks, C4 complex, sharp E3 bound and acyclicity criteria.
* FERRERS_AND_CHORDAL_CASES.md -- star theorems, universality, torsion, collapse failures.
* LOCAL_INTERACTION_MODELS.md -- the requested smallest graph models.
* COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md -- preserved and new negative results, explicit limits.
* C4_COUNTEREXAMPLE_PROOF.md -- hand proof and chain certificate for the eight-state unit d2.
* COMPUTATIONAL_INTERACTION_AUDIT.md -- exact scope, runtime, algorithms, counts, and reproduction commands.
* LITERATURE_PRIORITY_MAP.md -- primary-source theorem comparisons; novelty is not certified.
* ADVERSARIAL_REVIEWS.md -- actual internal attacks and resolutions, with detailed independent review files.

STRUCTURAL_AGENT_NOTES.md and FERRERS_AGENT_NOTES.md are retained derivation records; finalized named reports take precedence if a working note describes an earlier incomplete stage.

## Reproduction

Use Python 3.10 with SymPy 1.14.0. The runtime used here was
`C:\Users\brian\AppData\Local\Programs\Python\Python310\python.exe`.
The bundled document Python lacked SymPy, so it was not used for these calculations. No dependency installation was needed.

Run from this directory:

```powershell
python -B verify_interaction.py --exhaustive-n 5 --random-n 6 --random-trials 5000
python -B verify_local_interactions.py
python -B verify_d2_certificate.py --case all
python -B verify_c4_search.py --trials 20000
python -B verify_c4_search.py --audit-existing
python -B verify_torsion_star.py
python -B canonicalize_interaction_results.py
```

The main verifier imports the original matching verifier from the incoming package using the relative directory structure above. It disables bytecode writes before that import. Main-run outputs are reproducible; timing fields may differ. Targeted star discovery/minimization commands are documented in COMPUTATIONAL_INTERACTION_AUDIT.md and verify_local_interactions.py.

JSON files contain exact witnesses, integral groups, signed chains, and bounded search summaries. CSV files contain case summaries and graph-isomorphism aggregates. File names distinguish the main small-case run from targeted searches and explicit examples; zero higher differentials in the small sample must not be confused with the later counterexamples.

## Conventions and caution boundaries

Mathematical page coordinates are (p,q), with mixed total degree p+q and cone degree p+q-1. Computational page keys use (p,total_degree). Cone homology is reduced topological cofiber homology, or algebraic mapping-cone homology. Available links use augmented chains. The all-exclusive star formula has ordinary homology on its right-hand side.

The gate reaches Level B mathematically. Generic spectral-sequence and obstruction-complex machinery is prior art. Integral extensions, coefficient distinctions, negative results, and nonminimality qualifications are part of the result and must travel with it.

Next recommended phase: proof/priority/editorial convergence in the existing task, before any new manuscript version is merged. No external publication, commit, or push has occurred.
