"""Freeze and execute the natural-circuit correctness gate without timing arms."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from aiger_check import truth_bits
from prepare_natural_admission import HERE, CM_SOURCE, SOURCE, ast_stats, parse, translated
from validate_abc_aig import digest


RUN = HERE / 'run_natural_correctness_001'
CASES = [json.loads(line) for line in (HERE / 'NATURAL_CASES.jsonl').read_text(encoding='utf-8').splitlines()]


def identity(path: Path):
    blob = path.read_bytes()
    return {'sha256': sha256(blob).hexdigest(), 'bytes': len(blob)}


def frozen_files():
    paths = [HERE / name for name in (
        'NATURAL_CORRECTNESS_PROTOCOL.md', 'natural_correctness.py',
        'NATURAL_ADMISSION_RULES.md', 'NATURAL_ADMISSION.json',
        'NATURAL_CASES.jsonl', 'NATURAL_SCREEN.jsonl', 'NATURAL_VALIDATION.json',
        'CONES_MANIFEST.json', 'ABC_TOOL_PROVENANCE.json',
        'ABC_TOOL_VALIDATION.json', 'ABC_AIG_VALIDATION.json',
        'aiger_check.py', 'validate_abc_aig.py', 'prepare_natural_admission.py')]
    paths += sorted((HERE / 'abc_tool').iterdir())
    paths += sorted(SOURCE.rglob('*.blif'))
    paths += sorted((HERE / 'cones').glob('*.blif'))
    paths += sorted((HERE / 'aig_outputs').glob('*.aig'))
    paths += [CM_SOURCE.parent / 'SOURCE_SNAPSHOT.json']
    if len(paths) != 14 + 7 + 20 + 71 + 71 + 1:
        raise ValueError(f'unexpected frozen file count: {len(paths)}')
    return paths


def prepare():
    if RUN.exists():
        raise RuntimeError('run directory already exists')
    aig_gate = json.loads((HERE / 'ABC_AIG_VALIDATION.json').read_text(encoding='utf-8'))
    if aig_gate['status'] != 'PASS_NO_CM_COMPILATION_OR_TIMING' or aig_gate['passed'] != 71:
        raise ValueError('ABC AIG gate has not passed')
    files = {path.relative_to(HERE.parent).as_posix(): identity(path) for path in frozen_files()}
    RUN.mkdir()
    (RUN / 'CORRECTNESS.jsonl').write_bytes(b'')
    frozen = {'schema': 'cm-natural-correctness-freeze/v1',
              'status': 'FROZEN_BEFORE_CM_NATURAL_COMPILATION', 'case_count': len(CASES),
              'source_commit': '0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b',
              'epfl_commit': '0060e156826e733d69bf5b3322d1bdd0d03a1f9a',
              'abc_version': 'ABC 1.01 (compiled Jul 29 2026 04:36:08)',
              'abc_command': 'read_blif {cone}; strash; dc2; write_aiger {aig}',
              'case_timeout_seconds': 60, 'files': files,
              'result_files_initially_empty': {'CORRECTNESS.jsonl': identity(RUN / 'CORRECTNESS.jsonl')},
              'performance_measured': False}
    (RUN / 'FREEZE.json').write_text(json.dumps(frozen, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': frozen['status'], 'files': len(files), 'cases': len(CASES)}))


def verify_freeze():
    frozen = json.loads((RUN / 'FREEZE.json').read_text(encoding='utf-8'))
    if frozen['case_count'] != 71 or len(frozen['files']) != len(frozen_files()):
        raise ValueError('freeze inventory mismatch')
    for relative, expected in frozen['files'].items():
        if identity(HERE.parent / relative) != expected:
            raise ValueError(f'frozen file changed: {relative}')
    snapshot = json.loads((CM_SOURCE.parent / 'SOURCE_SNAPSHOT.json').read_text(encoding='utf-8'))
    if snapshot['commit'] != frozen['source_commit']:
        raise ValueError('CM source commit differs')
    for name, expected in snapshot['files'].items():
        actual = identity(CM_SOURCE / name)
        if any(actual[key] != expected[key] for key in ('sha256', 'bytes')):
            raise ValueError(f'CM source file changed: {name}')
    return frozen


def one_case(index: int):
    from bitset_backend import build_bitset_env, eval_cm_node_bitset, eval_expr_bitset
    from cm_build_pair import compile_expr_to_cm_pair_token
    from cm_ir import compile_expr_to_cm_ir
    from cm_token import cm_token_value

    case = CASES[index]
    design = json.loads((HERE / 'NATURAL_ADMISSION.json').read_text(encoding='utf-8'))['designs']
    descriptor = next(item for item in design if item['design'] == case['design'])
    _, _, nodes = parse(SOURCE / descriptor['relative_path'])
    expr = translated(case['output'], tuple(case['support']), nodes)
    if ast_stats(expr)['translated_ast_sha256'] != case['translated_ast_sha256']:
        raise ValueError('reconstructed AST differs from frozen case')
    support = tuple(case['support'])
    n = len(support)
    variable_order = [f'x{j}' for j in reversed(range(n))]
    row = {'case_index': index, 'design': case['design'], 'output': case['output'],
           'support_count': n, 'source_truth_sha256': case['source_truth_sha256']}

    direct = eval_expr_bitset(expr, build_bitset_env(variable_order))
    ir = compile_expr_to_cm_ir(expr)
    ordinary = eval_cm_node_bitset(ir, variable_order)
    aig_path = HERE / 'aig_outputs' / f'{index:04d}_{case["design"]}.aig'
    aig, shape = truth_bits(aig_path, support)
    row['truth_sha256'] = {'direct_packed': digest(direct, n),
                           'ordinary_cm_ir': digest(ordinary, n),
                           'abc_aig': digest(aig, n)}
    row['abc_and_gates'] = shape['and_gates']
    if any(value != case['source_truth_sha256'] for value in row['truth_sha256'].values()):
        raise ValueError(f'truth disagreement: {row["truth_sha256"]}')

    row['strategies'] = {}
    for strategy in ('pure_structural', 'hybrid', 'retabulate'):
        compiled, metrics = compile_expr_to_cm_pair_token(
            expr, ['x0'], [f'x{j}' for j in range(1, n)], {}, strategy=strategy)
        arm = {'root_outcome': metrics['root_outcome'], 'metrics': metrics,
               'token_returned': compiled is not None}
        if compiled is not None:
            row_variable = int(compiled.row_variable[1:])
            column_variable = int(compiled.column_variable[1:])
            bits = sum(cm_token_value(compiled.token, (assignment >> row_variable) & 1,
                                      (assignment >> column_variable) & 1) << assignment
                       for assignment in range(1 << n))
            arm['truth_sha256'] = digest(bits, n)
            arm['row_variable'] = compiled.row_variable
            arm['column_variable'] = compiled.column_variable
            if arm['truth_sha256'] != case['source_truth_sha256']:
                raise ValueError(f'{strategy} token truth disagreement')
        row['strategies'][strategy] = arm
    row['status'] = 'PASS'
    return row


def run():
    frozen = verify_freeze()
    result = RUN / 'CORRECTNESS.jsonl'
    if result.stat().st_size != 0:
        raise RuntimeError('result file is not empty; never overwrite a run')
    statuses = Counter()
    for index in range(len(CASES)):
        try:
            process = subprocess.run([sys.executable, str(Path(__file__).resolve()), 'case', str(index)],
                                     cwd=HERE, capture_output=True, text=True,
                                     timeout=frozen['case_timeout_seconds'])
            if process.returncode:
                raise RuntimeError(f'case process exit {process.returncode}: '
                                   f'{process.stderr[-1500:]}')
            row = json.loads(process.stdout)
        except Exception as error:
            row = {'case_index': index, 'design': CASES[index]['design'],
                   'output': CASES[index]['output'], 'status': 'FAIL',
                   'error': f'{type(error).__name__}: {error}'}
        with result.open('a', encoding='utf-8') as output:
            output.write(json.dumps(row, sort_keys=True) + '\n')
        statuses[row['status']] += 1
        print(f'{index + 1}/{len(CASES)} {row["status"]} {row["design"]} {row["output"]}', flush=True)
    summary = {'status': 'PASS' if statuses['PASS'] == len(CASES) else 'FAIL',
               'cases': len(CASES), 'passed': statuses['PASS'], 'failed': statuses['FAIL'],
               'result_sha256': identity(result)['sha256'], 'performance_measured': False}
    (RUN / 'SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))
    if summary['status'] != 'PASS':
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare', 'run', 'case'))
    parser.add_argument('index', nargs='?', type=int)
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare()
    elif args.command == 'run':
        run()
    else:
        if args.index is None or not 0 <= args.index < len(CASES):
            raise ValueError('case index required')
        print(json.dumps(one_case(args.index), sort_keys=True))


if __name__ == '__main__':
    main()
