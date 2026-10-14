#!/usr/bin/env python3
"""Independent targeted ablations and small Simon tests. Requires sympy for
an exact rational probability certificate; all other tests use standard Python.
"""
import laboratory as L
from laboratory import *
import sympy as sp

def load_inventory():
    d=json.loads((DATA/'independent_gate_and_ray_sets.json').read_text())
    L.GATES[:]=[tuple(g) for g in d['gates_u']]
    L.BASES[:]=[tuple(tuple(r) for r in b) for b in d['bases_u']]
    L.RAYS[:]=[tuple(r) for r in d['rays_u']]

def orthogonal_ablation():
    # IMPORTANT: standard transpose refers to the cyclic R-coordinate basis,
    # not the polynomial u-coordinate basis used elsewhere in the package.
    T=transpose((1,3,5,15));TI=inverse(T)
    def rop(a):return compose(compose(T,REG[a]),TI)
    OP=[rop(a) for a in range(16)]
    def full(g):return tuple(OP[g[2*i]][k]|(OP[g[2*i+1]][k]<<4) for i in range(2) for k in range(4))
    orth=[g for g in L.GATES if compose(full(g),transpose(full(g)))==eye(8)]
    ob=sorted({tuple(sorted((canon_ray(g[:2]),canon_ray(g[2:])))) for g in orth})
    assert len(orth)==512 and len(ob)==4
    rows=[]
    for a in range(4):
        for b in range(a,5):
            p=1<<a;q=0 if b==4 else 1<<b
            def value(r,t):return MUL[MUL[r[0]][p]][t[0]]^MUL[MUL[r[1]][q]][t[1]]
            tables=[tuple(int(bool(value(r,t))) for r,t in product(B,C)) for B,C in product(ob,repeat=2)]
            assignments=[];covered=[0]*16
            for s in product(range(2),repeat=8):
                if all(tables[4*i+j][2*s[i]+s[4+j]] for i,j in product(range(4),repeat=2)):
                    assignments.append(s)
                    for i,j in product(range(4),repeat=2):covered[4*i+j]|=1<<(2*s[i]+s[4+j])
            uncovered=sum(v and not ((covered[c]>>i)&1) for c,t in enumerate(tables) for i,v in enumerate(t))
            rows.append({'a':a,'b':b,'orthogonal_gates':512,'projective_measurements':4,'contexts':16,'assignments_tested':256,'global_assignments':len(assignments),'uncovered':uncovered,'classification':'strong' if not assignments else 'logical_not_strong' if uncovered else 'local'})
    csvsave('independent_orthogonal_ablation.csv',rows)
    # Phase alternating/quadratic forms checked for the entire GL4(F2).
    R=OP[3];J=OP[5]
    assert all(not (J[i]>>i)&1 for i in range(4))
    def Q(v):return (((v>>0)&1)&((v>>2)&1))^(((v>>1)&1)&((v>>3)&1))
    spcount=qcount=ocount=0;ovecs=[]
    for packed in range(65536):
        g=unflatten(packed,4)
        if rank(g)<4:continue
        if compose(compose(transpose(g),J),g)==J:spcount+=1
        if all(Q(apply(g,v))==Q(v) for v in range(16)):qcount+=1
        if compose(transpose(g),g)==eye(4):ocount+=1;ovecs.append(flatten(g))
    assert (spcount,qcount,ocount,rank(ovecs))==(720,72,48,10)
    # W and D have no invariant nondegenerate bilinear form (proof in report).
    save('independent_forms.json',{'rotation_basis_change_T':T,'J_rows':J,'Sp4_order':spcount,'split_quadratic_group_order':qcount,'O4_order':ocount,'O4_linear_span_dimension':rank(ovecs),'orthogonal_projective_bases_A2':ob})
    return {'A_gates_scanned':24576,'O8_intersection_A_linear':512,'measurement_bases':4,'canonical_nonzero_resource_representatives':14,'assignments_per_representative':256,'all_binary_4x4_matrices_scanned':65536,'output':'independent_orthogonal_ablation.csv; independent_forms.json'}

