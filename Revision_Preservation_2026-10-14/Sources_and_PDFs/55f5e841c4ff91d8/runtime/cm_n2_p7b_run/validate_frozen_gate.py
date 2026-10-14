import json,statistics,math
import n2_p7b_harness as h

def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
T,_=h.load_gate(); vals=[]; allrows=[]
for j,(cid,root,n,oracle,meta) in enumerate(h.validation_cases()):
    rows=h._timed_schedule(root,oracle,n,h.ARMS,h.VAL_REPS,h.VAL_SEED+j*19,T)
    meds=h._case_medians(rows); d=meds[h.DIRECT]; dec=h.dispatch_probe(root,T)
    vals.append({'case_id':cid,**meta,'pressure':dec['two_support_pressure'],'annotate':dec['annotate'],
                 'direct_median_ns':d,'p6_median_ns':meds[h.P6ARM],'dispatch_median_ns':meds[h.DISPATCH],
                 'p6_over_direct':meds[h.P6ARM]/d,'dispatch_over_direct':meds[h.DISPATCH]/d})
    allrows.extend([{**meta,'case_id':cid,**r} for r in rows])
out={'schema':'cm-n2-p7b-corrected-validation/v1','threshold':T,'cases':len(vals),
     'dispatch_over_direct_geomean':gm([r['dispatch_over_direct'] for r in vals]),
     'dispatch_over_direct_weighted':sum(r['dispatch_median_ns'] for r in vals)/sum(r['direct_median_ns'] for r in vals),
     'annotated_cases':sum(r['annotate'] for r in vals),'by_kind':{},'records':vals,'timing_rows':allrows}
for kind in ('gatep','pair_noise','random'):
    z=[r for r in vals if r['kind']==kind]
    out['by_kind'][kind]={'cases':len(z),'annotated':sum(r['annotate'] for r in z),'geomean_ratio':gm([r['dispatch_over_direct'] for r in z])}
open('validation_corrected.json','w').write(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('threshold','cases','dispatch_over_direct_geomean','dispatch_over_direct_weighted','annotated_cases','by_kind')},indent=2))
