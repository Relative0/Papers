"""Exact adversarial cases for Section 4.4; stdlib, no compiler/backend claim.

Run beside this audit's results. The preceding semantic checker is imported
read-only, but table probabilities and recursive crisp evaluation use a separate
weighted-outcome evaluator. No finite set of tests replaces the algebraic proof.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
checker = ROOT.parent/'semantic_boundary_20261013/semantic_contract_checker.py'
if not checker.exists():
    checker = ROOT.parent/'semantic_contract_checker.py'
spec = importlib.util.spec_from_file_location('boundary_checker', checker)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
CHECKS = 0

def check(value):
    global CHECKS
    CHECKS += 1
    if not value:
        raise AssertionError(f'Check {CHECKS} failed')

def weighted(table, p, q):
    a,b,d,e = table
    return a*p*q + b*p*(1-q) + d*(1-p)*q + e*(1-p)*(1-q)

def scalar(expr, env, crisp=False):
    if isinstance(expr, str):
        value = env[expr]
    elif isinstance(expr, int):
        value = F(expr)
    elif expr[0] == 'not':
        value = 1-scalar(expr[1], env, crisp)
    else:
        value = weighted(c.table(expr[0]), scalar(expr[1], env, crisp), scalar(expr[2], env, crisp))
    return F(value >= F(1,2)) if crisp else value

def run():
    grid = [F(0),F(1,4),F(1,2),F(3,4),F(1)]
    for table in product((0,1), repeat=4):
        for p,q in product(grid, repeat=2):
            check(weighted(table,p,q) == c.kernel(table,p,q))
            check(F(0) <= weighted(table,p,q) <= F(1))
        for p,q in product((0,1), repeat=2):
            check(weighted(table,F(p),F(q)) == table[(1-p)*2+(1-q)])

    source = ('xor',('imp','x',('not','y')),('imp',('not','y'),'x'))
    target = ('eq','x','y')
    ps,pt = c.soft(source,['x','y']),c.soft(target,['x','y'])
    for p,q in product(grid, repeat=2):
        env={'x':p,'y':q}
        check(ps.value([p,q]) == scalar(source,env))
        check(pt.value([p,q]) == scalar(target,env))
    check(scalar(source,{'x':F(1,2),'y':F(1,2)}) == F(3,8))
    check(scalar(target,{'x':F(1,2),'y':F(1,2)}) == F(1,2))
    for p,q in product((0,1), repeat=2):
        check(scalar(source,{'x':F(p),'y':F(q)}) == scalar(target,{'x':F(p),'y':F(q)}))
    check(ps.squarefree() == c.whole_table(target,['x','y']))
    check(ps != pt)

    # Distinct event identities may share a parameter without being aliased.
    t=c.Poly.var(1,0)
    distinct=c.whole_table(('and','x','y'),['x','y'])
    tied=distinct.substitute([t,t])
    repeated=c.whole_table(('and','x','x'),['x'])
    check(tied == t*t and repeated == t)
    check(tied != repeated)
    check(c.soft(('and','x','y'),['x','y']).substitute([t,t]) == tied)
    check(tied.degrees() == (2,))  # Criterion applies before parameter pullback.

    # A full-cube rejection does not imply rejection on every restricted domain.
    recursive=c.soft(('and','x','x'),['x'])
    check(recursive != repeated)
    for endpoint in (F(0),F(1)):
        check(recursive.value([endpoint]) == repeated.value([endpoint]))
    check(recursive.derivative(0).value([F(1)]) == 2)
    check(repeated.derivative(0).value([F(1)]) == 1)

    # Equal values on q=1; unequal ambient gradients; equal pullback gradients.
    p,q=c.Poly.var(2,0),c.Poly.var(2,1)
    f,g=p,p*q
    one=c.Poly.constant(1,1)
    fp,gp=f.substitute([t,one]),g.substitute([t,one])
    check(fp == gp == t)
    check(fp.derivative(0) == gp.derivative(0) == one)
    for x in grid:
        check(f.value([x,1]) == g.value([x,1]))
        check([f.derivative(i).value([x,1]) for i in range(2)] == [1,0])
        check([g.derivative(i).value([x,1]) for i in range(2)] == [1,x])
    check(f.derivative(1).value([F(1,2),1]) != g.derivative(1).value([F(1,2),1]))
    check(t != t+F(1,4))
    check(t.derivative(0) == (t+F(1,4)).derivative(0))

    # Recursive crispification is evaluated, including its tie rule.
    conjunction=('and','x','y')
    env={'x':F(3,5),'y':F(3,5)}
    check(scalar(conjunction,env) == F(9,25))
    check(scalar(conjunction,env,True) == 1)
    check(F(scalar(conjunction,env) >= F(1,2)) == 0)
    check(scalar('x',{'x':F(1,2)},True) == 1)

    # Same marginals do not determine a conjunction's probability.
    worlds=list(product((0,1),repeat=2))
    models={
        'independent': [F(1,4)]*4,
        'equal_events': [F(1,2),F(0),F(0),F(1,2)],
        'opposite_events': [F(0),F(1,2),F(1,2),F(0)],
    }
    joint={}
    for label,weights in models.items():
        px=sum(w*x for w,(x,y) in zip(weights,worlds))
        py=sum(w*y for w,(x,y) in zip(weights,worlds))
        both=sum(w*x*y for w,(x,y) in zip(weights,worlds))
        check(px == py == F(1,2))
        joint[label]=str(both)
    check(joint == {'independent':'1/4','equal_events':'1/2','opposite_events':'0'})
    # Almost-sure equality of X,Y under the equal-events model survives contexts.
    for table in product((0,1),repeat=4):
        for z in (0,1):
            for w,(x,y) in zip(models['equal_events'],worlds):
                if w:
                    check(table[(1-x)*2+(1-z)] == table[(1-y)*2+(1-z)])
    result={'status':'PASS','assertions':CHECKS,'arithmetic':'fractions.Fraction and sparse exact polynomials',
        'worked_fusion':{'source':'3/8','target':'1/2','point':['1/2','1/2']},
        'gradient_domain':{'functions':['p','p*q'],'equal_on':'q=1','ambient_gradients':['(1,0)','(1,p)'],
                           'common_pullback':'phi(t)=(t,1)','pullback_derivatives':['1','1']},
        'gradient_necessity_counterexample':'t and t+1/4 have equal derivatives but unequal values',
        'tied_independent_events':'t^2','repeated_event':'t',
        'crisp_example':{'inputs':['3/5','3/5'],'soft_product':'9/25','recursive_crisp':1,'final_threshold':0,'tie_rule':'>='},
        'same_marginals_different_joints':joint,
        'limits':'Finite exact diagnostics; not floating-point, autodiff, compiler integration, empirical rerun or a formal proof assistant.'}
    (ROOT/'exact_audit_results.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    run()
