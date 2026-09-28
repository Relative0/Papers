"""Direct in-memory persistence replay. Protocol v3; all source instances discarded."""
from pathlib import Path
import json,hashlib,time,statistics,sys,platform,random
from artifacts import discover
from checker import verify
from codec import dumps_binary,loads_binary
from baselines import PackedTruth,ReferenceBDD
ROOT=Path(__file__).resolve().parents[1]
def timed(fn):
    t=time.perf_counter_ns();result=fn();return result,time.perf_counter_ns()-t

def trial(method,truth,n,queries):
    start=time.perf_counter_ns()
    rec={}
    if method=='artifact':
        (obj,candidates),rec['compile_ns']=timed(lambda:discover(truth,n,16,encoding='binary'))
        del candidates
        valid,rec['verify_before_ns']=timed(lambda:obj.payload[0]==truth if obj.kind=='flat' else verify(obj,truth))
        assert valid
        blob,rec['serialize_ns']=timed(lambda:dumps_binary(obj))
        kind=obj.kind
        del obj
        obj,rec['load_ns']=timed(lambda:loads_binary(blob))
        valid,rec['verify_after_ns']=timed(lambda:obj.payload[0]==truth if obj.kind=='flat' else verify(obj,truth))
        assert valid
        if obj.kind=='flat':
            helper,rec['query_index_ns']=timed(lambda:PackedTruth(obj.payload[0],n))
            query=helper.query
        else:
            rec['query_index_ns']=0;query=obj.query_fused
    elif method=='packed':
        obj,rec['compile_ns']=timed(lambda:PackedTruth(truth,n))
        rec['verify_before_ns']=0
        blob,rec['serialize_ns']=timed(obj.dumps)
        del obj
        obj,rec['load_ns']=timed(lambda:PackedTruth.loads(blob))
        valid,rec['verify_after_ns']=timed(lambda:obj.truth==truth and obj.n==n)
        assert valid
        rec['query_index_ns']=0;query=obj.query;kind='packed'
    else:
        obj,rec['compile_ns']=timed(lambda:ReferenceBDD(truth,n))
        valid,rec['verify_before_ns']=timed(lambda:obj.verify(truth));assert valid
        blob,rec['serialize_ns']=timed(obj.dumps)
        del obj
        obj,rec['load_ns']=timed(lambda:ReferenceBDD.loads(blob))
        valid,rec['verify_after_ns']=timed(lambda:obj.verify(truth));assert valid
        rec['query_index_ns']=0;query=obj.query;kind='reference_robdd'
    answers,rec['batch_ns']=timed(lambda:[query(rho) for rho in queries])
    rec['complete_elapsed_ns']=time.perf_counter_ns()-start
    rec['query_count']=len(queries);rec['serialized_bytes']=len(blob);rec['kind']=kind
    return answers,rec

def run(start_index=0,end_index=38):
    cases=json.loads((ROOT/'data/cases.json').read_text())
    path=ROOT/'raw_results/benchmark_v3_replay.json'
    out=json.loads(path.read_text()) if path.exists() else []
    assert start_index==len(out),'Continuation must follow the recorded prefix exactly'
    for i in range(start_index,min(end_index,len(cases))):
        case=cases[i];n=case['n'];truth=int(case['truth_hex'],16)
        rng=random.Random(202609260000+i)
        queries=[{j:rng.randrange(2) for j in range(n) if rng.random()<0.5} for _ in range(128)]
        oracle=PackedTruth(truth,n);answers=[oracle.query(q) for q in queries]
        records={k:[] for k in ('artifact','packed','reference_robdd')}
        for rep in range(5):
            order=list(records);offset=rep%3;order=order[offset:]+order[:offset]
            for method in order:
                result,rec=trial(method,truth,n,queries)
                assert result==answers,(case['id'],method,rep)
                rec['rep']=rep;records[method].append(rec)
        medians={k:statistics.median([r['complete_elapsed_ns'] for r in rs]) for k,rs in records.items()}
        item={**case,'timings':records,'median_complete_elapsed_ns':medians,
              'artifact_better_than_packed':medians['artifact']<medians['packed'],
              'query_batch_sha256':hashlib.sha256(json.dumps(queries,sort_keys=True).encode()).hexdigest()}
        out.append(item);path.write_text(json.dumps(out,indent=2)+'\n')
        print(f"{i+1}/38 {case['id']} kind={records['artifact'][0]['kind']} replay_ratio={medians['artifact']/medians['packed']:.2f}",flush=True)
    env={'python':sys.version,'platform':platform.platform(),'clock':str(time.get_clock_info('perf_counter')),
         'dataset_sha256':hashlib.sha256((ROOT/'data/cases.json').read_bytes()).hexdigest(),
         'protocol_sha256':hashlib.sha256((ROOT.parent/'research/experiment_design/PROTOCOL_V3_REPLAY.json').read_bytes()).hexdigest(),
         'completed':len(out),'dependencies':'Python standard library only','full_query_batch_executed':128}
    (ROOT/'environment/environment_v3_replay.json').write_text(json.dumps(env,indent=2)+'\n')
    return out
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 0,int(sys.argv[2]) if len(sys.argv)>2 else 38)
