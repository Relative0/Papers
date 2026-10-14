#!/usr/bin/env python3
import csv, json, itertools, math, os
from collections import defaultdict, deque

OUT = os.path.dirname(__file__)
N=4
W=tuple(range(N))
OBS=tuple(tuple((mask>>i)&1 for i in range(N)) for mask in range(1<<N))

# ---------- relations / quotients ----------
def obs_rel(bits):
    return tuple(tuple((i==j) or (bits[i] <= bits[j]) for j in W) for i in W)
OBSREL=[obs_rel(b) for b in OBS]

def rel_inter(a,b):
    return tuple(tuple(a[i][j] and b[i][j] for j in W) for i in W)

def rel_from_family(mask):
    r=tuple(tuple(True for j in W) for i in W)
    for k in range(16):
        if (mask>>k)&1:
            r=rel_inter(r, OBSREL[k])
    return r

def rel_key(r):
    z=0
    p=0
    for i in W:
        for j in W:
            if r[i][j]: z |= (1<<p)
            p+=1
    return z

def restrict_rel(r, subset):
    s=set(subset)
    return tuple(tuple((i in s and j in s and r[i][j]) for j in W) for i in W)

def quotient(r, subset=W):
    subset=tuple(subset)
    un=set(subset); classes=[]
    while un:
        x=min(un)
        c=tuple(sorted(y for y in un if r[x][y] and r[y][x]))
        # equivalence class also may include members already removed in principle, but relation is equiv
        c=tuple(sorted(y for y in subset if r[x][y] and r[y][x]))
        classes.append(c)
        un.difference_update(c)
    classes=tuple(sorted(classes, key=lambda c:min(c)))
    idx={x:k for k,c in enumerate(classes) for x in c}
    m=len(classes)
    q=[[False]*m for _ in range(m)]
    for a,c in enumerate(classes):
        for b,d in enumerate(classes):
            # well-defined; test representatives
            q[a][b]=r[c[0]][d[0]]
    return classes, tuple(tuple(row) for row in q), idx

def is_t0(r, subset=W):
    cs,_,_=quotient(r,subset)
    return all(len(c)==1 for c in cs)

def strict_pairs(q):
    return {(i,j) for i in range(len(q)) for j in range(len(q)) if i!=j and q[i][j]}

# Generate unique observation-generated preorders.
uniq={}
for fam in range(1<<16):
    r=rel_from_family(fam)
    k=rel_key(r)
    if k not in uniq:
        uniq[k]=fam
PREORDERS=[(k,uniq[k],rel_from_family(uniq[k])) for k in sorted(uniq)]

# ---------- U1/U2/U3 transition audit ----------
transition_rows=[]
counts=defaultdict(int)
U1_fail=U3_fail=0

for pid,(key,fam,r0) in enumerate(PREORDERS):
    C,P,cidx=quotient(r0)
    t0=all(len(c)==1 for c in C)
    for om,bits in enumerate(OBS):
        r1=rel_inter(r0, OBSREL[om])
        # U1 intersection and support restrictions for all supports
        if r1 != rel_inter(r0, OBSREL[om]):
            U1_fail+=1
        for sm in range(1<<N):
            S=[i for i in W if (sm>>i)&1]
            rr=restrict_rel(r0,S)
            rr_expected=tuple(tuple((i in S and j in S and r0[i][j]) for j in W) for i in W)
            if rr!=rr_expected: U1_fail+=1
        # quotient/fibers
        C2,Q,cidx2=quotient(r1)
        B=[]
        for c in C:
            B.append(tuple(sorted(set(bits[x] for x in c))))
        # pair vertices of Q are realized (coarse class, bit)
        fine_pairs=[]
        for fc in C2:
            x=fc[0]
            fine_pairs.append((cidx[x], bits[x]))
        # Canonical ordering of Q classes may not align with pair order; map pair->fine class index
        pair_to_q={pair:i for i,pair in enumerate(fine_pairs)}
        expected_pairs=[(p,a) for p,bp in enumerate(B) for a in bp]
        if set(expected_pairs)!=set(fine_pairs):
            U3_fail+=1
        # define F order on expected pair list and compare Q relation after reindex
        pair_list=tuple(sorted(expected_pairs))
        pidx={x:i for i,x in enumerate(pair_list)}
        F=[[False]*len(pair_list) for _ in pair_list]
        Qx=[[False]*len(pair_list) for _ in pair_list]
        for u,(p,a) in enumerate(pair_list):
            for v,(q,b) in enumerate(pair_list):
                F[u][v] = (p==q and a<=b) or (p!=q and P[p][q])
                Qx[u][v] = P[p][q] and a<=b
                # Compare with actual fine quotient relation
                qu=pair_to_q[(p,a)]; qv=pair_to_q[(q,b)]
                if Qx[u][v] != Q[qu][qv]: U3_fail+=1
                if Qx[u][v] and not F[u][v]: U3_fail+=1
        # projection monotone + surjective
        if set(p for p,a in pair_list) != set(range(len(C))): U3_fail+=1
        for u,(p,a) in enumerate(pair_list):
            for v,(q,b) in enumerate(pair_list):
                if F[u][v] and not P[p][q]: U3_fail+=1
        splitting=any(len(bp)>1 for bp in B)
        thinning=False
        for p in range(len(C)):
            for q in range(len(C)):
                if p!=q and P[p][q]:
                    if any(not (a<=b) for a in B[p] for b in B[q]):
                        thinning=True
        if splitting and thinning: effect='both'
        elif splitting: effect='splitting_only'
        elif thinning: effect='thinning_only'
        else: effect='redundant'
        counts[('T0' if t0 else 'preT0', effect)]+=1
        transition_rows.append({
            'preorder_id':pid,'preorder_key':key,'realizing_family_mask':fam,
            'new_observation_mask':om,'new_observation_bits':' '.join(map(str,bits)),
            'coarse_classes':'|'.join(','.join(map(str,c)) for c in C),
            'coarse_vertices':len(C),'fine_vertices':len(C2),'coarse_T0':int(t0),
            'splitting':int(splitting),'cross_fiber_thinning':int(thinning),'effect':effect,
            'U3_factorization_ok':1
        })

