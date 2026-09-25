from itertools import combinations
from fractions import Fraction
import json
import sympy as sp

# Exact symbolic case study: F(x,y)=x+y+xy with x=eps1*a, y=eps2*b, a,b>0.
a,b = sp.symbols('a b', positive=True)
scores = {
    '11': sp.expand(a+b+a*b),
    '10': sp.expand(a-b-a*b),
    '01': sp.expand(-a+b-a*b),
    '00': sp.expand(-a-b+a*b),
}

# True-first operator truth tables in (11,10,01,00) order.
operators = {
    'AND':   (1,0,0,0),
    'X':     (1,1,0,0),
    'Y':     (1,0,1,0),
    'XNOR':  (1,0,0,1),
}
coords = ('11','10','01','00')

# Certificate identities showing at most one of the three nontrivial scores is positive.
certificate_identities = {
    'g10+g01': sp.expand(scores['10']+scores['01']),
    'g10+g00': sp.expand(scores['10']+scores['00']),
    'g01+g00': sp.expand(scores['01']+scores['00']),
}
expected = {
    'g10+g01': -2*a*b,
    'g10+g00': -2*b,
    'g01+g00': -2*a,
}
assert all(sp.expand(certificate_identities[k]-expected[k]) == 0 for k in expected)
assert scores['11'] == a+b+a*b

# Discriminant curves solved explicitly where possible.
curves = {
    'g10=0': sp.solve(sp.Eq(scores['10'],0), b)[0],  # b=a/(1+a)
    'g01=0': sp.solve(sp.Eq(scores['01'],0), a)[0],  # a=b/(1+b)
    'g00=0': sp.solve(sp.Eq(scores['00'],0), b)[0],  # b=a/(a-1)
}

# Curvature of the X/AND boundary; nonzero for a>0.
curve_x = sp.simplify(curves['g10=0'])
curve_x_second = sp.simplify(sp.diff(curve_x,a,2))
assert curve_x_second != 0

# Minimum polarity probes for the realized operator family.
def distinguish_subset(indices):
    seen = set()
    for name,t in operators.items():
        sig = tuple(t[i] for i in indices)
        if sig in seen:
            return False
        seen.add(sig)
    return True

minimum_probe_sets=[]
for k in range(1,5):
    for inds in combinations(range(4),k):
        if distinguish_subset(inds):
            minimum_probe_sets.append(tuple(coords[i] for i in inds))
    if minimum_probe_sets:
        min_probe_size=k
        break
assert min_probe_size == 3

# Exact rational spot checks, avoiding boundary values.
def classify(aa,bb):
    aa=Fraction(aa); bb=Fraction(bb)
    vals=(aa+bb+aa*bb, aa-bb-aa*bb, -aa+bb-aa*bb, -aa-bb+aa*bb)
    if any(v==0 for v in vals): return 'BOUNDARY', vals
    bits=tuple(int(v>0) for v in vals)
    for name,t in operators.items():
        if bits==t: return name, vals
    return 'UNEXPECTED', vals

samples = {
    'AND': (Fraction(1,2),Fraction(1,2)),
    'X': (Fraction(2,1),Fraction(1,2)),
    'Y': (Fraction(1,2),Fraction(2,1)),
    'XNOR': (Fraction(3,1),Fraction(3,1)),
}
for expected_name,(aa,bb) in samples.items():
    got,_=classify(aa,bb)
    assert got==expected_name,(expected_name,got,aa,bb)

# Exhaustive rational grid sanity check: every off-boundary point is one of the four operators.
counts={k:0 for k in list(operators)+['BOUNDARY']}
for p in range(1,21):
    for q in range(1,21):
        aa=Fraction(p,4); bb=Fraction(q,4)
        name,_=classify(aa,bb)
        assert name in counts, (aa,bb,name)
        counts[name]+=1

# Transition graph: curved zero sets are pairwise disjoint for a,b>0 by the negative-sum identities.
# Each one separates AND from exactly one leaf operator.
transition_edges = [('AND','X','g10=0'),('AND','Y','g01=0'),('AND','XNOR','g00=0')]

result = {
    'scores': {k:str(v) for k,v in scores.items()},
    'certificate_identities': {k:str(v) for k,v in certificate_identities.items()},
    'curves': {k:str(v) for k,v in curves.items()},
    'x_boundary_second_derivative': str(curve_x_second),
    'operators_true_first_11_10_01_00': {k:list(v) for k,v in operators.items()},
    'minimum_probe_size': min_probe_size,
    'minimum_probe_sets': [list(x) for x in minimum_probe_sets],
    'sample_classifications': {k:[str(v[0]),str(v[1])] for k,v in samples.items()},
    'grid_counts': counts,
    'transition_edges': transition_edges,
    'status':'PASS'
}
with open('/mnt/data/Restricted_Guard_CM_LM_Research_2026-09-24/nonlinear_case_study_results.json','w') as f:
    json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
