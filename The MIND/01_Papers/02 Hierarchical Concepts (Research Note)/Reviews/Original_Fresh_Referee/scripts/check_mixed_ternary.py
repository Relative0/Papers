"""Independent bounded tree-group regression for Paper U v0.2.

Pure standard library. Reconstructs Aut(T_3,2) by permutation-group closure,
not by the asserted order formula; computes stabilizers by cylinder tests.
Its finite action on a nonuniform truncation below an uneven old frontier
tests mixed h_s, h_s=0, nonnormality, and pointwise/setwise confusion.
Run: python check_mixed_ternary.py --out OUTPUT_DIRECTORY
"""
import argparse
from collections import deque
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def words(m, depth):
    return tuple("".join(map(str, p)) for p in product(range(m), repeat=depth))


def compose(a, b):
    """a after b, acting on indices."""
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    result = [0] * len(a)
    for i, j in enumerate(a):
        result[j] = i
    return tuple(result)


def generators(leaves, m):
    depth = len(leaves[0])
    index = {word: i for i, word in enumerate(leaves)}
    result = []
    for level in range(depth):
        for vertex in words(m, level):
            for child in range(m - 1):
                perm = []
                for leaf in leaves:
                    image = leaf
                    if leaf.startswith(vertex):
                        digit = int(leaf[level])
                        if digit in (child, child + 1):
                            image = leaf[:level] + str(2 * child + 1 - digit) + leaf[level + 1:]
                    perm.append(index[image])
                result.append((f"swap {vertex or 'root'}:{child}<->{child+1}", tuple(perm)))
    return result


def closure(gens, size):
    identity = tuple(range(size))
    seen = {identity}
    todo = deque([identity])
    while todo:
        item = todo.popleft()
        for gen in gens:
            new = compose(gen, item)
            if new not in seen:
                seen.add(new)
                todo.append(new)
    return sorted(seen)


def cells(frontier, leaves):
    return tuple(frozenset(i for i, leaf in enumerate(leaves) if leaf.startswith(v)) for v in frontier)


def fixes_cells(perm, partition):
    return all(frozenset(perm[i] for i in cell) == cell for cell in partition)


def stabilizes_partition(perm, partition):
    return {frozenset(perm[i] for i in cell) for cell in partition} == set(partition)


def internal(frontier):
    return {word[:i] for word in frontier for i in range(len(word))}


def frontier_of(split_vertices, m):
    result = []
    todo = [""]
    while todo:
        v = todo.pop()
        if v in split_vertices:
            todo.extend(v + str(i) for i in range(m))
        else:
            result.append(v)
    return tuple(sorted(result))


def relative_report(frontier, group, gens, leaves):
    partition = cells(frontier, leaves)
    subgroup = [g for g in group if fixes_cells(g, partition)]
    subgroup_set = set(subgroup)
    setwise = [g for g in group if stabilizes_partition(g, partition)]
    witness = None
    conjugation_tests = 0
    for name, g in gens:
        gi = inverse(g)
        for h in subgroup:
            conjugation_tests += 1
            conjugate = compose(compose(g, h), gi)
            if conjugate not in subgroup_set:
                witness = {
                    "ambient_generator": name,
                    "g": {x: leaves[g[i]] for i, x in enumerate(leaves)},
                    "h": {x: leaves[h[i]] for i, x in enumerate(leaves)},
                    "g_h_g_inverse": {x: leaves[conjugate[i]] for i, x in enumerate(leaves)},
                }
                break
        if witness:
            break
    index = len(group) // len(subgroup)
    normal = witness is None
    predicted_normal = len({len(v) for v in frontier}) == 1
    assert index == 6 ** len(internal(frontier))
    assert normal == predicted_normal
    return {
        "relative_frontier": frontier,
        "ambient_order_enumerated": len(group),
        "pointwise_vertex_stabilizer_order_enumerated": len(subgroup),
        "setwise_frontier_stabilizer_order_enumerated": len(setwise),
        "index_observed": index,
        "split_count": len(internal(frontier)),
        "normality_observed_by_conjugation": normal,
        "conjugation_tests": conjugation_tests,
        "nonnormal_witness": witness,
    }


