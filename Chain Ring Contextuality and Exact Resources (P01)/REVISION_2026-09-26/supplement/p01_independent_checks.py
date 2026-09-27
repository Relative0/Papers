#!/usr/bin/env python3
"""Independent P01 checks. No manuscript-package imports.
Run: python p01_independent_checks.py --out RESULTS
Support is decided by direct contraction tables and implication graphs,
not Smith data. Smith data are calculated only for subsequent comparison.
"""
from __future__ import annotations
import argparse, csv, hashlib, itertools as it, json, platform, random, sys, time
from collections import Counter
from pathlib import Path

class Ring:
    def __init__(self,p,s,kind='poly'):
        self.p,self.s,self.kind=p,s,kind; self.n=4 if kind=='F4' else p**s
        self.length=1 if kind=='F4' else s; self.pi=p if self.length>1 else 0
        self.name=f'Z/{self.n}Z' if kind=='int' else ('F4' if kind=='F4' else f'F{p}[u]/(u^{s})')
        def digits(a): return [(a//p**i)%p for i in range(s)]
        def add(a,b):
            if kind=='int': return (a+b)%self.n
            if kind=='F4': return a^b
            return sum(((x+y)%p)*p**i for i,(x,y) in enumerate(zip(digits(a),digits(b))))
        def mul(a,b):
            if kind=='int': return (a*b)%self.n
            if kind=='F4':
                v=0
                for i in range(2):
                    if (b>>i)&1: v^=a<<i
                return v^7 if v&4 else v
            x,y=digits(a),digits(b)
            return sum((sum(x[j]*y[i-j] for j in range(i+1))%p)*p**i for i in range(s))
        self.add=[[add(a,b) for b in range(self.n)] for a in range(self.n)]
        self.mul=[[mul(a,b) for b in range(self.n)] for a in range(self.n)]
        self.neg=[next(b for b in range(self.n) if self.add[a][b]==0) for a in range(self.n)]
        self.inv={a:next((b for b in range(self.n) if self.mul[a][b]==1),None) for a in range(self.n)}
        self.units=[a for a in range(self.n) if self.inv[a] is not None]; self.val=[]
        for a in range(self.n):
            if kind=='F4': self.val.append(int(a==0)); continue
            v=0; b=a
            while v<s and b%p==0: v+=1; b//=p
            self.val.append(v)
    def sub(self,a,b): return self.add[a][self.neg[b]]
    def power(self,a,k):
        r=1
        for _ in range(k): r=self.mul[r][a]
        return r
    def matmul(self,A,B):
        C=[[0]*len(B[0]) for _ in A]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for h in range(len(B)): C[i][j]=self.add[C[i][j]][self.mul[A[i][h]][B[h][j]]]
        return C
    def inverse(self,A):
        n=len(A); a=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
        for j in range(n):
            k=next((i for i in range(j,n) if a[i][j] in self.units),None)
            if k is None: return None
            a[j],a[k]=a[k],a[j]; z=self.inv[a[j][j]]; a[j]=[self.mul[z][v] for v in a[j]]
            for i in range(n):
                if i!=j:
                    z=a[i][j]; a[i]=[self.sub(v,self.mul[z][w]) for v,w in zip(a[i],a[j])]
        return [row[n:] for row in a]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(A): return [list(x) for x in zip(*A)]
def reshape(m): return [list(m[:2]),list(m[2:])]
def rank_field(rows,p):
    if not rows: return 0
    a=[[v%p for v in r] for r in rows]; rank=0
    for j in range(len(a[0])):
        k=next((i for i in range(rank,len(a)) if a[i][j]),None)
        if k is None: continue
        a[k],a[rank]=a[rank],a[k]; z=pow(a[rank][j],-1,p); a[rank]=[(z*v)%p for v in a[rank]]
        for i in range(len(a)):
            if i!=rank:
                z=a[i][j]; a[i]=[(v-z*w)%p for v,w in zip(a[i],a[rank])]
        rank+=1
        if rank==len(a): break
    return rank

def smith2(R,m):
    if not any(m): return R.length,R.length
    ix=min(range(4),key=lambda i:R.val[m[i]]); A=reshape(m); i,j=divmod(ix,2)
    if i: A.reverse()
    if j: A=[row[::-1] for row in A]
    t=next(t for t in range(R.n) if R.mul[A[0][0]][t]==A[1][0])
    return R.val[A[0][0]],R.val[R.sub(A[1][1],R.mul[t][A[0][1]])]
def expected_type(R,m):
    a,b=smith2(R,m)
    return 'excluded' if a==R.length else ('local' if b==R.length else ('strong' if a==b else 'logical_not_strong'))

class SupportChecker:
    def __init__(self,R):
        self.R=R
        def canon(x): return min(tuple(R.mul[u][t] for t in x) for u in R.units)
        self.rays=sorted({canon(x) for x in it.product(range(R.n),repeat=2) if any(v in R.units for v in x)})
        self.bases=[]
        for i,j in it.combinations(range(len(self.rays)),2):
            x,y=self.rays[i],self.rays[j]
            if R.sub(R.mul[x[0]][y[1]],R.mul[x[1]][y[0]]) in R.units: self.bases.append((i,j))
        self.cache={}
    def table(self,m):
        R=self.R; a,b,c,d=m; T=[]
        for x,y in self.rays:
            v=R.add[R.mul[x][a]][R.mul[y][c]]; w=R.add[R.mul[x][b]][R.mul[y][d]]
            T.append([R.add[R.mul[v][z]][R.mul[w][t]]!=0 for z,t in self.rays])
        return T
    def classify(self,m):
        T=self.table(m); key=bytes(v for row in T for v in row)
        if key in self.cache: return self.cache[key]
        B=self.bases; n=len(B); L=4*n; reach=[1<<i for i in range(L)]
        for i,aa in enumerate(B):
            for j,bb in enumerate(B):
                for x,y in it.product(range(2),repeat=2):
                    if not T[aa[x]][bb[y]]:
                        u=2*i+x; v=2*(n+j)+y
                        reach[u]|=1<<(v^1); reach[v]|=1<<(u^1)
        for k in range(L):
            mask=1<<k; row=reach[k]
            for i in range(L):
                if reach[i]&mask: reach[i]|=row
        if any(((reach[i]>>(i^1))&1) and ((reach[i^1]>>i)&1) for i in range(0,L,2)):
            result=('strong',None)
        else:
            even=sum(1<<i for i in range(0,L,2)); odd=even<<1; witness=None
            def bad(r): return bool(r&(((r&even)<<1)|((r&odd)>>1)))
            for i,aa in enumerate(B):
                for j,bb in enumerate(B):
                    for x,y in it.product(range(2),repeat=2):
                        if T[aa[x]][bb[y]] and bad(reach[2*i+x]|reach[2*(n+j)+y]): witness=[i,j,x,y]; break
                    if witness is not None: break
                if witness is not None: break
            result=('logical_not_strong' if witness else 'local',witness)
        self.cache[key]=result; return result
    def brute(self,m):
        T=self.table(m); n=len(self.bases); ext=set(); assignments=0
        for b in it.product(range(2),repeat=2*n):
            if all(T[self.bases[i][b[i]]][self.bases[j][b[n+j]]] for i in range(n) for j in range(n)):
                assignments+=1; ext.update((i,j,b[i],b[n+j]) for i in range(n) for j in range(n))
        if not assignments:return 'strong'
        for i,a in enumerate(self.bases):
            for j,b in enumerate(self.bases):
                for x,y in it.product(range(2),repeat=2):
                    if T[a[x]][b[y]] and (i,j,x,y) not in ext: return 'logical_not_strong'
        return 'local'

def support_tests(out, exhaustive_up_to_order=9):
    rng=random.Random(20260926); records=[]; summaries=[]
    rings=[Ring(2,1),Ring(3,1),Ring(2,1,'F4'),Ring(2,2),Ring(2,2,'int'),Ring(2,3),Ring(2,3,'int'),Ring(3,2),Ring(3,2,'int'),Ring(2,4)]
    for R in rings:
        start=time.monotonic(); S=SupportChecker(R); all_cases=R.n<=exhaustive_up_to_order
        if all_cases: matrices=list(it.product(range(R.n),repeat=4))[1:]
        else:
            matrices=[(R.power(R.pi,a),0,0,R.power(R.pi,b)) for a in range(R.length) for b in range(a,R.length+1)]
            matrices+=sorted({tuple(rng.randrange(R.n) for _ in range(4)) for _ in range(24)}-{(0,0,0,0)})
        counts=Counter()
        for m in matrices:
            actual,witness=S.classify(m); expected=expected_type(R,m); counts[actual]+=1
            assert actual==expected,(R.name,m,actual,expected)
            if R.n==2: assert S.brute(m)==actual
            records.append(dict(ring=R.name,matrix=list(m),smith=list(smith2(R,m)),actual=actual,expected=expected,witness=witness))
        summaries.append(dict(ring=R.name,resources=len(matrices),exhaustive_all_resources=all_cases,rays=len(S.rays),bases=len(S.bases),counts=dict(counts),distinct_support_tables=len(S.cache),mismatches=0,seconds=time.monotonic()-start))
        print('SUPPORT',summaries[-1],flush=True)
    (out/'support_cases.json').write_text(json.dumps(records,indent=2)); return summaries

def inventory(out):
    R=Ring(2,4); c=Counter(smith2(R,m) for m in it.product(range(R.n),repeat=4)); aggregate=Counter()
    for (a,b),n in c.items(): aggregate['excluded' if a==4 else ('local' if b==4 else ('strong' if a==b else 'logical_not_strong'))]+=n
    rows=[dict(a=a,b=b,count=n) for (a,b),n in sorted(c.items())]
    with (out/'A2_smith_inventory.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['a','b','count']); w.writeheader(); w.writerows(rows)
    return dict(total=sum(c.values()),aggregate=dict(aggregate),classes=rows,method='Exhaustive ring elimination. Category totals use the Smith-invariance proof and separately SAT-tested representatives, not direct SAT on all 65535 matrices.')

def hardy_tests():
    records=[]
    for R in [Ring(2,1),Ring(3,1),Ring(2,2),Ring(2,3),Ring(2,4),Ring(3,2),Ring(2,2,'int'),Ring(2,3,'int'),Ring(3,2,'int')]:
        for a in range(R.length):
            for b in range(a,R.length):
                p,q,c=R.power(R.pi,a),R.power(R.pi,b),R.power(R.pi,b-a)
                D=[[p,0],[0,q]]; F=[[0,1],[1,0]]; X=[[1,0],[1,1]]; C=[[1,0],[R.neg[c],1]]
                T=[R.matmul(R.matmul(A,D),transpose(B)) for A,B in [(F,F),(F,X),(C,X),(C,F)]]
                strings=[''.join('1' if z else '0' for row in t for z in row) for t in T]
                assert strings==['1001','0111','1110','0111']; records.append(dict(ring=R.name,a=a,b=b,strings=strings))
    return dict(cases=len(records),status='PASS',details=records)

def analyzer_tests(out):
    results=[]
    for R in [Ring(2,2,'int'),Ring(2,3,'int'),Ring(3,2,'int'),Ring(2,2),Ring(2,3),Ring(2,4),Ring(3,2)]:
        for d in [1,2,3,4]:
            I=eye(d); candidates=[I]
            for i in range(d):
                for j in range(d):
                    if i!=j:
                        E=[r[:] for r in I]; E[i][j]=1; candidates.append(E)
                if d>1:
                    j=(i+1)%d; P=[r[:] for r in I]; P[i],P[j]=P[j],P[i]; E=[r[:] for r in I]; E[j][i]=1
                    candidates += [P,R.matmul(P,E)]
            mats=[]; flat=[]
            for A in candidates:
                v=sum(A,[])
                if rank_field(flat+[v],R.p)>len(flat): mats.append(A); flat.append(v)
            assert len(flat)==d*d and R.inverse(flat) is not None and all(R.inverse(A) is not None for A in mats)
            M=[r[:] for r in I]
            if d>1:M[0][1]=1
            for E in mats:
                T=R.matmul(transpose(M),transpose(E)); C=R.inverse(T)
                assert C is not None and R.matmul(C,T)==I
            results.append(dict(ring=R.name,d=d,effects=mats,analysis=flat,status='PASS'))
    (out/'independent_analyzer_certificates.json').write_text(json.dumps(results,indent=2))
    return dict(configurations=len(results),status='PASS',scope='Both invertibilities and branch correction identities for one explicitly invertible resource per dimension; d=1 included.')

def coding_certificates(out):
    results=[]
    for R in [Ring(2,2,'int'),Ring(2,3,'int'),Ring(3,2,'int'),Ring(2,2),Ring(2,3),Ring(2,4),Ring(3,2)]:
        GL=[reshape(m) for m in it.product(range(R.n),repeat=4) if R.sub(R.mul[m[0]][m[3]],R.mul[m[1]][m[2]]) in R.units]
        for a in range(R.length):
            for b in range(a,R.length+1):
                D=[[R.power(R.pi,a),0],[0,R.power(R.pi,b)]]; N=[[1,0],[0,R.power(R.pi,b-a)]]; enc=[]; cols=[]
                for U in GL:
                    v=sum(R.matmul(U,N),[])
                    if rank_field(cols+[v],R.p)>len(cols): enc.append(U); cols.append(v)
                k=len(cols); Bcols=[x[:] for x in cols]
                for v in eye(4):
                    if rank_field(Bcols+[v],R.p)>len(Bcols): Bcols.append(v)
                decoder=R.inverse(transpose(Bcols)); assert decoder is not None; decoded=[]
                for i,U in enumerate(enc):
                    vector=[[v] for v in sum(R.matmul(U,D),[])]; res=[r[0] for r in R.matmul(decoder,vector)]
                    assert res==[R.power(R.pi,a) if j==i else 0 for j in range(4)]; decoded.append(res)
                assert k==2*(2 if a==b else 1)
                results.append(dict(ring=R.name,smith=[a,b],encoders=enc,decoder=decoder,decoded=decoded,messages=k))
    (out/'independent_coding_certificates.json').write_text(json.dumps(results,indent=2))
    return dict(cases=len(results),status='PASS',scope='Lower-bound certificates only; no exhaustive upper-bound search over ring decoders.')

def binary_coding_exhaustive():
    R=Ring(2,1); GL2=[reshape(m) for m in it.product(range(2),repeat=4) if R.inverse(reshape(m)) is not None]; dec=[]
    for rows in it.permutations(range(1,16),4):
        piv={}
        for x in rows:
            while x:
                j=x.bit_length()-1
                if j in piv:x^=piv[j]
                else:piv[j]=x;break
        if len(piv)==4:dec.append(rows)
    assert len(dec)==20160
    parity=[i.bit_count()%2 for i in range(16)]; results=[]
    for m in it.product(range(2),repeat=4):
        if not any(m):continue
        orbit={sum(v<<i for i,v in enumerate(sum(R.matmul(U,reshape(m)),[]))) for U in GL2}; best=0
        for rows in dec:
            masks={sum(parity[row&v]<<i for i,row in enumerate(rows)) for v in orbit}; dp={0:0}
            for mask in masks:
                for used,n in list(dp.items()):
                    if not used&mask:dp[used|mask]=max(dp.get(used|mask,0),n+1)
            best=max(best,max(dp.values()))
        a,b=smith2(R,m); assert best==(4 if b==0 else 2); results.append(dict(matrix=list(m),maximum=best))
    return dict(resources=15,decoders_per_resource=20160,status='PASS',results=results)

def two_setting_test():
    effects=[[(1,0),(0,1)],[(1,0),(1,1)]]; masks=[]
    for assignment in it.product(range(2),repeat=6):
        cm=[]
        for contexts in it.product(range(2),repeat=3):
            rows=[effects[contexts[p]][assignment[2*p+contexts[p]]] for p in range(3)]; mask=0
            for i,idx in enumerate(it.product(range(2),repeat=3)):
                if all(rows[p][idx[p]] for p in range(3)):mask|=1<<i
            cm.append(mask)
        masks.append(cm)
    for state in range(1,256):assert any(all((state&m).bit_count()%2 for m in mm) for mm in masks)
    return dict(parties=3,states=255,assignments_per_state_maximum=64,status='PASS',scope='One representative pair of distinct settings per party; all distinct pairs equivalent by GL2(F2).')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('independent_results'));ap.add_argument('--exhaustive-up-to-order',type=int,default=9);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True);t=time.monotonic()
    r=dict(python=sys.version,platform=platform.platform(),seed=20260926,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    r['support']=support_tests(args.out,args.exhaustive_up_to_order);r['inventory']=inventory(args.out);r['hardy']=hardy_tests();r['analyzers']=analyzer_tests(args.out);r['coding_certificates']=coding_certificates(args.out);r['binary_coding']=binary_coding_exhaustive();r['two_settings']=two_setting_test();r['seconds']=time.monotonic()-t
    (args.out/'independent_results.json').write_text(json.dumps(r,indent=2)); print('ALL TESTS PASS',r['seconds'],flush=True)
if __name__=='__main__':main()
