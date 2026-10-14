from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p8_harness as h

def setup(cid):
    gate=h.load_gate(); recipes,selection,selsha=h.natural_eval_recipes(); by={x[0]:x for x in recipes}; x=by[cid]
    cid,circuit,d,build,oracle,c=x
    meta={'corpus':'natural','circuit':circuit,'root':c['root'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':d}
    seed=h.SEED^int(hashlib.sha256(cid.encode()).hexdigest()[:8],16)^0x8800
    return gate,selsha,build,oracle,meta,seed

def symbolic(cid,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    tf,troot,n=build(h.TelemetryFactory); feat=tf.features(); pf,proot,pn=build(h.base.Factory)
    d=h.compile_once(proot,h.COMP_DIRECT,oracle,n,True); q=h.compile_once(proot,h.COMP_P6,oracle,n,True)
    pred=h.eval_tree(gate['tree'],feat); annotate=pred<=gate['cutoff']; z=q if annotate else d
    qs=h.p6_stats(proot,oracle,n)
    sym={'case_id':cid,**meta,'features':feat,'predicted_ratio':pred,'annotate':annotate,'backend':h.COMP_P6 if annotate else h.COMP_DIRECT,
         'direct':{k:d.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6':{k:q.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p8':{k:z.get(k) for k in ('digest','multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','python_peak_bytes')},
         'p6_folds':qs.get('fold_lowerings',0),'p6_accepted':qs.get('selector_accepted',0),'p6_accepted_shared':qs.get('selector_accepted_shared',0)}
    mem=[{'case_id':cid,**meta,**h.source_arm_once(build,oracle,gate,a,True)} for a in (h.DIRECT,h.P6ARM,h.P8)]
    Path(out).write_text(json.dumps({'symbolic':sym,'memory_rows':mem,'selection_sha256':selsha},indent=2))

def timing(cid,kind,start,end,out):
    gate,selsha,build,oracle,meta,seed=setup(cid)
    if kind=='source':
        rr=random.Random(seed); sched=[a for _ in range(h.NAT_REPS) for a in (h.DIRECT,h.P6ARM,h.P8)]; rr.shuffle(sched)
        rows=[]
        for pos in range(start,min(end,len(sched))):
            a=sched[pos]; r=h.source_arm_once(build,oracle,gate,a,False)
            rows.append({'case_id':cid,**meta,'rep':pos,**{k:r[k] for k in ('arm','source_pipeline_ns','source_build_ns','compiler_ns','backend','annotate','predicted_ratio','ok')}})
    else:
        tf,troot,n=build(h.TelemetryFactory); feat=tf.features()
        rr=random.Random(seed^0xC0A1); sched=[a for _ in range(h.NAT_REPS) for a in (h.DIRECT,h.P6ARM,h.P8)]; rr.shuffle(sched)
        rows=[]
        for pos in range(start,min(end,len(sched))):
            a=sched[pos]; r=h.compiler_dispatch_once(troot,oracle,n,gate,feat,a)
            rows.append({'case_id':cid,**meta,'rep':pos,**r})
    Path(out).write_text(json.dumps(rows,indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--mode',choices=('symbolic','source','compiler'),required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int,default=45); ap.add_argument('--out',required=True); a=ap.parse_args()
    if a.mode=='symbolic': symbolic(a.case_id,a.out)
    else: timing(a.case_id,a.mode,a.start,a.end,a.out)
if __name__=='__main__':main()
