#!/usr/bin/env python3
"""Independent finite Boolean/modal laboratory. Python 3.10+, standard library only.
Not imported from supplied artifacts. A elements use polynomial u coefficients,
not the supplied implementation's R coefficients. Rows of binary matrices are
integers, with bit j the coefficient of input j. No stochastic sampling is used.
"""
from itertools import product, combinations
from collections import Counter, deque
from pathlib import Path
import json, csv, time, platform, sys
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
METRICS={}
METRIC_FILE="independent_metrics.json"
def save(name,obj):
    (DATA/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def csvsave(name,rows):
    rows=list(rows)
    with (DATA/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def timed(name,fn):
    t=time.perf_counter(); result=fn(); seconds=time.perf_counter()-t
    METRICS[name]={'seconds':seconds,**result};save(METRIC_FILE,METRICS)
    print(name,round(seconds,4),json.dumps(result),flush=True)
def parity(x):return x.bit_count()&1
def rank(vectors):
    piv={}
    for x in vectors:
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    return len(piv)
def eye(n):return tuple(1<<i for i in range(n))
def apply(M,v):return sum(parity(row&v)<<i for i,row in enumerate(M))
def transpose(M,n=None):
    n=len(M) if n is None else n
    return tuple(sum(((row>>j)&1)<<i for i,row in enumerate(M)) for j in range(n))
def compose(M,N):
    return tuple(xors(N[j] for j in range(len(N)) if (r>>j)&1) for r in M)
def xors(xs):
    r=0
    for x in xs:r^=int(x)
    return r
def inverse(M):
    n=len(M);r=[M[i]|(1<<(n+i)) for i in range(n)]
    for j in range(n):
        p=next((i for i in range(j,n) if (r[i]>>j)&1),None)
        if p is None:raise ValueError('singular binary matrix')
        r[j],r[p]=r[p],r[j]
        for i in range(n):
            if i!=j and (r[i]>>j)&1:r[i]^=r[j]
    return tuple(a>>n for a in r)
def flatten(M,n=None):
    n=len(M) if n is None else n
    return sum(a<<(i*n) for i,a in enumerate(M))
def unflatten(x,n):return tuple((x>>(i*n))&((1<<n)-1) for i in range(n))
def kron(A,B):
    n=len(B);return tuple(sum(b<<(n*j) for j in range(len(A)) if (a>>j)&1) for a in A for b in B)
def vector_tensor(v,w,n):return xors(w<<(i*n) for i in range(v.bit_length()) if (v>>i)&1)
def mul(a,b):return xors((a<<j)&15 for j in range(4) if (b>>j)&1)
MUL=tuple(tuple(mul(a,b) for b in range(16)) for a in range(16))
def val(a):return 4 if a==0 else ((a&-a).bit_length()-1)
UNITS=tuple(range(1,16,2)); INVS={a:next(b for b in UNITS if MUL[a][b]==1) for a in UNITS}
def pwr(a,n):
    r=1
    for _ in range(n):r=MUL[r][a]
    return r
def amat(a,b):
    return tuple(MUL[a[2*i]][b[j]]^MUL[a[2*i+1]][b[2+j]] for i in range(2) for j in range(2))
def at(a):return (a[0],a[2],a[1],a[3])
def ainv(a):
    det=MUL[a[0]][a[3]]^MUL[a[1]][a[2]]
    if not det&1:raise ValueError('nonunit determinant')
    z=INVS[det];return tuple(MUL[z][v] for v in (a[3],a[1],a[2],a[0]))
def avec(a,v):return (MUL[a[0]][v[0]]^MUL[a[1]][v[1]],MUL[a[2]][v[0]]^MUL[a[3]][v[1]])
def regular(a):return transpose(tuple(MUL[a][1<<j] for j in range(4)))
REG=tuple(regular(a) for a in range(16))
def lift(a):return tuple(REG[a[2*i]][k]|(REG[a[2*i+1]][k]<<4) for i in range(2) for k in range(4))
def canon_ray(v):return min(tuple(MUL[t][x] for x in v) for t in UNITS)
GATES=[]; BASES=[]; RAYS=[]; COUNTS={}

def inventory():
    global GATES,BASES,RAYS,COUNTS
    allstates=list(product(range(16),repeat=2))
    products={tuple(MUL[x][y] for x in a for y in b) for a in allstates for b in allstates}
    rec=[];c=Counter()
    for a in product(range(16),repeat=4):
        br=rank(lift(a)); lo=min(map(val,a)); hi=8-br-lo
        assert lo<=hi<=4
        key=(lo,hi);c[key]+=1
        assert (a in products)==(hi==4)
        if (MUL[a[0]][a[3]]^MUL[a[1]][a[2]])&1:
            GATES.append(a);assert br==8
        rec.append({'u_entries':','.join(map(str,a)),'a':lo,'b':hi,'binary_rank':br,'shared_product_including_zero':int(hi==4),'literal_product_including_zero':int(br<=1)})
    RAYS=sorted({canon_ray(v) for v in allstates if any(x&1 for x in v)})
    BASES=sorted({tuple(sorted((canon_ray(a[:2]),canon_ray(a[2:])))) for a in GATES})
    assert len(GATES)==24576 and len(RAYS)==24 and len(BASES)==192
    assert len(products)==5266
    COUNTS=dict(c)
    csvsave('independent_resource_inventory.csv',rec)
    csvsave('independent_smith_counts.csv',[{'a':a,'b':b,'resources':n,'binary_rank':8-a-b} for (a,b),n in sorted(c.items())])
    csvsave('independent_measurements.csv',[{'id':i,'rows':str(b)} for i,b in enumerate(BASES)])
    save('independent_gate_and_ray_sets.json',{'gates_u':GATES,'rays_u':RAYS,'bases_u':BASES})
    return {'states_A2_including_zero':256,'resources_including_zero':65536,'gates':len(GATES),'rays':len(RAYS),'measurements':len(BASES),'shared_nonzero_products':5265,'literal_nonzero_products_in_structured_family':sum(n for (a,b),n in c.items() if 8-a-b==1),'algorithm':'polynomial multiplication; independent binary Gaussian rank; 65536 outer products','output':'independent_resource_inventory.csv'}

def support_classification():
    # Variable = one binary setting; literal node 2*v+outcome. A forbidden pair
    # gives implications (A=i)->(B=1-j) and conversely. Bitset Warshall closure.
    n=len(BASES); nv=2*n; nn=2*nv; even=sum(1<<(2*i) for i in range(nv));odd=even<<1
    def conflict(mask):return bool(((mask&even)<<1)&mask)
    results=[]
    for a,b in combinations(range(6),2):
        # combinations shifted gives every 0<=a<=b<=4 exactly once
        b-=1
        p=0 if a==4 else 1<<a;q=0 if b==4 else 1<<b
        if p==q==0:continue
        dots={(r,t):MUL[MUL[r[0]][p]][t[0]]^MUL[MUL[r[1]][q]][t[1]] for r in RAYS for t in RAYS}
        reach=[1<<i for i in range(nn)];events=[];forbidden=0
        for bi,B in enumerate(BASES):
            for ci,C in enumerate(BASES):
                for i,j in product(range(2),repeat=2):
                    x=2*bi+i;y=2*(n+ci)+j
                    if dots[B[i],C[j]]:events.append((x,y))
                    else:
                        reach[x]|=1<<(y^1);reach[y]|=1<<(x^1);forbidden+=1
        for k in range(nn):
            bit=1<<k;rk=reach[k]
            for i in range(nn):
                if reach[i]&bit:reach[i]|=rk
        strong=any(reach[2*i]&(1<<(2*i+1)) and reach[2*i+1]&(1<<(2*i)) for i in range(nv))
        unextended=len(events) if strong else sum(conflict(reach[x]|reach[y]) for x,y in events)
        category='strong' if strong else 'logical_not_strong' if unextended else 'local'
        expect='local' if b==4 else 'strong' if a==b else 'logical_not_strong'
        assert category==expect,(a,b,category)
        results.append({'a':a,'b':b,'contexts':n*n,'possible_events':len(events),'forbidden_pairs':forbidden,'unextendable_events':unextended,'classification':category,'resources':COUNTS[a,b]})
    csvsave('independent_contextuality.csv',results)
    return {'nonzero_smith_classes':14,'resources_covered':65535,'measurements_per_party':192,'contexts_per_class':36864,'boolean_variables':384,'algorithm':'2-SAT implication transitive closure plus every supported two-literal extension','classification_totals':dict(Counter({k:sum(r['resources'] for r in results if r['classification']==k) for k in ('local','logical_not_strong','strong')})),'output':'independent_contextuality.csv'}

def small_bell_ghz():
    bases=((1,2),(3,1),(2,3)) # Z,X,Y effect rows
    bt=[]
    for B,C in product(bases,repeat=2):bt.append(tuple(parity(r&t) for r,t in product(B,C)))
    glob=[]
    for a in product(range(2),repeat=6):
        if all(bt[3*i+j][2*a[i]+a[3+j]] for i,j in product(range(3),repeat=2)):glob.append(a)
    assert not glob
    gt=[]
    for B,C,D in product(bases,repeat=3):gt.append(tuple(parity(r&s&t) for r,s,t in product(B,C,D)))
    gg=[]
    for a in product(range(2),repeat=9):
        if all(gt[9*i+3*j+k][4*a[i]+2*a[3+j]+a[6+k]] for i,j,k in product(range(3),repeat=3)):gg.append(a)
    assert not gg and sum(map(sum,gt))==112
    save('independent_bell_ghz.json',{'basis_effect_rows':bases,'bell_support':bt,'bell_globals':glob,'ghz_support':gt,'ghz_globals':gg})
    return {'Bell_states':1,'Bell_measurements_per_site':3,'Bell_contexts':9,'Bell_assignments_enumerated':64,'GHZ_states':1,'GHZ_contexts':27,'GHZ_assignments_enumerated':512,'GHZ_possible_events':112,'output':'independent_bell_ghz.json'}

def exact_protocols():
    L=((2,3),(1,3),(2,1),(1,2))
    assert all(rank(t)==2 for t in L) and rank([flatten(t) for t in L])==4
    rec=[]
    for d in (2,8):
        E=L if d==2 else tuple(kron(kron(a,b),c) for a,b,c in product(L,repeat=3))
        analyzer=tuple(flatten(t) for t in E);assert rank(analyzer)==d*d
        wordcols=[flatten(t) for t in E]
        decoder=inverse(transpose(tuple(wordcols)))
        checks=0
        for m,t in enumerate(E):
            branch=transpose(t);correction=inverse(branch)
            assert compose(correction,branch)==eye(d)
            for v in range(1<<d):assert apply(correction,apply(branch,v))==v;checks+=1
            assert apply(decoder,wordcols[m])==1<<m
            # entanglement-swapping coefficient E, correction inverse on Alice
            assert compose(inverse(t),t)==eye(d)
        rec.append({'d':d,'input_vectors_including_zero':1<<d,'analyzer_effects':d*d,'direct_input_branch_checks':checks,'dense_messages':d*d,'swapping_branches':d*d})
    # Shared A^2: same four ring-valued effects, using u coefficient representation.
    checksA=0
    for t in L:
        tA=tuple((t[i]>>j)&1 for i in range(2) for j in range(2)); branch=at(tA);correction=ainv(branch)
        for v in product(range(16),repeat=2):assert avec(correction,avec(branch,v))==v;checksA+=1
    save('independent_protocols.json',{'invertible_matrix_basis_F2_2':L,'literal_tests':rec,'shared_input_branch_checks':checksA})
    return {'literal_dimensions':[2,8],'literal_input_branch_checks':sum(r['direct_input_branch_checks'] for r in rec),'shared_input_branch_checks':checksA,'resources':'identity in each carrier; all branch maps checked as identities','gates':'displayed complete invertible-matrix bases; inverse corrections','output':'independent_protocols.json'}

def dense_resource_capacities():
    rows=[];witnesses=[]
    for a in range(4):
        for b in range(a,5):
            M=(1<<a,0,0,0 if b==4 else 1<<b);r=8-a-b;h=2 if a==b else 1
            words=[amat(g,M) for g in GATES]
            # Whole literal codeword span: expanded 8x8 matrix vectorization.
            literal_span=rank(flatten(lift(w)) for w in words)
            assert literal_span==2*r,(a,b,literal_span)
            # Dividing a chosen representative by u^a gives a primitive vector;
            # residue independence gives extendibility to an A-basis (Nakayama).
            selected=[];rs=[]
            for g,w in zip(GATES,words):
                quot=tuple(x>>a for x in w);red=sum((x&1)<<i for i,x in enumerate(quot))
                if rank(rs+[red])>len(rs):selected.append((g,quot));rs.append(red)
                if len(rs)==2*h:break
            assert len(rs)==2*h
            # Extend independent quotients using coordinate columns, then invert
            # the 16x16 binary expansion of the resulting 4x4 A matrix.
            cols=[w for _,w in selected]
            for j in range(4):
                v=tuple(int(i==j) for i in range(4));red=1<<j
                if rank(rs+[red])>len(rs):cols.append(v);rs.append(red)
            assert len(cols)==4
            rawrows=tuple(sum(REG[cols[j][i]][k]<<(4*j) for j in range(4)) for i in range(4) for k in range(4))
            dec=inverse(rawrows)
            for m,(g,quot) in enumerate(selected):
                word=amat(g,M);packed=sum(x<<(4*i) for i,x in enumerate(word))
                assert apply(dec,packed)==1<<(4*m+a)
            rows.append({'a':a,'b':b,'binary_rank_r':r,'leading_rank_h':h,'shared_exact_block_messages':2*h,'literal_restricted_encoding_full_readout_messages':literal_span,'literal_full_GL_messages':8*r,'universal_A2_teleportation':int(a==b==0),'universal_F2_8_teleportation':int(a==b==0)})
            witnesses.append({'a':a,'b':b,'encoding_A_matrices':[g for g,w in selected],'decoder_binary_rows_u_basis':dec})
    csvsave('new_dense_capacity_classes.csv',rows);save('new_dense_decoders.json',witnesses)
    return {'resources_smith_classes':14,'encodings_per_class':24576,'joint_measurement_block_labels':4,'algorithm':'span of complete local encoding orbit plus explicit invertible joint decoders','output':'new_dense_capacity_classes.csv','counterexample':'D(1,1): four shared block messages but no universal A^2 teleportation'}

def pauli_and_gate_groups():
    I=(1,0,0,1);X=(0,1,1,0);R=3;z=5;Z=(1,0,0,z);W=(1,0,1,1)
    P={tuple(MUL[pwr(R,k)][v] for v in amat(X if a else I,Z if b else I)) for k,a,b in product(range(4),range(2),range(2))}
    assert len(P)==16
    assert amat(X,Z)==tuple(MUL[z][v] for v in amat(Z,X))
    normals=[];images=Counter()
    for g in GATES:
        gi=ainv(g);cx=amat(amat(g,X),gi);cz=amat(amat(g,Z),gi)
        if cx in P and cz in P:
            normals.append(g)
            def label(v):
                return next((a,b) for k,a,b in product(range(4),range(2),range(2)) if tuple(MUL[pwr(R,k)][t] for t in amat(X if a else I,Z if b else I))==v)
            images[str((label(cx),label(cz)))]+=1
    assert W not in normals and len(images)==2
    # Native W on each mobit + coordinate swap gives local GL2; CNOT is joint.
    wf=(1,3);xf=(2,1);I2=eye(2)
    CNOT=tuple(1<<(i^((i>>1)&1)) for i in range(4))
    gens=(kron(wf,I2),kron(xf,I2),kron(I2,wf),kron(I2,xf),CNOT)
    seen={eye(4)};queue=deque(seen)
    while queue:
        g=queue.popleft()
        for t in gens:
            h=compose(t,g)
            if h not in seen:seen.add(h);queue.append(h)
    assert len(seen)==20160
    save('new_pauli_normalizer.json',{'Pauli_like_order':len(P),'normalizer_order':len(normals),'induced_symplectic_images':dict(images),'native_W_in_normalizer':False,'rank_X_plus_I':rank(lift(tuple(x^y for x,y in zip(X,I)))),'rank_Z_plus_I':rank(lift(tuple(x^y for x,y in zip(Z,I)))),'normalizer_A_matrices':normals})
    return {'ambient_local_A_gates':24576,'Pauli_like_group_order':16,'normalizer_order':len(normals),'symplectic_image_order':2,'generated_two_mobit_group_order':len(seen),'algorithm':'exhaustive conjugation and independent BFS closure','output':'new_pauli_normalizer.json'}

def oracle_apply(v,n,truth):
    # basis index = x + 2^n*y; standard oracle, no embedded answer.
    N=1<<n
    return xors(1<<(i^(N if (truth>>(i&(N-1)))&1 else 0)) for i in range(2*N) if (v>>i)&1)
def gate_bit(v,total,bit,G):
    out=0
    for i in range(1<<total):
        if (v>>i)&1:
            col=(i>>bit)&1
            for r in range(2):
                if (G[r]>>col)&1:out^=1<<((i&~(1<<bit))|(r<<bit))
    return out

def algorithms():
    records=[]
    # Deutsch: all 15 nonzero preparation states, then 255 with a two-level
    # spectator ancilla. Pre/postprocessing is covered by span invariance.
    for anc in (1,2):
        d=4*anc;checked=0
        def oracle(v,f):
            return xors(1<<((i//anc ^ (2 if (f>>(i//anc&1))&1 else 0))*anc+i%anc) for i in range(d) if (v>>i)&1)
        for v in range(1,1<<d):
            states=[oracle(v,f) for f in range(4)]
            c=[states[0],states[3]];b=[states[1],states[2]]
            assert rank(c)+rank(b)>rank(c+b)
            checked+=1
        records.append({'experiment':'Deutsch one query no perfect discrimination','dimension':d,'preparations':checked,'oracle_functions':4})
    # DJ spanning identity for n=2,3 and every nonzero preparation in n=2.
    djchecks=0
    for n in (2,3,4):
        N=1<<n;blocks=[sum(1<<i for i in range(j*N//4,(j+1)*N//4)) for j in range(4)]
        fs=[blocks[0]^blocks[1],blocks[0]^blocks[2],blocks[1]^blocks[2]]
        assert all(f.bit_count()==N//2 for f in fs)
        # Check equality as an operator on every coordinate basis, not samples.
        for i in range(2*N):
            v=1<<i;assert xors(oracle_apply(v,n,f) for f in fs)==v;djchecks+=1
    # BV: all s for n<=5; verify linear dependence of one-query oracles for n>=2.
    bv=[]
    for n in range(1,6):
        N=1<<n;fs=[sum(parity(s&x)<<x for x in range(N)) for s in range(N)]
        mats=[tuple(oracle_apply(1<<i,n,f) for i in range(2*N)) for f in fs]
        if n>=2:assert all(xors(M[i] for M in mats)==0 for i in range(2*N))
        bv.append({'n':n,'oracles':N,'operator_span':rank(flatten(M,2*N) for M in mats),'exact_query_bound':n})
    # Reproduce Willcock-Sabry UNIQUE-SAT as a positive control.
    # Lower shear s and its transpose are different, neither a unitary Hadamard.
    S=(1,3);ST=(3,2);unique=[]
    for n in range(1,7):
        N=1<<n
        for truth in [0]+[1<<i for i in range(N)]:
            v=1
            for b in range(n):v=gate_bit(v,n+1,b,S)
            v=oracle_apply(v,n,truth)
            for b in range(n):v=gate_bit(v,n+1,b,S)
            v=gate_bit(v,n+1,n,ST)
            v=xors(1<<(i^((N-1) if i&N else 0)) for i in range(2*N) if (v>>i)&1)
            v=gate_bit(v,n+1,n,ST)
            assert v and ((v==1) if truth==0 else not v&1)
            unique.append({'n':n,'marked_input':-1 if truth==0 else truth.bit_length()-1,'final_support_bitset':hex(v),'all_zero_possible':int(bool(v&1))})
    # Kickback identity checked for all A-valued coefficients, f=0,1.
    chi=(1,5);X=(0,1,1,0);kick=0
    for c,f in product(range(16),range(2)):
        v=tuple(MUL[c][t] for t in chi);out=avec(X,v) if f else v
        assert out==tuple(MUL[MUL[c][5 if f else 1]][t] for t in chi);kick+=1
    assert (1^5)==4 and not (1^5)&1
    save('new_algorithm_checks.json',{'Deutsch':records,'DJ_operator_coordinate_checks':djchecks,'BV':bv,'kickback_scalar_checks':kick,'Fourier_2_by_2_determinant_u':4})
    csvsave('unique_sat_reproduction.csv',unique)
    return {'Deutsch_preparations_total':270,'DJ_operator_coordinate_checks':djchecks,'BV_hidden_strings_total':sum(r['oracles'] for r in bv),'UNIQUE_SAT_promised_functions':len(unique),'UNIQUE_SAT_n_range':[1,6],'kickback_cases':kick,'algorithm':'exact basis-operator identities; exhaustive small preparations and promised functions','output':'new_algorithm_checks.json; unique_sat_reproduction.csv'}

def deletion_error_correction():
    # Linear non-reversible deletion in F2, and reversible span obstruction.
    deletion=[]
    for d in (2,3,4):
        clones=[vector_tensor(v,v,d) for v in range(1,1<<d)]
        D=tuple(1<<(i*d+i) for i in range(d))
        assert all(apply(D,c)==v for v,c in enumerate([0]+clones) if v)
        assert rank(clones)==d*(d+1)//2>d
        deletion.append({'d':d,'nonzero_states':(1<<d)-1,'clone_span_dimension':rank(clones),'deletion_decoder_rows':D})
    # Three-mobit repetition: input basis e0->000, e1->111.
    errors=(0,1,2,4);colmap=[]
    for syndrome,err in enumerate(errors):
        for bit in range(2):colmap.append(((7*bit)^err,2*syndrome+bit))
    decoder=tuple(1<<next(i for i,j in colmap if j==o) for o in range(8))
    count=0
    for v in (1,2,3):
        for errvec in range(1,16):
            noisy=xors(1<<((7*b)^errors[k]) for k in range(4) for b in range(2) if (errvec>>k)&1 and (v>>b)&1)
            expected=xors(v<<(2*k) for k in range(4) if (errvec>>k)&1)
            assert apply(decoder,noisy)==expected;count+=1
    # Native W takes an affine-support Bell state to a 3-element support.
    bell=(1<<0)|(1<<3);out=apply(kron((1,3),eye(2)),bell)
    assert out.bit_count()==3
    save('new_deletion_and_error_correction.json',{'deletion':deletion,'repetition_decoder_rows':decoder,'error_coherent_checks':count,'affine_support_escape':{'input':bell,'output':out}})
    return {'deletion_state_checks':25,'error_input_states':3,'coherent_error_combinations':15,'error_checks':count,'output':'new_deletion_and_error_correction.json'}

def main():
    save('environment.json',{'python':sys.version,'platform':platform.platform(),'processor':platform.processor(),'encoding':'A polynomial coefficients in u, u^4=0; bitpacked F2 rows','source_reuse':'no supplied code imported'})
    for name,fn in [('inventory',inventory),('contextuality',support_classification),('Bell_GHZ',small_bell_ghz),('protocols',exact_protocols),('dense_capacities',dense_resource_capacities),('Pauli_normalizer',pauli_and_gate_groups),('algorithms',algorithms),('deletion_QEC',deletion_error_correction)]:timed(name,fn)
if __name__=='__main__':main()
