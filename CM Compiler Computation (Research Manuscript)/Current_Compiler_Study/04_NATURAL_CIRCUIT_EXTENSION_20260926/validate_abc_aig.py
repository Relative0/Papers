"""Convert every frozen cone with ABC and exhaustively check the output AIG."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess

from aiger_check import truth_bits


HERE = Path(__file__).resolve().parent


def digest(bits: int, inputs: int) -> str:
    rows = 1 << inputs
    return sha256(inputs.to_bytes(1, 'little')
                  + bits.to_bytes((rows + 7) // 8, 'little')).hexdigest()


def main():
    cases = [json.loads(line) for line in (HERE / 'NATURAL_CASES.jsonl').read_text(encoding='utf-8').splitlines()]
    manifest = json.loads((HERE / 'CONES_MANIFEST.json').read_text(encoding='utf-8'))
    provenance = json.loads((HERE / 'ABC_TOOL_PROVENANCE.json').read_text(encoding='utf-8'))
    binary = HERE / 'abc_tool' / 'yosys-abc.exe'
    if sha256(binary.read_bytes()).hexdigest() != provenance['files']['yosys-abc.exe']['sha256']:
        raise ValueError('ABC executable hash differs from provenance')
    if len(cases) != 71 or len(manifest['records']) != len(cases):
        raise ValueError('frozen case or cone count differs')
    output_dir = HERE / 'aig_outputs'
    output_dir.mkdir(exist_ok=True)
    results = []
    for index, (case, cone) in enumerate(zip(cases, manifest['records'])):
        record = {'case_index': index, 'design': case['design'], 'source_output': case['output']}
        try:
            source = HERE / cone['path']
            if cone['case_index'] != index or sha256(source.read_bytes()).hexdigest() != cone['sha256']:
                raise ValueError('frozen cone mismatch')
            destination = output_dir / (source.stem + '.aig')
            if destination.exists():
                raise ValueError('AIG output already exists; run in a clean project copy')
            command = f'read_blif {cone["path"]}; strash; dc2; write_aiger {destination.relative_to(HERE).as_posix()}'
            run = subprocess.run([str(binary), '-c', command], cwd=HERE,
                                 capture_output=True, text=True, timeout=60)
            record['abc_return_code'] = run.returncode
            record['abc_stdout'] = run.stdout
            record['abc_stderr'] = run.stderr
            if run.returncode:
                raise RuntimeError(f'ABC exit {run.returncode}')
            if not destination.exists():
                raise RuntimeError('ABC produced no AIG output')
            bits, shape = truth_bits(destination, tuple(case['support']))
            actual = digest(bits, len(case['support']))
            record.update({'aig_path': destination.relative_to(HERE).as_posix(),
                           'aig_sha256': sha256(destination.read_bytes()).hexdigest(),
                           'aig_bytes': destination.stat().st_size,
                           'aig_shape': shape, 'truth_sha256': actual})
            if actual != case['source_truth_sha256']:
                raise ValueError('AIG truth table differs from frozen source')
            record['status'] = 'PASS'
        except Exception as error:
            record['status'] = 'FAIL'
            record['error'] = f'{type(error).__name__}: {error}'
        results.append(record)
        print(f'{index + 1}/{len(cases)} {record["status"]} {case["design"]} {case["output"]}', flush=True)
    passed = sum(row['status'] == 'PASS' for row in results)
    result = {'status': 'PASS_NO_CM_COMPILATION_OR_TIMING' if passed == len(cases) else 'FAIL',
              'case_count': len(cases), 'passed': passed, 'failed': len(cases) - passed,
              'abc_sha256': provenance['files']['yosys-abc.exe']['sha256'],
              'command_template': 'read_blif {cone}; strash; dc2; write_aiger {aig}',
              'timeout_seconds_per_case': 60, 'records': results}
    (HERE / 'ABC_AIG_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'passed': passed, 'failed': len(cases) - passed}))
    if passed != len(cases):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
