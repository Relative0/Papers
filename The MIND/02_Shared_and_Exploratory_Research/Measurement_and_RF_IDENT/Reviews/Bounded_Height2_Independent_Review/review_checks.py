"""Independent, bounded audit checks. Python 3.10+, standard library only.

Run the unchanged verifier in reproduction/ first. This script reads the
original phase, never writes it, and writes only REVIEW_CHECKS.json here.
"""
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent
PHASE = HERE.parent / "RF-IDENT Bounded Height2 2026-09-29"


def require(condition, context):
    if not condition:
        raise AssertionError(context)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_order(n):
    return tuple(tuple(i == j or i == 0 or j == n - 1
                       for j in range(n)) for i in range(n))


@lru_cache(None)
def faces(n, support):
    """Full order complex, without consulting query values or safety rules."""
    order = canonical_order(n)
    states = [i for i in range(n) if support >> i & 1]
    return frozenset(cell for size in (1, 2, 3)
                     for cell in combinations(states, size)
                     if all(order[i][j] for i, j in combinations(cell, 2)))


def collapse_safe(n, support, query):
    """Actually remove relative free edge/triangle pairs; no matrix or rank."""
    current = set(faces(n, support))
    target = {cell for cell in current
              if all((query >> i & 1) <= (query >> j & 1)
                     for i, j in combinations(cell, 2))}
    while current != target:
        pair = None
        for edge in sorted(current - target):
            if len(edge) != 2:
                continue
            cofaces = [cell for cell in current
                       if len(cell) == 3 and set(edge).issubset(cell)]
            if len(cofaces) == 1 and cofaces[0] not in target:
                pair = (edge, cofaces[0])
                break
        if pair is None:
            return False
        current.difference_update(pair)
    return True


def recognize(order):
    """Explicit O(n^2) relation validator, with the trivial empty convention."""
    n = len(order)
    if any(len(row) != n for row in order):
        return False
    if n <= 1:
        return not n or order[0][0]
    bottoms = [i for i in range(n) if all(order[i])]
    tops = [j for j in range(n) if all(order[i][j] for i in range(n))]
    if len(bottoms) != 1 or len(tops) != 1 or bottoms[0] == tops[0]:
        return False
    a, z = bottoms[0], tops[0]
    return all(order[i][j] == (i == j or i == a or j == z)
               for i in range(n) for j in range(n))


def definition_accepts(order):
    """Slow independent definition: partial order, endpoints, no four-chain."""
    n = len(order)
    if not n:
        return True
    if any(not order[i][i] for i in range(n)):
        return False
    if any(order[i][j] and order[j][i] for i, j in combinations(range(n), 2)):
        return False
    if any(order[i][j] and order[j][k] and not order[i][k]
           for i in range(n) for j in range(n) for k in range(n)):
        return False
    if not any(all(row) for row in order):
        return False
    if not any(all(order[i][j] for i in range(n)) for j in range(n)):
        return False
    return not any(order[a][b] and order[b][c] and order[c][d]
                   for a, b, c, d in permutations(range(n), 4))


def validate_protocol(example):
    n, queries = example["n"], example["queries"]
    def visit(node, support, used):
        if "states" in node:
            states = [i for i in range(n) if support >> i & 1]
            require(node["states"] == states and len(states) == 1,
                    ("leaf", node, support))
            return 0, 1, 0
        index = node["query_index"]
        require(0 <= index < len(queries) and index not in used, "query ID")
        query = queries[index]
        zero, one = support & ~query, support & query
        require(zero and one and collapse_safe(n, support, query),
                ("illegal node", n, support, query))
        require(len(node["children"]) == 2, "binary tree")
        left = visit(node["children"][0], zero, used | {index})
        right = visit(node["children"][1], one, used | {index})
        return 1 + left[0] + right[0], left[1] + right[1], 1 + max(left[2], right[2])
    nodes, leaves, depth = visit(example["tree"], (1 << n) - 1, set())
    require(nodes == n - 1 and leaves == n, "tree size")
    if "constructed_depth" in example:
        require(depth == example["constructed_depth"], "recorded depth")
    return nodes


