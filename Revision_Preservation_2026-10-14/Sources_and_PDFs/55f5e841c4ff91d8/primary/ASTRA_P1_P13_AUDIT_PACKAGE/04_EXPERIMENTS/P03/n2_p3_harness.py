from __future__ import annotations
import argparse, dataclasses, hashlib, json, math, os, platform, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P2_DIR=HERE.parent/'cm_n2_p2_run'
if str(P2_DIR) not in sys.path: sys.path.insert(0,str(P2_DIR))
import n2_p2_harness as p2
p1=p2.p1
base=p2.base

SEED=20260918
PREREG_SHA256='d37fc5b385f8d36f1b4e863dcc6112ba035513bfa4d8a43b78b96e54d383a47b'
NATURAL_TIMING_REPS=25
GATEP_TIMING_REPS=25
FUZZ_CASES=1000
P3='cm_demand_profit_sparse'
DIRECT='direct_sparse_anf'
P2='cm_inline_profit_sparse'
PRIMARY_ARMS=(DIRECT,P3,P2)
SYMBOLIC_REFERENCE_ARMS=(DIRECT,P3,P2,'cm_profit_sparse','generic_2support_sparse')

@dataclass
class DemandStats:
    successful_folds:int=0
    same_operand_folds:int=0
    transpose_alignments:int=0
    cut_retabulations:int=0
    cse_hits:int=0
    associative_flattened_nodes:int=0
    commutative_reorders:int=0
    output_unique_nodes:int=0
    selector_nodes_checked:int=0
    selector_candidates:int=0
    selector_accepted:int=0
    selector_accepted_shared:int=0
    selector_rejected_nonpositive:int=0
    selector_rejected_min_benefit:int=0
    selector_rejected_fraction:int=0
    selector_estimated_benefit:int=0
    selector_estimated_keep_cost:int=0
    selector_estimated_fold_cost:int=0
    fold_lowerings:int=0
    bypassed_child_shells:int=0
    estimator_cache_entries:int=0
    source_ref_nodes:int=0
    source_ref_edges:int=0
    match_ns:int=0
    refscan_ns:int=0


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def source_refs(root:base.Node):
    refs=defaultdict(int); nodes={}; edges=0; stack=[root]
    while stack:
        n=stack.pop()
        if n.nid in nodes: continue
        nodes[n.nid]=n
        for c in n.args:
            refs[c.nid]+=1; edges+=1; stack.append(c)
    return nodes,refs,edges


def token_for_raw_child(child:base.Node,a:base.Node,b:base.Node):
    """Return (token, is_operator_shell, swapped_alignment) for an immediate source child."""
    if child is a: return base.TOK_X,False,False
    if child is b: return base.TOK_Y,False,False
    if child.op=='not' and child.args[0] is a: return base.TOK_X ^ 15,False,False
    if child.op=='not' and child.args[0] is b: return base.TOK_Y ^ 15,False,False
    if child.op in ('and','or','xor'):
        tok={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}[child.op]
        x,y=child.args
        if x is a and y is b: return tok,True,False
        if x is b and y is a: return base.swap_token(tok),True,True
    if child.op=='tf':
        x,y=child.args
        if x is a and y is b: return child.value,True,False
        if x is b and y is a: return base.swap_token(child.value),True,True
    return None


def seed_pair(child:base.Node):
    if child.op in ('and','or','xor','tf') and len(child.args)==2:
        return child.args
    return None


def token_estimate(token:int,ma:int,mb:int)->int:
    t=token & 15
    v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
    ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
    return min(p1.MONOMIAL_CAP, ca + cb*ma + cc*mb + cd*ma*mb)


def apply_tf_poly(token:int,a:set[int],b:set[int],st:base.AnfStats):
    t=token & 15
    v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
    ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
    p={0} if ca else set()
    if cb: p=base.xor_poly(p,a)
    if cc: p=base.xor_poly(p,b)
    if cd: p=base.xor_poly(p,base.mul_poly(a,b,st))
    base.update_peak(p,st)
    return p


