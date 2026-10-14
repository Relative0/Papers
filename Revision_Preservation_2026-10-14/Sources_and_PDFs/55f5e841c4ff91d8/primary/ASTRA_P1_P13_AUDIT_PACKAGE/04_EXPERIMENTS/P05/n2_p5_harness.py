from __future__ import annotations
import argparse, dataclasses, hashlib, json, random, sys, time, tracemalloc
from array import array
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P4_DIR=HERE.parent/'cm_n2_p4_run'
if str(P4_DIR) not in sys.path: sys.path.insert(0,str(P4_DIR))
import n2_p4_harness as p4
p3=p4.p3
p2=p4.p2
p1=p4.p1
base=p4.base

SEED=20260918
PREREG_SHA256='c91961a3665c2ec0a87b3e7da47c38cd39f5c62def3f68ce911733d1c6621ff8'
NATURAL_LOWER_REPS=25
GATEP_LOWER_REPS=25
NATURAL_PIPE_REPS=15
GATEP_PIPE_REPS=15
FUZZ_CASES=1000

DIRECT_PACKED='direct_packed_sparse_anf'
P5='cm_packed_sig_sparse'
P4='cm_meta_sig_sparse'
DIRECT_ORIG='direct_sparse_anf'
P3='cm_demand_profit_sparse'
P2='cm_inline_profit_sparse'
DIRECT_BUILD='direct_build_sparse'
P4_BUILD='cm_meta_sig_build_sparse'
P5_BUILD='cm_packed_sig_build_sparse'
LOWER_ARMS=(DIRECT_PACKED,P5,P4)
PIPE_ARMS=(DIRECT_BUILD,P5_BUILD,P4_BUILD)

PARENT_TOKENS={'and':base.TOK_AND,'or':base.TOK_OR,'xor':base.TOK_XOR}
PARENT_INDEX={'and':0,'or':1,'xor':2}
SENTINEL=(1<<32)-1

# Small frozen truth-token tables. ANF coefficient mask bits: c0, ca, cb, cab.
def _anf_mask(token:int)->int:
    t=token & 15
    v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
    c0=v00; ca=v10^v00; cb=v01^v00; cab=v11^v10^v01^v00
    return c0 | (ca<<1) | (cb<<2) | (cab<<3)
ANF_MASK=tuple(_anf_mask(t) for t in range(16))
NONLINEAR=tuple((ANF_MASK[t]>>3)&1 for t in range(16))
SWAP_TOKEN=tuple(base.swap_token(t) for t in range(16))
TOKEN_APPLY=tuple(tuple(tuple(base.token_apply(op,a,b) for b in range(16)) for a in range(16))
                  for op in ('and','or','xor'))

@dataclass
class P5Stats:
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
    propagated_candidate_nodes:int=0


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def token_estimate_fast(token:int,ma:int,mb:int)->int:
    mask=ANF_MASK[token & 15]
    x=(mask&1) + (((mask>>1)&1)*ma) + (((mask>>2)&1)*mb) + (((mask>>3)&1)*ma*mb)
    return p1.MONOMIAL_CAP if x>p1.MONOMIAL_CAP else x


