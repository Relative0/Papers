from __future__ import annotations
import argparse, dataclasses, hashlib, json, random, sys, time, tracemalloc
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P5_DIR=HERE.parent/'cm_n2_p5_run'
if str(P5_DIR) not in sys.path: sys.path.insert(0,str(P5_DIR))
import n2_p5_harness as p5
p4=p5.p4
p3=p5.p3
p2=p5.p2
p1=p5.p1
base=p5.base

SEED=20260918
PREREG_SHA256='898781343d0e9379bdf37d7c053eece3deb9c674b7bc514d2722504d97b0f60b'
NATURAL_LOWER_REPS=25
GATEP_LOWER_REPS=25
NATURAL_PIPE_REPS=15
GATEP_PIPE_REPS=15
FUZZ_CASES=1000

DIRECT_INNODE='direct_innode_sparse_anf'
P6='cm_innode_sig_sparse'
P5='cm_packed_sig_sparse'
DIRECT_ORIG='direct_sparse_anf'
DIRECT_BUILD='direct_build_sparse'
P6_BUILD='cm_innode_sig_build_sparse'
P5_BUILD='cm_packed_sig_build_sparse'
LOWER_ARMS=(DIRECT_INNODE,P6,P5)
PIPE_ARMS=(DIRECT_BUILD,P6_BUILD,P5_BUILD)

PARENT_TOKENS=p5.PARENT_TOKENS
PARENT_INDEX=p5.PARENT_INDEX
ANF_MASK=p5.ANF_MASK
NONLINEAR=p5.NONLINEAR
SWAP_TOKEN=p5.SWAP_TOKEN
TOKEN_APPLY=p5.TOKEN_APPLY

# meta_word: low 13 bits are m_est (0..4096), upper bits are edge-use count.
EST_BITS=13
EST_MASK=(1<<EST_BITS)-1
USE_INC=1<<EST_BITS
# sig_word: 20-bit a, 20-bit b, 4-bit token, propagated bit, valid bit.
ID_BITS=20
ID_MASK=(1<<ID_BITS)-1
B_SHIFT=ID_BITS
TOKEN_SHIFT=2*ID_BITS
PROP_BIT=1<<(TOKEN_SHIFT+4)
VALID_BIT=1<<(TOKEN_SHIFT+5)
MAX_NODES=1<<ID_BITS

@dataclass
class P6Stats:
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


def meta_est(n:base.Node)->int:
    return n.meta_word & EST_MASK


def meta_uses(n:base.Node)->int:
    return n.meta_word >> EST_BITS


def pack_sig(a:int,b:int,token:int,propagated:bool)->int:
    if not (0<=a<MAX_NODES and 0<=b<MAX_NODES):
        raise OverflowError(('P6 signature node id overflow',a,b,MAX_NODES))
    return VALID_BIT | (PROP_BIT if propagated else 0) | ((token&15)<<TOKEN_SHIFT) | (b<<B_SHIFT) | a


def sig_a(word:int)->int:
    return word & ID_MASK


def sig_b(word:int)->int:
    return (word>>B_SHIFT)&ID_MASK


def sig_token(word:int)->int:
    return (word>>TOKEN_SHIFT)&15


class InNode(base.Node):
    __slots__=('meta_word','sig_word')
    def __init__(self,nid:int,op:str,args:tuple[base.Node,...]=(),value=None):
        super().__init__(nid,op,args,value)
        self.meta_word=0
        self.sig_word=0


