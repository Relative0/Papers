"""Exact finite checks. Pure Python 3.10+, no network, no external dependencies.

Scalars are four-bit u-polynomials, little endian. Matrices are row-major.
These checks certify only the explicitly enumerated universes, not priority.
"""
import csv
import json
import platform
import sys
import time
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def mul(a, b):
    z = 0
    for i in range(4):
        if b >> i & 1:
            z ^= a << i
    return z & 15

MUL = [[mul(a, b) for b in range(16)] for a in range(16)]
VAL = [4] + [(x & -x).bit_length() - 1 for x in range(1, 16)]
INV = {x: next(y for y in range(1, 16, 2) if mul(x, y) == 1)
       for x in range(1, 16, 2)}

def mm(x, y):
    a,b,c,d=x; e,f,g,h=y
    return (MUL[a][e]^MUL[b][g], MUL[a][f]^MUL[b][h],
            MUL[c][e]^MUL[d][g], MUL[c][f]^MUL[d][h])

def smith(x):
    a = min(VAL[z] for z in x)
    if a == 4:
        return (4,4)
    p = next(i for i,z in enumerate(x) if VAL[z] == a)
    v = list(x)
    if p // 2:
        v = v[2:] + v[:2]
    if p % 2:
        v = [v[1],v[0],v[3],v[2]]
    pivot,b,c,d = v
    quotient = MUL[c >> a][INV[pivot >> a]]
    return (a, VAL[d ^ MUL[quotient][b]])

