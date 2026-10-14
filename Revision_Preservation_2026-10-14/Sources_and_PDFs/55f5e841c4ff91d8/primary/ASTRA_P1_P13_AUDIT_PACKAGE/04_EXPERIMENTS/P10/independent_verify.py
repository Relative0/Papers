from __future__ import annotations
import hashlib,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; P8=ROOT/'cm_n2_p8_run'
D='direct_source_pipeline';P6='p6_source_pipeline';P9='p9_min_source_dispatch';P10='p10_fused_source_dispatch'
EXPECTED_PREREG='874326c0427e14d4b64781087752c6da85f6c89733c9f27c1017cb20e6c9cd42'
EXPECTED_HARNESS='ae589924e976225d45b2db229537dd4063c0e7f655847ebfcbf515a79209efba'
PRIMS=('node_count','edge_count','binary_nodes','max_depth','reuse_edge_events','pair_repeat_excess','max_pair_shells')
USED=('max_depth','max_pair_shells','binary_density','reuse_density','pair_repeat_density')
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
 return geo(rr),sum(m[(c,a)] for c in cs)/sum(m[(c,b)] for c in cs)
issues=[]
if sha(HERE/'N2_P10_PREREGISTRATION.md')!=EXPECTED_PREREG:issues.append('prereg hash')
if sha(HERE/'n2_p10_harness.py')!=EXPECTED_HARNESS:issues.append('harness hash')
inv=json.load(open(HERE/'invariance.json'));fuzz=json.load(open(HERE/'fuzz.json'));g=json.load(open(HERE/'gatep.json'))
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
# exact evaluation feature and decision identity
for z in g['symbolic']+[x['symbolic'] for x in natural]:
 for k in PRIMS+USED:
  if z['p9_features'][k]!=z['p10_features'][k]:issues.append('feature mismatch '+z['case_id']+':'+k);break
 if z['annotate']!=(z['predicted_ratio']<=0.8):issues.append('decision consistency '+z['case_id'])
if sum(r['annotate'] for r in g['symbolic'])!=5:issues.append('gatep annotation count')
if sum(x['symbolic']['annotate'] for x in natural)!=0:issues.append('natural annotation count')
def work(field):
 rr=[]
 for r in g['symbolic']:
  d=r['direct'].get(field);z=r['p10'].get(field)
  if d not in (None,0):rr.append(z/d)
 return geo(rr)
g10d,g10dw=ratio(g['source_timing_rows'],'source_pipeline_ns',P10,D);g10p9,g10p9w=ratio(g['source_timing_rows'],'source_pipeline_ns',P10,P9)
gbd,gbdw=ratio(g['source_timing_rows'],'source_build_ns',P10,D);gbp9,gbp9w=ratio(g['source_timing_rows'],'source_build_ns',P10,P9)
nd,ndw=ratio(ns,'source_pipeline_ns',P10,D);np9,np9w=ratio(ns,'source_pipeline_ns',P10,P9)
# Reverify frozen EPFL input files against selection hashes.
sel=json.load(open(P8/'P8_EPFL_TRAINVAL_SELECTION.json')); ep=ROOT/'cm_n2_p7b_run'/'epfl'
for split in ('train','validation'):
 for c in sel[split]:
  p=ep/c['file']
  if not p.exists() or sha(p)!=c['file_sha256']:issues.append('EPFL source '+c['file'])
out={'status':'PASS' if not issues else 'FAIL','issues':issues,
'hashes':{'prereg':sha(HERE/'N2_P10_PREREGISTRATION.md'),'harness':sha(HERE/'n2_p10_harness.py'),'p8_gate':sha(P8/'P8_FROZEN_GATE.json')},
'row_counts':{'gatep_source':len(g['source_timing_rows']),'natural_source':len(ns),'timed_total':len(g['source_timing_rows'])+len(ns)},
'invariance_cases':inv['total'],'fuzz_cases':fuzz['cases'],
'gatep':{'p10_over_direct_source':g10d,'p10_over_direct_source_weighted':g10dw,'p10_over_p9_source':g10p9,'p10_over_p9_source_weighted':g10p9w,'p10_over_direct_build':gbd,'p10_over_p9_build':gbp9,'annotated':sum(r['annotate'] for r in g['symbolic']),'fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic']),'work':{k:work(k) for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}},
'natural':{'p10_over_direct_source':nd,'p10_over_direct_source_weighted':ndw,'p10_over_p9_source':np9,'p10_over_p9_source_weighted':np9w,'annotated':sum(x['symbolic']['annotate'] for x in natural)}}
(HERE/'N2_P10_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
