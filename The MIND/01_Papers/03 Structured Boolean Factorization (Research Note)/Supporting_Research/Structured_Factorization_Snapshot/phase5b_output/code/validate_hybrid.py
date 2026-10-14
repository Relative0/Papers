"""Exhaustive tiny-universe and seeded independent tests of real backends."""
from __future__ import annotations

import argparse
import json
import random
from itertools import combinations, product
from pathlib import Path
from time import perf_counter

from hybrid_core import (FourCornerSession, balanced_tree, brute_partition,
                         canonical, compile_extract, exact_refine, leaves,
                         probe_defects)


def models_for(n, clauses):
    return {x for x in product((0, 1), repeat=n)
            if all(any(x[abs(lit) - 1] == (lit > 0) for lit in cl) for cl in clauses)}


def relation_cut(models, cut, n):
    cut = set(cut)
    left = {tuple(x[v - 1] for v in sorted(cut)) for x in models}
    right = {tuple(x[v - 1] for v in range(1, n + 1) if v not in cut) for x in models}
    return len(models) == len(left) * len(right)


def direct_truth(tree, models, n):
    def recurse(t):
        if isinstance(t, int):
            return [[t]]
        L, R = sorted(leaves(t[0])), sorted(leaves(t[1]))
        M = {tuple(x[v - 1] for v in L + R) for x in models}
        a = {tuple(x[v - 1] for v in L) for x in models}
        b = {tuple(x[v - 1] for v in R) for x in models}
        return recurse(t[0]) + recurse(t[1]) if len(M) == len(a) * len(b) else [sorted(L + R)]
    return canonical(recurse(tree))


def cnf_for_truth(n, mask):
    return [tuple(-(v + 1) if (row >> v) & 1 else v + 1 for v in range(n))
            for row in range(1 << n) if not (mask >> row) & 1]


def independent_lcc(n, *partitions):
    neighbors = {v: {v} for v in range(1, n + 1)}
    for partition in partitions:
        for b in partition:
            for v in b:
                neighbors[v].update(b)
    blocks, unseen = [], set(range(1, n + 1))
    while unseen:
        reached, queue = set(), [min(unseen)]
        while queue:
            v = queue.pop()
            if v not in reached:
                reached.add(v)
                queue.extend(neighbors[v] - reached)
        unseen -= reached
        blocks.append(sorted(reached))
    return canonical(blocks)


