from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, Mapping, MutableMapping, Optional, Set, Tuple

from .core import Expr, Var, Bin, cm_anf_coeffs, expr_key, expr_key_cached

Monomial = FrozenSet[str]
Polynomial = FrozenSet[Monomial]


class ANFBudgetExceeded(RuntimeError):
    """Raised before a sparse ANF operation would exceed a declared local budget."""

    def __init__(self, reason: str, observed: int, limit: int):
        super().__init__(f"{reason}: observed={observed} limit={limit}")
        self.reason = reason
        self.observed = int(observed)
        self.limit = int(limit)


@dataclass
class ANFBudget:
    max_monomials: Optional[int] = None
    max_pair_terms_per_multiply: Optional[int] = None
    max_pair_terms_total: Optional[int] = None


@dataclass
class ANFStats:
    multiplications: int = 0
    multiplication_pair_terms: int = 0
    peak_monomials: int = 0
    peak_degree: int = 0
    nodes_evaluated: int = 0
    cache_hits: int = 0
    peak_cache_entries: int = 0


def xor_poly(a: Polynomial, b: Polynomial) -> Polynomial:
    return frozenset(set(a) ^ set(b))


def mul_poly(a: Polynomial, b: Polynomial, stats: ANFStats | None = None) -> Polynomial:
    if stats is not None:
        stats.multiplications += 1
        stats.multiplication_pair_terms += len(a) * len(b)
    out: Set[Monomial] = set()
    for ma in a:
        for mb in b:
            m = frozenset(set(ma) | set(mb))  # Boolean x^2=x
            if m in out:
                out.remove(m)
            else:
                out.add(m)
    p = frozenset(out)
    if stats is not None:
        _observe(p, stats)
    return p


def _observe(p: Polynomial, s: ANFStats):
    s.peak_monomials = max(s.peak_monomials, len(p))
    if p:
        s.peak_degree = max(s.peak_degree, max(len(m) for m in p))


def var_poly(name: str) -> Polynomial:
    return frozenset([frozenset([name])])


def const_poly(v: int) -> Polynomial:
    return frozenset([frozenset()]) if v else frozenset()


def propagate(expr: Expr, stats: ANFStats | None = None) -> Polynomial:
    """Small reference sparse-ANF implementation.

    This intentionally remains simple and non-budgeted. The benchmark path uses the
    bitmask implementation below, while tests use this representation as an
    independent coordinate encoding.
    """
    if stats is None:
        stats = ANFStats()
    if isinstance(expr, Var):
        p = var_poly(expr.name)
        _observe(p, stats)
        return p
    a, b, c, d = cm_anf_coeffs(expr.op)
    # Avoid evaluating semantically dead operands. This makes the reference path a
    # reasonable symbolic baseline for constants/projections as well.
    px = propagate(expr.left, stats) if (b or d) else frozenset()
    py = propagate(expr.right, stats) if (c or d) else frozenset()
    p = const_poly(a)
    if b:
        p = xor_poly(p, px)
    if c:
        p = xor_poly(p, py)
    if d:
        p = xor_poly(p, mul_poly(px, py, stats))
    _observe(p, stats)
    return p


# Canonical sparse backend used for the benchmark. Variable i maps to bit i;
# a polynomial is a frozenset of integer monomial masks.
MaskPoly = FrozenSet[int]


def _mask_observe(p: MaskPoly, stats: ANFStats, budget: ANFBudget | None) -> None:
    size = len(p)
    if budget is not None and budget.max_monomials is not None and size > budget.max_monomials:
        raise ANFBudgetExceeded("max_monomials", size, budget.max_monomials)
    stats.peak_monomials = max(stats.peak_monomials, size)
    if p:
        stats.peak_degree = max(stats.peak_degree, max(m.bit_count() for m in p))


def _mask_xor(a: MaskPoly, b: MaskPoly, stats: ANFStats, budget: ANFBudget | None) -> MaskPoly:
    p = frozenset(set(a) ^ set(b))
    _mask_observe(p, stats, budget)
    return p


