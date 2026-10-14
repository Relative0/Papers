#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import time
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from native_block import *

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOGS = ROOT / "logs"
DATA.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)


def write_json(name, obj):
    (DATA / name).write_text(json.dumps(obj, indent=2) + "\n")


def write_csv(name, rows):
    rows = list(rows)
    if not rows:
        return
    with (DATA / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def basis_selectors(basis):
    vals=[]
    for effect in basis:
        vals.append(tuple(selector_from_operator(B) for B in effect_blocks(effect,2)))
    return tuple(vals)


def fast_support_table_diag(a: int, b: int, basis_a, basis_b):
    va=apply(N_POWERS[a],E0_VEC)
    vb=apply(N_POWERS[b],E0_VEC)
    out=[]
    for e in basis_a:
        eb=effect_blocks(e,2)
        for f in basis_b:
            fb=effect_blocks(f,2)
            x=apply(eb[0], apply(fb[0],va)) ^ apply(eb[1], apply(fb[1],vb))
            out.append(int(x!=0))
    return tuple(out)


def two_sat_coverage_from_tables(tables, n):
    Nvars=2*n
    adj=[[] for _ in range(2*Nvars)]
    clauses=[]
    def node(v,val): return 2*v+val
    def neg(x): return x^1
    def add_clause(v1,val1,v2,val2):
        clauses.append((v1,val1,v2,val2))
        adj[node(v1,1-val1)].append(node(v2,val2))
        adj[node(v2,1-val2)].append(node(v1,val1))
    for (i,j),t in tables.items():
        for a in (0,1):
            for b in (0,1):
                if not t[2*a+b]: add_clause(i,1-a,n+j,1-b)
    idx=0; stack=[]; on=[False]*(2*Nvars); ids=[-1]*(2*Nvars); low=[0]*(2*Nvars); comp=[-1]*(2*Nvars); cc=0
    import sys; sys.setrecursionlimit(max(10000,4*Nvars+100))
    def dfs(v):
        nonlocal idx,cc
        ids[v]=low[v]=idx; idx+=1; stack.append(v); on[v]=True
        for w in adj[v]:
            if ids[w]<0:
                dfs(w); low[v]=min(low[v],low[w])
            elif on[w]: low[v]=min(low[v],ids[w])
        if low[v]==ids[v]:
            while True:
                w=stack.pop(); on[w]=False; comp[w]=cc
                if w==v: break
            cc+=1
    for v in range(2*Nvars):
        if ids[v]<0: dfs(v)
    possible=sum(sum(t) for t in tables.values())
    sat=not any(comp[2*v]==comp[2*v+1] for v in range(Nvars))
    if not sat:
        return {"satisfiable":False,"clauses":len(clauses),"possible_sections":possible,
                "extendable_possible_sections":0,"uncovered_possible_sections":possible,"first_uncovered":None}
    reachable=[]
    for start in range(2*Nvars):
        seen=1<<start; st=[start]
        while st:
            v=st.pop()
            for w in adj[v]:
                bit=1<<w
                if not seen&bit:
                    seen|=bit; st.append(w)
        reachable.append(seen)
    def reaches(x,y): return bool(reachable[x]&(1<<y))
    extendable=0; uncovered=[]
    for (i,j),t in tables.items():
        for a in (0,1):
            for b in (0,1):
                if not t[2*a+b]: continue
                l=node(i,a); m=node(n+j,b)
                bad=(reaches(l,neg(l)) or reaches(m,neg(m)) or reaches(l,neg(m)) or reaches(m,neg(l)))
                if bad: uncovered.append((i,j,a,b))
                else: extendable+=1
    return {"satisfiable":True,"clauses":len(clauses),"possible_sections":possible,
            "extendable_possible_sections":extendable,"uncovered_possible_sections":len(uncovered),
            "first_uncovered":None if not uncovered else uncovered[0]}


def ghz_analysis_native(state32, bases=MQT_BASES, names=MQT_NAMES):
    n=len(bases); contexts=[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                t=support_table3(state32,bases[i],bases[j],bases[k])
                contexts.append((i,j,k,t))
    assignments=list(product((0,1),repeat=3*n))
    good=[q for q in assignments if all(t[4*q[i]+2*q[n+j]+q[2*n+k]] for i,j,k,t in contexts)]
    uncovered=[]
    for i,j,k,t in contexts:
        for idx,possible in enumerate(t):
            if not possible: continue
            o=(idx>>2,(idx>>1)&1,idx&1)
            if not any(q[i]==o[0] and q[n+j]==o[1] and q[2*n+k]==o[2] for q in good):
                uncovered.append((i,j,k,o))
    min_unsat=None
    if not good:
        masks=[]; full=(1<<len(assignments))-1
        for i,j,k,t in contexts:
            mask=0
            for qi,q in enumerate(assignments):
                if t[4*q[i]+2*q[n+j]+q[2*n+k]]: mask|=1<<qi
            masks.append(mask)
        for r in range(1,7):
            found=None
            for comb in combinations(range(len(contexts)),r):
                m=full
                for x in comb: m &= masks[x]
                if not m:
                    found=comb; break
            if found is not None:
                min_unsat=[{"A":names[contexts[x][0]],"B":names[contexts[x][1]],"C":names[contexts[x][2]],"table":contexts[x][3]} for x in found]
                break
    rows=[]
    for i,j,k,t in contexts:
        for idx,possible in enumerate(t):
            rows.append({"A":names[i],"B":names[j],"C":names[k],"outA":idx>>2,"outB":(idx>>1)&1,"outC":idx&1,"possible":possible})
    return {"global_assignments":len(good),"uncovered_possible_sections":len(uncovered),
            "minimum_unsat_context_count":None if min_unsat is None else len(min_unsat),"minimum_unsat_contexts":min_unsat},rows


def ghz_coverage_small(state32,bases):
    n=len(bases); contexts=[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                contexts.append((i,j,k,support_table3(state32,bases[i],bases[j],bases[k])))
    good=[]
    for q in product((0,1),repeat=3*n):
        if all(t[4*q[i]+2*q[n+j]+q[2*n+k]] for i,j,k,t in contexts): good.append(q)
    uncovered=[]
    for i,j,k,t in contexts:
        for idx,p in enumerate(t):
            if not p: continue
            o=(idx>>2,(idx>>1)&1,idx&1)
            if not any(q[i]==o[0] and q[n+j]==o[1] and q[2*n+k]==o[2] for q in good): uncovered.append((i,j,k,o))
    return len(good),len(uncovered)


def main():
    t0=time.time()
    summary={}

    # 1) Native phase algebra and exact centralizer result.
    centralizer=[]
    for raw in range(1<<16):
        A=tuple((raw>>(4*i))&0xF for i in range(4))
        if compose(A,P)==compose(P,A): centralizer.append(A)
    phase_set=set(PHASE_OPS)
    assert set(centralizer)==phase_set
    summary["phase_algebra"]={
        "P4_is_identity":power(P,4)==I4,
        "P_transpose_is_P3":transpose(P,4)==P3,
        "KPK_is_P3":compose(compose(K,P),K)==P3,
        "N4_is_zero":N4==Z4,
        "N_ranks":[rank(X,4) for X in N_POWERS],
        "generated_operator_count":len(PHASE_OPS),
        "invertible_phase_operator_count":len(UNIT_SELECTORS),
        "centralizer_of_P_count":len(centralizer),
        "centralizer_equals_generated_algebra":set(centralizer)==phase_set,
    }
    write_json("phase_algebra_native.json",{
        **summary["phase_algebra"],
        "P":rows_to_lists(P,4),"K":rows_to_lists(K,4),"N":rows_to_lists(N,4),
        "N2":rows_to_lists(N2,4),"N3":rows_to_lists(N3,4),
        "unit_selectors":UNIT_SELECTORS,
    })

    # 2) Gate and measurement-basis inventory entirely as 8x8 block matrices.
    gate_rows, inv_gates, orth_gates = enumerate_phase_block_gates()
    bases=measurement_bases(inv_gates); unitary_bases=unitary_measurement_bases(orth_gates)
    assert len(inv_gates)==24576 and len(orth_gates)==512 and len(bases)==192 and len(unitary_bases)==4
    summary["gate_inventory"]={"all":65536,"invertible_8x8_block_gates":len(inv_gates),
                               "orthogonal_8x8_block_gates":len(orth_gates),"projective_reversible_bases":len(bases),
                               "projective_orthogonal_bases":len(unitary_bases)}
    base_rows=[]
    for i,b in enumerate(bases):
        s=basis_selectors(b)
        base_rows.append({"basis_id":i,"out0_left":s[0][0],"out0_right":s[0][1],"out1_left":s[1][0],"out1_right":s[1][1]})
    write_csv("measurement_bases_native_192.csv",base_rows)

    # 3) Bell support contradiction in embedded Boolean bases.
    bell=bell_support_state(); delta=bell_delta_state()
    bell_rows=[]; bell_tables={}
    for i,A in enumerate(MQT_BASES):
        for j,B in enumerate(MQT_BASES):
            t=support_table2(bell,A,B); bell_tables[MQT_NAMES[i]+MQT_NAMES[j]]=t
            for idx,p in enumerate(t):
                bell_rows.append({"alice_setting":MQT_NAMES[i],"bob_setting":MQT_NAMES[j],"alice_outcome":idx//2,"bob_outcome":idx%2,"possible":p})
    bell_globals=compatible_bell_globals(bell,MQT_BASES)
    assert len(bell_globals)==0
    write_csv("bell_native_mqt_tables.csv",bell_rows)
    summary["bell"]={"tables":{k:list(v) for k,v in bell_tables.items()},"compatible_global_assignments":0,
                     "explicit_contradiction":"ZZ fixes common z; XY fixes bY=x; YX fixes bX=y; ZX/XZ/YY forbid 11 and ZY/XX/YZ forbid 00, forcing three pairwise-unequal Boolean values."}

    # 4) Rotation-filtration class inventory and complete 192-basis contextuality.
    class_count=Counter(); resource_inventory=[]
    simple=simple_tensor_states()
    assert len(simple)==5266
    teleport_success=0; branch_equiv_fail=0
    for entries in product(range(16),repeat=4):
        cls=rotation_class(entries); class_count[cls]+=1
        M=resource_transfer_matrix(entries); rr=rank(M,8)
        Ts=teleport_branch_maps(entries); branks=tuple(rank(T,8) for T in Ts)
        full=all(r==8 for r in branks)
        if full: teleport_success+=1
        if full != (rr==8): branch_equiv_fail+=1
        state=pack_phase_branches(entries)
        resource_inventory.append({"m00":entries[0],"m01":entries[1],"m10":entries[2],"m11":entries[3],
                                   "class_a":cls[0],"class_b":cls[1],"boolean_rank8":rr,
                                   "universal_exact_fixed_analyzer":int(full),"separable":int(state in simple),
                                   "branch_ranks":"/".join(map(str,branks))})
    assert teleport_success==24576 and branch_equiv_fail==0
    expected_counts={(0,0):24576,(0,1):18432,(0,2):9216,(0,3):4608,(0,4):4608,
                     (1,1):1536,(1,2):1152,(1,3):576,(1,4):576,(2,2):96,(2,3):72,(2,4):72,(3,3):6,(3,4):9,(4,4):1}
    assert dict(class_count)==expected_counts
    mismatch=sum(((pack_phase_branches((r["m00"],r["m01"],r["m10"],r["m11"])) in simple) != (r["class_b"]==4)) for r in resource_inventory)
    assert mismatch==0
    write_csv("native_resource_inventory_65536.csv",resource_inventory)

    ctxt_rows=[]
    for a in range(5):
        for b in range(a,5):
            if a==4 and b==4:
                cov={"satisfiable":False,"clauses":4*len(bases)*len(bases),"possible_sections":0,
                     "extendable_possible_sections":0,"uncovered_possible_sections":0}
                status="DEGENERATE_ZERO_EXCLUDED"
            else:
                tables={(i,j):fast_support_table_diag(a,b,bases[i],bases[j]) for i in range(len(bases)) for j in range(len(bases))}
                cov=two_sat_coverage_from_tables(tables,len(bases))
                if not cov["satisfiable"]: status="STRONG_CONTEXTUAL"
                elif cov["uncovered_possible_sections"]: status="LOGICAL_CONTEXTUAL_NOT_STRONG"
                else: status="RELATIONALLY_LOCAL"
            prof=rotation_rank_profile((apply(N_POWERS[a],E0_VEC),0,0,apply(N_POWERS[b],E0_VEC)))
            ctxt_rows.append({"class_a":a,"class_b":b,"rank_profile":"/".join(map(str,prof)),
                              "resource_boolean_rank":prof[0],"state_count":class_count[(a,b)],
                              "separable_class":int(b==4),"classification":status,
                              "satisfiable_global_section":int(cov["satisfiable"]),"clauses":cov["clauses"],
                              "possible_sections":cov["possible_sections"],"extendable_possible_sections":cov["extendable_possible_sections"],
                              "uncovered_possible_sections":cov["uncovered_possible_sections"]})
    write_csv("contextuality_native_by_rotation_class.csv",ctxt_rows)
    summary["contextuality"]={"measurement_bases_per_party":len(bases),
        "strong_classes":sum(r["classification"]=="STRONG_CONTEXTUAL" for r in ctxt_rows),
        "logical_not_strong_classes":sum(r["classification"]=="LOGICAL_CONTEXTUAL_NOT_STRONG" for r in ctxt_rows),
        "local_nonzero_classes":sum(r["classification"]=="RELATIONALLY_LOCAL" for r in ctxt_rows),
        "zero_classes":1,
        "state_counts":{"strong":sum(r["state_count"] for r in ctxt_rows if r["classification"]=="STRONG_CONTEXTUAL"),
                        "logical_not_strong":sum(r["state_count"] for r in ctxt_rows if r["classification"]=="LOGICAL_CONTEXTUAL_NOT_STRONG"),
                        "local_nonzero":sum(r["state_count"] for r in ctxt_rows if r["classification"]=="RELATIONALLY_LOCAL")}}

    # 5) Bell-derived delta resource: generated natively and contextuality status.
    H_first=lift_single_bit_gate(H_ROT,2,0); C01=logical_cnot(2,0,1); B_ROT=compose(C01,H_first)
    beta=apply(B_ROT,pack_phase_branches((E0_VEC,0,0,0)))
    assert unpack_phase_branches(beta,4)==(1,0,0,5)
    beta_small_good,beta_small_uncovered=bell_support_coverage_small(beta,MQT_BASES)
    beta_complete=two_sat_support_coverage(beta,bases)
    summary["bell_delta"]={"generated_by_Hrot_then_CNOT":True,"state_branches":unpack_phase_branches(beta,4),
        "embedded_3_basis_global_assignments":len(beta_small_good),"embedded_3_basis_uncovered":len(beta_small_uncovered),
        "complete_192_basis":beta_complete}

    # 6) Teleportation: explicit 32x32 analyzer, 8x8 branch maps/corrections, all 256 inputs.
    bell_resource=(1,0,0,1)
    T=teleport_branch_maps(bell_resource)
    corrections=tuple(inverse(x,8) for x in T)
    assert all(c is not None for c in corrections)
    tele_rows=[]
    for A in range(16):
        for B in range(16):
            psi=A | (B<<4)
            for m,Tm in enumerate(T):
                recv=apply(Tm,psi); corr=apply(corrections[m],recv)
                assert corr==psi
                tele_rows.append({"A_phase":A,"B_phase":B,"outcome":m,"received":recv,"corrected":corr,"exact":1})
    write_csv("teleportation_native_all_256_x4.csv",tele_rows)
    # delta under standard Bell analyzer and under inverse of its native preparation gate
    Tdelta=teleport_branch_maps((1,0,0,5))
    Binv=inverse(B_ROT,16); assert Binv is not None
    Tdelta_natural=teleport_branch_maps_with_phase_analyzer((1,0,0,5),Binv)
    summary["teleportation"]={
        "bell_analyzer_f2":rows_to_lists(BELL_ANALYZER_F2,4),
        "global_analyzer_dimension":"32x32",
        "support_bell_branch_ranks":[rank(x,8) for x in T],
        "support_bell_branch_block_selectors":[block_selectors_2x2(x) for x in T],
        "support_bell_correction_block_selectors":[block_selectors_2x2(c) for c in corrections],
        "exhaustive_exact_checks":len(tele_rows),
        "universal_resource_count":teleport_success,
        "universal_iff_resource_boolean_rank8":branch_equiv_fail==0,
        "delta_resource_boolean_rank":rank(resource_transfer_matrix((1,0,0,5)),8),
        "delta_standard_bell_analyzer_branch_ranks":[rank(x,8) for x in Tdelta],
        "delta_natural_inverse_preparation_analyzer_branch_ranks":[rank(x,8) for x in Tdelta_natural],
        "delta_natural_branch_block_selectors":[block_selectors_2x2(x) for x in Tdelta_natural],
    }

    tele_class_rows=[]
    for r in ctxt_rows:
        a,b=r["class_a"],r["class_b"]
        rep=(apply(N_POWERS[a],E0_VEC),0,0,apply(N_POWERS[b],E0_VEC))
        M=resource_transfer_matrix(rep)
        Ts=teleport_branch_maps(rep)
        tele_class_rows.append({"class_a":a,"class_b":b,"state_count":class_count[(a,b)],
                                "resource_boolean_rank":rank(M,8),"rank_profile":r["rank_profile"],
                                "fixed_bell_analyzer_branch_ranks":"/".join(str(rank(x,8)) for x in Ts),
                                "universal_exact":int(rank(M,8)==8)})
    write_csv("teleportation_native_by_rotation_class.csv",tele_class_rows)

    # 7) GHZ states generated by native block gates and support analysis.
    seed3=pack_phase_branches((1,0,0,0,0,0,0,0))
    shear_first=lift_single_bit_gate(SHEAR2,3,0)
    hrot_first=lift_single_bit_gate(H_ROT,3,0)
    c01_3=logical_cnot(3,0,1); c02_3=logical_cnot(3,0,2)
    support_generated=apply(c02_3,apply(c01_3,apply(shear_first,seed3)))
    delta_generated=apply(c02_3,apply(c01_3,apply(hrot_first,seed3)))
    assert support_generated==ghz_state(0); assert delta_generated==ghz_state(2)
    ghz_support_summary,ghz_support_rows=ghz_analysis_native(support_generated)
    ghz_delta_summary,ghz_delta_rows=ghz_analysis_native(delta_generated)
    write_csv("ghz_support_native_contexts.csv",ghz_support_rows)
    write_csv("ghz_delta_native_contexts.csv",ghz_delta_rows)
    su_good,su_un=ghz_coverage_small(support_generated,unitary_bases)
    de_good,de_un=ghz_coverage_small(delta_generated,unitary_bases)
    summary["ghz"]={"support_generated_natively":True,"delta_generated_natively":True,
                    "support_embedded_3_basis":ghz_support_summary,"delta_embedded_3_basis":ghz_delta_summary,
                    "support_4_orthogonal_bases":{"global_assignments":su_good,"uncovered_possible_sections":su_un},
                    "delta_4_orthogonal_bases":{"global_assignments":de_good,"uncovered_possible_sections":de_un}}

    # 8) Exact regression against prior published raw tables when present locally.
    prior=Path('/mnt/data/Pure_Boolean_Modal_Quantum/data')
    compare={}
    if prior.exists():
        # contextuality values, ignoring renamed class columns and native rank fields
        pfile=prior/'bell_contextuality_by_smith_class.csv'
        if pfile.exists():
            with pfile.open() as f: old=list(csv.DictReader(f))
            old_map={(int(x['smith_a']),int(x['smith_b'])):x for x in old}
            fields=['classification','satisfiable_global_section','clauses','possible_sections','extendable_possible_sections','uncovered_possible_sections']
            mism=[]
            for r in ctxt_rows:
                o=old_map[(r['class_a'],r['class_b'])]
                for field in fields:
                    if str(r[field])!=str(o[field]): mism.append((r['class_a'],r['class_b'],field,r[field],o[field]))
            compare['contextuality_table_exact_match']=not mism
            compare['contextuality_mismatches']=mism[:20]
        pfile=prior/'modal_bell_mqt_tables.csv'
        if pfile.exists():
            with pfile.open() as f: old=list(csv.DictReader(f))
            norm_old=[(r['alice_setting'],r['bob_setting'],int(r['alice_outcome']),int(r['bob_outcome']),int(r['possible'])) for r in old]
            norm_new=[(r['alice_setting'],r['bob_setting'],int(r['alice_outcome']),int(r['bob_outcome']),int(r['possible'])) for r in bell_rows]
            compare['bell_table_exact_match']=norm_old==norm_new
        pfile=prior/'ghz_support_mqt_contexts.csv'
        if pfile.exists():
            with pfile.open() as f: old=list(csv.DictReader(f))
            norm_old=[(r['A'],r['B'],r['C'],int(r['outA']),int(r['outB']),int(r['outC']),int(r['possible'])) for r in old]
            norm_new=[(r['A'],r['B'],r['C'],int(r['outA']),int(r['outB']),int(r['outC']),int(r['possible'])) for r in ghz_support_rows]
            compare['ghz_support_table_exact_match']=norm_old==norm_new
        pfile=prior/'ghz_delta_mqt_contexts.csv'
        if pfile.exists():
            with pfile.open() as f: old=list(csv.DictReader(f))
            norm_old=[(r['A'],r['B'],r['C'],int(r['outA']),int(r['outB']),int(r['outC']),int(r['possible'])) for r in old]
            norm_new=[(r['A'],r['B'],r['C'],int(r['outA']),int(r['outB']),int(r['outC']),int(r['possible'])) for r in ghz_delta_rows]
            compare['ghz_delta_table_exact_match']=norm_old==norm_new
    summary['prior_raw_regression']=compare

    # 9) Native/new deductions.
    summary['new_native_deductions']={
        "phase_algebra_is_full_centralizer_of_P":True,
        "N_interpretation":"N=P XOR I is a one-step rotation-difference operator; N^4=0 and rank(N^a)=4-a.",
        "rotation_class_profile_formula":"For canonical (a,b), rank after N^j filtering is max(4-a-j,0)+max(4-b-j,0).",
        "teleportation_native_criterion":"Universal exact one-bit transfer iff the 8x8 Boolean resource transfer matrix has full rank 8.",
        "delta_rank_loss":"The (0,2) resource is diag(I4,N^2), rank 6: two of eight Boolean phase dimensions are collapsed before correction.",
        "orthogonality_reinterpretation":"The 512 previously intrinsic-unitary gates are exactly ordinary 8x8 Boolean orthogonal block matrices in this representation.",
    }

    elapsed=time.time()-t0
    summary['elapsed_seconds']=elapsed
    write_json('native_rebuild_summary.json',summary)
    (LOGS/'run_summary.txt').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
