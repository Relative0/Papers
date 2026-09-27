#!/usr/bin/env python3
"""Symbolic valuation -> reversible Boolean oracle checks, tensor counterexamples,
and phase/Fourier rank ablations. All arithmetic exact, no supplied code imports.
"""
import laboratory as L
from laboratory import *

def lm_oracles():
    rows=[];pairings=oracles=0
    for mask in range(16):
        # Storage bit x+2*y. Conversion to Paper B true-first CM is explicit.
        f=lambda x,y:(mask>>(x+2*y))&1
        CM=((f(1,1),f(1,0)),(f(0,1),f(0,0)))
        coeff=(f(0,0),f(1,0)^f(0,0),f(0,1)^f(0,0),f(0,0)^f(1,0)^f(0,1)^f(1,1))
        for X,Y,A,B in product(range(2),repeat=4):
            LM=((f(X,Y),f(X,1-Y)),(f(1-X,Y),f(1-X,1-Y)))
            assert LM[1-A][1-B]==f(int(A==X),int(Y==B));pairings+=1
            if X==Y==1:assert LM==CM
        cols=[]
        for x,y,t in product(range(2),repeat=3):
            computed=t^coeff[0]^(coeff[1]&x)^(coeff[2]&y)^(coeff[3]&x&y)
            assert computed==t^f(x,y);oracles+=1
            cols.append((x+2*y+4*t,x+2*y+4*computed))
        perm=tuple(1<<next(i for i,j in cols if j==o) for o in range(8))
        assert compose(perm,perm)==eye(8)
        rows.append({'truth_mask_x_plus_2y':mask,'true_first_CM':str(CM),'ANF_const_x_y_xy':str(coeff),'oracle_binary_rows':str(perm),'Toffoli_required_in_this_ANF_compiler':coeff[3]})
    csvsave('lm_reversible_oracles.csv',rows)
    return {'CM_tokens':16,'LM_pairing_valuations':pairings,'reversible_oracle_basis_cases':oracles,'oracle_state_dimension':8,'ancillas':0,'gate_set':'NOT, CNOT, Toffoli; ANF compilation only for these two-input functions','output':'lm_reversible_oracles.csv'}

def phase_fourier():
    # Four-level cyclic target T on A^4; eigenvector chi_j=R^{-j}.
    R=3;chi=tuple(pwr(R,(-j)%4) for j in range(4));cases=0
    for c,f in product(range(16),range(2)):
        v=tuple(MUL[c][z] for z in chi);out=v[-1:]+v[:-1] if f else v
        assert out==tuple(MUL[MUL[c][R if f else 1]][z] for z in chi);cases+=1
    ranks=[]
    for n in range(1,7):
        N=1<<n;z=5
        # Walsh-like matrix over A, H[s,x]=z^(s dot x).
        A=[[z if parity(s&x) else 1 for x in range(N)] for s in range(N)]
        binary=tuple(sum(REG[A[i][j]][k]<<(4*j) for j in range(N)) for i in range(N) for k in range(4))
        r=rank(binary);assert r==4+2*n
        columns=tuple(sum(A[s][x]<<(4*s) for s in range(N)) for x in range(N))
        assert rank(columns)==n+1
        ranks.append({'n':n,'ring_matrix_dimension':N,'binary_matrix_dimension':4*N,'binary_rank':r,'F2_span_of_unit_amplitude_phase_columns':rank(columns)})
    # Standard bit-flip cannot kick back R on any primitive A^2 eigenvector.
    primitive=good=0
    for a,b in product(range(16),repeat=2):
        if (a|b)&1:
            primitive+=1
            good+=int((b,a)==(MUL[R][a],MUL[R][b]))
    assert primitive==192 and good==0
    save('new_phase_fourier.json',{'four_level_R_kickback_eigenvector':chi,'four_level_kickback_cases':cases,'oracle_contract':'pointwise controlled cyclic increment by f(x), not the standard Boolean XOR oracle','primitive_R_eigenvectors_of_standard_bit_flip':good,'primitive_vectors_checked':primitive,'Walsh_R_squared_ranks':ranks,'factorization_warning':'R^(a xor b) != R^a R^b when a=b=1; R^2 is not 1.'})
    return {'four_level_kickback_cases':cases,'primitive_eigenvectors_checked':primitive,'Walsh_n_range':[1,6],'algorithm':'exact phase identities and binary ranks; closed-form Smith proof in report','output':'new_phase_fourier.json'}

