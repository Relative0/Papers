"""Independent finite audit; no imports from the author's implementation.

Finite table cases are exhaustive. Generated expression checks are bounded
verification of a reference formalization, NOT a rerun of the author suite.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Optional
import json, random, hashlib, sys

ASSIGNMENTS = ((1,1),(1,0),(0,1),(0,0))
OPS = {'AND':8,'OR':14,'XOR':6,'IMP':11,'EQV':9}

def oracle(t: int, x: int, y: int) -> int:
    return int(f'{t:04b}'[ASSIGNMENTS.index((x,y))])

def pack(bits) -> int:
    return int(''.join(map(str,bits)), 2)

def transpose(t: int) -> int:
    return (t & 9) | ((t & 2) << 1) | ((t & 4) >> 1)

def swap_row(t: int) -> int:
    return ((t & 3) << 2) | ((t & 12) >> 2)

def swap_col(t: int) -> int:
    return ((t & 5) << 1) | ((t & 10) >> 1)

def align(t: int, swapped: bool, first_neg: bool, second_neg: bool) -> int:
    if first_neg: t=swap_row(t)
    if second_neg: t=swap_col(t)
    return transpose(t) if swapped else t

def fuse(a: int, b: int, outer: int) -> int:
    # DNF masks over the four positions; independent of scalar truth lookup.
    out=0
    for bit,(x,y) in zip((8,4,2,1), ASSIGNMENTS):
        if outer & bit:
            out |= (a if x else ~a) & (b if y else ~b)
    return out & 15

@dataclass(frozen=True)
class E:
    op: str
    a: Optional['E']=None
    b: Optional['E']=None

X,Y,Z=E('X'),E('Y'),E('Z')

def ev(e: E, env: dict[str,int]) -> int:
    if e.op in ('X','Y','Z'): return env[e.op]
    if e.op=='NOT': return 1-ev(e.a, env)
    a,b=ev(e.a,env),ev(e.b,env)
    if e.op=='AND': return int(a and b)
    if e.op=='OR': return int(a or b)
    if e.op=='XOR': return int(a!=b)
    if e.op=='IMP': return int(not a or b)
    if e.op=='EQV': return int(a==b)
    raise ValueError(e.op)

def variables(e: E) -> set[str]:
    if e.a is None: return {e.op}
    return variables(e.a) | (variables(e.b) if e.b is not None else set())

def lit(e: E):
    parity=False
    while e.op=='NOT': parity=not parity; e=e.a
    return (e.op,parity) if e.op in ('X','Y','Z') else None

def ref_compile(e: E, strategy='hybrid', fixed=None):
    fixed=fixed or {}
    def tab(e):
        if variables(e)-fixed.keys() != {'X','Y'}: return None
        return (pack(ev(e, dict(fixed, X=x, Y=y)) for x,y in ASSIGNMENTS),'T')
    if strategy=='retabulate': return tab(e)
    if e.op in OPS:
        a,b=lit(e.a),lit(e.b)
        if a and b and {a[0],b[0]}=={'X','Y'} and not ({'X','Y'} & fixed.keys()):
            return align(OPS[e.op],a[0]=='Y',a[1],b[1]),'S'
    if e.op=='NOT':
        a=ref_compile(e.a,strategy,fixed)
        if a: return a[0]^15, 'S' if a[1]=='S' else 'H'
    elif e.op in OPS:
        a,b=ref_compile(e.a,strategy,fixed),ref_compile(e.b,strategy,fixed)
        if a and b: return fuse(a[0],b[0],OPS[e.op]), 'S' if a[1]==b[1]=='S' else 'H'
    return tab(e) if strategy=='hybrid' else None

def main():
    report={'scope':'Independent scalar/matrix/token calculations and a reference model; not author implementation tests.'}
    selection=0
    for t in range(16):
        m=[[oracle(t,x,y) for y in (1,0)] for x in (1,0)]
        for x,y in ASSIGNMENTS:
            val=0
            for i,r in enumerate((1,0)):
                for j,c in enumerate((1,0)):
                    val ^= int(x==r) & m[i][j] & int(y==c)
            assert val==oracle(t,x,y);selection+=1
    report['selection_evaluations']=selection
    records=[]
    for t,s,a,b in product(range(16),range(2),range(2),range(2)):
        n=align(t,bool(s),bool(a),bool(b))
        values=[]
        for x,y in ASSIGNMENTS:
            p,q=(y,x) if s else (x,y)
            wanted=oracle(t,p^a,q^b)
            assert oracle(n,x,y)==wanted
            values.append(wanted)
        records.append((n,values))
    report['signed_frame_records']=len(records)
    report['signed_frame_assignment_checks']=4*len(records)
    fusion=0
    for a,va in records:
        for b,vb in records:
            for outer in range(16):
                n=fuse(a,b,outer)
                for k,(x,y) in enumerate(ASSIGNMENTS):
                    assert oracle(n,x,y)==oracle(outer,va[k],vb[k]);fusion+=1
    report['signed_fusion_assignment_checks']=fusion
    report['signed_fusion_table_cases']=fusion//4
    structural=[]
    for op,s,a,b in product(OPS,range(2),range(2),range(2)):
        p,q=(Y,X) if s else (X,Y)
        if a:p=E('NOT',p)
        if b:q=E('NOT',q)
        structural.append(E(op,p,q))
    cases=structural+[E('NOT',a) for a in structural]+[E(op,a,b) for op in OPS for a in structural for b in structural]
    for e in cases:
        got=ref_compile(e,'pure_structural')
        assert got is not None and got[1]=='S'
        assert got[0]==pack(ev(e,{'X':x,'Y':y}) for x,y in ASSIGNMENTS)
    report['bounded_structural_expressions']=len(cases)
    random.seed(20260926)
    def generate(d):
        if d<=0 or random.random()<0.2:return random.choice((X,Y,Z))
        if random.random()<0.2:return E('NOT',generate(d-1))
        return E(random.choice(tuple(OPS)),generate(d-1),generate(d-1))
    counts={'S':0,'T':0,'H':0,'fallback':0}
    valid=0
    for i in range(5000):
        e=generate(5);fixed={'Z':i%2}
        for strategy in ('pure_structural','hybrid','retabulate'):
            got=ref_compile(e,strategy,fixed)
            if got is None:counts['fallback']+=1;continue
            counts[got[1]]+=1;valid+=1
            assert got[0]==pack(ev(e,dict(fixed,X=x,Y=y)) for x,y in ASSIGNMENTS)
    report['seeded_expression_strategy_runs']=15000
    report['seeded_successful_tokens']=valid
    report['seeded_outcomes']=counts
    left=E('IMP',X,E('NOT',Y));right=E('IMP',E('NOT',Y),X)
    worked=E('XOR',left,right)
    assert ref_compile(left)[0]==7 and ref_compile(right)[0]==14 and ref_compile(worked)[0]==9
    structural_e=E('AND',X,Y)
    tab_e=E('OR',X,E('AND',Y,Y))
    hybrid=E('XOR',structural_e,tab_e)
    assert ref_compile(structural_e)[1]=='S'
    assert ref_compile(tab_e)[1]=='T'
    assert ref_compile(E('NOT',tab_e))[1]=='H'
    assert ref_compile(hybrid)[1]=='H'
    zero=E('XOR',structural_e,structural_e)
    assert variables(zero)=={'X','Y'} and ref_compile(zero)[0]==0
    wrong=11^11; correct=11^transpose(11)
    assert wrong==0 and correct==6
    report['explicit_regressions']={
        'worked_tokens':['0111','1110','1001'],
        'untransported_implications':{'wrong_token':wrong,'correct_token':correct},
        'syntactic_support_vs_constant':{'syntactic':['X','Y'],'essential':[],'token':0},
        'tabulated_example':{'expression':'X OR (Y AND Y)','provenance':'T'},
        'negated_tabulated_example':'H','mixed_child_example':'H',
        'derivability_note':'X AND Y permits S by primitive rule and T by unguarded TAB, but structural-first hybrid strategy selects S.'}
    report['status']='PASS'
    report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=Path(__file__).with_name('independent_finite_results.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
