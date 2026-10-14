#!/usr/bin/env python3
import itertools, json, os, sys
from collections import defaultdict

OUT=os.path.dirname(__file__)
N=4; W=tuple(range(N))
OBS=tuple(tuple((mask>>i)&1 for i in range(N)) for mask in range(1<<N))

def obs_rel(bits): return tuple(tuple((i==j) or bits[i]<=bits[j] for j in W) for i in W)
OBSREL=[obs_rel(b) for b in OBS]
def rel_inter(a,b): return tuple(tuple(a[i][j] and b[i][j] for j in W) for i in W)
def rel_key(r):
    z=p=0
    for i in W:
        for j in W:
            if r[i][j]: z|=1<<p
            p+=1
    return z

def rel_from_family(mask):
    r=tuple(tuple(True for j in W) for i in W)
    for k in range(16):
        if (mask>>k)&1: r=rel_inter(r,OBSREL[k])
    return r

def quotient(r):
    un=set(W); cs=[]
    while un:
        x=min(un); c=tuple(sorted(y for y in W if r[x][y] and r[y][x])); cs.append(c); un.difference_update(c)
    cs=tuple(sorted(cs,key=min)); idx={x:k for k,c in enumerate(cs) for x in c}
    m=len(cs); q=[[False]*m for _ in range(m)]
    for a,c in enumerate(cs):
        for b,d in enumerate(cs): q[a][b]=r[c[0]][d[0]]
    return cs,tuple(tuple(row) for row in q),idx

uniq={}
for fam in range(1<<16):
    r=rel_from_family(fam); uniq.setdefault(rel_key(r),fam)
PRE=[rel_from_family(uniq[k]) for k in sorted(uniq)]

# ---------- F2 linear algebra with bit vectors ----------
def pivot(v): return v.bit_length()-1

def make_basis(vectors):
    """Return pivot dict for span, vectors in row-echelon form."""
    B={}
    for v in vectors:
        x=v
        while x:
            p=pivot(x)
            if p in B: x ^= B[p]
            else:
                B[p]=x; break
    return B

def rank(vectors): return len(make_basis(vectors))

def nullspace_from_columns(cols, n_dom):
    """Kernel basis as bit vectors in domain; cols[j] is image bitvector."""
    P={} # target pivot -> (image, combination)
    ker=[]
    for j in range(n_dom):
        v=cols[j]; comb=1<<j
        while v:
            p=pivot(v)
            if p in P:
                v ^= P[p][0]; comb ^= P[p][1]
            else:
                P[p]=(v,comb); break
        if not v: ker.append(comb)
    return ker

def independent_extension(base_vectors, candidates):
    B=make_basis(base_vectors)
    chosen=[]
    for v in candidates:
        x=v
        while x:
            p=pivot(x)
            if p in B: x ^= B[p]
            else:
                B[p]=x; chosen.append(v); break
    return chosen

def coordinate_solver(vectors):
    """Independent vectors -> pivot dict (reduced enough) tracking combination indices; solve span coordinates."""
    P={}
    for j,v0 in enumerate(vectors):
        v=v0; comb=1<<j
        while v:
            p=pivot(v)
            if p in P:
                v ^= P[p][0]; comb ^= P[p][1]
            else:
                P[p]=(v,comb); break
        if not v: raise ValueError('dependent solver basis')
    def solve(x):
        comb=0; y=x
        while y:
            p=pivot(y)
            if p not in P: return None
            y ^= P[p][0]; comb ^= P[p][1]
        return comb
    return solve

def apply_map(cols, v):
    out=0; j=0; x=v
    while x:
        lsb=x & -x; j=lsb.bit_length()-1; out ^= cols[j]; x ^= lsb
    return out

# ---------- simplicial chain complexes ----------
def linear_extension(rel):
    n=len(rel); remaining=set(range(n)); out=[]
    while remaining:
        mins=[x for x in remaining if not any(y!=x and y in remaining and rel[y][x] for y in remaining)]
        if not mins: raise ValueError('cycle in poset')
        x=min(mins); out.append(x); remaining.remove(x)
    return out

