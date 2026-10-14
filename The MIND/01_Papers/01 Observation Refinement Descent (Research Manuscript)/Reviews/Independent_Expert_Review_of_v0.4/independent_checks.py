"""Independent constructions; no imports from project verifiers. Run with python -B.
Integral method: cancel unit chain entries, then SNF on disjoint residual
source/target supports. This is deliberately limited, and asserts that condition.
"""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json, sys, sympy
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent
def order(n, edges):
    le = [[i == j for j in range(n)] for i in range(n)]
    for i,j in edges: le[i][j] = True
    for k in range(n):
        for i in range(n):
            for j in range(n): le[i][j] |= le[i][k] and le[k][j]
    assert all(not le[j][i] for i in range(n) for j in range(i+1,n))
    return le

def chains(vertices, less):
    return [s for k in range(1,len(vertices)+1) for s in combinations(vertices,k)
            if all(less(a,b) for a,b in zip(s,s[1:]))]

def boundary(cells, augmented=False):
    keys=set(cells); d={s:{} for s in cells}
    for s in cells:
        for i in range(len(s)):
            t=s[:i]+s[i+1:]
            if t in keys: d[s][t]=(-1)**i
    for s in cells:
        dd=Counter()
        for t,a in d[s].items():
            for u,b in d[t].items(): dd[u]+=a*b
        assert not any(dd.values())
    return d

def integral(cells, d=None):
    d=boundary(cells) if d is None else {s:dict(col) for s,col in d.items()}
    original=len(cells); cancelled=0
    while True:
        pivot=next(((x,y,a) for x,col in d.items() for y,a in col.items() if abs(a)==1),None)
        if pivot is None: break
        x,y,a=pivot
        dx=dict(d[x])
        for z,col in d.items():
            if z in (x,y): continue
            c=col.get(y,0)
            if c:
                for w,b in dx.items():
                    col[w]=col.get(w,0)-c*b//a
                    if not col[w]: del col[w]
            col.pop(x,None); col.pop(y,None)
        del d[x]; del d[y]; cancelled+=1
    sources={s for s,col in d.items() if col}
    targets={t for col in d.values() for t in col}
    assert not sources & targets, 'Residual differential needs a more general kernel calculation'
    dims=Counter(len(s)-1 for s in d); ranks=Counter(); tors={}
    residual={}
    for n in sorted(dims):
        cols=[s for s in d if len(s)-1==n]
        rows=[s for s in d if len(s)-1==n-1]
        mat=Matrix([[d[s].get(t,0) for s in cols] for t in rows]) if rows and cols else Matrix.zeros(len(rows),len(cols))
        sm=smith_normal_form(mat,domain=ZZ)
        inv=[abs(int(sm[i,i])) for i in range(min(sm.shape)) if sm[i,i]]
        ranks[n]=len(inv); tors[n-1]=[a for a in inv if a>1]
        if inv: residual[n]=inv
    hom={n:{'free':v-ranks[n]-ranks[n+1],'torsion':tors.get(n,[])} for n,v in dims.items()}
    hom={n:g for n,g in sorted(hom.items()) if g['free'] or g['torsion']}
    return {'homology':hom,'cells':original,'unit_cancellations':cancelled,'residual_invariants':residual}

