from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p9_harness as h

def setup(cid):
    gate=h.load_gate(); recipes,selection,selsha=h.p8.natural_eval_recipes(); by={x[0]:x for x in recipes}
    cid,circuit,d,build,oracle,c=by[cid]
    meta={'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':d}
    seed=h.SEED^int(hashlib.sha256(cid.encode()).hexdigest()[:8],16)^0x9900
    return gate,selsha,build,oracle,meta,seed

def symbolic(cid,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    mf,mroot,n=build(h.MinimalTelemetryFactory); mfeat=mf.features()
    ff,froot,fn=build(h.p8.TelemetryFactory); ffeat=ff.features(); h.compare_used_features(mfeat,ffeat,cid)
    pred9=h.eval_tree_min(gate['tree'],mfeat); pred8=h.p8.eval_tree(gate['tree'],ffeat)
    if pred9!=pred8: raise AssertionError(('P8/P9 prediction drift',cid,pred8,pred9))
    annotate=pred9<=gate['cutoff']
    pf,proot,pn=build(h.base.Factory)
    d=h.compile_once(proot,h.COMP_DIRECT,oracle,n,True); q=h.compile_once(proot,h.COMP_P6,oracle,n,True); z=q if annotate else d
    qs=h.p6_stats(proot,oracle,n)
    if not (d['ok'] and q['ok'] and d['digest']==q['digest']): raise AssertionError(('symbolic',cid))
    if qs.get('selector_accepted',0)!=qs.get('fold_lowerings',0): raise AssertionError(('P6 utilization',cid))
    sym={'case_id':cid,**meta,'p9_features':mfeat,'predicted_ratio':pred9,'annotate':annotate,'backend':h.COMP_P6 if annotate else h.COMP_DIRECT,
         'direct':{k:d.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6':{k:q.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p9':{k:z.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6_folds':qs.get('fold_lowerings',0),'p6_accepted':qs.get('selector_accepted',0),'p6_accepted_shared':qs.get('selector_accepted_shared',0)}
    mem=[]
    for a in (h.DIRECT,h.P6ARM,h.P8FULL,h.P9):
        r=h.source_arm_once(build,oracle,gate,a,True)
        if not r['ok']: raise AssertionError(('memory',cid,a))
        mem.append({'case_id':cid,**meta,**r})
    Path(out).write_text(json.dumps({'symbolic':sym,'memory_rows':mem,'selection_sha256':selsha},indent=2))

def timing(cid,start,end,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    rr=random.Random(seed); sched=[a for _ in range(h.NAT_REPS) for a in (h.DIRECT,h.P6ARM,h.P8FULL,h.P9)]; rr.shuffle(sched)
    rows=[]
    for pos in range(start,min(end,len(sched))):
        a=sched[pos]; r=h.source_arm_once(build,oracle,gate,a,False)
        if not r['ok']: raise AssertionError(('timed source',cid,a))
        rows.append({'case_id':cid,**meta,'rep':pos,**{k:r[k] for k in ('arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','ok')}})
    Path(out).write_text(json.dumps(rows,indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--mode',choices=('symbolic','source'),required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int,default=60); ap.add_argument('--out',required=True); a=ap.parse_args()
    if a.mode=='symbolic': symbolic(a.case_id,a.out)
    else: timing(a.case_id,a.start,a.end,a.out)
if __name__=='__main__': main()
