# Paper U — Targeted Research Closure and Theorem-Strengthening Gate

**Project:** Hierarchical Concepts Under Finite Resolution: Ultrametric Geometry, Observational Equivalence, and Symmetry\
**Working manuscript:** Paper U draft v0.1\
**Date:** 29 September 2026

## Role

Act as an **independent research team and pre-referee closure panel** with expertise in:

- ultrametric and non-Archimedean analysis;
- p-adic integers and profinite/inverse-limit structures;
- general topology, quotient/partition topologies, pseudometrics, and Kolmogorov quotients;
- rooted trees, tree boundaries, automorphism groups, and branch-group methods;
- symbolic dynamics, cylinder sets, generating partitions, and filtrations;
- information theory, coarse-graining, finite-resolution observation, and statistical experiments;
- mathematical psychology and formal models of cognition;
- Matte-Blanco, Khrennikov, and the history of ultrametric/p-adic mental-space models.

You are **not** being asked to protect the manuscript. Treat every theorem, interpretation, novelty suggestion, and literature claim as provisional. If the paper is mostly a repackaging of standard facts, say so clearly. If a stronger theorem is available, derive it. If a section weakens the paper, recommend cutting or moving it.

## Materials

Use all supplied materials, especially:

1. `PAPER_U_RESOLUTION_LIMITED_ULTRAMETRIC_CONCEPTS_DRAFT_v0.1.zip` — current Paper U manuscript and bibliography;
2. `PADIC_ULTRAMETRIC_UNCONSCIOUS_AUDIT_2026.zip` — prior mathematical/literature audit and finite example;
3. the 2015 thesis `Thesis v_12.pdf` — historical source only, not an authority.

If other related project files are supplied, use them only where directly relevant. Do **not** import Paper F / ProLT / CM machinery merely to make Paper U look broader.

---

# Central question

Determine whether Paper U can become a **defensible research paper** rather than only an expository correction/synthesis.

The current core is:

\\[ \boxed{ \text{ultrametric hierarchy} + \text{finite-resolution observation} + \text{observational equivalence} + \text{symmetry} } \\]

with a latent Hausdorff ultrametric space \\((X,d)\\), observation maps

\\[ \pi_k:X\to X_k, \\]

finite-resolution equivalence

\\[ x\sim_k y \iff \pi_k(x)=\pi_k(y), \\]

partition topologies \\(\tau_k\\), ultrapseudometrics \\(d^{(k)}\\), and the prime-base specialization

\\[ \mathbb Z_p \cong \varprojlim_k \mathbb Z/p^k\mathbb Z. \\]

The proposed cognitive interpretation is deliberately limited: members of a class may be **observationally equivalent without being literally identical**.

The goal of this research phase is to determine exactly what in this package is standard, what is a useful synthesis, and whether there is a theorem-level contribution worth foregrounding.

---

# Phase A — Reconstruct and attack every mathematical claim

Build a theorem/definition ledger for the entire manuscript. For each numbered or substantive claim give:

`Claim | Status | Proof reconstructed? | Standard source? | Needed correction | Publication role`

At minimum check rigorously:

1. the prefix ultrametric;
2. cylinder/ball identification and radius conventions;
3. clopen and laminar ball structure;
4. the fixed-depth Boolean algebra of observable concepts;
5. the finite-resolution equivalence relations;
6. the observation topology \\(\tau_k\\);
7. internal indiscreteness of fibers;
8. recovery of the full ultrametric topology from all finite resolutions;
9. the truncated ultrapseudometric \\(d^{(k)}\\);
10. the relation between its topology and \\(\tau_k\\);
11. the metric identification / quotient by zero pseudodistance;
12. the six-part “resolution-equivalence” theorem;
13. the group action used in the orbit clause;
14. the distance–distinguishing-depth relation;
15. inverse-limit reconstruction;
16. the isometry with \\(\mathbb Z_p\\);
17. the interpretation of \\(\pi_k\\) as reduction modulo \\(p^k\\);
18. the symmetry-chain claim \\(G\_{k+1}\subsetneq G_k\\);
19. the XOR orbit quotient and anchored-XOR reconstruction;
20. entropy and conditional-information formulas;
21. conditional expectation / martingale statements and hypotheses;
22. adaptive frontiers and local refinement.

