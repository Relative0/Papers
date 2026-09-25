"""Verification for ProLT Observation Refinement Classification v0.2.

Small finite-poset/order-complex computations over F_2.
The code is intentionally dependency-light and independently checks the worked examples.
"""
from itertools import combinations, product
from collections import defaultdict


def rank_mod2(rows):
    A = [list(map(int, r)) for r in rows]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    r = c = 0
    while r < m and c < n:
        piv = next((i for i in range(r, m) if A[i][c] & 1), None)
        if piv is None:
            c += 1
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(m):
            if i != r and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[r])]
        r += 1
        c += 1
    return r


def leq(a, b):
    if isinstance(a, tuple):
        return a[0] <= b[0] and a[1] <= b[1]
    return a <= b


def strict(a, b):
    return a != b and leq(a, b)


def chains(P):
    P = list(P)
    out = {0: [(p,) for p in P]}
    for k in range(2, len(P) + 1):
        vals = []
        for sub in combinations(P, k):
            def key(x):
                return (len(x[0]), x[1]) if isinstance(x, tuple) else (len(x),)
            s = tuple(sorted(sub, key=key))
            if all(strict(s[i], s[i + 1]) for i in range(k - 1)):
                vals.append(s)
        if vals:
            out[k - 1] = vals
    return out


def boundary_matrix(ch, k):
    rows = ch.get(k - 1, [])
    cols = ch.get(k, [])
    rid = {s: i for i, s in enumerate(rows)}
    M = [[0] * len(cols) for _ in rows]
    if k == 0:
        return M
    for j, s in enumerate(cols):
        for i in range(len(s)):
            f = s[:i] + s[i + 1:]
            M[rid[f]][j] ^= 1
    return M


def betti(P):
    ch = chains(P)
    md = max(ch) if ch else -1
    br = {0: 0, md + 1: 0}
    for k in range(1, md + 1):
        br[k] = rank_mod2(boundary_matrix(ch, k))
    return tuple(len(ch.get(k, [])) - br.get(k, 0) - br.get(k + 1, 0)
                 for k in range(md + 1))


def beat_core(P):
    P = set(P)
    changed = True
    while changed and len(P) > 1:
        changed = False
        for x in list(P):
            lower = [y for y in P if y != x and leq(y, x)]
            upper = [y for y in P if y != x and leq(x, y)]
            if upper:
                mins = [u for u in upper if all(not (v != u and leq(v, u)) for v in upper)]
                if len(mins) == 1 and all(leq(mins[0], u) for u in upper):
                    P.remove(x); changed = True; break
            if lower:
                maxs = [l for l in lower if all(not (v != l and leq(l, v)) for v in lower)]
                if len(maxs) == 1 and all(leq(l, maxs[0]) for l in lower):
                    P.remove(x); changed = True; break
    return P


def beat_contractible(P):
    return len(beat_core(P)) == 1


def Q_from(P, assignment):
    return [(p, b) for p, B in zip(P, assignment) for b in B]


def lower_fiber(Q, p):
    return [x for x in Q if x[0] <= p]


def upper_fiber(Q, p):
    return [x for x in Q if p <= x[0]]


def lower_quillen(P, Q):
    return all(beat_contractible(lower_fiber(Q, p)) for p in P)


def upper_quillen(P, Q):
    return all(beat_contractible(upper_fiber(Q, p)) for p in P)


def min_section(P, assignment):
    b = {p: min(B) for p, B in zip(P, assignment)}
    return all(not strict(p, q) or b[p] <= b[q] for p in P for q in P)


def max_section(P, assignment):
    b = {p: max(B) for p, B in zip(P, assignment)}
    return all(not strict(p, q) or b[p] <= b[q] for p in P for q in P)


def redundant(P, assignment):
    if any(len(B) != 1 for B in assignment):
        return False
    b = {p: B[0] for p, B in zip(P, assignment)}
    return all(not strict(p, q) or b[p] <= b[q] for p in P for q in P)


def acyclic_lower(P, Q):
    for p in P:
        B = betti(lower_fiber(Q, p))
        if not B or B[0] != 1 or any(B[1:]):
            return False
    return True


def chain_map_matrix(P, Q, k):
    chQ = chains(Q); chP = chains(P)
    dom = chQ.get(k, []); cod = chP.get(k, [])
    rid = {s: i for i, s in enumerate(cod)}
    M = [[0] * len(dom) for _ in cod]
    for j, s in enumerate(dom):
        img = tuple(x[0] for x in s)
        if len(set(img)) < len(img):
            continue
        if img not in rid:
            img = tuple(sorted(img, key=len))
        M[rid[img]][j] ^= 1
    return M


