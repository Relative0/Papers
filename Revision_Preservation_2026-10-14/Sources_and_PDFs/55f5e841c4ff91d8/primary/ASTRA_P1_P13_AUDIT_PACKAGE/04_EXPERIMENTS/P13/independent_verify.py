from __future__ import annotations
import hashlib,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; P8=ROOT/'cm_n2_p8_run'
D='direct_source_pipeline';P6='p6_source_pipeline';P12='p12_lazy_reuse_dispatch';P13='p13_deferred_pair_dispatch'
EXPECTED_PREREG='28cd2f282764cd34d2c9c3bc2c9beca283fb34bf5d8f3900789f58a87eaf922a'
EXPECTED_HARNESS='9678b4e8e5d75980c235411462e6999d159f55f911b4bcf582168d55b2beeedb'
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
if sha(HERE/'N2_P13_PREREGISTRATION.md')!=EXPECTED_PREREG:issues.append('prereg hash')
if sha(HERE/'n2_p13_harness.py')!=EXPECTED_HARNESS:issues.append('harness hash')
inv=json.load(open(HERE/'invariance.json'));fuzz=json.load(open(HERE/'fuzz.json'));g=json.load(open(HERE/'gatep.json'));summary=json.load(open(HERE/'N2_P13_SUMMARY.json'))
if not inv.get('passed') or inv.get('total')!=332:issues.append('invariance')
if not fuzz.get('passed') or fuzz.get('cases')!=1000:issues.append('fuzz')
if len(g['source_timing_rows'])!=2880 or any(not r.get('ok') for r in g['source_timing_rows']):issues.append('gatep rows/correctness')
cnt=Counter((r['case_id'],r['arm']) for r in g['source_timing_rows'])
if len(cnt)!=36*4 or any(v!=20 for v in cnt.values()):issues.append('gatep schedule')
natfiles=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
natural=[json.load(open(HERE/'natural'/x)) for x in natfiles];ns=[r for x in natural for r in x['source_timing_rows']]
if len(ns)!=600 or any(not r.get('ok') for r in ns):issues.append('natural rows/correctness')
ncnt=Counter((r['case_id'],r['arm']) for r in ns)
if len(ncnt)!=10*4 or any(v!=15 for v in ncnt.values()):issues.append('natural schedule')
# Recheck final symbolic payload consistency.
for z in g['symbolic']+[x['symbolic'] for x in natural]:
 d12=z['p12_dispatch'];d13=z['p13_dispatch']
 if d13['edge_count']!=d12['edge_count'] or d13['binary_nodes']!=d12['binary_nodes']:issues.append('base counter mismatch '+z['case_id'])
 if d13['pair_repeat_excess'] is not None and d13['pair_repeat_excess']!=d12['pair_repeat_excess']:issues.append('repeat mismatch '+z['case_id'])
 if bool(z['annotate']) != (z['p13_decision_code']=='annotate_leaf10'):issues.append('decision code mismatch '+z['case_id'])
 if z['direct']['digest']!=z['p6']['digest'] or z['direct']['digest']!=z['p13']['digest']:issues.append('digest mismatch '+z['case_id'])
 if d13['reuse_scanned']!=d12['reuse_scanned']:issues.append('reuse eligibility mismatch '+z['case_id'])
 if d13['reuse_scanned'] and (d13['reuse_early_abort']!=d12['reuse_early_abort'] or d13['reuse_scan_edges']!=d12['reuse_scan_edges'] or d13['reuse_edge_events']!=d12['reuse_edge_events']):issues.append('reuse scan mismatch '+z['case_id'])
if sum(r['annotate'] for r in g['symbolic'])!=5:issues.append('gatep annotation count')
if sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic'])!=5:issues.append('gatep fold case count')
if sum(x['symbolic']['annotate'] for x in natural)!=0:issues.append('natural annotation count')

def work(field):
 rr=[]
 for r in g['symbolic']:
  d=r['direct'].get(field);z=r['p13'].get(field)
  if d not in (None,0):rr.append(z/d)
 return geo(rr)
g13d,g13dw,g13wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P13,D);g13p12,g13p12w,g13p12wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P13,P12)
gbd,gbdw,gbdwins=ratio(g['source_timing_rows'],'source_build_ns',P13,D);gbp12,gbp12w,gbp12wins=ratio(g['source_timing_rows'],'source_build_ns',P13,P12)
nd,ndw,ndwins=ratio(ns,'source_pipeline_ns',P13,D);np12,np12w,np12wins=ratio(ns,'source_pipeline_ns',P13,P12)
checks=[('g13d',g13d,summary['gatep_source']['p13_direct']['geomean_ratio']),('g13p12',g13p12,summary['gatep_source']['p13_p12']['geomean_ratio']),('gbd',gbd,summary['gatep_source_build']['p13_direct']['geomean_ratio']),('gbp12',gbp12,summary['gatep_source_build']['p13_p12']['geomean_ratio']),('nd',nd,summary['natural_source']['p13_direct']['geomean_ratio'])]
for name,a,b in checks:
 if abs(a-b)>1e-12:issues.append('summary mismatch '+name)
# Reverify frozen EPFL files used by train/validation and natural controls.
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
'hashes':{'prereg':sha(HERE/'N2_P13_PREREGISTRATION.md'),'harness':sha(HERE/'n2_p13_harness.py'),'p8_gate':sha(P8/'P8_FROZEN_GATE.json')},
'row_counts':{'gatep_source':len(g['source_timing_rows']),'natural_source':len(ns),'timed_total':len(g['source_timing_rows'])+len(ns)},
'invariance_cases':inv['total'],'fuzz_cases':fuzz['cases'],
'gatep':{'p13_over_direct_source':g13d,'p13_over_direct_source_weighted':g13dw,'p13_over_direct_source_wins':g13wins,'p13_over_p12_source':g13p12,'p13_over_p12_source_weighted':g13p12w,'p13_over_p12_source_wins':g13p12wins,'p13_over_direct_build':gbd,'p13_over_p12_build':gbp12,'p13_over_p12_build_wins':gbp12wins,'annotated':sum(r['annotate'] for r in g['symbolic']),'fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic']),'pair_exactification_cases':sum(r['p13_dispatch']['pair_exactified'] for r in g['symbolic']),'reuse_scan_cases':sum(r['p13_dispatch']['reuse_scanned'] for r in g['symbolic']),'work':{k:work(k) for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}},
'natural':{'p13_over_direct_source':nd,'p13_over_direct_source_weighted':ndw,'p13_over_p12_source':np12,'p13_over_p12_source_weighted':np12w,'annotated':sum(x['symbolic']['annotate'] for x in natural),'pair_exactification_cases':sum(x['symbolic']['p13_dispatch']['pair_exactified'] for x in natural)},
'predeclared':{'direct_crossover_pass':summary['predeclared_gatep_direct_crossover_pass'],'deferred_pair_engineering_success':summary['predeclared_deferred_pair_engineering_success']}}
(HERE/'N2_P13_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
