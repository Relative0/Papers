#!/usr/bin/env python3
"""SAT encoder for the four-corner CM rank-defect test.

Input semantics are CNF over variables 1..n. For a declared cut A|B, the
program constructs a CNF whose satisfiability is equivalent to the existence
of a nonzero 2x2 minor of the implicit correspondence flattening [f]_{A|B}.

No external SAT package is required for small validation: a compact DPLL solver
is included. DIMACS export is provided for use with industrial SAT solvers.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product, combinations
from typing import List, Tuple, Dict, Iterable, Optional, Sequence, Set
import argparse, json, random, time

Clause = Tuple[int, ...]
CNF = List[Clause]


def parse_dimacs(path: str):
    n = 0; clauses=[]
    with open(path, 'r', encoding='utf-8') as f:
        acc=[]
        for line in f:
            line=line.strip()
            if not line or line.startswith('c'): continue
            if line.startswith('p'):
                parts=line.split(); n=int(parts[2]); continue
            for tok in line.split():
                x=int(tok)
                if x==0:
                    clauses.append(tuple(acc)); acc=[]
                else: acc.append(x)
        if acc: clauses.append(tuple(acc))
    return n, clauses


def write_dimacs(path: str, nvars: int, clauses: CNF, comments: Sequence[str]=()):
    with open(path,'w',encoding='utf-8') as f:
        for c in comments: f.write('c '+c+'\n')
        f.write(f'p cnf {nvars} {len(clauses)}\n')
        for cl in clauses: f.write(' '.join(map(str,cl))+' 0\n')


def eval_cnf(clauses: CNF, assignment: Dict[int,bool]) -> bool:
    for cl in clauses:
        ok=False
        for lit in cl:
            val=assignment[abs(lit)]
            if lit<0: val=not val
            if val: ok=True; break
        if not ok: return False
    return True

class VarPool:
    def __init__(self): self.n=0; self.names={}
    def new(self, name):
        self.n += 1; self.names[self.n]=name; return self.n


def add_or_equiv(out:int, lits:Sequence[int], cnf:CNF):
    """out <-> OR(lits)."""
    if not lits:
        cnf.append((-out,))
        return
    cnf.append(tuple([-out] + list(lits)))
    for lit in lits:
        cnf.append((-lit, out))


def add_and_equiv(out:int, ins:Sequence[int], cnf:CNF):
    """out <-> AND(ins)."""
    if not ins:
        cnf.append((out,)); return
    for x in ins: cnf.append((-out, x))
    cnf.append(tuple([out] + [-x for x in ins]))

@dataclass
class DefectEncoding:
    n_original: int
    cut_A: Set[int]
    nvars: int
    clauses: CNF
    pool_names: Dict[int,str]
    input_clone: Dict[Tuple[int,int],int]
    corner_output: Dict[Tuple[int,int],int]
    p_var: int
    q_var: int


def build_defect_encoding(n:int, formula:CNF, cut_A:Iterable[int]) -> DefectEncoding:
    A=set(cut_A); V=set(range(1,n+1)); B=V-A
    if not A or not B: raise ValueError('cut must be nontrivial')
    vp=VarPool(); out_cnf=[]
    # Two assignment copies per original variable. Their interpretation depends on cut side.
    clone={(v,i):vp.new(f'x{v}_{i}') for v in range(1,n+1) for i in (0,1)}
    corner_out={}
    for i,j in product((0,1), repeat=2):
        clause_gates=[]
        for ci,cl in enumerate(formula):
            mapped=[]
            for lit in cl:
                v=abs(lit); bit=i if v in A else j
                z=clone[(v,bit)]
                mapped.append(z if lit>0 else -z)
            s=vp.new(f'c{ci}_{i}{j}')
            add_or_equiv(s,mapped,out_cnf)
            clause_gates.append(s)
        y=vp.new(f'F_{i}{j}')
        add_and_equiv(y,clause_gates,out_cnf)
        corner_out[(i,j)]=y
    p=vp.new('P=F00&F11'); q=vp.new('Q=F01&F10')
    add_and_equiv(p,[corner_out[(0,0)],corner_out[(1,1)]],out_cnf)
    add_and_equiv(q,[corner_out[(0,1)],corner_out[(1,0)]],out_cnf)
    # P XOR Q = 1
    out_cnf.append((p,q)); out_cnf.append((-p,-q))
    return DefectEncoding(n,A,vp.n,out_cnf,vp.names,clone,corner_out,p,q)


def simplify(clauses:CNF, assignment:Dict[int,bool]):
    out=[]
    for cl in clauses:
        new=[]; sat=False
        for lit in cl:
            v=abs(lit)
            if v in assignment:
                val=assignment[v]
                if lit<0: val=not val
                if val: sat=True; break
            else: new.append(lit)
        if sat: continue
        if not new: return None
        out.append(tuple(new))
    return out


def unit_propagate(clauses:CNF, assignment:Dict[int,bool]):
    clauses=list(clauses)
    while True:
        units=[cl[0] for cl in clauses if len(cl)==1]
        if not units: return clauses, assignment
        changed=False
        for lit in units:
            v=abs(lit); val=lit>0
            if v in assignment and assignment[v]!=val: return None, None
            if v not in assignment:
                assignment[v]=val; changed=True
        if not changed: return clauses,assignment
        clauses=simplify(clauses,assignment)
        if clauses is None: return None,None


def dpll(clauses:CNF, nvars:int, assignment=None):
    if assignment is None: assignment={}
    clauses,assignment=unit_propagate(clauses,dict(assignment))
    if clauses is None: return None
    if not clauses:
        for v in range(1,nvars+1): assignment.setdefault(v,False)
        return assignment
    # simple occurrence heuristic
    counts={}
    for cl in clauses:
        for lit in cl: counts[abs(lit)]=counts.get(abs(lit),0)+1
    v=max(counts,key=counts.get)
    for val in (True,False):
        a=dict(assignment); a[v]=val
        sub=simplify(clauses,a)
        if sub is None: continue
        r=dpll(sub,nvars,a)
        if r is not None: return r
    return None


def witness_from_model(enc:DefectEncoding, model:Dict[int,bool]):
    a0={}; a1={}; b0={}; b1={}
    B=set(range(1,enc.n_original+1))-enc.cut_A
    for v in enc.cut_A:
        a0[v]=model[enc.input_clone[(v,0)]]; a1[v]=model[enc.input_clone[(v,1)]]
    for v in B:
        b0[v]=model[enc.input_clone[(v,0)]]; b1[v]=model[enc.input_clone[(v,1)]]
    return a0,a1,b0,b1


def merge_assign(*parts):
    d={}
    for p in parts: d.update(p)
    return d


def verify_witness(formula:CNF, witness):
    a0,a1,b0,b1=witness
    vals={
        '00':eval_cnf(formula,merge_assign(a0,b0)),
        '01':eval_cnf(formula,merge_assign(a0,b1)),
        '10':eval_cnf(formula,merge_assign(a1,b0)),
        '11':eval_cnf(formula,merge_assign(a1,b1)),
    }
    defect=(vals['00'] and vals['11']) ^ (vals['01'] and vals['10'])
    return vals, bool(defect)


def brute_rank1(n:int, formula:CNF, cut_A:Set[int]) -> bool:
    A=sorted(cut_A); B=sorted(set(range(1,n+1))-cut_A)
    rows=[]
    for aa in product((False,True), repeat=len(A)):
        row=[]
        for bb in product((False,True), repeat=len(B)):
            d={v:x for v,x in zip(A,aa)}; d.update({v:x for v,x in zip(B,bb)})
            row.append(int(eval_cnf(formula,d)))
        rows.append(row)
    for r0 in range(len(rows)):
        for r1 in range(r0+1,len(rows)):
            for c0 in range(len(rows[0])):
                for c1 in range(c0+1,len(rows[0])):
                    if (rows[r0][c0]*rows[r1][c1]) ^ (rows[r0][c1]*rows[r1][c0]):
                        return False
    return True


def all_block_bipartitions(blocks:Sequence[Sequence[int]]):
    """Unordered nontrivial bipartitions, fixing block 0 on A side."""
    k=len(blocks)
    if k<2: return
    for mask in range(0,1<<(k-1)):
        Aidx={0}
        for j in range(1,k):
            if mask & (1<<(j-1)): Aidx.add(j)
        if len(Aidx)==k: continue
        A=set(v for j in Aidx for v in blocks[j])
        yield A, Aidx


def factor_blocks(n:int, formula:CNF, blocks:Sequence[Sequence[int]], stats=None):
    """Recover a finest factorization by recursive valid-cut splitting.
    Exponential in number of carrier blocks in worst case; intended as SAT refinement baseline.
    """
    if stats is None: stats={'sat_calls':0,'cuts_tested':0}
    blocks=[tuple(sorted(b)) for b in blocks]
    if len(blocks)<=1: return blocks,stats
    for A,Aidx in all_block_bipartitions(blocks):
        stats['cuts_tested']+=1; stats['sat_calls']+=1
        enc=build_defect_encoding(n,formula,A)
        model=dpll(enc.clauses,enc.nvars)
        if model is None: # separable cut
            left=[blocks[j] for j in sorted(Aidx)]
            right=[blocks[j] for j in range(len(blocks)) if j not in Aidx]
            lf,stats=factor_blocks(n,formula,left,stats)
            rf,stats=factor_blocks(n,formula,right,stats)
            return lf+rf,stats
    # No valid split => merge all carrier blocks into one semantic factor.
    return [tuple(sorted(v for b in blocks for v in b))],stats


def random_cnf(n:int,m:int,width:int,rng):
    cls=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1), min(width,n))
        cls.append(tuple(v if rng.random()<.5 else -v for v in vs))
    return cls


def self_test(seed=1, trials=100):
    rng=random.Random(seed); failures=[]; rows=[]
    for t in range(trials):
        n=rng.randint(2,7); m=rng.randint(1, max(1,2*n)); w=rng.randint(1,min(4,n))
        f=random_cnf(n,m,w,rng)
        split=rng.randint(1,n-1); A=set(rng.sample(range(1,n+1),split))
        enc=build_defect_encoding(n,f,A)
        model=dpll(enc.clauses,enc.nvars)
        sat=model is not None
        exact=not brute_rank1(n,f,A)
        good=(sat==exact)
        if sat:
            vals,defect=verify_witness(f,witness_from_model(enc,model)); good=good and defect
        if not good: failures.append(t)
        rows.append({'trial':t,'n':n,'m':m,'width':w,'cut_A':sorted(A),'encoding_vars':enc.nvars,'encoding_clauses':len(enc.clauses),'defect_sat':sat,'brute_defect':exact,'ok':good})
    return failures,rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dimacs')
    ap.add_argument('--cut', help='comma-separated variables on A side')
    ap.add_argument('--export')
    ap.add_argument('--self-test',type=int,default=0)
    ap.add_argument('--json-out')
    args=ap.parse_args()
    if args.self_test:
        fail,rows=self_test(trials=args.self_test)
        data={'tests':len(rows),'failures':fail,'rows':rows}
        print(json.dumps({'tests':len(rows),'failure_count':len(fail)},indent=2))
        if args.json_out:
            with open(args.json_out,'w') as f: json.dump(data,f,indent=2)
        raise SystemExit(1 if fail else 0)
    if not args.dimacs or not args.cut: ap.error('--dimacs and --cut required unless --self-test')
    n,f=parse_dimacs(args.dimacs); A={int(x) for x in args.cut.split(',') if x.strip()}
    enc=build_defect_encoding(n,f,A)
    if args.export:
        write_dimacs(args.export,enc.nvars,enc.clauses,[f'four-corner defect for cut A={sorted(A)}'])
    model=dpll(enc.clauses,enc.nvars)
    if model is None:
        print('UNSAT defect: implicit CM has rank <= 1; cut is AND-separable')
    else:
        wit=witness_from_model(enc,model); vals,ok=verify_witness(f,wit)
        print('SAT defect: rank > 1; cut is NOT AND-separable')
        print('corner values:',vals,'verified=',ok)
        print('witness:',wit)

if __name__=='__main__': main()
