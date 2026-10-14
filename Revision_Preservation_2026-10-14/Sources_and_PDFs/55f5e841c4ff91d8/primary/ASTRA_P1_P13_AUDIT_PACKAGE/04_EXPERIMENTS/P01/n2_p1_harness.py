from __future__ import annotations
import argparse, dataclasses, hashlib, json, math, os, platform, random, statistics, sys, time, tracemalloc
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
N1_DIR = HERE.parent / 'cm_n1_gatep'
if str(N1_DIR) not in sys.path:
    sys.path.insert(0, str(N1_DIR))
import n1_gatep_harness as base

SEED = 20260918
EPFL_COMMIT = '0060e156826e733d69bf5b3322d1bdd0d03a1f9a'
NATURAL_SUPPORT_MIN = 9
NATURAL_SUPPORT_MAX = 12
MAX_SOURCE_NODES = 128
CASES_PER_CIRCUIT = 2
NATURAL_TIMING_REPS = 15
GATEP_TIMING_REPS = 20
GATEP_DEPTHS = (6,8,10)
GATEP_CASES_PER_DEPTH = 12
FUZZ_CASES = 500
MONOMIAL_CAP = 4096
BENEFIT_MIN = 16
SHARED_FRACTION_MIN = 0.20
UNSHARED_FRACTION_MIN = 0.10
PREREG_SHA256 = 'ab1f5e6d698b0130c768ef78ac0d1e912af3c19cd3a8c260e90444765a6a6e6a'

NATURAL_SOURCES = {
    'adder': ('adder_size_2022.blif', '1a16f1fea72e7fbf67aac019ec97c6aaf871fcdd'),
    'bar': ('bar_size_2015.blif', 'a2b2177aa0be92ac60f5c694bcf6eb9806aaa9c2'),
    'cavlc': ('cavlc_size_2024.blif', '3ebfd39f6193da20b2ae0491dd41bc18eeffce3e'),
    'int2float': ('int2float_size_2025.blif', '5c202a31a74dc2b4da0d1ac59377e92c6c37c6d9'),
    'priority': ('priority_size_2024.blif', '4156ea7455044d0a9a49855cca5876ffaa8a003b'),
    'router': ('router_size_2024.blif', '553e80bc24de67a307b4ce7aafef8adb9603ad26'),
}

ARMS = ('direct_sparse_anf','generic_2support_sparse','cm_frontend_sparse','cm_frontend_guarded_sparse','cm_profit_sparse')
TIMED_GATEP_ARMS = ('generic_2support_sparse','cm_frontend_sparse','cm_frontend_guarded_sparse','cm_profit_sparse')


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def git_blob_hash(path:Path)->str:
    data=path.read_bytes(); return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def token_nonlinear(token:int)->int:
    v00=(token>>0)&1; v01=(token>>1)&1; v10=(token>>2)&1; v11=(token>>3)&1
    return v11 ^ v10 ^ v01 ^ v00


def estimate_monomials(n:base.Node, memo=None)->int:
    if memo is None: memo={}
    if n.nid in memo: return memo[n.nid]
    cap=MONOMIAL_CAP
    if n.op=='const': m=1 if n.value else 0
    elif n.op=='var': m=1
    elif n.op=='not': m=min(cap, estimate_monomials(n.args[0],memo)+1)
    elif n.op=='xor': m=min(cap, estimate_monomials(n.args[0],memo)+estimate_monomials(n.args[1],memo))
    elif n.op=='and': m=min(cap, estimate_monomials(n.args[0],memo)*estimate_monomials(n.args[1],memo))
    elif n.op=='or':
        a=estimate_monomials(n.args[0],memo); b=estimate_monomials(n.args[1],memo); m=min(cap,a+b+a*b)
    elif n.op=='andn':
        m=1
        for c in n.args: m=min(cap,m*estimate_monomials(c,memo))
    elif n.op=='orn':
        m=0
        for c in n.args:
            q=estimate_monomials(c,memo); m=min(cap,m+q+m*q)
    elif n.op=='tf':
        a=estimate_monomials(n.args[0],memo); b=estimate_monomials(n.args[1],memo); t=n.value
        v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
        ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
        m=min(cap,ca + cb*a + cc*b + cd*a*b)
    else: raise ValueError(n.op)
    memo[n.nid]=m; return m


