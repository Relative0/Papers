#!/usr/bin/env python3
"""Exhaustive finite computations for the CM measurement audit.

Conventions
-----------
* A binary correspondence matrix (CM) stores truth values in true-first order
  (11,10,01,00) as [[11,10],[01,00]].
* Four compact-CM multiplication laws are kept separate:
    - XOR-AND matrix multiplication over F_2;
    - OR-AND Boolean-semiring matrix multiplication;
    - ordinary integer matrix multiplication (equivalently real/rational for
      idempotence of the 0/1 input matrices);
    - cyclic convolution over F_2 on the four coefficient positions in the
      quarter-turn cycle 11 -> 10 -> 00 -> 01 -> 11.
* The canonical measurement representation is *not* the compact 2x2 CM.  It is
  D_C = diag(C_11,C_10,C_01,C_00) on the four-dimensional valuation space.
"""
from itertools import product
from pathlib import Path
import csv
import json

OUT = Path('/mnt/data/cm_measurement_audit')
OUT.mkdir(parents=True, exist_ok=True)

# True-first CM ordering: (11,10,01,00); matrix [[11,10],[01,00]].
CONNECTIVES = {
    'FALSE': (0,0,0,0),
    'AND': (1,0,0,0),
    'X_AND_NOT_Y': (0,1,0,0),
    'NOT_X_AND_Y': (0,0,1,0),
    'NOR': (0,0,0,1),
    'X': (1,1,0,0),
    'Y': (1,0,1,0),
    'XOR': (0,1,1,0),
    'XNOR': (1,0,0,1),
    'NOT_Y': (0,1,0,1),
    'NOT_X': (0,0,1,1),
    'X_IMPLIES_Y': (1,0,1,1),
    'Y_IMPLIES_X': (1,1,0,1),
    'OR': (1,1,1,0),
    'NAND': (0,1,1,1),
    'TRUE': (1,1,1,1),
}
REV = {v:k for k,v in CONNECTIVES.items()}
VAL_LABELS = ('11','10','01','00')
B2 = ((0,0),(1,0),(0,1),(1,1))


def mat(bits4):
    a,b,c,d = bits4
    return ((a,b),(c,d))


def bits(A):
    return (A[0][0],A[0][1],A[1][0],A[1][1])


def bits_str(b):
    return ''.join(map(str,b))


def mat_str(A):
    return f'[[{A[0][0]},{A[0][1]}],[{A[1][0]},{A[1][1]}]]'


def prod_f2(A,B):
    return tuple(tuple((A[i][0]*B[0][j] + A[i][1]*B[1][j]) % 2
                       for j in range(2)) for i in range(2))


def prod_int(A,B):
    return tuple(tuple(A[i][0]*B[0][j] + A[i][1]*B[1][j]
                       for j in range(2)) for i in range(2))


def prod_bool(A,B):
    return tuple(tuple(int((A[i][0] and B[0][j]) or
                           (A[i][1] and B[1][j]))
                       for j in range(2)) for i in range(2))


def conv_vec_from_bits(b):
    # Quarter-turn coefficient cycle: 11 -> 10 -> 00 -> 01 -> 11.
    a11,a10,a01,a00 = b
    return (a11,a10,a00,a01)


def bits_from_conv(v):
    a11,a10,a00,a01 = v
    return (a11,a10,a01,a00)


def prod_conv_bits(a,b):
    x = conv_vec_from_bits(a)
    y = conv_vec_from_bits(b)
    z = [0]*4
    for i,xi in enumerate(x):
        for j,yj in enumerate(y):
            z[(i+j) % 4] ^= (xi & yj)
    return bits_from_conv(tuple(z))


def rank_f2(A):
    if all(x == 0 for row in A for x in row):
        return 0
    det = (A[0][0]*A[1][1] + A[0][1]*A[1][0]) % 2
    return 2 if det else 1


def rank_q(A):
    if all(x == 0 for row in A for x in row):
        return 0
    det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    return 2 if det else 1


def bool_rank(A):
    if all(x == 0 for row in A for x in row):
        return 0
    nonzero = ((0,1),(1,0),(1,1))
    for u in nonzero:
        for v in nonzero:
            O = ((u[0]&v[0],u[0]&v[1]),(u[1]&v[0],u[1]&v[1]))
            if O == A:
                return 1
    return 2


