from __future__ import annotations
import hashlib,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; P8=ROOT/'cm_n2_p8_run'
D='direct_source_pipeline';P6='p6_source_pipeline';P11='p11_tree_specialized_dispatch';P12='p12_lazy_reuse_dispatch'
EXPECTED_PREREG='90963ffa72693a066b2bc9441887f586204015c647684c68e7cb9afef7a3b3f7'
EXPECTED_HARNESS='d453974ccdbdc78569792e97a7b46f971047bdd3ba5c8b1beb94434293c42549'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def geo(xs):return math.exp(sum(math.log(x) for x in xs)/len(xs))
def med(rows,metric):
 d=defaultdict(list)
 for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
 return {k:statistics.median(v) for k,v in d.items()}
def ratio(rows,metric,a,b):
 m=med(rows,metric);cs=sorted({r['case_id'] for r in rows});rr=[m[(c,a)]/m[(c,b)] for c in cs]
 return geo(rr),sum(m[(c,a)] for c in cs)/sum(m[(c,b)] for c in cs),sum(m[(c,a)]<m[(c,b)] for c in cs)
issues=[]
if sha(HERE/'N2_P12_PREREGISTRATION.md')!=EXPECTED_PREREG:issues.append('prereg hash')
if sha(HERE/'n2_p12_harness.py')!=EXPECTED_HARNESS:issues.append('harness hash')
inv=json.load(open(HERE/'invariance.json'));fuzz=json.load(open(HERE/'fuzz.json'));g=json.load(open(HERE/'gatep.json'));summary=json.load(open(HERE/'N2_P12_SUMMARY.json'))
if not inv.get('passed') or inv.get('total')!=332:issues.append('invariance')
if not fuzz.get('passed') or fuzz.get('cases')!=1000:issues.append('fuzz')
if len(g['source_timing_rows'])!=2880 or any(not r.get('ok') for r in g['source_timing_rows']):issues.append('gatep rows/correctness')
cnt=Counter((r['case_id'],r['arm']) for r in g['source_timing_rows'])
if len(cnt)!=36*4 or any(v!=20 for v in cnt.values()):issues.append('gatep schedule')
natfiles=['adder_f_4.json','adder_f_5.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
natural=[json.load(open(HERE/'natural'/x)) for x in natfiles];ns=[r for x in natural for r in x['source_timing_rows']]
if len(ns)!=600 or any(not r.get('ok') for r in ns):issues.append('natural rows/correctness')
ncnt=Counter((r['case_id'],r['arm']) for r in ns)
if len(ncnt)!=10*4 or any(v!=15 for v in ncnt.values()):issues.append('natural schedule')
# Recheck symbolic decision/counter identities available in the final payload.
for z in g['symbolic']+[x['symbolic'] for x in natural]:
 c=z['p11_counters'];d=z['p12_dispatch']
 if d['pair_repeat_excess']!=c['pair_repeat_excess']:issues.append('repeat mismatch '+z['case_id'])
 if bool(d['shell_ge5'])!=bool(c['shell_ge5']):issues.append('shell mismatch '+z['case_id'])
 if d['edge_count']!=c['edge_count'] or d['binary_nodes']!=c['binary_nodes']:issues.append('base counter mismatch '+z['case_id'])
 if bool(z['annotate']) != (z['p12_decision_code']=='annotate_leaf10'):issues.append('decision code mismatch '+z['case_id'])
 if z['direct']['digest']!=z['p6']['digest'] or z['direct']['digest']!=z['p12']['digest']:issues.append('digest mismatch '+z['case_id'])
 if d['reuse_scanned'] and not d['reuse_early_abort'] and d['reuse_edge_events']!=c['reuse_edge_events']:issues.append('reuse exact mismatch '+z['case_id'])
if sum(r['annotate'] for r in g['symbolic'])!=5:issues.append('gatep annotation count')
if sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic'])!=5:issues.append('gatep fold case count')
if sum(x['symbolic']['annotate'] for x in natural)!=0:issues.append('natural annotation count')
if sum(x['symbolic']['p12_dispatch']['reuse_scanned'] for x in natural)!=0:issues.append('natural reuse scan count')
def work(field):
 rr=[]
 for r in g['symbolic']:
  d=r['direct'].get(field);z=r['p12'].get(field)
  if d not in (None,0):rr.append(z/d)
 return geo(rr)
g12d,g12dw,g12wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P12,D);g12p11,g12p11w,g12p11wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P12,P11)
gbd,gbdw,gbdwins=ratio(g['source_timing_rows'],'source_build_ns',P12,D);gbp11,gbp11w,gbp11wins=ratio(g['source_timing_rows'],'source_build_ns',P12,P11)
nd,ndw,ndwins=ratio(ns,'source_pipeline_ns',P12,D);np11,np11w,np11wins=ratio(ns,'source_pipeline_ns',P12,P11)
checks=[('g12d',g12d,summary['gatep_source']['p12_direct']['geomean_ratio']),('g12p11',g12p11,summary['gatep_source']['p12_p11']['geomean_ratio']),('gbd',gbd,summary['gatep_source_build']['p12_direct']['geomean_ratio']),('gbp11',gbp11,summary['gatep_source_build']['p12_p11']['geomean_ratio']),('nd',nd,summary['natural_source']['p12_direct']['geomean_ratio'])]
for name,a,b in checks:
 if abs(a-b)>1e-12:issues.append('summary mismatch '+name)
