#!/usr/bin/env python3
"""Reproduce frozen Phase 4/5 claims without writing into their archives.

Only literal machine-specific path strings are changed in executable copies.
The independent audit computes projection products directly; it does not use
the semantic prime partition to obtain factor-exposure scores.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys
import time
from contextlib import redirect_stdout, redirect_stderr

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parents[1]
ARCHIVE = OUT.parent / "continuity_archive"
REP = OUT / "reproduction"
PHASES = {
    "phase4": ARCHIVE / "03_UNPACKED_PHASE4" / "structured_factorization_phase4",
    "phase5": ARCHIVE / "04_UNPACKED_PHASE5" / "phase5_output",
}
CAMPAIGNS = [
    ("phase4", "sdd_direct_extraction.py", ["sdd_extraction_validation.json"]),
    ("phase4", "cm_operator_tree_factor.py", ["operator_tree_validation.json"]),
    ("phase4", "validate_incremental.py", ["incremental_validation.json", "incremental_example_base.cnf", "incremental_example_queries.json"]),
    ("phase5", "vtree_exhaustive.py", ["n4_vtree_exhaustive.json", "n4_vtree_per_tree.csv"]),
    ("phase5", "defect_localization.py", ["defect_localization_counterexamples.json"]),
    ("phase5", "benchmark_vtrees.py", ["n5_benchmark_results.json", "n5_benchmark_summary.csv", "n5_benchmark_records.csv"]),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def prepare():
    translations = {
        "/mnt/data/phase5_work/structured_factorization_phase4/code": str(REP / "relocated" / "phase4" / "code").replace("\\", "/"),
        "/mnt/data/structured_factorization_phase4": str(REP / "relocated" / "phase4").replace("\\", "/"),
        "/mnt/data/phase5_output": str(REP / "relocated" / "phase5").replace("\\", "/"),
    }
    records = []
    for phase, src in PHASES.items():
        dest = REP / "relocated" / phase
        (dest / "code").mkdir(parents=True, exist_ok=True)
        (dest / "data").mkdir(parents=True, exist_ok=True)
        for source in sorted((src / "code").glob("*.py")):
            original = REP / "frozen_original" / phase / "code" / source.name
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, original)
            text = source.read_text(encoding="utf-8")
            changes = {}
            for old, new in translations.items():
                count = text.count(old)
                if count:
                    changes[old] = {"replacement": new, "occurrences": count}
                    text = text.replace(old, new)
            relocated = dest / "code" / source.name
            relocated.write_text(text, encoding="utf-8", newline="\n")
            records.append({"archive_source": str(source.relative_to(ARCHIVE)), "original_copy": str(original.relative_to(OUT)),
                            "relocated_copy": str(relocated.relative_to(OUT)), "archive_sha256": sha(source),
                            "original_copy_sha256": sha(original), "relocated_sha256": sha(relocated), "literal_path_changes": changes})
    dump(REP / "source_relocation_manifest.json", records)
    return records


def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items() if k != "runtime_seconds"}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj


def compare_file(phase, name):
    expected = PHASES[phase] / "data" / name
    actual = REP / "relocated" / phase / "data" / name
    if name.endswith(".json"):
        a = normalize(json.loads(actual.read_text()))
        e = normalize(json.loads(expected.read_text()))
        mode = "parsed JSON; ignore runtime_seconds only"
    elif name.endswith(".csv"):
        a = list(csv.DictReader(io.StringIO(actual.read_text())))
        e = list(csv.DictReader(io.StringIO(expected.read_text())))
        mode = "parsed CSV rows"
    else:
        a, e = actual.read_text().splitlines(), expected.read_text().splitlines()
        mode = "text lines; ignore platform newlines"
    return {"file": name, "match": a == e, "comparison": mode, "actual_sha256": sha(actual), "frozen_sha256": sha(expected)}


def run_frozen():
    records = prepare()
    reports = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    logs = REP / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    for phase, script, outputs in CAMPAIGNS:
        label = phase + "_" + Path(script).stem
        start = time.perf_counter()
        cmd = [sys.executable, "-B", str(REP / "relocated" / phase / "code" / script)]
        with (logs / (label + ".stdout.txt")).open("w", encoding="utf-8") as out, (logs / (label + ".stderr.txt")).open("w", encoding="utf-8") as err:
            proc = subprocess.run(cmd, cwd=REP / "relocated" / phase, env=env, stdout=out, stderr=err)
        row = {"campaign": label, "command": cmd, "returncode": proc.returncode, "wall_seconds": time.perf_counter() - start,
               "stdout": str((logs / (label + ".stdout.txt")).relative_to(OUT)), "stderr": str((logs / (label + ".stderr.txt")).relative_to(OUT))}
        row["comparisons"] = [compare_file(phase, name) for name in outputs] if proc.returncode == 0 else []
        row["passed"] = proc.returncode == 0 and all(x["match"] for x in row["comparisons"])
        reports.append(row)
        dump(REP / "frozen_comparison_report.json", reports)
        print(label, "PASS" if row["passed"] else "FAIL", round(row["wall_seconds"], 3), flush=True)
        if not row["passed"]:
            raise RuntimeError("Frozen reproduction failed: " + label)
    for record in records:
        if sha(ARCHIVE / record["archive_source"]) != record["archive_sha256"]:
            raise RuntimeError("Archive source changed: " + record["archive_source"])
    dump(REP / "runtime.json", {"python": sys.version, "executable": sys.executable, "platform": platform.platform(),
                               "python_hash_seed": "0 (frozen subprocesses)", "python_dont_write_bytecode": True,
                               "archive_source_hashes_unchanged": True})


def masks(tree):
    if tree[0] == "L":
        return (1 << tree[1], None, None)
    left, right = masks(tree[1]), masks(tree[2])
    return (left[0] | right[0], left, right)


def extract_by_projection(sizes, tree):
    """Use |pi_U(R)|=|pi_L(R)||pi_R(R)|; no prime partition input."""
    whole, left, right = tree
    if left is None or sizes[whole] != sizes[left[0]] * sizes[right[0]]:
        return (tuple(i for i in range(whole.bit_length()) if whole & (1 << i)),)
    return tuple(sorted(extract_by_projection(sizes, left) + extract_by_projection(sizes, right)))


def projection_sizes(bits, n):
    sats = [a for a in range(1 << n) if bits & (1 << a)]
    return [len({a & mask for a in sats}) for mask in range(1 << n)]


def partitions(labels):
    if not labels:
        yield ()
        return
    first, *rest = labels
    for p in partitions(rest):
        yield ((first,),) + p
        for j in range(len(p)):
            yield p[:j] + (tuple(sorted((first,) + p[j])),) + p[j + 1:]


def run_independent_n4():
    sys.path[:0] = [str(REP / "relocated" / "phase4" / "code"), str(REP / "relocated" / "phase5" / "code")]
    sdd = importlib.import_module("sdd_direct_extraction")
    ve = importlib.import_module("vtree_exhaustive")
    trees = ve.all_vtrees(4)
    encoded = [masks(t) for t in trees]
    parts = [(p, [sum(1 << i for i in b) for b in p]) for p in partitions(list(range(4)))]
    failures = []
    decomp = 0
    aligned_counts = [0] * len(trees)
    decomposable_aligned_counts = [0] * len(trees)
    exposure_pairs = 0
    cut_checks = 0
    prime_aligned_pairs = 0
    # Every relation is a subset of four-bit assignments. This cache computes
    # existential projections by set union, independently of rank/prime code.
    projections = [[0] * (1 << 16) for _ in range(16)]
    for bits in range(1, 1 << 16):
        low = bits & -bits
        assignment = low.bit_length() - 1
        rest = bits ^ low
        for mask in range(16):
            projections[mask][bits] = projections[mask][rest] | (1 << (assignment & mask))
    start = time.perf_counter()
    for bits in range(1, 1 << 16):
        sizes = [projections[mask][bits].bit_count() for mask in range(16)]
        valid = []
        for p, pmasks in parts:
            count = 1
            for mask in pmasks:
                count *= sizes[mask]
            if count == sizes[15]:
                valid.append(tuple(sorted(p)))
        max_count = max(map(len, valid))
        best = {p for p in valid if len(p) == max_count}
        if len(best) != 1:
            failures.append({"bits": bits, "kind": "nonunique independent optimum"})
            continue
        prime = next(iter(best))
        if prime != tuple(sdd.full_prime_partition(bits, 4)):
            failures.append({"bits": bits, "kind": "independent prime mismatch"})
        if len(prime) > 1:
            decomp += 1
        # Check every unordered cut by explicit nonzero cofactor sets as well
        # as projection cardinality; this is distinct from the archive's row code.
        sats = [a for a in range(16) if bits & (1 << a)]
        for left in (1, 3, 5, 7, 9, 11, 13):
            right = 15 ^ left
            rows = {}
            for a in sats:
                rows.setdefault(a & left, set()).add(a & right)
            compressed_accept = len({frozenset(row) for row in rows.values()}) == 1
            product_accept = sizes[15] == sizes[left] * sizes[right]
            if compressed_accept != product_accept:
                failures.append({"bits": bits, "cut": left, "kind": "criterion mismatch"})
            cut_checks += 1
        for j, (tree, encoded_tree) in enumerate(zip(trees, encoded)):
            got = extract_by_projection(sizes, encoded_tree)
            expected = ve.laminar_from_prime(prime, tree)
            if got != expected:
                failures.append({"bits": bits, "tree_index": j, "kind": "exposure mismatch"})
            exposure_pairs += 1
            if got == prime:
                aligned_counts[j] += 1
                if len(prime) > 1:
                    decomposable_aligned_counts[j] += 1
            if ve.partition_is_aligned(prime, tree):
                prime_aligned_pairs += 1
                if got != prime:
                    failures.append({"bits": bits, "tree_index": j, "kind": "prime alignment mismatch"})
    result = {"functions": 65535, "unordered_cuts_checked": cut_checks, "function_vtree_exposure_pairs": exposure_pairs,
              "independent_partition_method": "Enumerate all 15 set partitions; product of existential-projection cardinalities equals relation cardinality",
              "independent_extraction_method": "Recursive projection-cardinality product criterion, no semantic prime input",
              "decomposable_functions": decomp, "aligned_counts": aligned_counts,
              "decomposable_aligned_counts": decomposable_aligned_counts, "prime_aligned_pairs": prime_aligned_pairs,
              "failures": failures, "wall_seconds": time.perf_counter() - start}
    dump(REP / "independent_n4_audit.json", result)
    print("independent_n4", "PASS" if not failures else "FAIL", exposure_pairs, flush=True)
    if failures:
        raise RuntimeError("Independent n4 audit failed")


def run_independent_n5():
    sys.path[:0] = [str(REP / "relocated" / "phase4" / "code"), str(REP / "relocated" / "phase5" / "code")]
    bv = importlib.import_module("benchmark_vtrees")
    original_cnf_bits = bv.cnf_bits
    original_extracted = bv.extracted_from_prime
    manifest = []
    current = {}
    counter = {"comparisons": 0, "failures": 0}
    def tracked_bits(cnf, n):
        bits = original_cnf_bits(cnf, n)
        if bits:
            current.clear()
            current.update(bits=bits, sizes=projection_sizes(bits, n))
            manifest.append({"accepted_index": len(manifest), "n": n, "cnf": cnf, "truth_bits": bits})
        return bits
    def audited_extracted(full, tree):
        expected = original_extracted(full, tree)
        actual = extract_by_projection(current["sizes"], masks(tree))
        counter["comparisons"] += 1
        if actual != expected:
            counter["failures"] += 1
            raise AssertionError("Frozen n5 prime-derived exposure differs from direct projection extraction")
        return expected
    bv.cnf_bits = tracked_bits
    bv.extracted_from_prime = audited_extracted
    start = time.perf_counter()
    with (REP / "logs" / "independent_n5.stdout.txt").open("w", encoding="utf-8") as out, (REP / "logs" / "independent_n5.stderr.txt").open("w", encoding="utf-8") as err, redirect_stdout(out), redirect_stderr(err):
        bv.run(seed=20260929, n=5, per_family=180)
    for index, record in enumerate(manifest):
        record.update(family=["factorable_clean", "factorable_redundant_cross", "random_cnf"][index // 180], instance=index % 180)
    dump(REP / "frozen_n5_accepted_instance_manifest.json", {"seed": 20260929, "instances": manifest})
    comparisons = [compare_file("phase5", name) for name in ("n5_benchmark_results.json", "n5_benchmark_records.csv", "n5_benchmark_summary.csv")]
    result = {"seed": 20260929, "accepted_instances": len(manifest), "exposure_comparisons": counter["comparisons"],
              "failures": counter["failures"], "output_comparisons_after_instrumentation": comparisons,
              "wall_seconds": time.perf_counter() - start, "scope": "Exact reproduction of frozen oracle-assisted scoring, independently cross-checked against relational projections; not a scalable non-oracle benchmark"}
    dump(REP / "independent_n5_audit.json", result)
    print("independent_n5", "PASS" if not counter["failures"] and all(c["match"] for c in comparisons) else "FAIL", counter["comparisons"], flush=True)
    if counter["failures"] or not all(c["match"] for c in comparisons):
        raise RuntimeError("Independent n5 audit failed")


def run_assumptions_audit():
    sys.path[:0] = [str(REP / "relocated" / "phase4" / "code"), str(REP / "relocated" / "phase5" / "code")]
    vi = importlib.import_module("validate_incremental")
    ve = importlib.import_module("vtree_exhaustive")
    sdd = importlib.import_module("sdd_direct_extraction")
    rng = random.Random(41)
    false_trials = []
    for trial in range(120):
        n = rng.randint(2, 8)
        formula = vi.fc.random_cnf(n, rng.randint(1, max(2, 2*n)), rng.randint(1, min(4, n)), rng)
        vi.random_partition(n, rng)
        satisfiable = any(all(any(bool((a >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause) for clause in formula) for a in range(1 << n))
        if not satisfiable:
            false_trials.append(trial)
    fixed = ve.fixed_balanced4()
    crossing_bits = sum(1 << a for a in range(16) if ((a >> 0) & 1) == ((a >> 2) & 1) and ((a >> 1) & 1) == ((a >> 3) & 1))
    prime_bits = (1 << 0) | (1 << 15)
    examples = []
    for name, bits in (("crossing_product_of_equalities", crossing_bits), ("one_prime_all_equal", prime_bits)):
        examples.append({"name": name, "truth_bits": bits, "full_prime": sdd.full_prime_partition(bits, 4),
                         "direct_fixed_tree": extract_by_projection(projection_sizes(bits, 4), masks(fixed))})
    result = {"incremental_seed": 41, "incremental_trials": 120, "false_formula_trial_ids": false_trials,
              "false_formula_count": len(false_trials),
              "false_function_scope": "SAT encoding equivalence remains valid on false input, but a nonempty-relation prime-factor uniqueness theorem cannot be inferred from those trials",
              "indistinguishable_direct_partition_examples": examples,
              "prime_alignment_limit": "Alignment suffices mathematically, but direct extraction alone does not certify that its unresolved blocks are semantic primes; bypass residual SAT only with an independent certificate or a theorem-class promise",
              "local_truth_index_contract": "Phase4 row_patterns reads bits in leaves(tree) order; arbitrary vtree permutations require reindexing"}
    dump(REP / "assumptions_audit.json", result)
    print("assumptions_audit", "false_input_trials", len(false_trials), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["all", "frozen", "independent"], default="all")
    args = parser.parse_args()
    REP.mkdir(parents=True, exist_ok=True)
    if args.mode in ("all", "frozen"):
        run_frozen()
    if args.mode in ("all", "independent"):
        if not (REP / "source_relocation_manifest.json").exists():
            prepare()
        run_independent_n4()
        run_independent_n5()
        run_assumptions_audit()


if __name__ == "__main__":
    main()
