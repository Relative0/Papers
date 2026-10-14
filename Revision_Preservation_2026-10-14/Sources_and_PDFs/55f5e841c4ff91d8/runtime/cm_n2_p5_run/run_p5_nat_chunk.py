from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p5_harness as h

def get_case(case_id):
    cases,selection,selsha=h.load_cases(); by={c['case_id']:c for c in cases}; return by[case_id],selsha

def meta_of(c): return {k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--kind',choices=('symmem','lower','pipe'),required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int); ap.add_argument('--out',required=True); a=ap.parse_args()
    c,selsha=get_case(a.case_id); meta=meta_of(c); seed=h.SEED ^ int(hashlib.sha256(a.case_id.encode()).hexdigest()[:8],16) ^ 0x5500
    obj={'schema':'cm-n2-p5-natural-chunk/v1','case_id':a.case_id,'selection_sha256':selsha,'kind':a.kind,'start':a.start,'end':a.end}
    if a.kind=='symmem':
        sym,p5root,pf,p4root,mf=h.run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
        mem=[{**meta,**h.run_pipeline_once(c['root_node'],arm,c['oracle'],c['support'],True)} for arm in h.PIPE_ARMS]
        obj.update(symbolic_rows=sym,pipeline_memory_rows=mem)
    elif a.kind=='lower':
        p5root,pf=h.build_packed(c['root_node']); p4root,mf=h.build_p4(c['root_node'])
        rng=random.Random(seed); schedule=[arm for _ in range(h.NATURAL_LOWER_REPS) for arm in h.LOWER_ARMS]; rng.shuffle(schedule)
        end=len(schedule) if a.end is None else a.end; rows=[]
        for rep in range(a.start,end):
            arm=schedule[rep]
            if arm==h.DIRECT_PACKED: r=h.run_direct_packed(p5root,pf,c['oracle'],c['support'],False)
            elif arm==h.P5: r=h.run_p5(p5root,pf,c['oracle'],c['support'],False,False)
            elif arm==h.P4: r=h.run_p4(p4root,mf,c['oracle'],c['support'],False,False)
            else: raise ValueError(arm)
            if not r['ok']: raise AssertionError((a.case_id,rep,arm))
            rows.append({**meta,'rep':rep,'arm':arm,'lower_ns':r['lower_ns'],'compile_ns':r['compile_ns'],'ok':True})
        obj['lower_timing_rows']=rows
    else:
        rng=random.Random(seed^0xB17D); schedule=[arm for _ in range(h.NATURAL_PIPE_REPS) for arm in h.PIPE_ARMS]; rng.shuffle(schedule)
        end=len(schedule) if a.end is None else a.end; rows=[]
        for rep in range(a.start,end):
            arm=schedule[rep]; r=h.run_pipeline_once(c['root_node'],arm,c['oracle'],c['support'],False)
            if not r['ok']: raise AssertionError((a.case_id,rep,arm))
            rows.append({**meta,'rep':rep,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r['dag_build_ns'],'lower_ns':r['lower_ns'],'ok':True})
        obj['pipeline_timing_rows']=rows
    Path(a.out).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'ok':True,'case_id':a.case_id,'kind':a.kind,'start':a.start,'end':a.end,'rows':len(obj.get('lower_timing_rows',obj.get('pipeline_timing_rows',obj.get('symbolic_rows',[]))))}))
if __name__=='__main__': main()
