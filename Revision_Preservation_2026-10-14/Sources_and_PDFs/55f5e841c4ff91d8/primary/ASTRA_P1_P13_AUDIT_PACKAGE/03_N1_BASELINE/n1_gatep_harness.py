from __future__ import annotations
import argparse, dataclasses, hashlib, json, math, os, platform, random, statistics, time, tracemalloc
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

# Frozen protocol constants: set before any timing measurements.
SEED = 20260917
ARMS = ("direct_sparse_anf", "cse_flat_sparse", "generic_2support_sparse", "cm_frontend_sparse")
NATURAL_SUPPORT_MIN = 9
NATURAL_SUPPORT_MAX = 12
COLD_REPS = 15
WARM_REUSES = (8, 32, 128)
GATEP_DEPTHS = (6, 8, 10)
GATEP_CASES_PER_DEPTH = 12
GATEP_TIMING_REPS = 15
FUZZ_CASES = 500
N1_CM_ADVANTAGE_THRESHOLD = 0.05  # paired improvement over generic required on natural stratum
GATEP_TIMING_THRESHOLD = 0.10      # exploratory implementation-level threshold
EXPECTED_EPFL_GIT_BLOB = "ac0cb9d3f2f576f05a14ceb2604a843c16526c8e"

# Four-bit truth tokens: bit index = 2*x+y, i.e. 00,01,10,11.
TOK_AND = 0b1000
TOK_OR  = 0b1110
TOK_XOR = 0b0110
TOK_X   = 0b1100
TOK_Y   = 0b1010
TOK_0   = 0b0000
TOK_1   = 0b1111

class Node:
    __slots__ = ("nid", "op", "args", "value")
    def __init__(self, nid:int, op:str, args:tuple["Node",...]=(), value=None):
        self.nid=nid; self.op=op; self.args=args; self.value=value
    def __repr__(self):
        if self.op == 'var': return f"v{self.value}"
        if self.op == 'const': return str(self.value)
        if self.op == 'tf': return f"TF({self.value:04b},{self.args[0].nid},{self.args[1].nid})"
        return f"{self.op}({','.join(str(a.nid) for a in self.args)})"

class Factory:
    def __init__(self):
        self.cache = {}
        self.nodes = []
    def _make(self, op, args=(), value=None):
        key=(op, tuple(a.nid for a in args), value)
        n=self.cache.get(key)
        if n is None:
            n=Node(len(self.nodes), op, tuple(args), value)
            self.cache[key]=n; self.nodes.append(n)
        return n
    def var(self, i): return self._make('var',(),int(i))
    def const(self, v): return self._make('const',(),1 if v else 0)
    def not_(self,a):
        if a.op=='const': return self.const(1-a.value)
        if a.op=='not': return a.args[0]
        return self._make('not',(a,))
    def bin(self,op,a,b):
        # Only safe local Boolean identities; preserve operand order otherwise.
        if op=='and':
            if a.op=='const': return b if a.value else a
            if b.op=='const': return a if b.value else b
            if a is b: return a
        elif op=='or':
            if a.op=='const': return a if a.value else b
            if b.op=='const': return b if b.value else a
            if a is b: return a
        elif op=='xor':
            if a.op=='const': return self.not_(b) if a.value else b
            if b.op=='const': return self.not_(a) if b.value else a
            if a is b: return self.const(0)
        return self._make(op,(a,b))
    def nary(self,op,args):
        args=tuple(args)
        if not args: return self.const(1 if op=='andn' else 0)
        if len(args)==1: return args[0]
        return self._make(op,args)
    def tf(self,token,a,b):
        token &= 15
        if token==TOK_0: return self.const(0)
        if token==TOK_1: return self.const(1)
        if token==TOK_X: return a
        if token==TOK_Y: return b
        if token==(TOK_X ^ 15): return self.not_(a)
        if token==(TOK_Y ^ 15): return self.not_(b)
        if a is b:
            v0=(token>>0)&1; v1=(token>>3)&1
            if v0==v1: return self.const(v0)
            return a if (v0,v1)==(0,1) else self.not_(a)
        return self._make('tf',(a,b),token)

def balanced(factory:Factory, op:str, items:list[Node], identity:int) -> Node:
    if not items: return factory.const(identity)
    cur=list(items)
    while len(cur)>1:
        nxt=[]
        for i in range(0,len(cur),2):
            nxt.append(cur[i] if i+1==len(cur) else factory.bin(op,cur[i],cur[i+1]))
        cur=nxt
    return cur[0]

@dataclass
class BlifNode:
    inputs: tuple[str,...]
    cubes: tuple[str,...]
    cube_output: int

@dataclass
class Blif:
    inputs: tuple[str,...]
    outputs: tuple[str,...]
    nodes: dict[str,BlifNode]


def logical_lines(path:Path):
    out=[]; pending=''
    for raw in path.read_text(encoding='utf-8').splitlines():
        line=raw.split('#',1)[0].strip()
        if not line: continue
        pending=(pending+' '+line).strip() if pending else line
        if pending.endswith('\\'):
            pending=pending[:-1].rstrip(); continue
        out.append(pending); pending=''
    if pending: raise ValueError('unterminated continuation')
    return out

def parse_blif(path:Path) -> Blif:
    lines=logical_lines(path); inputs=[]; outputs=[]; nodes={}; i=0
    while i<len(lines):
        parts=lines[i].split(); d=parts[0]
        if d=='.inputs': inputs.extend(parts[1:])
        elif d=='.outputs': outputs.extend(parts[1:])
        elif d=='.names':
            fanins=tuple(parts[1:-1]); out=parts[-1]; cubes=[]; cube_output=None; i+=1
            while i<len(lines) and not lines[i].startswith('.'):
                row=lines[i].split()
                if fanins:
                    if len(row)!=2: raise ValueError(f'bad truth row: {lines[i]}')
                    patt, bit=row
                    if len(patt)!=len(fanins) or any(c not in '01-' for c in patt) or bit not in ('0','1'):
                        raise ValueError('bad cube')
                else:
                    patt=''; bit=row[0]
                b=int(bit)
                if cube_output is None: cube_output=b
                elif cube_output!=b: raise ValueError('mixed cube outputs unsupported')
                cubes.append(patt); i+=1
            nodes[out]=BlifNode(fanins,tuple(cubes),1 if cube_output is None else cube_output)
            continue
        elif d=='.end': break
        i+=1
    return Blif(tuple(inputs),tuple(outputs),nodes)

