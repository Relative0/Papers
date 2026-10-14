from itertools import combinations, product
from collections import defaultdict, deque


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
    for i in range(n):
        for j in range(n):
            if i!=j and (i,j) in rel:
                for k in range(n):
                    if j!=k and (j,k) in rel and (i,k) not in rel:
                        return False
    return True


def natural_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    for mask in range(1<<len(pairs)):
        rel={(i,i) for i in range(n)}
        for t,p in enumerate(pairs):
            if mask>>t &1: rel.add(p)
        if transitive(n,rel):
            yield rel


def height(n, rel):
    dp=[0]*n
    for j in range(n):
        dp[j]=max([dp[i]+1 for i in range(j) if (i,j) in rel] or [0])
    return max(dp, default=0)


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
    rows=ch.get(k-1,[]); cols=ch.get(k,[])
    rid={s:i for i,s in enumerate(rows)}
    M=[[0]*len(cols) for _ in rows]
    for j,s in enumerate(cols):
        for t in range(len(s)):
            f=s[:t]+s[t+1:]
            M[rid[f]][j]^=1
    return M


def betti(n,rel):
    ch=chains(n,rel); md=max(ch,default=-1)
    ranks={0:0,md+1:0}
    for k in range(1,md+1): ranks[k]=rank_mod2(boundary(ch,k))
    return tuple(len(ch.get(k,[]))-ranks.get(k,0)-ranks.get(k+1,0) for k in range(md+1))


def relative_data(n, relP, relQ):
    chP=chains(n,relP); chQ=chains(n,relQ)
    md=max(chP,default=-1)
    dims={}
    ranks={0:0,md+1:0}
    relsimp={}
    for k in range(md+1):
        qset=set(chQ.get(k,[]))
        relsimp[k]=[s for s in chP.get(k,[]) if s not in qset]
        dims[k]=len(relsimp[k])
    for k in range(1,md+1):
        rows=relsimp.get(k-1,[]); cols=relsimp.get(k,[])
        rid={s:i for i,s in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,s in enumerate(cols):
            for t in range(len(s)):
                f=s[:t]+s[t+1:]
                if f in rid: M[rid[f]][j]^=1
        ranks[k]=rank_mod2(M)
    hb=tuple(dims[k]-ranks.get(k,0)-ranks.get(k+1,0) for k in range(md+1))
    return hb, relsimp, ranks


def comps(n,rel):
    adj=[set() for _ in range(n)]
    for i,j in rel:
        if i!=j:
            adj[i].add(j);adj[j].add(i)
    seen=set(); c=0
    for s in range(n):
        if s in seen: continue
        c+=1; dq=[s]; seen.add(s)
        while dq:
            u=dq.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); dq.append(v)
    return c


def is_redundant(n,rel,bits):
    return all(bits[i] <= bits[j] for i,j in rel)


def is_antitone(n,rel,bits):
    return all(bits[i] >= bits[j] for i,j in rel)


def chain_theorem(maxn=9):
    for n in range(1,maxn+1):
        rel={(i,j) for i in range(n) for j in range(i,n)}
        for bits in product([0,1], repeat=n):
            qr=qrel(n,rel,bits)
            B=betti(n,qr)
            fine_contract_hom = (B==(1,)+(0,)*(len(B)-1))
            strict_antitone = (0 in bits and 1 in bits and all(bits[i]>=bits[i+1] for i in range(n-1)))
            predicted = not strict_antitone
            if fine_contract_hom != predicted:
                raise AssertionError((n,bits,B,strict_antitone))
    print('chain exact classification verified through n=',maxn)


def bounded_height_tests(maxn=5):
    stats=defaultdict(int)
    first_h2=[]
    for n in range(1,maxn+1):
        posets=list(natural_posets(n))
        print('n',n,'natural transitive posets',len(posets))
        for rel in posets:
            h=height(n,rel)
            for bits in product([0,1], repeat=n):
                qr=qrel(n,rel,bits)
                red=is_redundant(n,rel,bits)
                hb,rs,ranks=relative_data(n,rel,qr)
                neutral=all(x==0 for x in hb)
                stats[(h,red,neutral)] += 1
                if h<=1 and neutral != red:
                    raise AssertionError(('height1 rigidity fail',n,rel,bits,hb))
                if h<=2:
                    d1=len(rs.get(1,[])); d2=len(rs.get(2,[])); r2=ranks.get(2,0)
                    criterion=(d1==d2==r2)
                    if neutral != criterion:
                        raise AssertionError(('height2 matrix criterion fail',n,bits,hb,d1,d2,r2))
                    if h==2 and neutral and not red and len(first_h2)<10:
                        first_h2.append((n,bits,d1,d2,betti(n,rel),betti(n,qr)))
                # antitone rigidity
                if is_antitone(n,rel,bits):
                    if neutral != red:
                        raise AssertionError(('antitone rigidity fail',n,bits,hb))
    print('height/neutral stats')
    for k,v in sorted(stats.items()): print(k,v)
    print('sample nonredundant height2 neutral',first_h2[:10])



def chain_quillen_tests(maxn=9):
    for n in range(1,maxn+1):
        rel={(i,j) for i in range(n) for j in range(i,n)}
        for bits in product([0,1], repeat=n):
            lower_all=True
            for k in range(1,n+1):
                pr=bits[:k]
                strict=(0 in pr and 1 in pr and all(pr[i]>=pr[i+1] for i in range(k-1)))
                if strict: lower_all=False; break
            upper_all=True
            for k in range(n):
                su=bits[k:]
                strict=(0 in su and 1 in su and all(su[i]>=su[i+1] for i in range(len(su)-1)))
                if strict: upper_all=False; break
            pred_lower=(bits[0]==0 or all(b==1 for b in bits))
            pred_upper=(bits[-1]==1 or all(b==0 for b in bits))
            assert lower_all==pred_lower, (n,bits,lower_all,pred_lower)
            assert upper_all==pred_upper, (n,bits,upper_all,pred_upper)
    print('chain lower/upper Quillen classifications verified through n=',maxn)


def chain_counts(maxn=10):
    rows=[]
    for n in range(1,maxn+1):
        red=defect=neutral_nonred=0
        for bits in product([0,1], repeat=n):
            nondec=all(bits[i]<=bits[i+1] for i in range(n-1))
            strictanti=(0 in bits and 1 in bits and all(bits[i]>=bits[i+1] for i in range(n-1)))
            if nondec: red+=1
            elif strictanti: defect+=1
            else: neutral_nonred+=1
        rows.append((n,red,defect,neutral_nonred))
    print('chain counts n, redundant, defective, neutral_nonredundant')
    for row in rows: print(*row)

if __name__=='__main__':
    chain_theorem(9)
    bounded_height_tests(5)
    chain_quillen_tests(9)
    chain_counts(10)
    print('ALL ASSERTIONS PASSED')
