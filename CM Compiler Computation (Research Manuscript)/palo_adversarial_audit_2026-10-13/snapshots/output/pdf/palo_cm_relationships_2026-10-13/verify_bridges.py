"""Exact, bounded checks of elementary connections in the accompanying report."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
counts = {}


def check(kind, actual, expected=True):
    assert actual == expected, (kind, actual, expected)
    counts[kind] = counts.get(kind, 0) + 1


def bilinear(c, p, q):
    a, b, e, d = c
    return a*p*q + b*p*(1-q) + e*(1-p)*q + d*(1-p)*(1-q)


def joint(c, p, q, r):
    a, b, e, d = c
    return a*r + b*(p-r) + e*(q-r) + d*(1-p-q+r)


grid = [Q(i, 8) for i in range(9)]
tables = list(product((0, 1), repeat=4))
corners = [(1, 1), (1, 0), (0, 1), (0, 0)]
for c in tables:
    a, b, e, d = c
    for index, (p, q) in enumerate(corners):
        check('boolean_corners', bilinear(c, p, q), c[index])
    for p, q in product(grid, repeat=2):
        value = bilinear(c, p, q)
        check('probability_range', 0 <= value <= 1)
        check('transpose', value, bilinear((a, e, b, d), q, p))
        check('input_complement', value, bilinear((e, d, a, b), 1-p, q))
        check('output_complement', 1-value, bilinear(tuple(1-x for x in c), p, q))
        lo, hi = max(Q(0), p+q-1), min(p, q)
        endpoint_values = [joint(c, p, q, lo), joint(c, p, q, hi)]
        for t in grid:
            r = lo + t*(hi-lo)
            j = [r, p-r, q-r, 1-p-q+r]
            check('joint_feasibility', all(x >= 0 for x in j) and sum(j) == 1)
            exact = joint(c, p, q, r)
            check('covariance_correction', exact-value, (a-b-e+d)*(r-p*q))
            check('endpoint_bounds', min(endpoint_values) <= exact <= max(endpoint_values))

for p, q in product(grid, repeat=2):
    check('palo_and', bilinear((1, 0, 0, 0), p, q), p*q)
    check('palo_or', bilinear((1, 1, 1, 0), p, q), p+q-p*q)
    check('palo_implication', bilinear((1, 0, 1, 1), p, q), 1-p+p*q)
    check('palo_equivalence', bilinear((1, 0, 0, 1), p, q), 1-p-q+2*p*q)
    check('xor_extension', bilinear((0, 1, 1, 0), p, q), p+q-2*p*q)

p = Q(1, 2)
check('counterexample_repeat', p*p, Q(1, 4))
check('counterexample_repeat_disagrees', p*p != p)
check('counterexample_complement', p*(1-p), Q(1, 4))
check('counterexample_equivalence', (1-p+p*p)**2, Q(9, 16))
check('counterexample_equivalence_disagrees', (1-p+p*p)**2 != Q(1, 2))
p = q = Q(3, 5)
check('crispification_order', int(p*q >= Q(1, 2)), 0)
check('crispification_order', int(p >= Q(1, 2))*int(q >= Q(1, 2)), 1)

witnesses = [((Q(1, 2), Q(1, 2)), (1, 0, 0, 0)),
             ((Q(2), Q(1, 2)), (1, 1, 0, 0)),
             ((Q(1, 2), Q(2)), (1, 0, 1, 0)),
             ((Q(3), Q(3)), (1, 0, 0, 1))]
quartic_codes = [(0, 0), (1, 0), (0, 1), (1, 1)]
for ((a, b), expected), code in zip(witnesses, quartic_codes):
    scores = [a+b+a*b, a-b-a*b, -a+b-a*b, -a-b+a*b]
    check('guard_witness_nonzero', all(x != 0 for x in scores))
    check('guard_witness_table', tuple(int(x > 0) for x in scores), expected)
    _, h1, h2, h3 = scores
    check('guard_quartic_codes', (int(h1*h3 < 0), int(h2*h3 < 0)), code)
    u, v = 1/a, 1/b
    check('reciprocal_coordinates', [x/(a*b) for x in scores],
          [u+v+1, v-u-1, u-v-1, 1-u-v])

result = {
    'status': 'passed',
    'arithmetic': 'Python fractions.Fraction; exact rational arithmetic',
    'truth_tables': len(tables),
    'marginal_grid': '0, 1/8, ..., 1',
    'joint_interpolation_grid': '0, 1/8, ..., 1 between Frechet endpoints',
    'checks_by_family': counts,
    'total_assertions': sum(counts.values()),
    'scope': 'Elementary derived identities and examples only; not a LIME integration or source-paper proof audit',
}
(ROOT / 'verification_results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
