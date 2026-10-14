"""Independent ProLT audit checks. No imports from supplied verifiers.
Run: python audit_checks.py
Requires Python >=3.10 and sympy for exact Smith normal forms.
All exhaustive posets use a fixed natural linear extension; isomorphism classes
can occur repeatedly, but no isomorphism type on the specified size is omitted.
"""
from __future__ import annotations
import itertools as it
import json, math, time
from pathlib import Path
from collections import deque

OUT=Path(__file__).resolve().parent

def dump(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2), encoding='utf-8')

def transitive(n, rel):
    return all((a,c) in rel for a,b in rel for b2,c in rel if b==b2)

def natural_posets(n, max_height=None):
    pairs=list(it.combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        r={pairs[i] for i in range(len(pairs)) if mask>>i&1}
        if not transitive(n,r): continue
        if max_height is not None:
            height=[0]*n
            for v in range(n):
                height[v]=max([height[u]+1 for u in range(v) if (u,v) in r]+[0])
            if max(height,default=0)>max_height: continue
        yield r

def thin(n, rel, labels):
    if len(labels)!=n: raise ValueError('one label is required per vertex')
    return {(a,b) for a,b in rel if labels[a]&~labels[b]==0}

def cells(n, rel, maxdim=None):
    ans=[[(v,) for v in range(n)]]
    while ans[-1] and (maxdim is None or len(ans)<=maxdim):
        nxt=[c+(v,) for c in ans[-1] for v in range(c[-1]+1,n)
             if all((u,v) in rel for u in c)]
        if not nxt: break
        ans.append(nxt)
    return ans

def matrix(rows, cols):
    ix={x:i for i,x in enumerate(rows)}
    out=[[0]*len(cols) for _ in rows]
    for j,c in enumerate(cols):
        for k in range(len(c)):
            face=c[:k]+c[k+1:]
            if face in ix: out[ix[face]][j]=(-1)**k
    return out

def rank_mod(a,p,ncols=None):
    if not a: return 0
    a=[[x%p for x in row] for row in a]
    m,n=len(a),len(a[0]); row=0
    for col in range(n):
        pivot=next((r for r in range(row,m) if a[r][col]),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        inv=pow(a[row][col],-1,p)
        a[row]=[(x*inv)%p for x in a[row]]
        for r in range(row+1,m):
            if a[r][col]:
                k=a[r][col]
                a[r]=[(x-k*y)%p for x,y in zip(a[r],a[row])]
        row+=1
        if row==m: break
    return row

def relative(n,p,q):
    pc,qc=cells(n,p),cells(n,q)
    deleted=[]
    for k, cc in enumerate(pc):
        kept=set(qc[k]) if k<len(qc) else set()
        deleted.append([c for c in cc if c not in kept])
    return deleted

def relative_betti(n,p,q,prime=2):
    d=relative(n,p,q)
    ranks=[0]+[rank_mod(matrix(d[k-1],d[k]),prime) for k in range(1,len(d))]+[0]
    return [len(d[k])-ranks[k]-ranks[k+1] for k in range(len(d))]

def beat_sequence(vertices,rel):
    alive=set(vertices); sequence=[]
    while len(alive)>1:
        chosen=None
        for v in sorted(alive):
            lo=[u for u in alive if (u,v) in rel]
            hi=[u for u in alive if (v,u) in rel]
            greatest=next((w for w in lo if all(u==w or (u,w) in rel for u in lo)),None)
            least=next((w for w in hi if all(u==w or (w,u) in rel for u in hi)),None)
            if greatest is not None: chosen=(v,'down',greatest);break
            if least is not None: chosen=(v,'up',least);break
        if chosen is None: break
        sequence.append(chosen);alive.remove(chosen[0])
    return sequence, sorted(alive)

def chromatic(n,edges):
    if n==0:return 0,[]
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    def solve(k):
        col=[-1]*n
        def dfs(done):
            if done==n:return col.copy()
            v=max((x for x in range(n) if col[x]<0),
                  key=lambda x:(len({col[y] for y in adj[x] if col[y]>=0}),len(adj[x])))
            forbidden={col[y] for y in adj[v]}
            used=max(col)+1
            for c in range(min(k,used+1)):
                if c not in forbidden:
                    col[v]=c
                    got=dfs(done+1)
                    if got is not None:return got
            col[v]=-1
            return None
        return dfs(0)
    for k in range(1,n+1):
        sol=solve(k)
        if sol is not None:return k,sol
    raise AssertionError

def dimension_conflicts(n,p,q):
    demands=sorted(p-q)
    edges=[]
    le=lambda x,y: x==y or (x,y) in q
    for i,(a,b) in enumerate(demands):
        for j in range(i+1,len(demands)):
            c,d=demands[j]
            if le(a,d) or le(c,b):edges.append((i,j))
    return demands,edges

def dimension_setcover(n,p,q):
    """Independent exact minimum cover by all Q-upsets, with bitmask DP."""
    demands=sorted(p-q)
    if not demands:return 0
    covers=[]
    for mask in range(1<<n):
        if any(mask>>a&1 and not(mask>>b&1) for a,b in q):continue
        covered=sum(1<<i for i,(a,b) in enumerate(demands)
                    if mask>>a&1 and not(mask>>b&1))
        if covered:covers.append(covered)
    target=(1<<len(demands))-1
    distance={0:0};queue=deque([0])
    while queue:
        mask=queue.popleft()
        if mask==target:return distance[mask]
        for cover in covers:
            nxt=mask|cover
            if nxt not in distance:distance[nxt]=distance[mask]+1;queue.append(nxt)
    raise AssertionError('universality failed')

def run_dimension():
    records=[]
    for n in range(1,5):
        count=0
        for p in natural_posets(n):
            pe=sorted(p)
            for mask in range(1<<len(pe)):
                q={pe[i] for i in range(len(pe)) if mask>>i&1}
                if not transitive(n,q):continue
                d,g=dimension_conflicts(n,p,q)
                a,_=chromatic(len(d),g);b=dimension_setcover(n,p,q)
                assert a==b,(n,p,q,a,b)
                count+=1
        records.append({'vertices':n,'pairs_P_Q':count})
    graphcount=0
    for n in range(1,6):
        pairs=list(it.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            g={pairs[i] for i in range(len(pairs)) if mask>>i&1}
            q={(i,n+j) for i,j in g}|{(j,n+i) for i,j in g}
            p=q|{(i,n+i) for i in range(n)}
            d,c=dimension_conflicts(2*n,p,q)
            assert c==sorted(g),(g,c,d)
            graphcount+=1
    ans={'exhaustive_pairs':records,'height_one_graph_reductions':graphcount,
         'counterexamples':[{'P':'two-element chain','Q':'same chain','odim':0,'classical_dim2':1},
                            {'P':'two-element chain','Q':'two-element antichain','odim':1,'classical_dim2':2}]}
    dump('dimension_checks.json',ans);print('dimension',ans,flush=True)

def forest_test(n,p,labels):
    q=thin(n,p,labels);d=relative(n,p,q)
    de=d[1] if len(d)>1 else[];dt=d[2] if len(d)>2 else[]
    b=matrix(de,dt)
    assert all(sum(x!=0 for x in col)<=2 for col in zip(*b))
    # Full signs: two nonzeros must be opposite; hence an oriented incidence matrix.
    for j in range(len(dt)):
        vals=[b[i][j] for i in range(len(de)) if b[i][j]]
        assert len(vals) in (1,2)
        if len(vals)==2:assert sum(vals)==0
    # Use a single extra root: roots from different coarse components can be
    # identified without changing cycle/rootless component counts.
    parent=list(range(len(de)+1));root=len(de)
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    cycles=0
    for j in range(len(dt)):
        incident=[i for i in range(len(de)) if b[i][j]]
        if len(incident)==1:incident.append(root)
        a,c=map(find,incident)
        if a==c:cycles+=1
        else:parent[a]=c
    rootless=len({find(i) for i in range(len(de)) if find(i)!=find(root)})
    for prime in (2,3,5):
        rank=rank_mod(b,prime)
        assert len(dt)-rank==cycles
        assert len(de)-rank==rootless
    return bool(de or dt),not(cycles or rootless)

def run_onebit():
    stats=[]
    for n in range(1,7):
        posets=cases=nonred=neutral_nonred=0
        exact2posets=exact2cases=exact2neutral_nonred=0
        for p in natural_posets(n,2):
            posets+=1
            is2=len(cells(n,p))==3
            exact2posets+=is2
            for labels in it.product(range(2),repeat=n):
                changed,neutral=forest_test(n,p,labels)
                cases+=1;nonred+=changed;neutral_nonred+=changed and neutral
                if is2:
                    exact2cases+=1;exact2neutral_nonred+=changed and neutral
        row={'n':n,'height_at_most_two_posets':posets,'cases':cases,
             'changed_cases':nonred,'neutral_changed_cases':neutral_nonred,
             'height_exactly_two_posets':exact2posets,'height_exactly_two_cases':exact2cases,
             'height_exactly_two_neutral_changed':exact2neutral_nonred}
        stats.append(row);print('onebit',row,flush=True)
    dump('onebit_exhaustive.json',stats)

def run_chain():
    records=[]
    for n in range(1,13):
        p=set(it.combinations(range(n),2));nonred=unsafe=missed=0
        for labels in it.product(range(2),repeat=n):
            q=thin(n,p,labels)
            monotone=all(labels[i]<=labels[i+1] for i in range(n-1))
            anti=all(labels[i]>=labels[i+1] for i in range(n-1)) and len(set(labels))==2
            seq,left=beat_sequence(range(n),q)
            # Unsafe case is exactly two nonempty chain components, not contractible.
            assert (len(left)==1)==(not anti),(n,labels,left)
            down=all(len(beat_sequence(range(v+1),q)[1])==1 for v in range(n))
            up=all(len(beat_sequence(range(v,n),q)[1])==1 for v in range(n))
            assert down==(labels[0]==0 or all(labels))
            assert up==(labels[-1]==1 or not any(labels))
            nonred+=not monotone;unsafe+=anti;missed+=(not anti and not down and not up)
        assert unsafe==n-1
        assert 2**n-nonred==n+1
        if n>=2:assert missed==2**(n-2)-(n-1)
        row={'n':n,'profiles':2**n,'redundant':n+1,'unsafe':unsafe,
             'neutral_nonredundant':nonred-unsafe,'neutral_missed_by_both_fibers':missed}
        records.append(row)
    dump('chain_checks.json',records);print('chains',records[-1],flush=True)

def matchings(b):
    n=len(b)
    if any(len(row)!=n for row in b):return []
    result=[]
    def dfs(remrows,used,current):
        if not remrows:result.append(current.copy());return
        r=min(remrows,key=lambda r:sum(b[r][j]!=0 and j not in used for j in range(n)))
        for j in range(n):
            if b[r][j] and j not in used:
                current[r]=j;dfs(remrows-{r},used|{j},current)
    dfs(set(range(n)),set(),{})
    return result

def acyclic_matching(b,matching):
    n=len(b);succ=[set() for _ in range(n)]
    for r,j in matching.items():
        succ[r]={s for s in range(n) if s!=r and b[s][j]}
    indeg=[sum(v in succ[u] for u in range(n)) for v in range(n)]
    queue=deque(i for i,x in enumerate(indeg) if x==0);count=0
    while queue:
        u=queue.popleft();count+=1
        for v in succ[u]:
            indeg[v]-=1
            if indeg[v]==0:queue.append(v)
    return count==n

def greedy_collapse(de,dt):
    remain_e=set(de);remain_t=set(dt);pairs=[]
    while remain_e:
        options=[]
        for e in sorted(remain_e):
            co=[t for t in remain_t if set(e)<=set(t)]
            if len(co)==1:options.append((e,co[0]))
        if not options:break
        e,t=options[0];pairs.append([e,t]);remain_e.remove(e);remain_t.remove(t)
    return pairs,not(remain_e or remain_t)

def example_record(name,n,p,labels):
    from sympy import Matrix,ZZ
    from sympy.matrices.normalforms import smith_normal_form
    assert transitive(n,p)
    q=thin(n,p,labels);d=relative(n,p,q)
    de=d[1] if len(d)>1 else[];dt=d[2] if len(d)>2 else[]
    b=matrix(de,dt);m=Matrix(b)
    snf=smith_normal_form(m,domain=ZZ)
    ms=matchings(b) if len(de)<=15 else None
    pairs,collapsed=greedy_collapse(de,dt)
    rec={'name':name,'n':n,'P_strict':sorted(p),'labels':labels,'Q_strict':sorted(q),
         'deleted_edges':de,'deleted_triangles':dt,'relative_matrix':b,
         'determinant':int(m.det()) if m.rows==m.cols else None,
         'smith_diagonal':[int(snf[i,i]) for i in range(min(snf.shape))],
         'relative_betti':{str(pr):relative_betti(n,p,q,pr) for pr in(2,3,5)},
         'perfect_matchings':ms,'acyclic_matchings':sum(acyclic_matching(b,x) for x in ms) if ms is not None else None,
         'collapse_succeeds':collapsed,'collapse_pairs':pairs,
         'P_beat_sequence':beat_sequence(range(n),p),'Q_beat_sequence':beat_sequence(range(n),q)}
    dump(name+'.json',rec)
    print('example',name,'det',rec['determinant'],'matchings',len(ms) if ms is not None else None,
          'acyclic',rec['acyclic_matchings'],flush=True)
    return rec

def run_named():
    p=set(it.combinations(range(3),2))
    rec=example_record('destructive_3',3,p,[1,2,1])
    assert rec['relative_betti']['2']==[0,1,0]
    p={(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)}
    rec=example_record('compensating_5',5,p,[3,0,1,2,3])
    assert abs(rec['determinant'])==1 and len(rec['perfect_matchings'])==1
    p={(0,2),(0,3),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),
       (2,5),(2,6),(2,7),(3,5),(3,6),(3,7),(4,5),(4,6)}
    rec=example_record('cyclic_8',8,p,[1,3,4,6,0,3,4,6])
    assert rec['determinant']==1 and len(rec['perfect_matchings'])==3 and rec['acyclic_matchings']==0
    assert len(rec['P_beat_sequence'][1])==len(rec['Q_beat_sequence'][1])==1

def tree_suborder(n,p,minima):
    edges=[(a,b) for a,b in sorted(p) if a in minima and b not in minima]
    parent=list(range(n));tree=set()
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for a,b in edges:
        x,y=find(a),find(b)
        if x!=y:parent[x]=y;tree.add((a,b))
    assert len(tree)==n-1
    return tree

def universal_labels(n,q):
    return [sum(1<<i for i in range(n) if i==v or (i,v) in q) for v in range(n)]

def torsion_record(name,n,p,q,expected,description):
    from sympy import Matrix,ZZ
    from sympy.matrices.normalforms import smith_normal_form
    labels=universal_labels(n,q)
    assert thin(n,p,labels)==q
    d=relative(n,p,q);b=matrix(d[1],d[2])
    m=Matrix(b)
    print('Smith start',name,m.shape,flush=True)
    snf=smith_normal_form(m,domain=ZZ)
    diag=[abs(int(snf[i,i])) for i in range(min(snf.shape))]
    assert len(d[1])==len(d[2]) and all(x==1 for x in diag[:-1]) and diag[-1]==expected,diag
    determinant=math.prod(diag)
    rec={'name':name,'construction':description,'n':n,'P_strict':sorted(p),'Q_strict':sorted(q),
         'labels_principal_Q_ideals':labels,'deleted_edges':d[1],'deleted_triangles':d[2],
         'matrix_shape':[m.rows,m.cols],'relative_matrix':b,'smith_diagonal_absolute':diag,
         'determinant_absolute':determinant,'relative_H1_torsion':[expected],
         'relative_betti':{str(pr):relative_betti(n,p,q,pr) for pr in(2,3,5)},
         'Q_beat_sequence':beat_sequence(range(n),q)}
    dump(name+'.json',rec)
    print('torsion',name,rec['matrix_shape'],expected,rec['relative_betti'],flush=True)

def run_torsion():
    # Face poset of the antipodal quotient of the octahedron boundary.
    edge_specs=[(0,1,s) for s in (1,-1)]+[(0,2,s) for s in (1,-1)]+[(1,2,s) for s in (1,-1)]
    p=set()
    edge_id={spec:3+i for i,spec in enumerate(edge_specs)}
    for spec,e in edge_id.items():
        a,b,s=spec;p.add((a,e));p.add((b,e))
    for i,(s,t) in enumerate(it.product((1,-1),repeat=2)):
        f=9+i
        for spec in ((0,1,s),(0,2,t),(1,2,s*t)):p.add((edge_id[spec],f))
        for v in range(3):p.add((v,f))
    assert transitive(13,p)
    q=tree_suborder(13,p,set(range(3)))
    torsion_record('torsion2_RP2_13',13,p,q,2,
      '13-element face poset of the regular CW antipodal octahedral quotient RP2; Q is a vertex-to-positive-cell spanning tree.')
    # Simplicial mapping cone of the degree-three map C9 -> C3.
    facets=[]
    for i in range(9):
        u=3+i;un=3+(i+1)%9;j=i%3;jn=(j+1)%3
        facets.extend([tuple(sorted(t)) for t in ((u,j,jn),(u,un,jn),(12,u,un))])
    allfaces=set()
    for f in facets:
        for size in range(1,4):allfaces.update(it.combinations(f,size))
    faces=sorted(allfaces,key=lambda x:(len(x),x));n=len(faces)
    p={(i,j) for i in range(n) for j in range(i+1,n) if set(faces[i])<set(faces[j])}
    minima={i for i,f in enumerate(faces) if len(f)==1}
    q=tree_suborder(n,p,minima)
    dump('torsion3_base_complex.json',{'facets':facets,'face_vector':[sum(len(f)==k for f in faces) for k in(1,2,3)],'faces':faces})
    torsion_record('torsion3_Moore_79',n,p,q,3,
      'Face poset of simplicial mapping cone of degree-three C9-to-C3 map, with 13 vertices, 39 edges, 27 triangles in the base; Q is a spanning tree.')

def run_block():
    summary=[]
    for n in range(1,5):
        count=neutral=destructive=unique=0
        for p in natural_posets(n,2):
            for labels in it.product(range(4),repeat=n):
                q=thin(n,p,labels);d=relative(n,p,q)
                de=d[1] if len(d)>1 else[];dt=d[2] if len(d)>2 else[]
                b=matrix(de,dt)
                good=len(de)==len(dt)==rank_mod(b,2)
                ms=matchings(b)
                if not de and not dt:ms=[{}]
                greedy=greedy_collapse(de,dt)[1]
                assert greedy==(len(ms)==1)
                assert greedy==(any(acyclic_matching(b,m) for m in ms))
                if good: assert greedy  # finite enumeration claim only
                single=[]
                for bit in (0,1):
                    qi=thin(n,p,[(x>>bit)&1 for x in labels])
                    single.append(not any(relative_betti(n,p,qi,2)))
                count+=1;neutral+=good;unique+=len(ms)==1
                destructive+=all(single) and not good
        row={'n':n,'cases':count,'F2_neutral':neutral,'unique_matching':unique,'destructive':destructive}
        summary.append(row);print('blocks',row,flush=True)
    dump('block_exhaustive.json',summary)

if __name__=='__main__':
    start=time.perf_counter()
    run_dimension();run_named();run_torsion();run_block();run_chain();run_onebit()
    dump('independent_run.json',{'seconds':round(time.perf_counter()-start,3),'status':'ALL_ASSERTIONS_PASSED'})
    print('ALL PASSED',time.perf_counter()-start,flush=True)
