"""Small exact-rational diagnostics, not proof or historical-priority checks.

Run with any Python 3.10+ interpreter. All writes stay beside this file.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial, lgamma, log, log1p, exp, sqrt
from pathlib import Path
import json
import hashlib
import sys

OUT = Path(__file__).resolve().parent
counts = {'exact_rational_assertions': 0, 'floating_assertions': 0}

def check(condition, floating=False):
    assert condition
    counts['floating_assertions' if floating else 'exact_rational_assertions'] += 1

def sign(x):
    return (x > 0) - (x < 0)

def extension(table, corners, x):
    return sum(label * product_q((1 + s*t)/2 for s, t in zip(corner, x))
               for corner, label in zip(corners, table))

def product_q(values):
    value = Q(1)
    for x in values:
        value *= x
    return value

def affine_tables(n):
    corners = list(product((-1, 1), repeat=n))
    return {tuple(c * product_q(s for s, e in zip(corner, exponents) if e)
                  for corner in corners)
            for c in (-1, 1) for exponents in product((0, 1), repeat=n)}

def poly_mul(p, q):
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return r

def poly_eval(p, x):
    value = Q(0)
    for a in reversed(p):
        value = value*x + a
    return value

def rational_nodes(m):
    # Two copies of each dyadic scale: a Newman-style construction.
    p = [Q(1)]
    for j in range(m+1):
        a = Q(1, 2**j)
        p = poly_mul(p, [a*a, 2*a, Q(1)])
    a = [v * (1 - (-1)**i) for i, v in enumerate(p)]
    q = [v * (1 + (-1)**i) for i, v in enumerate(p)]
    return a, q

def main():
    # Every truth table admits exact finite-corner polynomial fitting.
    for n in (2, 3):
        corners = list(product((-1, 1), repeat=n))
        affine = affine_tables(n)
        check(len(affine) == 2**(n+1))
        for table in product((-1, 1), repeat=2**n):
            for x, label in zip(corners, table):
                check(extension(table, corners, tuple(map(Q, x))) == label)
            # A non-affine law has a non-affine two-dimensional face.
            non_affine_face = False
            for i in range(n):
                for j in range(i+1, n):
                    fixed = [k for k in range(n) if k not in (i, j)]
                    for values in product((-1, 1), repeat=len(fixed)):
                        face = []
                        for u, v in product((-1, 1), repeat=2):
                            x = [0]*n
                            x[i], x[j] = u, v
                            for k, value in zip(fixed, values):
                                x[k] = value
                            face.append(table[corners.index(tuple(x))])
                        non_affine_face |= tuple(face) not in affine_tables(2)
            check(non_affine_face == (table not in affine))

    # All eight non-affine binary tables are AND with input/output flips.
    corners = list(product((-1, 1), repeat=2))
    orbit = {tuple(c*(1 if a*x > 0 and b*y > 0 else -1) for x,y in corners)
             for a,b,c in product((-1,1), repeat=3)}
    check(len(orbit) == 8)
    check(orbit.isdisjoint(affine_tables(2)))

    # Exact dyadic rational construction, polynomial after clearing denominators.
    rows = []
    for m in range(1, 7):
        delta = Q(1, 2**m)
        a, q = rational_nodes(m)
        check(all(c >= 0 for c in q))
        check(q[0] > 0)
        magnitudes = [delta + (1-delta)*Q(i, 16) for i in range(17)]
        samples = [-t for t in magnitudes] + magnitudes
        cache = {x: (poly_eval(a,x), poly_eval(q,x)) for x in samples}
        for x, (ax,qx) in cache.items():
            check(qx > 0)
            check(abs(ax/qx - sign(x)) <= Q(1,5))
            check(abs(ax) <= qx)
        q1 = poly_eval(q, Q(1))
        qd = poly_eval(q, delta)
        norm = 3*q1*q1
        margin_bound = Q(1,5)*(qd/q1)**2
        for x,y in product(samples, repeat=2):
            ax,qx = cache[x]
            ay,qy = cache[y]
            p = ax*qy + ay*qx - qx*qy
            expected = 1 if x > 0 and y > 0 else -1
            check(sign(p) == expected)
            check(abs(p) <= norm)
            check(expected*p/norm >= margin_bound)
        rows.append({'m':m, 'delta':str(delta), 'total_degree_upper':4*(m+1),
                     'certified_normalized_margin_lower':str(margin_bound),
                     'log10_margin_lower':(log(margin_bound.numerator)-log(margin_bound.denominator))/log(10),
                     'corner_normalized_margin':str((qd/q1)**2/3)})

    # Finite representatives do not imply uniform orthant signs.
    for t in [Q(1,2**k) for k in range(1,13)]:
        f = lambda x,y: x+y+x*y
        check(f(t,-t) < 0)
        check(f(2*t,-t/2) > 0)
        p = lambda x,y: (x+y+x*y-1)/2
        check(p(t,t) < 0 if t < Q(1,4) else True)
        # Analytic rounded R-conjunction, epsilon = delta = t.
        check(2*t*t > t*t)
        # Exact ReLU expression for min: one ReLU plus an affine skip.
        for x,y in product((-t,t), repeat=2):
            relu_min = x-max(Q(0),x-y)
            check(relu_min == min(x,y))
            check(sign(relu_min) == (1 if x>0 and y>0 else -1))

    float_rows = []
    for delta in (0.5,0.25,0.125,0.0625):
        beta = 2*log(2)/delta
        soft_min = lambda x,y: min(x,y)-log1p(exp(-beta*abs(x-y)))/beta
        for x,y in product((-delta,delta), repeat=2):
            value = soft_min(x,y)
            check(sign(value) == (1 if x>0 and y>0 else -1), True)
            check(abs(value) >= delta/2-1e-12, True)
        float_rows.append({'delta':delta,'beta':beta,'softmin_positive_margin':soft_min(delta,delta),
                           'rounded_R_positive_margin':(2-sqrt(3))*delta,
                           'flat_selector_log_abs_at_balanced_corner_n2':-2/(delta*delta),
                           'bounded_polynomial_degree_lower_gamma_half':0.5*sqrt(1-delta*delta)/delta})

    result = {'scope':'Finite rational identities and bounded diagnostic samples; no universal sign certificate from sampling.',
              'python':sys.version,'counts':counts,'rational_constructions':rows,'floating_illustrations':float_rows,
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'verification_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'counts':counts,'rational_margins':[{'delta':r['delta'],'degree':r['total_degree_upper'],
                                                       'log10_margin_lower':r['log10_margin_lower']} for r in rows]},indent=2))

if __name__ == '__main__':
    main()
