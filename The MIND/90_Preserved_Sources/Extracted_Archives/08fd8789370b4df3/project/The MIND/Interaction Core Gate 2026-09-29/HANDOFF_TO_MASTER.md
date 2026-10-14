# Handoff to master: interaction-core gate

**Date:** 29 September 2026. **Verdict:** Level B mathematically; priority conservative. **Baseline:** unchanged.

## Read next

Read INTERACTION_CORE_RESEARCH_GATE.md for the verdict and all eleven final answers, then SPECTRAL_SEQUENCE_CONSTRUCTION.md, MAX_DEGREE_TWO_CLASSIFICATION.md, COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md, LITERATURE_PRIORITY_MAP.md, and ADVERSARIAL_REVIEWS.md. Proofs of the positive star result are in FERRERS_AND_CHORDAL_CASES.md; the exact C4 witness is in C4_COUNTEREXAMPLE_PROOF.md.

## New proved results

The filtration is on C(K,U), with cone homology H_n=H_(n+1)(K,U). Missing-first orientations give E1_(p,q)=sum Htilde_q(Lambda_S) and signed core-deletion d1. The abutment cone degree is p+q-1. If maximum mixed-core size is M>=2, E^(M-1)=E_infinity.

If no core has size four, C(K,U)=Cone(h:B->A)[2], with A=edge-link augmented chains, B=triple-link augmented chains. Hence H_n(cone)=H_(n-1)(Cone h), with the exact kernel/cokernel sequence and acyclicity iff h is a quasi-isomorphism. E2 collapse does **not** assert a canonical integral direct sum.

Degree-two graphs have cores of size at most four. Four-cores occur only at C4 components whose same-colour pairs are both comparable. Excluding those gives the two-column theorem. Paths have only endpoint star blocks (the three-edge path shares its middle edge); cycles >=6 have no triple core and retain the coarse-edge-link sum. The full degree-two class has an explicit three-column C4 block and stabilizes at E3, sharply.

## New negative results

* Seven-state K1,3: integral E1=E2 has Z² at(2,1), Z at(4,0); d2 is primitive rank one; cone H2=Z. Forest, Ferrers, and chordal-bipartite E2-collapse are false.
* Eight-state K2,2: integral E1=E2 has Z at(2,1), Z at(4,0); d2 is a unit; the cone is acyclic. Maximum-degree-two E2-collapse is false.
* All-exclusive star Q={p}+R: every available link has reduced H0=Z; d1 is ordinary chains of Delta R, so H_n(cone)=H_(n-1)(Delta R). An explicit RP2 face-poset gives cone H2=Z/2 despite all available/coarse links being torsion-free. This is interaction-created torsion.

Do not claim global minimality: seven/eight states are verified witnesses minimal under their own induced restrictions. Do not erase the old three-state forest failure, matching torsion universality, or historical counterexamples.

## Computation and preservation

Main exhaustive run: all90,201 naturally labelled poset/profile cases through n5 over F2; additional5,000 seeded n6 trials. Integral checks are selected (435 in the main run), supplemented by exact local models, both signed integer d2 certificates, and every link plus the reduced torsion interaction matrix. Targeted C4 search:20,000 samples n6..10. Consult COMPUTATIONAL_INTERACTION_AUDIT.md for precise scope and canonicalization records. Never call the complete n5 run integral.

The transferred handoff resides at ../Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29/. All83 original manifest entries verify. Its v0.3 and existing MANUSCRIPT_REVISION_SECTION.tex remain frozen and unmerged. This gate's MANUSCRIPT_INTERACTION_SECTION.tex is a separate new candidate insertion. It is not compiled or integrated.

## Priority and next phase

The available links are exactly CJS-T obstruction complexes; the spectral sequence and cone algebra are standard. Candidate contribution: this observation-product specialization, its path/cycle recognition and explicit integral obstruction hierarchy. Bjorner--Wachs--Welker is a different exact decomposition under different attachment/connectivity hypotheses, not superseded by this gate.

Recommend a proof/priority/editorial convergence pass in the current task before merging matching plus interaction into a new manuscript version. No manuscript merge, external publication, commit, or push was performed. Existing authorization covers scoped reversible workspace research, not external publication.

Next optional theorem: realize or restrict d2 multiplication by k>=2 in a K2,2 profile with torsion-free available links. Defer until convergence. Preserve integral extension data, negative results, and the distinction between graph classes and the additional same-colour order/link diagram.
