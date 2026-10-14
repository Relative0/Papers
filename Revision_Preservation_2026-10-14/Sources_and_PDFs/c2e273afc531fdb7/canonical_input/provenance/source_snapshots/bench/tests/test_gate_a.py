import itertools
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cmbench.anf import ANFBudget, ANFBudgetExceeded, ANFStats, eval_mask_poly, propagate_mask_dag
from cmbench.core import Bin, OPS, Var, eval_expr, vars_of
from cmbench.optimize import cm_frontend, cse_flat_frontend, generic_2support_frontend
from cmbench.workloads import mixed_support_dag, same_operand_tree


class TestGateA(unittest.TestCase):
    def assert_equiv(self, a, b):
        order = tuple(sorted(vars_of(a)))
        self.assertEqual(order, tuple(sorted(vars_of(b))))
        if len(order) <= 10:
            for bits in itertools.product((0, 1), repeat=len(order)):
                env = dict(zip(order, bits))
                self.assertEqual(eval_expr(a, env), eval_expr(b, env))

    def test_frontends_equivalent(self):
        for seed in range(10):
            e = mixed_support_dag(6, 4, seed, 0.25, 0.5)
            for fn in (cm_frontend, generic_2support_frontend, cse_flat_frontend):
                out, _ = fn(e)
                self.assert_equiv(e, out)

    def test_generic_cut_is_stronger_than_cm_on_two_support_shape(self):
        x, y = Var("x"), Var("y")
        left = Bin(OPS["AND"], x, y)
        right = Bin(OPS["XOR"], x, Bin(OPS["AND"], x, y))
        e = Bin(OPS["OR"], left, right)
        cm, cms = cm_frontend(e)
        gen, gs = generic_2support_frontend(e)
        self.assert_equiv(e, cm)
        self.assert_equiv(e, gen)
        self.assertGreater(gs.successful_folds, cms.successful_folds)

    def test_cse_flat_xnor_reassociation(self):
        vs = [Var(f"x{i}") for i in range(5)]
        e = Bin(OPS["XNOR"], Bin(OPS["XNOR"], vs[0], vs[1]), Bin(OPS["XNOR"], vs[2], Bin(OPS["XNOR"], vs[3], vs[4])))
        out, stats = cse_flat_frontend(e)
        self.assert_equiv(e, out)
        self.assertGreaterEqual(stats.associative_flattened_nodes, 1)

    def test_mask_backend_matches_source(self):
        for seed in range(10):
            e = same_operand_tree(5, seed=seed, reverse_prob=0.5, affine_fraction=0.5)
            order = tuple(sorted(vars_of(e)))
            s = ANFStats()
            p = propagate_mask_dag(e, order, s, budget=ANFBudget(max_monomials=10000))
            for bits in itertools.product((0, 1), repeat=len(order)):
                env = dict(zip(order, bits))
                self.assertEqual(eval_expr(e, env), eval_mask_poly(p, order, env))

    def test_budget_guard(self):
        e = mixed_support_dag(12, 7, 123, 0.0, 0.25)
        order = tuple(sorted(vars_of(e)))
        with self.assertRaises(ANFBudgetExceeded):
            propagate_mask_dag(
                e,
                order,
                ANFStats(),
                budget=ANFBudget(max_monomials=1),
            )


if __name__ == "__main__":
    unittest.main()
