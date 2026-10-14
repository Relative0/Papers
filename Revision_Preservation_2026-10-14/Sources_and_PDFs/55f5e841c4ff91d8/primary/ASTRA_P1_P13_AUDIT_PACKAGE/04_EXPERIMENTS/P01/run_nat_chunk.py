from __future__ import annotations
import argparse, hashlib, json, random, time
from pathlib import Path
import n2_p1_harness as h
base = h.base

ROOT=Path('/mnt/data/cm_n2_p1')
EPFL=ROOT/'epfl'
MANIFEST=json.loads((ROOT/'natural_selection_frozen.json').read_text())

def load_case(case_id:str):
    circuit,root=case_id.split(':',1)
    doc=next(x for x in MANIFEST['circuits'] if x['circuit']==circuit)
    item=next(x for x in doc['selected'] if x['root']==root)
    fname=doc['file']; path=EPFL/fname
    blif=base.parse_blif(path)
    support_names=tuple(item['support_names'])
    _f,root_node=h.build_cone_expr(blif,root,support_names)
    oracle=h.eval_blif_cone(blif,root,support_names)
    return {**item,'circuit':circuit,'case_id':case_id,'file':fname,'git_blob':doc['git_blob'],
            'file_sha256':h.sha256_file(path),'root_node':root_node,'oracle':oracle,'support_names':support_names}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('case_id'); ap.add_argument('--symbolic',action='store_true'); ap.add_argument('--start',type=int,default=0); ap.add_argument('--end',type=int,default=0); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    c=load_case(a.case_id); sym=[]; timing=[]
    if a.symbolic:
        bd=None
        for arm in h.ARMS:
            r,_=h.run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=True)
            r.update({k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}); sym.append(r)
            if bd is None: bd=r['digest']
            elif r['digest']!=bd: raise AssertionError(f'digest mismatch {a.case_id} {arm}')
            if not r['ok']: raise AssertionError(f'oracle mismatch {a.case_id} {arm}')
    if a.end>a.start:
        rng=random.Random(h.SEED ^ int(hashlib.sha256(c['case_id'].encode()).hexdigest()[:8],16))
        schedule=[arm for _ in range(h.NATURAL_TIMING_REPS) for arm in h.ARMS]; rng.shuffle(schedule)
        if not (0<=a.start<=a.end<=len(schedule)): raise ValueError('bad range')
        for rep in range(a.start,a.end):
            arm=schedule[rep]
            t0=time.perf_counter_ns(); rr,_=h.run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=False); elapsed=time.perf_counter_ns()-t0
            timing.append({'case_id':c['case_id'],'circuit':c['circuit'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':c['depth'],
                           'rep':rep,'arm':arm,'elapsed_ns':elapsed,'optimize_ns':rr['optimize_ns'],'propagate_ns':rr['propagate_ns'],'ok':rr['ok']})
            if not rr['ok']: raise AssertionError(f'timing oracle mismatch {a.case_id} {arm}')
    a.out.write_text(json.dumps({'case_id':a.case_id,'symbolic':sym,'timing':timing,'range':[a.start,a.end]},indent=2),encoding='utf-8')
    print(json.dumps({'case_id':a.case_id,'symbolic':len(sym),'timing':len(timing),'out':str(a.out)}))
if __name__=='__main__': main()
