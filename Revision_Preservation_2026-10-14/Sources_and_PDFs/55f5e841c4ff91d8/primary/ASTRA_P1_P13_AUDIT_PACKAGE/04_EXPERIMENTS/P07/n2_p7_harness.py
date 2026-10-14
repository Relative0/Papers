from __future__ import annotations
import argparse, dataclasses, hashlib, json, random, sys, time, tracemalloc
from array import array
from dataclasses import dataclass
from pathlib import Path

HERE=Path(__file__).resolve().parent
P6_DIR=HERE.parent/'cm_n2_p6_run'
if str(P6_DIR) not in sys.path: sys.path.insert(0,str(P6_DIR))
import n2_p6_harness as p6
p5=p6.p5; p4=p6.p4; p3=p6.p3; p2=p6.p2; p1=p6.p1; base=p6.base

SEED=20260918
PREREG_SHA256='eb581a115b6d5a8214787d642d9ea496e8b6f9cb2439e9973017c083bf11ff9a'
NATURAL_LOWER_REPS=25
GATEP_LOWER_REPS=25
NATURAL_PIPE_REPS=15
GATEP_PIPE_REPS=15
FUZZ_CASES=1000

DIRECT_CWORD='direct_cword_sparse_anf'
P7='cm_cword_sig_sparse'
P6='cm_innode_sig_sparse'
P5='cm_packed_sig_sparse'
DIRECT_ORIG='direct_sparse_anf'
DIRECT_BUILD='direct_build_sparse'
P7_BUILD='cm_cword_sig_build_sparse'
P6_BUILD='cm_innode_sig_build_sparse'
P5_BUILD='cm_packed_sig_build_sparse'
LOWER_ARMS=(DIRECT_CWORD,P7,P6,P5)
PIPE_ARMS=(DIRECT_BUILD,P7_BUILD,P6_BUILD,P5_BUILD)

PARENT_TOKENS=p6.PARENT_TOKENS
PARENT_INDEX=p6.PARENT_INDEX
NONLINEAR=p6.NONLINEAR
SWAP_TOKEN=p6.SWAP_TOKEN
TOKEN_APPLY=p6.TOKEN_APPLY
EST_BITS=p6.EST_BITS; EST_MASK=p6.EST_MASK; USE_INC=p6.USE_INC
ID_BITS=p6.ID_BITS; ID_MASK=p6.ID_MASK; B_SHIFT=p6.B_SHIFT; TOKEN_SHIFT=p6.TOKEN_SHIFT
PROP_BIT=p6.PROP_BIT; VALID_BIT=p6.VALID_BIT; MAX_NODES=p6.MAX_NODES

@dataclass
class P7Stats:
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


def pack_sig(a:int,b:int,token:int,propagated:bool)->int:
    return p6.pack_sig(a,b,token,propagated)


