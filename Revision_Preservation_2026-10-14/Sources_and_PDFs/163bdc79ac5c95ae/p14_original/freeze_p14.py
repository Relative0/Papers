"""Create the P14-PY0 holdout and protocol freeze without timing it."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import platform
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from p14_common import (
    SYNTHETIC_FAMILIES, S_MASTER_SEED, synthetic_factors, make_trace, base,
)

EPFL_COMMIT = "0060e156826e733d69bf5b3322d1bdd0d03a1f9a"
KNOWN = {"adder", "bar", "cavlc", "int2float", "priority", "router"}
NATURAL_SUPPORT_MIN = 4
NATURAL_SUPPORT_MAX = 12
NATURAL_CONE_NODE_MAX = 128
NATURAL_PER_DESIGN = 8
LOCAL_WALL_CAP_SECONDS = 90 * 60
LOCAL_STORAGE_CAP_BYTES = 4 * 1024**3
PROCESS_MEMORY_CAP_BYTES = 1024**3
MONOMIAL_CAP = 1_000_000
COMPILE_CAP_SECONDS = 60


def sha(path):
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""):digest.update(chunk)
    return digest.hexdigest()


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def select_quantiles(rows, number):
    if len(rows) <= number: return rows
    indexes = [round(i*(len(rows)-1)/(number-1)) for i in range(number)]
    return [rows[i] for i in indexes]


def natural_manifest():
    roots = list((HERE/"epfl_snapshot").glob(f"benchmarks-{EPFL_COMMIT}/best_results/size/*.blif"))
    selected = []
    excluded = []
    sys.setrecursionlimit(100000)
    p1 = __import__("n2_p13_harness").p8.p1
    for path in sorted(roots):
        design = path.stem.split("_size_")[0]
        if design in KNOWN:
            excluded.append(design)
            continue
        blif = base.parse_blif(path)
        smemo, dmemo = {}, {}
        candidates = []
        for root in sorted(blif.nodes):
            support = p1.capped_support(blif, root, NATURAL_SUPPORT_MAX+1, smemo)
            if not NATURAL_SUPPORT_MIN <= len(support) <= NATURAL_SUPPORT_MAX: continue
            count = p1.cone_node_count(blif, root, NATURAL_CONE_NODE_MAX+1)
            if count > NATURAL_CONE_NODE_MAX: continue
            depth = p1.cone_depth(blif, root, dmemo)
            names = [name for name in blif.inputs if name in support]
            candidates.append({"root":root, "support_names":names, "support":len(names),
                               "cone_nodes":count, "depth":depth})
        candidates.sort(key=lambda x:(x["cone_nodes"],x["depth"],x["root"]))
        cases = select_quantiles(candidates, NATURAL_PER_DESIGN)
        selected.append({"design":design, "path":path.relative_to(HERE).as_posix(),
                         "sha256":sha(path), "git_blob":git_blob(path),
                         "candidate_count":len(candidates), "cases":cases})
    return {"source":"EPFL best_results/size", "commit":EPFL_COMMIT,
            "selection":"all non-P1-P13 design families; support 4-12; cone nodes <=128; eight structural quantiles",
            "known_designs_excluded":sorted(excluded), "designs":selected}


def main():
    synthetic=[]
    for fi, family in enumerate(SYNTHETIC_FAMILIES):
        for index in range(32):
            factors=synthetic_factors(index)
            seed=S_MASTER_SEED ^ (fi << 24) ^ index
            trace=make_trace(fi,index,seed,factors)
            raw=json.dumps(trace,sort_keys=True,separators=(",",":")).encode()
            synthetic.append({"case_id":f"{family}:{index:02d}","family":family,"index":index,
                              "seed":seed,"factors":factors,"trace":trace,
                              "trace_sha256":hashlib.sha256(raw).hexdigest()})
    natural=natural_manifest()
    (HERE/"synthetic_holdout.json").write_text(json.dumps({"schema":"p14-py0-synthetic/v1","master_seed":S_MASTER_SEED,"cases":synthetic},indent=2)+"\n")
    (HERE/"natural_holdout.json").write_text(json.dumps({"schema":"p14-py0-natural/v1",**natural},indent=2)+"\n")
    source_files=[HERE/"p14_common.py",HERE/"freeze_p14.py",HERE/"run_correctness.py",
                  HERE/"run_timing.py",HERE/"run_memory.py",HERE/"analyze_p14.py"]
    source_hashes={p.name:sha(p) for p in source_files}
    host={"platform":platform.platform(),"processor":platform.processor(),"logical_cpu_count":os.cpu_count(),
          "python":sys.version,"power_scheme":"Windows Balanced (read-only powercfg query)",
          "affinity":"uncontrolled; fresh sequential workers","paid_compute":False}
    freeze={"schema":"p14-py0-freeze/v1","frozen_utc":datetime.now().astimezone().isoformat(),
            "status":"FROZEN BEFORE HOLDOUT OPPORTUNITY OR TIMING INSPECTION",
            "protocol":str((HERE.parent/"P14_PREREGISTRATION_DRAFT.md").resolve()),
            "source_hashes":source_hashes,
            "manifests":{"synthetic_holdout.json":sha(HERE/"synthetic_holdout.json"),
                         "natural_holdout.json":sha(HERE/"natural_holdout.json")},
            "host":host,"compute_budget":{"local_wall_seconds":LOCAL_WALL_CAP_SECONDS,
                "storage_bytes":LOCAL_STORAGE_CAP_BYTES,"process_memory_bytes":PROCESS_MEMORY_CAP_BYTES,
                "per_compile_seconds":COMPILE_CAP_SECONDS,"monomials":MONOMIAL_CAP,
                "worker_design":"3 sessions x 1 fresh sequential worker; recipe and compiler-IR endpoints; 3 measured blocks after 1 warmup; per-case common batches target >=10ms for the fastest arm and cap the slowest predicted arm at 40ms; separate tracemalloc pass",
                "departure_from_draft":"30 workers x >=100ms x 512 cases requires at least 20.7h. The 90-minute local cap reduces workers, blocks, and minimum batch duration and adds a 40ms slow-arm cap; intervals are descriptive and close effects are inconclusive."},
            "analysis":{"bootstrap_draws":10000,"seed":2026091902,"primary":["E/F","E/D"],
                        "familywise_alpha":0.05,"simultaneous_method":"Bonferroni 98.75% two-sided bootstrap intervals over four confirmatory comparisons"},
            "natural_scope_note":f"The pinned snapshot has {len(natural['designs'])} uninspected size-optimized design families after excluding six historical families; reduced from target 16 before results."}
    (HERE/"P14_FREEZE.json").write_text(json.dumps(freeze,indent=2)+"\n")
    print(json.dumps({"synthetic_cases":len(synthetic),"natural_designs":len(natural["designs"]),
                      "natural_cases":sum(len(x["cases"]) for x in natural["designs"]),
                      "source_hashes":source_hashes,"budget":freeze["compute_budget"]},indent=2))


if __name__=="__main__":main()
