"""Freeze, execute and analyze the disclosed synthetic-only protocol v4."""
from __future__ import annotations

import argparse
import ctypes
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
RUN = HERE / 'run_v4_001'
sys.path.insert(0, str(HERE))
MODULE_LOAD_START = time.perf_counter_ns()
from primary_cell_pilot import (HELD_OUT_SEEDS, SOURCE, call_arm, make_case,
                                oracle)
MODULE_LOAD_NS = time.perf_counter_ns() - MODULE_LOAD_START


def hashed(path):
    return sha256(path.read_bytes()).hexdigest()


def json_line(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n'


def scalar_eval(expr, x0, x1):
    from cm_exprlib import And, Eqv, Imp, Not, Or, Var, Xor
    if isinstance(expr, Var):
        return (x0, x1)[expr.i]
    if isinstance(expr, Not):
        return 1 - scalar_eval(expr.a, x0, x1)
    a, b = scalar_eval(expr.a, x0, x1), scalar_eval(expr.b, x0, x1)
    if isinstance(expr, And): return a & b
    if isinstance(expr, Or): return a | b
    if isinstance(expr, Xor): return a ^ b
    if isinstance(expr, Imp): return (1-a) | b
    if isinstance(expr, Eqv): return 1-(a ^ b)
    raise TypeError(expr)


def checked_case(seed):
    from cm_token import cm_token_value
    expr, stats = make_case(seed)
    token, metrics = oracle(expr)
    for x0 in (0, 1):
        for x1 in (0, 1):
            assert scalar_eval(expr, x0, x1) == cm_token_value(token, x0, x1)
    assert metrics['root_outcome'] == 'pure_structural'
    return expr, stats, token, metrics


def prepare():
    if RUN.exists():
        raise RuntimeError('Run directory already exists; never overwrite a frozen run')
    verify_source()
    RUN.mkdir()
    corpus = []
    for case_id, seed in enumerate(HELD_OUT_SEEDS):
        expr, stats, token, metrics = checked_case(seed)
        corpus.append({'case_id': case_id, **stats,
                       'ast_repr_sha256': sha256(repr(expr).encode('utf-8')).hexdigest(),
                       'source_token': token, 'root_outcome': metrics['root_outcome'],
                       'direct_pair_retabulations': metrics['direct_pair_retabulations']})
    (RUN/'CORPUS.jsonl').write_text(''.join(json_line(x) for x in corpus), encoding='utf-8')
    configuration = {
        'schema': 'cm-pair-v4-synthetic/v1', 'case_count': 64,
        'repetitions_per_case': 30, 'target_block_ns': 100_000_000,
        'calibration_retarget_ns': 150_000_000,
        'max_inner_calls': 1000, 'case_timeout_s': 60,
        'schedule_seed_rule': '202610020099 XOR formula_seed',
        'bootstrap_seed': 202610020001, 'bootstrap_draws': 10000,
        'primary_time_ratio': 'median over formulas of median(packed repetitions)/median(CM repetitions)',
        'primary_memory_increase': 'median over formulas of CM peak working set / packed peak working set - 1',
        'time_threshold': 1.20, 'interval_lower_threshold': 1.00,
        'memory_increase_max': 0.10,
    }
    (RUN/'RUN_CONFIG.json').write_text(json.dumps(configuration, indent=2)+'\n', encoding='utf-8')
    import numpy
    env = {'platform': platform.platform(), 'processor': platform.processor(),
           'python': sys.version, 'executable': sys.executable,
           'numpy': numpy.__version__, 'logical_cpus': os.cpu_count(),
           'source_commit': '0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b',
           'source_snapshot_manifest_sha256': hashed(SOURCE.parent/'SOURCE_SNAPSHOT.json'),
           'source_file_count': 63,
           'working_directory': str(HERE),
           'time_measurement': 'perf_counter_ns, sequential fresh case processes',
           'memory_measurement': 'Windows GetProcessMemoryInfo, fresh arm processes'}
    (RUN/'ENVIRONMENT.json').write_text(json.dumps(env, indent=2)+'\n', encoding='utf-8')
    for name in ('TIMING.jsonl', 'MEMORY.jsonl', 'FAILURES.jsonl'):
        (RUN/name).write_bytes(b'')
    files = [HERE/'PROTOCOL_V4_SYNTHETIC_CONFIRMATION.md', HERE/'primary_cell_pilot.py',
             HERE/'study_v4.py', SOURCE.parent/'SOURCE_SNAPSHOT.json',
             RUN/'CORPUS.jsonl', RUN/'RUN_CONFIG.json', RUN/'ENVIRONMENT.json',
             RUN/'TIMING.jsonl', RUN/'MEMORY.jsonl', RUN/'FAILURES.jsonl']
    freeze = {'schema': 'cm-pair-v4-freeze/v1', 'status': 'FROZEN_BEFORE_HELD_OUT_TIMING',
              'source_commit': env['source_commit'],
              'files': {str(p.relative_to(HERE.parent).as_posix()): {'sha256': hashed(p), 'bytes': p.stat().st_size}
                        for p in files},
              'result_files_initially_empty': True,
              'natural_aig_scope': 'Outside v4; v3 full circuit comparison remains open'}
    (RUN/'FREEZE.json').write_text(json.dumps(freeze, indent=2)+'\n', encoding='utf-8')
    print(f"FROZEN: {len(corpus)} held-out cases in {RUN}")


def verify_freeze():
    freeze = json.loads((RUN/'FREEZE.json').read_text(encoding='utf-8'))
    for relative, identity in freeze['files'].items():
        if relative.endswith(('TIMING.jsonl', 'MEMORY.jsonl', 'FAILURES.jsonl')):
            continue
        path = HERE.parent / relative
        assert path.is_file() and hashed(path) == identity['sha256'], relative
        assert path.stat().st_size == identity['bytes'], relative
    verify_source()
    return freeze


def verify_source():
    snapshot = json.loads((SOURCE.parent/'SOURCE_SNAPSHOT.json').read_text(encoding='utf-8'))
    assert snapshot['commit'] == '0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b'
    assert len(snapshot['files']) == 63
    for name, record in snapshot['files'].items():
        path = SOURCE / name
        assert path.stat().st_size == record['bytes'] and hashed(path) == record['sha256'], name


def timed_case(seed):
    preparation_start = time.perf_counter_ns()
    expr, stats, token, metrics = checked_case(seed)
    preparation_ns = time.perf_counter_ns() - preparation_start
    for arm in ('CM', 'packed'):
        observed, _ = call_arm(expr, arm)
        assert observed == token
    initial = {arm: sum(call_arm(expr, arm)[1] for _ in range(3))/3
               for arm in ('CM', 'packed')}
    loops = {arm: min(1000, max(1, math.ceil(100_000_000/initial[arm])))
             for arm in initial}
    calibration_trials = {}
    for arm in ('CM', 'packed'):
        trial_ns = sum(call_arm(expr, arm)[1] for _ in range(loops[arm]))
        if trial_ns < 100_000_000:
            loops[arm] = min(1000, max(loops[arm]+1,
                                       math.ceil(150_000_000/(trial_ns/loops[arm]))))
            trial_ns = sum(call_arm(expr, arm)[1] for _ in range(loops[arm]))
        assert trial_ns >= 100_000_000, f'calibration shortfall {arm}: {trial_ns}'
        calibration_trials[arm] = trial_ns
    rng = random.Random(202610020099 ^ seed)
    rows = []
    for rep in range(30):
        arms = ['CM', 'packed']
        rng.shuffle(arms)
        for order, arm in enumerate(arms):
            elapsed = []
            for _ in range(loops[arm]):
                observed, ns = call_arm(expr, arm)
                assert observed == token
                elapsed.append(ns)
            rows.append({'seed': seed, 'repetition': rep, 'arm': arm,
                         'order': order, 'inner_calls': loops[arm],
                         'sum_ns': sum(elapsed), 'per_call_ns': sum(elapsed)/len(elapsed),
                         'ast_occurrences': stats['ast_occurrences'],
                         'unique_object_nodes': stats['unique_object_nodes'],
                         'root_outcome': metrics['root_outcome']})
    from bitset_backend import bitset_env_cache_stats
    from cm_normalize import cm_normalize_cache_stats
    from cm_token import cm_compose
    cache_after = {'bitset_env': bitset_env_cache_stats(),
                   'cm_compose': cm_compose.cache_info()._asdict(),
                   'cm_normalize': cm_normalize_cache_stats()}
    return {'seed': seed, 'module_load_ns': MODULE_LOAD_NS, 'preparation_ns': preparation_ns,
            'cache_after': cache_after, 'calibration_ns': initial,
            'calibration_trial_ns': calibration_trials, 'inner_calls': loops,
            'correctness': 'PASS', 'rows': rows}


class ProcessMemoryCounters(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_uint32), ('PageFaultCount', ctypes.c_uint32),
                ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]


