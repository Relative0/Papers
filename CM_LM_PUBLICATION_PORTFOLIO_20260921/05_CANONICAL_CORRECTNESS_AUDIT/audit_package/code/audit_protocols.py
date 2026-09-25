"""Independent protocols, counterexamples, and semantic boundary audit."""
from pathlib import Path
from itertools import product
from collections import deque,Counter
import json,csv,time,random
import numpy as np
from boolean_kernel import *
import audit_models as a
ROOT=a.ROOT;DATA=a.DATA
RESULT=json.loads((DATA/'audit_summary.json').read_text())
TIMES=json.loads((DATA/'audit_timing.json').read_text())
def done(k,v,t):
    RESULT[k]=v;TIMES[k]=time.time()-t;a.save('audit_summary.json',RESULT);a.save('audit_timing.json',TIMES);print(k,round(TIMES[k],2),flush=True)

def full_group_and_bases():
    t=time.time();P=a.P;T=(3,2,4,8);I=ident(4)
    parent={I:(None,'')};todo=deque([I]);gens=[('P',P),('p',power(P,3)),('T',T)]
    while todo:
        m=todo.popleft()
        for name,g in gens:
            new=compose(g,m,4)
            if new not in parent:parent[new]=(m,name);todo.append(new)
    assert len(parent)==20160
    # Canonical, search-free basis: tensor the four logical Bell effects.
    L=a.L;assert all(rank(x)==2 for x in L)
    V=[kron(x,y,2) for x,y in product(L,repeat=2)]
    R=[kron(x,y,4) for x in L for y in V]
    A=tuple(flatten(x,8) for x in R)
    assert rank(A)==64 and all(rank(x)==8 for x in R)
    assert rank(tuple(flatten(x,4) for x in V))==16
    words=[]
    for m in V:
        w=[];cur=m
        while parent[cur][0] is not None:
            prev,n=parent[cur];w.append(n);cur=prev
        w=''.join(w[::-1]);cur=I
        for s in w:cur=compose(dict(gens)[s],cur,4)
        assert cur==m
        words.append(w)
    a.save('canonical_bell_basis.json',{'logical_effects':[list(x) for x in L],'phase_effects':[list(x) for x in V],'phase_synthesis_words':words,'effects_8x8':[list(x) for x in R],'analyzer_rows_64bit':list(A),'bit_order':'least significant bit = column 0; flatten row-major','construction':'R_ijk = L_i tensor L_j tensor L_k'})
    # Validate original saved synthesis words and original protocol exactly, without importing old source.
    old=json.loads((ROOT/'source_snapshots/Independent_Phase_CM_Tensor_Audit/data/phase_bell_effect_basis_16.json').read_text())
    oldV=[]
    for item in old['basis']:
        mat=tuple(int(s,2) for s in item['matrix_rows_binary']);cur=I
        for s in item['synthesis_word']:cur=compose(dict(gens)[s],cur,4)
        assert cur==mat and rank(mat)==4;oldV.append(mat)
    assert rank(tuple(flatten(x,4) for x in oldV))==16
    oldR=[kron(x,y,4) for x in L for y in oldV]
    oldA=tuple(flatten(x,8) for x in oldR);assert rank(oldA)==64
    done('gate_synthesis',{'group_P_T_size':20160,'canonical_phase_basis_rank':16,'old_phase_basis_rank':16,'literal_analyzer_rank':64,'logical_effects':L,'uses_T_not_commuting_with_P':compose(T,P,4)!=compose(P,T,4),'common_nonzero_invariant_bilinear_form':False,'old_synthesis_words_verified':16,'new_max_word_length':max(map(len,words))},t)
    return R,A,oldR,oldA


def direct_branches(M,A):
    """Contract explicit 512x8 prep and 512x512 global analyzer, not formula."""
    prep=tuple((1<<i) if (M[j]>>k)&1 else 0 for i,j,k in product(range(8),repeat=3))
    globalA=kron(A,ident(8),8)
    after=compose(globalA,prep,8)
    return [after[8*m:8*m+8] for m in range(64)]

