"""Small independent algebra/domain checks; no changes outside the audit folder."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
OUT=Path(__file__).resolve().parent
counts={}
def check(kind,p):
    assert p,kind
    counts[kind]=counts.get(kind,0)+1
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2))%2 for j in range(2)] for i in range(2)]
tables=list(product((0,1),repeat=4))
for c in tables:
    C=[list(c[:2]),list(c[2:])]
    for A,B,X,Y in product((0,1),repeat=4):
        sx=[[X,1-X],[1-X,X]];sy=[[Y,1-Y],[1-Y,Y]]
        lm=mm(mm(sx,C),sy)
        direct=[[c[(1-u)*2+(1-v)] for v in (Y,1-Y)] for u in (X,1-X)]
        check('LM_normal_form',lm==direct)
        bra=[A,1-A];ket=[B,1-B]
        pairing=sum(bra[i]*lm[i][j]*ket[j] for i in range(2) for j in range(2))%2
        check('logical_pairing',pairing==c[(1-int(A==X))*2+(1-int(Y==B))])
for X in (0,1):check('Boolean_switch_involution',mm([[X,1-X],[1-X,X]],[[X,1-X],[1-X,X]])==[[1,0],[0,1]])
for p in (Q(0),Q(1,3),Q(1,2),Q(1)):
    check('real_switch_determinant',p*p-(1-p)**2==2*p-1)
    s=[[p,1-p],[1-p,p]]
    squared=[[sum(s[i][k]*s[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    check('real_switch_involution_domain',(squared==[[1,0],[0,1]])==(p in (0,1)))
def ring_mul(a,b):
    result=0
    for i,j in product(range(4),repeat=2):
        if i+j<4 and a&(1<<i) and b&(1<<j):result^=1<<(i+j)
    return result
check('nilpotent_support',ring_mul(8,2)==0)
for a,b in product(range(16),repeat=2):check('unit_predicate',int(bool(ring_mul(a,b)&1))==int(bool(a&1))*int(bool(b&1)))
for x,y in product((Q(-1),Q(-1,8),Q(1,8),Q(1)),repeat=2):
    relu_min=x-max(Q(0),x-y)
    check('ReLU_min_AND',relu_min==min(x,y) and (relu_min>0)==(x>0 and y>0))
# Local margins are strict and domain-relative; equality allows a zero.
gamma=Q(1,2);L=2
check('Lipschitz_boundary',gamma-L*(gamma/L)==0)
# Pairwise feasible anticorrelations need not admit a global joint law.
check('pairwise_global_conflict',all(not(x!=y and y!=z and z!=x) for x,y,z in product((0,1),repeat=3)))
result={'status':'PASS','checks_by_family':counts,'total_assertions':sum(counts.values()),
        'scope':'Exhaustive finite Boolean valuations and F2[u]/u4 scalar checks; concrete domain counterexamples. Not a full ring-contextuality proof.'}
(OUT/'additional_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
