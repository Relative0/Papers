from pathlib import Path
from itertools import combinations
from math import comb
from collections import Counter
import hashlib,json,time,sys
ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'convergence_followthrough_20260928'
def sha(data):return hashlib.sha256(data).hexdigest()
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2),encoding='utf-8')
def D(d,k):return sum(comb(d,j) for j in range(min(d,k)+1))
def subsets(coords,h):
    for j in range(min(len(coords),h)+1):
        for c in combinations(coords,j):yield sum(1<<v for v in c)
def rank(vectors):
    piv={}
    for x in vectors:
        while x:
            i=x.bit_length()-1
            if i not in piv:piv[i]=x;break
            x^=piv[i]
    return len(piv)
def actual_rank(U,W):
    basis=[];piv={}
    for a in U:
        x=a
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;basis.append(a);break
            x^=piv[j]
    return rank(sum(((a&b).bit_count()%2)<<i for i,b in enumerate(W)) for a in basis)
def selected(scope,rho):
    tests=[(len(scope)-1-i,rho[v]) for i,v in enumerate(scope) if v in rho]
    return [a for a in range(1<<len(scope)) if all((a>>j)&1==b for j,b in tests)]
def oracle(case,rho):
    # Independent exact enumeration over selected factor rows/columns, grouped only to reduce duplicate work.
    u=Counter(case['U'][i] for i in selected(case['left'],rho))
    w=Counter(case['W'][i] for i in selected(case['right'],rho))
    return sum(c*d for a,c in u.items() for b,d in w.items() if (a&b).bit_count()%2)
def payloads(c,k):
    p,q,r=c['p'],c['q'],c['r'];su=len(set(c['U'])-{0});sw=len(set(c['W'])-{0})
    dr=(2**r-1)*((p+1)*D(p,k)+(q+2)*D(q,k))
    dc=(2**r-1)*((q+1)*D(q,k)+(p+2)*D(p,k))
    sr=su*(r+(p+1)*D(p,k)+(q+2)*D(q,k))
    sc=sw*(r+(q+1)*D(q,k)+(p+2)*D(p,k))
    raw=r*((1<<p)+(1<<q))
    return dict(dense_row_bits=dr,dense_column_bits=dc,sparse_row_bits=sr,sparse_column_bits=sc,
                chosen_orientation='row' if sr<=sc else 'column',chosen_bits=min(sr,sc),raw_factor_bits=raw,
                row_support=su,column_support=sw,dense_favorable=dr<raw,sparse_row_favorable=sr<raw,
                adaptive_favorable=min(sr,sc)<raw)
def factor_bytes(c):
    # Canonical artifact-input identity, retaining explicit named cut and supplied width.
    return json.dumps({x:c[x] for x in ('n','p','q','r','left','right','U','W')},sort_keys=True,separators=(',',':')).encode()