@dataclass
class ProfitOptStats:
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


def fold_frontend_profit(root:base.Node):
    f=base.Factory(); stats=ProfitOptStats(); memo={}
    source_refs=defaultdict(int); seen=set(); stack=[root]
    while stack:
        n=stack.pop()
        if n.nid in seen: continue
        seen.add(n.nid)
        for c in n.args:
            source_refs[c.nid]+=1; stack.append(c)
    var_cache={}
    def clone_var(v):
        if v.value not in var_cache: var_cache[v.value]=f.var(v.value)
        return var_cache[v.value]
    estmemo={}
    def candidate_cost(n_src, l, r, parent_token, a, b, composed):
        ma=estimate_monomials(a,estmemo); mb=estimate_monomials(b,estmemo)
        ml=estimate_monomials(l,estmemo); mr=estimate_monomials(r,estmemo)
        keep=token_nonlinear(parent_token)*ml*mr
        # A direct child TF's local product is removable only if the source child has fanout one.
        for src,child in zip(n_src.args,(l,r)):
            if source_refs[src.nid] == 1 and child.op=='tf':
                x,y=child.args
                # Only charge the child-local product when it is expressed on the same base pair.
                if (x is a and y is b) or (x is b and y is a):
                    keep += token_nonlinear(child.value)*ma*mb
        fold=token_nonlinear(composed)*ma*mb
        benefit=keep-fold
        shared=any(source_refs[c.nid]>1 for c in n_src.args)
        fraction=benefit/max(1,keep)
        return keep,fold,benefit,shared,fraction
    def accept_candidate(n_src,l,r,parent_token,a,b,composed):
        stats.selector_candidates += 1
        keep,fold,benefit,shared,fraction=candidate_cost(n_src,l,r,parent_token,a,b,composed)
        stats.selector_estimated_keep_cost += keep
        stats.selector_estimated_fold_cost += fold
        if benefit<=0:
            stats.selector_rejected_nonpositive += 1; return False
        if benefit<BENEFIT_MIN:
            stats.selector_rejected_min_benefit += 1; return False
        minfrac=SHARED_FRACTION_MIN if shared else UNSHARED_FRACTION_MIN
        if fraction<minfrac:
            stats.selector_rejected_fraction += 1; return False
        stats.selector_accepted += 1
        stats.selector_estimated_benefit += benefit
        if shared: stats.selector_accepted_shared += 1
        return True
    def rec(n):
        if n.nid in memo:
            stats.cse_hits+=1; return memo[n.nid]
        if n.op=='var': out=clone_var(n)
        elif n.op=='const': out=f.const(n.value)
        elif n.op=='not':
            c=rec(n.args[0])
            # Complementing a 2-input TF preserves its nonlinear coefficient, so under the frozen
            # benefit model NOT-over-TF cannot have positive nonlinear benefit and is conservatively left.
            if c.op=='tf':
                stats.selector_candidates += 1; stats.selector_rejected_nonpositive += 1
            out=f.not_(c)
        elif n.op in ('and','or','xor'):
            l=rec(n.args[0]); r=rec(n.args[1]); parent_token={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}[n.op]
            folded=None
            candidates=[]
            if l.op=='tf': candidates.append(l.args)
            if r.op=='tf': candidates.append(r.args)
            for a,b in candidates:
                tl=base.base_token_for(l,a,b); tr=base.base_token_for(r,a,b)
                if tl is None or tr is None: continue
                composed=base.token_apply(n.op,tl,tr)
                if accept_candidate(n,l,r,parent_token,a,b,composed):
                    folded=f.tf(composed,a,b); stats.successful_folds+=1; stats.same_operand_folds+=1
                    if (l.op=='tf' and l.args==(b,a)) or (r.op=='tf' and r.args==(b,a)):
                        stats.transpose_alignments+=1
                    break
            out=folded if folded is not None else f.tf(parent_token,l,r)
        elif n.op in ('andn','orn'):
            out=f.nary(n.op,[rec(a) for a in n.args])
        elif n.op=='tf': out=f.tf(n.value,rec(n.args[0]),rec(n.args[1]))
        else: raise ValueError(n.op)
        memo[n.nid]=out; return out
    preliminary=rec(root)
    normalized,cstats=base.cse_flatten(preliminary)
    stats.cse_hits += cstats.cse_hits
    stats.associative_flattened_nodes += cstats.associative_flattened_nodes
    stats.commutative_reorders += cstats.commutative_reorders
    stats.output_unique_nodes=base.reachable_nodes(normalized)
    return normalized,stats


