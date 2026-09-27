"""Independent, bounded checks for the viability review; no manuscript imports."""
import itertools as it, json, pathlib, math, hashlib, time
W=pathlib.Path(__file__).parent
def rank2(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return len(piv)
def chains(n,R):
    return [tuple(c) for k in range(1,n+1) for c in it.combinations(range(n),k) if all((a,b) in R for a,b in it.combinations(c,2))]
def betti(n,R):
    C=chains(n,R);by=[[c for c in C if len(c)==k+1] for k in range(n)]
    ranks=[0]
    for k in range(1,n):
        ix={c:i for i,c in enumerate(by[k-1])}
        ranks.append(rank2([sum(1<<ix[c[:j]+c[j+1:]] for j in range(len(c))) for c in by[k]]))
    ranks.append(0)
    return [len(by[k])-ranks[k]-ranks[k+1] for k in range(n)]
def thin(R,bs):return {(x,y) for x,y in R if all(b[x]<=b[y] for b in bs)}
out={"scope":"Fresh finite spot checks, not general proof certification or performance benchmarks","checks":{}}
t=time.time()
# Direct projective-basis support enumeration over Z/4, independent of Smith criterion.
v=list(it.product(range(4),repeat=2));primitive=[x for x in v if any(a%2 for a in x)]
rays=sorted({min(x,tuple(3*a%4 for a in x)) for x in primitive})
bases=[p for p in it.combinations(range(len(rays)),2) if (rays[p[0]][0]*rays[p[1]][1]-rays[p[0]][1]*rays[p[1]][0])%2]
cases=[]
for a,b,expected in [(0,2,'local'),(1,2,'local'),(0,1,'logical_not_strong'),(0,0,'strong'),(1,1,'strong')]:
    D=(2**a%4,2**b%4)
    allowed=[[sum(x[i]*D[i]*y[i] for i in range(2))%4!=0 for y in rays] for x in rays]
    possible={(i,j,x,y) for i,A in enumerate(bases) for j,B in enumerate(bases) for x in A for y in B if allowed[x][y]}
    covered=set();valid=0
    for choice in it.product(*bases):
        Y=[y for y in range(len(rays)) if all(allowed[x][y] for x in set(choice))]
        Boptions=[set(B)&set(Y) for B in bases]
        if all(Boptions):
            valid+=1
            for i,x in enumerate(choice):
                for j,opts in enumerate(Boptions):
                    covered.update((i,j,x,y) for y in opts)
    got='strong' if valid==0 else ('local' if covered==possible else 'logical_not_strong')
    assert got==expected
    cases.append(dict(smith_exponents=[a,b],classification=got,possible_events=len(possible),covered_events=len(covered),extendible_A_choices=valid))
out['checks']['P01_Z4_direct_support']={'rays':len(rays),'unordered_bases':len(bases),'cases':cases,'note':'Unordered bases suffice since ordering only relabels outcomes. Exponent 2 means zero in Z/4.'}
# All naturally labelled orders and all transitive suborders through four vertices.
pairs_count=0;max_min=0
for n in range(1,5):
    edges=list(it.combinations(range(n),2))
    orders=[]
    for mask in range(1<<len(edges)):
        R={e for j,e in enumerate(edges) if mask>>j&1}
        if all((a,c) in R for a,b in R for b2,c in R if b==b2):orders.append(R)
    for P in orders:
        for Q in orders:
            if not Q<=P:continue
            E=sorted(P-Q);full=(1<<len(E))-1
            # Cover DP uses only Q-upsets. Direct DP uses all bit maps and exact retained relations.
            masks=[]
            for b in it.product((0,1),repeat=n):
                if all(b[x]<=b[y] for x,y in Q):
                    masks.append(sum(1<<j for j,(x,y) in enumerate(E) if b[x]>b[y]))
            dp={0:0}
            for m in masks:
                for old,c in list(dp.items()):dp[old|m]=min(dp.get(old|m,n+1),c+1)
            direct={frozenset(P):0}
            for b in it.product((0,1),repeat=n):
                for old,c in list(direct.items()):
                    nxt=frozenset(thin(old,[b]))
                    direct[nxt]=min(direct.get(nxt,n+1),c+1)
            assert dp[full]==direct[frozenset(Q)]
            # Principal Q-upsets always separate each deleted oriented pair.
            assert all(any(x in {z for z in range(n) if z==s or (s,z) in Q} and y not in {z for z in range(n) if z==s or (s,z) in Q} for s in range(n)) for x,y in E)
            pairs_count+=1;max_min=max(max_min,dp[full])
out['checks']['GR_corrected_cover']={'P_Q_pairs':pairs_count,'max_vertices':4,'maximum_observed_minimum':max_min,'result':'Cover optimum equals direct bit-family optimum in every case'}
P=set(it.combinations(range(3),2));bs=[(0,1,0),(1,0,1)]
out['checks']['GR_destructive_pair']={'single_betti':[betti(3,thin(P,[b])) for b in bs],'joint_betti':betti(3,thin(P,bs))}
assert out['checks']['GR_destructive_pair']=={'single_betti':[[1,0,0],[1,0,0]],'joint_betti':[2,0,0]}
P={(0,i) for i in range(1,5)}|{(1,i) for i in range(2,5)};labels=[(1,1),(0,0),(0,1),(1,0),(1,1)];bs=list(zip(*labels))
out['checks']['GR_compensating_pair']={'single_betti':[betti(5,thin(P,[b])) for b in bs],'joint_betti':betti(5,thin(P,bs))}
assert out['checks']['GR_compensating_pair']=={'single_betti':[[1,1,0,0,0],[1,1,0,0,0]],'joint_betti':[1,0,0,0,0]}
# P02 Reed-Muller evaluation ranks. Independent GF2 row reduction.
rows=[]
for n in range(1,8):
    for q in range(n+1):
        monos=[s for s in range(1<<n) if s.bit_count()<=q]
        rank=rank2([sum(1<<j for j,s in enumerate(monos) if x&s==s) for x in range(1<<n)])
        assert rank==sum(math.comb(n,k) for k in range(q+1))
        rows.append({'n':n,'q':q,'rank':rank})
out['checks']['P02_evaluation_ranks']={'cases':rows,'note':'Confirms the coefficient-space calculation only, not reachability of arbitrary rank-saturating states.'}
# PC elementary obstruction and BR idempotents; polynomial-basis arithmetic.
def mul(a,b):
    r=0
    for i in range(4):
        if b>>i&1:r^=a<<i
    return r&15
assert mul(2,8)==0
idempotents=[a for a in range(16) if mul(a,a)==a];assert idempotents==[0,1]
out['checks']['PC_BR_zero_divisors']={'u_times_u3':mul(2,8),'idempotents':idempotents}
# GU exact positive rational interior region witnesses; boundary completeness is not tested.
from fractions import Fraction as F
def scores(a,b):return [a+b+a*b,a-b-a*b,-a+b-a*b,-a-b+a*b]
pts={'AND':(F(1),F(1)),'X':(F(1),F(1,4)),'Y':(F(1,4),F(1)),'XNOR':(F(3),F(3))}
out['checks']['GU_rational_witnesses']={k:[str(s) for s in scores(*p)] for k,p in pts.items()}
assert [int(x>0) for x in scores(*pts['AND'])]==[1,0,0,0]
assert [int(x>0) for x in scores(*pts['X'])]==[1,1,0,0]
assert [int(x>0) for x in scores(*pts['Y'])]==[1,0,1,0]
assert [int(x>0) for x in scores(*pts['XNOR'])]==[1,0,0,1]
out['elapsed_seconds']=round(time.time()-t,3)
out['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
out['result']='PASS'
(W/'spot_check_results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
print(json.dumps({k:v for k,v in out['checks'].items() if k!='P02_evaluation_ranks'},indent=2))
