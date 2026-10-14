from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p13_harness as h

def setup(cid):
    gate=h.load_gate(); recipes,selection,selsha=h.p8.natural_eval_recipes(); by={x[0]:x for x in recipes}
    cid,circuit,d,build,oracle,c=by[cid]
    meta={'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':d}
    seed=h.SEED^int(hashlib.sha256(cid.encode()).hexdigest()[:8],16)^0xB130
    return gate,selsha,build,oracle,meta,seed

def symbolic(cid,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    f12,r12,n12=build(h.p12.LazyReuseTelemetryFactory)
    f13,r13,n13=build(h.DeferredPairTelemetryFactory)
    d12,d13,annotate,code12,code13,leaf12,leaf13=h._compare_p12_p13(f12,f13,cid,gate)
    pf,proot,n=build(h.base.Factory)
    d=h.compile_once(proot,h.COMP_DIRECT,oracle,n,True); q=h.compile_once(proot,h.COMP_P6,oracle,n,True); z=q if annotate else d
    qs=h.p6_stats(proot,oracle,n)
    if not (d['ok'] and q['ok'] and d['digest']==q['digest']): raise AssertionError(('symbolic',cid))
    if qs.get('selector_accepted',0)!=qs.get('fold_lowerings',0): raise AssertionError(('P6 utilization',cid))
    sym={'case_id':cid,**meta,'p12_dispatch':d12,'p13_dispatch':d13,'p12_decision_code':code12,'p13_decision_code':code13,'annotate':annotate,'backend':h.COMP_P6 if annotate else h.COMP_DIRECT,
         'direct':{k:d.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6':{k:q.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p13':{k:z.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6_folds':qs.get('fold_lowerings',0),'p6_accepted':qs.get('selector_accepted',0),'p6_accepted_shared':qs.get('selector_accepted_shared',0)}
    mem=[]
    for arm in (h.DIRECT,h.P6ARM,h.P12ARM,h.P13):
        r=h.source_arm_once(build,oracle,gate,arm,True)
        if not r['ok']: raise AssertionError(('memory',cid,arm))
        mem.append({'case_id':cid,**meta,**r})
    Path(out).write_text(json.dumps({'symbolic':sym,'memory_rows':mem,'selection_sha256':selsha},indent=2))

def timing(cid,start,end,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    rr=random.Random(seed); sched=[a for _ in range(h.NAT_REPS) for a in (h.DIRECT,h.P6ARM,h.P12ARM,h.P13)]; rr.shuffle(sched)
    rows=[]
    for pos in range(start,min(end,len(sched))):
        arm=sched[pos]; r=h.source_arm_once(build,oracle,gate,arm,False)
        if not r['ok']: raise AssertionError(('timed source',cid,arm))
        rows.append({'case_id':cid,**meta,'rep':pos,**{k:r[k] for k in ('arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','decision_code','dispatch_diag','ok')}})
    Path(out).write_text(json.dumps(rows,indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--mode',choices=('symbolic','source'),required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int,default=60); ap.add_argument('--out',required=True); a=ap.parse_args()
    if a.mode=='symbolic': symbolic(a.case_id,a.out)
    else: timing(a.case_id,a.start,a.end,a.out)
if __name__=='__main__':main()
