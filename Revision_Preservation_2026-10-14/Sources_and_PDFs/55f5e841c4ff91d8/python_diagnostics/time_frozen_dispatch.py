"""Post-hoc timing of the frozen exact-dispatch prototype. Not a P14 trial."""
from pathlib import Path
from collections import defaultdict
import argparse
import gc
import hashlib
import json
import math
import platform
import random
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dispatch_diagnostics import h, base, GATE, TupleBoundFactory
from stats_free_diagnostic import make_backend
p6 = h.p8.p6
cb, cp3, cp6 = make_backend(base, p6.p3, p6)
SEED = 20260918 ^ 0xFD14
ARMS = ('direct', 'p13', 'tuple_bounds')


def build_once(build, arm):
    cls = {'direct':base.Factory, 'p13':h.DeferredPairTelemetryFactory,
           'tuple_bounds':TupleBoundFactory}[arm]
    f, root, nv = build(cls)
    annotate = f.dispatch(GATE)[0] if arm == 'p13' else f.dispatch_bool() if arm == 'tuple_bounds' else False
    return f, root, nv, annotate


def pipeline_once(build, arm):
    f, root, nv, annotate = build_once(build, arm)
    if annotate:
        rr, inf = p6.build_innode(root)
        poly = cp6.lower_p6(rr, inf, collect_stats=False)[0]
    else:
        poly = cb.lower_anf(root)[0]
    return poly


def worker(wi, rounds, batch):
    rng = random.Random(SEED+wi)
    gp = [('gatep', cid, build) for cid, depth, idx, build in h.p8.gatep_eval_recipes()]
    natural = [('natural', cid, build) for cid, circuit, depth, build, oracle, extra in h.p8.natural_eval_recipes()[0]]
    recipes = gp+natural
    rng.shuffle(recipes)
    rows = []
    checks = 0
    for split, cid, build in recipes:
        f, root, nv, _ = build_once(build, 'direct')
        expected = base.lower_anf(root)[0] if split == 'gatep' else None
        choice = build_once(build,'p13')[3]
        assert choice == build_once(build,'tuple_bounds')[3]
        endpoints = ['build_dispatch', 'clean_pipeline'] if split == 'gatep' else ['build_dispatch']
        for endpoint in endpoints:
            fn = build_once if endpoint == 'build_dispatch' else pipeline_once
            for arm in ARMS:
                for _ in range(2):
                    result = fn(build, arm)
                    if endpoint == 'clean_pipeline':
                        assert result == expected
                        checks += 1
            for block in range(rounds):
                arms = list(ARMS)
                rng.shuffle(arms)
                for order, arm in enumerate(arms):
                    t0 = time.perf_counter_ns()
                    for _ in range(batch):
                        result = fn(build, arm)
                    elapsed = time.perf_counter_ns()-t0
                    if endpoint == 'clean_pipeline':
                        assert result == expected
                        checks += 1
                    rows.append(dict(worker=wi, block=block, order=order, split=split,
                                     case_id=cid, endpoint=endpoint, arm=arm, batch=batch,
                                     elapsed_ns=elapsed, per_call_ns=elapsed/batch))
    out = dict(label='Exploratory combined exact-dispatch prototype; not preregistered or holdout evidence',
               worker=wi, seed=SEED+wi, python=sys.version, platform=platform.platform(),
               rounds=rounds,batch=batch, gc_enabled=gc.isenabled(),gc_threshold=gc.get_threshold(),
               affinity='uncontrolled', power_mode='uncontrolled',
               clock=vars(time.get_clock_info('perf_counter')),
               script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               prototype_sha256=hashlib.sha256((HERE/'dispatch_diagnostics.py').read_bytes()).hexdigest(),
               stats_free_script_sha256=hashlib.sha256((HERE.parent/'stats_free_diagnostic.py').read_bytes()).hexdigest(),
               equality_checks=checks, rows=rows)
    (HERE/f'timing_worker_{wi}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(f'worker {wi} PASS {checks} ANF equality checks, {len(rows)} timed blocks',flush=True)


def summarize(workers):
    rows = []
    for i in range(workers):
        rows.extend(json.loads((HERE/f'timing_worker_{i}.json').read_text())['rows'])
    out = {}
    for split, endpoint in [('gatep','build_dispatch'),('gatep','clean_pipeline'),('natural','build_dispatch')]:
        sub = [r for r in rows if r['split']==split and r['endpoint']==endpoint]
        groups = defaultdict(list)
        for r in sub:
            groups[(r['case_id'],r['arm'])].append(r['per_call_ns'])
        med = {k:statistics.median(v) for k,v in groups.items()}
        cases = sorted({r['case_id'] for r in sub})
        for a,b in [('tuple_bounds','p13'),('tuple_bounds','direct'),('p13','direct')]:
            rr = [med[(c,a)]/med[(c,b)] for c in cases]
            wg = []
            for wi in range(workers):
                wgroups = defaultdict(list)
                for r in sub:
                    if r['worker']==wi:
                        wgroups[(r['case_id'],r['arm'])].append(r['per_call_ns'])
                wm = {k:statistics.median(v) for k,v in wgroups.items()}
                wg.append(math.exp(statistics.mean(math.log(wm[(c,a)]/wm[(c,b)]) for c in cases)))
            out[f'{split}/{endpoint}/{a}/{b}'] = dict(cases=len(cases),
                geomean=math.exp(statistics.mean(map(math.log,rr))),
                aggregate=sum(med[(c,a)] for c in cases)/sum(med[(c,b)] for c in cases),
                median=statistics.median(rr), wins=sum(r<1 for r in rr), worker_geomeans=wg)
    result = dict(exploratory=True, workers=workers, rows=len(rows), comparisons=out,
                  limitations='Uncontrolled affinity and power; known cases; combined prototype changes; P13 emits counters but candidate returns boolean only. Fresh processes run sequentially.')
    (HERE/'timing_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--worker',type=int)
    ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('--rounds',type=int,default=5)
    ap.add_argument('--batch',type=int,default=10)
    a=ap.parse_args()
    if a.worker is not None:
        worker(a.worker,a.rounds,a.batch)
    else:
        for i in range(a.workers):
            subprocess.run([sys.executable,__file__,'--worker',str(i),'--rounds',str(a.rounds),'--batch',str(a.batch)],check=True)
        summarize(a.workers)
