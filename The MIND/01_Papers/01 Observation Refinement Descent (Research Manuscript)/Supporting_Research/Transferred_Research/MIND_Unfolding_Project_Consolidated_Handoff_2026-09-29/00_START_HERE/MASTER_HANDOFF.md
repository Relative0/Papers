# MASTER HANDOFF — Unfolding / Observation-Refinement / Carrier-Splitting Program

**Date:** 29 September 2026  
**Status:** Active research program. Latest gate reached **Level A mathematically** on a restricted natural class. Publication-level novelty remains subject to conservative theorem-level priority review.

---

## A. Research arc to date

### Phase 0 — historical recovery from the thesis

The 2015 thesis proposed:

- Mental Space as a topological representation of the mind;
- concepts as simplicial complexes;
- a logical "distinguishing/unfolding" operator `partial` intended to decompose concepts;
- gluing/integration back to larger concepts;
- cycles/boundaries as possible symmetry/asymmetry indicators;
- ProLT/presheaf/exact-sequence/homology analogies.

The audit found a real mathematical seed but also important defects:

- the thesis unfolding operator is not the genuine simplicial boundary;
- it is presentation-sensitive as a Boolean operator;
- its repeated application is better understood through Boolean/Hamming layers;
- the printed gluing identity is not generally correct;
- cycles do not characterize symmetry;
- the thesis's topology/homology analogies require principled reconstruction.

See `05_ORIGINAL_UNFOLDING_AUDIT/`.

### Phase 1 — two-operator modern model

The project separated:

- `d`, the genuine chain differential with `d^2=0`;
- `U_k`, an unfolding/refinement map between complexes/stages.

If `U_k` is induced by a simplicial map, `d U_k = U_k d`, so refinement induces homology maps. Mapping cones and relative homology became the natural measures of structural change.

The old simplex notes also led to an exact Hamming-layer viewpoint and a cumulative skeleton filtration. See `04_OBSERVATION_REFINEMENT_DRAFT/`.

### Phase 2 — observation-refinement descent and cone theorem

For compatible observational covers/refinements, the project formulated mapping-cone defects and descent/reconstruction defects. The key conceptual split became:

- **structural change:** `H_*(Cone U)`;
- **reconstruction failure:** kernel/cokernel of the restriction-to-compatible-local-data map.

This phase also replaced "cycles = symmetry" with a distinct observational symmetry group, whose invisible transformations can only shrink under finer observations.

### Phase 3 — carrier splitting

The major issue was what happens when a new observation splits one old `T0` observational state into multiple refined states.

Let `Q` be the old finite observational poset and `Q^psi subset Q x {0,1}` the refined carrier. The carrier-splitting gate proved:

1. Introduce a split completion `Qhat^psi` that duplicates/splits the carrier but retains all old coarse comparisons.
2. `Qhat^psi -> Q` is homotopy-neutral (beat-point reduction).
3. The actual refined order `Q^psi` is obtained from `Qhat^psi` by one-bit monotonicity thinning.
4. Therefore carrier splitting is **neutral blow-up + order defect**.
5. The cone homology is the relative homology `H_*(Delta Qhat^psi, Delta Q^psi)`.
6. Relative chains are exactly split-completion chains whose bit-word contains a descent `1...0`.

For weighted height `<=2`, the gate obtained a complete integral rooted-incidence classification and a total-unimodularity result. Above that height, unrestricted torsion/universality forbids a universal rooted-forest criterion.

See `03_CARRIER_SPLITTING_GATE/`.

### Phase 4 — higher-dimensional inversion complex

The latest gate changed to a full-doubling model:

`D = Q x {0<1}`,

with the actual refined carrier obtained by deleting missing copies:

- `(p,0)` for 1-only states `p`;
- `(z,1)` for 0-only states `z`.

This converts carrier splitting into a highly structured two-colour vertex-deletion problem in `Delta(Q x 2)`.

Define the **exclusive inversion graph**

`G_psi = (P sqcup Z, E_psi)`,

`E_psi = {(p,z): p in P, z in Z, p < z}`.

Every mixed relative simplex has a missing-core whose endpoints form a chain-supported biclique of this graph.

---

## B. Strongest current theorem

### Exclusive-Inversion Matching Theorem

If `E_psi` is a matching, then for every integer `n` and every coefficient ring `R`,

`H_n(Cone(Delta pi);R)`

is naturally isomorphic to

`direct_sum_{(p,z) in E_psi} H~_{n-2}(lk_{Delta Q}[p,z];R)`.

Consequences:

- exact all-dimensional classification on this class;
- integral torsion is retained and computed from the edge links;
- homology equivalence occurs iff every relevant coarse edge link is acyclic (with chosen coefficients);
- for a bounded coarse poset, only the global endpoint inversion can contribute;
- endpoint profiles on finite distributive lattices are neutral except for Boolean lattices, where the cone has a single top-dimensional `Z` class;
- arbitrary finite-poset reduced homology can be shifted by two degrees into a one-edge matching carrier-split system.

Formal proofs are in `02_LATEST_HIGHER_DIMENSIONAL_GATE/EXACT_THEOREMS_AND_PROOFS.md`.

---

## C. Why the theorem works

Two separate colour deletions are individually homotopy-neutral. Their mixed interaction is where the defect lives. Under the matching hypothesis, every relative simplex contains exactly one missing lower/upper pair, so the relative chain complex splits directly over exclusive inversion edges.

Each fixed-edge summand is the augmented chain complex of the product-edge link, shifted. The product-edge link is homotopy equivalent to a suspension of the corresponding coarse edge link. This yields the formula above.

