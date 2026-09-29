import json, csv
from pathlib import Path
W=range(4)
PAIR=[(i,j) for i in W for j in W]
INDEX={p:k for k,p in enumerate(PAIR)}
ALL=(1<<16)-1
Robs=[]
for E in range(16):
    m=0
    for k,(i,j) in enumerate(PAIR):
        bi=(E>>i)&1; bj=(E>>j)&1
        if bi<=bj: m|=1<<k
    Robs.append(m)
rels={ALL}
for e in range(16):
    current=list(rels)
    rels |= {r & Robs[e] for r in current}

def eqmask(r):
    m=0
    for k,(i,j) in enumerate(PAIR):
        k2=INDEX[(j,i)]
        if (r>>k)&1 and (r>>k2)&1: m|=1<<k
    return m

def t0(r):
    for i in W:
        for j in W:
            if i!=j and ((r>>INDEX[(i,j)])&1) and ((r>>INDEX[(j,i)])&1):
                return False
    return True
counts={}
for r in rels:
    oldeq=eqmask(r)
    for ro in Robs:
        rp=r&ro
        assert rp & ~r == 0
        if rp==r:
            typ='redundant'
        else:
            neweq=eqmask(rp)
            split=neweq!=oldeq
            deleted=r & ~rp
            thin=bool(deleted & ~oldeq)
            typ='both' if split and thin else 'split_only' if split else 'thin_only' if thin else 'other'
        key=('T0' if t0(r) else 'preT0',typ)
        counts[key]=counts.get(key,0)+1
summary={
    'distinct_observation_generated_preorders':len(rels),
    't0_preorders':sum(1 for r in rels if t0(r)),
    'non_t0_preorders':sum(1 for r in rels if not t0(r)),
    'one_observation_transitions':len(rels)*16,
    'counts':{f'{a}:{b}':v for (a,b),v in sorted(counts.items())}
}
root=Path(__file__).resolve().parents[1]
(root/'results'/'PREORDER_TRANSITION_SUMMARY.json').write_text(json.dumps(summary,indent=2))
with (root/'results'/'PREORDER_TRANSITION_SUMMARY.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['regime','transition_type','count'])
    for (a,b),v in sorted(counts.items()): w.writerow([a,b,v])
print(json.dumps(summary,indent=2))
