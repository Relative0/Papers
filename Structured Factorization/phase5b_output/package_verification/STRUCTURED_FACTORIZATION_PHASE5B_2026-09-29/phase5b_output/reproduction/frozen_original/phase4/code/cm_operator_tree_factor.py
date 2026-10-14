#!/usr/bin/env python3
"""Exact prime AND-factor extraction for read-once CM/LM operator trees.

Internal binary gates are arbitrary *essential* Boolean connectives. Each leaf
variable occurs once, so child supports are disjoint. For a node f=Theta(g,h):
  - if the 2x2 CM of the requested output polarity has F2-rank 2, every variable
    in supp(g) and supp(h) is forced into one prime factor block;
  - if it has rank 1, the gate is a signed conjunction of its two child outputs,
    and factor extraction recurses independently on the corresponding child
    polarities.

This is a representation-specific formulation of a read-once factorization fact;
read-once Boolean factorization itself has classical antecedents.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Tuple, List, Set, Dict, Iterable
import json, random, statistics

# Truth-table order 00,01,10,11. A table is a 4-tuple of 0/1.
Table=Tuple[int,int,int,int]
MASK_CACHE={}

def table_eval(t:Table,a:int,b:int)->int: return t[(a<<1)|b]
def complement(t:Table)->Table: return tuple(1-x for x in t)  # type: ignore

def depends_left(t:Table)->bool: return any(table_eval(t,0,b)!=table_eval(t,1,b) for b in (0,1))
def depends_right(t:Table)->bool: return any(table_eval(t,a,0)!=table_eval(t,a,1) for a in (0,1))
def essential(t:Table)->bool: return depends_left(t) and depends_right(t)
def det_f2(t:Table)->int: return (t[0]*t[3]) ^ (t[1]*t[2])
def rank_f2(t:Table)->int:
    if not any(t): return 0
    return 2 if det_f2(t) else 1

def essential_tables()->List[Table]:
    out=[]
    for z in range(16):
        t=tuple((z>>i)&1 for i in range(4))
        if essential(t): out.append(t) # type: ignore
    return out
ESS=essential_tables()

def rank1_signed_children(t:Table)->Tuple[int,int]:
    """For an essential rank-one table return child polarities (pl,pr).

    pl=0 means use g, pl=1 means use not-g; similarly right. Since an essential
    rank-one 2x2 Boolean matrix has exactly one 1, it is the conjunction of one
    literal of each child output.
    """
    if not essential(t) or rank_f2(t)!=1: raise ValueError('requires essential rank-one table')
    ones=[i for i,x in enumerate(t) if x]
    if len(ones)!=1: raise AssertionError('essential rank-one Boolean table must be singleton support')
    i=ones[0]; a=i>>1; b=i&1
    # indicator [g=a] is g when a=1, !g when a=0
    return (0 if a==1 else 1, 0 if b==1 else 1)

@dataclass(frozen=True)
class Leaf:
    v:int
@dataclass(frozen=True)
class Gate:
    table:Table
    left:object
    right:object


def support(t)->Tuple[int,...]:
    if isinstance(t,Leaf): return (t.v,)
    return tuple(sorted(support(t.left)+support(t.right)))

def predicted_partition(t, polarity:int=0)->List[Tuple[int,...]]:
    if isinstance(t,Leaf): return [(t.v,)]
    tab=complement(t.table) if polarity else t.table
    r=rank_f2(tab)
    if r==2: return [support(t)]
    if r==1:
        pl,pr=rank1_signed_children(tab)
        return predicted_partition(t.left,pl)+predicted_partition(t.right,pr)
    raise ValueError('constant-zero target excluded')


def var_bitset(n:int,v:int)->int:
    bits=0
    for a in range(1<<n):
        if (a>>v)&1: bits|=1<<a
    return bits

def apply_gate_bits(tab:Table,A:int,B:int,n:int)->int:
    mask=(1<<(1<<n))-1
    na=(~A)&mask; nb=(~B)&mask
    terms=[na&nb, na&B, A&nb, A&B]
    out=0
    for i,x in enumerate(tab):
        if x: out|=terms[i]
    return out

def eval_bits(t,n:int)->int:
    if isinstance(t,Leaf): return var_bitset(n,t.v)
    return apply_gate_bits(t.table,eval_bits(t.left,n),eval_bits(t.right,n),n)

def bit(bits:int,i:int)->int: return (bits>>i)&1

def cut_rank1(bits:int,n:int,A:Set[int])->bool:
    L=sorted(A); R=[i for i in range(n) if i not in A]
    nonzero=None
    for aa in range(1<<len(L)):
        row=0
        for bb in range(1<<len(R)):
            idx=0
            for i,v in enumerate(L): idx|=((aa>>i)&1)<<v
            for j,v in enumerate(R): idx|=((bb>>j)&1)<<v
            if bit(bits,idx): row|=1<<bb
        if row:
            if nonzero is None: nonzero=row
            elif row!=nonzero: return False
    return True

def all_cuts(n:int):
    for mask in range(1<<(n-1)):
        A={0}
        for j in range(1,n):
            if mask&(1<<(j-1)): A.add(j)
        if len(A)<n: yield A

def prime_partition_brute(bits:int,n:int)->List[Tuple[int,...]]:
    sep=[[False]*n for _ in range(n)]
    for A in all_cuts(n):
        if cut_rank1(bits,n,A):
            for x in A:
                for y in range(n):
                    if y not in A: sep[x][y]=sep[y][x]=True
    unseen=set(range(n)); out=[]
    while unseen:
        x=min(unseen); B={y for y in unseen if not sep[x][y]}
        for a in B:
            for b in B:
                if sep[a][b]: raise AssertionError('prime-block relation failed transitivity')
        out.append(tuple(sorted(B))); unseen-=B
    return sorted(out)

def shapes(vars_:Tuple[int,...]):
    if len(vars_)==1:
        yield Leaf(vars_[0]); return
    for k in range(1,len(vars_)):
        for l in shapes(vars_[:k]):
            for r in shapes(vars_[k:]): yield ('shape',l,r)

def internal_count(sh)->int:
    return 0 if isinstance(sh,Leaf) else 1+internal_count(sh[1])+internal_count(sh[2])
def instantiate(sh,tabs_iter)->object:
    if isinstance(sh,Leaf): return sh
    tab=next(tabs_iter)
    return Gate(tab,instantiate(sh[1],tabs_iter),instantiate(sh[2],tabs_iter))

def validate_exhaustive(max_n=5, max_n5=None, seed=123):
    rng=random.Random(seed); total=0; failures=[]; by_n={}
    for n in range(2,max_n+1):
        tested=0; fail=0; shs=list(shapes(tuple(range(n))))
        assignments_total=len(shs)*(len(ESS)**(n-1))
        sample_limit=assignments_total if (n<5 or max_n5 is None) else min(max_n5,assignments_total)
        # exhaustive for n<5; for n=5 allow reservoir-like random gate labels if capped
        if n<5 or sample_limit==assignments_total:
            iterator=[]
            # stream manually below to avoid materializing labels
            for sh in shs:
                for labs in product(ESS, repeat=n-1):
                    t=instantiate(sh,iter(labs)); bits=eval_bits(t,n)
                    got=sorted(predicted_partition(t,0)); exp=prime_partition_brute(bits,n)
                    tested+=1; total+=1
                    if got!=exp:
                        fail+=1
                        if len(failures)<20: failures.append({'n':n,'bits':bits,'got':got,'exp':exp,'tables':[list(x) for x in labs]})
        else:
            for _ in range(sample_limit):
                sh=rng.choice(shs); labs=[rng.choice(ESS) for _ in range(n-1)]
                t=instantiate(sh,iter(labs)); bits=eval_bits(t,n)
                got=sorted(predicted_partition(t,0)); exp=prime_partition_brute(bits,n)
                tested+=1; total+=1
                if got!=exp:
                    fail+=1
                    if len(failures)<20: failures.append({'n':n,'bits':bits,'got':got,'exp':exp,'tables':[list(x) for x in labs]})
        by_n[str(n)]={'tree_instances_tested':tested,'available_if_exhaustive':assignments_total,'failures':fail}
    return {'essential_binary_connectives':len(ESS),'total_tested':total,'failures':failures,'by_n':by_n}

if __name__=='__main__':
    d=validate_exhaustive(max_n=5,max_n5=30000)
    print(json.dumps({'essential_binary_connectives':d['essential_binary_connectives'],'total_tested':d['total_tested'],'failure_count':len(d['failures']),'by_n':d['by_n']},indent=2))
    with open('/mnt/data/structured_factorization_phase4/data/operator_tree_validation.json','w') as f: json.dump(d,f,indent=2)
