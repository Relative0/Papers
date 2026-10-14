from itertools import combinations, product
from collections import defaultdict

# ---------- basic finite-poset / simplicial routines ----------
def rank_mod2(M):
    if not M: return 0
    A=[[x&1 for x in row] for row in M]
    m=len(A); n=len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        for i in range(m):
            if i!=r and A[i][c]:
                for j in range(c,n): A[i][j]^=A[r][j]
        r+=1
        if r==m: break
    return r

def det_bareiss(A):
    n=len(A)
    if n==0: return 1
    if any(len(r)!=n for r in A): return 0
    B=[row[:] for row in A]; sign=1; prev=1
    for k in range(n-1):
        p=next((i for i in range(k,n) if B[i][k]),None)
        if p is None:return 0
        if p!=k:B[k],B[p]=B[p],B[k];sign=-sign
        piv=B[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                B[i][j]=(B[i][j]*piv-B[i][k]*B[k][j])//prev
        for i in range(k+1,n): B[i][k]=0
        prev=piv
    return sign*B[n-1][n-1]

def qrel(P, labels):
    return {(i,j) for i,j in P if all(a<=b for a,b in zip(labels[i],labels[j]))}

def qrel_bit(P,b):
    return {(i,j) for i,j in P if b[i]<=b[j]}

def chains(n,P,k):
    # k-simplex = chain of k+1 vertices, natural-label posets only in exhaustive tests
    if k==0:return [(i,) for i in range(n)]
    return [s for s in combinations(range(n),k+1) if all((s[i],s[i+1]) in P for i in range(k))]

def rel_matrix(n,P,Q):
    E=[e for e in chains(n,P,1) if e not in set(chains(n,Q,1))]
    T=[t for t in chains(n,P,2) if t not in set(chains(n,Q,2))]
    er={e:i for i,e in enumerate(E)}
    B=[[0]*len(T) for _ in E]
    for j,(a,b,c) in enumerate(T):
        for e,s in [((b,c),1),((a,c),-1),((a,b),1)]:
            if e in er:B[er[e]][j]=s
    return E,T,B

def neutral_f2(n,P,Q):
    E,T,B=rel_matrix(n,P,Q)
    return len(E)==len(T) and rank_mod2(B)==len(E)

def perfect_matchings(B,cap=10**9):
    n=len(B)
    if n==0:return 1
    if any(len(r)!=n for r in B):return 0
    adj=[[j for j,x in enumerate(row) if x] for row in B]
    order=sorted(range(n),key=lambda i:len(adj[i])); used=[False]*n; c=0
    def rec(t):
        nonlocal c
        if c>=cap:return
        if t==n:c+=1;return
        i=order[t]
        for j in adj[i]:
            if not used[j]:used[j]=1;rec(t+1);used[j]=0
    rec(0);return c

def greedy_relative_collapse(B):
    if not B:return True
    R=set(range(len(B)));C=set(range(len(B[0])))
    while R:
        pick=None
        for i in R:
            ns=[j for j in C if B[i][j]]
            if len(ns)==1:pick=(i,ns[0]);break
        if pick is None:return False
        R.remove(pick[0]);C.remove(pick[1])
    return not C

def strict(P): return {(i,j) for i,j in P if i!=j}

def beat_reduce(n,P):
    alive=set(range(n)); steps=[]
    while len(alive)>1:
        found=None
        for x in sorted(alive):
            below=[y for y in alive if y!=x and (y,x) in P]
            above=[y for y in alive if y!=x and (x,y) in P]
            # down beat: below has greatest g
            for g in below:
                if all((y,g) in P for y in below): found=(x,'down',g);break
            if found:break
            for g in above:
                if all((g,y) in P for y in above): found=(x,'up',g);break
            if found:break
        if not found:break
        alive.remove(found[0]);steps.append(found)
    return alive,steps

# ---------- examples ----------
def ex_destructive():
    n=3; P={(i,i) for i in range(n)}|{(0,1),(1,2),(0,2)}
    b1=(0,1,0);b2=(1,0,1); labels=list(zip(b1,b2))
    Q1=qrel_bit(P,b1);Q2=qrel_bit(P,b2);Q=qrel(P,labels)
    assert neutral_f2(n,P,Q1) and neutral_f2(n,P,Q2)
    assert not neutral_f2(n,P,Q)
    return {'P':sorted(strict(P)),'b1':b1,'b2':b2,'Q':sorted(strict(Q))}

def ex_compensating():
    n=5
    P={(i,i) for i in range(n)}|{(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)}
    labels=[(1,1),(0,0),(0,1),(1,0),(1,1)]
    Q=qrel(P,labels);E,T,B=rel_matrix(n,P,Q)
    b1=tuple(x[0] for x in labels);b2=tuple(x[1] for x in labels)
    assert neutral_f2(n,P,Q)
    assert not neutral_f2(n,P,qrel_bit(P,b1)); assert not neutral_f2(n,P,qrel_bit(P,b2))
    # Neither order gives a safe first step.
    assert det_bareiss(B) in (1,-1)
    assert perfect_matchings(B)==1 and greedy_relative_collapse(B)
    return {'P':sorted(strict(P)),'labels':labels,'Q':sorted(strict(Q)),'E':E,'T':T,'B':B,'det':det_bareiss(B)}

def ex_multiorientation():
    n=8
    comps=[(0,2),(0,3),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(2,5),(2,6),(2,7),(3,5),(3,6),(3,7),(4,5),(4,6)]
    P={(i,i) for i in range(n)}|set(comps)
    labels=[(0,0,1),(0,1,1),(1,0,0),(1,1,0),(0,0,0),(0,1,1),(1,0,0),(1,1,0)]
    Q=qrel(P,labels);E,T,B=rel_matrix(n,P,Q)
    d=det_bareiss(B);pm=perfect_matchings(B,cap=100)
    assert d in (1,-1) and neutral_f2(n,P,Q)
    assert pm==3 and not greedy_relative_collapse(B)
    aliveP,stepsP=beat_reduce(n,P);aliveQ,stepsQ=beat_reduce(n,Q)
    assert len(aliveP)==1 and len(aliveQ)==1
    return {'P':sorted(strict(P)),'labels':labels,'Q':sorted(strict(Q)),'E':E,'T':T,'B':B,'det':d,'pm':pm,'stepsP':stepsP,'stepsQ':stepsQ}

# small exhaustive: all natural height<=2 posets n<=4, all 2-bit labels
def transitive(n,R):
    for i,j in list(R):
        if i==j:continue
        for k in range(n):
            if (j,k) in R and (i,k) not in R:return False
    return True

def nat_posets(n):
    ps=[(i,j) for i in range(n) for j in range(i+1,n)]
    for mask in range(1<<len(ps)):
        R={(i,i) for i in range(n)}|{p for t,p in enumerate(ps) if (mask>>t)&1}
        if transitive(n,R):yield R

def height(n,P):
    dp=[0]*n
    for j in range(n):dp[j]=max([dp[i]+1 for i in range(j) if (i,j) in P] or [0])
    return max(dp,default=0)

def exhaustive4():
    stats=defaultdict(int)
    for n in range(1,5):
        for P in nat_posets(n):
            if height(n,P)>2:continue
            for vals in product(range(4),repeat=n):
                labels=[((v>>1)&1,v&1) for v in vals]
                Q=qrel(P,labels); neutral=neutral_f2(n,P,Q)
                b1=tuple(x[0] for x in labels);b2=tuple(x[1] for x in labels)
                ind1=neutral_f2(n,P,qrel_bit(P,b1));ind2=neutral_f2(n,P,qrel_bit(P,b2))
                E,T,B=rel_matrix(n,P,Q)
                greedy=(len(E)==len(T) and greedy_relative_collapse(B))
                stats['total']+=1
                stats['neutral']+=int(neutral);stats['greedy']+=int(greedy)
                stats['both_ind_safe_joint_bad']+=int(ind1 and ind2 and not neutral)
    return dict(stats)

if __name__=='__main__':
    A=ex_destructive();B=ex_compensating();C=ex_multiorientation();S=exhaustive4()
    print('DESTRUCTIVE',A)
    print('COMPENSATING',B)
    print('MULTIORIENTATION det/pm/greedy',C['det'],C['pm'],False)
    print('MULTIORIENTATION P beat steps',C['stepsP'])
    print('MULTIORIENTATION Q beat steps',C['stepsQ'])
    print('EXHAUSTIVE_N_LE_4',S)

def enumerate_matchings(B,cap=100000):
    n=len(B); out=[]
    if n==0:return [()]
    adj=[[j for j,x in enumerate(row) if x] for row in B]
    order=sorted(range(n),key=lambda i:len(adj[i])); used=[False]*n; a=[None]*n
    def rec(t):
        if len(out)>=cap:return
        if t==n:out.append(tuple(a));return
        i=order[t]
        for j in adj[i]:
            if not used[j]:
                used[j]=True;a[i]=j;rec(t+1);used[j]=False;a[i]=None
    rec(0);return out

def matching_acyclic(B,m):
    n=len(B); G=[set() for _ in range(n)]
    for i,j in enumerate(m):
        for i2 in range(n):
            if i2!=i and B[i2][j]:G[i].add(i2)
    state=[0]*n
    def dfs(v):
        state[v]=1
        for w in G[v]:
            if state[w]==1:return False
            if state[w]==0 and not dfs(w):return False
        state[v]=2;return True
    return all(state[v] or dfs(v) for v in range(n))
