"""Exact finite checks; independent polynomial-basis implementation, stdlib only.

Integers 0..15 encode sum(bit_i*u**i), NOT the audit's rotation basis.
Run with Python 3.10+: python code/verify_process_semantics.py
No randomness, network, secret access, or imported historical kernels.
"""
from itertools import product, combinations
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

def mul(a, b):
    return ((a if b & 1 else 0) ^ (a << 1 if b & 2 else 0) ^
            (a << 2 if b & 4 else 0) ^ (a << 3 if b & 8 else 0)) & 15

MUL = [[mul(a,b) for b in range(16)] for a in range(16)]
UNITS = tuple(range(1,16,2))
VAL = [4] + [(a & -a).bit_length()-1 for a in range(1,16)]

def rank(rows):
    pivots = {}
    for x in rows:
        while x:
            k = x.bit_length()-1
            if k not in pivots:
                pivots[k] = x
                break
            x ^= pivots[k]
    return len(pivots)

def apply(rows, v):
    return sum(((r & v).bit_count() & 1) << i for i,r in enumerate(rows))

def transpose(rows, n):
    return tuple(sum(((r >> j) & 1) << i for i,r in enumerate(rows)) for j in range(n))

def compose(a,b):
    bt = transpose(b, len(a))
    return tuple(sum(((x & y).bit_count() & 1) << j for j,y in enumerate(bt)) for x in a)

def regular(a):
    return tuple(sum(((MUL[a][1 << j] >> i) & 1) << j for j in range(4)) for i in range(4))

REG = tuple(map(regular, range(16)))
J = (8,4,2,1)

def binary(m, frobenius=False):
    blocks = [REG[a] for a in m]
    if frobenius:
        blocks = [compose(b,J) for b in blocks]
    return tuple(blocks[2*i][k] | (blocks[2*i+1][k] << 4) for i in range(2) for k in range(4))

def matmul(a,b):
    return tuple(MUL[a[2*i]][b[j]] ^ MUL[a[2*i+1]][b[2+j]] for i in range(2) for j in range(2))

def determinant(a):
    return MUL[a[0]][a[3]] ^ MUL[a[1]][a[2]]

def scalar(a, m):
    return tuple(MUL[a][x] for x in m)

def diag(a,b):
    return (1 << a if a < 4 else 0,0,0,1 << b if b < 4 else 0)

TYPES = tuple((a,b) for a in range(5) for b in range(a,5))
PROFILE = {tuple(max(4-a-t,0)+max(4-b-t,0) for t in range(4)):(a,b) for a,b in TYPES}

def smith(m):
    # Independent from pivot elimination: dimensions of u^t times the image.
    return PROFILE[tuple(rank(binary(scalar(1 << t,m))) for t in range(4))]

def smith_pivot(m):
    a = min(VAL[x] for x in m)
    if a == 4:
        return (4,4)
    # Move a least-valuation entry to top left, then eliminate below it.
    x = list(m)
    at = next(i for i,v in enumerate(x) if VAL[v] == a)
    if at >= 2:
        x = x[2:] + x[:2]
        at -= 2
    if at == 1:
        x = [x[1],x[0],x[3],x[2]]
    q = next(q for q in range(16) if MUL[q][x[0]] == x[2])
    return (a, VAL[x[3] ^ MUL[q][x[1]]])

def effect_value(x,m,y):
    return MUL[MUL[x[0]][m[0]] ^ MUL[x[1]][m[2]]][y[0]] ^ MUL[MUL[x[0]][m[1]] ^ MUL[x[1]][m[3]]][y[1]]

def canonical_ray(x):
    return min((MUL[c][x[0]],MUL[c][x[1]]) for c in UNITS)

def ray_space(x):
    return frozenset(MUL[a][x[0]] | (MUL[a][x[1]] << 4) for a in range(16))

def automorphism(a,c,d):
    z = 2 | (c << 2) | (d << 3)
    powers = (1,z,MUL[z][z],MUL[MUL[z][z]][z])
    out = 0
    for i,p in enumerate(powers):
        if a >> i & 1:
            out ^= p
    return out

