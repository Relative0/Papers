import unittest
from itertools import product

from src.cm_ring import (
    E0, E1, E2, DELTA, OMEGA, UNITS, bar, identity, inverse_matrix,
    kron, matmul, matvec, quotient, star,
)
from src.analysis_core import (
    BASIS_X, BASIS_Y, BASIS_Z, CNOT, C_SHEAR_LOWER, HSTAR, I2, X2,
    bell_support_coverage, bell_tables, bstar_teleportation_failure,
    compatible_bell_globals, gate_inventory, ghz_analysis, measurement_bases,
    offdiagonal_hardy_witnesses, smith_class_inventory, smith_modal_contextuality_inventory,
    teleportation_protocol, teleportation_resource_theorem, teleportation_resource_smith_summary,
    singular_teleportation_hierarchy,
    two_sat_all_bases, two_sat_support_coverage_all_bases,
    verify_known_structures,
)


class RingTests(unittest.TestCase):
    def test_phase_relations(self):
        self.assertEqual(star(E1, E1), E2)
        self.assertEqual(star(E2, E2), E0)
        self.assertEqual(star(DELTA, DELTA), 0)
        self.assertEqual(star(OMEGA, OMEGA), 0)
        self.assertNotEqual(E2, E0)

    def test_conjugation_and_units(self):
        self.assertEqual(bar(E1), 8)  # E3
        self.assertEqual(bar(E2), E2)
        for g in UNITS:
            self.assertEqual(star(bar(g), g), E0)

    def test_original_support_quotient(self):
        self.assertEqual(quotient(0b1110, 0b0110), 0b1000)
        self.assertEqual(quotient(0b1010, 0b1010), 0)


class KnownGateTests(unittest.TestCase):
    def test_requested_regressions(self):
        r = verify_known_structures()
        self.assertTrue(r["C_squared_identity"])
        self.assertTrue(r["Hstar_squared_identity"])
        self.assertTrue(r["Hstar_dagger_Hstar_identity"])
        self.assertEqual(r["C_basis0"], (E0, E0))
        self.assertTrue(r["phase_kickback_Xchi_equals_zchi"])
        self.assertTrue(r["P_fourth_power_identity"])
        self.assertTrue(r["P_transpose_equals_inverse"])
        self.assertEqual(r["Bstar_basis_nonzero_branch_counts"], (2, 2, 2, 2))
        self.assertEqual(r["Bstar_reversible_state_checks"], 16 ** 4)

    def test_hstar_splits_both_basis_states(self):
        self.assertEqual(matvec(HSTAR, (E0, 0), 2), (E0, DELTA))
        self.assertEqual(matvec(HSTAR, (0, E0), 2), (DELTA, E0))


class GateAndMeasurementClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.GL, cls.UNI, cls.summary = gate_inventory()
        cls.bases, cls.unitary_bases = measurement_bases(cls.GL, cls.UNI)

    def test_gate_counts(self):
        s = self.summary
        self.assertEqual(s["all_2x2_matrices"], 65536)
        self.assertEqual(s["invertible"], 24576)
        self.assertEqual(s["intrinsic_unitary"], 512)
        self.assertEqual(s["monomial_phase_permutation"], 128)
        self.assertEqual(s["genuine_branch_mixer"], 24448)
        self.assertEqual(s["full_two_branch_splitter"], 20608)
        self.assertEqual(s["unitary_monomial"], 128)
        self.assertEqual(s["unitary_full_splitter"], 384)

    def test_projective_measurement_basis_counts(self):
        self.assertEqual(len(self.bases), 192)
        self.assertEqual(len(self.unitary_bases), 4)

    def test_bstar_logical_but_not_strong_for_all_192_reversible_bases(self):
        beta = (E0, 0, 0, DELTA)
        cov = two_sat_support_coverage_all_bases(beta, self.bases)
        self.assertTrue(cov["satisfiable"])
        self.assertEqual(cov["possible_sections"], 137216)
        self.assertEqual(cov["extendable_possible_sections"], 100352)
        self.assertEqual(cov["uncovered_possible_sections"], 36864)
        self.assertEqual(cov["first_uncovered"], (0, 0, 0, 0))

    def test_support_coverage_2sat_matches_bruteforce_on_unitary_bases(self):
        beta = (E0, 0, 0, DELTA)
        good, uncovered = bell_support_coverage(beta, self.unitary_bases)
        cov = two_sat_support_coverage_all_bases(beta, self.unitary_bases)
        self.assertTrue(cov["satisfiable"])
        self.assertEqual(len(uncovered), cov["uncovered_possible_sections"])
        self.assertEqual(cov["uncovered_possible_sections"], 0)
        self.assertGreater(len(good), 0)

    def test_offdiagonal_hardy_witnesses(self):
        witnesses = offdiagonal_hardy_witnesses(self.bases)
        self.assertEqual(len(witnesses), 6)
        expected = {
            "R/R": (1, 0, 0, 1),
            "R/X": (0, 1, 1, 1),
            "D/X": (1, 1, 1, 0),
            "D/R": (0, 1, 1, 1),
        }
        self.assertTrue(all(w["tables"] == expected for w in witnesses))

    def test_complete_smith_contextuality_classification(self):
        rows, summary = smith_modal_contextuality_inventory(self.bases)
        self.assertEqual(summary["strong_contextual_classes"], 4)
        self.assertEqual(summary["logical_not_strong_classes"], 6)
        self.assertEqual(summary["relationally_local_nonzero_classes"], 4)
        self.assertEqual(summary["degenerate_zero_classes"], 1)
        statuses = {(r["smith_a"], r["smith_b"]): r["classification"] for r in rows}
        for a in range(4):
            self.assertEqual(statuses[(a, a)], "STRONG_CONTEXTUAL")
            self.assertEqual(statuses[(a, 4)], "RELATIONALLY_LOCAL")
        for a in range(4):
            for b in range(a + 1, 4):
                self.assertEqual(statuses[(a, b)], "LOGICAL_CONTEXTUAL_NOT_STRONG")
        self.assertEqual(statuses[(4, 4)], "DEGENERATE_ZERO_EXCLUDED")


class ModalBellTests(unittest.TestCase):
    def test_support_bell_has_no_global_assignment(self):
        state = (E0, 0, 0, E0)
        good = compatible_bell_globals(state, (BASIS_Z, BASIS_X, BASIS_Y))
        self.assertEqual(len(good), 0)

    def test_bell_tables_match_regression(self):
        tables, _ = bell_tables()
        self.assertEqual(tables[("Z", "Z")], (1, 0, 0, 1))
        self.assertEqual(tables[("Z", "X")], (1, 1, 1, 0))
        self.assertEqual(tables[("Z", "Y")], (0, 1, 1, 1))
        self.assertEqual(tables[("X", "Y")], (1, 0, 0, 1))


