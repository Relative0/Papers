"""Non-confirmatory protocol-v3 synthetic primary-cell harness pilot.

Pilot seeds are disjoint from the proposed held-out corpus. No confirmatory
measurements are made by this script.
"""
from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / '02_CONTRACT_REVISION_20260926/reproducibility/source'
sys.path.insert(0, str(SOURCE))

from bitset_backend import build_bitset_env, clear_bitset_env_cache, eval_expr_bitset
from cm_build_pair import _expr_stats, compile_expr_to_cm_pair_token
from cm_exprlib import And, Eqv, Imp, Not, Or, Var, Xor
from cm_normalize import clear_cm_normalize_caches
from cm_token import cm_compose, cm_token_value

OPS = (And, Or, Xor, Imp, Eqv)
PILOT_SEEDS = tuple(202609270000 + i for i in range(8))
HELD_OUT_SEEDS = tuple(202610010000 + i for i in range(64))


def make_case(seed: int):
    rng = random.Random(seed)
    primitive_count = 205
    negated = set(rng.sample(range(2 * primitive_count), 204))
    leaves = []
    for i in range(primitive_count):
        operands = [Var(0), Var(1)]
        if 2*i in negated:
            operands[0] = Not(operands[0])
        if 2*i+1 in negated:
            operands[1] = Not(operands[1])
        if rng.getrandbits(1):
            operands.reverse()
        leaves.append(OPS[rng.randrange(5)](*operands))

    def combine(parts):
        if len(parts) == 1:
            return parts[0]
        middle = len(parts)//2
        return OPS[rng.randrange(5)](combine(parts[:middle]), combine(parts[middle:]))

    expr = combine(leaves)
    variables, occurrences, unique, height = _expr_stats(expr)
    assert variables == ['x0', 'x1'] and occurrences == unique == 1023
    assert height <= 128
    return expr, {'seed': seed, 'ast_occurrences': occurrences,
                  'unique_object_nodes': unique, 'ast_height': height,
                  'primitive_count': primitive_count, 'literal_negations': len(negated)}


def oracle(expr):
    token = eval_expr_bitset(expr, build_bitset_env(['x0', 'x1']))
    compiled, metrics = compile_expr_to_cm_pair_token(expr, ['x0'], ['x1'], {}, strategy='pure_structural')
    assert compiled is not None and metrics['root_outcome'] == 'pure_structural'
    assert metrics['direct_pair_retabulations'] == 0
    assert compiled.token == token
    for r in (0, 1):
        for c in (0, 1):
            assert cm_token_value(compiled.token, r, c) == cm_token_value(token, r, c)
    return token, metrics


def call_arm(expr, arm):
    if arm == 'CM':
        cm_compose.cache_clear()
        clear_cm_normalize_caches()
        start = time.perf_counter_ns()
        result, metrics = compile_expr_to_cm_pair_token(expr, ['x0'], ['x1'], {}, strategy='pure_structural')
        elapsed = time.perf_counter_ns() - start
        assert result is not None and metrics['root_outcome'] == 'pure_structural'
        return result.token, elapsed
    clear_bitset_env_cache()
    start = time.perf_counter_ns()
    env = build_bitset_env(['x0', 'x1'])
    token = eval_expr_bitset(expr, env)
    elapsed = time.perf_counter_ns() - start
    return token, elapsed


def one_block(expr, arm, count):
    samples = []
    for _ in range(count):
        _, elapsed = call_arm(expr, arm)
        samples.append(elapsed)
    return {'inner_calls': count, 'sum_ns': sum(samples), 'per_call_ns': sum(samples)/count}


def main():
    schedule = random.Random(202609270099)
    rows = []
    calibration = []
    for case_id, seed in enumerate(PILOT_SEEDS):
        expr, stats = make_case(seed)
        token, metrics = oracle(expr)
        for arm in ('CM', 'packed'):
            call_arm(expr, arm)  # untimed warm-up
        initial = {arm: one_block(expr, arm, 3)['per_call_ns'] for arm in ('CM', 'packed')}
        loops = {arm: min(500, max(1, math.ceil(100_000_000 / initial[arm]))) for arm in initial}
        calibration.append({'case_id': case_id, 'seed': seed, 'initial_ns': initial, 'loops': loops})
        for repetition in range(10):
            arms = ['CM', 'packed']
            schedule.shuffle(arms)
            for arm in arms:
                block = one_block(expr, arm, loops[arm])
                rows.append({'case_id': case_id, 'seed': seed, 'repetition': repetition,
                             'arm': arm, 'order': arms.index(arm), **block})
        print(f'pilot case {case_id+1}/{len(PILOT_SEEDS)} complete', flush=True)
    noise = {}
    for arm in ('CM', 'packed'):
        cv = []
        for case_id in range(len(PILOT_SEEDS)):
            series = [r['per_call_ns'] for r in rows if r['case_id'] == case_id and r['arm'] == arm]
            median = statistics.median(series)
            cv.append(statistics.median(abs(x-median) for x in series)/median)
        noise[arm] = {'per_case_mad_over_median': cv, 'median': statistics.median(cv), 'max': max(cv)}
    output = {'status': 'NON_CONFIRMATORY_PILOT', 'primary_cell': {'N': 1023, 'U': 1023,
              'signed_stratum': 'B', 'reuse': 1, 'output': 'token'},
              'pilot_seeds': PILOT_SEEDS, 'held_out_seeds_sha256': sha256(json.dumps(HELD_OUT_SEEDS).encode()).hexdigest(),
              'cache_policy': 'Post-import resident process. Clear documented CM and packed caches outside each timed call; build packed environment inside direct arm.',
              'source_snapshot': SOURCE.as_posix(), 'repetitions_per_case': 10,
              'target_block_ns': 100_000_000, 'calibration': calibration, 'noise': noise, 'rows': rows,
              'no_primary_effect_estimate': True}
    (HERE/'PILOT_RESULTS.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': output['status'], 'cases': len(PILOT_SEEDS), 'noise': noise}, indent=2))


if __name__ == '__main__':
    main()
