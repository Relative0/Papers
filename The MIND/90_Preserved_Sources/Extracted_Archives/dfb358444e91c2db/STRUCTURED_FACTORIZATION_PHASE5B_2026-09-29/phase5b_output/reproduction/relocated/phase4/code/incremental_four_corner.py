#!/usr/bin/env python3
"""Incremental-control four-corner CM defect encoding.

Builds ONE base CNF for a semantic CNF and a fixed carrier-block partition.
Cut membership is represented by one selector per carrier block.  Each query is
therefore only an assumption vector on the selectors.  With an industrial
assumption-capable CDCL solver, learned clauses can be retained across queries.

The bundled fallback backend reuses the base encoding but restarts the small
pure-Python DPLL search; it is for correctness/reproducibility, not performance.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Sequence, Set, Tuple, Optional
import importlib.util, json, os, random, time

_BASE=os.path.join(os.path.dirname(__file__),'four_corner_sat_phase3_baseline.py')
spec=importlib.util.spec_from_file_location('fcbase',_BASE)
fc=importlib.util.module_from_spec(spec)
import sys
sys.modules['fcbase']=fc
spec.loader.exec_module(fc)
Clause=Tuple[int,...]
CNF=List[Clause]

class VarPool:
    def __init__(self): self.n=0; self.names={}
    def new(self,name:str)->int:
        self.n+=1; self.names[self.n]=name; return self.n

def add_or_equiv(out:int,lits:Sequence[int],cnf:CNF):
    if not lits: cnf.append((-out,)); return
    cnf.append(tuple([-out]+list(lits)))
    for lit in lits: cnf.append((-lit,out))

def add_and_equiv(out:int,ins:Sequence[int],cnf:CNF):
    if not ins: cnf.append((out,)); return
    for x in ins: cnf.append((-out,x))
    cnf.append(tuple([out]+[-x for x in ins]))

def add_ite_equiv(out:int, sel:int, when_true:int, when_false:int, cnf:CNF):
    """out <-> (sel ? when_true : when_false)."""
    # sel -> (out <-> when_true)
    cnf.append((-sel,-out, when_true))
    cnf.append((-sel, out,-when_true))
    # !sel -> (out <-> when_false)
    cnf.append(( sel,-out, when_false))
    cnf.append(( sel, out,-when_false))

@dataclass
class ControlledEncoding:
    n_original:int
    formula:CNF
    blocks:Tuple[Tuple[int,...],...]
    block_of:Dict[int,int]
    selectors:Dict[int,int]
    clone:Dict[Tuple[int,int],int]
    mux01:Dict[int,int]
    mux10:Dict[int,int]
    corner_output:Dict[Tuple[int,int],int]
    nvars:int
    clauses:CNF
    pool_names:Dict[int,str]
    p_var:int
    q_var:int

    def assumptions(self,A_block_indices:Iterable[int])->Dict[int,bool]:
        A=set(A_block_indices)
        if not A or len(A)==len(self.blocks):
            raise ValueError('cut must be nontrivial')
        return {self.selectors[b]:(b in A) for b in range(len(self.blocks))}

    def cut_A_variables(self,A_block_indices:Iterable[int])->Set[int]:
        A=set(A_block_indices)
        return {v for b in A for v in self.blocks[b]}


def _validate_blocks(n:int, blocks:Sequence[Sequence[int]]):
    flat=[v for b in blocks for v in b]
    if sorted(flat)!=list(range(1,n+1)) or len(flat)!=len(set(flat)):
        raise ValueError('blocks must partition variables 1..n exactly')
    if not blocks: raise ValueError('at least one block required')


def build_controlled_encoding(n:int, formula:CNF, blocks:Sequence[Sequence[int]])->ControlledEncoding:
    blocks=tuple(tuple(sorted(b)) for b in blocks)
    _validate_blocks(n,blocks)
    block_of={v:i for i,b in enumerate(blocks) for v in b}
    vp=VarPool(); cnf:CNF=[]
    selectors={i:vp.new(f'sel_B{i}') for i in range(len(blocks))}
    clone={(v,k):vp.new(f'x{v}_{k}') for v in range(1,n+1) for k in (0,1)}
    mux01={}; mux10={}
    for v in range(1,n+1):
        s=selectors[block_of[v]]; x0=clone[(v,0)]; x1=clone[(v,1)]
        z01=vp.new(f'x{v}_01'); z10=vp.new(f'x{v}_10')
        add_ite_equiv(z01,s,x0,x1,cnf)
        add_ite_equiv(z10,s,x1,x0,cnf)
        mux01[v]=z01; mux10[v]=z10

    def sig(v:int,i:int,j:int)->int:
        if (i,j)==(0,0): return clone[(v,0)]
        if (i,j)==(1,1): return clone[(v,1)]
        if (i,j)==(0,1): return mux01[v]
        if (i,j)==(1,0): return mux10[v]
        raise AssertionError

    corner={}
    for i,j in product((0,1),repeat=2):
        cg=[]
        for ci,cl in enumerate(formula):
            mapped=[]
            for lit in cl:
                z=sig(abs(lit),i,j)
                mapped.append(z if lit>0 else -z)
            c=vp.new(f'c{ci}_{i}{j}')
            add_or_equiv(c,mapped,cnf); cg.append(c)
        y=vp.new(f'F_{i}{j}')
        add_and_equiv(y,cg,cnf); corner[(i,j)]=y
    p=vp.new('P=F00&F11'); q=vp.new('Q=F01&F10')
    add_and_equiv(p,[corner[(0,0)],corner[(1,1)]],cnf)
    add_and_equiv(q,[corner[(0,1)],corner[(1,0)]],cnf)
    cnf.append((p,q)); cnf.append((-p,-q))
    return ControlledEncoding(n,list(formula),blocks,block_of,selectors,clone,mux01,mux10,corner,vp.n,cnf,vp.names,p,q)


def solve_restart(enc:ControlledEncoding,Aidx:Iterable[int]):
    """Correctness fallback: same base clauses, fresh DPLL search under assumptions."""
    ass=enc.assumptions(Aidx)
    sub=fc.simplify(enc.clauses,ass)
    if sub is None: return None
    return fc.dpll(sub,enc.nvars,ass)


def witness_from_model(enc:ControlledEncoding,Aidx:Iterable[int],model:Dict[int,bool]):
    Ablocks=set(Aidx); A=enc.cut_A_variables(Ablocks); B=set(range(1,enc.n_original+1))-A
    a0={v:model[enc.clone[(v,0)]] for v in A}; a1={v:model[enc.clone[(v,1)]] for v in A}
    b0={v:model[enc.clone[(v,0)]] for v in B}; b1={v:model[enc.clone[(v,1)]] for v in B}
    return a0,a1,b0,b1


def all_block_cuts(blocks:Sequence[Sequence[int]]):
    k=len(blocks)
    if k<2: return
    for mask in range(1<<(k-1)):
        A={0}
        for j in range(1,k):
            if mask & (1<<(j-1)): A.add(j)
        if len(A)==k: continue
        yield A


def factor_blocks_controlled(enc:ControlledEncoding, active:Optional[Sequence[int]]=None, stats=None):
    """Recursive exact factor recovery using one controlled base encoding.

    `active` lists carrier block indices currently being refined.  Blocks outside
    the active set are put on the B side of each queried global cut.
    """
    if active is None: active=list(range(len(enc.blocks)))
    active=list(active)
    if stats is None: stats={'sat_calls':0,'cuts_tested':0}
    if len(active)<=1:
        return [tuple(enc.blocks[active[0]])] if active else [],stats
    first=active[0]; rest=active[1:]
    for mask in range(1<<len(rest)):
        Aidx={first}
        for j,b in enumerate(rest):
            if mask & (1<<j): Aidx.add(b)
        if len(Aidx)==len(active): continue
        stats['cuts_tested']+=1; stats['sat_calls']+=1
        model=solve_restart(enc,Aidx)
        if model is None:
            left=[b for b in active if b in Aidx]
            right=[b for b in active if b not in Aidx]
            lf,stats=factor_blocks_controlled(enc,left,stats)
            rf,stats=factor_blocks_controlled(enc,right,stats)
            return lf+rf,stats
    merged=tuple(sorted(v for b in active for v in enc.blocks[b]))
    return [merged],stats

class PySATSession:
    """Optional true incremental backend; requires python-sat in the runtime."""
    def __init__(self,enc:ControlledEncoding,solver_name:Optional[str]=None):
        try:
            from pysat.solvers import Solver
        except Exception as e:
            raise RuntimeError('python-sat is not installed; use an IPASIR/PySAT environment for learned-clause benchmarking') from e
        self.enc=enc; self.solver=Solver(name=solver_name,bootstrap_with=[list(c) for c in enc.clauses])
    def solve(self,Aidx:Iterable[int]):
        ass=self.enc.assumptions(Aidx)
        lits=[v if val else -v for v,val in ass.items()]
        sat=self.solver.solve(assumptions=lits)
        if not sat: return None
        m=self.solver.get_model(); return {abs(x):x>0 for x in m}
    def close(self): self.solver.delete()


def export_query_bundle(enc:ControlledEncoding,base_dimacs:str,queries_json:str):
    fc.write_dimacs(base_dimacs,enc.nvars,enc.clauses,[
        'incremental four-corner base CNF; set selector literals by assumptions',
        'selectors: '+json.dumps({str(k):v for k,v in enc.selectors.items()})
    ])
    qs=[]
    for A in all_block_cuts(enc.blocks):
        ass=enc.assumptions(A)
        qs.append({'A_blocks':sorted(A),'A_variables':sorted(enc.cut_A_variables(A)),
                   'assumption_literals':[v if val else -v for v,val in ass.items()]})
    with open(queries_json,'w',encoding='utf-8') as f: json.dump({'blocks':enc.blocks,'selectors':enc.selectors,'queries':qs},f,indent=2)

if __name__=='__main__':
    # Small demonstration
    n=4; formula=[(1,-2),(2,3),(-3,4)]; blocks=[(1,2),(3,),(4,)]
    enc=build_controlled_encoding(n,formula,blocks)
    print(json.dumps({'nvars':enc.nvars,'clauses':len(enc.clauses),'selectors':enc.selectors},indent=2))
    for A in all_block_cuts(blocks):
        m=solve_restart(enc,A)
        print(sorted(A),'SAT defect' if m else 'UNSAT defect')
