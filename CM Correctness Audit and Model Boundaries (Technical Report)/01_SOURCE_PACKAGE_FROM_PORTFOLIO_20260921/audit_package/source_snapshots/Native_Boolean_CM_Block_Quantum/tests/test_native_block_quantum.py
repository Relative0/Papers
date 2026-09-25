from __future__ import annotations

import csv
from itertools import product
from pathlib import Path

import pytest

from native_block import *

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def inventories():
    rows, inv, orth = enumerate_phase_block_gates()
    return rows, inv, orth, measurement_bases(inv), unitary_measurement_bases(orth)


def test_native_rotation_and_difference_chain():
    assert power(P,4)==I4
    assert P2!=I4
    assert transpose(P,4)==P3
    assert compose(compose(K,P),K)==P3
    assert N4==Z4
    assert [rank(x,4) for x in N_POWERS]==[4,3,2,1,0]
    assert N2==xor_matrix(I4,P2)


def test_phase_algebra_is_exact_centralizer():
    centralizer=[]
    for raw in range(1<<16):
        A=tuple((raw>>(4*i))&0xF for i in range(4))
        if compose(A,P)==compose(P,A): centralizer.append(A)
    assert len(centralizer)==16
    assert set(centralizer)==set(PHASE_OPS)
    assert len(UNIT_SELECTORS)==8


def test_block_gate_and_basis_counts(inventories):
    rows,inv,orth,bases,ubases=inventories
    assert len(rows)==65536
    assert len(inv)==24576
    assert len(orth)==512
    assert len(bases)==192
    assert len(ubases)==4


def test_bell_support_tables_and_strong_contradiction():
    expected={
        ('Z','Z'):(1,0,0,1),('Z','X'):(1,1,1,0),('Z','Y'):(0,1,1,1),
        ('X','Z'):(1,1,1,0),('X','X'):(0,1,1,1),('X','Y'):(1,0,0,1),
        ('Y','Z'):(0,1,1,1),('Y','X'):(1,0,0,1),('Y','Y'):(1,1,1,0),
    }
    s=bell_support_state()
    for i,A in enumerate(MQT_BASES):
        for j,B in enumerate(MQT_BASES):
            assert support_table2(s,A,B)==expected[(MQT_NAMES[i],MQT_NAMES[j])]
    assert compatible_bell_globals(s,MQT_BASES)==[]


def test_delta_bell_is_generated_by_native_blocks():
    H1=lift_single_bit_gate(H_ROT,2,0)
    C=logical_cnot(2,0,1)
    B=compose(C,H1)
    seed=pack_phase_branches((1,0,0,0))
    assert unpack_phase_branches(apply(B,seed),4)==(1,0,0,5)
    assert PHASE_OPS[5]==N2


def test_teleport_support_bell_exact_all_states():
    Ts=teleport_branch_maps((1,0,0,1))
    assert [rank(T,8) for T in Ts]==[8,8,8,8]
    Cs=[inverse(T,8) for T in Ts]
    assert all(C is not None for C in Cs)
    for a,b in product(range(16),repeat=2):
        psi=a|(b<<4)
        for T,C in zip(Ts,Cs):
            assert apply(C,apply(T,psi))==psi


def test_bell_analyzer_preserves_resource_rank_exhaustively():
    successful=0
    for entries in product(range(16),repeat=4):
        r=rank(resource_transfer_matrix(entries),8)
        br=[rank(T,8) for T in teleport_branch_maps(entries)]
        assert br==[r,r,r,r]
        successful += (r==8)
    assert successful==24576


def test_delta_teleportation_failure_and_natural_analyzer():
    delta=(1,0,0,5)
    assert rank(resource_transfer_matrix(delta),8)==6
    assert [rank(T,8) for T in teleport_branch_maps(delta)]==[6,6,6,6]
    H1=lift_single_bit_gate(H_ROT,2,0); C=logical_cnot(2,0,1); B=compose(C,H1)
    Binv=inverse(B,16); assert Binv is not None
    Ts=teleport_branch_maps_with_phase_analyzer(delta,Binv)
    assert [rank(T,8) for T in Ts]==[4,4,4,4]
    assert [block_selectors_2x2(T) for T in Ts]==[(1,0,0,0),(0,5,5,0),(5,0,0,5),(0,1,0,0)]


def test_rotation_classes_and_separability_exhaustive():
    expected={(0,0):24576,(0,1):18432,(0,2):9216,(0,3):4608,(0,4):4608,
              (1,1):1536,(1,2):1152,(1,3):576,(1,4):576,(2,2):96,(2,3):72,
              (2,4):72,(3,3):6,(3,4):9,(4,4):1}
    counts={k:0 for k in expected}
    simple=simple_tensor_states()
    assert len(simple)==5266
    for entries in product(range(16),repeat=4):
        cls=rotation_class(entries); counts[cls]+=1
        assert (pack_phase_branches(entries) in simple)==(cls[1]==4)
    assert counts==expected


def test_contextuality_generated_table_matches_expected(inventories):
    _,_,_,bases,_=inventories
    # Directly check representative statuses for the three key strata.
    c00=two_sat_support_coverage(canonical_state(0,0),bases)
    c02=two_sat_support_coverage(canonical_state(0,2),bases)
    c04=two_sat_support_coverage(canonical_state(0,4),bases)
    assert not c00['satisfiable']
    assert c02['satisfiable'] and c02['uncovered_possible_sections']==36864
    assert c04['satisfiable'] and c04['uncovered_possible_sections']==0


def test_ghz_states_generated_natively_and_support_properties(inventories):
    _,_,_,_,ubases=inventories
    seed=pack_phase_branches((1,0,0,0,0,0,0,0))
    c01=logical_cnot(3,0,1); c02=logical_cnot(3,0,2)
    support=apply(c02,apply(c01,apply(lift_single_bit_gate(SHEAR2,3,0),seed)))
    delta=apply(c02,apply(c01,apply(lift_single_bit_gate(H_ROT,3,0),seed)))
    assert support==ghz_state(0)
    assert delta==ghz_state(2)
    # embedded 3-setting global sections
    def globals_count(state,bases):
        n=len(bases); contexts=[(i,j,k,support_table3(state,bases[i],bases[j],bases[k])) for i in range(n) for j in range(n) for k in range(n)]
        return sum(all(t[4*q[i]+2*q[n+j]+q[2*n+k]] for i,j,k,t in contexts) for q in product((0,1),repeat=3*n))
    assert globals_count(support,MQT_BASES)==0
    assert globals_count(delta,MQT_BASES)==16
    assert globals_count(support,ubases)==44
    assert globals_count(delta,ubases)==23


def test_generated_csv_cardinalities():
    expected={
        'measurement_bases_native_192.csv':192,
        'bell_native_mqt_tables.csv':36,
        'contextuality_native_by_rotation_class.csv':15,
        'native_resource_inventory_65536.csv':65536,
        'teleportation_native_all_256_x4.csv':1024,
        'teleportation_native_by_rotation_class.csv':15,
        'ghz_support_native_contexts.csv':216,
        'ghz_delta_native_contexts.csv':216,
    }
    for name,n in expected.items():
        with (ROOT/'data'/name).open() as f:
            assert sum(1 for _ in csv.DictReader(f))==n