def complex_from_poset(rel):
    n=len(rel); ext=linear_extension(rel); pos={v:i for i,v in enumerate(ext)}
    by=[]
    for k in range(1,n+1):
        sims=[]
        for sub in itertools.combinations(range(n),k):
            ok=True
            for a,b in itertools.combinations(sub,2):
                if not (rel[a][b] or rel[b][a]): ok=False; break
            if ok: sims.append(tuple(sorted(sub,key=lambda v:pos[v])))
        if not sims: break
        by.append(sims)
    idx=[{s:i for i,s in enumerate(sims)} for sims in by]
    dims=[len(s) for s in by]
    d=[]
    for k,sims in enumerate(by):
        if k==0: d.append([0]*len(sims)); continue
        cols=[]
        for s in sims:
            v=0
            for t in range(len(s)):
                face=s[:t]+s[t+1:]
                v ^= 1<<idx[k-1][face]
            cols.append(v)
        d.append(cols)
    return {'simplices':by,'index':idx,'dims':dims,'d':d}

def map_from_vertex_map(A,B,vmap):
    maxd=max(len(A['dims']),len(B['dims']))
    maps=[]
    for k in range(maxd):
        if k>=len(A['dims']): maps.append([]); continue
        cols=[]
        for s in A['simplices'][k]:
            im=[vmap[v] for v in s]
            if len(set(im))<len(im): cols.append(0); continue
            # monotone image order is inherited; find target simplex tuple as sorted by target linear ext via exact matching set
            target=None
            ims=set(im)
            for t in B['simplices'][k]:
                if set(t)==ims: target=t; break
            if target is None:
                raise ValueError(('image not simplex',s,im,k))
            cols.append(1<<B['index'][k][target])
        maps.append(cols)
    return maps

def compose_maps(f,g):
    # f:A->B, g:B->C, return g f
    out=[]
    for k in range(len(f)):
        if k>=len(g): out.append([0]*len(f[k])); continue
        out.append([apply_map(g[k],col) for col in f[k]])
    return out

def cone(A,B,f):
    # Cone(f)_n = B_n + A_{n-1}
    maxn=max(len(B['dims']),len(A['dims'])+1)
    dims=[]; d=[]
    def dim(C,k): return C['dims'][k] if 0<=k<len(C['dims']) else 0
    def dc(C,k): return C['d'][k] if 0<=k<len(C['d']) else []
    def fmap(k): return f[k] if 0<=k<len(f) else []
    for n in range(maxn): dims.append(dim(B,n)+dim(A,n-1))
    for n in range(maxn):
        target_dim = dims[n-1] if n-1>=0 else 0
        cols=[]
        # B_n basis
        for j in range(dim(B,n)):
            v = dc(B,n)[j] if n>0 else 0
            cols.append(v)  # first block target B_{n-1}
        # A_{n-1} basis -> f into B_{n-1}, plus dA into A_{n-2}
        offsetB=dim(B,n-1)
        for j in range(dim(A,n-1)):
            v = fmap(n-1)[j] if j < len(fmap(n-1)) else 0
            if n-1>0:
                v |= (dc(A,n-1)[j] << offsetB) # blocks disjoint; XOR same as OR
            cols.append(v)
        d.append(cols)
    return {'dims':dims,'d':d}

def homology_data(C):
    H=[]
    maxn=len(C['dims'])
    for n in range(maxn):
        dn=C['d'][n] if n<len(C['d']) else []
        ker=nullspace_from_columns(dn,C['dims'][n])
        bcols=C['d'][n+1] if n+1<len(C['d']) else []
        boundaries=independent_extension([],bcols)
        reps=independent_extension(boundaries,ker)
        solve=coordinate_solver(boundaries+reps) if boundaries or reps else (lambda x: 0 if x==0 else None)
        H.append({'ker':ker,'boundaries':boundaries,'reps':reps,'solve':solve,'bcount':len(boundaries),'dim':len(reps),'chain_dim':C['dims'][n]})
    return H

def induced_homology_map(HC,HD,chain_maps,deg_shift=0):
    # map source degree n -> target degree n+deg_shift. Return list maps cols Hsrc->Htgt
    out=[]
    for n,hs in enumerate(HC):
        m=n+deg_shift
        if m<0 or m>=len(HD): out.append([0]*hs['dim']); continue
        hd=HD[m]; cols=[]
        cmap=chain_maps[n] if 0<=n<len(chain_maps) else []
        for rep in hs['reps']:
            img=apply_map(cmap,rep)
            comb=hd['solve'](img)
            if comb is None:
                raise ValueError(('image not homology span',n,m,img))
            coords=comb >> hd['bcount']
            cols.append(coords)
        out.append(cols)
    return out