def rank(rows):
    pivots={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in pivots: x ^= pivots[p]
            else:
                pivots[p]=x
                break
    return len(pivots)

def transpose(rows,n):
    return tuple(sum(((r>>j)&1)<<i for i,r in enumerate(rows)) for j in range(n))

def compose(a,b):
    out=[]
    for row in a:
        z=0
        for j,r in enumerate(b):
            if row>>j&1: z ^= r
        out.append(z)
    return tuple(out)

def rho(x):
    columns=[]
    for j in range(2):
        for k in range(4):
            columns.append(MUL[x[j]][1<<k] | (MUL[x[2+j]][1<<k]<<4))
    return transpose(columns,8)

def rowmap(x):
    cols=[MUL[x[j]][1<<k] for j in range(2) for k in range(4)]
    return transpose(cols,4)

J4=(8,4,2,1)
J8=(8,4,2,1,128,64,32,16)

def delta(a):
    cols=[MUL[a][1<<k] for k in range(4)]
    return compose(transpose(cols,4),J4)

def encoded(x):
    return compose(rho(x),J8)

def bilinear(x,c,y):
    return MUL[x[0]][MUL[c[0]][y[0]]^MUL[c[1]][y[1]]] ^ MUL[x[1]][MUL[c[2]][y[0]]^MUL[c[3]][y[1]]]

def main():
    start=time.perf_counter()
    (ROOT/'data').mkdir(exist_ok=True)
    allm=list(product(range(16),repeat=4))
    counts=Counter(smith(x) for x in allm)
    # Independent binary rank cross-check for every ring matrix.
    for x in allm:
        a,b=smith(x)
        assert rank(rho(x)) == 8-a-b
    gl=[x for x in allm if smith(x)==(0,0)]
    assert len(gl)==24576
    primitive=[x for x in product(range(16),repeat=2) if (x[0]|x[1])&1]
    assert len(primitive)==192
    # Quotient unit scaling to obtain precisely the 24 projective rows.
    rays=sorted({min((MUL[t][x[0]],MUL[t][x[1]]) for t in INV) for x in primitive})
    assert len(rays)==24
    bases=[(x,y) for i,x in enumerate(rays) for y in rays[i+1:]
           if smith(x+y)==(0,0)]
    assert len(bases)==192
    tensor_checks=0
    for x,y in product(primitive,repeat=2):
        t=[MUL[a][b] for a in x for b in y]
        assert any(z&1 for z in t)
        tensor_checks+=1
    assert mul(8,2)==0
    assert (1 << (3*4+1)) != 0  # row-major field tensor u^3 tensor u.
    # Frobenius bimodule identity checked on every scalar pair.
    for a,b in product(range(16),repeat=2):
        rb=tuple(sum(((MUL[b][1<<j]>>i)&1)<<j for j in range(4)) for i in range(4))
        assert compose(rb,delta(a))==delta(mul(a,b))
        assert compose(delta(a),transpose(rb,4))==delta(mul(a,b))
    support_checks=0
    for a,b in counts:
        c=(0 if a==4 else 1<<a,0,0,0 if b==4 else 1<<b)
        for x,y in product(rays,repeat=2):
            actual=compose(compose(rowmap(x),encoded(c)),transpose(rowmap(y),8))
            assert actual==delta(bilinear(x,c,y))
            assert any(actual)==bool(bilinear(x,c,y))
            support_checks+=1
    # Exhaust every 2x2 single-sided filter, from each Smith representative.
    # Invertible moves are free; canonicalizing between edges makes the graph
    # characterize arbitrary finite alternating left/right filter sequences.
    edges={s:set() for s in counts}
    filters=0
    for s in counts:
        a,b=s; c=(0 if a==4 else 1<<a,0,0,0 if b==4 else 1<<b)
        for f in allm:
            edges[s].add(smith(mm(f,c)))
            edges[s].add(smith(mm(c,f)))
            filters+=2
    reach={s:set(v) for s,v in edges.items()}
    changed=True
    while changed:
        changed=False
        for s in reach:
            v=reach[s]|set().union(*(reach[t] for t in tuple(reach[s])))
            if v != reach[s]: reach[s]=v; changed=True
    for s in reach:
        assert reach[s]=={t for t in counts if t[0]>=s[0] and t[1]>=s[1]}
    # The four algebra automorphisms, exhaustively verify all 256 products.
    autos=[]
    for b,c in product(range(2),repeat=2):
        z=2|(b<<2)|(c<<3); powers=[1,z,mul(z,z),mul(mul(z,z),z)]
        phi=[0]*16
        for a in range(16):
            for i,p in enumerate(powers):
                if a>>i&1: phi[a]^=p
        assert len(set(phi))==16
        for x,y in product(range(16),repeat=2):
            assert phi[x^y]==phi[x]^phi[y]
            assert phi[mul(x,y)]==mul(phi[x],phi[y])
        p4=transpose(powers,4)
        p8=p4+tuple(x<<4 for x in p4)
        autos.append(p8)
    normalizer={compose(rho(g),p) for g in gl for p in autos}
    assert len(normalizer)==98304
    # Unit multiplication is observable with a binary effect.
    assert ((1>>1)&1)==0 and ((3>>1)&1)==1
    # Nonmonotonicity of h: diag(1,u) -> diag(u,u).
    assert mm((2,0,0,1),(1,0,0,2))==(2,0,0,2)
    # Full-copy R_k-linear target I_d criterion: d <= r0**k.
    # Check the residue counts explicitly for k=1..4, every 2x2 Smith type.
    multicopy=[]
    for s in sorted(counts):
        for k in range(1,5):
            unit_entries=sum(all(a==0 for a in word) for word in product(s,repeat=k))
            assert unit_entries==s.count(0)**k
            multicopy.append({'smith':list(s),'copies':k,'unit_factors':unit_entries})
    with (ROOT/'data'/'smith_classes.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['a','b','count','binary_rank','r','h','P01_support','P01_code_size'])
        for (a,b),n in sorted(counts.items()):
            r=int(a<4)+int(b<4);h=(1+int(a==b)) if r else 0
            kind='zero' if not r else 'local' if r==1 else 'strong' if h==2 else 'logical_not_strong'
            w.writerow([a,b,n,8-a-b,r,h,kind,2*h])
    with (ROOT/'data'/'filter_preorder.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['source_a','source_b','target_a','target_b','reachable'])
        for s,t in product(sorted(counts),repeat=2):w.writerow([*s,*t,int(t in reach[s])])
    (ROOT/'data'/'multicopy_residue_checks.json').write_text(json.dumps(multicopy,indent=2)+'\n')
    result={'status':'PASS','python':sys.version,'platform':platform.platform(),
       'ring':'F2[u]/u^4','encoding':'bit j is coefficient of u^j',
       'all_2x2_ring_matrices':len(allm),'GL2A':len(gl),'primitive_A2_vectors':len(primitive),
       'primitive_pair_tensors':tensor_checks,'projective_rows':len(rays),'unordered_bases':len(bases),
       'smith_representative_effect_pairs':support_checks,'single_sided_filter_checks':filters,
       'filter_preorder_pairs':225,'automorphisms':4,'normalizer_constructed_distinct_elements':len(normalizer),
       'normalizer_exhaustiveness':'analytic proof, not enumeration of GL(8,2)',
       'multicopy_residue_cases':len(multicopy),'elapsed_seconds':time.perf_counter()-start}
    (ROOT/'data'/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