def run(output):
    start = perf_counter()
    rng = random.Random(2026092905)
    checks = {"sdd_compilations": 0, "dynamic_minimizations": 0,
              "direct_partition_comparisons": 0, "hybrid_semantic_comparisons": 0,
              "carrier_lcc_comparisons": 0, "sat_cut_comparisons": 0,
              "witness_semantic_checks": 0, "minimality_queries": 0,
              "unsat_sdd_cases": 0}
    samples = []

    def validate(n, clauses, tree, minimize=False, query_cuts=False):
        models = models_for(n, clauses)
        result = compile_extract(n, clauses, tree, minimize=minimize)
        checks["sdd_compilations"] += 1
        checks["dynamic_minimizations"] += int(minimize)
        if not models:
            assert result["satisfiable"] is False and result["direct_partition"] is None
            checks["unsat_sdd_cases"] += 1
            return
        assert result["satisfiable"]
        expected_direct = direct_truth(result["tree"], models, n)
        assert result["direct_partition"] == expected_direct, (n, clauses, result, expected_direct)
        checks["direct_partition_comparisons"] += 1
        truth = brute_partition(n, clauses)
        order = list(range(1, n + 1))
        rng.shuffle(order)
        carrier = [order[i:i + 2] for i in range(0, n, 2)]
        exact = exact_refine(n, clauses, result["direct_partition"], carrier)
        assert exact["semantic_partition"] == truth, (clauses, tree, truth, exact)
        assert exact["partition"] == independent_lcc(n, truth, carrier)
        checks["hybrid_semantic_comparisons"] += 1
        checks["carrier_lcc_comparisons"] += 1
        if query_cuts and n >= 2:
            session = FourCornerSession(n, clauses)
            try:
                for r in range(n - 1):
                    for extra in combinations(range(2, n + 1), r):
                        cut = {1, *extra}
                        model = session.query(cut)
                        assert (model is None) == relation_cut(models, cut, n)
                        checks["sat_cut_comparisons"] += 1
            finally:
                session.close()

    # All truth functions through n=3, every unordered labelled n=3 topology.
    for n in range(1, 4):
        trees = [balanced_tree(range(1, n + 1))] if n < 3 else [(1, (2, 3)), (2, (1, 3)), (3, (1, 2))]
        for mask in range(1 << (1 << n)):
            for ti, tree in enumerate(trees):
                validate(n, cnf_for_truth(n, mask), tree, minimize=(mask % 13 == 0), query_cuts=(ti == 0))

    # Larger random CNFs, random leaf permutations, true/free/literal paths.
    for index in range(100):
        n = rng.randrange(4, 9)
        order = list(range(1, n + 1))
        rng.shuffle(order)
        tree = balanced_tree(order)
        clauses = [tuple(v * rng.choice([-1, 1]) for v in rng.sample(range(1, n + 1), rng.randrange(1, min(4, n) + 1)))
                   for _ in range(rng.randrange(0, 2 * n + 1))]
        validate(n, clauses, tree, minimize=index % 2 == 0, query_cuts=index < 20)
    for tree in [((1, 2), (3, 4)), (4, (3, (2, 1))), ((3, 1), (4, 2))]:
        for clauses in [[], [(1,)], [(1, 2)], [(1, -2), (-1, 2)], [(1, 3), (2, 4)]]:
            validate(4, clauses, tree, query_cuts=True)

    # Defect supports checked against models and prime partition, with all-equal
    # family forcing a genuine nonsingleton support hyperedge on every cut.
    for n in range(3, 9):
        clauses = [c for v in range(2, n + 1) for c in [(-1, v), (1, -v)]]
        cut = list(range(1, n // 2 + 1))
        probe = probe_defects(n, clauses, [cut], shrink=True)
        assert len(probe["witnesses"]) == 1
        witness = probe["witnesses"][0]
        assert witness["final_width"] == n
        assert witness["singleton_must_link"] is None
        samples.append({"n": n, **probe})
        checks["witness_semantic_checks"] += 1
    for index in range(40):
        n = 6
        clauses = [tuple(v * rng.choice([-1, 1]) for v in rng.sample(range(1, n + 1), 3)) for _ in range(8)]
        truth = brute_partition(n, clauses)
        if truth is None:
            continue
        cut = {1, 2, 3}
        session = FourCornerSession(n, clauses)
        try:
            witness = session.witness(cut, shrink=True)
            if witness is None:
                continue
            U, W = set(witness["U"]), set(witness["W"])
            assert any(set(b) & U and set(b) & W for b in truth)
            x0, x1 = witness["x0"], witness["x1"]
            actual = []
            for i, j in product((0, 1), repeat=2):
                assignment = [(x0 if (i if v in cut else j) == 0 else x1)[v - 1] for v in range(1, n + 1)]
                actual.append(int(all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses)))
            assert actual == witness["corners"]
            assert (actual[0] * actual[3]) != (actual[1] * actual[2])
            for v in U | W:
                assert session.query(cut, set(range(1, n + 1)) - (U | W) | {v}) is None
                checks["minimality_queries"] += 1
            checks["witness_semantic_checks"] += 1
        finally:
            session.close()
    report = {"seed": 2026092905, "result": "PASS", "discrepancies": 0,
              "checks": checks, "all_equal_defect_samples": samples,
              "seconds": perf_counter() - start}
    Path(output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "all_equal_defect_samples"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(Path(__file__).resolve().parents[1] / "data" / "hybrid_validation.json"))
    run(parser.parse_args().output)
