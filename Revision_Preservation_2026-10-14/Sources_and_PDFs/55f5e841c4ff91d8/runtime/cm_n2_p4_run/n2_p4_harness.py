from __future__ import annotations
import argparse, dataclasses, hashlib, json, math, random, statistics, sys, time, tracemalloc
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P3_DIR=HERE.parent/'cm_n2_p3_run'
if str(P3_DIR) not in sys.path: sys.path.insert(0,str(P3_DIR))
import n2_p3_harness as p3
p2=p3.p2
p1=p3.p1
base=p3.base

SEED=20260918
PREREG_SHA256='052a4f097bdc9677c7d0899f5510458d788aa21ad8fb2b5e72a8f09da2d37971'
NATURAL_LOWER_REPS=25
GATEP_LOWER_REPS=25
NATURAL_PIPE_REPS=15
GATEP_PIPE_REPS=15
FUZZ_CASES=1000

DIRECT_META='direct_meta_sparse_anf'
P4_NATIVE='cm_meta_native_sparse'
P4_PROP='cm_meta_sig_sparse'
P3='cm_demand_profit_sparse'
P2='cm_inline_profit_sparse'
DIRECT_ORIG='direct_sparse_anf'
DIRECT_BUILD='direct_build_sparse'
P4_BUILD='cm_meta_sig_build_sparse'
LOWER_ARMS=(DIRECT_META,P4_NATIVE,P4_PROP,P3)
PIPE_ARMS=(DIRECT_BUILD,P4_BUILD)
SYMBOLIC_ARMS=(DIRECT_ORIG,DIRECT_META,P4_NATIVE,P4_PROP,P3,P2)

PARENT_TOKENS={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}

@dataclass(frozen=True, slots=True)
class Sig:
    a:int
    b:int
    token:int
    span:int

@dataclass(frozen=True, slots=True)
class Candidate:
    a:int
    b:int
    tl:int
    tr:int
    composed:int
    left_nid:int
    right_nid:int
    left_shell:bool
    right_shell:bool
    swapped:bool
    parent_pair_cost:int
    left_shell_cost:int
    right_shell_cost:int
    fold_cost:int
    span:int

@dataclass
class P4Stats:
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
    signature_nodes:int=0
    propagated_signature_nodes:int=0
    native_candidate_nodes:int=0
    propagated_candidate_nodes:int=0
    propagated_only_candidate_nodes:int=0


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def token_estimate(token:int,ma:int,mb:int)->int:
    t=token & 15
    v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
    ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
    return min(p1.MONOMIAL_CAP, ca + cb*ma + cc*mb + cd*ma*mb)


