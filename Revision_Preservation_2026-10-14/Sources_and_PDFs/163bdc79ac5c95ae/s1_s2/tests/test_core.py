import itertools, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from cmbench.core import *
from cmbench.anf import *
from cmbench.workloads import same_operand_tree,mixed_tree

class TestCM(unittest.TestCase):
  def test_anf_rule_all_16(self):
    for bits in itertools.product((0,1), repeat=4):
      cm=tuple(bits); a,b,c,d=cm_anf_coeffs(cm)
      for x,y in itertools.product((0,1),repeat=2):
        self.assertEqual(cm_eval(cm,x,y), a^ (b&x) ^ (c&y) ^ (d&x&y))
  def test_parity_nonlinear(self):
    for bits in itertools.product((0,1),repeat=4):
      cm=tuple(bits)
      self.assertEqual(bool(cm_feature_parity(cm)),cm_is_nonlinear(cm))
  def test_transpose(self):
    for bits in itertools.product((0,1),repeat=4):
      cm=tuple(bits); tr=cm_swap_operands(cm)
      for x,y in itertools.product((0,1),repeat=2):
        self.assertEqual(cm_eval(tr,x,y),cm_eval(cm,y,x))
  def test_operand_negations(self):
    for bits in itertools.product((0,1),repeat=4):
      cm=tuple(bits)
      for x,y in itertools.product((0,1),repeat=2):
        self.assertEqual(cm_eval(cm_negate_left_operand(cm),x,y),cm_eval(cm,1-x,y))
        self.assertEqual(cm_eval(cm_negate_right_operand(cm),x,y),cm_eval(cm,x,1-y))
  def test_composition_all(self):
    cms=list(itertools.product((0,1),repeat=4))
    for phi in cms:
      for a in cms:
       for b in cms:
        h=cm_compose(phi,a,b)
        for x,y in itertools.product((0,1),repeat=2):
          self.assertEqual(cm_eval(h,x,y),cm_eval(phi,cm_eval(a,x,y),cm_eval(b,x,y)))
  def test_fold_exhaustive_envs(self):
    for seed in range(20):
      e=same_operand_tree(4,seed)
      for fn in (fold_cm,fold_generic_2support):
        f=fn(e,[])
        for x,y in itertools.product((0,1),repeat=2):
          env={"x":x,"y":y}; self.assertEqual(eval_expr(e,env),eval_expr(f,env))
  def test_anf_backends(self):
    for seed in range(20):
      e=mixed_tree(6,4,seed); p=propagate(e,ANFStats()); order=tuple(sorted(vars_of(e))); pm=propagate_mask(e,order)
      decoded=frozenset(frozenset(order[i] for i in range(len(order)) if (m>>i)&1) for m in pm)
      self.assertEqual(p,decoded)

if __name__=='__main__': unittest.main()
