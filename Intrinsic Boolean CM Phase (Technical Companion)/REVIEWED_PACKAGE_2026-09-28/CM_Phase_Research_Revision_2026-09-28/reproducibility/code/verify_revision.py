#!/usr/bin/env python3
"""Independent finite checks for the 2026-09-28 CM phase revision.
Standard library only. Does not import or call the inherited verifier.
Binary matrices are tuples of column images, encoded as integers.
All arithmetic is exact; finite checks supplement, not replace, proofs.
"""
from __future__ import annotations
import hashlib, itertools, json, math, pathlib, platform, time
from collections import Counter


def apply(cols: tuple[int, ...], x: int) -> int:
    y = 0
    while x:
        low = x & -x
        y ^= cols[low.bit_length()-1]
        x ^= low
    return y


def compose(a, b):
    return tuple(apply(a, v) for v in b)


def rank(vectors) -> int:
    pivots = {}
    for x in vectors:
        while x:
            p = x.bit_length()-1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return len(pivots)


def cyclic_product(a: int, b: int) -> int:
    out = 0
    for i in range(4):
        if (a >> i) & 1:
            out ^= ((b << i) | (b >> (4-i))) & 15
    return out


M = [[cyclic_product(a,b) for b in range(16)] for a in range(16)]


def conjugate(a):
    return (a & 5) | ((a & 2) << 2) | ((a & 8) >> 2)


def rmul(a,b):
    x,y,z,w = a; p,q,r,s = b
    return (M[x][p]^M[y][r], M[x][q]^M[y][s],
            M[z][p]^M[w][r], M[z][q]^M[w][s])


def adj(a):
    x,y,z,w = a
    return tuple(map(conjugate, (x,z,y,w)))


def subspaces(m: int):
    """Each subspace exactly once via its unique reduced row echelon basis."""
    for k in range(m+1):
        for pivots in itertools.combinations(range(m),k):
            nonp = set(range(m))-set(pivots)
            slots = [(i,j) for i,p in enumerate(pivots) for j in sorted(nonp) if j>p]
            for mask in range(1 << len(slots)):
                rows = [1 << p for p in pivots]
                for bit,(i,j) in enumerate(slots):
                    if (mask >> bit) & 1:
                        rows[i] |= 1 << j
                yield rows


def span(rows):
    words = [0]
    for v in rows:
        words += [w ^ v for w in words]
    return words