# Reverify frozen EPFL train/validation and natural files.
sel=json.load(open(P8/'P8_EPFL_TRAINVAL_SELECTION.json')); ep=ROOT/'cm_n2_p7b_run'/'epfl'
for split in ('train','validation'):
 for c in sel[split]:
  p=ep/c['file']
  if not p.exists() or sha(p)!=c['file_sha256']:issues.append('EPFL source '+c['file'])
selnat=json.load(open(ROOT/'cm_n2_p3_run'/'natural_selection_frozen.json'))
for item in selnat.get('sources',[]):
 p=ROOT/'cm_n2_p3_run'/'epfl'/item['file']
 if not p.exists():issues.append('natural EPFL missing '+item['file'])
out={'status':'PASS' if not issues else 'FAIL','issues':issues,
'hashes':{'prereg':sha(HERE/'N2_P12_PREREGISTRATION.md'),'harness':sha(HERE/'n2_p12_harness.py'),'p8_gate':sha(P8/'P8_FROZEN_GATE.json')},
'row_counts':{'gatep_source':len(g['source_timing_rows']),'natural_source':len(ns),'timed_total':len(g['source_timing_rows'])+len(ns)},
'invariance_cases':inv['total'],'fuzz_cases':fuzz['cases'],
'gatep':{'p12_over_direct_source':g12d,'p12_over_direct_source_weighted':g12dw,'p12_over_direct_source_wins':g12wins,'p12_over_p11_source':g12p11,'p12_over_p11_source_weighted':g12p11w,'p12_over_p11_source_wins':g12p11wins,'p12_over_direct_build':gbd,'p12_over_p11_build':gbp11,'p12_over_p11_build_wins':gbp11wins,'annotated':sum(r['annotate'] for r in g['symbolic']),'fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic']),'reuse_scan_cases':sum(r['p12_dispatch']['reuse_scanned'] for r in g['symbolic']),'reuse_early_abort_cases':sum(r['p12_dispatch']['reuse_early_abort'] for r in g['symbolic']),'work':{k:work(k) for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}},
'natural':{'p12_over_direct_source':nd,'p12_over_direct_source_weighted':ndw,'p12_over_p11_source':np11,'p12_over_p11_source_weighted':np11w,'annotated':sum(x['symbolic']['annotate'] for x in natural),'reuse_scan_cases':sum(x['symbolic']['p12_dispatch']['reuse_scanned'] for x in natural)},
'predeclared':{'direct_crossover_pass':summary['predeclared_gatep_direct_crossover_pass'],'lazy_statistics_engineering_success':summary['predeclared_lazy_statistics_engineering_success']}}
(HERE/'N2_P12_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
