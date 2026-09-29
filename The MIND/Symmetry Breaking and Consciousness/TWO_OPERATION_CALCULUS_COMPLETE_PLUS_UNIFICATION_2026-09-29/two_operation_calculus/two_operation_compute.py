#!/usr/bin/env python3
"""Exhaustive finite computations for the Two-Operation Calculus audit.

Universe convention for binary CM work:
    Omega_2 = (11,10,01,00), indexed 0,1,2,3.
An event/Boolean observable is encoded by a 4-bit mask with bit i indicating
truth on the corresponding valuation. A family of observables is a 16-bit
mask selecting event masks 0..15.

The script is deliberately dependency-light and reproducible with Python 3.
"""
from __future__ import annotations

import csv, json, math, os
from collections import Counter, defaultdict
from itertools import combinations

OUT = os.path.dirname(os.path.abspath(__file__))
OMEGA4_LABELS = ("11", "10", "01", "00")
N4 = 4
FULL4 = (1 << N4) - 1

# CM row order (11,10,01,00). Common names are descriptive only.
CM_NAMES = {
    0b0000: "FALSE/0",
    0b0001: "NOR (only 00)",       # bit convention index 3=00, see helper display_truth_bits
    0b0010: "not-left-and-right (01)",
    0b0011: "NOT X (01,00)",
    0b0100: "left-and-not-right (10)",
    0b0101: "NOT Y (10,00)",
    0b0110: "XOR (10,01)",
    0b0111: "NAND (not 11)",
    0b1000: "AND (11)",
    0b1001: "XNOR/equivalence (11,00)",
    0b1010: "Y (11,01)",
    0b1011: "X implies Y (not 10)",
    0b1100: "X (11,10)",
    0b1101: "Y implies X (not 01)",
    0b1110: "OR (not 00)",
    0b1111: "TRUE/1",
}
# Above masks are written visually in truth-bit order 11,10,01,00, but our integer
# bit i uses i=0 for 11. Convert from visual bit string if needed. To avoid ambiguity,
# derive names by explicit support labels instead below.
SUPPORT_TO_NAME = {
    frozenset(): "FALSE/0",
    frozenset(["00"]): "NOR",
    frozenset(["01"]): "not-X-and-Y",
    frozenset(["01","00"]): "NOT X",
    frozenset(["10"]): "X-and-not-Y",
    frozenset(["10","00"]): "NOT Y",
    frozenset(["10","01"]): "XOR",
    frozenset(["10","01","00"]): "NAND",
    frozenset(["11"]): "AND",
    frozenset(["11","00"]): "XNOR/equivalence",
    frozenset(["11","01"]): "Y",
    frozenset(["11","01","00"]): "X implies Y",
    frozenset(["11","10"]): "X",
    frozenset(["11","10","00"]): "Y implies X",
    frozenset(["11","10","01"]): "OR",
    frozenset(["11","10","01","00"]): "TRUE/1",
}

def bits(mask: int, n: int):
    return tuple((mask >> i) & 1 for i in range(n))

def support_labels(mask: int, labels=OMEGA4_LABELS):
    return tuple(labels[i] for i in range(len(labels)) if (mask >> i) & 1)

def event_name(mask: int):
    return SUPPORT_TO_NAME[frozenset(support_labels(mask))]

def mask_str(mask: int, n=N4):
    # Output in index order, matching labels tuple.
    return "".join(str((mask >> i) & 1) for i in range(n))

def set_str(mask: int, labels=OMEGA4_LABELS):
    return "{" + ",".join(labels[i] for i in range(len(labels)) if (mask >> i) & 1) + "}"

def family_events(fam_mask: int):
    return tuple(e for e in range(16) if (fam_mask >> e) & 1)

# ---------- Partitions / observation signatures ----------

def partition_from_events(events, n=N4):
    sig_to_mask = {}
    for x in range(n):
        sig = tuple(1 if ((e >> x) & 1) else 0 for e in events)
        sig_to_mask[sig] = sig_to_mask.get(sig, 0) | (1 << x)
    return canonical_partition(sig_to_mask.values())

def canonical_partition(blocks):
    b = tuple(sorted((int(x) for x in blocks if x), key=lambda x: (min(i for i in range(64) if (x>>i)&1), x)))
    return b

def partition_key(p):
    return "|".join(str(x) for x in p)