class PackedMetaFactory(base.Factory):
    """Factory semantics plus packed primitive construction annotations only."""
    __slots__=('cache','nodes','uses','est','sig_a','sig_b','sig_token','sig_propagated')
    def __init__(self):
        super().__init__()
        self.uses=array('I')
        self.est=array('H')
        self.sig_a=array('I')
        self.sig_b=array('I')
        self.sig_token=bytearray()
        self.sig_propagated=bytearray()

    def _align_code(self,child:base.Node,a:int,b:int)->int:
        nid=child.nid
        if nid==a: return base.TOK_X
        if nid==b: return base.TOK_Y
        if child.op=='not':
            c=child.args[0].nid
            if c==a: return (base.TOK_X ^ 15)
            if c==b: return (base.TOK_Y ^ 15)
        sa=self.sig_a[nid]
        if sa==SENTINEL: return -1
        sb=self.sig_b[nid]; tok=self.sig_token[nid]
        if sa==a and sb==b: return tok | 16
        if sa==b and sb==a: return SWAP_TOKEN[tok] | 16 | 32
        return -1

    def _propagate_pair(self,op:str,left:base.Node,right:base.Node):
        li=left.nid; ri=right.nid
        la=self.sig_a[li]
        rb_a=self.sig_a[ri]
        tried_a=SENTINEL; tried_b=SENTINEL
        opi=PARENT_INDEX[op]
        if la!=SENTINEL:
            a=la; b=self.sig_b[li]; tried_a=a; tried_b=b
            lc=self._align_code(left,a,b); rc=self._align_code(right,a,b)
            if lc>=0 and rc>=0 and ((lc|rc)&16):
                return a,b,TOKEN_APPLY[opi][lc&15][rc&15]
        if rb_a!=SENTINEL:
            a=rb_a; b=self.sig_b[ri]
            if a!=tried_a or b!=tried_b:
                lc=self._align_code(left,a,b); rc=self._align_code(right,a,b)
                if lc>=0 and rc>=0 and ((lc|rc)&16):
                    return a,b,TOKEN_APPLY[opi][lc&15][rc&15]
        return None

    def _estimate_new(self,op:str,args:tuple[base.Node,...],value)->int:
        cap=p1.MONOMIAL_CAP
        if op=='const': return 1 if value else 0
        if op=='var': return 1
        if op=='not':
            x=self.est[args[0].nid]+1
            return cap if x>cap else x
        if op=='xor':
            x=self.est[args[0].nid]+self.est[args[1].nid]
            return cap if x>cap else x
        if op=='and':
            x=self.est[args[0].nid]*self.est[args[1].nid]
            return cap if x>cap else x
        if op=='or':
            a=self.est[args[0].nid]; b=self.est[args[1].nid]; x=a+b+a*b
            return cap if x>cap else x
        if op=='andn':
            m=1
            for c in args:
                m*=self.est[c.nid]
                if m>=cap: return cap
            return m
        if op=='orn':
            m=0
            for c in args:
                q=self.est[c.nid]; m=m+q+m*q
                if m>=cap: return cap
            return m
        if op=='tf': return token_estimate_fast(int(value),self.est[args[0].nid],self.est[args[1].nid])
        raise ValueError(op)

    def _make(self,op,args=(),value=None):
        args=tuple(args)
        key=(op,tuple(a.nid for a in args),value)
        n=self.cache.get(key)
        if n is not None: return n
        n=base.Node(len(self.nodes),op,args,value)
        self.cache[key]=n; self.nodes.append(n)
        self.uses.append(0); self.est.append(0)
        self.sig_a.append(SENTINEL); self.sig_b.append(SENTINEL)
        self.sig_token.append(0); self.sig_propagated.append(0)
        for c in args: self.uses[c.nid]+=1
        nid=n.nid
        self.est[nid]=self._estimate_new(op,args,value)
        if op in ('and','or','xor','tf') and len(args)==2:
            tok=(PARENT_TOKENS[op] if op in PARENT_TOKENS else int(value)&15)
            if op in PARENT_TOKENS:
                q=self._propagate_pair(op,args[0],args[1])
                if q is not None:
                    a,b,ct=q
                    self.sig_a[nid]=a; self.sig_b[nid]=b; self.sig_token[nid]=ct; self.sig_propagated[nid]=1
                    return n
            self.sig_a[nid]=args[0].nid; self.sig_b[nid]=args[1].nid; self.sig_token[nid]=tok
        return n


def clone_dag(root:base.Node,factory:base.Factory):
    return p4.clone_dag(root,factory)


def independent_refs(root:base.Node):
    return p4.independent_refs(root)


