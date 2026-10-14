from __future__ import annotations
import json, glob, hashlib, math, random, statistics, time
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
SEED=20260918
DIRECT_META='direct_meta_sparse_anf'; P4_NATIVE='cm_meta_native_sparse'; P4_PROP='cm_meta_sig_sparse'; P3='cm_demand_profit_sparse'; P2='cm_inline_profit_sparse'; DIRECT_ORIG='direct_sparse_anf'; DIRECT_BUILD='direct_build_sparse'; P4_BUILD='cm_meta_sig_build_sparse'

def gm(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def med(xs): return statistics.median(xs) if xs else None

def bootstrap(vals,n=5000,seed=SEED):
    if not vals:return None
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

def symratio(rows,metric,num=P4_PROP,den=DIRECT_META):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]; bycase={}
    for c in sorted({r['case_id'] for r in rows}):
        a=by.get((c,num),{}).get(metric); b=by.get((c,den),{}).get(metric)
        if a is not None and b not in (None,0):
            q=a/b; vals.append(q); bycase[c]=q
    return {'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':med(vals) if vals else None,'case_ratios':bycase}

def aggregate(rows,arm,key): return sum((r.get(key,0) or 0) for r in rows if r['arm']==arm)

def load_natural():
    ns=[]; nl=[]; np=[]; nm=[]
    # regular one-file cases, excluding cavlc35 split files
    for p in sorted(HERE.glob('chunks/natural_*.json')):
        name=p.name
        if name.startswith('natural_cavlc_35_'): continue
        d=json.load(open(p)); ns+=d.get('symbolic_rows',[]); nl+=d.get('lower_timing_rows',[]); np+=d.get('pipeline_timing_rows',[]); nm+=d.get('pipeline_memory_rows',[])
    # cavlc35 split chunks
    d=json.load(open(HERE/'chunks/natural_cavlc_35_symmem.json')); ns+=d['symbolic_rows']; nm+=d['pipeline_memory_rows']
    for p in sorted(HERE.glob('chunks/natural_cavlc_35_lower_*.json')):
        nl+=json.load(open(p)).get('lower_timing_rows',[])
    for p in sorted(HERE.glob('chunks/natural_cavlc_35_pipe_*.json')):
        np+=json.load(open(p)).get('pipeline_timing_rows',[])
    return ns,nl,np,nm

