#!/usr/bin/env python3
import csv, json, math, os
from functools import lru_cache
OUT=os.path.dirname(__file__)
INF=10**9

def bits(mask,n): return tuple((mask>>i)&1 for i in range(n))
def is_redundant(b): return all(b[i] <= b[i+1] for i in range(len(b)-1))
def is_defective(b):
    n=len(b)
    return any(b == (1,)*k + (0,)*(n-k) for k in range(1,n))
def cls(b):
    if is_redundant(b): return 'redundant'
    if is_defective(b): return 'defective'
    return 'nonredundant_homotopy_neutral'

def branch_sizes(b): return (b.count(0),b.count(1))

@lru_cache(None)
def opt(n):
    if n<=1: return (0,0,None) # depth, max redundant count, query
    best=(INF,INF,None)
    for mask in range(1,1<<n):
        b=bits(mask,n)
        if all(x==1 for x in b): continue
        c=cls(b)
        if c=='defective': continue
        z,o=branch_sizes(b)
        if not z or not o: continue
        d0,r0,_=opt(z); d1,r1,_=opt(o)
        if d0>=INF or d1>=INF: continue
        d=1+max(d0,d1)
        r=(1 if c=='redundant' else 0)+max(r0,r1)
        cand=(d,r,b)
        if cand[:2] < best[:2]: best=cand
    return best

@lru_cache(None)
def opt_nonred_only(n):
    if n<=1:return 0
    best=INF
    for mask in range(1,1<<n):
        b=bits(mask,n)
        if all(x==1 for x in b): continue
        if cls(b)!='nonredundant_homotopy_neutral': continue
        z,o=branch_sizes(b)
        if not z or not o: continue
        d0=opt_nonred_only(z);d1=opt_nonred_only(o)
        if max(d0,d1)<INF: best=min(best,1+max(d0,d1))
    return best

@lru_cache(None)
def min_redundancy(n):
    if n<=1:return 0
    best=INF
    for mask in range(1,1<<n):
        b=bits(mask,n)
        if all(x==1 for x in b): continue
        c=cls(b)
        if c=='defective': continue
        z,o=branch_sizes(b)
        if not z or not o: continue
        a=min_redundancy(z);d=min_redundancy(o)
        if max(a,d)>=INF: continue
        best=min(best,(1 if c=='redundant' else 0)+max(a,d))
    return best

def alternating(n): return tuple(i%2 for i in range(n))
def construction(n):
    if n<=1: return {'n':n,'leaf':True}
    if n==2: b=(0,1)
    else: b=alternating(n)
    z=b.count(0);o=b.count(1)
    return {'n':n,'query':' '.join(map(str,b)),'class':cls(b),'zero':construction(z),'one':construction(o)}

rows=[]; profiles=[]
for n in range(2,11):
    d,r,b=opt(n); nr=opt_nonred_only(n); mr=min_redundancy(n)
    # construction stats recurrence
    rows.append({
        'n':n,'information_lower_bound':math.ceil(math.log2(n)),
        'optimal_HN_depth':d,'min_max_redundant_count_among_depth_optimal':r,
        'minimum_possible_max_redundant_count':mr,
        'nonredundant_HN_only_depth':('INF' if nr>=INF else nr),
        'alternating_construction_depth':math.ceil(math.log2(n)),
        'theorem_checks':int(d==math.ceil(math.log2(n)) and r==1 and mr==1 and nr>=INF)
    })
    for mask in range(1<<n):
        b=bits(mask,n); c=cls(b); z,o=branch_sizes(b)
        profiles.append({'n':n,'mask':mask,'profile':' '.join(map(str,b)),'class':c,'zero_size':z,'one_size':o,'informative':int(z>0 and o>0)})

with open(os.path.join(OUT,'CHAIN_ADAPTIVE_DEPTHS.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT,'LEGAL_QUERY_PROFILES.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(profiles[0].keys())); w.writeheader(); w.writerows(profiles)
with open(os.path.join(OUT,'OPTIMAL_PROTOCOLS.json'),'w') as f:
    json.dump({str(n):construction(n) for n in range(2,11)},f,indent=2)
summary={'rows':rows,'all_checks_pass':all(r['theorem_checks'] for r in rows),'profiles':len(profiles)}
with open(os.path.join(OUT,'CHAIN_ADAPTIVE_SUMMARY.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
