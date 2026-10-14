"""Reproducible small exact-count benchmark. See the frozen research protocol."""
from __future__ import annotations
from pathlib import Path
import gc, hashlib, json, math, platform, random, statistics, sys, time
from collections import Counter
from artifacts import Artifact, discover
from checker import verify
from codec import dumps_binary, loads_binary
from baselines import PackedTruth, ReferenceBDD

ROOT = Path(__file__).resolve().parents[1]

def timed(operation):
    start = time.perf_counter_ns()
    value = operation()
    return value, time.perf_counter_ns()-start

def median(values): return statistics.median(values)

def run(label='v1', fused=False, encoding='json'):
    dataset = json.loads((ROOT/'data'/'cases.json').read_text())
    existing = ROOT/'raw_results'/f'benchmark_{label}.json'
    output = json.loads(existing.read_text()) if '--resume' in sys.argv and existing.exists() else []
    completed = len(output)
    allqueries = {}
    for index, case in enumerate(dataset):
        n, truth = case['n'], int(case['truth_hex'],16)
        rng = random.Random(202609260000+index)
        queries = [{j:rng.randrange(2) for j in range(n) if rng.random()<0.5} for _ in range(128)]
        allqueries[case['id']] = queries
        if index < completed:
            assert output[index]['id'] == case['id']
            continue
        oracle = PackedTruth(truth,n)
        answers = [oracle.query(q) for q in queries]
        records = {'artifact':[], 'packed':[], 'robdd':[]}
        best, allc = discover(truth,n,16,encoding=encoding)
        # Validate every candidate separately outside measured selection trials.
        for a in allc:
            assert verify(a,truth), (case['id'],a)
        families = {}
        for kind in sorted({a.kind for a in allc}):
            pool = [a for a in allc if a.kind==kind]
            a = min(pool,key=lambda a:(len(a.dumps()),a.ideal_bits(),a.dumps()))
            families[kind] = {'json_bytes':len(a.dumps()),'ideal_bits':a.ideal_bits(),
                              'minimum_binary_bytes':min(len(dumps_binary(x)) for x in pool),
                              'minimum_ideal_bits':min(x.ideal_bits() for x in pool)}
        for rep in range(5):
            # Rotate method order by repetition, avoiding a fixed first-method slot.
            methods = ('artifact','packed','robdd')
            methods = methods[rep%3:] + methods[:rep%3]
            for method in methods:
                if method == 'artifact':
                    (a,_), compile_ns = timed(lambda:discover(truth,n,16,encoding=encoding))
                    valid, verify_ns = timed(lambda:(a.payload[0]==truth if a.kind=='flat' else verify(a,truth)))
                    assert valid
                    blob, serialize_ns = timed(lambda:dumps_binary(a) if encoding=='binary' else a.dumps())
                    loaded, load_ns = timed(lambda:loads_binary(blob) if encoding=='binary' else Artifact.loads(blob))
                    if a.kind=='flat':
                        helper, extra_ns = timed(lambda:PackedTruth(truth,n))
                        compile_ns += extra_ns
                        query = helper.query
                    else:
                        query = loaded.query_fused if fused else loaded.query
                    assert [query(q) for q in queries] == answers
                    # One untimed warm batch, then measured batch.
                    results, batch_ns = timed(lambda:[query(q) for q in queries])
                    assert results == answers
                elif method == 'packed':
                    helper, compile_ns = timed(lambda:PackedTruth(truth,n))
                    # No representation-change certificate: source bits are the input.
                    verify_ns = 0
                    blob, serialize_ns = timed(helper.dumps)
                    decoded, load_ns = timed(lambda:json.loads(blob))
                    assert decoded['truth']==truth
                    query = helper.query
                    assert [query(q) for q in queries] == answers
                    results,batch_ns = timed(lambda:[query(q) for q in queries])
                    assert results==answers
                else:
                    helper,compile_ns = timed(lambda:ReferenceBDD(truth,n))
                    valid,verify_ns = timed(lambda:helper.verify(truth))
                    assert valid
                    blob,serialize_ns = timed(helper.dumps)
                    decoded,load_ns = timed(lambda:json.loads(blob))
                    assert decoded['root']==helper.root
                    query=helper.query
                    assert [query(q) for q in queries]==answers
                    results,batch_ns=timed(lambda:[query(q) for q in queries])
                    assert results==answers
                records[method].append({'rep':rep,'compile_ns':compile_ns,'verify_ns':verify_ns,
                                        'serialize_ns':serialize_ns,'load_ns':load_ns,
                                        'query_batch_ns':batch_ns,'query_count':len(queries),
                                        'json_bytes':len(blob)})
        item={**case,'selected_kind':best.kind,'selected_json_bytes':len(best.dumps()),
              'selection_encoding':encoding,'selected_binary_bytes':len(dumps_binary(best)),
              'selected_ideal_bits':best.ideal_bits(), 'raw_truth_payload_bytes':max(1,math.ceil((1<<n)/8)),
              'families':families,'candidates':len(allc),'timings':records,'summary':{}}
        for method,recs in records.items():
            setup=median([sum(r[k] for k in ('compile_ns','verify_ns','serialize_ns','load_ns')) for r in recs])
            perquery=median([r['query_batch_ns']/r['query_count'] for r in recs])
            item['summary'][method]={'setup_ns':setup,'query_ns':perquery,
                'lifecycle_ns':{str(q):setup+q*perquery for q in (1,10,100,1000)}}
        art,flat=item['summary']['artifact'],item['summary']['packed']
        gain=flat['query_ns']-art['query_ns']
        item['estimated_break_even_vs_packed']=max(0,math.ceil((art['setup_ns']-flat['setup_ns'])/gain)) if gain>0 else None
        output.append(item)
        (ROOT/'raw_results'/f'benchmark_{label}.json').write_text(json.dumps(output,indent=2)+'\n')
        print(f"{index+1:02d}/{len(dataset)} {case['id']} n={n} {best.kind} ratio={art['query_ns']/flat['query_ns']:.2f}",flush=True)
    (ROOT/'data'/f'queries_{label}.json').write_text(json.dumps(allqueries,indent=2)+'\n')
    environment={'python':sys.version,'platform':platform.platform(),'clock':str(time.get_clock_info('perf_counter')),
                 'label':label,'fused':fused,'selection_encoding':encoding,'dependencies':'Python standard library only',
                 'dataset_sha256':hashlib.sha256((ROOT/'data'/'cases.json').read_bytes()).hexdigest()}
    (ROOT/'environment'/f'environment_{label}.json').write_text(json.dumps(environment,indent=2)+'\n')
    return output

if __name__=='__main__':
    label=sys.argv[1] if len(sys.argv)>1 else 'v1'
    run(label, '--fused' in sys.argv, 'binary' if '--binary' in sys.argv else 'json')
