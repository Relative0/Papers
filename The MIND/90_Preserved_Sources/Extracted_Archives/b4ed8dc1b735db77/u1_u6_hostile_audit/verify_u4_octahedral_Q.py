#!/usr/bin/env python3
import itertools, json, os, sys
import sympy as sp
OUT=os.path.dirname(__file__)
N=4; W=tuple(range(N))
OBS=tuple(tuple((mask>>i)&1 for i in range(N)) for mask in range(1<<N))

def obs_rel(bits): return tuple(tuple((i==j) or bits[i]<=bits[j] for j in W) for i in W)
OBSREL=[obs_rel(b) for b in OBS]
def inter(a,b): return tuple(tuple(a[i][j] and b[i][j] for j in W) for i in W)
def key(r):
    z=p=0
    for i in W:
        for j in W:
            if r[i][j]: z|=1<<p
            p+=1
    return z

def relfam(mask):
    r=tuple(tuple(True for j in W) for i in W)
    for k in range(16):
        if (mask>>k)&1:r=inter(r,OBSREL[k])
    return r

def quot(r):
    un=set(W);cs=[]
    while un:
        x=min(un);c=tuple(sorted(y for y in W if r[x][y] and r[y][x]));cs.append(c);un.difference_update(c)
    cs=tuple(sorted(cs,key=min));idx={x:i for i,c in enumerate(cs) for x in c};m=len(cs)
    q=tuple(tuple(r[cs[i][0]][cs[j][0]] for j in range(m)) for i in range(m))
    return cs,q,idx
uniq={}
for fam in range(1<<16):
    r=relfam(fam);uniq.setdefault(key(r),fam)
PRE=[relfam(uniq[k]) for k in sorted(uniq)]

def linext(rel):
    rem=set(range(len(rel)));out=[]
    while rem:
        mins=[x for x in rem if not any(y!=x and y in rem and rel[y][x] for y in rem)]
        x=min(mins);out.append(x);rem.remove(x)
    return out

def cx(rel):
    n=len(rel); ex=linext(rel); pos={v:i for i,v in enumerate(ex)}; sims=[]
    for k in range(1,n+1):
        arr=[]
        for sub in itertools.combinations(range(n),k):
            if all(rel[a][b] or rel[b][a] for a,b in itertools.combinations(sub,2)):
                arr.append(tuple(sorted(sub,key=lambda v:pos[v])))
        if not arr: break
        sims.append(arr)
    idx=[{s:i for i,s in enumerate(a)} for a in sims]; dims=[len(a) for a in sims]; d=[]
    for k,a in enumerate(sims):
        if k==0: d.append(sp.zeros(0,dims[0]));continue
        M=sp.zeros(dims[k-1],dims[k])
        for j,s in enumerate(a):
            for t in range(len(s)):
                face=s[:t]+s[t+1:]; M[idx[k-1][face],j]+=(-1)**t
        d.append(M)
    return {'s':sims,'idx':idx,'dims':dims,'d':d}

def smap(A,B,vmap):
    maps=[]
    for k,a in enumerate(A['s']):
        M=sp.zeros(B['dims'][k] if k<len(B['dims']) else 0,A['dims'][k])
        if k>=len(B['dims']): maps.append(M);continue
        for j,s in enumerate(a):
            im=[vmap[v] for v in s]
            if len(set(im))<len(im): continue
            target=next(t for t in B['s'][k] if set(t)==set(im))
            # monotone map preserves chain order, so sign +1
            M[B['idx'][k][target],j]=1
        maps.append(M)
    return maps

def mapdeg(maps,k,rows,cols):
    return maps[k] if 0<=k<len(maps) else sp.zeros(rows,cols)

def cone(A,B,f):
    maxn=max(len(B['dims']),len(A['dims'])+1);dims=[];d=[]
    dim=lambda X,k: X['dims'][k] if 0<=k<len(X['dims']) else 0
    for n in range(maxn):dims.append(dim(B,n)+dim(A,n-1))
    for n in range(maxn):
        rows=dims[n-1] if n>0 else 0; cols=dims[n];M=sp.zeros(rows,cols)
        Bn=dim(B,n); Bm=dim(B,n-1); Am=dim(A,n-1); Amm=dim(A,n-2)
        if n>0 and Bn: M[:Bm,:Bn]=B['d'][n]
        if Am:
            ff=f[n-1] if n-1<len(f) else sp.zeros(Bm,Am)
            M[:Bm,Bn:Bn+Am]=ff
            if n-1>0: M[Bm:Bm+Amm,Bn:Bn+Am]=-A['d'][n-1]
        d.append(M)
    return {'dims':dims,'d':d}

def hom(C):
    H=[]
    for n,cn in enumerate(C['dims']):
        dn=C['d'][n]
        Z=dn.nullspace() if cn else []
        dnext=C['d'][n+1] if n+1<len(C['d']) else sp.zeros(cn,0)
        B=dnext.columnspace()
        reps=[]; current=B[:]
        r=sp.Matrix.hstack(*current).rank() if current else 0
        for z in Z:
            M=sp.Matrix.hstack(*(current+[z])) if current else z
            rr=M.rank()
            if rr>r: reps.append(z); current.append(z); r=rr
        basis=B+reps
        BM=sp.Matrix.hstack(*basis) if basis else sp.zeros(cn,0)
        H.append({'B':B,'H':reps,'basis':BM,'dim':len(reps),'b':len(B),'chain_dim':cn})
    return H

