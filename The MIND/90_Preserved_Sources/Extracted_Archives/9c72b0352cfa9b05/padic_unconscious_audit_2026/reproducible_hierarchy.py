from itertools import product
from fractions import Fraction
import csv, json, os

OUT = os.path.dirname(__file__)
M = 2
DEPTH = 4
points = [''.join(map(str,b)) for b in product(range(M), repeat=DEPTH)]

def lcp(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y: break
        n+=1
    return n

def d_prefix(a,b):
    if a==b: return Fraction(0,1)
    return Fraction(1, M**lcp(a,b))

def int_lsd(bits):
    return sum(int(bit)*(M**i) for i,bit in enumerate(bits))

def v_p(n,p=2):
    if n==0: return None
    n=abs(n); v=0
    while n%p==0:
        v+=1; n//=p
    return v

def d_padic(a,b):
    x,y=int_lsd(a),int_lsd(b)
    if x==y: return Fraction(0,1)
    return Fraction(1, M**v_p(x-y,M))

# Verify prefix metric is ultrametric.
ultra=True
for x in points:
    for y in points:
        for z in points:
            if d_prefix(x,z) > max(d_prefix(x,y), d_prefix(y,z)):
                ultra=False
                raise AssertionError((x,y,z))

# Verify agreement with 2-adic metric on distinct finite representatives.
for x in points:
    for y in points:
        assert d_prefix(x,y) == d_padic(x,y), (x,y,d_prefix(x,y),d_padic(x,y))

# Prefix balls / quotient classes.
balls=[]
quotients={}
for k in range(DEPTH+1):
    prefixes=[''.join(map(str,b)) for b in product(range(M), repeat=k)] if k else ['']
    quotients[k]=prefixes
    for pref in prefixes:
        members=[x for x in points if x.startswith(pref)]
        balls.append({
            'depth_k':k,
            'prefix':pref if pref else 'epsilon',
            'cardinality_in_depth4_model':len(members),
            'members':' '.join(members),
            'uniform_measure':str(Fraction(1, M**k)),
            'information_bits':k
        })

with open(os.path.join(OUT,'balls_depth4.csv'),'w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=balls[0].keys()); w.writeheader(); w.writerows(balls)

with open(os.path.join(OUT,'quotients.json'),'w') as f:
    json.dump({str(k):v for k,v in quotients.items()}, f, indent=2)

with open(os.path.join(OUT,'distance_matrix.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['point']+points)
    for x in points:
        w.writerow([x]+[str(d_prefix(x,y)) for y in points])

summary={
    'm':M,'depth':DEPTH,'number_of_points':len(points),
    'ultrametric_verified':ultra,
    'prefix_equals_2adic_distance_verified':True,
    'quotient_sizes':{str(k):len(v) for k,v in quotients.items()},
    'ball_count_all_depths':len(balls),
    'sample':{
        '0000_vs_0001':str(d_prefix('0000','0001')),
        '0000_vs_0010':str(d_prefix('0000','0010')),
        '0000_vs_0100':str(d_prefix('0000','0100')),
        '0000_vs_1000':str(d_prefix('0000','1000'))
    }
}
with open(os.path.join(OUT,'computation_summary.json'),'w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