def teleport_dense(R,A,oldR,oldA):
    t=time.time()
    outputs=[];oldmatch=0
    oldcsv=list(csv.DictReader((ROOT/'source_snapshots/Independent_Phase_CM_Tensor_Audit/data/teleportation_literal_256x64.csv').open()))
    direct=direct_branches(ident(8),A);olddirect=direct_branches(ident(8),oldA)
    for effects,analyzer,branches,name in ((R,A,direct,'canonical'),(oldR,oldA,olddirect,'historical')):
        for m,E in enumerate(effects):
            expected=trans(E,8);assert branches[m]==expected
            corr=invert(branches[m]);assert corr is not None and compose(corr,branches[m],8)==ident(8)
            for psi in range(256):
                recv=apply(branches[m],psi);out=apply(corr,recv);assert out==psi
                if name=='canonical':outputs.append({'input':psi,'outcome':m,'received':recv,'recovered':out,'possible':int(recv!=0),'exact':1})
                else:
                    archived=oldcsv[psi*64+m]
                    assert (recv,out)==(int(archived['received_8bit']),int(archived['corrected_8bit']));oldmatch+=1
    a.csvsave('teleportation_direct_256x64.csv',outputs)
    # Direct matrix identity on arbitrary reference system: C T tensor I = I.
    # Two-dimensional reference is exhaustive over all 2^16 vectors once CT=I.
    refchecks=0
    for m,Tm in enumerate(direct):
        corr=invert(Tm);ct=compose(corr,Tm,8);ext=kron(ct,ident(2),2)
        assert ext==ident(16);refchecks+=1
    # Full rank equality over 65,536 resources and ALL 64 canonical branches.
    mats=np.array([a.resource(a.phase_entries(i)) for i in range(65536)],dtype=np.uint64)
    ranks=batch_rank(mats,8)
    # rank(M^T R^T)=rank(R M): use transpose invariance but explicitly compose R M
    # by transposing resources once and right-composing with each R^T.
    mt=np.array([trans(tuple(map(int,x)),8) for x in mats],dtype=np.uint64)
    counts=[]
    for m,E in enumerate(R):
        tm=batch_right_compose(mt,trans(E,8),8)
        rr=batch_rank(tm,8);assert np.array_equal(rr,ranks)
        counts.append({'outcome':m,'resources_checked':65536,'rank_mismatches':int(np.count_nonzero(rr!=ranks))})
    a.csvsave('all_resource_branch_rank_audit.csv',counts)
    # Direct literal contraction for every canonical resource and deterministic random nonsymmetric resources.
    selected=[]
    for aa in range(5):
        for bb in range(aa,5):selected.append(block2(a.NP[aa],a.Z4,a.Z4,a.NP[bb]))
    rng=random.Random(9172026)
    selected += [a.resource(a.phase_entries(rng.randrange(65536))) for _ in range(16)]
    n=0
    for M in selected:
        dd=direct_branches(M,A)
        for m,E in enumerate(R):
            assert dd[m]==compose(trans(M,8),trans(E,8),8);n+=1
    # Dense coding: encodings R_m acting on first factor of vec(I).
    phi=flatten(ident(8),8);states=[]
    for E in R:
        st=apply(kron(E,ident(8),8),phi);assert st==flatten(E,8);states.append(st)
    B=trans(tuple(states),64);D=invert(B);assert D is not None
    assert len(set(states))==64 and rank(states)==64
    a.csvsave('dense_coding_64_messages.csv',({'message':m,'state_64bit':st,'decoded_64bit':apply(D,st),'exact':int(apply(D,st)==1<<m)} for m,st in enumerate(states)))
    assert all(apply(D,st)==1<<m for m,st in enumerate(states))
    # Audit logical-only analyzer: each 4-outcome block retains sixteen Alice sectors.
    A4=[]
    for m,p,q in product(range(4),range(4),range(4)):
        row=0
        for x,y in product(range(2),repeat=2):
            if (a.A2[m]>>(2*x+y))&1:row^=1<<((4*x+p)*8+4*y+q)
        A4.append(row)
    after=compose(kron(tuple(A4),ident(8),8),tuple((1<<i) if j==k else 0 for i,j,k in product(range(8),repeat=3)),8)
    residual=[]
    for m in range(4):
        maps=[after[(m*16+r)*8:(m*16+r+1)*8] for r in range(16)]
        residual.append({'outcome':m,'distinct_maps':len(set(maps)),'map_ranks':sorted(set(rank(x) for x in maps)),'all_nonzero':all(any(x) for x in maps)})
    # Old shared protocol also verified with explicit 32x8 preparation maps.
    sharedchecks=0
    for psi in range(256):
        for Lm in a.L:
            Tm=kron(trans(Lm,2),ident(4),4);C=invert(Tm)
            assert apply(C,apply(Tm,psi))==psi;sharedchecks+=1
    done('protocols',{'shared_checks_including_null':sharedchecks,'literal_checks_new':16384,'literal_checks_historical_recomputed':oldmatch,'nonzero_input_outcome_checks_per_protocol':255*64,'null_checks':64,'direct_tensor_formula_checks':n,'all_resource_branch_ranks_checks':65536*64,'full_rank_structured_resources':int(np.count_nonzero(ranks==8)),'dense_messages':64,'dense_state_rank':64,'reference_identity_maps_checked':refchecks,'logical_only_failure':residual,'analyzer_orthogonal':compose(trans(A,64),A,64)==ident(64),'orthogonal_corrections_count':sum(compose(trans(invert(trans(x,8)),8),invert(trans(x,8)),8)==ident(8) for x in R)},t)


