"""Exhaustive finite investigations for the pure-Boolean CM modal program."""
from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from typing import Dict, Iterable, List, Sequence, Tuple

from .cm_ring import (
    DELTA, E0, MUL, U, UNITS, bar, canonical_unordered_basis, det2,
    effect_amplitude2, identity, inverse_matrix, is_invertible2,
    is_monomial_unit_gate, is_unitary2, kron, local_action, matmul, matvec,
    outer2, star, support_table2, support_table3, transpose,
)

I2 = (E0, 0, 0, E0)
X2 = (0, E0, E0, 0)
HSTAR = (E0, DELTA, DELTA, E0)
C_SHEAR_LOWER = (E0, 0, E0, E0)
K_SHEAR_UPPER = (E0, E0, 0, E0)
CNOT = (
    E0,0,0,0,
    0,E0,0,0,
    0,0,0,E0,
    0,0,E0,0,
)

# Embedded F2 modal bases. Each row is an effect. Labels are conventional only.
BASIS_Z = ((E0, 0), (0, E0))
BASIS_X = ((E0, E0), (E0, 0))
BASIS_Y = ((0, E0), (E0, E0))
MQT_BASES = (BASIS_Z, BASIS_X, BASIS_Y)
MQT_NAMES = ("Z", "X", "Y")


def gate_inventory():
    rows = []
    GL = []
    UNI = []
    for A in product(range(16), repeat=4):
        inv = is_invertible2(A)
        uni = inv and is_unitary2(A)
        mono = inv and is_monomial_unit_gate(A)
        full = inv and all(x != 0 for x in A)
        branch = inv and not mono
        row = {
            "a00": A[0], "a01": A[1], "a10": A[2], "a11": A[3],
            "det": det2(A), "det_is_unit": int(det2(A) in UNITS),
            "invertible": int(inv), "unitary": int(uni),
            "monomial_phase_permutation": int(mono),
            "genuine_branch_mixer": int(branch),
            "full_two_branch_splitter": int(full),
        }
        rows.append(row)
        if inv:
            GL.append(A)
        if uni:
            UNI.append(A)
    summary = {
        "all_2x2_matrices": len(rows),
        "invertible": len(GL),
        "intrinsic_unitary": len(UNI),
        "monomial_phase_permutation": sum(r["monomial_phase_permutation"] for r in rows),
        "genuine_branch_mixer": sum(r["genuine_branch_mixer"] for r in rows),
        "full_two_branch_splitter": sum(r["full_two_branch_splitter"] for r in rows),
        "unitary_monomial": sum(r["unitary"] and r["monomial_phase_permutation"] for r in rows),
        "unitary_full_splitter": sum(r["unitary"] and r["full_two_branch_splitter"] for r in rows),
    }
    return rows, GL, UNI, summary


def measurement_bases(GL, UNI):
    all_bases = sorted({canonical_unordered_basis(A) for A in GL})
    unitary_bases = sorted({canonical_unordered_basis(A) for A in UNI})
    return all_bases, unitary_bases


def bell_tables(state=(E0,0,0,E0), bases=MQT_BASES, names=MQT_NAMES):
    rows = []
    tables = {}
    for i, A in enumerate(bases):
        for j, B in enumerate(bases):
            table = support_table2(state, A, B)
            tables[(names[i], names[j])] = table
            for idx, possible in enumerate(table):
                rows.append({
                    "alice_setting": names[i], "bob_setting": names[j],
                    "alice_outcome": idx // 2, "bob_outcome": idx % 2,
                    "possible": possible,
                })
    return tables, rows