class InNodeFactory(base.Factory):
    """Ordinary Factory semantics plus exactly two integer annotation words per node."""
    def _align_code(self,child:InNode,a:int,b:int)->int:
        nid=child.nid
        if nid==a: return base.TOK_X
        if nid==b: return base.TOK_Y
        if child.op=='not':
            c=child.args[0].nid
            if c==a: return base.TOK_X ^ 15
            if c==b: return base.TOK_Y ^ 15
        w=child.sig_word
        if not (w & VALID_BIT): return -1
        sa=w&ID_MASK; sb=(w>>B_SHIFT)&ID_MASK; tok=(w>>TOKEN_SHIFT)&15
        if sa==a and sb==b: return tok|16
        if sa==b and sb==a: return SWAP_TOKEN[tok]|16|32
        return -1

    def _propagate_pair(self,op:str,left:InNode,right:InNode):
        lw=left.sig_word; rw=right.sig_word; opi=PARENT_INDEX[op]
        tried_a=-1; tried_b=-1
        if lw & VALID_BIT:
            a=lw&ID_MASK; b=(lw>>B_SHIFT)&ID_MASK; tried_a=a; tried_b=b
            lc=self._align_code(left,a,b); rc=self._align_code(right,a,b)
            if lc>=0 and rc>=0 and ((lc|rc)&16):
                return a,b,TOKEN_APPLY[opi][lc&15][rc&15]
        if rw & VALID_BIT:
            a=rw&ID_MASK; b=(rw>>B_SHIFT)&ID_MASK
            if a!=tried_a or b!=tried_b:
                lc=self._align_code(left,a,b); rc=self._align_code(right,a,b)
                if lc>=0 and rc>=0 and ((lc|rc)&16):
                    return a,b,TOKEN_APPLY[opi][lc&15][rc&15]
        return None

    def _estimate_new(self,op:str,args:tuple[InNode,...],value)->int:
        cap=p1.MONOMIAL_CAP
        if op=='const': return 1 if value else 0
        if op=='var': return 1
        if op=='not':
            x=(args[0].meta_word&EST_MASK)+1
            return cap if x>cap else x
        if op=='xor':
            x=(args[0].meta_word&EST_MASK)+(args[1].meta_word&EST_MASK)
            return cap if x>cap else x
        if op=='and':
            x=(args[0].meta_word&EST_MASK)*(args[1].meta_word&EST_MASK)
            return cap if x>cap else x
        if op=='or':
            a=args[0].meta_word&EST_MASK; b=args[1].meta_word&EST_MASK; x=a+b+a*b
            return cap if x>cap else x
        if op=='andn':
            m=1
            for c in args:
                m*=c.meta_word&EST_MASK
                if m>=cap: return cap
            return m
        if op=='orn':
            m=0
            for c in args:
                q=c.meta_word&EST_MASK; m=m+q+m*q
                if m>=cap: return cap
            return m
        if op=='tf':
            return p5.token_estimate_fast(int(value),args[0].meta_word&EST_MASK,args[1].meta_word&EST_MASK)
        raise ValueError(op)

    def _make(self,op,args=(),value=None):
        args=tuple(args)
        key=(op,tuple(a.nid for a in args),value)
        n=self.cache.get(key)
        if n is not None: return n
        nid=len(self.nodes)
        if nid>=MAX_NODES: raise OverflowError(('P6 node id overflow',nid,MAX_NODES))
        n=InNode(nid,op,args,value)
        self.cache[key]=n; self.nodes.append(n)
        for c in args: c.meta_word += USE_INC
        n.meta_word=self._estimate_new(op,args,value)
        if op in ('and','or','xor','tf') and len(args)==2:
            tok=PARENT_TOKENS[op] if op in PARENT_TOKENS else int(value)&15
            if op in PARENT_TOKENS:
                q=self._propagate_pair(op,args[0],args[1])
                if q is not None:
                    a,b,ct=q; n.sig_word=pack_sig(a,b,ct,True); return n
            n.sig_word=pack_sig(args[0].nid,args[1].nid,tok,False)
        return n


def clone_dag(root:base.Node,factory:base.Factory):
    return p5.clone_dag(root,factory)


def independent_refs(root:base.Node):
    return p5.independent_refs(root)


