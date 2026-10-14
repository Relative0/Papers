"""Bounded-height-two RF-IDENT theorem audit; Python 3.10+, stdlib only.

Independent explicit relative-matrix DP versus the signature criterion and
constructive protocol. No imports from the previous gate's implementations.
Query bit i is the value on vertex i. Endpoints are 0 and n-1.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import random
import time


def vertices(s):
    return [i for i in range(s.bit_length()) if s >> i & 1]


def matrix_safe(n, support, query):
    """Build relative cells from the full induced order, then row-reduce."""
    v = vertices(support)
    z = n - 1
    def less(i, j):
        return i < j and (i == 0 or j == z)
    def bit(i):
        return query >> i & 1
    edges = [(i, j) for i, j in combinations(v, 2)
             if less(i, j) and bit(i) > bit(j)]
    triangles = [(i, j, k) for i, j, k in combinations(v, 3)
                 if less(i, j) and less(j, k)
                 and not bit(i) <= bit(j) <= bit(k)]
    rows = []
    for edge in edges:
        rows.append(sum(1 << col for col, tri in enumerate(triangles)
                        if set(edge).issubset(tri)))
    rank = 0
    for col in range(len(triangles)):
        pivot = next((i for i in range(rank, len(rows))
                      if rows[i] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(rank + 1, len(rows)):
            if rows[i] >> col & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank == len(edges) == len(triangles)


def structural_safe(n, support, query):
    a, z = 1, 1 << (n - 1)
    if support & a and support & z:
        return not query & a or bool(query & z)
    if support & a:
        return not query & a or query & support == support
    if support & z:
        return bool(query & z) or query & support == 0
    return True


def criterion(n, queries):
    """Return the exact decision and a succinct obstruction when negative."""
    z = n - 1
    safe = [q for q in queries if not q & 1 or q >> z & 1]
    for i, j in combinations(range(1, z), 2):
        if all((q >> i & 1) == (q >> j & 1) for q in queries):
            return False, {"kind": "middle_twins", "pair": [i, j]}
    for i in (0, z):
        for j in range(n):
            if i != j and all((q >> i & 1) == (q >> j & 1)
                              for q in safe):
                return False, {"kind": "endpoint_safe_twins", "pair": [i, j]}
    return True, None


def canonical_tree(n, queries):
    """Use only supplied query IDs, in input order; no optimality claim."""
    queries = tuple(queries)
    a, z = 1, 1 << (n - 1)
    def build(s):
        if s.bit_count() <= 1:
            return {"states": vertices(s)}
        for index, q in enumerate(queries):
            if not 0 < (q & s) < s:
                continue
            if s & a and s & z:
                # Peel equal-endpoint tests before any separating test.
                if bool(q & a) != bool(q & z):
                    continue
            elif not structural_safe(n, s, q):
                continue
            return {"query_index": index,
                    "children": [build(s & ~q), build(s & q)]}
        if s & a and s & z:
            for index, q in enumerate(queries):
                if not q & a and q & z:
                    return {"query_index": index,
                            "children": [build(s & ~q), build(s & q)]}
        raise AssertionError(("canonical construction stuck", n, queries, s))
    return build((1 << n) - 1)


def verify_tree(n, queries, tree):
    nodes = 0
    def visit(s, node, used):
        nonlocal nodes
        if "states" in node:
            assert node["states"] == vertices(s) and s.bit_count() == 1
            return 0
        index = node["query_index"]
        assert 0 <= index < len(queries) and index not in used
        q = queries[index]
        assert q & s and s & ~q
        assert matrix_safe(n, s, q)
        nodes += 1
        return 1 + max(visit(s & ~q, node["children"][0], used | {index}),
                       visit(s & q, node["children"][1], used | {index}))
    depth = visit((1 << n) - 1, tree, set())
    assert nodes == n - 1
    return nodes, depth


def matrix_dp(n, queries, safe):
    """Generic feasibility recursion, without the theorem's criterion."""
    @lru_cache(None)
    def solve(s):
        if s.bit_count() <= 1:
            return True
        for q in queries:
            one, zero = s & q, s & ~q
            if one and zero and safe(s, q) and solve(zero) and solve(one):
                return True
        return False
    return solve((1 << n) - 1)