class MetaFactory(base.Factory):
    """Frozen Factory semantics plus construction-time side metadata."""
    def __init__(self):
        super().__init__()
        self.uses=[]
        self.est=[]
        self.native_sig=[]
        self.prop_sig=[]
        self.native_candidate=[]
        self.prop_candidate=[]

    def _token_on_pair(self, child:base.Node, a:int, b:int, propagated:bool):
        if child.nid==a: return base.TOK_X,False,False,0
        if child.nid==b: return base.TOK_Y,False,False,0
        if child.op=='not':
            c=child.args[0]
            if c.nid==a: return base.TOK_X ^ 15,False,False,0
            if c.nid==b: return base.TOK_Y ^ 15,False,False,0
        sig=(self.prop_sig if propagated else self.native_sig)[child.nid]
        if sig is None: return None
        if sig.a==a and sig.b==b:
            return sig.token,True,False,sig.span
        if sig.a==b and sig.b==a:
            return base.swap_token(sig.token),True,True,sig.span
        return None

    def _candidate_from_children(self, op:str, left:base.Node, right:base.Node, propagated:bool):
        if op not in PARENT_TOKENS: return None
        sigs=self.prop_sig if propagated else self.native_sig
        pairs=[]
        for ch in (left,right):
            s=sigs[ch.nid]
            if s is not None and (s.a,s.b) not in pairs:
                pairs.append((s.a,s.b))
        parent_tok=PARENT_TOKENS[op]
        for a,b in pairs:
            lt=self._token_on_pair(left,a,b,propagated)
            rt=self._token_on_pair(right,a,b,propagated)
            if lt is None or rt is None: continue
            tl,lshell,lswap,lspan=lt; tr,rshell,rswap,rspan=rt
            if not (lshell or rshell):
                continue
            composed=base.token_apply(op,tl,tr)
            ma=self.est[a]; mb=self.est[b]
            ml=token_estimate(tl,ma,mb); mr=token_estimate(tr,ma,mb)
            parent_pair=p1.token_nonlinear(parent_tok)*ml*mr
            lcost=(p1.token_nonlinear(tl)*ma*mb) if lshell else 0
            rcost=(p1.token_nonlinear(tr)*ma*mb) if rshell else 0
            fold=p1.token_nonlinear(composed)*ma*mb
            span=1+(lspan if lshell else 0)+(rspan if rshell else 0)
            return Candidate(a,b,tl,tr,composed,left.nid,right.nid,lshell,rshell,
                             bool(lswap or rswap),parent_pair,lcost,rcost,fold,span)
        return None

    def _estimate_new(self, op:str, args:tuple[base.Node,...], value):
        cap=p1.MONOMIAL_CAP
        if op=='const': return 1 if value else 0
        if op=='var': return 1
        if op=='not': return min(cap,self.est[args[0].nid]+1)
        if op=='xor': return min(cap,self.est[args[0].nid]+self.est[args[1].nid])
        if op=='and': return min(cap,self.est[args[0].nid]*self.est[args[1].nid])
        if op=='or':
            a=self.est[args[0].nid]; b=self.est[args[1].nid]
            return min(cap,a+b+a*b)
        if op=='andn':
            m=1
            for c in args: m=min(cap,m*self.est[c.nid])
            return m
        if op=='orn':
            m=0
            for c in args:
                q=self.est[c.nid]; m=min(cap,m+q+m*q)
            return m
        if op=='tf': return token_estimate(int(value),self.est[args[0].nid],self.est[args[1].nid])
        raise ValueError(op)

    def _make(self, op, args=(), value=None):
        args=tuple(args)
        key=(op,tuple(a.nid for a in args),value)
        n=self.cache.get(key)
        if n is not None:
            return n
        n=base.Node(len(self.nodes),op,args,value)
        self.cache[key]=n; self.nodes.append(n)
        self.uses.append(0); self.est.append(0); self.native_sig.append(None); self.prop_sig.append(None)
        self.native_candidate.append(None); self.prop_candidate.append(None)
        for c in args: self.uses[c.nid]+=1
        self.est[n.nid]=self._estimate_new(op,args,value)
        if op in ('and','or','xor','tf') and len(args)==2:
            tok=(PARENT_TOKENS[op] if op in PARENT_TOKENS else int(value)&15)
            native=Sig(args[0].nid,args[1].nid,tok,1)
            self.native_sig[n.nid]=native
            nc=self._candidate_from_children(op,args[0],args[1],False) if op in PARENT_TOKENS else None
            pc=self._candidate_from_children(op,args[0],args[1],True) if op in PARENT_TOKENS else None
            self.native_candidate[n.nid]=nc
            self.prop_candidate[n.nid]=pc
            if pc is not None:
                self.prop_sig[n.nid]=Sig(pc.a,pc.b,pc.composed,pc.span)
            else:
                self.prop_sig[n.nid]=native
        return n


def clone_dag(root:base.Node,factory:base.Factory):
    memo={}
    def rec(n):
        if n.nid in memo: return memo[n.nid]
        if n.op=='var': out=factory.var(n.value)
        elif n.op=='const': out=factory.const(n.value)
        elif n.op=='not': out=factory.not_(rec(n.args[0]))
        elif n.op in ('and','or','xor'): out=factory.bin(n.op,rec(n.args[0]),rec(n.args[1]))
        elif n.op in ('andn','orn'): out=factory.nary(n.op,[rec(c) for c in n.args])
        elif n.op=='tf': out=factory.tf(n.value,rec(n.args[0]),rec(n.args[1]))
        else: raise ValueError(n.op)
        memo[n.nid]=out; return out
    out=rec(root)
    return out,factory


