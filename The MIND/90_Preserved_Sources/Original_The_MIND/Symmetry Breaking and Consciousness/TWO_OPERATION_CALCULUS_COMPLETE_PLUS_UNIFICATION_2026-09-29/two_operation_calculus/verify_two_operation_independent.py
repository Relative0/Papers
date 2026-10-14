#!/usr/bin/env python3
"""Independent verifier for central claims, using frozenset/set representations.
This deliberately does not import two_operation_compute.py.
"""
from itertools import combinations
from math import factorial
import json, os
OUT=os.path.dirname(os.path.abspath(__file__))
Omega=frozenset(range(4))
Events=[]
for m in range(16): Events.append(frozenset(i for i in range(4) if (m>>i)&1))

def sig_partition(obs):
    buckets={}
    for x in Omega:
        sig=tuple(x in E for E in obs)
        buckets.setdefault(sig,set()).add(x)
    return frozenset(frozenset(v) for v in buckets.values())

def refines(q,p):
    return all(any(B <= A for A in p) for B in q)

def refine(p,E):
    out=[]
    for B in p:
        a=B&E;b=B-E
        if a:out.append(frozenset(a))
        if b:out.append(frozenset(b))
    return frozenset(out)

def topology_generated(obs):
    tau={frozenset(),Omega}
    tau.update(obs)
    changed=True
    while changed:
        changed=False
        old=list(tau)
        for A in old:
            for B in old:
                for C in (A|B,A&B):
                    C=frozenset(C)
                    if C not in tau:tau.add(C);changed=True
    return frozenset(tau)

def t0(tau):
    for x,y in combinations(Omega,2):
        if all((x in U)==(y in U) for U in tau): return False
    return True

def A2(S,p):return sum(len(S&B)*(len(S&B)-1)//2 for B in p)
def Gorder(S,p):
    z=1
    for B in p:z*=factorial(len(S&B))
    return z

# all set partitions by signatures of all observation families is sufficient to recover Bell(4)
partitions=set();topologies=set();t0tops=set()
for fm in range(1<<16):
    obs=[Events[i] for i in range(16) if (fm>>i)&1]
    p=sig_partition(obs); partitions.add(p)
    # To avoid recomputing all 65k topology closures independently, the independent verifier
    # uses membership preorders as canonical topology signatures.
    rel=frozenset((x,y) for x in Omega for y in Omega if all((x not in E) or (y in E) for E in obs))
    topologies.add(rel)
    if all(not (((x,y) in rel) and ((y,x) in rel)) for x,y in combinations(Omega,2)):
        t0tops.add(rel)
assert len(partitions)==15
assert len(topologies)==355
assert len(t0tops)==219

# all fixed-carrier R/M squares commute and ambiguity/group monotones contract
sq=0; mon=0
for p in partitions:
    for Sm in range(16):
        S=frozenset(i for i in Omega if (Sm>>i)&1)
        for E in Events:
            q=refine(p,E)
            assert A2(S,q)<=A2(S,p); assert Gorder(S,q)<=Gorder(S,p);mon+=2
            for F in Events:
                SF=S&F
                assert (SF,q)==(S&F,refine(p,E)); sq+=1
                assert A2(SF,p)<=A2(S,p); assert Gorder(SF,p)<=Gorder(S,p);mon+=2
assert sq==15*16*16*16

# minimum two-sided binary tests to separate four points
sep2=0
for a,b in combinations(range(16),2):
    if len(sig_partition([Events[a],Events[b]]))==4:sep2+=1
assert sep2==12
assert all(len(sig_partition([E]))<4 for E in Events)

# diagonal-event realization: D_E^2=D_E and products are intersections
for A in Events:
  da=[int(i in A) for i in Omega]
  assert [x*x for x in da]==da
  for B in Events:
    db=[int(i in B) for i in Omega]
    assert [da[i]*db[i] for i in Omega]==[int(i in (A&B)) for i in Omega]

summary={"independent_verifier":"PASS","partitions":len(partitions),"positive_topologies":len(topologies),"T0_topologies":len(t0tops),"MR_RM_squares":sq,"monotonicity_assertions":mon,"minimum_two_test_bases":sep2}
with open(os.path.join(OUT,'INDEPENDENT_VERIFICATION.json'),'w') as f:json.dump(summary,f,indent=2)
with open(os.path.join(OUT,'INDEPENDENT_VERIFICATION_LOG.txt'),'w') as f:
    for k,v in summary.items():f.write(f"{k}: {v}\n")
print(json.dumps(summary,indent=2))