Be especially alert for statements that are correct only for a **regular full rooted tree** but are written as though they were general ultrametric facts.

Do not accept the group-orbit clause merely from intuition. Check the precise definition of \\(G_k\\), whether it acts transitively on every boundary fiber, and what changes for nonregular trees.

---

# Phase B — Theorem-level priority and literature audit through 2026

This is the most important research task.

Search primary or authoritative sources and identify theorem-level overlap, not merely keyword similarity.

## B1. General topology / observational equivalence

Search for:

- partition topologies;
- topological indistinguishability;
- Kolmogorov \\(T_0\\) quotients;
- “almost discrete” / partition spaces;
- initial topologies induced by a finite-valued observation map;
- observational equivalence under finite precision;
- coarse-graining by partitions;
- factor maps and finite observation functions.

Determine whether the manuscript's \\(\tau_k\\) construction is a standard partition topology in established terminology, and cite the correct theory.

## B2. Pseudometric / ultrapseudometric identification

Search for:

- pseudometric zero-distance equivalence;
- metric identification / Hausdorff reflection;
- quotient metrics and pseudometrics;
- ultrapseudometrics and quotients;
- universal properties of the zero-distance quotient.

Determine whether \\(d^{(k)}\\) is merely a standard pullback/truncation construction or whether any stronger universal characterization can be proved.

## B3. Rooted trees and ultrametric representation

Search modern representation results for:

- finite ultrametric spaces and representing trees;
- totally bounded / compact ultrametric spaces and locally finite rooted trees;
- ball posets and dendrograms;
- boundaries/end spaces of rooted trees;
- nested partitions and ultrametrics.

Include recent work through 2026, especially 2023–2026 representation results.

Ask whether the regular prefix model should be replaced or supplemented by a coordinate-free theorem for arbitrary compact/totally bounded ultrametric spaces.

## B4. Symbolic dynamics and profinite structure

Compare Paper U with standard material on:

- one-sided full shifts \\(\Sigma_m^{\mathbb N}\\);
- cylinder sigma-algebras;
- finite-coordinate filtrations;
- generating partitions;
- inverse limits of finite discrete systems;
- profinite spaces and \\(\mathbb Z_p\\).

A referee may regard much of the current core as textbook symbolic dynamics/profinite topology. Quantify that risk precisely.

## B5. Rooted-tree automorphism groups

Search the literature on:

- level stabilizers and rigid stabilizers;
- automorphism groups of regular rooted trees;
- wreath-recursion descriptions;
- orbit structure on tree boundaries;
- quotients of successive level stabilizers.

Test and, if useful, prove the stronger regular-tree statements

\\[ G_k \cong \operatorname{Aut}(T_m)^{m^k} \\]

and

\\[ G_k/G\_{k+1}\cong \operatorname{Sym}(m)^{m^k}, \\]

with whatever qualifications are necessary.

Determine whether this provides a sharper quantitative meaning of “symmetry reduction by resolution.” Do not present it as novel if it is standard group theory.

## B6. Hierarchical information theory

Search for:

- information theory on hierarchical partitions;
- hierarchical entropy and hierarchical mutual information;
- filtration-based information gain;
- adaptive partition refinement;
- decision trees, prefix codes, and complete antichains/frontiers;
- active sensing / optimal refinement where relevant.

In particular, compare the manuscript's entropy/filtering section with established work on hierarchical partition information. Decide whether it should be strengthened, cited and retained, or shortened as standard background.

## B7. Finite-resolution observation in other fields

Search for mathematically close formulations of:

\\[ \text{latent state}\to\text{finite-valued observation}\to\text{equivalence classes}. \\]

Include coarse-graining in dynamical systems, observational equivalence, finite-precision measurement, statistical experiments, and any 2025–2026 work explicitly organized around “resolution geometry” or observation quotients.