def structural_support(blif:Blif, root:str):
    inputs=set(blif.inputs); memo={}
    def rec(s):
        if s in inputs: return frozenset((s,))
        if s in memo: return memo[s]
        n=blif.nodes[s]; sup=set()
        relevant={j for cube in n.cubes for j,ch in enumerate(cube) if ch in '01'}
        for j,ch in enumerate(n.inputs):
            if j in relevant: sup.update(rec(ch))
        memo[s]=frozenset(sup); return memo[s]
    return rec(root)

def build_expr(blif:Blif, root:str, factory:Factory):
    varmap={name:factory.var(i) for i,name in enumerate(blif.inputs)}; memo={}; active=set()
    def rec(s):
        if s in varmap: return varmap[s]
        if s in memo: return memo[s]
        if s in active: raise ValueError('cycle')
        active.add(s); n=blif.nodes[s]; cubes=[]
        for patt in n.cubes:
            lits=[]
            for bit,ch in zip(patt,n.inputs):
                if bit=='-': continue
                c=rec(ch); lits.append(c if bit=='1' else factory.not_(c))
            cubes.append(balanced(factory,'and',lits,1))
        val=balanced(factory,'or',cubes,0)
        if n.cube_output==0: val=factory.not_(val)
        active.remove(s); memo[s]=val; return val
    return rec(root)

def reachable_nodes(root:Node):
    seen=set(); stack=[root]
    while stack:
        n=stack.pop()
        if n.nid in seen: continue
        seen.add(n.nid); stack.extend(n.args)
    return len(seen)

def bitset_env(n):
    count=1<<n; env=[]
    for i in range(n):
        x=0
        for a in range(count):
            if (a>>i)&1: x |= 1<<a
        env.append(x)
    return env

def eval_blif_bitset(blif:Blif, root:str):
    nvars=len(blif.inputs); env=bitset_env(nvars); vals={name:env[i] for i,name in enumerate(blif.inputs)}
    mask=(1<<(1<<nvars))-1; active=set()
    def rec(s):
        if s in vals: return vals[s]
        if s in active: raise ValueError('cycle')
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

def token_apply(op:str,t1:int,t2:int):
    out=0
    for q in range(4):
        a=(t1>>q)&1; b=(t2>>q)&1
        v=(a & b) if op=='and' else ((a|b) if op=='or' else (a^b))
        out |= v<<q
    return out

def swap_token(t:int):
    # 00,01,10,11 -> 00,10,01,11
    return (t&1) | (((t>>2)&1)<<1) | (((t>>1)&1)<<2) | (t&8)

def base_token_for(node:Node,a:Node,b:Node):
    if node is a: return TOK_X
    if node is b: return TOK_Y
    if node.op=='not' and node.args[0] is a: return TOK_X ^ 15
    if node.op=='not' and node.args[0] is b: return TOK_Y ^ 15
    if node.op=='tf':
        x,y=node.args
        if x is a and y is b: return node.value
        if x is b and y is a: return swap_token(node.value)
    return None

@dataclass
class OptStats:
    successful_folds:int=0
    same_operand_folds:int=0
    transpose_alignments:int=0
    cut_retabulations:int=0
    cse_hits:int=0
    associative_flattened_nodes:int=0
    commutative_reorders:int=0
    output_unique_nodes:int=0