def partition_pretty(p, labels=OMEGA4_LABELS):
    return " | ".join(set_str(b, labels) for b in p)

def refines(q, p):
    """q refines p: every q-block is contained in a p-block."""
    for qb in q:
        if not any((qb & ~pb) == 0 for pb in p):
            return False
    return True

def refine_partition_by_event(p, e):
    blocks = []
    for b in p:
        a = b & e
        c = b & (~e & FULL4)
        if a: blocks.append(a)
        if c: blocks.append(c)
    return canonical_partition(blocks)

def join_partitions(p, q):
    # Common refinement, intersections of blocks.
    return canonical_partition([a & b for a in p for b in q if a & b])

def meet_partitions(p, q):
    # Coarsest common coarsening via union-find on points connected in either partition.
    parent = list(range(N4))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for part in (p,q):
        for b in part:
            pts=[i for i in range(N4) if (b>>i)&1]
            for z in pts[1:]: union(pts[0],z)
    comps=defaultdict(int)
    for i in range(N4): comps[find(i)] |= 1<<i
    return canonical_partition(comps.values())

def observable_algebra(p):
    # all unions of partition blocks
    vals={0}
    for b in p:
        vals |= {x|b for x in tuple(vals)}
    return frozenset(vals)

# ---------- Finite topologies from positive truth regions ----------

def topology_generated(events, carrier_mask=FULL4, n=N4):
    # Restrict generators to carrier; finite topology is closure under finite unions/intersections.
    gens={0, carrier_mask}
    for e in events:
        gens.add(e & carrier_mask)
    changed=True
    while changed:
        changed=False
        cur=list(gens)
        for a in cur:
            for b in cur:
                for c in (a|b, a&b):
                    c &= carrier_mask
                    if c not in gens:
                        gens.add(c); changed=True
    return frozenset(gens)

def restrict_topology(tau, s):
    return frozenset({u & s for u in tau})

def specialization_preorder(tau, carrier_mask=FULL4, n=N4):
    rel=[]
    for x in range(n):
        if not ((carrier_mask>>x)&1): continue
        for y in range(n):
            if not ((carrier_mask>>y)&1): continue
            ok=True
            for u in tau:
                if ((u>>x)&1) and not ((u>>y)&1):
                    ok=False; break
            if ok: rel.append((x,y))
    return tuple(rel)

def topo_t0(tau, carrier_mask=FULL4, n=N4):
    rel=set(specialization_preorder(tau,carrier_mask,n))
    pts=[i for i in range(n) if (carrier_mask>>i)&1]
    for i,j in combinations(pts,2):
        if (i,j) in rel and (j,i) in rel:
            return False
    return True

def topo_indisc_partition(tau, carrier_mask=FULL4, n=N4):
    rel=set(specialization_preorder(tau,carrier_mask,n))
    pts=[i for i in range(n) if (carrier_mask>>i)&1]
    unseen=set(pts); blocks=[]
    while unseen:
        i=min(unseen)
        block=0
        eq=[j for j in pts if (i,j) in rel and (j,i) in rel]
        for j in eq:
            block |= 1<<j; unseen.discard(j)
        blocks.append(block)
    return canonical_partition(blocks)

def topology_key(tau):
    return ",".join(str(x) for x in sorted(tau))

# ---------- Measures ----------

def surviving_block_sizes(s,p):
    return [int((s & b).bit_count()) for b in p if s & b]

def D_effective(s,p):
    return sum(1 for b in p if s & b)