def mixed_case(name, old, refinements, reports):
    new = tuple(sorted(s + t for s in old for t in refinements[s]))
    n = len(internal(new) - internal(old))
    ambient_order = 1
    subgroup_order = 1
    normal = True
    for s in old:
        r = reports[tuple(refinements[s])]
        ambient_order *= r["ambient_order_enumerated"]
        subgroup_order *= r["pointwise_vertex_stabilizer_order_enumerated"]
        normal = normal and r["normality_observed_by_conjugation"]
    observed_index = ambient_order // subgroup_order
    assert observed_index == 6 ** n
    return {
        "name": name,
        "old_frontier": old,
        "old_absolute_depths": sorted({len(s) for s in old}),
        "new_frontier": new,
        "refinements_by_old_cell": refinements,
        "new_absolute_depths": sorted({len(s) for s in new}),
        "finite_action": "product of explicitly enumerated Aut(T_3,2) factors, one below each old cell; 45 terminal nodes",
        "ambient_product_order": ambient_order,
        "stabilizer_product_order": subgroup_order,
        "index_observed_from_enumerated_factors": observed_index,
        "N_computed_directly_from_global_frontiers": n,
        "index_predicted": 6 ** n,
        "normality_observed_from_exhaustive_factor_conjugation": normal,
    }


def appendix_tests(m, depth):
    def all_frontiers(d):
        if d == 0:
            return [("",)]
        below = all_frontiers(d - 1)
        result = [("",)]
        for choices in product(below, repeat=m):
            result.append(tuple(str(i) + word for i, front in enumerate(choices) for word in front))
        return result

    frontiers = all_frontiers(depth)
    leaves = words(m, depth)
    for f in frontiers:
        assert sum(Fraction(1, m ** len(s)) for s in f) == 1
        assert len(f) == 1 + (m - 1) * len(internal(f))
    ideals = {frozenset(internal(f)): f for f in frontiers}
    for a, b in product(ideals, repeat=2):
        assert a | b in ideals and a & b in ideals
    counts = []
    sample_tests = 0
    for sample_size in range(len(leaves) + 1):
        for sample in combinations(leaves, sample_size):
            split = {v for level in range(depth) for v in words(m, level)
                     if sum(s.startswith(v) for s in sample) >= 2}
            candidate = frontier_of(split, m)
            separates = [f for f in frontiers if all(sum(s.startswith(v) for s in sample) <= 1 for v in f)]
            assert candidate in separates
            assert all(split <= internal(f) for f in separates)
            assert len(candidate) == min(map(len, separates))
            assert sum(len(f) == len(candidate) for f in separates) == 1
            if sample_size <= 1:
                assert candidate == ("",)
            sample_tests += 1
            counts.append(len(candidate))
    return {"m": m, "depth": depth, "frontiers": len(frontiers),
            "lattice_pairs": len(frontiers) ** 2, "sample_subsets": sample_tests,
            "empty_and_singleton_cases": len(leaves) + 1,
            "minimum_leaf_range": [min(counts), max(counts)]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    leaves = words(3, 2)
    gens = generators(leaves, 3)
    group = closure([g for _, g in gens], len(leaves))
    frontiers = [("",), words(3, 1), words(3, 2), ("00", "01", "02", "1", "2")]
    reports = {f: relative_report(f, group, gens, leaves) for f in frontiers}
    old = ("0", "10", "11", "12", "2")
    normal_refinement = {"0": words(3, 2), "10": words(3, 1), "11": ("",),
                         "12": words(3, 1), "2": words(3, 2)}
    nonnormal_refinement = dict(normal_refinement)
    nonnormal_refinement["10"] = ("00", "01", "02", "1", "2")
    cases = [mixed_case("mixed old depths and mixed relative full levels, including zero", old, normal_refinement, reports),
             mixed_case("mixed old depths, with one uneven refinement inside an old cell", old, nonnormal_refinement, reports)]
    assert cases[0]["normality_observed_from_exhaustive_factor_conjugation"]
    assert not cases[1]["normality_observed_from_exhaustive_factor_conjugation"]
    assert reports[words(3, 1)]["setwise_frontier_stabilizer_order_enumerated"] == len(group)
    assert reports[words(3, 1)]["pointwise_vertex_stabilizer_order_enumerated"] < len(group)
    result = {"status": "PASS", "construction": "breadth-first closure of eight explicitly constructed local adjacent-swap permutations",
              "finite_group_order_enumerated": len(group), "finite_group_generators": [n for n, _ in gens],
              "factor_checks": list(reports.values()), "mixed_frontier_checks": cases,
              "appendix_checks": appendix_tests(3, 2),
              "limitation": "Bounded finite-image checks, not a proof of the infinite-boundary theorem; full product group is not enumerated."}
    output = args.out / "mixed_ternary_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS: explicit finite rooted permutation group order", len(group))
    for case in cases:
        print("PASS:", case["name"], "N=", case["N_computed_directly_from_global_frontiers"],
              "index=", case["index_observed_from_enumerated_factors"],
              "normal=", case["normality_observed_from_exhaustive_factor_conjugation"])
    print("PASS: setwise/pointwise frontier distinction")
    print("PASS: appendix checks", result["appendix_checks"])
    print("Results:", output.resolve())


if __name__ == "__main__":
    main()
