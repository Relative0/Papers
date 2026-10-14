# Interaction-core research gate

Date: 29 September 2026.

**Verdict: Level B mathematically, with conservative priority.** A second exact interacting theorem exists. The gate also disproves unrestricted E2-collapse for every proposed broad graph class by explicit integral witnesses. The frozen handoff, v0.3 manuscript, and its pre-existing unmerged matching section remain unchanged.

## Principal results

1. The mixed-core spectral sequence is made explicit on C_*(K,U), with missing-first orientations, augmented available links, signed d1 inclusion maps, and the correct one-degree shift to cone homology. If the largest core has M>=2 vertices, it stabilizes at E^(M-1).
2. If there is no mixed core of size four, the entire relative complex is Cone(h:B->A)[2], where A and B are sums of edge- and triple-core available-link chains. This gives E2 collapse, exact integral homology with extensions retained, and a necessary-and-sufficient acyclicity criterion: h is a quasi-isomorphism.
3. The no-four-core condition holds for degree-two graphs except C4 components whose two colour pairs are both comparable. Paths reduce to endpoint star blocks, with the three-edge path retaining its shared middle edge. Cycles of length at least six have no triple cores and satisfy the old coarse-edge-link sum under a strictly broader hypothesis than graph matching.
4. All degree-two systems stabilize by E3. The residual C4 block has an explicit three-column complex and a single possible d2, computed by a signed filling zigzag. The eight-state C4 example realizes d2:Z->Z as a unit, proving the E3 bound sharp.
5. A seven-state K1,3 example has d2:Z->Z² primitive injective. Thus forest, Ferrers, and chordal-bipartite hypotheses alone do not give E2 collapse, even with free first-page groups.
6. In the all-exclusive star Q={p}+R, every available core link has reduced H0=Z and d1 is the ordinary chain boundary of Delta R. The sequence collapses at E2, and H_n(cone)=H_(n-1)(Delta R), ordinary homology on the right. A 32-state projective-plane realization produces Z/2 through interaction even though every available core link and coarse edge link is torsion-free.

These are homology results. They are not universal homotopy decompositions, TU theorems, or canonical integral direct sums.

## Proof and evidence separation

The general statements are proved in SPECTRAL_SEQUENCE_CONSTRUCTION.md, MAX_DEGREE_TWO_CLASSIFICATION.md, and FERRERS_AND_CHORDAL_CASES.md. The counterexamples have exact link/chain proofs and integral certificates. Computation is supporting evidence and witness verification.

The principal exhaustive field run covers 90,201 naturally labelled poset/profile cases through five states, plus 5,000 random six-state trials. It is supplemented by selected integral SNF checks, local examples, targeted star/C4 searches, signed integral d2 certificates, and a separate torsion audit. The exact scopes, coefficients, seeds, and scripts are in COMPUTATIONAL_INTERACTION_AUDIT.md. No full integral enumeration through five states is claimed. No global minimality of either higher-differential witness is claimed.

The 83-file handoff manifest was verified before research and after the computations. The baseline and prepared matching section are byte-for-byte unchanged. One old-record clarification is preserved: the 1,707 product-link checks were over F2, whereas the 3,242 matching cases were integral. The distributive endpoint statement implicitly requires distinct bottom and top; the empty generating poset is excluded.

## Required final questions

