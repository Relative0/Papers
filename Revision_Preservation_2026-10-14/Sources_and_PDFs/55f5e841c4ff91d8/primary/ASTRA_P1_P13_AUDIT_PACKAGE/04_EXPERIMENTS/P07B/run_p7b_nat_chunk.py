from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p7b_harness as h

def getcase(cid):
    cases,selection,selsha=h.p7.load_cases(); by={c['case_id']:c for c in cases}; return by[cid],selsha

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--mode',choices=('symmem','timing'),required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--stop',type=int,default=0); ap.add_argument('--out',required=True); a=ap.parse_args()
    T,_=h.load_gate(); c,selsha=getcase(a.case_id); meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}; meta['corpus']='natural'
    seed=h.SEED ^ int(hashlib.sha256(a.case_id.encode()).hexdigest()[:8],16) ^ 0x7B00
    if a.mode=='symmem':
        d=h.run_backend(c['root_node'],h.DIRECT,c['oracle'],c['support'],True); q=h.run_backend(c['root_node'],h.P6ARM,c['oracle'],c['support'],True); z=h.run_dispatch(c['root_node'],c['oracle'],c['support'],T,True)
        for r in (d,q,z): r.update(meta)
        obj={'schema':'cm-n2-p7b-natural-chunk/v1','mode':'symmem','case_id':a.case_id,'selection_sha256':selsha,'symbolic_rows':[d,q,z]}
    else:
        rng=random.Random(seed); schedule=[arm for _ in range(h.NATURAL_REPS) for arm in h.ARMS]; rng.shuffle(schedule)
        rows=[]
        for idx in range(a.start,min(a.stop,len(schedule))):
            arm=schedule[idx]
            if arm==h.DISPATCH: r=h.run_dispatch(c['root_node'],c['oracle'],c['support'],T,False)
            else: r=h.run_backend(c['root_node'],arm,c['oracle'],c['support'],False)
            if not r['ok']: raise AssertionError((a.case_id,idx,arm))
            rows.append({**meta,'rep':idx,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r.get('dag_build_ns'),'lower_ns':r.get('lower_ns'),'probe_ns':r.get('probe_ns',0),'backend':r.get('backend',arm),'annotate':r.get('annotate',arm==h.P6ARM),'two_support_pressure':r.get('two_support_pressure'),'ok':True})
        obj={'schema':'cm-n2-p7b-natural-chunk/v1','mode':'timing','case_id':a.case_id,'selection_sha256':selsha,'start':a.start,'stop':a.stop,'timing_rows':rows}
    Path(a.out).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'case_id':a.case_id,'mode':a.mode,'rows':len(obj.get('timing_rows',obj.get('symbolic_rows',[]))),'out':a.out}))
if __name__=='__main__': main()
