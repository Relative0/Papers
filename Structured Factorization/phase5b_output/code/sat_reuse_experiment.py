#!/usr/bin/env python3
"""Training-only Glucose4 reuse diagnostic; run after principal timings.

Compare three workloads on the same cuts:
  persistent_controlled: one Phase4 controlled encoding and one live solver;
  fresh_solver_same_base: same controlled encoding, new solver for every cut;
  fresh_phase3_per_cut: new cut-specific Phase3 encoding and solver per cut.

The first comparison isolates solver persistence from encoding size/reuse.
The third includes the different encoding's construction and solver loading.
Counters are actual solver counters, never inferred learned-clause counts.
No result is an input to heuristic selection, objective weights or held-out work.

Usage, from phase5b_output, after the principal timing campaign has finished:
  python -B code/sat_reuse_experiment.py
The default output is data/sat_reuse_results.json; per-run events are written to
logs/sat_reuse_events.jsonl. Existing outputs are preserved (use a new --output).
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PHASE4_CODE = ROOT / "reproduction" / "relocated" / "phase4" / "code"
METHODS = ("persistent_controlled", "fresh_solver_same_base", "fresh_phase3_per_cut")
STAT_KEYS = ("conflicts", "decisions", "propagations", "restarts")
ORDER_SEED = 2026092913
REPLICATES = (0, 1, 2)


def load_phase4():
    path = PHASE4_CODE / "incremental_four_corner.py"
    spec = importlib.util.spec_from_file_location("sat_reuse_frozen_incremental", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, module.fc


def cuts_for(n):
    """Ascending bit mask, variable 1 on the left; all unordered proper cuts."""
    return [[v for v in range(1, n + 1) if mask & (1 << (v - 1))]
            for mask in range(1, (1 << n) - 1, 2)]


def expected_statuses(instance, cuts):
    """Independent evaluation only: projection-product criterion, outside timing."""
    n, clauses = instance["n"], instance["clauses"]
    models = [a for a in range(1 << n)
              if all(any(bool(a & (1 << (abs(lit) - 1))) == (lit > 0)
                         for lit in clause) for clause in clauses)]
    if not models:
        raise ValueError("Training diagnostic retains the nonfalse input contract")
    result = []
    for cut in cuts:
        left = sum(1 << (v - 1) for v in cut)
        right = ((1 << n) - 1) ^ left
        separable = len({a & left for a in models}) * len({a & right for a in models}) == len(models)
        result.append(not separable)  # SAT means a rank-two defect exists.
    return result


def solver_stats(solver):
    raw = solver.accum_stats()
    return {key: int(raw.get(key, 0)) for key in STAT_KEYS}


def add_stats(target, source):
    for key in STAT_KEYS:
        target[key] += source[key]


def workload(payload):
    # Imports and module loading are excluded equally from algorithm timing.
    from pysat.solvers import Solver
    inc, phase3 = load_phase4()
    instance, method = payload["instance"], payload["method"]
    n, clauses = instance["n"], instance["clauses"]
    cuts = cuts_for(n)
    details, encodings = [], []
    encode_seconds = solver_setup_seconds = solve_seconds = delete_seconds = 0.0
    setup_stats = {key: 0 for key in STAT_KEYS}
    total_stats = {key: 0 for key in STAT_KEYS}
    controlled = persistent = None
    solver_creations = clause_load_total = 0
    started = time.perf_counter()
    try:
        if method != "fresh_phase3_per_cut":
            start = time.perf_counter()
            controlled = inc.build_controlled_encoding(n, [tuple(c) for c in clauses], [(v,) for v in range(1, n + 1)])
            encode_seconds = time.perf_counter() - start
            encodings.append({"query_index": None, "variables": controlled.nvars, "clauses": len(controlled.clauses)})
        if method == "persistent_controlled":
            start = time.perf_counter()
            persistent = Solver(name="g4", bootstrap_with=controlled.clauses)
            solver_setup_seconds += time.perf_counter() - start
            solver_creations += 1
            clause_load_total += len(controlled.clauses)
            add_stats(setup_stats, solver_stats(persistent))
        for index, cut in enumerate(cuts):
            query_encode = query_setup = query_delete = 0.0
            current = None
            if method == "fresh_phase3_per_cut":
                start = time.perf_counter()
                encoding = phase3.build_defect_encoding(n, [tuple(c) for c in clauses], cut)
                query_encode = time.perf_counter() - start
                encode_seconds += query_encode
                encodings.append({"query_index": index, "variables": encoding.nvars, "clauses": len(encoding.clauses)})
                base_clauses, assumptions = encoding.clauses, []
            else:
                base_clauses = controlled.clauses
                cut_set = set(cut)
                assumptions = [selector if block_index + 1 in cut_set else -selector
                               for block_index, selector in controlled.selectors.items()]
            try:
                if persistent is None:
                    start = time.perf_counter()
                    current = Solver(name="g4", bootstrap_with=base_clauses)
                    query_setup = time.perf_counter() - start
                    solver_setup_seconds += query_setup
                    solver_creations += 1
                    clause_load_total += len(base_clauses)
                    add_stats(setup_stats, solver_stats(current))
                else:
                    current = persistent
                before = solver_stats(current)
                start = time.perf_counter()
                sat = bool(current.solve(assumptions=assumptions))
                query_solve = time.perf_counter() - start
                solve_seconds += query_solve
                after = solver_stats(current)
                delta = {key: after[key] - before[key] for key in STAT_KEYS}
                if any(value < 0 for value in delta.values()):
                    raise AssertionError("Expected monotone cumulative solver counters")
                if persistent is None:
                    add_stats(total_stats, after)
            finally:
                if current is not None and persistent is None:
                    start = time.perf_counter()
                    current.delete()
                    query_delete = time.perf_counter() - start
                    delete_seconds += query_delete
            details.append({"query_index": index, "cut": cut, "sat_defect": sat,
                            "encoding_seconds": query_encode, "solver_setup_seconds": query_setup,
                            "solve_seconds": query_solve, "solver_delete_seconds": query_delete,
                            "solve_counter_deltas": delta, "cumulative_solver_counters_after": after})
        if persistent is not None:
            add_stats(total_stats, solver_stats(persistent))
    finally:
        if persistent is not None:
            start = time.perf_counter()
            persistent.delete()
            delete_seconds += time.perf_counter() - start
    elapsed = time.perf_counter() - started
    # Hashing, JSON serialization and independent correctness checks are outside timing.
    controlled_hash = hashlib.sha256(json.dumps(controlled.clauses, separators=(",", ":")).encode()).hexdigest() if controlled is not None else None
    return {"id": instance["id"], "family": instance["family"], "n": n, "split": "train",
            "replicate": payload["replicate"], "method": method, "status": "ok",
            "end_to_end_seconds": elapsed, "encoding_seconds": encode_seconds,
            "solver_setup_seconds": solver_setup_seconds, "solve_seconds": solve_seconds,
            "solver_delete_seconds": delete_seconds, "solver_creations": solver_creations,
            "solver_clause_load_total": clause_load_total,
            "encoded_clause_emission_total": sum(e["clauses"] for e in encodings),
            "setup_solver_counters": setup_stats, "total_solver_counters": total_stats,
            "query_count": len(cuts), "controlled_base_sha256": controlled_hash,
            "encodings": encodings, "queries": details}


def geomean(values):
    return math.exp(statistics.mean(math.log(value) for value in values))


def summarize(rows):
    good = [r for r in rows if r["status"] == "ok" and r.get("all_statuses_correct")]
    output = {"completed_runs": len(good), "failed_or_incorrect_runs": len(rows) - len(good),
              "checked_query_results": sum(r["query_count"] for r in good), "methods": {}}
    for method in METHODS:
        group = [r for r in good if r["method"] == method]
        if group:
            output["methods"][method] = {"runs": len(group),
                **{key: {"median": statistics.median(r[key] for r in group),
                         "mean": statistics.mean(r[key] for r in group)}
                   for key in ("end_to_end_seconds", "encoding_seconds", "solver_setup_seconds", "solve_seconds")},
                "counter_totals": {key: sum(r["total_solver_counters"][key] for r in group) for key in STAT_KEYS}}
    # Paired instance medians of all three reps; no survivor-only incomplete cells.
    cells = {}
    for row in good:
        cells.setdefault((row["id"], row["method"]), []).append(row)
    pairs = []
    for instance_id in sorted({r["id"] for r in good}):
        if all(len(cells.get((instance_id, method), [])) == 3 for method in METHODS):
            medians = {method: statistics.median(r["end_to_end_seconds"] for r in cells[instance_id, method]) for method in METHODS}
            pairs.append({"id": instance_id, "median_end_to_end_seconds": medians,
                          "persistent_over_fresh_same_base": medians[METHODS[0]] / medians[METHODS[1]],
                          "persistent_over_fresh_phase3": medians[METHODS[0]] / medians[METHODS[2]]})
    output["paired_instance_medians"] = pairs
    output["full_campaign_pairing_complete"] = len(pairs) == 20 and len(good) == 180
    if output["full_campaign_pairing_complete"]:
        output["geometric_mean_paired_ratios"] = {key: geomean([p[key] for p in pairs]) for key in
            ("persistent_over_fresh_same_base", "persistent_over_fresh_phase3")}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "sat_reuse_results.json")
    parser.add_argument("--timeout", type=float, default=30.0, help="Full worker process watchdog per instance/method/replicate")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("Preserving existing diagnostic output; select a new --output")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be positive")
    manifest_path = ROOT / "data" / "benchmark_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    instances = [r for r in manifest["records"] if r["split"] == "train"]
    if len(instances) != 20 or {r["n"] for r in instances} != {6, 8}:
        raise SystemExit("Expected exactly the 20 frozen n=6,8 training instances")
    instance_by_id = {r["id"]: r for r in instances}
    expected = {r["id"]: expected_statuses(r, cuts_for(r["n"])) for r in instances}
    sources = [Path(__file__).resolve(), manifest_path, PHASE4_CODE / "incremental_four_corner.py", PHASE4_CODE / "four_corner_sat_phase3_baseline.py"]
    metadata = {"scope": "Post-primary training-only SAT reuse diagnostic; no held-out instances or heuristic feedback",
                "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "python": sys.version, "platform": platform.platform(), "executable": sys.executable,
                "python_sat_version": importlib.metadata.version("python-sat"), "solver": "PySAT g4 / Glucose4",
                "solver_constructor_options": {"name": "g4"}, "replicates": list(REPLICATES),
                "method_order": "Cyclic rotations across the three repetitions, balanced within each instance",
                "instance_order_seed": ORDER_SEED, "query_order": "All ascending odd proper masks; variable 1 on left",
                "instance_ids": [r["id"] for r in instances], "worker_timeout_seconds": args.timeout,
                "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                "timing_contract": "End-to-end includes encoding, solver setup, assumptions, solving, counter collection, query record assembly and solver deletion; excludes imports, input parsing, hashing, JSON I/O and independent evaluation. Full subprocess time is recorded separately.",
                "counter_contract": "Raw solver totals include initialization propagation; per-query deltas subtract pre-solve counters. No learned-clause count is measured or inferred.",
                "encoding_contract": "Both controlled methods use the byte-identical Phase4 selector encoding over singleton blocks, not the Phase5B equality-enabled shrinking encoding. The fresh Phase3 method has its own cut-specific CNF.",
                "failures_contract": "Timeout/error/incorrect runs remain explicit. No geometric-mean comparison is emitted unless all 180 runs and every expected query succeed."}
    rows = []
    output.parent.mkdir(parents=True, exist_ok=True)
    log = ROOT / "logs" / ("sat_reuse_events.jsonl" if output.name == "sat_reuse_results.json" else output.stem + "_events.jsonl")
    log.parent.mkdir(parents=True, exist_ok=True)
    if log.exists():
        raise SystemExit("Preserving existing diagnostic event log; select a new --output")
    def checkpoint():
        output.write_text(json.dumps({"metadata": metadata, "summary": summarize(rows), "runs": rows}, indent=2) + "\n", encoding="utf-8")
    checkpoint()
    for replicate in REPLICATES:
        ordered_ids = [r["id"] for r in instances]
        random.Random(ORDER_SEED + replicate).shuffle(ordered_ids)
        for instance_id in ordered_ids:
            instance = instance_by_id[instance_id]
            method_order = METHODS[replicate:] + METHODS[:replicate]
            for method in method_order:
                # The worker receives neither expected statuses nor any prime partition.
                payload = {"instance": instance, "method": method, "replicate": replicate}
                start = time.perf_counter()
                try:
                    proc = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "worker"],
                                          input=json.dumps(payload), capture_output=True, text=True, timeout=args.timeout)
                    if proc.returncode != 0:
                        raise RuntimeError(proc.stderr[-12000:] or proc.stdout[-12000:])
                    row = json.loads(proc.stdout)
                    observed = [q["sat_defect"] for q in row["queries"]]
                    row["all_statuses_correct"] = observed == expected[instance_id]
                    row["status_disagreements"] = [i for i, (actual, wanted) in enumerate(zip(observed, expected[instance_id])) if actual != wanted]
                    if len(observed) != len(expected[instance_id]):
                        row["status"] = "incorrect_query_count"
                    elif not row["all_statuses_correct"]:
                        row["status"] = "incorrect"
                except subprocess.TimeoutExpired:
                    row = {"id": instance_id, "family": instance["family"], "n": instance["n"], "replicate": replicate, "method": method, "status": "timeout"}
                except Exception as exc:
                    row = {"id": instance_id, "family": instance["family"], "n": instance["n"], "replicate": replicate, "method": method, "status": "error", "error": str(exc)}
                row["process_wall_seconds"] = time.perf_counter() - start
                rows.append(row)
                event = {key: row[key] for key in ("id", "replicate", "method", "status", "process_wall_seconds")}
                event["completed_runs"] = len(rows)
                with log.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(event) + "\n")
                checkpoint()
                if row["status"] != "ok":
                    print(json.dumps(event), flush=True)
                    raise SystemExit("Diagnostic stopped on explicit failure; partial evidence preserved")
            if len(rows) % 30 == 0:
                print(f"SAT reuse diagnostic: {len(rows)}/180 runs; all statuses agree", flush=True)
    # The primary isolated comparison must really have identical permanent clauses.
    for instance_id in instance_by_id:
        hashes = {r["controlled_base_sha256"] for r in rows if r["id"] == instance_id and r["method"] in METHODS[:2]}
        if len(hashes) != 1:
            raise AssertionError("Controlled base changed across methods or repetitions")
    metadata["controlled_bases_identical_across_methods_and_replicates"] = True
    metadata["expected_statuses_by_instance"] = expected
    checkpoint()
    print(json.dumps({"output": str(output), "runs": len(rows), "summary": summarize(rows)}, indent=2), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        try:
            print(json.dumps(workload(json.load(sys.stdin)), separators=(",", ":")))
        except Exception:
            traceback.print_exc()
            raise SystemExit(1)
    else:
        main()