1. **Does a second exact theorem exist?** Yes: the two-column interaction theorem, its degree-two structural recognition, and the all-exclusive star theorem are exact. The strongest general degree-two page statement is E3, not E2.
2. **Which class gives the strongest result?** For controlled overlap, degree at most two with no doubly comparable C4 gives an exact chain-cone formula and necessary-and-sufficient homology-neutrality test. The full degree-two class additionally has an exact three-column/d2 calculation. The all-exclusive star is an independent unbounded-core class with a closed integral homology formula.
3. **What is the exact spectral sequence/complex?** E1_(p,q)=sum_(|S|=p) Htilde_q(Lambda_S), with d1 the signed core-deletion inclusions, converging to gr H_(p+q)(K,U), hence cone degree p+q-1. With only edge/triple cores, C(K,U)=Cone(h)[2]. With a four-core, retain its third column and secondary zigzag differential.
4. **When does E2 collapse?** Proven when there is no mixed core of size four; in degree two this is exactly exclusion of a C4 with both pairs comparable. This is a sufficient class condition, not a necessary condition for a particular system to collapse: the minimal four-chain C4 does collapse at E2. All-exclusive stars also collapse at E2 by a one-row argument. Unrestricted degree two, Ferrers, chordal-bipartite, and forest claims are false.
5. **How are empty graphs and matching recovered?** No exclusive edges means the mixed complex vanishes and the frozen isotone-section theorem gives homotopy neutrality. Matching gives only edge cores, full product links, and the original shifted coarse-edge-link sum. More generally the same formula holds whenever comparable same-colour common-neighbour pairs are absent.
6. **How is K1,2 explained?** In the frozen three-state K1,2 counterexample, its triple-link reduced H0=Z maps by the primitive signed diagonal to the two available-edge-link reduced H0 groups Z². The cokernel is Z in cone degree one. The coarse links alone omit this attachment data.
7. **Does interaction create torsion?** Yes. The verified RP2 face-poset all-exclusive star has only free link homology, but d1 produces cone H2=Z/2 (and H1=Z). It is distinct from torsion inherited from a matching link.
8. **What is the smallest counterexample outside the hypotheses?** K1,2 on three states remains the smallest failure of independent coarse-edge summation. The gate has a seven-state star and an eight-state C4 for E2 noncollapse, each minimal under its own induced restrictions. A globally smallest d2 witness is not established; exhaustive F2 coverage through five states does not settle six states.
9. **Is this stronger than standard obstruction/fiber theory?** It gives exact model-specific computations beyond sufficient fibre-contractibility tests. It is not a stronger general theory. The available links are literally the obstruction complexes of Chacholski--Jin--Scolamiero--Tombari, and the filtration algebra is classical. The value is the special recognition, graph restrictions, and explicit integral failure boundary; priority remains conservative.
10. **Merge or second paper?** The matching and interaction results form one coherent theorem arc and should be considered together after a proof/priority/editorial convergence pass. Retain a separate research supplement now. The gate has not merged or rewritten v0.3, and does not justify presenting a submission-ready manuscript.
11. **Single next theorem?** Determine which integral maps can occur as the C4 secondary differential when every available link has free homology. Specifically, for each k>=2, can a K2,2 system realize d2:Z->Z as multiplication by k, or is there a structural restriction? This would locate interaction-created torsion at the smallest graph permitting a higher differential. Defer this new research until the convergence pass.

## Deliverables and review

The required reports, reproducible scripts, machine-readable tables, and HANDOFF_TO_MASTER.md are included beside this file. MANUSCRIPT_INTERACTION_SECTION.tex is a new candidate insertion, not a modification of either frozen manuscript file. It has been mathematically reviewed but not compiled into the baseline; the local MiKTeX installation is uninitialized, and no environment changes were made to repair it.

ADVERSARIAL_REVIEWS.md records actual independent agent attacks and the fixes/limits they established. These are internal adversarial reviews, not reports by external human referees. LITERATURE_PRIORITY_MAP.md records primary-source comparisons and uncertainty rather than certifying novelty.

## Recommended next action

The requested gate is complete. The next useful phase is proof/priority/editorial convergence before any merge, in this task while these definitions, proofs, and authorization boundaries remain active. Use a strong mathematical reasoning model (gpt-6-astra, high effort); an inexpensive copy-editing pass alone would not address the remaining priority and theorem-scope judgments. No further computation is required for this gate. A new theorem search is optional and should wait for that convergence decision.
