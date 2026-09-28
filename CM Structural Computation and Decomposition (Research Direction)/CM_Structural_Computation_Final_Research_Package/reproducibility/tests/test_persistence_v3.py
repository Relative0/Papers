"""Persistent-state boundary tests; exact tiny counterexamples, not priority claims."""
from pathlib import Path
from itertools import product
from collections import Counter
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from artifacts import Artifact,discover,xor_artifact
from checker import verify,independent_rank
from codec import dumps_binary,loads_binary
from baselines import PackedTruth,ReferenceBDD
from test_core import reference_restrict

def run():
    start=time.perf_counter(); count=Counter()
    for n in range(4):
        for truth in range(1<<(1<<n)):
            a,_=discover(truth,n,8,encoding='binary')
            blob=dumps_binary(a); loaded=loads_binary(blob)
            p=PackedTruth.loads(PackedTruth(truth,n).dumps())
            b=ReferenceBDD.loads(ReferenceBDD(truth,n).dumps())
            assert verify(loaded,truth) and b.verify(truth) and p.truth==truth
            count['fresh_three_backend_roundtrips']+=1
            for values in product((-1,0,1),repeat=n):
                rho={i:v for i,v in enumerate(values) if v!=-1}
                expected=reference_restrict(truth,n,rho).bit_count()
                assert loaded.query_fused(rho)==p.query(rho)==b.query(rho)==expected
                count['fresh_instance_query_triples']+=1
    scope=[0,1]; payload=[[0],[1],[0,1],[2]]
    a=Artifact('rank',scope,payload); before=a.dumps()
    scope[0]=9; payload[0][0]=9; payload[2][1]=0; payload[3][0]=0
    assert a.dumps()==before and verify(a,8)
    count['caller_alias_mutation_checks']+=1
    for kind,scope,p in [('flat',[0,0],[0]),('flat',[True],[0]),('flat',[0],{'truth':0}),('x',[0],[0])]:
        try:Artifact(kind,scope,p)
        except (ValueError,TypeError):count['constructor_rejections']+=1
        else:raise AssertionError('invalid constructor accepted')
    bad_json=[b'{"schema":"sc-reference/v1","schema":"sc-reference/v1","kind":"flat","scope":[],"payload":[0]}',
              b'{"schema":"sc-reference/v1","kind":"flat","scope":[],"payload":[2]}',
              b'{"schema":"sc-reference/v1","kind":"rank","scope":[0,1],"payload":[[0],[1],[0],[2]]}']
    for blob in bad_json:
        try:Artifact.loads(blob)
        except (ValueError,TypeError):count['json_structure_rejections']+=1
        else:raise AssertionError('bad JSON accepted')
    valid=dumps_binary(Artifact('flat',(0,),(2,)))
    for blob in [valid+b'\x00',b'XX'+valid[2:],valid[:2],valid[:-1]]:
        try:loads_binary(blob)
        except (ValueError,TypeError):count['binary_structure_rejections']+=1
        else:raise AssertionError('bad binary accepted')
    try:dumps_binary(Artifact('flat',(16,),(2,)))
    except ValueError:count['codec_label_policy_rejections']+=1
    else:raise AssertionError('unsupported label')
    # A residual scope does not accept a second assignment to an already removed variable.
    a=Artifact('flat',(0,1),(8,)).condition({0:0})
    for rho in ({0:0},{1:2},{1:True}):
        try:a.condition(rho)
        except ValueError:count['residual_assignment_rejections']+=1
        else:raise AssertionError('invalid residual assignment')
    # Same coefficient/column-profile histograms, different named-variable restriction.
    f=Artifact('rank',(0,1),((0,),(1,),(0,1),(2,)))
    g=Artifact('rank',(0,1),((0,),(1,),(1,0),(2,)))
    assert verify(f,8) and verify(g,2) and f.count()==g.count()==1
    assert Counter(f.payload[2])==Counter(g.payload[2])
    assert f.query_fused({0:0})==0 and g.query_fused({0:0})==1
    hist={'f':'x*y','g':'(1-x)*y','f_truth_hex':'0x8','g_truth_hex':'0x2',
          'coefficient_histogram':{'0':1,'1':1},'column_profile_histogram':{'0':1,'1':1},
          'unconditional_counts':[1,1],'counts_given_x_0':[0,1]}
    # Rediscovery can split a stored component after conditioning.
    truth=0
    for i in range(8):
        x,y,z=(i>>2)&1,(i>>1)&1,i&1
        truth|=((x*y*z)^x^y)<<i
    original=xor_artifact(truth,(0,1,2)); residual=original.condition({2:0})
    expected=reference_restrict(truth,3,{2:0})
    rediscovered=xor_artifact(expected,(0,1))
    assert verify(residual,expected) and verify(rediscovered,expected)
    assert len(original.payload[1])==len(residual.payload[1])==1 and len(rediscovered.payload[1])==2
    split={'formula':'x*y*z XOR x XOR y','truth_hex':hex(truth),'restriction':{'z':0},
           'residual_formula':'x XOR y','original_factor_count':1,'retained_factor_count':1,'rediscovered_factor_count':2}
    # Every fixed-cut zero matrix and every one-spike matrix have binary rank <=1.
    for n in range(1,9):
        left=n//2; C=1<<(n-left); R=1<<left
        for a in range(1<<n):
            rows=[0]*R; rows[a//C]=1<<(a%C)
            assert independent_rank(tuple(rows))==1
            count['single_spike_rank_checks']+=1
    count['explicit_histogram_counterexamples']+=1
    count['explicit_factor_refinement_counterexamples']+=1
    return {'status':'PASS','counts':dict(count),'histogram_counterexample':hist,
            'factor_refinement_counterexample':split,'elapsed_seconds':time.perf_counter()-start}

if __name__=='__main__':
    out=run();root=Path(__file__).resolve().parents[1]
    (root/'raw_results/persistence_v3.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
