"""Independent finite checks for the LM-to-modal bridge investigation.

Target algebra: A = F2[u]/(u^4), encoded by 4-bit coefficient vectors
in basis (1,u,u^2,u^3).  The script independently checks finite claims
used in the bridge report; the mathematical theorems do not rely on
finite enumeration except where explicitly described as an exhaustive
finite classification/check.
"""
from itertools import product
import json
import platform
import sys

# ---------------------------------------------------------------------------
# Chain ring A = F2[u]/(u^4)
# ---------------------------------------------------------------------------

def add(a, b):
    return a ^ b


def mul(a, b):
    out = 0
    for i in range(4):
        if (a >> i) & 1:
            for j in range(4 - i):
                if (b >> j) & 1:
                    out ^= 1 << (i + j)
    return out


def inv_unit(a):
    for b in range(16):
        if mul(a, b) == 1:
            return b
    raise ValueError(a)


units = [a for a in range(16) if a & 1]
idempotents = [a for a in range(16) if mul(a, a) == a]


def det(M):
    a, b, c, d = M
    return add(mul(a, d), mul(b, c))  # subtraction = addition in char 2


def mm(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (
        add(mul(a, e), mul(b, g)),
        add(mul(a, f), mul(b, h)),
        add(mul(c, e), mul(d, g)),
        add(mul(c, f), mul(d, h)),
    )


def mv(A, v):
    a, b, c, d = A
    x, y = v
    return (add(mul(a, x), mul(b, y)), add(mul(c, x), mul(d, y)))


def inv2(A):
    a, b, c, d = A
    z = det(A)
    zi = inv_unit(z)
    return (mul(zi, d), mul(zi, b), mul(zi, c), mul(zi, a))


I = (1, 0, 0, 1)
ZERO2 = (0, 0, 0, 0)
P0 = (1, 0, 0, 0)
P1 = (0, 0, 0, 1)


def scale_row(M, u0, u1):
    a, b, c, d = M
    return (mul(u0, a), mul(u0, b), mul(u1, c), mul(u1, d))


def swap_rows(M):
    a, b, c, d = M
    return (c, d, a, b)


def canon(M):
    """Canonical representative modulo independent unit row scaling and swap."""
    reps = []
    for u0 in units:
        for u1 in units:
            X = scale_row(M, u0, u1)
            reps.append(X)
            reps.append(swap_rows(X))
    return min(reps)


gl = []
projective = set()
for M in product(range(16), repeat=4):
    if det(M) in units:
        gl.append(M)
        projective.add(canon(M))

# ---------------------------------------------------------------------------
# Reversible-basis branch projectors J_i^B = B^{-1} P_i B
# ---------------------------------------------------------------------------

basis_projector_checks = 0
branch_equiv_checks = 0
same_basis_repeat_checks = 0
orthogonality_checks = 0
resolution_checks = 0

for B in projective:
    Bi = inv2(B)
    projectors = []
    for P, idx in ((P0, 0), (P1, 1)):
        J = mm(mm(Bi, P), B)
        projectors.append(J)
        assert mm(J, J) == J
        basis_projector_checks += 1
        for psi in product(range(16), repeat=2):
            coeff = mv(B, psi)[idx]
            branch = mv(J, psi)
            assert (branch != (0, 0)) == (coeff != 0)
            after = mv(B, branch)
            assert after[idx] == coeff and after[1 - idx] == 0
            branch_equiv_checks += 1
            same_basis_repeat_checks += 1
    assert mm(projectors[0], projectors[1]) == ZERO2
    assert mm(projectors[1], projectors[0]) == ZERO2
    orthogonality_checks += 2
    assert tuple(add(x, y) for x, y in zip(*projectors)) == I
    resolution_checks += 1

# Projective invariance under independent unit scaling of effect rows.
row_scale_checks = 0
for B in projective:
    Binv = inv2(B)
    J0 = mm(mm(Binv, P0), B)
    J1 = mm(mm(Binv, P1), B)
    for u0 in units:
        for u1 in units:
            Bs = scale_row(B, u0, u1)
            Bsi = inv2(Bs)
            assert mm(mm(Bsi, P0), Bs) == J0
            assert mm(mm(Bsi, P1), Bs) == J1
            row_scale_checks += 2

# ---------------------------------------------------------------------------
# Symbolic support: B \otimes_F2 A, with B represented extensionally on
# two Boolean variables by 4-bit truth-table masks.
# ---------------------------------------------------------------------------

support_checks = 0
for fs in product(range(16), repeat=4):
    support_mask = fs[0] | fs[1] | fs[2] | fs[3]
    for valuation in range(4):
        qv = 0
        for k, f in enumerate(fs):
            if (f >> valuation) & 1:
                qv |= 1 << k
        assert (((support_mask >> valuation) & 1) == 1) == (qv != 0)
        support_checks += 1

# ---------------------------------------------------------------------------
# Paper-B LM family is not closed under ordinary Boolean-ring matrix product.
# Formula algebra on X,Y is represented by 4-bit truth masks in true-first
# assignment order (11,10,01,00).
# ---------------------------------------------------------------------------

vals = [(1, 1), (1, 0), (0, 1), (0, 0)]
index = {xy: i for i, xy in enumerate(vals)}


def formula_mask(fn):
    m = 0
    for k, (x, y) in enumerate(vals):
        if fn(x, y):
            m |= 1 << k
    return m


def token_value(token, x, y):
    return (token >> index[(x, y)]) & 1


def lm_of_token(token):
    # [ X Theta Y, X Theta not-Y ; not-X Theta Y, not-X Theta not-Y ]
    entries = []
    for flip_x, flip_y in ((0, 0), (0, 1), (1, 0), (1, 1)):
        entries.append(
            formula_mask(
                lambda x, y, fx=flip_x, fy=flip_y:
                token_value(token, x ^ fx, y ^ fy)
            )
        )
    return tuple(entries)


def boolring_mm(A, B):
    a, b, c, d = A
    e, f, g, h = B
    # XOR is Boolean-ring addition; AND is multiplication.
    return (
        (a & e) ^ (b & g),
        (a & f) ^ (b & h),
        (c & e) ^ (d & g),
        (c & f) ^ (d & h),
    )


lm_family = {lm_of_token(t): t for t in range(16)}
lm_product_inside = 0
lm_product_outside = 0
lm_product_counterexamples = []
for ta, tb in product(range(16), repeat=2):
    p = boolring_mm(lm_of_token(ta), lm_of_token(tb))
    if p in lm_family:
        lm_product_inside += 1
    else:
        lm_product_outside += 1
        if len(lm_product_counterexamples) < 8:
            lm_product_counterexamples.append(
                {"left_token": ta, "right_token": tb, "product_masks": p}
            )
assert lm_product_inside == 112
assert lm_product_outside == 144

# ---------------------------------------------------------------------------
# Obstructions and closure counterexamples
# ---------------------------------------------------------------------------

assert idempotents == [0, 1]


def supp(a):
    return int(a != 0)


add_counterexample = {
    "a": 2,               # u
    "b": 4,               # u^2
    "a_plus_b": add(2, 4),
    "supp_sum": supp(add(2, 4)),
    "xor_of_supports": supp(2) ^ supp(4),
}
assert add_counterexample["supp_sum"] != add_counterexample["xor_of_supports"]

mul_counterexample = {
    "a": 2,               # u
    "b": 8,               # u^3
    "a_times_b": mul(2, 8),
    "supp_product": supp(mul(2, 8)),
    "and_of_supports": supp(2) & supp(8),
}
assert mul_counterexample["supp_product"] != mul_counterexample["and_of_supports"]

# Nonzero states are not tensor-closed over A because zero divisors can annihilate.
psi = (2, 0)   # (u,0)
phi = (8, 0)   # (u^3,0)
tensor = [mul(x, y) for x in psi for y in phi]
assert tensor == [0, 0, 0, 0]

# Even if preparations are restricted to unimodular vectors, conditioning can
# yield nonunimodular nonzero states.  M=diag(1,u) is unimodular as a 4-vector;
# Alice's second standard effect leaves Bob in (0,u).
M = (1, 0, 0, 2)
conditional = (M[2], M[3])
assert conditional == (0, 2)
assert all((x & 1) == 0 for x in conditional)

out = {
    "environment": {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    },
    "ring_order": 16,
    "units": units,
    "idempotents": idempotents,
    "GL2_count": len(gl),
    "unordered_projective_basis_count": len(projective),
    "basis_projector_idempotence_checks": basis_projector_checks,
    "projector_orthogonality_checks": orthogonality_checks,
    "projector_resolution_of_identity_checks": resolution_checks,
    "branch_nonzero_iff_effect_nonzero_checks": branch_equiv_checks,
    "same_basis_repeatability_checks": same_basis_repeat_checks,
    "row_unit_scaling_invariance_checks": row_scale_checks,
    "symbolic_support_fiber_checks": support_checks,
    "paper_b_lm_matrix_products_total": 256,
    "paper_b_lm_matrix_products_remaining_in_family": lm_product_inside,
    "paper_b_lm_matrix_products_leaving_family": lm_product_outside,
    "paper_b_lm_product_counterexamples": lm_product_counterexamples,
    "support_add_counterexample": add_counterexample,
    "support_mul_counterexample": mul_counterexample,
    "nonzero_tensor_zero_example": {
        "psi": psi,
        "phi": phi,
        "tensor": tensor,
    },
    "unimodular_bipartite_conditional_nonunimodular_example": {
        "M": M,
        "effect": (0, 1),
        "conditional": conditional,
    },
}
print(json.dumps(out, indent=2))
