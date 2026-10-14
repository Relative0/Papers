from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .core import (
    CM,
    CM_TO_NAME,
    OPS,
    Bin,
    Expr,
    RewriteCertificate,
    Var,
    cm_compose,
    cm_eval,
    cm_swap_operands,
    eval_expr,
    expr_key,
    expr_key_cached,
)


@dataclass
class OptimizerStats:
    visited_nodes: int = 0
    output_unique_nodes: int = 0
    same_operand_folds: int = 0
    transpose_alignments: int = 0
    cut_retabulations: int = 0
    structural_cse_hits: int = 0
    commutative_reorders: int = 0
    associative_flattened_nodes: int = 0
    certificates: int = 0

    @property
    def successful_folds(self) -> int:
        return self.same_operand_folds + self.cut_retabulations


COMMUTATIVE = {
    OPS["AND"],
    OPS["OR"],
    OPS["XOR"],
    OPS["XNOR"],
    OPS["NAND"],
    OPS["NOR"],
}
ASSOCIATIVE = {
    OPS["AND"],
    OPS["OR"],
    OPS["XOR"],
    OPS["XNOR"],
}


def _intern_count(expr: Expr) -> int:
    seen: set[tuple] = set()
    key_memo: dict[int, tuple] = {}

    def rec(e: Expr) -> None:
        k = expr_key_cached(e, key_memo)
        if k in seen:
            return
        seen.add(k)
        if isinstance(e, Bin):
            rec(e.left)
            rec(e.right)

    rec(expr)
    return len(seen)


def _support(expr: Expr, memo: Optional[dict[tuple, frozenset[str]]] = None) -> frozenset[str]:
    if memo is None:
        memo = {}
    k = expr_key(expr)
    if k in memo:
        return memo[k]
    if isinstance(expr, Var):
        s = frozenset([expr.name])
    else:
        s = _support(expr.left, memo) | _support(expr.right, memo)
    memo[k] = s
    return s


def _primitive_pair(expr: Expr, a: str, b: str) -> bool:
    return (
        isinstance(expr, Bin)
        and isinstance(expr.left, Var)
        and isinstance(expr.right, Var)
        and expr.left.name == a
        and expr.right.name == b
    )


def _retabulate_two_support(expr: Expr, names: Tuple[str, str]) -> Bin:
    a, b = names
    table = tuple(
        eval_expr(expr, {a: x, b: y})
        for x, y in ((1, 1), (1, 0), (0, 1), (0, 0))
    )
    return Bin(table, Var(a), Var(b))  # type: ignore[arg-type]


def _aligned_same_operands(a: Bin, b: Bin, key_fn=expr_key):
    ka0, ka1 = key_fn(a.left), key_fn(a.right)
    kb0, kb1 = key_fn(b.left), key_fn(b.right)
    if (ka0, ka1) == (kb0, kb1):
        return a.op, b.op, a.left, a.right, "same"
    if (ka0, ka1) == (kb1, kb0):
        return a.op, cm_swap_operands(b.op), a.left, a.right, "transpose"
    return None


def cm_frontend(
    expr: Expr,
    certs: Optional[List[RewriteCertificate]] = None,
) -> tuple[Expr, OptimizerStats]:
    """Typed CM same-operand fusion with operand-exchange normalization.

    This deliberately performs only the formally established local rule used by
    the current Gate-A campaign. Quotient/containment-specific shortcuts remain
    disabled until an additional rewrite rule is independently certified.
    """
    stats = OptimizerStats()
    memo: dict[tuple, Expr] = {}
    key_memo: dict[int, tuple] = {}
    def key(e: Expr) -> tuple:
        return expr_key_cached(e, key_memo)

    def rec(e: Expr) -> Expr:
        stats.visited_nodes += 1
        k0 = key(e)
        if k0 in memo:
            stats.structural_cse_hits += 1
            return memo[k0]
        if isinstance(e, Var):
            memo[k0] = e
            return e
        l = rec(e.left)
        r = rec(e.right)
        node: Expr = Bin(e.op, l, r)
        if isinstance(l, Bin) and isinstance(r, Bin):
            aligned = _aligned_same_operands(l, r, key)
            if aligned is not None:
                lop, rop, x, y, orientation = aligned
                h = cm_compose(e.op, lop, rop)
                out = Bin(h, x, y)
                stats.same_operand_folds += 1
                if orientation == "transpose":
                    stats.transpose_alignments += 1
                if certs is not None:
                    certs.append(
                        RewriteCertificate(
                            rule="CM_SAME_OPERAND_COMPOSITION",
                            before=key(node),
                            after=key(out),
                            details={
                                "orientation": orientation,
                                "phi": e.op,
                                "theta1": lop,
                                "theta2": rop,
                                "result": h,
                            },
                        )
                    )
                    stats.certificates += 1
                # The fold can expose another same-operand fold one level up, but
                # children x/y are already recursively prepared. No retabulation is
                # used here.
                node = out
        memo[k0] = node
        return node

    out = rec(expr)
    stats.output_unique_nodes = _intern_count(out)
    return out, stats


