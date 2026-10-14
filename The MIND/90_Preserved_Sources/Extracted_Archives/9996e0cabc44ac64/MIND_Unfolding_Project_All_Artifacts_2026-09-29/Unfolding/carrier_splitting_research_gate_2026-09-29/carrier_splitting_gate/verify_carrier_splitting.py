from itertools import combinations, product
from collections import defaultdict, deque
import numpy as np

# Finite posets represented by <= boolean matrix with reflexive diagonal.

def natural_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    seen=set()
    for bits in range(1<<len(pairs)):
        le=[[False]*n for _ in range(n)]
        for i in range(n): le[i][i]=True
        for k,(i,j) in enumerate(pairs):
            if bits>>k & 1: le[i][j]=True
        # transitive closure
        for k in range(n):
            for i in range(n):
                if le[i][k]:
                    for j in range(n):
                        if le[k][j]: le[i][j]=True
        key=tuple(tuple(r) for r in le)
        if key not in seen:
            seen.add(key); yield le

def strict(le,i,j): return i!=j and le[i][j]

def chains(le):
    n=len(le)
    out=defaultdict(list)
    # recursive increasing chains under natural labels (valid since le respects labels)
    for i in range(n): out[0].append((i,))
    def extend(chain):
        last=chain[-1]
        for j in range(last+1,n):
            if strict(le,last,j):
                c=chain+(j,); out[len(c)-1].append(c); extend(c)
    for i in range(n): extend((i,))
    # deduplicate (recursion can only unique)
    return out

def gf2_rank(A):
    if not A: return 0
    A=[row[:] for row in A]
    m=len(A); n=len(A[0]) if m else 0
    r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]&1),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        for i in range(m):
            if i!=r and A[i][c]&1:
                A[i]=[(x^y) for x,y in zip(A[i],A[r])]
        r+=1
        if r==m: break
    return r

