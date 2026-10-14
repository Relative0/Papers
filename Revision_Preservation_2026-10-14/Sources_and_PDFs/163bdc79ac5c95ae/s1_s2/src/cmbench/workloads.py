from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from .core import Expr, Var, Bin, OPS, cm_is_nonlinear, expr_key, expr_key_cached

# Keep the original nondegenerate connective family used in the prototype.
# XOR/XNOR are affine; the remaining six are nonlinear in ANF.
BASIC_NAMES = ("AND", "OR", "XOR", "XNOR", "IMP", "RIMP", "NAND", "NOR")
BASIC = [OPS[x] for x in BASIC_NAMES]
AFFINE = [OPS[x] for x in BASIC_NAMES if not cm_is_nonlinear(OPS[x])]
NONLINEAR = [OPS[x] for x in BASIC_NAMES if cm_is_nonlinear(OPS[x])]


@dataclass(frozen=True)
class StructureStats:
    occurrence_nodes: int
    unique_structural_nodes: int
    unique_object_nodes: int
    bin_occurrences: int
    realized_affine_fraction: float
    source_shared_fraction: float


def _choose_op(rng: random.Random, affine_fraction: float):
    pool = AFFINE if rng.random() < affine_fraction else NONLINEAR
    return rng.choice(pool)


def expression_structure_stats(expr: Expr) -> StructureStats:
    occurrences = 0
    bin_count = 0
    affine = 0
    structural: set[tuple] = set()
    objects: set[int] = set()
    key_memo: dict[int, tuple] = {}

    def rec(e: Expr) -> None:
        nonlocal occurrences, bin_count, affine
        occurrences += 1
        structural.add(expr_key_cached(e, key_memo))
        objects.add(id(e))
        if isinstance(e, Bin):
            bin_count += 1
            if not cm_is_nonlinear(e.op):
                affine += 1
            rec(e.left)
            rec(e.right)

    rec(expr)
    shared = 0.0 if occurrences == 0 else max(0.0, 1.0 - len(objects) / occurrences)
    return StructureStats(
        occurrence_nodes=occurrences,
        unique_structural_nodes=len(structural),
        unique_object_nodes=len(objects),
        bin_occurrences=bin_count,
        realized_affine_fraction=(affine / bin_count if bin_count else 1.0),
        source_shared_fraction=shared,
    )


def same_operand_tree(
    depth: int,
    seed: int = 1,
    reverse_prob: float = 0.35,
    affine_fraction: float = 0.5,
) -> Expr:
    """S1-style favorable tree: every primitive is a function of the same x/y pair.

    `depth` counts binary combination levels above the primitive leaves, so the
    source has 2**depth primitive pair leaves. Operator affine/nonlinear choice is
    applied to both primitive and internal operators.
    """
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    rng = random.Random(seed)
    x = Var("x")
    y = Var("y")
    leaves: list[Expr] = []
    for _ in range(1 << depth):
        theta = _choose_op(rng, affine_fraction)
        if rng.random() < reverse_prob:
            leaves.append(Bin(theta, y, x))
        else:
            leaves.append(Bin(theta, x, y))
    cur = leaves
    while len(cur) > 1:
        nxt: list[Expr] = []
        for i in range(0, len(cur), 2):
            nxt.append(Bin(_choose_op(rng, affine_fraction), cur[i], cur[i + 1]))
        cur = nxt
    return cur[0]


def mixed_tree(n_vars: int, depth: int, seed: int = 1, affine_fraction: float = 0.5) -> Expr:
    """Compatibility unfavorable tree without deliberate object sharing."""
    rng = random.Random(seed)
    vs = [Var(f"x{i}") for i in range(n_vars)]

    def rec(d: int) -> Expr:
        if d <= 0:
            return rng.choice(vs)
        return Bin(_choose_op(rng, affine_fraction), rec(d - 1), rec(d - 1))

    return rec(depth)


