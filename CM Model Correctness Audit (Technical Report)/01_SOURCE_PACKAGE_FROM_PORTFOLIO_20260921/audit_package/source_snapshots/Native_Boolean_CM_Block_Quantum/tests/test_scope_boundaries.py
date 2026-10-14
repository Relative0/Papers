from __future__ import annotations

from itertools import product

from native_block import (
    BELL_ANALYZER_F2,
    E0_VEC,
    H_ROT,
    I4,
    PHASE_OPS,
    SHEAR2,
    block_matrix,
    compose,
    identity,
    inverse,
    rank,
    resource_transfer_matrix,
    teleport_branch_maps,
    transpose,
)


def is_orthogonal(A, n):
    return compose(transpose(A, n), A) == identity(n)


def test_standard_universal_teleportation_uses_general_reversible_not_orthogonal_dynamics():
    # The standard analyzer itself is invertible but not orthogonal.
    assert rank(BELL_ANALYZER_F2, 4) == 4
    assert not is_orthogonal(BELL_ANALYZER_F2, 4)

    # For the support-Bell resource, all four branch maps are invertible, but
    # only two are orthogonal. Hence two exact corrections are necessarily
    # non-orthogonal as well.
    branches = teleport_branch_maps((1, 0, 0, 1))
    assert [rank(T, 8) for T in branches] == [8, 8, 8, 8]
    assert [is_orthogonal(T, 8) for T in branches] == [False, False, True, True]
    corrections = [inverse(T, 8) for T in branches]
    assert all(C is not None for C in corrections)
    assert [is_orthogonal(C, 8) for C in corrections] == [False, False, True, True]


def test_native_splitters_have_different_orthogonality_status():
    # The simple support-splitting shear is reversible but non-orthogonal.
    assert rank(SHEAR2, 8) == 8
    assert not is_orthogonal(SHEAR2, 8)
    # H_ROT is an involutory Boolean-orthogonal splitter.
    assert is_orthogonal(H_ROT, 8)


def test_support_bell_has_no_orthogonal_exact_branch_with_orthogonal_outcome_block():
    # Exhaust every possible 4x16 single-outcome analyzer row-block whose four
    # 4x4 blocks lie in the P-generated phase algebra. If the global analyzer
    # were Boolean-orthogonal, each such outcome block E must satisfy E E^T=I4.
    # For the support-Bell resource, exact correction by an orthogonal 8x8 map
    # would require the corresponding Bob branch map T itself to be orthogonal.
    # No such outcome exists in this block algebra.
    row_orthogonal = 0
    invertible_branch = 0
    orthogonal_branch = 0

    for q00, q01, q10, q11 in product(range(16), repeat=4):
        E = block_matrix([[PHASE_OPS[q00], PHASE_OPS[q01], PHASE_OPS[q10], PHASE_OPS[q11]]], 4)
        if compose(E, transpose(E, 16)) != I4:
            continue
        row_orthogonal += 1

        # For |00> XOR |11>, T[b,i] = analyzer_block[i,b].
        T = block_matrix(
            [
                [PHASE_OPS[q00], PHASE_OPS[q10]],
                [PHASE_OPS[q01], PHASE_OPS[q11]],
            ],
            4,
        )
        if rank(T, 8) == 8:
            invertible_branch += 1
        if is_orthogonal(T, 8):
            orthogonal_branch += 1

    assert row_orthogonal == 16384
    assert invertible_branch == 8192
    assert orthogonal_branch == 0
