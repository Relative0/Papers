"""Fresh, reproducible audit of CM Boolean models. See README for scopes.

All phase products are computed by 4x4 AND/XOR matrix composition. Lookup tables
cache these derived results, not an additional primitive. Counts and LPs are
external diagnostics. Historical modules are not imported.
"""
from pathlib import Path
from itertools import product,combinations,permutations
from collections import Counter,deque
import csv,json,time,hashlib,sys,math
import numpy as np
from boolean_kernel import *
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; LOG=ROOT/'logs'
RESULT={};TIMES={}
def save(name,data): (DATA/name).write_text(json.dumps(data,indent=2)+'\n')
def csvsave(name,rows):
    rows=list(rows)
    with (DATA/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def done(name,data,start):
    RESULT[name]=data;TIMES[name]=time.time()-start;save('audit_summary.json',RESULT);save('audit_timing.json',TIMES)
    print(name,round(TIMES[name],2),flush=True)
I4=ident(4);Z4=(0,)*4;P=(8,1,2,4);K=(1,8,4,2);N=bxor(I4,P)
PP=[power(P,k) for k in range(4)];NP=[power(N,k) for k in range(5)]
OPS=[]
for s in range(16):
    a=Z4
    for k in range(4):
        if (s>>k)&1:a=bxor(a,PP[k])
    OPS.append(a)
OPS=tuple(OPS)
ACT=np.array([[apply(a,apply(b,1)) for b in OPS] for a in OPS],dtype=np.uint8)
CONJ=np.array([apply(trans(a,4),1) for a in OPS],dtype=np.uint8)
UNITS=[i for i,a in enumerate(OPS) if rank(a)==4]
VAL=[next((j for j in range(5) if rank(a)==4-j),None) for a in OPS]
NV=[apply(a,1) for a in NP]
I2=ident(2);X2=(2,1);C2=(1,3)
# Start from the previous logical Bell basis but independently derive its dual.
BELL_STATES=[I2,X2,(3,2),compose((3,2),X2,2)]
Q2=trans(tuple(flatten(x,2) for x in BELL_STATES),4)
A2=invert(Q2);L=[unflatten(r,2,2) for r in A2]
MQT=[((1,0),(0,1)),((1,1),(1,0)),((0,1),(1,1))]
# Definitions use effects [0|,[1|,[0| XOR [1|; no probabilistic inputs.
# The canonical choices matching legacy Z/X/Y are Z=(a,b), X=(a+b,a), Y=(b,a+b).


def phase_entries(a):return tuple((a>>(4*i))&15 for i in range(4))
def resource(e):return block2(OPS[e[0]],OPS[e[1]],OPS[e[2]],OPS[e[3]])
def mat2prod(a,b):
    return tuple(int(ACT[a[2*i],b[j]])^int(ACT[a[2*i+1],b[2+j]]) for i in range(2) for j in range(2))
def canon_effect(e):return min(tuple(int(ACT[t,x]) for x in e) for t in UNITS)
def effects_gate(e):return tuple(sorted((canon_effect(e[:2]),canon_effect(e[2:]))))
def exp_effect(e):return tuple(OPS[e[0]][i]^(OPS[e[1]][i]<<4) for i in range(4))

def algebra():
    t=time.time()
    # 16 truth-table CMs, all assignments, all binary truth-table connectives.
    def f(a,x,y):return (a>>(2*(1-x)+(1-y)))&1
    checks=0
    for a,b,o,x,y in product(range(16),range(16),range(16),range(2),range(2)):
        fused=sum(f(o,(a>>i)&1,(b>>i)&1)<<i for i in range(4))
        assert f(fused,x,y)==f(o,f(a,x,y),f(b,x,y));checks+=1
    for a,b in product(OPS,repeat=2): assert compose(a,b,4)==naive_compose(a,b,4)
    assert power(P,4)==I4 and compose(compose(K,P,4),K,4)==power(P,3)
    assert [rank(a) for a in NP]==[4,3,2,1,0]
    center=[];invariant=[];gl2=[]
    T=(3,2,4,8)
    for packed in range(65536):
        a=unflatten(packed,4,4)
        if compose(a,P,4)==compose(P,a,4):center.append(a)
        if compose(compose(trans(P,4),a,4),P,4)==a and compose(compose(trans(T,4),a,4),T,4)==a:invariant.append(a)
    assert set(center)==set(OPS) and invariant==[Z4]
    for p in range(16):
        a=unflatten(p,2,2)
        if rank(a)==2:
            order=next(k for k in range(1,7) if power(a,k)==I2);gl2.append({'rows':a,'order':order})
    assert len(gl2)==6
    J3=(3,6,4);assert power(J3,4)==ident(3) and power(J3,2)!=ident(3)
    d=NP[2];H=block2(I4,d,d,I4)
    assert compose(H,H,8)==ident(8) and compose(trans(H,8),H,8)==ident(8)
    interfer=[]
    for k in range(4):interfer.append({'k':k,'output_second_branch':1^apply(PP[k],1)})
    # Ordinary 2x2 identity AND/idempotence, separate from lifted N^2.
    assert compose(I2,I2,2)==I2 and compose(d,d,4)==Z4
    done('algebra',{'truth_fusion_checks':checks,'phase_pair_checks':256,'centralizer_scan':65536,'centralizer_count':len(center),'invariant_bilinear_forms_P_T':len(invariant),'only_invariant_form_is_zero':True,'GL2':gl2,'order4_3dim_counterexample':J3,'phase_units':UNITS,'difference_ranks':[rank(a) for a in NP],'interferometer':interfer},t)

GATES=None;ORTH=None;BASES=None;OB=None;ENTRIES=None;MATRICES=None;CLASSES=None

def inventories():
    global GATES,ORTH,BASES,OB,ENTRIES,MATRICES,CLASSES
    t=time.time()
    entries=np.array([phase_entries(i) for i in range(65536)],dtype=np.uint8);ENTRIES=entries
    mats=np.array([resource(e) for e in entries],dtype=np.uint64);MATRICES=mats
    ranks=batch_rank(mats,8)
    # Independent invariant profiles, computed by ordinary 8x8 Boolean products.
    profiles=[ranks]
    canon={}
    for n in NP[1:4]:profiles.append(batch_rank(batch_right_compose(mats,block2(n,Z4,Z4,n),8),8))
    for a in range(5):
        for b in range(a,5):canon[tuple(max(4-a-j,0)+max(4-b-j,0) for j in range(4))]=(a,b)
    cls=[canon[tuple(int(x[i]) for x in profiles)] for i in range(65536)];CLASSES=cls
    counts=Counter(cls)
    inv=[tuple(int(x) for x in e) for e,r in zip(entries,ranks) if r==8];GATES=inv
    orth=[]
    for e in inv:
        m=resource(e)
        if compose(trans(m,8),m,8)==ident(8):orth.append(e)
    ORTH=orth
    bases=sorted({effects_gate(e) for e in inv});BASES=bases
    ob=sorted({effects_gate(e) for e in orth});OB=ob
    assert len(inv)==24576 and len(orth)==512 and len(bases)==192 and len(ob)==4
    monomial=sum(((e[0] in UNITS and e[3] in UNITS and e[1]==e[2]==0) or (e[1] in UNITS and e[2] in UNITS and e[0]==e[3]==0)) for e in inv)
    assert monomial==128
    # Exhaustive shared-module simple tensor set, with zero included.
    product_states=set()
    for a,b,c,d in product(range(16),repeat=4):
        ee=(int(ACT[a,c]),int(ACT[a,d]),int(ACT[b,c]),int(ACT[b,d]))
        product_states.add(sum(x<<(4*i) for i,x in enumerate(ee)))
    assert len(product_states)==5266
    assert all((packed in product_states)==(b==4) for packed,(a,b) in enumerate(cls))
    rows=[]
    for a,b in sorted(counts):
        r=8-a-b
        k=next((k for k in range(1,5) if r**k>=8),None)
        rows.append({'a':a,'b':b,'count':counts[a,b],'literal_rank':r,'shared_separable':int(b==4),'literal_separable_nonzero':int(r==1),'universal_single_copy':int(r==8),'literal_activation_min_copies_rank_bound':k or 'never','shared_max_exact_vectors':256 if b==0 else (16 if a==0 else 1),'literal_max_exact_subspace_vectors':2**r})
    csvsave('class_inventory_audited.csv',rows)
    csvsave('resource_inventory_audited_65536.csv',({'packed':i,'a':a,'b':b,'rank':int(ranks[i]),'profile':':'.join(str(int(x[i])) for x in profiles)} for i,(a,b) in enumerate(cls)))
    csvsave('measurement_bases_audited_192.csv',({'id':i,'e00':e[0][0],'e01':e[0][1],'e10':e[1][0],'e11':e[1][1]} for i,e in enumerate(bases)))
    # Local stabilizers of canonical resources: for each U, count V solving U D V^T = D by brute relation fiber sizes.
    stab=[]
    for a,b in sorted(counts):
        diag=(NV[a],0,0,NV[b]);freq=Counter(mat2prod(diag,(v[0],v[2],v[1],v[3])) for v in inv)
        n=sum(freq[mat2prod(u,diag)] for u in inv) # u^-1 runs over the same group
        assert n*counts[a,b]==24576**2
        stab.append({'a':a,'b':b,'stabilizer_size':n,'orbit_size':counts[a,b]})
    csvsave('local_stabilizers_audited.csv',stab)
    # Two-party basis permutations: exhaustive images of every separable input.
    permrows=[]
    for perm in permutations(range(4)):
        create=0
        for x in product_states:
            y=sum(((x>>(4*j))&15)<<(4*i) for i,j in enumerate(perm))
            create+=int(y not in product_states)
        permrows.append({'permutation':''.join(map(str,perm)),'separable_inputs_becoming_nonseparable':create})
    csvsave('basis_permutation_entanglers.csv',permrows)
    done('inventories',{'all_gates_and_resources':65536,'invertible':len(inv),'orthogonal':len(orth),'monomial':monomial,'nonmonomial_invertible':len(inv)-monomial,'measurement_bases':len(bases),'orthogonal_bases':len(ob),'shared_product_vectors_including_zero':len(product_states),'shared_nonseparable':65536-len(product_states),'literal_nonseparable_in_structured_family':int(np.count_nonzero(ranks>1)),'literal_product_nonzero':int(np.count_nonzero(ranks==1)),'rank_counts':{str(int(k)):int(v) for k,v in Counter(ranks).items()},'permutation_entanglers':sum(r['separable_inputs_becoming_nonseparable']>0 for r in permrows),'stabilizers':stab},t)

# Local MQT settings taken explicitly from row effects, not historical outputs.
Z=((1,0),(0,1)); X=((1,1),(1,0)); Y=((0,1),(1,1))
# These are three ordered dual bases, not complex Pauli observables.


def support_grid(ea,eb,a,b,literal=False):
    e=np.array(ea,dtype=np.uint8);f=np.array(eb,dtype=np.uint8)
    if literal:f=CONJ[f]
    v0=ACT[ACT[e[:,0],NV[a]][:,None],f[:,0][None,:]]
    v1=ACT[ACT[e[:,1],NV[b]][:,None],f[:,1][None,:]]
    return (v0^v1)!=0

def context_tables(bases,a,b,literal=False):
    effects=[e for pair in bases for e in pair]
    g=support_grid(effects,effects,a,b,literal)
    n=len(bases)
    return g.reshape(n,2,n,2).transpose(0,2,1,3).reshape(n,n,4)

def closure_coverage(tabs):
    """Independent bitset Warshall 2SAT, no Tarjan routine from old code."""
    n=tabs.shape[0];V=2*n;size=2*V
    reach=[1<<i for i in range(size)];clauses=0
    for i,j,a,b in product(range(n),range(n),range(2),range(2)):
        if not tabs[i,j,2*a+b]:
            x=2*i+a;y=2*(n+j)+b
            reach[x]|=1<<(y^1);reach[y]|=1<<(x^1);clauses+=1
    for k in range(size):
        bit=1<<k;rk=reach[k]
        for i in range(size):
            if reach[i]&bit:reach[i]|=rk
    sat=all(not ((reach[2*v]>>(2*v+1))&1 and (reach[2*v+1]>>(2*v))&1) for v in range(V))
    possible=int(np.count_nonzero(tabs));uncovered=[]
    if not sat:return {'satisfiable':False,'possible':possible,'extendable':0,'uncovered':possible,'clauses':clauses,'witness':None}
    for i,j,a,b in product(range(n),range(n),range(2),range(2)):
        if not tabs[i,j,2*a+b]:continue
        x=2*i+a;y=2*(n+j)+b
        bad=((reach[x]>>(x^1))&1) or ((reach[y]>>(y^1))&1) or ((reach[x]>>(y^1))&1) or ((reach[y]>>(x^1))&1)
        if bad:uncovered.append((i,j,a,b))
    return {'satisfiable':True,'possible':possible,'extendable':possible-len(uncovered),'uncovered':len(uncovered),'clauses':clauses,'witness':uncovered[0] if uncovered else None}

def brute_coverage(tabs):
    n=len(tabs);goods=[];cover=np.zeros_like(tabs)
    for assignment in product(range(2),repeat=2*n):
        if all(tabs[i,j,2*assignment[i]+assignment[n+j]] for i,j in product(range(n),repeat=2)):
            goods.append(assignment)
            for i,j in product(range(n),repeat=2):cover[i,j,2*assignment[i]+assignment[n+j]]=True
    return len(goods),int(cover.sum())

def contexts():
    global MQT
    t=time.time()
    # The three settings giving the archived outcome convention.
    MQT=[((1,0),(0,1)),((1,1),(1,0)),((0,1),(1,1))]
    # Confirm exact tables by direct numerical-free Boolean matrix effects.
    bell=context_tables(MQT,0,0)
    expected=['1001','1110','0111','1110','0111','1001','0111','1001','1110']
    strings=[''.join(str(int(x)) for x in bell[i,j]) for i,j in product(range(3),repeat=2)]
    # Keep actual convention independent and emit a failure instead of inventing matches.
    assert strings==expected,(strings,expected)
    globals_bell,_=brute_coverage(bell);assert globals_bell==0
    names='ZXY'
    csvsave('bell_tables_audited.csv',({'alice':names[i],'bob':names[j],'support':strings[3*i+j]} for i,j in product(range(3),repeat=2)))
    # Conjugating Bob's basis is an exact relabeling, explaining ALL raw-table differences.
    mapping=[]
    for pair in BASES:
        e=tuple(canon_effect(tuple(int(CONJ[x]) for x in eff)) for eff in pair)
        cp=tuple(sorted(e));mapping.append((BASES.index(cp),int(e[0]!=cp[0])))
    rows=[];checks=0;max_non_signalling=0;classcounts=Counter(CLASSES)
    for a in range(5):
        for b in range(a,5):
            st=context_tables(BASES,a,b,False);li=context_tables(BASES,a,b,True)
            for j,(jj,flip) in enumerate(mapping):
                perm=[2*i+(k^flip) for i in range(2) for k in range(2)]
                assert np.array_equal(li[:,j,:],st[:,jj,:][:,perm])
            sc=closure_coverage(st);lc=closure_coverage(li)
            assert tuple(sc[x] for x in ('satisfiable','possible','extendable','uncovered'))==tuple(lc[x] for x in ('satisfiable','possible','extendable','uncovered'))
            for tabs in (st,li):
                shaped=tabs.reshape(192,192,2,2)
                am=shaped.any(axis=3);bm=shaped.any(axis=2)
                assert np.all(am==am[:,0:1,:]) and np.all(bm==bm[0:1,:,:])
            # Certify symbolic-conjugation shortcut against direct matrices at every effect pair.
            eff=sorted(set(e for pair in BASES for e in pair));g=support_grid(eff,eff,a,b,True)
            m=block2(NP[a],Z4,Z4,NP[b])
            for i,e in enumerate(eff):
                for j,f in enumerate(eff):
                    raw=compose(compose(exp_effect(e),m,8),trans(exp_effect(f),8),4)
                    assert any(raw)==g[i,j];checks+=1
            # Entire small orthogonal setting universe checked with brute force.
            ot=context_tables(OB,a,b);nb,ex=brute_coverage(ot);oc=closure_coverage(ot)
            assert (nb>0)==oc['satisfiable'] and ex==oc['extendable']
            status='ZERO' if a==b==4 else ('STRONG' if not sc['satisfiable'] else ('LOGICAL' if sc['uncovered'] else 'LOCAL'))
            rows.append({'a':a,'b':b,'count':classcounts[a,b],'status_192':status,'possible':sc['possible'],'extendable':sc['extendable'],'uncovered':sc['uncovered'],'different_raw_contexts':int(np.count_nonzero(np.any(st!=li,axis=2))),'orthogonal_global_assignments':nb,'orthogonal_uncovered':oc['uncovered']})
    csvsave('contextuality_audited_15_classes.csv',rows)
    save('bob_conjugation_basis_relabeling.json',mapping)
    done('contextuality',{'bell_all_deterministic_assignments':64,'bell_compatible':0,'basis_pairs_per_class':192**2,'classes':15,'two_models_recomputed':True,'all_class_counts':dict(Counter({s:sum(r['count'] for r in rows if r['status_192']==s) for s in ('STRONG','LOGICAL','LOCAL','ZERO')})),'direct_literal_effect_pairs_checked':checks,'pointwise_table_difference_is_setting_relabeling':True,'modal_no_signalling_checks_pass':True},t)


def ghz():
    t=time.time();rows=[];tables=[]
    # Independent literal tensor construction: full local correlated basis.
    v=sum(1<<(j*64+j*8+j) for j in range(8))
    weights=[]
    vw=0
    for p in range(4):
        vw ^= 1<<(p*64+p*8+p)
        for q in range(4):
            if (apply(NP[2],1<<p)>>q)&1:vw^=1<<((4+p)*64+(4+p)*8+4+q)
    def table_family(state,bases):
        contexts=[]
        for i,j,k in product(range(len(bases)),repeat=3):
            vals=[]
            for e,f,g in product(bases[i],bases[j],bases[k]):
                operator=kron(kron(exp_effect(e),exp_effect(f),8),exp_effect(g),8)
                vals.append(int(apply(operator,state)!=0))
            contexts.append((i,j,k,vals))
        ass=list(product(range(2),repeat=3*len(bases)));masks=[]
        full=(1<<len(ass))-1;valid=full
        for i,j,k,vals in contexts:
            mask=sum(1<<r for r,q in enumerate(ass) if vals[4*q[i]+2*q[len(bases)+j]+q[2*len(bases)+k]])
            masks.append(mask);valid &=mask
        globals=[q for r,q in enumerate(ass) if (valid>>r)&1];poss=0;cov=0
        for i,j,k,vals in contexts:
            for a,b,c in product(range(2),repeat=3):
                if vals[4*a+2*b+c]:
                    poss+=1;cov+=any((q[i],q[len(bases)+j],q[2*len(bases)+k])==(a,b,c) for q in globals)
        return contexts,masks,{'globals':len(globals),'possible':poss,'uncovered':poss-cov}
    contexts,masks,cover=table_family(v,MQT);assert cover['globals']==0
    counts={}
    for n in range(1,6):
        num=0
        for ix in combinations(range(27),n):
            m=(1<<512)-1
            for i in ix:m &=masks[i]
            assert m!=0;num+=1
        counts[n]=num
    witness=None
    for ix in combinations(range(27),6):
        m=(1<<512)-1
        for i in ix:m &=masks[i]
        if m==0:witness=ix;break
    assert witness is not None
    csvsave('ghz_tables_audited.csv',({'A':'ZXY'[i],'B':'ZXY'[j],'C':'ZXY'[k],'support':''.join(map(str,vals))} for i,j,k,vals in contexts))
    _,_,orth=table_family(v,OB);_,_,wz=table_family(vw,MQT);_,_,wo=table_family(vw,OB)
    # All bipartition ranks = 8 for full GHZ, weighted leg variant also nonseparable.
    flats=[]
    for state in (v,vw):
        rs=[]
        for party in range(3):
            a=[0]*8
            for i,j,k in product(range(8),repeat=3):
                if (state>>(i*64+j*8+k))&1:
                    q=(i,j,k);others=[q[x] for x in range(3) if x!=party];a[q[party]] ^=1<<(8*others[0]+others[1])
            rs.append(rank(a))
        flats.append(rs)
    done('ghz',{'ZXY':cover,'minimum_contexts':6,'subsets_exhausted_below_six':counts,'six_context_witness':[[contexts[i][j] for j in range(3)] for i in witness],'orthogonal_family':orth,'weighted_ZXY':wz,'weighted_orthogonal':wo,'bipartition_ranks_full_and_weighted':flats},t)

if __name__=='__main__':
    algebra();inventories();contexts();ghz()