def model(n,edges,av):
    le=order(n,edges); vertices=list(range(2*n))
    less=lambda a,b: a!=b and le[a//2][b//2] and a%2<=b%2
    allcells=chains(vertices,less)
    missing={2*i+(0 if a==1 else 1) for i,a in enumerate(av) if a!=2}
    low={v for v in missing if v%2==0}; high=missing-low
    mixed=[s for s in allcells if set(s)&low and set(s)&high]
    pair=[s for s in allcells if set(s)&missing]
    cores=sorted({tuple(v for v in s if v in missing) for s in mixed},key=lambda s:(len(s),s))
    links={}
    for core in cores:
        vs=[v for v in vertices if v not in missing and all(less(v,w) or less(w,v) for w in core)]
        lc=[()]+chains(vs,less)
        links[core]=(lc,integral(lc))
    # Independently verify every missing-first orientation and every boundary entry.
    md=boundary(mixed)
    sign=lambda s: (-1)**sum(a not in missing and b in missing for i,a in enumerate(s) for b in s[i+1:])
    for s,col in md.items():
        c=tuple(v for v in s if v in missing); t=tuple(v for v in s if v not in missing)
        for f,coef in col.items():
            removed=next(v for v in s if v not in f)
            expected=(-1)**c.index(removed) if removed in missing else (-1)**(len(c)+t.index(removed))
            assert coef*sign(s)*sign(f)==expected
    out={'mixed':integral(mixed),'direct_pair':integral(pair),'links':{str(c):{'facets':[s for s in lc if not any(set(s)<set(t) for t in lc)],**r} for c,(lc,r) in links.items()},'orientation_identity':True}
    assert {k-1:v for k,v in out['mixed']['homology'].items()}==out['direct_pair']['homology']
    return out,links

def path_chain(path):
    out=Counter()
    for a,b in zip(path,path[1:]): out[tuple(sorted((a,b)))]+=1 if a<b else -1
    return dict(out)

def path_check(links,core,path):
    lc,_=links[core]; pc=path_chain(path); d=boundary(lc)
    bd=Counter()
    for e,a in pc.items():
        assert e in d
        for v,b in d[e].items(): bd[v]+=a*b
    assert {v:a for v,a in bd.items() if a}=={(path[-1],):1,(path[0],):-1}
    return pc

def main():
    results={'python':sys.version,'sympy':sympy.__version__,'method':'independent subset enumeration, signed unit cancellation, residual Smith form'}
    cases={
      'empty_graph':(1,[],[2]),
      'empty_coarse_link':(2,[(0,1)],[1,0]),
      'disconnected_matching':(4,[(0,1),(2,3)],[1,0,1,0]),
      'matching_disconnected_coarse_link':(4,[(0,1),(0,2),(1,3),(2,3)],[1,2,2,0]),
      'three_chain':(3,[(0,1),(1,2)],[1,0,0]),
      'disconnected_star_R':(3,[(0,1),(0,2)],[1,0,0]),
      'shared_middle_path':(4,[(0,1),(0,2),(1,3),(2,3)],[1,1,0,0]),
      'cycle6':(6,[(0,3),(0,5),(1,3),(1,4),(2,4),(2,5)],[1,1,1,0,0,0]),
      'star7':(7,[(0,1),(0,2),(1,3),(2,3),(2,5),(3,4),(3,6),(5,6)],[1,2,0,0,2,2,0]),
      'cycle4_8':(8,[(a,b) for a in (0,1) for b in range(2,8)]+[(2,5),(3,4),(3,5)]+[(a,b) for a in range(2,6) for b in (6,7)],[1,2,2,1,2,0,0,2])}
    saved={}
    for name,args in cases.items():
        results[name],saved[name]=model(*args)
    # C4 named paths: a=0,a'=1,v=2,b=3,w=4,x=5,y=6,y'=7.
    lk=saved['cycle4_8']
    paths={(0,6,11):[10,15,7],(0,6,13):[10,12,8,9,7],(0,11,13):[10,4,5,1,7],(6,11,13):[10,2,7]}
    pcs={c:path_check(lk,c,p) for c,p in paths.items()}
    target=Counter(pcs[(0,11,13)])
    for e,a in pcs[(0,6,13)].items(): target[e]-=a
    target={e:a for e,a in target.items() if a}
    lc,_=lk[(0,13)]; d=boundary(lc)
    # A formal extra 2-cell bounding the zigzag kills H1 without torsion iff primitive.
    formal=('formal', 'cell', 'd2'); d[formal]=target
    killed=integral(lc+[formal],d)
    assert killed['homology']=={}
    results['c4_explicit_paths']={'paths':{str(c):p for c,p in paths.items()},'target_cycle':str(target),'augmented_homology_after_attaching_target':killed}
    # Independently recover shortest paths in each star triple link, all from 2_0 to 0_1.
    lk=saved['star7']; sp={}
    for c,(lc,r) in lk.items():
        if len(c)!=3: continue
        queue=[[4]]; seen={4}
        for p in queue:
            if p[-1]==1: sp[c]=p; break
            for e in lc:
                if len(e)==2 and p[-1] in e:
                    w=next(v for v in e if v!=p[-1])
                    if w not in seen: seen.add(w); queue.append(p+[w])
        assert c in sp
    pc={c:path_check(lk,c,p) for c,p in sp.items()}
    # Core (0_0,2_1,3_1,6_1); deletion signs for triples 027,0213,0713 are -,+,-.
    c4=(0,5,7,13); signed={tuple(c4[:i]+c4[i+1:]):(-1)**i for i in (1,2,3)}
    targets={}
    for c,a in signed.items():
        for i in range(1,3):
            edge=c[:i]+c[i+1:]; target=targets.setdefault(edge,Counter())
            for e,b in pc[c].items(): target[e]+=a*((-1)**i)*b
    checks={}
    for edge,t in targets.items():
        lc,_=lk[edge]; d=boundary(lc); t={e:a for e,a in t.items() if a}
        formal=('formal','star','d2'); d[formal]=t
        checks[str(edge)]=integral(lc+[formal],d)
    assert any(r['homology']=={} for r in checks.values())
    results['star_explicit_paths']={'paths':{str(c):p for c,p in sp.items()},'targets':{str(c):str(dict(t)) for c,t in targets.items()},'target_attaching_checks':checks}
    facets=[(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),(1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
    faces=sorted({s for f in facets for k in (1,2,3) for s in combinations(f,k)},key=lambda s:(len(s),s))
    results['projective_plane_original_triangulation']=integral(faces)
    assert results['projective_plane_original_triangulation']['homology']=={0:{'free':1,'torsion':[]},1:{'free':0,'torsion':[2]}}
    (ROOT/'independent_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps({name:results[name]['direct_pair']['homology'] for name in cases},indent=2))
    print('C4 and star signed path fillings and primitivity passed; RP2 residual invariant is 2.')

if __name__=='__main__': main()
