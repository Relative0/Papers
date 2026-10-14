from __future__ import annotations
import argparse, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
P7_DIR=HERE.parent/'cm_n2_p7_run'
if str(P7_DIR) not in sys.path: sys.path.insert(0,str(P7_DIR))
import n2_p7_harness as p7
p6=p7.p6; base=p7.base

SEED=20260918
CAL_SEED=SEED ^ 0x7BCA1
VAL_SEED=SEED ^ 0x7B0A1
FUZZ_SEED=SEED ^ 0x7BF22
PREREG_SHA256='b34a830b65a64e01bb397411ee4b6fcd7501d30d662f80024894a51419046799'
CAL_REPS=9
VAL_REPS=9
GATEP_REPS=20
NATURAL_REPS=15
FUZZ_CASES=1000
THRESHOLDS=tuple(range(2,33))

DIRECT='direct_build_sparse'
P6ARM='cm_innode_sig_build_sparse'
DISPATCH='dispatch_p6_or_direct'
ARMS=(DIRECT,P6ARM,DISPATCH)
BINARY={'and','or','xor','tf'}
TOK={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def geomean(xs):
    xs=[float(x) for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None


def _reachable(root):
    stack=[root]; seen={}; order=[]; refs=defaultdict(int)
    while stack:
        n=stack.pop()
        if n.nid in seen: continue
        seen[n.nid]=n; order.append(n)
        for c in n.args:
            refs[c.nid]+=1
            if c.nid not in seen: stack.append(c)
    return order,refs


def _canon_token(n):
    if n.op=='tf': tok=int(n.value)&15
    else: tok=TOK[n.op]
    a,b=n.args
    if a.nid<=b.nid: return (a.nid,b.nid,tok)
    return (b.nid,a.nid,base.swap_token(tok))


def dispatch_probe(root,threshold:int):
    """Frozen P7B source-DAG probe. Returns decision and pressure diagnostics."""
    order,refs=_reachable(root)
    groups={}
    for n in order:
        if n.op not in BINARY or len(n.args)!=2: continue
        a,b,tok=_canon_token(n)
        key=(a,b)
        g=groups.get(key)
        if g is None:
            g=[0,set(),0]  # pressure, tokens, shell count
            groups[key]=g
        g[0]+=max(1,refs.get(n.nid,0)); g[1].add(tok); g[2]+=1
    pressure=0; eligible=0; max_shells=0
    for p,toks,shells in groups.values():
        if len(toks)>=2:
            eligible+=1
            if p>pressure: pressure=p
            if shells>max_shells: max_shells=shells
    return {'annotate':pressure>=threshold,'two_support_pressure':pressure,
            'reachable_nodes':len(order),'eligible_pair_groups':eligible,'max_group_shells':max_shells}


def timed_probe(root,threshold:int):
    t0=time.perf_counter_ns(); info=dispatch_probe(root,threshold); t1=time.perf_counter_ns()
    return info,t1-t0


def run_backend(root,arm,oracle,nvars,memory=False):
    if arm==DIRECT:
        r=p7.run_pipeline_once(root,p7.DIRECT_BUILD,oracle,nvars,memory)
    elif arm==P6ARM:
        r=p7.run_pipeline_once(root,p7.P6_BUILD,oracle,nvars,memory)
    else: raise ValueError(arm)
    r=dict(r); r['arm']=arm
    return r


def run_dispatch(root,oracle,nvars,threshold,memory=False):
    # The preregistered dispatch endpoint is probe + the selected backend's
    # construction/lowering endpoint.  Correctness conversion/reporting in
    # run_backend remains outside the backend pipeline timer and therefore
    # must also remain outside dispatch timing.
    if memory: tracemalloc.start()
    wall0=time.perf_counter_ns(); probe,probe_ns=timed_probe(root,threshold)
    chosen=P6ARM if probe['annotate'] else DIRECT
    r=run_backend(root,chosen,oracle,nvars,False)
    wall1=time.perf_counter_ns(); peak=None
    if memory:
        _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    out=dict(r)
    out.update({'arm':DISPATCH,'backend':chosen,'probe_ns':probe_ns,
                'pipeline_ns':probe_ns+r['pipeline_ns'],'dispatch_wall_ns':wall1-wall0,
                'python_peak_bytes':peak,**probe})
    return out


def _timed_schedule(root,oracle,nvars,arms,reps,seed,threshold=None):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in arms]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        if arm==DISPATCH:
            r=run_dispatch(root,oracle,nvars,threshold,False)
        else:
            r=run_backend(root,arm,oracle,nvars,False)
        if not r['ok']: raise AssertionError(('timed correctness',arm))
        rows.append({'rep':rep,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r.get('dag_build_ns'),
                     'lower_ns':r.get('lower_ns'),'probe_ns':r.get('probe_ns',0),'backend':r.get('backend',arm),
                     'annotate':r.get('annotate',arm==P6ARM),'two_support_pressure':r.get('two_support_pressure'),
                     'ok':True})
    return rows


def _case_medians(rows):
    by=defaultdict(list)
    for r in rows: by[r['arm']].append(r['pipeline_ns'])
    return {a:statistics.median(v) for a,v in by.items()}


def fresh_gatep_cases(seed,count_per_depth,depths):
    rng=random.Random(seed); out=[]
    for d in depths:
        for i in range(count_per_depth):
            f,root,n=base.gatep_case(rng,d,i); out.append((f'gatep:{d}:{i}',root,n,base.eval_node_bitset(root,n),{'kind':'gatep','depth':d}))
    return out


def pair_noise_case(rng,depth,idx):
    f=base.Factory(); nvars=8
    bases=[base.make_base_expr(rng,nvars,3,f) for _ in range(6)]
    pairs=((0,1),(2,3),(4,5),(0,2),(1,4),(3,5),(0,4),(1,5))
    a,b=pairs[0]
    cur=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
    for level in range(depth):
        a,b=pairs[(level+1)%len(pairs)]
        q=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
        # A second shell can be shared, but the dominant operand pair rotates.
        s=f.bin(rng.choice(('and','or','xor')),bases[a],bases[b])
        left=f.bin(rng.choice(('and','or','xor')),cur,q)
        cur=f.bin(rng.choice(('and','or','xor')),left,s)
    return f,cur,nvars


def pair_noise_cases(seed,count_per_depth,depths):
    rng=random.Random(seed); out=[]
    for d in depths:
        for i in range(count_per_depth):
            f,root,n=pair_noise_case(rng,d,i); out.append((f'noise:{d}:{i}',root,n,base.eval_node_bitset(root,n),{'kind':'pair_noise','depth':d}))
    return out


def random_cases(seed,count):
    rng=random.Random(seed); out=[]
    for i in range(count):
        f=base.Factory(); n=8; d=rng.randint(6,12); root=base.random_expr(rng,n,d,f)
        out.append((f'random:{i}',root,n,base.eval_node_bitset(root,n),{'kind':'random','depth':d}))
    return out


def calibration_cases():
    return (fresh_gatep_cases(CAL_SEED,8,(4,6,8,10,12,14))+
            pair_noise_cases(CAL_SEED^0x2222,6,(6,8,10,12,14,16))+
            random_cases(CAL_SEED^0x3333,36))


def validation_cases():
    return (fresh_gatep_cases(VAL_SEED,4,(4,6,8,10,12,14))+
            pair_noise_cases(VAL_SEED^0x2222,3,(6,8,10,12,14,16))+
            random_cases(VAL_SEED^0x3333,18))


def calibrate():
    cases=calibration_cases(); records=[]
    for j,(cid,root,n,oracle,meta) in enumerate(cases):
        pressure=dispatch_probe(root,2)['two_support_pressure']
        rows=_timed_schedule(root,oracle,n,(DIRECT,P6ARM),CAL_REPS,CAL_SEED+j*17)
        meds=_case_medians(rows)
        # Probe timing is threshold-independent because the frozen feature is fully computed.
        ps=[]
        for k in range(CAL_REPS):
            _,ns=timed_probe(root,2); ps.append(ns)
        records.append({'case_id':cid,**meta,'pressure':pressure,'direct_median_ns':meds[DIRECT],
                        'p6_median_ns':meds[P6ARM],'probe_median_ns':statistics.median(ps),
                        'p6_over_direct':meds[P6ARM]/meds[DIRECT]})
    objective=[]
    for t in THRESHOLDS:
        ratios=[]; weighted_num=weighted_den=0.0; annotated=0
        for r in records:
            choose=r['pressure']>=t
            annotated+=int(choose)
            pred=r['probe_median_ns']+(r['p6_median_ns'] if choose else r['direct_median_ns'])
            ratios.append(pred/r['direct_median_ns']); weighted_num+=pred; weighted_den+=r['direct_median_ns']
        objective.append({'threshold':t,'geomean_ratio':geomean(ratios),'weighted_ratio':weighted_num/weighted_den,
                          'annotated_cases':annotated})
    best=min(x['geomean_ratio'] for x in objective)
    eligible=[x for x in objective if x['geomean_ratio']<=best+0.0025]
    selected=max(eligible,key=lambda x:x['threshold'])
    T=selected['threshold']
    # Validation is diagnostic and cannot retune T.
    vals=[]; allrows=[]
    for j,(cid,root,n,oracle,meta) in enumerate(validation_cases()):
        pressure=dispatch_probe(root,T)['two_support_pressure']
        rows=_timed_schedule(root,oracle,n,ARMS,VAL_REPS,VAL_SEED+j*19,T)
        meds=_case_medians(rows); d=meds[DIRECT]
        dec=dispatch_probe(root,T)
        vals.append({'case_id':cid,**meta,'pressure':pressure,'annotate':dec['annotate'],
                     'direct_median_ns':d,'p6_median_ns':meds[P6ARM],'dispatch_median_ns':meds[DISPATCH],
                     'p6_over_direct':meds[P6ARM]/d,'dispatch_over_direct':meds[DISPATCH]/d})
        allrows.extend([{**meta,'case_id':cid,**r} for r in rows])
    vr=[r['dispatch_over_direct'] for r in vals]
    validation={'cases':len(vals),'dispatch_over_direct_geomean':geomean(vr),
                'dispatch_over_direct_weighted':sum(r['dispatch_median_ns'] for r in vals)/sum(r['direct_median_ns'] for r in vals),
                'annotated_cases':sum(r['annotate'] for r in vals),
                'by_kind':{}}
    for kind in ('gatep','pair_noise','random'):
        z=[r for r in vals if r['kind']==kind]
        validation['by_kind'][kind]={'cases':len(z),'annotated':sum(r['annotate'] for r in z),
            'geomean_ratio':geomean([r['dispatch_over_direct'] for r in z])}
    return {'schema':'cm-n2-p7b-calibration/v1','prereg_sha256':PREREG_SHA256,
            'calibration_seed':CAL_SEED,'validation_seed':VAL_SEED,'selected_threshold':T,
            'selection_rule':'minimum calibration case-geomean; thresholds within +0.0025 absolute choose larger T',
            'objective':objective,'calibration_records':records,'validation_summary':validation,
            'validation_records':vals,'validation_timing_rows':allrows}


def load_gate():
    path=HERE/'P7B_FROZEN_GATE.json'
    obj=json.loads(path.read_text())
    if obj.get('schema')!='cm-n2-p7b-frozen-gate/v1': raise ValueError('bad frozen gate schema')
    return int(obj['selected_threshold']),obj


def fuzz():
    T,_=load_gate(); rng=random.Random(FUZZ_SEED); failures=[]; annotated=0
    for i in range(FUZZ_CASES):
        f=base.Factory(); n=rng.randint(2,8); root=base.random_expr(rng,n,rng.randint(2,9),f); oracle=base.eval_node_bitset(root,n)
        try:
            d=run_backend(root,DIRECT,oracle,n,False); q=run_backend(root,P6ARM,oracle,n,False); z=run_dispatch(root,oracle,n,T,False)
            if not (d['ok'] and q['ok'] and z['ok']): raise AssertionError('oracle')
            if len({d['digest'],q['digest'],z['digest']})!=1: raise AssertionError('digest')
            if z['backend']==DIRECT:
                for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
                    if z.get(k)!=d.get(k): raise AssertionError(('bypass work',k,z.get(k),d.get(k)))
            else:
                annotated+=1
                for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
                    if z.get(k)!=q.get(k): raise AssertionError(('annotated work',k,z.get(k),q.get(k)))
        except Exception as e:
            failures.append({'case':i,'error':repr(e)})
            if len(failures)>=20: break
    return {'schema':'cm-n2-p7b-fuzz/v1','cases':FUZZ_CASES,'annotated':annotated,'failures':failures,'passed':not failures}


def _eval_case(root,oracle,nvars,meta,reps,seed,T):
    # Symbolic/memory rows outside timed schedule.
    d=run_backend(root,DIRECT,oracle,nvars,True); q=run_backend(root,P6ARM,oracle,nvars,True); z=run_dispatch(root,oracle,nvars,T,True)
    # Collect P6 selector/fold statistics outside all timed endpoints so the
    # policy PASS can verify that dispatched annotated cases actually fold.
    p6root,inf=p7.build_p6(root)
    qstats=p7.run_p6(p6root,inf,oracle,nvars,False,True)
    selector_keys=('selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared',
                   'selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction',
                   'selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost',
                   'fold_lowerings','bypassed_child_shells','transpose_alignments','propagated_signature_nodes')
    for k in selector_keys:
        if k in qstats: q[k]=qstats[k]
    if z['backend']==P6ARM:
        for k in selector_keys:
            if k in qstats: z[k]=qstats[k]
    for r in (d,q,z): r.update(meta)
    if not (d['ok'] and q['ok'] and z['ok']): raise AssertionError(('symbolic correctness',meta))
    if len({d['digest'],q['digest'],z['digest']})!=1: raise AssertionError(('symbolic digest',meta))
    if z['backend']==DIRECT:
        for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
            if z.get(k)!=d.get(k): raise AssertionError(('dispatch bypass work',meta,k))
    else:
        for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
            if z.get(k)!=q.get(k): raise AssertionError(('dispatch p6 work',meta,k))
        if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError(('P6 utilization',meta))
    rows=_timed_schedule(root,oracle,nvars,ARMS,reps,seed,T)
    rows=[{**meta,**r} for r in rows]
    return [d,q,z],rows


def run_gatep_eval():
    T,gate=load_gate(); sym=[]; timing=[]
    for depth,i,root,n,oracle in p7.generate_gate_cases():
        meta={'corpus':'gatep','depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        s,t=_eval_case(root,oracle,n,meta,GATEP_REPS,SEED+depth*1000+i+0x7B00,T); sym.extend(s); timing.extend(t)
    return {'schema':'cm-n2-p7b-gatep/v1','threshold':T,'gate_sha256':sha256_file(HERE/'P7B_FROZEN_GATE.json'),
            'symbolic_rows':sym,'timing_rows':timing}


def run_natural_case(case_id):
    T,gate=load_gate(); cases,selection,selsha=p7.load_cases(); by={c['case_id']:c for c in cases}; c=by[case_id]
    meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}; meta['corpus']='natural'
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x7B00
    s,t=_eval_case(c['root_node'],c['oracle'],c['support'],meta,NATURAL_REPS,seed,T)
    return {'schema':'cm-n2-p7b-natural-case/v1','threshold':T,'selection_sha256':selsha,
            'gate_sha256':sha256_file(HERE/'P7B_FROZEN_GATE.json'),'symbolic_rows':s,'timing_rows':t}


def selection():
    cases,sel,sha=p7.load_cases(); return {'selection':sel,'selection_sha256':sha,'case_ids':[c['case_id'] for c in cases]}


def main():
    if sha256_file(HERE/'N2_P7B_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P7B preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',required=True,choices=('calibrate','fuzz','gatep','natural-case','selection'))
    ap.add_argument('--case-id'); ap.add_argument('--out',required=True); a=ap.parse_args()
    if a.mode=='calibrate': obj=calibrate()
    elif a.mode=='fuzz': obj=fuzz()
    elif a.mode=='gatep': obj=run_gatep_eval()
    elif a.mode=='natural-case':
        if not a.case_id: raise SystemExit('--case-id required')
        obj=run_natural_case(a.case_id)
    else: obj=selection()
    Path(a.out).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'mode':a.mode,'out':a.out,'ok':True,'summary':{k:obj[k] for k in ('selected_threshold','cases','passed','threshold') if k in obj}},indent=2))

if __name__=='__main__': main()