def prepare_arm(root,arm):
    if arm=='cm_profit_sparse': return fold_frontend_profit(root)
    return base.prepare_arm(root,arm)


def run_arm(root,arm,oracle,nvars,memory=False):
    if arm!='cm_profit_sparse':
        r,opt=base.run_arm(root,arm,oracle,nvars,memory=memory)
        # Normalize selector fields for rectangular tables.
        for k in dataclasses.asdict(ProfitOptStats()).keys():
            if k not in r: r[k]=0
        return r,opt
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); optimized,ost=fold_frontend_profit(root); t1=time.perf_counter_ns()
    poly,ast=base.lower_anf(optimized); t2=time.perf_counter_ns()
    peak_py=None
    if memory:
        _,peak_py=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars); ok=(got==oracle)
    return {'arm':arm,'ok':ok,'optimize_ns':t1-t0,'propagate_ns':t2-t1,'frontend_anf_ns':t2-t0,
            'python_peak_bytes':peak_py,'final_monomials':len(poly),
            'final_degree':max((m.bit_count() for m in poly),default=0),'serialized_bytes':base.poly_serialized_bytes(poly),
            'digest':base.poly_digest(poly),**dataclasses.asdict(ost),**dataclasses.asdict(ast)},optimized


# ----- Natural BLIF cone selection -----
def capped_support(blif:base.Blif, root:str, cap=13, memo=None):
    inputs=set(blif.inputs); memo={} if memo is None else memo
    active=set()
    def rec(s):
        if s in inputs: return frozenset((s,))
        if s in memo: return memo[s]
        if s in active: raise ValueError('cycle')
        active.add(s); nd=blif.nodes[s]; u=set()
        relevant={j for cube in nd.cubes for j,ch in enumerate(cube) if ch in '01'}
        for j,ch in enumerate(nd.inputs):
            if j not in relevant: continue
            u.update(rec(ch))
            if len(u)>=cap:
                # Identity of all members is irrelevant once over the admission cap.
                u=set(sorted(u)[:cap]); break
        active.remove(s); memo[s]=frozenset(u); return memo[s]
    return rec(root)


def cone_node_count(blif:base.Blif, root:str, cap=MAX_SOURCE_NODES+1):
    inputs=set(blif.inputs); seen=set(); stack=[root]
    while stack:
        s=stack.pop()
        if s in inputs or s in seen: continue
        seen.add(s)
        if len(seen)>=cap: return len(seen)
        nd=blif.nodes.get(s)
        if nd is None: raise KeyError(s)
        relevant={j for cube in nd.cubes for j,ch in enumerate(cube) if ch in '01'}
        stack.extend(ch for j,ch in enumerate(nd.inputs) if j in relevant)
    return len(seen)


def cone_depth(blif:base.Blif, root:str, memo=None):
    inputs=set(blif.inputs); memo={} if memo is None else memo
    def rec(s):
        if s in inputs: return 0
        if s in memo: return memo[s]
        nd=blif.nodes[s]; relevant={j for cube in nd.cubes for j,ch in enumerate(cube) if ch in '01'}
        d=1+max((rec(ch) for j,ch in enumerate(nd.inputs) if j in relevant),default=0); memo[s]=d; return d
    return rec(root)


