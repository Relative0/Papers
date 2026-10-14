#!/usr/bin/env python3
from itertools import combinations
import random,json,csv,sys,time,statistics
sys.path.insert(0,'/mnt/data/phase5_work/structured_factorization_phase4/code')
import sdd_direct_extraction as sdd
sys.path.insert(0,'/mnt/data/phase5_output/code')
import vtree_exhaustive as ve

def balanced_tree(labels):
    labels=list(labels)
    if len(labels)==1:return ('L',labels[0])
    m=len(labels)//2
    return ve.canon(('N',balanced_tree(labels[:m]),balanced_tree(labels[m:])))

def tree_from_partition(part):
    sub=[balanced_tree(sorted(B)) for B in part]
    while len(sub)>1:
        nxt=[]
        for i in range(0,len(sub),2):
            if i+1<len(sub): nxt.append(ve.canon(('N',sub[i],sub[i+1])))
            else:nxt.append(sub[i])
        sub=nxt
    return sub[0]

def cnf_eval(cnf,a):
    for C in cnf:
        if not any((((a>>(abs(l)-1))&1)==1) if l>0 else (((a>>(abs(l)-1))&1)==0) for l in C): return 0
    return 1

def cnf_bits(cnf,n):
    z=0
    for a in range(1<<n):
        if cnf_eval(cnf,a): z|=1<<a
    return z

def interaction_components(cnf,n):
    adj=[set() for _ in range(n)]
    used=set()
    for C in cnf:
        vs=sorted(set(abs(l)-1 for l in C)); used.update(vs)
        for i in vs:
            for j in vs:
                if i!=j: adj[i].add(j)
    # all variables are included, isolated vars are components
    seen=set(); comps=[]
    for i in range(n):
        if i in seen:continue
        st=[i]; seen.add(i); B=[]
        while st:
            x=st.pop(); B.append(x)
            for y in adj[x]:
                if y not in seen:seen.add(y);st.append(y)
        comps.append(tuple(sorted(B)))
    return tuple(sorted(comps))

def random_partition(n,rng,min_blocks=1,max_blocks=None):
    if max_blocks is None:max_blocks=n
    k=rng.randint(min_blocks,max_blocks)
    # ensure nonempty blocks
    vals=list(range(n)); rng.shuffle(vals)
    blocks=[[vals[i]] for i in range(k)]
    for v in vals[k:]: blocks[rng.randrange(k)].append(v)
    return tuple(sorted(tuple(sorted(b)) for b in blocks))

def make_factorable(n,rng,redundant_cross=False):
    # choose 2-3 intended blocks, create connected positive/negative CNF inside each
    part=random_partition(n,rng,2,min(3,n))
    cnf=[]
    forced=[]
    for B in part:
        B=list(B)
        if len(B)==1:
            # nonconstant singleton
            lit=B[0]+1 if rng.random()<.5 else -(B[0]+1); cnf.append((lit,)); forced.append(lit)
        else:
            # chain clauses to connect; random signs, plus one forcing unit in some families
            for u,v in zip(B,B[1:]):
                lu=(u+1) if rng.random()<.5 else -(u+1)
                lv=(v+1) if rng.random()<.5 else -(v+1)
                cnf.append((lu,lv))
            if redundant_cross:
                u=B[0]; lit=(u+1) if rng.random()<.5 else -(u+1); cnf.append((lit,)); forced.append(lit)
    if redundant_cross and len(part)>=2:
        # add syntactically crossing clauses made true by a forced literal from one block
        # each clause is implied by its unit literal and hence semantically redundant
        for i in range(len(part)-1):
            B=part[i]; C=part[i+1]
            # find/create a positive/negative unit from B
            unit=None
            for cl in cnf:
                if len(cl)==1 and abs(cl[0])-1 in B: unit=cl[0]; break
            if unit is None:
                unit=B[0]+1; cnf.append((unit,))
            y=C[0]+1 if rng.random()<.5 else -(C[0]+1)
            cnf.append((unit,y))
    return cnf,part

def make_random_cnf(n,rng,m=8):
    cnf=[]
    for _ in range(m):
        k=rng.choice([2,2,3]); vs=rng.sample(range(n),k)
        cnf.append(tuple((v+1) if rng.random()<.5 else -(v+1) for v in vs))
    return cnf,None