def tensor_counterexamples():
    a=(8,0);b=(2,0);shared=tuple(MUL[x][y] for x in a for y in b)
    literal=vector_tensor(8,2,8)
    assert shared==(0,0,0,0) and literal!=0
    M=(1,0,0,2);conditioned=(0,2)
    assert any(x&1 for x in M) and conditioned!=(0,0) and not any(x&1 for x in conditioned)
    product_shared=(1,0,0,0);assert rank(lift(product_shared))==4
    save('independent_tensor_counterexamples.json',{'nonzero_preparations_u':{'Alice':a,'Bob':b},'shared_tensor_u':shared,'literal_tensor_bitset':literal,'primitive_joint_state_u':M,'nonprimitive_nonzero_conditioned_state_u':conditioned,'shared_product_literal_entangled_u':product_shared,'literal_rank_of_shared_product':4})
    return {'counterexamples':3,'gate_or_measurement':'standard second-coordinate effect for conditioning witness','output':'independent_tensor_counterexamples.json'}


def description_readout_ablation():
    # A deliberately DIFFERENT readout contract: inspect classical coefficients.
    # The simulator evaluates f at every address, not once as a classical oracle.
    def vector_oracle_state(n, truth):
        N=1<<n
        return sum(1<<(x+N*((truth>>x)&1)) for x in range(N))
    rows=[]
    for n in range(1,5):
        N=1<<n;mask=(1<<N)-1;count=0
        promises=[0,mask]+[sum(1<<x for x in subset) for subset in combinations(range(N),N//2)]
        for truth in promises:
            state=vector_oracle_state(n,truth)
            recovered=(state>>N)&mask
            assert recovered==truth
            constant=recovered in (0,mask)
            assert constant==(truth in (0,mask));count+=1
        rows.append({'task':'Deutsch-Jozsa with CLASSICAL coefficient access','n':n,'promised_functions':count,'abstract_vector_oracle_calls':1,'simulator_point_evaluations_per_function':N,'coefficient_bits_available':2*N})
    for n in range(1,9):
        N=1<<n
        for secret in range(N):
            truth=sum(parity(secret&x)<<x for x in range(N))
            state=vector_oracle_state(n,truth)
            recovered=sum(((state>>(N+(1<<j)))&1)<<j for j in range(n))
            assert recovered==secret
        rows.append({'task':'BV with CLASSICAL coefficient access','n':n,'promised_functions':N,'abstract_vector_oracle_calls':1,'simulator_point_evaluations_per_function':N,'coefficient_bits_available':2*N})
    for truth in range(4):
        state=vector_oracle_state(1,truth)
        assert (((state>>2)&1)^((state>>3)&1))==parity(truth)
    save('description_readout_ablation.json',{'scope':'Not modal measurement. Oracle action is standard U_f but its entire output coefficient description is inspectable. A classical machine with the same batch-vector interface has the same access; no point-query advantage is established.','Deutsch_truth_functions':4,'campaigns':rows})
    return {'Deutsch_functions':4,'DJ_functions':sum(r['promised_functions'] for r in rows if r['task'].startswith('Deutsch')),'BV_hidden_strings':sum(r['promised_functions'] for r in rows if r['task'].startswith('BV')),'readout_contract':'classical full coefficient inspection, NOT complete modal readout','algorithm':'standard oracle permutation plus classical coefficient extraction; all promised cases in stated n ranges','output':'description_readout_ablation.json'}

if __name__=='__main__':
    L.METRIC_FILE='bridge_phase_metrics.json'
    for name,fn in [('LM_oracles',lm_oracles),('phase_Fourier',phase_fourier),('tensor_boundaries',tensor_counterexamples),('description_readout_ablation',description_readout_ablation)]:L.timed(name,fn)
