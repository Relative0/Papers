"""Additional independent-kernel and evidence checks; no old code imported."""
import sys,json,csv,random
from pathlib import Path
from itertools import product
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from boolean_kernel import *
import audit_models as a
SUMMARY=json.loads((ROOT/'data/audit_summary.json').read_text())

def test_kernel_all_2x2_pairs():
    mats=[unflatten(i,2,2) for i in range(16)]
    for x,y in product(mats,repeat=2):assert compose(x,y,2)==naive_compose(x,y,2)

def test_kernel_random_rectangular_pairs():
    rng=random.Random(117)
    for _ in range(200):
        m,n,p=[rng.randrange(1,10) for i in range(3)]
        x=tuple(rng.randrange(1<<n) for i in range(m));y=tuple(rng.randrange(1<<p) for i in range(n))
        assert compose(x,y,p)==naive_compose(x,y,p)

def test_batch_rank_all_4x4():
    mats=np.array([unflatten(i,4,4) for i in range(65536)],dtype=np.uint64)
    assert np.array_equal(batch_rank(mats,4),[rank(tuple(map(int,m))) for m in mats])

def test_inverse_all_4x4():
    count=0
    for i in range(65536):
        m=unflatten(i,4,4);inv=invert(m)
        if inv is not None:
            assert compose(m,inv,4)==compose(inv,m,4)==ident(4);count+=1
    assert count==20160

def test_rectangular_normal_form():
    rng=random.Random(119)
    for n,m in ((2,3),(4,4),(5,7),(8,8),(9,6)):
        for _ in range(20):
            M=tuple(rng.randrange(1<<n) for i in range(m));r,U,V,D=row_col_normal_form(M,n)
            assert compose(compose(U,M,n),V,n)==D
            assert D==tuple(1<<i if i<r else 0 for i in range(m))
            assert rank(U)==m and rank(V)==n and r==rank(M)

def test_tensor_functoriality():
    rng=random.Random(120)
    for _ in range(30):
        A,B,C,D=[unflatten(rng.randrange(16),2,2) for i in range(4)]
        assert compose(kron(A,B,2),kron(C,D,2),4)==kron(compose(A,C,2),compose(B,D,2),2)

def test_rotation_and_transpose():
    assert power(a.P,4)==ident(4) and power(a.P,2)!=ident(4)
    assert trans(a.P,4)==power(a.P,3)
    assert compose(compose(a.K,a.P,4),a.K,4)==power(a.P,3)

def test_type_distinction():
    assert compose(ident(2),ident(2),2)==ident(2)
    assert compose(a.NP[2],a.NP[2],4)==(0,)*4 and a.NP[2]!=(0,)*4

def test_difference_filtration():
    assert [rank(x) for x in a.NP]==[4,3,2,1,0]

def test_three_dimensional_order_four():
    J=(3,6,4)
    assert power(J,4)==ident(3) and power(J,2)!=ident(3)

def test_mixer_and_kernel_exception():
    H=block2(a.I4,a.NP[2],a.NP[2],a.I4)
    assert power(H,2)==ident(8) and compose(trans(H,8),H,8)==ident(8)
    assert apply(a.NP[2],5)==0 # splitting is not guaranteed for every phase pattern

def test_shared_tensor_zero_counterexample():
    assert a.NV[3] and a.NV[1] and not a.ACT[a.NV[3],a.NV[1]]
    assert kron((a.NV[3],),(a.NV[1],),4)!=(0,)

def test_choi_changes_separability():
    M=a.resource((1,0,0,0))
    assert rank(M)==4 # shared simple tensor, literal entangled state

def test_shared_counts_and_literal_counts():
    d=SUMMARY['inventories']
    assert d['invertible']==24576 and d['orthogonal']==512
    assert d['shared_nonseparable']==60270 and d['literal_nonseparable_in_structured_family']==65526

def test_context_counts():
    assert SUMMARY['contextuality']['all_class_counts']==dict(STRONG=26214,LOGICAL=34056,LOCAL=5265,ZERO=1)

def test_two_sat_against_random_bruteforce():
    rng=np.random.default_rng(121)
    for n in (1,2,3):
        for _ in range(40):
            t=rng.integers(0,2,size=(n,n,4),dtype=np.uint8).astype(bool)
            k,cover=a.brute_coverage(t);c=a.closure_coverage(t)
            assert bool(k)==c['satisfiable'] and cover==c['extendable']

def test_bell_contradiction():
    mqt=[((1,0),(0,1)),((1,1),(1,0)),((0,1),(1,1))]
    t=a.context_tables(mqt,0,0)
    assert a.brute_coverage(t)[0]==0

def test_ghz_minimum_record():
    d=SUMMARY['ghz'];assert d['minimum_contexts']==6 and d['ZXY']['globals']==0
    assert sum(d['subsets_exhausted_below_six'].values())==101583