def map_rank(cols): return rank(cols)
def ker_dim(cols,n_dom): return len(nullspace_from_columns(cols,n_dom))
def composition_zero(a,b):
    # b after a
    return all(apply_map(b,col)==0 for col in a)

def check_exact(im_cols, next_cols, mid_dim):
    return composition_zero(im_cols,next_cols) and map_rank(im_cols)==ker_dim(next_cols,mid_dim)

# utility to make zero complex-ish maps dimensions
def alpha_maps(A,B,C,f,g,h,Cf,Ch):
    # Cone f -> Cone h : (b,a)->(g b,a)
    maps=[]
    for n,sd in enumerate(Cf['dims']):
        Bn=B['dims'][n] if n<len(B['dims']) else 0
        An1=A['dims'][n-1] if n-1>=0 and n-1<len(A['dims']) else 0
        Cn=C['dims'][n] if n<len(C['dims']) else 0
        cols=[]
        gn=g[n] if n<len(g) else []
        for j in range(Bn): cols.append(gn[j])
        for j in range(An1): cols.append(1<<(Cn+j))
        maps.append(cols)
    return maps

def beta_maps(A,B,C,f,g,h,Ch,Cg):
    # Cone h -> Cone g : (c,a)->(c,f a)
    maps=[]
    for n,sd in enumerate(Ch['dims']):
        Cn=C['dims'][n] if n<len(C['dims']) else 0
        An1=A['dims'][n-1] if n-1>=0 and n-1<len(A['dims']) else 0
        Bn1=B['dims'][n-1] if n-1>=0 and n-1<len(B['dims']) else 0
        cols=[]
        for j in range(Cn): cols.append(1<<j)
        fn1=f[n-1] if n-1>=0 and n-1<len(f) else []
        for j in range(An1): cols.append(fn1[j]<<Cn)
        maps.append(cols)
    return maps

def gamma_degree_lowering(B,C,g,Cg,Cf):
    # Cone g degree n -> Cone f degree n-1: (c,b)->(b,0)
    maps=[]
    for n,sd in enumerate(Cg['dims']):
        Cn=C['dims'][n] if n<len(C['dims']) else 0
        Bn1=B['dims'][n-1] if n-1>=0 and n-1<len(B['dims']) else 0
        cols=[0]*Cn
        for j in range(Bn1): cols.append(1<<j)
        maps.append(cols)
    return maps

