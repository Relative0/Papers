import csv,glob,hashlib,json,math,random,statistics,collections
from pathlib import Path
HERE=Path('.')
DIRECT='direct_build_sparse'; P6='cm_innode_sig_build_sparse'; DISP='dispatch_p6_or_direct'

def gm(xs):
    xs=[float(x) for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def boot(vals,seed=20260918,B=30000):
    rng=random.Random(seed); n=len(vals); out=[]
    for _ in range(B): out.append(gm([vals[rng.randrange(n)] for _ in range(n)]))
    out.sort(); return [out[int(.025*(B-1))],out[int(.975*(B-1))]]

def case_table(rows,symrows):
    by=collections.defaultdict(lambda:collections.defaultdict(list))
    for r in rows: by[r['case_id']][r['arm']].append(r)
    sym={r['case_id']:r for r in symrows if r['arm']==DISP}
    out=[]
    for cid,a in sorted(by.items()):
        med={arm:statistics.median([x['pipeline_ns'] for x in rr]) for arm,rr in a.items()}
        probe=statistics.median([x['probe_ns'] for x in a[DISP]])
        z=sym[cid]
        row={'case_id':cid,'depth':z.get('depth'),'circuit':z.get('circuit'),'root':z.get('root'),
             'pressure':z.get('two_support_pressure'),'annotate':bool(z.get('annotate')),'backend':z.get('backend'),
             'folds':int(z.get('fold_lowerings',0) or 0),'accepted':int(z.get('selector_accepted',0) or 0),
             'direct_median_ns':med[DIRECT],'p6_median_ns':med[P6],'dispatch_median_ns':med[DISP],
             'probe_median_ns':probe,'p6_over_direct':med[P6]/med[DIRECT],
             'dispatch_over_direct':med[DISP]/med[DIRECT],'probe_over_direct':probe/med[DIRECT]}
        out.append(row)
    return out

def summarize(table,seed):
    dr=[r['dispatch_over_direct'] for r in table]; pr=[r['p6_over_direct'] for r in table]
    return {'cases':len(table),'dispatch_over_direct_geomean':gm(dr),'dispatch_ci':boot(dr,seed),
            'dispatch_over_direct_weighted':sum(r['dispatch_median_ns'] for r in table)/sum(r['direct_median_ns'] for r in table),
            'dispatch_wins':sum(r['dispatch_over_direct']<1 for r in table),
            'p6_over_direct_geomean':gm(pr),'p6_ci':boot(pr,seed^0x55),
            'p6_over_direct_weighted':sum(r['p6_median_ns'] for r in table)/sum(r['direct_median_ns'] for r in table),
            'p6_wins':sum(r['p6_over_direct']<1 for r in table),
            'annotated':sum(r['annotate'] for r in table),'fold_cases':sum(r['folds']>0 for r in table),
            'folds':sum(r['folds'] for r in table),'probe_over_direct_geomean':gm([r['probe_over_direct'] for r in table])}

g=json.load(open('gatep.json'))
natural=[]; nsym=[]
for p in sorted(glob.glob('natural/*.json')):
    x=json.load(open(p)); natural.extend(x['timing_rows']); nsym.extend(x['symbolic_rows'])
gtab=case_table(g['timing_rows'],g['symbolic_rows']); ntab=case_table(natural,nsym)
gsum=summarize(gtab,SEED:=20260918); nsum=summarize(ntab,SEED^1)
# depth summaries
depth={}
for d in (6,8,10): depth[str(d)]=summarize([r for r in gtab if r['depth']==d],SEED+d)
# mixed
mixed=gtab+ntab
msum=summarize(mixed,SEED^0x777)
# confusion against simultaneous P6 timing win
conf={'p6_wins':sum(r['p6_over_direct']<1 for r in gtab),
      'p6_wins_annotated':sum(r['p6_over_direct']<1 and r['annotate'] for r in gtab),
      'p6_wins_bypassed':sum(r['p6_over_direct']<1 and not r['annotate'] for r in gtab),
      'annotated_p6_wins':sum(r['annotate'] and r['p6_over_direct']<1 for r in gtab),
      'annotated_p6_losses':sum(r['annotate'] and r['p6_over_direct']>=1 for r in gtab)}
# symbolic work ratios Gate-P
sb=collections.defaultdict(dict)
for r in g['symbolic_rows']: sb[r['case_id']][r['arm']]=r
work={}
for field in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
    vals=[]
    for v in sb.values():
        d=v[DIRECT][field]; q=v[DISP][field]
        if d==0: vals.append(1.0 if q==0 else float('inf'))
        else: vals.append(q/d)
    vals=[x for x in vals if math.isfinite(x)]
    work[field]={'geomean_ratio':gm(vals),'median_ratio':statistics.median(vals)}
# memory ratios
memory={}
for label,sym in [('gatep',g['symbolic_rows']),('natural',nsym)]:
    bb=collections.defaultdict(dict)
    for r in sym: bb[r['case_id']][r['arm']]=r
    memory[label]={}
    for arm in (DISP,P6):
        vals=[]
        for v in bb.values():
            a=v[arm].get('python_peak_bytes'); d=v[DIRECT].get('python_peak_bytes')
            if a and d: vals.append(a/d)
        memory[label][arm]={'geomean_ratio':gm(vals),'median_ratio':statistics.median(vals)}
# calibration and corrected validation
cal=json.load(open('calibration.json')); val=json.load(open('validation_corrected.json')); gate=json.load(open('P7B_FROZEN_GATE.json'))
calbest=min(cal['objective'],key=lambda x:x['geomean_ratio'])
# post-hoc zero-probe diagnostic, not used for fitting
zero=[]
for t in range(2,33):
    rr=[]
    for z in cal['calibration_records']:
        chosen=z['p6_median_ns'] if z['pressure']>=t else z['direct_median_ns']; rr.append(chosen/z['direct_median_ns'])
    zero.append({'threshold':t,'geomean_ratio':gm(rr),'annotated_cases':sum(z['pressure']>=t for z in cal['calibration_records'])})
zero_best=min(zero,key=lambda x:x['geomean_ratio'])
probe_cal=gm([z['probe_median_ns']/z['direct_median_ns'] for z in cal['calibration_records']])
# all correctness
fuzz=json.load(open('fuzz.json'))
all_timed=g['timing_rows']+natural
all_sym=g['symbolic_rows']+nsym
correct=bool(fuzz['passed'] and all(r['ok'] for r in all_timed) and all(r['ok'] for r in all_sym))
summary={'schema':'cm-n2-p7b-summary/v1','threshold':gate['selected_threshold'],'correct':correct,
         'fuzz':{'cases':fuzz['cases'],'passed':fuzz['passed'],'annotated':fuzz['annotated']},
         'calibration':{'cases':len(cal['calibration_records']),'selected_threshold':cal['selected_threshold'],
                        'best_predicted_ratio_with_probe':calbest['geomean_ratio'],'selected_predicted_ratio_with_probe':next(x['geomean_ratio'] for x in cal['objective'] if x['threshold']==cal['selected_threshold']),
                        'zero_probe_best':zero_best,'probe_over_direct_geomean':probe_cal},
         'validation_corrected':{k:val[k] for k in ('cases','dispatch_over_direct_geomean','dispatch_over_direct_weighted','annotated_cases','by_kind')},
         'gatep':gsum,'natural':nsum,'mixed':msum,'by_depth':depth,'confusion':conf,'gatep_work':work,'memory':memory,
         'hashes':{'prereg':hashlib.sha256(open('N2_P7B_PREREGISTRATION.md','rb').read()).hexdigest(),
                   'frozen_gate':hashlib.sha256(open('P7B_FROZEN_GATE.json','rb').read()).hexdigest(),
                   'harness_corrected':hashlib.sha256(open('n2_p7b_harness.py','rb').read()).hexdigest(),
                   'harness_prefixed_bug':hashlib.sha256(open('n2_p7b_harness_prefixed_bug.py','rb').read()).hexdigest()}}
open('N2_P7B_SUMMARY.json','w').write(json.dumps(summary,indent=2)+'\n')
# CSVs
fields=['case_id','depth','circuit','root','pressure','annotate','backend','folds','accepted','direct_median_ns','p6_median_ns','dispatch_median_ns','probe_median_ns','p6_over_direct','dispatch_over_direct','probe_over_direct']
for name,tab in [('N2_P7B_GATEP_CASE_SUMMARY.csv',gtab),('N2_P7B_NATURAL_CASE_SUMMARY.csv',ntab)]:
    with open(name,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(tab)
# raw merged
raw={'schema':'cm-n2-p7b-results/v1','summary':summary,'calibration':cal,'validation_corrected':val,'fuzz':fuzz,'gatep':g,
     'natural_cases':[json.load(open(p)) for p in sorted(glob.glob('natural/*.json'))]}
open('n2_p7b_results.json','w').write(json.dumps(raw,indent=2)+'\n')
print(json.dumps(summary,indent=2))