class CWordFactory(base.Factory):
    """Ordinary Node objects plus exactly two C-backed uint64 annotation arrays."""
    __slots__=('cache','nodes','meta_word','sig_word')
    def __init__(self):
        super().__init__()
        self.meta_word=array('Q')
        self.sig_word=array('Q')

    def _align_code(self,child:base.Node,a:int,b:int)->int:
        nid=child.nid
        if nid==a: return base.TOK_X
        if nid==b: return base.TOK_Y
        if child.op=='not':
            c=child.args[0].nid
            if c==a: return base.TOK_X ^ 15
            if c==b: return base.TOK_Y ^ 15
        w=self.sig_word[nid]
        if not (w & VALID_BIT): return -1
        sa=w&ID_MASK; sb=(w>>B_SHIFT)&ID_MASK; tok=(w>>TOKEN_SHIFT)&15
        if sa==a and sb==b: return tok|16
        if sa==b and sb==a: return SWAP_TOKEN[tok]|16|32
        return -1

    def _propagate_pair(self,op:str,left:base.Node,right:base.Node):
        lw=self.sig_word[left.nid]; rw=self.sig_word[right.nid]; opi=PARENT_INDEX[op]
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

    def _estimate_new(self,op:str,args:tuple[base.Node,...],value)->int:
        cap=p1.MONOMIAL_CAP; meta=self.meta_word
        if op=='const': return 1 if value else 0
        if op=='var': return 1
        if op=='not':
            x=(meta[args[0].nid]&EST_MASK)+1; return cap if x>cap else x
        if op=='xor':
            x=(meta[args[0].nid]&EST_MASK)+(meta[args[1].nid]&EST_MASK); return cap if x>cap else x
        if op=='and':
            x=(meta[args[0].nid]&EST_MASK)*(meta[args[1].nid]&EST_MASK); return cap if x>cap else x
        if op=='or':
            a=meta[args[0].nid]&EST_MASK; b=meta[args[1].nid]&EST_MASK; x=a+b+a*b; return cap if x>cap else x
        if op=='andn':
            m=1
            for c in args:
                m*=meta[c.nid]&EST_MASK
                if m>=cap: return cap
            return m
        if op=='orn':
            m=0
            for c in args:
                q=meta[c.nid]&EST_MASK; m=m+q+m*q
                if m>=cap: return cap
            return m
        if op=='tf':
            return p5.token_estimate_fast(int(value),meta[args[0].nid]&EST_MASK,meta[args[1].nid]&EST_MASK)
        raise ValueError(op)

    def _make(self,op,args=(),value=None):
        args=tuple(args); key=(op,tuple(a.nid for a in args),value)
        n=self.cache.get(key)
        if n is not None: return n
        nid=len(self.nodes)
        if nid>=MAX_NODES: raise OverflowError(('P7 node id overflow',nid,MAX_NODES))
        n=base.Node(nid,op,args,value)
        self.cache[key]=n; self.nodes.append(n)
        self.meta_word.append(0); self.sig_word.append(0)
        for c in args: self.meta_word[c.nid] += USE_INC
        self.meta_word[nid]=self._estimate_new(op,args,value)
        if op in ('and','or','xor','tf') and len(args)==2:
            tok=PARENT_TOKENS[op] if op in PARENT_TOKENS else int(value)&15
            if op in PARENT_TOKENS:
                q=self._propagate_pair(op,args[0],args[1])
                if q is not None:
                    a,b,ct=q; self.sig_word[nid]=pack_sig(a,b,ct,True); return n
            self.sig_word[nid]=pack_sig(args[0].nid,args[1].nid,tok,False)
        return n


def clone_dag(root,factory): return p5.clone_dag(root,factory)
def independent_refs(root): return p5.independent_refs(root)


def validate_cword(root:base.Node,cf:CWordFactory):
    nodes,refs=independent_refs(root); issues=[]
    for nid,n in nodes.items():
        u=cf.meta_word[nid]>>EST_BITS
        if u!=refs[nid]: issues.append(('fanout',nid,u,refs[nid]))
    memo={}
    for nid,n in nodes.items():
        exp=p1.estimate_monomials(n,memo); got=cf.meta_word[nid]&EST_MASK
        if got!=exp: issues.append(('estimate',nid,got,exp))
    return issues


def compare_cword_to_p6(p7root,cf,p6root,inf):
    issues=[]
    if len(cf.nodes)!=len(inf.nodes): issues.append(('node_count',len(cf.nodes),len(inf.nodes)))
    for nid in range(min(len(cf.nodes),len(inf.nodes))):
        a=cf.nodes[nid]; b=inf.nodes[nid]
        if a.op!=b.op or a.value!=b.value or tuple(c.nid for c in a.args)!=tuple(c.nid for c in b.args):
            issues.append(('node',nid)); continue
        if cf.meta_word[nid]!=b.meta_word: issues.append(('meta_word',nid,cf.meta_word[nid],b.meta_word))
        if cf.sig_word[nid]!=b.sig_word: issues.append(('sig_word',nid,cf.sig_word[nid],b.sig_word))
        if len(issues)>=20: break
    return issues


