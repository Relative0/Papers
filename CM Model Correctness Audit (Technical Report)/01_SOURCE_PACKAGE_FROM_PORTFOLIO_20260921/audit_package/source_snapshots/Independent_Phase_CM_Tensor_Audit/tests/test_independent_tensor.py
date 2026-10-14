from __future__ import annotations

import csv
import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from native_block import *
from independent_tensor_audit import (
    factorized_bell_effect_basis,
    ghz_literal_state,
    ghz_tables_and_coverage,
    local_tensor_support,
    local_tensor_support_direct,
    logical_only_pair_analyzer,
    minimum_unsat_ghz_contexts,
    naive_four_outcome_residual_profile,
    orthogonal_even_weight_no_go,
    phase_word_basis,
    support_table_literal,
    teleport_branch_map,
)


def test_P_and_phase_group_generation():
    assert power(P, 4) == I4
    assert transpose(P, 4) == P3
    mats, words, meta = phase_word_basis()
    assert len(mats) == 16
    assert meta["generated_group_size"] == 20160
    assert rank(tuple(sum(r << (4*i) for i, r in enumerate(M)) for M in mats), 16) == 16
    assert all(rank(M, 4) == 4 for M in mats)
    assert max(map(len, words)) <= 24


def test_literal_choi_support_formula_matches_direct_tensor():
    _, inv, _ = enumerate_phase_block_gates()
    bases = measurement_bases(inv)
    M = identity(8)
    for i, j in ((0, 0), (2, 2), (16, 50), (191, 100)):
        for e in bases[i]:
            for f in bases[j]:
                assert local_tensor_support(M, e, f) == local_tensor_support_direct(M, e, f)


def test_bell_ZXY_tables_and_hidden_variable_failure():
    M = identity(8)
    expected = {
        "ZZ": (1,0,0,1), "ZX": (1,1,1,0), "ZY": (0,1,1,1),
        "XZ": (1,1,1,0), "XX": (0,1,1,1), "XY": (1,0,0,1),
        "YZ": (0,1,1,1), "YX": (1,0,0,1), "YY": (1,1,1,0),
    }
    tables = {}
    for i,A in enumerate(MQT_BASES):
        for j,B in enumerate(MQT_BASES):
            key = MQT_NAMES[i] + MQT_NAMES[j]
            tables[(i,j)] = support_table_literal(M, A, B)
            assert tables[(i,j)] == expected[key]
    good = []
    for q in product((0,1), repeat=6):
        if all(tables[(i,j)][2*q[i] + q[3+j]] for i in range(3) for j in range(3)):
            good.append(q)
    assert good == []


def test_contextuality_generated_table_has_expected_classification():
    rows = list(csv.DictReader((ROOT / "data" / "contextuality_literal_choi_by_rotation_class.csv").open()))
    assert len(rows) == 15
    by = {(int(r["class_a"]), int(r["class_b"])): r for r in rows}
    assert by[(0,0)]["classification"] == "STRONG_CONTEXTUAL"
    assert by[(0,2)]["classification"] == "LOGICAL_CONTEXTUAL_NOT_STRONG"
    assert by[(0,4)]["classification"] == "RELATIONALLY_LOCAL"
    assert by[(3,3)]["classification"] == "STRONG_CONTEXTUAL"
    assert by[(4,4)]["classification"] == "DEGENERATE_ZERO_EXCLUDED"
    assert sum(int(r["state_count"]) for r in rows) == 65536
    assert int(by[(0,0)]["basis_pair_tables_differing_from_shared_model"]) > 0
    assert int(by[(0,3)]["basis_pair_tables_differing_from_shared_model"]) == 0


def test_literal_GHZ_six_context_contradiction():
    contexts, cov = ghz_tables_and_coverage(ghz_literal_state(True), MQT_BASES)
    assert cov["global_assignments"] == 0
    count, ctx = minimum_unsat_ghz_contexts(contexts, 3)
    assert count == 6
    assert ctx == [(0,0,0),(0,1,1),(1,0,2),(1,1,1),(2,2,0),(2,2,2)]


def test_factorized_64_outcome_analyzer_is_complete_and_invertible():
    Rs, Vs, words, meta = factorized_bell_effect_basis()
    analyzer = tuple(sum(r << (8*i) for i, r in enumerate(R)) for R in Rs)
    assert len(Rs) == 64
    assert rank(analyzer, 64) == 64
    assert all(rank(R, 8) == 8 for R in Rs)
    assert len(Vs) == 16
    assert meta["generated_group_size"] == 20160


def test_universal_literal_teleportation_all_inputs_all_outcomes():
    Rs, _, _, _ = factorized_bell_effect_basis()
    M = identity(8)
    corrections = [inverse(teleport_branch_map(M,R), 8) for R in Rs]
    assert all(C is not None for C in corrections)
    checks = 0
    for psi in range(256):
        for R, C in zip(Rs, corrections):
            T = teleport_branch_map(M, R)
            assert apply(C, apply(T, psi)) == psi
            checks += 1
    assert checks == 256 * 64


def test_resource_rank_is_preserved_by_every_canonical_branch():
    Rs, _, _, _ = factorized_bell_effect_basis()
    for a in range(5):
        for b in range(a,5):
            M = block_matrix([[N_POWERS[a],Z4],[Z4,N_POWERS[b]]],4)
            rr = rank(M,8)
            assert {rank(teleport_branch_map(M,R),8) for R in Rs} == {rr}


def test_exact_full_rank_resource_count():
    full = 0
    hist = {}
    for packed in range(65536):
        entries = (packed & 15, (packed >> 4) & 15, (packed >> 8) & 15, (packed >> 12) & 15)
        r = rank(expand_selector_matrix(entries,2,2),8)
        hist[r] = hist.get(r,0)+1
        full += r == 8
    assert full == 24576
    assert hist == {4:5280,5:5760,6:10752,7:18432,8:24576,3:648,2:78,1:9,0:1}


def test_naive_four_logical_outcomes_leave_unresolved_phase_residual():
    profile = naive_four_outcome_residual_profile(identity(8))
    assert rank(logical_only_pair_analyzer(),64) == 64
    assert len(profile) == 4
    for p in profile:
        assert p["global_branch_rank"] == 8
        assert p["nonzero_residual_phase_blocks"] == 16
        assert p["distinct_nonzero_bob_maps"] == 16
        assert p["factorizes_as_fixed_alice_residual_times_one_bob_map"] is False


def test_orthogonal_complete_effect_basis_no_go_and_O4_span():
    info = orthogonal_even_weight_no_go(8)
    assert info["therefore_no_full_orthogonal_effect_basis"] is True
    orth4=[]
    for raw in range(1<<16):
        M=tuple((raw>>(4*i))&15 for i in range(4))
        if compose(transpose(M,4),M)==I4:
            orth4.append(M)
    flat=tuple(sum(r<<(4*i) for i,r in enumerate(M)) for M in orth4)
    assert len(orth4)==48
    assert rank(flat,16)==10


def test_summary_headlines():
    s=json.load((ROOT/"data"/"independent_tensor_summary.json").open())
    h=s["headline"]
    assert h["bell_survives_literal_tensor"] is True
    assert h["support_GHZ_survives_literal_tensor"] is True
    assert h["old_compact_4_outcome_universal_teleportation_survives"] is False
    assert h["universal_exact_teleportation_survives_with_full_independent_register_Bell_analysis"] is True
    assert h["full_literal_tensor_outcomes"] == 64
