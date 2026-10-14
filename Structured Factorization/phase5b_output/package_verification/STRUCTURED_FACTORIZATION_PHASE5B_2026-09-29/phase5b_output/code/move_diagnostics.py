"""Post-campaign residual-cost diagnostics. NEVER feeds timing into search.

Run only after all principal performance runs have finished. One fresh worker
measures each distinct (instance, certified direct partition) exactly once;
these measurements are explicitly reused across move/method/seed mappings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
from time import perf_counter
import traceback

ROOT = Path(__file__).resolve().parents[1]


def canonical(partition):
    return sorted([sorted(b) for b in partition], key=lambda b: tuple(b))


def serialized(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def identity(value):
    return hashlib.sha256(serialized(value).encode()).hexdigest()


def worker(payload):
    from hybrid_core import exact_refine
    start = perf_counter()
    result = exact_refine(payload["n"], payload["clauses"], payload["partition"], carrier=payload["carrier"])
    return {"status": "ok", "exact": result, "diagnostic_wall_seconds": perf_counter() - start}


def load_inputs():
    files = sorted((ROOT / "data").glob("*_results.jsonl"))
    if not files:
        raise SystemExit("No completed principal result files exist")
    manifest_path = ROOT / "data" / "benchmark_manifest.json"
    truth_path = ROOT / "data" / "independent_ground_truth.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = {r["id"]: r for r in manifest["records"]}
    truths = json.loads(truth_path.read_text(encoding="utf-8"))
    paths = files + [manifest_path, truth_path, Path(__file__).resolve(), ROOT / "code" / "hybrid_core.py"]
    receipt = {"files": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
               "timeout_seconds": 15, "measurement_cache": "one fresh process per unique (instance, certified partition)",
               "purpose": "post-campaign exploratory diagnostics; never fed back into objectives"}
    receipt_path = ROOT / "data" / "move_diagnostics_freeze.json"
    if receipt_path.exists():
        if json.loads(receipt_path.read_text(encoding="utf-8")) != receipt:
            raise SystemExit("Diagnostic inputs changed; preserve the previous diagnostic directory before rerunning")
    else:
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    partitions, moves, mappings = {}, {}, []
    for file in files:
        for row_no, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            row = json.loads(line)
            if row["status"] != "ok":
                continue
            traces = row.get("moves", [])
            if not traces:
                continue
            if row["id"] not in records or row["id"] not in truths:
                raise ValueError("Missing input or ground truth for " + row["id"])
            # Total compilation/extraction is an accumulated sum over initial
            # compilation and every recorded move, so recover the initial cost.
            compile_by_tree = {serialized(traces[0]["parent_tree"]): {
                "compile_seconds": row["compile_seconds"] - sum(m["compile_seconds"] for m in traces),
                "extract_seconds": row["extract_seconds"] - sum(m["extract_seconds"] for m in traces),
                "provenance": "initial cost from run total minus all recorded move costs"}}
            for move_index, trace in enumerate(traces):
                parent_partition = canonical(trace["parent_partition"])
                candidate_partition = canonical(trace["direct_partition"])
                parent_key = identity([row["id"], parent_partition])
                candidate_key = identity([row["id"], candidate_partition])
                for key, part in [(parent_key, parent_partition), (candidate_key, candidate_partition)]:
                    value = {"id": row["id"], "partition": part}
                    assert key not in partitions or partitions[key] == value
                    partitions[key] = value
                move_key = identity([row["id"], trace["parent_tree"], trace["tree"]])
                structural = {
                    "move_id": move_key, "id": row["id"], "family": row["family"], "split": row["split"],
                    "parent_tree": trace["parent_tree"], "candidate_tree": trace["tree"],
                    "parent_measurement_id": parent_key, "candidate_measurement_id": candidate_key,
                    "parent_partition": parent_partition, "candidate_partition": candidate_partition,
                    "parent_sdd_size": trace["sdd_size"] - trace["delta_size"],
                    "candidate_sdd_size": trace["sdd_size"], "delta_size": trace["delta_size"],
                    "parent_exposed_blocks": trace["exposed_blocks"] - trace["delta_exposure"],
                    "candidate_exposed_blocks": trace["exposed_blocks"], "delta_exposure": trace["delta_exposure"],
                    "parent_residual_volume": trace["residual_volume"] - trace["delta_residual_volume"],
                    "candidate_residual_volume": trace["residual_volume"], "delta_residual_volume": trace["delta_residual_volume"],
                }
                assert move_key not in moves or moves[move_key] == structural, "Repeated move has inconsistent exact structure"
                moves[move_key] = structural
                parent_cost = compile_by_tree[serialized(trace["parent_tree"])]
                mapping = {
                    "move_id": move_key, "source_file": str(file.relative_to(ROOT)), "source_row": row_no,
                    "move_index": move_index, "id": row["id"], "method": row["method"], "seed": row["seed"],
                    "parent_measurement_id": parent_key, "candidate_measurement_id": candidate_key,
                    "candidate_compile_seconds": trace["compile_seconds"],
                    "candidate_extract_seconds": trace["extract_seconds"],
                    "parent_compile_seconds": parent_cost["compile_seconds"],
                    "parent_extract_seconds": parent_cost["extract_seconds"],
                    "parent_compile_provenance": parent_cost["provenance"],
                    "objective_score": trace["score"],
                    "residual_timing_reused": True,
                }
                mappings.append(mapping)
                compile_by_tree[serialized(trace["tree"])] = {
                    "compile_seconds": trace["compile_seconds"], "extract_seconds": trace["extract_seconds"],
                    "provenance": "previous candidate compilation in this same principal run"}
    return records, truths, partitions, moves, mappings


def run():
    start = perf_counter()
    records, truths, partitions, moves, mappings = load_inputs()
    measurement_file = ROOT / "data" / "move_residual_measurements.jsonl"
    measurements = {}
    if measurement_file.exists():
        measurements = {x["measurement_id"]: x for x in map(json.loads, measurement_file.read_text(encoding="utf-8").splitlines())}
    for index, (key, item) in enumerate(sorted(partitions.items()), 1):
        if key in measurements:
            continue
        record = records[item["id"]]
        payload = {"n": record["n"], "clauses": record["clauses"], "carrier": record["carrier"], "partition": item["partition"]}
        begin = perf_counter()
        try:
            process = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--worker"],
                                     input=json.dumps(payload), text=True, capture_output=True, timeout=15)
            if process.returncode:
                raise RuntimeError(process.stderr[-6000:])
            result = json.loads(process.stdout)
            result["semantic_correct"] = canonical(result["exact"]["semantic_partition"]) == canonical(truths[item["id"]]["semantic"])
            result["simultaneous_correct"] = canonical(result["exact"]["partition"]) == canonical(truths[item["id"]]["simultaneous"])
        except subprocess.TimeoutExpired:
            result = {"status": "timeout", "semantic_correct": None, "simultaneous_correct": None}
        except Exception as exc:
            result = {"status": "error", "error": str(exc), "semantic_correct": None, "simultaneous_correct": None}
        result.update({"measurement_id": key, "id": item["id"], "partition": item["partition"],
                       "process_wall_seconds": perf_counter() - begin,
                       "cache_policy": "one measurement reused across all occurrences of this instance/partition"})
        measurements[key] = result
        with measurement_file.open("a", encoding="utf-8") as stream:
            stream.write(serialized(result) + "\n")
        if result["status"] == "error" or result["semantic_correct"] is False or result["simultaneous_correct"] is False:
            print(json.dumps(result), flush=True)
            raise SystemExit("Diagnostic correctness/tool failure; retain logs and investigate")
        if index % 25 == 0:
            print(f"Residual diagnostic {index}/{len(partitions)}: {result['status']}", flush=True)

    metrics = ["sat_calls", "sat_seconds", "sat_setup_seconds", "residual_seconds", "conflicts", "decisions", "propagations", "restarts"]
    alignment = {k: 0 for k in ["size_down_exposure_up", "size_down_exposure_down", "size_up_exposure_up", "size_up_exposure_down",
                                "size_equal_exposure_changes", "exposure_equal_size_changes", "both_equal"]}
    pareto = {"candidate_dominates_size_calls": 0, "parent_dominates_size_calls": 0,
              "tradeoff_size_calls": 0, "equal_size_calls": 0, "unavailable": 0}
    grouped_mappings = {}
    for mapping in mappings:
        grouped_mappings.setdefault(mapping["move_id"], []).append(mapping)
    move_records = []
    for key, item in sorted(moves.items()):
        parent = measurements[item["parent_measurement_id"]]
        candidate = measurements[item["candidate_measurement_id"]]
        record = dict(item)
        record["mapping_count"] = len(grouped_mappings[key])
        record["residual_timing_reused"] = True
        record["parent_status"], record["candidate_status"] = parent["status"], candidate["status"]
        record["candidate_compile_seconds_samples"] = [m["candidate_compile_seconds"] for m in grouped_mappings[key]]
        record["parent_compile_seconds_samples"] = [m["parent_compile_seconds"] for m in grouped_mappings[key]]
        record["candidate_compile_seconds_median"] = statistics.median(record["candidate_compile_seconds_samples"])
        record["parent_compile_seconds_median"] = statistics.median(record["parent_compile_seconds_samples"])
        for metric in metrics:
            record["parent_" + metric] = parent.get("exact", {}).get(metric)
            record["candidate_" + metric] = candidate.get("exact", {}).get(metric)
            record["delta_" + metric] = (candidate["exact"][metric] - parent["exact"][metric]
                                         if parent["status"] == candidate["status"] == "ok" else None)
        ds, de = record["delta_size"], record["delta_exposure"]
        if ds and de:
            alignment[f"size_{'down' if ds < 0 else 'up'}_exposure_{'down' if de < 0 else 'up'}"] += 1
        elif ds:
            alignment["exposure_equal_size_changes"] += 1
        elif de:
            alignment["size_equal_exposure_changes"] += 1
        else:
            alignment["both_equal"] += 1
        dc = record["delta_sat_calls"]
        if dc is None:
            pareto["unavailable"] += 1
        elif ds <= 0 and dc <= 0 and (ds < 0 or dc < 0):
            pareto["candidate_dominates_size_calls"] += 1
        elif ds >= 0 and dc >= 0 and (ds > 0 or dc > 0):
            pareto["parent_dominates_size_calls"] += 1
        elif ds == dc == 0:
            pareto["equal_size_calls"] += 1
        else:
            pareto["tradeoff_size_calls"] += 1
        move_records.append(record)
    (ROOT / "data" / "move_diagnostics.jsonl").write_text("".join(serialized(x) + "\n" for x in move_records), encoding="utf-8")
    (ROOT / "data" / "move_diagnostic_mapping.jsonl").write_text("".join(serialized(x) + "\n" for x in mappings), encoding="utf-8")
    summary = {
        "unique_moves": len(moves), "original_move_occurrences": len(mappings),
        "unique_residual_measurements": len(partitions),
        "measurement_status": {status: sum(m["status"] == status for m in measurements.values()) for status in ["ok", "timeout", "error"]},
        "correctness_disagreements": sum(m.get("semantic_correct") is False or m.get("simultaneous_correct") is False for m in measurements.values()),
        "size_exposure_alignment": alignment, "size_sat_calls_pareto": pareto,
        "diagnostic_total_seconds": perf_counter() - start,
        "interpretation": "Exploratory post-campaign measurements. Each unique instance/partition measured once, then cached and reused across all move occurrences. No timing replicates or inferential runtime claims; timing was never fed back into objectives. Compilation samples are original principal-run measurements, with initial parent compilation recovered by subtraction from run totals.",
    }
    (ROOT / "data" / "move_diagnostics_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    if "--worker" in sys.argv:
        print(json.dumps(worker(json.load(sys.stdin)), separators=(",", ":")))
    else:
        run()
