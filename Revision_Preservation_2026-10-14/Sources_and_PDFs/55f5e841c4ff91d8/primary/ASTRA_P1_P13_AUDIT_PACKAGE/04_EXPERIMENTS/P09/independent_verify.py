from __future__ import annotations
import hashlib, json, math, statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
P8=ROOT/'cm_n2_p8_run'
D='direct_source_pipeline'; P6='p6_source_pipeline'; P8A='p8_full_source_dispatch'; P9='p9_min_source_dispatch'
EXPECTED_PREREG='76ab67e4918d625552313acdd8611d8ff0a86523b9114b1d6ed721b3052645d3'
EXPECTED_HARNESS='09248f110f992c2cc64e40834499fa9b94dcccbccafc59c1a47e0d74e22c693b'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def geo(xs):
    return math.exp(sum(math.log(x) for x in xs)/len(xs))

def med(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}

def ratio(rows,metric,a,b):
    m=med(rows,metric); cs=sorted({r['case_id'] for r in rows}); rr=[m[(c,a)]/m[(c,b)] for c in cs]
    return geo(rr),sum(m[(c,a)] for c in cs)/sum(m[(c,b)] for c in cs)

issues=[]
if sha(HERE/'N2_P9_PREREGISTRATION.md')!=EXPECTED_PREREG:issues.append('prereg hash')
if sha(HERE/'n2_p9_harness.py')!=EXPECTED_HARNESS:issues.append('harness hash')
inv=json.load(open(HERE/'invariance.json')); fuzz=json.load(open(HERE/'fuzz.json')); g=json.load(open(HERE/'gatep.json'))
if not inv.get('passed') or inv.get('total')!=332:issues.append('invariance')
if not fuzz.get('passed') or fuzz.get('cases')!=1000:issues.append('fuzz')
if any(not r.get('ok') for r in g['source_timing_rows']):issues.append('gatep correctness')
if len(g['source_timing_rows'])!=2880:issues.append('gatep row count')
# exact arm repetition counts per Gate-P case
cnt=Counter((r['case_id'],r['arm']) for r in g['source_timing_rows'])
if any(v!=20 for v in cnt.values()) or len(cnt)!=36*4:issues.append('gatep schedule')

natfiles=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
natural=[json.load(open(HERE/'natural'/x)) for x in natfiles]
ns=[r for x in natural for r in x['source_timing_rows']]
if len(ns)!=600 or any(not r.get('ok') for r in ns):issues.append('natural rows/correctness')
ncnt=Counter((r['case_id'],r['arm']) for r in ns)
if any(v!=15 for v in ncnt.values()) or len(ncnt)!=10*4:issues.append('natural schedule')

# P8/P9 policy identity on evaluation symbolic records.
if any(r['annotate'] != (r['predicted_ratio']<=0.8) for r in g['symbolic']):issues.append('gatep decision consistency')
if sum(r['annotate'] for r in g['symbolic'])!=5:issues.append('gatep annotation count')
if sum(r['annotate'] for x in natural for r in [x['symbolic']])!=0:issues.append('natural annotation count')

# Work ratios are independently recalculated from symbolic rows.
def work(field):
    rr=[]
    for r in g['symbolic']:
        d=r['direct'].get(field); z=r['p9'].get(field)
        if d not in (None,0):rr.append(z/d)
    return geo(rr)

g_p9_d,g_p9_d_w=ratio(g['source_timing_rows'],'source_pipeline_ns',P9,D)
g_p9_p8,g_p9_p8_w=ratio(g['source_timing_rows'],'source_pipeline_ns',P9,P8A)
g_b_d,g_b_d_w=ratio(g['source_timing_rows'],'source_build_ns',P9,D)
g_b_p8,g_b_p8_w=ratio(g['source_timing_rows'],'source_build_ns',P9,P8A)
n_p9_d,n_p9_d_w=ratio(ns,'source_pipeline_ns',P9,D)
n_p9_p8,n_p9_p8_w=ratio(ns,'source_pipeline_ns',P9,P8A)

# Local EPFL source files still match P8 frozen training/validation selection SHA256s.
sel=json.load(open(P8/'P8_EPFL_TRAINVAL_SELECTION.json'))
ep=P8/'epfl_trainval'
# P8 bundle may store only selection docs and use P7B epfl files outside this dir; use P7B exact inputs.
ep=ROOT/'cm_n2_p7b_run'/'epfl'
for split in ('train','validation'):
    for c in sel[split]:
        p=ep/c['file']
        if not p.exists() or sha(p)!=c['file_sha256']:
            issues.append('EPFL source '+c['file'])

out={
 'status':'PASS' if not issues else 'FAIL','issues':issues,
 'hashes':{'prereg':sha(HERE/'N2_P9_PREREGISTRATION.md'),'harness':sha(HERE/'n2_p9_harness.py'),'p8_gate':sha(P8/'P8_FROZEN_GATE.json')},
 'row_counts':{'gatep_source':len(g['source_timing_rows']),'natural_source':len(ns),'timed_total':len(g['source_timing_rows'])+len(ns)},
 'invariance_cases':inv['total'],'fuzz_cases':fuzz['cases'],
 'gatep':{
   'p9_over_direct_source':g_p9_d,'p9_over_direct_source_weighted':g_p9_d_w,
   'p9_over_p8_source':g_p9_p8,'p9_over_p8_source_weighted':g_p9_p8_w,
   'p9_over_direct_build':g_b_d,'p9_over_p8_build':g_b_p8,
   'annotated':sum(r['annotate'] for r in g['symbolic']),'fold_cases':sum(r['annotate'] and r['p6_folds']>0 for r in g['symbolic']),
   'work':{k:work(k) for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated')}
 },
 'natural':{'p9_over_direct_source':n_p9_d,'p9_over_direct_source_weighted':n_p9_d_w,'p9_over_p8_source':n_p9_p8,'annotated':sum(x['symbolic']['annotate'] for x in natural)},
}
(HERE/'N2_P9_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