def process_memory():
    if os.name != 'nt':
        raise RuntimeError('v4 memory endpoint requires Windows')
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    get_current_process = ctypes.windll.kernel32.GetCurrentProcess
    get_current_process.restype = ctypes.c_void_p
    get_memory_info = ctypes.windll.psapi.GetProcessMemoryInfo
    get_memory_info.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32]
    get_memory_info.restype = ctypes.c_int
    process = get_current_process()
    ok = get_memory_info(process, ctypes.byref(counters), counters.cb)
    if not ok:
        raise OSError('GetProcessMemoryInfo failed')
    return {'working_set_bytes': int(counters.WorkingSetSize),
            'peak_working_set_bytes': int(counters.PeakWorkingSetSize),
            'private_commit_bytes': int(counters.PagefileUsage),
            'peak_private_commit_bytes': int(counters.PeakPagefileUsage)}


def memory_case(seed, arm):
    expr, stats = make_case(seed)
    before = process_memory()
    observed, _ = call_arm(expr, arm)
    after = process_memory()
    return {'seed': seed, 'arm': arm, 'token': observed,
            'ast_occurrences': stats['ast_occurrences'],
            'before': before, 'after': after,
            'peak_working_set_bytes': after['peak_working_set_bytes']}


def child(mode, seed, arm=None):
    result = timed_case(seed) if mode == 'timing' else memory_case(seed, arm)
    print(json.dumps(result, separators=(',', ':')))


