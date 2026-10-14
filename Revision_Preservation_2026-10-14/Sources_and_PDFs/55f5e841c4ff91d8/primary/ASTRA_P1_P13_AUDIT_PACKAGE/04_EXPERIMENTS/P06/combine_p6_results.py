from __future__ import annotations
import json, math, random, statistics, time
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
SEED=20260918
DIRECT='direct_innode_sparse_anf'; P6='cm_innode_sig_sparse'; P5='cm_packed_sig_sparse'
DB='direct_build_sparse'; P6B='cm_innode_sig_build_sparse'; P5B='cm_packed_sig_build_sparse'

def gm(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def med(xs): return statistics.median(xs) if xs else None

def bootstrap(vals,n=5000,seed=SEED):
    if not vals: return None
    rng=random.Random(seed); m=len(vals); out=[]
    for _ in range(n): out.append(gm([vals[rng.randrange(m)] for __ in range(m)]))
    out.sort(); return {'estimate':gm(vals),'ci95':[out[int(.025*n)],out[min(n-1,int(.975*n))]]}

def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows:
        if r.get('ok',True): d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:med(v) for k,v in d.items()}

def compare(rows,num,den,metric,seed=SEED):
    m=medmap(rows,metric); cs=sorted({r['case_id'] for r in rows}); vals=[]; bycase={}
    for c in cs:
        a=m.get((c,num)); b=m.get((c,den))
        if a is not None and b not in (None,0):
            q=a/b; vals.append(q); bycase[c]=q
    return {'n':len(vals),'geomean_ratio':gm(vals),'bootstrap':bootstrap(vals,seed=seed),'case_ratios':bycase,
            'cases_below_1':sum(v<1 for v in vals),'cases_below_0_95':sum(v<=.95 for v in vals)}

def weighted(rows,num,den,metric):
    m=medmap(rows,metric); cs=sorted({r['case_id'] for r in rows}); a=b=0
    for c in cs:
        x=m.get((c,num)); y=m.get((c,den))
        if x is not None and y is not None: a+=x; b+=y
    return a/b if b else None

def symratio(rows,metric,num=P6,den=DIRECT):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]; bycase={}
    for c in sorted({r['case_id'] for r in rows}):
        a=by.get((c,num),{}).get(metric); b=by.get((c,den),{}).get(metric)
        if a is not None and b not in (None,0):
            q=a/b; vals.append(q); bycase[c]=q
        elif a==0 and b==0: bycase[c]=1.0
    return {'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':med(vals) if vals else None,'case_ratios':bycase}

def aggregate(rows,arm,key): return sum((r.get(key,0) or 0) for r in rows if r['arm']==arm)

def diag(rows,arm):
    keys=('selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive',
          'selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit','selector_estimated_keep_cost',
          'selector_estimated_fold_cost','fold_lowerings','bypassed_child_shells','signature_nodes','propagated_signature_nodes','propagated_candidate_nodes')
    return {k:aggregate(rows,arm,k) for k in keys}

def memory_ratio(rows,num,den):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]
    for c in sorted({r['case_id'] for r in rows}):
        a=by.get((c,num),{}).get('python_peak_bytes'); b=by.get((c,den),{}).get('python_peak_bytes')
        if a is not None and b not in (None,0): vals.append(a/b)
    return {'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':med(vals) if vals else None}

def group_compare(rows,num,den,metric,groups):
    m=medmap(rows,metric); out={}
    for name,cases in groups.items():
        vals=[]
        for c in cases:
            a=m.get((c,num)); b=m.get((c,den))
            if a is not None and b not in (None,0): vals.append(a/b)
        out[str(name)]={'n':len(vals),'geomean_ratio':gm(vals),'cases_below_1':sum(v<1 for v in vals)}
    return out

def load_natural():
    ns=[]; nl=[]; np=[]; nm=[]
    for p in sorted((HERE/'natural').glob('*.json')):
        d=json.load(open(p)); ns+=d.get('symbolic_rows',[]); nl+=d.get('lower_timing_rows',[]); np+=d.get('pipeline_timing_rows',[]); nm+=d.get('pipeline_memory_rows',[])
    return ns,nl,np,nm

