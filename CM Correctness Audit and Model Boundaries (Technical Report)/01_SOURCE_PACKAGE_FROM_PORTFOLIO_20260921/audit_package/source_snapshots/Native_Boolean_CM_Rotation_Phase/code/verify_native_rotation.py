#!/usr/bin/env python3
import json
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'data' / 'native_rotation_results.json'

def xor_mat(A,B):
    return [[a^b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]

def mm(A,B):
    n=len(A); m=len(B); p=len(B[0])
    assert len(A[0])==m
    return [[sum((A[i][k] & B[k][j]) for k in range(m)) & 1 for j in range(p)] for i in range(n)]

def mv(A,v):
    return [sum((A[i][k] & v[k]) for k in range(len(v))) & 1 for i in range(len(A))]

def eye(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def zero(n,m): return [[0]*m for _ in range(n)]

def mpow(A,k):
    R=eye(len(A))
    X=A
    while k:
        if k&1: R=mm(R,X)
        X=mm(X,X); k//=2
    return R

def transpose(A): return [list(row) for row in zip(*A)]

def rank2(A):
    A=[row[:] for row in A]
    r=0; cols=len(A[0]); rows=len(A)
    for c in range(cols):
        piv=next((i for i in range(r,rows) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(rows):
            if i!=r and A[i][c]:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1
        if r==rows: break
    return r

def block2(A,B,C,D):
    n=len(A); m=len(A[0]); n2=len(C); m2=len(C[0])
    assert len(B)==n and len(D)==n2 and len(B[0])==len(D[0])
    return [A[i]+B[i] for i in range(n)] + [C[i]+D[i] for i in range(n2)]

def mat_key(A): return tuple(tuple(r) for r in A)

def vec_weight(v): return sum(v)

# CM cyclic coordinate order v(A)=(a,b,d,c) corresponding E0,E1,E2,E3.
P = [
    [0,0,0,1],
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
]
I4=eye(4); Z4=zero(4,4)
K = [ # CM transpose: E1 <-> E3, E0,E2 fixed
    [1,0,0,0],
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
]
P2=mpow(P,2); P3=mpow(P,3); P4=mpow(P,4)
N=xor_mat(P,I4)
Delta=xor_mat(I4,P2)
Omega=xor_mat(xor_mat(I4,P),xor_mat(P2,P3))

# Operator algebra span(I,P,P2,P3), indexed by four-bit mask.
pows=[I4,P,P2,P3]
def op(mask):
    A=zero(4,4)
    for j in range(4):
        if (mask>>j)&1: A=xor_mat(A,pows[j])
    return A
ops=[op(m) for m in range(16)]
assert len({mat_key(A) for A in ops})==16

# Native cyclic-convolution mask computed only as reference to compare operator composition.
def cyclic_mask(a,b):
    out=0
    for k in range(4):
        bit=0
        for r in range(4):
            s=(k-r)%4
            bit ^= ((a>>r)&1) & ((b>>s)&1)
        out |= bit<<k
    return out
composition_matches=True
for a,b in product(range(16), repeat=2):
    if mat_key(mm(ops[a],ops[b])) != mat_key(ops[cyclic_mask(a,b)]):
        composition_matches=False; break

units=[m for m,A in enumerate(ops) if rank2(A)==4]

# Strict 2x2 branch shear: creates a modal superposition-like vector from one basis vector.
C2=[[1,0],[1,1]]
e0=[1,0]; e1=[0,1]
# Enumerate GL2(F2), test whether any reversible 2x2 map splits BOTH basis vectors into weight 2.
gl2=[]
for bits in product([0,1], repeat=4):
    A=[list(bits[:2]),list(bits[2:])]
    if rank2(A)==2: gl2.append(A)
both_split=[A for A in gl2 if vec_weight(mv(A,e0))==2 and vec_weight(mv(A,e1))==2]

# CNOT in ascending branch order 00,01,10,11: |x,y> -> |x, x XOR y>
CNOT=[
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,1],
    [0,0,1,0],
]
# Apply C2 to first bit, i.e. C2 tensor I2.
def kron(A,B):
    return [[A[i][j]&B[r][c] for j in range(len(A[0])) for c in range(len(B[0]))]
            for i in range(len(A)) for r in range(len(B))]
C2_first=kron(C2,eye(2))
ket00=[1,0,0,0]
bell=mv(CNOT,mv(C2_first,ket00))

# 8x8 branch x 4-phase-register constructions.
C8=block2(I4,Z4,I4,I4) # (A,B)->(A,A XOR B)
H8=block2(I4,Delta,Delta,I4)

def controlled_phase(k):
    return block2(I4,Z4,Z4,mpow(P,k))

seed0=[1,0,0,0, 0,0,0,0]
seed1=[0,0,0,0, 1,0,0,0]

def split(v): return (v[:4],v[4:])

shear_interference=[]
for k in range(4):
    out=mv(C8,mv(controlled_phase(k),mv(C8,seed0)))
    b0,b1=split(out)
    shear_interference.append({'k':k,'branch0':b0,'branch1':b1,'branch1_weight':sum(b1)})

symmetric_split=[]
for label,seed in [('0',seed0),('1',seed1)]:
    out=mv(H8,seed); b0,b1=split(out)
    symmetric_split.append({'input_branch':label,'branch0':b0,'branch1':b1})

symmetric_interference=[]
for k in range(4):
    out=mv(H8,mv(controlled_phase(k),mv(H8,seed0)))
    b0,b1=split(out)
    symmetric_interference.append({'k':k,'branch0':b0,'branch1':b1,'branch1_weight':sum(b1)})

results={
  'P':P,
  'P2':P2,
  'P3':P3,
  'P4_is_I':P4==I4,
  'P2_is_not_I':P2!=I4,
  'P_transpose_is_inverse':transpose(P)==P3,
  'transpose_reflection_K':K,
  'K2_is_I':mm(K,K)==I4,
  'KPK_is_P_inverse':mm(mm(K,P),K)==P3,
  'generated_symmetry_group_note':'P and K satisfy P^4=K^2=I and KPK=P^-1 (dihedral D4 relations).',
  'N_P_xor_I':N,
  'N_nilpotency':{
      'N1_nonzero':N!=Z4,
      'N2_nonzero':mpow(N,2)!=Z4,
      'N3_nonzero':mpow(N,3)!=Z4,
      'N4_zero':mpow(N,4)==Z4,
  },
  'Delta_operator_I_xor_P2':Delta,
  'Delta_operator_square_zero':mm(Delta,Delta)==Z4,
  'Omega_operator':Omega,
  'Omega_operator_square_zero':mm(Omega,Omega)==Z4,
  'operator_algebra_size':len({mat_key(A) for A in ops}),
  'operator_algebra_units_count':len(units),
  'operator_algebra_unit_masks':units,
  'operator_composition_matches_cyclic_mask_for_all_256_pairs':composition_matches,
  'strict_branch_shear_C2':C2,
  'C2_squared_is_I':mm(C2,C2)==eye(2),
  'C2_on_e0':mv(C2,e0),
  'C2_on_e1':mv(C2,e1),
  'GL2_F2_count':len(gl2),
  'GL2_maps_splitting_both_basis_vectors_count':len(both_split),
  'bell_from_shear_then_CNOT':bell,
  'bell_expected_1001':bell==[1,0,0,1],
  'C8_squared_is_I':mm(C8,C8)==eye(8),
  'H8_squared_is_I':mm(H8,H8)==eye(8),
  'H8_symmetric_split':symmetric_split,
  'controlled_rotation_shear_interference':shear_interference,
  'controlled_rotation_symmetric_interference':symmetric_interference,
}
OUT.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