def select_cones(path:Path,circuit:str):
    blif=base.parse_blif(path); smemo={}; dmemo={}; candidates=[]
    for root in sorted(blif.nodes):
        sup=capped_support(blif,root,13,smemo)
        if not (NATURAL_SUPPORT_MIN<=len(sup)<=NATURAL_SUPPORT_MAX): continue
        n=cone_node_count(blif,root)
        if n>MAX_SOURCE_NODES: continue
        d=cone_depth(blif,root,dmemo)
        candidates.append({'root':root,'support_names':tuple(name for name in blif.inputs if name in sup),'support':len(sup),'source_nodes':n,'depth':d})
    candidates.sort(key=lambda x:(x['source_nodes'],x['depth'],x['root']))
    if not candidates: return blif,[],0
    idx=[0] if len(candidates)==1 else [0,len(candidates)-1]
    selected=[candidates[i] for i in idx]
    return blif,selected,len(candidates)


def build_cone_expr(blif:base.Blif,root:str,support_names:tuple[str,...]):
    f=base.Factory(); varmap={name:f.var(i) for i,name in enumerate(support_names)}; memo={}; active=set()
    def rec(s):
        if s in varmap: return varmap[s]
        if s in memo: return memo[s]
        if s in active: raise ValueError('cycle')
        if s in blif.inputs: raise ValueError(f'undeclared support input {s}')
        active.add(s); nd=blif.nodes[s]; cubes=[]
        for patt in nd.cubes:
            lits=[]
            for bit,ch in zip(patt,nd.inputs):
                if bit=='-': continue
                c=rec(ch); lits.append(c if bit=='1' else f.not_(c))
            cubes.append(base.balanced(f,'and',lits,1))
        val=base.balanced(f,'or',cubes,0)
        if nd.cube_output==0: val=f.not_(val)
        active.remove(s); memo[s]=val; return val
    return f,rec(root)


def eval_blif_cone(blif:base.Blif,root:str,support_names:tuple[str,...]):
    n=len(support_names); env=base.bitset_env(n); vals={name:env[i] for i,name in enumerate(support_names)}; mask=(1<<(1<<n))-1; active=set()
    def rec(s):
        if s in vals: return vals[s]
        if s in active: raise ValueError('cycle')
        if s in blif.inputs: raise ValueError(f'undeclared support input {s}')
        active.add(s); nd=blif.nodes[s]; value=0
        for patt in nd.cubes:
            cube=mask
            for bit,ch in zip(patt,nd.inputs):
                if bit=='-': continue
                cv=rec(ch); cube &= cv if bit=='1' else ((~cv)&mask)
            value |= cube
        if nd.cube_output==0: value=(~value)&mask
        active.remove(s); vals[s]=value; return value
    return rec(root)


def freeze_natural_selection(epfl_dir:Path,outdir:Path):
    docs=[]; cases=[]
    for circuit,(fname,expected_blob) in NATURAL_SOURCES.items():
        path=epfl_dir/fname
        if not path.exists(): raise FileNotFoundError(path)
        blob=git_blob_hash(path)
        if blob!=expected_blob: raise ValueError(f'{fname} git blob mismatch {blob} != {expected_blob}')
        blif,sel,candidate_count=select_cones(path,circuit)
        for item in sel:
            _f,root=build_cone_expr(blif,item['root'],item['support_names'])
            oracle=eval_blif_cone(blif,item['root'],item['support_names'])
            case_id=f"{circuit}:{item['root']}"
            case={**item,'circuit':circuit,'case_id':case_id,'file':fname,'git_blob':blob,'file_sha256':sha256_file(path),'root_node':root,'oracle':oracle}
            cases.append(case)
        docs.append({'circuit':circuit,'file':fname,'git_blob':blob,'candidate_count':candidate_count,
                     'selected':[{k:v for k,v in x.items() if k!='support_names'}|{'support_names':list(x['support_names'])} for x in sel]})
    manifest={'schema':'cm-n2-p1-natural-selection/v1','created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
              'epfl_commit':EPFL_COMMIT,'selection_contract':'structural only; first/last by (source_nodes,depth,root); support 9-12; source nodes <=128',
              'circuits':docs}
    p=outdir/'natural_selection_frozen.json'; p.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return cases,manifest,sha256_file(p)


