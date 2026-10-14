# Height-Two Repair-Safe Adaptive Identification with a Fixed Observation Library

**Project:** ProLT Adaptive Differentiation - Height-Two Repair Forests, Fixed Observation Libraries, and Optimal Identification

## Primary materials

Use the account-transfer package. In particular read:

- `00_START_HERE/MASTER_HANDOFF_FOR_NEW_ACCOUNT.md`
- `07_U1_U6_HOSTILE_AUDIT/U1_U6_HOSTILE_AUDIT.md`
- `07_U1_U6_HOSTILE_AUDIT/THEOREM_STATUS.csv`
- `07_U1_U6_HOSTILE_AUDIT/ADAPTIVE_THEOREM_FINAL.md`
- `03_PROLT_PRIMARY_SOURCES/ProLT_Controlled_Refinement_Regimes_v0.3.pdf`
- `03_PROLT_PRIMARY_SOURCES/ProLT_Homotopy_Preserving_Observations_v0.4.pdf`
- `03_PROLT_PRIMARY_SOURCES/ProLT_Simultaneous_Observation_Refinement_v0.5.pdf`
- matching TeX sources and the research ledger/claim-audit table.

Treat prior theorem statements as authoritative only after checking them against the latest source and the hostile-audit corrections.

---

## Central research question

Investigate adaptive identification on post-T0 height-two ProLTs when:

1. observations must be selected from a **fixed finite library** `Q`;
2. a query may be asked at a node only if its one-bit refinement is **repair-forest safe on the current branch before conditioning**;
3. the goal is to identify the surviving valuation/state exactly;
4. legality of unused observations may change after conditioning.

The goal is to determine whether this interaction produces genuinely new mathematics beyond ordinary restricted decision trees.

---

## 1. Role

Act as an independent hostile research panel with expertise in finite posets/topology, simple homotopy, discrete Morse theory, relative homology, rooted forests, graphic/cellular matroids, Boolean functions, adaptive decision trees, Twenty Questions, test cover, active learning, group testing, parameterized complexity, and theorem-level novelty auditing.

Do not assume the proposed direction is new or even nontrivial.

---

## 2. Reconstruct the exact height-two source theorem

For post-T0 `P` with `ht(P) <= 2` and one Boolean observation `b:P->{0,1}`, reconstruct the exact source theorem from ProLT v0.4.

Verify the claimed equivalence of:

- homotopy equivalence of the refined inclusion;
- simple-homotopy equivalence;
- collapse by deleted edge--triangle pairs;
- F2 homology equivalence;
- invertibility of the relative boundary matrix;
- rooted repair graph is a forest with exactly one formal root in each component.

Do not proceed until hypotheses, conventions, deleted-cell definitions, and root conventions are explicit.

---

## 3. Reconstruct the repair graph exactly

For a one-bit labeling `b`, define a descent edge `p<q` with `b(p)=1`, `b(q)=0`.

Classify deleted three-chain bit words. Recover the authoritative construction in which:

- each deleted edge is a graph vertex;
- each coarse connected component contributes a formal root;
- one-deleted-edge triangles produce root edges;
- two-deleted-edge triangles produce dependency edges.

Independently verify that the relative boundary matrix is the reduced incidence matrix of this graph over F2.

---

## 4. Formal adaptive model

Let the initial state be a finite post-T0, height-<=2 signature poset `P0` on support `S0`.

Let

`Q = {q1,...,qm}`

be a fixed finite library of Boolean observations, specified before the protocol begins. No arbitrary new Boolean query may be synthesized later.

At history `h`, maintain:

`(S_h, Phi_h, Q_h)`

where `S_h` is the current support, `Phi_h` accumulated observations, and `Q_h` the unused/still-useful library tests.

Define the current branch poset `P_h=P_{Phi_h,S_h}`.

Prove whether every branch remains T0 once the initial state is T0.

---

## 5. Query legality

A library query `q in Q_h` is repair-safe at history `h` iff its one-bit refinement of `P_h` satisfies the exact repair-forest theorem **before conditioning on the outcome**.

Check legality independently via:

1. repair graph; and
2. relative boundary matrix.

Any disagreement must be treated as a bug or theorem failure.

---

## 6. Outcome update and branch cancellation

For legal `q`, define outcome branches:

`S_{h,b} = {x in S_h : q(x)=b}`.

The observation is added before conditioning:

`Phi_{h,b}=Phi_h union {q}`.

Investigate the candidate **branch-cancellation lemma**:

> After conditioning on `q=b`, the new coordinate is constant on the branch and contributes no further internal order thinning, so the next branch poset is canonically the induced old subposet on the surviving support.

Formally test whether:

`P_{Phi_h union {q}, S_{h,b}} ~= P_{Phi_h,S_h}|_{S_{h,b}}`.

Prove or refute. Search for prior equivalents.

This lemma is a priority because it determines the correct dynamic-programming state.

---

## 7. State-dependent query admissibility

For an unused query `r`, compare repair-safety on `P_h` with repair-safety on an induced branch `P_h|_T`.

Determine whether repair-safety is hereditary under support restriction.

