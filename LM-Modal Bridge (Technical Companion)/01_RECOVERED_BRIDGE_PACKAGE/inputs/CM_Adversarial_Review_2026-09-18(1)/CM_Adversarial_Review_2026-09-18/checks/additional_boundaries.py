"""Additional exact checks: forms and unimodular equal-rank resources.
Run: python additional_boundaries.py
Uses only the fresh independent implementation, not the supplied archive code.
"""
from pathlib import Path
import json, time
import numpy as np
from independent_extensions import Ring, possible_global_from_hyperplanes, binary_rank
out=Path(__file__).resolve().parent
start=time.time()
# All 65536 binary 4x4 matrices, vectorized exact characteristic-two products.
codes=np.arange(65536,dtype=np.uint32)
U=((codes[:,None]>>np.arange(16,dtype=np.uint32))&1).astype(np.uint8).reshape(-1,4,4)
R=np.zeros((4,4),dtype=np.uint8)
for j in range(4):R[(j+1)%4,j]=1
J=(R@R)%2
sp=((U.transpose(0,2,1)@J@U)%2==J).all(axis=(1,2))
V=((np.arange(16)[:,None]>>np.arange(4))&1).astype(np.uint8)
Q=lambda x:(x[...,0]*x[...,2]+x[...,1]*x[...,3])%2
UV=(U@V.T)%2
qp=(Q(UV.transpose(0,2,1))==Q(V)[None,:]).all(axis=1)
# Q preservation implies invertibility since its polar form is nonsingular.
assert sp.sum()==720 and qp.sum()==72
units=[]
for a in range(16):
    T=np.zeros((4,4),dtype=np.uint8);P=np.eye(4,dtype=np.uint8)
    for j in range(4):
        if a>>j&1:T^=P
        P=P@R%2
    if a.bit_count()%2:
        units.append({'coefficient_mask':a,'symplectic':bool(np.array_equal(T.T@J@T%2,J)),
                      'quadratic':bool(np.array_equal(Q((T@V.T%2).T),Q(V)))})
assert all(x['symplectic'] for x in units) and sum(x['quadratic'] for x in units)==4
# Two unimodular 3x3 resources over the original length-four ring.
S=Ring(2,4);rays=S.rays(3);forced=S.forced(rays,3)
examples=[]
for vals,expected in [((0,0,3),False),((0,1,2),True)]:
    supp=S.support(rays,rays,vals)
    witness=possible_global_from_hyperplanes(supp,forced,forced)
    assert bool(witness)==expected
    blocks=[]
    for a in vals:
        # Regular multiplication by u^a in the u-basis.
        B=np.zeros((4,4),dtype=np.uint8)
        for j in range(4-a):B[j+a,j]=1
        blocks.append(B)
    M=np.zeros((12,12),dtype=np.uint8)
    for i,B in enumerate(blocks):M[4*i:4*i+4,4*i:4*i+4]=B
    rank=binary_rank([sum(int(b)<<j for j,b in enumerate(row)) for row in M])
    assert rank==9
    examples.append({'smith_exponents':vals,'unimodular_coefficient_vector':True,
                     'binary_rank':rank,'global_assignment_exists':bool(witness),
                     'class_by_proved_theorem':'strong' if not expected else 'logical_not_strong',
                     'ray_count':len(rays),'hyperplane_count':len(forced),
                     'possible_ray_pairs':int(supp.sum())})
res={'success':True,'all_binary_4x4_search_size':65536,'Sp4_F2_order':int(sp.sum()),
     'split_quadratic_isometry_group_order':int(qp.sum()),'coefficient_units':units,
     'unimodular_rank9_examples':examples,'elapsed_seconds':time.time()-start,
     'qualification':'Global-existence checks use the proved hyperplane lemma; not independent tests of that lemma.'}
(out/'additional_boundaries.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
