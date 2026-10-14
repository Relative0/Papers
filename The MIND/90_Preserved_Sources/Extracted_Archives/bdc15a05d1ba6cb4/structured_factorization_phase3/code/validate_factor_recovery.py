#!/usr/bin/env python3
from itertools import product
import random, json, importlib.util
spec=importlib.util.spec_from_file_location('fc','/mnt/data/structured_factorization_phase3/code/four_corner_sat.py')
fc=importlib.util.module_from_spec(spec); import sys; sys.modules['fc']=fc; spec.loader.exec_module(fc)

def partitions(seq):
    if not seq:
        yield []; return
    first=seq[0]
    for rest in partitions(seq[1:]):
        yield [[first]]+[b[:] for b in rest]
        for i in range(len(rest)):
            nr=[b[:] for b in rest]; nr[i]=[first]+nr[i]
            yield nr

def cut_rank1(n,f,A): return fc.brute_rank1(n,f,set(A))

def partition_valid(n,f,part):
    # For Cartesian product / AND factorization across blocks, it suffices that all bipartitions
    # formed by one block vs the rest are rank-one; validate directly by relation projection product.
    sats=[]
    for bits in product((False,True), repeat=n):
        d={i+1:bits[i] for i in range(n)}
        if fc.eval_cnf(f,d): sats.append(bits)
    if not sats: return True
    projs=[]
    for B in part:
        inds=[v-1 for v in B]; projs.append(set(tuple(x[i] for i in inds) for x in sats))
    prod_size=1
    for p in projs: prod_size*=len(p)
    return prod_size==len(sats)

def finest_brute(n,f,carrier_blocks):
    # partitions of carrier blocks; choose max block count among valid => unique expected
    vals=[]
    idx=list(range(len(carrier_blocks)))
    for pp in partitions(idx):
        merged=[[v for bi in blockids for v in carrier_blocks[bi]] for blockids in pp]
        if partition_valid(n,f,merged): vals.append(merged)
    maxk=max(len(p) for p in vals)
    best=[p for p in vals if len(p)==maxk]
    norm=lambda p: sorted([tuple(sorted(b)) for b in p])
    uniq={tuple(norm(p)) for p in best}
    if len(uniq)!=1: return None, len(uniq)
    return list(next(iter(uniq))),1

def random_partition(n,rng):
    # random contiguous-ish partition labels
    labels=[0]
    for i in range(2,n+1):
        labels.append(rng.randrange(max(labels)+2))
    # normalize labels
    mp={}; blocks=[]
    for v,l in enumerate(labels,1):
        if l not in mp: mp[l]=len(blocks); blocks.append([])
        blocks[mp[l]].append(v)
    return blocks

def run(trials=80,seed=7):
    rng=random.Random(seed); rows=[]; failures=[]
    for t in range(trials):
        n=rng.randint(2,7); f=fc.random_cnf(n,rng.randint(1,2*n),rng.randint(1,min(3,n)),rng)
        blocks=random_partition(n,rng)
        got,st=fc.factor_blocks(n,f,blocks)
        exact,unq=finest_brute(n,f,blocks)
        ng=sorted(tuple(sorted(b)) for b in got)
        ok=(exact is not None and ng==exact)
        if not ok: failures.append(t)
        all_var_cuts=(1<<(n-1))-1
        carrier_cuts=(1<<(len(blocks)-1))-1 if len(blocks)>1 else 0
        rows.append({'trial':t,'n':n,'carrier_blocks':blocks,'k':len(blocks),'all_variable_bipartitions':all_var_cuts,'carrier_bipartitions':carrier_cuts,'sat_calls':st['sat_calls'],'cuts_tested':st['cuts_tested'],'recovered':ng,'exact':exact,'ok':ok})
    return {'trials':trials,'failures':failures,'rows':rows}

if __name__=='__main__':
    d=run(); print(json.dumps({'trials':d['trials'],'failure_count':len(d['failures'])},indent=2))
    with open('/mnt/data/structured_factorization_phase3/data/factor_recovery_validation.json','w') as f: json.dump(d,f,indent=2)
