from itertools import combinations, product
from math import comb
import json
import sympy as sp


def subsets(n, max_size=None, exact=None):
    if exact is not None:
        sizes=[exact]
    else:
        sizes=range((n if max_size is None else max_size)+1)
    return [S for r in sizes for S in combinations(range(n),r)]


def points(n):
    return list(product((0,1), repeat=n))


def query_rows(n,k,exact=False):
    X=points(n)
    rows=[]
    Ss=subsets(n, exact=k) if exact else subsets(n,max_size=k)
    for S in Ss:
        for a in product((0,1), repeat=len(S)):
            rows.append([int(all(x[i]==a[j] for j,i in enumerate(S))) for x in X])
    return rows


def qvector(f,n,k):
    X=points(n)
    out=[]
    for S in subsets(n,max_size=k):
        for a in product((0,1), repeat=len(S)):
            out.append(sum(f[idx] for idx,x in enumerate(X) if all(x[i]==a[j] for j,i in enumerate(S))))
    return tuple(out)


def walsh(f,n,T):
    X=points(n)
    return sum(f[idx] * (-1)**sum(x[i] for i in T) for idx,x in enumerate(X))


def parity_pair(n,m):
    X=points(n)
    even=[int(sum(x[:m])%2==0) for x in X]
    odd=[1-v for v in even]
    return even,odd

results={"rank_checks":[],"fourier_equivalence":[],"parity_separation":[],"min_boolean_collision_distance":[]}

# Exact ranks for at-most-k and exactly-k workloads.
for n in range(0,6):
    for k in range(0,n+1):
        A=sp.Matrix(query_rows(n,k,False))
        E=sp.Matrix(query_rows(n,k,True))
        rA=A.rank(); rE=E.rank(); target=sum(comb(n,j) for j in range(k+1))
        assert rA==target==rE
        results["rank_checks"].append({"n":n,"k":k,"rank_at_most":rA,"rank_exact":rE,"target":target})

# Exhaustively verify Q_k equality iff low unnormalized Walsh equality for all Boolean pairs n<=3.
for n in range(0,4):
    N=2**n
    funcs=[tuple((mask>>i)&1 for i in range(N)) for mask in range(2**N)]
    for k in range(n+1):
        qgroups={}
        wgroups={}
        Ts=subsets(n,max_size=k)
        for f in funcs:
            qgroups.setdefault(qvector(f,n,k),[]).append(f)
            w=tuple(walsh(f,n,T) for T in Ts)
            wgroups.setdefault(w,[]).append(f)
        assert sorted(sorted(v) for v in qgroups.values()) == sorted(sorted(v) for v in wgroups.values())
        results["fourier_equivalence"].append({"n":n,"k":k,"functions":len(funcs),"q_fibers":len(qgroups),"walsh_fibers":len(wgroups),"pass":True})
        if k < n:
            mind=None
            for fiber in qgroups.values():
                if len(fiber)<2:
                    continue
                for i in range(len(fiber)):
                    for j in range(i+1,len(fiber)):
                        d=sum(a!=b for a,b in zip(fiber[i],fiber[j]))
                        if mind is None or d<mind:
                            mind=d
            target_dist=2**(k+1)
            assert mind==target_dist
            results["min_boolean_collision_distance"].append({"n":n,"k":k,"minimum_hamming_distance":mind,"target":target_dist})

# Verify adjacent-level parity separation through n=6.
for n in range(1,7):
    for k in range(n):
        f,g=parity_pair(n,k+1)
        same=qvector(f,n,k)==qvector(g,n,k)
        diff=qvector(f,n,k+1)!=qvector(g,n,k+1)
        assert same and diff
        results["parity_separation"].append({"n":n,"k":k,"parity_variables":k+1,"same_Qk":same,"different_Qk_plus_1":diff})

with open('/mnt/data/theory_work/qk_verification_results.json','w') as fh:
    json.dump(results,fh,indent=2)
print('PASS')
print('rank cases',len(results['rank_checks']))
print('exhaustive Fourier-equivalence cases',len(results['fourier_equivalence']))
print('parity separation cases',len(results['parity_separation']))
