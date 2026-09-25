# Test Run Guide

Every CSV and JSON result currently available in the working session is included under `test_runs/all/`. This intentionally favors provenance over tidiness.

## Start with these pure-Boolean files

- `All_16_CMs_in_the_intrinsic_phase_algebra.csv`
- `Intrinsic_phase_algebra_summary.csv`
- `All_Boolean_square_roots_of_the_180-degree_phase.csv`
- `All_unital_XOR-linear_star_automorphisms.csv`
- `Distinct_principal_ideals__the_full_ideal_chain_.csv`
- `Nilpotent_chain_generated_by_u____AND__XOR__UP_____L_.csv`
- `star-conjugate_norm_values.csv`
- `Intrinsic_2x2_star-unitary_search.csv`
- `Sample_non-monomial_intrinsic_star-unitaries.csv`
- `Reversible_CM-mixer_search.csv`
- `CM-native_splitter___phase___recombiner_experiment.csv`
- `Exact_CM_phase_kickback_identity.csv`
- `CM_kickback_for_Boolean_oracle_values.csv`
- `CM_phase_transform___ANF_transform_verification.csv`
- `CM_constant-vs-nonconstant_exhaustive_verification.csv`
- `CM_affine_hidden-string___Bernstein-Vazirani-like_verification.csv`
- `Fresh_CM-to-ANF_propagation_verification.csv`
- `Illustrative_operator-folding_benchmark.csv`
- `Two-bit_CM_Grover-like_search.csv`
- `Pure-Boolean_CM_Bell-state_experiment.csv`
- `Four_Bell-like_CM_states.csv`
- `Local_CM_gates_generate_Bell-like_orbit.csv`
- `Local_reversible_CM_mixers_preserving_Bell_correlation.csv`
- `Pure-Boolean_intrinsic-unitary_Bell_transform.csv`
- `Boolean_Bell-basis_local_encoding_and_decoding.csv`

## Useful negative/obstruction results

- `Exhaustive_Hadamard-analogue_search.csv`
- `Exhaustive_normalized-Hamming_operator_search.csv`
- `C4_isometry_classification.csv`
- `Structure_of_the_measure-preserving_operators.csv`
- `All_phase-response_patterns_allowed_by_strict_shell_preservation.csv`

These document why certain Hamming-preserving/Hadamard-like approaches failed. They are valuable constraints, not discarded failures.

## Signed-lift reference files

Files such as `Clifford_closure_tests.csv`, `C8___T-gate_extension_tests.csv`, `Corrected_CHSH_phase-layer_result.csv`, `Exact_lifted-CM_H-S-H_interference.csv`, Bell-correlation CSVs and Grover/Deutsch-Jozsa lifted tests belong to the separate signed/cyclotomic extension. They are useful comparison material but are not part of the pure-Boolean algebra's core claims.

## Superseded historical hypotheses

Treat these filenames as historical provenance, not current conclusions:

- `Exact_CHSH___C16_phase_extension.csv`
- `Why_maximal_CHSH_needs_the_C16_lift.csv`

The earlier C16-necessity interpretation was corrected. The current signed-lift conclusion is that C8/Clifford+T suffices projectively for the optimal CHSH measurement rotations.

## Re-run rule

A new thread should prefer re-running decisive finite searches from source rather than treating CSV rows as proof. The latest `Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip` and `CM_Phase_Calculus_Source_and_Verification.zip` contain the reproducibility materials for the two papers.
