#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
DIRECT='direct_sparse_anf'; P3='cm_demand_profit_sparse'; P2='cm_inline_profit_sparse'
EXPECTED_PREREG='d37fc5b385f8d36f1b4e863dcc6112ba035513bfa4d8a43b78b96e54d383a47b'
EXPECTED_HARNESS='8b9a74cc952d53ed69b278091e9d36472a35d78d24806c0861cb7a2e8fc255c6'
EXPECTED_BLOBS={
 'adder_size_2022.blif':'1a16f1fea72e7fbf67aac019ec97c6aaf871fcdd',
 'bar_size_2015.blif':'a2b2177aa0be92ac60f5c694bcf6eb9806aaa9c2',
 'cavlc_size_2024.blif':'3ebfd39f6193da20b2ae0491dd41bc18eeffce3e',
 'int2float_size_2025.blif':'5c202a31a74dc2b4da0d1ac59377e92c6c37c6d9',
 'priority_size_2024.blif':'4156ea7455044d0a9a49855cca5876ffaa8a003b',
 'router_size_2024.blif':'553e80bc24de67a307b4ce7aafef8adb9603ad26',
}
EXPECTED_CASES=[
 'adder:f[4]','adder:f[5]','cavlc:17','cavlc:35','int2float:e4','int2float:y6',
 'priority:new_n130','priority:new_n174','router:105','router:92']
IDENTITY_FIELDS=['digest','output_unique_nodes','multiplications','pair_terms','peak_monomials','final_monomials','final_degree']

def sha256(path):
 h=hashlib.sha256();
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def git_blob(path):
 b=Path(path).read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def gmean(xs):
 if not xs: return None
 return math.exp(sum(math.log(x) for x in xs)/len(xs))

def medians(rows, metric):
 g=defaultdict(list)
 for r in rows:
  g[(r['case_id'],r['arm'])].append(r[metric])
 return {k:statistics.median(v) for k,v in g.items()}

def ratio(rows,a,b,metric='compile_ns'):
 m=medians(rows,metric); cases=sorted({r['case_id'] for r in rows})
 vals=[m[(c,a)]/m[(c,b)] for c in cases]
 return gmean(vals), vals

def aggregate(rows,arm,key): return sum(int(r.get(key,0)) for r in rows if r['arm']==arm)

def validate_schedule(rows, cases, reps=25):
 seen=defaultdict(list)
 for r in rows: seen[(r['case_id'],r['arm'])].append(r['rep'])
 arms={DIRECT,P3,P2}; issues=[]
 for c in cases:
  combined=[]
  for a in arms:
   got=sorted(seen.get((c,a),[])); combined.extend(got)
   if len(got)!=reps or len(got)!=len(set(got)):
    issues.append({'case':c,'arm':a,'got_n':len(got),'unique_n':len(set(got))})
  if sorted(combined)!=list(range(reps*len(arms))):
   issues.append({'case':c,'arm':'ALL','schedule_error':True,'combined_n':len(combined),'unique_n':len(set(combined))})
 unexpected=[{'case':c,'arm':a} for (c,a) in seen if c not in cases or a not in arms]
 return {'ok':not issues and not unexpected,'issues':issues,'unexpected':unexpected}


D=json.load(open(HERE/'n2_p3_results.json'))
P2REF=json.load(open(HERE/'N2_P2_RESULTS_REFERENCE.json'))
sel=json.load(open(HERE/'chunks'/'selection.json'))
ns,nt,gs,gt=D['natural_symbolic_rows'],D['natural_timing_rows'],D['gatep_symbolic_rows'],D['gatep_timing_rows']
checks={}
checks['prereg_sha256']={'actual':sha256(HERE/'N2_P3_PREREGISTRATION.md'),'expected':EXPECTED_PREREG}
checks['harness_sha256']={'actual':sha256(HERE/'n2_p3_harness.py'),'expected':EXPECTED_HARNESS}
checks['source_blobs']={name:{'actual':git_blob(HERE/'epfl'/name),'expected':exp} for name,exp in EXPECTED_BLOBS.items()}
checks['natural_case_ids']={'actual':sel['case_ids'],'expected':EXPECTED_CASES}
checks['row_counts']={'natural_symbolic':len(ns),'natural_timing':len(nt),'gatep_symbolic':len(gs),'gatep_timing':len(gt),'total':len(ns)+len(nt)+len(gs)+len(gt)}
checks['all_rows_ok']=all(r.get('ok') is True for r in ns+nt+gs+gt)
checks['fuzz']=D['fuzz']
natural_cases=sorted({r['case_id'] for r in ns}); gate_cases=sorted({r['case_id'] for r in gs})
checks['natural_schedule']=validate_schedule(nt,natural_cases)
checks['gatep_schedule']=validate_schedule(gt,gate_cases)
checks['natural_p3_utilization']={'accepted':aggregate(ns,P3,'selector_accepted'),'fold_lowerings':aggregate(ns,P3,'fold_lowerings')}
checks['gatep_p3_utilization']={'accepted':aggregate(gs,P3,'selector_accepted'),'fold_lowerings':aggregate(gs,P3,'fold_lowerings')}
# Frozen P2 direct identity check, independent of harness validation.
cur={r['case_id']:r for r in gs if r['arm']==DIRECT}
old={r['case_id']:r for r in P2REF['gatep_symbolic_rows'] if r['arm']==DIRECT}
identity=[]
for c in sorted(cur):
 for f in IDENTITY_FIELDS:
  if cur[c][f]!=old[c][f]: identity.append({'case_id':c,'field':f,'p3_run':cur[c][f],'p2_reference':old[c][f]})