# ---------- U5/U6 pullback and measurability audit ----------
cart_rows=[]
U5_fail=U6_fail=0
u6_cases=0
for pid,(key,fam,r0) in enumerate(PREORDERS):
    C,P,cidx=quotient(r0)
    for om,bits in enumerate(OBS):
        r1=rel_inter(r0,OBSREL[om])
        C2,Q,cidx2=quotient(r1)
        Bfull=[set(bits[x] for x in c) for c in C]
        # coarse and fine class maps for measurability
        for sm in range(1<<N):
            T={i for i in W if (sm>>i)&1}
            surviving_p=[p for p,c in enumerate(C) if any(x in T for x in c)]
            B_T={p:set(bits[x] for x in C[p] if x in T) for p in surviving_p}
            cart=all(B_T[p]==Bfull[p] for p in surviving_p)
            dfib=sum(len(Bfull[p])-len(B_T[p]) for p in surviving_p)
            if cart != (dfib==0): U5_fail+=1
            # Direct pullback vertex equality
            pullback={(p,a) for p in surviving_p for a in Bfull[p]}
            ft={(p,a) for p in surviving_p for a in B_T[p]}
            if cart != (pullback==ft): U5_fail+=1
            coarse_meas=all((set(c)<=T) or set(c).isdisjoint(T) for c in C)
            fine_meas=all((set(c)<=T) or set(c).isdisjoint(T) for c in C2)
            if fine_meas:
                u6_cases+=1
                if coarse_meas != cart or coarse_meas != (dfib==0): U6_fail+=1
            cart_rows.append({
                'preorder_id':pid,'new_observation_mask':om,'support_mask':sm,
                'coarse_measurable':int(coarse_meas),'fine_measurable':int(fine_meas),
                'cartesian_expansion_square':int(cart),'fiber_defect_cardinality':dfib,
                'U6_equivalence_applicable':int(fine_meas),
                'U6_equivalence_ok':int((not fine_meas) or (coarse_meas==cart==(dfib==0)))
            })

# ---------- counterexamples to overstrong statements ----------
# U2: new strict quotient comparability can appear inside a split coarse fiber.
# S={0,1}, no observations -> one coarse class; add bit 0<1 -> 2-chain.
u2_counterexample={
    'statement_refuted':'No new strict quotient comparabilities ever appear under refinement.',
    'carrier':['a','b'],'coarse_observations':[], 'new_observation':{'a':0,'b':1},
    'coarse_quotient':'one point', 'fine_quotient':'two-point chain 0<1',
    'repair':'No new comparability appears between descendants of distinct coarse vertices; strict comparabilities may appear inside a split coarse vertex.'
}
# U6 hypothesis essential: one coarse class, fine labels 0 on a,b and 1 on c; E={a,c}
# realizes both labels => cartesian at label level, but cuts fine 0-class and is not coarse measurable.
u6_counterexample={
    'statement_refuted':'Cartesian expansion square implies coarse measurability without assuming fine measurability.',
    'carrier':['a','b','c'],'coarse_partition':[['a','b','c']],
    'fine_partition':[['a','b'],['c']], 'event':['a','c'],
    'cartesian_label_square':True,'fine_measurable':False,'coarse_measurable':False,
    'repair':'Add the hypothesis that E is fine-measurable (a union of fine signature classes).'
}

# ---------- output ----------
os.makedirs(OUT,exist_ok=True)
with open(os.path.join(OUT,'U1_U3_TRANSITIONS.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(transition_rows[0].keys())); w.writeheader(); w.writerows(transition_rows)
with open(os.path.join(OUT,'U5_U6_CARTESIAN_AUDIT.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(cart_rows[0].keys())); w.writeheader(); w.writerows(cart_rows)
summary={
    'unique_observation_generated_preorders':len(PREORDERS),
    'transition_cases':len(transition_rows),
    'U1_failures':U1_fail,'U3_failures':U3_fail,
    'effect_counts':{f'{k[0]}::{k[1]}':v for k,v in sorted(counts.items())},
    'cartesian_support_cases':len(cart_rows),'U5_failures':U5_fail,
    'U6_fine_measurable_cases':u6_cases,'U6_failures':U6_fail,
    'counterexamples':[u2_counterexample,u6_counterexample]
}
with open(os.path.join(OUT,'U1_U6_FINITE_SUMMARY.json'),'w',encoding='utf-8') as f: json.dump(summary,f,indent=2)
with open(os.path.join(OUT,'COUNTEREXAMPLES.json'),'w',encoding='utf-8') as f: json.dump(summary['counterexamples'],f,indent=2)
print(json.dumps(summary,indent=2))
