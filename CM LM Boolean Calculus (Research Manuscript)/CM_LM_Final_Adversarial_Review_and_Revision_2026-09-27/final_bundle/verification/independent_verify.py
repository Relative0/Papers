#!/usr/bin/env python3
"""Independent exact checks for the CM/LM foundations audit (2026-09-26).

No manuscript implementation, external package, random sample, or floating-point
arithmetic is used. Each counted check is one explicit equality/characterization;
whole tuples and scalar comparisons are distinguished in the JSON family labels.
Truth words are written in true-first row-major order. Formula masks encode the
complete Boolean algebra on two free generators, so dependent and constant
formulas are included, not assumed independent.
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
from itertools import product, permutations
from pathlib import Path
import hashlib, json, platform, sys, time

COUNTS: Counter[str] = Counter()
def check(family: str, actual: object, expected: object, context: object = None) -> None:
    COUNTS[family] += 1
    if actual != expected:
        raise AssertionError((family, context, actual, expected))

BITS = (1, 0)
MATS = [tuple((m >> (3-i)) & 1 for i in range(4)) for m in range(16)]
I = (1,0,0,1)
P = (0,1,1,0)
def gate(m: int, x: int, y: int) -> int:
    return (m >> (2*x+y)) & 1

def term(m: int, x: int, y: int, one: int) -> int:
    nx, ny = one ^ x, one ^ y
    return ((x & y) if m & 8 else 0) ^ ((x & ny) if m & 4 else 0) ^ ((nx & y) if m & 2 else 0) ^ ((nx & ny) if m & 1 else 0)

def mul(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    return (a[0]&b[0] ^ a[1]&b[2], a[0]&b[1] ^ a[1]&b[3],
            a[2]&b[0] ^ a[3]&b[2], a[2]&b[1] ^ a[3]&b[3])

def frame(x: int, one: int=1) -> tuple[int,...]:
    return x, one^x, one^x, x

def lift(m: int, x: int, y: int, one: int=1) -> tuple[int,...]:
    return tuple(term(m,u,v,one) for u,v in product((x,one^x),(y,one^y)))

def pair(a: int, M: tuple[int,...], b: int, one: int=1) -> int:
    return a&M[0]&b ^ a&M[1]&(one^b) ^ (one^a)&M[2]&b ^ (one^a)&M[3]&(one^b)

def word(M: tuple[int,...]) -> int:
    return sum(b << (len(M)-1-i) for i,b in enumerate(M))

def bx(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    return tuple(x^y for x,y in zip(a,b))

def truth(mask: int, x: tuple[int,...]) -> int:
    index=0
    for b in x: index=2*index+b
    return (mask >> index) & 1

def lmcell(mask: int, x: tuple[int,...], alpha: tuple[int,...]) -> int:
    return truth(mask,tuple(u if a else 1-u for u,a in zip(x,alpha)))

def rank(rows: list[int], cols: int) -> int:
    a=rows[:]; k=0
    for bit in range(cols-1,-1,-1):
        pivot=next((i for i in range(k,len(a)) if (a[i]>>bit)&1),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        for j in range(len(a)):
            if j!=k and ((a[j]>>bit)&1):a[j]^=a[k]
        k+=1
    return k

def run(out: Path) -> dict:
    t0=time.perf_counter();one=15
    # Complete formula algebra on two free generators (16 elements).
    frames={x:frame(x,one) for x in range(16)}
    lifts={}
    for x in range(16):
        check('formula_frame_involution_whole_matrix',mul(frames[x],frames[x]),(one,0,0,one),x)
        for y in range(16):
            for m,C in enumerate(MATS):
                L=lift(m,x,y,one);lifts[m,x,y]=L
                const=tuple(one if b else 0 for b in C)
                check('formula_normal_form_whole_matrix',L,mul(mul(frames[x],const),frames[y]),(m,x,y))
                check('formula_inverse_whole_matrix',mul(mul(frames[x],L),frames[y]),const,(m,x,y))
                for a,b in product(range(16),repeat=2):
                    check('all_two_generator_formula_pairings_whole_formula',pair(a,L,b,one),term(m,one^a^x,one^y^b,one),(m,x,y,a,b))
    for m,C in enumerate(MATS):
        for x,y in product(BITS,repeat=2):
            check('binary_selection_scalar',pair(x,C,y),gate(m,x,y))
            check('binary_valuation_whole_matrix',lift(m,x,y),mul(mul(frame(x),C),frame(y)))
        for x,y,a,b in product(BITS,repeat=4):
            check('binary_pairing_scalar',pair(a,lift(m,x,y),b),gate(m,1^a^x,1^y^b))
    # Arbitrary binary outer operations, not only XOR or conjunction.
    for f,h,g in product(range(16),repeat=3):
        derived=tuple(gate(g,a,b) for a,b in zip(MATS[f],MATS[h])); d=word(derived)
        for x,y in product(BITS,repeat=2):
            L1,L2=lift(f,x,y),lift(h,x,y)
            check('aligned_superposition_whole_matrix',tuple(gate(g,a,b) for a,b in zip(L1,L2)),lift(d,x,y))
            for a,b in product(BITS,repeat=2):
                check('pairing_preserves_outer_operations_scalar',pair(a,lift(d,x,y),b),gate(g,pair(a,L1,b),pair(a,L2,b)))
    # Frame transformations and independent alignment, using permutation inverses.
    assignments=list(product(BITS,repeat=2)); frames_idx=[]
    for perm in permutations(range(2)):
        for eps in product(BITS,repeat=2):
            idx=[assignments.index(tuple(v[perm[i]]^eps[i] for i in range(2))) for v in assignments]
            frames_idx.append(idx)
    for f,h,g in product(range(16),repeat=3):
        expected=tuple(gate(g,a,b) for a,b in zip(MATS[f],MATS[h]))
        for p1,p2 in product(frames_idx,repeat=2):
            a=tuple(MATS[f][k] for k in p1); b=tuple(MATS[h][k] for k in p2)
            inv1=[p1.index(k) for k in range(4)]; inv2=[p2.index(k) for k in range(4)]
            got=tuple(gate(g,a[inv1[k]],b[inv2[k]]) for k in range(4))
            check('independent_signed_frame_alignment_whole_matrix',got,expected)
    for f,h in product(range(16),repeat=2):
        d=word(mul(MATS[f],MATS[h]))
        for x,y,z in product(BITS,repeat=3):
            check('matched_kernel_product_whole_matrix',mul(lift(f,x,y),lift(h,y,z)),lift(d,x,z))
    # Intrinsic image: all 65,536 formula-valued 2x2 matrices over F(P,Q).
    substitutions={}
    for mask in range(16):
        for d in product(BITS,repeat=2):
            substitutions[mask,d]=word(tuple(truth(mask,bx(x,d)) for x in assignments))
    image={lift(m,12,10,15) for m in range(16)}
    image_count=0
    for T in product(range(16),repeat=4):
        eq=True
        for di,d in enumerate(assignments):
            for j,a in enumerate(assignments):
                if substitutions[T[j],d] != T[assignments.index(bx(a,d))]:eq=False;break
            if not eq:break
        image_count+=eq
        check('polarity_image_characterization_whole_formula_tensor',eq,T in image)
    check('polarity_image_cardinality',image_count,16)
    # Selector characterization, both formula-ring and pointwise descriptions.
    partitions=[]
    for w in product(range(16),repeat=4):
        orth=all((w[i]&w[j])==0 for i in range(4) for j in range(i))
        unit=(w[0]^w[1]^w[2]^w[3])==15
        at_each_atom=all(sum((a>>k)&1 for a in w)==1 for k in range(4))
        check('selector_characterization_weight_tuple',orth and unit,at_each_atom)
        if orth and unit:partitions.append(w)
    check('selector_partition_count',len(partitions),256)
    def q(w,T):return w[0]&T[0]^w[1]&T[1]^w[2]&T[2]^w[3]&T[3]
    test_tensors=[(12,10,8,3),(15,0,6,9),(1,2,4,8),(0,0,0,0),(15,15,15,15)]
    for w in partitions:
        for T,U in product(test_tensors,repeat=2):
            for g in range(16):
                check('selector_outer_operations_selected_tensors_whole_formula',q(w,tuple(term(g,a,b,15) for a,b in zip(T,U))),term(g,q(w,T),q(w,U),15))
    # Every ternary function and all reference/selector assignments.
    a3=list(product(BITS,repeat=3)); frames3=list(product(list(permutations(range(3))),a3))
    for f in range(256):
        for x in a3:
            delta=tuple(1-u for u in x)
            for a in a3:
                check('ternary_valuation_scalar',lmcell(f,x,a),truth(f,bx(a,delta)))
            for selector in a3:
                value=0
                for a in a3:
                    weight=int(all(s==p for s,p in zip(selector,a)))
                    value^=weight&lmcell(f,x,a)
                check('ternary_pairing_scalar',value,truth(f,tuple(1^u^v for u,v in zip(selector,x))))
        for perm,eps in frames3:
            def phi(v):return tuple(v[perm[i]]^eps[i] for i in range(3))
            transformed=word(tuple(truth(f,phi(v)) for v in a3))
            for a in a3:
                check('ternary_signed_numeric_action_scalar',truth(transformed,a),truth(f,phi(a)))
            for x in a3:
                lhs=tuple(lmcell(transformed,x,a) for a in a3)
                sx=tuple(x[perm[i]] for i in range(3))
                rhs=tuple(lmcell(f,sx,phi(a)) for a in a3)
                check('explicit_symbolic_signed_transport_whole_tensor',lhs,rhs)
        for perm in permutations(range(3)):
            for p in (1,2):
                R,C=perm[:p],perm[p:]
                for x in a3:
                    rr=tuple(x[i] for i in R);cc=tuple(x[i] for i in C)
                    assembled=[None]*3
                    for i,b in zip(R,rr):assembled[i]=b
                    for i,b in zip(C,cc):assembled[i]=b
                    check('ordered_rectangular_selection_scalar',truth(f,tuple(assembled)),truth(f,x))
    # All 4-variable block lifts built from two binary inner functions.
    for f,h,g in product(range(16),repeat=3):
        block=tuple(gate(g,a,b) for a in MATS[f] for b in MATS[h])
        for i,(w,x) in enumerate(assignments):
            for j,(y,z) in enumerate(assignments):
                check('four_variable_block_lift_scalar',block[4*i+j],gate(g,gate(f,w,x),gate(h,y,z)))
    # Independent shortest-XOR decomposition by breadth-first search, not rank.
    rankone={((v if u&2 else 0)<<4)|(v if u&1 else 0) for u in range(1,4) for v in range(1,16)}
    distance={0:0};queue=deque([0])
    while queue:
        a=queue.popleft()
        for b in rankone:
            z=a^b
            if z not in distance:distance[z]=distance[a]+1;queue.append(z)
    rankhist=Counter()
    for m in range(256):
        rk=rank([m>>4,m&15],4);rankhist[rk]+=1
        check('2x4_minimum_xor_decomposition_equals_rank',distance[m],rk,m)
        check('2x4_conjunctive_separability',m==0 or m in rankone,rk<=1,m)
    # ANF via fast subset transform: all functions through arity four.
    for n in range(1,5):
        for f in range(1<<(1<<n)):
            coef=[(f>>i)&1 for i in range(1<<n)]
            for k in range(n):
                for i in range(1<<n):
                    if i&(1<<k):coef[i]^=coef[i^(1<<k)]
            check('anf_top_parity_through_arity_four_scalar',coef[-1],f.bit_count()%2)
    # Complete 16-CM field-linear spectral atlas.
    atlas=[]
    for m,A in enumerate(MATS):
        tr=A[0]^A[3];det=A[0]&A[3]^A[1]&A[2]
        A2=mul(A,A)
        ch=tuple(a^((tr&b))^(det&i) for a,b,i in zip(A2,A,I))
        check('cayley_hamilton_whole_matrix',ch,(0,0,0,0),m)
        eigen={}
        for lam in (0,1):
            eigen[str(lam)]=[list(v) for v in ((0,1),(1,0),(1,1)) if (A[0]&v[0]^A[1]&v[1],A[2]&v[0]^A[3]&v[1])==tuple(lam&b for b in v)]
        minimal=([0,1] if m==0 else [1,1] if A==I else [det,tr,1])
        powers=[];state=I
        while state not in powers:
            powers.append(state);state=mul(state,A)
        atlas.append({'truth_word':format(m,'04b'),'matrix':[list(A[:2]),list(A[2:])],
                      'rank':rank([(A[0]<<1)|A[1],(A[2]<<1)|A[3]],2),
                      'characteristic_coefficients_low_to_high':[det,tr,1],
                      'minimal_coefficients_low_to_high':minimal,'eigenvectors_nonzero':eigen,
                      'idempotent':A2==A,'symmetric':A[1]==A[2],
                      'power_preperiod':powers.index(state),'power_period':len(powers)-powers.index(state)})
        rotated=(A[2],A[0],A[3],A[1])
        for x,y in assignments:
            check('clockwise_rotation_scalar',gate(word(rotated),x,y),gate(m,1-y,x))
    check('idempotent_count',sum(a['idempotent'] for a in atlas),8)
    check('symmetric_idempotent_count',sum(a['idempotent'] and a['symmetric'] for a in atlas),4)
    # Expected counterexamples: not failures of the qualified manuscript.
    counterexamples={
      'missing_joint_true_valuation':{'references':['P','not P'],'possible_pairs':[[1,0],[0,1]],'inverse_normal_form_still_valid':True},
      'unaligned_implication_xor':{'naive_word':'0000','aligned_word':'0110'},
      'output_complement_not_unchanged_xor':{'inputs':[0,0],'complement_of_xor':1,'xor_of_complements':0},
      'unmatched_intermediate':{'C':'1001','D':'1001','X':1,'Y':1,'W':0,'Z':1,'actual_product':list(mul(lift(9,1,1),lift(9,0,1))),'wrong_matched_prediction':list(lift(9,1,1))},
      'simultaneous_polarity_in_both_indices_and_references':{'arity':1,'f':'identity','X':1,'alpha':1,'epsilon':1,'wanted':0,'double_flip':1},
      'general_xor_vs_or_product':{'left':[1,1],'right':[1,1],'xor_and':0,'or_and':1},
      'selector_requires_partition':{'weights':[1,1],'unit_image':0,'expected_for_unital':1},
      'raw_or_has_no_F2_eigenvalue':{'matrix':[[1,1],[1,0]],'characteristic':'lambda^2+lambda+1'},
      'matrix_multiplication_not_pointwise_and':{'matrix_word':'0110','matrix_square_word':'1001','entrywise_and_self_word':'0110'}
    }
    result={'status':'PASS','date':'2026-09-26','python':sys.version,'platform':platform.platform(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'assertion_count':sum(COUNTS.values()),'families':dict(COUNTS),
            'seconds':round(time.perf_counter()-t0,3),'2x4_rank_histogram':dict(rankhist),
            'historical_20873_reproduced':False,
            'historical_20873_status':'Original checker not found in supplied artifacts. These are new independently specified checks, not its reconstruction.',
            'scope_limits':'Finite checks complement, not replace, arbitrary-arity proofs; no performance or novelty claim.'}
    out.mkdir(parents=True,exist_ok=True)
    (out/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'compact_cm_atlas.json').write_text(json.dumps(atlas,indent=2)+'\n')
    (out/'boundary_counterexamples.json').write_text(json.dumps(counterexamples,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    run(parser.parse_args().output)