def lower_anf_demand(root:base.Node, nodes:dict[int,base.Node], refs:dict[int,int], refscan_ns:int):
    ast=base.AnfStats(); dst=DemandStats(output_unique_nodes=len(nodes),source_ref_nodes=len(nodes),
                                        source_ref_edges=sum(len(n.args) for n in nodes.values()),refscan_ns=refscan_ns)
    memo={}; estmemo={}

    def choose_fold(n:base.Node):
        if n.op not in ('and','or','xor'):
            return None
        dst.selector_nodes_checked += 1
        parent_token={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}[n.op]
        l,r=n.args
        pairs=[]
        q=seed_pair(l)
        if q is not None: pairs.append(q)
        q=seed_pair(r)
        if q is not None: pairs.append(q)
        for a,b in pairs:
            lt=token_for_raw_child(l,a,b); rt=token_for_raw_child(r,a,b)
            if lt is None or rt is None: continue
            dst.selector_candidates += 1
            tl,lshell,lswap=lt; tr,rshell,rswap=rt
            composed=base.token_apply(n.op,tl,tr)
            ma=p1.estimate_monomials(a,estmemo); mb=p1.estimate_monomials(b,estmemo)
            ml=token_estimate(tl,ma,mb); mr=token_estimate(tr,ma,mb)
            keep=p1.token_nonlinear(parent_token)*ml*mr
            if refs[l.nid]==1 and lshell: keep += p1.token_nonlinear(tl)*ma*mb
            if refs[r.nid]==1 and rshell: keep += p1.token_nonlinear(tr)*ma*mb
            fold=p1.token_nonlinear(composed)*ma*mb
            benefit=keep-fold
            shared=(refs[l.nid]>1 or refs[r.nid]>1)
            fraction=benefit/max(1,keep)
            dst.selector_estimated_keep_cost += keep
            dst.selector_estimated_fold_cost += fold
            if benefit<=0:
                dst.selector_rejected_nonpositive += 1; continue
            if benefit<p1.BENEFIT_MIN:
                dst.selector_rejected_min_benefit += 1; continue
            minfrac=p1.SHARED_FRACTION_MIN if shared else p1.UNSHARED_FRACTION_MIN
            if fraction<minfrac:
                dst.selector_rejected_fraction += 1; continue
            dst.selector_accepted += 1; dst.selector_estimated_benefit += benefit
            if shared: dst.selector_accepted_shared += 1
            if lswap or rswap: dst.transpose_alignments += 1
            return composed,a,b,lshell,rshell
        return None

    def rec(n:base.Node):
        if n.nid in memo:
            ast.cache_hits+=1; return memo[n.nid]
        ast.anf_nodes_evaluated+=1
        fold=None
        if n.op in ('and','or','xor'):
            t0=time.perf_counter_ns(); fold=choose_fold(n); dst.match_ns += time.perf_counter_ns()-t0
        if fold is not None:
            tok,a,b,lshell,rshell=fold
            dst.successful_folds += 1; dst.same_operand_folds += 1; dst.fold_lowerings += 1
            dst.bypassed_child_shells += int(lshell) + int(rshell)
            pa=rec(a); pb=rec(b); p=apply_tf_poly(tok,pa,pb,ast)
        elif n.op=='const': p={0} if n.value else set()
        elif n.op=='var': p={1<<n.value}
        elif n.op=='not':
            p=rec(n.args[0]).copy(); (p.remove(0) if 0 in p else p.add(0)); base.update_peak(p,ast)
        elif n.op=='xor': p=base.xor_poly(rec(n.args[0]),rec(n.args[1])); base.update_peak(p,ast)
        elif n.op=='and': p=base.mul_poly(rec(n.args[0]),rec(n.args[1]),ast)
        elif n.op=='or':
            a=rec(n.args[0]); b=rec(n.args[1]); p=base.xor_poly(base.xor_poly(a,b),base.mul_poly(a,b,ast)); base.update_peak(p,ast)
        elif n.op=='andn':
            level=[rec(c).copy() for c in n.args]
            if not level: p={0}
            else:
                while len(level)>1:
                    nxt=[]
                    for i in range(0,len(level),2): nxt.append(level[i] if i+1==len(level) else base.mul_poly(level[i],level[i+1],ast))
                    level=nxt
                p=level[0]
        elif n.op=='orn':
            level=[rec(c).copy() for c in n.args]
            if not level: p=set()
            else:
                while len(level)>1:
                    nxt=[]
                    for i in range(0,len(level),2):
                        if i+1==len(level): nxt.append(level[i])
                        else:
                            a,b=level[i],level[i+1]; q=base.xor_poly(base.xor_poly(a,b),base.mul_poly(a,b,ast)); base.update_peak(q,ast); nxt.append(q)
                    level=nxt
                p=level[0]
        elif n.op=='tf': p=apply_tf_poly(n.value,rec(n.args[0]),rec(n.args[1]),ast)
        else: raise ValueError(n.op)
        memo[n.nid]=p; ast.peak_cache_entries=max(ast.peak_cache_entries,len(memo)); base.update_peak(p,ast)
        return p

    poly=rec(root); dst.estimator_cache_entries=len(estmemo)
    return poly,ast,dst