def carrier_for(part,n,rng,mode):
    if mode=='aligned':
        return tuple(part)
    if mode=='singleton': return tuple((i,) for i in range(n))
    # crossing: random until at least one crossing with semantic partition
    for _ in range(100):
        K=random_partition(n,rng,2,min(3,n))
        if any(set(A)&set(B) and not(set(A)<=set(B) or set(B)<=set(A)) for A in K for B in part): return K
    return random_partition(n,rng,2,min(3,n))

def extracted_from_prime(full,t): return ve.laminar_from_prime(full,t)

def score(full,t):
    got=extracted_from_prime(full,t)
    return len(got), max(len(b) for b in got)

def run(seed=20260929,n=5,per_family=180):
    rng=random.Random(seed); trees=ve.all_vtrees(n)
    fixed=balanced_tree(range(n))
    records=[]
    families=['factorable_clean','factorable_redundant_cross','random_cnf']
    for fam in families:
      made=0; tries=0
      while made<per_family and tries<per_family*20:
        tries+=1
        if fam=='factorable_clean': cnf,intended=make_factorable(n,rng,False)
        elif fam=='factorable_redundant_cross': cnf,intended=make_factorable(n,rng,True)
        else: cnf,intended=make_random_cnf(n,rng,rng.randint(5,10))
        bits=cnf_bits(cnf,n)
        if bits==0: continue
        full=tuple(tuple(b) for b in sdd.full_prime_partition(bits,n)); k=len(full)
        comps=interaction_components(cnf,n)
        syntree=tree_from_partition(comps)
        # carrier mode chosen balanced among aligned/crossing/singleton
        cmode=['aligned','crossing','singleton'][made%3]
        carrier=carrier_for(full,n,rng,cmode)
        cartree=tree_from_partition(carrier)
        # global factor-exposure search: maximizes direct factor count, no truth partition in actual objective;
        # evaluated here equivalently using the exact prime partition for speed.
        best=max(trees,key=lambda t:(score(full,t)[0],-score(full,t)[1]))
        # one uniform random tree
        rt=rng.choice(trees)
        methods={'fixed':fixed,'random':rt,'syntax_components':syntree,'carrier_locked':cartree,'global_exposure_search':best}
        for meth,t in methods.items():
            d,maxr=score(full,t)
            records.append({'family':fam,'instance':made,'method':meth,'prime_blocks':k,'direct_blocks':d,
                            'full_alignment':int(d==k),'variables_direct_fraction':sum(len(b) for b in extracted_from_prime(full,t) if len(b)==1)/n,
                            'max_residual':maxr,'residual_cut_volume':sum((1<<(len(b)-1))-1 for b in extracted_from_prime(full,t) if len(b)>1),'syntax_components':len(comps),'carrier_mode':cmode,
                            'carrier_blocks':len(carrier),'cnf_clauses':len(cnf)})
        made+=1
    # aggregate
    groups={}
    for r in records:
        key=(r['family'],r['method']); groups.setdefault(key,[]).append(r)
    summary=[]
    for (fam,meth),rs in sorted(groups.items()):
        summary.append({'family':fam,'method':meth,'instances':len(rs),
                        'alignment_rate':sum(r['full_alignment'] for r in rs)/len(rs),
                        'mean_direct_blocks':statistics.mean(r['direct_blocks'] for r in rs),
                        'mean_prime_blocks':statistics.mean(r['prime_blocks'] for r in rs),
                        'mean_max_residual':statistics.mean(r['max_residual'] for r in rs),
                        'mean_residual_cut_volume':statistics.mean(r['residual_cut_volume'] for r in rs),
                        'mean_singleton_direct_fraction':statistics.mean(r['variables_direct_fraction'] for r in rs)})
    out={'seed':seed,'n':n,'per_family':per_family,'num_vtrees':len(trees),'summary':summary,'records':records}
    json.dump(out,open('/mnt/data/phase5_output/data/n5_benchmark_results.json','w'),indent=2)
    with open('/mnt/data/phase5_output/data/n5_benchmark_summary.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
    with open('/mnt/data/phase5_output/data/n5_benchmark_records.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
