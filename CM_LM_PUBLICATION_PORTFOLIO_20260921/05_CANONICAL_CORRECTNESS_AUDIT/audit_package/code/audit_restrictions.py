"""Exhaustive checks for the older rotation-linear restricted subtheory."""
import json,time,csv
from itertools import product
from collections import Counter
import numpy as np
import audit_models as a
from boolean_kernel import *
DATA=a.DATA;RESULT=json.loads((DATA/'audit_summary.json').read_text());TIMES=json.loads((DATA/'audit_timing.json').read_text())
def done(k,v,t):
    RESULT[k]=v;TIMES[k]=time.time()-t;a.save('audit_summary.json',RESULT);a.save('audit_timing.json',TIMES);print(k,round(TIMES[k],2),flush=True)

def cm_lm():
    t=time.time()
    def f(c,x,y):return (c>>(2*(1-x)+(1-y)))&1
    pairing=0;alignments=0
    for c,x,y,A,B in product(range(16),range(2),range(2),range(2),range(2)):
        lm=tuple(f(c,u,v) for u,v in ((x,y),(x,1-y),(1-x,y),(1-x,1-y)))
        out=lm[2*(1-A)+(1-B)]
        assert out==f(c,int(A==x),int(y==B));pairing+=1
    for c,fx,fy,sw,x,y in product(range(16),range(2),range(2),range(2),range(2),range(2)):
        def changed(x,y):
            u,v=(y,x) if sw else (x,y)
            return f(c,u^fx,v^fy)
        cc=sum(changed(u,v)<<(2*(1-u)+(1-v)) for u,v in product(range(2),repeat=2))
        assert f(cc,x,y)==changed(x,y);alignments+=1
    assert pairing==256 and alignments==512
    done('CM_LM',{'general_logical_pairing_valuations':pairing,'signed_axis_alignments':alignments,'meaning':'logical truth extraction, not modal outcome postulate','modal_state_nonzero_policy_is_added':True},t)


def shared_hierarchy():
    t=time.time();E=np.array([a.phase_entries(i) for i in range(65536)],dtype=np.uint8)
    ALL=np.array([a.resource(e) for e in E],dtype=np.uint64);rows=[]
    for aa in range(5):
        for bb in range(aa,5):
            D=block2(a.NP[aa],a.Z4,a.Z4,a.NP[bb]);CD=batch_right_compose(ALL,D,8)
            fixed=8-batch_rank(CD^np.array(ident(8),dtype=np.uint64)[None,:],8)
            best=int(np.max(fixed));expected=8 if bb==0 else 4 if aa==0 else 0
            assert best==expected
            # For every possible analyzer row R, T=D R^(block transpose).
            # Row corrections solve an 8-bit system. Image inclusion certifies existence.
            success=[]
            for e in E:
                Rtuple=tuple(map(int,e))
                T=(int(a.ACT[a.NV[aa],e[0]]),int(a.ACT[a.NV[aa],e[2]]),int(a.ACT[a.NV[bb],e[1]]),int(a.ACT[a.NV[bb],e[3]]))
                # Row C times T, presented as a Boolean map on C's two 4-bit selectors.
                Q=a.resource((T[0],T[2],T[1],T[3]));cols=trans(Q,8);r=rank(cols)
                yes=rank(cols+(a.NV[aa],a.NV[bb]<<4))==r
                if yes:
                    residue=sum((int(x).bit_count()&1)<<i for i,x in enumerate(e));success.append(residue)
            maxgood=rank(success);exp=4 if aa==bb else 3 if bb==4 else 2
            assert maxgood==exp,(aa,bb,maxgood,exp)
            rows.append({'a':aa,'b':bb,'corrections_exhausted':65536,'max_fixed_vectors':1<<best,'analyzer_rows_exhausted':65536,'quotient_correctable_rows':len(success),'max_independent_quotient_success_outcomes':maxgood})
    a.csvsave('shared_restricted_and_quotient_exhaustive.csv',rows)
    # Recover a full free line with reversible corrections (repair old projector-only example).
    Rrows=[(1,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1)];tests=0
    for b in range(1,5):
        D=(1,0,0,a.NV[b])
        for R in Rrows:
            T=a.mat2prod(D,(R[0],R[2],R[1],R[3]))
            C=(1,0,int(a.ACT[a.NV[b],R[1]]),1)
            mat=a.resource(C)
            assert rank(mat)==8
            for psi in range(16):
                assert apply(mat,apply(a.resource(T),psi))==psi;tests+=1
    done('shared_hierarchy',{'classes':15,'fixed_state_correction_searches':15*65536,'quotient_analyzer_row_searches':15*65536,'four_outcome_free_line_reversible_checks':tests,'table':rows,'no_activation_scope':'only tensor over rotation algebra and rotation-linear local maps'},t)


def orthogonal_branches():
    t=time.time();valid=0;invertible=0;correctable=0
    # A row of a 4x4 phase-block analyzer consists of four 4x4 operator blocks.
    # Its 4x16 row E must satisfy E E^T = I4 in any orthogonal completion.
    for packed in range(65536):
        e=a.phase_entries(packed)
        row=tuple(a.OPS[e[0]][r]^(a.OPS[e[1]][r]<<4)^(a.OPS[e[2]][r]<<8)^(a.OPS[e[3]][r]<<12) for r in range(4))
        if compose(row,trans(row,16),4)==ident(4):
            valid+=1;Tm=a.resource((e[0],e[2],e[1],e[3]))
            if rank(Tm)==8:
                invertible+=1;C=invert(Tm)
                if compose(trans(C,8),C,8)==ident(8):correctable+=1
    assert (valid,invertible,correctable)==(16384,8192,0)
    # Enumerate ALL GL4 maps and check orthogonal flattening parity.
    orth=[]
    for i in range(65536):
        M=unflatten(i,4,4)
        if compose(trans(M,4),M,4)==ident(4):
            assert sum(x.bit_count() for x in M)%2==0;orth.append(flatten(M,4))
    done('orthogonality',{'shared_outcome_structures_exhausted':65536,'necessary_orthogonal_row_condition':valid,'invertible_branch_among_them':invertible,'orthogonally_correctable_branch':correctable,'O4_count':len(orth),'span_of_flattened_O4':rank(orth),'even_dim_orthogonal_effect_basis_impossible':True,'proof_scope':'complete rank-one Bell analyzer; all branch corrections orthogonal; any invertible resource; no blanket claim about arbitrary instruments'},t)

if __name__=='__main__':cm_lm();shared_hierarchy();orthogonal_branches()
