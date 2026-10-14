"""Independent raw-row recount of the frozen v4 primary point and memory endpoints."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent / 'run_v4_001'

def rows(name):
    return [json.loads(line) for line in (ROOT/name).read_text(encoding='utf-8').splitlines() if line]

def main():
    freeze = json.loads((ROOT/'FREEZE.json').read_text(encoding='utf-8'))
    source_root = ROOT.parent.parent
    for relative, identity in freeze['files'].items():
        if relative.endswith(('TIMING.jsonl', 'MEMORY.jsonl', 'FAILURES.jsonl')):
            continue
        path = source_root/relative
        assert sha256(path.read_bytes()).hexdigest() == identity['sha256'], relative
    corpus, timing, memory, failures = (rows(n) for n in ('CORPUS.jsonl','TIMING.jsonl','MEMORY.jsonl','FAILURES.jsonl'))
    assert len(corpus)==64 and len(timing)==3840 and len(memory)==128 and not failures
    groups = defaultdict(list)
    for r in timing:
        assert r['ast_occurrences']==r['unique_object_nodes']==1023
        assert r['root_outcome']=='pure_structural'
        groups[r['case_id'],r['arm']].append(r)
    mem = {(r['case_id'],r['arm']):r for r in memory}
    ratios, increases = [], []
    for c in range(64):
        for arm in ('CM','packed'):
            entries = groups[c,arm]
            assert len(entries)==30 and sorted(x['repetition'] for x in entries)==list(range(30))
            assert all(x['inner_calls']>0 and x['sum_ns']>0 for x in entries)
        packed = statistics.median(x['sum_ns']/x['inner_calls'] for x in groups[c,'packed'])
        cm = statistics.median(x['sum_ns']/x['inner_calls'] for x in groups[c,'CM'])
        ratios.append(packed/cm)
        increases.append(mem[c,'CM']['peak_working_set_bytes']/mem[c,'packed']['peak_working_set_bytes']-1)
    analysis = json.loads((ROOT/'ANALYSIS.json').read_text(encoding='utf-8'))
    assert abs(statistics.median(ratios)-analysis['median_time_ratio_packed_over_cm'])<1e-12
    assert abs(statistics.median(increases)-analysis['median_peak_memory_increase'])<1e-12
    assert analysis['correctness_disagreements']==0 and analysis['primary_success'] is False
    assert analysis['hierarchical_bootstrap_95_interval'][1]<1
    result = {'status':'PASS','cases':64,'timing_rows':3840,'memory_rows':128,'failures':0,
              'raw_median_time_ratio':statistics.median(ratios),
              'raw_median_memory_increase':statistics.median(increases),
              'matches_frozen_analyzer':True,
              'bootstrap_note':'Interval read from frozen analyzer; this recount independently recomputes the point and memory endpoints.'}
    (ROOT.parent/'V4_INDEPENDENT_RECOUNT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