def model_boundary_counterexamples(R,A):
    t=time.time();rows=[];witnesses=[]
    # Shared tensor over phase algebra can annihilate two nonzero preparations.
    x=a.NV[3];y=a.NV[1];shared=int(a.ACT[x,y]);literal=0
    for i,j in product(range(4),repeat=2):
        if ((x>>i)&1) and ((y>>j)&1):literal ^=1<<(4*i+j)
    assert x and y and not shared and literal
    # Under full Boolean GL, all equal-rank resources are locally equivalent.
    M02=block2(a.I4,a.Z4,a.Z4,a.NP[2]);M11=block2(a.NP[1],a.Z4,a.Z4,a.NP[1])
    r,U,V,D=row_col_normal_form(M02,8);s,Us,Vs,Ds=row_col_normal_form(M11,8)
    assert r==s==6 and D==Ds
    left=compose(invert(Us),U,8);right=compose(V,invert(Vs),8)
    assert compose(compose(left,M02,8),right,8)==M11
    eq={'M02':M02,'M11':M11,'left_GL8':left,'right_GL8':right,'equation':'left M02 right = M11'}
    # Finite-copy activation via local invertibles and one heralded coordinate filter.
    for aa in range(5):
        for bb in range(aa,5):
            M=block2(a.NP[aa],a.Z4,a.Z4,a.NP[bb]);rank1=rank(M)
            if rank1<2:
                rows.append({'a':aa,'b':bb,'rank':rank1,'copies':'none','resource_power_rank':rank1,'extracted_I8':0});continue
            k=next(k for k in range(1,4) if rank1**k>=8)
            mm=M;dim=8
            for _ in range(k-1):mm=kron(mm,M,8);dim*=8
            rp,uu,vv,dd=row_col_normal_form(mm,dim)
            assert rp==rank1**k
            # Filtering onto first 8 basis coordinates on both local systems.
            J=tuple(1<<i for i in range(8)) # 8 x dim
            FA=compose(J,uu,dim);FB=compose(J,trans(vv,dim),dim)
            extracted=compose(compose(FA,mm,dim),trans(FB,dim),8)
            assert extracted==ident(8)
            rows.append({'a':aa,'b':bb,'rank':rank1,'copies':k,'resource_power_rank':rp,'extracted_I8':1})
            if (aa,bb)==(0,2):
                witnesses.append({'class':[aa,bb],'copies':k,'local_dim':dim,'original_resource_rows':M,'Alice_filter_rows':FA,'Bob_filter_rows':FB,'extracted_rows':extracted,'note':'Each 8x64 filter is first-8 coordinate selection after an invertible local 64x64 map.'})
    a.csvsave('literal_finite_copy_activation.csv',rows);a.save('literal_activation_witness.json',witnesses);a.save('equal_rank_class_equivalence.json',eq)
    # Restricted-state correction is possible on all r-dimensional inputs under full GL.
    # Canonical resource diag(I_r,0); construct 64 effect rows with invertible top-left r block.
    restricted=[]
    for r in range(1,9):
        piv={};effects=[]
        def admit(M):
            v=flatten(M,8);q=v
            while q:
                p=q.bit_length()-1
                if p in piv:q ^=piv[p]
                else:piv[p]=q;effects.append(M);return True
            return False
        # Build an invertible basis of r x r matrix space without random dependence.
        small=[];spiv={}
        def adm_small(M):
            q=flatten(M,r)
            while q:
                p=q.bit_length()-1
                if p in spiv:q^=spiv[p]
                else:spiv[p]=q;small.append(M);return
        adm_small(ident(r))
        for i,j in product(range(r),repeat=2):
            if i!=j:
                m=list(ident(r));m[i]^=1<<j;adm_small(tuple(m))
        # Permutation matrices and short products complete the diagonal directions.
        if r>1:
            for i in range(r):
                for j in range(r):
                    if i==j:continue
                    m=list(ident(r));m[i],m[j]=m[j],m[i];adm_small(tuple(m))
                    m[i]^=m[j];adm_small(tuple(m))
        assert len(small)==r*r
        for m in small:admit(tuple(m)+(0,)*(8-r))
        base=tuple(ident(r))+(0,)*(8-r)
        for i,j in product(range(8),repeat=2):
            if i<r and j<r:continue
            mm=list(base);mm[i]^=1<<j;admit(tuple(mm))
        assert len(effects)==64
        D=tuple((1<<i) if i<r else 0 for i in range(8));total=0
        for E in effects:
            Tm=compose(D,trans(E,8),8)
            smallT=tuple(Tm[i]&((1<<r)-1) for i in range(r));ci=invert(smallT);assert ci is not None
            C=tuple(ci)+tuple(1<<i for i in range(r,8));assert rank(C)==8
            for psi in range(1<<r):assert apply(C,apply(Tm,psi))==psi;total+=1
        restricted.append({'rank':r,'analyzer_rank':rank(tuple(flatten(e,8) for e in effects)),'nonzero_exact_subspace_states':(1<<r)-1,'checks_including_zero':total})
    a.csvsave('literal_restricted_subspaces.csv',restricted)
    # No-cloning: a fixed linear copier on basis vectors fails every nontrivial sum.
    clone=tuple((1<<i) if i==j else 0 for i,j in product(range(8),repeat=2))
    failures=0
    for x in range(256):
        desired=sum(1<<(8*i+j) for i,j in product(range(8),repeat=2) if ((x>>i)&1) and ((x>>j)&1))
        if apply(clone,x)!=desired:failures+=1
    assert failures==247
    # P-compatible invertible encodings span only a 16-dimensional space, not 64.
    all_inv=[]
    for packed in range(65536):
        m=a.resource(a.phase_entries(packed))
        if rank(m)==8:all_inv.append(flatten(m,8))
    assert rank(all_inv)==16
    done('model_boundaries',{'shared_nonzero_product_null_counterexample':{'x':a.NV[3],'y':a.NV[1],'shared_result':shared,'literal_result_nonzero':literal},'equal_rank_02_11_equivalence_verified':True,'02_two_copy_activation':True,'activation_rows':rows,'literal_restricted_subspace_checks':sum(z['checks_including_zero'] for z in restricted),'basis_cloner_failures_out_of_256':failures,'P_block_dense_encoding_span':16,'full_dense_encoding_span':64,'no_bilinear_form_can_preserve_all_P_T_gates':True},t)


