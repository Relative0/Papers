from __future__ import annotations
import argparse, hashlib, json, os, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p4_harness as h

ap=argparse.ArgumentParser()
ap.add_argument('--case-id',required=True)
ap.add_argument('--symbolic',action='store_true')
ap.add_argument('--memory',action='store_true')
ap.add_argument('--lower-start',type=int,default=0)
ap.add_argument('--lower-end',type=int,default=0)
ap.add_argument('--pipe-start',type=int,default=0)
ap.add_argument('--pipe-end',type=int,default=0)
ap.add_argument('--out',required=True)
a=ap.parse_args()
if h.sha256_file(HERE/'N2_P4_PREREGISTRATION.md')!=h.PREREG_SHA256: raise SystemExit('prereg mismatch')
cases,selection,selsha=h.load_cases(); by={c['case_id']:c for c in cases}; c=by[a.case_id]
meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
meta_root,mf=h.build_meta(c['root_node'])
issues=h.validate_meta(meta_root,mf)
if issues: raise AssertionError(issues[:5])
out={'schema':'cm-n2-p4-natural-chunk/v1','case_id':a.case_id,'selection_sha256':selsha,'symbolic_rows':[],'lower_timing_rows':[],'pipeline_timing_rows':[],'pipeline_memory_rows':[]}
if a.symbolic:
    out['symbolic_rows'],_,_=h.run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
if a.memory:
    out['pipeline_memory_rows']=[{**meta,**h.run_pipeline_once(c['root_node'],arm,c['oracle'],c['support'],True)} for arm in h.PIPE_ARMS]
seed=h.SEED ^ int(hashlib.sha256(a.case_id.encode()).hexdigest()[:8],16) ^ 0x4400
lrng=random.Random(seed); ls=[arm for _ in range(h.NATURAL_LOWER_REPS) for arm in h.LOWER_ARMS]; lrng.shuffle(ls)
lend=a.lower_end if a.lower_end else len(ls)
for rep in range(a.lower_start,lend):
    arm=ls[rep]
    if arm==h.DIRECT_META: r=h.run_direct_meta(meta_root,mf,c['oracle'],c['support'],False)
    elif arm==h.P4_NATIVE: r=h.run_p4(meta_root,mf,h.P4_NATIVE,c['oracle'],c['support'],False,False)
    elif arm==h.P4_PROP: r=h.run_p4(meta_root,mf,h.P4_PROP,c['oracle'],c['support'],False,False)
    elif arm==h.P3: r=h.run_p3(c['root_node'],c['oracle'],c['support'],False)
    else: raise ValueError(arm)
    if not r['ok']: raise AssertionError((a.case_id,'lower',rep,arm))
    out['lower_timing_rows'].append({**meta,'rep':rep,'arm':arm,'lower_ns':r['lower_ns'],'compile_ns':r['compile_ns'],'ok':True})
prng=random.Random(seed^0xB17D); ps=[arm for _ in range(h.NATURAL_PIPE_REPS) for arm in h.PIPE_ARMS]; prng.shuffle(ps)
pend=a.pipe_end if a.pipe_end else len(ps)
for rep in range(a.pipe_start,pend):
    arm=ps[rep]; r=h.run_pipeline_once(c['root_node'],arm,c['oracle'],c['support'],False)
    if not r['ok']: raise AssertionError((a.case_id,'pipe',rep,arm))
    out['pipeline_timing_rows'].append({**meta,'rep':rep,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r['dag_build_ns'],'lower_ns':r['lower_ns'],'ok':True})
Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'case_id':a.case_id,'symbolic':len(out['symbolic_rows']),'lower':len(out['lower_timing_rows']),'pipe':len(out['pipeline_timing_rows']),'memory':len(out['pipeline_memory_rows']),'lower_range':[a.lower_start,lend],'pipe_range':[a.pipe_start,pend]},indent=2))
