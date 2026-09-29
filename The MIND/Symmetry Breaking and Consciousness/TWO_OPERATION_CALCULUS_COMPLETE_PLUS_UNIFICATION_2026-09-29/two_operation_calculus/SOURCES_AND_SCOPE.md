# Sources, scope, and verification discipline

**Project:** A Mathematical Calculus of Differentiation, Observation, and Conditioning  
**Audit date:** 28 September 2026

## Supplied project sources used

The audit treated all supplied claims as provisional and used the following project materials as its primary internal source base:

1. `Thesis v_12.pdf` (2015), especially the CM/bra-ket sections, the logical projection/measurement definitions, the context-relative "pure logic state" discussion, and the distinguishing/unfolding operator.
2. `CM_MEASUREMENT_AUDIT_PACKAGE_2026-09-28.zip` and its extracted reports/tables, especially `CM_MEASUREMENT_AUDIT.md` and `MEASUREMENT_FORMALISM.md`.
3. `CM_LM_Boolean_Operator_Calculus_Revised.tex`, the current typed CM/LM foundations manuscript.
4. `ProLT_Observation_Topologies_Submission_v0.9_FINAL.tex`, especially its section **Information refinement and logical update**.
5. Library ProLT research notes v0.1--v0.5, especially:
   - `ProLT_Controlled_Refinement_Regimes_v0.3.pdf`;
   - `ProLT_Homotopy_Preserving_Observations_v0.4.pdf`;
   - `ProLT_Simultaneous_Observation_Refinement_v0.5.pdf`;
   - `ProLT_Research_Ledger_v0.1-v0.5.md`.
6. `binary_order_thinning_finite_posets_reviewed_v3.tex`, used to delimit same-carrier post-T0 refinement from pre-T0 point splitting.
7. `Chain Ring.tex`, used only to locate the boundary at which additional modal/nonclassical state-effect semantics enter.

## External literature search

A theorem/construction-level web search was run through 2026. The main antecedent clusters were:

- information partitions and common knowledge (Aumann 1976);
- rough-set information systems and indiscernibility partitions (Pawlak 1982 and later surveys);
- Blackwell comparison of experiments (Blackwell 1951/1953; active extensions continue through 2026);
- Dynamic Epistemic Logic and Public Announcement Logic;
- Test Cover / separating systems;
- Formal Concept Analysis and attribute reduction;
- information algebras;
- Eigenlogic;
- modal quantum theory;
- sheaf-theoretic contextuality.

The literature conclusion is conservative: the **base two-operation calculus is not a new mathematical foundation**. Its partition/refinement and event-conditioning pieces are standard in several mature literatures. The potentially distinctive project content lies in the way those operations are connected to the existing ProLT positive-observation topology/order-complex machinery and to the typed CM/LM representation layer.

## Computational verification

`two_operation_compute.py` performs the principal exhaustive finite computations. `verify_two_operation_independent.py` independently reconstructs the core claims using sets/frozensets rather than importing the main implementation.

The independent verifier passed. All numerical claims in the audit should be understood as bounded finite evidence, not as novelty evidence.
