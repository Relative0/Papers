#!/usr/bin/env python3
"""Reproducible finite audit of the intrinsic CM phase calculus.
Python >=3.10, NumPy >=1.24. No network, cloud, or user-account operations.
CM bits are clockwise: a0,a1,a2,a3 -> [[a0,a1],[a3,a2]].
Register coordinates are labelled in ascending binary order, independent of CM axes.
"""
from __future__ import annotations
import csv, hashlib, itertools as it, json, platform, random, sys, time
from pathlib import Path
import numpy as np

OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data'
OUT.mkdir(parents=True,exist_ok=True)
RESULTS={}; START=time.perf_counter()
NAMES=['0','AND','UP','L','NOR','XNOR','NOT_R','LEFT_IMPLIES','DOWN','R','XOR','OR','NOT_L','IMPLIES','NAND','TOP']
E=[1,2,4,8]; ONE,T,Z,DELTA,OMEGA=1,2,4,5,15

def bits(a:int)->tuple[int,...]: return tuple((a>>k)&1 for k in range(4))
def mul_direct(a:int,b:int)->int:
    out=0
    for i in range(4):
        for j in range(4): out ^= (((a>>i)&1)&((b>>j)&1)) << ((i+j)%4)
    return out
M=np.array([[mul_direct(a,b) for b in range(16)] for a in range(16)],dtype=np.uint8)
W=np.array([a.bit_count() for a in range(16)],dtype=np.uint8)
def mul(a:int,b:int)->int: return int(M[a,b])
def powr(a:int,n:int)->int:
    x=ONE
    for _ in range(n): x=mul(x,a)
    return x
def tr(a:int)->int: return sum(((a>>k)&1)<<((-k)%4) for k in range(4))
TR=np.array([tr(a) for a in range(16)],dtype=np.uint8)
def rot(a:int,k:int=1)->int:return mul(E[k%4],a)
def comp(a:int)->int:return a^15
def diff(a:int,b:int)->int:return a&(15^b)
def norm(a:int)->int:return mul(a,tr(a))
NV=np.array([norm(a) for a in range(16)],dtype=np.uint8)
def inverse(a:int): return next((b for b in range(16) if mul(a,b)==1),None)
INV=[inverse(a) for a in range(16)]
def order(a:int):return next((k for k in range(1,9) if powr(a,k)==1),None)
def nilidx(a:int):return next((k for k in range(1,5) if powr(a,k)==0),None)
def val(a:int)->int:
    # in F2[u]/u^4, u=1+t. change basis is self-inverse subset transform
    coeff=0
    for k in range(4):
        if (a>>k)&1:
            for j in range(4):
                if j&k==j: coeff ^= 1<<j
    return next((k for k in range(4) if (coeff>>k)&1),4)
def mul_u(a:int,b:int)->int:
    def cv(x):
        y=0
        for k in range(4):
            if (x>>k)&1:
                for j in range(4):
                    if j&k==j:y^=1<<j
        return y
    aa,bb=cv(a),cv(b); c=0
    for i in range(4):
        for j in range(4-i): c^=(((aa>>i)&1)&((bb>>j)&1))<<(i+j)
    return cv(c)
def regular(a:int)->list[list[int]]:
    return [[(mul(a,E[j])>>i)&1 for j in range(4)] for i in range(4)]
