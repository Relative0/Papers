"""Run and compare the complete stated finite evidence without external inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def substantive(value):
    if isinstance(value, dict):
        return {key: substantive(item) for key, item in value.items()
                if key not in {'seconds', 'python', 'platform'}}
    if isinstance(value, list):
        return [substantive(item) for item in value]
    return value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise RuntimeError('Do not use python -O/-OO or PYTHONOPTIMIZE: assertions must run')
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=ROOT / 'reproduced')
    args = ap.parse_args()
    out = args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f'Refusing to overwrite nonempty output directory: {out}')
    out.mkdir(parents=True, exist_ok=True)
    record = dict(status='RUNNING', utc=datetime.now(timezone.utc).isoformat(),
                  python=sys.version, executable=sys.executable,
                  platform=platform.platform(), stages=[])
    start = time.monotonic()
    try:
        stages = [
            ('audit_checks', [sys.executable, '-B', str(ROOT / 'p01_independent_checks.py'),
                              '--out', str(out / 'results')]),
            ('companion_checks', [sys.executable, '-B', str(ROOT / 'run_companion_checks.py'),
                                  '--out', str(out / 'companion_results.json')]),
            ('generate_table', [sys.executable, '-B', str(ROOT / 'generate_assets.py'),
                                '--results', str(out / 'results'), '--out', str(out / 'smith_table.tex')]),
        ]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        for label, command in stages:
            print(f'Running {label}', flush=True)
            stage_start = time.monotonic()
            proc = subprocess.run(command, cwd=ROOT.parent, env=env, capture_output=True,
                                  text=True, encoding='utf-8', errors='replace')
            (out / f'{label}.log').write_text(proc.stdout + proc.stderr, encoding='utf-8')
            record['stages'].append(dict(stage=label, argv=command, cwd=str(ROOT.parent),
                                         exit_code=proc.returncode, seconds=time.monotonic()-stage_start))
            if proc.returncode:
                raise RuntimeError(f'{label} failed; see {out / (label + ".log")}')
        comparisons = []
        for reference in sorted((ROOT / 'reference_results').iterdir()):
            actual = out / 'results' / reference.name
            if reference.suffix == '.json':
                same = substantive(json.loads(reference.read_text())) == substantive(json.loads(actual.read_text()))
            else:
                same = reference.read_text() == actual.read_text()
            if not same:
                raise AssertionError(f'Substantive output mismatch: {reference.name}')
            comparisons.append(reference.name)
        expected_companion = ROOT / 'companion_reference.json'
        if substantive(json.loads(expected_companion.read_text())) != substantive(json.loads((out / 'companion_results.json').read_text())):
            raise AssertionError('Companion output mismatch')
        if (out / 'smith_table.tex').read_text() != (ROOT.parent / 'manuscript/smith_table.tex').read_text():
            raise AssertionError('Manuscript table differs from freshly generated table')
        record.update(status='PASS', reference_comparisons=comparisons,
                      companion_comparison='PASS', manuscript_table_comparison='PASS')
    except Exception as error:
        record.update(status='FAIL', error=str(error))
        raise
    finally:
        record['seconds'] = time.monotonic()-start
        inputs = sorted(ROOT.glob('*.py')) + sorted((ROOT / 'companion_source').glob('*.py'))
        inputs += sorted((ROOT / 'reference_results').glob('*')) + [ROOT / 'companion_reference.json', ROOT.parent / 'manuscript/smith_table.tex']
        record['input_sha256'] = {p.relative_to(ROOT.parent).as_posix(): digest(p) for p in inputs}
        record['output_sha256'] = {p.relative_to(out).as_posix(): digest(p) for p in sorted(out.rglob('*')) if p.is_file()}
        (out / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('PASS: full checks, companion comparison, reference comparison and manuscript table')


if __name__ == '__main__':
    main()