def append_row(path, row):
    with path.open('a', encoding='utf-8', newline='') as out:
        out.write(json_line(row))
        out.flush()
        os.fsync(out.fileno())


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def run():
    verify_freeze()
    corpus = read_rows(RUN/'CORPUS.jsonl')
    timings = read_rows(RUN/'TIMING.jsonl')
    memory = read_rows(RUN/'MEMORY.jsonl')
    counts = {case['case_id']: sum(r['case_id'] == case['case_id'] for r in timings) for case in corpus}
    done_timing = {case_id for case_id, count in counts.items() if count == 60}
    done_memory = {(r['case_id'], r['arm']) for r in memory}
    for case in corpus:
        case_id, seed = case['case_id'], case['seed']
        if case_id not in done_timing:
            if any(r['case_id'] == case_id for r in timings):
                raise RuntimeError(f'Incomplete prior case {case_id}; retain raw rows and issue a new run')
            try:
                proc = subprocess.run([sys.executable, str(HERE/'study_v4.py'), 'child', 'timing', str(seed)],
                                      capture_output=True, text=True, timeout=60, check=True,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                result = json.loads(proc.stdout)
                assert result['correctness'] == 'PASS' and len(result['rows']) == 60
                for row in result['rows']:
                    append_row(RUN/'TIMING.jsonl', {'case_id': case_id, **row,
                               'calibration_ns': result['calibration_ns'],
                               'calibration_trial_ns': result['calibration_trial_ns'],
                               'calibrated_inner_calls': result['inner_calls'],
                               'module_load_ns': result['module_load_ns'],
                               'preparation_ns': result['preparation_ns'],
                               'cache_after': result['cache_after']})
                print(f'timing {case_id+1}/64', flush=True)
            except Exception as exc:
                append_row(RUN/'FAILURES.jsonl', {'case_id': case_id, 'seed': seed,
                           'stage': 'timing', 'error': repr(exc)})
                raise
        for arm in ('CM', 'packed'):
            if (case_id, arm) in done_memory:
                continue
            try:
                proc = subprocess.run([sys.executable, str(HERE/'study_v4.py'), 'child', 'memory', str(seed), arm],
                                      capture_output=True, text=True, timeout=60, check=True,
                                      env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                result = json.loads(proc.stdout)
                assert result['token'] == case['source_token']
                append_row(RUN/'MEMORY.jsonl', {'case_id': case_id, **result})
            except Exception as exc:
                append_row(RUN/'FAILURES.jsonl', {'case_id': case_id, 'seed': seed,
                           'stage': 'memory', 'arm': arm, 'error': repr(exc)})
                raise
    print('MEASUREMENT COMPLETE: 64 cases')


def percentile(values, p):
    ordered = sorted(values)
    x = (len(ordered)-1)*p
    i = int(x)
    f = x-i
    return ordered[i]*(1-f) + ordered[min(i+1,len(ordered)-1)]*f


def analyze():
    verify_freeze()
    corpus = read_rows(RUN/'CORPUS.jsonl')
    timings = read_rows(RUN/'TIMING.jsonl')
    memory = read_rows(RUN/'MEMORY.jsonl')
    failures = read_rows(RUN/'FAILURES.jsonl')
    if failures or len(timings) != 64*30*2 or len(memory) != 64*2:
        raise RuntimeError(f'Incomplete run: {len(timings)} timing rows, {len(memory)} memory rows, {len(failures)} failures')
    by_case = {}
    formula_rows = []
    for case in corpus:
        case_id = case['case_id']
        subset = [r for r in timings if r['case_id'] == case_id]
        assert len(subset) == 60
        by_arm = {arm: sorted((r for r in subset if r['arm'] == arm), key=lambda r: r['repetition'])
                  for arm in ('CM', 'packed')}
        assert all([r['repetition'] for r in by_arm[arm]] == list(range(30)) for arm in by_arm)
        times = {arm: [r['per_call_ns'] for r in by_arm[arm]] for arm in by_arm}
        assert all(r['root_outcome'] == 'pure_structural' for r in subset)
        mem = {arm: next(r['peak_working_set_bytes'] for r in memory if r['case_id'] == case_id and r['arm'] == arm)
               for arm in ('CM', 'packed')}
        assert min(mem.values()) > 0
        row = {'case_id': case_id, 'seed': case['seed'], 'median_cm_ns': statistics.median(times['CM']),
               'median_packed_ns': statistics.median(times['packed']),
               'time_ratio_packed_over_cm': statistics.median(times['packed'])/statistics.median(times['CM']),
               'peak_cm_bytes': mem['CM'], 'peak_packed_bytes': mem['packed'],
               'peak_memory_increase': mem['CM']/mem['packed']-1}
        formula_rows.append(row)
        by_case[case_id] = times
    estimate = statistics.median(r['time_ratio_packed_over_cm'] for r in formula_rows)
    memory_increase = statistics.median(r['peak_memory_increase'] for r in formula_rows)
    rng = random.Random(202610020001)
    draws = []
    for _ in range(10000):
        ratios = []
        for _ in range(64):
            case_id = rng.randrange(64)
            indices = [rng.randrange(30) for _ in range(30)]
            pair = by_case[case_id]
            cm = statistics.median(pair['CM'][j] for j in indices)
            packed = statistics.median(pair['packed'][j] for j in indices)
            ratios.append(packed/cm)
        draws.append(statistics.median(ratios))
    interval = [percentile(draws, .025), percentile(draws, .975)]
    success = estimate >= 1.20 and interval[0] > 1.0 and memory_increase <= .10
    outcome = {'status': 'PASS_COMPLETED', 'scope': 'Synthetic-only protocol v4 primary cell',
               'source_commit': '0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b',
               'cases': len(corpus), 'repetitions_per_case': 30, 'correctness_disagreements': 0,
               'median_time_ratio_packed_over_cm': estimate,
               'hierarchical_bootstrap_95_interval': interval,
               'median_peak_memory_increase': memory_increase,
               'primary_success': success, 'formula_rows': formula_rows,
               'timing_rows_sha256': hashed(RUN/'TIMING.jsonl'),
               'memory_rows_sha256': hashed(RUN/'MEMORY.jsonl'),
               'failures_rows_sha256': hashed(RUN/'FAILURES.jsonl'),
               'bootstrap_seed': 202610020001, 'bootstrap_draws': 10000,
               'limitations': ['Synthetic signed/permuted N=U=1023 cell only',
                               'Post-import cache-reset timing; import/startup excluded',
                               'Natural corpus and ABC circuit gate not tested']}
    (RUN/'ANALYSIS.json').write_text(json.dumps(outcome, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in outcome.items() if k not in ('formula_rows', 'limitations')}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'child', 'run', 'analyze'))
    parser.add_argument('mode', nargs='?')
    parser.add_argument('seed', nargs='?', type=int)
    parser.add_argument('arm', nargs='?')
    args = parser.parse_args()
    if args.action == 'prepare': prepare()
    elif args.action == 'child': child(args.mode, args.seed, args.arm)
    elif args.action == 'run': run()
    else: analyze()


if __name__ == '__main__':
    main()