The question is not whether those papers discuss cognition. The question is whether they already contain the same mathematical architecture.

## B8. Ultrametric cognition and Matte-Blanco

Deeply audit:

- Khrennikov's 1997/1998 p-adic subconscious work;
- neural/pathway and probability extensions;
- 2007 m-adic mental-space paper;
- 2010 categories-as-balls paper;
- later ultrametric cognition papers;
- Lauro-Grotto on Matte-Blanco and ultrametric sets;
- Murtagh's ultrametric model of mind / bi-logic papers;
- any later work through 2026.

Create an exact chronology of:

- states as branches/points;
- associations/categories as balls;
- ideas as collections of balls;
- conscious/unconscious flows;
- hierarchy and symmetry;
- finite resolution or coarse observational equivalence, if present;
- topology or quotient structures, if present.

Do not attribute originality to Paper U for any ingredient already explicit in this literature.

---

# Phase C — Audit the Matte-Blanco interpretation from primary sources

Paper U should model only what the source material actually supports.

Using Matte-Blanco's primary text where available, distinguish among:

1. class membership/generalization;
2. the principle of symmetry;
3. equivalence versus literal identity;
4. part/whole symmetrization;
5. absence or alteration of negation;
6. infinite-set language;
7. conscious “unfolding” or asymmetrization.

Determine which of these are genuinely represented by \\(x\sim_k y\\), which are only analogies, and which require additional relational/logical structure.

The manuscript must not imply that observational equivalence is a complete formalization of Matte-Blanco's bi-logic.

Produce exact page/source references for every psychological claim retained in the revised manuscript.

---

# Phase D — Search for a stronger mathematical center

The current draft is mathematically coherent but may be too close to standard constructions. Actively test the following routes to a stronger paper.

## D1. Coordinate-free generalization

Try to formulate the theory for a compact or totally bounded ultrametric space \\((X,d)\\) with a discrete sequence of resolution thresholds or a nested family of finite clopen ball partitions.

Determine the strongest correct theorem connecting:

- radius-threshold equivalence;
- finite ball partitions;
- partition topology;
- ultrapseudometric collapse;
- quotient ultrametric;
- minimum distinguishing resolution.

State precisely what extra hypotheses are required.

## D2. Universal-property formulation

Investigate whether the observation quotient has a useful universal property, for example as:

- the Kolmogorov quotient of \\((X,\tau_k)\\);
- the metric identification of \\((X,d^{(k)})\\);
- the universal target for all level-\\(k\\) observables;
- an initial/final object in an appropriate category of finite-resolution observations.

If several of these are standard manifestations of the same quotient, unify them cleanly into one theorem rather than listing parallel facts.

## D3. Quantitative symmetry loss

For the regular \\(m\\)-ary tree, determine whether successive resolution admits an exact group-theoretic decomposition such as

\\[ G_k/G\_{k+1}\cong \operatorname{Sym}(m)^{m^k}. \\]

If so, interpret carefully what is being counted and whether a local adaptive refinement has an analogous quotient.

Explore—but do not force—a relation between symmetry reduction and information gain. Any formula linking group index, entropy, or distinguishing capacity must be proved and not sold by analogy.

## D4. Adaptive frontiers as a mathematical object

Study finite prefix-free complete frontiers as partitions of the boundary.

Determine whether the refinement order forms a known lattice/poset, how it relates to prefix codes and Kraft-type constraints, and whether there is a useful theorem about local resolution, minimal separating frontiers, or observation cost.

If this becomes a genuinely nontrivial result, consider making adaptive resolution rather than the uniform \\(k\\)-model the paper's strongest new component.

## D5. Noisy resolution

Do only a bounded study. Determine whether a clean extension from exact fibers to stochastic observation channels adds real value to Paper U or should be deferred.

Do not expand into a second paper unless a concise theorem emerges.

---

# Phase E — Adversarial attempts to kill the paper

Run at least four explicit attacks before revising.

### Attack 1 — “This is all textbook mathematics”

Try to show that every theorem is an immediate combination of standard facts about cylinder sets, partition topologies, pseudometric identifications, and inverse limits.