def validate_packed(root:base.Node,pf:PackedMetaFactory):
    nodes,refs=independent_refs(root); issues=[]
    for nid,n in nodes.items():
        if pf.uses[nid]!=refs[nid]: issues.append(('fanout',nid,pf.uses[nid],refs[nid]))
    memo={}
    for nid,n in nodes.items():
        exp=p1.estimate_monomials(n,memo)
        if pf.est[nid]!=exp: issues.append(('estimate',nid,pf.est[nid],exp))
    return issues


def compare_packed_to_p4(p5root:base.Node,pf:PackedMetaFactory,p4root:base.Node,mf:p4.MetaFactory):
    issues=[]
    if len(pf.nodes)!=len(mf.nodes): issues.append(('node_count',len(pf.nodes),len(mf.nodes)))
    lim=min(len(pf.nodes),len(mf.nodes))
    for nid in range(lim):
        a=pf.nodes[nid]; b=mf.nodes[nid]
        if a.op!=b.op or a.value!=b.value or tuple(c.nid for c in a.args)!=tuple(c.nid for c in b.args):
            issues.append(('node',nid,a.op,b.op,a.value,b.value)); continue
        if pf.uses[nid]!=mf.uses[nid]: issues.append(('uses',nid,pf.uses[nid],mf.uses[nid]))
        if pf.est[nid]!=mf.est[nid]: issues.append(('est',nid,pf.est[nid],mf.est[nid]))
        ps=mf.prop_sig[nid]
        if ps is None:
            if pf.sig_a[nid]!=SENTINEL: issues.append(('sig_presence',nid,pf.sig_a[nid],None))
        else:
            got=(pf.sig_a[nid],pf.sig_b[nid],pf.sig_token[nid])
            exp=(ps.a,ps.b,ps.token)
            if got!=exp: issues.append(('sig',nid,got,exp))
        exp_prop=1 if mf.prop_candidate[nid] is not None else 0
        if int(pf.sig_propagated[nid])!=exp_prop:
            issues.append(('prop_flag',nid,int(pf.sig_propagated[nid]),exp_prop))
        if len(issues)>=20: break
    return issues