def compare_cword_to_p5(p7root,cf,p5root,pf):
    issues=[]
    if len(cf.nodes)!=len(pf.nodes): issues.append(('node_count',len(cf.nodes),len(pf.nodes)))
    for nid in range(min(len(cf.nodes),len(pf.nodes))):
        a=cf.nodes[nid]; b=pf.nodes[nid]
        if a.op!=b.op or a.value!=b.value or tuple(c.nid for c in a.args)!=tuple(c.nid for c in b.args):
            issues.append(('node',nid)); continue
        m=cf.meta_word[nid]; uses=m>>EST_BITS; est=m&EST_MASK
        if uses!=pf.uses[nid]: issues.append(('uses',nid,uses,pf.uses[nid]))
        if est!=pf.est[nid]: issues.append(('est',nid,est,pf.est[nid]))
        w=cf.sig_word[nid]; pvalid=(pf.sig_a[nid]!=p5.SENTINEL)
        if bool(w&VALID_BIT)!=pvalid: issues.append(('sig_presence',nid))
        elif pvalid:
            got=(w&ID_MASK,(w>>B_SHIFT)&ID_MASK,(w>>TOKEN_SHIFT)&15,int(bool(w&PROP_BIT)))
            exp=(pf.sig_a[nid],pf.sig_b[nid],pf.sig_token[nid],int(pf.sig_propagated[nid]))
            if got!=exp: issues.append(('sig',nid,got,exp))
        if len(issues)>=20: break
    return issues


def lower_p7(root:base.Node,cf:CWordFactory,collect_stats:bool=True):
    ast=base.AnfStats(); dst=P7Stats(output_unique_nodes=base.reachable_nodes(root))
    meta=cf.meta_word; sig=cf.sig_word; nodes=cf.nodes; align=cf._align_code
    if collect_stats:
        dst.signature_nodes=sum(1 for w in sig if w&VALID_BIT)
        dst.propagated_signature_nodes=sum(1 for w in sig if w&PROP_BIT)
        dst.propagated_candidate_nodes=dst.propagated_signature_nodes
    memo={}
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
            w=sig[nid]
            if w&PROP_BIT:
                if collect_stats: dst.selector_candidates+=1
                a=w&ID_MASK; b=(w>>B_SHIFT)&ID_MASK; composed=(w>>TOKEN_SHIFT)&15
                left,right=n.args; lc=align(left,a,b); rc=align(right,a,b)
                if lc<0 or rc<0 or not ((lc|rc)&16): raise AssertionError(('P7 alignment',nid,a,b,lc,rc))
                tl=lc&15; tr=rc&15; ma=meta[a]&EST_MASK; mb=meta[b]&EST_MASK
                ml=p5.token_estimate_fast(tl,ma,mb); mr=p5.token_estimate_fast(tr,ma,mb)
                parent_pair=NONLINEAR[PARENT_TOKENS[n.op]]*ml*mr
                keep=parent_pair
                if (lc&16) and (meta[left.nid]>>EST_BITS)==1: keep += NONLINEAR[tl]*ma*mb
                if (rc&16) and (meta[right.nid]>>EST_BITS)==1: keep += NONLINEAR[tr]*ma*mb
                fold=NONLINEAR[composed]*ma*mb; benefit=keep-fold
                shared=((meta[left.nid]>>EST_BITS)>1 or (meta[right.nid]>>EST_BITS)>1)
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
                dst.bypassed_child_shells+=int(bool(lc&16))+int(bool(rc&16))
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
                            x,y=level[i],level[i+1]; nxt.append(base.xor_poly(base.xor_poly(x,y),base.mul_poly(x,y,ast)))
                    level=nxt
                p=level[0]
        elif n.op=='tf': p=p3.apply_tf_poly(int(n.value),rec(n.args[0]),rec(n.args[1]),ast)
        else: raise ValueError(n.op)
        memo[nid]=p; base.update_peak(p,ast); return p
    poly=rec(root); return poly,ast,dst