def cone_betti(P, Q):
    chP = chains(P); chQ = chains(Q)
    md = max(max(chP, default=-1), max(chQ, default=-1) + 1)
    dims = {n: len(chP.get(n, [])) + len(chQ.get(n - 1, [])) for n in range(md + 1)}
    ranks = {0: 0, md + 1: 0}
    for n in range(1, md + 1):
        Pn = chP.get(n, []); Qn1 = chQ.get(n - 1, [])
        Pn1 = chP.get(n - 1, []); Qn2 = chQ.get(n - 2, [])
        M = [[0] * (len(Pn) + len(Qn1)) for _ in range(len(Pn1) + len(Qn2))]
        dP = boundary_matrix(chP, n)
        for i in range(len(Pn1)):
            for j in range(len(Pn)):
                M[i][j] = dP[i][j]
        f = chain_map_matrix(P, Q, n - 1)
        for i in range(len(Pn1)):
            for j in range(len(Qn1)):
                M[i][len(Pn) + j] = f[i][j]
        if n - 1 >= 1:
            dQ = boundary_matrix(chQ, n - 1)
            for i in range(len(Qn2)):
                for j in range(len(Qn1)):
                    M[len(Pn1) + i][len(Pn) + j] = dQ[i][j]
        ranks[n] = rank_mod2(M)
    return tuple(dims[n] - ranks.get(n, 0) - ranks.get(n + 1, 0) for n in range(md + 1))


def fs(*xs):
    return frozenset(xs)


def report(name, P, assignment):
    Q = Q_from(P, assignment)
    out = {
        "coarse_betti": betti(P),
        "fine_betti": betti(Q),
        "cone_betti": cone_betti(P, Q),
        "redundant": redundant(P, assignment),
        "left_adjoint": min_section(P, assignment),
        "right_adjoint": max_section(P, assignment),
        "lower_quillen": lower_quillen(P, Q),
        "upper_quillen": upper_quillen(P, Q),
    }
    print(name, out)
    return out


def main():
    diamond = [fs(), fs("X"), fs("Y"), fs("X", "Y")]
    r1 = report("redundant AND", diamond, [(0,), (0,), (0,), (1,)])
    assert r1["redundant"] and all(x == 0 for x in r1["cone_betti"])

    r2 = report("XOR: Quillen but no adjoint", diamond, [(0,), (1,), (1,), (0,)])
    assert (not r2["redundant"] and not r2["left_adjoint"] and not r2["right_adjoint"]
            and r2["lower_quillen"] and all(x == 0 for x in r2["cone_betti"]))

    edge = [fs(), fs("X")]
    r3 = report("negation split", edge, [(1,), (0,)])
    assert r3["fine_betti"][0] == 2 and r3["cone_betti"][1] == 1

    r4 = report("splitting but adjoint-neutral", edge, [(0, 1), (0, 1)])
    assert r4["left_adjoint"] and r4["right_adjoint"] and all(x == 0 for x in r4["cone_betti"])

    chain4 = [fs(), fs(0), fs(0, 1), fs(0, 1, 2)]
    r5 = report("alternating 4-chain", chain4, [(1,), (0,), (1,), (0,)])
    assert beat_contractible(chain4)
    Q5 = Q_from(chain4, [(1,), (0,), (1,), (0,)])
    assert beat_contractible(Q5)
    assert not r5["lower_quillen"] and not r5["upper_quillen"]
    assert all(x == 0 for x in r5["cone_betti"])

    # Exhaust all one-bit profiles over nonempty subposets of B2.
    fibers = [(0,), (1,), (0, 1)]
    counts = defaultdict(int)
    for sz in range(1, 5):
        for Psub_t in combinations(diamond, sz):
            Psub = list(Psub_t)
            for assignment in product(fibers, repeat=sz):
                Q = Q_from(Psub, assignment)
                key = (
                    redundant(Psub, assignment),
                    min_section(Psub, assignment) or max_section(Psub, assignment),
                    lower_quillen(Psub, Q),
                    acyclic_lower(Psub, Q),
                    all(x == 0 for x in cone_betti(Psub, Q)),
                )
                counts[key] += 1
    assert sum(counts.values()) == 255
    expected = {
        (False, False, False, False, False): 24,
        (False, False, False, False, True): 16,
        (False, False, True, True, True): 20,
        (False, True, True, True, True): 144,
        (True, True, True, True, True): 51,
    }
    assert dict(counts) == expected
    print("B2 exhaustive profile counts:")
    for k, v in sorted(counts.items()):
        print(k, v)
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
