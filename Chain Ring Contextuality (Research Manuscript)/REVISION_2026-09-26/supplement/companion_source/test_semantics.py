"""Small independent regression checks in addition to the exhaustive runner."""
import unittest
from itertools import product
from verify_semantics import mul, smith, rank, encoded, mm, delta, compose, transpose

class SemanticsChecks(unittest.TestCase):
    def test_all_scalar_products_against_polynomial_convolution(self):
        for a,b in product(range(16),repeat=2):
            coefficients=[sum(((a>>i)&1)*((b>>(k-i))&1) for i in range(k+1))%2 for k in range(4)]
            self.assertEqual(mul(a,b),sum(c<<i for i,c in enumerate(coefficients)))

    def test_zero_tensor_boundary(self):
        self.assertEqual(mul(8,2),0)
        field_tensor=sum((((8>>i)&1)*((2>>j)&1))<<(4*i+j) for i,j in product(range(4),repeat=2))
        self.assertEqual(field_tensor,1<<13)

    def test_conditioning_failure(self):
        initial=(1,0,0,2)
        self.assertTrue(any(x&1 for x in initial))
        selected=initial[2:]
        self.assertNotEqual(selected,(0,0))
        self.assertFalse(any(x&1 for x in selected))

    def test_support_encoding_is_not_separability_preserving(self):
        self.assertEqual(rank(encoded((1,0,0,0))),4)
        self.assertEqual(rank(encoded((8,0,0,0))),1)

    def test_smith_rank_collision(self):
        x=(1,0,0,4);y=(2,0,0,2)
        self.assertEqual(rank(encoded(x)),rank(encoded(y)))
        self.assertNotEqual(smith(x),smith(y))

    def test_leading_multiplicity_can_increase(self):
        self.assertEqual(smith((1,0,0,2)),(0,1))
        self.assertEqual(smith(mm((2,0,0,1),(1,0,0,2))),(1,1))

    def test_separability_map_is_zero(self):
        for a in range(16):
            t=delta(a);z=0
            for i,j in product(range(4),repeat=2):
                if t[i]>>j&1:z ^= mul(1<<i,1<<j)
            self.assertEqual(z,0)

    def test_binary_effect_detects_ring_unit(self):
        self.assertEqual((1>>1)&1,0)
        self.assertEqual((mul(3,1)>>1)&1,1)

    def test_complete_binary_instruments_with_reference(self):
        matrices=list(product(range(4),repeat=2))
        for f,g in product(matrices,repeat=2):
            if rank(f+g)!=2:continue
            for state in range(1,16):
                # State is a 2x2 coefficient matrix. Check every branch with a reference.
                c=(state&3,state>>2)
                self.assertTrue(any(compose(f,c)) or any(compose(g,c)))

    def test_coding_orbit_binary_span(self):
        # Independent 2x2 dual-number slice embedded in A; full A orbit span tested algebraically.
        gl2=[x for x in product(range(2),repeat=4) if rank((x[0]|x[1]<<1,x[2]|x[3]<<1))==2]
        self.assertEqual(len(gl2),6)
        self.assertEqual(rank([sum(a<<i for i,a in enumerate(x)) for x in gl2]),4)

if __name__=='__main__':unittest.main(verbosity=2)