def lower_p5(root:base.Node,pf:PackedMetaFactory,collect_stats:bool=True):
    ast=base.AnfStats(); dst=P5Stats(output_unique_nodes=base.reachable_nodes(root))
    if collect_stats:
        dst.signature_nodes=sum(1 for x in pf.sig_a if x!=SENTINEL)
        dst.propagated_signature_nodes=sum(pf.sig_propagated)
        dst.propagated_candidate_nodes=sum(pf.sig_propagated)
    memo={}
    uses=pf.uses; est=pf.est; siga=pf.sig_a; sigb=pf.sig_b; sigtok=pf.sig_token; sigprop=pf.sig_propagated; nodes=pf.nodes

    def rec(n:base.Node):
        nid=n.nid
        if nid in memo:
            ast.cache_hits+=1
            if collect_stats: dst.cse_hits+=1
            return memo[nid]
        ast.anf_nodes_evaluated+=1
        accepted=False; a=b=tl=tr=composed=0; lc=rc=-1
        if n.op in PARENT_TOKENS:
            if collect_stats: dst.selector_nodes_checked+=1
            if sigprop[nid]:
                if collect_stats: dst.selector_candidates+=1
                a=siga[nid]; b=sigb[nid]; composed=sigtok[nid]
                left,right=n.args
                lc=pf._align_code(left,a,b); rc=pf._align_code(right,a,b)
                if lc<0 or rc<0 or not ((lc|rc)&16):
                    raise AssertionError(('packed candidate alignment failure',nid,a,b,lc,rc))
                tl=lc&15; tr=rc&15; ma=est[a]; mb=est[b]
                ml=token_estimate_fast(tl,ma,mb); mr=token_estimate_fast(tr,ma,mb)
                parent_pair=NONLINEAR[PARENT_TOKENS[n.op]]*ml*mr
                left_shell=bool(lc&16); right_shell=bool(rc&16)
                keep=parent_pair
                if left_shell and uses[left.nid]==1: keep += NONLINEAR[tl]*ma*mb
                if right_shell and uses[right.nid]==1: keep += NONLINEAR[tr]*ma*mb
                fold=NONLINEAR[composed]*ma*mb
                benefit=keep-fold
                shared=(uses[left.nid]>1 or uses[right.nid]>1)
                if collect_stats:
                    dst.selector_estimated_keep_cost+=keep; dst.selector_estimated_fold_cost+=fold
                if benefit<=0:
                    if collect_stats: dst.selector_rejected_nonpositive+=1
                elif benefit<p1.BENEFIT_MIN:
                    if collect_stats: dst.selector_rejected_min_benefit+=1
                else:
                    minfrac=p1.SHARED_FRACTION_MIN if shared else p1.UNSHARED_FRACTION_MIN
                    if benefit/max(1,keep)<minfrac:
                        if collect_stats: dst.selector_rejected_fraction+=1
                    else:
                        accepted=True
                        if collect_stats:
                            dst.selector_accepted+=1; dst.selector_estimated_benefit+=benefit
                            if shared: dst.selector_accepted_shared+=1
                            if (lc|rc)&32: dst.transpose_alignments+=1
        if accepted:
            if collect_stats:
                dst.successful_folds+=1; dst.same_operand_folds+=1; dst.fold_lowerings+=1
                dst.bypassed_child_shells += int(bool(lc&16))+int(bool(rc&16))
            p=p3.apply_tf_poly(composed,rec(nodes[a]),rec(nodes[b]),ast)
        elif n.op=='const': p={0} if n.value else set()
        elif n.op=='var': p={1<<n.value}
        elif n.op=='not':
            p=rec(n.args[0]).copy(); (p.remove(0) if 0 in p else p.add(0)); base.update_peak(p,ast)
        elif n.op=='xor': p=base.xor_poly(rec(n.args[0]),rec(n.args[1])); base.update_peak(p,ast)
        elif n.op=='and': p=base.mul_poly(rec(n.args[0]),rec(n.args[1]),ast)
        elif n.op=='or':
            x=rec(n.args[0]); y=rec(n.args[1]); p=base.xor_poly(base.xor_poly(x,y),base.mul_poly(x,y,ast)); base.update_peak(p,ast)
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
                            x,y=level[i],level[i+1]; q=base.xor_poly(base.xor_poly(x,y),base.mul_poly(x,y,ast)); base.update_peak(q,ast); nxt.append(q)
                    level=nxt
                p=level[0]
        elif n.op=='tf': p=p3.apply_tf_poly(n.value,rec(n.args[0]),rec(n.args[1]),ast)
        else: raise ValueError(n.op)
        memo[nid]=p; ast.peak_cache_entries=max(ast.peak_cache_entries,len(memo)); base.update_peak(p,ast)
        return p
    poly=rec(root)
    return poly,ast,dst