If this attack succeeds, recommend an expository/correction note or find a stronger theorem.

### Attack 2 — “The cognitive interpretation is post hoc”

Argue that any finite partition of any state space yields observational equivalence, so the ultrametric adds little.

The paper must answer exactly what ultrametricity contributes beyond arbitrary coarse-graining.

### Attack 3 — “The p-adics are decorative”

Try to remove every p-adic statement and see whether the core paper changes materially.

Retain the p-adic specialization only if its canonical residue/inverse-limit structure makes a substantive difference.

### Attack 4 — “The paper is overstuffed”

Attack the XOR, martingale, adaptive-resolution, cognitive, and Paper-F bridge sections as scope creep.

Identify the minimal coherent paper and which material belongs in appendices or future work.

Also run a **hostile priority referee** whose job is to find the nearest prior theorem or conceptual architecture to every claimed contribution.

---

# Phase F — Revise the manuscript

After the research and attacks, produce a new manuscript **only from claims that survive**.

Create:

`Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.tex`

and, if the environment supports it, a compiled PDF.

Revision requirements:

- remove all working-draft/process language;
- repair any mathematical errors;
- cite standard results rather than presenting them as contributions;
- state the strongest theorem early;
- clearly separate **new theorem**, **new synthesis**, **standard background**, and **psychological interpretation**;
- use exact established terminology such as partition topology / Kolmogorov quotient where appropriate;
- add theorem-level citations for rooted-tree and ultrametric representation results;
- sharply limit novelty language unless priority survives the audit;
- make the role of ultrametricity explicit and nonredundant;
- either justify XOR as a useful minimal example or move/remove it;
- either strengthen the information/adaptive sections or shorten them;
- retain the Paper U / Paper F boundary but keep Paper F subordinate;
- include a limitations subsection that explicitly says what the model does **not** establish empirically.

If the strongest defensible form is a short mathematical note rather than a full paper, revise toward that form rather than padding it.

---

# Required deliverables

Produce a complete research package containing at least:

1. `PAPER_U_RESEARCH_CLOSURE_REPORT.md`
2. `PAPER_U_THEOREM_LEDGER.md`
3. `PAPER_U_PRIORITY_AND_LITERATURE_MAP.md`
4. `PAPER_U_MATTE_BLANCO_SOURCE_AUDIT.md`
5. `PAPER_U_GENERALIZATION_AND_STRENGTHENING_STUDY.md`
6. `PAPER_U_ADVERSARIAL_ATTACKS.md`
7. `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2.tex`
8. revised `.bib` file;
9. any reproducible scripts used for finite examples, group computations, or exhaustive checks;
10. a `HANDOFF_TO_REVIEW_GATE.md` stating exactly what survived and what remains unresolved.

Bundle the outputs into one ZIP.

---

# Final research-closure verdict

End with one of the following:

- **READY FOR INDEPENDENT SPECIALIST/REFEREE PASS**
- **READY ONLY AS A SHORT SYNTHESIS/CORRECTION NOTE**
- **MORE MATHEMATICAL RESEARCH REQUIRED**
- **DO NOT PURSUE AS A STANDALONE PAPER**

Do not choose the verdict from an average score. A serious correctness or priority problem overrides numerical readiness.

Also answer explicitly:

1. What is the strongest theorem/result after revision?
2. Which parts are definitely standard?
3. Which parts, if any, appear genuinely new or at least nontrivially synthesized?
4. What does ultrametricity contribute that an arbitrary partition does not?
5. What do the p-adics contribute that an arbitrary rooted tree does not?
6. Is the symmetry-group component substantive or decorative?
7. Should XOR remain in the main text?
8. Should information theory remain in the main text?
9. Is the Matte-Blanco interpretation historically and mathematically disciplined?
10. What is the best publication form and likely venue family?
11. Is the manuscript ready to be subjected to the **full hostile specialist/referee review and publication-readiness scorecard**?

Do **not** run the final publication-readiness referee scorecard in this phase unless the research closure is unequivocally complete. The next thread will perform that independent referee pass after this gate.