def _finish_row(arm,poly,ast,oracle,nvars,lower_ns,peak,extra=None):
    got=base.anf_to_bitset(poly,nvars)
    row={'arm':arm,'ok':got==oracle,'lower_ns':lower_ns,'compile_ns':lower_ns,'python_peak_bytes':peak,
         'digest':base.poly_digest(poly),'final_monomials':len(poly),'final_degree':max((m.bit_count() for m in poly),default=0),
         **dataclasses.asdict(ast)}
    if extra: row.update(extra)
    return row


def run_direct_original(root,oracle,nvars,memory=False): return p6.run_direct_original(root,oracle,nvars,memory)

def run_direct_cword(root,cf,oracle,nvars,memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast=base.lower_anf(root); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(DIRECT_CWORD,poly,ast,oracle,nvars,t1-t0,peak,{'output_unique_nodes':base.reachable_nodes(root)})

def run_p7(root,cf,oracle,nvars,memory=False,collect_stats=True):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); poly,ast,dst=lower_p7(root,cf,collect_stats); t1=time.perf_counter_ns()
    peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return _finish_row(P7,poly,ast,oracle,nvars,t1-t0,peak,dataclasses.asdict(dst) if collect_stats else {})

def run_p6(root,inf,oracle,nvars,memory=False,collect_stats=True):
    r=p6.run_p6(root,inf,oracle,nvars,memory,collect_stats); r['arm']=P6; return r

def run_p5(root,pf,oracle,nvars,memory=False,collect_stats=True):
    r=p6.run_p5(root,pf,oracle,nvars,memory,collect_stats); r['arm']=P5; return r


def build_cword(root):
    f=CWordFactory(); rr,_=clone_dag(root,f); return rr,f

def build_p6(root): return p6.build_innode(root)
def build_p5(root): return p6.build_p5(root)

DECISION_FIELDS=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated',
                 'selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared',
                 'selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction',
                 'selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost',
                 'fold_lowerings','bypassed_child_shells','transpose_alignments')

def decision_equivalence(a,b): return {k:(a.get(k),b.get(k)) for k in DECISION_FIELDS if a.get(k)!=b.get(k)}


def run_symbolic(root,oracle,nvars,meta):
    p7root,cf=build_cword(root); p6root,inf=build_p6(root); p5root,pf=build_p5(root)
    issues=validate_cword(p7root,cf)
    if issues: raise AssertionError(f'P7 invariant failure {meta} {issues[:5]}')
    eq=compare_cword_to_p6(p7root,cf,p6root,inf)
    if eq: raise AssertionError(f'P7/P6 metadata drift {meta} {eq[:5]}')
    eq=compare_cword_to_p5(p7root,cf,p5root,pf)
    if eq: raise AssertionError(f'P7/P5 metadata drift {meta} {eq[:5]}')
    d=run_direct_original(root,oracle,nvars,True); dc=run_direct_cword(p7root,cf,oracle,nvars,True)
    q=run_p7(p7root,cf,oracle,nvars,True,True); r6=run_p6(p6root,inf,oracle,nvars,True,True); r5=run_p5(p5root,pf,oracle,nvars,True,True)
    rows=[]
    for x in (d,dc,q,r6,r5): x.update(meta); rows.append(x)
    if not all(x['ok'] for x in rows): raise AssertionError(f'oracle mismatch {meta}')
    if len({x['digest'] for x in rows})!=1: raise AssertionError(f'digest mismatch {meta}')
    fields=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated','output_unique_nodes')
    bad={k:(d.get(k),dc.get(k)) for k in fields if d.get(k)!=dc.get(k)}
    if bad: raise AssertionError(f'P7 clone direct identity drift {meta} {bad}')
    bad=decision_equivalence(q,r6)
    if bad: raise AssertionError(f'P7/P6 symbolic drift {meta} {bad}')
    bad=decision_equivalence(q,r5)
    if bad: raise AssertionError(f'P7/P5 symbolic drift {meta} {bad}')
    if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P7 utilization')
    return rows,p7root,cf,p6root,inf,p5root,pf


