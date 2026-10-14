#!/usr/bin/env python3
"""Independent cross-check for the CM measurement audit.

This file intentionally does not import cm_measurement_compute.py.  It uses a
separate integer/bit implementation and asserts the reported classifications.
"""
from itertools import product
from pathlib import Path
import json

OUT = Path('/mnt/data/cm_measurement_audit')
checks = 0

def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)

# Bit 3,2,1,0 correspond to truth positions 11,10,01,00.
NAMES = [
    'FALSE','AND','X_AND_NOT_Y','NOT_X_AND_Y','NOR','X','Y','XOR',
    'XNOR','NOT_Y','NOT_X','X_IMPLIES_Y','Y_IMPLIES_X','OR','NAND','TRUE'
]
B = {
    'FALSE':0b0000,'AND':0b1000,'X_AND_NOT_Y':0b0100,'NOT_X_AND_Y':0b0010,
    'NOR':0b0001,'X':0b1100,'Y':0b1010,'XOR':0b0110,'XNOR':0b1001,
    'NOT_Y':0b0101,'NOT_X':0b0011,'X_IMPLIES_Y':0b1011,
    'Y_IMPLIES_X':0b1101,'OR':0b1110,'NAND':0b0111,'TRUE':0b1111,
}
INV = {v:k for k,v in B.items()}
ck(len(B)==16 and len(set(B.values()))==16, '16 truth functions not bijective')
ck(set(B.values())==set(range(16)), 'not all sixteen four-bit tables present')

def entries(z):
    return ((z>>3)&1,(z>>2)&1,(z>>1)&1,z&1)

def m(z):
    a,b,c,d=entries(z)
    return ((a,b),(c,d))

def enc(A):
    return (A[0][0]<<3)|(A[0][1]<<2)|(A[1][0]<<1)|A[1][1]

def f2(A,C):
    return tuple(tuple((A[i][0]*C[0][j]^A[i][1]*C[1][j]) for j in range(2)) for i in range(2))

def boo(A,C):
    return tuple(tuple(int((A[i][0]&C[0][j])|(A[i][1]&C[1][j])) for j in range(2)) for i in range(2))

def integer(A,C):
    return tuple(tuple(A[i][0]*C[0][j]+A[i][1]*C[1][j] for j in range(2)) for i in range(2))

def cyc(z,w):
    # convert bit order 11,10,01,00 to cycle coefficient order 11,10,00,01
    a=entries(z); b=entries(w)
    x=(a[0],a[1],a[3],a[2]); y=(b[0],b[1],b[3],b[2])
    q=[0]*4
    for i in range(4):
        for j in range(4):
            q[(i+j)&3] ^= x[i]&y[j]
    # back to 11,10,01,00
    return (q[0]<<3)|(q[1]<<2)|(q[3]<<1)|q[2]

# Idempotent lists.
idem_f2=[INV[z] for z in range(16) if f2(m(z),m(z))==m(z)]
idem_bool=[INV[z] for z in range(16) if boo(m(z),m(z))==m(z)]
idem_int=[INV[z] for z in range(16) if integer(m(z),m(z))==m(z)]
idem_cyc=[INV[z] for z in range(16) if cyc(z,z)==z]
expected_f2=['FALSE','AND','NOR','X','Y','XNOR','NOT_Y','NOT_X']
expected_bool=expected_f2+['X_IMPLIES_Y','Y_IMPLIES_X','TRUE']
expected_cyc=['FALSE','AND']
ck(set(idem_f2)==set(expected_f2), f'F2 idempotents {idem_f2}')
ck(set(idem_int)==set(expected_f2), f'integer idempotents {idem_int}')
ck(set(idem_bool)==set(expected_bool), f'Boolean-semiring idempotents {idem_bool}')
ck(set(idem_cyc)==set(expected_cyc), f'cyclic idempotents {idem_cyc}')

# Sequential pair counts and commutation counts independently.
def stats(names,law):
    comm=idemprod=0
    for a in names:
        for b in names:
            A=m(B[a]); C=m(B[b])
            if law=='f2':
                AC=f2(A,C); CA=f2(C,A); sq=f2(AC,AC)
            elif law=='bool':
                AC=boo(A,C); CA=boo(C,A); sq=boo(AC,AC)
            elif law=='int':
                AC=integer(A,C); CA=integer(C,A); sq=integer(AC,AC)
            else:
                za=cyc(B[a],B[b]); zc=cyc(B[b],B[a]);
                comm += (za==zc); idemprod += (cyc(za,za)==za); continue
            comm += (AC==CA); idemprod += (sq==AC)
    return len(names)**2,comm,idemprod
ck(stats(idem_f2,'f2')==(64,40,58), 'F2 sequential stats')
ck(stats(idem_bool,'bool')==(121,65,115), 'Boolean sequential stats')
ck(stats(idem_int,'int')==(64,36,54), 'integer sequential stats')
ck(stats(idem_cyc,'cyc')==(4,4,4), 'cyclic sequential stats')

