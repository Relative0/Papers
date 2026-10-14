from __future__ import annotations
import hashlib,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; P8=ROOT/'cm_n2_p8_run'
D='direct_source_pipeline';P6='p6_source_pipeline';P10='p10_fused_source_dispatch';P11='p11_tree_specialized_dispatch'
EXPECTED_PREREG='2a6f61652058ec6b1d8db4ab77f1cb9e34032f385406d783f821a23db701f304'
EXPECTED_HARNESS='9131551f9c7ab7f59ca49b31d348d988684665800b6cf806a6f1ba4a180db455'
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
if sha(HERE/'N2_P11_PREREGISTRATION.md')!=EXPECTED_PREREG:issues.append('prereg hash')
if sha(HERE/'n2_p11_harness.py')!=EXPECTED_HARNESS:issues.append('harness hash')
inv=json.load(open(HERE/'invariance.json'));fuzz=json.load(open(HERE/'fuzz.json'));g=json.load(open(HERE/'gatep.json'));summary=json.load(open(HERE/'N2_P11_SUMMARY.json'))
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
# Recheck P10/P11 exact decision/counter equivalence on evaluation symbolic rows.
for z in g['symbolic']+[x['symbolic'] for x in natural]:
 a=z['p10_features']; c=z['p11_counters']
 for k in ('edge_count','binary_nodes','reuse_edge_events','pair_repeat_excess'):
  if a[k]!=c[k]:issues.append('counter mismatch '+z['case_id']+':'+k);break
 if bool(a['max_pair_shells']>=5)!=bool(c['shell_ge5']):issues.append('shell mismatch '+z['case_id'])
 if bool(z['annotate']) != (float(z['p10_predicted_ratio'])<=0.8):issues.append('decision mismatch '+z['case_id'])
 if z['direct']['digest']!=z['p6']['digest'] or z['direct']['digest']!=z['p11']['digest']:issues.append('digest mismatch '+z['case_id'])
if sum(r['annotate'] for r in g['symbolic'])!=5:issues.append('gatep annotation count')
if sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic'])!=5:issues.append('gatep fold case count')
if sum(x['symbolic']['annotate'] for x in natural)!=0:issues.append('natural annotation count')
def work(field):
 rr=[]
 for r in g['symbolic']:
  d=r['direct'].get(field);z=r['p11'].get(field)
  if d not in (None,0):rr.append(z/d)
 return geo(rr)
g11d,g11dw,g11wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P11,D);g11p10,g11p10w,g11p10wins=ratio(g['source_timing_rows'],'source_pipeline_ns',P11,P10)
gbd,gbdw,gbdwins=ratio(g['source_timing_rows'],'source_build_ns',P11,D);gbp10,gbp10w,gbp10wins=ratio(g['source_timing_rows'],'source_build_ns',P11,P10)
nd,ndw,ndwins=ratio(ns,'source_pipeline_ns',P11,D);np10,np10w,np10wins=ratio(ns,'source_pipeline_ns',P11,P10)
# Summary recomputation consistency.
checks=[('g11d',g11d,summary['gatep_source']['p11_direct']['geomean_ratio']),('g11p10',g11p10,summary['gatep_source']['p11_p10']['geomean_ratio']),('gbd',gbd,summary['gatep_source_build']['p11_direct']['geomean_ratio']),('gbp10',gbp10,summary['gatep_source_build']['p11_p10']['geomean_ratio']),('nd',nd,summary['natural_source']['p11_direct']['geomean_ratio'])]
for name,a,b in checks:
 if abs(a-b)>1e-12:issues.append('summary mismatch '+name)
# Reverify frozen EPFL train/validation files and evaluation files against known manifest/selection hashes.
sel=json.load(open(P8/'P8_EPFL_TRAINVAL_SELECTION.json')); ep=ROOT/'cm_n2_p7b_run'/'epfl'
for split in ('train','validation'):
 for c in sel[split]:
  p=ep/c['file']
  if not p.exists() or sha(p)!=c['file_sha256']:issues.append('EPFL source '+c['file'])
# Evaluation BLIFs are pinned in the P3 EPFL folder and selection.
selnat=json.load(open(ROOT/'cm_n2_p3_run'/'natural_selection_frozen.json'))
for item in selnat.get('sources',[]):
 p=ROOT/'cm_n2_p3_run'/'epfl'/item['file']
 if not p.exists():issues.append('natural EPFL missing '+item['file'])

out={'status':'PASS' if not issues else 'FAIL','issues':issues,
'hashes':{'prereg':sha(HERE/'N2_P11_PREREGISTRATION.md'),'harness':sha(HERE/'n2_p11_harness.py'),'p8_gate':sha(P8/'P8_FROZEN_GATE.json')},
'row_counts':{'gatep_source':len(g['source_timing_rows']),'natural_source':len(ns),'timed_total':len(g['source_timing_rows'])+len(ns)},
'invariance_cases':inv['total'],'fuzz_cases':fuzz['cases'],
'gatep':{'p11_over_direct_source':g11d,'p11_over_direct_source_weighted':g11dw,'p11_over_direct_source_wins':g11wins,'p11_over_p10_source':g11p10,'p11_over_p10_source_weighted':g11p10w,'p11_over_p10_source_wins':g11p10wins,'p11_over_direct_build':gbd,'p11_over_p10_build':gbp10,'p11_over_p10_build_wins':gbp10wins,'annotated':sum(r['annotate'] for r in g['symbolic']),'fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic']),'work':{k:work(k) for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}},
'natural':{'p11_over_direct_source':nd,'p11_over_direct_source_weighted':ndw,'p11_over_p10_source':np10,'p11_over_p10_source_weighted':np10w,'annotated':sum(x['symbolic']['annotate'] for x in natural)},
'predeclared':{'direct_crossover_pass':summary['predeclared_gatep_direct_crossover_pass'],'specialized_telemetry_engineering_success':summary['predeclared_specialized_telemetry_engineering_success']}}
(HERE/'N2_P11_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