fail=0; cases=0; exact_checks=0; relative_checks=0; postt0_cases=0
examples=[]
for pid,r0 in enumerate(PRE):
    C,P,cidx=quotient(r0)
    for om,bits in enumerate(OBS):
        r1=rel_inter(r0,OBSREL[om]); C2,Qactual,cidx2=quotient(r1)
        Bp=[tuple(sorted(set(bits[x] for x in c))) for c in C]
        pairs=tuple(sorted((p,a) for p,b in enumerate(Bp) for a in b)); pix={v:i for i,v in enumerate(pairs)}
        m=len(pairs)
        Frel=[[False]*m for _ in range(m)]; Qrel=[[False]*m for _ in range(m)]
        for i,(p,a) in enumerate(pairs):
            for j,(q,b) in enumerate(pairs):
                Frel[i][j]=(p==q and a<=b) or (p!=q and P[p][q])
                Qrel[i][j]=P[p][q] and a<=b
        Frel=tuple(tuple(x) for x in Frel); Qrel=tuple(tuple(x) for x in Qrel)
        A=complex_from_poset(Qrel); Bc=complex_from_poset(Frel); Cc=complex_from_poset(P)
        # vertex maps
        jmap=list(range(m)); pmap=[p for p,a in pairs]
        f=map_from_vertex_map(A,Bc,jmap); g=map_from_vertex_map(Bc,Cc,pmap); h=map_from_vertex_map(A,Cc,pmap)
        # composition equality
        comp=compose_maps(f,g)
        if any(comp[k]!=h[k] for k in range(len(A['dims']))):
            fail+=1;
            if len(examples)<10: examples.append({'pid':pid,'obs':om,'stage':'composition'})
            continue
        Cf=cone(A,Bc,f); Ch=cone(A,Cc,h); Cg=cone(Bc,Cc,g)
        HF=homology_data(Cf); HH=homology_data(Ch); HG=homology_data(Cg)
        am=alpha_maps(A,Bc,Cc,f,g,h,Cf,Ch); bm=beta_maps(A,Bc,Cc,f,g,h,Ch,Cg); gm=gamma_degree_lowering(Bc,Cc,g,Cg,Cf)
        aH=induced_homology_map(HF,HH,am,0); bH=induced_homology_map(HH,HG,bm,0); gH=induced_homology_map(HG,HF,gm,-1)
        # exact at HH_n and HG_n, and HF_{n-1}
        maxn=max(len(HF),len(HH),len(HG))
        ok=True
        for n in range(maxn):
            # at HH_n: im a_n = ker b_n
            ha=HF[n]['dim'] if n<len(HF) else 0; hh=HH[n]['dim'] if n<len(HH) else 0; hg=HG[n]['dim'] if n<len(HG) else 0
            aa=aH[n] if n<len(aH) else [0]*ha; bb=bH[n] if n<len(bH) else [0]*hh; gg=gH[n] if n<len(gH) else [0]*hg
            if not check_exact(aa,bb,hh): ok=False
            # at HG_n: im b_n = ker gamma_n
            if not check_exact(bb,gg,hg): ok=False
            # at HF_{n-1}: im gamma_n = ker a_{n-1}
            if n-1>=0:
                aa_prev=aH[n-1] if n-1<len(aH) else []
                targetdim=HF[n-1]['dim']
                if not check_exact(gg,aa_prev,targetdim): ok=False
            exact_checks+=3
        # relative homology check for inclusion j: dim H(Cone j)=dim H(F,Q)
        # Build relative chain complex dimensions using quotient chains: F simplices not in Q (since same vertices inclusion)
        # Differential mod Q by dropping faces lying in Q.
        qsets=[set(s) for s in A['simplices']]
        # easier key sets by dim
        rel={'dims':[],'d':[]}
        ridx=[]; rsims=[]
        for k,fs in enumerate(Bc['simplices']):
            qk=set(A['simplices'][k]) if k<len(A['simplices']) else set()
            r=[s for s in fs if s not in qk]; rsims.append(r); ridx.append({s:i for i,s in enumerate(r)}); rel['dims'].append(len(r))
        for k,r in enumerate(rsims):
            if k==0: rel['d'].append([0]*len(r)); continue
            qprev=set(A['simplices'][k-1]) if k-1<len(A['simplices']) else set()
            cols=[]
            for s in r:
                v=0
                for t in range(len(s)):
                    face=s[:t]+s[t+1:]
                    if face in qprev: continue
                    v ^= 1<<ridx[k-1][face]
                cols.append(v)
            rel['d'].append(cols)
        HR=homology_data(rel)
        for n in range(max(len(HF),len(HR))):
            if (HF[n]['dim'] if n<len(HF) else 0)!=(HR[n]['dim'] if n<len(HR) else 0): ok=False
            relative_checks+=1
        # post-T0 expansion cone acyclic and total=thin dimensions
        if all(len(c)==1 for c in C):
            postt0_cases+=1
            if any(hh['dim'] != hf['dim'] for hh,hf in itertools.zip_longest(HH,HF,fillvalue={'dim':0})): ok=False
            if any(x['dim'] for x in HG): ok=False
        if not ok:
            fail+=1
            if len(examples)<10: examples.append({'pid':pid,'obs':om,'pairs':pairs,'HF':[x['dim'] for x in HF],'HH':[x['dim'] for x in HH],'HG':[x['dim'] for x in HG]})
        cases+=1

summary={'cases':cases,'failures':fail,'exactness_checks':exact_checks,'relative_homology_dimension_checks':relative_checks,'postT0_cases':postt0_cases,'failure_examples':examples}
with open(os.path.join(OUT,'U4_OCTAHEDRAL_F2_SUMMARY.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
if fail: sys.exit(1)