def independent_refs(root:base.Node):
    refs=defaultdict(int); nodes={}; stack=[root]
    while stack:
        n=stack.pop()
        if n.nid in nodes: continue
        nodes[n.nid]=n
        for c in n.args:
            refs[c.nid]+=1; stack.append(c)
    return nodes,refs


def validate_meta(root:base.Node,mf:MetaFactory):
    nodes,refs=independent_refs(root)
    issues=[]
    for nid,n in nodes.items():
        if mf.uses[nid]!=refs[nid]: issues.append(('fanout',nid,mf.uses[nid],refs[nid]))
    memo={}
    for nid,n in nodes.items():
        exp=p1.estimate_monomials(n,memo)
        if mf.est[nid]!=exp: issues.append(('estimate',nid,mf.est[nid],exp))
    return issues


def apply_tf_poly(token:int,a:set[int],b:set[int],st:base.AnfStats):
    return p3.apply_tf_poly(token,a,b,st)


def lower_p4(root:base.Node,mf:MetaFactory,mode:str,collect_stats:bool=True):
    if mode not in (P4_NATIVE,P4_PROP): raise ValueError(mode)
    candidates=mf.native_candidate if mode==P4_NATIVE else mf.prop_candidate
    ast=base.AnfStats(); dst=P4Stats(output_unique_nodes=base.reachable_nodes(root))
    if collect_stats:
        dst.signature_nodes=sum(s is not None for s in mf.prop_sig)
        dst.propagated_signature_nodes=sum(1 for n,s,ns in zip(mf.nodes,mf.prop_sig,mf.native_sig)
                                           if s is not None and ns is not None and (s.a,s.b,s.token)!=(ns.a,ns.b,ns.token))
        dst.native_candidate_nodes=sum(c is not None for c in mf.native_candidate)
        dst.propagated_candidate_nodes=sum(c is not None for c in mf.prop_candidate)
        dst.propagated_only_candidate_nodes=sum(pc is not None and nc is None for pc,nc in zip(mf.prop_candidate,mf.native_candidate))
    memo={}

    def decide(n:base.Node,c:Candidate):
        keep=c.parent_pair_cost
        if c.left_shell and mf.uses[c.left_nid]==1: keep += c.left_shell_cost
        if c.right_shell and mf.uses[c.right_nid]==1: keep += c.right_shell_cost
        fold=c.fold_cost; benefit=keep-fold
        shared=(mf.uses[c.left_nid]>1 or mf.uses[c.right_nid]>1)
        frac=benefit/max(1,keep)
        if collect_stats:
            dst.selector_candidates+=1; dst.selector_estimated_keep_cost+=keep; dst.selector_estimated_fold_cost+=fold
        if benefit<=0:
            if collect_stats: dst.selector_rejected_nonpositive+=1
            return False,benefit,shared
        if benefit<p1.BENEFIT_MIN:
            if collect_stats: dst.selector_rejected_min_benefit+=1
            return False,benefit,shared
        minfrac=p1.SHARED_FRACTION_MIN if shared else p1.UNSHARED_FRACTION_MIN
        if frac<minfrac:
            if collect_stats: dst.selector_rejected_fraction+=1
            return False,benefit,shared
        if collect_stats:
            dst.selector_accepted+=1; dst.selector_estimated_benefit+=benefit
            if shared: dst.selector_accepted_shared+=1
            if c.swapped: dst.transpose_alignments+=1
        return True,benefit,shared

    def rec(n:base.Node):
        if n.nid in memo:
            ast.cache_hits+=1
            if collect_stats: dst.cse_hits+=1
            return memo[n.nid]
        ast.anf_nodes_evaluated+=1
        c=None; accepted=False
        if n.op in PARENT_TOKENS:
            if collect_stats: dst.selector_nodes_checked+=1
            c=candidates[n.nid]
            if c is not None: accepted,_,_=decide(n,c)
        if accepted:
            if collect_stats:
                dst.successful_folds+=1; dst.same_operand_folds+=1; dst.fold_lowerings+=1
                dst.bypassed_child_shells += int(c.left_shell)+int(c.right_shell)
            p=apply_tf_poly(c.composed,rec(mf.nodes[c.a]),rec(mf.nodes[c.b]),ast)
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
    poly=rec(root)
    return poly,ast,dst