def vec_apply(A,v,law):
    if law == 'f2':
        return ((A[0][0]*v[0]+A[0][1]*v[1]) % 2,
                (A[1][0]*v[0]+A[1][1]*v[1]) % 2)
    if law == 'boolean_semiring':
        return (int((A[0][0] and v[0]) or (A[0][1] and v[1])),
                int((A[1][0] and v[0]) or (A[1][1] and v[1])))
    if law == 'integer':
        return (A[0][0]*v[0]+A[0][1]*v[1],
                A[1][0]*v[0]+A[1][1]*v[1])
    raise ValueError(law)


def regular_conv_matrix(b):
    """Regular representation of multiplication by b on F_2[C4]."""
    a = conv_vec_from_bits(b)
    cols = []
    for j in range(4):
        e = [0]*4
        e[j] = 1
        z = [0]*4
        for i,ai in enumerate(a):
            for k,ek in enumerate(e):
                z[(i+k) % 4] ^= ai & ek
        cols.append(z)
    return [[cols[j][i] for j in range(4)] for i in range(4)]


def gf2_rank_general(M):
    A = [row[:] for row in M]
    m = len(A)
    n = len(A[0]) if m else 0
    r = c = 0
    while r < m and c < n:
        piv = next((i for i in range(r,m) if A[i][c]), None)
        if piv is None:
            c += 1
            continue
        A[r],A[piv] = A[piv],A[r]
        for i in range(m):
            if i != r and A[i][c]:
                A[i] = [x^y for x,y in zip(A[i],A[r])]
        r += 1
        c += 1
    return r


LAWS = {
    'f2': lambda a,b: bits(prod_f2(mat(a),mat(b))),
    'boolean_semiring': lambda a,b: bits(prod_bool(mat(a),mat(b))),
    'integer': lambda a,b: prod_int(mat(a),mat(b)),
    'cyclic_convolution_f2': prod_conv_bits,
}


def compact_is_idempotent(b,law):
    if law == 'integer':
        return prod_int(mat(b),mat(b)) == mat(b)
    return LAWS[law](b,b) == b


# ---------------------------------------------------------------------------
# 1. Compact-CM idempotent classification under all four multiplication laws.
# ---------------------------------------------------------------------------
rows = []
for name,b in CONNECTIVES.items():
    A = mat(b)
    for law in LAWS:
        if law == 'integer':
            sq = prod_int(A,A)
            idem = (sq == A)
            sq_repr = mat_str(sq)
        else:
            sqb = LAWS[law](b,b)
            idem = (sqb == b)
            sq_repr = bits_str(sqb)

        row = {
            'representation':'compact_cm',
            'name':name,
            'bits_11_10_01_00':bits_str(b),
            'matrix':mat_str(A),
            'law':law,
            'idempotent':int(idem),
            'square':sq_repr,
            'rank_F2':rank_f2(A),
            'rank_Q':rank_q(A),
            'boolean_rank':bool_rank(A),
            'truth_support_size':sum(b),
        }

        if law in ('f2','boolean_semiring','integer'):
            outs = [vec_apply(A,v,law) for v in B2]
            fixed = [v for v,o in zip(B2,outs) if o == v]
            killed = [v for v,o in zip(B2,outs) if o == (0,0)]
            image = []
            for o in outs:
                if o not in image:
                    image.append(o)
            nonzero = B2[1:]
            nonzero_outs = [vec_apply(A,v,law) for v in nonzero]
            row.update({
                'actions_on_B2_00_10_01_11':';'.join(f'{v}->{o}' for v,o in zip(B2,outs)),
                'fixed_points_on_B2':';'.join(map(str,fixed)),
                'kernel_preimage_on_B2':';'.join(map(str,killed)),
                'image_on_B2':';'.join(map(str,image)),
                'fixed_nonzero_B2_count':sum(o == v for v,o in zip(nonzero,nonzero_outs)),
                'killed_nonzero_B2_count':sum(o == (0,0) for o in nonzero_outs),
                'transformed_nonzero_B2_count':sum(o != v and o != (0,0) for v,o in zip(nonzero,nonzero_outs)),
            })
            if law == 'f2':
                row['linear_image_dimension'] = rank_f2(A)
                row['linear_kernel_dimension'] = 2-rank_f2(A)
            elif law == 'integer':
                row['linear_image_dimension'] = rank_q(A)
                row['linear_kernel_dimension'] = 2-rank_q(A)
            else:
                row['linear_image_dimension'] = ''
                row['linear_kernel_dimension'] = ''
        else:
            rr = gf2_rank_general(regular_conv_matrix(b))
            row.update({
                'actions_on_B2_00_10_01_11':'N/A: convolution acts on four coefficient coordinates, not B2 state columns',
                'fixed_points_on_B2':'N/A',
                'kernel_preimage_on_B2':'N/A',
                'image_on_B2':'N/A',
                'fixed_nonzero_B2_count':'N/A',
                'killed_nonzero_B2_count':'N/A',
                'transformed_nonzero_B2_count':'N/A',
                'regular_rank_F2':rr,
                'linear_image_dimension':rr,
                'linear_kernel_dimension':4-rr,
            })
        rows.append(row)