def run():
    started = time.time()
    (ROOT/'data').mkdir(exist_ok=True, parents=True)
    matrices = list(product(range(16),repeat=4))
    gates = [m for m in matrices if determinant(m) & 1]
    rays = sorted({canonical_ray((x,y)) for x,y in product(range(16),repeat=2) if (x|y)&1})
    bases = [p for p in combinations(rays,2) if determinant(p[0]+p[1]) & 1]
    counts = Counter()
    lookup = {}
    for m in matrices:
        s = smith(m)
        assert s == smith_pivot(m)
        assert rank(binary(m,True)) == 8-s[0]-s[1]
        counts[s] += 1
        lookup[m] = s
    assert len(gates)==24576 and len(rays)==24 and len(bases)==192
    # Balanced tensors, primitive products, and independent literal tensors.
    primitive = [(x,y) for x,y in product(range(16),repeat=2) if (x|y)&1]
    for x in primitive:
        for y in primitive:
            assert any(MUL[a][b]&1 for a in x for b in y)
    assert MUL[8][2] == 0
    assert 8 != 0 and 2 != 0
    # v=(1,u^3) is primitive; selecting coordinate 1 produces u^3.
    # Tensor with quotient A/(u) erases that outcome before conditioning.
    assert (8 & 1) == 0
    # Product of two primitive local vectors still loses jointly possible events.
    assert MUL[8][2] == 0  # branches of (1,u^3) and (1,u)
    # Explicit Frobenius contraction: four binary covectors per coarse effect.
    support_checks = 0
    for a,b in TYPES[:-1]:
        m=diag(a,b)
        phi=binary(m,True)
        for x in rays:
            erows=tuple(REG[x[0]][i] | (REG[x[1]][i]<<4) for i in range(4))
            for y in rays:
                frows=tuple(REG[y[0]][i] | (REG[y[1]][i]<<4) for i in range(4))
                blocks=[]
                for e in erows:
                    row=0
                    for k in range(8):
                        if e >> k & 1: row ^= phi[k]
                    blocks.append(sum(((row & f).bit_count()&1)<<j for j,f in enumerate(frows)))
                z=effect_value(x,m,y)
                assert tuple(blocks)==compose(REG[z],J)
                support_checks += 1
    # All one-sided filters on every Smith representative. The predicted
    # downsets are closed under a second side, so this also checks all types
    # achievable by arbitrary finite sequences of left/right filters.
    transitions=[]
    for s in TYPES:
        dest=Counter(lookup[matmul(l,diag(*s))] for l in matrices)
        expected={t for t in TYPES if all(y>=x for x,y in zip(s,t))}
        assert set(dest)==expected
        transitions.extend({'source':str(s),'target':str(t),'left_filters':n} for t,n in sorted(dest.items()))
    # Normalizer: enumerate GL2(A) times the four explicit ring automorphisms.
    normalizer=set()
    for c,d in product(range(2),repeat=2):
        cols=[automorphism(1<<i,c,d) for i in range(4)]
        f=transpose(cols,4)
        sigma=tuple(f)+tuple(x<<4 for x in f)
        for g in gates:
            normalizer.add(compose(binary(g),sigma))
    assert len(normalizer)==98304
    # Verify generator invariance on every ray and context; proof gives upper bound.
    generators=[(0,1,1,0)] + [(1,z,0,1) for z in (1,2,4,8)] + [(c,0,0,1) for c in UNITS]
    bin_generators=[binary(g) for g in generators]
    for c,d in ((1,0),(0,1)):
        f=transpose([automorphism(1<<i,c,d) for i in range(4)],4)
        bin_generators.append(tuple(f)+tuple(x<<4 for x in f))
    spaces={ray_space(x):x for x in rays}
    context_set={frozenset(p) for p in bases}
    for g in bin_generators:
        perm={x:spaces[frozenset(apply(g,v) for v in ray_space(x))] for x in rays}
        assert len(set(perm.values()))==24
        assert {frozenset(perm[x] for x in p) for p in bases}==context_set
    # Codebook count with A-linear encoders, arbitrary complete binary decoder.
    class_rows=[]
    for s in TYPES:
        m=diag(*s)
        span_rank=rank(sum(x << (4*i) for i,x in enumerate(matmul(g,m))) for g in gates)
        br=8-s[0]-s[1]
        assert span_rank==2*br
        h=0 if s==(4,4) else sum(x==s[0] for x in s)
        r=sum(x<4 for x in s)
        cls='zero' if not r else 'local' if r==1 else 'strong' if h>=2 else 'logical-not-strong'
        class_rows.append({'a':s[0],'b':s[1],'matrix_count':counts[s],'binary_rank':br,'smith_rank':r,'leading_multiplicity':h,'P01_support':cls,'P01_code_size':2*h,'lift_restricted_encoder_binary_decoder_size':span_rank,'lift_full_binary_code_size':8*br,'universal_8D_transfer':br==8})
    # Contextuality/leading multiplicity need not decrease under filters.
    assert matmul((2,0,0,1),diag(0,1)) == diag(1,1)
    # Unit multiplication is invisible to coarse ring outcomes, but not field effects.
    assert mul(3,1)==3 and ((1>>1)&1)==0 and ((3>>1)&1)==1
    for name,rows in [('smith_classes.csv',class_rows),('filter_transitions.csv',transitions)]:
        with (ROOT/'data'/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    result={'status':'PASS','matrix_universe':65536,'smith_classes_including_zero':15,'nonzero_smith_classes':14,'primitive_vectors_A2':len(primitive),'primitive_tensor_pairs':len(primitive)**2,'GL2A':len(gates),'projective_rays':len(rays),'unordered_complete_projective_bases':len(bases),'frobenius_coarse_support_checks':support_checks,'one_sided_filter_cases':len(TYPES)*len(matrices),'normalizer_constructed_distinct_elements':len(normalizer),'normalizer_upper_bound':'analytic pointwise-stabilizer proof; no exhaustive GL(8,2) scan','normalizer_generator_context_checks':len(bin_generators)*len(bases),'codebook_orbit_vectors_scanned':len(TYPES)*len(gates),'seconds':round(time.time()-started,3),'python':sys.version,'platform':platform.platform(),'inputs':{'field':2,'nilpotency':4,'encoding':'polynomial basis (1,u,u^2,u^3)','matrices':'all four-tuples in range(16)^4','randomness':'none'},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'data'/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    run()