def natural_campaign(cases):
    symbolic=[]; timing=[]
    # Symbolic/memory first; selection is already frozen on disk.
    for c in cases:
        base_digest=None
        for arm in ARMS:
            r,_=run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=True)
            r.update({k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')})
            symbolic.append(r)
            if base_digest is None: base_digest=r['digest']
            elif r['digest']!=base_digest: raise AssertionError(f"natural digest mismatch {c['case_id']} {arm}")
            if not r['ok']: raise AssertionError(f"natural oracle mismatch {c['case_id']} {arm}")
        rng=random.Random(SEED ^ int(hashlib.sha256(c['case_id'].encode()).hexdigest()[:8],16))
        schedule=[a for _ in range(NATURAL_TIMING_REPS) for a in ARMS]; rng.shuffle(schedule)
        for rep,arm in enumerate(schedule):
            t0=time.perf_counter_ns(); rr,_=run_arm(c['root_node'],arm,c['oracle'],c['support'],memory=False); elapsed=time.perf_counter_ns()-t0
            timing.append({'case_id':c['case_id'],'circuit':c['circuit'],'support':c['support'],'source_nodes':c['source_nodes'],'depth':c['depth'],
                           'rep':rep,'arm':arm,'elapsed_ns':elapsed,'optimize_ns':rr['optimize_ns'],'propagate_ns':rr['propagate_ns'],'ok':rr['ok']})
    return symbolic,timing


def gatep_campaign():
    rng=random.Random(base.SEED^0x6A7E); cases=[]
    for d in GATEP_DEPTHS:
        for i in range(GATEP_CASES_PER_DEPTH):
            f,r,n=base.gatep_case(rng,d,i); oracle=base.eval_node_bitset(r,n); cases.append((d,i,r,n,oracle))
    symbolic=[]; timing=[]
    for d,i,root,n,oracle in cases:
        base_digest=None
        for arm in ARMS:
            r,_=run_arm(root,arm,oracle,n,memory=True); r.update({'depth':d,'case':i,'case_id':f'{d}:{i}'}); symbolic.append(r)
            if base_digest is None: base_digest=r['digest']
            elif r['digest']!=base_digest: raise AssertionError('Gate-P ANF digest mismatch')
            if not r['ok']: raise AssertionError('Gate-P oracle mismatch')
        schedule=[a for _ in range(GATEP_TIMING_REPS) for a in TIMED_GATEP_ARMS]
        local_rng=random.Random(SEED+d*1000+i); local_rng.shuffle(schedule)
        for rep,arm in enumerate(schedule):
            t0=time.perf_counter_ns(); rr,_=run_arm(root,arm,oracle,n,memory=False); elapsed=time.perf_counter_ns()-t0
            timing.append({'depth':d,'case':i,'case_id':f'{d}:{i}','rep':rep,'arm':arm,'elapsed_ns':elapsed,
                           'optimize_ns':rr['optimize_ns'],'propagate_ns':rr['propagate_ns'],'ok':rr['ok']})
    return symbolic,timing


def fuzz_profit():
    rng=random.Random(SEED^0xF122); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,7),f); oracle=base.eval_node_bitset(root,nvars)
        r,_=run_arm(root,'cm_profit_sparse',oracle,nvars,memory=False)
        if not r['ok']:
            failures.append({'case':i,'nvars':nvars})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def geomean(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def median(xs): return statistics.median(xs) if xs else None

def bootstrap_geomean(ratios,n=5000,seed=SEED):
    rng=random.Random(seed); vals=[]; m=len(ratios)
    if not m:return None
    for _ in range(n): vals.append(geomean([ratios[rng.randrange(m)] for __ in range(m)]))
    vals.sort(); return {'estimate':geomean(ratios),'ci95':[vals[int(.025*n)],vals[min(n-1,int(.975*n))]]}

def case_medians(rows,metric='elapsed_ns'):
    g=defaultdict(list)
    for r in rows:
        if r.get('ok',True): g[(r['case_id'],r['arm'])].append(r[metric])
    return {(c,a):median(v) for (c,a),v in g.items()}

def compare_timing(rows,num,den,filter_fn=lambda r:True):
    rs=[r for r in rows if filter_fn(r)]; med=case_medians(rs); cases=sorted({r['case_id'] for r in rs}); ratios=[]
    for c in cases:
        a=med.get((c,num)); b=med.get((c,den))
        if a and b: ratios.append(a/b)
    return {'n':len(ratios),'geomean_ratio':geomean(ratios),'bootstrap':bootstrap_geomean(ratios),'case_ratios':ratios}

def symbolic_ratio(rows,metric,num='cm_profit_sparse',den='generic_2support_sparse'):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]
    for c in sorted({r['case_id'] for r in rows}):
        a=by.get((c,num)); b=by.get((c,den))
        if a and b and b[metric]>0: vals.append(a[metric]/b[metric])
    return {'n':len(vals),'geomean_ratio':geomean(vals),'median_ratio':median(vals)}


