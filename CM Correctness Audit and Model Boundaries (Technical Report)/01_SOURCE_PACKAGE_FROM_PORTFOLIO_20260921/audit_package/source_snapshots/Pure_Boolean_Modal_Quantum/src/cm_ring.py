"""Pure-Boolean CM phase ring utilities.

Core state arithmetic uses only 0/1 coefficients, XOR addition and the
cyclic-convolution ``star`` product. Python integers 0..15 are only compact
bit-pattern encodings of four Boolean coefficients (E0,E1,E2,E3).
No signed, real, or complex amplitudes occur in this module.
"""
from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence, Tuple

E0, E1, E2, E3 = 1, 2, 4, 8
ZERO = 0
ONE = E0
T = E1
Z = E2
DELTA = E0 ^ E2          # u^2
OMEGA = E0 ^ E1 ^ E2 ^ E3  # u^3
U = E0 ^ E1             # u = 1 + t

# Full 16x16 multiplication table. The construction itself is Boolean:
# coefficient products are AND; coefficient accumulation is XOR.
MUL = [[0] * 16 for _ in range(16)]
for _a in range(16):
    for _b in range(16):
        _r = 0
        for _i in range(4):
            if (_a >> _i) & 1:
                for _j in range(4):
                    if (_b >> _j) & 1:
                        _r ^= 1 << ((_i + _j) & 3)
        MUL[_a][_b] = _r

UNITS = tuple(a for a in range(16) if a.bit_count() & 1)
NONUNITS = tuple(a for a in range(16) if not (a.bit_count() & 1))
INV = {a: next(b for b in range(16) if MUL[a][b] == ONE) for a in UNITS}


def add(a: int, b: int) -> int:
    return a ^ b


def star(a: int, b: int) -> int:
    return MUL[a][b]


def complement(a: int) -> int:
    """Entrywise Boolean complement of a four-feature CM pattern."""
    return a ^ 0b1111


def quotient(a: int, b: int) -> int:
    """Original-paper support quotient A \\ B = A AND NOT B."""
    return a & ((~b) & 0b1111)


def bar(a: int) -> int:
    """CM transpose/intrinsic conjugation: E1 <-> E3, E0/E2 fixed."""
    return (a & E0) | ((a & E1) << 2) | (a & E2) | ((a & E3) >> 2)


def rotate(a: int, k: int = 1) -> int:
    """Clockwise cyclic feature rotation, equivalently t^k star a."""
    k &= 3
    return star(1 << k, a)


def is_unit(a: int) -> bool:
    return a in INV


def inverse(a: int) -> int:
    if a not in INV:
        raise ValueError(f"not a unit: {a}")
    return INV[a]


def u_coeff_bits(a: int) -> Tuple[int, int, int, int]:
    """Coordinates in 1,u,u^2,u^3 for u=1+t."""
    a0, a1, a2, a3 = ((a >> i) & 1 for i in range(4))
    return (a0 ^ a1 ^ a2 ^ a3, a1 ^ a3, a2 ^ a3, a3)


def valuation(a: int) -> int:
    """u-adic valuation in {0,1,2,3,4}; v(0)=4."""
    c = u_coeff_bits(a)
    for i, bit in enumerate(c):
        if bit:
            return i
    return 4


def elem_name(a: int) -> str:
    if a == 0:
        return "0"
    specials = {
        E0: "E0",
        E1: "E1=t",
        E2: "E2=z",
        E3: "E3=t^3",
        U: "u=E0^E1",
        DELTA: "delta=E0^E2",
        OMEGA: "Omega",
    }
    if a in specials:
        return specials[a]
    return "^".join(f"E{i}" for i in range(4) if (a >> i) & 1)


def matmul(A: Sequence[int], B: Sequence[int], n: int) -> Tuple[int, ...]:
    return tuple(
        _xor_reduce(MUL[A[i * n + k]][B[k * n + j]] for k in range(n))
        for i in range(n)
        for j in range(n)
    )


def matvec(A: Sequence[int], v: Sequence[int], n: int) -> Tuple[int, ...]:
    return tuple(
        _xor_reduce(MUL[A[i * n + j]][v[j]] for j in range(n))
        for i in range(n)
    )


def transpose(A: Sequence[int], n: int) -> Tuple[int, ...]:
    return tuple(A[j * n + i] for i in range(n) for j in range(n))


