"""Bounded, independent checks; no claim of universal proof or priority.

Run with Python 3 from any directory. Writes only diagnostics.json beside this file.
Uses the standard library; source documents are read only.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import factorial, prod
from pathlib import Path
import json
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
CURRENT = ROOT / "REVISED_PACKAGE_2026-10-13/MANUSCRIPT/finite_jet_sign_laws_REVISED_2026-10-13.tex"
OLD = ROOT / "FINAL_REVIEWED_PACKAGE_2026-09-27/FINAL_SUBMISSION_PACKAGE/FINAL_MANUSCRIPT/finite_jet_sign_laws_FINAL_SUBMISSION.tex"
EXPECTED = {
    "tex": "a9bb9bce6ab7aee4db9af72cc2b292386c5dd8ad47ddcec3e5c957e99513d079",
    "pdf": "3e574c5fea708bf599d5bcc4bf1b70bddce4c36e824684763a6944145d569bd3",
}


def check_source():
    text = CURRENT.read_text(encoding="utf-8")
    old = OLD.read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text)
    bib = re.findall(r"\\bibitem\{([^}]+)\}", text)
    cites = [k.strip() for s in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", text) for k in s.split(",")]
    blocks = re.findall(r"\\begin\{(theorem|lemma|corollary|proof)\}.*?\\end\{\1\}", old, re.S)
    full_blocks = [m.group(0) for m in re.finditer(r"\\begin\{(theorem|lemma|corollary|proof)\}.*?\\end\{\1\}", old, re.S)]
    hashes = {ext: sha256(CURRENT.with_suffix("." + ext).read_bytes()).hexdigest() for ext in EXPECTED}
    assert hashes == EXPECTED, hashes
    assert all(b in text for b in full_blocks)
    assert not (set(refs) - set(labels))
    assert not (set(cites) - set(bib))
    assert not [k for k, v in Counter(labels).items() if v > 1]
    return {"hashes": hashes, "old_source_sha256": sha256(OLD.read_bytes()).hexdigest(),
            "old_proof_and_theorem_blocks_preserved_verbatim": len(blocks),
            "labels": len(labels), "bibliography_entries": len(bib),
            "missing_refs": sorted(set(refs) - set(labels)), "missing_cites": sorted(set(cites) - set(bib))}


def check_faces():
    counts = {}
    for n in range(1, 5):
        faces = [(b, b | (1 << i), b | (1 << j), b | (1 << i) | (1 << j))
                 for i in range(n) for j in range(i + 1, n)
                 for b in range(1 << n) if not (b & ((1 << i) | (1 << j)))]
        affine = 0
        for table in range(1 << (1 << n)):
            values = [(table >> j) & 1 for j in range(1 << n)]
            coefficients = values.copy()
            for i in range(n):
                for j in range(1 << n):
                    if j & (1 << i):
                        coefficients[j] ^= coefficients[j ^ (1 << i)]
            is_affine = all(not c or j.bit_count() <= 1 for j, c in enumerate(coefficients))
            bad_face = any(values[a] ^ values[b] ^ values[c] ^ values[d] for a, b, c, d in faces)
            assert is_affine == (not bad_face), (n, table)
            affine += is_affine
        assert affine == 2 ** (n + 1)
        counts[str(n)] = {"truth_tables": 1 << (1 << n), "affine": affine}
    # All eight non-affine binary tables are input/output flips of AND.
    orbits = set()
    for flip in range(4):
        for neg in range(2):
            orbits.add(sum((((int((j ^ flip) == 3)) ^ neg) << j) for j in range(4)))
    assert len(orbits) == 8
    assert all(sum((table >> j) & 1 for j in range(4)) in (1, 3) for table in orbits)
    return {"face_equivalence": counts, "binary_AND_orbit_size": len(orbits)}


def rational(t, nodes, L=1):
    p = prod((t + node) ** (2 * L) for node in nodes)
    pm = prod((-t + node) ** (2 * L) for node in nodes)
    q = p + pm
    assert q > 0
    return (p - pm) / q, p - pm, q


def check_rational():
    widths = [F(99, 100), F(3, 5), F(1, 2), F(3, 10), F(1, 16), F(1, 100), F(1, 1024)]
    bounds = 0
    signs = 0
    for delta in widths:
        m = 0
        while F(1, 2 ** m) > delta:
            m += 1
        nodes = [F(1, 2 ** j) for j in range(m + 1)]
        pts = sorted(set([delta, (1 + delta) / 2, F(1)] + [t for t in nodes if t >= delta]))
        for t in pts:
            rt, _, _ = rational(t, nodes)
            rn, _, _ = rational(-t, nodes)
            assert F(4, 5) <= rt <= 1 and rn == -rt
            assert 1 - rt <= F(2, 9)
            bounds += 1
        # Binary AND numerator has degree <=4(m+1) and positive denominator.
        for x, y in product([s * t for s in (-1, 1) for t in pts], repeat=2):
            rx, ax, qx = rational(x, nodes)
            ry, ay, qy = rational(y, nodes)
            numerator = ax * qy + ay * qx - qx * qy
            truth = 1 if x > 0 and y > 0 else -1
            assert truth * numerator > 0
            assert numerator / (qx * qy) == rx + ry - 1
            signs += 1
    return {"widths": [str(x) for x in widths], "exact_univariate_bounds": bounds,
            "exact_cleared_binary_AND_signs": signs}


def check_expectation():
    n = 3
    epsilon = F(1, 5)
    signs = list(product((-1, 1), repeat=n))
    checks = 0
    for table in range(1 << len(signs)):
        h = [1 if table & (1 << j) else -1 for j in range(len(signs))]
        for j, s in enumerate(signs):
            u = [si * (1 - epsilon) for si in s]
            value = sum(h[z] * prod((1 + ti * ui) / 2 for ti, ui in zip(t, u))
                        for z, t in enumerate(signs))
            assert abs(value) <= 1
            assert h[j] * value >= 1 - n * epsilon
            checks += 1
    return {"n": n, "epsilon": str(epsilon), "all_truth_tables_and_corners": checks}


def check_axis_and_majority():
    # F_k(t,0)=0 for t>=0 and -2(-t)^(k+1) for t<0.
    jumps = []
    for k in range(9):
        left = -2 * ((-1) ** (k + 1)) * factorial(k + 1)
        right = 0
        assert left != right
        jumps.append({"k": k, "left_derivative_order_k_plus_1": left, "right": right})
    arities = []
    for delta in [F(1, 3), F(1, 4), F(3, 10), F(1, 100)]:
        N = delta.denominator // delta.numerator
        if N % 2 == 0:
            N -= 1
        assert N > 0 and N % 2 and F(1, N) >= delta
        assert all(abs(F(2 * j - N, N)) >= delta for j in range(N + 1))
        arities.append({"delta": str(delta), "odd_N": N})
    return {"R_function_axis_derivative_jumps": jumps, "majority_guard_examples": arities}


def main():
    result = {"source": check_source(), "Boolean_reduction": check_faces(),
              "rational_construction": check_rational(), "expectation_extension": check_expectation(),
              "endpoint_diagnostics": check_axis_and_majority(),
              "limitations": "Finite algebraic checks only. Universal analytic estimates, cited lower bounds, and historical priority are not proved by these checks."}
    (OUT / "diagnostics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
