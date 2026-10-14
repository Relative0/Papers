#!/usr/bin/env python3
"""Direct AND-factor extraction for compressed SDD decompositions (small exact validator).

This module validates the theorem:
  At an SDD decision node over a vtree split L|R, f is disjoint-AND separable
  across L|R iff all non-false subs are equivalent. In a compressed SDD this
  means there is at most one non-false sub element.

For exhaustive small-n validation, we construct the canonical semantic
cofactor partition induced by a vtree directly from truth tables. This avoids
requiring an external SDD library while exactly matching the compressed
partition semantics relevant to the theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import List, Tuple, Dict, Iterable, Set
import json, statistics

VTree = object

def leaf(v:int): return ('L',v)
def node(l,r): return ('N',l,r)
def leaves(t):
    if t[0]=='L': return [t[1]]
    return leaves(t[1])+leaves(t[2])

def assignments(k): return range(1<<k)

def bit(bits:int,idx:int)->int: return (bits>>idx)&1

def truth_index(vals:Dict[int,int], order:List[int])->int:
    # little-endian local convention
    z=0
    for i,v in enumerate(order): z |= (vals[v]&1)<<i
    return z

def row_patterns(bits:int,L:List[int],R:List[int])->List[int]:
    order=L+R; rows=[]
    for a in assignments(len(L)):
        rm=0
        for b in assignments(len(R)):
            idx=a | (b<<len(L))
            if bit(bits,idx): rm |= 1<<b
        rows.append(rm)
    return rows

def root_compressed_profile(bits:int,t)->Dict:
    assert t[0]=='N'
    L=leaves(t[1]); R=leaves(t[2]); rows=row_patterns(bits,L,R)
    groups={}
    for a,r in enumerate(rows): groups.setdefault(r,[]).append(a)
    nz=[r for r in groups if r!=0]
    return {'left':L,'right':R,'groups':groups,'nonzero_subs':nz,'factor_cut':len(nz)<=1}

def rank1_cut(bits:int,L:List[int],R:List[int])->bool:
    rows=row_patterns(bits,L,R); nz={r for r in rows if r}
    return len(nz)<=1

def project_factor_tables(bits:int,t):
    prof=root_compressed_profile(bits,t)
    nz=prof['nonzero_subs']
    if len(nz)>1: return None
    if not nz: return 0,0
    h=nz[0]
    g=0
    for a,r in enumerate(row_patterns(bits,prof['left'],prof['right'])):
        if r: g |= 1<<a
    return g,h

def extract_t_laminar(bits:int,t)->List[Tuple[int,...]]:
    vs=leaves(t)
    if len(vs)==1: return [tuple(vs)]
    prof=root_compressed_profile(bits,t)
    if not prof['factor_cut']:
        return [tuple(vs)]
    gh=project_factor_tables(bits,t)
    if gh==(0,0):
        # Empty relation: prime Cartesian factorization is not canonical under the
        # nonempty-relation convention. The exhaustive campaign excludes it.
        raise ValueError('false function excluded')
    g,h=gh
    return extract_t_laminar(g,t[1])+extract_t_laminar(h,t[2])

def partition_valid(bits:int,vars_:List[int],part:List[List[int]])->bool:
    # nonempty relation only
    sats=[]
    for a in assignments(len(vars_)):
        if bit(bits,a): sats.append(a)
    if not sats: return False
    prodsz=1
    pos={v:i for i,v in enumerate(vars_)}
    for B in part:
        vals=set()
        for a in sats:
            z=0
            for j,v in enumerate(B): z |= ((a>>pos[v])&1)<<j
            vals.add(z)
        prodsz*=len(vals)
    return prodsz==len(sats)

def laminar_partitions(t):
    vs=leaves(t)
    if t[0]=='L': return [[[t[1]]]]
    out=[[vs]]
    for p in laminar_partitions(t[1]):
        for q in laminar_partitions(t[2]): out.append(p+q)
    # dedupe canonical
    seen=set(); ans=[]
    for p in out:
        k=tuple(sorted(tuple(sorted(b)) for b in p))
        if k not in seen: seen.add(k); ans.append([list(b) for b in k])
    return ans

def finest_laminar_brute(bits:int,t):
    vs=leaves(t); vals=[]
    for p in laminar_partitions(t):
        if partition_valid(bits,vs,p): vals.append(p)
    m=max(map(len,vals)); best=[p for p in vals if len(p)==m]
    keys={tuple(sorted(tuple(sorted(b)) for b in p)) for p in best}
    if len(keys)!=1: raise AssertionError('nonunique laminar finest partition')
    return list(next(iter(keys)))

def all_unordered_cuts(n:int):
    # fix variable 0 on A side
    for mask in range(1<<(n-1)):
        A={0}
        for j in range(1,n):
            if mask & (1<<(j-1)): A.add(j)
        if len(A)<n: yield A

def cut_rank1_global(bits:int,n:int,A:Set[int])->bool:
    L=sorted(A); R=[i for i in range(n) if i not in A]
    # permute global truth table logically
    rows=[]
    for aa in assignments(len(L)):
        rm=0
        for bb in assignments(len(R)):
            idx=0
            for i,v in enumerate(L): idx |= ((aa>>i)&1)<<v
            for j,v in enumerate(R): idx |= ((bb>>j)&1)<<v
            if bit(bits,idx): rm|=1<<bb
        rows.append(rm)
    return len({r for r in rows if r})<=1

def full_prime_partition(bits:int,n:int):
    # Recover prime blocks from all valid factor cuts: p,q are in same prime iff no valid cut separates them.
    separable=[[False]*n for _ in range(n)]
    for A in all_unordered_cuts(n):
        if cut_rank1_global(bits,n,A):
            for i in A:
                for j in range(n):
                    if j not in A: separable[i][j]=separable[j][i]=True
    # same relation should be an equivalence; make blocks by identical inseparability
    unseen=set(range(n)); blocks=[]
    while unseen:
        i=min(unseen); B={j for j in unseen if not separable[i][j]}
        # verify pairwise
        for x in B:
            for y in B:
                if separable[x][y]: raise AssertionError('inseparability not transitive')
        blocks.append(tuple(sorted(B))); unseen-=B
    return sorted(blocks)

def validate_all_n4():
    # balanced vtree ((0,1),(2,3))
    t=node(node(leaf(0),leaf(1)),node(leaf(2),leaf(3)))
    root_fail=0; lam_fail=0; hidden=0; full_decomp=0; aligned_exact=0
    hidden_examples=[]
    for bits in range(1,1<<16): # exclude false; include true
        prof=root_compressed_profile(bits,t)
        brute_root=cut_rank1_global(bits,4,{0,1})
        if prof['factor_cut']!=brute_root: root_fail+=1
        got=sorted(tuple(sorted(b)) for b in extract_t_laminar(bits,t))
        exp=sorted(tuple(sorted(b)) for b in finest_laminar_brute(bits,t))
        if got!=exp: lam_fail+=1
        full=full_prime_partition(bits,4)
        if len(full)>1: full_decomp+=1
        if got==full: aligned_exact+=1
        elif len(full)>len(got):
            hidden+=1
            if len(hidden_examples)<12:
                hidden_examples.append({'truth_bits':bits,'t_laminar':got,'full_prime':full})
    return {
      'functions_tested':(1<<16)-1,'root_cut_failures':root_fail,'laminar_extraction_failures':lam_fail,
      'full_decomposable_functions':full_decomp,'t_aligned_equals_full':aligned_exact,
      'full_factorization_strictly_finer_than_t_aligned':hidden,'hidden_examples':hidden_examples
    }

if __name__=='__main__':
    d=validate_all_n4(); print(json.dumps(d,indent=2))
    with open('/mnt/data/structured_factorization_phase4/data/sdd_extraction_validation.json','w') as f: json.dump(d,f,indent=2)
