from __future__ import annotations
import dataclasses, hashlib, json, math, os, platform, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P1_DIR=HERE.parent/'cm_n2_p1_bundle'
if str(P1_DIR) not in sys.path: sys.path.insert(0,str(P1_DIR))
import n2_p1_harness as p1
base=p1.base

SEED=20260918
PREREG_SHA256='8fce1ff89f7843dc337b27fab437bd1bb018d450197241b7bd55d9baa2f84318'
NATURAL_TIMING_REPS=25
GATEP_TIMING_REPS=25
FUZZ_CASES=1000
ARMS=('direct_sparse_anf','cm_inline_profit_sparse','cm_profit_sparse','generic_2support_sparse')
P2='cm_inline_profit_sparse'
DIRECT='direct_sparse_anf'
P1='cm_profit_sparse'
GENERIC='generic_2support_sparse'

@dataclass
class PlanEntry:
    token:int
    a_nid:int
    b_nid:int
    keep_cost:int
    fold_cost:int
    benefit:int
    shared:bool

@dataclass
class PlanStats:
    successful_folds:int=0
    same_operand_folds:int=0
    transpose_alignments:int=0
    cut_retabulations:int=0
    cse_hits:int=0
    associative_flattened_nodes:int=0
    commutative_reorders:int=0
    output_unique_nodes:int=0
    selector_candidates:int=0
    selector_accepted:int=0
    selector_accepted_shared:int=0
    selector_rejected_nonpositive:int=0
    selector_rejected_min_benefit:int=0
    selector_rejected_fraction:int=0
    selector_estimated_benefit:int=0
    selector_estimated_keep_cost:int=0
    selector_estimated_fold_cost:int=0
    plan_entries:int=0
    virtual_nodes:int=0

PLAN_FIELDS=tuple(dataclasses.asdict(PlanStats()).keys())


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def source_graph(root:base.Node):
    nodes={}; refs=defaultdict(int); stack=[root]
    while stack:
        n=stack.pop()
        if n.nid in nodes: continue
        nodes[n.nid]=n
        for c in n.args:
            refs[c.nid]+=1
            stack.append(c)
    return nodes,refs


