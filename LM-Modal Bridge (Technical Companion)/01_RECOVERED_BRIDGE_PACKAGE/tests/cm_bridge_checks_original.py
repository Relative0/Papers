from itertools import product
import json

# A = F2[u]/(u^4), elements are 4-bit coefficient vectors in basis 1,u,u^2,u^3.
def add(a,b): return a ^ b

def mul(a,b):
    out=0
    for i in range(4):
        if (a>>i)&1:
            for j in range(4-i):
                if (b>>j)&1:
                    out ^= 1<<(i+j)
    return out

def inv_unit(a):
    for b in range(16):
        if mul(a,b)==1:
            return b
    raise ValueError(a)

units=[a for a in range(16) if a&1]
idempotents=[a for a in range(16) if mul(a,a)==a]

def det(M):
    a,b,c,d=M
    return add(mul(a,d),mul(b,c)) # minus = plus in char 2

def mm(A,B):
    a,b,c,d=A; e,f,g,h=B
    return (add(mul(a,e),mul(b,g)), add(mul(a,f),mul(b,h)),
            add(mul(c,e),mul(d,g)), add(mul(c,f),mul(d,h)))

def mv(A,v):
    a,b,c,d=A; x,y=v
    return (add(mul(a,x),mul(b,y)), add(mul(c,x),mul(d,y)))

def inv2(A):
    a,b,c,d=A; z=det(A); zi=inv_unit(z)
    # adjugate signs are + in char 2
    return (mul(zi,d), mul(zi,b), mul(zi,c), mul(zi,a))

I=(1,0,0,1)
P0=(1,0,0,0)
P1=(0,0,0,1)

# Canonicalize a reversible ordered basis under row unit scaling and row swap.
def scale_row(M,u0,u1):
    a,b,c,d=M
    return (mul(u0,a),mul(u0,b),mul(u1,c),mul(u1,d))
def swap_rows(M):
    a,b,c,d=M
    return (c,d,a,b)
def canon(M):
    reps=[]
    for u0 in units:
        for u1 in units:
            X=scale_row(M,u0,u1)
            reps.append(X); reps.append(swap_rows(X))
    return min(reps)

gl=[]; projective=set()
for M in product(range(16), repeat=4):
    if det(M) in units:
        gl.append(M); projective.add(canon(M))

# Check basis-projector update for each projective basis and every concrete state.
update_checks=0
branch_equiv_checks=0
same_basis_repeat_checks=0
for B in projective:
    Bi=inv2(B)
    for P,idx in [(P0,0),(P1,1)]:
        J=mm(mm(Bi,P),B)
        assert mm(J,J)==J
        other=P1 if idx==0 else P0
        Jo=mm(mm(Bi,other),B)
        assert mm(J,Jo)==(0,0,0,0)
        assert tuple(add(x,y) for x,y in zip(J,Jo))==I
        update_checks += 1
        for psi in product(range(16), repeat=2):
            coeff=mv(B,psi)[idx]
            br=mv(J,psi)
            assert (br!=(0,0)) == (coeff!=0)
            # B applied to branch has exactly one coordinate retained
            bc=mv(B,br)
            assert bc[idx]==coeff and bc[1-idx]==0
            branch_equiv_checks += 1
            same_basis_repeat_checks += 1

# Unit row-scaling invariance of J for every projective basis, both outcomes, all units.
row_scale_checks=0
for B in projective:
    for u0 in units:
        for u1 in units:
            Bs=scale_row(B,u0,u1)
            Bsi=inv2(Bs)
            for P in (P0,P1):
                J=mm(mm(inv2(B),P),B)
                Js=mm(mm(Bsi,P),Bs)
                assert J==Js
                row_scale_checks += 1

# Symbolic support theorem for F on 2 propositional variables.
# A Boolean formula modulo equivalence is represented by a 4-bit truth table mask.
# q in F tensor A is tuple (f0,f1,f2,f3) of four formula truth masks.
support_checks=0
for fs in product(range(16), repeat=4):
    support_mask = fs[0] | fs[1] | fs[2] | fs[3]
    for v in range(4):
        qv=0
        for k,f in enumerate(fs):
            if (f>>v)&1: qv |= 1<<k
        assert (((support_mask>>v)&1)==1) == (qv!=0)
        support_checks += 1

# Direct homomorphism obstruction: Boolean generator image must be idempotent.
# In this local chain ring only 0 and 1 are idempotent.
assert idempotents == [0,1]

# Support map is not an additive or multiplicative homomorphism.
def supp(a): return int(a!=0)
add_counterexample=(2,4,add(2,4),supp(add(2,4)),supp(2)^supp(4),supp(2)|supp(4))
mul_counterexample=(2,8,mul(2,8),supp(mul(2,8)),supp(2)&supp(8))
assert add_counterexample[3] != add_counterexample[4] # not F2-additive
assert mul_counterexample[3] != mul_counterexample[4] # not multiplicative to Boolean support

# Tensor closure failure for nonzero-state policy; unimodular tensor closure and update failure example.
psi=(2,0)     # (u,0), nonzero
phi=(8,0)     # (u^3,0), nonzero
tensor=[mul(x,y) for x in psi for y in phi]
assert tensor == [0,0,0,0]
# Bipartite coefficient matrix diag(1,u) is unimodular as a 4-vector; computational effect e=(0,1)
M=(1,0,0,2)
conditional=(M[2],M[3])
assert conditional==(0,2) and all((x&1)==0 for x in conditional)

out={
    'ring_order':16,
    'units':units,
    'idempotents':idempotents,
    'GL2_count':len(gl),
    'unordered_projective_basis_count':len(projective),
    'basis_projector_idempotence_checks':update_checks,
    'branch_nonzero_iff_effect_nonzero_checks':branch_equiv_checks,
    'same_basis_repeatability_checks':same_basis_repeat_checks,
    'row_unit_scaling_invariance_checks':row_scale_checks,
    'symbolic_support_fiber_checks':support_checks,
    'support_add_counterexample':add_counterexample,
    'support_mul_counterexample':mul_counterexample,
    'nonzero_tensor_zero_example':{'psi':psi,'phi':phi,'tensor':tensor},
    'unimodular_bipartite_conditional_nonunimodular_example':{'M':M,'effect':(0,1),'conditional':conditional}
}
print(json.dumps(out,indent=2))