def summarize(nsym,ntime,gsym,gtime,fuzz):
    natcmp={}
    for den in ('generic_2support_sparse','direct_sparse_anf','cm_frontend_sparse','cm_frontend_guarded_sparse'):
        natcmp[f'p1_over_{den}']=compare_timing(ntime,'cm_profit_sparse',den)
    gatecmp={}
    for den in ('generic_2support_sparse','cm_frontend_sparse','cm_frontend_guarded_sparse'):
        gatecmp[f'p1_over_{den}']=compare_timing(gtime,'cm_profit_sparse',den)
    # Per-circuit P1/generic.
    for circuit in NATURAL_SOURCES:
        natcmp[f'p1_over_generic:{circuit}']=compare_timing(ntime,'cm_profit_sparse','generic_2support_sparse',lambda r,c=circuit:r['circuit']==c)
    smetrics={m:symbolic_ratio(nsym,m) for m in ('multiplications','pair_terms','peak_monomials','output_unique_nodes','python_peak_bytes')}
    by={(r['case_id'],r['arm']):r for r in nsym}; cases=sorted({r['case_id'] for r in nsym})
    lost={}
    for arm in ('cm_frontend_sparse','cm_frontend_guarded_sparse','cm_profit_sparse'):
        lost[arm]={
            'multiplications_gt_direct':sum(by[(c,arm)]['multiplications']>by[(c,'direct_sparse_anf')]['multiplications'] for c in cases),
            'pair_terms_gt_direct':sum(by[(c,arm)]['pair_terms']>by[(c,'direct_sparse_anf')]['pair_terms'] for c in cases),
            'pair_terms_gt_direct_5pct':sum(by[(c,arm)]['pair_terms']>1.05*by[(c,'direct_sparse_anf')]['pair_terms'] for c in cases if by[(c,'direct_sparse_anf')]['pair_terms']>0),
        }
    p1rows=[r for r in nsym if r['arm']=='cm_profit_sparse']
    p1diag={k:sum(r[k] for r in p1rows) for k in ('selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit')}
    # Natural predeclared win criterion.
    time_ratio=natcmp['p1_over_generic_2support_sparse']['geomean_ratio']
    pair_ratio=smetrics['pair_terms']['geomean_ratio']; peak_ratio=smetrics['peak_monomials']['geomean_ratio']
    nat_win=bool(time_ratio is not None and time_ratio<=0.95 and (pair_ratio is None or pair_ratio<=1.05) and (peak_ratio is None or peak_ratio<=1.05)
                 and all(r['ok'] for r in nsym))
    return {'natural_timing':natcmp,'gatep_timing':gatecmp,'natural_symbolic_p1_over_generic':smetrics,'lost_sharing_counts':lost,
            'p1_selector_natural_totals':p1diag,'fuzz':fuzz,'predeclared_natural_speed_win':nat_win}