def build_profit_plan(root:base.Node):
    """Build a P1-equivalent local fold decision plan, but do not return a rewritten executable DAG."""
    source_nodes,source_refs=source_graph(root)
    vf=base.Factory(); stats=PlanStats(output_unique_nodes=len(source_nodes)); memo={}; v_origin={}; estmemo={}; plan={}
    var_cache={}

    def register_origin(v,src):
        # Preserve the earliest source representative when Factory simplification/CSE returns
        # an existing virtual value; it remains semantically equivalent and acyclic bottom-up.
        if v.nid not in v_origin: v_origin[v.nid]=src

    def clone_var(v):
        if v.value not in var_cache:
            var_cache[v.value]=vf.var(v.value)
            register_origin(var_cache[v.value],v)
        return var_cache[v.value]

    def candidate_cost(n_src,l,r,parent_token,a,b,composed):
        ma=p1.estimate_monomials(a,estmemo); mb=p1.estimate_monomials(b,estmemo)
        ml=p1.estimate_monomials(l,estmemo); mr=p1.estimate_monomials(r,estmemo)
        keep=p1.token_nonlinear(parent_token)*ml*mr
        for src,child in zip(n_src.args,(l,r)):
            if source_refs[src.nid]==1 and child.op=='tf':
                x,y=child.args
                if (x is a and y is b) or (x is b and y is a):
                    keep += p1.token_nonlinear(child.value)*ma*mb
        fold=p1.token_nonlinear(composed)*ma*mb
        benefit=keep-fold
        shared=any(source_refs[c.nid]>1 for c in n_src.args)
        fraction=benefit/max(1,keep)
        return keep,fold,benefit,shared,fraction

    def accept(n_src,l,r,parent_token,a,b,composed):
        stats.selector_candidates+=1
        keep,fold,benefit,shared,fraction=candidate_cost(n_src,l,r,parent_token,a,b,composed)
        stats.selector_estimated_keep_cost+=keep
        stats.selector_estimated_fold_cost+=fold
        if benefit<=0:
            stats.selector_rejected_nonpositive+=1; return None
        if benefit<p1.BENEFIT_MIN:
            stats.selector_rejected_min_benefit+=1; return None
        minfrac=p1.SHARED_FRACTION_MIN if shared else p1.UNSHARED_FRACTION_MIN
        if fraction<minfrac:
            stats.selector_rejected_fraction+=1; return None
        stats.selector_accepted+=1
        stats.selector_estimated_benefit+=benefit
        if shared: stats.selector_accepted_shared+=1
        return keep,fold,benefit,shared

    def rec(n):
        if n.nid in memo:
            stats.cse_hits+=1
            return memo[n.nid]
        if n.op=='var':
            out=clone_var(n)
        elif n.op=='const':
            out=vf.const(n.value); register_origin(out,n)
        elif n.op=='not':
            c=rec(n.args[0])
            if c.op=='tf':
                # Frozen P1 rule: complement preserves nonlinear coefficient, so this is rejected.
                stats.selector_candidates+=1; stats.selector_rejected_nonpositive+=1
            out=vf.not_(c)
            register_origin(out,n)
        elif n.op in ('and','or','xor'):
            l=rec(n.args[0]); r=rec(n.args[1])
            parent_token={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}[n.op]
            folded=None
            candidates=[]
            if l.op=='tf': candidates.append(l.args)
            if r.op=='tf': candidates.append(r.args)
            for a,b in candidates:
                tl=base.base_token_for(l,a,b); tr=base.base_token_for(r,a,b)
                if tl is None or tr is None: continue
                composed=base.token_apply(n.op,tl,tr)
                decision=accept(n,l,r,parent_token,a,b,composed)
                if decision is None: continue
                if a.nid not in v_origin or b.nid not in v_origin:
                    raise AssertionError('virtual base lacks source origin')
                keep,fold,benefit,shared=decision
                plan[n.nid]=PlanEntry(composed,v_origin[a.nid].nid,v_origin[b.nid].nid,keep,fold,benefit,shared)
                folded=vf.tf(composed,a,b)
                stats.successful_folds+=1; stats.same_operand_folds+=1
                if (l.op=='tf' and l.args==(b,a)) or (r.op=='tf' and r.args==(b,a)):
                    stats.transpose_alignments+=1
                break
            out=folded if folded is not None else vf.tf(parent_token,l,r)
            register_origin(out,n)
        elif n.op in ('andn','orn'):
            out=vf.nary(n.op,[rec(a) for a in n.args]); register_origin(out,n)
        elif n.op=='tf':
            out=vf.tf(n.value,rec(n.args[0]),rec(n.args[1])); register_origin(out,n)
        else:
            raise ValueError(n.op)
        memo[n.nid]=out
        return out

    rec(root)
    stats.plan_entries=len(plan); stats.virtual_nodes=len(vf.nodes)
    return plan,stats,source_nodes


def apply_tf_poly(token:int,a:set[int],b:set[int],st:base.AnfStats):
    v00=(token>>0)&1; v01=(token>>1)&1; v10=(token>>2)&1; v11=(token>>3)&1
    ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
    p={0} if ca else set()
    if cb: p=base.xor_poly(p,a)
    if cc: p=base.xor_poly(p,b)
    if cd: p=base.xor_poly(p,base.mul_poly(a,b,st))
    base.update_peak(p,st)
    return p