def induced(Hs,Ht,maps,shift=0):
    out=[]
    for n,hs in enumerate(Hs):
        m=n+shift
        if m<0 or m>=len(Ht): out.append(sp.zeros(0,hs['dim']));continue
        ht=Ht[m]; M=sp.zeros(ht['dim'],hs['dim'])
        cm=maps[n]
        for j,z in enumerate(hs['H']):
            y=cm*z
            if ht['basis'].cols==0:
                assert y==sp.zeros(y.rows,1);continue
            sol=ht['basis'].gauss_jordan_solve(y)[0]
            for i in range(ht['dim']):M[i,j]=sol[ht['b']+i,0]
        out.append(M)
    return out

def exact(A,B):
    # im A == ker B; middle dim = A.rows = B.cols
    if A.rows!=B.cols: return False
    if B*A != sp.zeros(B.rows,A.cols): return False
    return A.rank() == B.cols-B.rank()

def cone_maps(A,B,C,f,g,h,Cf,Ch,Cg):
    dim=lambda X,k: X['dims'][k] if 0<=k<len(X['dims']) else 0
    am=[];bm=[];gm=[]
    for n in range(len(Cf['dims'])):
        Bn=dim(B,n);An1=dim(A,n-1);Cn=dim(C,n)
        M=sp.zeros(dim(C,n)+An1,Bn+An1)
        if Bn: M[:Cn,:Bn]=g[n]
        if An1: M[Cn:,Bn:]=sp.eye(An1)
        am.append(M)
    for n in range(len(Ch['dims'])):
        Cn=dim(C,n);An1=dim(A,n-1);Bn1=dim(B,n-1)
        M=sp.zeros(Cn+Bn1,Cn+An1)
        if Cn:M[:Cn,:Cn]=sp.eye(Cn)
        if An1:M[Cn:,Cn:]=f[n-1]
        bm.append(M)
    for n in range(len(Cg['dims'])):
        Cn=dim(C,n);Bn1=dim(B,n-1)
        # target Cone f degree n-1 dim = B_{n-1}+A_{n-2}; only first B block
        tdim=Cf['dims'][n-1] if n-1>=0 else 0
        M=sp.zeros(tdim,Cn+Bn1)
        if Bn1:M[:Bn1,Cn:]=sp.eye(Bn1)
        gm.append(M)
    return am,bm,gm

fail=0; cases=0; checks=0
# Representative exact-rational census: all 355 coarse preorders x four observation masks.
OBS_SAMPLE={0,1,6,15}
for pid,r0 in enumerate(PRE):
    C,P,_=quot(r0)
    for om,bits in enumerate(OBS):
        if om not in OBS_SAMPLE: continue
        r1=inter(r0,OBSREL[om]); Bp=[tuple(sorted(set(bits[x] for x in c))) for c in C]
        pairs=tuple(sorted((p,a) for p,b in enumerate(Bp) for a in b));m=len(pairs)
        F=tuple(tuple((p==q and a<=b) or (p!=q and P[p][q]) for q,b in pairs) for p,a in pairs)
        Q=tuple(tuple(P[p][q] and a<=b for q,b in pairs) for p,a in pairs)
        A=cx(Q);B=cx(F);Cc=cx(P)
        f=smap(A,B,list(range(m)));g=smap(B,Cc,[p for p,a in pairs]);h=smap(A,Cc,[p for p,a in pairs])
        # composition on each source degree
        for k in range(len(A['dims'])):
            if g[k]*f[k] != h[k]: fail+=1
        Cf=cone(A,B,f);Ch=cone(A,Cc,h);Cg=cone(B,Cc,g)
        HF=hom(Cf);HH=hom(Ch);HG=hom(Cg)
        am,bm,gm=cone_maps(A,B,Cc,f,g,h,Cf,Ch,Cg)
        aH=induced(HF,HH,am);bH=induced(HH,HG,bm);gH=induced(HG,HF,gm,-1)
        maxn=max(len(HF),len(HH),len(HG))
        ok=True
        for n in range(maxn):
            ha=HF[n]['dim'] if n<len(HF) else 0;hh=HH[n]['dim'] if n<len(HH) else 0;hg=HG[n]['dim'] if n<len(HG) else 0
            aa=aH[n] if n<len(aH) else sp.zeros(hh,ha)
            bb=bH[n] if n<len(bH) else sp.zeros(hg,hh)
            gg=gH[n] if n<len(gH) else sp.zeros(0,hg)
            if not exact(aa,bb):ok=False
            if not exact(bb,gg):ok=False
            if n-1>=0:
                ap=aH[n-1] if n-1<len(aH) else sp.zeros(0,0)
                if not exact(gg,ap):ok=False
            checks+=3
        if not ok: fail+=1
        cases+=1

summary={'field':'Q','cases':cases,'exactness_checks':checks,'failures':fail}
open(os.path.join(OUT,'U4_OCTAHEDRAL_Q_SUMMARY.json'),'w').write(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
if fail:sys.exit(1)
