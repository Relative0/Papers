"""Independent finite checks for the 2026-09-18 CM novelty review.
No imports from the supplied audit. All ring arithmetic is exact.
Run: python independent_extensions.py
"""
from itertools import product, combinations_with_replacement, combinations, permutations
from pathlib import Path
import json,time,platform,math
import numpy as np
OUT=Path(__file__).resolve().parent

def binary_rank(rows):
    piv={}
    for a in rows:
        while a:
            j=a.bit_length()-1
            if j in piv:a^=piv[j]
            else:piv[j]=a;break
    return len(piv)

class Ring:
    def __init__(self,q,s,kind='poly'):
        self.q,self.s,self.kind=q,s,kind;self.order=q**s
        if q not in (2,3,4,5):raise ValueError('Supported residue fields: 2,3,4,5')
        if kind=='mod' and q==4:raise ValueError('mod model needs prime residue')
        self.name=(f'F{q}[u]/u^{s}' if kind=='poly' else f'Z/{q**s}')
        def fadd(a,b):return a^b if q==4 else (a+b)%q
        def fmul(a,b):
            if q!=4:return a*b%q
            r=0
            for _ in range(2):
                if b&1:r^=a
                b>>=1;a<<=1
                if a&4:a^=7
            return r
        self.fa,self.fm=fadd,fmul
        self.digits=[tuple((a//q**i)%q for i in range(s)) for a in range(self.order)]
        self.add=np.zeros((self.order,self.order),dtype=np.int64)
        self.mul=np.zeros_like(self.add)
        for a,b in product(range(self.order),repeat=2):
            if kind=='mod':self.add[a,b]=(a+b)%self.order;self.mul[a,b]=(a*b)%self.order;continue
            aa,bb=self.digits[a],self.digits[b]
            self.add[a,b]=sum(fadd(aa[i],bb[i])*q**i for i in range(s))
            co=[0]*s
            for i in range(s):
                for j in range(s-i):co[i+j]=fadd(co[i+j],fmul(aa[i],bb[j]))
            self.mul[a,b]=sum(co[i]*q**i for i in range(s))
        self.neg=[next(b for b in range(self.order) if self.add[a,b]==0) for a in range(self.order)]
        self.units=[a for a in range(self.order) if a%q]
        self.inv={a:next(b for b in self.units if self.mul[a,b]==1) for a in self.units}
        self.powers=[q**i for i in range(s)]+[0]
    def dot(self,x,y):
        a=0
        for b,c in zip(x,y):a=int(self.add[a,self.mul[b,c]])
        return a
    def rays(self,d):
        ans=set()
        for v in product(range(self.order),repeat=d):
            ix=next((i for i,a in enumerate(v) if a%self.q),None)
            if ix is not None:ans.add(tuple(int(self.mul[self.inv[v[ix]],a]) for a in v))
        return sorted(ans)
    def field_rays(self,d):
        ans=[]
        for v in product(range(self.q),repeat=d):
            ix=next((i for i,a in enumerate(v) if a),None)
            if ix is not None and v[ix]==1:ans.append(v)
        return ans
    def forced(self,rays,d):
        hs=self.field_rays(d)
        masks=[]
        for h in hs:
            mask=[]
            for v in rays:
                t=0
                for a,b in zip(v,h):t=self.fa(t,self.fm(a%self.q,b))
                mask.append(t!=0)
            masks.append(mask)
        return np.array(masks,dtype=bool)
    def support(self,left,right,vals):
        L=np.array(left,dtype=np.int64);R=np.array(right,dtype=np.int64)
        total=np.zeros((len(left),len(right)),dtype=np.int64)
        for i,a in enumerate(vals):
            term=self.mul[self.mul[L[:,i],self.powers[a]][:,None],R[:,i][None,:]]
            total=self.add[total,term]
        return total!=0

def possible_global_from_hyperplanes(support,forced_left,forced_right):
    """Exact by the hyperplane-selection lemma proved in the report."""
    witness=[]
    for i,a in enumerate(forced_left):
        forbidden_columns=(~support[a,:]).any(axis=0)
        for j,b in enumerate(forced_right):
            if not (forbidden_columns&b).any():witness.append((i,j))
    return witness

def full_bases_2(ring,rays):
    ans=[]
    for i,j in combinations(range(len(rays)),2):
        a,b=rays[i],rays[j]
        det=ring.add[ring.mul[a[0],b[1]],ring.neg[int(ring.mul[a[1],b[0]])]]
        if det%ring.q:ans.append((i,j))
    return ans

def two_sat(bases,support,extra=()):
    """Iterative Kosaraju SCC; no Warshall or historical audit imports."""
    nb=len(bases);nv=2*nb;n=2*nv
    adj=[[] for _ in range(n)];rev=[[] for _ in range(n)]
    def edge(a,b):adj[a].append(b);rev[b].append(a)
    for i,B in enumerate(bases):
        for j,C in enumerate(bases):
            for a,b in product(range(2),repeat=2):
                if not support[B[a],C[b]]:
                    x=2*i+a;y=2*(nb+j)+b
                    edge(x,y^1);edge(y,x^1)
    for x in extra:edge(x^1,x)
    seen=set();order=[]
    for st in range(n):
        if st in seen:continue
        seen.add(st);stack=[(st,0)]
        while stack:
            v,k=stack[-1]
            if k==len(adj[v]):order.append(v);stack.pop();continue
            w=adj[v][k];stack[-1]=(v,k+1)
            if w not in seen:seen.add(w);stack.append((w,0))
    comp=[-1]*n;c=0
    for st in reversed(order):
        if comp[st]>=0:continue
        comp[st]=c;stack=[st]
        while stack:
            v=stack.pop()
            for w in rev[v]:
                if comp[w]<0:comp[w]=c;stack.append(w)
        c+=1
    return all(comp[i]!=comp[i^1] for i in range(0,n,2))

def hardy_check(ring,a,b):
    p,q=ring.powers[a],ring.powers[b];c=ring.powers[b-a]
    F=((0,1),(1,0));X=((1,0),(1,1));C=((1,0),(ring.neg[c],1))
    def table(B,D):return [int(x) for x in ring.support(B,D,(a,b)).flat]
    tabs={'FF':table(F,F),'FX':table(F,X),'CX':table(C,X),'CF':table(C,F)}
    assert tabs=={'FF':[1,0,0,1],'FX':[0,1,1,1],'CX':[1,1,1,0],'CF':[0,1,1,1]},(ring.name,a,b,tabs)
    return {'a':a,'b':b,'p':p,'q_coefficient':q,'c':c,'C':C,'tables':tabs}

def chain_campaign():
    cases=[(2,1,'poly',2,2),(2,2,'poly',2,2),(2,3,'poly',2,2),(2,4,'poly',2,2),
           (2,5,'poly',2,2),(3,1,'poly',2,2),(3,2,'poly',2,2),(4,1,'poly',2,2),
           (4,2,'poly',2,2),(5,1,'poly',2,2),(2,2,'mod',2,2),(2,3,'mod',2,2),
           (2,4,'mod',2,2),(3,2,'mod',2,2),(3,3,'mod',2,2),
           (2,1,'poly',3,3),(2,2,'poly',3,3),(2,2,'mod',3,3),(3,2,'poly',3,3),
           (2,1,'poly',4,4),(2,2,'poly',4,4),(2,2,'poly',2,3)]
    rows=[];hardy=[]
    for q,s,kind,m,n in cases:
        start=time.time();ring=Ring(q,s,kind)
        L,R=ring.rays(m),ring.rays(n);HL,HR=ring.forced(L,m),ring.forced(R,n)
        bases=full_bases_2(ring,L) if m==n==2 else []
        if bases:assert len(bases)==q*(q+1)//2*q**(2*(s-1))
        classes=[]
        for vals in combinations_with_replacement(range(s+1),min(m,n)):
            S=ring.support(L,R,vals);r=sum(a<s for a in vals)
            k=sum(a==vals[0] for a in vals) if r else 0
            gs=possible_global_from_hyperplanes(S,HL,HR)
            expected='ZERO' if not r else ('STRONG' if k>=2 else ('LOGICAL' if r>=2 else 'LOCAL'))
            if r:assert bool(gs)==(expected!='STRONG'),(ring.name,m,n,vals,expected,gs)
            else:assert not gs and not S.any()
            checked_sat=False
            # Direct full-basis 2-SAT, independently of hyperplane reduction.
            if bases and len(bases)<=192:
                sat=two_sat(bases,S)
                assert sat==bool(gs),(ring.name,vals)
                checked_sat=True
            classes.append({'valuations':vals,'nonzero_factors':r,'minimal_multiplicity':k,'status':expected,
                            'hyperplane_pair_witnesses':len(gs),'full_basis_2sat_checked':checked_sat,
                            'possible_projective_effect_pairs':int(S.sum())})
        for a,b in combinations(range(s),2):hardy.append({'ring':ring.name,**hardy_check(ring,a,b)})
        row={'ring':ring.name,'dimensions':[m,n],'left_projective_rays':len(L),'right_projective_rays':len(R),
             'residue_hyperplanes':[len(HL),len(HR)],'basis_count_dim2':len(bases) or None,
             'classes':classes,'seconds':time.time()-start}
        rows.append(row);print('Chain campaign',ring.name,m,n,len(classes),'seconds',round(row['seconds'],3),flush=True)
        (OUT/'chain_ring_generalization.json').write_text(json.dumps(rows,indent=2))
    (OUT/'uniform_hardy_generalization.json').write_text(json.dumps(hardy,indent=2))

def degree_campaign():
    results=[]
    for n in range(1,5):
        start=time.time();N=1<<n;checked=0;units=0
        for f in range(1<<N):
            a=[(f>>j)&1 for j in range(N)];c=a[:];b=a[:]
            for i in range(n):
                for j in range(N):
                    if j&(1<<i):c[j]^=c[j^(1<<i)]
                    else:b[j]^=b[j|(1<<i)]
            degree=max((j.bit_count() for j,v in enumerate(c) if v),default=-1)
            nu=next((j for j,v in enumerate(b) if v),N)
            aug=min((j.bit_count() for j,v in enumerate(b) if v),default=n+1)
            assert bool(f.bit_count()%2)==(degree==n)==(nu==0)
            if f:assert aug==n-degree
            rows=[sum(a[(i-j)%N]<<j for j in range(N)) for i in range(N)]
            rank=binary_rank(rows)
            assert rank==N-nu
            units+=int(rank==N);checked+=1
        results.append({'variables':n,'truth_positions':N,'all_functions_checked':checked,'units':units,
                        'cyclic_rank_and_valuation_checked':True,'Berman_degree_radical_identity_checked':True,
                        'seconds':time.time()-start})
        print('Boolean campaign',n,checked,round(results[-1]['seconds'],3),flush=True)
    (OUT/'degree_and_filtration.json').write_text(json.dumps(results,indent=2))

def orthogonal_campaign():
    rows=[]
    for n in range(1,5):
        orth=[]
        for bits in range(1<<(n*n)):
            M=[(bits>>(n*i))&((1<<n)-1) for i in range(n)]
            if all(((M[i]&M[j]).bit_count()%2)==(i==j) for i,j in product(range(n),repeat=2)):orth.append(bits)
        span=binary_rank(orth)
        assert span==(n-1)**2+1
        rows.append({'dimension':n,'all_matrices_scanned':1<<(n*n),'orthogonal_count':len(orth),
                     'span_dimension':span,'predicted_span_dimension':(n-1)**2+1})
    # Invariant bilinear forms for W and D_R via exact linear equations (64 unknown entries).
    n=4;d=2*n
    R=np.zeros((n,n),dtype=np.uint8)
    for j in range(n):R[(j+1)%n,j]=1
    I=np.eye(n,dtype=np.uint8);Z=np.zeros((n,n),dtype=np.uint8)
    W=np.block([[I,Z],[I,I]]);D=np.block([[I,Z],[Z,R]])
    equations=[]
    for U in (W,D):
        for i,j in product(range(d),repeat=2):
            eq=1<<(i*d+j)
            for a,b in product(range(d),repeat=2):
                if U[a,i] and U[b,j]:eq^=1<<(a*d+b)
            equations.append(eq)
    nullity=d*d-binary_rank(equations)
    rows.append({'W_D_common_bilinear_solution_space_dimension':nullity,
                 'all_solutions_degenerate_by_block_proof':True})
    (OUT/'stronger_orthogonal_span.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':
    start=time.time();chain_campaign();degree_campaign();orthogonal_campaign()
    (OUT/'extension_run_summary.json').write_text(json.dumps({'success':True,'python':platform.python_version(),
         'platform':platform.platform(),'numpy':np.__version__,'total_seconds':time.time()-start},indent=2))
