"""Larger complete bipartite family, using the exact height-one legality rule.

This supplementary solver uses a bitwise isotonicity predicate and checks it
against BOTH independent implementations on 1000 seeded (support,query) cases.
It is intentionally separate from run_exhaustive.solve and solve_case.
"""
import csv,json,random
from functools import lru_cache
from pathlib import Path
import repair_graph,boundary_matrix

HERE=Path(__file__).resolve().parent

def main():
    rows=[]
    rng=random.Random(29102026)
    for k in (2,3,4):
        n=1<<k;full=(1<<n)-1;low=(1<<(n//2))-1;up=full^low
        codes=[x for x in range(n) if x.bit_count()%2==0]+[x for x in range(n) if x.bit_count()%2==1]
        coords=[sum((x>>j&1)<<i for i,x in enumerate(codes)) for j in range(k)]
        base=coords+[1<<i for i in range(n)]
        queries=tuple(sorted(set(base+[full^q for q in base])))
        def safe(S,q):return not(S&low&q) or not(S&up&(full^q))
        checks=0
        for _ in range(1000):
            S=rng.randrange(1,full+1);q=rng.choice(queries)
            states=[i for i in range(n) if S>>i&1]
            pairs=tuple((i,j) for i,a in enumerate(states) for j,b in enumerate(states) if a<n//2<=b)
            qp=sum((q>>s&1)<<i for i,s in enumerate(states))
            assert safe(S,q)==repair_graph.analyze(len(states),pairs,qp)[0]==boundary_matrix.analyze(len(states),pairs,qp)[0]
            checks+=1
        @lru_cache(None)
        def rf(S):
            size=S.bit_count()
            if size<2:return 0
            lower=(size-1).bit_length();best=size-1
            for q in queries:
                T=S&q;U=S^T
                if not T or not U or not safe(S,q):continue
                best=min(best,1+max(rf(T),rf(U)))
                if best==lower:break
            return best
        depth=rf(full)
        assert depth==n//2+k-1
        rows.append([n,k,len(queries),k,depth,depth-k,checks,rf.cache_info().currsize,n//2+k-1])
        print(f'n={n}: ad={k}, RF={depth}, visited_supports={rf.cache_info().currsize}',flush=True)
    with (HERE/'PARITY_BIPARTITE_DEPTHS.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['n','k','query_count','ordinary_depth','repair_safe_depth','finite_gap','independent_predicate_samples','visited_supports','proved_formula_depth']);w.writerows(rows)
    (HERE/'parity_bipartite_run.log').write_text('\n'.join(map(str,rows))+'\nCOMPLETE\n',encoding='utf-8')

if __name__=='__main__':main()