def boundary_mats(le):
    ch=chains(le)
    maxd=max(ch.keys(), default=0)
    mats={}
    for d in range(1,maxd+1):
        rows=ch[d-1]; cols=ch[d]
        ridx={c:i for i,c in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,c in enumerate(cols):
            for k in range(len(c)):
                f=c[:k]+c[k+1:]
                M[ridx[f]][j]^=1
        mats[d]=M
    return ch,mats

def betti(le):
    ch,m=boundary_mats(le)
    maxd=max(ch.keys(),default=0)
    b=[]
    for d in range(maxd+1):
        nd=len(ch[d]); rd=gf2_rank(m.get(d,[])) if d>=1 else 0
        rnext=gf2_rank(m.get(d+1,[])) if d+1 in m else 0
        b.append(nd-rd-rnext)
    while b and b[-1]==0: b.pop()
    return tuple(b)

def blowup(le, avail):
    # avail list entries 0:{0}, 1:{1}, 2:{0,1}
    verts=[]
    for s,a in enumerate(avail):
        if a in (0,2): verts.append((s,0))
        if a in (1,2): verts.append((s,1))
    idx={v:i for i,v in enumerate(verts)}
    N=len(verts)
    hat=[[False]*N for _ in range(N)]
    fine=[[False]*N for _ in range(N)]
    for i,x in enumerate(verts):
        for j,y in enumerate(verts):
            s,a=x; t,b=y
            if s==t:
                if a<=b:
                    hat[i][j]=fine[i][j]=True
            elif le[s][t]:
                hat[i][j]=True
                if a<=b: fine[i][j]=True
    return verts,hat,fine

def weighted_height(le,avail):
    C={i for i,a in enumerate(avail) if a==2}
    ch=chains(le)
    return max((d+sum(1 for x in c if x in C) for d,cs in ch.items() for c in cs), default=0)

def relative_betti(hat,fine):
    # same vertices and fine order subset; chain complexes relative over F2
    chH,mH=boundary_mats(hat); chL,_=boundary_mats(fine)
    maxd=max(chH.keys(),default=0)
    rel={d:[c for c in chH[d] if c not in set(chL.get(d,[]))] for d in range(maxd+1)}
    mats={}
    for d in range(1,maxd+1):
        rows=rel[d-1]; cols=rel[d]; ridx={c:i for i,c in enumerate(rows)}
        M=[[0]*len(cols) for _ in rows]
        for j,c in enumerate(cols):
            for k in range(len(c)):
                f=c[:k]+c[k+1:]
                if f in ridx: M[ridx[f]][j]^=1
        mats[d]=M
    b=[]
    for d in range(maxd+1):
        nd=len(rel[d]); rd=gf2_rank(mats.get(d,[])) if d>=1 else 0
        rnext=gf2_rank(mats.get(d+1,[])) if d+1 in mats else 0
        b.append(nd-rd-rnext)
    while b and b[-1]==0: b.pop()
    return tuple(b), rel, mats

def cone_betti_projection(le,avail):
    # normalized simplicial chain map fine->base over F2, build cone C_n(base) + C_{n-1}(fine)
    verts,hat,fine=blowup(le,avail)
    chB,mB=boundary_mats(le); chF,mF=boundary_mats(fine)
    maxd=max(max(chB.keys(),default=0),max(chF.keys(),default=0)+1)
    # map f_d from fine d-chains to base d-chains: image zero if repeated coarse vertex
    fmap={}
    for d,cs in chF.items():
        brow=chB.get(d,[]); bidx={c:i for i,c in enumerate(brow)}
        M=[[0]*len(cs) for _ in brow]
        for j,c in enumerate(cs):
            base=tuple(verts[v][0] for v in c)
            if len(set(base))<len(base): continue
            # base is strictly ordered chain
            if base in bidx: M[bidx[base]][j]=1
        fmap[d]=M
    # cone groups dims and differential from Cone_n=B_n + F_{n-1} to Cone_{n-1}=B_{n-1}+F_{n-2}
    dims={n:len(chB.get(n,[]))+len(chF.get(n-1,[])) for n in range(maxd+1)}
    dm={}
    for n in range(1,maxd+1):
        nb=len(chB.get(n,[])); nfprev=len(chF.get(n-1,[]))
        rb=len(chB.get(n-1,[])); rfprev=len(chF.get(n-2,[]))
        M=[[0]*(nb+nfprev) for _ in range(rb+rfprev)]
        # d_B
        MB=mB.get(n,[])
        for i in range(rb):
            for j in range(nb): M[i][j]=MB[i][j]
        # f_{n-1}: F_{n-1}->B_{n-1}
        FM=fmap.get(n-1,[])
        for i in range(rb):
            for j in range(nfprev):
                if FM: M[i][nb+j]^=FM[i][j]
        # d_F from F_{n-1}->F_{n-2}; sign irrelevant mod2
        MF=mF.get(n-1,[])
        for i in range(rfprev):
            for j in range(nfprev):
                if MF: M[rb+i][nb+j]^=MF[i][j]
        dm[n]=M
    b=[]
    for n in range(maxd+1):
        rn=gf2_rank(dm.get(n,[])) if n>=1 else 0
        rn1=gf2_rank(dm.get(n+1,[])) if n+1 in dm else 0
        b.append(dims[n]-rn-rn1)
    while b and b[-1]==0: b.pop()
    return tuple(b)

def graph_formula(hat, fine):
    chH,_=boundary_mats(hat); chL,_=boundary_mats(fine)
    E=[c for c in chH.get(1,[]) if c not in set(chL.get(1,[]))]
    T=[c for c in chH.get(2,[]) if c not in set(chL.get(2,[]))]
    # components of hat 1-skeleton
    n=len(hat); adj=[set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j and (hat[i][j] or hat[j][i]): adj[i].add(j)
    comp=[None]*n; cc=0
    for i in range(n):
        if comp[i] is not None: continue
        dq=[i]; comp[i]=cc
        while dq:
            x=dq.pop()
            for y in adj[x]:
                if comp[y] is None: comp[y]=cc; dq.append(y)
        cc+=1
    # graph vertices deleted edges + roots per component
    ev={e:i for i,e in enumerate(E)}
    root_offset=len(E); roots={c:root_offset+c for c in range(cc)}
    gadj=[[] for _ in range(len(E)+cc)]
    gedges=0
    for tri in T:
        faces=[tri[:k]+tri[k+1:] for k in range(3)]
        dels=[f for f in faces if f in ev]
        if len(dels)==1:
            u=ev[dels[0]]; r=roots[comp[tri[0]]]
            gadj[u].append(r); gadj[r].append(u); gedges+=1
        elif len(dels)==2:
            u,v=ev[dels[0]],ev[dels[1]]
            gadj[u].append(v); gadj[v].append(u); gedges+=1
        else:
            return None
    # graph components
    seen=set(); beta=0; c0=0
    rootset=set(roots.values())
    for i in range(len(gadj)):
        if i in seen: continue
        stack=[i]; seen.add(i); vs=[]; degsum=0
        while stack:
            x=stack.pop(); vs.append(x); degsum += len(gadj[x])
            for y in gadj[x]:
                if y not in seen: seen.add(y); stack.append(y)
        ecount=degsum//2
        beta += ecount-len(vs)+1
        if not any(v in rootset for v in vs): c0+=1
    return (0,c0,beta) # H0,H1,H2 ranks

def fmt(b): return ','.join(map(str,b)) if b else '0'

def main():
    total=0; checked_low=0; nontriv=[]; anchored_fail=[]; formula_fail=[]; cone_fail=[]; blow_fail=[]
    examples=[]
    for n in range(1,5):
        for le in natural_posets(n):
            for avail in product(range(3), repeat=n):
                total+=1
                verts,hat,fine=blowup(le,avail)
                if betti(hat)!=betti(le): blow_fail.append((n,le,avail,betti(le),betti(hat))); raise SystemExit('blowup fail')
                rb,_,_=relative_betti(hat,fine)
                cb=cone_betti_projection(le,avail)
                if rb!=cb:
                    cone_fail.append((n,avail,rb,cb)); raise SystemExit(f'cone fail {n} {avail} {rb} {cb}')
                if (all(a in (1,2) for a in avail) or all(a in (0,2) for a in avail)) and any(rb):
                    anchored_fail.append((n,avail,rb)); raise SystemExit('anchor fail')
                wh=weighted_height(le,avail)
                if wh<=2:
                    checked_low+=1
                    gf=graph_formula(hat,fine)
                    target=(rb+(0,0,0))[:3]
                    if gf is None or tuple(target)!=gf:
                        formula_fail.append((n,avail,wh,rb,gf)); raise SystemExit(f'graph fail {formula_fail[-1]}')
                if any(rb) and len(nontriv)<20:
                    nontriv.append((n,avail,wh,rb,betti(le),betti(fine)))
    print('EXHAUSTIVE n<=4 PASS')
    print('cases',total,'weighted-height<=2 cases',checked_low)
    print('nontrivial sample rows: n avail wh coneBetti baseBetti fineBetti')
    for row in nontriv[:12]: print(row)
    print('all tests passed')

if __name__=='__main__': main()
