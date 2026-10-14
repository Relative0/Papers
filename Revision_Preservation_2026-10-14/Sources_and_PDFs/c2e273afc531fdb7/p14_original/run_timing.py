"""Frozen P14-PY0 fresh-process timing runner."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import gc
import hashlib
import json
import math
import os
import platform
import random
import statistics
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from p14_common import *
from run_correctness import check_freeze,natural_recipes,synthetic_recipes,sha

SESSIONS=3
WORKERS_PER_SESSION=1
WARM_BLOCKS=1
MEASURED_BLOCKS=3
TARGET_BATCH_NS=10_000_000
MAX_PREDICTED_ARM_NS=40_000_000
WALL_CAP_SECONDS=90*60


def all_recipes():
    out=[]
    for cid,family,build,meta in synthetic_recipes():out.append(("synthetic",family,cid,build))
    for cid,design,build,oracle,nvars,meta in natural_recipes():out.append(("natural",design,cid,build))
    return out


def calibrate(build,endpoint,arms=ARMS):
    timings=[]
    root=None
    if endpoint=="ir":
        fac,root,nvars=build(base.Factory)
    for arm in arms:
        t0=time.perf_counter_ns()
        if endpoint=="recipe":
            compile_recipe(build,arm)
        else:
            build_ir(root,arm)
        timings.append(time.perf_counter_ns()-t0)
    fastest=max(1,min(timings));slowest=max(timings)
    target=max(1,math.ceil(TARGET_BATCH_NS/fastest))
    cap=max(1,MAX_PREDICTED_ARM_NS//max(1,slowest))
    return min(1_000_000,target,cap),min(timings),max(timings)


def worker(session,worker):
    check_freeze()
    if not json.loads((HERE/"correctness_results.json").read_text()).get("status")=="PASS":
        raise RuntimeError("correctness gate absent")
    seed=2026091904+session*100+worker
    rng=random.Random(seed);recipes=all_recipes();rng.shuffle(recipes)
    rows=[];checks=0
    started=time.time()
    for ci,(corpus,family,cid,build) in enumerate(recipes,1):
        expected=compile_recipe(build,"D")[0]
        for arm in ARMS:
            assert compile_recipe(build,arm)[0]==expected;checks+=1
        for endpoint in ("recipe","ir"):
            base_ir=build(base.Factory) if endpoint=="ir" else None
            batch,calibration_min_ns,calibration_max_ns=calibrate(build,endpoint)
            for block in range(WARM_BLOCKS+MEASURED_BLOCKS):
                arms=list(ARMS);rng.shuffle(arms)
                for order,arm in enumerate(arms):
                    t0=time.perf_counter_ns()
                    if endpoint=="recipe":
                        for _ in range(batch):poly,choice=compile_recipe(build,arm)
                    else:
                        fac,root,nvars=base_ir
                        for _ in range(batch):poly,choice=build_ir(root,arm)
                    elapsed=time.perf_counter_ns()-t0
                    assert poly==expected;checks+=1
                    if block>=WARM_BLOCKS:
                        rows.append({"session":session,"worker":worker,"case_id":cid,"corpus":corpus,
                                     "family":family,"endpoint":endpoint,"block":block-WARM_BLOCKS,"order":order,"arm":arm,
                                     "batch":batch,"elapsed_ns":elapsed,"per_compile_ns":elapsed/batch,
                                     "selected":choice,"monomials":len(poly),"calibration_min_ns":calibration_min_ns,
                                     "calibration_max_ns":calibration_max_ns})
        if corpus=="synthetic":
            canonical_batch,canonical_min_ns,canonical_max_ns=calibrate(build,"recipe",CANONICAL_ARMS)
            for block in range(WARM_BLOCKS+MEASURED_BLOCKS):
                arms=list(CANONICAL_ARMS);rng.shuffle(arms)
                for order,arm in enumerate(arms):
                    t0=time.perf_counter_ns()
                    for _ in range(canonical_batch):poly,choice=compile_recipe(build,arm)
                    elapsed=time.perf_counter_ns()-t0
                    assert poly==expected;checks+=1
                    if block>=WARM_BLOCKS:
                        rows.append({"session":session,"worker":worker,"case_id":cid,"corpus":"canonical",
                                     "family":family,"endpoint":"recipe","block":block-WARM_BLOCKS,"order":order,"arm":arm,
                                     "batch":canonical_batch,"elapsed_ns":elapsed,"per_compile_ns":elapsed/canonical_batch,
                                     "selected":choice,"monomials":len(poly),"calibration_min_ns":canonical_min_ns,
                                     "calibration_max_ns":canonical_max_ns})
        if time.time()-started>WALL_CAP_SECONDS:
            raise RuntimeError("worker wall cap reached")
        if ci%25==0:print(f"session {session} worker {worker}: {ci}/{len(recipes)}",flush=True)
    out={"schema":"p14-py0-timing-worker/v1","session":session,"worker":worker,"seed":seed,
         "freeze_sha256":sha(HERE/"P14_FREEZE.json"),"python":sys.version,"platform":platform.platform(),
         "pid":os.getpid(),"gc_enabled":gc.isenabled(),"gc_threshold":gc.get_threshold(),
         "power":"Balanced","affinity":"uncontrolled","warm_blocks":WARM_BLOCKS,
         "measured_blocks":MEASURED_BLOCKS,"target_batch_ns":TARGET_BATCH_NS,
         "max_predicted_arm_ns":MAX_PREDICTED_ARM_NS,
         "checks":checks,"wall_seconds":time.time()-started,"rows":rows}
    path=HERE/f"timing_s{session}_w{worker}.json"
    path.write_text(json.dumps(out,separators=(",",":"))+"\n")
    print(f"PASS {path.name}: {len(rows)} rows {out['wall_seconds']:.1f}s",flush=True)


def controller():
    check_freeze();start=time.time()
    for session in range(SESSIONS):
        for worker_id in range(WORKERS_PER_SESSION):
            if time.time()-start>WALL_CAP_SECONDS:raise RuntimeError("total local wall cap reached")
            subprocess.run([sys.executable,__file__,"--session",str(session),"--worker",str(worker_id)],check=True)
    print(f"All workers complete in {time.time()-start:.1f}s")


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--session",type=int);ap.add_argument("--worker",type=int)
    args=ap.parse_args()
    worker(args.session,args.worker) if args.session is not None else controller()