def run_lower_timing(p7root,cf,p6root,inf,p5root,pf,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in LOWER_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        if arm==DIRECT_CWORD: r=run_direct_cword(p7root,cf,oracle,nvars,False)
        elif arm==P7: r=run_p7(p7root,cf,oracle,nvars,False,False)
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
        f=base.Factory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns(); l0=time.perf_counter_ns(); poly,ast=base.lower_anf(rr); l1=time.perf_counter_ns()
    elif arm==P7_BUILD:
        f=CWordFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns(); l0=time.perf_counter_ns(); poly,ast,_=lower_p7(rr,f,False); l1=time.perf_counter_ns()
    elif arm==P6_BUILD:
        f=p6.InNodeFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns(); l0=time.perf_counter_ns(); poly,ast,_=p6.lower_p6(rr,f,False); l1=time.perf_counter_ns()
    elif arm==P5_BUILD:
        f=p5.PackedMetaFactory(); b0=time.perf_counter_ns(); rr,_=clone_dag(root,f); b1=time.perf_counter_ns(); l0=time.perf_counter_ns(); poly,ast,_=p5.lower_p5(rr,f,False); l1=time.perf_counter_ns()
    else: raise ValueError(arm)
    t1=time.perf_counter_ns(); peak=None
    if memory: _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=base.anf_to_bitset(poly,nvars)
    return {'arm':arm,'ok':got==oracle,'pipeline_ns':t1-t0,'dag_build_ns':b1-b0,'lower_ns':l1-l0,'python_peak_bytes':peak,
            'digest':base.poly_digest(poly),'final_monomials':len(poly),'final_degree':max((m.bit_count() for m in poly),default=0),**dataclasses.asdict(ast)}


def run_pipeline_timing(root,oracle,nvars,meta,reps,seed):
    rng=random.Random(seed); schedule=[a for _ in range(reps) for a in PIPE_ARMS]; rng.shuffle(schedule); rows=[]
    for rep,arm in enumerate(schedule):
        r=run_pipeline_once(root,arm,oracle,nvars,False)
        if not r['ok']: raise AssertionError(f'pipeline mismatch {meta} {arm}')
        rows.append({**meta,'rep':rep,'arm':arm,'pipeline_ns':r['pipeline_ns'],'dag_build_ns':r['dag_build_ns'],'lower_ns':r['lower_ns'],'ok':True})
    return rows


def fresh_fuzz():
    rng=random.Random(SEED^0xF777); failures=[]
    for i in range(FUZZ_CASES):
        f=base.Factory(); nvars=rng.randint(2,8); root=base.random_expr(rng,nvars,rng.randint(2,8),f); oracle=base.eval_node_bitset(root,nvars)
        try:
            p7root,cf=build_cword(root); p6root,inf=build_p6(root); p5root,pf=build_p5(root)
            issues=validate_cword(p7root,cf)
            if issues: raise AssertionError(issues[:5])
            eq=compare_cword_to_p6(p7root,cf,p6root,inf)
            if eq: raise AssertionError(('P7/P6 metadata',eq[:5]))
            eq=compare_cword_to_p5(p7root,cf,p5root,pf)
            if eq: raise AssertionError(('P7/P5 metadata',eq[:5]))
            d=run_direct_original(root,oracle,nvars); dc=run_direct_cword(p7root,cf,oracle,nvars)
            q=run_p7(p7root,cf,oracle,nvars,False,True); r6=run_p6(p6root,inf,oracle,nvars,False,True); r5=run_p5(p5root,pf,oracle,nvars,False,True)
            p4root,mf=p5.build_p4(root); y=p5.run_p4(p4root,mf,oracle,nvars,False,True)
            x=dict(p3.run_p3(root,oracle,nvars,memory=False)); z=dict(p3.run_p2(root,oracle,nvars,memory=False))
            db=run_pipeline_once(root,DIRECT_BUILD,oracle,nvars); qb=run_pipeline_once(root,P7_BUILD,oracle,nvars); q6b=run_pipeline_once(root,P6_BUILD,oracle,nvars); q5b=run_pipeline_once(root,P5_BUILD,oracle,nvars)
            allrows=(d,dc,q,r6,r5,y,x,z,db,qb,q6b,q5b)
            if not all(v.get('ok',False) for v in allrows): raise AssertionError('correctness')
            if len({v['digest'] for v in allrows})!=1: raise AssertionError('digest')
            fields=('multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated')
            bad={k:(d.get(k),dc.get(k)) for k in fields if d.get(k)!=dc.get(k)}
            if bad: raise AssertionError(('direct clone identity',bad))
            if decision_equivalence(q,r6): raise AssertionError(('P7/P6 decision',decision_equivalence(q,r6)))
            if decision_equivalence(q,r5): raise AssertionError(('P7/P5 decision',decision_equivalence(q,r5)))
            if q.get('selector_accepted',0)!=q.get('fold_lowerings',0): raise AssertionError('P7 utilization')
        except Exception as e:
            failures.append({'case':i,'nvars':nvars,'error':repr(e)})
            if len(failures)>=20: break
    return {'cases':FUZZ_CASES,'failures':failures,'passed':not failures}


def load_cases(): return p6.load_cases()
def generate_gate_cases(): return p6.generate_gate_cases()


def run_natural_case(case_id):
    cases,selection,selsha=load_cases(); by={c['case_id']:c for c in cases}; c=by[case_id]
    meta={k:v for k,v in c.items() if k not in ('root_node','oracle','support_names')}
    sym,p7root,cf,p6root,inf,p5root,pf=run_symbolic(c['root_node'],c['oracle'],c['support'],meta)
    seed=SEED ^ int(hashlib.sha256(case_id.encode()).hexdigest()[:8],16) ^ 0x7700
    lower=run_lower_timing(p7root,cf,p6root,inf,p5root,pf,c['oracle'],c['support'],meta,NATURAL_LOWER_REPS,seed)
    pipe=run_pipeline_timing(c['root_node'],c['oracle'],c['support'],meta,NATURAL_PIPE_REPS,seed^0xB17D)
    mem=[{**meta,**run_pipeline_once(c['root_node'],a,c['oracle'],c['support'],True)} for a in PIPE_ARMS]
    return {'schema':'cm-n2-p7-natural-case/v1','case_id':case_id,'selection_sha256':selsha,'symbolic_rows':sym,
            'lower_timing_rows':lower,'pipeline_timing_rows':pipe,'pipeline_memory_rows':mem}


def run_gatep():
    cases=generate_gate_cases(); sym=[]; lower=[]; pipe=[]; pmem=[]
    for depth,i,root,n,oracle in cases:
        meta={'depth':depth,'case':i,'case_id':f'{depth}:{i}'}
        s,p7root,cf,p6root,inf,p5root,pf=run_symbolic(root,oracle,n,meta); sym.extend(s)
        seed=SEED+depth*1000+i+0x7700
        lower.extend(run_lower_timing(p7root,cf,p6root,inf,p5root,pf,oracle,n,meta,GATEP_LOWER_REPS,seed))
        pipe.extend(run_pipeline_timing(root,oracle,n,meta,GATEP_PIPE_REPS,seed^0xB17D))
        pmem.extend([{**meta,**run_pipeline_once(root,a,oracle,n,True)} for a in PIPE_ARMS])
    return {'schema':'cm-n2-p7-gatep/v1','symbolic_rows':sym,'lower_timing_rows':lower,'pipeline_timing_rows':pipe,'pipeline_memory_rows':pmem}


def main():
    if sha256_file(HERE/'N2_P7_PREREGISTRATION.md')!=PREREG_SHA256: raise SystemExit('P7 preregistration hash mismatch')
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=('fuzz','gatep','natural-case','selection'),required=True); ap.add_argument('--case-id'); ap.add_argument('--out',required=True); a=ap.parse_args()
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