# Thesis projector-definition counterexample: |1><0| = E_12 is nilpotent, not idempotent.
E12=((0,1),(0,0))
ck(f2(E12,E12)==((0,0),(0,0)), '|1><0| should square to zero over F2')
ck(integer(E12,E12)==((0,0),(0,0)), '|1><0| should square to zero ordinarily')
ck(E12!=((0,0),(0,0)), 'counterexample must be nonzero')

# Diagonal truth effects: all 16 sharp projectors, all sequential products commute and are intersection.
for z in range(16):
    e=entries(z)
    # diagonal idempotence is entrywise b^2=b
    ck(all(x*x==x for x in e), f'diagonal effect {z} not idempotent')
for z in range(16):
    for w in range(16):
        ez=entries(z); ew=entries(w)
        zw=tuple(a*b for a,b in zip(ez,ew))
        wz=tuple(b*a for a,b in zip(ez,ew))
        ck(zw==wz, 'diagonal effects do not commute')
        ck(zw==tuple(a&b for a,b in zip(ez,ew)), 'diagonal sequence not intersection')

# D4 stabilizers by all swaps/flips of the square.
cells=[(1,1),(1,0),(0,1),(0,0)]
pos={c:i for i,c in enumerate(cells)}
perms=[]
for sw,fx,fy in product((0,1),repeat=3):
    p=[]
    for x,y in cells:
        if sw: x,y=y,x
        if fx: x=1-x
        if fy: y=1-y
        p.append(pos[(x,y)])
    if p not in perms: perms.append(p)
ck(len(perms)==8,'D4 generation')

def apply(z,p):
    e=entries(z); out=[0]*4
    for i,a in enumerate(e):
        if a: out[p[i]]=1
    return (out[0]<<3)|(out[1]<<2)|(out[2]<<1)|out[3]

def stab(z): return sum(apply(z,p)==z for p in perms)
SWAP=[0,2,1,3]
ck(sum(apply(z,SWAP)==z for z in range(16))==8, 'transpose symmetry count')
inc=dec=same=0
inc_example=dec_example=same_example=None
for s in range(16):
    for e in range(16):
        t=s&e
        if t!=s and t!=0:
            d=stab(t)-stab(s)
            if d>0:
                inc+=1; inc_example=inc_example or (INV[s],INV[e],INV[t],stab(s),stab(t))
            elif d<0:
                dec+=1; dec_example=dec_example or (INV[s],INV[e],INV[t],stab(s),stab(t))
            else:
                same+=1; same_example=same_example or (INV[s],INV[e],INV[t],stab(s),stab(t))
ck((inc,dec,same)==(8,30,72), f'symmetry restriction counts {(inc,dec,same)}')
ck(stab(B['X_IMPLIES_Y'] & B['XNOR']) > stab(B['X_IMPLIES_Y']), 'specified stabilizer-increase example')
ck(stab(B['XOR'] & B['X_AND_NOT_Y']) < stab(B['XOR']), 'specified stabilizer-decrease example')

# Cylinder extension theorem for support cardinality: each unused bit doubles support.
def cylinder_count(native_support_size,m_unused):
    return native_support_size*(2**m_unused)
ck(cylinder_count(1,2)==4,'X 1->3 cylinder')
ck(cylinder_count(1,1)==2,'X&!Y 2->3 cylinder')
ck(cylinder_count(2,1)==4,'XOR 2->3 cylinder')

# A complete finite differentiation path using valid restriction only.
S0=B['TRUE']
S1=S0 & B['XOR']
S2=S1 & B['X']
ck(INV[S1]=='XOR','TRUE then XOR outcome')
ck(INV[S2]=='X_AND_NOT_Y','XOR then X=true outcome')
ck((S0.bit_count(),S1.bit_count(),S2.bit_count())==(4,2,1),'support path 4->2->1')
# Thesis-style AND -> XOR is not conditioning: supports are disjoint.
ck((B['AND'] & B['XOR'])==B['FALSE'],'AND to XOR is not a restriction outcome')

report={
    'status':'PASS',
    'assertions':checks,
    'compact_idempotents':{
        'f2':idem_f2,
        'boolean_semiring':idem_bool,
        'integer':idem_int,
        'cyclic_convolution_f2':idem_cyc,
    },
    'sequential_stats':{
        'f2':stats(idem_f2,'f2'),
        'boolean_semiring':stats(idem_bool,'bool'),
        'integer':stats(idem_int,'int'),
        'cyclic_convolution_f2':stats(idem_cyc,'cyc'),
        'diagonal_truth_effects':{'ordered_pairs':256,'commuting_pairs':256},
    },
    'projector_definition_counterexample':'|1><0| = E12 is nonzero and E12^2=0, so a general |alpha><beta| is not automatically a projector.',
    'symmetry':{
        'transpose_symmetric_connectives':8,
        'strict_nonempty_restrictions':{'stabilizer_increase':inc,'decrease':dec,'same':same},
        'increase_example':inc_example,
        'decrease_example':dec_example,
    },
    'finite_differentiation_path':['TRUE (4 valuations)','XOR (2 valuations)','X_AND_NOT_Y (1 valuation)'],
}
(OUT/'verification_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