def mixed_support_dag(
    live_k: int,
    depth: int,
    seed: int,
    shared_subgraph_fraction: float,
    affine_fraction: float,
) -> Expr:
    """S2 mixed-support DAG with *guaranteed semantic support* `live_k`.

    Construction is `parity(x0..x{k-1}) XOR h`, where every ANF monomial of
    `h` has degree 0 or at least 2. Therefore `h` has no linear coefficient and
    cannot cancel any of the `k` linear parity terms; every declared variable is
    semantically essential in the final function.

    The mixed core `h` starts from two-variable AND atoms and is closed under the
    full BASIC operator family. The no-linear-term invariant is preserved because
    a two-input Boolean operator has ANF a XOR bP XOR cQ XOR dPQ: if P and Q
    contain only constants and degree>=2 monomials, so does the result. Source-DAG
    sharing is introduced only inside this core. `depth` is the recursive core
    depth, so all frozen (live_k, depth) cells are well-defined, including
    live_k=20, depth=3.
    """
    if live_k < 2:
        raise ValueError("live_k must be at least 2 for the S2 construction")
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if not 0.0 <= shared_subgraph_fraction <= 1.0:
        raise ValueError("shared_subgraph_fraction outside [0,1]")
    if not 0.0 <= affine_fraction <= 1.0:
        raise ValueError("affine_fraction outside [0,1]")

    rng = random.Random(seed)
    variables = [Var(f"x{i}") for i in range(live_k)]

    # Linear support guard: XOR parity has one unique degree-1 monomial per input.
    parity: Expr = variables[0]
    for v in variables[1:]:
        parity = Bin(OPS["XOR"], parity, v)

    # Degree>=2 atom pool. Use canonical variable order in each pair atom.
    pair_atoms: list[Expr] = []
    for i in range(live_k):
        for j in range(i + 1, live_k):
            pair_atoms.append(Bin(OPS["AND"], variables[i], variables[j]))

    pools: dict[int, list[Expr]] = {0: pair_atoms}

    def make(d: int) -> Expr:
        if d <= 0:
            return rng.choice(pair_atoms)

        def child() -> Expr:
            candidates = pools.get(d - 1, [])
            if candidates and rng.random() < shared_subgraph_fraction:
                return rng.choice(candidates)
            return make(d - 1)

        left = child()
        right = child()
        node = Bin(_choose_op(rng, affine_fraction), left, right)
        pools.setdefault(d, []).append(node)
        return node

    core = make(depth)
    return Bin(OPS["XOR"], parity, core)


def s1_cases():
    for depth in (2, 4, 6, 8, 10):
        for affine_fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            for reverse_fraction in (0.0, 0.25, 0.5):
                for seed in range(50):
                    case_seed = (
                        seed
                        + 1000 * depth
                        + int(affine_fraction * 100) * 100_000
                        + int(reverse_fraction * 100) * 10_000_000
                    )
                    yield {
                        "family": "S1",
                        "depth": depth,
                        "affine_fraction": affine_fraction,
                        "reverse_fraction": reverse_fraction,
                        "seed": seed,
                        "case_seed": case_seed,
                        "expr": same_operand_tree(
                            depth,
                            seed=case_seed,
                            reverse_prob=reverse_fraction,
                            affine_fraction=affine_fraction,
                        ),
                    }


def s2_cases():
    for live_k in (4, 8, 12, 16, 20):
        for depth in (3, 5, 7):
            for shared_fraction in (0.0, 0.25, 0.5):
                for affine_fraction in (0.25, 0.5, 0.75):
                    for seed in range(50):
                        case_seed = (
                            seed
                            + live_k * 1000
                            + depth * 100_000
                            + int(shared_fraction * 100) * 10_000_000
                            + int(affine_fraction * 100) * 1_000_000_000
                        )
                        yield {
                            "family": "S2",
                            "live_k": live_k,
                            "depth": depth,
                            "shared_fraction": shared_fraction,
                            "affine_fraction": affine_fraction,
                            "seed": seed,
                            "case_seed": case_seed,
                            "expr": mixed_support_dag(
                                live_k,
                                depth,
                                case_seed,
                                shared_fraction,
                                affine_fraction,
                            ),
                        }