def fold_frontend(root:Node, mode:str, sharing_guard:bool=False):
    """CM: local operator composition on a common ordered operand pair.
    Generic: same local fold plus arbitrary primary-support<=2 retabulation.
    Both are followed by a structural CSE/flattening pass.
    """
    f=Factory(); stats=OptStats(); memo={}; support_memo={}; evaltok_memo={}
    source_refs=defaultdict(int); _seen=set(); _stack=[root]
    while _stack:
        _n=_stack.pop()
        if _n.nid in _seen: continue
        _seen.add(_n.nid)
        for _c in _n.args:
            source_refs[_c.nid]+=1; _stack.append(_c)
    var_cache={}
    def clone_var(v):
        if v.value not in var_cache: var_cache[v.value]=f.var(v.value)
        return var_cache[v.value]
    def psup(n:Node):
        if n.nid in support_memo: return support_memo[n.nid]
        if n.op=='var': s=frozenset((n.value,))
        elif n.op=='const': s=frozenset()
        else:
            u=set()
            for a in n.args: u.update(psup(a))
            s=frozenset(u)
        support_memo[n.nid]=s; return s
    def bool_eval(n:Node, assign:dict[int,int]):
        key=(n.nid,tuple(sorted(assign.items())))
        if key in evaltok_memo: return evaltok_memo[key]
        if n.op=='const': v=n.value
        elif n.op=='var': v=assign[n.value]
        elif n.op=='not': v=1-bool_eval(n.args[0],assign)
        elif n.op in ('and','or','xor'):
            a=bool_eval(n.args[0],assign); b=bool_eval(n.args[1],assign)
            v=(a&b) if n.op=='and' else ((a|b) if n.op=='or' else (a^b))
        elif n.op in ('andn','orn'):
            vals=[bool_eval(a,assign) for a in n.args]
            v=(all(vals) if n.op=='andn' else any(vals)); v=int(v)
        elif n.op=='tf':
            a=bool_eval(n.args[0],assign); b=bool_eval(n.args[1],assign); v=(n.value>>(2*a+b))&1
        else: raise ValueError(n.op)
        evaltok_memo[key]=v; return v
    def generic_retab(n:Node):
        s=sorted(psup(n))
        if len(s)>2 or n.op in ('const','var'): return n
        if len(s)==0: return f.const(bool_eval(n,{}))
        if len(s)==1:
            a=f.var(s[0]); v0=bool_eval(n,{s[0]:0}); v1=bool_eval(n,{s[0]:1})
            stats.cut_retabulations += 1
            if v0==v1: return f.const(v0)
            return a if (v0,v1)==(0,1) else f.not_(a)
        a=f.var(s[0]); b=f.var(s[1]); tok=0
        for x in (0,1):
            for y in (0,1): tok |= bool_eval(n,{s[0]:x,s[1]:y})<<(2*x+y)
        stats.cut_retabulations += 1
        return f.tf(tok,a,b)
    def rec(n:Node):
        if n.nid in memo:
            stats.cse_hits += 1; return memo[n.nid]
        if n.op=='var': out=clone_var(n)
        elif n.op=='const': out=f.const(n.value)
        elif n.op=='not':
            c=rec(n.args[0])
            if c.op=='tf' and not (sharing_guard and source_refs[n.args[0].nid]>1): out=f.tf(c.value^15,c.args[0],c.args[1]); stats.successful_folds+=1; stats.same_operand_folds+=1
            else: out=f.not_(c)
        elif n.op in ('and','or','xor'):
            l=rec(n.args[0]); r=rec(n.args[1]); parent_tok={'and':TOK_AND,'or':TOK_OR,'xor':TOK_XOR}[n.op]
            folded=None
            # Candidate base pairs from any TF child. Try exact then swapped orientation.
            candidates=[]
            if l.op=='tf': candidates.append(l.args)
            if r.op=='tf': candidates.append(r.args)
            for a,b in candidates:
                if sharing_guard and (source_refs[n.args[0].nid]>1 or source_refs[n.args[1].nid]>1):
                    continue
                tl=base_token_for(l,a,b); tr=base_token_for(r,a,b)
                if tl is not None and tr is not None:
                    folded=f.tf(token_apply(n.op,tl,tr),a,b)
                    stats.successful_folds+=1; stats.same_operand_folds+=1
                    # count an alignment if either TF had to be viewed swapped
                    if (l.op=='tf' and l.args==(b,a)) or (r.op=='tf' and r.args==(b,a)):
                        stats.transpose_alignments+=1
                    break
            out=folded if folded is not None else f.tf(parent_tok,l,r)
        elif n.op in ('andn','orn'):
            # Should not appear in source; preserve if it does.
            out=f.nary(n.op,[rec(a) for a in n.args])
        elif n.op=='tf':
            out=f.tf(n.value,rec(n.args[0]),rec(n.args[1]))
        else: raise ValueError(n.op)
        if mode=='generic' and out.op not in ('const','var'):
            before=out; out=generic_retab(out)
            if out is not before: stats.successful_folds += 1
        memo[n.nid]=out; return out
    preliminary=rec(root)
    normalized, cstats=cse_flatten(preliminary)
    stats.cse_hits += cstats.cse_hits
    stats.associative_flattened_nodes += cstats.associative_flattened_nodes
    stats.commutative_reorders += cstats.commutative_reorders
    stats.output_unique_nodes=reachable_nodes(normalized)
    return normalized,stats

def structural_key(n:Node,memo=None):
    if memo is None: memo={}
    if n.nid in memo: return memo[n.nid]
    if n.op in ('var','const'): k=(n.op,n.value)
    elif n.op=='tf': k=('tf',n.value,structural_key(n.args[0],memo),structural_key(n.args[1],memo))
    else: k=(n.op,tuple(structural_key(a,memo) for a in n.args))
    memo[n.nid]=k; return k

def cse_flatten(root:Node):
    f=Factory(); stats=OptStats(); memo={}; keymemo={}
    def rec(n):
        if n.nid in memo: stats.cse_hits+=1; return memo[n.nid]
        if n.op=='var': out=f.var(n.value)
        elif n.op=='const': out=f.const(n.value)
        elif n.op=='not': out=f.not_(rec(n.args[0]))
        elif n.op in ('and','or'):
            opn=n.op+'n'; flat=[]
            def collect(x):
                y=rec(x)
                if y.op==opn:
                    stats.associative_flattened_nodes += 1; flat.extend(y.args)
                elif y.op==n.op:
                    stats.associative_flattened_nodes += 1; collect(y.args[0]); collect(y.args[1])
                else: flat.append(y)
            collect(n.args[0]); collect(n.args[1])
            # sort by structural key for canonical commutative CSE; remove exact duplicate ids
            before=[a.nid for a in flat]; flat.sort(key=lambda a:repr(structural_key(a,keymemo)))
            if [a.nid for a in flat]!=before: stats.commutative_reorders += 1
            uniq=[]; seen=set()
            for a in flat:
                if a.nid not in seen: uniq.append(a); seen.add(a.nid)
            out=f.nary(opn,uniq)
        elif n.op=='xor':
            a,b=rec(n.args[0]),rec(n.args[1]);
            if repr(structural_key(a,keymemo)) > repr(structural_key(b,keymemo)):
                a,b=b,a; stats.commutative_reorders+=1
            out=f.bin('xor',a,b)
        elif n.op=='tf': out=f.tf(n.value,rec(n.args[0]),rec(n.args[1]))
        elif n.op in ('andn','orn'):
            children=[]
            for a in n.args:
                z=rec(a)
                if z.op==n.op: stats.associative_flattened_nodes+=1; children.extend(z.args)
                else: children.append(z)
            before=[a.nid for a in children]; children.sort(key=lambda a:repr(structural_key(a,keymemo)))
            if [a.nid for a in children]!=before: stats.commutative_reorders+=1
            uniq=[]; seen=set()
            for a in children:
                if a.nid not in seen: uniq.append(a); seen.add(a.nid)
            out=f.nary(n.op,uniq)
        else: raise ValueError(n.op)
        memo[n.nid]=out; return out
    out=rec(root); stats.output_unique_nodes=reachable_nodes(out); return out,stats

@dataclass
class AnfStats:
    multiplications:int=0
    pair_terms:int=0
    peak_monomials:int=0
    peak_degree:int=0
    anf_nodes_evaluated:int=0
    cache_hits:int=0
    peak_cache_entries:int=0


def xor_poly(a:set[int],b:set[int]): return a.symmetric_difference(b)

def mul_poly(a:set[int],b:set[int],st:AnfStats):
    st.multiplications += 1; st.pair_terms += len(a)*len(b)
    out=set()
    for x in a:
        for y in b:
            m=x|y
            if m in out: out.remove(m)
            else: out.add(m)
    update_peak(out,st); return out