def detector_weights(N: int, tau: int, constancy=False):
    # Find a basis of the ideal tau A, together with coefficient lifts.
    images, lifts = [], []
    for v in range(16):
        image = M[tau][v]
        if rank(images+[image]) > len(images):
            images.append(image); lifts.append(v)
    r = len(images)
    checks = N-1 if constancy else N//2
    if not constancy and N % 4 == 2:
        return [[lifts[0]]*N], r
    weights = [[0]*N for _ in range((checks+r-1)//r)]
    for i in range(checks):
        j,s = divmod(i,r)
        weights[j][0] ^= lifts[s]
        weights[j][i+1] ^= lifts[s]
    return weights, r


def output(weights, f, tau):
    out=[]
    for row in weights:
        v=0
        for i,w in enumerate(row):
            v ^= M[w][1 ^ (tau if (f >> i)&1 else 0)]
        out.append(v)
    return out


def main():
    start=time.perf_counter()
    report={'date':'2026-09-28','python':platform.python_version(),
            'method':'New standard-library implementation; no inherited-code imports',
            'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
    I=(1,2,4,8); R=(2,4,8,1); Delta=(5,10,5,10)
    K={0,5,10,15}
    counts=Counter()
    for G in itertools.product(range(16), repeat=4):
        inv=rank(G)==4
        commute=compose(G,R)==compose(R,G)
        preserve=all(apply(G,k) in K for k in K)
        sandwich_zero=all(v==0 for v in compose(Delta,compose(G,Delta)))
        assert preserve==sandwich_zero, ('gate boundary',G)
        counts['binary_matrices']+=1
        counts['invertible']+=inv
        counts['centralizer']+=commute
        counts['centralizer_invertible']+=commute and inv
        counts['ideal_preservers']+=preserve
        counts['ideal_preservers_invertible']+=preserve and inv
    assert dict(counts)=={'binary_matrices':65536,'invertible':20160,'centralizer':16,
                         'centralizer_invertible':8,'ideal_preservers':4096,
                         'ideal_preservers_invertible':576}, counts
    G=(1,4,2,8) # swap t and t^2
    witness=apply(compose(Delta,compose(G,Delta)),1)
    assert witness==15
    counts['coordinate_permutations_preserving_ideal']=sum(
        all(apply(g,k) in K for k in K) for g in itertools.permutations(I))
    counts['coordinate_permutations_commuting_with_rotation']=sum(
        compose(g,R)==compose(R,g) for g in itertools.permutations(I))
    report['star_free_gate_boundary']={**counts,'Delta_G_Delta_e0':witness}
    print('PASS: all 65536 binary gate boundaries',flush=True)

    units=[a for a in range(16) if a.bit_count()%2]
    expected=set(); forms={}; by_form=Counter()
    for a,d,k,e in itertools.product(units,units,sorted(K),range(2)):
        U=(a,M[a][k],M[d][k],d)
        if e: U=(U[1],U[0],U[3],U[2])
        assert U not in forms
        forms[U]=(a,d,k,e)
        assert rmul(adj(U),U)==(1,0,0,1)
        invtest=rmul(U,U)==(1,0,0,1)
        analytic=(M[a][d]==1) if e else (M[a][a]==1 and M[d][d]==1)
        assert invtest==analytic
        if invtest:
            by_form['swap' if e else 'no_swap']+=1
    for U in itertools.product(range(16),repeat=4):
        if rmul(adj(U),U)==(1,0,0,1): expected.add(U)
    assert set(forms)==expected and len(expected)==512
    invol=sum(rmul(U,U)==(1,0,0,1) for U in expected)
    mono=sum(k==0 for a,d,k,e in forms.values())
    mixinv=sum(k!=0 and rmul(U,U)==(1,0,0,1) for U,(a,d,k,e) in forms.items())
    assert (invol,mono,mixinv)==(96,128,72)
    report['unitary_normal_form']={'operators_examined':65536,'unitaries':512,
        'unique_normal_forms':512,'monomial':mono,'involutions':invol,
        'nonmonomial_involutions':mixinv,'involution_form_counts':dict(by_form)}
    print('PASS: complete unitary normal form and analytic involution conditions',flush=True)

    code_records=[]
    for N in (2,4,8):
        allones=(1<<N)-1; total=0; maxdim=0; admissible=Counter()
        for rows in subspaces(N-1):
            total+=1
            words=span(rows)
            # A complementary section with last coordinate zero parametrizes C/<1>.
            good=not any(w.bit_count()==N//2 or (w^allones).bit_count()==N//2 for w in words)
            if good:
                d=len(rows)+1
                assert d<=N//2
                maxdim=max(maxdim,d); admissible[d]+=1
        assert maxdim==N//2
        code_records.append({'N':N,'subspaces_containing_ones':total,
                             'max_balanced_avoiding_dimension':maxdim,
                             'admissible_by_dimension':dict(sorted(admissible.items()))})
    report['forbidden_weight_subspaces']=code_records
    print('PASS: exhaustive subspaces containing all-ones at lengths 2, 4, 8',flush=True)

    det_records=[]
    for N in (2,4,6,8,10,12,14,16):
        for tau in (3,5,15): # u, u^2, u^3 in cyclic coordinates
            w,r=detector_weights(N,tau)
            wc,_=detector_weights(N,tau,True)
            promised=0; full=0
            assert len(w)==(1 if N % 4 == 2 else math.ceil(N/(2*r)))
            for f in range(1<<N):
                constant=f in (0,(1<<N)-1)
                if constant or f.bit_count()==N//2:
                    v=output(w,f,tau)
                    assert (not any(v))==constant,(N,tau,f,v)
                    promised+=1
                v=output(wc,f,tau)
                assert (not any(v))==constant,(N,tau,'constancy',f,v)
                full+=1
            det_records.append({'N':N,'tau_code':tau,'ideal_binary_dimension':r,
                'optimal_promised_channels':len(w),'optimal_constancy_channels':len(wc),
                'promised_inputs_checked':promised,'all_constancy_inputs_checked':full,
                'promised_weights':w})
    report['detector_constructions']=det_records
    report['detector_totals']={'promise_checks':sum(x['promised_inputs_checked'] for x in det_records),
                              'constancy_checks':sum(x['all_constancy_inputs_checked'] for x in det_records)}
    print('PASS: detector constructions at all even lengths 2 through 16, three ideals',flush=True)

    # Elementary-symmetric polynomial parity identity used in the alternative proof.
    q_tests=0
    for n in range(1,11):
        N=1<<n; L=N//2
        for wgt in range(N+1):
            q=(math.comb(wgt,L) if wgt>=L else 0) ^ (math.comb(N-wgt,L) if N-wgt>=L else 0)
            assert (q&1)==(wgt not in (0,L,N))
            q_tests+=1
    report['polynomial_proof_weight_checks']=q_tests

    # Independently rebuild the supplied balanced-A tensor analyzer rank table.
    ranks=[]
    for n in range(1,7):
        N=1<<n; cols=[]
        for j in range(N):
            for b in range(4):
                col=0
                for i in range(N):
                    entry=4 if ((i&j).bit_count()&1) else 1
                    col |= M[entry][1<<b] << (4*i)
                cols.append(col)
        got=rank(cols)
        assert got==4+2*n
        ranks.append({'n':n,'binary_dimension':4*N,'binary_rank':got})
    report['companion_phase_table_independent_check']=ranks
    # A nonzero literal tensor becomes zero only after multiplication/balancing.
    literal=sum(1<<(4*i+j) for i in (0,2) for j in (0,2))
    assert literal!=0 and M[5][5]==0
    report['tensor_boundary']={'delta_tensor_delta_binary_code':literal,'product_delta_squared':0}
    report['elapsed_seconds']=round(time.perf_counter()-start,3)
    report['status']='PASS'
    out=pathlib.Path(__file__).resolve().parents[1]/'data'/'revision_verification.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':report['elapsed_seconds'],
                      'detector_totals':report['detector_totals'],
                      'subspaces':code_records},indent=2))

if __name__=='__main__':
    main()
