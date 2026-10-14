#!/usr/bin/env python3
"""Exhaustive sanity checks for the pure Horn/dual-Horn refined-signature regime.

Enumerates every nonempty Boolean relation R subseteq {0,1}^d for d<=4,
selects meet-closed (Horn) and join-closed (dual-Horn) relations, and checks that
both R and its coordinate projection have a least/greatest element respectively.
This gives an elementary contractibility certificate for their order complexes.
"""
from itertools import product
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent

def meet(x,y): return tuple(a&b for a,b in zip(x,y))
def join(x,y): return tuple(a|b for a,b in zip(x,y))
def is_closed(R,op):
    S=set(R)
    return all(op(x,y) in S for x in R for y in R)
def min_element(R):
    if not R: return None
    m=R[0]
    for x in R[1:]: m=meet(m,x)
    return m if m in set(R) else None
def max_element(R):
    if not R: return None
    m=R[0]
    for x in R[1:]: m=join(m,x)
    return m if m in set(R) else None

def main():
    rows=[]
    for d in range(1,5):
        U=list(product((0,1),repeat=d)); total=(1<<len(U))-1
        horn=dual=0; hfail=dfail=0
        for mask in range(1,1<<len(U)):
            R=[U[i] for i in range(len(U)) if mask>>i & 1]
            if is_closed(R,meet):
                horn+=1
                P=sorted(set(x[:-1] for x in R)) if d>1 else [()]
                if min_element(R) is None or min_element(P) is None: hfail+=1
            if is_closed(R,join):
                dual+=1
                P=sorted(set(x[:-1] for x in R)) if d>1 else [()]
                if max_element(R) is None or max_element(P) is None: dfail+=1
        rows.append({'dimension':d,'nonempty_relations':total,'meet_closed':horn,
                     'join_closed':dual,'horn_minimum_failures':hfail,'dual_horn_maximum_failures':dfail})
    out={'cases':rows}
    (OUT/'boolean_horn_verification.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
