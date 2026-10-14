import json,csv
from pathlib import Path
W=tuple(range(4))

def parts(seq):
    if not seq:
        yield (); return
    x=seq[0]
    for p in parts(seq[1:]):
        yield (frozenset([x]),)+p
        for i in range(len(p)):
            q=list(p); q[i]=q[i]|{x}; yield tuple(q)

def canon(p): return tuple(sorted((tuple(sorted(b)) for b in p), key=lambda b:b[0]))
Ps={canon(p) for p in parts(W)}

def refine(P,E):
    out=[]
    for b in P:
        z=tuple(w for w in b if not ((E>>w)&1))
        o=tuple(w for w in b if ((E>>w)&1))
        if z: out.append(z)
        if o: out.append(o)
    return canon(out)

def measurable(E,P):
    return all(len({(E>>w)&1 for w in b})==1 for b in P)

def defect(P,theta,E):
    F=refine(P,theta)
    touched=[set(b) for b in P if any((E>>w)&1 for w in b)]
    selected=[set(b) for b in F if any((E>>w)&1 for w in b)]
    pull=[set(fb) for fb in F if any(set(fb)<=cb for cb in touched)]
    missing=[fb for fb in pull if fb not in selected]
    return len(missing)

buckets={}; failures=0
for P in Ps:
    for theta in range(16):
        F=refine(P,theta)
        for E in range(16):
            c=measurable(E,P); f=measurable(E,F); d=defect(P,theta,E); z=(d==0)
            buckets[(c,f,z)]=buckets.get((c,f,z),0)+1
            if f and (c!=z): failures+=1
assert failures==0
summary={
  'partitions':len(Ps),'cases':len(Ps)*16*16,'fine_measurable_equivalence_failures':failures,
  'counts':{f'coarse_{c}_fine_{f}_cartesian_{z}':v for (c,f,z),v in sorted(buckets.items())}
}
root=Path(__file__).resolve().parents[1]
(root/'results'/'CARTESIAN_MEASUREMENT_SUMMARY.json').write_text(json.dumps(summary,indent=2))
with (root/'results'/'CARTESIAN_MEASUREMENT_SUMMARY.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['coarse_measurable','fine_measurable','cartesian','count'])
    for (c,fi,z),v in sorted(buckets.items()): w.writerow([c,fi,z,v])
print(json.dumps(summary,indent=2))