def run_direct(root,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars)
    return {'arm':DIRECT,'ok':got==oracle,'compile_ns':t1-t0,'propagate_ns':t1-t0,'plan_ns':0,'optimize_ns':0,
            'refscan_ns':0,'match_ns':0,'net_lower_ns':t1-t0,'python_peak_bytes':peak,'output_unique_nodes':base.reachable_nodes(root),
            'final_monomials':len(poly),'final_degree':max((m.bit_count() for m in poly),default=0),'serialized_bytes':base.poly_serialized_bytes(poly),
            'digest':base.poly_digest(poly),**dataclasses.asdict(ast)}


def run_p3(root,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    c0=time.perf_counter_ns(); r0=time.perf_counter_ns(); nodes,refs,edges=source_refs(root); r1=time.perf_counter_ns()
    poly,ast,dst=lower_anf_demand(root,nodes,refs,r1-r0); c1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars)
    compile_ns=c1-c0; net=max(0,compile_ns-dst.refscan_ns-dst.match_ns)
    return {'arm':P3,'ok':got==oracle,'compile_ns':compile_ns,'propagate_ns':compile_ns-dst.refscan_ns,'plan_ns':0,'optimize_ns':0,
            'net_lower_ns':net,'python_peak_bytes':peak,'final_monomials':len(poly),
            'final_degree':max((m.bit_count() for m in poly),default=0),'serialized_bytes':base.poly_serialized_bytes(poly),
            'digest':base.poly_digest(poly),**dataclasses.asdict(dst),**dataclasses.asdict(ast)}


def run_p2(root,oracle,nvars,memory=False):
    row,_=p2.run_arm(root,P2,oracle,nvars,memory=memory)
    row=dict(row); row['arm']=P2; row['refscan_ns']=0; row['match_ns']=row.get('plan_ns',0); row['net_lower_ns']=row.get('propagate_ns',0)
    return row


def run_reference(root,arm,oracle,nvars,memory=False):
    if arm==DIRECT: return run_direct(root,oracle,nvars,memory)
    if arm==P3: return run_p3(root,oracle,nvars,memory)
    if arm==P2: return run_p2(root,oracle,nvars,memory)
    row,_=p1.run_arm(root,arm,oracle,nvars,memory=memory)
    row=dict(row); row['compile_ns']=row['frontend_anf_ns']; row['refscan_ns']=0; row['match_ns']=row.get('optimize_ns',0); row['net_lower_ns']=row.get('propagate_ns',0)
    return row


def fresh_fuzz():
    rng=random.Random(SEED^0xF333); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        d=run_direct(root,oracle,nvars,False); q=run_p3(root,oracle,nvars,False); z=run_p2(root,oracle,nvars,False)
        if not (d['ok'] and q['ok'] and z['ok'] and d['digest']==q['digest']==z['digest']):
            failures.append({'case':i,'nvars':nvars,'direct_ok':d['ok'],'p3_ok':q['ok'],'p2_ok':z['ok'],
                             'digest_equal':d['digest']==q['digest']==z['digest']})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def load_cases():
    cases,selection,selsha=p2.freeze_cases(HERE/'epfl',HERE)
    return cases,selection,selsha


def p2_gate_reference():
    d=json.loads((HERE/'N2_P2_RESULTS_REFERENCE.json').read_text())
    return {(int(r['depth']),int(r['case'])):r for r in d['gatep_symbolic_rows'] if r['arm']==DIRECT}


