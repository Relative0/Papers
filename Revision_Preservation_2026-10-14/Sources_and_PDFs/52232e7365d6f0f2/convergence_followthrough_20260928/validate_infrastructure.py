"""Exhaustive small endpoint checks and natural-source cross-checks."""
from pathlib import Path
import argparse, itertools, json, sys
from backends import METHODS, Packed, make
from lifecycle import scalar_count, queries

ROOT=Path(__file__).resolve().parent

def main(output,cudd):
    output.mkdir(parents=True,exist_ok=False)
    methods=['packed_binary','coordinate_rank_baseline']+(['cudd_fixed_order_binary'] if cudd else [])
    counts={m:0 for m in methods};roundtrips=0;rejections=0
    for n in range(4):
        scope=tuple(range(n));left=scope[:n//2]
        for f in range(1<<(1<<n)):
            for m in methods:
                obj=make(m,f,n,left);obj.index();blob=obj.dumps();obj=METHODS[m].loads(blob);obj.index();roundtrips+=1
                try:METHODS[m].loads(blob+b'\x00')
                except (ValueError,AssertionError):rejections+=1
                else:raise AssertionError((m,'accepted trailing data'))
                for values in itertools.product((None,0,1),repeat=n):
                    rho={v:b for v,b in enumerate(values) if b is not None};want=scalar_count(f,n,rho)
                    assert obj.query(rho)==want
                    residual=obj.condition(rho);residual.index();assert residual.query({})==want
                    residual=METHODS[m].loads(residual.dumps());residual.index();assert residual.query({})==want
                    counts[m]+=1
    # The query grid must execute requested batches and obey per-episode budgets.
    for n in range(7):
        for k in sorted({min(n,j) for j in (0,1,2,4,n)}):
            for q in (1,8,64,256):
                for sem in ('independent','sequential_cumulative'):
                    rows=queries(n,k,q,sem,20260928);assert len(rows)==q
                    assert all(len(r['restriction'])<=k for r in rows)
                    if sem=='independent':assert all(len(r['restriction'])==k for r in rows)
                    else:
                        episodes={}
                        for row in rows:
                            seen=episodes.setdefault(row['episode'],{})
                            assert not set(seen)&row['delta'].keys();seen.update(row['delta']);assert seen==row['restriction']
    result={'status':'PASS','query_checks_per_backend':counts,'binary_roundtrips':roundtrips,'trailing_byte_rejections':rejections,
        'coverage':'every Boolean function n=0..3; every restriction; original/residual/reloaded residual; batch generator n=0..6'}
    (output/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--cudd',action='store_true');a=p.parse_args();main(a.output,a.cudd)
