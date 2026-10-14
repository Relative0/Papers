#!/usr/bin/env python3
from itertools import combinations
from pathlib import Path
import json, importlib.util
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('v',P/'verify_matching_inversion_theorem.py'); v=importlib.util.module_from_spec(sp); sp.loader.exec_module(v)

def ideals_of_poset(le):
    n=len(le); ideals=[]
    for mask in range(1<<n):
        S={i for i in range(n) if mask>>i & 1}
        ok=True
        for x in list(S):
            for y in range(n):
                if le[y][x] and y not in S: ok=False; break
            if not ok: break
        if ok: ideals.append(frozenset(S))
    ideals.sort(key=lambda s:(len(s),tuple(sorted(s))))
    m=len(ideals); L=[[False]*m for _ in range(m)]
    for i,a in enumerate(ideals):
        for j,b in enumerate(ideals): L[i][j]=a<=b
    return ideals,L

def main():
    out=[]; failures=[]
    for rn in range(1,4):
        for pid,R in enumerate(v.natural_posets(rn)):
            ideals,L=ideals_of_poset(R); n=len(L)
            av=[2]*n; av[0]=1; av[-1]=0
            actual=v.relative_pair_Z(L,tuple(av)); pred=v.matching_formula_Z(L,tuple(av))
            antichain=all(not v.strict(R,i,j) for i in range(rn) for j in range(rn))
            expected={rn:{'free':1,'torsion':[]}} if antichain and rn>=1 else {}
            row={'generating_poset_n':rn,'poset_id':pid,'lattice_size':n,'generator_antichain':antichain,
                 'actual_Z':actual,'pred_Z':pred,'expected_distributive':expected}
            out.append(row)
            if actual!=pred or actual!=expected: failures.append(row)
    data={'cases':len(out),'failures':len(failures),'rows':out}
    (P/'distributive_verification.json').write_text(json.dumps(data,indent=2,sort_keys=True))
    print(json.dumps({'cases':len(out),'failures':len(failures)},indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
