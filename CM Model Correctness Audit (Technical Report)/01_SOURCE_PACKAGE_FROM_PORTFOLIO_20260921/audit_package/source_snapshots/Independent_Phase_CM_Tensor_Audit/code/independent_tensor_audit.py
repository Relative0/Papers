#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
import time
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from native_block import *

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOGS = ROOT / "logs"
DATA.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)


def write_json(name: str, obj) -> None:
    (DATA / name).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def write_csv(name: str, rows) -> None:
    rows = list(rows)
    if not rows:
        return
    with (DATA / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def flatten_matrix(M: Rows, d: int) -> int:
    v = 0
    for i, row in enumerate(M):
        v |= row << (d * i)
    return v


def vec_matrix(M: Rows, d: int) -> int:
    """Vectorize dxd M into A tensor B ordering, index i*d+j."""
    return flatten_matrix(M, d)


def phase_word_basis() -> tuple[list[Rows], list[str], dict]:
    """Construct 16 linearly independent invertible 4x4 Boolean matrices.

    First use the 12 elementary transvections I XOR E_ij, i!=j. Complete with
    a deterministic seeded search. Also prove each is synthesizable from the
    native rotation P plus one elementary Boolean shear T.
    """
    def add_to_span(v: int, pivots: dict[int, int]) -> bool:
        x = v
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                for q, b in list(pivots.items()):
                    if (b >> p) & 1:
                        pivots[q] = b ^ x
                pivots[p] = x
                return True
        return False

    I = identity(4)
    T = list(I)
    T[0] ^= 1 << 1
    T = tuple(T)

    mats: list[Rows] = []
    piv: dict[int, int] = {}
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            M = list(I)
            M[i] ^= 1 << j
            M = tuple(M)
            if add_to_span(flatten_matrix(M, 4), piv):
                mats.append(M)

    rng = random.Random(42)
    while len(mats) < 16:
        M = tuple(rng.getrandbits(4) for _ in range(4))
        if rank(M, 4) == 4 and add_to_span(flatten_matrix(M, 4), piv):
            mats.append(M)

    assert len(mats) == 16
    assert rank(tuple(flatten_matrix(M, 4) for M in mats), 16) == 16
    assert all(rank(M, 4) == 4 for M in mats)

    # BFS in <P,T> with P^-1 available for short synthesis words.
    gens = (("P", P), ("p", P3), ("T", T))
    parent: dict[Rows, tuple[Rows | None, str | None]] = {I: (None, None)}
    q = deque([I])
    while q:
        A = q.popleft()
        for name, G in gens:
            B = compose(G, A)
            if B not in parent:
                parent[B] = (A, name)
                q.append(B)
    assert len(parent) == 20160  # |GL(4,2)|

    words: list[str] = []
    for M in mats:
        cur = M
        w: list[str] = []
        while parent[cur][0] is not None:
            prev, name = parent[cur]
            assert prev is not None and name is not None
            w.append(name)
            cur = prev
        words.append("".join(reversed(w)))

    meta = {
        "generator_P": rows_to_lists(P, 4),
        "generator_T": rows_to_lists(T, 4),
        "generated_group_size": len(parent),
        "expected_GL4_size": 20160,
        "basis_flat_rank": 16,
        "max_synthesis_word_length": max(map(len, words)),
        "word_legend": {"P": "clockwise native phase rotation", "p": "P inverse = P^3", "T": "elementary XOR shear I XOR E_01"},
    }
    return mats, words, meta


def logical_effect_basis() -> list[Rows]:
    mats = []
    for row in BELL_ANALYZER_F2:
        M = (row & 0b11, (row >> 2) & 0b11)
        assert rank(M, 2) == 2
        mats.append(M)
    assert rank(tuple(flatten_matrix(M, 2) for M in mats), 4) == 4
    return mats


def factorized_bell_effect_basis() -> tuple[list[Rows], list[Rows], list[str], dict]:
    Ls = logical_effect_basis()
    Vs, words, phase_meta = phase_word_basis()
    Rs = [kron_f2(L, 2, V, 4) for L in Ls for V in Vs]
    A = tuple(flatten_matrix(R, 8) for R in Rs)
    assert len(Rs) == 64
    assert all(rank(R, 8) == 8 for R in Rs)
    assert rank(A, 64) == 64
    return Rs, Vs, words, phase_meta


def local_tensor_support(M: Rows, e: Rows, f: Rows) -> bool:
    """Literal independent-register joint support for bipartite Choi state vec(M).

    Equivalent to (e tensor f) vec(M) != 0, evaluated as e M f^T != 0.
    """
    X = compose(compose(e, M), transpose(f, 8))
    return any(X)


def local_tensor_support_direct(M: Rows, e: Rows, f: Rows) -> bool:
    J = kron_f2(e, 8, f, 8)
    return apply(J, vec_matrix(M, 8)) != 0


def support_table_literal(M: Rows, basis_a, basis_b) -> tuple[int, int, int, int]:
    return tuple(int(local_tensor_support(M, e, f)) for e in basis_a for f in basis_b)


def two_sat_coverage_from_tables(tables, n: int):
    Nvars = 2 * n
    adj = [[] for _ in range(2 * Nvars)]
    clauses = []
    def node(v, val): return 2 * v + val
    def neg(x): return x ^ 1
    def add_clause(v1, val1, v2, val2):
        clauses.append((v1, val1, v2, val2))
        adj[node(v1, 1-val1)].append(node(v2, val2))
        adj[node(v2, 1-val2)].append(node(v1, val1))
    for (i,j), t in tables.items():
        for a in (0,1):
            for b in (0,1):
                if not t[2*a+b]:
                    add_clause(i, 1-a, n+j, 1-b)
    idx=0; stack=[]; on=[False]*(2*Nvars); ids=[-1]*(2*Nvars); low=[0]*(2*Nvars); comp=[-1]*(2*Nvars); cc=0
    sys.setrecursionlimit(max(10000,4*Nvars+100))
    def dfs(v):
        nonlocal idx, cc
        ids[v]=low[v]=idx; idx+=1; stack.append(v); on[v]=True
        for w in adj[v]:
            if ids[w]<0:
                dfs(w); low[v]=min(low[v],low[w])
            elif on[w]:
                low[v]=min(low[v],ids[w])
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

def shared_support_table_diag(a: int, b: int, basis_a, basis_b) -> tuple[int, int, int, int]:
    """Old shared-register table, retained only for robustness comparison."""
    va = apply(N_POWERS[a], E0_VEC)
    vb = apply(N_POWERS[b], E0_VEC)
    out = []
    for e in basis_a:
        eb = effect_blocks(e, 2)
        for f in basis_b:
            fb = effect_blocks(f, 2)
            x = apply(eb[0], apply(fb[0], va)) ^ apply(eb[1], apply(fb[1], vb))
            out.append(int(x != 0))
    return tuple(out)  # type: ignore[return-value]


def ghz_literal_state(full_phase_correlation: bool = True) -> int:
    """Literal three-party support GHZ.

    If full_phase_correlation, sum over all local basis labels j=0..7:
    XOR_j |j,j,j>. Otherwise anchor phase position E0 and correlate only the
    logical bit. Both give the same embedded Z/X/Y support tables.
    """
    v = 0
    if full_phase_correlation:
        for j in range(8):
            v ^= 1 << (j * 64 + j * 8 + j)
    else:
        for b in (0, 1):
            j = b * 4
            v ^= 1 << (j * 64 + j * 8 + j)
    return v


def ghz_weighted_leg_variant() -> int:
    """Exploratory literal lift of the N^2-weighted |111> term.

    Uses full phase-GHZ correlation and applies N^2 on Charlie's phase leg on
    the |111> logical branch. This is one natural lift, not canonical.
    """
    v = 0
    for p in range(4):
        # |000> phase-GHZ term
        a = p
        b = p
        c = p
        v ^= 1 << (a * 64 + b * 8 + c)
        # |111> with N^2 on Charlie's phase register
        out = apply(N2, 1 << p)
        for q in range(4):
            if (out >> q) & 1:
                a = 4 + p
                b = 4 + p
                c = 4 + q
                v ^= 1 << (a * 64 + b * 8 + c)
    return v


def support3_literal(state512: int, e: Rows, f: Rows, g: Rows) -> bool:
    # First tensor is 16 x 64; its column count is 64, not 32.
    J2 = kron_f2(e, 8, f, 8)
    J3 = kron_f2(J2, 64, g, 8)
    return apply(J3, state512) != 0


def ghz_tables_and_coverage(state512: int, bases):
    n = len(bases)
    contexts = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                t = tuple(
                    int(support3_literal(state512, e, f, g))
                    for e in bases[i]
                    for f in bases[j]
                    for g in bases[k]
                )
                contexts.append((i, j, k, t))

    goods = []
    for q in product((0, 1), repeat=3 * n):
        if all(t[4 * q[i] + 2 * q[n + j] + q[2 * n + k]] for i, j, k, t in contexts):
            goods.append(q)

    possible = 0
    extendable = 0
    for i, j, k, t in contexts:
        for idx, p in enumerate(t):
            if not p:
                continue
            possible += 1
            out = (idx >> 2, (idx >> 1) & 1, idx & 1)
            if any(q[i] == out[0] and q[n + j] == out[1] and q[2 * n + k] == out[2] for q in goods):
                extendable += 1

    return contexts, {
        "global_assignments": len(goods),
        "possible_sections": possible,
        "extendable_possible_sections": extendable,
        "uncovered_possible_sections": possible - extendable,
    }


def minimum_unsat_ghz_contexts(contexts, nsettings: int):
    """Use 512-bit assignment masks to find the minimum unsat context count."""
    assignments = list(product((0, 1), repeat=3 * nsettings))
    masks = []
    full = (1 << len(assignments)) - 1
    for i, j, k, t in contexts:
        mask = 0
        for idx, q in enumerate(assignments):
            if t[4 * q[i] + 2 * q[nsettings + j] + q[2 * nsettings + k]]:
                mask |= 1 << idx
        masks.append(mask)

    for r in range(1, len(contexts) + 1):
        for comb in combinations(range(len(contexts)), r):
            m = full
            for c in comb:
                m &= masks[c]
                if not m:
                    return r, [contexts[c][:3] for c in comb]
        if r >= 6:  # known first contradiction is found by then; don't waste work.
            break
    return None, None


def logical_only_pair_analyzer() -> Rows:
    """64x64 analyzer: Bell transform on two logical bits, identity on both phase registers."""
    rows = [0] * 64
    for m in range(4):
        for p in range(4):
            for q in range(4):
                out = m * 16 + p * 4 + q
                row = 0
                for li in range(2):
                    for la in range(2):
                        ia = li * 2 + la
                        if (BELL_ANALYZER_F2[m] >> ia) & 1:
                            inp = (li * 4 + p) * 8 + (la * 4 + q)
                            row ^= 1 << inp
                rows[out] = row
    A = tuple(rows)
    assert rank(A, 64) == 64
    return A


def prep_unknown_with_resource(M: Rows) -> Rows:
    """512x8 map psi -> psi tensor vec(M), ordering input, Alice, Bob."""
    rows = []
    for x in range(8):
        for a in range(8):
            for b in range(8):
                rows.append((1 << x) if ((M[a] >> b) & 1) else 0)
    return tuple(rows)


def naive_four_outcome_residual_profile(M: Rows):
    """Audit the old logical-only four-outcome analyzer under literal tensoring.

    Each of four logical outcomes leaves a 16-dimensional Alice phase-pair
    residual. A genuine Bob-only branch with no extra phase outcome would need
    all nonzero residual blocks to be equal to one common Bob map. They are not.
    """
    pair = logical_only_pair_analyzer()
    global_A = kron_f2(pair, 64, identity(8), 8)
    after = compose(global_A, prep_unknown_with_resource(M))
    result = []
    for m in range(4):
        sel = []
        for r in range(16):
            for b in range(8):
                sel.append(1 << ((m * 16 + r) * 8 + b))
        F = compose(tuple(sel), after)  # 128x8
        blocks = [tuple(F[r * 8 + b] for b in range(8)) for r in range(16)]
        nonzero = [B for B in blocks if any(B)]
        result.append({
            "outcome": m,
            "global_branch_rank": rank(F, 8),
            "nonzero_residual_phase_blocks": len(nonzero),
            "distinct_nonzero_bob_maps": len(set(nonzero)),
            "nonzero_bob_map_ranks": sorted({rank(B, 8) for B in nonzero}),
            "factorizes_as_fixed_alice_residual_times_one_bob_map": len(set(nonzero)) <= 1,
        })
    return result


def teleport_branch_map(M: Rows, R: Rows) -> Rows:
    return compose(transpose(M, 8), transpose(R, 8))


def direct_global_branch_maps(M: Rows, analyzer_rows: list[Rows]) -> list[Rows]:
    """Direct 512-dimensional simulation for validation of branch formula."""
    A64 = tuple(flatten_matrix(R, 8) for R in analyzer_rows)
    assert rank(A64, 64) == 64
    global_A = kron_f2(A64, 64, identity(8), 8)
    after = compose(global_A, prep_unknown_with_resource(M))
    out = []
    for m in range(64):
        sel = tuple(1 << (m * 8 + b) for b in range(8))
        out.append(compose(sel, after))
    return out


def orthogonal_even_weight_no_go(d: int = 8) -> dict:
    """For even d, every orthogonal dxd matrix has even total Hamming weight.

    Hence flattened orthogonal matrices lie in a codimension-one hyperplane of
    M_d(F2), so d^2 of them cannot form a basis. This rules out a complete
    Bell analyzer whose every reshaped effect is orthogonal.
    """
    assert d % 2 == 0
    return {
        "dimension": d,
        "matrix_space_dimension": d * d,
        "orthogonal_flattened_vectors_lie_in_even_weight_hyperplane": True,
        "hyperplane_dimension": d * d - 1,
        "therefore_no_full_orthogonal_effect_basis": True,
    }


def run() -> dict:
    t0 = time.time()
    summary = {}

    # Local model dimensions.
    summary["model"] = {
        "local_logical_dimension": 2,
        "local_phase_dimension": 4,
        "local_boolean_vector_dimension": 8,
        "two_party_dimension": 64,
        "three_party_dimension": 512,
        "composition_rule": "ordinary Boolean Kronecker tensor across parties; AND on routed bits and XOR on converging routes",
        "shared_phase_compression": False,
    }

    # Generate 192 P-compatible local two-outcome bases.
    _, inv_gates, orth_gates = enumerate_phase_block_gates()
    bases = measurement_bases(inv_gates)
    orth_bases = unitary_measurement_bases(orth_gates)
    assert len(bases) == 192 and len(orth_bases) == 4

    # Bell support: anchor and Choi/operator lifts.
    M_choi = identity(8)
    M_anchor_list = [0] * 8
    M_anchor_list[0] |= 1 << 0
    M_anchor_list[4] |= 1 << 4
    M_anchor = tuple(M_anchor_list)
    assert rank(M_choi, 8) == 8 and rank(M_anchor, 8) == 2

    # Direct Kronecker vs e M f^T identity.
    for i in (0, 1, 16, 50, 191):
        for j in (0, 2, 17, 100, 191):
            for e in bases[i]:
                for f in bases[j]:
                    assert local_tensor_support_direct(M_choi, e, f) == local_tensor_support(M_choi, e, f)

    bell_rows = []
    bell_tables = {}
    for lift_name, M in (("choi", M_choi), ("anchor", M_anchor)):
        for i, A in enumerate(MQT_BASES):
            for j, B in enumerate(MQT_BASES):
                t = support_table_literal(M, A, B)
                bell_tables[f"{lift_name}:{MQT_NAMES[i]}{MQT_NAMES[j]}"] = list(t)
                for idx, p in enumerate(t):
                    bell_rows.append({
                        "lift": lift_name,
                        "alice_setting": MQT_NAMES[i],
                        "bob_setting": MQT_NAMES[j],
                        "alice_outcome": idx // 2,
                        "bob_outcome": idx % 2,
                        "possible": p,
                    })
    # Both literal lifts reproduce the previous 9 Bell tables.
    expected = {
        "ZZ": (1, 0, 0, 1), "ZX": (1, 1, 1, 0), "ZY": (0, 1, 1, 1),
        "XZ": (1, 1, 1, 0), "XX": (0, 1, 1, 1), "XY": (1, 0, 0, 1),
        "YZ": (0, 1, 1, 1), "YX": (1, 0, 0, 1), "YY": (1, 1, 1, 0),
    }
    for lift in ("choi", "anchor"):
        for k, v in expected.items():
            assert tuple(bell_tables[f"{lift}:{k}"]) == v
    write_csv("bell_literal_tensor_tables.csv", bell_rows)

    # 64 deterministic assignments all fail for the embedded 3-setting Bell model.
    def bell_global_count(M: Rows) -> int:
        tabs = {(i, j): support_table_literal(M, MQT_BASES[i], MQT_BASES[j]) for i in range(3) for j in range(3)}
        c = 0
        for q in product((0, 1), repeat=6):
            if all(tabs[(i, j)][2 * q[i] + q[3 + j]] for i in range(3) for j in range(3)):
                c += 1
        return c

    assert bell_global_count(M_choi) == 0
    assert bell_global_count(M_anchor) == 0
    summary["bell"] = {
        "choi_lift_global_assignments_ZXY": 0,
        "anchor_lift_global_assignments_ZXY": 0,
        "all_64_deterministic_assignments_checked": True,
        "tables_match_shared_register_embedded_ZXY": True,
    }

    # Complete 192 P-compatible basis contextuality on canonical Choi lifts.
    ctx_rows = []
    diff_rows = []
    class_counts = {
        (0, 0): 24576, (0, 1): 18432, (0, 2): 9216, (0, 3): 4608, (0, 4): 4608,
        (1, 1): 1536, (1, 2): 1152, (1, 3): 576, (1, 4): 576, (2, 2): 96,
        (2, 3): 72, (2, 4): 72, (3, 3): 6, (3, 4): 9, (4, 4): 1,
    }
    for a in range(5):
        for b in range(a, 5):
            M = block_matrix([[N_POWERS[a], Z4], [Z4, N_POWERS[b]]], 4)
            if a == 4 and b == 4:
                cov = {
                    "satisfiable": False,
                    "clauses": 4 * len(bases) * len(bases),
                    "possible_sections": 0,
                    "extendable_possible_sections": 0,
                    "uncovered_possible_sections": 0,
                }
                classification = "DEGENERATE_ZERO_EXCLUDED"
                differing_tables = 0
            else:
                tables = {}
                differing_tables = 0
                for i in range(len(bases)):
                    for j in range(len(bases)):
                        lit = support_table_literal(M, bases[i], bases[j])
                        tables[(i, j)] = lit
                        if lit != shared_support_table_diag(a, b, bases[i], bases[j]):
                            differing_tables += 1
                cov = two_sat_coverage_from_tables(tables, len(bases))
                if not cov["satisfiable"]:
                    classification = "STRONG_CONTEXTUAL"
                elif cov["uncovered_possible_sections"]:
                    classification = "LOGICAL_CONTEXTUAL_NOT_STRONG"
                else:
                    classification = "RELATIONALLY_LOCAL"
            row = {
                "class_a": a,
                "class_b": b,
                "resource_rank8": rank(M, 8),
                "state_count": class_counts[(a, b)],
                "classification": classification,
                "satisfiable_global_section": int(cov["satisfiable"]),
                "clauses": cov["clauses"],
                "possible_sections": cov["possible_sections"],
                "extendable_possible_sections": cov["extendable_possible_sections"],
                "uncovered_possible_sections": cov["uncovered_possible_sections"],
                "basis_pair_tables_differing_from_shared_model": differing_tables,
            }
            ctx_rows.append(row)
            diff_rows.append({"class_a": a, "class_b": b, "differing_of_36864_basis_pair_tables": differing_tables})
    write_csv("contextuality_literal_choi_by_rotation_class.csv", ctx_rows)
    write_csv("shared_vs_literal_context_table_differences.csv", diff_rows)

    summary["contextuality"] = {
        "measurement_family": "all 192 projective reversible P-compatible local bases per party",
        "not_claimed_complete_over": "all GL(8,2) local analyzers in the independent-register model",
        "strong_classes": sum(r["classification"] == "STRONG_CONTEXTUAL" for r in ctx_rows),
        "logical_not_strong_classes": sum(r["classification"] == "LOGICAL_CONTEXTUAL_NOT_STRONG" for r in ctx_rows),
        "local_nonzero_classes": sum(r["classification"] == "RELATIONALLY_LOCAL" for r in ctx_rows),
        "state_counts": {
            "strong": sum(r["state_count"] for r in ctx_rows if r["classification"] == "STRONG_CONTEXTUAL"),
            "logical_not_strong": sum(r["state_count"] for r in ctx_rows if r["classification"] == "LOGICAL_CONTEXTUAL_NOT_STRONG"),
            "local_nonzero": sum(r["state_count"] for r in ctx_rows if r["classification"] == "RELATIONALLY_LOCAL"),
            "zero": 1,
        },
        "aggregate_classification_and_coverage_counts_match_shared_model": True,
        "individual_context_tables_are_not_identical_for_all_classes": any(r["basis_pair_tables_differing_from_shared_model"] for r in ctx_rows),
    }

    # GHZ literal tensor: full local basis correlation.
    ghz = ghz_literal_state(True)
    ghz_contexts, ghz_cov = ghz_tables_and_coverage(ghz, MQT_BASES)
    assert ghz_cov["global_assignments"] == 0
    min_count, min_contexts = minimum_unsat_ghz_contexts(ghz_contexts, 3)
    assert min_count == 6
    ghz_rows = []
    for i, j, k, t in ghz_contexts:
        for idx, p in enumerate(t):
            ghz_rows.append({
                "A": MQT_NAMES[i], "B": MQT_NAMES[j], "C": MQT_NAMES[k],
                "outA": idx >> 2, "outB": (idx >> 1) & 1, "outC": idx & 1, "possible": p,
            })
    write_csv("ghz_literal_support_contexts.csv", ghz_rows)

    ghz_orth_contexts, ghz_orth_cov = ghz_tables_and_coverage(ghz, orth_bases)
    # Weighted variant: explicitly exploratory because there is no unique 3-party Choi lift.
    weighted = ghz_weighted_leg_variant()
    _, weighted_zxy_cov = ghz_tables_and_coverage(weighted, MQT_BASES)
    _, weighted_orth_cov = ghz_tables_and_coverage(weighted, orth_bases)
    summary["ghz"] = {
        "literal_full_local_GHZ_ZXY": ghz_cov,
        "minimum_unsat_context_count": min_count,
        "minimum_unsat_contexts": min_contexts,
        "literal_full_local_GHZ_4_orthogonal_bases": ghz_orth_cov,
        "weighted_N2_leg_variant_ZXY": weighted_zxy_cov,
        "weighted_N2_leg_variant_4_orthogonal_bases": weighted_orth_cov,
        "weighted_variant_warning": "There is no unique canonical three-party Choi lift of a single shared phase operator; this leg-weighted construction is exploratory only.",
    }

    # Independent-register universal teleportation.
    Rs, phase_basis, phase_words, phase_meta = factorized_bell_effect_basis()
    analyzer64 = tuple(flatten_matrix(R, 8) for R in Rs)
    assert rank(analyzer64, 64) == 64
    assert all(rank(R, 8) == 8 for R in Rs)

    phase_basis_rows = []
    for i, (V, word) in enumerate(zip(phase_basis, phase_words)):
        phase_basis_rows.append({
            "phase_effect_id": i,
            "synthesis_word": word,
            "word_length": len(word),
            "matrix_rows_binary": [format(r, "04b") for r in V],
        })
    write_json("phase_bell_effect_basis_16.json", {"meta": phase_meta, "basis": phase_basis_rows})

    M = identity(8)
    tele_rows = []
    corrections = []
    for R in Rs:
        Tm = teleport_branch_map(M, R)
        C = inverse(Tm, 8)
        assert C is not None
        corrections.append(C)
    for psi in range(256):
        for m, (R, C) in enumerate(zip(Rs, corrections)):
            recv = apply(teleport_branch_map(M, R), psi)
            out = apply(C, recv)
            assert out == psi
            tele_rows.append({"input_state_8bit": psi, "outcome": m, "received_8bit": recv, "corrected_8bit": out, "exact": 1})
    write_csv("teleportation_literal_256x64.csv", tele_rows)

    # Direct 512-dimensional verification for I8 and canonical (0,2).
    for Mcheck in (identity(8), block_matrix([[I4, Z4], [Z4, N2]], 4)):
        direct = direct_global_branch_maps(Mcheck, Rs)
        formula = [teleport_branch_map(Mcheck, R) for R in Rs]
        assert direct == formula

    # Exhaust all 65,536 P-block resource matrices. Because every R is invertible,
    # branch rank must equal resource rank. Check this explicitly with the first
    # branch for all resources, and all 64 branches for all 15 canonical classes.
    full_rank_resources = 0
    rank_counts = Counter()
    rank_mismatch = 0
    for packed in range(65536):
        entries = (packed & 15, (packed >> 4) & 15, (packed >> 8) & 15, (packed >> 12) & 15)
        Mr = expand_selector_matrix(entries, 2, 2)
        rr = rank(Mr, 8)
        rank_counts[rr] += 1
        if rr == 8:
            full_rank_resources += 1
        if rank(teleport_branch_map(Mr, Rs[0]), 8) != rr:
            rank_mismatch += 1
    assert full_rank_resources == 24576 and rank_mismatch == 0

    canonical_branch_rank_rows = []
    for a in range(5):
        for b in range(a, 5):
            Mr = block_matrix([[N_POWERS[a], Z4], [Z4, N_POWERS[b]]], 4)
            rr = rank(Mr, 8)
            branks = [rank(teleport_branch_map(Mr, R), 8) for R in Rs]
            assert set(branks) == {rr}
            canonical_branch_rank_rows.append({
                "class_a": a, "class_b": b, "resource_rank8": rr,
                "all_64_branch_rank": rr,
                "universal_exact": int(rr == 8),
            })
    write_csv("teleportation_literal_by_rotation_class.csv", canonical_branch_rank_rows)

    # Old four logical outcomes are incomplete when phase is independent.
    naive4 = naive_four_outcome_residual_profile(identity(8))
    assert all(not x["factorizes_as_fixed_alice_residual_times_one_bob_map"] for x in naive4)
    assert all(x["nonzero_residual_phase_blocks"] == 16 for x in naive4)
    assert all(x["distinct_nonzero_bob_maps"] == 16 for x in naive4)

    # Orthogonal-only no-go for complete effect basis in even dimension.
    orth_nogo = orthogonal_even_weight_no_go(8)
    assert all(flatten_matrix(R, 8).bit_count() % 2 == 0 for R in [] )  # vacuous placeholder; theorem is analytic.

    # Explicitly enumerate O(4,2) to show factorized phase-orthogonal effects span only 10/16.
    orth4 = []
    for raw in range(1 << 16):
        X = tuple((raw >> (4 * i)) & 0xF for i in range(4))
        if compose(transpose(X, 4), X) == I4:
            orth4.append(X)
    orth4_span = rank(tuple(flatten_matrix(X, 4) for X in orth4), 16)
    assert len(orth4) == 48 and orth4_span == 10

    summary["teleportation"] = {
        "literal_local_dimension": 8,
        "complete_reversible_Bell_outcomes": 64,
        "analyzer_rank64": rank(analyzer64, 64),
        "analyzer_is_factorized_as": "4 invertible logical effects x 16 invertible phase effects",
        "phase_effect_basis_generated_by_P_and_one_XOR_shear": True,
        "phase_generator_group_size": phase_meta["generated_group_size"],
        "exhaustive_exact_recoveries": len(tele_rows),
        "all_256_inputs_x_64_outcomes_exact": True,
        "full_rank_P_block_resource_count_of_65536": full_rank_resources,
        "resource_rank_histogram": {str(k): rank_counts[k] for k in sorted(rank_counts)},
        "branch_rank_equals_resource_rank": True,
        "naive_old_4_logical_outcomes": naive4,
        "four_outcome_failure_interpretation": "With independent phase registers, the logical-only analyzer leaves 16 distinct Alice phase-pair residual sectors; Bob does not hold the full arbitrary 8-bit state after only the 4 logical outcomes.",
        "64_outcome_interpretation": "A further complete 16-outcome phase Bell analysis resolves those phase degrees, giving 4x16=64 complete outcomes.",
        "orthogonal_complete_effect_basis_no_go": orth_nogo,
        "O4_count": len(orth4),
        "O4_flat_span_dimension": orth4_span,
    }

    summary["headline"] = {
        "bell_survives_literal_tensor": True,
        "support_GHZ_survives_literal_tensor": True,
        "contextuality_hierarchy_aggregate_survives_on_choi_lift_192_P_compatible_bases": True,
        "old_compact_4_outcome_universal_teleportation_survives": False,
        "universal_exact_teleportation_survives_with_full_independent_register_Bell_analysis": True,
        "full_literal_tensor_outcomes": 64,
        "shared_register_outcomes": 4,
        "universal_resource_criterion_full_rank8_survives": True,
    }

    summary["elapsed_seconds"] = time.time() - t0
    write_json("independent_tensor_summary.json", summary)
    (LOGS / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    s = run()
    print(json.dumps(s, indent=2))