def dagger(A: Sequence[int], n: int) -> Tuple[int, ...]:
    return tuple(bar(x) for x in transpose(A, n))


def identity(n: int) -> Tuple[int, ...]:
    return tuple(ONE if i == j else ZERO for i in range(n) for j in range(n))


def kron(A: Sequence[int], B: Sequence[int], nA: int, nB: int) -> Tuple[int, ...]:
    """Kronecker product over A, row-major."""
    return tuple(
        MUL[A[ia * nA + ja]][B[ib * nB + jb]]
        for ia in range(nA)
        for ib in range(nB)
        for ja in range(nA)
        for jb in range(nB)
    )


def det2(A: Sequence[int]) -> int:
    # In characteristic two, ad-bc = ad+bc = XOR.
    return MUL[A[0]][A[3]] ^ MUL[A[1]][A[2]]


def is_invertible2(A: Sequence[int]) -> bool:
    return is_unit(det2(A))


def inverse_matrix(A: Sequence[int], n: int) -> Tuple[int, ...] | None:
    """Gauss-Jordan over the local ring, using unit pivots."""
    M = [list(A[i * n:(i + 1) * n]) + [ONE if i == j else ZERO for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if is_unit(M[r][col])), None)
        if pivot is None:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        iv = inverse(M[col][col])
        M[col] = [MUL[iv][x] for x in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if f:
                M[r] = [x ^ MUL[f][y] for x, y in zip(M[r], M[col])]
    return tuple(x for r in range(n) for x in M[r][n:])


def is_unitary2(A: Sequence[int]) -> bool:
    return matmul(dagger(A, 2), A, 2) == identity(2)


def is_monomial_unit_gate(A: Sequence[int]) -> bool:
    nz = tuple(x != 0 for x in A)
    pattern = (
        sum(nz[:2]) == 1
        and sum(nz[2:]) == 1
        and int(nz[0]) + int(nz[2]) == 1
        and int(nz[1]) + int(nz[3]) == 1
    )
    return pattern and all(is_unit(x) for x in A if x)


def outer2(x: Sequence[int], y: Sequence[int]) -> Tuple[int, int, int, int]:
    return (MUL[x[0]][y[0]], MUL[x[0]][y[1]], MUL[x[1]][y[0]], MUL[x[1]][y[1]])


def local_action(U2: Sequence[int], V2: Sequence[int], state_matrix: Sequence[int]) -> Tuple[int, ...]:
    """(U tensor V)|psi> represented as U M V^T."""
    return matmul(matmul(U2, state_matrix, 2), transpose(V2, 2), 2)


def effect_amplitude2(M: Sequence[int], e: Sequence[int], f: Sequence[int]) -> int:
    x0 = MUL[e[0]][M[0]] ^ MUL[e[1]][M[2]]
    x1 = MUL[e[0]][M[1]] ^ MUL[e[1]][M[3]]
    return MUL[x0][f[0]] ^ MUL[x1][f[1]]


def support_table2(M: Sequence[int], basis_a, basis_b) -> Tuple[int, int, int, int]:
    return tuple(int(effect_amplitude2(M, e, f) != 0) for e in basis_a for f in basis_b)


def effect_amplitude3(a000: int, a111: int, e, f, g) -> int:
    p0 = MUL[a000][MUL[e[0]][MUL[f[0]][g[0]]]]
    p1 = MUL[a111][MUL[e[1]][MUL[f[1]][g[1]]]]
    return p0 ^ p1


def support_table3(a000: int, a111: int, basis_a, basis_b, basis_c) -> Tuple[int, ...]:
    return tuple(
        int(effect_amplitude3(a000, a111, e, f, g) != 0)
        for e in basis_a for f in basis_b for g in basis_c
    )


def canonical_projective_row(row: Sequence[int]) -> Tuple[int, int]:
    """Canonicalize a unimodular effect row modulo multiplication by a unit."""
    return min((MUL[g][row[0]], MUL[g][row[1]]) for g in UNITS)


def canonical_unordered_basis(A: Sequence[int]):
    return tuple(sorted((canonical_projective_row(A[:2]), canonical_projective_row(A[2:]))))


def all_matrices2():
    return product(range(16), repeat=4)


def _xor_reduce(values: Iterable[int]) -> int:
    x = 0
    for v in values:
        x ^= v
    return x