def simon_small():
    # n=2 standard oracle, four address values and four output values.
    # For each nonzero shift, enumerate all 12 injective labelings of its two cosets.
    N=4;classes=[];cosets=[]
    for s in (1,2,3):
        pairs=[];seen=set()
        for x in range(N):
            if x not in seen:
                pair=(x,x^s);pairs.append(pair);seen.update(pair)
        fs=[]
        for a,b in product(range(N),repeat=2):
            if a==b:continue
            f=[0]*N
            for x in pairs[0]:f[x]=a
            for x in pairs[1]:f[x]=b
            fs.append(f)
        classes.append(fs);cosets.append([sum(1<<x for x in pair) for pair in pairs])
    lookups=[]
    for fs in classes:
        cl=[]
        for f in fs:
            columns=[1<<((i%4)+4*((i//4)^f[i%4])) for i in range(16)]
            low=[xors(columns[i] for i in range(8) if (v>>i)&1) for v in range(256)]
            high=[xors(columns[i+8] for i in range(8) if (v>>i)&1) for v in range(256)]
            cl.append((low,high))
        lookups.append(cl)
    successes=[];span_hist=Counter()
    for v in range(1,65536):
        vs=[[lo[v&255]^hi[v>>8] for lo,hi in cl] for cl in lookups]
        dims=list(map(rank,vs));joint=rank(vs[0]+vs[1]+vs[2]);span_hist[str((tuple(dims),joint))]+=1
        if sum(dims)==joint:successes.append(v)
    assert not successes
    # Standard coset states already have a common nonzero vector in all class spans.
    assert all(rank(C)==2 and xors(C)==15 for C in cosets)
    save('small_simon.json',{'n':2,'register_dimension':16,'oracles_by_hidden_shift':classes,'all_nonzero_preparations':65535,'one_query_perfect_preparations':successes,'span_histogram':dict(span_hist),'coset_states_by_shift':cosets,'common_coset_span_vector':15,'scope':'no spectator ancilla; arbitrary F2-linear preparation and final complete linear readout; NOT a general many-query lower bound'})
    return {'n':2,'state_dimension':16,'nonzero_preparations':65535,'valid_standard_oracles':36,'hidden_shifts':3,'one_query_successes':0,'algorithm':'span direct-sum discrimination criterion; all preparations and oracle labelings','output':'small_simon.json'}

def probability_certificate():
    bases=((1,2),(3,1),(2,3));allowed=[parity(r&t) for B,C in product(bases,repeat=2) for r,t in product(B,C)]
    rows=[];rhs=[]
    def add(d,b=0):rows.append([d.get(i,0) for i in range(36)]);rhs.append(b)
    for i,v in enumerate(allowed):
        if not v:add({i:1})
    for c in range(9):add({4*c+k:1 for k in range(4)},1)
    for a,out in product(range(3),range(2)):
        for b in (1,2):
            add({**{4*(3*a+b)+2*out+j:1 for j in range(2)},**{4*(3*a)+2*out+j:-1 for j in range(2)}})
    for b,out in product(range(3),range(2)):
        for a in (1,2):
            add({**{4*(3*a+b)+2*j+out:1 for j in range(2)},**{4*b+2*j+out:-1 for j in range(2)}})
    A=sp.Matrix(rows);B=sp.Matrix(rhs);pairs=((4,27),(11,12),(19,32));certs=[]
    for i,j in pairs:
        target=sp.zeros(36,1);target[i]=1;target[j]=1
        sol=next(iter(sp.linsolve((A.T,target))))
        params=set().union(*(e.free_symbols for e in sol));y=sp.Matrix([e.subs({p:0 for p in params}) for e in sol])
        assert y.T*A==target.T and (y.T*B)[0]==0
        certs.append({'pair':[i,j],'linear_constraint_weights':[str(x) for x in y]})
    A2=A;B2=B
    forced=[i for pair in pairs for i in pair]
    for i in forced:
        e=sp.zeros(1,36);e[i]=1;A2=A2.col_join(e);B2=B2.col_join(sp.zeros(1,1))
    solution=next(iter(sp.linsolve((A2,B2))))
    assert all(not x.free_symbols and x>=0 for x in solution)
    assert sum(allowed)==24 and sum(bool(x) for x in solution)==18
    correlations=[[sum((1 if i==j else -1)*solution[4*(3*a+b)+2*i+j] for i,j in product(range(2),repeat=2)) for b in range(3)] for a in range(3)]
    chsh=correlations[0][0]-correlations[0][1]-correlations[1][0]-correlations[1][1]
    assert chsh==4
    save('independent_probability_certificate.json',{'weak_completion_correlations':[[str(x) for x in row] for row in correlations],'weak_completion_CHSH_ZX':str(chsh),'support_allowed':allowed,'constraint_matrix':rows,'constraint_rhs':rhs,'nonnegative_zero_sum_pairs':certs,'six_modally_possible_but_forced_zero_events':forced,'unique_weak_nonsignalling_distribution':[str(x) for x in solution],'proof':'Each displayed pair sums to zero by exact rational linear combinations of support/normalization/no-signalling equations. Nonnegativity forces both entries zero. The augmented system has the displayed unique solution; all probabilities are 0 or 1/2.'})
    return {'contexts':9,'probability_variables':36,'modal_possible_events':24,'necessarily_zero_possible_events':6,'weak_positive_events':18,'algorithm':'exact rational linear algebra; explicit zero-sum certificates, no floating LP','output':'independent_probability_certificate.json'}

def ghz_two_setting_ablation():
    bases=((1,2),(3,1),(2,3));rows=[]
    for ca,cb,cc in product(tuple(combinations(range(3),2)),repeat=3):
        table=[tuple(parity(r&s&t) for r,s,t in product(bases[i],bases[j],bases[k])) for i,j,k in product(ca,cb,cc)]
        globals=[];covered=[0]*8
        for v in product(range(2),repeat=6):
            if all(table[4*i+2*j+k][4*v[i]+2*v[2+j]+v[4+k]] for i,j,k in product(range(2),repeat=3)):
                globals.append(v)
                for i,j,k in product(range(2),repeat=3):covered[4*i+2*j+k]|=1<<(4*v[i]+2*v[2+j]+v[4+k])
        unc=sum(x and not ((covered[c]>>o)&1) for c,t in enumerate(table) for o,x in enumerate(t))
        rows.append({'Alice':str(ca),'Bob':str(cb),'Charlie':str(cc),'contexts':8,'global_assignments':len(globals),'unextendable_events':unc})
    csvsave('ghz_two_setting_ablation.csv',rows)
    return {'GHZ_states':1,'two_setting_subscenarios':27,'contexts_each':8,'assignments_each':64,'strong_subscenarios':sum(not r['global_assignments'] for r in rows),'logical_subscenarios':sum(bool(r['unextendable_events']) for r in rows),'output':'ghz_two_setting_ablation.csv'}

def symplectic_protocol_and_normalizer():
    from itertools import permutations
    J2=(2,1);J4=kron(J2,J2)
    GL2=[unflatten(i,2) for i in range(16) if rank(unflatten(i,2))==2]
    candidates=[]
    for effects in permutations(GL2,4):
        analyzer=tuple(flatten(e) for e in effects)
        if compose(compose(analyzer,J4),transpose(analyzer))==J4:
            candidates.append((effects,analyzer))
    assert candidates
    effects,analyzer=candidates[0]
    for E in effects:
        C=inverse(transpose(E))
        assert compose(compose(transpose(C),J2),C)==J2
        assert compose(C,transpose(E))==eye(2)
    normals=[tuple(g) for g in json.loads((DATA/'new_pauli_normalizer.json').read_text())['normalizer_A_matrices']]
    bases=sorted({tuple(sorted((canon_ray(g[:2]),canon_ray(g[2:])))) for g in normals})
    # Orbit partition of all 255 nonzero raw A^2 vectors.
    remain=set(product(range(16),repeat=2));remain.remove((0,0));orbits=[]
    while remain:
        v=min(remain);orbit={avec(g,v) for g in normals};assert orbit<=remain
        remain-=orbit;orbits.append({'representative':v,'size':len(orbit)})
    save('new_symplectic_and_normalizer.json',{'symplectic_local_form':J2,'symplectic_tensor_form':J4,'complete_symplectic_teleportation_analyzers_count':len(candidates),'example_invertible_effect_matrices':effects,'example_symplectic_analyzer':analyzer,'Pauli_normalizer_projective_bases':bases,'Pauli_normalizer_nonzero_state_orbits':orbits,'scope':'symplectic alternative uses full isometry groups for the specified amplitude forms, not the native W/CNOT/R gate set and not the usual Pauli-label symplectic formalism'})
    return {'GL2_candidates':6,'ordered_analyzer_candidates':360,'valid_symplectic_analyzers':len(candidates),'Pauli_normalizer_gates':256,'Pauli_normalizer_bases':len(bases),'Pauli_normalizer_nonzero_state_orbits':len(orbits),'output':'new_symplectic_and_normalizer.json'}

def main():
    load_inventory()
    L.METRIC_FILE="ablation_metrics.json"
    for name,fn in [('orthogonal_ablation',orthogonal_ablation),('Simon_n2',simon_small),('probability',probability_certificate),('GHZ_two_settings',ghz_two_setting_ablation),('symplectic_and_normalizer',symplectic_protocol_and_normalizer)]:L.timed(name,fn)
if __name__=='__main__':main()