def rank2(rows:list[int],ncols:int)->int:
    rows=list(rows); r=0
    for k in range(ncols):
        p=next((i for i in range(r,len(rows)) if (rows[i]>>k)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and (rows[i]>>k)&1: rows[i]^=rows[r]
        r+=1
    return r

def write_csv(name:str,rows:list[dict])->None:
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def record(k:str,v):RESULTS[k]=v;print(k,':',v,flush=True)

# Basic ring axioms, independent polynomial multiplication, conjugation, difference.
for a,b in it.product(range(16),repeat=2):
    assert mul(a,b)==mul_u(a,b)==mul(b,a)
    assert tr(mul(a,b))==mul(tr(a),tr(b))
    assert norm(mul(a,b))==mul(norm(a),norm(b))
    assert mul(a,OMEGA)==(OMEGA if W[a]%2 else 0)
    for k in range(4):
        assert diff(rot(a,k),rot(b,k))==rot(diff(a,b),k)
    for c in range(16):
        assert mul(mul(a,b),c)==mul(a,mul(b,c))
        assert mul(a,b^c)==(mul(a,b)^mul(a,c))
        assert diff(a^c,b)==(diff(a,b)^diff(c,b))
record('ring_pairs_independently_checked',256)
record('ring_triples_associativity_distributivity',4096)
units=[a for a in range(16) if INV[a] is not None]
assert units==[a for a in range(16) if W[a]%2]
assert [a for a in range(16) if nilidx(a)]==[a for a in range(16) if W[a]%2==0]
for a in units: assert INV[a]==tr(a)
rows=[]
for a in range(16):
    r=regular(a);rr=rank2([sum(v<<j for j,v in enumerate(row)) for row in r],4)
    assert rr==4-val(a)
    rows.append(dict(code=a,CM=NAMES[a],cyclic_bits=''.join(map(str,bits(a))),matrix=str([[a&1,(a>>1)&1],[(a>>3)&1,(a>>2)&1]]),weight=int(W[a]),valuation=val(a),unit=INV[a] is not None,inverse=INV[a],order=order(a),nilpotency=nilidx(a),rank=rr,norm=norm(a),transpose=tr(a)))
write_csv('elements.csv',rows)
write_csv('star_table.csv',[dict(A=NAMES[a],**{NAMES[b]:NAMES[mul(a,b)] for b in range(16)}) for a in range(16)])
for k in range(4):write_csv(f'interference_{k}.csv',[dict(A=NAMES[a],**{NAMES[b]:NAMES[a^rot(b,k)] for b in range(16)}) for a in range(16)])
record('units',len(units));record('nonzero_zero_divisors',7)
record('roots_of_phase_half_turn',[a for a in range(16) if mul(a,a)==Z])
record('unit_orders',{str(n):sum(order(a)==n for a in units) for n in (1,2,4)})
record('norm_preimages',{str(v):[a for a in range(16) if norm(a)==v] for v in sorted(set(NV.tolist()))})
# Enumerate all subsets that are ideals, rather than assuming principal ideals.
ideals=[]
for mask in range(1,1<<16,2):
    els=[a for a in range(16) if (mask>>a)&1]
    if len(els) not in (1,2,4,8,16):continue
    if any(not ((mask>>(a^b))&1) for a in els for b in els):continue
    if any(not ((mask>>mul(a,b))&1) for a in els for b in range(16)):continue
    ideals.append(els)
assert sorted(map(len,ideals))==[1,2,4,8,16]
record('all_ideals',ideals)
# All possible unital algebra maps are determined by t; test all 16 images.
def substitution(a,x):
    out=0
    for k in range(4):
        if (a>>k)&1:out^=powr(x,k)
    return out
autos=[]
for x in range(16):
    if powr(x,4)!=1:continue
    f=[substitution(a,x) for a in range(16)]
    if len(set(f))==16:
        assert all(f[mul(a,b)]==mul(f[a],f[b]) for a in range(16) for b in range(16))
        autos.append(f)
assert len(autos)==4
assert all(all(f[f[a]]==a for a in range(16)) for f in autos)
record('automorphism_generator_images',[f[T] for f in autos])
transforms=[('identity',lambda a:a),('transpose',tr),('complement',comp)]
for k in (1,2,3):
    transforms.extend([(f'R{k}',lambda a,k=k:rot(a,k)),(f'R{k}_transpose',lambda a,k=k:rot(tr(a),k))])
write_csv('transformations.csv',[dict(name=name,xor_linear=all(f(a^b)==(f(a)^f(b)) for a in range(16) for b in range(16)),star_hom=all(f(mul(a,b))==mul(f(a),f(b)) for a in range(16) for b in range(16)),unital=f(1)==1,difference=all(f(diff(a,b))==diff(f(a),f(b)) for a in range(16) for b in range(16))) for name,f in transforms])
write_csv('division.csv',[dict(divisor=a,CM=NAMES[a],image_size=len(set(M[a].tolist())),solutions_if_solvable=16//len(set(M[a].tolist()))) for a in range(16)])
assert [b for b in range(16) if all(diff(mul(a,c),b)==mul(diff(a,b),diff(c,b)) for a in range(16) for c in range(16))]==[0,15]

# All 65,536 two-branch operators, using NumPy batches and an independent rank check.
OPS=np.array(list(it.product(range(16),repeat=4)),dtype=np.uint8)
a,b,c,d=OPS.T
DET=M[a,d]^M[b,c]
INV_TABLE=np.array([0 if x is None else x for x in INV],dtype=np.uint8)
invertible=(W[DET]%2)==1
DINV=INV_TABLE[DET]
OPINV=np.stack((M[DINV,d],M[DINV,b],M[DINV,c],M[DINV,a]),axis=1)
unitary=(NV[a]^NV[c]==1)&(NV[b]^NV[d]==1)&(M[TR[a],b]^M[TR[c],d]==0)
involution=(M[a,a]^M[b,c]==1)&(M[a,b]^M[b,d]==0)&(M[c,a]^M[d,c]==0)&(M[c,b]^M[d,d]==1)
# Operator action on every state.
xs=np.repeat(np.arange(16,dtype=np.uint8),16);ys=np.tile(np.arange(16,dtype=np.uint8),16)
weights=W[xs]+W[ys];shell=np.flatnonzero(weights==4)
global_iso=np.zeros(65536,dtype=bool);shell_iso=global_iso.copy()
for lo in range(0,65536,1024):
    aa,bb,cc,dd=[x[lo:lo+1024,None] for x in (a,b,c,d)]
    oo=M[aa,xs]^M[bb,ys];pp=M[cc,xs]^M[dd,ys]
    ww=W[oo]+W[pp]
    global_iso[lo:lo+1024]=np.all(ww==weights,axis=1)
    shell_iso[lo:lo+1024]=np.all(ww[:,shell]==4,axis=1)
# rank of binary regular block matrix computed without determinant criterion.
ranks=[]
for aa,bb,cc,dd in OPS.tolist():
    A,B,C,D=regular(aa),regular(bb),regular(cc),regular(dd)
    rows=[sum(v<<j for j,v in enumerate(A[i]+B[i])) for i in range(4)]
    rows += [sum(v<<j for j,v in enumerate(C[i]+D[i])) for i in range(4)]
    ranks.append(rank2(rows,8))
assert np.array_equal(np.array(ranks)==8,invertible)
assert all(invertible[unitary])
monomial=unitary&(((b==0)&(c==0))|((a==0)&(d==0)))
split=invertible&(a!=0)&(c!=0)
beta=M[M[a,c],DINV]
profiles=np.stack([W[M[beta,1^e]] for e in E],axis=1)
fringe=split&np.all(profiles==np.array([0,2,4,2]),axis=1)
record('operators_tested',len(OPS));record('states_per_operator',256)
record('invertible_operators',int(invertible.sum()));record('independent_binary_rank_checks',65536)
record('intrinsic_unitaries',int(unitary.sum()));record('nonmonomial_unitaries',int((unitary&~monomial).sum()))
record('unitary_involutions',int((unitary&involution).sum()))
record('mixing_unitary_involutions',int((unitary&involution&~monomial).sum()))
record('global_Hamming_isometries',int(global_iso.sum()));record('Hamming_shell_preservers',int(shell_iso.sum()))
record('unitary_and_Hamming_shell_intersection',int((unitary&shell_iso).sum()))
record('reversible_splitters',int(split.sum()));record('four_point_fringe_splitters',int(fringe.sum()))
assert [invertible.sum(),unitary.sum(),(unitary&~monomial).sum(),(unitary&involution).sum(),global_iso.sum(),shell_iso.sum(),split.sum(),fringe.sum()]==[24576,512,384,96,32,512,22528,8192]
write_csv('operators.csv',[dict(a=int(aa),b=int(bb),c=int(cc),d=int(dd),invertible=int(iv),binary_rank=rr,unitary=int(un),involution=int(ii),hamming_global=int(gg),hamming_shell=int(ss),splitter=int(sp),fringe_0242=int(ff)) for (aa,bb,cc,dd),iv,rr,un,ii,gg,ss,sp,ff in zip(OPS,invertible,ranks,unitary,involution,global_iso,shell_iso,split,fringe)])
# Scalar norm observability after unitary phase conjugation.
for aa,bb,cc,dd in OPS[unitary].tolist():
    det=mul(aa,dd)^mul(bb,cc);iv=INV[det]
    for t in E:
        o0=mul(iv,mul(mul(aa,dd),t)^mul(bb,cc))
        o1=mul(iv,mul(aa,cc));o1=mul(o1,1^t)
        assert (norm(o0),norm(o1))==(1,0)
record('unitary_interferometer_norm_checks',512*4)
write_csv('shear_fringe.csv',[dict(k=k,phase=e,detector=mul(3,1^e),CM=NAMES[mul(3,1^e)],weight=int(W[mul(3,1^e)])) for k,e in enumerate(E)])

# Deutsch-Jozsa compressed linear detectors.
balanced2=[f for f in it.product((0,1),repeat=4) if sum(f)==2]
def detector(ws,fs):
    out=0
    for w,f in zip(ws,fs):out^=mul(w,Z if f else ONE)
    return out
sol=[]
for ws in it.product(range(16),repeat=4):
    if (ws[0]^ws[1]^ws[2]^ws[3])!=0:continue
    if all(detector(ws,f)!=0 for f in balanced2):sol.append(ws)
assert len(sol)==1536
record('DJ_n2_single_CM_detectors',len(sol))
write_csv('DJ_n2_examples.csv',[dict(truth=''.join(map(str,f)),kind='balanced' if sum(f)==2 else 'constant',CM=NAMES[detector((0,1,2,3),f)]) for f in [(0,0,0,0),(1,1,1,1)]+balanced2])
sub4=list(it.combinations(range(8),4));masks={}
for first7 in it.product(range(4),repeat=7):
    last=0
    for q in first7:last^=q
    labels=first7+(last,);cover=0
    for i,S in enumerate(sub4):
        v=0
        for j in S:v^=labels[j]
        if v:cover|=1<<i
    masks.setdefault(cover,labels)
full=(1<<70)-1
assert full not in masks
pair=((0,0,0,0,0,1,2,3),(0,0,0,1,2,0,0,3))
for S in sub4:
    vals=[]
    for y in pair:
        v=0
        for j in S:v^=y[j]
        vals.append(v)
    assert any(vals)
record('DJ_n3_zero_sum_quotient_labelings',4**7)
record('DJ_n3_distinct_coverage_patterns',len(masks))
record('DJ_n3_minimum_linear_CM_channels',2)

# CM-to-ANF phase circuit (butterfly) versus independent subset matrix evaluation.
def mobius(v:list[int],n:int)->list[int]:
    out=list(v)
    for q in range(n):
        for s in range(1<<n):
            if (s>>q)&1:out[s]^=out[s^(1<<q)]
    return out
anfrows=[]
for n in range(1,5):
    N=1<<n;total=1<<N
    truth=((np.arange(total,dtype=np.uint32)[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
    # Primary model: prepare with C^tensor, apply phase on f, recombine.
    phase=np.where(truth,Z,ONE).astype(np.uint8)
    actual=phase.copy()
    for q in range(n):
        for s in range(N):
            if (s>>q)&1:actual[:,s]^=actual[:,s^(1<<q)]
    # Independent subset-sum specification, NOT the butterfly routine.
    expected=np.zeros_like(actual)
    for s in range(N):
        coef=np.zeros(total,dtype=np.uint8)
        for x in range(N):
            if (x&s)==x:coef^=truth[:,x]
        expected[:,s]=np.where(coef,DELTA,0)
    expected[:,0]^=ONE
    assert np.array_equal(actual,expected)
    pred=np.any(actual[:,1:]!=0,axis=1)
    nonconstant=np.any(truth!=truth[:,:1],axis=1)
    assert np.array_equal(pred,nonconstant)
    anfrows.append(dict(n=n,functions=total,phase_anf_mismatches=0,constancy_mismatches=0))
write_csv('phase_anf_exhaustive.csv',anfrows)
record('phase_anf_truth_functions_checked',sum(r['functions'] for r in anfrows))
# Kickback on every Boolean function through n=3 and each branch.
kchecks=0
for n in range(1,4):
    for mask in range(1<<(1<<n)):
        for x in range(1<<n):
            f=(mask>>x)&1;target=(Z,ONE) if f else (ONE,Z)
            phase=Z if f else ONE
            assert target==(phase,mul(phase,Z));kchecks+=1
record('kickback_basis_checks',kchecks)
# Hidden affine strings and marked patterns (n=1 edge case explicitly corrected).
affine=[];marks=[]
for n in range(1,7):
    N=1<<n;count=0
    for v in range(N):
        for b0 in (0,1):
            f=[((v&x).bit_count()%2)^b0 for x in range(N)]
            out=mobius([Z if bit else ONE for bit in f],n)
            bv=int(out[0]==Z);vv=sum((1<<q) for q in range(n) if out[1<<q]==DELTA)
            assert (vv,bv)==(v,b0);count+=1
    affine.append(dict(n=n,functions=count,mismatches=0))
    for m in range(N):
        f=[int(x==m) for x in range(N)]
        out=mobius([Z if bit else ONE for bit in f],n)
        expected=[(ONE if s==0 else 0) ^ (DELTA if (s&m)==m else 0) for s in range(N)]
        assert out==expected
        # remove the known e0 background before zero/nonzero decoding
        signal=out[:];signal[0]^=ONE
        decoded=sum((1<<q) for q in range(n) if signal[(N-1)^(1<<q)]==0)
        assert decoded==m
    marks.append(dict(n=n,marks=N,mismatches=0))
write_csv('affine_hidden_strings.csv',affine);write_csv('marked_pattern_decoding.csv',marks)
record('affine_cases',sum(r['functions'] for r in affine));record('marked_cases',sum(r['marks'] for r in marks))

# Local two-bit shear experiment: 24,576 invertible local U, four possible marks.
def local2(st,U,q):
    out=list(st);aa,bb,cc,dd=U
    for i,j in ([(0,2),(1,3)] if q==0 else [(0,1),(2,3)]):
        out[i]=mul(aa,st[i])^mul(bb,st[j]);out[j]=mul(cc,st[i])^mul(dd,st[j])
    return out
raw_unique=weight_unique=peak=0
for U,UI in zip(OPS[invertible].tolist(),OPINV[invertible].tolist()):
    prep=local2(local2([1,0,0,0],U,0),U,1);outs=[];wouts=[]
    for m in range(4):
        ss=prep[:];ss[m]=mul(Z,ss[m]);oo=local2(local2(ss,UI,1),UI,0)
        outs.append(tuple(oo));wouts.append(tuple(int(W[a]) for a in oo))
    raw_unique+=int(len(set(outs))==4);weight_unique+=int(len(set(wouts))==4)
    peak+=int(all(ws[m]>max(ws[j] for j in range(4) if j!=m) for m,ws in enumerate(wouts)))
record('two_bit_search_raw_unique',raw_unique);record('two_bit_search_weight_unique',weight_unique);record('two_bit_search_marked_peak',peak)
assert (raw_unique,weight_unique,peak)==(16384,16384,0)

# Local CM compiler and sparse ANF. These products are Boolean-polynomial
# products (set union of monomial masks), NOT the phase ring star product.
def predicate(cm,x,y):return (cm>>{(1,1):0,(1,0):1,(0,0):2,(0,1):3}[x,y])&1
def local_coeff(cm):
    aa,bb,dd,cc=bits(cm)
    return (dd,bb^dd,cc^dd,aa^bb^cc^dd)
def poly_mul(p:set[int],q:set[int],counter=None)->set[int]:
    r=set()
    for a in p:
        for b in q:
            if counter is not None:counter[0]+=1
            c=a|b
            if c in r:r.remove(c)
            else:r.add(c)
    return r

def propagate(cm,p,q,counter=None):
    a,b,c,d=local_coeff(cm);r={0} if a else set()
    if b:r^=p
    if c:r^=q
    if d:r^=poly_mul(p,q,counter)
    return r
for cm,x,y in it.product(range(16),(0,1),(0,1)):
    a,b,c,d=local_coeff(cm)
    assert predicate(cm,x,y)==(a^(b&x)^(c&y)^(d&x&y))
    assert d==int(W[cm]%2)
record('local_CM_ANF_cases',64)
rng=random.Random(17092026);nodechecks=0
for trial in range(50):
    pol=[{1<<i} for i in range(7)];truth=[[((x>>i)&1) for x in range(128)] for i in range(7)]
    for step in range(30):
        cm=rng.randrange(16);j=rng.randrange(len(pol));k=rng.randrange(len(pol))
        p=propagate(cm,pol[j],pol[k]); tt=[predicate(cm,x,y) for x,y in zip(truth[j],truth[k])]
        direct=[]
        for x in range(128):
            v=0
            for term in p:v^=int((x&term)==term)
            direct.append(v)
        assert direct==tt
        pol.append(p);truth.append(tt);nodechecks+=1
record('random_CM_DAG_nodes_verified',nodechecks)
# All pointwise same-operand ternary folding combinations, at four assignments.
foldchecks=0
for A,B,H in it.product(range(16),repeat=3):
    folded=sum(predicate(H,(A>>i)&1,(B>>i)&1)<<i for i in range(4))
    for x,y in it.product((0,1),repeat=2):
        assert predicate(folded,x,y)==predicate(H,predicate(A,x,y),predicate(B,x,y));foldchecks+=1
record('pointwise_CM_folding_checks',foldchecks)
bench=[]
for s in (10,20,30,40):
    p={1<<i for i in range(s)};q={1<<(i+s) for i in range(s)};count=[0]
    pq=poly_mul(p,q,count);po=p^q^pq;res=poly_mul(po,{0}^pq,count)
    assert res==p^q
    bench.append(dict(s=s,xy_terms=len(pq),naive_shared_pair_products=count[0],final_terms=len(res),CM_fold_pair_products=0,generic_same_identity_pair_products=0))
write_csv('synthetic_folding_operations.csv',bench)

# New nilpotent interaction bound, tested as exact polynomial in oracle bits.
def matmul(A,B):
    aa,bb,cc,dd=A;ee,ff,gg,hh=B
    return (mul(aa,ee)^mul(bb,gg),mul(aa,ff)^mul(bb,hh),mul(cc,ee)^mul(dd,gg),mul(cc,ff)^mul(dd,hh))
ID=(1,0,0,1)
interaction=[]
for p,maxdeg in ((1,3),(2,1)):
    largest=0
    for trial in range(100):
        fixed=[tuple(rng.randrange(16) for _ in range(4)) for _ in range(6)]
        selectors=[(rng.randrange(2),rng.randrange(2)) for _ in range(5)]
        vals=[]
        tag=powr(3,p)
        for f in it.product((0,1),repeat=5):
            A=fixed[0]
            for j,bv in enumerate(f):
                ds=selectors[j]
                O=(1^(tag if ds[0] and bv else 0),0,0,1^(tag if ds[1] and bv else 0))
                A=matmul(fixed[j+1],matmul(O,A))
            vals.append(A)
        for entry in range(4):
            coefs=mobius([v[entry] for v in vals],5)
            deg=max((s.bit_count() for s,v in enumerate(coefs) if v),default=0)
            assert deg<=maxdeg;largest=max(largest,deg)
    interaction.append(dict(tag=f'u^{p}',circuits=100,oracle_bits=5,proven_degree_bound=maxdeg,largest_observed_degree=largest))
write_csv('nilpotent_interaction_tests.csv',interaction)
record('nilpotent_interaction_circuits',200)
# Independent phase registers retain a mixed Boolean term, same-register tags kill it.
def tensor(a,b):return sum(((a>>i)&1)*((b>>j)&1)<<(4*i+j) for i in range(4) for j in range(4))
def tensor_mul(a,b):
    out=0
    for i in range(16):
        if not ((a>>i)&1):continue
        for j in range(16):
            if (b>>j)&1:out^=1<<((((i//4+j//4)%4)*4)+(i%4+j%4)%4)
    return out
one2=tensor(1,1);eta=tensor(DELTA,1);theta=tensor(1,DELTA);mixed=tensor(DELTA,DELTA)
assert tensor_mul(eta,theta)==mixed!=0
for f,g in it.product((0,1),repeat=2):
    out=tensor_mul(one2^(eta if f else 0),one2^(theta if g else 0))
    assert out==(one2^(eta if f else 0)^(theta if g else 0)^(mixed if f and g else 0))
    A=Z if f else 1;B=Z if g else 1
    # Boolean mask/decode, conjunction, re-encode: not R-linear.
    fa=mul(A&Z,Z);gb=mul(B&Z,Z)
    andtag=1^mul(DELTA,fa&gb)
    assert andtag==(Z if f and g else 1)
record('independent_register_and_mask_tag_checks',4)

# Full conjugated-oracle subset-interval kernel, independently enumerated.
# K_f = M diag(f) M. Compare every entry to direct interval parity and then
# verify K_f K_g = K_(f AND g) for all function pairs through n=3.
interval_count=0; interval_pair_count=0
for n in range(1,4):
    size=1<<n; nf=1<<size
    mm=np.array([[int((s&t)==t) for t in range(size)] for s in range(size)],dtype=np.uint8)
    fs=np.array([[(f>>x)&1 for x in range(size)] for f in range(nf)],dtype=np.uint8)
    ks=((mm[None,:,:]*fs[:,None,:])@mm)&1
    for f in range(nf):
        for sidx in range(size):
            for tidx in range(size):
                expected=0
                if (sidx&tidx)==tidx:
                    for x in range(size):
                        if (x&tidx)==tidx and (x&sidx)==x:
                            expected^=(f>>x)&1
                assert int(ks[f,sidx,tidx])==expected
        interval_count+=1
    for f in range(nf):
        target=np.array([f&g for g in range(nf)],dtype=int)
        assert np.array_equal((ks[f]@ks)&1,ks[target])
        interval_pair_count+=nf
record('subset_interval_kernels_checked',interval_count)
record('subset_interval_product_pairs',interval_pair_count)

RESULTS['runtime_seconds']=round(time.perf_counter()-START,3)
RESULTS['environment']={'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform(),'seed':17092026}
RESULTS['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(OUT/'verification.json').write_text(json.dumps(RESULTS,indent=2)+'\n',encoding='utf-8')
print('ALL CHECKS PASSED',RESULTS['runtime_seconds'],flush=True)
