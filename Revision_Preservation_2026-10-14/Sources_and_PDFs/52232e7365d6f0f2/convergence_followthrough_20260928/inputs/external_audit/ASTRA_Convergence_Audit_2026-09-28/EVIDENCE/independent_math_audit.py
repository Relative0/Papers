#!/usr/bin/env python3
"""Independent finite audit, using only the Python standard library.
No project code or submitted verification code is imported.
Truth bit x is f(x); coordinate j is bit j of x (LSB-first coordinate names).
Matrix cuts use the high p bits for rows and low q bits for columns.
Run: python independent_math_audit.py --output independent_math_results.json
Finite checks supplement, rather than prove, the general theorems.
"""
from __future__ import annotations
import argparse, itertools, json, math, platform, time
from collections import Counter
from pathlib import Path


def query_masks(n: int, k: int, exact: bool = True):
    out = []
    for t in ([k] if exact else range(k + 1)):
        for S in itertools.combinations(range(n), t):
            sm = sum(1 << j for j in S)
            for a in range(1 << t):
                value = sum(((a >> i) & 1) << j for i, j in enumerate(S))
                mask = sum(1 << x for x in range(1 << n) if x & sm == value)
                out.append((S, value, mask))
    return out


def sig(f: int, masks) -> bytes:
    return bytes((f & m).bit_count() for _, _, m in masks)