def fmt_ratio(x): return 'n/a' if x is None else f'{x:.4f}'
def fmt_ns(x):
    if x is None:return 'n/a'
    if x<1e3:return f'{x:.0f} ns'
    if x<1e6:return f'{x/1e3:.2f} us'
    if x<1e9:return f'{x/1e6:.2f} ms'
    return f'{x/1e9:.2f} s'


def make_report(meta,selection,summary,nsym,ntime,gsym,gtime):
    lines=['# N2/P1 Profitability-Aware Folding — Frozen Replay','',
           f"Run date: {meta['run_date']}",f"Preregistration SHA-256: `{meta['prereg_sha256']}`",
           f"Frozen natural selection SHA-256: `{meta['natural_selection_sha256']}`",'']
    lines += ['## Frozen P1 rule','',
              f'- Saturating ANF-size structural estimator cap: {MONOMIAL_CAP}.',
              f'- Minimum estimated pair-term benefit: {BENEFIT_MIN}.',
              f'- Minimum relative benefit: {UNSHARED_FRACTION_MIN:.0%} unshared, {SHARED_FRACTION_MIN:.0%} when either child is shared.',
              '- No tuning was performed after results; see `N2_P1_PREREGISTRATION.md`.','']
    lines += ['## Natural corpus','',f"- EPFL commit `{EPFL_COMMIT}`.",f"- Frozen circuits: {', '.join(NATURAL_SOURCES)}.",
              f"- Selected cases: **{len({r['case_id'] for r in nsym})}** across **{len({r['circuit'] for r in nsym})}** circuits.",'']
    lines += ['| circuit | candidates | selected roots |','|---|---:|---|']
    for c in selection['circuits']:
        lines.append(f"| {c['circuit']} | {c['candidate_count']} | {', '.join(x['root'] for x in c['selected']) or 'none'} |")
    lines += ['', '## Natural end-to-end timing (case medians pooled by geometric mean)','',
              '| comparison | cases | P1/other | bootstrap 95% CI |','|---|---:|---:|---:|']
    for key in ('p1_over_generic_2support_sparse','p1_over_direct_sparse_anf','p1_over_cm_frontend_sparse','p1_over_cm_frontend_guarded_sparse'):
        x=summary['natural_timing'][key]; ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
        lines.append(f"| {key} | {x['n']} | {fmt_ratio(x['geomean_ratio'])} | {fmt_ratio(ci[0])} – {fmt_ratio(ci[1])} |")
    lines += ['', 'Per-circuit P1/generic ratios:']
    for c in NATURAL_SOURCES:
        x=summary['natural_timing'][f'p1_over_generic:{c}']; lines.append(f"- {c}: {fmt_ratio(x['geomean_ratio'])} (n={x['n']})")
    lines += ['', '## Natural symbolic / allocation ratios: P1 over generic','', '| metric | n | geomean ratio | median ratio |','|---|---:|---:|---:|']
    for m,x in summary['natural_symbolic_p1_over_generic'].items(): lines.append(f"| {m} | {x['n']} | {fmt_ratio(x['geomean_ratio'])} | {fmt_ratio(x['median_ratio'])} |")
    lines += ['', 'Lost-sharing regression counts versus direct sparse ANF:','']
    for arm,x in summary['lost_sharing_counts'].items():
        lines.append(f"- `{arm}`: multiplications worse on {x['multiplications_gt_direct']} cases; pair terms worse on {x['pair_terms_gt_direct']} cases; >5% pair-term regression on {x['pair_terms_gt_direct_5pct']} cases.")
    pd=summary['p1_selector_natural_totals']
    lines += ['', 'P1 natural selector totals: ' + ', '.join(f"{k}={v}" for k,v in pd.items()) + '.',
              '', f"**Predeclared natural speed-win criterion: {'PASS' if summary['predeclared_natural_speed_win'] else 'NO PASS'}.**",'']
    lines += ['## Gate-P replay','', '| comparison | cases | P1/other | bootstrap 95% CI |','|---|---:|---:|---:|']
    for key,x in summary['gatep_timing'].items():
        ci=x['bootstrap']['ci95'] if x['bootstrap'] else [None,None]
        lines.append(f"| {key} | {x['n']} | {fmt_ratio(x['geomean_ratio'])} | {fmt_ratio(ci[0])} – {fmt_ratio(ci[1])} |")
    # Gate-P fold totals.
    gp=[r for r in gsym if r['arm']=='cm_profit_sparse']
    lines += ['', f"P1 Gate-P folds: accepted {sum(r['selector_accepted'] for r in gp)} of {sum(r['selector_candidates'] for r in gp)} candidates; accepted-shared {sum(r['selector_accepted_shared'] for r in gp)}.",'']
    lines += ['## Correctness','',f"- Natural arm checks: {len(nsym)}; failures: {sum(not r['ok'] for r in nsym)}.",
              f"- Gate-P arm checks: {len(gsym)}; failures: {sum(not r['ok'] for r in gsym)}.",
              f"- Fresh P1 fuzz: {summary['fuzz']['cases']} cases; failures: {len(summary['fuzz']['failures'])}.",'']
    lines += ['## Interpretation boundary','',
              'This test asks whether a **frozen cost heuristic** can preserve useful CM folding without blindly discarding DAG reuse. It does not establish that the local identity is uniquely CM-specific: the generic two-support arm remains the strong artifact-equivalent comparator. Any speed result is therefore a result for this implementation/representation path, not a claim that generic Boolean optimizers cannot implement the same cost-aware idea.',
              '', 'The natural selection is structural and was frozen before any arm ran. Gate-P remains deliberately fold-rich; the multi-circuit EPFL set is the main check against overfitting to that synthetic family.']
    return '\n'.join(lines)+'\n'


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--epfl-dir',type=Path,default=HERE/'epfl'); ap.add_argument('--out',type=Path,default=HERE); args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    preg=args.out/'N2_P1_PREREGISTRATION.md'
    if sha256_file(preg)!=PREREG_SHA256: raise SystemExit('Preregistration hash mismatch; refusing to run')
    start=time.time()
    cases,selection,selsha=freeze_natural_selection(args.epfl_dir,args.out)
    if not cases: raise SystemExit('No natural cases selected')
    fuzz=fuzz_profit()
    if not fuzz['passed']: raise SystemExit(f"P1 fuzz failure: {fuzz['failures'][:3]}")
    nsym,ntime=natural_campaign(cases)
    gsym,gtime=gatep_campaign()
    summary=summarize(nsym,ntime,gsym,gtime,fuzz)
    meta={'schema':'cm-n2-p1-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_s':time.time()-start,
          'prereg_sha256':PREREG_SHA256,'natural_selection_sha256':selsha,'epfl_commit':EPFL_COMMIT,'seed':SEED,
          'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
          'protocol':{'arms':ARMS,'natural_timing_reps':NATURAL_TIMING_REPS,'gatep_timing_reps':GATEP_TIMING_REPS,
                      'gatep_depths':GATEP_DEPTHS,'gatep_cases_per_depth':GATEP_CASES_PER_DEPTH,'fuzz_cases':FUZZ_CASES,
                      'selector':{'monomial_cap':MONOMIAL_CAP,'benefit_min':BENEFIT_MIN,'shared_fraction_min':SHARED_FRACTION_MIN,'unshared_fraction_min':UNSHARED_FRACTION_MIN}}}
    payload={'meta':meta,'selection':selection,'summary':summary,'natural_symbolic_rows':nsym,'natural_timing_rows':ntime,'gatep_symbolic_rows':gsym,'gatep_timing_rows':gtime,'fuzz':fuzz}
    (args.out/'n2_p1_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (args.out/'N2_P1_RESULTS.md').write_text(make_report(meta,selection,summary,nsym,ntime,gsym,gtime),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