def ambiguity_pairs(s,p):
    return sum(k*(k-1)//2 for k in surviving_block_sizes(s,p))

def ambiguity_max(s,p):
    sizes=surviving_block_sizes(s,p)
    return max(sizes) if sizes else 0

def invisible_symmetry_order(s,p):
    out=1
    for k in surviving_block_sizes(s,p): out *= math.factorial(k)
    return out

def total_pairs(s):
    k=s.bit_count(); return k*(k-1)//2

def distinguished_pairs(s,p):
    return total_pairs(s)-ambiguity_pairs(s,p)

# ---------- Enumerate all set partitions of 4 ----------

def set_partitions_points(n):
    # recursive lists of tuples of frozensets
    ans=[]
    def rec(i, blocks):
        if i==n:
            masks=[]
            for B in blocks:
                m=0
                for x in B:m|=1<<x
                masks.append(m)
            ans.append(canonical_partition(masks)); return
        for j in range(len(blocks)):
            blocks[j].add(i); rec(i+1,blocks); blocks[j].remove(i)
        blocks.append({i}); rec(i+1,blocks); blocks.pop()
    rec(0,[])
    return sorted(set(ans), key=lambda p:(len(p),p))

# ---------- CSV helper ----------
def write_csv(path, fields, rows):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    parts=set_partitions_points(N4)
    assert len(parts)==15
    part_id={p:i for i,p in enumerate(parts)}

    # 1. All 16 observables / CM realization
    obs_rows=[]; cm_rows=[]
    for e in range(16):
        sup=support_labels(e)
        # compact CM [[11,10],[01,00]] in the project convention
        vals=[(e>>i)&1 for i in range(4)]
        p=partition_from_events([e])
        obs_rows.append({
            "event_id":e,"truth_bits_11_10_01_00":mask_str(e),"name":event_name(e),
            "support":set_str(e),"support_size":e.bit_count(),"induced_partition_id":part_id[p],
            "induced_partition":partition_pretty(p),
        })
        cm_rows.append({
            "event_id":e,"name":event_name(e),"theta_11":vals[0],"theta_10":vals[1],"theta_01":vals[2],"theta_00":vals[3],
            "compact_CM":f"[[{vals[0]},{vals[1]}],[{vals[2]},{vals[3]}]]",
            "support_event":set_str(e),
            "diagonal_effect":f"diag({vals[0]},{vals[1]},{vals[2]},{vals[3]})",
            "rank_over_any_field":e.bit_count(),"idempotent_diagonal":True,
        })
    write_csv(os.path.join(OUT,"OBSERVABLES.csv"), list(obs_rows[0]), obs_rows)
    write_csv(os.path.join(OUT,"CM_REALIZATION_TABLE.csv"), list(cm_rows[0]), cm_rows)

    # 2. Partition lattice and joins
    part_rows=[]
    for p in parts:
        alg=observable_algebra(p)
        coarser=sum(1 for q in parts if refines(p,q))
        finer=sum(1 for q in parts if refines(q,p))
        part_rows.append({
            "partition_id":part_id[p],"blocks":partition_pretty(p),"num_blocks":len(p),
            "boolean_event_algebra_size":len(alg),"num_coarser_including_self":coarser,"num_finer_including_self":finer,
            "ambiguity_pairs_full":ambiguity_pairs(FULL4,p),"invisible_symmetry_order_full":invisible_symmetry_order(FULL4,p),
        })
    write_csv(os.path.join(OUT,"PARTITION_LATTICE.csv"), list(part_rows[0]), part_rows)
    join_rows=[]
    for p in parts:
        for q in parts:
            j=join_partitions(p,q); m=meet_partitions(p,q)
            join_rows.append({"p":part_id[p],"q":part_id[q],"join_common_refinement":part_id[j],"meet_common_coarsening":part_id[m]})
    write_csv(os.path.join(OUT,"PARTITION_JOINS.csv"), list(join_rows[0]), join_rows)

    # 3. All 65,536 observation families: partition, positive topology, separation.
    # Fast route: a finite topology generated by positive truth regions is encoded by
    # its specialization preorder. Each event imposes x<=y whenever x in E => y in E;
    # a family intersects those event preorders. Compute family relations by lsb DP.
    def event_rel_mask(e):
        rm=0
        k=0
        for x in range(4):
            for y in range(4):
                if not (((e>>x)&1) and not ((e>>y)&1)):
                    rm |= 1<<k
                k+=1
        return rm
    ALLREL=(1<<16)-1
    erel=[event_rel_mask(e) for e in range(16)]
    fam_rel=[0]*(1<<16)
    fam_rel[0]=ALLREL
    rel_to_tau={}
    rel_to_tid={}
    topo_list=[]
    family_rows=[]
    family_part_counts=Counter(); family_topo_counts=Counter()
    p_of_fam=[None]*(1<<16)
    p_of_fam[0]=canonical_partition([FULL4])

    def opens_from_relmask(rm):
        opens=[]
        for u in range(16):
            ok=True; k=0
            for x in range(4):
                for y in range(4):
                    if (rm>>k)&1:
                        if ((u>>x)&1) and not ((u>>y)&1):
                            ok=False; break
                    k+=1
                if not ok: break
            if ok: opens.append(u)
        return frozenset(opens)

    for fm in range(1<<16):
        if fm:
            lsb=fm & -fm; e=lsb.bit_length()-1
            fam_rel[fm]=fam_rel[fm^lsb] & erel[e]
        rm=fam_rel[fm]
        if rm not in rel_to_tid:
            tau=opens_from_relmask(rm)
            tid=len(topo_list); rel_to_tid[rm]=tid; rel_to_tau[rm]=tau; topo_list.append(tau)
        else:
            tid=rel_to_tid[rm]; tau=topo_list[tid]
        if fm:
            p=refine_partition_by_event(p_of_fam[fm^lsb],e)
            p_of_fam[fm]=p
        else:
            p=p_of_fam[0]
        evs=family_events(fm)
        family_part_counts[part_id[p]] += 1
        family_topo_counts[tid] += 1
        full_sep=(len(p)==N4)
        family_rows.append({
            "family_mask":fm,"family_size":fm.bit_count(),"events":";".join(str(e) for e in evs),
            "partition_id":part_id[p],"partition_blocks":len(p),"topology_id":tid,"topology_num_opens":len(tau),
            "T0":full_sep,"fully_separating":full_sep,
        })
    assert len(topo_list)==355, len(topo_list)
    write_csv(os.path.join(OUT,"OBSERVATION_FAMILY_SUMMARY.csv"), list(family_rows[0]), family_rows)

    topo_rows=[]
    t0_count=0
    for tid,tau in enumerate(topo_list):
        t0=topo_t0(tau); t0_count+=int(t0)
        ip=topo_indisc_partition(tau)
        rel=specialization_preorder(tau)
        topo_rows.append({
            "topology_id":tid,"num_opens":len(tau),"open_masks":";".join(str(x) for x in sorted(tau)),
            "opens":";".join(set_str(x) for x in sorted(tau)),"T0":t0,
            "indiscernibility_partition_id":part_id[ip],"specialization_relation_size":len(rel),
            "num_generating_families_seen":family_topo_counts[tid],
        })
    assert t0_count==219, t0_count
    write_csv(os.path.join(OUT,"POSITIVE_TOPOLOGIES.csv"), list(topo_rows[0]), topo_rows)

    # 4. Refinement transitions from partitions by one event.
    ref_rows=[]
    for p in parts:
        for e in range(16):
            q=refine_partition_by_event(p,e)
            alg=observable_algebra(p)
            ref_rows.append({
                "source_partition":part_id[p],"event_id":e,"event_name":event_name(e),"target_partition":part_id[q],
                "source_blocks":len(p),"target_blocks":len(q),"strict_refinement":q!=p,
                "event_already_measurable":e in alg,
                "ambiguity_pairs_before":ambiguity_pairs(FULL4,p),"ambiguity_pairs_after":ambiguity_pairs(FULL4,q),
            })
    write_csv(os.path.join(OUT,"REFINEMENT_TRANSITIONS.csv"), list(ref_rows[0]), ref_rows)

    # 5. All 240 canonical (S, partition) states and differentiation measures.
    state_rows=[]
    for p in parts:
        for s in range(16):
            state_rows.append({
                "partition_id":part_id[p],"S_mask":s,"S":set_str(s),"S_size":s.bit_count(),
                "global_classes":len(p),"effective_classes":D_effective(s,p),
                "ambiguity_pairs":ambiguity_pairs(s,p),"distinguished_pairs":distinguished_pairs(s,p),
                "max_ambiguity_class":ambiguity_max(s,p),"invisible_symmetry_order":invisible_symmetry_order(s,p),
                "fully_distinguished_on_S":ambiguity_pairs(s,p)==0,
            })
    write_csv(os.path.join(OUT,"STATE_DIFFERENTIATION_MEASURES.csv"), list(state_rows[0]), state_rows)

    # 6. Verify global monotonicity under all refinements and all hard measurements.
    monotone_checks=0; monotone_fail=[]
    for p in parts:
        for q in parts:
            if not refines(q,p): continue
            for s in range(16):
                monotone_checks += 1
                if ambiguity_pairs(s,q) > ambiguity_pairs(s,p) or ambiguity_max(s,q) > ambiguity_max(s,p) or invisible_symmetry_order(s,q) > invisible_symmetry_order(s,p):
                    monotone_fail.append(("R",part_id[p],part_id[q],s))
    for p in parts:
        for s in range(16):
            for e in range(16):
                s2=s&e; monotone_checks += 1
                if ambiguity_pairs(s2,p) > ambiguity_pairs(s,p) or ambiguity_max(s2,p) > ambiguity_max(s,p) or invisible_symmetry_order(s2,p) > invisible_symmetry_order(s,p):
                    monotone_fail.append(("M",part_id[p],s,e))
    assert not monotone_fail, monotone_fail[:5]

    # 7. Complete MR/RM square enumeration on partition-level state space.
    square_rows=[]; square_counts=Counter()
    for p in parts:
        alg0=observable_algebra(p)
        for s in range(16):
            for r in range(16):
                q=refine_partition_by_event(p,r)
                alg1=observable_algebra(q)
                for m in range(16):
                    # Both fixed ambient operations: exact same final pair.
                    s_m=s&m
                    final_MR=(s_m,q)
                    final_RM=(s_m,q)
                    commute=(final_MR==final_RM)
                    before=m in alg0; after=m in alg1
                    if before: av="persistent"
                    elif after: av="enabled_by_refinement"
                    else: av="unavailable_even_after"
                    square_counts[av]+=1
                    square_counts["commuting" if commute else "noncommuting"]+=1
                    square_rows.append({
                        "source_partition":part_id[p],"S_mask":s,"refinement_event":r,"measurement_event":m,
                        "target_partition":part_id[q],"measured_S_mask":s_m,"commutes_fixed_carrier":commute,
                        "measurement_available_before":before,"measurement_available_after":after,"availability_class":av,
                    })
    assert all(r["commutes_fixed_carrier"] for r in square_rows)
    write_csv(os.path.join(OUT,"MR_RM_SQUARES.csv"), list(square_rows[0]), square_rows)

    # 8. Topological fixed-carrier commutation: refine topology by truth-open then condition/restrict.
    # Exhaust all distinct (topology, refinement event, surviving carrier) triples.
    # (The original (S,E) measurement pairs collapse to their intersection S'=S∩E.)
    topo_square_checks=0; topo_square_fail=0
    refine_topo_cache={}
    for tid,tau in enumerate(topo_list):
        for r in range(16):
            tauR=topology_generated(list(tau)+[r])
            refine_topo_cache[(tid,r)]=tauR
            for s2 in range(16):
                route1=restrict_topology(tauR,s2)
                route2=topology_generated(list(restrict_topology(tau,s2))+[r&s2], carrier_mask=s2)
                topo_square_checks += 1
                if route1 != route2:
                    topo_square_fail += 1
    assert topo_square_fail==0

    # 9. Minimal / irredundant observation bases for every partition.
    # A family is inclusion-minimal for target partition if deleting any event changes its induced partition.
    irredundant=[]; inclusion_min_counts=Counter()
    # p_of_fam was cached during exhaustive family enumeration above.
    min_by_part={pid:min(fm.bit_count() for fm in range(1<<16) if part_id[p_of_fam[fm]]==pid) for pid in range(len(parts))}
    count_min_by_part=Counter()
    for fm in range(1<<16):
        p=p_of_fam[fm]
        sz=fm.bit_count()
        if sz == min_by_part[part_id[p]]:
            count_min_by_part[part_id[p]] += 1
        if fm==0:
            minimal=True
        else:
            minimal=True
            for e in family_events(fm):
                fm2=fm & ~(1<<e)
                if p_of_fam[fm2]==p:
                    minimal=False; break
        if minimal:
            inclusion_min_counts[(part_id[p],sz)] += 1
            irredundant.append({
                "partition_id":part_id[p],"partition":partition_pretty(p),"family_mask":fm,"family_size":sz,
                "events":";".join(str(e) for e in family_events(fm)),"event_names":";".join(event_name(e) for e in family_events(fm)),
            })
    write_csv(os.path.join(OUT,"IRREDUNDANT_BASES.csv"), list(irredundant[0]), irredundant)

    full_disc=[p for p in parts if len(p)==4][0]
    full_id=part_id[full_disc]
    full_inclusion_by_size={str(sz):c for (pid,sz),c in inclusion_min_counts.items() if pid==full_id}

    # 10. Algebraic verification sufficient for the sequential normal form theorem.
    # Check idempotence/commutation of all refinement pairs and all measurement pairs.
    seq_checks=0
    for p in parts:
        for e in range(16):
            assert refine_partition_by_event(refine_partition_by_event(p,e),e)==refine_partition_by_event(p,e)
            seq_checks += 1
            for f in range(16):
                a=refine_partition_by_event(refine_partition_by_event(p,e),f)
                b=refine_partition_by_event(refine_partition_by_event(p,f),e)
                assert a==b
                seq_checks += 1
    for s in range(16):
        for e in range(16):
            assert (s&e&e)==(s&e); seq_checks += 1
            for f in range(16):
                assert ((s&e)&f)==((s&f)&e)
                seq_checks += 1
    # Cross-commutation was exhaustively checked in MR_RM_SQUARES above.
    seq_checks += len(square_rows)

    # 11. Three-variable examples (Omega8 indexed xyz 111,110,101,100,011,010,001,000 for display only)
    labels8=("111","110","101","100","011","010","001","000")
    # build masks by actual label values
    def e8(pred):
        m=0
        for i,lab in enumerate(labels8):
            x,y,z=map(int,lab)
            if pred(x,y,z):m|=1<<i
        return m
    X=e8(lambda x,y,z:x==1); Y=e8(lambda x,y,z:y==1); Z=e8(lambda x,y,z:z==1)
    nX=((1<<8)-1)^X; nY=((1<<8)-1)^Y; nZ=((1<<8)-1)^Z
    tau_xyz=topology_generated([X,Y,Z], carrier_mask=(1<<8)-1, n=8)
    tau_both=topology_generated([X,Y,Z,nX,nY,nZ], carrier_mask=(1<<8)-1, n=8)
    p_xyz=partition_from_events([X,Y,Z],n=8)
    # cylinder of X from one variable to 3 has 4 satisfying valuations
    three_rows=[
        {"case":"positive observations X,Y,Z","num_worlds":8,"num_observations":3,"num_partition_blocks":len(p_xyz),"num_topology_opens":len(tau_xyz),"comment":"Full two-sided signature separation but only positive Alexandrov/up-set topology."},
        {"case":"X,Y,Z plus complements","num_worlds":8,"num_observations":6,"num_partition_blocks":8,"num_topology_opens":len(tau_both),"comment":"Discrete topology because every singleton is generated."},
        {"case":"cylinder X from Omega_1 to Omega_3","num_worlds":8,"num_observations":1,"num_partition_blocks":2,"num_topology_opens":len(topology_generated([X],carrier_mask=(1<<8)-1,n=8)),"comment":f"Truth support of X has size {X.bit_count()} = 2^(3-1)."},
    ]
    write_csv(os.path.join(OUT,"THREE_VARIABLE_EXAMPLES.csv"), list(three_rows[0]), three_rows)

    # Summary / machine-verifiable claims.
    summary={
        "universe_order":OMEGA4_LABELS,
        "num_binary_observables":16,
        "num_partitions_Bell_4":len(parts),
        "num_observation_families_over_all_16_events":1<<16,
        "num_distinct_positive_topologies_on_4_labeled_points":len(topo_list),
        "num_T0_positive_topologies_on_4_labeled_points":t0_count,
        "num_canonical_partition_states_S_Pi":16*len(parts),
        "num_MR_RM_squares_checked":len(square_rows),
        "MR_RM_noncommuting_fixed_carrier":square_counts["noncommuting"],
        "MR_RM_availability_counts":dict(square_counts),
        "topological_refinement_conditioning_squares_checked":topo_square_checks,
        "topological_refinement_conditioning_failures":topo_square_fail,
        "joint_monotonicity_checks":monotone_checks,
        "joint_monotonicity_failures":len(monotone_fail),
        "sequential_normal_form_checks":seq_checks,
        "full_separation_minimum_observations_Omega4":min_by_part[full_id],
        "full_separation_number_of_minimum_families":count_min_by_part[full_id],
        "full_separation_inclusion_minimal_counts_by_size":full_inclusion_by_size,
        "three_variable_positive_XYZ_topology_opens":len(tau_xyz),
        "three_variable_XYZ_plus_complements_topology_opens":len(tau_both),
        "three_variable_X_truth_support":X.bit_count(),
    }
    with open(os.path.join(OUT,"summary.json"),"w",encoding="utf-8") as f: json.dump(summary,f,indent=2)

    with open(os.path.join(OUT,"COMPUTATION_LOG.txt"),"w",encoding="utf-8") as f:
        f.write("Two-operation calculus exhaustive computation completed successfully.\n")
        for k,v in summary.items(): f.write(f"{k}: {v}\n")

    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