This is stronger/more explicit than merely applying a generic fiber-contractibility criterion, but it is structurally close to classical vertex-deletion/cofiber and obstruction-complex theory. Priority claims must reflect that.

---

## D. Sharp failures / boundaries

### D1. Forest is not enough

The coarse chain `0<1<2` with availability `(1-only, 0-only, 0-only)` has exclusive inversion graph `K_{1,2}`, a forest. Yet the actual cone has `H~_1 ~= Z`, while summing individual edge-link contributions gives zero.

Thus the first shared endpoint creates a genuine 3-vertex interaction core.

### D2. Matching does not imply torsion-free or TU

Let `Q = 0hat + R + 1hat`, take only the endpoint inversion, and split every state of `R`. The exclusive graph is one edge but

`H_n(Cone;Z) ~= H~_{n-2}(Delta R;Z)`.

Arbitrary torsion can therefore occur inside the matching class.

### D3. Horn is mainly neutral in the strongest relational form

A nonempty meet-closed full refined relation has a minimum; its projection is also meet-closed with a minimum. Both order complexes are contractible. Dual-Horn is dual.

### D4. Universal all-height graph criteria are impossible

The companion one-bit thinning theory already permits torsion and very general homotopy behavior. Carrier splitting contains that regime. Any further theorem must impose real structural restrictions.

---

## E. Interaction-core filtration: current open frontier

For a relative simplex `sigma`, let `S(sigma)` be the set of missing vertices it contains. Filtering the relative complex by `|S(sigma)|` gives an associated graded complex indexed by mixed missing cores. These cores correspond to chain-supported bicliques of the exclusive inversion graph.

- no exclusive edges -> isotone-section neutrality;
- matching -> only 2-vertex mixed cores -> exact direct-sum edge-link theorem;
- a star -> 3-vertex cores appear -> first nontrivial interactions/differentials;
- larger bicliques -> higher interaction levels.

This hierarchy is the key to the next theorem.

---

## F. Computational evidence already obtained

Latest higher-dimensional gate:

- 3,242 matching cases through 4 coarse states checked integrally by Smith normal form: 0 formula failures;
- 1,707 product-edge link-suspension checks through 5 states: 0 failures;
- 639 additional nonempty-matching 5-state cases checked over `F_2`: 0 failures;
- Horn/dual-Horn closure families exhaustively checked through 4 refined coordinates;
- small finite distributive-lattice endpoint cases checked integrally.

Earlier carrier-splitting gate:

- 3,450 poset/profile cases through 4 coarse states;
- 2,172 weighted-height `<=2` cases all agreed with the rooted-incidence theorem;
- mapping-cone and relative split-completion computations agreed in every tested case.

All scripts/results are included.

---

## G. Literature and novelty boundary

Established ingredients that must be credited:

- Stong: finite `T0` spaces / beat points;
- Quillen/Barmak: poset-fiber criteria and simple-homotopy refinements;
- Björner–Wachs–Welker: poset-fiber homotopy decompositions;
- Fernández–Minian: relation/mapping-cylinder constructions in finite posets;
- Chachólski–Jin–Scolamiero–Tombari: vertex-cover obstruction complexes and homotopical decompositions;
- Dey–Hirani–Krishnamoorthy: total unimodularity vs torsion in relative simplicial pairs;
- classical crosscut/distributive-lattice topology;
- classical Horn/intersection-closure theory.

Current defensible candidate contribution:

> A Boolean observation split becomes a special two-colour missing-copy problem in `Delta(Q x 2)`. The 1-only-to-0-only comparison graph organizes the interactions. When that graph is a matching, the relative chain complex separates and yields an exact all-dimensional integral coarse-edge-link formula.

Do **not** claim a new general theory of vertex deletion, cofibers, nerves, or poset fibers.

---

## H. Manuscript status and merge policy

Current baseline manuscript:

`01_CURRENT_MANUSCRIPT/Observation_Refinement_Descent_and_Cone_Draft_v0.3.tex`

Latest theorem insertion prepared but not merged:

`01_CURRENT_MANUSCRIPT/MANUSCRIPT_REVISION_SECTION.tex`

Recommended policy:

1. keep v0.3 frozen as baseline;
2. run the next interaction-core research gate;
3. if the next gate yields Level A/B, decide whether matching + interacting theorem form one coherent paper;
4. then merge and run a hostile proof/priority/editorial pass;
5. only after that produce a submission candidate.

---

## I. Next research theorem

The next target is not another generic carrier-splitting theorem. It is:

### Interaction-Core Spectral Sequence Classification Beyond Matching

Start with exclusive inversion graphs having controlled overlap, especially:

- maximum degree `<=2` (paths/cycles);
- Ferrers bipartite graphs;
- chordal-bipartite graphs;
- bounded biclique/core size.

Determine whether the core-size filtration spectral sequence collapses at `E^2` and give exact formulas for the differentials/homology from coarse links plus overlap data.

A successful theorem should recover:

- empty graph neutrality;
- matching edge-link direct sums;
- the two-edge star counterexample as the first nontrivial interaction term.

The full research prompt is `00_START_HERE/NEXT_RESEARCH_PROMPT.md`.

---

## J. What the next agent should NOT do first

Do not immediately rewrite the paper. Do not restart the thesis audit. Do not rerun only the same small computations. Do not broaden into generic cognition/topology literature before understanding the exact current theorem hierarchy.

First verify the baseline theorem statements, then attack the next interaction-core gate.
