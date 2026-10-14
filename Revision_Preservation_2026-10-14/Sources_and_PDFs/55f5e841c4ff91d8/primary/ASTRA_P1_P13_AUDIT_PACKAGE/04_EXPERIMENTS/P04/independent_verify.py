#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math,statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXPECTED_PREREG='052a4f097bdc9677c7d0899f5510458d788aa21ad8fb2b5e72a8f09da2d37971'
EXPECTED_HARNESS='b01e27b95f76678f72742ce5c51fa9163d05b73c55cf6b96385fec0fb03db3d7'
EXPECTED_BLOBS={
 'adder_size_2022.blif':'1a16f1fea72e7fbf67aac019ec97c6aaf871fcdd',
 'bar_size_2015.blif':'a2b2177aa0be92ac60f5c694bcf6eb9806aaa9c2',
 'cavlc_size_2024.blif':'3ebfd39f6193da20b2ae0491dd41bc18eeffce3e',
 'int2float_size_2025.blif':'5c202a31a74dc2b4da0d1ac59377e92c6c37c6d9',
 'priority_size_2024.blif':'4156ea7455044d0a9a49855cca5876ffaa8a003b',
 'router_size_2024.blif':'553e80bc24de67a307b4ce7aafef8adb9603ad26'}
EXPECTED_CASES=['adder:f[4]','adder:f[5]','cavlc:17','cavlc:35','int2float:e4','int2float:y6','priority:new_n130','priority:new_n174','router:105','router:92']
DIRECT_ORIG='direct_sparse_anf'; DIRECT_META='direct_meta_sparse_anf'; P4_NATIVE='cm_meta_native_sparse'; P4_PROP='cm_meta_sig_sparse'; P3='cm_demand_profit_sparse'; P2='cm_inline_profit_sparse'; DIRECT_BUILD='direct_build_sparse'; P4_BUILD='cm_meta_sig_build_sparse'
LOWER_ARMS={DIRECT_META,P4_NATIVE,P4_PROP,P3}; PIPE_ARMS={DIRECT_BUILD,P4_BUILD}
IDENTITY=['digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes']

def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def git_blob(p):
 b=Path(p).read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def gm(xs):return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None
def meds(rows,metric):
 d=defaultdict(list)
 for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
 return {k:statistics.median(v) for k,v in d.items()}
def ratio(rows,a,b,metric):
 m=meds(rows,metric);cs=sorted({r['case_id'] for r in rows});vals=[m[(c,a)]/m[(c,b)] for c in cs];return gm(vals),vals
def sched(rows,cases,arms,reps):
 seen=defaultdict(list);issues=[]
 for r in rows:seen[(r['case_id'],r['arm'])].append(r['rep'])
 for c in cases:
  allrep=[]
  for a in arms:
   got=seen.get((c,a),[]);allrep+=got
   if len(got)!=reps or len(set(got))!=reps:issues.append({'case':c,'arm':a,'n':len(got),'unique':len(set(got))})
  if sorted(allrep)!=list(range(reps*len(arms))):issues.append({'case':c,'arm':'ALL','n':len(allrep),'unique':len(set(allrep))})
 unexpected=[(c,a) for c,a in seen if c not in cases or a not in arms]
 return {'ok':not issues and not unexpected,'issues':issues,'unexpected':unexpected}
def agg(rows,arm,key):return sum((r.get(key,0) or 0) for r in rows if r['arm']==arm)