def main():
    started = time.perf_counter()
    counts = {"all_support_query_safety": 0, "exhaustive_libraries": 0,
              "seeded_libraries": 0, "feasible_libraries": 0,
              "protocol_nodes_matrix_checked": 0}
    coverage = []
    # Includes empty/full supports and constants. Each n has one bounded poset.
    for n in range(2, 9):
        for support in range(1 << n):
            for query in range(1 << n):
                assert matrix_safe(n, support, query) == structural_safe(n, support, query)
                counts["all_support_query_safety"] += 1
    print("all support/query matrix checks passed", flush=True)
    rng = random.Random(2026092907)
    examples = {}
    for n in range(2, 11):
        safe = lru_cache(None)(lambda s, q, n=n: matrix_safe(n, s, q))
        effective = range(1, (1 << n) - 1)
        if n <= 4:
            libraries = (tuple(q for j, q in enumerate(effective) if mask >> j & 1)
                         for mask in range(1 << len(effective)))
            kind = "exhaustive_libraries"
        else:
            # Sizes alternate sparse/dense; constants and duplicates are allowed.
            libraries = (tuple(rng.randrange(1 << n)
                               for _ in range(rng.randrange(0, 3 * n + 1)))
                         for _ in range(1500))
            kind = "seeded_libraries"
        cases = positives = 0
        for queries in libraries:
            result, obstruction = criterion(n, queries)
            exact = matrix_dp(n, queries, safe)
            assert result == exact, (n, queries, result, exact, obstruction)
            counts[kind] += 1
            cases += 1
            if result:
                positives += 1
                counts["feasible_libraries"] += 1
                tree = canonical_tree(n, queries)
                nodes, depth = verify_tree(n, queries, tree)
                counts["protocol_nodes_matrix_checked"] += nodes
                if n not in examples:
                    examples[n] = {"n": n, "queries": queries,
                                   "tree": tree, "constructed_depth": depth}
        coverage.append({"n": n, "kind": kind, "cases": cases, "feasible": positives})
        print(coverage[-1], flush=True)
    # The inherited legal-but-destructive first move must remain visible.
    n, queries = 3, (2, 6)  # words 010, 011
    assert criterion(n, queries)[0]
    assert matrix_safe(n, 7, 6)
    assert not matrix_dp(2, (1, 3), lambda s, q: matrix_safe(2, s, q))
    assert not matrix_safe(n, 6, 2)
    tree = canonical_tree(n, queries)
    assert tree["query_index"] == 0
    examples["deactivation"] = {"n": n, "queries": queries, "tree": tree}
    # Descending endpoint tests can still be essential for middle pairs.
    n, queries = 4, (6, 8, 3)  # words 0110, 0001, 1100
    assert criterion(n, queries)[0]
    assert not criterion(n, queries[:-1])[0]
    tree = canonical_tree(n, queries)
    verify_tree(n, queries, tree)
    examples["descending_query_essential"] = {"n": n, "queries": queries, "tree": tree}
    summary = {"status": "all checks passed", "seed": 2026092907,
               "counts": counts, "coverage": coverage,
               "seconds": round(time.perf_counter() - started, 3),
               "limitations": ["One bounded poset per n, not all height-two posets.",
                               "All effective libraries only for n <= 4.",
                               "Larger library samples are seeded, not exhaustive.",
                               "Finite checks do not replace the general proof."]}
    here = Path(__file__).resolve().parent
    (here / "VERIFICATION.json").write_text(json.dumps(summary, indent=2) + "\n")
    (here / "PROTOCOL_EXAMPLES.json").write_text(json.dumps(examples, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