checks['gatep_direct_identity']={'ok':not identity,'mismatches':identity,'cases_compared':len(cur)}
# Structural equality on natural P3 vs direct because there were no accepted folds.
struct_fields=['digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated']
by={(r['case_id'],r['arm']):r for r in ns}
struct_diff=[]
for c in natural_cases:
 for f in struct_fields:
  if by[(c,P3)][f]!=by[(c,DIRECT)][f]: struct_diff.append({'case_id':c,'field':f,'p3':by[(c,P3)][f],'direct':by[(c,DIRECT)][f]})
checks['natural_p3_direct_structural_identity']={'ok':not struct_diff,'mismatches':struct_diff}
# Recompute primary ratios without importing experiment code.
nat_p3_direct,_=ratio(nt,P3,DIRECT)
nat_p3_p2,_=ratio(nt,P3,P2)
gat_p3_direct,_=ratio(gt,P3,DIRECT)
gat_p3_p2,_=ratio(gt,P3,P2)
checks['recomputed_ratios']={'natural_p3_over_direct_compile':nat_p3_direct,'natural_p3_over_p2_compile':nat_p3_p2,'gatep_p3_over_direct_compile':gat_p3_direct,'gatep_p3_over_p2_compile':gat_p3_p2}
# Work ratios over nonzero denominators, symbolic rows.
def sym_ratio(rows,key):
 by=defaultdict(dict)
 for r in rows: by[r['case_id']][r['arm']]=r
 vals=[]
 for c,d in by.items():
  den=d[DIRECT][key]
  if den: vals.append(d[P3][key]/den)
 return gmean(vals),len(vals)
checks['gatep_symbolic_ratios']={k:{'geomean_ratio':sym_ratio(gs,k)[0],'n_nonzero':sym_ratio(gs,k)[1]} for k in ['multiplications','pair_terms','anf_nodes_evaluated','peak_monomials','python_peak_bytes']}
# Overall status.
ok=True
ok &= checks['prereg_sha256']['actual']==EXPECTED_PREREG
ok &= checks['harness_sha256']['actual']==EXPECTED_HARNESS
ok &= all(x['actual']==x['expected'] for x in checks['source_blobs'].values())
ok &= checks['natural_case_ids']['actual']==EXPECTED_CASES
ok &= checks['row_counts']=={'natural_symbolic':50,'natural_timing':750,'gatep_symbolic':180,'gatep_timing':2700,'total':3680}
ok &= checks['all_rows_ok']
fuzz_failures=D['fuzz'].get('failures',[])
ok &= D['fuzz'].get('cases')==1000 and ((isinstance(fuzz_failures,list) and len(fuzz_failures)==0) or fuzz_failures==0) and D['fuzz'].get('passed') is True
ok &= checks['natural_schedule']['ok'] and checks['gatep_schedule']['ok']
ok &= checks['natural_p3_utilization']=={'accepted':0,'fold_lowerings':0}
ok &= checks['gatep_p3_utilization']=={'accepted':58,'fold_lowerings':58}
ok &= checks['gatep_direct_identity']['ok']
ok &= checks['natural_p3_direct_structural_identity']['ok']
summary={'status':'PASS' if ok else 'FAIL','prereg_sha256':checks['prereg_sha256']['actual'],'harness_sha256':checks['harness_sha256']['actual'],
 'source_manifest_all_verified':all(x['actual']==x['expected'] for x in checks['source_blobs'].values()),
 'row_counts':checks['row_counts'],'all_correct':checks['all_rows_ok'],'fuzz':checks['fuzz'],
 'natural_cases':EXPECTED_CASES,'natural_p3_over_direct_time':nat_p3_direct,'natural_p3_over_p2_time':nat_p3_p2,
 'gatep_p3_over_direct_time':gat_p3_direct,'gatep_p3_over_p2_time':gat_p3_p2,
 'natural_p3_selector_accepted':checks['natural_p3_utilization']['accepted'],'gatep_p3_selector_accepted':checks['gatep_p3_utilization']['accepted'],
 'gatep_p3_fold_lowerings':checks['gatep_p3_utilization']['fold_lowerings'],'gatep_direct_identity_verified':checks['gatep_direct_identity']['ok'],
 'checks':checks}
(HERE/'N2_P3_INDEPENDENT_VERIFY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))
if not ok: raise SystemExit(1)
