# START HERE — Mathematical Reconstruction of Matte-Blanco's Unfolding Function and Mental Space

**Handoff date:** 29 September 2026  
**Purpose:** Transfer the full active research thread to a new GPT/Astra account without losing mathematical results, proofs, computations, novelty cautions, or the next research target.

## 1. What this project is

The project began by recovering the strongest mathematical ideas from the 2015 thesis **On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces**. The thesis is treated as a historical source of ideas, not as an authority. The central question became:

> Can successive differentiation/unfolding of a concept be modeled rigorously as a transformation between complexes, while keeping genuine chain boundaries, observational refinement, gluing/reconstruction, and homology conceptually separate?

The work has now progressed well beyond the original thesis operator. The current mathematical core is an **observation-refinement / finite-poset / mapping-cone theory** for changes in observational resolution.

## 2. Read these files first, in this order

1. `00_START_HERE/MASTER_HANDOFF.md` — authoritative current-state summary.
2. `00_START_HERE/CLAIM_STATUS_MATRIX.md` — what is proved, computationally verified, standard prior art, false, or still open.
3. `02_LATEST_HIGHER_DIMENSIONAL_GATE/HANDOFF_TO_MASTER.md` — compact latest-gate handoff.
4. `02_LATEST_HIGHER_DIMENSIONAL_GATE/EXACT_THEOREMS_AND_PROOFS.md` — exact statements/proofs of the newest results.
5. `02_LATEST_HIGHER_DIMENSIONAL_GATE/COUNTEREXAMPLES_AND_OBSTRUCTIONS.md` — sharp failure boundaries.
6. `02_LATEST_HIGHER_DIMENSIONAL_GATE/LITERATURE_PRIORITY_MAP.md` — novelty/priority boundaries.
7. `01_CURRENT_MANUSCRIPT/Observation_Refinement_Descent_and_Cone_Draft_v0.3.pdf` — current integrated manuscript baseline.
8. `01_CURRENT_MANUSCRIPT/MANUSCRIPT_REVISION_SECTION.tex` — **not yet merged** higher-dimensional theorem section prepared after the latest gate.
9. `00_START_HERE/NEXT_RESEARCH_PROMPT.md` — the next research gate.

If time permits, then read the chronological prior gates in folders `03`, `04`, and `05`.

## 3. Current headline result

Let `Q` be the current finite observational `T0` poset. A new Boolean observation gives a refined carrier `Q^psi subset Q x {0,1}`. Define:

- `P`: 1-only coarse states;
- `Z`: 0-only coarse states;
- `C`: genuinely split states.

The **exclusive inversion graph** is the bipartite graph

`E_psi = {(p,z) in P x Z : p < z in Q}`.

If this graph is a **matching**, then for every coefficient ring `R`:

`H_n(Cone(Delta pi);R) ~= direct_sum_{(p,z) in E_psi} H~_{n-2}(lk_{Delta Q}[p,z];R).`

This is all-dimensional and integral. It can carry torsion. It gives a complete homology classification on a natural noninteraction class.

The theorem is proved chain-theoretically and heavily verified computationally. The literature review indicates that the underlying deletion/cofiber machinery is standard, while the exact observation-theoretic two-colour matching specialization and edge-link formula are candidate project-specific contributions. Novelty wording must remain conservative.

## 4. What is NOT true

Do not regress to any of the following claims:

- the original thesis `partial` is the simplicial chain differential;
- the original logical unfolding operator is well-defined modulo arbitrary Boolean presentation;
- cycles equal symmetry;
- proper faces alone reconstruct a filled simplex;
- an exclusive inversion **forest** is sufficient for the matching formula;
- matching implies torsion-free homology or total unimodularity;
- Horn closure is the source of rich higher topology (in the strongest whole-relation formulation it is a neutral regime);
- the project has invented general vertex-deletion, cofiber, nerve, or poset-fiber theory.

## 5. Current manuscript status

`Observation_Refinement_Descent_and_Cone_Draft_v0.3.{tex,pdf}` is the current manuscript baseline. It contains the observation-refinement, descent/cone, and carrier-splitting results through the previous gate.

The latest higher-dimensional matching theorem is **not yet merged** into v0.3. The file `MANUSCRIPT_REVISION_SECTION.tex` is a prepared candidate insertion. Do not merge it blindly: first complete the next research gate and then run a proof/priority/editorial convergence pass.

## 6. Immediate next research target

The matching theorem succeeds because every relative simplex has a unique mixed inversion edge. The first failure beyond matching occurs when exclusive inversion edges share an endpoint; a 3-state two-edge star already creates a new homology class not predicted by independent edge contributions.

The next target is therefore the **exclusive-inversion interaction-core spectral sequence beyond matching**, beginning with structurally controlled interaction graphs:

- maximum degree 2;
- disjoint paths/cycles;
- Ferrers bipartite graphs;
- chordal-bipartite graphs;
- bounded biclique/core size.

The goal is an exact theorem describing when the interaction-core spectral sequence collapses (ideally at `E^2`) and an explicit formula for the surviving homology/differentials. See `NEXT_RESEARCH_PROMPT.md`.

## 7. Reproducibility

The package includes all research scripts and machine-readable outputs created in the gates. Keep exact computations as supporting evidence, not substitutes for proofs. Preserve integral Smith-normal-form checks wherever torsion is relevant.

## 8. Primary source policy

The original thesis and the old `Logical Complexes.tex` notes are included in `06_PRIMARY_SOURCES`. They are historical sources, not authoritative mathematics. Do not silently repair them when describing what the thesis claimed.

## 9. Project principle

Always distinguish:

1. **source-derived historical claims**;
2. **standard mathematics/prior art**;
3. **new proved project-specific theorems**;
4. **computational evidence**;
5. **conjectures/open directions**.

That distinction has been essential to keeping the project mathematically defensible.
