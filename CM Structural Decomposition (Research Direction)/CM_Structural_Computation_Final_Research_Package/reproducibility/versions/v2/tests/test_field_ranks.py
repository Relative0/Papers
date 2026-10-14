from pathlib import Path
from fractions import Fraction
import json

def rank_real(rows):
    a=[[Fraction(x) for x in row] for row in rows]
    m,n=len(a),len(a[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        pivot=a[r][c]
        for j in range(c,n): a[r][j]/=pivot
        for i in range(r+1,m):
            val=a[i][c]
            if val:
                for j in range(c,n): a[i][j]-=val*a[r][j]
        r+=1
    return r

if __name__=='__main__':
    results=[]
    for r in range(1,6):
        d=1<<r; M=[[(x&y).bit_count()%2 for y in range(d)] for x in range(d)]
        H=[[1-2*v for v in row] for row in M]
        rm,rh=rank_real(M),rank_real(H)
        assert rm==d-1 and rh==d
        results.append({'r':r,'dimension':d,'rank_real_01':rm,'rank_real_sign':rh,
                        'expected_GF2_rank':r,'prototype_classes':d})
    root=Path(__file__).resolve().parents[1]
    (root/'raw_results/field_ranks_v2.json').write_text(json.dumps({'status':'PASS','exact_arithmetic':'fractions.Fraction','cases':results},indent=2)+'\n')
    print(json.dumps(results,indent=2))
