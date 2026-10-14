#!/usr/bin/env python3
from functools import lru_cache
from itertools import combinations
import json, csv, os, random, statistics, math, time, sys
sys.path.insert(0,'C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase4/code')
import sdd_direct_extraction as sdd

def canon(t):
    if t[0]=='L': return t
    a,b=canon(t[1]),canon(t[2])
    return ('N',a,b) if repr(a)<repr(b) else ('N',b,a)

@lru_cache(None)
def all_vtrees_tuple(labels):
    labels=tuple(sorted(labels))
    if len(labels)==1: return (('L',labels[0]),)
    first=labels[0]; rest=labels[1:]
    out=set()
    # split with first in A to avoid A/B duplicate
    for r in range(0,len(rest)):
        for sub in combinations(rest,r):
            A=(first,)+sub
            if len(A)==len(labels): continue
            B=tuple(x for x in labels if x not in A)
            for ta in all_vtrees_tuple(tuple(A)):
                for tb in all_vtrees_tuple(tuple(B)):
                    out.add(canon(('N',ta,tb)))
    return tuple(sorted(out,key=repr))

def all_vtrees(n): return list(all_vtrees_tuple(tuple(range(n))))

def clusters(t):
    if t[0]=='L': return {frozenset([t[1]])}
    L=frozenset(sdd.leaves(t))
    return {L}|clusters(t[1])|clusters(t[2])

def part_key(p): return tuple(sorted(tuple(sorted(b)) for b in p))

def partition_is_aligned(part,t):
    cl=clusters(t)
    return all(frozenset(b) in cl for b in part)

def partition_valid_global(bits,n,part):
    sats=[a for a in range(1<<n) if (bits>>a)&1]
    if not sats: return False
    prod=1
    for B in part:
        vals=set()
        SB=sorted(B)
        for a in sats:
            z=0
            for j,v in enumerate(SB): z |= ((a>>v)&1)<<j
            vals.add(z)
        prod*=len(vals)
    return prod==len(sats)

def finest_laminar_global(bits,n,t):
    vals=[]
    for p in sdd.laminar_partitions(t):
        if partition_valid_global(bits,n,p): vals.append(p)
    m=max(map(len,vals))
    best=[part_key(p) for p in vals if len(p)==m]
    if len(set(best))!=1: raise AssertionError('nonunique laminar finest')
    return best[0]


def laminar_from_prime(full,t):
    """Finest vtree-laminar coarsening of the true prime partition."""
    if t[0]=='L': return ((t[1],),)
    L=set(sdd.leaves(t[1])); R=set(sdd.leaves(t[2]));
    for B in full:
        S=set(B)
        if S & L and S & R:
            return (tuple(sorted(L|R)),)
    left=[B for B in full if set(B)<=L]
    right=[B for B in full if set(B)<=R]
    return tuple(sorted(laminar_from_prime(left,t[1]) + laminar_from_prime(right,t[2])))

def tree_newick(t):
    if t[0]=='L': return f'x{t[1]}'
    return '('+tree_newick(t[1])+','+tree_newick(t[2])+')'

def fixed_balanced4(): return sdd.node(sdd.node(sdd.leaf(0),sdd.leaf(1)),sdd.node(sdd.leaf(2),sdd.leaf(3)))

def n4_campaign(out_json, out_csv):
    trees=all_vtrees(4)
    assert len(trees)==15, len(trees)
    fixed=canon(fixed_balanced4())
    ti={repr(t):i for i,t in enumerate(trees)}
    fixed_idx=ti[repr(fixed)]
    aligned_counts=[0]*len(trees)
    decomp_aligned_counts=[0]*len(trees)
    score_sums=[0]*len(trees)
    decomp=0; fixed_full=0; any_full=0
    aligned_tree_count_hist={}
    fixed_residual_hist={}; best_residual_hist={}
    rows=[]
    examples=[]
    start=time.time()
    for bits in range(1,1<<16):
        full=sdd.full_prime_partition(bits,4); k=len(full)
        if k>1: decomp+=1
        scores=[]; aligned=[]; residual_max=[]
        for j,t in enumerate(trees):
            got=laminar_from_prime(full,t); sc=len(got)
            scores.append(sc); score_sums[j]+=sc
            ok=(got==part_key(full))
            if ok:
                aligned_counts[j]+=1
                if k>1: decomp_aligned_counts[j]+=1
                aligned.append(j)
            residual_max.append(max(len(b) for b in got))
        if scores[fixed_idx]==k: fixed_full+=1
        if max(scores)==k: any_full+=1
        ac=len(aligned); aligned_tree_count_hist[ac]=aligned_tree_count_hist.get(ac,0)+1
        fr=residual_max[fixed_idx]; br=min(residual_max)
        fixed_residual_hist[fr]=fixed_residual_hist.get(fr,0)+1
        best_residual_hist[br]=best_residual_hist.get(br,0)+1
        if k>1 and len(examples)<20 and scores[fixed_idx]<k:
            examples.append({'truth_bits':bits,'prime_partition':full,'fixed_extracted':laminar_from_prime(full,trees[fixed_idx]),
                             'aligned_tree_count':ac,'example_aligned_vtree':tree_newick(trees[aligned[0]]) if aligned else None})
    total=(1<<16)-1
    # Expected alignment for uniformly random labelled vtree, over decomposable funcs
    mean_decomp_align_prob=sum(decomp_aligned_counts)/(decomp*len(trees))
    result={
      'n':4,'functions_tested':total,'labelled_binary_vtrees':len(trees),'decomposable_functions':decomp,
      'fixed_tree':tree_newick(trees[fixed_idx]),'fixed_full_alignment_all_functions':fixed_full,
      'fixed_full_alignment_decomposable':decomp_aligned_counts[fixed_idx],
      'global_direct_exposure_optimum_reaches_full_prime':any_full,
      'random_vtree_alignment_probability_on_decomposable_functions':mean_decomp_align_prob,
      'aligned_tree_count_histogram':dict(sorted(aligned_tree_count_hist.items())),
      'fixed_max_residual_block_histogram':dict(sorted(fixed_residual_hist.items())),
      'best_over_vtrees_max_residual_block_histogram':dict(sorted(best_residual_hist.items())),
      'per_vtree':[{'index':j,'newick':tree_newick(t),'aligned_all':aligned_counts[j],'aligned_decomposable':decomp_aligned_counts[j],
                    'mean_direct_blocks':score_sums[j]/total} for j,t in enumerate(trees)],
      'hidden_examples':examples,'runtime_seconds':time.time()-start}
    with open(out_json,'w') as f: json.dump(result,f,indent=2)
    with open(out_csv,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['index','newick','aligned_all','aligned_decomposable','mean_direct_blocks'])
        w.writeheader(); w.writerows(result['per_vtree'])
    print(json.dumps({k:v for k,v in result.items() if k not in ('per_vtree','hidden_examples')},indent=2))

if __name__=='__main__':
    n4_campaign('C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase5/data/n4_vtree_exhaustive.json','C:/Users/brian/Documents/Math Latex etc/Papers for Publication/Structured Factorization/phase5b_output/reproduction/relocated/phase5/data/n4_vtree_per_tree.csv')