Define and search for:

### Activation

`r` unsafe on `P` but safe on `P|_T`.

### Deactivation

`r` safe on `P` but unsafe on `P|_T`.

Find the smallest examples or prove impossibility in a natural class.

If transitions occur, explain them in repair-graph terms:

- cycle deletion/creation;
- loss/gain of anchors;
- component/root changes;
- disappearance of dependency or anchor triangles.

---

## 8. Repair-graph dynamics under conditioning

Derive the exact transformation from `R_r(P)` to `R_r(P|_T)`.

Do not assume it is an induced subgraph because:

- deleted edges may disappear;
- deleted triangles may disappear;
- coarse connected components may change;
- formal roots may change.

Seek an exact **repair-graph restriction theorem** and classify all four safety transitions:

- safe -> safe;
- safe -> unsafe;
- unsafe -> safe;
- unsafe -> unsafe.

This is one of the strongest theorem targets.

---

## 9. Define repair-safe adaptive identification depth

Define `d_RF(P,Q)` as the minimum worst-case number of additional observations needed to identify every state, subject to:

- fixed library;
- every selected query repair-safe on the current branch before conditioning.

Set `d_RF=infinity` if no legal identifying protocol exists.

Compare with ordinary fixed-library adaptive depth `d_ad(P,Q)`.

Define repair-safety penalty:

`Delta_RF = d_RF - d_ad`

when both are finite.

---

## 10. Exact dynamic program

After resolving branch cancellation, derive and prove the correct recursion. Candidate:

`D(P,Q)=1 + min_{q in L(P,Q)} max(D(P|q=0,Q\{q}), D(P|q=1,Q\{q}))`

where `L(P,Q)` is the set of nonconstant currently repair-safe library queries.

Base cases:

- `D=0` for one or zero candidates;
- `D=infinity` if multiple candidates remain and no legal separating test exists.

If more state than `(P,Q)` must be retained, identify it exactly.

---

## 11. Feasibility and depth decision problems

Define:

- `RF-SAFE(P,q)` - is one query repair-safe?
- `RF-IDENT(P,Q)` - does any repair-safe adaptive identification tree exist?
- `RF-DEPTH(P,Q,k)` - is `d_RF(P,Q) <= k`?
- optionally weighted `RF-COST`.

First derive exact recursive feasibility conditions. Only then investigate complexity.

---

## 12. Fixed-library gaps

Search for:

1. ordinary identification possible but repair-safe identification impossible:
   `d_ad < infinity`, `d_RF = infinity`;
2. finite strict depth gap:
   `d_RF > d_ad`;
3. an infinite family with growing/unbounded gap, if it exists.

Find smallest examples first.

A rigorous impossibility/gap theorem would be a strong result.

---

## 13. Adaptive advantage from query activation

Search for libraries in which an initially illegal query becomes legal only after another legal query is answered.

Determine whether adaptive protocols can exploit this latent activation in a way no natural nonadaptive repair-safe protocol can.

Be careful to distinguish:

- individual one-bit safety;
- sequential-prefix safety;
- simultaneous block safety.

Use ProLT v0.5 for simultaneous-refinement interactions.

---

## 14. Structured library regimes

Primary model: arbitrary supplied finite test library.

Then test structured libraries:

- coordinate/literal tests;
- bounded formula-size tests;
- monotone;
- Horn;
- dual-Horn;
- affine/XOR;
- CM/LM-supported observables only if the allowed class is defined rigorously.

Do not let these variants replace the fixed-library core problem.

---

## 15. Structured height-two poset families

Search for an exact theorem on one natural family after reconnaissance:

- crowns;
- fences;
- complete three-level incidence posets;
- rooted-tree Hasse diagrams;
- series-parallel posets;
- bounded-treewidth Hasse diagrams;
- naturally occurring Boolean-signature subposets.

For the best family seek exact feasibility, depth, or polynomial/FPT algorithm.

---

## 16. Boundary-matrix updates

For each candidate query at a node build the relative boundary matrix.

Investigate whether conditioning allows exact incremental updates by row/column deletion, low-rank update, component decomposition, or another operation rather than full recomputation.

If so, derive an algorithm and complexity bound.

---

## 17. Matroid interpretation

Because the height-two boundary is a reduced incidence matrix, test whether legal repair graphs correspond to bases of a rooted graphic matroid.

Then determine whether conditioning acts by:

- deletion;
- contraction;
- root change;
- a matroid minor;
- or no clean standard operation.

If the adaptive theory reduces to known matroid dynamics, say so.

---

## 18. Information lower bounds

Compare ordinary binary lower bound `ceil(log2 |S|)` with stronger bounds arising from the current legal split family.

Define a best legal balance parameter if useful and derive adversary/Kraft/entropy bounds.

---

## 19. Exhaustive finite computation

Enumerate post-T0 height-<=2 posets as far as feasible, preferably through at least 6 vertices.

For every poset:

1. enumerate Boolean labelings;
2. construct deleted edges;
3. construct deleted triangles;
4. construct repair graph;
5. classify repair safety;
6. independently compute the relative boundary matrix;
7. verify equivalence.