def probability_audit():
    """External real-valued LP diagnostics; not Boolean state evolution."""
    t=time.time();from scipy.optimize import linprog
    mqt=[((1,0),(0,1)),((1,1),(1,0)),((0,1),(1,1))]
    tabs=a.context_tables(mqt,0,0);n=36
    def ix(i,j,x,y):return 4*(3*i+j)+2*x+y
    eq=[];rhs=[]
    for i,j in product(range(3),repeat=2):
        row=[0]*n
        for x,y in product(range(2),repeat=2):row[ix(i,j,x,y)]=1
        eq.append(row);rhs.append(1)
    for i,x,j in product(range(3),range(2),range(1,3)):
        row=[0]*n
        for y in range(2):row[ix(i,j,x,y)]+=1;row[ix(i,0,x,y)]-=1
        eq.append(row);rhs.append(0)
    for j,y,i in product(range(3),range(2),range(1,3)):
        row=[0]*n
        for x in range(2):row[ix(i,j,x,y)]+=1;row[ix(0,j,x,y)]-=1
        eq.append(row);rhs.append(0)
    bounds=[(0,None) if tabs[i,j,2*x+y] else (0,0) for i,j,x,y in product(range(3),range(3),range(2),range(2))]
    # Maximize minimal positive probability across all modal-possible events.
    E=np.c_[np.array(eq,float),np.zeros(len(eq))];ub=[]
    for i,b in enumerate(bounds):
        if b[1] is None:
            row=[0]*(n+1);row[i]=-1;row[-1]=1;ub.append(row)
    objective=[0]*n+[-1]
    lp=linprog(objective,A_ub=np.array(ub),b_ub=np.zeros(len(ub)),A_eq=E,b_eq=rhs,bounds=bounds+[(0,None)],method='highs')
    maxima=[]
    for i,b in enumerate(bounds):
        if b[1] is None:
            ob=[0]*n;ob[i]=-1
            rr=linprog(ob,A_eq=eq,b_eq=rhs,bounds=bounds,method='highs');assert rr.success
            maxima.append({'event_index':i,'max_probability':float(-rr.fun)})
    forced=[x['event_index'] for x in maxima if abs(x['max_probability'])<1e-9]
    a.save('external_probability_LP.json',{'external_not_CM_evolution':True,'support':tabs.astype(int).tolist(),'max_min_probability':float(lp.x[-1]),'forced_zero_possible_event_indices':forced,'per_event_maxima':maxima,'weak_resolution':lp.x[:-1].tolist(),'equality_matrix':eq,'rhs':rhs})
    assert lp.success and abs(lp.x[-1])<1e-9 and len(forced)>0
    # Exact symbolic solution with positivity implications recorded for the PDF.
    import sympy as sp
    vars=sp.symbols('p0:36');zs=[i for i,b in enumerate(bounds) if b==(0,0)]
    equations=[sum(sp.Integer(c)*v for c,v in zip(row,vars))-b for row,b in zip(eq,rhs)]+[vars[i] for i in zs]
    sol=sp.linsolve(equations,vars)
    a.save('probability_exact_affine_constraints.json',{'variables':[str(x) for x in vars],'solution':str(sol),'forced_possible_events':forced})
    done('probability',{'external_LP_not_state_dynamics':True,'modal_non_signalling_support':True,'strict_positive_support_no_signalling_extension_exists':False,'forced_zero_possible_event_indices':forced,'max_min_probability':float(lp.x[-1]),'exact_affine_solution':str(sol)},t)

if __name__=='__main__':
    R,A,oldR,oldA=full_group_and_bases()
    teleport_dense(R,A,oldR,oldA)
    model_boundary_counterexamples(R,A)
    probability_audit()
