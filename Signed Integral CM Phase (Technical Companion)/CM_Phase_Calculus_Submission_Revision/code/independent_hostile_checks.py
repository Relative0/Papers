from itertools import product, combinations
import json

def bits4(x): return [(x>>i)&1 for i in range(4)]
def enc(v): return sum((b&1)<<i for i,b in enumerate(v))
def rot(x,k=1):
    v=bits4(x); k%=4
    return enc([v[(i-k)%4] for i in range(4)])
def mul(a,b):
    A=bits4(a); B=bits4(b); C=[0]*4
    for i in range(4):
        for j in range(4): C[(i+j)%4]^=A[i]&B[j]
    return enc(C)
def wt4(x): return x.bit_count()
def add(a,b): return a^b

def op_apply(U,s):
    a,b,c,d=U; x,y=s
    return (mul(a,x)^mul(b,y), mul(c,x)^mul(d,y))
def wt8(s): return wt4(s[0])+wt4(s[1])

# Q maps coefficient order (E0,E1,E2,E3) to Z^2.
def Q(x):
    a=bits4(x); return (a[0]-a[2], a[1]-a[3])
def Q_int(v): return (v[0]-v[2], v[1]-v[3])
def P_int(v): return (v[3],v[0],v[1],v[2])
def J(q): return (-q[1],q[0])

# QP = JQ on a nontrivial integer box.
qp_ok=all(Q_int(P_int(v))==J(Q_int(v)) for v in product(range(-2,3), repeat=4))
# kernel on bounded box matches (a,b,a,b).
ker_ok=all((Q_int(v)==(0,0)) == (v[0]==v[2] and v[1]==v[3]) for v in product(range(-2,3), repeat=4))
# carry identity all binary pairs.
carry_ok=True
for A in range(16):
  for B in range(16):
    lhs=Q(A^B); qa=Q(A); qb=Q(B); qab=Q(A&B)
    rhs=(qa[0]+qb[0]-2*qab[0], qa[1]+qb[1]-2*qab[1])
    if lhs!=rhs: carry_ok=False

# Fresh classification using only images of the 8 binary unit coordinates.
units=[(1<<i,0) for i in range(4)] + [(0,1<<i) for i in range(4)]
global_iso=[]
shell_pres=[]
shell=[(enc([1 if i in S else 0 for i in range(4)]), enc([1 if i+4 in S else 0 for i in range(4)])) for S in combinations(range(8),4)]
# sanity unique shell
assert len(set(shell))==70
fringe_targets={(0,2,4,2),(2,4,2,0),(4,2,0,2),(2,0,2,4),(4,2,0,2),(2,0,2,4),(0,2,4,2),(2,4,2,0)}
fringe_hits=0
phase_profiles={}
for U in product(range(16), repeat=4):
    imgs=[op_apply(U,e) for e in units]
    # a binary linear map preserves full Hamming weight iff unit images are eight distinct units.
    coords=[]; ok=True
    for z in imgs:
        if wt8(z)!=1: ok=False; break
        if z[0]: coord=(0, bits4(z[0]).index(1))
        else: coord=(1, bits4(z[1]).index(1))
        coords.append(coord)
    if ok and len(set(coords))==8:
        global_iso.append(U)
    sh_ok=True
    for s in shell:
        if wt8(op_apply(U,s))!=4:
            sh_ok=False; break
    if sh_ok:
        shell_pres.append(U)
        for s in shell:
            prof=[]
            for k in range(4):
                phased=(rot(s[0],k),s[1])
                out=op_apply(U,phased)
                prof.append(wt4(out[0]))
            t=tuple(prof); phase_profiles[t]=phase_profiles.get(t,0)+1
            if t in fringe_targets: fringe_hits+=1

# Oracle and phase-carry identities, evaluated directly on truth tables.
def f(A,x,y):
    # displayed CM [[a,b],[c,d]] with row x=1,0 and col y=1,0; encoding coeffs [a,b,d,c]
    coeff=bits4(A)
    idx={(1,1):0,(1,0):1,(0,0):2,(0,1):3}[(x,y)]
    return coeff[idx]
phasecarry_ok=True
oracle_comp_ok=True
for A in range(16):
  for B in range(16):
    for x,y in product((0,1), repeat=2):
      if (f(A,x,y)^f(B,x,y)) != f(A^B,x,y): oracle_comp_ok=False
      for k in range(8):
        lhs=(k*f(A^B,x,y))%8
        rhs=(k*f(A,x,y)+k*f(B,x,y)-2*k*(f(A,x,y)&f(B,x,y)))%8
        if lhs!=rhs: phasecarry_ok=False

out={
 'QP_equals_JQ_on_box':qp_ok,
 'kernel_pattern_on_box':ker_ok,
 'carry_all_256_pairs':carry_ok,
 'global_hamming_isometries':len(global_iso),
 'shell_preservers':len(shell_pres),
 'fringe_hits':fringe_hits,
 'phase_profiles':{','.join(map(str,k)):v for k,v in sorted(phase_profiles.items())},
 'oracle_xor_truth_identity':oracle_comp_ok,
 'phase_carry_all_cases':phasecarry_ok,
}
print(json.dumps(out,indent=2,sort_keys=True))