Then study fixed libraries using exhaustive enumeration where feasible and restricted/random/canonical libraries beyond that.

For each manageable `(P,Q)` compute:

- ordinary adaptive feasibility/depth;
- repair-safe feasibility/depth;
- penalty;
- legal root queries;
- query activation/deactivation counts;
- optimal protocol;
- smallest examples of each phenomenon.

---

## 20. Independent verification

Use two independent implementations for central claims:

- A: repair graph;
- B: boundary matrix, without calling repair-graph routines.

For small adaptive problems independently verify dynamic programming with brute-force tree search or a separately formulated solver.

Preserve counterexamples and failed conjectures.

---

## 21. Literature/priority audit through 2026

Search theorem-level prior art in:

- restricted Twenty Questions;
- optimal binary decision trees;
- adaptive test cover/separating systems;
- active learning with query constraints;
- group testing with constrained pools;
- decision trees on posets;
- graph-constrained queries;
- state-dependent action sets;
- matroid-constrained adaptive selection;
- contingent planning;
- finite-space topology;
- discrete Morse theory;
- rooted forests;
- graphic/cellular matroids.

Search specifically for models where conditioning changes which future tests are admissible.

For every apparent new theorem classify it conservatively.

---

## 22. Hostile reduction test

Repeatedly ask:

> Once repair-safety is computed at each support, is the problem merely an ordinary restricted decision tree with a state-dependent legal action set?

If yes, the contribution must be a structural theorem about the legal-action geometry, such as:

- exact activation/deactivation characterization;
- repair-graph restriction theorem;
- exact height-two family;
- unbounded repair-safety gap;
- matroid/minor interpretation;
- efficient algorithm exploiting repair dynamics.

Notation alone is not a contribution.

---

## 23. Priority theorem program

Attempt, but do not force:

- H1 Branch-cancellation theorem.
- H2 Repair-graph restriction theorem.
- H3 Safety activation/deactivation theorem.
- H4 Exact adaptive feasibility theorem.
- H5 Fixed-library gap theorem.
- H6 Structured-family theorem.
- H7 Complexity theorem.
- H8 Main adaptive theorem: strongest surviving result.

A principal theorem must be correct, nontrivial, ProLT-specific, and priority-surviving.

---

## 24. Required deliverables

Produce:

- `HEIGHT2_ADAPTIVE_MASTER_AUDIT.md`
- `FORMAL_ADAPTIVE_MODEL.md`
- `BRANCH_CANCELLATION.md`
- `REPAIR_GRAPH_DYNAMICS.md`
- `QUERY_ACTIVATION_DEACTIVATION.md`
- `FIXED_LIBRARY_IDENTIFICATION.md`
- `ADAPTIVE_DEPTH_THEORY.md`
- `COMPLEXITY_AUDIT.md`
- `MATROID_INTERPRETATION.md`
- `STRUCTURED_LIBRARY_RESULTS.md`
- `LITERATURE_PRIORITY_AUDIT.md`
- `HOSTILE_REFEREE_REPORTS.md`
- `MAIN_THEOREM.md`
- `COUNTEREXAMPLES.md`
- `OPEN_PROBLEMS.md`
- `HANDOFF_TO_MASTER.md`

Computational artifacts:

- `HEIGHT2_POSETS.csv`
- `QUERY_REPAIR_SAFETY.csv`
- `SAFETY_TRANSITIONS.csv`
- `FIXED_LIBRARY_RESULTS.csv`
- `ADAPTIVE_DEPTHS.csv`
- `REPAIR_SAFETY_GAPS.csv`
- `OPTIMAL_PROTOCOLS.json`
- scripts, independent scripts, logs, hashes, reproducibility README.

---

## 25. Final questions

Answer explicitly:

1. Does branch cancellation hold?
2. Is repair-safety hereditary under conditioning?
3. Can unsafe queries become safe later?
4. Can safe queries become unsafe later?
5. What are the smallest activation/deactivation examples?
6. Can ordinary fixed-library identification succeed while repair-safe identification fails?
7. Can repair safety create a strict depth penalty?
8. Can the penalty grow without bound?
9. Can adaptivity exploit initially unavailable queries?
10. Is there a genuine adaptive advantage over natural nonadaptive repair-safe protocols?
11. Is there a clean graph/matroid explanation?
12. What is the strongest exact result on a natural height-two family?
13. Is RF-IDENT substantially different from standard restricted decision-tree feasibility?
14. Which result is the best publication candidate?
15. What is its novelty confidence?
16. What is the single highest-value next step?

---

## Research discipline

Use:

`exact ProLT theorem -> adaptive formalization -> counterexample search -> finite computation -> structural theorem -> priority audit`.

Do not interpret computational patterns as theorems.

Do not call a query safe because the *conditioned branches* look simple: safety is evaluated on the refinement **before conditioning**.

Do not replace the fixed library with arbitrary Boolean queries.

If the whole problem reduces to standard restricted decision-tree theory plus a polynomial-time legal-test predicate, report that as the main negative result rather than manufacturing novelty.