def _finish_row(arm,poly,ast,oracle,nvars,lower_ns,peak,extra=None):
    got=base.anf_to_bitset(poly,nvars)
    row={'arm':arm,'ok':got==oracle,'compile_ns':lower_ns,'lower_ns':lower_ns,'python_peak_bytes':peak,
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


def run_direct_packed(root,pf,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(DIRECT_PACKED,poly,ast,oracle,nvars,t1-t0,peak,{'output_unique_nodes':base.reachable_nodes(root)})


def run_p5(root,pf,oracle,nvars,memory=False,collect_stats=True):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast,dst=lower_p5(root,pf,collect_stats=collect_stats); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(P5,poly,ast,oracle,nvars,t1-t0,peak,dataclasses.asdict(dst) if collect_stats else {})


def run_p4(root,mf,oracle,nvars,memory=False,collect_stats=True):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast,dst=p4.lower_p4(root,mf,p4.P4_PROP,collect_stats=collect_stats); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(P4,poly,ast,oracle,nvars,t1-t0,peak,dataclasses.asdict(dst) if collect_stats else {})


def build_packed(root):
    pf=PackedMetaFactory(); rr,_=clone_dag(root,pf); return rr,pf


def build_p4(root):
    mf=p4.MetaFactory(); rr,_=clone_dag(root,mf); return rr,mf


def decision_equivalence(p5row,p4row):
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated',
            'selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared',
            'selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction',
            'selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost',
            'fold_lowerings','bypassed_child_shells','transpose_alignments')
    return {k:(p5row.get(k),p4row.get(k)) for k in fields if p5row.get(k)!=p4row.get(k)}


def run_symbolic(root,oracle,nvars,meta):
    p5root,pf=build_packed(root); p4root,mf=build_p4(root)
    issues=validate_packed(p5root,pf)
    if issues: raise AssertionError(f'packed invariant failure {meta} {issues[:5]}')
    eq=compare_packed_to_p4(p5root,pf,p4root,mf)
    if eq: raise AssertionError(f'P5/P4 metadata drift {meta} {eq[:5]}')
    d=run_direct_original(root,oracle,nvars,True)
    dp=run_direct_packed(p5root,pf,oracle,nvars,True)
    q=run_p5(p5root,pf,oracle,nvars,True,True)
    r=run_p4(p4root,mf,oracle,nvars,True,True)
    rows=[]
    for x in (d,dp,q,r): x.update(meta); rows.append(x)
    if not all(x['ok'] for x in rows): raise AssertionError(f'oracle mismatch {meta}')
    if len({x['digest'] for x in rows})!=1: raise AssertionError(f'digest mismatch {meta}')
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes')
    bad={k:(d.get(k),dp.get(k)) for k in fields if d.get(k)!=dp.get(k)}
    if bad: raise AssertionError(f'packed clone direct identity drift {meta} {bad}')
    bad=decision_equivalence(q,r)
    if bad: raise AssertionError(f'P5/P4 symbolic decision drift {meta} {bad}')
    if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P5 utilization')
    return rows,p5root,pf,p4root,mf


def run_lower_timing(p5root,pf,p4root,mf,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in LOWER_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        if arm==DIRECT_PACKED: r=run_direct_packed(p5root,pf,oracle,nvars,False)
        elif arm==P5: r=run_p5(p5root,pf,oracle,nvars,False,False)
        elif arm==P4: r=run_p4(p4root,mf,oracle,nvars,False,False)
        else: raise ValueError(arm)
        if not r['ok']: raise AssertionError(f'timed lower mismatch {meta} {arm}')
        rows.append({**meta,'rep':rep,'arm':arm,'lower_ns':r['lower_ns'],'compile_ns':r['compile_ns'],'ok':True})
    return rows


def run_pipeline_once(root,arm,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns()
    if arm==DIRECT_BUILD:
        f=base.Factory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast=base.lower_anf(rr); l1=time.perf_counter_ns()
    elif arm==P5_BUILD:
        f=PackedMetaFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast,_=lower_p5(rr,f,collect_stats=False); l1=time.perf_counter_ns()
    elif arm==P4_BUILD:
        f=p4.MetaFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast,_=p4.lower_p4(rr,f,p4.P4_PROP,collect_stats=False); l1=time.perf_counter_ns()
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
    rng=random.Random(SEED^0xF555); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        try:
            p5root,pf=build_packed(root); p4root,mf=build_p4(root)
            issues=validate_packed(p5root,pf)
            if issues: raise AssertionError(issues[:5])
            eq=compare_packed_to_p4(p5root,pf,p4root,mf)
            if eq: raise AssertionError(('metadata equivalence',eq[:5]))
            d=run_direct_original(root,oracle,nvars,False); dp=run_direct_packed(p5root,pf,oracle,nvars,False)
            q=run_p5(p5root,pf,oracle,nvars,False,True); r=run_p4(p4root,mf,oracle,nvars,False,True)
            x=dict(p3.run_p3(root,oracle,nvars,memory=False)); z=dict(p3.run_p2(root,oracle,nvars,memory=False))
            db=run_pipeline_once(root,DIRECT_BUILD,oracle,nvars,False); qb=run_pipeline_once(root,P5_BUILD,oracle,nvars,False); rb=run_pipeline_once(root,P4_BUILD,oracle,nvars,False)
            allrows=(d,dp,q,r,x,z,db,qb,rb)
            if not all(v.get('ok',False) for v in allrows): raise AssertionError('correctness')
            if len({v['digest'] for v in allrows})!=1: raise AssertionError('digest')
            fields=('multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated')
            bad={k:(d.get(k),dp.get(k)) for k in fields if d.get(k)!=dp.get(k)}
            if bad: raise AssertionError(('direct clone identity',bad))
            bad=decision_equivalence(q,r)
            if bad: raise AssertionError(('P5/P4 decision',bad))
            if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P5 utilization')
        except Exception as e:
            failures.append({'case':i,'nvars':nvars,'error':repr(e)})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def load_cases():
    return p4.load_cases()


def generate_gate_cases():
    return p4.generate_gate_cases()


def run_natural_case(case_id):
    cases,selection,selsha=load_cases(); by={c['case_id']:c for c in cases}; c=by[case_id]
    meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
    sym,p5root,pf,p4root,mf=run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x5500
    lower=run_lower_timing(p5root,pf,p4root,mf,c['oracle'],c['support'],meta,NATURAL_LOWER_REPS,seed)
    pipe=run_pipeline_timing(c['root_node'],c['oracle'],c['support'],meta,NATURAL_PIPE_REPS,seed^0xB17D)
    mem=[{**meta,**run_pipeline_once(c['root_node'],a,c['oracle'],c['support'],True)} for a in PIPE_ARMS]
    return {'schema':'cm-n2-p5-natural-case/v1','case_id':case_id,'selection_sha256':selsha,
            'symbolic_rows':sym,'lower_timing_rows':lower,'pipeline_timing_rows':pipe,'pipeline_memory_rows':mem}


def run_gatep():
    cases=generate_gate_cases(); sym=[]; lower=[]; pipe=[]; pmem=[]
    for depth,i,root,n,oracle in cases:
        meta={'depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        s,p5root,pf,p4root,mf=run_symbolic(root,oracle,n,meta); sym.extend(s)
        seed=SEED+depth*1000+i+0x5500
        lower.extend(run_lower_timing(p5root,pf,p4root,mf,oracle,n,meta,GATEP_LOWER_REPS,seed))
        pipe.extend(run_pipeline_timing(root,oracle,n,meta,GATEP_PIPE_REPS,seed^0xB17D))
        pmem.extend([{**meta,**run_pipeline_once(root,a,oracle,n,True)} for a in PIPE_ARMS])
    return {'schema':'cm-n2-p5-gatep/v1','symbolic_rows':sym,'lower_timing_rows':lower,
            'pipeline_timing_rows':pipe,'pipeline_memory_rows':pmem}


def main():
    if sha256_file(HERE/'N2_P5_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P5 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=('fuzz','gatep','natural-case','selection'),required=True); ap.add_argument('--case-id'); ap.add_argument('--out',required=True)
    a=ap.parse_args()
    if a.mode=='fuzz': obj=fresh_fuzz()
    elif a.mode=='gatep': obj=run_gatep()
    elif a.mode=='natural-case':
        if not a.case_id: raise SystemExit('--case-id required')
        obj=run_natural_case(a.case_id)
    else:
        cases,selection,selsha=load_cases(); obj={'selection':selection,'selection_sha256':selsha,'case_ids':[c['case_id'] for c in cases]}
    Path(a.out).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'mode':a.mode,'out':a.out,'ok':True,'summary':({k:obj[k] for k in ('cases','passed') if k in obj})},indent=2))

if __name__=='__main__': main()
