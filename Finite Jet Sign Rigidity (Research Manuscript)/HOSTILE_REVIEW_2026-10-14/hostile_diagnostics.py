"""Independent finite falsification checks for Section 7; no third-party modules.

These checks supplement, and do not certify, the continuous proofs.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
MS = Path(r"C:\Users\brian\Documents\Math Latex etc\Papers for Publication\Finite Jet Sign Rigidity (Research Manuscript)\REVISED_PACKAGE_2026-10-13\MANUSCRIPT")
results = {"scope": "finite falsification checks, not proof certification", "checks": {}}

def check_faces(n):
    vertices = range(1 << n)
    affine = {sum(((b ^ ((mask & x).bit_count() % 2)) << x) for x in vertices)
              for b in (0, 1) for mask in vertices}
    faces = []
    for i, j in combinations(range(n), 2):
        for x in vertices:
            if not (x & ((1 << i) | (1 << j))):
                faces.append((x, x | (1 << i), x | (1 << j), x | (1 << i) | (1 << j)))
    witnesses = 0
    for law in range(1 << (1 << n)):
        has_face = any(sum((law >> x) & 1 for x in f) % 2 for f in faces)
        assert has_face == (law not in affine), (n, law)
        witnesses += has_face
    return {"all_laws": 1 << (1 << n), "affine": len(affine), "non_affine_with_face": witnesses}

results["checks"]["non_affine_face_reduction"] = {str(n): check_faces(n) for n in (1, 2, 3, 4)}

and_orbit = set()
for a, b, c in product((0, 1), repeat=3):
    and_orbit.add(sum(((((x & 1) ^ a) & (((x >> 1) & 1) ^ b)) ^ c) << x for x in range(4)))
assert len(and_orbit) == 8
assert and_orbit == {law for law in range(16) if law.bit_count() % 2}
results["checks"]["binary_AND_orbit"] = {"orbit_size": len(and_orbit), "exact_non_affine_laws": True}

def aq(t, m, L):
    p = Q(1)
    pm = Q(1)
    for j in range(m + 1):
        u = Q(1, 2 ** j)
        p *= (t + u) ** (2 * L)
        pm *= (u - t) ** (2 * L)
    return p - pm, p + pm

univariate_checks = 0
for m in range(1, 10):
    delta = Q(1, 2 ** m)
    for L in (1, 2, 3):
        samples = {delta, Q(1)} | {Q(1, 2 ** j) for j in range(m + 1)} | {Q(3, 2 ** (j + 1)) for j in range(1, m + 1)}
        for t in samples:
            a, q = aq(t, m, L)
            an, qn = aq(-t, m, L)
            assert q > 0 and qn == q and an == -a
            assert Q(0) <= 1 - a / q <= Q(2, 3 ** (2 * L))
            univariate_checks += 1
        for t in (Q(0), delta / 7, -delta / 7, Q(2), Q(-2)):
            a, q = aq(t, m, L)
            assert q > 0 and abs(a) <= q
            univariate_checks += 1
results["checks"]["dyadic_rational"] = {"exact_rational_cases": univariate_checks}

binary_checks = 0
for m in (1, 3, 6):
    delta = Q(1, 2 ** m)
    positive = {delta, (1 + delta) / 2, Q(1)}
    samples = sorted(positive | {-v for v in positive})
    for x, y in product(samples, repeat=2):
        ax, qx = aq(x, m, 1)
        ay, qy = aq(y, m, 1)
        for law in range(16):
            # Clear denominators directly, without floating-point polynomial expansion.
            value = sum((2 * ((law >> i) & 1) - 1) * (qx + sx * ax) * (qy + sy * ay) / 4
                        for i, (sx, sy) in enumerate(product((-1, 1), repeat=2)))
            index = 2 * (x > 0) + (y > 0)
            target = 2 * ((law >> index) & 1) - 1
            assert target * value > 0, (m, x, y, law)
            assert target * value / (qx * qy) >= Q(1) - Q(4, 9)
            binary_checks += 1
results["checks"]["denominator_clearing_all_binary_laws"] = {"exact_cases": binary_checks}

normalized_corner = {}
for m in (1, 2, 4, 8):
    delta = Q(1, 2 ** m)
    a, q = aq(delta, m, 1)
    a1, q1 = aq(Q(1), m, 1)
    assert a == q and a1 == q1
    ratio = (q / q1) ** 2
    # q has nonnegative even coefficients; |H_h| <= 1 and |H_h|=1 at vertices.
    # Thus q(1)^2 is the exact whole-square norm of the cleared binary polynomial.
    normalized_corner[str(delta)] = {"exact_fraction": str(ratio), "approx": float(ratio)}
results["checks"]["normalization_distinguishes_resources"] = normalized_corner

hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in MS.iterdir() if p.suffix in (".tex", ".pdf")}
results["manuscript_sha256"] = hashes
results["status"] = "PASS"
(OUT / "HOSTILE_DIAGNOSTICS.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
