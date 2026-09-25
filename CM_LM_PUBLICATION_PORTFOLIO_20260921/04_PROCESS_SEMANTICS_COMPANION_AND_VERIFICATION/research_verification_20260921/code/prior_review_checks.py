"""Independent exact checks for the review. Python 3.10+, standard library only.

No historical kernel imports. Bit j is the monomial with mixed-radix index j.
In B_2 indices i+4*j mean u_1^i*u_2^j. Binary matrices are lists of row integers.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import time

ROOT = Path(__file__).resolve().parents[1]

def rank(rows):
    piv = {}
    for row in rows:
        while row:
            j = row.bit_length() - 1
            if j not in piv:
                piv[j] = row
                break
            row ^= piv[j]
    return len(piv)

def transpose(rows, columns):
    return [sum(((row >> j) & 1) << i for i, row in enumerate(rows))
            for j in range(columns)]

def compose(left, right):
    out = []
    for row in left:
        acc = 0
        for j, rrow in enumerate(right):
            if row >> j & 1:
                acc ^= rrow
        out.append(acc)
    return out

class Ring:
    def __init__(self, depths):
        self.depths = tuple(depths)
        self.dim = 1
        for d in depths:
            self.dim *= d
        self.exps = []
        for index in range(self.dim):
            exp = []
            for d in depths:
                exp.append(index % d)
                index //= d
            self.exps.append(tuple(exp))
        self.monomial_products = {}
        for i, a in enumerate(self.exps):
            for j, b in enumerate(self.exps):
                c = tuple(x+y for x,y in zip(a,b))
                self.monomial_products[i,j] = (1 << self.exps.index(c)) if all(x<d for x,d in zip(c,depths)) else 0

    @lru_cache(maxsize=None)
    def mul(self, a, b):
        out = 0
        for i in range(self.dim):
            if a >> i & 1:
                for j in range(self.dim):
                    if b >> j & 1:
                        out ^= self.monomial_products[i,j]
        return out

    @lru_cache(maxsize=None)
    def reg(self, a):
        return tuple(transpose([self.mul(a,1 << j) for j in range(self.dim)],self.dim))

    def binary(self, matrix, phi=False):
        out = []
        d = self.dim
        for mrow in matrix:
            blocks = [self.reg(a) for a in mrow]
            for i in range(d):
                row = 0
                for j, block in enumerate(blocks):
                    bits = block[i]
                    if phi:
                        bits = sum(((bits >> q) & 1) << (d-1-q) for q in range(d))
                    row |= bits << (j*d)
                out.append(row)
        return out

    def mm(self, a, b):
        out = []
        for row in a:
            line = []
            for j in range(len(b[0])):
                val = 0
                for k in range(len(b)):
                    val ^= self.mul(row[k], b[k][j])
                line.append(val)
            out.append(line)
        return out

    def inverse_unit(self, a):
        assert a & 1
        # Geometric series, since every positive-degree element is nilpotent.
        n, term, acc = a ^ 1, 1, 1
        for _ in range(sum(d-1 for d in self.depths)+1):
            term = self.mul(term,n)
            acc ^= term
        assert self.mul(a,acc) == 1
        return acc

def diagonal(values):
    return [[v if i==j else 0 for j in range(len(values))] for i,v in enumerate(values)]

def residue_rank(m):
    return rank(sum((v&1) << j for j,v in enumerate(row)) for row in m)

def smith2(ring, entries):
    val = lambda x: (x & -x).bit_length()-1 if x else 4
    a = min(map(val,entries))
    if a == 4:
        return (4,4)
    m = [list(entries[:2]),list(entries[2:])]
    i,j = next((i,j) for i in range(2) for j in range(2) if val(m[i][j])==a)
    m[0],m[i] = m[i],m[0]
    for row in m:
        row[0],row[j] = row[j],row[0]
    q = next(q for q in range(16) if ring.mul(q,m[0][0])==m[1][0])
    return a,val(m[1][1] ^ ring.mul(q,m[0][1]))

def check_free_extraction(ring, alphabet):
    cases = 0
    unit_minor_witnesses = 0
    for entries in product(alphabet, repeat=4):
        m = [list(entries[:2]),list(entries[2:])]
        r = residue_rank(m)
        socle = 1 << (ring.dim-1)
        s = [[ring.mul(socle,a) for a in row] for row in m]
        assert rank(ring.binary(s)) == r
        if r >= 1:
            i,j = next((i,j) for i in range(2) for j in range(2) if m[i][j]&1)
            l = [[ring.inverse_unit(m[i][j]) if k==i else 0 for k in range(2)]]
            q = [[1 if k==j else 0] for k in range(2)]
            assert ring.mm(ring.mm(l,m),q) == [[1]]
            unit_minor_witnesses += 1
        if r == 2:
            a,b,c,d = entries
            invdet = ring.inverse_unit(ring.mul(a,d)^ring.mul(b,c))
            inverse = [[ring.mul(invdet,d),ring.mul(invdet,b)],
                       [ring.mul(invdet,c),ring.mul(invdet,a)]]
            assert ring.mm(inverse,m) == [[1,0],[0,1]]
            unit_minor_witnesses += 1
        cases += 1
    return {'matrices':cases,'explicit_nonzero_free_targets':unit_minor_witnesses}

def phase_disposal_witness():
    a, b = Ring((4,)), Ring((4,4))
    # Logical input order (0,0),(0,1),(1,0),(1,1).
    m = diagonal([1,1<<8,1<<2,1<<10])
    l = [[1,0,0,0],[1<<4,0,0,0]]
    q = [[1<<12,0,0,0],[1<<8,0,0,0]]
    qt = [list(row) for row in zip(*q)]
    after = b.mm(b.mm(l,m),qt)
    assert after == [[1<<12,1<<8],[0,1<<12]]
    x = b.binary(m,phi=True)
    filtered = compose(compose(b.binary(l),x),transpose(b.binary(q),64))
    assert filtered == b.binary(after,phi=True)
    # Both parties apply id_(logical,A1) tensor coefficient[u2^3].
    disposal = [1 << (logical*16 + i + 12) for logical in range(2) for i in range(4)]
    out = compose(compose(disposal,filtered),transpose(disposal,32))
    target = a.binary([[1,0],[0,1]],phi=True)
    assert out == target and rank(out)==8
    # Full unresolved phase disposal instead joins all 16 coefficient branches.
    branches = []
    for p,r in product(range(4),repeat=2):
        dp = [1 << (logical*16+i+4*p) for logical in range(2) for i in range(4)]
        dr = [1 << (logical*16+i+4*r) for logical in range(2) for i in range(4)]
        y = compose(compose(dp,filtered),transpose(dr,32))
        branches.append(sum(row << (8*i) for i,row in enumerate(y)))
    mixed_dim = rank(branches)
    assert mixed_dim > 1
    # Intertwining the retained register; failure for the disposed register.
    full_l = compose(disposal,b.binary(l))
    in_u1 = b.binary(diagonal([2]*4))
    out_u1 = a.binary(diagonal([2]*2))
    assert compose(full_l,in_u1)==compose(out_u1,full_l)
    in_u2 = b.binary(diagonal([1<<4]*4))
    assert any(compose(full_l,in_u2))  # Not linear to the quotient u2=0 action.
    return {'input_B2_matrix':m,'Alice_B2_filter':l,'Bob_B2_filter':q,
            'filtered_B2_matrix':after,'selected_disposal_binary_rows':disposal,
            'target_binary_rows':target,'actual_output_binary_rows':out,
            'binary_ranks':{'input':rank(x),'before_disposal':rank(filtered),'output':rank(out)},
            'unobserved_disposal_state_subspace_dimension':mixed_dim,
            'all_disposal_branch_vectors':branches,
            'retained_A1_intertwining':True,'quotient_u2_intertwining':False}

def run():
    started = time.time()
    a = Ring((4,))
    types = tuple((x,y) for x in range(5) for y in range(x,5))
    lookup = {}
    for entries in product(range(16),repeat=4):
        t = smith2(a,entries)
        m = [list(entries[:2]),list(entries[2:])]
        profiles = tuple(rank(a.binary([[a.mul(1<<j,x) for x in row] for row in m])) for j in range(4))
        assert profiles == tuple(sum(max(4-x-j,0) for x in t) for j in range(4))
        lookup[entries] = t
    # Every filter on both sides of every 2-by-2 Smith representative.
    checked = 0
    for s in types:
        ds = [1<<x if x<4 else 0 for x in s]
        observed_left,observed_right = set(),set()
        for entries in lookup:
            left = tuple(a.mul(x,ds[j%2]) for j,x in enumerate(entries))
            right = tuple(a.mul(ds[j//2],x) for j,x in enumerate(entries))
            observed_left.add(lookup[left])
            observed_right.add(lookup[right])
            checked += 2
        expected = {t for t in types if all(y>=x for x,y in zip(s,t))}
        assert observed_left == expected == observed_right
    # Profile inequalities are strictly weaker than the actual filter preorder.
    source,target = (0,2),(1,1)
    rho = lambda t:[sum(max(4-x-j,0) for x in t) for j in range(4)]
    assert all(y<=x for x,y in zip(rho(source),rho(target)))
    assert not all(y>=x for x,y in zip(source,target))
    # Larger-size combinatorial equivalence of complete counts and component order.
    profiles = list(product(range(5),repeat=3))
    profiles = sorted(set(tuple(sorted(t)) for t in profiles))
    order_pairs = 0
    for s,t in product(profiles,repeat=2):
        component = all(y>=x for x,y in zip(s,t))
        counts = all(sum(x<j for x in t)<=sum(x<j for x in s) for j in range(1,5))
        assert component == counts
        order_pairs += 1
    small = check_free_extraction(Ring((2,2)),range(16))
    alphabet = (0,1,2,16,18,32,32768,32769)
    actual = check_free_extraction(Ring((4,4)),alphabet)
    witness = phase_disposal_witness()
    result = {'status':'PASS','python':platform.python_version(),'platform':platform.platform(),
              'A_2x2_matrix_classifications':len(lookup),'one_sided_filter_checks_both_sides':checked,
              'three_entry_order_comparisons':order_pairs,
              'small_nonchain_ring':{'depths':[2,2],'alphabet':list(range(16)),**small},
              'actual_B2_sample':{'depths':[4,4],'alphabet':alphabet,**actual},
              'incomplete_profile_counterexample':{'source':source,'target':target,'source_rho':rho(source),'target_rho':rho(target)},
              'phase_disposal_witness':witness,
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'seconds':round(time.time()-started,3),'randomness':'none'}
    (ROOT/'data').mkdir(exist_ok=True,parents=True)
    (ROOT/'data'/'review_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    run()
