"""Exact research prototype, not an integrated compiler or novelty proof.

Finite propositional PALO-style polynomial kernels only. Pure Python, rational
arithmetic, independent Boolean evaluator, deterministic witnesses and Bernstein
box bounds. Run with Python 3.10+. Writes only beside this file.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
import time

OUT = Path(__file__).resolve().parent
CHECKS = 0

def check(condition):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(f'check {CHECKS} failed')

class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.t = {tuple(a): F(c) for a,c in (terms or {}).items() if c}
    @staticmethod
    def constant(n, c):
        return Poly(n, {(0,)*n:F(c)})
    @staticmethod
    def var(n, i):
        a = [0]*n
        a[i] = 1
        return Poly(n, {tuple(a):1})
    def coerce(self, other):
        return other if isinstance(other, Poly) else Poly.constant(self.n, other)
    def __add__(self, other):
        other = self.coerce(other)
        assert self.n == other.n
        t = dict(self.t)
        for a,c in other.t.items():
            t[a] = t.get(a, F(0)) + c
        return Poly(self.n, t)
    __radd__ = __add__
    def __neg__(self):
        return Poly(self.n, {a:-c for a,c in self.t.items()})
    def __sub__(self, other):
        return self + (-self.coerce(other))
    def __rsub__(self, other):
        return self.coerce(other) - self
    def __mul__(self, other):
        other = self.coerce(other)
        assert self.n == other.n
        t = {}
        for a,c in self.t.items():
            for b,d in other.t.items():
                e = tuple(x+y for x,y in zip(a,b))
                t[e] = t.get(e, F(0)) + c*d
        return Poly(self.n, t)
    __rmul__ = __mul__
    def __pow__(self, k):
        assert isinstance(k,int) and k >= 0
        r = Poly.constant(self.n,1)
        for _ in range(k):
            r = r*self
        return r
    def __eq__(self, other):
        return isinstance(other,Poly) and self.n == other.n and self.t == other.t
    def value(self, x):
        assert len(x) == self.n
        return sum((c * prod(F(v)**k for v,k in zip(x,a)) for a,c in self.t.items()), F(0))
    def derivative(self, i):
        t = {}
        for a,c in self.t.items():
            if a[i]:
                b = list(a)
                b[i] -= 1
                t[tuple(b)] = c*a[i]
        return Poly(self.n,t)
    def degrees(self):
        return tuple(max((a[i] for a in self.t), default=0) for i in range(self.n))
    def squarefree(self):
        t = {}
        for a,c in self.t.items():
            b = tuple(int(k>0) for k in a)
            t[b] = t.get(b,F(0))+c
        return Poly(self.n,t)
    def substitute(self, values):
        assert len(values) == self.n and values
        m = values[0].n
        return sum((prod([Poly.constant(m,c)] + [v**k for v,k in zip(values,a)]) for a,c in self.t.items()), Poly.constant(m,0))
    def json(self):
        return [{'powers':list(a),'coefficient':str(c)} for a,c in sorted(self.t.items())]

def prod(values):
    r = 1
    for v in values:
        r = r*v
    return r

# Four coefficients ordered (11,10,01,00). A token is not a soft-expression hash.
TABLES = {
    'and':(1,0,0,0), 'or':(1,1,1,0), 'imp':(1,0,1,1),
    'eq':(1,0,0,1), 'xor':(0,1,1,0),
}

def table(op):
    return TABLES[op] if isinstance(op,str) else op

def kernel(op, p, q):
    a,b,c,d = table(op)
    return d+(b-d)*p+(c-d)*q+(a-b-c+d)*p*q

def soft(e, variables):
    n = len(variables)
    if isinstance(e,str):
        return Poly.var(n, variables.index(e))
    if isinstance(e,int):
        return Poly.constant(n,e)
    if e[0] == 'not':
        return 1-soft(e[1], variables)
    return kernel(e[0], soft(e[1],variables), soft(e[2],variables))

def boolean(e, env):
    if isinstance(e,str):
        return int(env[e])
    if isinstance(e,int):
        return e
    if e[0] == 'not':
        return 1-boolean(e[1],env)
    p,q = boolean(e[1],env),boolean(e[2],env)
    return table(e[0])[(1-p)*2+(1-q)]

def whole_table(e, variables):
    n = len(variables)
    ps = [Poly.var(n,i) for i in range(n)]
    r = Poly.constant(n,0)
    for bits in product((0,1),repeat=n):
        if boolean(e,dict(zip(variables,bits))):
            r += prod(p if b else 1-p for p,b in zip(ps,bits))
    return r

def witness(delta):
    """Complete finite identity rejection for explicit bounded-degree polynomials."""
    if not delta.t:
        return None
    ds = delta.degrees()
    grids = [[F(j+1,d+2) for j in range(d+1)] for d in ds]
    for x in product(*grids):
        if delta.value(x):
            return {'point':[str(v) for v in x],'residual':str(delta.value(x))}
    raise AssertionError('Nonzero polynomial vanished on its unisolvent grid')

def bernstein_bounds(poly, box):
    """Sound convex-hull bounds, no claim of sharpness or decision completeness."""
    n = poly.n
    transformed = poly.substitute([lo+(hi-lo)*Poly.var(n,i) for i,(lo,hi) in enumerate(box)])
    ds = transformed.degrees()
    coefficients = []
    for k in product(*(range(d+1) for d in ds)):
        b = F(0)
        for a,c in transformed.t.items():
            if all(ai<=ki for ai,ki in zip(a,k)):
                b += c*prod(F(comb(ki,ai),comb(di,ai)) for ai,ki,di in zip(a,k,ds))
        coefficients.append(b)
    return min(coefficients),max(coefficients)

def abs_bound(bounds):
    return max(abs(v) for v in bounds)

def boolean_ideal_certificate(poly):
    """Return M(poly), H_i with poly=M(poly)+sum((x_i^2-x_i)H_i).

    A deterministic telescoping decomposition; ordinary polynomial algebra,
    supplied as an auditable certificate rather than claimed as a new theorem.
    """
    hs = [Poly.constant(poly.n,0) for _ in range(poly.n)]
    for a,c in poly.t.items():
        for i,m in enumerate(a):
            if m < 2:
                continue
            for k in range(m-1):
                b = tuple(int(v>0) if j<i else k if j==i else v for j,v in enumerate(a))
                hs[i] += Poly(poly.n,{b:c})
    normal = poly.squarefree()
    reconstructed = normal
    for i,h in enumerate(hs):
        x = Poly.var(poly.n,i)
        reconstructed += (x*x-x)*h
    check(poly==reconstructed)
    return normal,hs

def rewrite_record(name, a, b, variables):
    pa,pb = soft(a,variables),soft(b,variables)
    delta = pa-pb
    wa,wb = whole_table(a,variables),whole_table(b,variables)
    corners = list(product((0,1),repeat=len(variables)))
    bool_eq = all(boolean(a,dict(zip(variables,x))) == boolean(b,dict(zip(variables,x))) for x in corners)
    check(bool_eq == (wa == wb))
    check(pa.squarefree() == wa)
    check(pb.squarefree() == wb)
    normal,hs = boolean_ideal_certificate(delta)
    check(bool_eq == (not normal.t))
    w = witness(delta)
    if w:
        x = list(map(F,w['point']))
        check(pa.value(x)-pb.value(x) == F(w['residual']))
    return {'name':name,'source_ast':a,'target_ast':b,'variables':variables,'boolean_equivalent':bool_eq,
            'same_expectation_every_joint_model':bool_eq,
            'recursive_soft_equal':not delta.t,'exact_soft_residual':delta.json(),
            'boolean_ideal_certificate':[h.json() for h in hs],
            'rational_soft_counterexample':w,
            'gradient_residuals':[delta.derivative(i).json() for i in range(len(variables))]}

def run():
    started = time.perf_counter()
    x,y,z = 'x','y','z'
    N = lambda a:('not',a)
    A = lambda a,b:('and',a,b)
    O = lambda a,b:('or',a,b)
    I = lambda a,b:('imp',a,b)
    E = lambda a,b:('eq',a,b)
    R = lambda a,b:('xor',a,b)
    specs = [
      ('and_commutativity',A(x,y),A(y,x),[x,y]),
      ('and_associativity',A(A(x,y),z),A(x,A(y,z)),[x,y,z]),
      ('or_associativity',O(O(x,y),z),O(x,O(y,z)),[x,y,z]),
      ('de_morgan',N(A(x,y)),O(N(x),N(y)),[x,y]),
      ('implication_expansion',I(x,y),O(N(x),y),[x,y]),
      ('equivalence_to_two_implications',E(x,y),A(I(x,y),I(y,x)),[x,y]),
      ('and_idempotence',A(x,x),x,[x]),
      ('or_idempotence',O(x,x),x,[x]),
      ('excluded_middle',O(x,N(x)),1,[x]),
      ('contradiction',A(x,N(x)),0,[x]),
      ('absorption',A(x,O(x,y)),x,[x,y]),
      ('distribution',A(x,O(y,z)),O(A(x,y),A(x,z)),[x,y,z]),
      ('xor_self',R(x,x),0,[x]),
      ('signed_frame_transport',I(N(y),x),O(y,x),[x,y]),
      ('compiler_paper_worked_fusion',R(I(x,N(y)),I(N(y),x)),E(x,y),[x,y]),
      ('shared_support_cancellation',O(A(x,y),A(x,N(y))),x,[x,y]),
      ('dag_cse_value',A(I(x,y),I(x,y)),A(I(x,y),I(x,y)),[x,y]),
    ]
    rewrites = [rewrite_record(*s) for s in specs]
    # Independent exact evaluations of the handoff's elementary bridges.
    p,q = F(1,2),F(1,2)
    check(kernel('eq',p,q)==F(1,2))
    check(kernel('and',kernel('imp',p,q),kernel('imp',q,p))==F(9,16))
    check(F(3,5)**2 < F(1,2))
    check(1*1 >= F(1,2))
    check(Poly.var(1,0).value([p])**2==F(1,4))
    for C in product((0,1),repeat=4):
        a,b,c,d = C
        for p,q in product((F(0),F(1,3),F(1,2),F(1)),repeat=2):
            for r in {max(F(0),p+q-1),min(p,q),p*q}:
                joint = a*r+b*(p-r)+c*(q-r)+d*(1-p-q+r)
                check(joint-kernel(C,p,q)==(a-b-c+d)*(r-p*q))
    # Arbitrary operator composition, with overlap, not merely 16 primitives.
    tables = list(product((0,1),repeat=4))
    exhaustive = []
    for label, variables, pair1, pair2 in [
        ('same_frame',[x,y],(x,y),(x,y)),
        ('overlapping_support',[x,y,z],(x,y),(y,z)),
        ('disjoint_support',[x,y,z,'w'],(x,y),(z,'w')),
    ]:
        admissible = rejected = 0
        for outer,c1,c2 in product(tables,repeat=3):
            e = (outer,(c1,*pair1),(c2,*pair2))
            polynomial = soft(e,variables)
            # Boolean quotient reconstruction is checked against independent oracle.
            event_polynomial = whole_table(e,variables)
            check(polynomial.squarefree()==event_polynomial)
            safe = polynomial==event_polynomial
            check(safe == all(d<=1 for d in polynomial.degrees()))
            if safe:
                admissible += 1
            else:
                rejected += 1
                w = witness(polynomial-event_polynomial)
                check(w is not None)
            # One rational point checks sound corners plus interior range of kernels.
            v = polynomial.value([F(1,3)]*len(variables))
            check(F(0)<=v<=F(1))
        exhaustive.append({'family':label,'circuits':admissible+rejected,
                           'soft_preserving_table_folds':admissible,'rejected_folds':rejected})
    # A parameter constraint changes admissibility; variable IDs alone are insufficient.
    diff = soft(E(x,y),[x,y])-soft(A(I(x,y),I(y,x)),[x,y])
    t = Poly.var(1,0)
    pullback = diff.substitute([t,Poly.constant(1,1)])
    check(not pullback.t)
    # Same numerical parameter does not mean same Bernoulli event.
    independent_and = soft(A(x,y),[x,y]).substitute([t,t])
    same_event_and = whole_table(A(x,x),[x])
    check(independent_and != same_event_and)
    # Equal expectations at one model are not a contextual replacement contract.
    uniform = {bits:F(1,4) for bits in product((0,1),repeat=2)}
    def expect(e):
        return sum(w*boolean(e,dict(zip([x,y],bits))) for bits,w in uniform.items())
    check(expect(x)==expect(y)==F(1,2))
    check(expect(A(x,x))==F(1,2))
    check(expect(A(x,y))==F(1,4))
    # A value-small rewrite can have a large derivative defect.
    narrow = [(F(0),F(1,100))]
    delta = soft(A(x,x),[x])-soft(x,[x])
    vb = bernstein_bounds(delta,narrow)
    gb = bernstein_bounds(delta.derivative(0),narrow)
    check(abs_bound(vb)==F(99,10000))
    check(abs_bound(gb)==1)
    # Exact box decision certificate: both x and x^2 are >= .5 on [.75,1].
    decision_box = [(F(3,4),F(1))]
    px = soft(x,[x]); pxx = soft(A(x,x),[x])
    bx,bxx = bernstein_bounds(px,decision_box),bernstein_bounds(pxx,decision_box)
    check(bx[0]>=F(1,2) and bxx[0]>=F(1,2))
    # Bernstein convex-hull checks on all test residuals and derivative residuals.
    for r,s in zip(rewrites,specs):
        delta = soft(s[1],s[3])-soft(s[2],s[3])
        box = [(F(0),F(1))]*len(s[3])
        for poly in [delta]+[delta.derivative(i) for i in range(delta.n)]:
            lo,hi = bernstein_bounds(poly,box)
            for point in product((F(0),F(1,4),F(1,2),F(3,4),F(1)),repeat=poly.n):
                check(lo<=poly.value(point)<=hi)
    # Arbitrary correlated model: Boolean-equivalent rewrites preserve expectation.
    joint_checks = 0
    for spec in specs:
        _,a,b,vs = spec
        worlds = list(product((0,1),repeat=len(vs)))
        weights = [F(i+1,sum(range(1,len(worlds)+1))) for i in range(len(worlds))]
        ea = sum(w*boolean(a,dict(zip(vs,bits))) for w,bits in zip(weights,worlds))
        eb = sum(w*boolean(b,dict(zip(vs,bits))) for w,bits in zip(weights,worlds))
        check(ea==eb)
        joint_checks += 1
    results = {'status':'PASS','assertions':CHECKS,'elapsed_seconds':time.perf_counter()-started,
       'scope':'bounded exact research checks, not a PALO integration, performance benchmark or priority proof',
       'rewrites':rewrites,'exhaustive_composition_families':exhaustive,
       'correlated_expectation_examples':joint_checks,
       'parameter_restriction_example':{'condition':'q=1, p=t','equivalence_expansion_residual':pullback.json()},
       'marginal_context_counterexample':{'model':'independent fair X,Y',
           'P(X)':'1/2','P(Y)':'1/2','P(X and X)':'1/2','P(X and Y)':'1/4'},
       'gradient_falsification':{'box':['0','1/100'],'value_error_bound':str(abs_bound(vb)),
                                'input_gradient_error_bound':str(abs_bound(gb))},
       'decision_certificate':{'box':['3/4','1'],'threshold':'1/2','x_range':list(map(str,bx)),
                               'x_squared_range':list(map(str,bxx))}}
    (OUT/'checker_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in results.items() if k not in ('rewrites',)},indent=2))

if __name__ == '__main__':
    run()
