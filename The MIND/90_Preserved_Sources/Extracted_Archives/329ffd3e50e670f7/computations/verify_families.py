"""Independent support-mask DP for explicit families; verifies both predicates.

This implementation keeps every ORIGINAL fixed-library query, with no query
complementing or synthesis; queried tests become constant automatically.
"""
import csv,json,math,time
from functools import lru_cache
from pathlib import Path
import repair_graph,boundary_matrix

HERE=Path(__file__).resolve().parent
INF=99

def solve_case(n,pairs,queries):
    checks=0
    @lru_cache(None)
    def details(S,q):
        nonlocal checks
        states=[i for i in range(n) if S>>i&1]
        rel=tuple((i,j) for i,a in enumerate(states) for j,b in enumerate(states) if (a,b) in pairs)
        qp=sum((q>>s&1)<<i for i,s in enumerate(states))
        ga=repair_graph.analyze(len(states),rel,qp)
        ma=boundary_matrix.analyze(len(states),rel,qp)
        assert ga[:3]==ma[:3]
        checks+=1
        return ga[0]
    @lru_cache(None)
    def solve(S,rf):
        size=S.bit_count()
        if size<=1:return 0
        best=INF;lower=(size-1).bit_length()
        for q in queries:
            T=S&q;U=S^T
            if not T or not U:continue
            if rf and not details(S,q):continue
            value=min(INF,1+max(solve(T,rf),solve(U,rf)))
            best=min(best,value)
            if best==lower:break
        return best
    def tree(S,rf):
        states=[i for i in range(n) if S>>i&1]
        if S.bit_count()<=1:return {'states':states}
        depth=solve(S,rf)
        if depth==INF:return {'states':states,'impossible':True}
        for q in queries:
            T=S&q;U=S^T
            if not T or not U or (rf and not details(S,q)):continue
            if 1+max(solve(T,rf),solve(U,rf))==depth:
                return {'states':states,'original_query_mask':q,'depth':depth,'outcome0':tree(U,rf),'outcome1':tree(T,rf)}
        raise AssertionError()
    full=(1<<n)-1
    ad=solve(full,False);rf=solve(full,True)
    result={'n':n,'pairs':pairs,'queries':queries,'ordinary_depth':ad,'repair_safe_depth':rf,'matrix_graph_checks':checks}
    if n<=6:result.update(ordinary_protocol=tree(full,False),repair_safe_protocol=tree(full,True))
    result['matrix_graph_checks']=checks
    return result

def main():
    results=[]
    for family in ('height1_star','exact_height2_suspension'):
        for n in range(3 if family=='exact_height2_suspension' else 2,13):
            k=(n-1).bit_length();full=(1<<n)-1
            if family=='height1_star':
                pairs=tuple((i,n-1) for i in range(n-1))
                codes=list(range(1,n))+[0]
            else:
                pairs=tuple([(0,i) for i in range(1,n)]+[(i,n-1) for i in range(1,n-1)])
                codes=[(1<<k)-1]+list(range(1,n-1))+[0]
            peels=[full^(1<<i) for i in range(n-1)]
            codequeries=[sum((code>>j&1)<<i for i,code in enumerate(codes)) for j in range(k)]
            queries=sorted(set(peels+codequeries))
            out=solve_case(n,pairs,queries)
            assert out['ordinary_depth']==k and out['repair_safe_depth']==n-1,out
            out.update(family=family,codes=codes,peel_queries=peels,code_queries=codequeries)
            results.append(out)
            print(f'{family} n={n}: ad={k} RF={n-1}, independent matrix/graph checks={out["matrix_graph_checks"]}',flush=True)
    cases=[('activation_n3',3,((0,1),),(1,2)),
           ('deactivation_n3',3,((0,1),(0,2),(1,2)),(2,6)),
           ('complement_closed_gap_n4',4,((0,1),(2,3)),(1,2,4,6,7,8,9,11,13,14)),
           ('minimal_library_gap_n4',4,((0,1),),(1,2,5)),
           ('minimal_complement_closed_gap_n4',4,((0,3),(1,2)),(4,5,7,8,10,11))]
    for name,n,pairs,queries in cases:
        out=solve_case(n,pairs,queries);out['family']=name;results.append(out)
    assert results[-1]['ordinary_depth']==2 and results[-1]['repair_safe_depth']==3
    for k in (2,3):
        n=1<<k;full=(1<<n)-1
        even=[x for x in range(n) if x.bit_count()%2==0]
        odd=[x for x in range(n) if x.bit_count()%2==1]
        codes=even+odd
        pairs=tuple((i,j) for i in range(n//2) for j in range(n//2,n))
        coords=[sum((code>>j&1)<<i for i,code in enumerate(codes)) for j in range(k)]
        base=coords+[1<<i for i in range(n)]
        queries=sorted(set(base+[full^q for q in base]))
        out=solve_case(n,pairs,queries)
        out.update(family='complement_closed_parity_bipartite',codes=codes)
        assert out['ordinary_depth']==k and out['repair_safe_depth']>=n//4+k
        results.append(out)
        print(f'complement_closed_parity_bipartite n={n}: ad={out["ordinary_depth"]} RF={out["repair_safe_depth"]}',flush=True)
    with (HERE/'STRUCTURED_FAMILY_DEPTHS.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['family','n','query_count','ordinary_depth','repair_safe_depth','finite_gap','matrix_graph_checks'])
        for r in results:w.writerow([r['family'],r['n'],len(r['queries']),r['ordinary_depth'],r['repair_safe_depth'],r['repair_safe_depth']-r['ordinary_depth'],r['matrix_graph_checks']])
    (HERE/'STRUCTURED_FAMILY_CERTIFICATES.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    (HERE/'family_run.log').write_text('\n'.join(f'{r["family"]}: n={r["n"]}, ad={r["ordinary_depth"]}, RF={r["repair_safe_depth"]}, matrix/graph checks={r["matrix_graph_checks"]}' for r in results)+'\nCOMPLETE; all asserted identities passed\n',encoding='utf-8')
    print('Family verification complete',flush=True)

if __name__=='__main__':main()
