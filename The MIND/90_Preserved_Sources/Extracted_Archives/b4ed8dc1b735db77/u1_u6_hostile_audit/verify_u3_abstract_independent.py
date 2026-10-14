#!/usr/bin/env python3
from itertools import product
import json

# Generate naturally labelled posets on n <= 4 as transitively closed relations with i<=j labels.
def posets_n(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    out=[]
    for bits in product((0,1), repeat=len(pairs)):
        R={(i,i) for i in range(n)} | {p for p,b in zip(pairs,bits) if b}
        ok=True
        for i,j in list(R):
            for a,k in list(R):
                if a==j and (i,k) not in R:
                    ok=False; break
            if not ok: break
        if ok: out.append(R)
    return out

# Nonempty subposets B of 2-chain {0<1}: {0},{1},{0,1}
fiber_options=((0,),(1,),(0,1))

def leB(a,b): return a<=b

cases=0; fail=0
for n in range(1,5):
  for P in posets_n(n):
    for fibers in product(fiber_options, repeat=n):
      verts=[(p,a) for p in range(n) for a in fibers[p]]
      F=set(); Q=set()
      for x in verts:
        for y in verts:
          p,a=x; q,b=y
          if p==q:
            lf=leB(a,b)
          elif (p,q) in P and p!=q:
            lf=True
          else:
            lf=False
          if lf: F.add((x,y))
          if (p,q) in P and leB(a,b): Q.add((x,y))
      cases+=1
      if not Q <= F:
        fail+=1; continue
      # projection monotone & surjective
      if set(p for p,a in verts) != set(range(n)):
        fail+=1; continue
      if any((x,y) in F and (x[0],y[0]) not in P for x,y in F):
        fail+=1

out={'cases':cases,'failures':fail,'n_max':4}
with open('/mnt/data/u1_u6_hostile_audit/U3_ABSTRACT_INDEPENDENT_SUMMARY.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
