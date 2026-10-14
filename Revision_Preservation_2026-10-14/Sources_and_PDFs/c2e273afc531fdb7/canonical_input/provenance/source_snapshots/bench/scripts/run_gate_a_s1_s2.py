#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cmbench.anf import (  # noqa: E402
    ANFBudget,
    ANFBudgetExceeded,
    ANFStats,
    eval_mask_poly,
    mask_poly_degree,
    mask_poly_digest,
    propagate_mask_dag,
)
from cmbench.core import Expr, Var, Bin, eval_expr, expr_key, expr_key_cached, vars_of  # noqa: E402
from cmbench.optimize import (  # noqa: E402
    OptimizerStats,
    cm_frontend,
    cse_flat_frontend,
    generic_2support_frontend,
)
from cmbench.workloads import (  # noqa: E402
    expression_structure_stats,
    s1_cases,
    s2_cases,
)

ARMS = (
    "direct_sparse_anf",
    "cse_flat_sparse",
    "generic_2support_sparse",
    "cm_frontend_sparse",
)


def _stable_case_id(meta: Mapping[str, Any]) -> str:
    keep = {k: v for k, v in meta.items() if k != "expr"}
    raw = json.dumps(keep, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()[:20]


def _expr_depth(expr: Expr, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    k = id(expr)
    if k in memo:
        return memo[k]
    if isinstance(expr, Var):
        d = 0
    else:
        d = 1 + max(_expr_depth(expr.left, memo), _expr_depth(expr.right, memo))
    memo[k] = d
    return d


def _source_unique_nodes(expr: Expr) -> int:
    seen: set[tuple] = set()
    key_memo: dict[int, tuple] = {}
    stack = [expr]
    while stack:
        e = stack.pop()
        k = expr_key_cached(e, key_memo)
        if k in seen:
            continue
        seen.add(k)
        if isinstance(e, Bin):
            stack.append(e.left)
            stack.append(e.right)
    return len(seen)


def _serialized_anf_bytes(poly: frozenset[int]) -> int:
    # Exact deterministic integer-mask serialization size used by the digest
    # convention: two-byte width prefix plus little-endian mask bytes.
    total = 0
    for m in poly:
        width = max(1, (m.bit_length() + 7) // 8)
        total += 2 + width
    return total


def _semantic_support_count(poly: frozenset[int]) -> int:
    union = 0
    for m in poly:
        union |= m
    return union.bit_count()


def _independent_check(expr: Expr, poly: frozenset[int], order: tuple[str, ...], family: str, case_seed: int) -> bool:
    if family == "S1":
        assignments = [
            {order[0]: x, order[1]: y}
            for x in (0, 1)
            for y in (0, 1)
        ]
    else:
        rng = random.Random(case_seed ^ 0xA5A5_2026_0917)
        assignments = []
        # Deterministic corner cases plus seeded random assignments.
        assignments.append({v: 0 for v in order})
        assignments.append({v: 1 for v in order})
        for _ in range(30):
            assignments.append({v: rng.getrandbits(1) for v in order})
    for env in assignments:
        if eval_expr(expr, env) != eval_mask_poly(poly, order, env):
            return False
    return True


def _prepare(arm: str, expr: Expr) -> tuple[Expr, OptimizerStats]:
    if arm == "direct_sparse_anf":
        return expr, OptimizerStats(
            visited_nodes=0,
            output_unique_nodes=_source_unique_nodes(expr),
        )
    if arm == "cse_flat_sparse":
        return cse_flat_frontend(expr)
    if arm == "generic_2support_sparse":
        return generic_2support_frontend(expr)
    if arm == "cm_frontend_sparse":
        return cm_frontend(expr)
    raise KeyError(arm)


def _arm_once(arm: str, expr: Expr, order: tuple[str, ...], budget: ANFBudget) -> dict[str, Any]:
    t0 = time.perf_counter_ns()
    prepared, opt = _prepare(arm, expr)
    t1 = time.perf_counter_ns()
    stats = ANFStats()
    poly = propagate_mask_dag(
        prepared,
        order,
        stats,
        budget=budget,
        memo_mode="structural",
    )
    t2 = time.perf_counter_ns()
    return {
        "status": "OK",
        "prepared": prepared,
        "poly": poly,
        "digest": mask_poly_digest(poly),
        "prep_ns": t1 - t0,
        "propagate_ns": t2 - t1,
        "end_to_end_ns": t2 - t0,
        "optimizer": opt,
        "anf": stats,
        "final_monomials": len(poly),
        "final_degree": mask_poly_degree(poly),
        "serialized_bytes": _serialized_anf_bytes(poly),
        "semantic_support": _semantic_support_count(poly),
    }


def _schedule(index: int) -> tuple[str, ...]:
    names = ARMS
    offset = index % len(names)
    order = names[offset:] + names[:offset]
    if (index // len(names)) % 2:
        order = tuple(reversed(order))
    return order


def _base_row(case: Mapping[str, Any], case_id: str, expr: Expr) -> dict[str, Any]:
    ss = expression_structure_stats(expr)
    row: dict[str, Any] = {
        "case_id": case_id,
        "family": case["family"],
        "seed": case["seed"],
        "case_seed": case["case_seed"],
        "depth": case["depth"],
        "affine_fraction_requested": case["affine_fraction"],
        "affine_fraction_realized": ss.realized_affine_fraction,
        "source_occurrence_nodes": ss.occurrence_nodes,
        "source_unique_structural_nodes": ss.unique_structural_nodes,
        "source_unique_object_nodes": ss.unique_object_nodes,
        "source_shared_fraction_realized": ss.source_shared_fraction,
        "source_ast_depth": _expr_depth(expr),
    }
    if case["family"] == "S1":
        row["live_k_requested"] = 2
        row["reverse_fraction_requested"] = case["reverse_fraction"]
        row["shared_fraction_requested"] = ""
    else:
        row["live_k_requested"] = case["live_k"]
        row["reverse_fraction_requested"] = ""
        row["shared_fraction_requested"] = case["shared_fraction"]
    return row


def _flatten_arm(row: dict[str, Any], arm: str, result: Mapping[str, Any]) -> None:
    prefix = arm
    row[f"{prefix}_status"] = result.get("status", "ERROR")
    if result.get("status") != "OK":
        row[f"{prefix}_budget_reason"] = result.get("budget_reason", "")
        row[f"{prefix}_budget_observed"] = result.get("budget_observed", "")
        row[f"{prefix}_budget_limit"] = result.get("budget_limit", "")
        return
    opt: OptimizerStats = result["optimizer"]
    anf: ANFStats = result["anf"]
    row[f"{prefix}_digest"] = result["digest"]
    row[f"{prefix}_prep_ns"] = result["prep_ns"]
    row[f"{prefix}_propagate_ns"] = result["propagate_ns"]
    row[f"{prefix}_end_to_end_ns"] = result["end_to_end_ns"]
    row[f"{prefix}_output_unique_nodes"] = opt.output_unique_nodes
    row[f"{prefix}_same_operand_folds"] = opt.same_operand_folds
    row[f"{prefix}_transpose_alignments"] = opt.transpose_alignments
    row[f"{prefix}_cut_retabulations"] = opt.cut_retabulations
    row[f"{prefix}_successful_folds"] = opt.successful_folds
    row[f"{prefix}_cse_hits"] = opt.structural_cse_hits
    row[f"{prefix}_commutative_reorders"] = opt.commutative_reorders
    row[f"{prefix}_associative_flattened_nodes"] = opt.associative_flattened_nodes
    row[f"{prefix}_multiplications"] = anf.multiplications
    row[f"{prefix}_pair_terms"] = anf.multiplication_pair_terms
    row[f"{prefix}_peak_monomials"] = anf.peak_monomials
    row[f"{prefix}_peak_degree"] = anf.peak_degree
    row[f"{prefix}_anf_nodes_evaluated"] = anf.nodes_evaluated
    row[f"{prefix}_anf_cache_hits"] = anf.cache_hits
    row[f"{prefix}_peak_cache_entries"] = anf.peak_cache_entries
    row[f"{prefix}_final_monomials"] = result["final_monomials"]
    row[f"{prefix}_final_degree"] = result["final_degree"]
    row[f"{prefix}_serialized_bytes"] = result["serialized_bytes"]
    row[f"{prefix}_semantic_support"] = result["semantic_support"]


def _iter_cases(families: set[str]):
    if "S1" in families:
        yield from s1_cases()
    if "S2" in families:
        yield from s2_cases()


def run(args: argparse.Namespace) -> tuple[Path, Path]:
    families = {x.strip().upper() for x in args.families.split(",") if x.strip()}
    unknown = families - {"S1", "S2"}
    if unknown:
        raise SystemExit(f"unknown families: {sorted(unknown)}")

    budget = ANFBudget(
        max_monomials=args.max_monomials,
        max_pair_terms_per_multiply=args.max_pair_terms_per_multiply,
        max_pair_terms_total=args.max_pair_terms_total,
    )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta_path = out.with_suffix(".meta.json")

    rows: list[dict[str, Any]] = []
    all_fieldnames: set[str] = set()
    start = time.time()
    attempted = 0
    admitted = 0
    mismatch_count = 0
    budget_rows = 0

    for index, case in enumerate(_iter_cases(families)):
        if index < args.skip_cases:
            continue
        if args.max_cases is not None and attempted >= args.max_cases:
            break
        attempted += 1
        expr: Expr = case["expr"]
        case_id = _stable_case_id(case)
        order = tuple(sorted(vars_of(expr), key=lambda x: (len(x), x)))
        row = _base_row(case, case_id, expr)
        row["syntactic_support"] = len(order)
        row["schedule"] = ">".join(_schedule(index))

        results: dict[str, dict[str, Any]] = {}
        for arm in _schedule(index):
            try:
                results[arm] = _arm_once(arm, expr, order, budget)
            except ANFBudgetExceeded as exc:
                results[arm] = {
                    "status": "BUDGET",
                    "budget_reason": exc.reason,
                    "budget_observed": exc.observed,
                    "budget_limit": exc.limit,
                }
            except Exception as exc:
                results[arm] = {"status": "ERROR", "error": repr(exc)}
                row[f"{arm}_error"] = repr(exc)
            _flatten_arm(row, arm, results[arm])

        ok = [arm for arm in ARMS if results.get(arm, {}).get("status") == "OK"]
        row["all_arms_ok"] = int(len(ok) == len(ARMS))
        if len(ok) != len(ARMS):
            budget_rows += int(any(results.get(a, {}).get("status") == "BUDGET" for a in ARMS))

        if ok:
            digests = {results[a]["digest"] for a in ok}
            row["successful_arms_agree"] = int(len(digests) == 1)
            if len(digests) != 1:
                mismatch_count += 1
                row["correctness_status"] = "MISMATCH"
            else:
                reference = results["direct_sparse_anf"] if "direct_sparse_anf" in ok else results[ok[0]]
                independent = _independent_check(
                    expr,
                    reference["poly"],
                    order,
                    case["family"],
                    case["case_seed"],
                )
                row["independent_eval_ok"] = int(independent)
                row["correctness_status"] = "OK" if independent else "SOURCE_POLY_MISMATCH"
                if not independent:
                    mismatch_count += 1
        else:
            row["successful_arms_agree"] = ""
            row["independent_eval_ok"] = ""
            row["correctness_status"] = "NO_SUCCESSFUL_ARM"

        if row["all_arms_ok"] and row["correctness_status"] == "OK":
            admitted += 1
            direct = results["direct_sparse_anf"]
            row["semantic_support"] = direct["semantic_support"]
            row["live_k_exact_match"] = int(direct["semantic_support"] == int(row["live_k_requested"]))
            dm = direct["anf"].multiplications
            dp = direct["anf"].multiplication_pair_terms
            for arm in ("cse_flat_sparse", "generic_2support_sparse", "cm_frontend_sparse"):
                ar = results[arm]
                row[f"{arm}_multiplications_avoided"] = dm - ar["anf"].multiplications
                row[f"{arm}_pair_terms_avoided"] = dp - ar["anf"].multiplication_pair_terms
                row[f"{arm}_over_direct_multiplications"] = (
                    ar["anf"].multiplications / dm if dm else (1.0 if ar["anf"].multiplications == 0 else math.inf)
                )
                row[f"{arm}_over_direct_pair_terms"] = (
                    ar["anf"].multiplication_pair_terms / dp if dp else (1.0 if ar["anf"].multiplication_pair_terms == 0 else math.inf)
                )
            gen = results["generic_2support_sparse"]
            cm = results["cm_frontend_sparse"]
            row["cm_over_generic_multiplications"] = (
                cm["anf"].multiplications / gen["anf"].multiplications
                if gen["anf"].multiplications
                else (1.0 if cm["anf"].multiplications == 0 else math.inf)
            )
            row["cm_over_generic_pair_terms"] = (
                cm["anf"].multiplication_pair_terms / gen["anf"].multiplication_pair_terms
                if gen["anf"].multiplication_pair_terms
                else (1.0 if cm["anf"].multiplication_pair_terms == 0 else math.inf)
            )
            row["cm_over_generic_peak_monomials"] = (
                cm["anf"].peak_monomials / gen["anf"].peak_monomials
                if gen["anf"].peak_monomials
                else 1.0
            )
            row["cm_over_generic_end_to_end_ns"] = (
                cm["end_to_end_ns"] / gen["end_to_end_ns"]
                if gen["end_to_end_ns"]
                else math.inf
            )

        rows.append(row)
        all_fieldnames.update(row.keys())
        if args.progress_every and attempted % args.progress_every == 0:
            elapsed = time.time() - start
            print(
                f"[{attempted}] admitted={admitted} mismatches={mismatch_count} "
                f"budget_rows={budget_rows} elapsed={elapsed:.1f}s",
                flush=True,
            )
        if args.fail_fast and mismatch_count:
            break

    # Keep deterministic human-useful leading columns, then all arm fields sorted.
    leading = [
        "case_id",
        "family",
        "seed",
        "case_seed",
        "live_k_requested",
        "semantic_support",
        "live_k_exact_match",
        "depth",
        "source_ast_depth",
        "affine_fraction_requested",
        "affine_fraction_realized",
        "reverse_fraction_requested",
        "shared_fraction_requested",
        "source_shared_fraction_realized",
        "source_occurrence_nodes",
        "source_unique_structural_nodes",
        "source_unique_object_nodes",
        "syntactic_support",
        "schedule",
        "all_arms_ok",
        "successful_arms_agree",
        "independent_eval_ok",
        "correctness_status",
    ]
    fieldnames = [f for f in leading if f in all_fieldnames] + sorted(all_fieldnames - set(leading))
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    meta = {
        "protocol": "BENCHMARK_PROTOCOL.md frozen v0.1 + source-integration addendum",
        "scope": sorted(families),
        "attempted_cases": attempted,
        "admitted_cases": admitted,
        "mismatch_count": mismatch_count,
        "rows_with_budget_event": budget_rows,
        "budget": {
            "max_monomials": budget.max_monomials,
            "max_pair_terms_per_multiply": budget.max_pair_terms_per_multiply,
            "max_pair_terms_total": budget.max_pair_terms_total,
        },
        "timing_status": "single-pass local diagnostics; symbolic counters are the primary S1/S2 evidence in this run",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "elapsed_seconds": time.time() - start,
        "output_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "s2_generator_note": (
            "corrected support-preserving generator: parity(x0..x{k-1}) XOR h, where h has no "
            "linear ANF monomials; depth is the recursive mixed-core depth and sharing occurs inside h"
        ),
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(meta, indent=2, sort_keys=True))
    return out, meta_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--families", default="S1,S2")
    parser.add_argument(
        "--output",
        default=str(ROOT / "results" / "raw" / "gate_a_s1_s2.csv"),
    )
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--skip-cases", type=int, default=0)
    parser.add_argument("--max-monomials", type=int, default=150_000)
    parser.add_argument("--max-pair-terms-per-multiply", type=int, default=2_000_000)
    parser.add_argument("--max-pair-terms-total", type=int, default=10_000_000)
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument("--fail-fast", action="store_true")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