def validate_innode(root:InNode,factory:InNodeFactory):
    nodes,refs=independent_refs(root); issues=[]
    for nid,n in nodes.items():
        u=meta_uses(n)
        if u!=refs[nid]: issues.append(('fanout',nid,u,refs[nid]))
    memo={}
    for nid,n in nodes.items():
        exp=p1.estimate_monomials(n,memo); got=meta_est(n)
        if got!=exp: issues.append(('estimate',nid,got,exp))
    return issues


def compare_innode_to_p5(p6root:InNode,inf:InNodeFactory,p5root:base.Node,pf:p5.PackedMetaFactory):
    issues=[]
    if len(inf.nodes)!=len(pf.nodes): issues.append(('node_count',len(inf.nodes),len(pf.nodes)))
    lim=min(len(inf.nodes),len(pf.nodes))
    for nid in range(lim):
        a=inf.nodes[nid]; b=pf.nodes[nid]
        if a.op!=b.op or a.value!=b.value or tuple(c.nid for c in a.args)!=tuple(c.nid for c in b.args):
            issues.append(('node',nid,a.op,b.op,a.value,b.value)); continue
        if meta_uses(a)!=pf.uses[nid]: issues.append(('uses',nid,meta_uses(a),pf.uses[nid]))
        if meta_est(a)!=pf.est[nid]: issues.append(('est',nid,meta_est(a),pf.est[nid]))
        w=a.sig_word; pvalid=(pf.sig_a[nid]!=p5.SENTINEL)
        if bool(w&VALID_BIT)!=pvalid:
            issues.append(('sig_presence',nid,bool(w&VALID_BIT),pvalid))
        elif pvalid:
            got=(w&ID_MASK,(w>>B_SHIFT)&ID_MASK,(w>>TOKEN_SHIFT)&15)
            exp=(pf.sig_a[nid],pf.sig_b[nid],pf.sig_token[nid])
            if got!=exp: issues.append(('sig',nid,got,exp))
        got_prop=1 if (w&PROP_BIT) else 0
        exp_prop=int(pf.sig_propagated[nid])
        if got_prop!=exp_prop: issues.append(('prop_flag',nid,got_prop,exp_prop))
        if len(issues)>=20: break
    return issues


def lower_p6(root:InNode,inf:InNodeFactory,collect_stats:bool=True):
    ast=base.AnfStats(); dst=P6Stats(output_unique_nodes=base.reachable_nodes(root))
    if collect_stats:
        valid=prop=0
        for n in inf.nodes:
            w=n.sig_word
            valid += int(bool(w&VALID_BIT)); prop += int(bool(w&PROP_BIT))
        dst.signature_nodes=valid; dst.propagated_signature_nodes=prop; dst.propagated_candidate_nodes=prop
    memo={}; nodes=inf.nodes; align=inf._align_code

    def rec(n:InNode):
        nid=n.nid
        if nid in memo:
            ast.cache_hits+=1
            if collect_stats: dst.cse_hits+=1
            return memo[nid]
        ast.anf_nodes_evaluated+=1
        accepted=False; a=b=tl=tr=composed=0; lc=rc=-1
        if n.op in PARENT_TOKENS:
            if collect_stats: dst.selector_nodes_checked+=1
            w=n.sig_word
            if w&PROP_BIT:
                if collect_stats: dst.selector_candidates+=1
                a=w&ID_MASK; b=(w>>B_SHIFT)&ID_MASK; composed=(w>>TOKEN_SHIFT)&15
                left,right=n.args
                lc=align(left,a,b); rc=align(right,a,b)
                if lc<0 or rc<0 or not ((lc|rc)&16):
                    raise AssertionError(('P6 candidate alignment failure',nid,a,b,lc,rc))
                tl=lc&15; tr=rc&15
                an=nodes[a]; bn=nodes[b]; ma=an.meta_word&EST_MASK; mb=bn.meta_word&EST_MASK
                ml=p5.token_estimate_fast(tl,ma,mb); mr=p5.token_estimate_fast(tr,ma,mb)
                parent_pair=NONLINEAR[PARENT_TOKENS[n.op]]*ml*mr
                left_shell=bool(lc&16); right_shell=bool(rc&16)
                keep=parent_pair
                if left_shell and (left.meta_word>>EST_BITS)==1: keep += NONLINEAR[tl]*ma*mb
                if right_shell and (right.meta_word>>EST_BITS)==1: keep += NONLINEAR[tr]*ma*mb
                fold=NONLINEAR[composed]*ma*mb
                benefit=keep-fold
                shared=((left.meta_word>>EST_BITS)>1 or (right.meta_word>>EST_BITS)>1)
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