def exact_integer_rank(rows):
    basis = {}
    for row in rows:
        v = list(row)
        for p, b in sorted(basis.items()):
            if v[p]:
                a, c = v[p], b[p]
                v = [c * x - a * y for x, y in zip(v, b)]
                g = math.gcd(*v)
                if g > 1:
                    v = [x // g for x in v]
        p = next((j for j, x in enumerate(v) if x), None)
        if p is not None:
            if v[p] < 0:
                v = [-x for x in v]
            basis[p] = v
    return len(basis)


def gf2_basis(rows):
    basis = {}
    for r in rows:
        v = r
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return [basis[p] for p in sorted(basis, reverse=True)]


def matrix_rows(f: int, p: int, q: int):
    c = 1 << q
    return [(f >> (i*c)) & ((1 << c) - 1) for i in range(1 << p)]


def walsh(f: int, n: int):
    v = [(f >> x) & 1 for x in range(1 << n)]
    step = 1
    while step < len(v):
        for start in range(0, len(v), 2*step):
            for j in range(start, start+step):
                a, b = v[j], v[j+step]
                v[j], v[j+step] = a+b, a-b
        step *= 2
    return v


def parity(n: int, constant: int = 0):
    return sum(1 << x for x in range(1 << n) if (x.bit_count() & 1) ^ constant)


def rectangles(p: int, q: int):
    r, c = 1 << p, 1 << q
    yield 0
    for u in range(1, 1 << r):
        for v in range(1, 1 << c):
            yield sum(v << (i*c) for i in range(r) if (u >> i) & 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=Path('independent_math_results.json'))
    args = ap.parse_args()
    started = time.perf_counter()
    result = {'python': platform.python_version(), 'coordinate_convention': __doc__, 'tests': {}}
    ranks = []
    for n in range(7):
        for k in range(n+1):
            want = sum(math.comb(n, j) for j in range(k+1))
            got = []
            for exact in (False, True):
                rows = [[(m >> x) & 1 for x in range(1 << n)] for _, _, m in query_masks(n, k, exact)]
                got.append(exact_integer_rank(rows))
            assert got == [want, want], (n, k, got, want)
            ranks.append({'n': n, 'k': k, 'rank_at_most': got[0], 'rank_exactly': got[1]})
    result['tests']['rational_operator_ranks'] = ranks
    print('Exact operator ranks PASS', flush=True)

    fibres = []
    for n in range(5):
        masks = [query_masks(n, k) for k in range(n+1)]
        forward = [dict() for _ in masks]
        backward = [dict() for _ in masks]
        for f in range(1 << (1 << n)):
            w = walsh(f, n)
            for k in range(n+1):
                qs = sig(f, masks[k])
                ws = tuple(w[t] for t in range(1 << n) if t.bit_count() <= k)
                assert forward[k].setdefault(qs, ws) == ws
                assert backward[k].setdefault(ws, qs) == qs
                if n <= 3:
                    for S, a, m in masks[k]:
                        sm = sum(1 << j for j in S)
                        total = sum((-1 if (a & t).bit_count() & 1 else 1) * w[t]
                                    for t in range(1 << n) if t & ~sm == 0)
                        assert total == (1 << k) * (f & m).bit_count()
        fibres.extend({'n': n, 'k': k, 'functions': 1 << (1 << n), 'fibres': len(forward[k])} for k in range(n+1))
    result['tests']['all_boolean_fourier_fibres'] = fibres
    print('All Boolean fibres through n=4 PASS', flush=True)

    threshold_rows = []
    for p, q in [(1, 1), (1, 2), (2, 1), (1, 3), (2, 2), (3, 1)]:
        n = p + q
        masks = [query_masks(n, k) for k in range(n+1)]
        classes = {1: [], 2: []}
        distribution = Counter()
        for f in range(1 << (1 << n)):
            rank = len(gf2_basis(matrix_rows(f, p, q)))
            distribution[rank] += 1
            for bound in classes:
                if rank <= bound:
                    classes[bound].append(f)
        for bound, fs in classes.items():
            unique = [len({sig(f, mm) for f in fs}) for mm in masks]
            threshold = next(k for k, v in enumerate(unique) if v == len(fs))
            want = max(p, q) if bound == 1 else n
            assert threshold == want
            threshold_rows.append({'p': p, 'q': q, 'rank_bound': bound, 'class_size': len(fs),
                                   'fibre_counts_by_k': unique, 'threshold': threshold,
                                   'rank_distribution_full_space': dict(distribution)})
    for p, q in [(2, 3), (3, 3)]:
        n, k = p+q, max(p, q)
        fs = list(rectangles(p, q))
        assert len(fs) == len(set(fs)) == 1+((1 << (1 << p))-1)*((1 << (1 << q))-1)
        sizes = []
        for j in (k-1, k):
            mm = query_masks(n, j)
            sizes.append(len({sig(f, mm) for f in fs}))
        assert sizes[0] < len(fs) == sizes[1]
        threshold_rows.append({'p': p, 'q': q, 'rank_bound': 1, 'class_size': len(fs),
                               'tested_depths': [k-1, k], 'fibre_counts': sizes, 'threshold': k})
    result['tests']['rank_thresholds'] = threshold_rows
    print('Direct rank-class thresholds PASS', flush=True)

    # All 4x4 Boolean matrices of rank <=2, every named-coordinate restriction.
    n, p, q = 4, 2, 2
    all_masks = query_masks(n, n, exact=False)
    checks = 0
    matrices = 0
    for f in range(1 << 16):
        rows = matrix_rows(f, p, q)
        W = gf2_basis(rows)
        if len(W) > 2:
            continue
        matrices += 1
        r = len(W)
        U = []
        for row in rows:
            coeff, residual = 0, row
            for j, b in enumerate(W):
                if residual & (1 << (b.bit_length()-1)):
                    residual ^= b
                    coeff |= 1 << j
            assert residual == 0
            U.append(coeff)
        V = [sum(((b >> col) & 1) << j for j, b in enumerate(W)) for col in range(4)]
        for S, a, m in all_masks:
            sm = sum(1 << j for j in S)
            ri = [x for x in range(4) if ((x << q) & sm) == (a & (12))]
            ci = [y for y in range(4) if (y & sm) == (a & 3)]
            alpha = Counter(U[x] for x in ri)
            beta = Counter(V[y] for y in ci)
            signed = sum(aa*bb*(-1 if (u & v).bit_count() & 1 else 1)
                         for u, aa in alpha.items() for v, bb in beta.items())
            numerator = len(ri)*len(ci)-signed
            assert numerator % 2 == 0
            assert numerator//2 == (f & m).bit_count()
            checks += 1
    assert matrices == 7576 and checks == 613656
    result['tests']['conditioned_rank_profiles'] = {'matrices': matrices, 'all_restrictions_per_matrix': 81,
                                                  'checks': checks, 'rank_bound': 2, 'shape': [4, 4]}
    print('All low-rank 4x4 conditioned profiles PASS', flush=True)

    counterexamples = []
    for n in range(2, 11):
        f, g = parity(n), parity(n, 1)
        mm = query_masks(n, n-1)
        assert sig(f, mm) == sig(g, mm)
        # Restrict highest coordinate to zero: remaining truth is lower half.
        cut = (1 << (1 << (n-1))) - 1
        rf, rg = f & cut, g & cut
        assert sig(rf, query_masks(n-1, n-1)) != sig(rg, query_masks(n-1, n-1))
        p, q = n//2, n-n//2
        assert len(gf2_basis(matrix_rows(f, p, q))) == len(gf2_basis(matrix_rows(g, p, q))) == 2
        counterexamples.append({'n': n, 'f_hex': hex(f), 'g_hex': hex(g), 'same_Q_n_minus_1': True,
                                'residual_full_Q_n_minus_1_differs': True, 'gf2_rank_both': 2,
                                'one_bit_distinguishes_in_two_element_class': True})
    result['tests']['parity_semantic_counterexamples'] = counterexamples
    result['status'] = 'PASS'
    result['elapsed_seconds'] = time.perf_counter()-started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('ALL PASS', result['elapsed_seconds'], flush=True)


if __name__ == '__main__':
    main()
