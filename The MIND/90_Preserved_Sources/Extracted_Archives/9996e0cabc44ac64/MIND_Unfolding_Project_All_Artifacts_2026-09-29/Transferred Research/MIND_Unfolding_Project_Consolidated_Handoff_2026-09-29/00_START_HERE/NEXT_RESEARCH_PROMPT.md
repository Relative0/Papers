# Next Research Gate — Interaction-Core Spectral Sequence Beyond Matching

**Project:** Mathematical Reconstruction of Matte-Blanco's Unfolding Function and Mental Space  
**Thread:** Observation refinement, carrier splitting, higher-dimensional inversion complexes

## Required starting materials

Use this consolidated package as the authoritative project handoff. Before beginning, read:

1. `00_START_HERE/MASTER_HANDOFF.md`;
2. `00_START_HERE/CLAIM_STATUS_MATRIX.md`;
3. `02_LATEST_HIGHER_DIMENSIONAL_GATE/EXACT_THEOREMS_AND_PROOFS.md`;
4. `02_LATEST_HIGHER_DIMENSIONAL_GATE/COUNTEREXAMPLES_AND_OBSTRUCTIONS.md`;
5. `02_LATEST_HIGHER_DIMENSIONAL_GATE/INVERSION_CHAIN_COMPLEX.md`;
6. `02_LATEST_HIGHER_DIMENSIONAL_GATE/LITERATURE_PRIORITY_MAP.md`;
7. `02_LATEST_HIGHER_DIMENSIONAL_GATE/ADVERSARIAL_REVIEWS.md`;
8. `07_RELATED_THEORY/binary_order_thinning_finite_posets_reviewed_v3.tex` where needed for the known higher-dimensional obstruction boundary.

The latest files supersede earlier formulations where they differ.

---

## Role

Act as an independent mathematical research panel specializing in finite posets, combinatorial topology, spectral sequences, discrete Morse theory, relative simplicial homology, graph/biclique structure, homotopy colimits, integer Smith normal form, and algorithmic topology.

This is a theorem-discovery gate, not an editorial pass.

Your task is to determine whether the **interaction-core filtration** of the higher-dimensional carrier-splitting inversion complex admits a second exact theorem beyond the exclusive-inversion matching case.

Do not optimize for a positive result.

---

## 1. Frozen baseline

Let `Q` be the old finite observational `T0` poset and let a new Boolean observation give `Q^psi subset Q x {0,1}`.

Let:

- `P` = 1-only coarse states;
- `Z` = 0-only coarse states;
- `C` = genuinely split states.

Define the exclusive inversion graph

`G_psi = (P sqcup Z, E_psi)`

with

`E_psi = {(p,z): p<z in Q}`.

In the full doubled product `D=Q x {0<1}`, let `K=Delta D` and let `L=Delta Q^psi` be the induced complex after deleting the missing lower copies of `P` and missing upper copies of `Z`.

The mapping-cone defect is represented by the relative pair `(K,L)`.

The latest gate proved:

### Matching theorem

If `G_psi` is a matching, then for every coefficient ring `R`,

`H_n(Cone(Delta pi);R) ~= direct_sum_{(p,z) in E_psi} H~_{n-2}(lk_{Delta Q}[p,z];R)`.

This theorem is frozen.

### Sharp failure of forest extension

The coarse chain `0<1<2` with `(1-only,0-only,0-only)` has exclusive graph `K_{1,2}` but produces `H~_1 ~= Z` even though the independent edge-link sum vanishes.

Therefore any theorem beyond matching must explicitly account for **shared-endpoint/higher-core interactions**.

---

## 2. Interaction-core filtration

For a relative simplex `sigma`, define its missing/interacting core `S(sigma)` to be the subset of missing vertices contained in `sigma`.

Filter the relative chain complex by core size:

`F_r C_* = span{sigma : |S(sigma)| <= r}`.

The associated graded complex is already known to decompose over mixed cores into shifted available-link complexes. Mixed cores are precisely **chain-supported bicliques** of the exclusive inversion graph.

Your first task is to reconstruct this filtration carefully, fix indexing/sign conventions, and write the spectral sequence explicitly, including the `E^0`, `E^1`, and the first potentially nonzero interaction differential.

Do not claim novelty for the general filtered-complex spectral-sequence machinery.

---

## 3. Primary structural classes to attack

Investigate these in parallel before committing to one.

### Class A — maximum degree at most 2

`G_psi` is a disjoint union of paths and even cycles.

Questions:

- Does the core-size spectral sequence collapse at `E^2`?
- Can the `d^1` differential be written explicitly as a signed incidence operator between edge-link and 3-vertex-core link groups?
- For a path component, is cone homology computable by an iterated mapping cone / chain complex of coarse-link homology groups?
- What new phenomenon occurs on the first cycle?
- Is there an exact necessary-and-sufficient acyclicity criterion?

The two-edge star counterexample must appear as the first nonmatching local model and must be recovered by the formula.

### Class B — Ferrers exclusive inversion graphs

Test whether nested neighborhoods force a tractable core poset or a spectral-sequence collapse.

Search for formulas in terms of:

- maximal bicliques;
- Ferrers diagrams;
- intervals/links in `Q`;
- Möbius functions;
- cellular resolutions or order-complex decompositions.

### Class C — chordal-bipartite exclusive inversion graphs

Determine whether the absence of induced cycles longer than 4 gives a recursive decomposition by bisimplicial edges/vertices.

Test whether this yields:

- an exact homology recursion;
- a discrete Morse matching;
- a collapse theorem;
- or merely an algorithmic decomposition.

### Class D — bounded biclique/core size