with open(OUT/'PROJECTOR_CLASSIFICATION.csv','w',newline='',encoding='utf-8') as f:
    fields = [
        'representation','name','bits_11_10_01_00','matrix','law','idempotent','square',
        'truth_support_size','rank_F2','rank_Q','boolean_rank','regular_rank_F2',
        'linear_image_dimension','linear_kernel_dimension','actions_on_B2_00_10_01_11',
        'fixed_points_on_B2','kernel_preimage_on_B2','image_on_B2',
        'fixed_nonzero_B2_count','killed_nonzero_B2_count','transformed_nonzero_B2_count'
    ]
    w = csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)


# ---------------------------------------------------------------------------
# 2. Sequential products.  Compact rows are algebraic diagnostics.  Canonical
#    diagonal-effect rows are the endorsed sharp Boolean measurement algebra.
# ---------------------------------------------------------------------------
seq = []
for law in LAWS:
    idem = [(n,b) for n,b in CONNECTIVES.items() if compact_is_idempotent(b,law)]
    for pn,p in idem:
        for qn,q in idem:
            if law == 'integer':
                pqM = prod_int(mat(p),mat(q))
                qpM = prod_int(mat(q),mat(p))
                pq_binary = all(x in (0,1) for row in pqM for x in row)
                qp_binary = all(x in (0,1) for row in qpM for x in row)
                pqb = bits(pqM) if pq_binary else None
                qpb = bits(qpM) if qp_binary else None
                commute = (pqM == qpM)
                pq_idem = (prod_int(pqM,pqM) == pqM)
                prod_name = REV.get(pqb,'NON_BINARY') if pqb is not None else 'NON_BINARY'
                reverse_name = REV.get(qpb,'NON_BINARY') if qpb is not None else 'NON_BINARY'
                prod_repr = mat_str(pqM)
                reverse_repr = mat_str(qpM)
            else:
                pqb = LAWS[law](p,q)
                qpb = LAWS[law](q,p)
                commute = (pqb == qpb)
                pq_idem = (LAWS[law](pqb,pqb) == pqb)
                prod_name = REV.get(pqb,'UNNAMED')
                reverse_name = REV.get(qpb,'UNNAMED')
                prod_repr = bits_str(pqb)
                reverse_repr = bits_str(qpb)
            seq.append({
                'representation':'compact_cm',
                'law':law,
                'P':pn,'Q':qn,
                'P_bits':bits_str(p),'Q_bits':bits_str(q),
                'PQ':prod_name,'QP':reverse_name,
                'PQ_repr':prod_repr,'QP_repr':reverse_repr,
                'commute':int(commute),'compatible_by_commutation':int(commute),
                'PQ_idempotent':int(pq_idem),
                'P_truth_support_size':sum(p),'Q_truth_support_size':sum(q),
                'PQ_truth_support_size':sum(pqb) if isinstance(pqb,tuple) and len(pqb)==4 else '',
                'semantic_note':'Algebraic compact-CM product; not automatically a logical measurement sequence.'
            })