def lower_anf_with_plan(root:base.Node,plan:dict[int,PlanEntry],source_nodes:dict[int,base.Node]):
    st=base.AnfStats(); memo={}; planned_hits=0
    def rec(n):
        nonlocal planned_hits
        if n.nid in memo:
            st.cache_hits+=1; return memo[n.nid]
        st.anf_nodes_evaluated+=1
        entry=plan.get(n.nid)
        if entry is not None:
            planned_hits+=1
            a=rec(source_nodes[entry.a_nid]); b=rec(source_nodes[entry.b_nid])
            p=apply_tf_poly(entry.token,a,b,st)
        elif n.op=='const': p={0} if n.value else set()
        elif n.op=='var': p={1<<n.value}
        elif n.op=='not':
            p=rec(n.args[0]).copy(); (p.remove(0) if 0 in p else p.add(0)); base.update_peak(p,st)
        elif n.op=='xor': p=base.xor_poly(rec(n.args[0]),rec(n.args[1])); base.update_peak(p,st)
        elif n.op=='and': p=base.mul_poly(rec(n.args[0]),rec(n.args[1]),st)
        elif n.op=='or':
            a=rec(n.args[0]); b=rec(n.args[1]); p=base.xor_poly(base.xor_poly(a,b),base.mul_poly(a,b,st)); base.update_peak(p,st)
        elif n.op=='andn':
            level=[rec(c).copy() for c in n.args]
            if not level: p={0}
            else:
                while len(level)>1:
                    nxt=[]
                    for i in range(0,len(level),2):
                        nxt.append(level[i] if i+1==len(level) else base.mul_poly(level[i],level[i+1],st))
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
                            a,b=level[i],level[i+1]
                            q=base.xor_poly(base.xor_poly(a,b),base.mul_poly(a,b,st)); base.update_peak(q,st); nxt.append(q)
                    level=nxt
                p=level[0]
        elif n.op=='tf':
            p=apply_tf_poly(n.value,rec(n.args[0]),rec(n.args[1]),st)
        else: raise ValueError(n.op)
        memo[n.nid]=p
        st.peak_cache_entries=max(st.peak_cache_entries,len(memo)); base.update_peak(p,st)
        return p
    poly=rec(root)
    return poly,st,planned_hits


def normalize_plan_fields(row):
    for k in PLAN_FIELDS:
        if k not in row: row[k]=0
    if 'plan_ns' not in row: row['plan_ns']=row.get('optimize_ns',0)
    if 'compile_ns' not in row: row['compile_ns']=row.get('frontend_anf_ns',row.get('optimize_ns',0)+row.get('propagate_ns',0))
    if 'planned_fold_lowerings' not in row: row['planned_fold_lowerings']=0
    return row


def run_arm(root,arm,oracle,nvars,memory=False):
    if arm!=P2:
        r,opt=p1.run_arm(root,arm,oracle,nvars,memory=memory)
        normalize_plan_fields(r)
        r['compile_ns']=r['frontend_anf_ns']; r['plan_ns']=r['optimize_ns']
        return r,opt
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); plan,pst,source_nodes=build_profit_plan(root); t1=time.perf_counter_ns()
    poly,ast,planned_hits=lower_anf_with_plan(root,plan,source_nodes); t2=time.perf_counter_ns()
    peak_py=None
    if memory:
        _,peak_py=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars); ok=(got==oracle)
    row={'arm':arm,'ok':ok,'optimize_ns':t1-t0,'plan_ns':t1-t0,'propagate_ns':t2-t1,'frontend_anf_ns':t2-t0,'compile_ns':t2-t0,
         'python_peak_bytes':peak_py,'final_monomials':len(poly),'final_degree':max((m.bit_count() for m in poly),default=0),
         'serialized_bytes':base.poly_serialized_bytes(poly),'digest':base.poly_digest(poly),'planned_fold_lowerings':planned_hits,
         **dataclasses.asdict(pst),**dataclasses.asdict(ast)}
    return row,root


def reference_selected_ids(path:Path):
    x=json.loads(path.read_text())
    out=[]
    for c in x['circuits']:
        for s in c['selected']: out.append(f"{c['circuit']}:{s['root']}")
    return sorted(out)


