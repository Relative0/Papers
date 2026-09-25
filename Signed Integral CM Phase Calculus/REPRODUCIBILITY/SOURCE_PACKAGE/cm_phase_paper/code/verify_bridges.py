#!/usr/bin/env python3
"""Supplementary exact bridge tests and independent binary-rank audit.
No NumPy, SymPy, floating-point or complex arithmetic is used here.
"""
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def rot(a,k=1):return tuple(a[(j-k)%4] for j in range(4))
def q(a):return (a[0]-a[2],a[1]-a[3])
def j(z):return (-z[1],z[0])
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def conv(a,b):return tuple(sum(a[t]*b[(k-t)%4] for t in range(4)) for k in range(4))
def gmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def bits(a):return tuple((a>>j)&1 for j in range(4))
def enc(a):return sum((x%2)<<j for j,x in enumerate(a))
def boolmul(a,b):return enc(conv(bits(a),bits(b)))
def truth(a,x,y):return (a>>{(1,1):0,(1,0):1,(0,0):2,(0,1):3}[(x,y)])&1

def rank(columns):
    piv={}
    for v in columns:
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return len(piv)

def main():
    res={}; grid=list(product((-1,0,1),repeat=4)); n=0
    for a in grid:
        assert q(rot(a))==j(q(a))
        assert sum(x*x for x in q(a))==sum(x*x for x in a)-sum(a[t]*a[(t-2)%4] for t in range(4))
        for b in grid:
            assert q(conv(a,b))==gmul(q(a),q(b))
            # Raw geometric H: (A+B, A+P^2 B), then quotient.
            assert q(plus(a,b))==plus(q(a),q(b))
            assert q(plus(a,rot(b,2)))==minus(q(a),q(b))
            n+=1
    res['integer_convolution_and_raw_H_pairs']=n
    checks=0
    for a,b in product(range(16),repeat=2):
        qa,qb=q(bits(a)),q(bits(b)); qc=q(bits(a&b))
        assert q(bits(a^b))==tuple(qa[t]+qb[t]-2*qc[t] for t in range(2))
        for x,y in product((0,1),repeat=2):
            assert truth(enc(rot(bits(a))),x,y)==truth(a,1-y,x)
            for phi in range(16):
                combined=enc(tuple(truth(phi,aa,bb) for aa,bb in zip(bits(a),bits(b))))
                assert truth(combined,x,y)==truth(phi,truth(a,x,y),truth(b,x,y))
                checks+=1
    res['all_pointwise_CM_composition_checks']=checks
    res['binary_CM_image_under_Q_size']=len({q(bits(a)) for a in range(16)})
    oracle_checks=0
    for a,b in product(range(16),repeat=2):
        def oracle(cm,i):
            x,y,z=(i>>2)&1,(i>>1)&1,i&1
            return i^truth(cm,x,y)
        assert len({oracle(a,i) for i in range(8)})==8
        for i in range(8):
            assert oracle(a,oracle(b,i))==oracle(a^b,i)
            oracle_checks+=1
    res['oracle_composition_checks']=oracle_checks
    logical_checks=0
    for a in range(16):
        # Source tensor basis order: 11,10,01,00.
        row=[truth(a,x,y) for x,y in [(1,1),(1,0),(0,1),(0,0)]]
        gate=[row,[1-v for v in row]]
        for col,(x,y) in enumerate([(1,1),(1,0),(0,1),(0,0)]):
            assert (gate[0][col],gate[1][col])==(truth(a,x,y),1-truth(a,x,y))
            logical_checks+=1
    res['CM_to_logical_gate_checks']=logical_checks
    # Independent verification of determinant-derived counts by binary rank.
    mul=[[boolmul(a,b) for b in range(16)] for a in range(16)]
    invertible=0; isometries=[]
    for a,b,c,d in product(range(16),repeat=4):
        col=[mul[a][1<<k]|(mul[c][1<<k]<<4) for k in range(4)]
        col += [mul[b][1<<k]|(mul[d][1<<k]<<4) for k in range(4)]
        invertible += rank(col)==8
        if len(set(col))==8 and all(v.bit_count()==1 for v in col):isometries.append([a,b,c,d])
    earlier=json.loads((ROOT/'data/finite_summary.json').read_text())
    assert invertible==earlier['invertible']
    assert isometries==earlier['weight_operators']
    res['independent_binary_rank_invertibles']=invertible
    res['independent_unit_column_isometries']=len(isometries)
    # The explicitly derived four shell-identity maps.
    for alpha,beta in product((0,1),repeat=2):
        a,b,c,d=1^(15*alpha),15*alpha,15*beta,1^(15*beta)
        for x,y in product(range(16),repeat=2):
            if x.bit_count()+y.bit_count()==4:
                assert (mul[a][x]^mul[b][y],mul[c][x]^mul[d][y])==(x,y)
    res['explicit_shell_kernel_maps']=4
    (ROOT/'data/bridge_summary.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))

if __name__=='__main__':main()
