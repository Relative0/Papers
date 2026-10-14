from itertools import combinations, product, permutations
from collections import defaultdict

# Basic finite-poset / F2 routines, independent of manuscript proofs.

def rank_mod2(M):
    A=[row[:] for row in M]
    if not A: return 0
    m=len(A); n=len(A[0]) if m else 0
    r=c=0
    while r<m and c<n:
        piv=next((i for i in range(r,m) if A[i][c]&1),None)
        if piv is None:
            c+=1; continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(m):
            if i!=r and A[i][c]:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1; c+=1
    return r

def transitive(n, rel):
    for i,j in rel:
        if i==j: continue
        for k in range(n):
            if (j,k) in rel and (i,k) not in rel:
                return False
    return True

def natural_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    for mask in range(1<<len(pairs)):
        rel={(i,i) for i in range(n)}
        for t,p in enumerate(pairs):
            if (mask>>t)&1: rel.add(p)
        if transitive(n,rel): yield rel

def qrel(n, rel, bits):
    return {(i,j) for (i,j) in rel if bits[i] <= bits[j]}

def chains(n, rel):
    out={0:[(i,) for i in range(n)]}
    for k in range(2,n+1):
        vals=[]
        for sub in combinations(range(n),k):
            if all((sub[i],sub[i+1]) in rel for i in range(k-1)):
                vals.append(sub)
        if vals: out[k-1]=vals
    return out

def boundary(ch,k):
    rows=ch.get(k-1,[]); cols=ch.get(k,[]); rid={s:i for i,s in enumerate(rows)}
    M=[[0]*len(cols) for _ in rows]
    for j,s in enumerate(cols):
        for t in range(len(s)):
            f=s[:t]+s[t+1:]
            M[rid[f]][j]^=1
    return M

def betti(n, rel):
    ch=chains(n,rel); md=max(ch,default=-1)
    ranks={0:0,md+1:0}
    for k in range(1,md+1): ranks[k]=rank_mod2(boundary(ch,k))
    return tuple(len(ch.get(k,[]))-ranks.get(k,0)-ranks.get(k+1,0) for k in range(md+1))

