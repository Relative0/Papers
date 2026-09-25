"""Independent XOR/AND Boolean linear algebra for the CM audit.

Matrices are tuples of packed Boolean rows (least-significant bit is column 0).
Only AND, XOR and parity enter state/operator calculations. Python integer
addition and multiplication below are for indices/shapes/counts, not scalars.
This file does not import any earlier CM implementation.
"""
from itertools import product
import numpy as np

def ident(n): return tuple(1 << i for i in range(n))
def bxor(a,b): return tuple(x ^ y for x,y in zip(a,b))
def trans(a,ncols):
    return tuple(sum(((r>>j)&1)<<i for i,r in enumerate(a)) for j in range(ncols))
def compose(a,b,ncols):
    cols=trans(b,ncols)
    return tuple(sum(((r&c).bit_count()&1)<<j for j,c in enumerate(cols)) for r in a)
def apply(a,v): return sum(((r&v).bit_count()&1)<<i for i,r in enumerate(a))
def rank(a):
    piv={}
    for r in a:
        while r:
            k=r.bit_length()-1
            if k in piv: r ^= piv[k]
            else: piv[k]=r;break
    return len(piv)
def invert(a):
    n=len(a); a=list(a); inv=list(ident(n))
    for c in range(n):
        p=next((i for i in range(c,n) if (a[i]>>c)&1),None)
        if p is None: return None
        a[c],a[p]=a[p],a[c];inv[c],inv[p]=inv[p],inv[c]
        for i in range(n):
            if i!=c and ((a[i]>>c)&1): a[i]^=a[c];inv[i]^=inv[c]
    assert tuple(a)==ident(n)
    return tuple(inv)
def kron(a,b,bcols):
    # Concatenate one AND-controlled copy of each B row per column of A.
    out=[]
    for ar in a:
        for br in b:
            r=0; p=ar
            while p:
                bit=p & -p;j=bit.bit_length()-1
                r ^= br << (j*bcols);p ^= bit
            out.append(r)
    return tuple(out)
def flatten(a,ncols): return sum(r<<(i*ncols) for i,r in enumerate(a))
def unflatten(v,nrows,ncols): return tuple((v>>(i*ncols))&((1<<ncols)-1) for i in range(nrows))
def block2(a,b,c,d):
    s=len(a)
    return tuple(x^(y<<s) for x,y in zip(a,b))+tuple(x^(y<<s) for x,y in zip(c,d))
def power(a,k):
    x=ident(len(a))
    for _ in range(k): x=compose(x,a,len(a))
    return x
def naive_compose(a,b,ncols):
    # A separate scalar implementation to detect packing/orientation bugs.
    out=[]
    for row in a:
        rr=0
        for j in range(ncols):
            bit=0
            for k in range(len(b)): bit ^= ((row>>k)&1)&((b[k]>>j)&1)
            rr |= bit << j
        out.append(rr)
    return tuple(out)
def batch_rank(rows,ncols):
    """Independent vectorized elimination for batches of packed row matrices."""
    a=np.array(rows,dtype=np.uint64,copy=True)
    if a.ndim!=2: raise ValueError('expected batch by row array')
    batch,nrows=a.shape; rr=np.zeros(batch,dtype=np.int64); idx=np.arange(batch)
    for col in range(ncols):
        admissible=(np.arange(nrows)[None,:]>=rr[:,None]) & (((a>>np.uint64(col))&np.uint64(1))!=0)
        ok=np.any(admissible,axis=1); bi=idx[ok]
        if not len(bi): continue
        pivot=np.argmax(admissible[ok],axis=1); r=rr[ok]
        old=a[bi,r].copy();a[bi,r]=a[bi,pivot];a[bi,pivot]=old
        prow=a[bi,r].copy()
        mask=(((a[bi]>>np.uint64(col))&np.uint64(1))!=0)
        mask[np.arange(len(bi)),r]=False
        a[bi] ^= np.where(mask,prow[:,None],np.uint64(0))
        rr[ok]+=1
    return rr

def batch_right_compose(rows,b,ncols):
    """Every batch row selects/XORs rows of fixed B; Boolean coefficients only."""
    rows=np.asarray(rows,dtype=np.uint64)
    out=np.zeros_like(rows)
    for k,br in enumerate(b):
        out ^= np.where(((rows>>np.uint64(k))&np.uint64(1))!=0,np.uint64(br),np.uint64(0))
    return out

def row_col_normal_form(a,ncols):
    """Return rank r and invertibles U,V with U A V = diag(I_r,0)."""
    a=list(a);m=len(a);u=list(ident(m));v=list(ident(ncols));r=0
    for k in range(min(m,ncols)):
        found=next(((i,j) for i in range(k,m) for j in range(k,ncols) if (a[i]>>j)&1),None)
        if found is None: break
        i,j=found
        a[k],a[i]=a[i],a[k];u[k],u[i]=u[i],u[k]
        if j!=k:
            for arr in (a,v):
                for z,x in enumerate(arr):
                    if ((x>>j)^(x>>k))&1: arr[z]=x^(1<<j)^(1<<k)
        for i in range(m):
            if i!=k and ((a[i]>>k)&1): a[i]^=a[k];u[i]^=u[k]
        # Kill other entries in pivot row by elementary column XORs.
        for j in range(ncols):
            if j!=k and ((a[k]>>j)&1):
                for arr in (a,v):
                    for z,x in enumerate(arr):
                        if (x>>k)&1: arr[z]=x^(1<<j)
        r+=1
    return r,tuple(u),tuple(v),tuple(a)
