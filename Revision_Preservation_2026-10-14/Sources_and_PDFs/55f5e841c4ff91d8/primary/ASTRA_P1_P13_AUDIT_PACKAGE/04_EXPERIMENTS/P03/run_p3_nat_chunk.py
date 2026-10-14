from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p3_harness as h

ap=argparse.ArgumentParser(); ap.add_argument('--case-id',required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int,default=0); ap.add_argument('--symbolic',action='store_true'); ap.add_argument('--out',required=True)
a=ap.parse_args()
if h.sha256_file(HERE/'N2_P3_PREREGISTRATION.md')!=h.PREREG_SHA256: raise SystemExit('prereg mismatch')
cases,selection,selsha=h.load_cases(); by={c['case_id']:c for c in cases}; c=by[a.case_id]
meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
out={'schema':'cm-n2-p3-natural-chunk/v1','case_id':a.case_id,'selection_sha256':selsha,'symbolic_rows':[],'timing_rows':[]}
if a.symbolic: out['symbolic_rows']=h.symbolic_case(c['root_node'],c['oracle'],c['support'],meta)
rng=random.Random(h.SEED ^ int(hashlib.sha256(a.case_id.encode()).hexdigest()[:8],16) ^ 0x3300)
schedule=[arm for _ in range(h.NATURAL_TIMING_REPS) for arm in h.PRIMARY_ARMS]; rng.shuffle(schedule)
end=a.end if a.end else len(schedule)
for rep in range(a.start,end):
    arm=schedule[rep]
    import time
    t0=time.perf_counter_ns(); r=h.run_reference(c['root_node'],arm,c['oracle'],c['support'],memory=False); elapsed=time.perf_counter_ns()-t0
    if not r['ok']: raise AssertionError((a.case_id,rep,arm))
    out['timing_rows'].append({**meta,'rep':rep,'arm':arm,'elapsed_ns':elapsed,'compile_ns':r['compile_ns'],'refscan_ns':r.get('refscan_ns',0),'match_ns':r.get('match_ns',0),'net_lower_ns':r.get('net_lower_ns',r.get('propagate_ns',0)),'propagate_ns':r.get('propagate_ns',0),'ok':r['ok']})
Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'case_id':a.case_id,'symbolic':len(out['symbolic_rows']),'timing':len(out['timing_rows']),'range':[a.start,end]},indent=2))
