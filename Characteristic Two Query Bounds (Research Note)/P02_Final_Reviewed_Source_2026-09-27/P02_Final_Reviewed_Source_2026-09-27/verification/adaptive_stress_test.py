#!/usr/bin/env python3
"""Finite F2 stress test for the fixed-tree adaptive-record interpretation of P02 Lemma 3.1.

This is not a proof. It deliberately generates secret-independent adaptive trees with
branch-specific second queries and complete instruments, keeps impossible branches as
zero coordinates, and checks the resulting total-record coordinate functions have
ANF degree at most the maximum query depth.
"""
from __future__ import annotations
import json, random, itertools
from pathlib import Path

NSECRET = 3
NADDR = 1 << NSECRET
TARGET = 2
DIM = NADDR * TARGET

GL2 = []
for a,b,c,d in itertools.product((0,1), repeat=4):
    if (a*d ^ b*c) == 1:  # determinant 1 in F2
        GL2.append(((a,b),(c,d)))
assert len(GL2) == 6

def mv2(M, x0, x1):
    return ((M[0][0]&x0) ^ (M[0][1]&x1),
            (M[1][0]&x0) ^ (M[1][1]&x1))

def qapply(v, secret, pair):
    G0,G1 = pair
    out = [0]*DIM
    for x in range(NADDR):
        parity = ((x & secret).bit_count() & 1)
        M = G1 if parity else G0
        y0,y1 = v[2*x], v[2*x+1]
        z0,z1 = mv2(M,y0,y1)
        out[2*x],out[2*x+1] = z0,z1
    return out

def permute(v, perm):
    out = [0]*len(v)
    for i,j in enumerate(perm):
        out[j] = v[i]
    return out

def masked(v, mask):
    return [x if m else 0 for x,m in zip(v,mask)]

def split_complete(v, mask):
    # Complementary coordinate projections; stacked map is injective.
    return masked(v, mask), masked(v, [1-m for m in mask])

def rnd_perm(rng):
    p=list(range(DIM)); rng.shuffle(p); return p

def rnd_mask(rng):
    # force both halves nonempty as linear maps
    while True:
        m=[rng.randrange(2) for _ in range(DIM)]
        if any(m) and not all(m): return m

def rnd_state(rng):
    while True:
        v=[rng.randrange(2) for _ in range(DIM)]
        if any(v): return v

def anf_degree(vals):
    a=list(vals)
    for i in range(NSECRET):
        bit=1<<i
        for mask in range(1<<NSECRET):
            if mask & bit:
                a[mask] ^= a[mask ^ bit]
    deg=-1
    for mask,c in enumerate(a):
        if c:
            deg=max(deg, mask.bit_count())
    return deg

def rank_f2(rows):
    if not rows: return 0
    ints=[]
    for row in rows:
        z=0
        for i,b in enumerate(row):
            if b: z |= 1<<i
        ints.append(z)
    rank=0
    col=max((z.bit_length() for z in ints), default=0)-1
    while col>=0:
        pivot=next((i for i in range(rank,len(ints)) if (ints[i]>>col)&1), None)
        if pivot is None:
            col-=1; continue
        ints[rank],ints[pivot]=ints[pivot],ints[rank]
        for i in range(len(ints)):
            if i!=rank and ((ints[i]>>col)&1): ints[i]^=ints[rank]
        rank+=1
        col-=1
        if rank==len(ints): break
    return rank

def one_tree(rng, early=False):
    root=permute(rnd_state(rng), rnd_perm(rng))
    q1=(rng.choice(GL2),rng.choice(GL2))
    m1=rnd_mask(rng)
    perms=[rnd_perm(rng),rnd_perm(rng)]
    q2=[(rng.choice(GL2),rng.choice(GL2)),(rng.choice(GL2),rng.choice(GL2))]
    m2=[rnd_mask(rng),rnd_mask(rng)]
    records=[]; zero_first=0; zero_terminal=0
    for s in range(1<<NSECRET):
        v=qapply(root,s,q1)
        bs=split_complete(v,m1)
        if any((not any(b)) for b in bs): zero_first += 1
        leaves=[]
        for b in (0,1):
            u=bs[b]
            if early and b==0:
                leaves.append(u)
                continue
            u=permute(u,perms[b])
            u=qapply(u,s,q2[b])
            c0,c1=split_complete(u,m2[b])
            leaves.extend([c0,c1])
        zero_terminal += sum(1 for z in leaves if not any(z))
        records.append([bit for leaf in leaves for bit in leaf])
    maxdeg=-1
    for coord in range(len(records[0])):
        maxdeg=max(maxdeg, anf_degree([records[s][coord] for s in range(1<<NSECRET)]))
    return {
        'max_anf_degree': maxdeg,
        'record_rank': rank_f2(records),
        'zero_first_branch_evaluations': zero_first,
        'zero_terminal_branch_evaluations': zero_terminal,
        'early_termination_variant': early,
        'terminal_record_dimension': len(records[0]),
    }

def main():
    rng=random.Random(20260927)
    trials=[]
    for i in range(400):
        r=one_tree(rng, early=(i%2==1))
        assert r['max_anf_degree'] <= 2, r
        assert r['record_rank'] <= 7, r  # sum_{j=0}^2 C(3,j)=7
        trials.append(r)
    out={
        'status':'PASS',
        'purpose':'finite stress test only; not a proof',
        'field':'F2',
        'secret_bits':NSECRET,
        'max_queries':2,
        'trials':len(trials),
        'degree_bound_checked':'max coordinate ANF degree <= 2',
        'rank_bound_checked':'rank of 8 recorded secret states <= 7',
        'max_degree_observed':max(r['max_anf_degree'] for r in trials),
        'max_rank_observed':max(r['record_rank'] for r in trials),
        'trials_with_secret_dependent_zero_first_branches':sum(r['zero_first_branch_evaluations']>0 for r in trials),
        'trials_with_zero_terminal_branches':sum(r['zero_terminal_branch_evaluations']>0 for r in trials),
        'early_termination_trials':sum(r['early_termination_variant'] for r in trials),
        'seed':20260927,
    }
    path=Path('/mnt/data/p02_final_gate/adaptive_stress_test_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
