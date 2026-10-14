"""Independent finite checks for the Phase 5B theorem audit; standard library only.

Does not import any archived research code or use any benchmark labels.
Run: python code/theory_independent_checks.py --output data/theory_independent_checks.json
"""
import argparse
import itertools
import json
from pathlib import Path


def partitions(items):
    if not items:
        yield ()
        return
    x, *rest = items
    for part in partitions(rest):
        yield (frozenset([x]),) + part
        for k in range(len(part)):
            yield part[:k] + (part[k] | {x},) + part[k + 1:]


def trees(items):
    if len(items) == 1:
        yield items[0]
        return
    first, *rest = items
    for mask in range(1 << len(rest)):
        left = (first,) + tuple(x for i, x in enumerate(rest) if mask >> i & 1)
        right = tuple(x for i, x in enumerate(rest) if not (mask >> i & 1))
        if not right:
            continue
        for a in trees(left):
            for b in trees(right):
                yield (a, b)


def clades(tree):
    if isinstance(tree, int):
        return {frozenset([tree])}
    a, b = clades(tree[0]), clades(tree[1])
    return a | b | {frozenset().union(*a, *b)}


def defect_supports(n, function, left):
    """Enumerate all pairs of full assignments; no SAT encoding reused."""
    mask = sum(1 << x for x in left)
    full = (1 << n) - 1
    supports = set()
    for x in range(1 << n):
        for y in range(x + 1, 1 << n):
            xy = (x & mask) | (y & (full ^ mask))
            yx = (y & mask) | (x & (full ^ mask))
            if (function(x) and function(y)) != (function(xy) and function(yx)):
                supports.add(frozenset(v for v in range(n) if (x ^ y) >> v & 1))
    return supports


def minimal_sets(family):
    return {s for s in family if not any(t < s for t in family)}


def greedy(supports, initial, order):
    current = set(initial)
    calls = 0
    for x in order:
        if x not in current:
            continue
        calls += 1
        candidate = current - {x}
        if any(s <= candidate for s in supports):
            current = candidate
    return sorted(current), calls


def grouped(supports, initial):
    current = set(initial)
    calls = 0

    def visit(group):
        nonlocal current, calls
        calls += 1
        candidate = current - set(group)
        if any(s <= candidate for s in supports):
            current = candidate
        elif len(group) > 1:
            middle = len(group) // 2
            visit(group[:middle])
            visit(group[middle:])
    visit(list(initial))
    return sorted(current), calls


def run():
    out = {"method": "independent finite enumeration; not proof", "laminar": [], "all_equal": []}
    for n in range(1, 6):
        ps = list(partitions(list(range(n))))
        cs = [clades(t) for t in trees(tuple(range(n)))]
        mismatches = 0
        for p in ps:
            for q in ps:
                family = set(p) | set(q)
                laminar = all(not (a & b) or a <= b or b <= a for a in family for b in family)
                represented = any(family <= c for c in cs)
                mismatches += laminar != represented
        assert mismatches == 0
        out["laminar"].append({"n": n, "partition_pairs": len(ps) ** 2, "unordered_binary_trees": len(cs), "mismatches": mismatches})
    for n in range(3, 9):
        f = lambda x, n=n: x in (0, (1 << n) - 1)
        cut_count = 0
        failures = 0
        for mask in range(1, 1 << (n - 1)):
            left = {i for i in range(n) if mask >> i & 1}
            supports = defect_supports(n, f, left)
            failures += supports != {frozenset(range(n))}
            cut_count += 1
        assert failures == 0
        out["all_equal"].append({"n": n, "unordered_nontrivial_cuts": cut_count, "support_sets": [list(range(n))], "failures": failures})
    # Two independent equality components have incomparable minimal supports.
    def f(x):
        return (x & 7) in (0, 7) and ((x >> 3) & 3) in (0, 3)
    supports = defect_supports(5, f, {0, 3})
    minimal = minimal_sets(supports)
    assert minimal == {frozenset([0, 1, 2]), frozenset([3, 4])}
    large, qlarge = greedy(supports, set(range(5)), [3, 4, 0, 1, 2])
    small, qsmall = greedy(supports, set(range(5)), [0, 1, 2, 3, 4])
    assert large == [0, 1, 2] and small == [3, 4]
    out["minimal_not_minimum"] = {"function": "EQ(x0,x1,x2) AND EQ(x3,x4)", "cut_left": [0, 3], "minimal_supports": sorted(map(sorted, minimal)), "deletion_order_34012": large, "deletion_order_01234": small, "queries": [qlarge, qsmall]}
    # A large witness's union can include distinct semantic blocks.
    assert frozenset(range(5)) in supports
    out["hyperedge_not_must_link"] = {"support": list(range(5)), "actual_semantic_blocks": [[0, 1, 2], [3, 4]], "witness_support_exists": True}
    # Every upward-closed feasible-support predicate for n<=4 corresponds to
    # a nonempty antichain. Check all via arbitrary nonempty families and dedup.
    checked = 0
    for n in range(1, 5):
        nonempty = [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1, 1 << n)]
        antichains = set()
        for selection in range(1, 1 << len(nonempty)):
            fam = frozenset(minimal_sets({s for i, s in enumerate(nonempty) if selection >> i & 1}))
            antichains.add(fam)
        for fam in antichains:
            for order in itertools.permutations(range(n)):
                result, calls = greedy(fam, set(range(n)), order)
                assert frozenset(result) in fam and calls <= n
                result2, calls2 = grouped(fam, order)
                assert frozenset(result2) in fam
                assert calls2 <= 1 + 2 * len(result2) * (n - 1).bit_length()
                checked += 1
    out["deletion_query_bound"] = {"upward_predicate_order_pairs_checked": checked, "max_n": 4, "linear_and_group_deletion": True, "failures": 0}
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