def generate_gate_cases():
    rng=random.Random(base.SEED^0x6A7E); cases=[]
    ref=p2_gate_reference(); fields=('digest','output_unique_nodes','multiplications','pair_terms','peak_monomials','final_monomials','final_degree')
    drift=[]
    for depth in p1.GATEP_DEPTHS:
        for i in range(p1.GATEP_CASES_PER_DEPTH):
            f,root,n=base.gatep_case(rng,depth,i); oracle=base.eval_node_bitset(root,n); d=run_direct(root,oracle,n,False); rr=ref[(depth,i)]
            bad={k:(d.get(k),rr.get(k)) for k in fields if d.get(k)!=rr.get(k)}
            if bad: drift.append({'depth':depth,'case':i,'differences':bad})
            cases.append((depth,i,root,n,oracle))
    if drift: raise AssertionError(f'Gate-P identity drift: {drift[:3]}')
    return cases


def symbolic_case(root,oracle,nvars,meta):
    rows=[]; digest=None
    for arm in SYMBOLIC_REFERENCE_ARMS:
        r=run_reference(root,arm,oracle,nvars,memory=True); r.update(meta); rows.append(r)
        if not r['ok']: raise AssertionError(f'oracle mismatch {meta} {arm}')
        if digest is None: digest=r['digest']
        elif r['digest']!=digest: raise AssertionError(f'digest mismatch {meta} {arm}')
    return rows


def timed_case(root,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in PRIMARY_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        t0=time.perf_counter_ns(); r=run_reference(root,arm,oracle,nvars,memory=False); elapsed=time.perf_counter_ns()-t0
        if not r['ok']: raise AssertionError(f'timed oracle mismatch {meta} {arm}')
        rows.append({**meta,'rep':rep,'arm':arm,'elapsed_ns':elapsed,'compile_ns':r['compile_ns'],'refscan_ns':r.get('refscan_ns',0),
                     'match_ns':r.get('match_ns',0),'net_lower_ns':r.get('net_lower_ns',r.get('propagate_ns',0)),'propagate_ns':r.get('propagate_ns',0),'ok':r['ok']})
    return rows


def run_natural_case(case_id):
    cases,selection,selsha=load_cases(); by={c['case_id']:c for c in cases}
    if case_id not in by: raise KeyError(case_id)
    c=by[case_id]; meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
    sym=symbolic_case(c['root_node'],c['oracle'],c['support'],meta)
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x3300
    timing=timed_case(c['root_node'],c['oracle'],c['support'],meta,NATURAL_TIMING_REPS,seed)
    return {'schema':'cm-n2-p3-natural-case/v1','case_id':case_id,'selection_sha256':selsha,'symbolic_rows':sym,'timing_rows':timing}


def run_gatep():
    cases=generate_gate_cases(); symbolic=[]; timing=[]
    for depth,i,root,n,oracle in cases:
        meta={'depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        symbolic.extend(symbolic_case(root,oracle,n,meta))
        timing.extend(timed_case(root,oracle,n,meta,GATEP_TIMING_REPS,SEED+depth*1000+i+0x3300))
    return {'schema':'cm-n2-p3-gatep/v1','symbolic_rows':symbolic,'timing_rows':timing}


def main():
    if sha256_file(HERE/'N2_P3_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P3 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=('fuzz','gatep','natural-case','selection'),required=True); ap.add_argument('--case-id'); ap.add_argument('--out',required=True)
    args=ap.parse_args()
    if args.mode=='fuzz': obj=fresh_fuzz()
    elif args.mode=='gatep': obj=run_gatep()
    elif args.mode=='natural-case':
        if not args.case_id: raise SystemExit('--case-id required')
        obj=run_natural_case(args.case_id)
    else:
        cases,selection,selsha=load_cases(); obj={'selection':selection,'selection_sha256':selsha,'case_ids':[c['case_id'] for c in cases]}
    Path(args.out).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps({'mode':args.mode,'out':args.out,'ok':True,'summary':({k:obj[k] for k in ('cases','passed') if k in obj})},indent=2))

if __name__=='__main__': main()