def main():
    require(not sys.flags.optimize, "Use ordinary Python, without -O or -OO.")
    # Avoid creating __pycache__ inside the original phase.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("reviewed_verifier", PHASE / "verify_bounded_height2.py")
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    source_hashes = {}
    for line in (PHASE / "SHA256SUMS.txt").read_text().splitlines():
        expected, name = line.split("  ", 1)
        actual = digest(PHASE / name)
        require(actual == expected, ("source hash", name))
        source_hashes[name] = actual
    require(digest(HERE / "reproduction" / "verify_bounded_height2.py") ==
            source_hashes["verify_bounded_height2.py"], "unchanged reproduction script")
    baseline = json.loads((PHASE / "VERIFICATION.json").read_text())
    rerun = json.loads((HERE / "reproduction" / "VERIFICATION.json").read_text())
    baseline.pop("seconds")
    rerun.pop("seconds")
    require(baseline == rerun, "reproduction matches except timing")
    require((PHASE / "PROTOCOL_EXAMPLES.json").read_bytes() ==
            (HERE / "reproduction" / "PROTOCOL_EXAMPLES.json").read_bytes(),
            "protocol examples byte identical")

    safety_cases = 0
    for n in range(9):
        for support in range(1 << n):
            for query in range(1 << n):
                require(collapse_safe(n, support, query) == original.matrix_safe(n, support, query),
                        ("collapse/matrix disagreement", n, support, query))
                safety_cases += 1

    relation_cases = 0
    accepted = {}
    for n in range(5):
        pairs = list(permutations(range(n), 2))
        positives = 0
        for mask in range(1 << len(pairs)):
            relation = [[i == j for j in range(n)] for i in range(n)]
            for bit, (i, j) in enumerate(pairs):
                relation[i][j] = bool(mask >> bit & 1)
            result = recognize(relation)
            require(result == definition_accepts(relation), ("recognition", n, mask))
            positives += result
            relation_cases += 1
        accepted[n] = positives
    require(not recognize([[False]]) and not recognize([[True, False]]), "malformed input")

    examples = json.loads((PHASE / "PROTOCOL_EXAMPLES.json").read_text())
    protocol_nodes = sum(validate_protocol(example) for example in examples.values())
    singleton_libraries = ((), (0,), (1,), (0, 1), (0, 0, 1, 1))
    for queries in singleton_libraries:
        require(original.criterion(1, queries)[0], "singleton criterion")
        require(original.canonical_tree(1, queries) == {"states": [0]}, "singleton tree")
        require(original.verify_tree(1, queries, {"states": [0]}) == (0, 0), "singleton verification")
    try:
        original.canonical_tree(0, ())
    except ValueError as error:
        empty_limitation = str(error)
    else:
        raise AssertionError("Expected the reviewed empty-constructor limitation")

    result = {
        "status": "all review checks passed",
        "python": sys.version.split()[0],
        "source_hashes": source_hashes,
        "reproduction_matches_except_seconds": True,
        "protocol_examples_byte_identical": True,
        "reproduced_counts": baseline["counts"],
        "additional_counts": {
            "collapse_vs_matrix_n_0_through_8": safety_cases,
            "reflexive_relation_recognition_n_0_through_4": relation_cases,
            "accepted_relations_by_n_including_empty_convention": accepted,
            "malformed_relation_checks": 2,
            "stored_protocols": len(examples),
            "stored_protocol_internal_nodes_collapse_checked": protocol_nodes,
            "singleton_libraries": len(singleton_libraries),
        },
        "observed_implementation_limits": {
            "canonical_tree_empty_carrier": empty_limitation,
            "original_verifier_accepts_explicit_order_matrix": False,
        },
        "limitations": [
            "The fresh collapse oracle uses the inherited relative-collapse equivalence.",
            "The original library sweep is reproduced, not replaced by a new library sweep.",
            "Finite checks support the proof and do not establish general height-two complexity.",
        ],
    }
    (HERE / "REVIEW_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