def _mask_mul(a: MaskPoly, b: MaskPoly, stats: ANFStats, budget: ANFBudget | None) -> MaskPoly:
    pair_terms = len(a) * len(b)
    if budget is not None and budget.max_pair_terms_per_multiply is not None:
        if pair_terms > budget.max_pair_terms_per_multiply:
            raise ANFBudgetExceeded(
                "max_pair_terms_per_multiply",
                pair_terms,
                budget.max_pair_terms_per_multiply,
            )
    if budget is not None and budget.max_pair_terms_total is not None:
        projected = stats.multiplication_pair_terms + pair_terms
        if projected > budget.max_pair_terms_total:
            raise ANFBudgetExceeded(
                "max_pair_terms_total", projected, budget.max_pair_terms_total
            )
    stats.multiplications += 1
    stats.multiplication_pair_terms += pair_terms
    out: set[int] = set()
    for x in a:
        for y in b:
            z = x | y
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    p = frozenset(out)
    _mask_observe(p, stats, budget)
    return p


def propagate_mask_dag(
    expr: Expr,
    order: Tuple[str, ...],
    stats: ANFStats | None = None,
    *,
    budget: ANFBudget | None = None,
    memo_mode: str = "structural",
) -> MaskPoly:
    """DAG-aware canonical sparse ANF propagation.

    `memo_mode="structural"` treats structurally identical immutable subexpressions
    as CSE-equivalent. `memo_mode="identity"` uses only source-object sharing.
    All benchmark arms use the same backend and default structural memoization; the
    frontends differ only in their preparation/rewrite pass.
    """
    if stats is None:
        stats = ANFStats()
    idx = {v: i for i, v in enumerate(order)}
    memo: dict[object, MaskPoly] = {}
    key_memo: dict[int, tuple] = {}

    def key(e: Expr) -> object:
        if memo_mode == "identity":
            return id(e)
        if memo_mode == "structural":
            return expr_key_cached(e, key_memo)
        raise ValueError(f"unknown memo_mode={memo_mode!r}")

    def rec(e: Expr) -> MaskPoly:
        k = key(e)
        if k in memo:
            stats.cache_hits += 1
            return memo[k]
        stats.nodes_evaluated += 1
        if isinstance(e, Var):
            p = frozenset([1 << idx[e.name]])
            _mask_observe(p, stats, budget)
        else:
            a, b, c, d = cm_anf_coeffs(e.op)
            # Lazy operand propagation: do not traverse an operand that the truth
            # function does not use. This avoids creating an artificial baseline.
            px = rec(e.left) if (b or d) else frozenset()
            py = rec(e.right) if (c or d) else frozenset()
            p: MaskPoly = frozenset([0]) if a else frozenset()
            _mask_observe(p, stats, budget)
            if b:
                p = _mask_xor(p, px, stats, budget)
            if c:
                p = _mask_xor(p, py, stats, budget)
            if d:
                p = _mask_xor(p, _mask_mul(px, py, stats, budget), stats, budget)
        memo[k] = p
        stats.peak_cache_entries = max(stats.peak_cache_entries, len(memo))
        return p

    return rec(expr)


def propagate_mask(expr: Expr, order: Tuple[str, ...]) -> MaskPoly:
    """Compatibility wrapper for the original independent bitmask check."""
    return propagate_mask_dag(expr, order, ANFStats(), memo_mode="identity")


def eval_mask_poly(poly: MaskPoly, order: Tuple[str, ...], env: Mapping[str, int]) -> int:
    """Evaluate a canonical bitmask ANF independently from the source AST."""
    assignment = 0
    for i, name in enumerate(order):
        if int(bool(env[name])):
            assignment |= 1 << i
    value = 0
    for monomial in poly:
        if monomial & ~assignment == 0:
            value ^= 1
    return value


def mask_poly_degree(poly: MaskPoly) -> int:
    return max((m.bit_count() for m in poly), default=0)


def mask_poly_digest(poly: MaskPoly) -> str:
    """Stable SHA-256 digest of a canonical sparse ANF artifact."""
    import hashlib

    h = hashlib.sha256()
    for m in sorted(poly):
        width = max(1, (m.bit_length() + 7) // 8)
        h.update(width.to_bytes(2, "little"))
        h.update(m.to_bytes(width, "little"))
    return h.hexdigest()
