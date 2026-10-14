"""Deterministic CNF-only inputs; no semantic labels in the benchmark manifest."""
from pathlib import Path
import hashlib, itertools, json, random

ROOT = Path(__file__).resolve().parents[1]
SEED = 2026092905
FAMILIES = ['clean_factorable', 'partially_factorable', 'redundant_cross',
            'bounded_treewidth', 'random_cnf', 'read_once', 'repeated_module',
            'carrier_aligned', 'carrier_crossing', 'indecomposable']

def eq(a, b):
    return [[-a,b],[a,-b]]

def generate(family, n, seed):
    rng = random.Random(seed)
    order = list(range(1,n+1)); rng.shuffle(order)
    groups = [order[i:i+2] for i in range(0,n,2)]
    clauses = [c for g in groups for c in eq(*g)]
    carrier = [[v] for v in range(1,n+1)]
    if family == 'partially_factorable':
        clauses = [c for a,b in zip(order[:n-2],order[1:n-2]) for c in eq(a,b)] + [order[-2:]]
    elif family == 'redundant_cross':
        clauses += [clauses[i] + [order[(i+3)%n]] for i in range(0,len(clauses),2)]
    elif family == 'bounded_treewidth':
        clauses = [[order[i], -order[i+1]] for i in range(n-1)]
    elif family == 'random_cnf':
        # Positive planted literal keeps the family nonfalse without rejection sampling.
        clauses=[]
        for _ in range(3*n):
            vs=rng.sample(order,3); signs=[rng.choice([-1,1]) for _ in vs]
            signs[rng.randrange(3)]=1
            clauses.append([v*s for v,s in zip(vs,signs)])
    elif family == 'read_once':
        # Read-once AND of OR modules; no Tseitin auxiliaries enter the semantic universe.
        clauses = [g[:] for g in groups]
    elif family == 'repeated_module':
        # Repeated syntactic use of (a <-> b), distributed: m AND (m OR c) = m.
        clauses = []
        for i,g in enumerate(groups):
            module=eq(*g); clauses += module + [c + [order[(2*i+2)%n]] for c in module]
    elif family == 'carrier_aligned':
        carrier = [g[:] for g in groups]
    elif family == 'carrier_crossing':
        carrier = [[order[i],order[(i+3)%n]] for i in range(0,n,2)]
        assert sorted(v for b in carrier for v in b)==list(range(1,n+1))
    elif family == 'indecomposable':
        clauses = [c for a,b in zip(order,order[1:]) for c in eq(a,b)]
    return {'n':n,'clauses':clauses,'carrier':carrier}

def main():
    records=[]
    for fi,family in enumerate(FAMILIES):
        for si,(split,sizes) in enumerate([('train',[6,8]),('validation',[6,8]),('heldout',[6,8,10])]):
            for ni,n in enumerate(sizes):
                seed=SEED+10000*fi+100*si+ni
                r={'id':f'{family}_{split}_n{n}', 'family':family,'split':split,'seed':seed,
                   'source':'generated','license':'CC0-1.0 generated instance data', **generate(family,n,seed)}
                r['cnf_sha256']=hashlib.sha256(json.dumps([r['n'],r['clauses']],separators=(',',':')).encode()).hexdigest()
                records.append(r)
    out=ROOT/'data'/'benchmark_manifest.json'
    if out.exists(): raise SystemExit('Manifest already frozen; refusing overwrite')
    out.write_text(json.dumps({'seed':SEED,'records':records},indent=2)+'\n')
    print(json.dumps({'instances':len(records),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))

if __name__=='__main__': main()
