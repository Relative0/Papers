"""Read-only audit of completed P14, no new timings or holdout generation."""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,math,random,statistics,time,shutil,sys
O=Path(__file__).resolve().parent; A=Path(r'C:\Users\brian\Documents\CM_Computation\audit_p1_p13_20260918');P=A/'p14_py0'; D=O/'evidence/p14_reconciliation';D.mkdir(exist_ok=True)
start=time.monotonic(); manifest=json.loads((P/'P14_ARTIFACT_MANIFEST.json').read_text()); checks={}
for rel,record in manifest['files'].items():
    p=(P/rel).resolve();assert p.is_relative_to(P.resolve())
    checks[rel]=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'] and p.stat().st_size==record['bytes']
assert all(checks.values()),[k for k,v in checks.items() if not v]
rows=[]; raw_metadata=[]
for p in sorted(P.glob('timing_s*_w*.json')):
    d=json.loads(p.read_text());rows+=d['rows'];raw_metadata.append({k:v for k,v in d.items() if k!='rows'})
expected=json.loads((P/'P14_RESULTS.json').read_text());groups=defaultdict(list); workers=defaultdict(lambda:defaultdict(list));families={}
for r in rows:
    k=(r['corpus'],r['endpoint'],r['case_id'],r['arm']);groups[k].append(r['per_compile_ns']);workers[k][(r['session'],r['worker'])].append(r['per_compile_ns']);families[(r['corpus'],r['case_id'])]=r['family']
med={k:statistics.median(v) for k,v in groups.items()}; wm={k:{w:statistics.median(v) for w,v in d.items()} for k,d in workers.items()}
out=[]
def quantile(v,p):
    x=(len(v)-1)*p;i=int(x);f=x-i;return v[i]*(1-f)+v[min(i+1,len(v)-1)]*f
for e in expected['comparisons']+expected['secondary_ir']:
    corpus=e['corpus']; endpoint=e['endpoint'];a,b=e['comparison'].split('/');cases=sorted(e['case_ratios']);ratios=[med[corpus,endpoint,c,a]/med[corpus,endpoint,c,b] for c in cases]
    geo=math.exp(statistics.mean(map(math.log,ratios)));assert abs(geo-e['geomean'])<1e-12
    assert all(abs(r-e['case_ratios'][c])<1e-12 for c,r in zip(cases,ratios))
    entry={'corpus':corpus,'endpoint':endpoint,'comparison':e['comparison'],'cases':len(cases),'geomean':geo,'all_case_ratios_match':True}
    if endpoint=='recipe' and corpus in ('synthetic','natural') and (a,b) in [('E','F'),('E','D')]:
        fg=defaultdict(list);wmratio={}
        for c in cases:
            fg[families[corpus,c]].append(c);wkeys=sorted(wm[corpus,endpoint,c,a]);wmratio[c]=[math.log(wm[corpus,endpoint,c,a][w]/wm[corpus,endpoint,c,b][w]) for w in wkeys]
        rng=random.Random(2026091902 ^ sum(map(ord,corpus+a+b)));fams=sorted(fg);draws=[]
        for _ in range(10000):
            sf=[rng.choice(fams) for _ in fams];logs=[]
            for family in sf:
                fc=fg[family]
                for _ in fc:
                    c=rng.choice(fc);logs.append(rng.choice(wmratio[c]))
            draws.append(math.exp(statistics.mean(logs)))
        draws.sort();ci=[quantile(draws,.00625),quantile(draws,.99375)];assert max(abs(x-y) for x,y in zip(ci,e['ci98_75']))<1e-12
        entry['ci98_75']=ci;entry['bootstrap_reproduced']=True
    out.append(entry)
copy_names=['P14_ARTIFACT_MANIFEST.json','P14_FREEZE.json','P14_FREEZE_V1_ORIGINAL.json','P14_BUDGET_EXTENSION.json','P14_ANALYSIS_EXECUTION_AMENDMENT.json','P14_EXECUTION_REPORT.md','P14_RESULTS.json','P14_CASE_RATIOS.csv','P14_MEMORY_SUMMARY.json','correctness_results.json','analyze_p14.py','analyze_p14_optimized.py','run_timing.py','p14_common.py','freeze_p14.py']
for name in copy_names:shutil.copy2(P/name,D/name)
for name in ['P15_LATE_SCAN_IMPLEMENTATION_REVIEW_20260919.md','P15_EXPOSED_CORRECTNESS_RESULTS.json']:shutil.copy2(A/'p15_py0_dev'/name,D/name)
result={'scope':'Existing completed P14 records; fresh arithmetic/manifest verification, not a new timing campaign','command':sys.argv,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'manifest_verified':checks,'raw_rows':len(rows),'raw_metadata':raw_metadata,'comparisons':out,'seconds':time.monotonic()-start,'bootstrap_seed':2026091902,'bootstrap_draws':10000,'memory_scope':'Inherited separate tracemalloc pass, not RSS; no new memory samples','source_root':str(P)}
(D/'RECONCILIATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'files_verified':len(checks),'raw_rows':len(rows),'comparisons':len(out),'primary_intervals_reproduced':4,'seconds':result['seconds']},indent=2))