def freeze_cases(epfl_dir:Path,outdir:Path):
    cases,selection,selsha=p1.freeze_natural_selection(epfl_dir,outdir)
    got=sorted(c['case_id'] for c in cases)
    ref=reference_selected_ids(outdir/'N2_P1_NATURAL_SELECTION_REFERENCE.json')
    if got!=ref: raise AssertionError(f'natural selection drift: got={got} ref={ref}')
    return cases,selection,selsha


def fuzz_p2():
    rng=random.Random(SEED^0xF222); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        d,_=run_arm(root,DIRECT,oracle,nvars,memory=False)
        r,_=run_arm(root,P2,oracle,nvars,memory=False)
        if (not r['ok']) or r['digest']!=d['digest']:
            failures.append({'case':i,'nvars':nvars,'ok':r['ok'],'digest_match':r['digest']==d['digest']})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def natural_campaign(cases):
    symbolic=[]; timing=[]
    for c in cases:
        digest=None
        for arm in ARMS:
            r,_=run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=True)
            r.update({k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}); symbolic.append(r)
            if digest is None: digest=r['digest']
            elif r['digest']!=digest: raise AssertionError(f"natural digest mismatch {c['case_id']} {arm}")
            if not r['ok']: raise AssertionError(f"natural oracle mismatch {c['case_id']} {arm}")
        rng=random.Random(SEED ^ int(hashlib.sha256(c['case_id'].encode()).hexdigest()[:8],16) ^ 0x2200)
        schedule=[a for _ in range(NATURAL_TIMING_REPS) for a in ARMS]; rng.shuffle(schedule)
        for rep,arm in enumerate(schedule):
            outer0=time.perf_counter_ns(); rr,_=run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=False); outer=time.perf_counter_ns()-outer0
            timing.append({'case_id':c['case_id'],'circuit':c['circuit'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':c['depth'],
                           'rep':rep,'arm':arm,'elapsed_ns':outer,'compile_ns':rr['compile_ns'],'plan_ns':rr['plan_ns'],
                           'optimize_ns':rr['optimize_ns'],'propagate_ns':rr['propagate_ns'],'ok':rr['ok']})
    return symbolic,timing


def gatep_campaign():
    rng=random.Random(base.SEED^0x6A7E); cases=[]
    for d in p1.GATEP_DEPTHS:
        for i in range(p1.GATEP_CASES_PER_DEPTH):
            f,r,n=base.gatep_case(rng,d,i); oracle=base.eval_node_bitset(r,n); cases.append((d,i,r,n,oracle))
    symbolic=[]; timing=[]
    for d,i,root,n,oracle in cases:
        digest=None
        for arm in ARMS:
            r,_=run_arm(root,arm,oracle,n,memory=True); r.update({'depth':d,'case':i,'case_id':f'{d}:{i}'}); symbolic.append(r)
            if digest is None: digest=r['digest']
            elif r['digest']!=digest: raise AssertionError(f'Gate-P digest mismatch {d}:{i} {arm}')
            if not r['ok']: raise AssertionError(f'Gate-P oracle mismatch {d}:{i} {arm}')
        schedule=[a for _ in range(GATEP_TIMING_REPS) for a in ARMS]
        rrng=random.Random(SEED+d*1000+i+0x2200); rrng.shuffle(schedule)
        for rep,arm in enumerate(schedule):
            outer0=time.perf_counter_ns(); rr,_=run_arm(root,arm,oracle,n,memory=False); outer=time.perf_counter_ns()-outer0
            timing.append({'depth':d,'case':i,'case_id':f'{d}:{i}','rep':rep,'arm':arm,'elapsed_ns':outer,
                           'compile_ns':rr['compile_ns'],'plan_ns':rr['plan_ns'],'optimize_ns':rr['optimize_ns'],
                           'propagate_ns':rr['propagate_ns'],'ok':rr['ok']})
    return symbolic,timing


def geomean(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def median(xs): return statistics.median(xs) if xs else None

def bootstrap_geomean(ratios,n=5000,seed=SEED):
    if not ratios: return None
    rng=random.Random(seed); m=len(ratios); vals=[]
    for _ in range(n): vals.append(geomean([ratios[rng.randrange(m)] for __ in range(m)]))
    vals.sort(); return {'estimate':geomean(ratios),'ci95':[vals[int(.025*n)],vals[min(n-1,int(.975*n))]]}

def case_medians(rows,metric):
    g=defaultdict(list)
    for r in rows:
        if r.get('ok',True): g[(r['case_id'],r['arm'])].append(r[metric])
    return {k:median(v) for k,v in g.items()}

def compare(rows,num,den,metric='compile_ns',filter_fn=lambda r:True):
    rs=[r for r in rows if filter_fn(r)]; med=case_medians(rs,metric); ratios=[]; cases=sorted({r['case_id'] for r in rs})
    for c in cases:
        a=med.get((c,num)); b=med.get((c,den))
        if a and b: ratios.append(a/b)
    return {'metric':metric,'n':len(ratios),'geomean_ratio':geomean(ratios),'bootstrap':bootstrap_geomean(ratios),'case_ratios':ratios}

def symbolic_ratio(rows,metric,num=P2,den=DIRECT):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]
    for c in sorted({r['case_id'] for r in rows}):
        a=by.get((c,num)); b=by.get((c,den))
        if a and b and b.get(metric) not in (None,0): vals.append(a[metric]/b[metric])
    return {'n':len(vals),'geomean_ratio':geomean(vals),'median_ratio':median(vals),'case_ratios':vals}


def summarize(nsym,ntime,gsym,gtime,fuzz):
    nat={}
    for metric in ('compile_ns','propagate_ns','elapsed_ns'):
        for den in (DIRECT,P1,GENERIC): nat[f'p2_over_{den}:{metric}']=compare(ntime,P2,den,metric)
    gate={}
    for metric in ('compile_ns','propagate_ns','elapsed_ns'):
        for den in (DIRECT,P1,GENERIC): gate[f'p2_over_{den}:{metric}']=compare(gtime,P2,den,metric)
    for circuit in p1.NATURAL_SOURCES:
        nat[f'p2_over_direct:{circuit}:compile_ns']=compare(ntime,P2,DIRECT,'compile_ns',lambda r,c=circuit:r['circuit']==c)
    sm={m:symbolic_ratio(nsym,m) for m in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','peak_cache_entries','python_peak_bytes')}
    p2nat=[r for r in nsym if r['arm']==P2]; p2gate=[r for r in gsym if r['arm']==P2]
    keys=('selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit','plan_entries','planned_fold_lowerings')
    natdiag={k:sum(r.get(k,0) for r in p2nat) for k in keys}; gatediag={k:sum(r.get(k,0) for r in p2gate) for k in keys}
    by={(r['case_id'],r['arm']):r for r in nsym}; cases=sorted({r['case_id'] for r in nsym})
    pairvals=[]; peakvals=[]
    for c in cases:
        d=by[(c,DIRECT)]; q=by[(c,P2)]
        if d['pair_terms']>0: pairvals.append(q['pair_terms']/d['pair_terms'])
        if d['peak_monomials']>0: peakvals.append(q['peak_monomials']/d['peak_monomials'])
    pr=geomean(pairvals); kr=geomean(peakvals)
    primary=nat[f'p2_over_{DIRECT}:compile_ns']; ci=primary['bootstrap']['ci95'] if primary['bootstrap'] else [None,None]
    natural_signal=bool(natdiag['selector_accepted']>0 and not fuzz['failures'] and all(r['ok'] for r in nsym) and
                        primary['geomean_ratio'] is not None and primary['geomean_ratio']<=0.95 and ci[1] is not None and ci[1]<1.0 and
                        (pr is None or pr<=1.05) and (kr is None or kr<=1.05))
    gprimary=gate[f'p2_over_{DIRECT}:compile_ns']; gci=gprimary['bootstrap']['ci95'] if gprimary['bootstrap'] else [None,None]
    gate_signal=bool(gatediag['selector_accepted']>0 and all(r['ok'] for r in gsym) and gprimary['geomean_ratio'] is not None and
                     gprimary['geomean_ratio']<=0.95 and gci[1] is not None and gci[1]<1.0)
    return {'natural_timing':nat,'gatep_timing':gate,'natural_symbolic_p2_over_direct':sm,'natural_p2_diag':natdiag,'gatep_p2_diag':gatediag,
            'natural_pair_geomean_vs_direct':pr,'natural_peak_geomean_vs_direct':kr,
            'predeclared_natural_actual_fold_speed_signal':natural_signal,'predeclared_gatep_mechanism_speed_signal':gate_signal,'fuzz':fuzz}


def fmt(x): return 'n/a' if x is None else f'{x:.4f}'

def report(meta,selection,summary,nsym,gsym):
    nat=summary['natural_timing']; gate=summary['gatep_timing']
    lines=['# N2/P2 — Direct-Baseline Inline Profitability Plan','',f"Run date: {meta['run_date']}",
           f"Preregistration SHA-256: `{meta['prereg_sha256']}`",f"Harness SHA-256: `{meta['harness_sha256']}`",'']
    lines += ['## Frozen design','',
              '- P2 reuses the P1 selector thresholds unchanged: benefit >=16; >=10% relative benefit when unshared; >=20% when shared; monomial estimate cap 4096.',
              '- The P2 executable ANF input is the original source DAG. A planning pass records accepted folds only; there is no rewritten/CSE-normalized executable DAG.',
              '- Primary endpoint is planning + ANF lowering (`compile_ns`) versus direct/no-rewrite sparse ANF.','']
    lines += ['## Natural corpus','',f"- Cases: {len({r['case_id'] for r in nsym})} across {len({r['circuit'] for r in nsym})} contributing circuits.",
              '- Selected case IDs exactly matched the frozen N2/P1 structural selection reference.','']
    lines += ['| comparison | cases | ratio | bootstrap 95% CI |','|---|---:|---:|---:|']
    for den in (DIRECT,P1,GENERIC):
        x=nat[f'p2_over_{den}:compile_ns']; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
        lines.append(f'| P2 / {den} compile | {x["n"]} | {fmt(x["geomean_ratio"])} | {fmt(ci[0])} – {fmt(ci[1])} |')
    x=nat[f'p2_over_{DIRECT}:propagate_ns']; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
    lines += ['',f'P2/direct **propagation-only** ratio: **{fmt(x["geomean_ratio"])}** (95% CI {fmt(ci[0])}–{fmt(ci[1])}).']
    x=nat[f'p2_over_{DIRECT}:elapsed_ns']; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
    lines += [f'P2/direct outer harness ratio: **{fmt(x["geomean_ratio"])}** (95% CI {fmt(ci[0])}–{fmt(ci[1])}).','']
    lines += ['Per-circuit P2/direct compile ratios:']
    for c in p1.NATURAL_SOURCES:
        x=nat[f'p2_over_direct:{c}:compile_ns']; lines.append(f'- {c}: {fmt(x["geomean_ratio"])} (n={x["n"]})')
    nd=summary['natural_p2_diag']
    lines += ['', 'Natural selector totals: '+', '.join(f'{k}={v}' for k,v in nd.items())+'.','',
              '| natural symbolic metric | cases | P2/direct geomean | median |','|---|---:|---:|---:|']
    for m,x in summary['natural_symbolic_p2_over_direct'].items(): lines.append(f'| {m} | {x["n"]} | {fmt(x["geomean_ratio"])} | {fmt(x["median_ratio"])} |')
    lines += ['',f"**Predeclared natural actual-fold speed signal: {'PASS' if summary['predeclared_natural_actual_fold_speed_signal'] else 'NO PASS'}.**",'']
    lines += ['## Gate-P mechanism replay','', '| comparison | cases | ratio | bootstrap 95% CI |','|---|---:|---:|---:|']
    for den in (DIRECT,P1,GENERIC):
        x=gate[f'p2_over_{den}:compile_ns']; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
        lines.append(f'| P2 / {den} compile | {x["n"]} | {fmt(x["geomean_ratio"])} | {fmt(ci[0])} – {fmt(ci[1])} |')
    x=gate[f'p2_over_{DIRECT}:propagate_ns']; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
    gd=summary['gatep_p2_diag']
    lines += ['',f'P2/direct propagation-only ratio: **{fmt(x["geomean_ratio"])}** (95% CI {fmt(ci[0])}–{fmt(ci[1])}).',
              'Gate-P selector totals: '+', '.join(f'{k}={v}' for k,v in gd.items())+'.','',
              f"**Predeclared Gate-P mechanism speed signal: {'PASS' if summary['predeclared_gatep_mechanism_speed_signal'] else 'NO PASS'}.**",'']
    lines += ['## Correctness','',f"- P2 fresh fuzz: {summary['fuzz']['cases']} cases; failures: {len(summary['fuzz']['failures'])}.",
              f"- Natural symbolic arm checks: {len(nsym)}; failures: {sum(not r['ok'] for r in nsym)}.",
              f"- Gate-P symbolic arm checks: {len(gsym)}; failures: {sum(not r['ok'] for r in gsym)}.",'']
    lines += ['## Frozen interpretation rule','',
              '- Propagation faster but compile not faster => accepted folding reduces ANF work, but planning overhead does not amortize.',
              '- Both faster => accepted folding saves enough work to pay for planning.',
              '- Neither faster => this frozen plan does not improve the direct path.',
              '- Zero natural accepted folds => only abstention overhead is measured; no natural folding-speed claim is made.']
    return '\n'.join(lines)+'\n'


def main():
    preg=HERE/'N2_P2_PREREGISTRATION.md'
    if sha256_file(preg)!=PREREG_SHA256: raise SystemExit('P2 preregistration hash mismatch; refusing to run')
    cases,selection,selsha=freeze_cases(HERE/'epfl',HERE)
    fuzz=fuzz_p2()
    if not fuzz['passed']: raise SystemExit(f'P2 fuzz failed: {fuzz["failures"][:3]}')
    start=time.time()
    nsym,ntime=natural_campaign(cases)
    gsym,gtime=gatep_campaign()
    summary=summarize(nsym,ntime,gsym,gtime,fuzz)
    meta={'schema':'cm-n2-p2-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_s':time.time()-start,
          'prereg_sha256':PREREG_SHA256,'harness_sha256':sha256_file(Path(__file__)),'natural_selection_sha256':selsha,
          'epfl_commit':p1.EPFL_COMMIT,'seed':SEED,'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
          'protocol':{'arms':ARMS,'natural_timing_reps':NATURAL_TIMING_REPS,'gatep_timing_reps':GATEP_TIMING_REPS,'fuzz_cases':FUZZ_CASES,
                      'selector':{'monomial_cap':p1.MONOMIAL_CAP,'benefit_min':p1.BENEFIT_MIN,'shared_fraction_min':p1.SHARED_FRACTION_MIN,'unshared_fraction_min':p1.UNSHARED_FRACTION_MIN}}}
    payload={'meta':meta,'selection':selection,'summary':summary,'natural_symbolic_rows':nsym,'natural_timing_rows':ntime,'gatep_symbolic_rows':gsym,'gatep_timing_rows':gtime,'fuzz':fuzz}
    (HERE/'n2_p2_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (HERE/'N2_P2_RESULTS.md').write_text(report(meta,selection,summary,nsym,gsym),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