def update_peak(p:set[int],st:AnfStats):
    st.peak_monomials=max(st.peak_monomials,len(p))
    if p: st.peak_degree=max(st.peak_degree,max(m.bit_count() for m in p))

def lower_anf(root:Node):
    st=AnfStats(); memo={}
    def rec(n):
        if n.nid in memo: st.cache_hits+=1; return memo[n.nid]
        st.anf_nodes_evaluated+=1
        if n.op=='const': p={0} if n.value else set()
        elif n.op=='var': p={1<<n.value}
        elif n.op=='not': p=rec(n.args[0]).copy(); (p.remove(0) if 0 in p else p.add(0)); update_peak(p,st)
        elif n.op=='xor': p=xor_poly(rec(n.args[0]),rec(n.args[1])); update_peak(p,st)
        elif n.op=='and': p=mul_poly(rec(n.args[0]),rec(n.args[1]),st)
        elif n.op=='or':
            a=rec(n.args[0]); b=rec(n.args[1]); p=xor_poly(xor_poly(a,b),mul_poly(a,b,st)); update_peak(p,st)
        elif n.op=='andn':
            level=[rec(c).copy() for c in n.args]
            if not level: p={0}
            else:
                while len(level)>1:
                    nxt=[]
                    for i in range(0,len(level),2):
                        nxt.append(level[i] if i+1==len(level) else mul_poly(level[i],level[i+1],st))
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
                            a,b=level[i],level[i+1]; q=xor_poly(xor_poly(a,b),mul_poly(a,b,st)); update_peak(q,st); nxt.append(q)
                    level=nxt
                p=level[0]
        elif n.op=='tf':
            a=rec(n.args[0]); b=rec(n.args[1]); t=n.value
            v00=(t>>0)&1; v01=(t>>1)&1; v10=(t>>2)&1; v11=(t>>3)&1
            ca=v00; cb=v10^v00; cc=v01^v00; cd=v11^v10^v01^v00
            p={0} if ca else set()
            if cb: p=xor_poly(p,a)
            if cc: p=xor_poly(p,b)
            if cd: p=xor_poly(p,mul_poly(a,b,st))
            update_peak(p,st)
        else: raise ValueError(n.op)
        memo[n.nid]=p; st.peak_cache_entries=max(st.peak_cache_entries,len(memo)); update_peak(p,st); return p
    p=rec(root); return p,st

def anf_to_bitset(poly:set[int],nvars:int,env=None):
    env=bitset_env(nvars) if env is None else env; mask=(1<<(1<<nvars))-1; out=0
    for mon in poly:
        v=mask
        for i in range(nvars):
            if (mon>>i)&1: v &= env[i]
        out ^= v
    return out

def poly_digest(poly:set[int]):
    h=hashlib.sha256()
    for m in sorted(poly): h.update(m.to_bytes(8,'little',signed=False))
    return h.hexdigest()

def poly_serialized_bytes(poly:set[int]):
    return len(poly)*8


def prepare_arm(root:Node, arm:str):
    if arm=='direct_sparse_anf': return root,OptStats(output_unique_nodes=reachable_nodes(root))
    if arm=='cse_flat_sparse': return cse_flatten(root)
    if arm=='generic_2support_sparse': return fold_frontend(root,'generic')
    if arm=='cm_frontend_sparse': return fold_frontend(root,'cm')
    if arm=='cm_frontend_guarded_sparse': return fold_frontend(root,'cm',sharing_guard=True)
    raise ValueError(arm)

def run_arm(root:Node, arm:str, oracle:int, nvars:int, memory=False):
    if memory: tracemalloc.start()
    t0=time.perf_counter_ns(); optimized,ost=prepare_arm(root,arm); t1=time.perf_counter_ns()
    poly,ast=lower_anf(optimized); t2=time.perf_counter_ns()
    peak_py=None
    if memory:
        _,peak_py=tracemalloc.get_traced_memory(); tracemalloc.stop()
    got=anf_to_bitset(poly,nvars); ok=(got==oracle)
    return {
        'arm':arm,'ok':ok,'optimize_ns':t1-t0,'propagate_ns':t2-t1,'frontend_anf_ns':t2-t0,
        'python_peak_bytes':peak_py,'final_monomials':len(poly),
        'final_degree':max((m.bit_count() for m in poly),default=0),'serialized_bytes':poly_serialized_bytes(poly),
        'digest':poly_digest(poly),**dataclasses.asdict(ost),**dataclasses.asdict(ast)
    }, optimized


def git_blob_hash(path:Path):
    data=path.read_bytes(); return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

def case_documents(path:Path):
    blif=parse_blif(path); f=Factory(); docs=[]
    for out in blif.outputs:
        sup=structural_support(blif,out)
        if NATURAL_SUPPORT_MIN <= len(sup) <= NATURAL_SUPPORT_MAX:
            root=build_expr(blif,out,f); oracle=eval_blif_bitset(blif,out)
            docs.append({'case_id':f'int2float:{out}','output':out,'support':len(sup),'root':root,'oracle':oracle,'source_nodes':reachable_nodes(root)})
    return blif,docs

def natural_symbolic(path:Path):
    blif,cases=case_documents(path); rows=[]
    for case in cases:
        for arm in ARMS:
            row,_=run_arm(case['root'],arm,case['oracle'],len(blif.inputs),memory=True)
            row.update({k:v for k,v in case.items() if k not in ('root','oracle')}); rows.append(row)
    return blif,cases,rows

