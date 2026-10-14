"""Preregistered complete-case accounting, paired ratios and baseline freeze."""
from pathlib import Path
import csv, hashlib, json, math, random, statistics, sys

ROOT=Path(__file__).resolve().parents[1]
METHODS=['B0','B1','B2','B3','M1','M2','M3','M4','M5','O']
SEEDS=[3101,3102,3103]

def read_split(split):
    manifest=json.loads((ROOT/'data'/'benchmark_manifest.json').read_text())['records']
    ids={r['id'] for r in manifest if r['split']==split}
    path=ROOT/'data'/f'{split}_results.jsonl'
    rows=[json.loads(l) for l in path.read_text().splitlines()]
    expected={(i,m,s) for i in ids for m in METHODS for s in SEEDS}
    observed=[(r['id'],r['method'],r['seed']) for r in rows]
    assert len(observed)==len(set(observed)) and set(observed)==expected, f'Incomplete/duplicate {split}'
    freeze=json.loads((ROOT/'data'/f'{split}_freeze.json').read_text())
    fingerprint=hashlib.sha256(json.dumps(freeze['files'],sort_keys=True).encode()).hexdigest()
    assert all(r['run_fingerprint']==fingerprint for r in rows)
    assert all(r.get('correct') and r.get('semantic_correct') for r in rows if r['status']=='ok')
    return rows

def cost(r):return r['total_seconds'] if r['status']=='ok' else 30.0
def gmean(xs):return math.exp(statistics.mean(math.log(x) for x in xs))
def grouped(rows):
    out={}
    for r in rows:out.setdefault((r['id'],r['method']),[]).append(r)
    return out
def medcost(group):return statistics.median(cost(r) for r in group)
def sats(r,key):return r['exact'].get(key,0)+r.get('probe',{}).get(key,0)
def reduction(method,base):
    if base==0:return 0.0 if method==0 else -math.inf
    return 1-method/base

def select_baseline():
    rows=read_split('validation');groups=grouped(rows)
    scores={m:gmean([medcost(rs) for (i,method),rs in groups.items() if method==m]) for m in ['B2','B3']}
    selected=min(scores,key=lambda m:(scores[m],m))
    x={'selected':selected,'validation_geometric_mean_seconds':scores,
       'validation_sha256':hashlib.sha256((ROOT/'data'/'validation_results.jsonl').read_bytes()).hexdigest(),
       'analysis_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
       'rule':'lower validation geometric mean of per-instance median runtime; PAR2=30 for failures'}
    path=ROOT/'data'/'baseline_selection.json'
    if path.exists():raise SystemExit('Baseline already frozen; refusing overwrite')
    if (ROOT/'data'/'heldout_results.jsonl').exists():raise SystemExit('Heldout exists before baseline freeze')
    path.write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))