D=json.load(open(HERE/'n2_p4_results.json'));P3REF=json.load(open(HERE/'N2_P3_RESULTS_REFERENCE.json'))
ns=D['natural_symbolic_rows'];nl=D['natural_lower_timing_rows'];np=D['natural_pipeline_timing_rows'];nm=D['natural_pipeline_memory_rows']
gs=D['gatep_symbolic_rows'];gl=D['gatep_lower_timing_rows'];gp=D['gatep_pipeline_timing_rows'];gmrows=D['gatep_pipeline_memory_rows']
checks={}
checks['prereg_sha256']={'actual':sha256(HERE/'N2_P4_PREREGISTRATION.md'),'expected':EXPECTED_PREREG}
checks['harness_sha256']={'actual':sha256(HERE/'n2_p4_harness.py'),'expected':EXPECTED_HARNESS}
checks['source_blobs']={n:{'actual':git_blob(HERE/'epfl'/n),'expected':e} for n,e in EXPECTED_BLOBS.items()}
checks['natural_cases']={'actual':D['selection']['case_ids'],'expected':EXPECTED_CASES}
checks['row_counts']={'natural_symbolic':len(ns),'natural_lower':len(nl),'natural_pipeline':len(np),'natural_pipeline_memory':len(nm),'gatep_symbolic':len(gs),'gatep_lower':len(gl),'gatep_pipeline':len(gp),'gatep_pipeline_memory':len(gmrows),'total':sum(map(len,[ns,nl,np,nm,gs,gl,gp,gmrows]))}
checks['all_rows_ok']=all(r.get('ok') is True for r in ns+nl+np+nm+gs+gl+gp+gmrows)
checks['fuzz']=D['fuzz']
natcases=sorted({r['case_id'] for r in ns});gatcases=sorted({r['case_id'] for r in gs})
checks['natural_lower_schedule']=sched(nl,natcases,LOWER_ARMS,25);checks['natural_pipeline_schedule']=sched(np,natcases,PIPE_ARMS,15)
checks['gatep_lower_schedule']=sched(gl,gatcases,LOWER_ARMS,25);checks['gatep_pipeline_schedule']=sched(gp,gatcases,PIPE_ARMS,15)
# direct original vs direct meta clone identity
for label,rows in [('natural',ns),('gatep',gs)]:
 by={(r['case_id'],r['arm']):r for r in rows};mis=[]
 for c in sorted({r['case_id'] for r in rows}):
  for f in IDENTITY:
   if by[(c,DIRECT_ORIG)].get(f)!=by[(c,DIRECT_META)].get(f):mis.append({'case':c,'field':f,'orig':by[(c,DIRECT_ORIG)].get(f),'meta':by[(c,DIRECT_META)].get(f)})
 checks[label+'_direct_meta_identity']={'ok':not mis,'mismatches':mis}
# P4 native is intended to reproduce P3 consumed work/acceptance despite fewer duplicate candidate attempts
for label,rows in [('natural',ns),('gatep',gs)]:
 by={(r['case_id'],r['arm']):r for r in rows};mis=[]
 fields=['digest','selector_accepted','fold_lowerings','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated']
 for c in sorted({r['case_id'] for r in rows}):
  for f in fields:
   if by[(c,P4_NATIVE)].get(f)!=by[(c,P3)].get(f):mis.append({'case':c,'field':f,'native':by[(c,P4_NATIVE)].get(f),'p3':by[(c,P3)].get(f)})
 checks[label+'_native_matches_p3_effect']={'ok':not mis,'mismatches':mis}
# Gate-P original direct identity against P3 frozen reference
old={r['case_id']:r for r in P3REF['gatep_symbolic_rows'] if r['arm']==DIRECT_ORIG};cur={r['case_id']:r for r in gs if r['arm']==DIRECT_ORIG};mis=[]
for c in sorted(cur):
 for f in ['digest','output_unique_nodes','multiplications','pair_terms','peak_monomials','final_monomials','final_degree']:
  if cur[c].get(f)!=old[c].get(f):mis.append({'case':c,'field':f,'p4':cur[c].get(f),'p3ref':old[c].get(f)})
checks['gatep_direct_identity_vs_p3']={'ok':not mis,'mismatches':mis,'cases':len(cur)}
# utilization
for label,rows in [('natural',ns),('gatep',gs)]:
 checks[label+'_utilization']={a:{'accepted':agg(rows,a,'selector_accepted'),'fold_lowerings':agg(rows,a,'fold_lowerings')} for a in (P4_NATIVE,P4_PROP)}