class TeleportationTests(unittest.TestCase):
    def test_universal_protocol(self):
        p, rows = teleportation_protocol()
        self.assertEqual(p["checks"], 1024)
        self.assertEqual(len(rows), 1024)
        self.assertTrue(all(r["exact"] for r in rows))
        self.assertTrue(all(r["branch_possible_for_nonzero_input"] for r in rows))
        self.assertEqual(matmul(p["Q_inverse"], p["Q"], 4), identity(4))

    def test_bstar_resource_obstruction(self):
        f = bstar_teleportation_failure()
        self.assertFalse(f["all_branch_maps_invertible"])
        self.assertEqual(tuple(f["branch_determinants"]), (0, 0, 0, 0))

    def test_resource_theorem_over_all_65536_resources(self):
        inventory, classes, stateclass, separable, summary = smith_class_inventory(24576)
        theorem, rows = teleportation_resource_theorem(stateclass)
        by_class = teleportation_resource_smith_summary(rows)
        self.assertEqual(theorem["resource_states_checked"], 65536)
        self.assertEqual(theorem["successful_resource_states"], 24576)
        self.assertTrue(theorem["all_fixed_analyzer_rows_invertible"])
        self.assertTrue(all(d in UNITS for d in theorem["fixed_analyzer_row_determinants"]))
        winners = [(r["smith_a"], r["smith_b"]) for r in by_class if r["teleportation_capable_class"]]
        self.assertEqual(winners, [(0,0)])
        self.assertEqual(next(r for r in by_class if (r["smith_a"],r["smith_b"])==(0,0))["universal_exact_teleportation_resources"], 24576)
        self.assertEqual(sum(r["universal_exact_teleportation_resources"] for r in by_class if (r["smith_a"],r["smith_b"])!=(0,0)), 0)

    def test_singular_resource_hierarchy(self):
        summary, rows = singular_teleportation_hierarchy()
        by = {(r["smith_a"], r["smith_b"]): r for r in rows}
        self.assertEqual(len(rows), 15)
        self.assertEqual(by[(0,0)]["max_exact_common_state_family_size"], 256)
        self.assertEqual(by[(0,2)]["max_exact_common_state_family_size"], 16)
        self.assertEqual(by[(1,1)]["max_exact_common_state_family_size"], 1)
        self.assertEqual(by[(0,2)]["canonical_quotient_classes"], 64)
        self.assertEqual(by[(1,1)]["canonical_quotient_classes"], 64)
        self.assertEqual(by[(0,2)]["max_fixed_quotient_success_outcomes_of_4"], 2)
        self.assertEqual(by[(1,1)]["max_fixed_quotient_success_outcomes_of_4"], 4)
        self.assertEqual(by[(0,4)]["max_fixed_quotient_success_outcomes_of_4"], 3)
        self.assertTrue(by[(0,2)]["deterministic_free_line_protocol"])
        self.assertFalse(by[(1,1)]["deterministic_free_line_protocol"])
        self.assertEqual(by[(0,2)]["residue_field_rank"], 1)
        self.assertEqual(by[(1,1)]["residue_field_rank"], 0)
        self.assertEqual(by[(0,2)]["finite_tensor_power_universal_activation"], 0)
        self.assertEqual(by[(1,1)]["finite_tensor_power_universal_activation"], 0)
        self.assertEqual(by[(0,0)]["finite_tensor_power_universal_activation"], 1)



class SmithAndSeparabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory, cls.classes, cls.stateclass, cls.separable, cls.summary = smith_class_inventory(24576)

    def test_class_counts(self):
        s = self.summary
        self.assertEqual(s["classes"], 15)
        self.assertEqual(s["separable_classes"], 5)
        self.assertEqual(s["nonseparable_classes"], 10)
        self.assertEqual(s["distinct_separable_states"], 5266)
        self.assertEqual(s["distinct_nonseparable_states"], 60270)
        self.assertEqual(s["factorization_class_mismatches"], 0)

    def test_support_and_bstar_bell_different_smith_classes(self):
        self.assertEqual(self.stateclass[(E0, 0, 0, E0)], (0, 0))
        self.assertEqual(self.stateclass[(E0, 0, 0, DELTA)], (0, 2))
        bstar_outputs = verify_known_structures()["Bstar_basis_outputs"]
        self.assertEqual(tuple(self.stateclass[v] for v in bstar_outputs), ((0,2),(0,2),(0,2),(0,2)))


class GHZTests(unittest.TestCase):
    def test_support_ghz_strong_modal_contradiction(self):
        result, _ = ghz_analysis(a000=E0, a111=E0)
        self.assertEqual(result["global_assignments"], 0)
        self.assertEqual(result["minimum_unsat_context_count"], 6)

    def test_delta_ghz_is_local_for_tested_mqt_family(self):
        result, _ = ghz_analysis(a000=E0, a111=DELTA)
        self.assertGreater(result["global_assignments"], 0)
        self.assertEqual(result["uncovered_possible_sections"], 0)


class GlobalUnitSupportTests(unittest.TestCase):
    def test_unit_scaling_preserves_zero_nonzero_support(self):
        for g, a in product(UNITS, range(16)):
            self.assertEqual(star(g, a) == 0, a == 0)


if __name__ == "__main__":
    unittest.main()