def generic_2support_frontend(
    expr: Expr,
    certs: Optional[List[RewriteCertificate]] = None,
) -> tuple[Expr, OptimizerStats]:
    """Strong representation-neutral structural comparator.

    It gets every local opportunity available to the CM frontend (same-operands
    2-input truth-function composition, including operand exchange) and additionally
    retabulates any remaining subtree whose *semantic variable support* is exactly
    two variables. This is intentionally stronger than a CM-only comparison and is
    the primary falsification baseline for a CM-specific advantage.
    """
    stats = OptimizerStats()
    memo: dict[tuple, tuple[Expr, frozenset[str]]] = {}
    key_memo: dict[int, tuple] = {}
    def key(e: Expr) -> tuple:
        return expr_key_cached(e, key_memo)

    def rec(e: Expr) -> tuple[Expr, frozenset[str]]:
        stats.visited_nodes += 1
        k0 = key(e)
        if k0 in memo:
            stats.structural_cse_hits += 1
            return memo[k0]
        if isinstance(e, Var):
            result = (e, frozenset([e.name]))
            memo[k0] = result
            return result

        l, sl = rec(e.left)
        r, sr = rec(e.right)
        node: Expr = Bin(e.op, l, r)
        support = sl | sr

        # Generic local LUT composition over identical operands is not CM-specific.
        if isinstance(l, Bin) and isinstance(r, Bin):
            aligned = _aligned_same_operands(l, r, key)
            if aligned is not None:
                lop, rop, x, y, orientation = aligned
                h = cm_compose(e.op, lop, rop)
                out = Bin(h, x, y)
                stats.same_operand_folds += 1
                if orientation == "transpose":
                    stats.transpose_alignments += 1
                if certs is not None:
                    certs.append(
                        RewriteCertificate(
                            rule="GENERIC_SAME_OPERAND_LUT_COMPOSITION",
                            before=key(node),
                            after=key(out),
                            details={
                                "orientation": orientation,
                                "phi": e.op,
                                "f": lop,
                                "g": rop,
                                "result": h,
                            },
                        )
                    )
                    stats.certificates += 1
                node = out
                support = support

        # Stronger cut/LUT path: canonicalize any exact two-variable subfunction.
        if len(support) == 2:
            names = tuple(sorted(support))
            if not _primitive_pair(node, names[0], names[1]):
                out = _retabulate_two_support(node, names)
                stats.cut_retabulations += 1
                if certs is not None:
                    certs.append(
                        RewriteCertificate(
                            rule="GENERIC_EXACT_2SUPPORT_RETABULATION",
                            before=key(node),
                            after=key(out),
                            details={"support": names, "result": out.op},
                        )
                    )
                    stats.certificates += 1
                node = out
        result = (node, support)
        memo[k0] = result
        return result

    out, _ = rec(expr)
    stats.output_unique_nodes = _intern_count(out)
    return out, stats


def cse_flat_frontend(expr: Expr) -> tuple[Expr, OptimizerStats]:
    """Generic sharing-aware CSE plus safe commutative/associative normalization.

    The pass does *not* retabulate functions and does not use CM frame metadata.
    For associative operators it flattens nested occurrences, sorts operands by a
    deterministic structural key when commutative, and rebuilds a balanced tree.
    All constructed nodes are hash-consed.
    """
    stats = OptimizerStats()
    intern: dict[tuple, Expr] = {}
    memo: dict[tuple, Expr] = {}
    key_memo: dict[int, tuple] = {}
    def key(e: Expr) -> tuple:
        return expr_key_cached(e, key_memo)

    def intern_var(v: Var) -> Expr:
        k = ("V", v.name)
        if k in intern:
            stats.structural_cse_hits += 1
            return intern[k]
        intern[k] = v
        return v

    def intern_bin(op: CM, l: Expr, r: Expr) -> Expr:
        kl, kr = key(l), key(r)
        if op in COMMUTATIVE and kr < kl:
            l, r = r, l
            kl, kr = kr, kl
            stats.commutative_reorders += 1
        k = ("B", op, kl, kr)
        if k in intern:
            stats.structural_cse_hits += 1
            return intern[k]
        n = Bin(op, l, r)
        intern[k] = n
        return n

    def collect_same(op: CM, e: Expr, out: list[Expr]) -> None:
        if isinstance(e, Bin) and e.op == op and op in ASSOCIATIVE:
            collect_same(op, e.left, out)
            collect_same(op, e.right, out)
        else:
            out.append(e)

    def build_balanced(op: CM, args: list[Expr]) -> Expr:
        if len(args) == 1:
            return args[0]
        cur = args
        while len(cur) > 1:
            nxt: list[Expr] = []
            i = 0
            while i + 1 < len(cur):
                nxt.append(intern_bin(op, cur[i], cur[i + 1]))
                i += 2
            if i < len(cur):
                nxt.append(cur[i])
            cur = nxt
        return cur[0]

    def rec(e: Expr) -> Expr:
        stats.visited_nodes += 1
        k0 = key(e)
        if k0 in memo:
            stats.structural_cse_hits += 1
            return memo[k0]
        if isinstance(e, Var):
            out = intern_var(e)
            memo[k0] = out
            return out
        l = rec(e.left)
        r = rec(e.right)
        if e.op in ASSOCIATIVE:
            args: list[Expr] = []
            collect_same(e.op, l, args)
            collect_same(e.op, r, args)
            if len(args) > 2:
                stats.associative_flattened_nodes += len(args) - 2
            if e.op in COMMUTATIVE:
                before = [key(a) for a in args]
                args = sorted(args, key=key)
                if [key(a) for a in args] != before:
                    stats.commutative_reorders += 1
            out = build_balanced(e.op, args)
        else:
            out = intern_bin(e.op, l, r)
        memo[k0] = out
        return out

    out = rec(expr)
    stats.output_unique_nodes = len(intern)
    return out, stats