def test_basis_data():
    d=json.loads((ROOT/'data/canonical_bell_basis.json').read_text())
    R=[tuple(x) for x in d['effects_8x8']]
    assert len(R)==64 and all(rank(x)==8 for x in R)
    assert rank([flatten(x,8) for x in R])==64

def test_teleportation_csv_all_rows():
    rows=list(csv.DictReader((ROOT/'data/teleportation_direct_256x64.csv').open()))
    assert len(rows)==16384 and sum(int(r['possible']) for r in rows)==16320
    assert all(r['input']==r['recovered'] and r['exact']=='1' for r in rows)

def test_dense_coding_csv_all_rows():
    rows=list(csv.DictReader((ROOT/'data/dense_coding_64_messages.csv').open()))
    assert len(rows)==64 and all(int(r['decoded_64bit'])==1<<int(r['message']) for r in rows)

def test_resource_rank_coverage():
    rows=list(csv.DictReader((ROOT/'data/all_resource_branch_rank_audit.csv').open()))
    assert sum(int(r['resources_checked']) for r in rows)==4194304
    assert all(r['rank_mismatches']=='0' for r in rows)

def test_local_equivalence_witness():
    d=json.loads((ROOT/'data/equal_rank_class_equivalence.json').read_text())
    assert compose(compose(tuple(d['left_GL8']),tuple(d['M02']),8),tuple(d['right_GL8']),8)==tuple(d['M11'])

def test_activation_witness():
    d=json.loads((ROOT/'data/literal_activation_witness.json').read_text())
    if isinstance(d,list):d=d[0]
    assert SUMMARY['model_boundaries']['02_two_copy_activation']
    assert d['copies']==2 and d['local_dim']==64

def test_restrictions_and_no_cloning():
    assert SUMMARY['model_boundaries']['literal_restricted_subspace_checks']==32640
    assert SUMMARY['model_boundaries']['basis_cloner_failures_out_of_256']==247

def test_orthogonal_no_go_counts():
    d=SUMMARY['orthogonality']
    assert d['necessary_orthogonal_row_condition']==16384 and d['orthogonally_correctable_branch']==0

def test_probability_obstruction():
    d=SUMMARY['probability'];assert not d['strict_positive_support_no_signalling_extension_exists']
    assert d['forced_zero_possible_event_indices']==[4,11,12,19,27,32]

def test_P_T_cannot_preserve_nonzero_bilinear_form():
    assert SUMMARY['algebra']['only_invariant_form_is_zero']

def test_phase_kickback():
    chi=1|(4<<4)
    X=block2(a.Z4,a.I4,a.I4,a.Z4)
    z=block2(a.PP[2],a.Z4,a.Z4,a.PP[2])
    assert apply(X,chi)==apply(z,chi)

def test_all_four_H_Bell_columns_nonseparable():
    H=block2(a.I4,a.NP[2],a.NP[2],a.I4)
    # Reorder H tensor logical identity into logical-branch-major phase coordinates.
    A=[]
    for x,y,p in product(range(2),range(2),range(4)):
        A.append(sum(((H[x*4+p]>>(xx*4+q))&1)<<((2*xx+y)*4+q) for xx,q in product(range(2),range(4))))
    cnot=tuple(1<<((2*x+(x^y))*4+p) for x,y,p in product(range(2),range(2),range(4)))
    B=compose(cnot,tuple(A),16)
    assert rank(B)==16
    analyzer=invert(B)
    effects=[]
    for m in range(4):
        effects.append(tuple(apply(tuple((analyzer[4*m+i]>>(4*j))&15 for i in range(4)),1) for j in range(4)))
    for b,expected in ((0,6),(2,4)):
        for effect in effects:
            rt=(effect[0],effect[2],effect[1],effect[3])
            assert rank(a.resource(a.mat2prod((1,0,0,a.NV[b]),rt)))==expected
    for j in range(4):
        out=apply(B,1<<(4*j));coeff=tuple((out>>(4*i))&15 for i in range(4))
        assert rank(a.resource(coeff))==6
        # A nonzero determinant excludes a simple tensor over the commutative ring.
        assert a.ACT[coeff[0],coeff[3]]^a.ACT[coeff[1],coeff[2]]

def test_nonlinear_coefficient_clone_is_not_forbidden():
    for v in range(256):
        # Ordinary Boolean copying of stored coefficients, then AND, constructs v tensor v.
        out=tuple(((v>>i)&1)&((v>>j)&1) for i,j in product(range(8),repeat=2))
        assert sum(x<<(8*i+j) for (i,j),x in zip(product(range(8),repeat=2),out))==flatten(tuple(v if (v>>i)&1 else 0 for i in range(8)),8)
    # The tensor-copy map itself is not XOR-linear.
    clone=lambda v:flatten(tuple(v if (v>>i)&1 else 0 for i in range(8)),8)
    assert clone(1^2)!=(clone(1)^clone(2))
