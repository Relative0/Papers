"""Freeze, run, and descriptively analyze selected natural-circuit secondary timing."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
NATURAL = HERE.parent / '04_NATURAL_CIRCUIT_EXTENSION_20260926'
RUN = HERE / 'run_natural_timing_001'
sys.path.insert(0, str(NATURAL))
MODULE_LOAD_START = time.perf_counter_ns()
from aiger_check import truth_bits
from build_manifest import inventory as natural_inventory
from natural_correctness import verify_freeze as verify_natural_correctness_freeze
from prepare_natural_admission import CM_SOURCE, SOURCE, ast_stats, parse, translated
from validate_abc_aig import digest
from bitset_backend import (bitset_env_cache_stats, build_bitset_env,
                            clear_bitset_env_cache, eval_cm_node_bitset, eval_expr_bitset)
from cm_build_pair import compile_expr_to_cm_pair_token
from cm_ir import clear_cm_ir_persistent_cache, compile_expr_to_cm_ir
from cm_normalize import clear_cm_normalize_caches, cm_normalize_cache_stats
from cm_token import cm_compose, cm_token_value
MODULE_LOAD_NS = time.perf_counter_ns() - MODULE_LOAD_START

CASES = [json.loads(line) for line in (NATURAL / 'NATURAL_CASES.jsonl').read_text(encoding='utf-8').splitlines()]
DESIGNS = {row['design']: row for row in json.loads((NATURAL / 'NATURAL_ADMISSION.json').read_text(encoding='utf-8'))['designs']}
CORRECTNESS = [json.loads(line) for line in (NATURAL / 'run_natural_correctness_001' / 'CORRECTNESS.jsonl').read_text(encoding='utf-8').splitlines()]
ARMS = ('CM_hybrid_fallback', 'direct_packed')
RESULTS = ('TIMING.jsonl', 'MEMORY.jsonl', 'ABC.jsonl', 'FAILURES.jsonl')
TIME_RE = re.compile(r'elapse: ([0-9]+(?:\.[0-9]+)?) seconds, total: ([0-9]+(?:\.[0-9]+)?) seconds')


def identity(path: Path):
    blob = path.read_bytes()
    return {'sha256': sha256(blob).hexdigest(), 'bytes': len(blob)}


def json_line(row):
    return json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n'


def read_rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def append_row(path: Path, row):
    with path.open('a', encoding='utf-8', newline='') as stream:
        stream.write(json_line(row))
        stream.flush()
        os.fsync(stream.fileno())


def capture_environment():
    import numpy
    import psutil
    process = psutil.Process()
    power = subprocess.run(['powercfg', '/GETACTIVESCHEME'], capture_output=True,
                           text=True, errors='replace', timeout=15)
    abc = subprocess.run([str(NATURAL / 'abc_tool' / 'yosys-abc.exe'), '-c', 'version'],
                         cwd=NATURAL, capture_output=True, text=True, timeout=15, check=True)
    return {'platform': platform.platform(), 'processor': platform.processor(),
            'python': sys.version, 'python_executable': sys.executable,
            'numpy': numpy.__version__, 'psutil': psutil.__version__,
            'logical_cpus': os.cpu_count(), 'physical_cpus': psutil.cpu_count(logical=False),
            'ram_bytes': psutil.virtual_memory().total,
            'process_affinity': process.cpu_affinity(), 'process_priority': process.nice(),
            'power_scheme_exit': power.returncode, 'power_scheme_stdout': power.stdout.strip(),
            'power_scheme_stderr': power.stderr.strip(),
            'abc_version': abc.stdout.strip().splitlines()[-1],
            'abc_sha256': identity(NATURAL / 'abc_tool' / 'yosys-abc.exe')['sha256'],
            'source_snapshot_sha256': identity(CM_SOURCE.parent / 'SOURCE_SNAPSHOT.json')['sha256'],
            'natural_manifest_sha256': identity(NATURAL / 'NATURAL_EXTENSION_MANIFEST_SHA256.json')['sha256'],
            'timing_clock': 'time.perf_counter_ns',
            'case_process_policy': 'fresh Python process per case/stage; sequential'}


def check_natural_inputs():
    if len(CASES) != 71 or len(CORRECTNESS) != 71:
        raise ValueError('natural case count changed')
    recorded = json.loads((NATURAL / 'NATURAL_EXTENSION_MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    if natural_inventory() != recorded['files']:
        raise ValueError('natural extension manifest mismatch')
    verify_natural_correctness_freeze()
    summary = json.loads((NATURAL / 'run_natural_correctness_001' / 'SUMMARY.json').read_text(encoding='utf-8'))
    if summary['status'] != 'PASS' or summary['passed'] != 71:
        raise ValueError('natural correctness gate not passed')
    if any(row['status'] != 'PASS' for row in CORRECTNESS):
        raise ValueError('natural correctness failure')


def prepare():
    if RUN.exists():
        raise RuntimeError('run directory already exists; use a new run identifier')
    check_natural_inputs()
    RUN.mkdir()
    (RUN / 'abc_tmp').mkdir()
    config = {'schema': 'cm-natural-secondary-v5/v1', 'case_count': 71,
              'python_arms': list(ARMS), 'abc_arm': 'fresh_subprocess_read_strash_dc2_write',
              'repetitions_per_case': 15, 'target_block_ns': 100_000_000,
              'retarget_block_ns': 150_000_000, 'max_inner_calls': 100_000,
              'case_process_timeout_s': 60,
              'schedule_seed_rule': '202610050000 XOR case_index',
              'output': 'full packed truth bitset in frozen support order',
              'analysis': 'descriptive case medians, stratified by frozen hybrid root outcome; no hypothesis test'}
    (RUN / 'RUN_CONFIG.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    environment = capture_environment()
    (RUN / 'ENVIRONMENT.json').write_text(json.dumps(environment, indent=2) + '\n', encoding='utf-8')
    for name in RESULTS:
        (RUN / name).write_bytes(b'')
    static = [HERE / 'PROTOCOL_V5_NATURAL_SECONDARY.md', Path(__file__).resolve(),
              NATURAL / 'NATURAL_EXTENSION_MANIFEST_SHA256.json',
              NATURAL / 'run_natural_correctness_001' / 'SUMMARY.json',
              NATURAL / 'run_natural_correctness_001' / 'CORRECTNESS.jsonl',
              CM_SOURCE.parent / 'SOURCE_SNAPSHOT.json',
              RUN / 'RUN_CONFIG.json', RUN / 'ENVIRONMENT.json']
    freeze = {'schema': 'cm-natural-secondary-v5-freeze/v1',
              'status': 'FROZEN_BEFORE_NATURAL_TIMING',
              'files': {path.relative_to(HERE.parent).as_posix(): identity(path) for path in static},
              'result_files_initially_empty': {name: identity(RUN / name) for name in RESULTS},
              'abc_tmp_initially_empty': True,
              'primary_v4_result': 'FAILED; cannot be replaced by this secondary study'}
    (RUN / 'FREEZE.json').write_text(json.dumps(freeze, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': freeze['status'], 'cases': len(CASES),
                      'result_files_initially_empty': True}))


def verify_run_freeze():
    freeze = json.loads((RUN / 'FREEZE.json').read_text(encoding='utf-8'))
    if freeze['status'] != 'FROZEN_BEFORE_NATURAL_TIMING':
        raise ValueError('run not frozen')
    for relative, expected in freeze['files'].items():
        if identity(HERE.parent / relative) != expected:
            raise ValueError(f'frozen file changed: {relative}')
    check_natural_inputs()
    for name in RESULTS:
        if not (RUN / name).exists():
            raise ValueError(f'missing result file: {name}')
    return freeze


def make_case(index: int):
    case = CASES[index]
    descriptor = DESIGNS[case['design']]
    _, _, nodes = parse(SOURCE / descriptor['relative_path'])
    expr = translated(case['output'], tuple(case['support']), nodes)
    if ast_stats(expr)['translated_ast_sha256'] != case['translated_ast_sha256']:
        raise ValueError('translated AST differs from frozen case')
    return case, expr


def token_bits(compiled, support_count: int):
    row = int(compiled.row_variable[1:])
    column = int(compiled.column_variable[1:])
    return sum(cm_token_value(compiled.token, (assignment >> row) & 1,
                              (assignment >> column) & 1) << assignment
               for assignment in range(1 << support_count))


def call_python_arm(expr, support_count: int, arm: str):
    order = [f'x{j}' for j in reversed(range(support_count))]
    clear_bitset_env_cache()
    if arm == 'CM_hybrid_fallback':
        cm_compose.cache_clear()
        clear_cm_normalize_caches()
        clear_cm_ir_persistent_cache()
        start = time.perf_counter_ns()
        compiled, metrics = compile_expr_to_cm_pair_token(
            expr, ['x0'], [f'x{j}' for j in range(1, support_count)], {}, strategy='hybrid')
        if compiled is None:
            bits = eval_cm_node_bitset(compile_expr_to_cm_ir(expr), order)
        else:
            bits = token_bits(compiled, support_count)
        elapsed = time.perf_counter_ns() - start
        return bits, elapsed, metrics['root_outcome']
    if arm == 'direct_packed':
        start = time.perf_counter_ns()
        bits = eval_expr_bitset(expr, build_bitset_env(order))
        elapsed = time.perf_counter_ns() - start
        return bits, elapsed, 'direct_packed'
    raise ValueError(arm)


def checked_python_call(expr, case, arm: str, expected_outcome: str):
    bits, elapsed, outcome = call_python_arm(expr, len(case['support']), arm)
    if digest(bits, len(case['support'])) != case['source_truth_sha256']:
        raise ValueError(f'{arm} truth disagreement')
    if arm == 'CM_hybrid_fallback' and outcome != expected_outcome:
        raise ValueError(f'CM outcome changed from {expected_outcome} to {outcome}')
    return elapsed, outcome


def calibrated_calls(expr, case, arm: str, expected_outcome: str):
    samples = [checked_python_call(expr, case, arm, expected_outcome)[0] for _ in range(3)]
    estimate = max(1, sum(samples) / len(samples))
    loops = min(100_000, max(1, math.ceil(100_000_000 / estimate)))
    trial = sum(checked_python_call(expr, case, arm, expected_outcome)[0] for _ in range(loops))
    first_trial = trial
    if trial < 100_000_000:
        loops = min(100_000, max(loops + 1, math.ceil(150_000_000 / max(1, trial / loops))))
        trial = sum(checked_python_call(expr, case, arm, expected_outcome)[0] for _ in range(loops))
    if trial < 100_000_000:
        raise ValueError(f'calibration shortfall for {arm}: {trial} ns at {loops} calls')
    return loops, {'three_call_mean_ns': estimate, 'first_trial_ns': first_trial,
                   'final_trial_ns': trial}


def timed_case(index: int):
    prepared_start = time.perf_counter_ns()
    case, expr = make_case(index)
    preparation_ns = time.perf_counter_ns() - prepared_start
    expected = CORRECTNESS[index]['strategies']['hybrid']['root_outcome']
    for arm in ARMS:
        checked_python_call(expr, case, arm, expected)  # untimed warm-up
    calibration = {}
    loops = {}
    for arm in ARMS:
        loops[arm], calibration[arm] = calibrated_calls(expr, case, arm, expected)
    schedule = random.Random(202610050000 ^ index)
    rows = []
    for repetition in range(15):
        order = list(ARMS)
        schedule.shuffle(order)
        for position, arm in enumerate(order):
            calls = [checked_python_call(expr, case, arm, expected)[0]
                     for _ in range(loops[arm])]
            rows.append({'case_index': index, 'design': case['design'],
                         'source_output': case['output'], 'repetition': repetition,
                         'arm': arm, 'order': position, 'inner_calls': loops[arm],
                         'sum_ns': sum(calls), 'per_call_ns': sum(calls) / len(calls),
                         'root_outcome': expected,
                         'support_count': len(case['support']),
                         'ast_occurrences': case['ast_occurrences'],
                         'unique_object_nodes': case['ast_unique_object_nodes']})
    cache_after = {'bitset_env': bitset_env_cache_stats(),
                   'cm_compose': cm_compose.cache_info()._asdict(),
                   'cm_normalize': cm_normalize_cache_stats()}
    return {'case_index': index, 'module_load_ns': MODULE_LOAD_NS,
            'preparation_ns': preparation_ns, 'calibration': calibration,
            'loops': loops, 'cache_after': cache_after, 'rows': rows}


class ProcessMemoryCounters(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_uint32), ('PageFaultCount', ctypes.c_uint32),
                ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]


def process_memory():
    if os.name != 'nt':
        raise RuntimeError('process memory endpoint requires Windows')
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    get_process = ctypes.windll.kernel32.GetCurrentProcess
    get_process.restype = ctypes.c_void_p
    get_info = ctypes.windll.psapi.GetProcessMemoryInfo
    get_info.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32]
    get_info.restype = ctypes.c_int
    if not get_info(get_process(), ctypes.byref(counters), counters.cb):
        raise OSError('GetProcessMemoryInfo failed')
    return {'working_set_bytes': int(counters.WorkingSetSize),
            'peak_working_set_bytes': int(counters.PeakWorkingSetSize),
            'private_commit_bytes': int(counters.PagefileUsage),
            'peak_private_commit_bytes': int(counters.PeakPagefileUsage)}


def memory_case(index: int, arm: str):
    case, expr = make_case(index)
    before = process_memory()
    bits, _, outcome = call_python_arm(expr, len(case['support']), arm)
    after = process_memory()
    if digest(bits, len(case['support'])) != case['source_truth_sha256']:
        raise ValueError('memory arm truth disagreement')
    return {'case_index': index, 'design': case['design'], 'source_output': case['output'],
            'arm': arm, 'root_outcome': outcome, 'before': before, 'after': after,
            'peak_working_set_bytes': after['peak_working_set_bytes'],
            'peak_private_commit_bytes': after['peak_private_commit_bytes']}


def one_abc_call(index: int, repetition: int | str):
    case = CASES[index]
    name = f'{index:04d}_{case["design"]}'
    cone = f'../04_NATURAL_CIRCUIT_EXTENSION_20260926/cones/{name}.blif'
    output = f'run_natural_timing_001/abc_tmp/{name}_{repetition}.aig'
    destination = HERE / output
    if destination.exists():
        raise RuntimeError(f'ABC temporary output already exists: {destination}')
    command = f'read_blif {cone}; time; strash; time; dc2; time; write_aiger {output}; time'
    start = time.perf_counter_ns()
    proc = subprocess.run([str(NATURAL / 'abc_tool' / 'yosys-abc.exe'), '-c', command],
                          cwd=HERE, capture_output=True, text=True, timeout=60)
    process_wall_ns = time.perf_counter_ns() - start
    if proc.returncode or not destination.exists():
        raise RuntimeError(f'ABC failed: exit {proc.returncode}; {proc.stderr[-1000:]}')
    stage_seconds = [float(match[0]) for match in TIME_RE.findall(proc.stdout)]
    if len(stage_seconds) != 4:
        raise ValueError(f'expected four ABC time diagnostics: {proc.stdout[-1000:]}')
    query_start = time.perf_counter_ns()
    bits, shape = truth_bits(destination, tuple(case['support']))
    query_ns = time.perf_counter_ns() - query_start
    if digest(bits, len(case['support'])) != case['source_truth_sha256']:
        raise ValueError('ABC AIG truth disagreement')
    row = {'case_index': index, 'design': case['design'], 'source_output': case['output'],
           'repetition': repetition, 'abc_process_wall_ns': process_wall_ns,
           'abc_stage_seconds_rounded': dict(zip(('read_blif', 'strash', 'dc2', 'write_aiger'),
                                                 stage_seconds)),
           'python_aiger_exhaustive_query_ns': query_ns,
           'aig_bytes': destination.stat().st_size, 'aig_and_gates': shape['and_gates'],
           'abc_return_code': proc.returncode, 'abc_stderr': proc.stderr,
           'truth_sha256': case['source_truth_sha256']}
    destination.unlink()
    return row


def abc_case(index: int):
    one_abc_call(index, 'warmup')
    rows = []
    for repetition in range(15):
        rows.append(one_abc_call(index, repetition))
    return {'case_index': index, 'rows': rows}


def child(mode: str, index: int, arm: str | None):
    if mode == 'timing':
        result = timed_case(index)
    elif mode == 'memory':
        if arm not in ARMS:
            raise ValueError('memory arm missing')
        result = memory_case(index, arm)
    elif mode == 'abc':
        result = abc_case(index)
    else:
        raise ValueError(mode)
    print(json.dumps(result, separators=(',', ':')))


def run_stage(index: int, mode: str, arm: str | None = None):
    command = [sys.executable, str(Path(__file__).resolve()), 'child', mode, str(index)]
    if arm is not None:
        command.append(arm)
    proc = subprocess.run(command, cwd=HERE, capture_output=True, text=True,
                          timeout=60, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    if proc.returncode:
        raise RuntimeError(f'{mode} exit {proc.returncode}: {proc.stderr[-1500:]}')
    return json.loads(proc.stdout)


def run():
    verify_run_freeze()
    timing = read_rows(RUN / 'TIMING.jsonl')
    memory = read_rows(RUN / 'MEMORY.jsonl')
    abc = read_rows(RUN / 'ABC.jsonl')
    failures = read_rows(RUN / 'FAILURES.jsonl')
    for index in range(len(CASES)):
        case_failures = {(row['stage'], row.get('arm')) for row in failures
                         if row['case_index'] == index}
        count = sum(row['case_index'] == index for row in timing)
        if count not in (0, 30):
            raise RuntimeError(f'incomplete prior timing case {index}; retain raw rows and issue new run')
        if count == 0 and ('timing', None) not in case_failures:
            try:
                result = run_stage(index, 'timing')
                if len(result['rows']) != 30:
                    raise ValueError('incomplete case timing result')
                for row in result['rows']:
                    append_row(RUN / 'TIMING.jsonl', {**row,
                               'module_load_ns': result['module_load_ns'],
                               'preparation_ns': result['preparation_ns'],
                               'calibration': result['calibration'],
                               'cache_after': result['cache_after']})
                print(f'timing {index + 1}/71 PASS', flush=True)
            except Exception as error:
                append_row(RUN / 'FAILURES.jsonl', {'case_index': index, 'stage': 'timing',
                           'error': f'{type(error).__name__}: {error}'})
                print(f'timing {index + 1}/71 FAIL', flush=True)
        for arm in ARMS:
            if any(row['case_index'] == index and row['arm'] == arm for row in memory):
                continue
            if ('memory', arm) in case_failures:
                continue
            try:
                row = run_stage(index, 'memory', arm)
                append_row(RUN / 'MEMORY.jsonl', row)
            except Exception as error:
                append_row(RUN / 'FAILURES.jsonl', {'case_index': index, 'stage': 'memory',
                           'arm': arm, 'error': f'{type(error).__name__}: {error}'})
        abc_count = sum(row['case_index'] == index for row in abc)
        if abc_count not in (0, 15):
            raise RuntimeError(f'incomplete prior ABC case {index}; retain raw rows and issue new run')
        if abc_count == 0 and ('abc', None) not in case_failures:
            try:
                result = run_stage(index, 'abc')
                if len(result['rows']) != 15:
                    raise ValueError('incomplete case ABC result')
                for row in result['rows']:
                    append_row(RUN / 'ABC.jsonl', row)
                print(f'ABC {index + 1}/71 PASS', flush=True)
            except Exception as error:
                append_row(RUN / 'FAILURES.jsonl', {'case_index': index, 'stage': 'abc',
                           'error': f'{type(error).__name__}: {error}'})
                print(f'ABC {index + 1}/71 FAIL', flush=True)
    (RUN / 'ENVIRONMENT_POSTRUN.json').write_text(
        json.dumps(capture_environment(), indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'RUN_COMPLETE_WITH_RETAINED_FAILURES',
                      'timing_rows': len(read_rows(RUN / 'TIMING.jsonl')),
                      'memory_rows': len(read_rows(RUN / 'MEMORY.jsonl')),
                      'abc_rows': len(read_rows(RUN / 'ABC.jsonl')),
                      'failures': len(read_rows(RUN / 'FAILURES.jsonl'))}))


def analyze():
    verify_run_freeze()
    timing = read_rows(RUN / 'TIMING.jsonl')
    memory = read_rows(RUN / 'MEMORY.jsonl')
    abc = read_rows(RUN / 'ABC.jsonl')
    failures = read_rows(RUN / 'FAILURES.jsonl')
    by_timing, by_memory, by_abc = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in timing:
        by_timing[row['case_index']].append(row)
    for row in memory:
        by_memory[row['case_index']].append(row)
    for row in abc:
        by_abc[row['case_index']].append(row)
    cases = []
    for index, case in enumerate(CASES):
        rows = by_timing[index]
        python_times = {}
        for arm in ARMS:
            selected = sorted((row for row in rows if row['arm'] == arm),
                              key=lambda row: row['repetition'])
            if len(selected) == 15 and [row['repetition'] for row in selected] == list(range(15)):
                python_times[arm] = statistics.median(row['per_call_ns'] for row in selected)
        memories = {row['arm']: row['peak_working_set_bytes'] for row in by_memory[index]}
        abc_rows = sorted(by_abc[index], key=lambda row: row['repetition'])
        abc_complete = (len(abc_rows) == 15 and
                        [row['repetition'] for row in abc_rows] == list(range(15)))
        outcome = CORRECTNESS[index]['strategies']['hybrid']['root_outcome']
        record = {'case_index': index, 'design': case['design'], 'output': case['output'],
                  'support_count': len(case['support']), 'root_outcome': outcome,
                  'python_repetitions': {arm: sum(row['arm'] == arm for row in rows) for arm in ARMS},
                  'memory_arms': sorted(memories), 'abc_repetitions': len(abc_rows)}
        if len(python_times) == 2:
            record['median_python_producer_ns'] = python_times
            record['ratio_direct_over_cm'] = (
                python_times['direct_packed'] / python_times['CM_hybrid_fallback'])
        if len(memories) == 2:
            record['peak_working_set_bytes'] = memories
            record['cm_peak_memory_increase'] = (
                memories['CM_hybrid_fallback'] / memories['direct_packed'] - 1)
        if abc_complete:
            record['median_abc_process_wall_ns'] = statistics.median(
                row['abc_process_wall_ns'] for row in abc_rows)
            record['median_python_aiger_query_ns'] = statistics.median(
                row['python_aiger_exhaustive_query_ns'] for row in abc_rows)
            record['median_abc_stage_seconds_rounded'] = {
                stage: statistics.median(row['abc_stage_seconds_rounded'][stage] for row in abc_rows)
                for stage in ('read_blif', 'strash', 'dc2', 'write_aiger')}
        cases.append(record)
    complete_python = [row for row in cases if 'ratio_direct_over_cm' in row]
    complete_memory = [row for row in cases if 'cm_peak_memory_increase' in row]
    complete_abc = [row for row in cases if 'median_abc_process_wall_ns' in row]
    strata = {}
    for outcome in ('pure_structural', 'full_retabulation', 'ordinary_fallback'):
        subset = [row for row in complete_python if row['root_outcome'] == outcome]
        strata[outcome] = {'cases': len(subset),
                           'median_direct_over_cm': statistics.median(
                               row['ratio_direct_over_cm'] for row in subset) if subset else None,
                           'median_cm_producer_ns': statistics.median(
                               row['median_python_producer_ns']['CM_hybrid_fallback']
                               for row in subset) if subset else None,
                           'median_direct_producer_ns': statistics.median(
                               row['median_python_producer_ns']['direct_packed']
                               for row in subset) if subset else None}
    design_rows = {}
    for design in sorted({case['design'] for case in CASES}):
        subset = [row for row in complete_python if row['design'] == design]
        design_rows[design] = {'cases': len(subset),
                               'median_direct_over_cm': statistics.median(
                                   row['ratio_direct_over_cm'] for row in subset) if subset else None}
    pre = json.loads((RUN / 'ENVIRONMENT.json').read_text(encoding='utf-8'))
    post = json.loads((RUN / 'ENVIRONMENT_POSTRUN.json').read_text(encoding='utf-8'))
    stable_keys = ('process_affinity', 'process_priority', 'power_scheme_exit', 'power_scheme_stdout')
    environment_stable = all(pre[key] == post[key] for key in stable_keys)
    complete = (not failures and len(timing) == 71 * 15 * 2 and
                len(memory) == 71 * 2 and len(abc) == 71 * 15 and
                len(complete_python) == len(complete_memory) == len(complete_abc) == 71)
    result = {'status': 'COMPLETE_DESCRIPTIVE_SECONDARY' if complete else 'INCOMPLETE_WITH_FAILURES',
              'primary_v4_result': 'FAILED; unchanged',
              'counts': {'admitted_cases': 71, 'python_timing_rows': len(timing),
                         'python_complete_cases': len(complete_python),
                         'memory_rows': len(memory), 'memory_complete_cases': len(complete_memory),
                         'abc_rows': len(abc), 'abc_complete_cases': len(complete_abc),
                         'failure_rows': len(failures)},
              'all_complete_case_median_direct_over_cm': statistics.median(
                  row['ratio_direct_over_cm'] for row in complete_python) if complete_python else None,
              'all_complete_case_median_cm_peak_memory_increase': statistics.median(
                  row['cm_peak_memory_increase'] for row in complete_memory) if complete_memory else None,
              'all_complete_case_median_abc_process_wall_ns': statistics.median(
                  row['median_abc_process_wall_ns'] for row in complete_abc) if complete_abc else None,
              'all_complete_case_median_python_aiger_query_ns': statistics.median(
                  row['median_python_aiger_query_ns'] for row in complete_abc) if complete_abc else None,
              'strata': strata, 'designs': design_rows,
              'environment_stable_before_after': environment_stable,
              'raw_sha256': {name: identity(RUN / name)['sha256'] for name in RESULTS},
              'cases': cases,
              'limits': ['Descriptive secondary cohort; cases cluster within nine designs and overlap P1-P14 families.',
                         'ABC process wall includes startup and serialization and is not a matched producer ratio.',
                         'ABC stage time diagnostics are rounded to 0.01 seconds.',
                         'Python AIGER exhaustive simulation is not native ABC query latency.',
                         'ABC process peak memory, ROBDD, prepared reuse, dense output and independent families remain unmeasured.']}
    (RUN / 'ANALYSIS.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'counts': result['counts'],
                      'median_direct_over_cm': result['all_complete_case_median_direct_over_cm'],
                      'strata': result['strata'],
                      'environment_stable': environment_stable}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'run', 'analyze', 'child'))
    parser.add_argument('mode', nargs='?')
    parser.add_argument('index', nargs='?', type=int)
    parser.add_argument('arm', nargs='?')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare()
    elif args.command == 'run':
        run()
    elif args.command == 'analyze':
        analyze()
    else:
        if args.mode not in ('timing', 'memory', 'abc') or args.index is None:
            raise ValueError('child mode and case index required')
        child(args.mode, args.index, args.arm)


if __name__ == '__main__':
    main()