def natural_cold_timings(path:Path,reps=COLD_REPS):
    rng=random.Random(SEED^0xC01D); rows=[]
    schedule=[a for _ in range(reps) for a in ARMS]; rng.shuffle(schedule)
    for ri,arm in enumerate(schedule):
        t0=time.perf_counter_ns(); blif=parse_blif(path); f=Factory(); dig=[]; ok=True; per=[]
        for out in blif.outputs:
            sup=structural_support(blif,out)
            if not (NATURAL_SUPPORT_MIN <= len(sup) <= NATURAL_SUPPORT_MAX): continue
            root=build_expr(blif,out,f); oracle=eval_blif_bitset(blif,out)
            r,_=run_arm(root,arm,oracle,len(blif.inputs),memory=False); dig.append(r['digest']); ok &= r['ok']; per.append(r)
        total=time.perf_counter_ns()-t0
        rows.append({'rep':ri,'arm':arm,'file_to_all_anf_ns':total,'ok':ok,'digests':dig,
                     'sum_optimize_ns':sum(x['optimize_ns'] for x in per),'sum_propagate_ns':sum(x['propagate_ns'] for x in per)})
    return rows

def natural_warm_timings(path:Path,reuses=WARM_REUSES):
    # Compile optimizer + ANF once. Reuse measures execution of the prepared ANF truth-vector
    # artifact, matching a compile-once/evaluate-many contract rather than rebuilding ANF.
    blif,cases=case_documents(path); rows=[]; exec_env=bitset_env(len(blif.inputs))
    for arm in ARMS:
        prepared=[]
        for c in cases:
            opt,_ost=prepare_arm(c['root'],arm); poly,_ast=lower_anf(opt); prepared.append((c,poly))
        for reuse in reuses:
            for rep in range(5):
                t0=time.perf_counter_ns(); ok=True; checksum=0
                for _ in range(reuse):
                    for c,poly in prepared:
                        got=anf_to_bitset(poly,len(blif.inputs),exec_env); checksum ^= got & ((1<<64)-1); ok &= (got==c['oracle'])
                elapsed=time.perf_counter_ns()-t0
                rows.append({'arm':arm,'reuse':reuse,'rep':rep,'batch_ns':elapsed,
                             'per_output_execution_ns':elapsed/(reuse*max(1,len(prepared))),'ok':ok,
                             'checksum64':checksum})
    return rows

# --- Fuzz correctness ---
def random_expr(rng:random.Random,nvars:int,depth:int,f:Factory):
    if depth<=0 or rng.random()<0.18: return f.var(rng.randrange(nvars)) if rng.random()<0.9 else f.const(rng.randrange(2))
    op=rng.choice(('and','or','xor','not'))
    if op=='not': return f.not_(random_expr(rng,nvars,depth-1,f))
    # deliberately create same-pair fold opportunities some of the time
    if rng.random()<0.25 and depth>=2:
        a=random_expr(rng,nvars,depth-2,f); b=random_expr(rng,nvars,depth-2,f)
        u=f.bin(rng.choice(('and','or','xor')),a,b); v=f.bin(rng.choice(('and','or','xor')),a,b)
        return f.bin(op,u,v)
    return f.bin(op,random_expr(rng,nvars,depth-1,f),random_expr(rng,nvars,depth-1,f))

def eval_node_bitset(root:Node,nvars:int):
    env=bitset_env(nvars); mask=(1<<(1<<nvars))-1; memo={}
    def rec(n):
        if n.nid in memo: return memo[n.nid]
        if n.op=='const': v=mask if n.value else 0
        elif n.op=='var': v=env[n.value]
        elif n.op=='not': v=(~rec(n.args[0]))&mask
        elif n.op=='and': v=rec(n.args[0])&rec(n.args[1])
        elif n.op=='or': v=rec(n.args[0])|rec(n.args[1])
        elif n.op=='xor': v=rec(n.args[0])^rec(n.args[1])
        elif n.op=='andn':
            v=mask
            for a in n.args: v &= rec(a)
        elif n.op=='orn':
            v=0
            for a in n.args: v |= rec(a)
        elif n.op=='tf':
            x=rec(n.args[0]); y=rec(n.args[1]); v=0
            for xb in (0,1):
                for yb in (0,1):
                    if (n.value>>(2*xb+yb))&1:
                        v |= (x if xb else (~x)&mask) & (y if yb else (~y)&mask)
        else: raise ValueError(n.op)
        memo[n.nid]=v; return v
    return rec(root)

def fuzz_correctness():
    rng=random.Random(SEED^0xF022); failures=[]; totals=defaultdict(int)
    for i in range(FUZZ_CASES):
        nvars=rng.randint(2,6); f=Factory(); root=random_expr(rng,nvars,rng.randint(2,7),f); oracle=eval_node_bitset(root,nvars)
        for arm in ARMS:
            r,_=run_arm(root,arm,oracle,nvars,memory=False); totals[arm]+=1
            if not r['ok'] or (failures and len(failures)>20):
                if not r['ok']: failures.append({'case':i,'arm':arm,'nvars':nvars})
    return {'cases':FUZZ_CASES,'arm_checks':dict(totals),'failures':failures,'passed':not failures}

# --- Gate-P equal-final-ANF mechanism/speed campaign ---
def make_base_expr(rng,nvars,depth,f):
    return random_expr(rng,nvars,max(1,depth),f)
def gatep_case(rng,depth,idx):
    f=Factory(); nvars=8
    # A/B are moderately complex but shared. The shell repeatedly combines different
    # truth functions of the same ordered operands, which both generic and CM may fold.
    A=make_base_expr(rng,nvars,3,f); B=make_base_expr(rng,nvars,3,f)
    cur=f.bin(rng.choice(('and','or','xor')),A,B)
    other=f.bin(rng.choice(('and','or','xor')),A,B)
    for level in range(depth):
        q=f.bin(rng.choice(('and','or','xor')),A,B)
        left=f.bin(rng.choice(('and','or','xor')),cur,q)
        # occasional swapped orientation stresses transpose/alignment handling
        s=f.bin(rng.choice(('and','or','xor')),B,A) if level%3==1 else other
        cur=f.bin(rng.choice(('and','or','xor')),left,s)
        other=q
    return f,cur,nvars