def run_direct_innode(root,inf,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(DIRECT_INNODE,poly,ast,oracle,nvars,t1-t0,peak,{'output_unique_nodes':base.reachable_nodes(root)})


def run_p6(root,inf,oracle,nvars,memory=False,collect_stats=True):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast,dst=lower_p6(root,inf,collect_stats=collect_stats); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(P6,poly,ast,oracle,nvars,t1-t0,peak,dataclasses.asdict(dst) if collect_stats else {})


def run_p5(root,pf,oracle,nvars,memory=False,collect_stats=True):
    r=p5.run_p5(root,pf,oracle,nvars,memory=memory,collect_stats=collect_stats)
    r['arm']=P5
    return r


def build_innode(root):
    f=InNodeFactory(); rr,_=clone_dag(root,f); return rr,f


def build_p5(root):
    return p5.build_packed(root)


def decision_equivalence(p6row,p5row):
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated',
            'selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared',
            'selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction',
            'selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost',
            'fold_lowerings','bypassed_child_shells','transpose_alignments')
    return {k:(p6row.get(k),p5row.get(k)) for k in fields if p6row.get(k)!=p5row.get(k)}


def run_symbolic(root,oracle,nvars,meta):
    p6root,inf=build_innode(root); p5root,pf=build_p5(root)
    issues=validate_innode(p6root,inf)
    if issues: raise AssertionError(f'P6 invariant failure {meta} {issues[:5]}')
    eq=compare_innode_to_p5(p6root,inf,p5root,pf)
    if eq: raise AssertionError(f'P6/P5 metadata drift {meta} {eq[:5]}')
    d=run_direct_original(root,oracle,nvars,True)
    di=run_direct_innode(p6root,inf,oracle,nvars,True)
    q=run_p6(p6root,inf,oracle,nvars,True,True)
    r=run_p5(p5root,pf,oracle,nvars,True,True)
    rows=[]
    for x in (d,di,q,r): x.update(meta); rows.append(x)
    if not all(x['ok'] for x in rows): raise AssertionError(f'oracle mismatch {meta}')
    if len({x['digest'] for x in rows})!=1: raise AssertionError(f'digest mismatch {meta}')
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes')
    bad={k:(d.get(k),di.get(k)) for k in fields if d.get(k)!=di.get(k)}
    if bad: raise AssertionError(f'P6 clone direct identity drift {meta} {bad}')
    bad=decision_equivalence(q,r)
    if bad: raise AssertionError(f'P6/P5 symbolic decision drift {meta} {bad}')
    if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P6 utilization')
    return rows,p6root,inf,p5root,pf


