import json,csv
from pathlib import Path
from functools import lru_cache
from itertools import combinations
W=frozenset(range(4)); EVENTS=tuple(range(16))

def splits(E,S):
    a=frozenset(w for w in S if (E>>w)&1); return a,S-a

def nonadaptive(pool):
    ev=list(pool)
    for k in range(len(ev)+1):
        for comb in combinations(ev,k):
            sigs=[tuple((E>>w)&1 for E in comb) for w in W]
            if len(set(sigs))==4:return k
    return None

def adaptive(pool):
    pool=tuple(pool)
    @lru_cache(None)
    def V(S):
        S=frozenset(S)
        if len(S)<=1:return 0
        best=99
        for E in pool:
            a,b=splits(E,S)
            if not a or not b:continue
            best=min(best,1+max(V(a),V(b)))
        return best
    d=V(W); return None if d>=99 else d
counts={}
for mask in range(1<<16):
    pool=[e for e in EVENTS if mask>>e&1]
    na=nonadaptive(pool); ad=adaptive(pool)
    counts[(na,ad)]=counts.get((na,ad),0)+1
solv=sum(v for (na,ad),v in counts.items() if na is not None)
gap=sum(v for (na,ad),v in counts.items() if na is not None and ad is not None and ad<na)
summary={'all_test_pools':1<<16,'solvable_pools':solv,'strict_adaptive_advantage_pools':gap,
         'counts':{f'nonadaptive_{na}_adaptive_{ad}':v for (na,ad),v in counts.items() if na is not None}}
root=Path(__file__).resolve().parents[1]
(root/'results'/'ADAPTIVE_PROTOCOL_SUMMARY.json').write_text(json.dumps(summary,indent=2))
with (root/'results'/'ADAPTIVE_PROTOCOL_SUMMARY.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['nonadaptive_optimum','adaptive_worst_case_depth','pool_count'])
    for (na,ad),v in sorted(counts.items(),key=lambda kv:(99 if kv[0][0] is None else kv[0][0],99 if kv[0][1] is None else kv[0][1])):
        if na is not None:w.writerow([na,ad,v])
print(json.dumps(summary,indent=2))