def summarize(sym,lower,pipe,pmem,label):
    s={}; seed=SEED^(0x66 if label=='natural' else 0x67)
    for num,den,key in [(P6,DIRECT,'p6_over_direct'),(P6,P5,'p6_over_p5'),(P5,DIRECT,'p5_over_direct')]:
        s[key+':lower_ns']=compare(lower,num,den,'lower_ns',seed=seed)
    for num,den,key in [(P6B,DB,'p6_build_over_direct'),(P6B,P5B,'p6_build_over_p5'),(P5B,DB,'p5_build_over_direct')]:
        s[key+':pipeline_ns']=compare(pipe,num,den,'pipeline_ns',seed=seed^0xB17D)
        s[key+':dag_build_ns']=compare(pipe,num,den,'dag_build_ns',seed=seed^0xB17E)
    s['weighted_p6_over_direct:lower_ns']=weighted(lower,P6,DIRECT,'lower_ns')
    s['weighted_p6_over_p5:lower_ns']=weighted(lower,P6,P5,'lower_ns')
    s['weighted_p6_build_over_direct:pipeline_ns']=weighted(pipe,P6B,DB,'pipeline_ns')
    s['weighted_p6_build_over_p5:pipeline_ns']=weighted(pipe,P6B,P5B,'pipeline_ns')
    metrics=('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','peak_cache_entries','python_peak_bytes')
    s['symbolic_p6_over_direct']={m:symratio(sym,m,P6,DIRECT) for m in metrics}
    s['symbolic_p6_over_p5']={m:symratio(sym,m,P6,P5) for m in metrics}
    s['p6_diag']=diag(sym,P6); s['p5_diag']=diag(sym,P5)
    s['lower_python_peak_p6_over_direct']=symratio(sym,'python_peak_bytes',P6,DIRECT)
    s['lower_python_peak_p6_over_p5']=symratio(sym,'python_peak_bytes',P6,P5)
    s['pipeline_python_peak_p6_over_direct']=memory_ratio(pmem,P6B,DB)
    s['pipeline_python_peak_p6_over_p5']=memory_ratio(pmem,P6B,P5B)
    acc=s['p6_diag']['selector_accepted']; folds=s['p6_diag']['fold_lowerings']; s['utilization']=(folds/acc if acc else None)
    c=s['p6_over_direct:lower_ns']; ci=c['bootstrap']['ci95'] if c['bootstrap'] else [None,None]
    pair=s['symbolic_p6_over_direct']['pair_terms']['geomean_ratio']; peak=s['symbolic_p6_over_direct']['peak_monomials']['geomean_ratio']
    s['lower_speed_signal']=bool(acc>0 and c['geomean_ratio']<=.95 and ci[1]<1 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    pc=s['p6_build_over_direct:pipeline_ns']; pci=pc['bootstrap']['ci95'] if pc['bootstrap'] else [None,None]
    s['pipeline_speed_signal']=bool(acc>0 and pc['geomean_ratio']<=.95 and pci[1]<1 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    return s

ns,nl,np,nm=load_natural(); g=json.load(open(HERE/'gatep.json'))
gs=g['symbolic_rows']; gl=g['lower_timing_rows']; gp=g['pipeline_timing_rows']; gmem=g['pipeline_memory_rows']
fuzz=json.load(open(HERE/'fuzz.json')); sel=json.load(open(HERE/'selection.json'))
N=summarize(ns,nl,np,nm,'natural'); G=summarize(gs,gl,gp,gmem,'gatep')
cases_by_depth=defaultdict(list)
for r in gs:
    if r['arm']==DIRECT: cases_by_depth[int(r['depth'])].append(r['case_id'])
G['depth_p6_over_direct_lower']=group_compare(gl,P6,DIRECT,'lower_ns',cases_by_depth)
G['depth_p6_build_over_direct_pipeline']=group_compare(gp,P6B,DB,'pipeline_ns',cases_by_depth)
S={'schema':'cm-n2-p6-results/v1','run_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'fuzz':fuzz,'selection':sel,
   'natural':N,'gatep':G,
   'natural_symbolic_rows':ns,'natural_lower_timing_rows':nl,'natural_pipeline_timing_rows':np,'natural_pipeline_memory_rows':nm,
   'gatep_symbolic_rows':gs,'gatep_lower_timing_rows':gl,'gatep_pipeline_timing_rows':gp,'gatep_pipeline_memory_rows':gmem}
(HERE/'n2_p6_results.json').write_text(json.dumps(S,indent=2)+'\n')
print(json.dumps({'fuzz':fuzz,'row_counts':{'natural_symbolic':len(ns),'natural_lower':len(nl),'natural_pipeline':len(np),'natural_pipeline_memory':len(nm),'gatep_symbolic':len(gs),'gatep_lower':len(gl),'gatep_pipeline':len(gp),'gatep_pipeline_memory':len(gmem)},'natural':N,'gatep':G},indent=2))
