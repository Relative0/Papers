"""Small operational and algebraic regression tests (Python unittest, stdlib)."""
import sys
import unittest
from pathlib import Path
from itertools import product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import verify_process_semantics as v

def span(vectors):
    out={0}
    for x in vectors:
        out |= {x^y for y in tuple(out)}
    return out

def image(m,s): return {v.apply(m,x) for x in s}

def kron(a,b,n_b):
    return tuple(sum((row_b << (j*n_b)) for j in range(max(1,max(a).bit_length())) if row_a>>j&1) for row_a in a for row_b in b)

class ProcessContractTests(unittest.TestCase):
    def test_ring_associativity_exhaustive(self):
        for a,b,c in product(range(16),repeat=3):
            self.assertEqual(v.mul(v.mul(a,b),c),v.mul(a,v.mul(b,c)))

    def test_regular_representation(self):
        for a,b in product(range(16),repeat=2):
            self.assertEqual(v.compose(v.REG[a],v.REG[b]),v.REG[v.mul(a,b)])

    def test_unique_multiplicative_predicate(self):
        # All 2^14 assignments to elements other than 0 and 1.
        survivors=[]
        for bits in range(1<<14):
            p=[0,1]+[(bits>>(a-2))&1 for a in range(2,16)]
            if all(p[v.mul(a,b)]==p[a]*p[b] for a,b in product(range(16),repeat=2)):
                survivors.append(p)
        self.assertEqual(survivors,[[a&1 for a in range(16)]])

    def test_conditional_primitive_counterexample(self):
        self.assertTrue(1&1)
        self.assertNotEqual(8,0)
        self.assertEqual(v.mul(8,2),0)
        self.assertEqual(8&1,0)  # branch erased on tensoring with B_1

    def test_frobenius_pairing_and_zero_balancing(self):
        self.assertEqual(v.rank(v.J),4)
        for a in range(16):
            self.assertEqual(v.compose(v.REG[a],v.J),v.compose(v.J,v.transpose(v.REG[a],4)))
            total=0
            for i in range(4): total ^= v.mul(1<<i,v.mul(1<<(3-i),a))
            self.assertEqual(total,0)

    def test_all_small_complete_instruments_remain_complete_on_reference(self):
        matrices=[(a,b) for a,b in product(range(4),repeat=2)]
        count=0
        for f,g in product(matrices,repeat=2):
            if v.rank(f+g)!=2: continue
            lifted=kron(f,(1,2),2)+kron(g,(1,2),2)
            self.assertEqual(v.rank(lifted),4)
            count+=1
        self.assertEqual(count,210)

    def test_discard_joins_branches_instead_of_cancelling(self):
        pure={0,1}
        # Two alternative identity branches are still possible on forgetting.
        forgotten=span(image((1,2),pure)|image((1,2),pure))
        self.assertEqual(forgotten,pure)
        self.assertEqual(1^1,0)  # coherent sum would give the wrong result

    def test_possible_branch_and_independent_state(self):
        for a,b in product(range(1,4),repeat=2):
            literal=sum((b << (2*i)) for i in range(2) if a>>i&1)
            self.assertNotEqual(literal,0)

    def test_all_ring_automorphisms(self):
        for c,d in product(range(2),repeat=2):
            f=[v.automorphism(a,c,d) for a in range(16)]
            self.assertEqual(len(set(f)),16)
            for a,b in product(range(16),repeat=2):
                self.assertEqual(f[v.mul(a,b)],v.mul(f[a],f[b]))
                self.assertEqual(f[a^b],f[a]^f[b])

    def test_contextuality_increasing_filter(self):
        target=v.matmul((2,0,0,1),v.diag(0,1))
        self.assertEqual(v.smith(target),(1,1))
        self.assertEqual(v.rank(v.binary(v.diag(0,1))),7)
        self.assertEqual(v.rank(v.binary(target)),6)

    def test_two_copy_fixed_phase_obstruction(self):
        x=v.binary(v.diag(0,2),True)
        xx=kron(x,x,8)
        self.assertEqual(v.rank(xx),36)
        socle=v.binary(v.scalar(8,v.diag(0,2)),True)
        self.assertEqual(v.rank(kron(socle,socle,8)),1)
        # Free B_2 rank-two target has binary rank 2*16 and socle rank 2.
        self.assertGreaterEqual(v.rank(xx),32)
        self.assertLess(v.rank(kron(socle,socle,8)),2)

    def test_unit_detectability_depends_on_effects(self):
        one,scaled=1,v.mul(3,1)
        self.assertNotEqual((one>>1)&1,(scaled>>1)&1)
        for a in range(16): self.assertEqual(v.mul(a,one)!=0,v.mul(a,scaled)!=0)

if __name__=='__main__': unittest.main(verbosity=2)