def gatep_campaign():
    rng=random.Random(SEED^0x6A7E); cases=[]
    for d in GATEP_DEPTHS:
        for i in range(GATEP_CASES_PER_DEPTH):
            f,r,n=gatep_case(rng,d,i); oracle=eval_node_bitset(r,n); cases.append((d,i,r,n,oracle))
    symbolic=[]; timing=[]
    for d,i,root,n,oracle in cases:
        base=None
        for arm in ARMS:
            r,_=run_arm(root,arm,oracle,n,memory=True); r.update({'depth':d,'case':i}); symbolic.append(r)
            if base is None: base=r['digest']
            if r['digest']!=base: raise AssertionError('Gate-P ANF digest mismatch')
        # Paired randomized timing only for generic vs CM: equal output is required above.
        schedule=[a for _ in range(GATEP_TIMING_REPS) for a in ('generic_2support_sparse','cm_frontend_sparse')]
        local_rng=random.Random(SEED+d*1000+i); local_rng.shuffle(schedule)
        for rep,arm in enumerate(schedule):
            t0=time.perf_counter_ns(); rr,_=run_arm(root,arm,oracle,n,memory=False); elapsed=time.perf_counter_ns()-t0
            timing.append({'depth':d,'case':i,'rep':rep,'arm':arm,'elapsed_ns':elapsed,'ok':rr['ok'],
                           'optimize_ns':rr['optimize_ns'],'propagate_ns':rr['propagate_ns']})
    return symbolic,timing