def compatible_bell_globals(state, bases):
    n = len(bases)
    good = []
    for assignment in product((0,1), repeat=2*n):
        ok = True
        for i in range(n):
            for j in range(n):
                t = support_table2(state, bases[i], bases[j])
                if not t[2*assignment[i] + assignment[n+j]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            good.append(assignment)
    return good


def bell_support_coverage(state, bases):
    """Exact relational locality test for small finite setting families."""
    n = len(bases)
    good = compatible_bell_globals(state, bases)
    uncovered = []
    for i in range(n):
        for j in range(n):
            t = support_table2(state, bases[i], bases[j])
            for idx, possible in enumerate(t):
                if not possible:
                    continue
                a, b = idx // 2, idx % 2
                if not any(g[i] == a and g[n+j] == b for g in good):
                    uncovered.append((i,j,a,b))
    return good, uncovered


def two_sat_all_bases(state, bases):
    """Strong-contextuality check for a bipartite dichotomic support model.

    Every impossible local outcome pair becomes a 2-SAT clause. A satisfying
    assignment is a global deterministic section compatible with all contexts.
    """
    n = len(bases)
    N = 2*n
    adj = [[] for _ in range(2*N)]
    clauses = []
    def node(v, val): return 2*v + val
    def add_clause(v1, val1, v2, val2):
        clauses.append((v1,val1,v2,val2))
        adj[node(v1,1-val1)].append(node(v2,val2))
        adj[node(v2,1-val2)].append(node(v1,val1))
    for i,A in enumerate(bases):
        for j,B in enumerate(bases):
            t = support_table2(state,A,B)
            for a in (0,1):
                for b in (0,1):
                    if not t[2*a+b]:
                        # forbid (Ai=a,Bj=b): (Ai!=a) OR (Bj!=b)
                        add_clause(i,1-a,n+j,1-b)
    # Tarjan SCC
    idx = 0; stack = []; on = [False]*(2*N)
    ids = [-1]*(2*N); low = [0]*(2*N); comp = [-1]*(2*N); cc = 0
    import sys
    sys.setrecursionlimit(max(10000,4*N+100))
    def dfs(v):
        nonlocal idx, cc
        ids[v] = low[v] = idx; idx += 1
        stack.append(v); on[v] = True
        for w in adj[v]:
            if ids[w] < 0:
                dfs(w); low[v] = min(low[v],low[w])
            elif on[w]:
                low[v] = min(low[v],ids[w])
        if low[v] == ids[v]:
            while True:
                w = stack.pop(); on[w] = False; comp[w] = cc
                if w == v: break
            cc += 1
    for v in range(2*N):
        if ids[v] < 0: dfs(v)
    if any(comp[2*v] == comp[2*v+1] for v in range(N)):
        return {"satisfiable": False, "assignment": None, "clauses": len(clauses)}
    assignment = None
    for orientation in ("lt", "gt"):
        vals = [int((comp[2*v] < comp[2*v+1]) if orientation == "lt" else (comp[2*v] > comp[2*v+1])) for v in range(N)]
        if all(vals[v1] == val1 or vals[v2] == val2 for v1,val1,v2,val2 in clauses):
            assignment = vals
            break
    assert assignment is not None
    return {"satisfiable": True, "assignment": assignment, "clauses": len(clauses)}



def two_sat_support_coverage_all_bases(state, bases):
    """Exact support-locality coverage test for a bipartite dichotomic model.

    The base support constraints are encoded as 2-SAT.  If they are
    satisfiable, transitive implication reachability is precomputed.  A
    possible section (Ai=a,Bj=b) extends to a deterministic global section
    iff the two corresponding literal assumptions are jointly consistent.

    For a satisfiable 2-SAT formula, two assumptions l,m are inconsistent iff
    l implies not-l, m implies not-m, l implies not-m, or m implies not-l.
    The implication graph already contains contrapositives, so this criterion
    also captures contradictions reached through other variables.
    """
    n = len(bases)
    N = 2 * n
    adj = [[] for _ in range(2 * N)]
    clauses = []

    def node(v, val):
        return 2 * v + val

    def neg_node(x):
        return x ^ 1

    def add_clause(v1, val1, v2, val2):
        clauses.append((v1, val1, v2, val2))
        adj[node(v1, 1 - val1)].append(node(v2, val2))
        adj[node(v2, 1 - val2)].append(node(v1, val1))

    tables = {}
    for i, A in enumerate(bases):
        for j, B in enumerate(bases):
            t = support_table2(state, A, B)
            tables[(i, j)] = t
            for a in (0, 1):
                for b in (0, 1):
                    if not t[2 * a + b]:
                        add_clause(i, 1 - a, n + j, 1 - b)

    # Tarjan SCC to reject a strongly contextual base model immediately.
    idx = 0
    stack = []
    on = [False] * (2 * N)
    ids = [-1] * (2 * N)
    low = [0] * (2 * N)
    comp = [-1] * (2 * N)
    cc = 0

    def dfs(v):
        nonlocal idx, cc
        ids[v] = low[v] = idx
        idx += 1
        stack.append(v)
        on[v] = True
        for w in adj[v]:
            if ids[w] < 0:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif on[w]:
                low[v] = min(low[v], ids[w])
        if low[v] == ids[v]:
            while True:
                w = stack.pop()
                on[w] = False
                comp[w] = cc
                if w == v:
                    break
            cc += 1

    for v in range(2 * N):
        if ids[v] < 0:
            dfs(v)

    satisfiable = not any(comp[2 * v] == comp[2 * v + 1] for v in range(N))
    possible_sections = sum(sum(t) for t in tables.values())
    if not satisfiable:
        return {
            "satisfiable": False,
            "clauses": len(clauses),
            "possible_sections": possible_sections,
            "extendable_possible_sections": 0,
            "uncovered_possible_sections": possible_sections,
            "first_uncovered": None,
        }

    # Reachability from each literal.  There are at most 768 literal nodes for
    # the 192-basis family, so a DFS per node is cheap and exact.
    reachable = []
    for start in range(2 * N):
        seen = 1 << start
        stack2 = [start]
        while stack2:
            v = stack2.pop()
            for w in adj[v]:
                bit = 1 << w
                if not (seen & bit):
                    seen |= bit
                    stack2.append(w)
        reachable.append(seen)

    def reaches(x, y):
        return bool(reachable[x] & (1 << y))

    uncovered = []
    extendable = 0
    for (i, j), t in tables.items():
        for a in (0, 1):
            for b in (0, 1):
                if not t[2 * a + b]:
                    continue
                l = node(i, a)
                m = node(n + j, b)
                bad = (
                    reaches(l, neg_node(l))
                    or reaches(m, neg_node(m))
                    or reaches(l, neg_node(m))
                    or reaches(m, neg_node(l))
                )
                if bad:
                    uncovered.append((i, j, a, b))
                else:
                    extendable += 1

    return {
        "satisfiable": True,
        "clauses": len(clauses),
        "possible_sections": possible_sections,
        "extendable_possible_sections": extendable,
        "uncovered_possible_sections": len(uncovered),
        "first_uncovered": None if not uncovered else uncovered[0],
    }


def _u_power_chain():
    """Return (1,u,u^2,u^3,0) in the chain ring A=F2[u]/(u^4)."""
    vals = [E0]
    for _ in range(3):
        vals.append(MUL[vals[-1]][U])
    vals.append(0)
    return tuple(vals)


def smith_modal_contextuality_inventory(bases):
    """Classify all 15 Smith representatives under a complete basis family.

    Each representative is diag(u^a,u^b), 0 <= a <= b <= 4 with u^4=0.
    For dichotomic local reversible bases, strong contextuality is exactly
    failure of the base 2-SAT instance.  When a global section exists, exact
    relational locality additionally requires every possible local section to
    extend to at least one global deterministic section.
    """
    up = _u_power_chain()
    rows = []
    for a in range(5):
        for b in range(a, 5):
            state = (up[a], 0, 0, up[b])
            if a == 4 and b == 4:
                rows.append({
                    "smith_a": a, "smith_b": b,
                    "separable_class": 1, "nonseparable_class": 0,
                    "classification": "DEGENERATE_ZERO_EXCLUDED",
                    "satisfiable_global_section": 0,
                    "clauses": 4 * len(bases) * len(bases),
                    "possible_sections": 0,
                    "extendable_possible_sections": 0,
                    "uncovered_possible_sections": 0,
                })
                continue
            cov = two_sat_support_coverage_all_bases(state, bases)
            if not cov["satisfiable"]:
                status = "STRONG_CONTEXTUAL"
            elif cov["uncovered_possible_sections"]:
                status = "LOGICAL_CONTEXTUAL_NOT_STRONG"
            else:
                status = "RELATIONALLY_LOCAL"
            rows.append({
                "smith_a": a, "smith_b": b,
                "separable_class": int(b == 4),
                "nonseparable_class": int(b < 4),
                "classification": status,
                "satisfiable_global_section": int(cov["satisfiable"]),
                "clauses": cov["clauses"],
                "possible_sections": cov["possible_sections"],
                "extendable_possible_sections": cov["extendable_possible_sections"],
                "uncovered_possible_sections": cov["uncovered_possible_sections"],
            })
    counts = Counter(r["classification"] for r in rows)
    summary = {
        "measurement_bases_per_party": len(bases),
        "smith_classes_total": len(rows),
        "strong_contextual_classes": counts["STRONG_CONTEXTUAL"],
        "logical_not_strong_classes": counts["LOGICAL_CONTEXTUAL_NOT_STRONG"],
        "relationally_local_nonzero_classes": counts["RELATIONALLY_LOCAL"],
        "degenerate_zero_classes": counts["DEGENERATE_ZERO_EXCLUDED"],
    }
    return rows, summary


def offdiagonal_hardy_witnesses(all_bases=None):
    """Hardy/logical-nonlocality witnesses for every off-diagonal Smith class.

    For D=diag(p,q) with p=u^a, q=u^b and a<b<4, put c=u^(b-a).
    Use R=((0,1),(1,0)), X=((1,0),(1,1)), and
    D_c=((1,0),(c,1)).  The four support tables are respectively
    1001, 0111, 1110, 0111.  Hence the possible RR event 00 cannot extend to
    a deterministic assignment for these three local settings.
    """
    up = _u_power_chain()
    R = ((0, E0), (E0, 0))
    Xc = ((E0, 0), (E0, E0))
    basis_id = None
    if all_bases is not None:
        basis_id = {b: i for i, b in enumerate(all_bases)}

    witnesses = []
    for a in range(4):
        for b in range(a + 1, 4):
            p, q = up[a], up[b]
            c = up[b - a]
            Dc = ((E0, 0), (c, E0))
            state = (p, 0, 0, q)
            tabs = {
                "R/R": support_table2(state, R, R),
                "R/X": support_table2(state, R, Xc),
                "D/X": support_table2(state, Dc, Xc),
                "D/R": support_table2(state, Dc, R),
            }
            assert tabs == {
                "R/R": (1, 0, 0, 1),
                "R/X": (0, 1, 1, 1),
                "D/X": (1, 1, 1, 0),
                "D/R": (0, 1, 1, 1),
            }
            row = {
                "smith_a": a, "smith_b": b,
                "p": p, "q": q, "c_u_power": b - a, "c": c,
                "R": R, "X": Xc, "D_c": Dc,
                "tables": tabs,
                "possible_seed_event": {"A_setting": "R", "A_outcome": 0,
                                        "B_setting": "R", "B_outcome": 0},
                "implication_chain": ["R_A=0", "X_B=1", "D_A=0", "R_B=1"],
                "contradicts_seed": "R_B=0",
            }
            if basis_id is not None:
                row["basis_ids"] = {
                    "R": basis_id[canonical_unordered_basis((R[0][0],R[0][1],R[1][0],R[1][1]))],
                    "X": basis_id[canonical_unordered_basis((Xc[0][0],Xc[0][1],Xc[1][0],Xc[1][1]))],
                    "D_c": basis_id[canonical_unordered_basis((Dc[0][0],Dc[0][1],Dc[1][0],Dc[1][1]))],
                }
            witnesses.append(row)
    return witnesses


def teleportation_protocol():
    """Universal ring-valued teleportation via an embedded-F2 Bell basis."""
    KX = matmul(K_SHEAR_UPPER, X2, 2)
    bell_mats = (I2, X2, K_SHEAR_UPPER, KX)
    # Bell transform: columns are row-major vectorizations of the four matrices.
    Q = tuple(bell_mats[j][i] for i in range(4) for j in range(4))
    Qinv = inverse_matrix(Q,4)
    assert Qinv is not None and matmul(Qinv,Q,4) == identity(4)
    resource = (E0,0,0,E0)
    branch_maps = _teleport_branch_maps(Qinv, resource)
    corrections = tuple(inverse_matrix(Tm,2) for Tm in branch_maps)
    assert all(c is not None for c in corrections)
    rows = []
    checks = 0
    for A in range(16):
        for B in range(16):
            psi = (A,B)
            for m,Tm in enumerate(branch_maps):
                recv = matvec(Tm,psi,2)
                corrected = matvec(corrections[m],recv,2)
                exact = corrected == psi
                assert exact
                if psi != (0,0):
                    assert recv != (0,0)
                rows.append({
                    "A": A, "B": B, "outcome": m,
                    "received0": recv[0], "received1": recv[1],
                    "corrected0": corrected[0], "corrected1": corrected[1],
                    "exact": int(exact), "branch_possible_for_nonzero_input": int(psi == (0,0) or recv != (0,0)),
                })
                checks += 1
    return {
        "Q": Q, "Q_inverse": Qinv,
        "bell_basis_matrices": bell_mats,
        "resource": resource,
        "branch_maps": branch_maps,
        "corrections": corrections,
        "checks": checks,
    }, rows



def teleportation_resource_theorem(stateclass=None):
    """Classify exact deterministic one-bit teleportation resources.

    Architecture: an arbitrary reversible 4x4 analyzer acts on the unknown bit
    and Alice's half of a two-party resource M. A computational outcome m
    selects one analyzer row r_m; reshaping that row into a 2x2 matrix R_m
    gives the receiver branch map

        T_m = M^T R_m^T.

    Therefore det(T_m)=det(M) det(R_m). An exact linear correction C_m with
    C_m T_m = I forces det(T_m) to be a unit, hence det(M) is a unit. Conversely
    the embedded-F2 Bell analyzer used by teleportation_protocol has four
    invertible reshaped rows, so every invertible M works on all four outcomes.
    """
    # Reuse the explicit Bell analyzer from the universal protocol.
    KX = matmul(K_SHEAR_UPPER, X2, 2)
    bell_mats = (I2, X2, K_SHEAR_UPPER, KX)
    Q = tuple(bell_mats[j][i] for i in range(4) for j in range(4))
    A = inverse_matrix(Q, 4)
    assert A is not None

    row_mats = []
    for m in range(4):
        row = tuple(A[4*m + j] for j in range(4))
        R = (row[0], row[1], row[2], row[3])
        row_mats.append(R)
    assert all(is_invertible2(R) for R in row_mats)

    rows = []
    successes = 0
    for M in product(range(16), repeat=4):
        d = det2(M)
        determinant_unit = d in UNITS
        branch_maps = _teleport_branch_maps(A, M)
        fixed_analyzer_success = all(is_invertible2(T) for T in branch_maps)
        # The theorem predicts exact equivalence for the chosen analyzer.
        assert fixed_analyzer_success == determinant_unit
        if fixed_analyzer_success:
            successes += 1
        cls = None if stateclass is None else stateclass[M]
        rows.append({
            "m00": M[0], "m01": M[1], "m10": M[2], "m11": M[3],
            "det": d, "det_is_unit": int(determinant_unit),
            "smith_a": "" if cls is None else cls[0],
            "smith_b": "" if cls is None else cls[1],
            "fixed_bell_analyzer_all_branches_invertible": int(fixed_analyzer_success),
            "universal_exact_teleportation_resource": int(determinant_unit),
        })

    # Exhaustive scalar unit/nonunit ideal check used by the impossibility step:
    # a nonunit times any scalar can never be a unit in this finite local ring.
    nonunits = tuple(x for x in range(16) if x not in UNITS)
    nonunit_absorption_checks = 0
    for a in nonunits:
        for b in range(16):
            assert star(a, b) not in UNITS
            nonunit_absorption_checks += 1

    return {
        "criterion": "universal exact deterministic teleportation iff det(resource) is a unit iff Smith class is (0,0)",
        "fixed_analyzer": A,
        "fixed_analyzer_reshaped_rows": tuple(row_mats),
        "fixed_analyzer_row_determinants": tuple(det2(R) for R in row_mats),
        "all_fixed_analyzer_rows_invertible": all(is_invertible2(R) for R in row_mats),
        "resource_states_checked": len(rows),
        "successful_resource_states": successes,
        "nonunit_absorption_checks": nonunit_absorption_checks,
    }, rows


def teleportation_resource_smith_summary(resource_rows):
    grouped = {}
    for r in resource_rows:
        if r["smith_a"] == "":
            continue
        key = (int(r["smith_a"]), int(r["smith_b"]))
        g = grouped.setdefault(key, {"state_count":0, "teleportation_resource_count":0})
        g["state_count"] += 1
        g["teleportation_resource_count"] += int(r["universal_exact_teleportation_resource"])
    out = []
    for (a,b),g in sorted(grouped.items()):
        out.append({
            "smith_a":a, "smith_b":b,
            "state_count":g["state_count"],
            "universal_exact_teleportation_resources":g["teleportation_resource_count"],
            "all_states_teleportation_capable":int(g["teleportation_resource_count"] == g["state_count"] and g["state_count"] > 0),
            "teleportation_capable_class":int((a,b) == (0,0)),
        })
    return out



def _residue_bit(a: int) -> int:
    """Image of a ring element in A/(u) ~= F2.

    In the E0,E1,E2,E3 bit encoding this is the parity of coefficients.
    """
    return a.bit_count() & 1


def _residue_rank2(M):
    b = tuple(_residue_bit(x) for x in M)
    if not any(b):
        return 0
    if (b[0] & b[3]) ^ (b[1] & b[2]):
        return 2
    return 1


def _f2_vec4_mask(R):
    return sum((_residue_bit(R[i]) << i) for i in range(4))


def _f2_rank_vec4(rows):
    xs = [_f2_vec4_mask(R) for R in rows]
    rank = 0
    for bit in range(4):
        pivot = next((j for j in range(rank, len(xs)) if (xs[j] >> bit) & 1), None)
        if pivot is None:
            continue
        xs[rank], xs[pivot] = xs[pivot], xs[rank]
        for j in range(len(xs)):
            if j != rank and ((xs[j] >> bit) & 1):
                xs[j] ^= xs[rank]
        rank += 1
    return rank


def _left_correction_to_target(D, R, target):
    """Find C with C D R^T = target, or None.

    The two rows of C are independent two-variable equations, so this searches
    only 2*16^2 row candidates instead of all 16^4 matrices.
    """
    F = matmul(D, transpose(R, 2), 2)
    out_rows = []
    for tr in (target[:2], target[2:]):
        found = None
        for x in range(16):
            for y in range(16):
                z0 = star(x, F[0]) ^ star(y, F[2])
                z1 = star(x, F[1]) ^ star(y, F[3])
                if (z0, z1) == tuple(tr):
                    found = (x, y)
                    break
            if found is not None:
                break
        if found is None:
            return None
        out_rows.extend(found)
    return tuple(out_rows)


def _complete_binary_analyzer_basis(preferred):
    """Complete independent 2x2 F2 row-matrices to a four-row analyzer."""
    chosen = []
    for R in preferred:
        if _f2_rank_vec4(chosen + [R]) > len(chosen):
            chosen.append(R)
    for R in product((0, E0), repeat=4):
        if len(chosen) == 4:
            break
        if _f2_rank_vec4(chosen + [R]) > len(chosen):
            chosen.append(R)
    assert len(chosen) == 4 and _f2_rank_vec4(chosen) == 4
    W = tuple(x for R in chosen for x in R)
    assert inverse_matrix(W, 4) is not None
    return tuple(chosen), W


def _fixed_state_count(K):
    """Number of psi in A^2 fixed by K, using the 8-bit F2 representation."""
    IK = (E0 ^ K[0], K[1], K[2], E0 ^ K[3])
    return 1 << (8 - _rank8(_rows8(IK)))


def singular_teleportation_hierarchy():
    """Classify the main sub-universal teleportation tasks by Smith class.

    Four tasks are separated explicitly:

    * exact unknown-state recovery on the largest common state family;
    * transfer of the canonical Smith quotient, represented by D psi;
    * heralded/postselected exact full-state recovery;
    * activation by local ancillas or finite tensor powers of the resource.

    The modal theory assigns no probabilities, so postselection is reported as
    a count of outcome labels that can be designated successful, not a success
    probability.
    """
    up = _u_power_chain()

    # A reversible analyzer whose four branches all recover the free line
    # L=A e0 for every canonical class (0,b), b>0.  Individual reshaped rows
    # may be singular; only the full 4x4 analyzer must be reversible.
    line_rows = (
        (E0, 0, 0, 0),
        (E0, E0, 0, 0),
        (E0, 0, E0, 0),
        (E0, 0, 0, E0),
    )
    line_analyzer = tuple(x for R in line_rows for x in R)
    assert inverse_matrix(line_analyzer, 4) is not None
    line_projection = (E0, 0, 0, 0)

    # Existing four-invertible-row Bell analyzer, useful for equal-valuation
    # quotient transfer and for checking that every branch keeps the Smith type.
    KX = matmul(K_SHEAR_UPPER, X2, 2)
    bell_mats = (I2, X2, K_SHEAR_UPPER, KX)
    Q = tuple(bell_mats[j][i] for i in range(4) for j in range(4))
    bell_analyzer = inverse_matrix(Q, 4)
    assert bell_analyzer is not None
    bell_rows = tuple(tuple(bell_analyzer[4*m:4*m+4]) for m in range(4))
    assert all(is_invertible2(R) for R in bell_rows)

    binary_rows = tuple(product((0, E0), repeat=4))
    rows = []
    detailed = {}

    for a in range(5):
        for b in range(a, 5):
            D = (up[a], 0, 0, up[b])
            key = f"{a},{b}"

            # Exhaust all 16^4 receiver corrections for the identity branch.
            # The theorem below gives a global analyzer-independent upper bound;
            # this exhaustive check confirms that the bound is attained already
            # on the canonical identity branch.
            max_fixed = 0
            max_fixed_C = None
            for C in product(range(16), repeat=4):
                Kmap = matmul(C, D, 2)
                nfix = _fixed_state_count(Kmap)
                if nfix > max_fixed:
                    max_fixed = nfix
                    max_fixed_C = C
            expected_fixed = 256 if (a, b) == (0, 0) else (16 if a == 0 else 1)
            assert max_fixed == expected_fixed

            # Explicit deterministic free-line protocol for every (0,b), b>0.
            line_ok = False
            if a == 0:
                branch_maps = _teleport_branch_maps(line_analyzer, D)
                line_ok = True
                for Tm in branch_maps:
                    for x in range(16):
                        psi = (x, 0)
                        recv = matvec(Tm, psi, 2)
                        corr = matvec(line_projection, recv, 2)
                        if corr != psi or (x != 0 and recv == (0, 0)):
                            line_ok = False
                            break
                    if not line_ok:
                        break
                assert line_ok

            # Fixed quotient target: D psi.  A successful branch has some C_m
            # satisfying C_m D R_m^T = D.  Reduction modulo u bounds how many
            # successful row matrices can coexist in a reversible analyzer.
            good_binary = []
            good_corrections = {}
            for R in binary_rows:
                C = _left_correction_to_target(D, R, D)
                if C is not None:
                    good_binary.append(tuple(R))
                    good_corrections[tuple(R)] = C
            good_span_rank = _f2_rank_vec4(good_binary)
            preferred = []
            for R in good_binary:
                if _f2_rank_vec4(preferred + [R]) > len(preferred):
                    preferred.append(R)
            max_rows, max_analyzer = _complete_binary_analyzer_basis(preferred)
            achieved = 0
            achieved_corrections = []
            for R in max_rows:
                C = _left_correction_to_target(D, R, D)
                if C is not None:
                    achieved += 1
                    achieved_corrections.append(C)
                    assert matmul(C, matmul(D, transpose(R, 2), 2), 2) == D
                else:
                    achieved_corrections.append(None)
            assert achieved == good_span_rank

            # For the equal-valuation classes the standard Bell analyzer gives
            # deterministic quotient transfer on all four outcomes.
            bell_quotient_success = sum(
                _left_correction_to_target(D, R, D) is not None for R in bell_rows
            )
            if a == b:
                assert bell_quotient_success == 4

            residue_rank = _residue_rank2(D)
            qclasses = 1 << (8 - a - b)
            qbits = 8 - a - b
            if a == 4:
                qtype0 = "0"
            elif a == 0:
                qtype0 = "A"
            else:
                qtype0 = f"A/(u^{4-a})"
            if b == 4:
                qtype1 = "0"
            elif b == 0:
                qtype1 = "A"
            else:
                qtype1 = f"A/(u^{4-b})"
            qtype = f"{qtype0} + {qtype1}"

            # A singular 2x2 matrix has residue-field rank <=1. Tensor powers
            # keep residue rank <=1 (rank multiplicativity), so no finite number
            # of copies can yield a branch with an A-linear left inverse A^2.
            r2 = residue_rank * residue_rank
            r3 = r2 * residue_rank
            finite_copy_activation = int((a, b) == (0, 0))

            row = {
                "smith_a": a,
                "smith_b": b,
                "resource_nonzero": int((a, b) != (4, 4)),
                "resource_separable": int(b == 4),
                "residue_field_rank": residue_rank,
                "universal_exact_full_state": int((a, b) == (0, 0)),
                "max_exact_common_state_family_size": max_fixed,
                "max_exact_common_nonzero_states": max_fixed - 1,
                "max_exact_free_rank": 2 if (a, b) == (0, 0) else (1 if a == 0 else 0),
                "deterministic_free_line_protocol": int(line_ok),
                "canonical_quotient_type": qtype,
                "canonical_quotient_classes": qclasses,
                "canonical_quotient_boolean_bits": qbits,
                "max_fixed_quotient_success_outcomes_of_4": good_span_rank,
                "fixed_quotient_all_four_outcomes": int(good_span_rank == 4),
                "max_universal_exact_postselected_outcomes_of_4": 4 if (a, b) == (0, 0) else 0,
                "residue_rank_two_copies": r2,
                "residue_rank_three_copies": r3,
                "finite_tensor_power_universal_activation": finite_copy_activation,
            }
            rows.append(row)
            detailed[key] = {
                "smith_representative": D,
                "max_fixed_identity_branch_correction": max_fixed_C,
                "good_binary_quotient_rows": good_binary,
                "good_binary_quotient_span_rank": good_span_rank,
                "max_quotient_analyzer_rows": max_rows,
                "max_quotient_analyzer": max_analyzer,
                "max_quotient_analyzer_corrections": achieved_corrections,
                "bell_analyzer_quotient_success_outcomes": bell_quotient_success,
            }

    summary = {
        "exact_restricted_state_theorem": (
            "max common exactly recoverable state family has 256 states for (0,0), "
            "16 states (one free A-line) for (0,b), b>0, and only the zero state when a>0"
        ),
        "fixed_quotient_target": "D psi for canonical Smith D=diag(u^a,u^b)",
        "fixed_quotient_success_pattern": {
            "equal_nonzero_or_full_classes_a_eq_b": 4,
            "offdiagonal_two_nonzero_factors_a_lt_b_lt_4": 2,
            "rank_one_separable_classes_b_eq_4_a_lt_4": 3,
            "zero_class": 4,
        },
        "postselected_full_state_no_go": (
            "every singular resource has zero universally exact correctable analyzer branches"
        ),
        "ancilla_and_multicopy_no_go": (
            "for any singular resource, reduction modulo (u) has rank <=1; local product ancillas "
            "do not change the factorization through the resource, and every finite tensor power "
            "has residue rank <=1, so no branch can have an A-linear left inverse onto A^2"
        ),
        "line_analyzer": line_analyzer,
        "line_analyzer_rows": line_rows,
        "line_projection_correction": line_projection,
        "bell_analyzer": bell_analyzer,
        "bell_analyzer_rows": bell_rows,
        "classes": detailed,
    }
    return summary, rows

def bstar_teleportation_failure():
    Bstar = matmul(CNOT, kron(HSTAR,I2,2,2),4)
    Binv = inverse_matrix(Bstar,4)
    assert Binv is not None
    beta00 = matvec(Bstar,(E0,0,0,0),4)
    branch_maps = _teleport_branch_maps(Binv,beta00)
    return {
        "Bstar": Bstar, "Bstar_inverse": Binv, "resource_beta00": beta00,
        "branch_maps": branch_maps,
        "branch_determinants": tuple(det2(x) for x in branch_maps),
        "all_branch_maps_invertible": all(is_invertible2(x) for x in branch_maps),
    }


def _teleport_branch_maps(analyzer4, resource4):
    O = kron(analyzer4,I2,4,2)
    maps = []
    for m in range(4):
        cols = []
        for inp in range(2):
            v = [0]*8
            for r,rv in enumerate(resource4):
                v[4*inp+r] = rv
            w = matvec(O,tuple(v),8)
            cols.append((w[2*m],w[2*m+1]))
        maps.append((cols[0][0],cols[1][0],cols[0][1],cols[1][1]))
    return tuple(maps)


# --- Smith/local-equivalence classification helpers ---
RHO = []
for a in range(16):
    rows = []
    for out in range(4):
        mask = 0
        for inp in range(4):
            if (MUL[a][1 << inp] >> out) & 1:
                mask |= 1 << inp
        rows.append(mask)
    RHO.append(tuple(rows))


def _rows8(M):
    return tuple(RHO[M[2*i]][p] | (RHO[M[2*i+1]][p] << 4) for i in range(2) for p in range(4))


def _rank8(rows):
    rows = list(rows); rank = 0
    for col in range(8):
        pivot = next((k for k in range(rank,8) if (rows[k] >> col) & 1), None)
        if pivot is not None:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            pr = rows[rank]
            for k in range(rank+1,8):
                if (rows[k] >> col) & 1:
                    rows[k] ^= pr
            rank += 1
    return rank


def smith_class_inventory(gl2_size: int):
    upows = [E0]
    for _ in range(3): upows.append(MUL[upows[-1]][U])
    scaled = [[MUL[upows[j]][a] for a in range(16)] for j in range(4)]
    canonical = {}
    for a in range(5):
        for b in range(a,5):
            da = 0 if a == 4 else upows[a]
            db = 0 if b == 4 else upows[b]
            D = (da,0,0,db)
            sig = tuple(_rank8(_rows8(tuple(scaled[j][x] for x in D))) for j in range(4))
            assert sig not in canonical
            canonical[sig] = (a,b)
    counts = Counter(); inventory = []
    stateclass = {}
    for M in product(range(16),repeat=4):
        sig = tuple(_rank8(_rows8(tuple(scaled[j][x] for x in M))) for j in range(4))
        cls = canonical[sig]
        stateclass[M] = cls; counts[cls] += 1
        inventory.append({"m00":M[0],"m01":M[1],"m10":M[2],"m11":M[3],"smith_a":cls[0],"smith_b":cls[1],"separable_class":int(cls[1]==4)})
    class_rows = []
    for cls in sorted(counts):
        size = counts[cls]
        class_rows.append({
            "smith_a": cls[0], "smith_b": cls[1], "state_count": size,
            "separable_class": int(cls[1] == 4),
            "nonseparable_class": int(cls[1] < 4),
            "local_exact_stabilizer_size": (gl2_size*gl2_size)//size,
        })
    # Exhaustive simple-tensor set and equivalence regression.
    separable = set()
    for x0,x1 in product(range(16),repeat=2):
        for y0,y1 in product(range(16),repeat=2):
            separable.add(outer2((x0,x1),(y0,y1)))
    mismatch = sum((M in separable) != (stateclass[M][1] == 4) for M in stateclass)
    assert mismatch == 0
    summary = {
        "classes": len(class_rows), "separable_classes": sum(r["separable_class"] for r in class_rows),
        "nonseparable_classes": sum(r["nonseparable_class"] for r in class_rows),
        "distinct_separable_states": len(separable),
        "distinct_nonseparable_states": 16**4-len(separable),
        "factorization_class_mismatches": mismatch,
    }
    return inventory, class_rows, stateclass, separable, summary


def basis_permutation_classification(separable_states):
    rows = []
    for p in permutations(range(4)):
        witness = None
        for M in separable_states:
            out = [0]*4
            for i,x in enumerate(M): out[p[i]] = x
            out = tuple(out)
            if out not in separable_states:
                witness = (M,out); break
        rows.append({
            "p0":p[0],"p1":p[1],"p2":p[2],"p3":p[3],
            "preserves_all_separable_states": int(witness is None),
            "can_create_nonseparability": int(witness is not None),
            "witness_input": "" if witness is None else repr(witness[0]),
            "witness_output": "" if witness is None else repr(witness[1]),
        })
    return rows


def ghz_analysis(bases=MQT_BASES, names=MQT_NAMES, a000=E0, a111=E0):
    n = len(bases)
    contexts = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                t = support_table3(a000,a111,bases[i],bases[j],bases[k])
                contexts.append((i,j,k,t))
    assignments = list(product((0,1),repeat=3*n))
    good = []
    for q in assignments:
        if all(t[4*q[i]+2*q[n+j]+q[2*n+k]] for i,j,k,t in contexts):
            good.append(q)
    uncovered = []
    for i,j,k,t in contexts:
        for idx,possible in enumerate(t):
            if not possible: continue
            o = (idx>>2,(idx>>1)&1,idx&1)
            if not any(q[i]==o[0] and q[n+j]==o[1] and q[2*n+k]==o[2] for q in good):
                uncovered.append((i,j,k,o))
    rows = []
    for i,j,k,t in contexts:
        for idx,possible in enumerate(t):
            rows.append({
                "A":names[i],"B":names[j],"C":names[k],
                "outA":idx>>2,"outB":(idx>>1)&1,"outC":idx&1,
                "possible":possible,
            })
    min_unsat = None
    if not good and len(assignments) <= 1024 and len(contexts) <= 30:
        masks = []; full = (1 << len(assignments))-1
        for i,j,k,t in contexts:
            mask = 0
            for qi,q in enumerate(assignments):
                if t[4*q[i]+2*q[n+j]+q[2*n+k]]:
                    mask |= 1 << qi
            masks.append(mask)
        for r in range(1, min(7,len(contexts)+1)):
            found = None
            for comb in combinations(range(len(contexts)),r):
                m = full
                for x in comb: m &= masks[x]
                if not m:
                    found = comb; break
            if found is not None:
                min_unsat = [
                    {"A":names[contexts[x][0]],"B":names[contexts[x][1]],"C":names[contexts[x][2]],"table":contexts[x][3]}
                    for x in found
                ]
                break
    return {
        "global_assignments": len(good),
        "uncovered_possible_sections": len(uncovered),
        "minimum_unsat_context_count": None if min_unsat is None else len(min_unsat),
        "minimum_unsat_contexts": min_unsat,
    }, rows


def verify_known_structures():
    C = C_SHEAR_LOWER
    H = HSTAR
    Bstar = matmul(CNOT,kron(H,I2,2,2),4)
    chi = (E0,4)
    Xchi = matvec(X2,chi,2)
    zchi = tuple(MUL[4][x] for x in chi)

    # 4x4 regular representation of multiplication by t=E1 on the CM basis.
    P = (
        0,0,0,E0,
        E0,0,0,0,
        0,E0,0,0,
        0,0,E0,0,
    )
    P2 = matmul(P,P,4)
    P4 = matmul(P2,P2,4)
    Pinv = inverse_matrix(P,4)

    basis4 = tuple(tuple(E0 if i == j else 0 for i in range(4)) for j in range(4))
    bstar_basis_outputs = tuple(matvec(Bstar,v,4) for v in basis4)

    # Linear identity of Bstar inverse implies action is reversible on all A^4;
    # still do the requested exhaustive state regression.
    Binv = inverse_matrix(Bstar,4)
    assert Binv is not None
    reversible_checks = 0
    for v in product(range(16),repeat=4):
        assert matvec(Binv,matvec(Bstar,v,4),4) == v
        reversible_checks += 1
    return {
        "C_squared_identity": matmul(C,C,2) == I2,
        "C_basis0": matvec(C,(E0,0),2),
        "Hstar_squared_identity": matmul(H,H,2) == I2,
        "Hstar_dagger_Hstar_identity": matmul(tuple(bar(x) for x in transpose(H,2)),H,2) == I2,
        "Hstar_basis0": matvec(H,(E0,0),2),
        "Hstar_basis1": matvec(H,(0,E0),2),
        "phase_kickback_Xchi_equals_zchi": Xchi == zchi,
        "P_fourth_power_identity": P4 == identity(4),
        "P_transpose_equals_inverse": Pinv is not None and transpose(P,4) == Pinv,
        "Bstar_basis_outputs": bstar_basis_outputs,
        "Bstar_basis_nonzero_branch_counts": tuple(sum(x != 0 for x in v) for v in bstar_basis_outputs),
        "Bstar_reversible_state_checks": reversible_checks,
    }