If every chain-supported mixed core has size at most `r`, determine whether the interaction spectral sequence is concentrated in a bounded range and whether this forces collapse at a bounded page.

A useful result could be of the form:

`max mixed core size <= r  =>  E^{r}=E^infinity`

but do not assume this is true.

---

## 4. Algebraic target

Try to replace the matching direct sum by a small explicit **interaction chain complex** whose terms are coarse-link homology groups indexed by mixed cores.

A desired form is schematically:

`I_p = direct_sum_{|S|=p+2} H~_{*-shift(S)}(Lambda_S)`

with boundary maps induced by deletion of one missing vertex/core incidence.

Prove whether the spectral sequence collapses so that the homology of this interaction chain complex is the actual cone homology on one of the target structural classes.

A theorem of this type would be stronger than a generic fiber criterion because it would compute the nontrivial cases rather than merely recognize homotopy equivalences.

---

## 5. Exact local models

Completely classify the smallest interacting exclusive graphs:

1. `K_{1,2}` and `K_{2,1}` stars;
2. path of three exclusive edges;
3. `K_{2,2}`;
4. first chordal-bipartite but non-Ferrers example;
5. first even-cycle interaction.

For each, derive a chain-level formula in terms of coarse links/intersections and compare with direct integral SNF.

Identify which local model first supports:

- a nonzero interaction differential;
- torsion produced by interaction rather than inherited from a link;
- a higher differential `d^r`, `r>=2`;
- noncollapse at `E^2`.

---

## 6. Controlled computational discovery

Build on the existing scripts rather than starting over.

At minimum:

- enumerate/deduplicate coarse posets through the next feasible size;
- enumerate availability profiles;
- compute exact integral cone homology via Smith normal form;
- build the exclusive graph and mixed-core poset;
- compute the interaction filtration and spectral-sequence pages algorithmically where feasible;
- group cases by exclusive graph isomorphism type;
- search separately within max-degree-2, Ferrers, and chordal-bipartite classes;
- find minimal counterexamples to every candidate collapse theorem;
- distinguish torsion inherited from coarse links from torsion created by interaction differentials.

Preserve machine-readable CSV/JSON outputs.

---

## 7. Priority/literature gate

Before declaring a theorem novel, search through 2026 for close results on:

- vertex-cover obstruction complexes;
- multi-vertex deletion cofibers;
- Mayer–Vietoris/Čech spectral sequences for vertex deletions;
- homotopy colimits indexed by biclique posets;
- Ferrers/chordal-bipartite independence/order complexes;
- spectral sequences of filtered relative simplicial complexes;
- poset fiber decompositions;
- discrete Morse theory for bipartite/Ferrers structures;
- biclique complexes and Dowker-type constructions.

In particular, compare every proposed theorem with Chachólski–Jin–Scolamiero–Tombari and Björner–Wachs–Welker rather than merely citing them in background.

For each theorem state explicitly:

- standard ingredient;
- closest prior theorem;
- project-specific additional content;
- confidence in priority.

---

## 8. Adversarial review

Run at least these attacks after finding a candidate theorem:

1. **spectral-sequence referee** — attacks indexing, convergence, extensions, and hidden higher differentials;
2. **combinatorial topology referee** — seeks a standard obstruction-complex reformulation;
3. **integer homology referee** — searches for torsion and coefficient dependence;
4. **graph theorist** — tests whether Ferrers/chordal/max-degree hypotheses are really natural and correctly characterized;
5. **hostile counterexample search** — find the smallest case violating the proposed formula.

Do not update the main manuscript until the theorem survives these attacks.

---

## 9. Gate success levels

### Level A — Strong success
A natural interacting class admits a necessary-and-sufficient exact formula/classification, with proof and computational verification.

### Level B — Significant success
A natural class admits an explicit interaction-chain complex plus a proved spectral-sequence collapse / exact recursion that computes the cone.

### Level C — Useful partial success
The spectral sequence is made explicit and useful sufficient conditions/collapse bounds are proved, but no closed classification.

### Level D — Negative but informative
The target classes fail, with minimal counterexamples and a clear obstruction hierarchy.

### Level E — Standard theory only
Nothing materially improves known generic obstruction/fiber machinery.

---

## 10. Required deliverables

Produce:

- `INTERACTION_CORE_RESEARCH_GATE.md`
- `SPECTRAL_SEQUENCE_CONSTRUCTION.md`
- `MAX_DEGREE_TWO_CLASSIFICATION.md`
- `FERRERS_AND_CHORDAL_CASES.md`
- `LOCAL_INTERACTION_MODELS.md`
- `COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md`
- `COMPUTATIONAL_INTERACTION_AUDIT.md`
- `LITERATURE_PRIORITY_MAP.md`
- `ADVERSARIAL_REVIEWS.md`
- reproducible scripts;
- machine-readable result tables;
- `HANDOFF_TO_MASTER.md`.

Only if the gate reaches Level A or B, also produce a manuscript-ready LaTeX section. Do **not** overwrite the v0.3 baseline.

---

## 11. Final questions

End by answering:

1. Does a second exact theorem exist beyond matching?
2. Which structural class gives the strongest result?
3. What is the exact spectral sequence / interaction complex?
4. Does it collapse at `E^2`, and under exactly what hypotheses?
5. How does it recover empty-graph neutrality and the matching theorem?
6. How does it explain the `K_{1,2}` counterexample?
7. Does interaction itself create torsion, independently of torsion already present in coarse links?
8. What is the smallest counterexample outside the theorem's hypotheses?
9. Is the theorem genuinely stronger than standard obstruction-complex or poset-fiber theory?
10. Should it be merged into the current paper, or reserved for a second paper?
11. What single theorem should be attacked next?

The final verdict must be conservative and theorem-level.