# Canonical diagonal projectors: all 16 effects, all ordered pairs.
for pn,p in CONNECTIVES.items():
    for qn,q in CONNECTIVES.items():
        pq = tuple(a & b for a,b in zip(p,q))
        seq.append({
            'representation':'diagonal_truth_effect',
            'law':'ordinary/F2/Boolean diagonal multiplication (all agree on 0/1 diagonals)',
            'P':pn,'Q':qn,
            'P_bits':bits_str(p),'Q_bits':bits_str(q),
            'PQ':REV[pq],'QP':REV[pq],
            'PQ_repr':f'diag({bits_str(pq)})','QP_repr':f'diag({bits_str(pq)})',
            'commute':1,'compatible_by_commutation':1,'PQ_idempotent':1,
            'P_truth_support_size':sum(p),'Q_truth_support_size':sum(q),
            'PQ_truth_support_size':sum(pq),
            'semantic_note':'Canonical sharp Boolean measurement: sequential product is truth-region intersection.'
        })

with open(OUT/'SEQUENTIAL_MEASUREMENTS.csv','w',newline='',encoding='utf-8') as f:
    fields = list(seq[0].keys())
    w = csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    w.writerows(seq)


# ---------------------------------------------------------------------------
# 3. Canonical diagonal truth-effect projectors on the valuation basis.
# ---------------------------------------------------------------------------
diag = []
for name,b in CONNECTIVES.items():
    fixed = [lbl for bit,lbl in zip(b,VAL_LABELS) if bit]
    killed = [lbl for bit,lbl in zip(b,VAL_LABELS) if not bit]
    diag.append({
        'name':name,
        'bits_11_10_01_00':bits_str(b),
        'operator':f'diag({bits_str(b)})',
        'idempotent':1,
        'self_adjoint_over_R_or_C':1,
        'projector_rank':sum(b),
        'image_dimension':sum(b),
        'kernel_dimension':4-sum(b),
        'fixed_basis_valuations':','.join(fixed),
        'killed_basis_valuations':','.join(killed),
        'complement':REV[tuple(1-x for x in b)],
    })
