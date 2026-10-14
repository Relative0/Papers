#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]


def f(row, key, default=float("nan")):
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return default


def i(row, key, default=0):
    try:
        return int(float(row[key]))
    except (KeyError, TypeError, ValueError):
        return default


def median(values):
    vals = [v for v in values if math.isfinite(v)]
    return statistics.median(vals) if vals else float("nan")


def geomean(values):
    vals = [v for v in values if math.isfinite(v) and v > 0]
    return math.exp(statistics.fmean(math.log(v) for v in vals)) if vals else float("nan")


def load(path: Path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def analyze(rows):
    admitted = [r for r in rows if i(r, "all_arms_ok") == 1 and r.get("correctness_status") == "OK"]
    s1 = [r for r in admitted if r["family"] == "S1"]
    s2 = [r for r in admitted if r["family"] == "S2"]

    result: dict[str, Any] = {
        "rows_total": len(rows),
        "rows_admitted": len(admitted),
        "correctness_failures": sum(r.get("correctness_status") not in ("OK", "NO_SUCCESSFUL_ARM") for r in rows),
        "budget_or_error_rows": sum(i(r, "all_arms_ok") == 0 for r in rows),
        "S1_rows_admitted": len(s1),
        "S2_rows_admitted": len(s2),
    }

    # SC-A: strict check of every predeclared S1 depth>=6, affine<=0.75 cell,
    # aggregating the 50 seeds and reverse-fraction subcells separately.
    strata = defaultdict(list)
    for r in s1:
        depth = i(r, "depth")
        aff = f(r, "affine_fraction_requested")
        rev = f(r, "reverse_fraction_requested")
        if depth >= 6 and aff <= 0.75:
            strata[(depth, aff, rev)].append(r)
    sca_rows = []
    for key in sorted(strata):
        subset = strata[key]
        direct_med = median(f(r, "direct_sparse_anf_multiplications") for r in subset)
        cm_med = median(f(r, "cm_frontend_sparse_multiplications") for r in subset)
        ratio = cm_med / direct_med if direct_med > 0 else (1.0 if cm_med == 0 else math.inf)
        sca_rows.append(
            {
                "depth": key[0],
                "affine_fraction": key[1],
                "reverse_fraction": key[2],
                "n": len(subset),
                "direct_multiplications_median": direct_med,
                "cm_multiplications_median": cm_med,
                "cm_over_direct_median_count": ratio,
                "passes_le_0_50": bool(ratio <= 0.50),
            }
        )
    result["SC_A_strata"] = sca_rows
    result["SC_A_pass_strict_all_predeclared_strata"] = bool(sca_rows) and all(x["passes_le_0_50"] for x in sca_rows)

    # Synthetic CM-specific comparison. This cannot satisfy SC-B (natural-only),
    # but it can falsify uniqueness on the mechanism workloads.
    def compare_counts(rows, metric):
        cmk = f"cm_frontend_sparse_{metric}"
        gk = f"generic_2support_sparse_{metric}"
        better = equal = worse = 0
        ratios = []
        for r in rows:
            cm = f(r, cmk)
            g = f(r, gk)
            if cm < g:
                better += 1
            elif cm > g:
                worse += 1
            else:
                equal += 1
            if g > 0:
                ratios.append(cm / g)
            elif cm == 0:
                ratios.append(1.0)
        return {
            "cm_better": better,
            "equal": equal,
            "cm_worse": worse,
            "geomean_ratio": geomean(ratios),
            "median_ratio": median(ratios),
        }

    result["synthetic_cm_vs_generic"] = {
        "S1_multiplications": compare_counts(s1, "multiplications"),
        "S1_pair_terms": compare_counts(s1, "pair_terms"),
        "S1_peak_monomials": compare_counts(s1, "peak_monomials"),
        "S2_multiplications": compare_counts(s2, "multiplications"),
        "S2_pair_terms": compare_counts(s2, "pair_terms"),
        "S2_peak_monomials": compare_counts(s2, "peak_monomials"),
    }

    # S2 exact semantic-support retention.
    result["S2_live_k_exact_match_fraction"] = (
        sum(i(r, "live_k_exact_match") for r in s2) / len(s2) if s2 else float("nan")
    )

    # SC-E diagnostic on no-CM-fold rows. Timings are single-pass local diagnostics,
    # so this is not elevated to an inferential timing claim.
    no_fold = [r for r in s2 if i(r, "cm_frontend_sparse_successful_folds") == 0]
    timing_ratios = [f(r, "cm_over_generic_end_to_end_ns") for r in no_fold]
    result["SC_E_local_timing_diagnostic"] = {
        "no_cm_fold_rows": len(no_fold),
        "median_cm_over_generic_end_to_end_ns": median(timing_ratios),
        "passes_median_le_1_10_descriptive": bool(timing_ratios and median(timing_ratios) <= 1.10),
        "status": "diagnostic_only_single_pass_local_timing",
    }

    # Compact S2 mechanism summary by requested sharing fraction.
    s2_share = []
    groups = defaultdict(list)
    for r in s2:
        groups[f(r, "shared_fraction_requested")].append(r)
    for share in sorted(groups):
        subset = groups[share]
        s2_share.append(
            {
                "shared_fraction_requested": share,
                "n": len(subset),
                "cm_successful_folds_median": median(f(r, "cm_frontend_sparse_successful_folds") for r in subset),
                "generic_successful_folds_median": median(f(r, "generic_2support_sparse_successful_folds") for r in subset),
                "cm_multiplications_median": median(f(r, "cm_frontend_sparse_multiplications") for r in subset),
                "generic_multiplications_median": median(f(r, "generic_2support_sparse_multiplications") for r in subset),
                "direct_multiplications_median": median(f(r, "direct_sparse_anf_multiplications") for r in subset),
            }
        )
    result["S2_by_requested_sharing"] = s2_share

    result["SC_B_status"] = "NOT_TESTED_BY_S1_S2: protocol requires a predeclared natural stratum"
    result["SC_C_status"] = "NOT_TESTED: XAG backend not part of this S1/S2 run"
    result["SC_D_status"] = "NOT_TESTED: specialized ZDD/FDD backend not part of this S1/S2 run"
    return result


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Gate A S1/S2 local results",
        "",
        "This report is generated from the frozen S1/S2 workload axes. Symbolic counters are the primary evidence. Single-pass local timings are retained only as diagnostics and are not used for an inferential speed claim.",
        "",
        f"- Total rows: **{summary['rows_total']}**",
        f"- Matched/correct admitted rows: **{summary['rows_admitted']}**",
        f"- Budget/error rows: **{summary['budget_or_error_rows']}**",
        f"- S1 admitted: **{summary['S1_rows_admitted']}**",
        f"- S2 admitted: **{summary['S2_rows_admitted']}**",
        f"- S2 exact semantic-support match: **{summary['S2_live_k_exact_match_fraction']:.3f}**",
        "",
        "## SC-A — folding mechanism",
        "",
        f"Strict all-predeclared-strata result: **{'PASS' if summary['SC_A_pass_strict_all_predeclared_strata'] else 'FAIL/INCOMPLETE'}**.",
        "",
        "| depth | affine | reversed | n | direct mult median | CM mult median | CM/direct | pass |",
        "|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for x in summary["SC_A_strata"]:
        lines.append(
            f"| {x['depth']} | {x['affine_fraction']:.2f} | {x['reverse_fraction']:.2f} | {x['n']} | "
            f"{x['direct_multiplications_median']:.3g} | {x['cm_multiplications_median']:.3g} | "
            f"{x['cm_over_direct_median_count']:.3g} | {'yes' if x['passes_le_0_50'] else 'no'} |"
        )

    lines += ["", "## CM vs strong generic 2-support comparator", ""]
    for name, x in summary["synthetic_cm_vs_generic"].items():
        lines.append(
            f"- `{name}`: CM better {x['cm_better']}, equal {x['equal']}, worse {x['cm_worse']}; "
            f"geomean ratio {x['geomean_ratio']:.6g}."
        )
    e = summary["SC_E_local_timing_diagnostic"]
    lines += [
        "",
        "## SC-E local diagnostic",
        "",
        f"Among {e['no_cm_fold_rows']} admitted S2 rows with zero CM folds, the single-pass median CM/generic end-to-end timing ratio was **{e['median_cm_over_generic_end_to_end_ns']:.3f}**. This is diagnostic only; repeated isolated timing is required before treating it as evidence.",
        "",
        "## Gates not answered by S1/S2",
        "",
        f"- SC-B: {summary['SC_B_status']}",
        f"- SC-C: {summary['SC_C_status']}",
        f"- SC-D: {summary['SC_D_status']}",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "results" / "raw" / "gate_a_s1_s2.csv"))
    ap.add_argument("--json", default=str(ROOT / "results" / "gate_a_s1_s2_summary.json"))
    ap.add_argument("--markdown", default=str(ROOT / "results" / "GATE_A_S1_S2_RESULTS.md"))
    args = ap.parse_args()
    rows = load(Path(args.input))
    summary = analyze(rows)
    Path(args.json).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    Path(args.markdown).write_text(markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
