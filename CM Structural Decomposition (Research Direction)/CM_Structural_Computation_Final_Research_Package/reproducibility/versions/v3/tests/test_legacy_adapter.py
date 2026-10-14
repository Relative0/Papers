from pathlib import Path
import sys,json,random,time,argparse
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from legacy_adapter import adapt
from baselines import PackedTruth
from codec import dumps_binary,loads_binary
from checker import verify

def run(source):
    sys.path.insert(0,str(source))
    from cmbench.recognition.gf2_decomposition import analyze_exact_gf2
    stats=Counter(); rng=random.Random(2026092623)
    for case in json.loads((ROOT/'data/cases.json').read_text()):
        n=case['n']; truth=int(case['truth_hex'],16)
        if not 2<=n<=10: continue
        analysis=analyze_exact_gf2(truth,n,max_partitions=16)
        oracle=PackedTruth(truth,n)
        for old in analysis.candidates:
            assert old.reconstruct()==truth
            a=adapt(old.to_dict(),truth)
            assert verify(loads_binary(dumps_binary(a)),truth)
            stats[old.kind]+=1
            for repeat in range(10):
                rho={j:rng.randrange(2) for j in range(n) if rng.random()<0.5}
                assert a.query(rho)==a.query_fused(rho)==oracle.query(rho)
                stats['queries']+=1
    assert all(stats[k]>0 for k in ('xor_components','gf2_rank','cofactor_blocks','kronecker'))
    return {'status':'PASS','counts':dict(stats),'scope':'At most 16 partitions, 2<=n<=10 cases in the shared dataset, not exhaustive legacy testing'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);args=p.parse_args()
    out=run(args.source);(ROOT/'raw_results/legacy_adapter_v2.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