# recompute ratios
nat_pd,_=ratio(nl,P4_PROP,DIRECT_META,'lower_ns');nat_pp3,_=ratio(nl,P4_PROP,P3,'lower_ns');nat_pipe,_=ratio(np,P4_BUILD,DIRECT_BUILD,'pipeline_ns')
gat_pd,_=ratio(gl,P4_PROP,DIRECT_META,'lower_ns');gat_pp3,_=ratio(gl,P4_PROP,P3,'lower_ns');gat_pipe,_=ratio(gp,P4_BUILD,DIRECT_BUILD,'pipeline_ns')
checks['recomputed_ratios']={'natural_p4_prop_over_direct_lower':nat_pd,'natural_p4_prop_over_p3_lower':nat_pp3,'natural_p4_pipeline_over_direct':nat_pipe,'gatep_p4_prop_over_direct_lower':gat_pd,'gatep_p4_prop_over_p3_lower':gat_pp3,'gatep_p4_pipeline_over_direct':gat_pipe}
# symbolic ratios gatep independent
def symratio(rows,key,a,b):
 by={(r['case_id'],r['arm']):r for r in rows};vals=[]
 for c in sorted({r['case_id'] for r in rows}):
  den=by[(c,b)].get(key)
  if den not in (None,0):vals.append(by[(c,a)].get(key)/den)
 return gm(vals),len(vals)
checks['gatep_symbolic_p4_prop_over_direct']={k:{'ratio':symratio(gs,k,P4_PROP,DIRECT_META)[0],'n':symratio(gs,k,P4_PROP,DIRECT_META)[1]} for k in ['multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes']}
# status
ok=True
ok &= checks['prereg_sha256']['actual']==EXPECTED_PREREG and checks['harness_sha256']['actual']==EXPECTED_HARNESS
ok &= all(v['actual']==v['expected'] for v in checks['source_blobs'].values())
ok &= checks['natural_cases']['actual']==EXPECTED_CASES
ok &= checks['row_counts']=={'natural_symbolic':60,'natural_lower':1000,'natural_pipeline':300,'natural_pipeline_memory':20,'gatep_symbolic':216,'gatep_lower':3600,'gatep_pipeline':1080,'gatep_pipeline_memory':72,'total':6348}
ok &= checks['all_rows_ok'] and D['fuzz'].get('cases')==1000 and D['fuzz'].get('passed') is True and not D['fuzz'].get('failures')
ok &= all(checks[k]['ok'] for k in ['natural_lower_schedule','natural_pipeline_schedule','gatep_lower_schedule','gatep_pipeline_schedule','natural_direct_meta_identity','gatep_direct_meta_identity','natural_native_matches_p3_effect','gatep_native_matches_p3_effect','gatep_direct_identity_vs_p3'])
ok &= checks['natural_utilization'][P4_PROP]['accepted']==checks['natural_utilization'][P4_PROP]['fold_lowerings']
ok &= checks['gatep_utilization'][P4_PROP]['accepted']==checks['gatep_utilization'][P4_PROP]['fold_lowerings']
ok &= checks['gatep_utilization'][P4_NATIVE]['accepted']==checks['gatep_utilization'][P4_NATIVE]['fold_lowerings']
summary={'status':'PASS' if ok else 'FAIL','prereg_sha256':checks['prereg_sha256']['actual'],'harness_sha256':checks['harness_sha256']['actual'],'source_manifest_all_verified':all(v['actual']==v['expected'] for v in checks['source_blobs'].values()),'row_counts':checks['row_counts'],'all_correct':checks['all_rows_ok'],'fuzz':D['fuzz'],'natural_cases':EXPECTED_CASES,'natural_p4_prop_over_direct_lower':nat_pd,'natural_p4_pipeline_over_direct':nat_pipe,'gatep_p4_prop_over_direct_lower':gat_pd,'gatep_p4_pipeline_over_direct':gat_pipe,'gatep_p4_prop_accepted':checks['gatep_utilization'][P4_PROP]['accepted'],'gatep_p4_prop_fold_lowerings':checks['gatep_utilization'][P4_PROP]['fold_lowerings'],'checks':checks}
(HERE/'N2_P4_INDEPENDENT_VERIFY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))
if not ok: raise SystemExit(1)
