from __future__ import annotations
import hashlib,json,math,statistics,pathlib
from collections import defaultdict
HERE=pathlib.Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def gm(xs):return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None
def tree_eval(tree,names,features):
    x=[float(features[k]) for k in names]; i=0
    while True:
        l=tree['children_left'][i]; r=tree['children_right'][i]
        if l==r or l<0:return math.exp(tree['value'][i])
        i=l if x[tree['feature'][i]]<=tree['threshold'][i] else r

def cmp(rows,metric,num,den):
    g=defaultdict(list)
    for r in rows:g[(r['case_id'],r['arm'])].append(r[metric])
    cs=sorted({r['case_id'] for r in rows}); vals=[]; an=ad=0
    for c in cs:
        a=statistics.median(g[(c,num)]); b=statistics.median(g[(c,den)]); vals.append(a/b); an+=a; ad+=b
    return gm(vals),an/ad

gate=json.load(open(HERE/'P8_FROZEN_GATE.json')); cal=json.load(open(HERE/'calibration.json')); fuzz=json.load(open(HERE/'fuzz.json')); gp=json.load(open(HERE/'gatep.json')); summary=json.load(open(HERE/'N2_P8_SUMMARY.json'))
files=['adder_f_4_.json','adder_f_5_.json','cavlc_17.json','cavlc_35.json','int2float_e4.json','int2float_y6.json','priority_new_n130.json','priority_new_n174.json','router_105.json','router_92.json']
nat=[json.load(open(HERE/'natural'/x)) for x in files]
issues=[]
if sha(HERE/'N2_P8_PREREGISTRATION.md')!=gate['prereg_sha256']:issues.append('prereg hash')
if sha(HERE/'n2_p8_harness.py')!=gate['harness_sha256']:issues.append('harness hash')
if sha(HERE/'P8_EPFL_TRAINVAL_SELECTION.json')!=gate['selection_sha256']:issues.append('selection hash')
if sha(HERE/'calibration.json')!=gate['calibration_sha256']:issues.append('calibration hash')
if not fuzz['passed'] or fuzz['failures']:issues.append('fuzz')
# Tree decision/work equivalence.
for r in gp['symbolic']+[x['symbolic'] for x in nat]:
    pred=tree_eval(gate['tree'],gate['feature_names'],r['features']); ann=pred<=gate['cutoff']
    if ann!=r['annotate']:issues.append(('decision',r['case_id']))
    target=r['p6'] if ann else r['direct']
    for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
        if r['p8'].get(k)!=target.get(k):issues.append(('work',r['case_id'],k))
# Counts and ok.
exp={'gate_source':36*20*3,'gate_comp':36*20*3,'nat_source':10*15*3,'nat_comp':10*15*3}
counts={'gate_source':len(gp['source_timing_rows']),'gate_comp':len(gp['compiler_timing_rows']),
        'nat_source':sum(len(x['source_timing_rows']) for x in nat),'nat_comp':sum(len(x['compiler_timing_rows']) for x in nat)}
if counts!=exp:issues.append(('counts',counts,exp))
for r in gp['source_timing_rows']+gp['compiler_timing_rows']+[r for x in nat for r in x['source_timing_rows']+x['compiler_timing_rows']]:
    if not r.get('ok',False):issues.append(('timed correctness',r.get('case_id')))
# Arm counts.
for rows,reps in ((gp['source_timing_rows'],20),(gp['compiler_timing_rows'],20)):
    g=defaultdict(int)
    for r in rows:g[(r['case_id'],r['arm'])]+=1
    if any(v!=reps for v in g.values()) or len(g)!=36*3:issues.append('gate arm schedule')
for getter in ('source_timing_rows','compiler_timing_rows'):
    g=defaultdict(int)
    for x in nat:
        for r in x[getter]:g[(r['case_id'],r['arm'])]+=1
    if any(v!=15 for v in g.values()) or len(g)!=10*3:issues.append(('natural arm schedule',getter))
# Recompute principal ratios.
gsrc=cmp(gp['source_timing_rows'],'source_pipeline_ns','p8_source_dispatch','direct_source_pipeline')
gcomp=cmp(gp['compiler_timing_rows'],'compiler_dispatch_ns','p8_source_dispatch','direct_source_pipeline')
ns=[r for x in nat for r in x['source_timing_rows']]; nc=[r for x in nat for r in x['compiler_timing_rows']]
nsrc=cmp(ns,'source_pipeline_ns','p8_source_dispatch','direct_source_pipeline')
if abs(gsrc[0]-summary['gatep_source']['p8_direct']['geomean_ratio'])>1e-12:issues.append('gate source ratio')
if abs(gcomp[0]-summary['gatep_compiler']['p8_direct']['geomean_ratio'])>1e-12:issues.append('gate compiler ratio')
if abs(nsrc[0]-summary['natural_source']['p8_direct']['geomean_ratio'])>1e-12:issues.append('natural source ratio')
out={'status':'PASS' if not issues else 'FAIL','issues':issues,'hashes':{'prereg':gate['prereg_sha256'],'harness':gate['harness_sha256'],'gate':sha(HERE/'P8_FROZEN_GATE.json')},
     'row_counts':counts,'fuzz_cases':fuzz['cases'],'gatep_p8_over_direct_source':gsrc[0],'gatep_p8_over_direct_source_weighted':gsrc[1],
     'gatep_p8_over_direct_compiler':gcomp[0],'natural_p8_over_direct_source':nsrc[0],'cutoff':gate['cutoff'],
     'gatep_annotated':sum(r['annotate'] for r in gp['symbolic']),'natural_annotated':sum(x['symbolic']['annotate'] for x in nat)}
(HERE/'N2_P8_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