with open(OUT/'DIAGONAL_EFFECT_PROJECTORS.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,fieldnames=list(diag[0].keys()))
    w.writeheader()
    w.writerows(diag)


# ---------------------------------------------------------------------------
# 4. Symmetry under the signed-input square group D4 and under operand swap.
# ---------------------------------------------------------------------------
cells = [(1,1),(1,0),(0,1),(0,0)]
idx = {c:i for i,c in enumerate(cells)}

def transforms():
    fs = []
    for swap in [0,1]:
        for fx in [0,1]:
            for fy in [0,1]:
                perm = []
                for x,y in cells:
                    if swap:
                        x,y = y,x
                    if fx:
                        x = 1-x
                    if fy:
                        y = 1-y
                    perm.append(idx[(x,y)])
                if perm not in fs:
                    fs.append(perm)
    return fs
D4 = transforms()
assert len(D4) == 8

# operand swap permutation on truth cells: 11 fixed,10<->01,00 fixed
SWAP = [0,2,1,3]

def act_subset(b,perm):
    out = [0]*4
    for i,val in enumerate(b):
        if val:
            out[perm[i]] = 1
    return tuple(out)


def stab_size(b):
    return sum(act_subset(b,p) == b for p in D4)

sym = []
for n,b in CONNECTIVES.items():
    swap_sym = int(act_subset(b,SWAP) == b)
    sym.append({
        'name':n,'bits':bits_str(b),'truth_support_size':sum(b),
        'transpose_operand_swap_symmetric':swap_sym,
        'stabilizer_operand_swap_group':2 if swap_sym else 1,
        'stabilizer_D4':stab_size(b),
        'orbit_size_D4':8//stab_size(b),
    })
with open(OUT/'SYMMETRY_TABLE.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,fieldnames=list(sym[0].keys()))
    w.writeheader()
    w.writerows(sym)

# All support restrictions S -> S & E.
restr = []
for sn,s in CONNECTIVES.items():
    for en,e in CONNECTIVES.items():
        t = tuple(a&b for a,b in zip(s,e))
        tn = REV[t]
        restr.append({
            'state':sn,'effect':en,'result':tn,
            'state_size':sum(s),'result_size':sum(t),
            'state_transpose_symmetric':int(act_subset(s,SWAP)==s),
            'result_transpose_symmetric':int(act_subset(t,SWAP)==t),
            'state_stabilizer_D4':stab_size(s),'result_stabilizer_D4':stab_size(t),
            'stabilizer_change_D4':stab_size(t)-stab_size(s),
            'strict_restriction':int(t != s),
            'outcome_possible':int(sum(t)>0),
        })
with open(OUT/'RESTRICTION_SYMMETRY_TRANSITIONS.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,fieldnames=list(restr[0].keys()))
    w.writeheader()
    w.writerows(restr)


# ---------------------------------------------------------------------------
# 5. Three-variable cylinder embeddings.
# ---------------------------------------------------------------------------
vals3 = list(product([1,0], repeat=3))

def supp3(fn):
    return [v for v in vals3 if fn(*v)]

embedding_rows = [
    {
        'formula':'X','native_variables':1,'native_true_support_size':1,
        'embedded_to_3_support_size':len(supp3(lambda x,y,z:x==1)),
        'expected_cylinder_multiplier':4,
        'embedded_support':str(supp3(lambda x,y,z:x==1)),
        'pure_native':1,'pure_after_embedding':0,
    },
    {
        'formula':'X_AND_NOT_Y','native_variables':2,'native_true_support_size':1,
        'embedded_to_3_support_size':len(supp3(lambda x,y,z:x==1 and y==0)),
        'expected_cylinder_multiplier':2,
        'embedded_support':str(supp3(lambda x,y,z:x==1 and y==0)),
        'pure_native':1,'pure_after_embedding':0,
    },
    {
        'formula':'X_XOR_Y','native_variables':2,'native_true_support_size':2,
        'embedded_to_3_support_size':len(supp3(lambda x,y,z:(x^y)==1)),
        'expected_cylinder_multiplier':2,
        'embedded_support':str(supp3(lambda x,y,z:(x^y)==1)),
        'pure_native':0,'pure_after_embedding':0,
    },
]
with open(OUT/'THREE_VARIABLE_EMBEDDING.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,fieldnames=list(embedding_rows[0].keys()))
    w.writeheader()
    w.writerows(embedding_rows)


# ---------------------------------------------------------------------------
# 6. Summary.
# ---------------------------------------------------------------------------
summary = {}
for law in LAWS:
    idem = [r['name'] for r in rows if r['law']==law and r['idempotent']==1]
    srows = [r for r in seq if r['representation']=='compact_cm' and r['law']==law]
    summary[law] = {
        'idempotents':idem,
        'count':len(idem),
        'ordered_idempotent_pairs':len(srows),
        'commuting_pairs':sum(r['commute'] for r in srows),
        'noncommuting_pairs':sum(1-r['commute'] for r in srows),
        'pq_idempotent_pairs':sum(r['PQ_idempotent'] for r in srows),
    }

counter_inc = [r for r in restr if r['strict_restriction'] and r['outcome_possible'] and r['stabilizer_change_D4']>0]
counter_dec = [r for r in restr if r['strict_restriction'] and r['outcome_possible'] and r['stabilizer_change_D4']<0]
counter_same = [r for r in restr if r['strict_restriction'] and r['outcome_possible'] and r['stabilizer_change_D4']==0]
summary['diagonal_truth_effects'] = {
    'projectors':16,
    'ordered_pairs':256,
    'commuting_pairs':256,
    'sequential_product_rule':'D_E D_F = D_{E intersection F}',
}
summary['symmetry'] = {
    'D4_group_size':8,
    'transpose_symmetric_connectives':sum(r['transpose_operand_swap_symmetric'] for r in sym),
    'nonempty_strict_restrictions_increasing_stabilizer':len(counter_inc),
    'nonempty_strict_restrictions_decreasing_stabilizer':len(counter_dec),
    'nonempty_strict_restrictions_preserving_stabilizer':len(counter_same),
    'example_increase':counter_inc[0] if counter_inc else None,
    'example_decrease':counter_dec[0] if counter_dec else None,
    'example_same':counter_same[0] if counter_same else None,
}
summary['three_variable_embedding'] = {
    'rows':embedding_rows,
    'general_rule':'support size multiplies by 2^m under a canonical cylinder extension by m unused Boolean variables',
}
with open(OUT/'summary.json','w',encoding='utf-8') as f:
    json.dump(summary,f,indent=2)

print(json.dumps(summary,indent=2))