def relative_data(n,P,Q):
    cP=chains(n,P); cQ=chains(n,Q); md=max(cP,default=-1)
    rs={}; ranks={0:0,md+1:0}; mats={}
    for k in range(md+1):
        qset=set(cQ.get(k,[])); rs[k]=[s for s in cP.get(k,[]) if s not in qset]
    for k in range(1,md+1):
        rows=rs[k-1]; cols=rs[k]; rid={s:i for i,s in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,s in enumerate(cols):
            for t in range(len(s)):
                f=s[:t]+s[t+1:]
                if f in rid: M[rid[f]][j]^=1
        mats[k]=M; ranks[k]=rank_mod2(M)
    hb=[]
    for k in range(md+1):
        hb.append(len(rs[k])-ranks.get(k,0)-ranks.get(k+1,0))
    return tuple(hb),rs,mats

def height(n,rel):
    # natural labels are a linear extension
    dp=[0]*n
    for j in range(n):
        dp[j]=max([dp[i]+1 for i in range(j) if (i,j) in rel] or [0])
    return max(dp,default=0)

def comparable_component_sets(n,rel):
    adj=[set() for _ in range(n)]
    for i,j in rel:
        if i!=j:
            adj[i].add(j); adj[j].add(i)
    seen=set(); out=[]
    for s in range(n):
        if s in seen: continue
        st=[s]; seen.add(s); C=[]
        while st:
            u=st.pop(); C.append(u)
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        out.append(set(C))
    return out

def component_anchor_safe(n,rel,bits):
    for C in comparable_component_sets(n,rel):
        mins=[x for x in C if all((x,y) in rel for y in C)]
        maxs=[x for x in C if all((y,x) in rel for y in C)]
        ok=(any(bits[x]==0 for x in mins) or any(bits[x]==1 for x in maxs))
        if not ok: return False
    return True

def false_floor_safe(n,rel,bits):
    for p in range(n):
        cand=[q for q in range(n) if bits[q]==0 and (q,p) in rel]
        if not cand: return False
        # greatest candidate
        if not any(all((q,g) in rel for q in cand) for g in cand): return False
    return True

def true_ceiling_safe(n,rel,bits):
    for p in range(n):
        cand=[q for q in range(n) if bits[q]==1 and (p,q) in rel]
        if not cand: return False
        if not any(all((g,q) in rel for q in cand) for g in cand): return False
    return True

def count_perfect_matchings(M, cap=None):
    # M rows=left, cols=right; count exact for small matrices
    n=len(M)
    if n==0: return 1
    if any(len(r)!=n for r in M): return 0
    # backtracking smallest-degree row
    rows=list(range(n)); used=[False]*n; count=0
    order=sorted(rows,key=lambda i:sum(M[i]))
    def rec(k):
        nonlocal count
        if cap is not None and count>=cap: return
        if k==n:
            count+=1; return
        i=order[k]
        for j,x in enumerate(M[i]):
            if x and not used[j]:
                used[j]=True; rec(k+1); used[j]=False
    rec(0); return count

def greedy_leaf_exhausts(M):
    # Row leaf elimination in the deleted-edge/deleted-triangle graph.
    if not M: return True
    R=set(range(len(M))); C=set(range(len(M[0]) if M else 0))
    while R or C:
        if len(R)!=len(C): return False
        leaf=None
        for i in sorted(R):
            neigh=[j for j in C if M[i][j]]
            if len(neigh)==1:
                leaf=(i,neigh[0]); break
        if leaf is None: return False
        i,j=leaf
        R.remove(i); C.remove(j)
    return True

def is_redundant(rel,bits):
    return all(bits[i]<=bits[j] for i,j in rel)

def run(maxn=5):
    stats=defaultdict(int)
    h2=defaultdict(int)
    first_multi=[]
    for n in range(1,maxn+1):
        ps=list(natural_posets(n))
        print('n',n,'posets',len(ps))
        for P in ps:
            h=height(n,P)
            for bits in product([0,1], repeat=n):
                Q=qrel(n,P,bits)
                hb,rs,mats=relative_data(n,P,Q)
                neutral=all(x==0 for x in hb)
                anchor=component_anchor_safe(n,P,bits)
                floor=false_floor_safe(n,P,bits)
                ceil=true_ceiling_safe(n,P,bits)
                if anchor and not neutral:
                    raise AssertionError(('anchor fail',n,P,bits,hb))
                if floor and not neutral:
                    raise AssertionError(('floor fail',n,P,bits,hb))
                if ceil and not neutral:
                    raise AssertionError(('ceil fail',n,P,bits,hb))
                stats[(h,neutral,anchor,floor,ceil)] += 1
                if h<=2:
                    E=rs.get(1,[]); T=rs.get(2,[]); M=mats.get(2,[])
                    # transpose orientation irrelevant; M rows edges, cols triangles
                    pm=count_perfect_matchings(M) if len(E)==len(T) else 0
                    odd=(pm%2==1)
                    if neutral != odd:
                        raise AssertionError(('matching parity fail',n,bits,hb,len(E),len(T),pm,M))
                    unique=(pm==1)
                    greedy=greedy_leaf_exhausts(M) if len(E)==len(T) else False
                    if unique != greedy:
                        raise AssertionError(('unique-greedy fail',n,bits,pm,M))
                    if unique and not neutral:
                        raise AssertionError(('unique not neutral',n,bits,M))
                    if h==2 and neutral and not is_redundant(P,bits):
                        h2[('neutral_nonred',)] +=1
                        if unique: h2[('unique',)] +=1
                        elif pm>1:
                            h2[('odd_multi',)] +=1
                            if len(first_multi)<5:
                                first_multi.append((n,bits,len(E),pm,M,E,T))
    print('height2',dict(h2))
    print('first odd-multiple perfect matching examples:',first_multi)
    # aggregate guarantee coverage among neutral nonredundant by height
    cov=defaultdict(lambda:[0,0,0,0,0])
    for (h,neutral,anchor,floor,ceil),cnt in stats.items():
        if neutral:
            cov[h][0]+=cnt
            if anchor: cov[h][1]+=cnt
            if floor: cov[h][2]+=cnt
            if ceil: cov[h][3]+=cnt
            if anchor or floor or ceil: cov[h][4]+=cnt
    print('neutral coverage h: total anchor floor ceil union')
    for h,v in sorted(cov.items()): print(h,*v)

if __name__=='__main__':
    run(5)
    print('ALL ASSERTIONS PASSED')