# --- Analysis helpers ---
def median(xs): return statistics.median(xs) if xs else None
def geomean(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def quantile(xs,p):
    s=sorted(xs)
    if not s: return None
    pos=(len(s)-1)*p; lo=int(pos); hi=min(lo+1,len(s)-1); frac=pos-lo
    return s[lo]*(1-frac)+s[hi]*frac

def bootstrap_ratio_of_medians(a,b,n=5000,seed=SEED):
    if not a or not b: return {'ratio':None,'ci95':[None,None]}
    rng=random.Random(seed); vals=[]
    for _ in range(n):
        aa=[rng.choice(a) for _ in a]; bb=[rng.choice(b) for _ in b]
        den=statistics.median(bb)
        if den>0: vals.append(statistics.median(aa)/den)
    return {'ratio':statistics.median(a)/statistics.median(b),'ci95':[quantile(vals,.025),quantile(vals,.975)],'bootstrap_n':n}

def bootstrap_geomean_ratio(ratios,n=5000,seed=SEED):
    ratios=[x for x in ratios if x and x>0]
    if not ratios: return {'ratio':None,'ci95':[None,None]}
    rng=random.Random(seed); vals=[]
    for _ in range(n): vals.append(geomean([rng.choice(ratios) for _ in ratios]))
    return {'ratio':geomean(ratios),'ci95':[quantile(vals,.025),quantile(vals,.975)],'bootstrap_n':n}

def paired_case_ratio(rows,metric,num_arm,den_arm,keys=('case_id',)):
    by=defaultdict(dict)
    for r in rows: by[tuple(r.get(k) for k in keys)][r['arm']]=r
    vals=[]
    for k,d in by.items():
        if num_arm in d and den_arm in d and d[den_arm][metric]: vals.append(d[num_arm][metric]/d[den_arm][metric])
    return vals

def summarize(natural_rows,cold_rows,warm_rows,fuzz,gatep_sym,gatep_time):
    byarm=defaultdict(list)
    for r in natural_rows: byarm[r['arm']].append(r)
    nat={}
    for a,rs in byarm.items():
        nat[a]={m:median([r[m] for r in rs]) for m in ('multiplications','pair_terms','peak_monomials','final_monomials','output_unique_nodes','python_peak_bytes','same_operand_folds','cut_retabulations')}
        nat[a]['all_ok']=all(r['ok'] for r in rs); nat[a]['cases']=len(rs)
    # paired CM/generic ratios on natural symbolic metrics (lower is better)
    cmgen={}
    for m in ('multiplications','pair_terms','peak_monomials','output_unique_nodes','python_peak_bytes'):
        ratios=paired_case_ratio(natural_rows,m,'cm_frontend_sparse','generic_2support_sparse')
        cmgen[m]={'median_ratio':median(ratios),'geomean_ratio':geomean(ratios),'n':len(ratios)}
    cold={}
    for a in ARMS:
        xs=[r['file_to_all_anf_ns'] for r in cold_rows if r['arm']==a]; cold[a]={'median_ns':median(xs),'n':len(xs),'all_ok':all(r['ok'] for r in cold_rows if r['arm']==a)}
    cold_components={}
    for a in ARMS:
        rs=[r for r in cold_rows if r['arm']==a]
        cold_components[a]={'median_optimize_ns':median([r['sum_optimize_ns'] for r in rs]),
                            'median_propagate_ns':median([r['sum_propagate_ns'] for r in rs])}
    cold_cm=[r['file_to_all_anf_ns'] for r in cold_rows if r['arm']=='cm_frontend_sparse']
    cold_gen=[r['file_to_all_anf_ns'] for r in cold_rows if r['arm']=='generic_2support_sparse']
    cold_direct=[r['file_to_all_anf_ns'] for r in cold_rows if r['arm']=='direct_sparse_anf']
    cold_compare={'cm_over_generic':bootstrap_ratio_of_medians(cold_cm,cold_gen,seed=SEED^0xC01D),
                  'cm_over_direct':bootstrap_ratio_of_medians(cold_cm,cold_direct,seed=SEED^0xD1EC7)}
    warm={}
    for reuse in WARM_REUSES:
        warm[str(reuse)]={}
        for a in ARMS:
            xs=[r['per_output_execution_ns'] for r in warm_rows if r['arm']==a and r['reuse']==reuse]
            warm[str(reuse)][a]=median(xs)
    # Gate-P aggregate paired per-case timing medians.
    gp_cases=defaultdict(lambda:defaultdict(list))
    for r in gatep_time: gp_cases[(r['depth'],r['case'])][r['arm']].append(r['elapsed_ns'])
    gp_rat=[]; gp_bydepth=defaultdict(list)
    for k,d in gp_cases.items():
        if d['generic_2support_sparse'] and d['cm_frontend_sparse']:
            ratio=median(d['cm_frontend_sparse'])/median(d['generic_2support_sparse']); gp_rat.append(ratio); gp_bydepth[k[0]].append(ratio)
    gatep={'cm_over_generic_median_ratio':median(gp_rat),'cm_over_generic_geomean_ratio':geomean(gp_rat),'cases':len(gp_rat),
           'by_depth':{str(d):{'median_ratio':median(v),'geomean_ratio':geomean(v),'n':len(v)} for d,v in gp_bydepth.items()}}
    gatep['cm_over_generic_geomean_bootstrap']=bootstrap_geomean_ratio(gp_rat,seed=SEED^0x6A7E)
    # Gate-P equal-symbolic counters between generic/CM.
    diffs=defaultdict(int); pairs=defaultdict(dict)
    for r in gatep_sym: pairs[(r['depth'],r['case'])][r['arm']]=r
    for d in pairs.values():
        g=d['generic_2support_sparse']; c=d['cm_frontend_sparse']
        for m in ('multiplications','pair_terms','peak_monomials','final_monomials','output_unique_nodes'):
            if g[m]!=c[m]: diffs[m]+=1
    gatep['generic_cm_symbolic_difference_rows']=dict(diffs)
    # Preregistered N1 natural success: CM >=5% better than generic in BOTH paired symbolic work and intermediate size.
    # Here use pair_terms (work) and peak_monomials (intermediate/backend pressure). Zero denominator handled as no evidence.
    pr=cmgen['pair_terms']['geomean_ratio']; pm=cmgen['peak_monomials']['geomean_ratio']
    n1_positive=bool(pr is not None and pm is not None and pr <= 1-N1_CM_ADVANTAGE_THRESHOLD and pm <= 1-N1_CM_ADVANTAGE_THRESHOLD and all(r['ok'] for r in natural_rows))
    gatep_positive=bool(gatep['cm_over_generic_geomean_ratio'] is not None and gatep['cm_over_generic_geomean_ratio'] <= 1-GATEP_TIMING_THRESHOLD)
    return {'natural':nat,'natural_cm_over_generic':cmgen,'natural_cold':cold,'natural_cold_components':cold_components,'natural_cold_comparisons':cold_compare,'natural_warm':warm,'fuzz':fuzz,'gatep':gatep,
            'pre_registered_outcomes':{'n1_cm_specific_advantage':n1_positive,'gatep_exploratory_speed_signal':gatep_positive}}

def fmt_ns(x):
    if x is None:return 'n/a'
    if x<1e3:return f'{x:.0f} ns'
    if x<1e6:return f'{x/1e3:.2f} us'
    if x<1e9:return f'{x/1e6:.2f} ms'
    return f'{x/1e9:.2f} s'

def make_report(meta,summary,natural_rows):
    ncases=len({r['case_id'] for r in natural_rows}); nat=summary['natural']; cg=summary['natural_cm_over_generic']; gate=summary['gatep']
    lines=[]
    lines += ['# N1 Natural Replay + Gate-P Speed Campaign','',f"Run date: {meta['run_date']}",
              f"Frozen natural source: `{meta['source_name']}` (Git blob `{meta['source_git_blob']}`)",
              f"Natural cases admitted: **{ncases}** outputs with structural support {NATURAL_SUPPORT_MIN}-{NATURAL_SUPPORT_MAX}.",'']
    lines += ['## Pre-registered protocol','',
              f'- Arms: {", ".join(f"`{a}`" for a in ARMS)}.',
              '- Correctness gate: every arm must reproduce an independent BLIF packed truth-table oracle.',
              f'- N1 CM-specific positive criterion: at least {N1_CM_ADVANTAGE_THRESHOLD*100:.0f}% paired improvement over `generic_2support_sparse` in both pair-term work and peak intermediate monomials on this untouched natural stratum, with zero mismatches.',
              f'- Cold timing: {COLD_REPS} randomized file-to-all-output repetitions per arm; timing includes BLIF parse, formula construction, optimization, and sparse-ANF propagation.',
              f'- Warm timing: optimizer + sparse ANF are prepared once; the prepared ANF truth-vector execution is repeated for {WARM_REUSES}.',
              f'- Gate-P: {GATEP_CASES_PER_DEPTH} cases at each depth {GATEP_DEPTHS}; generic and CM produce the same ANF before timing; {GATEP_TIMING_REPS} randomized repetitions per arm/case.',
              '- Python allocation peaks use `tracemalloc`; they are not process RSS. Timings are local single-process diagnostics, not cross-machine headline benchmarks.','']
    lines += ['## N1 natural symbolic results','', '| arm | mult median | pair-terms median | peak monomials | final monomials | IR nodes | Python peak | folds | cut retabs |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for a in ARMS:
        x=nat[a]; lines.append(f"| `{a}` | {x['multiplications']:.1f} | {x['pair_terms']:.1f} | {x['peak_monomials']:.1f} | {x['final_monomials']:.1f} | {x['output_unique_nodes']:.1f} | {x['python_peak_bytes']/1024:.1f} KiB | {x['same_operand_folds']:.1f} | {x['cut_retabulations']:.1f} |")
    lines += ['', 'CM / generic paired ratios (lower is better):']
    for m in ('multiplications','pair_terms','peak_monomials','output_unique_nodes','python_peak_bytes'):
        x=cg[m]; lines.append(f"- {m}: geometric mean ratio `{x['geomean_ratio']:.4f}` across {x['n']} comparable outputs" if x['geomean_ratio'] is not None else f'- {m}: n/a')
    lines += ['',f"**Pre-registered N1 outcome: {'PASS (CM-specific natural advantage)' if summary['pre_registered_outcomes']['n1_cm_specific_advantage'] else 'NO PASS / no CM-specific natural advantage under this criterion'}.**",'']
    lines += ['## Cold end-to-end timing','', '| arm | median file -> all ANFs | reps |', '|---|---:|---:|']
    for a in ARMS:
        x=summary['natural_cold'][a]; lines.append(f"| `{a}` | {fmt_ns(x['median_ns'])} | {x['n']} |")
    cc=summary['natural_cold_comparisons']; comp=summary['natural_cold_components']
    lines += ['', f"- CM/generic cold ratio: **{cc['cm_over_generic']['ratio']:.4f}**, exploratory bootstrap 95% CI [{cc['cm_over_generic']['ci95'][0]:.4f}, {cc['cm_over_generic']['ci95'][1]:.4f}].",
              f"- CM/direct cold ratio: **{cc['cm_over_direct']['ratio']:.4f}**, exploratory bootstrap 95% CI [{cc['cm_over_direct']['ci95'][0]:.4f}, {cc['cm_over_direct']['ci95'][1]:.4f}].",
              f"- Median summed optimizer time across the seven outputs: generic {fmt_ns(comp['generic_2support_sparse']['median_optimize_ns'])}, CM {fmt_ns(comp['cm_frontend_sparse']['median_optimize_ns'])}; median summed ANF propagation: generic {fmt_ns(comp['generic_2support_sparse']['median_propagate_ns'])}, CM {fmt_ns(comp['cm_frontend_sparse']['median_propagate_ns'])}."]
    lines += ['', '## Warm optimizer-reuse timing', '', 'Median time per output execution after optimizer + sparse ANF are prepared:', '', '| reuse | direct | CSE-flat | generic 2-support | CM frontend |','|---:|---:|---:|---:|---:|']
    for r in WARM_REUSES:
        w=summary['natural_warm'][str(r)]; lines.append(f"| {r} | {fmt_ns(w['direct_sparse_anf'])} | {fmt_ns(w['cse_flat_sparse'])} | {fmt_ns(w['generic_2support_sparse'])} | {fmt_ns(w['cm_frontend_sparse'])} |")
    lines += ['', '## Gate-P equal-result speed test','',
              f"- CM/generic geometric-mean paired time ratio: **{gate['cm_over_generic_geomean_ratio']:.4f}** (lower favors CM) across {gate['cases']} cases.",
              f"- Paired-case bootstrap 95% CI for that geometric-mean ratio: **[{gate['cm_over_generic_geomean_bootstrap']['ci95'][0]:.4f}, {gate['cm_over_generic_geomean_bootstrap']['ci95'][1]:.4f}]**.",
              f"- CM/generic symbolic-difference counts: `{json.dumps(gate['generic_cm_symbolic_difference_rows'],sort_keys=True)}`.",
              f"- Exploratory >= {GATEP_TIMING_THRESHOLD*100:.0f}% CM speed signal: **{'YES' if summary['pre_registered_outcomes']['gatep_exploratory_speed_signal'] else 'NO'}**.",'']
    lines += ['## Correctness / falsification checks','',
              f"- Natural rows: {len(natural_rows)}; mismatches: {sum(not r['ok'] for r in natural_rows)}.",
              f"- Random exhaustive fuzz: {summary['fuzz']['cases']} formulas x {len(ARMS)} arms = {sum(summary['fuzz']['arm_checks'].values())} checks; failures: {len(summary['fuzz']['failures'])}.",'']
    lines += ['## Interpretation','',
              'This run distinguishes **pre-expansion reduction** from **CM-specific advantage**. A pre-expansion win over direct ANF would still be useful even when the generic two-support reducer obtains the same reduction; this particular natural pilot did not show such a win for the CM frontend. The CM-specific question is whether the CM frontend beats that strongest artifact-equivalent generic reducer on untouched natural formulas.',
              '', 'This is a **natural-stratum pilot**, not the complete EPFL campaign: it freezes every eligible output of one pinned public `int2float` netlist rather than selecting favorable outputs. Broader cross-circuit validation remains the next step if the result is worth pursuing.']
    return '\n'.join(lines)+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--blif',type=Path,default=Path('/mnt/data/int2float_depth_2025.blif')); ap.add_argument('--out',type=Path,default=Path('/mnt/data/cm_n1_gatep')); args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    blob=git_blob_hash(args.blif)
    if blob!=EXPECTED_EPFL_GIT_BLOB: raise SystemExit(f'Frozen BLIF hash mismatch: {blob}')
    started=time.time(); blif,cases,natural_rows=natural_symbolic(args.blif)
    if not cases: raise SystemExit('No natural cases admitted')
    if any(not r['ok'] for r in natural_rows): raise SystemExit('Natural correctness failure')
    fuzz=fuzz_correctness()
    if not fuzz['passed']: raise SystemExit(f"Fuzz correctness failure: {fuzz['failures'][:3]}")
    cold=natural_cold_timings(args.blif)
    warm=natural_warm_timings(args.blif)
    gps,gpt=gatep_campaign()
    summary=summarize(natural_rows,cold,warm,fuzz,gps,gpt)
    meta={'schema':'cm-n1-gatep-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_s':time.time()-started,
          'source_name':args.blif.name,'source_git_blob':blob,'epfl_commit':'0060e156826e733d69bf5b3322d1bdd0d03a1f9a',
          'seed':SEED,'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
          'protocol':{'arms':ARMS,'natural_support':[NATURAL_SUPPORT_MIN,NATURAL_SUPPORT_MAX],'cold_reps':COLD_REPS,'warm_reuses':WARM_REUSES,
                      'gatep_depths':GATEP_DEPTHS,'gatep_cases_per_depth':GATEP_CASES_PER_DEPTH,'gatep_timing_reps':GATEP_TIMING_REPS,'fuzz_cases':FUZZ_CASES,
                      'n1_cm_advantage_threshold':N1_CM_ADVANTAGE_THRESHOLD,'gatep_timing_threshold':GATEP_TIMING_THRESHOLD},
          'natural_cases':[{k:v for k,v in c.items() if k not in ('root','oracle')} for c in cases]}
    payload={'meta':meta,'summary':summary,'natural_symbolic_rows':natural_rows,'natural_cold_rows':cold,'natural_warm_rows':warm,'fuzz':fuzz,'gatep_symbolic_rows':gps,'gatep_timing_rows':gpt}
    (args.out/'n1_gatep_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (args.out/'N1_GATEP_RESULTS.md').write_text(make_report(meta,summary,natural_rows),encoding='utf-8')
    readme=f"""# N1 / Gate-P reproduction\n\nRun:\n\n```bash\npython n1_gatep_harness.py --blif int2float_depth_2025.blif --out .\n```\n\nThe harness refuses to run unless the BLIF Git blob hash is `{EXPECTED_EPFL_GIT_BLOB}`.\nSee `N1_GATEP_RESULTS.md` and `n1_gatep_results.json`.\n"""
    (args.out/'README.md').write_text(readme,encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
