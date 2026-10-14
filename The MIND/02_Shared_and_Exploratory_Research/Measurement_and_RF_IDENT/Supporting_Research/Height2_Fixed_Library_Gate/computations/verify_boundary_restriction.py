"""Independent explicit-matrix audit of the induced-support restriction theorem.

No graph, boundary_matrix, or main-run functions are imported. Matrices retain
original edge/triangle labels, and rank is obtained by ROW elimination, whereas
boundary_matrix.py uses column elimination.
"""
import csv,json,time
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent

def orders(n):
    possible=list(combinations(range(n),2))
    for mask in range(1<<len(possible)):
        relation={e for i,e in enumerate(possible) if mask>>i&1}
        if any((x,y) in relation and (y,z) in relation and (x,z) not in relation
               for x,y,z in combinations(range(n),3)):continue
        if any(all(e in relation for e in zip(chain,chain[1:]))
               for chain in combinations(range(n),4)):continue
        yield relation

def explicit_matrix(relation,states,q):
    edges=tuple((a,b) for a,b in combinations(states,2)
                if (a,b) in relation and (q>>a&1)>(q>>b&1))
    triangles=tuple((a,b,c) for a,b,c in combinations(states,3)
                    if (a,b) in relation and (b,c) in relation and (a,c) in relation
                    and not((q>>a&1)<=(q>>b&1)<=(q>>c&1)))
    rows=tuple(tuple(int(set(edge).issubset(triangle)) for triangle in triangles)
               for edge in edges)
    return edges,triangles,rows

def rank_rows(rows):
    basis={}
    for row in rows:
        value=sum(bit<<j for j,bit in enumerate(row))
        while value:
            pivot=(value&-value).bit_length()-1
            if pivot not in basis:
                basis[pivot]=value;break
            value^=basis[pivot]
    return len(basis)

def main():
    start=time.time();results=[]
    for n in range(1,6):
        count=0;safeparents=0;queries=0;posets=0
        for relation in orders(n):
            posets+=1
            for q in range(1<<n):
                queries+=1
                e,t,B=explicit_matrix(relation,tuple(range(n)),q)
                rank=rank_rows(B);nullity=len(t)-rank
                parent_safe=(len(e)==len(t)==rank)
                for support in range(1,1<<n):
                    states=tuple(i for i in range(n) if support>>i&1)
                    eset=set(states)
                    ce,ct,C=explicit_matrix(relation,states,q)
                    I=[i for i,edge in enumerate(e) if set(edge)<=eset]
                    J=[j for j,triangle in enumerate(t) if set(triangle)<=eset]
                    assert ce==tuple(e[i] for i in I)
                    assert ct==tuple(t[j] for j in J)
                    assert C==tuple(tuple(B[i][j] for j in J) for i in I)
                    removed=set(range(len(e)))-set(I)
                    assert all(B[i][j]==0 for i in removed for j in J)
                    crank=rank_rows(C)
                    assert len(ct)-crank<=nullity
                    if parent_safe:
                        safeparents+=1
                        assert crank==len(ct)
                        assert (len(ce)==len(ct)==crank)==(len(ce)==len(ct))
                        assert len(ce)-crank==len(ce)-len(ct)
                    count+=1
        row={'n':n,'posets':posets,'parent_queries':queries,'nonempty_support_cases':count,
             'safe_parent_support_cases':safeparents,'failures':0}
        results.append(row);print(json.dumps(row),flush=True)
    payload={'results':results,'total_cases':sum(r['nonempty_support_cases'] for r in results),
             'total_safe_parent_cases':sum(r['safe_parent_support_cases'] for r in results),
             'elapsed_seconds':time.time()-start,'claims_checked':[
                 'exact retained-row retained-column submatrix',
                 'removed rows vanish on all retained columns',
                 'child kernel dimension at most parent kernel dimension',
                 'safe parent gives child full column rank',
                 'safe parent: child safe iff retained-edge count equals retained-triangle count',
                 'safe parent: child cokernel dimension equals retained edges minus retained triangles']}
    (HERE/'BOUNDARY_RESTRICTION_SUMMARY.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    with (HERE/'BOUNDARY_RESTRICTION_CHECKS.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    (HERE/'boundary_restriction_run.log').write_text('\n'.join(json.dumps(r) for r in results)+f'\nCOMPLETE: {payload["total_cases"]} cases; zero failures; {payload["elapsed_seconds"]:.3f} seconds\n',encoding='utf-8')

if __name__=='__main__':main()