def summarize(sym,lower,pipe,pmem,label):
    s={}
    for num,den,key in [(P4_PROP,DIRECT_META,'p4_prop_over_direct'),(P4_NATIVE,DIRECT_META,'p4_native_over_direct'),(P4_PROP,P3,'p4_prop_over_p3'),(P4_NATIVE,P3,'p4_native_over_p3'),(P3,DIRECT_META,'p3_over_direct')]:
        s[key+':lower_ns']=compare(lower,num,den,'lower_ns',seed=SEED^(0x44 if label=='natural' else 0x45))
    s['p4_build_over_direct_build:pipeline_ns']=compare(pipe,P4_BUILD,DIRECT_BUILD,'pipeline_ns',seed=SEED^0xB17D)
    s['p4_build_over_direct_build:dag_build_ns']=compare(pipe,P4_BUILD,DIRECT_BUILD,'dag_build_ns',seed=SEED^0xB17E)
    s['weighted_p4_prop_over_direct:lower_ns']=weighted(lower,P4_PROP,DIRECT_META,'lower_ns')
    s['weighted_p4_prop_over_p3:lower_ns']=weighted(lower,P4_PROP,P3,'lower_ns')
    s['weighted_p4_build_over_direct_build:pipeline_ns']=weighted(pipe,P4_BUILD,DIRECT_BUILD,'pipeline_ns')
    metrics=('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','peak_cache_entries','python_peak_bytes')
    s['symbolic_p4_prop_over_direct']={m:symratio(sym,m,P4_PROP,DIRECT_META) for m in metrics}
    s['symbolic_p4_native_over_direct']={m:symratio(sym,m,P4_NATIVE,DIRECT_META) for m in metrics}
    s['symbolic_p4_prop_over_p3']={m:symratio(sym,m,P4_PROP,P3) for m in metrics}
    s['symbolic_p4_prop_over_p2']={m:symratio(sym,m,P4_PROP,P2) for m in metrics}
    for arm,prefix in [(P4_NATIVE,'native'),(P4_PROP,'prop'),(P3,'p3'),(P2,'p2')]:
        s[prefix+'_diag']={k:aggregate(sym,arm,k) for k in (
            'selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared','fold_lowerings','bypassed_child_shells',
            'signature_nodes','propagated_signature_nodes','native_candidate_nodes','propagated_candidate_nodes','propagated_only_candidate_nodes','selector_estimated_benefit')}
    # pipeline memory ratio from one untimed row per case
    pm={(r['case_id'],r['arm']):r for r in pmem}; vals=[]
    for c in sorted({r['case_id'] for r in pmem}):
        a=pm.get((c,P4_BUILD),{}).get('python_peak_bytes'); b=pm.get((c,DIRECT_BUILD),{}).get('python_peak_bytes')
        if a is not None and b not in (None,0): vals.append(a/b)
    s['pipeline_python_peak_p4_over_direct']={'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':med(vals) if vals else None}
    propacc=s['prop_diag']['selector_accepted']; propfold=s['prop_diag']['fold_lowerings']; natacc=s['native_diag']['selector_accepted']; natfold=s['native_diag']['fold_lowerings']
    s['utilization']={'prop':(propfold/propacc if propacc else None),'native':(natfold/natacc if natacc else None)}
    # predeclared signals
    corr=True
    c=s['p4_prop_over_direct:lower_ns']; ci=c['bootstrap']['ci95'] if c['bootstrap'] else [None,None]
    pair=s['symbolic_p4_prop_over_direct']['pair_terms']['geomean_ratio']; peak=s['symbolic_p4_prop_over_direct']['peak_monomials']['geomean_ratio']
    s['lower_speed_signal']=bool(propacc>0 and corr and c['geomean_ratio']<=.95 and ci[1]<1 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    pc=s['p4_build_over_direct_build:pipeline_ns']; pci=pc['bootstrap']['ci95'] if pc['bootstrap'] else [None,None]
    s['pipeline_speed_signal']=bool(propacc>0 and corr and pc['geomean_ratio']<=.95 and pci[1]<1 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    return s

ns,nl,np,nm=load_natural()
g=json.load(open(HERE/'chunks/gatep.json')); gs=g['symbolic_rows']; gl=g['lower_timing_rows']; gp=g['pipeline_timing_rows']; gm_rows=g['pipeline_memory_rows']
fuzz=json.load(open(HERE/'chunks/fuzz.json')); sel=json.load(open(HERE/'chunks/selection.json'))
S={'schema':'cm-n2-p4-results/v1','run_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'fuzz':fuzz,'selection':sel,
   'natural':summarize(ns,nl,np,nm,'natural'),'gatep':summarize(gs,gl,gp,gm_rows,'gatep'),
   'natural_symbolic_rows':ns,'natural_lower_timing_rows':nl,'natural_pipeline_timing_rows':np,'natural_pipeline_memory_rows':nm,
   'gatep_symbolic_rows':gs,'gatep_lower_timing_rows':gl,'gatep_pipeline_timing_rows':gp,'gatep_pipeline_memory_rows':gm_rows}
(HERE/'n2_p4_results.json').write_text(json.dumps(S,indent=2)+'\n')
print(json.dumps({'fuzz':fuzz,'row_counts':{'natural_symbolic':len(ns),'natural_lower':len(nl),'natural_pipeline':len(np),'natural_pipeline_memory':len(nm),'gatep_symbolic':len(gs),'gatep_lower':len(gl),'gatep_pipeline':len(gp),'gatep_pipeline_memory':len(gm_rows)},'natural':S['natural'],'gatep':S['gatep']},indent=2)[:30000])