def analyze():
    receipts=[json.loads((ROOT/'data'/f'{s}_freeze.json').read_text()) for s in ['train','validation','heldout']]
    assert all(x['files']==receipts[0]['files'] for x in receipts), 'Algorithm/protocol/manifest changed across splits'
    allrows=[r for split in ['train','validation','heldout'] for r in read_split(split)]
    selection=json.loads((ROOT/'data'/'baseline_selection.json').read_text());base=selection['selected']
    assert selection['validation_sha256']==hashlib.sha256((ROOT/'data'/'validation_results.jsonl').read_bytes()).hexdigest()
    assert selection['analysis_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rows=[r for r in allrows if r['split']=='heldout'];groups=grouped(rows)
    ids=sorted({r['id'] for r in rows});summary={};pairs=[]
    for m in METHODS:
        costs=[medcost(groups[i,m]) for i in ids]
        basecost=[medcost(groups[i,base]) for i in ids]
        ratios=[a/b for a,b in zip(costs,basecost)]
        logs=list(map(math.log,ratios));rng=random.Random(2026092907)
        boots=sorted(math.exp(statistics.mean(rng.choices(logs,k=len(logs)))) for _ in range(10000))
        successes=[r for r in rows if r['method']==m and r['status']=='ok']
        calls_reduction=[];wall_reduction=[];wall_saving=[]
        for i,ratio in zip(ids,ratios):
            mg=groups[i,m];bg=groups[i,base]
            complete=all(r['status']=='ok' for r in mg+bg)
            if complete:
                mc=statistics.median(sats(r,'sat_calls') for r in mg);bc=statistics.median(sats(r,'sat_calls') for r in bg)
                mw=statistics.median(sats(r,'sat_seconds') for r in mg);bw=statistics.median(sats(r,'sat_seconds') for r in bg)
                cr=reduction(mc,bc);wr=reduction(mw,bw);saving=bw-mw
            else:mc=bc=mw=bw=None;cr=wr=-math.inf;saving=-math.inf
            calls_reduction.append(cr);wall_reduction.append(wr);wall_saving.append(saving)
            pairs.append({'id':i,'method':m,'baseline':base,'ratio':ratio,'method_median_seconds':medcost(mg),
                          'baseline_median_seconds':medcost(bg),'method_sat_calls':mc,'baseline_sat_calls':bc,
                          'method_sat_seconds':mw,'baseline_sat_seconds':bw,'complete':complete})
        failures=sum(r['status']!='ok' for r in rows if r['method']==m)
        basefail=sum(r['status']!='ok' for r in rows if r['method']==base)
        qs=statistics.quantiles(costs,n=4,method='inclusive')
        sm={'instances':len(ids),'trials':sum(r['method']==m for r in rows),'failures':failures,
            'median_seconds':statistics.median(costs),'mean_seconds':statistics.mean(costs),'iqr_seconds':qs[2]-qs[0],
            'geometric_mean_seconds':gmean(costs),'paired_geometric_ratio':gmean(ratios),
            'paired_ratio_bootstrap_95':[boots[249],boots[9749]],
            'wins':sum(r<1 for r in ratios),'ties':sum(r==1 for r in ratios),'losses':sum(r>1 for r in ratios),
            'median_sat_calls':statistics.median(sats(r,'sat_calls') for r in successes) if successes else None,
            'median_sat_seconds':statistics.median(sats(r,'sat_seconds') for r in successes) if successes else None,
            'median_sdd_size':statistics.median(r['sdd_size'] for r in successes) if successes else None,
            'median_direct_blocks':statistics.median(r['direct_blocks'] for r in successes) if successes else None,
            'median_peak_memory_bytes':statistics.median(r['peak_memory_bytes'] for r in successes) if successes else None,
            'median_sat_call_reduction':statistics.median(calls_reduction),'median_sat_wall_reduction':statistics.median(wall_reduction),
            'median_sat_wall_saving_seconds':statistics.median(wall_saving)}
        sm['pilot_runtime_criterion']=sm['paired_geometric_ratio']<=.90 and boots[9749]<1 and failures<=basefail
        sm['residual_rescue_criterion']=sm['median_sat_call_reduction']>=.25 and sm['median_sat_wall_reduction']>=.10 and sm['median_sat_wall_saving_seconds']>=.005 and failures<=basefail
        summary[m]=sm
    result={'baseline':base,'summary':summary,'total_trials':len(allrows),
            'all_successful_correct':all(r.get('correct') and r.get('semantic_correct') for r in allrows if r['status']=='ok'),
            'total_failures':sum(r['status']!='ok' for r in allrows),
            'primary_pilot_go':summary['M5']['pilot_runtime_criterion'],
            'primary_residual_rescue':summary['M5']['residual_rescue_criterion'],
            'bootstrap_scope':'conditional descriptive instance resampling; related generator shapes are not independent populations'}
    def json_safe(x):
        if isinstance(x,float) and not math.isfinite(x):return '-infinity' if x<0 else 'infinity'
        if isinstance(x,dict):return {k:json_safe(v) for k,v in x.items()}
        if isinstance(x,list):return [json_safe(v) for v in x]
        return x
    (ROOT/'data'/'statistical_summary.json').write_text(json.dumps(json_safe(result),indent=2)+'\n')
    (ROOT/'data'/'paired_heldout_results.json').write_text(json.dumps(pairs,indent=2)+'\n')
    flat=[]
    for r in allrows:
        d={k:r.get(k) for k in ['id','family','split','n','method','seed','status','correct','semantic_correct','total_seconds','process_wall_seconds','sdd_size','sdd_count','direct_blocks','direct_prime_blocks_evaluation','singleton_resolved_fraction','residual_volume','peak_memory_bytes','run_fingerprint']}
        for k in ['sat_calls','sat_seconds','conflicts','decisions','propagations']:
            d[k+'_including_probe']=sats(r,k) if r['status']=='ok' else None
        flat.append(d)
    with (ROOT/'data'/'per_instance_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    with (ROOT/'data'/'paired_heldout_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
    print(json.dumps(json_safe(result),indent=2))

if __name__=='__main__':
    select_baseline() if sys.argv[1]=='select' else analyze()