def run_lower_timing(p6root,inf,p5root,pf,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in LOWER_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        if arm==DIRECT_INNODE: r=run_direct_innode(p6root,inf,oracle,nvars,False)
        elif arm==P6: r=run_p6(p6root,inf,oracle,nvars,False,False)
        elif arm==P5: r=run_p5(p5root,pf,oracle,nvars,False,False)
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
    elif arm==P6_BUILD:
        f=InNodeFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast,_=lower_p6(rr,f,collect_stats=False); l1=time.perf_counter_ns()
    elif arm==P5_BUILD:
        f=p5.PackedMetaFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns()
        l0=time.perf_counter_ns(); poly,ast,_=p5.lower_p5(rr,f,collect_stats=False); l1=time.perf_counter_ns()
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
    rng=random.Random(SEED^0xF666); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        try:
            p6root,inf=build_innode(root); p5root,pf=build_p5(root)
            issues=validate_innode(p6root,inf)
            if issues: raise AssertionError(issues[:5])
            eq=compare_innode_to_p5(p6root,inf,p5root,pf)
            if eq: raise AssertionError(('metadata equivalence',eq[:5]))
            d=run_direct_original(root,oracle,nvars,False); di=run_direct_innode(p6root,inf,oracle,nvars,False)
            q=run_p6(p6root,inf,oracle,nvars,False,True); r=run_p5(p5root,pf,oracle,nvars,False,True)
            p4root,mf=p5.build_p4(root); y=p5.run_p4(p4root,mf,oracle,nvars,False,True)
            x=dict(p3.run_p3(root,oracle,nvars,memory=False)); z=dict(p3.run_p2(root,oracle,nvars,memory=False))
            db=run_pipeline_once(root,DIRECT_BUILD,oracle,nvars,False); qb=run_pipeline_once(root,P6_BUILD,oracle,nvars,False); rb=run_pipeline_once(root,P5_BUILD,oracle,nvars,False)
            allrows=(d,di,q,r,y,x,z,db,qb,rb)
            if not all(v.get('ok',False) for v in allrows): raise AssertionError('correctness')
            if len({v['digest'] for v in allrows})!=1: raise AssertionError('digest')
            fields=('multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated')
            bad={k:(d.get(k),di.get(k)) for k in fields if d.get(k)!=di.get(k)}
            if bad: raise AssertionError(('direct clone identity',bad))
            bad=decision_equivalence(q,r)
            if bad: raise AssertionError(('P6/P5 decision',bad))
            if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P6 utilization')
        except Exception as e:
            failures.append({'case':i,'nvars':nvars,'error':repr(e)})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def load_cases(): return p5.load_cases()
def generate_gate_cases(): return p5.generate_gate_cases()


def run_natural_case(case_id):
    cases,selection,selsha=load_cases(); by={c['case_id']:c for c in cases}; c=by[case_id]
    meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
    sym,p6root,inf,p5root,pf=run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x6600
    lower=run_lower_timing(p6root,inf,p5root,pf,c['oracle'],c['support'],meta,NATURAL_LOWER_REPS,seed)
    pipe=run_pipeline_timing(c['root_node'],c['oracle'],c['support'],meta,NATURAL_PIPE_REPS,seed^0xB17D)
    mem=[{**meta,**run_pipeline_once(c['root_node'],a,c['oracle'],c['support'],True)} for a in PIPE_ARMS]
    return {'schema':'cm-n2-p6-natural-case/v1','case_id':case_id,'selection_sha256':selsha,
            'symbolic_rows':sym,'lower_timing_rows':lower,'pipeline_timing_rows':pipe,'pipeline_memory_rows':mem}


def run_gatep():
    cases=generate_gate_cases(); sym=[]; lower=[]; pipe=[]; pmem=[]
    for depth,i,root,n,oracle in cases:
        meta={'depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        s,p6root,inf,p5root,pf=run_symbolic(root,oracle,n,meta); sym.extend(s)
        seed=SEED+depth*1000+i+0x6600
        lower.extend(run_lower_timing(p6root,inf,p5root,pf,oracle,n,meta,GATEP_LOWER_REPS,seed))
        pipe.extend(run_pipeline_timing(root,oracle,n,meta,GATEP_PIPE_REPS,seed^0xB17D))
        pmem.extend([{**meta,**run_pipeline_once(root,a,oracle,n,True)} for a in PIPE_ARMS])
    return {'schema':'cm-n2-p6-gatep/v1','symbolic_rows':sym,'lower_timing_rows':lower,
            'pipeline_timing_rows':pipe,'pipeline_memory_rows':pmem}


def main():
    if sha256_file(HERE/'N2_P6_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P6 preregistration hash mismatch')
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