def _finish_row(arm,poly,ast,oracle,nvars,compile_ns,peak,extra=None):
    got=base.anf_to_bitset(poly,nvars)
    row={'arm':arm,'ok':got==oracle,'compile_ns':compile_ns,'lower_ns':compile_ns,'python_peak_bytes':peak,
         'final_monomials':len(poly),'final_degree':max((m.bit_count() for m in poly),default=0),
         'serialized_bytes':base.poly_serialized_bytes(poly),'digest':base.poly_digest(poly),**dataclasses.asdict(ast)}
    if extra: row.update(extra)
    return row


def run_direct_original(root,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(DIRECT_ORIG,poly,ast,oracle,nvars,t1-t0,peak,{'output_unique_nodes':base.reachable_nodes(root)})


def run_direct_meta(meta_root,mf,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(meta_root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(DIRECT_META,poly,ast,oracle,nvars,t1-t0,peak,{'output_unique_nodes':base.reachable_nodes(meta_root)})


def run_p4(meta_root,mf,arm,oracle,nvars,memory=False,collect_stats=True):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast,dst=lower_p4(meta_root,mf,arm,collect_stats=collect_stats); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    extra=dataclasses.asdict(dst) if collect_stats else {}
    return _finish_row(arm,poly,ast,oracle,nvars,t1-t0,peak,extra)


def run_p3(root,oracle,nvars,memory=False):
    r=p3.run_p3(root,oracle,nvars,memory=memory); r=dict(r); r['arm']=P3; r['lower_ns']=r['compile_ns']; return r


def run_p2(root,oracle,nvars,memory=False):
    r=p3.run_p2(root,oracle,nvars,memory=memory); r=dict(r); r['arm']=P2; r['lower_ns']=r['compile_ns']; return r


def build_meta(root):
    mf=MetaFactory(); mr,_=clone_dag(root,mf); return mr,mf


def run_symbolic(root,oracle,nvars,meta):
    meta_root,mf=build_meta(root)
    issues=validate_meta(meta_root,mf)
    if issues: raise AssertionError(f'metadata invariant failure {meta} {issues[:5]}')
    rows=[]
    funcs=[lambda:run_direct_original(root,oracle,nvars,True),
           lambda:run_direct_meta(meta_root,mf,oracle,nvars,True),
           lambda:run_p4(meta_root,mf,P4_NATIVE,oracle,nvars,True,True),
           lambda:run_p4(meta_root,mf,P4_PROP,oracle,nvars,True,True),
           lambda:run_p3(root,oracle,nvars,True),
           lambda:run_p2(root,oracle,nvars,True)]
    digest=None
    for fn in funcs:
        r=fn(); r.update(meta); rows.append(r)
        if not r['ok']: raise AssertionError(f'oracle mismatch {meta} {r["arm"]}')
        if digest is None: digest=r['digest']
        elif r['digest']!=digest: raise AssertionError(f'digest mismatch {meta} {r["arm"]}')
    # direct structural identity between original and meta clone
    d=rows[0]; dm=rows[1]
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes')
    bad={k:(d.get(k),dm.get(k)) for k in fields if d.get(k)!=dm.get(k)}
    if bad: raise AssertionError(f'meta clone direct identity drift {meta} {bad}')
    return rows,meta_root,mf


def run_lower_timing(root,meta_root,mf,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in LOWER_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        if arm==DIRECT_META: r=run_direct_meta(meta_root,mf,oracle,nvars,False)
        elif arm==P4_NATIVE: r=run_p4(meta_root,mf,P4_NATIVE,oracle,nvars,False,False)
        elif arm==P4_PROP: r=run_p4(meta_root,mf,P4_PROP,oracle,nvars,False,False)
        elif arm==P3: r=run_p3(root,oracle,nvars,False)
        else: raise ValueError(arm)
        if not r['ok']: raise AssertionError(f'timed lower mismatch {meta} {arm}')
        rows.append({**meta,'rep':rep,'arm':arm,'lower_ns':r['lower_ns'],'compile_ns':r['compile_ns'],'ok':True})
    return rows


def run_pipeline_once(root,arm,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns()
    if arm==DIRECT_BUILD:
        f=base.Factory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast=base.lower_anf(rr); l1=time.perf_counter_ns(); stats=None
    elif arm==P4_BUILD:
        f=MetaFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast,stats=lower_p4(rr,f,P4_PROP,collect_stats=False); l1=time.perf_counter_ns()
    else: raise ValueError(arm)
    t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars)
    return {'arm':arm,'ok':got==oracle,'pipeline_ns':t1-t0,'dag_build_ns':b1-b0,'lower_ns':l1-l0,
            'python_peak_bytes':peak,'digest':base.poly_digest(poly),'final_monomials':len(poly),
            'final_degree':max((m.bit_count() for m in poly),default=0),**dataclasses.asdict(ast)}


def run_pipeline_timing(root,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in PIPE_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        r=run_pipeline_once(root,arm,oracle,nvars,False)
        if not r['ok']: raise AssertionError(f'pipeline mismatch {meta} {arm}')
        rows.append({**meta,'rep':rep,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r['dag_build_ns'],'lower_ns':r['lower_ns'],'ok':True})
    return rows


def fresh_fuzz():
    rng=random.Random(SEED^0xF444); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        try:
            meta_root,mf=build_meta(root); issues=validate_meta(meta_root,mf)
            if issues: raise AssertionError(issues[:5])
            d=run_direct_original(root,oracle,nvars,False); dm=run_direct_meta(meta_root,mf,oracle,nvars,False)
            n=run_p4(meta_root,mf,P4_NATIVE,oracle,nvars,False,True); q=run_p4(meta_root,mf,P4_PROP,oracle,nvars,False,True)
            x=run_p3(root,oracle,nvars,False); z=run_p2(root,oracle,nvars,False)
            db=run_pipeline_once(root,DIRECT_BUILD,oracle,nvars,False); qb=run_pipeline_once(root,P4_BUILD,oracle,nvars,False)
            digs={d['digest'],dm['digest'],n['digest'],q['digest'],x['digest'],z['digest'],db['digest'],qb['digest']}
            if not (all(r['ok'] for r in (d,dm,n,q,x,z,db,qb)) and len(digs)==1):
                raise AssertionError('correctness/digest')
            fields=('multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes')
            bad={k:(d.get(k),dm.get(k)) for k in fields if d.get(k)!=dm.get(k)}
            if bad: raise AssertionError(('direct clone identity',bad))
            if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P4 prop utilization')
            if n.get('selector_accepted',0)!=n.get('fold_lowerings',0): raise AssertionError('P4 native utilization')
        except Exception as e:
            failures.append({'case':i,'nvars':nvars,'error':repr(e)})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def load_cases():
    cases,selection,selsha=p3.load_cases()
    ref=json.loads((HERE/'N2_P3_NATURAL_SELECTION_REFERENCE.json').read_text())
    expected=[]
    for c in ref['circuits']:
        for s in c['selected']: expected.append(f"{c['circuit']}:{s['root']}")
    got=[c['case_id'] for c in cases]
    if sorted(got)!=sorted(expected): raise AssertionError(f'natural selection drift {got} != {expected}')
    return cases,selection,selsha


def p3_gate_reference():
    d=json.loads((HERE/'N2_P3_RESULTS_REFERENCE.json').read_text())
    return {(int(r['depth']),int(r['case'])):r for r in d['gatep_symbolic_rows'] if r['arm']==DIRECT_ORIG}


def generate_gate_cases():
    rng=random.Random(base.SEED^0x6A7E); cases=[]; ref=p3_gate_reference(); drift=[]
    fields=('digest','output_unique_nodes','multiplications','pair_terms','peak_monomials','final_monomials','final_degree')
    for depth in p1.GATEP_DEPTHS:
        for i in range(p1.GATEP_CASES_PER_DEPTH):
            f,root,n=base.gatep_case(rng,depth,i); oracle=base.eval_node_bitset(root,n); d=run_direct_original(root,oracle,n,False); rr=ref[(depth,i)]
            bad={k:(d.get(k),rr.get(k)) for k in fields if d.get(k)!=rr.get(k)}
            if bad: drift.append({'depth':depth,'case':i,'differences':bad})
            cases.append((depth,i,root,n,oracle))
    if drift: raise AssertionError(f'Gate-P identity drift {drift[:3]}')
    return cases


def run_natural_case(case_id):
    cases,selection,selsha=load_cases(); by={c['case_id']:c for c in cases}; c=by[case_id]
    meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
    sym,meta_root,mf=run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x4400
    lower=run_lower_timing(c['root_node'],meta_root,mf,c['oracle'],c['support'],meta,NATURAL_LOWER_REPS,seed)
    pipe=run_pipeline_timing(c['root_node'],c['oracle'],c['support'],meta,NATURAL_PIPE_REPS,seed^0xB17D)
    mem=[{**meta,**run_pipeline_once(c['root_node'],a,c['oracle'],c['support'],True)} for a in PIPE_ARMS]
    return {'schema':'cm-n2-p4-natural-case/v1','case_id':case_id,'selection_sha256':selsha,
            'symbolic_rows':sym,'lower_timing_rows':lower,'pipeline_timing_rows':pipe,'pipeline_memory_rows':mem}


def run_gatep():
    cases=generate_gate_cases(); sym=[]; lower=[]; pipe=[]; pmem=[]
    for depth,i,root,n,oracle in cases:
        meta={'depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        s,mr,mf=run_symbolic(root,oracle,n,meta); sym.extend(s)
        seed=SEED+depth*1000+i+0x4400
        lower.extend(run_lower_timing(root,mr,mf,oracle,n,meta,GATEP_LOWER_REPS,seed))
        pipe.extend(run_pipeline_timing(root,oracle,n,meta,GATEP_PIPE_REPS,seed^0xB17D))
        pmem.extend([{**meta,**run_pipeline_once(root,a,oracle,n,True)} for a in PIPE_ARMS])
    return {'schema':'cm-n2-p4-gatep/v1','symbolic_rows':sym,'lower_timing_rows':lower,
            'pipeline_timing_rows':pipe,'pipeline_memory_rows':pmem}


def main():
    if sha256_file(HERE/'N2_P4_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P4 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=('fuzz','gatep','natural-case','selection'),required=True); ap.add_argument('--case-id'); ap.add_argument('--out',required=True)
    a=ap.parse_args()
    if a.mode=='fuzz': obj=fresh_fuzz()
    elif a.mode=='gatep': obj=run_gatep()
    elif a.mode=='natural-case':
        if not a.case_id: raise SystemExit('--case-id required')
        obj=run_natural_case(a.case_id)
    else:
        cases,selection,selsha=load_cases(); obj={'selection':selection,'selection_sha256':selsha,'case_ids':[c['case_id'] for c in cases]}
    Path(a.out).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps({'mode':a.mode,'out':a.out,'ok':True,'summary':({k:obj[k] for k in ('cases','passed') if k in obj})},indent=2))

if __name__=='__main__': main()
