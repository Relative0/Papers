"""Fresh consolidation checks. No imports from any supplied mathematical implementation.
Python standard library only. Exact bit arithmetic; full dual-number support tables
are tested by 2-SAT, NOT by the claimed residue-hyperplane theorem.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json,csv,time,hashlib,sys,platform,math
OUT=Path(__file__).resolve().parent

def mul(a,b,s):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
    return z&((1<<s)-1)
def val(a,s):return s if not a else (a&-a).bit_length()-1
def rank(rows):
    p={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in p:x^=p[k]
            else:p[k]=x;break
    return len(p)
def inverse(A,s):
    n=len(A);a=[list(r)+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]&1),None)
        if k is None:return None
        a[j],a[k]=a[k],a[j];u=next(x for x in range(1,1<<s,2) if mul(x,a[j][j],s)==1)
        a[j]=[mul(x,u,s) for x in a[j]]
        for i in range(n):
            if i!=j:
                c=a[i][j];a[i]=[x^mul(c,y,s) for x,y in zip(a[i],a[j])]
    return [r[n:] for r in a]
def mm(A,B,s):
    out=[]
    for r in A:
        row=[]
        for c in zip(*B):
            z=0
            for x,y in zip(r,c):z^=mul(x,y,s)
            row.append(z)
        out.append(row)
    return out
def smith2(e,s):
    a=min(val(x,s) for x in e)
    if a==s:return (s,s)
    M=[list(e[:2]),list(e[2:])];i,j=next((i,j) for i,j in product(range(2),repeat=2) if val(M[i][j],s)==a)
    M[0],M[i]=M[i],M[0]
    if j: M=[r[::-1] for r in M]
    unit=M[0][0]>>a;iu=next(x for x in range(1,1<<s,2) if mul(x,unit,s)==1)
    q=mul(M[1][0]>>a,iu,s)
    return a,val(M[1][1]^mul(q,M[0][1],s),s)
def literal_rank(e,s):
    rows=[]
    for i in range(2):
        for k in range(s):
            row=0
            for j in range(2):
                for l in range(s):row|=((mul(e[2*i+j],1<<l,s)>>k)&1)<<(s*j+l)
            rows.append(row)
    return rank(rows)
def sat(n,clauses,pins=()):
    # Literal (i,b) means variable i must equal b. Clauses exclude a pair of values.
    g=[[] for _ in range(2*n)];gr=[[] for _ in range(2*n)]
    def edge(a,b):g[a].append(b);gr[b].append(a)
    for i,a,j,b in clauses:
        edge(2*i+a,2*j+1-b);edge(2*j+b,2*i+1-a)
    for i,b in pins:edge(2*i+1-b,2*i+b)
    seen=set();order=[]
    def dfs(v):
        seen.add(v)
        for w in g[v]:
            if w not in seen:dfs(w)
        order.append(v)
    for v in range(2*n):
        if v not in seen:dfs(v)
    comp={}
    def visit(v,c):
        comp[v]=c
        for w in gr[v]:
            if w not in comp:visit(w,c)
    for v in reversed(order):
        if v not in comp:visit(v,len(comp))
    return all(comp[2*i]!=comp[2*i+1] for i in range(n))
def dual_numbers():
    s=2;units=[1,3]
    def canon(r):return min(tuple(mul(u,x,s) for x in r) for u in units)
    bases=set()
    for e in product(range(4),repeat=4):
        if (mul(e[0],e[3],s)^mul(e[1],e[2],s))&1:bases.add(tuple(sorted([canon(e[:2]),canon(e[2:])])))
    bases=sorted(bases);assert len(bases)==12
    counts=Counter();records=[];calls=0;events=0
    for e in product(range(4),repeat=4):
        if not any(e):continue
        M=[e[:2],e[2:]];clauses=[];possible=[]
        for i,A in enumerate(bases):
            for j,B in enumerate(bases):
                T=mm(mm(A,M,s),list(zip(*B)),s)
                for a,b in product(range(2),repeat=2):
                    if T[a][b]:possible.append((i,a,j+12,b))
                    else:clauses.append((i,a,j+12,b))
        calls+=1;has=sat(24,clauses)
        if not has:status='STRONG';uncovered=len(possible)
        else:
            uncovered=0
            for i,a,j,b in possible:
                calls+=1
                if not sat(24,clauses,[(i,a),(j,b)]):uncovered+=1
            status='LOGICAL' if uncovered else 'LOCAL'
        a,b=smith2(e,s);expected='LOCAL' if b==s else ('STRONG' if a==b else 'LOGICAL')
        assert status==expected,(e,status,expected)
        counts[status]+=1;events+=len(possible)
        records.append({'entries_u':e,'a':a,'b':b,'status':status,'possible_events':len(possible),'unextendable_events':uncovered})
    (OUT/'dual_number_contextuality.json').write_text(json.dumps(records,indent=2))
    return {'resources_nonzero':255,'basis_count_per_party':12,'contexts_per_resource':144,'SAT_calls':calls,'possible_events_counted':events,'counts':dict(counts),'method':'Independent explicit support tables and SCC 2-SAT including seeded-event extension; does not use hyperplane lemma to classify'}
def ring_inventory():
    counts=Counter();units=0;separable=set()
    for e in product(range(16),repeat=4):
        a,b=smith2(e,4);assert literal_rank(e,4)==8-a-b
        counts[(a,b)]+=1
        if a==b==0:units+=1
    for x in product(range(16),repeat=2):
        for y in product(range(16),repeat=2):separable.add(tuple(mul(a,b,4) for a in x for b in y))
    assert units==24576 and len(separable)==5266
    assert all(smith2(e,4)[1]==4 for e in separable)
    table=[{'a':a,'b':b,'count':c,'binary_rank':8-a-b,'shared_messages':0 if a==4 else(4 if a==b else 2),'literal_restricted_messages':2*(8-a-b),'universal_teleportation':a==b==0} for (a,b),c in sorted(counts.items())]
    (OUT/'resource_inventory_summary.json').write_text(json.dumps(table,indent=2))
    return {'resources':65536,'smith_classes':len(counts),'invertible_resources':units,'simple_tensors_including_zero':len(separable),'rank_checks':65536}
def dense_decoders():
    gl=[[[e[0],e[1]],[e[2],e[3]]] for e in product(range(2),repeat=4) if (e[0]*e[3])^(e[1]*e[2])]
    records=[]
    for a in range(4):
        for b in range(a,5):
            N=[[1,0],[0,0 if b==4 else 1<<(b-a)]]
            chosen=[];cols=[];res=[]
            for U in gl:
                v=sum(mm(U,N,4),[]);r=sum((x&1)<<i for i,x in enumerate(v))
                if rank(res+[r])>len(res):res.append(r);cols.append(v);chosen.append(U)
            k=4 if a==b else 2;assert len(cols)==k
            for i in range(4):
                v=[int(i==j) for j in range(4)];r=1<<i
                if rank(res+[r])>len(res):res.append(r);cols.append(v)
            decoder=inverse(list(map(list,zip(*cols))),4);assert decoder is not None
            M=[[1<<a,0],[0,0 if b==4 else 1<<b]]
            outputs=[]
            for i,U in enumerate(chosen):
                code=sum(mm(U,M,4),[]);y=sum(mm(decoder,[[x] for x in code],4),[])
                assert y==[1<<a if i==j else 0 for j in range(4)];outputs.append(y)
            records.append({'smith':[a,b],'messages':k,'encoders':chosen,'decoder':decoder,'decoded':outputs})
    # Minimal shared dual-number example: nilpotent identity has 4 exact labels but a kernel.
    assert mul(2,2,2)==0
    (OUT/'explicit_dense_decoders.json').write_text(json.dumps(records,indent=2))
    return {'classes':14,'actual_decoder_matrices_verified':14,'codewords':sum(x['messages'] for x in records),'dual_number_minimal_witness':'epsilon I_2; use any embedded F2 invertible-matrix basis and its flattening decoder; epsilon*(epsilon,0)=0'}
def paper_b():
    # One bit per (x,y) valuation, f indexed by x+2*y. Use complete formula truth masks.
    F=[]
    for c in range(16):
        F.append(tuple(sum(((c>>((x^i)+2*(y^j)))&1)<<(x+2*y) for x,y in product(range(2),repeat=2)) for i,j in product(range(2),repeat=2)))
    assert len(set(F))==16
    inside=0;example=None
    for A,B in product(F,repeat=2):
        C=tuple((A[2*i]&B[j])^(A[2*i+1]&B[2+j]) for i,j in product(range(2),repeat=2))
        inside+=C in F
        if C not in F and example is None:example={'A':A,'B':B,'product':C,'encoding':'four-bit truth masks indexed x+2y; matrix entries ordered i,j=0,1'}
    assert inside==112
    return {'LM_products':256,'inside':inside,'outside':256-inside,'counterexample':example}
def benchmark(root):
    p=root/'results/raw/gate_a_s1_s2.csv';rows=list(csv.DictReader(p.open()));ok=[r for r in rows if r['all_arms_ok']=='1' and r['correctness_status']=='OK']
    metrics=['final_degree','final_monomials','multiplications','output_unique_nodes','pair_terms','peak_monomials','serialized_bytes']
    diffs={m:sum(r['cm_frontend_sparse_'+m]!=r['generic_2support_sparse_'+m] for r in ok) for m in metrics}
    assert len(rows)==10500 and len(ok)==10389 and not any(diffs.values())
    return {'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':len(rows),'fully_admitted':len(ok),'not_fully_admitted':len(rows)-len(ok),'admitted_families':dict(Counter(r['family'] for r in ok)),'metric_differences':diffs,'fresh_timing_campaign':False}
def main():
    out={'python':sys.version,'platform':platform.platform(),'implementation_origin':'new in this consolidation; no supplied mathematical imports'}
    funcs=[('ring_inventory',ring_inventory),('dual_number_contextuality',dual_numbers),('dense_decoders',dense_decoders),('LM_product_boundary',paper_b)]
    for name,f in funcs:
        t=time.perf_counter();out[name]=f();out[name]['seconds']=time.perf_counter()-t;print(name,json.dumps(out[name]),flush=True)
        (OUT/'independent_results.json').write_text(json.dumps(out,indent=2))
    if len(sys.argv)>1:out['benchmark_raw_recount']=benchmark(Path(sys.argv[1]))
    out['success']=True;(OUT/'independent_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
