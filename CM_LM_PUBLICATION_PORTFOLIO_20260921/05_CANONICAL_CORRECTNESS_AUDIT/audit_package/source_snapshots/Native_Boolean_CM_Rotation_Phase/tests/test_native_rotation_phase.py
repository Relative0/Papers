import importlib.util
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/'code'/'verify_native_rotation.py'
spec=importlib.util.spec_from_file_location('v',SRC)
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

def test_rotation_native():
    assert v.mpow(v.P,4)==v.I4
    assert v.mpow(v.P,2)!=v.I4
    assert v.transpose(v.P)==v.mpow(v.P,3)

def test_dihedral_transpose():
    assert v.mm(v.K,v.K)==v.I4
    assert v.mm(v.mm(v.K,v.P),v.K)==v.mpow(v.P,3)

def test_rotation_operator_algebra():
    assert len({v.mat_key(A) for A in v.ops})==16
    assert all(v.mat_key(v.mm(v.ops[a],v.ops[b]))==v.mat_key(v.ops[v.cyclic_mask(a,b)])
               for a in range(16) for b in range(16))

def test_unipotent_not_complex_scalar():
    N=v.xor_mat(v.P,v.I4)
    assert v.mpow(N,3)!=v.Z4
    assert v.mpow(N,4)==v.Z4

def test_delta_operator_typed():
    assert v.mm(v.Delta,v.Delta)==v.Z4
    # This Delta is I4 XOR P^2, not the 2x2 CM identity itself.

def test_strict_shear_superposition():
    assert v.mm(v.C2,v.C2)==v.eye(2)
    assert v.mv(v.C2,[1,0])==[1,1]
    assert len(v.both_split)==0

def test_bell_generation():
    assert v.bell==[1,0,0,1]

def test_phase_register_symmetric_splitter():
    assert v.mm(v.H8,v.H8)==v.eye(8)
    for seed in [v.seed0,v.seed1]:
        out=v.mv(v.H8,seed)
        assert any(out[:4]) and any(out[4:])

def test_shear_interferometer_distinguishes_rotations_by_exact_pattern():
    pats=[]
    for k in range(4):
        out=v.mv(v.C8,v.mv(v.controlled_phase(k),v.mv(v.C8,v.seed0)))
        pats.append(tuple(out[4:]))
    assert len(set(pats))==4
    assert pats[0]==(0,0,0,0)

def test_symmetric_interferometer_detects_rotation_parity():
    pats=[]
    for k in range(4):
        out=v.mv(v.H8,v.mv(v.controlled_phase(k),v.mv(v.H8,v.seed0)))
        pats.append(tuple(out[4:]))
    assert pats[0]==pats[2]==(0,0,0,0)
    assert pats[1]==pats[3]==(1,1,1,1)
