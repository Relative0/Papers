from pathlib import Path
import sys,json,random,time
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from artifacts import Artifact, factor_candidates, rank_factor, cofactor_payload, walsh_count, recompress_rank
from checker import verify, independent_rank, minimal_rank_witness
from codec import dumps_binary, loads_binary
from test_core import reference_restrict

def run():
    t=time.perf_counter(); stats=Counter(); distribution=Counter()
    for truth in range(1<<16):
        rows=tuple((truth>>(4*i))&15 for i in range(4))
        coef,basis=rank_factor(rows); r=len(basis)
        assert independent_rank(rows)==r
        delta=int(independent_rank(rows+(15,))==r)
        protos,refs=cofactor_payload(rows,4); k=len(protos)
        assert r<=k+delta and k<=min(4,1<<(r-delta))
        a=Artifact('rank',(0,1,2,3),((0,1),(2,3),coef,basis))
        assert a.count()==walsh_count(a)==truth.bit_count()
        assert minimal_rank_witness(a)
        stats['matrices_4x4']+=1; distribution[(r,delta,k)]+=1
    rng=random.Random(2026092622)
    for n in (4,6,8,10,12):
        left=tuple(range(n//2)); right=tuple(range(n//2,n)); R,C=1<<len(left),1<<len(right)
        for case in range(10):
            rank=min(5,R,C); coef=tuple(rng.randrange(1<<rank) for _ in range(R)); basis=tuple(rng.getrandbits(C) for _ in range(rank))
            a=Artifact('rank',tuple(range(n)),(left,right,coef,basis))
            truth=0
            for x in range(R):
                for y in range(C):
                    val=sum(((coef[x]>>j)&1)*((basis[j]>>y)&1) for j in range(rank))%2
                    truth|=val<<(x*C+y)
            assert verify(a,truth)
            other=list(factor_candidates(truth,tuple(range(n)),left))
            for item in [a]+other:
                binary=dumps_binary(item); restored=loads_binary(binary)
                assert verify(restored,truth)
                assert restored.count()==truth.bit_count()
                stats['binary_roundtrips']+=1
                try: loads_binary(binary+b'\x00')
                except ValueError: stats['trailing_data_rejections']+=1
                else: raise AssertionError('noncanonical trailing data accepted')
                for repeat in range(20):
                    rho={j:rng.randrange(2) for j in range(n) if rng.random()<0.5}
                    r1={j:b for j,b in rho.items() if j%2==0}; r2={j:b for j,b in rho.items() if j%2}
                    expected=reference_restrict(truth,n,rho)
                    combined=item.condition(rho); sequential=item.condition(r1).condition(r2)
                    assert verify(combined,expected) and verify(sequential,expected)
                    assert combined.count()==sequential.count()==item.query_fused(rho)==expected.bit_count()
                    assert verify(loads_binary(dumps_binary(combined)),expected)
                    stats['sequential_fused_condition_checks']+=1
                    if item.kind=='rank':
                        minimal=recompress_rank(combined)
                        assert verify(minimal,expected) and minimal_rank_witness(minimal)
                        assert minimal.count()==walsh_count(minimal)==expected.bit_count()
                        stats['recompression_checks']+=1
    result={'status':'PASS','counts':dict(stats),'quotient_distribution':[
        {'rank':r,'delta':d,'prototype_classes':k,'matrices':count} for (r,d,k),count in sorted(distribution.items())],
        'elapsed_seconds':time.perf_counter()-t}
    return result

if __name__=='__main__':
    out=run(); root=Path(__file__).resolve().parents[1]
    (root/'raw_results/extensions_v2.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='quotient_distribution'},indent=2))
