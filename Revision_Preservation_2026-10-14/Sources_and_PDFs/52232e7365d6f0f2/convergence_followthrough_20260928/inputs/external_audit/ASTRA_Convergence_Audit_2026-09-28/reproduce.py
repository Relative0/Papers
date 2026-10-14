"""Replay an audit component from included frozen inputs into a NEW directory.

Python 3.13.5 was used for the recorded run. Standard library except the original
Theory component, which requires SymPy (recorded version 1.14.0).
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
BASELINE = 'CM_Computation_Baseline_Handoff_for_Convergence_Audit_2026-09-28.zip'
THEORY = 'QK_THEORY_MILESTONE_1_BUNDLE(1).zip'


def extract_checked(archive: Path, target: Path) -> None:
    """Extract only regular relative members under target; refuse unsafe paths."""
    target.mkdir(parents=True, exist_ok=False)
    root = target.resolve()
    with zipfile.ZipFile(archive) as z:
        if sum(i.file_size for i in z.infolist()) > 200_000_000:
            raise ValueError('Unexpectedly large input archive')
        for i in z.infolist():
            p = Path(i.filename)
            mode = (i.external_attr >> 16) & 0xFFFF
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename or stat.S_ISLNK(mode):
                raise ValueError(f'Unsafe ZIP member: {i.filename}')
            dest = (root / p).resolve()
            if not dest.is_relative_to(root):
                raise ValueError(f'Escaping ZIP member: {i.filename}')
        z.extractall(root)


def run(command: list[str], log: Path) -> None:
    print('Executing:', ' '.join(command), flush=True)
    with log.open('w', encoding='utf-8') as f:
        p = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, check=False)
    if p.returncode:
        raise RuntimeError(f'Command returned {p.returncode}; inspect {log}')
    print(f'PASS; log: {log}', flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=('independent', 'baseline', 'theory', 'benchmark'))
    ap.add_argument('--output', type=Path, required=True, help='New directory; existing paths are refused.')
    a = ap.parse_args()
    output = a.output.resolve()
    if output.exists():
        ap.error('Output already exists. Select a new path to preserve previous evidence.')
    if a.mode == 'theory' and importlib.util.find_spec('sympy') is None:
        ap.error('Theory replay needs SymPy. Recorded version: python -m pip install sympy==1.14.0')
    output.mkdir(parents=True)
    if a.mode == 'independent':
        run([sys.executable, str(ROOT/'EVIDENCE/independent_math_audit.py'),
             '--output', str(output/'independent_math_results.json')], output/'run.log')
    elif a.mode in ('baseline', 'benchmark'):
        extract_checked(ROOT/'INPUT_SNAPSHOTS'/BASELINE, output/'input')
        b = output/'input/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility'
        script = 'run_correctness.py' if a.mode == 'baseline' else 'run_benchmark_copy.py'
        dest = output/('clean_correctness_replay.json' if a.mode == 'baseline' else 'timing_replay')
        run([sys.executable, str(b/script), '--output', str(dest)], output/'run.log')
    else:
        extract_checked(ROOT/'INPUT_SNAPSHOTS'/THEORY, output/'input')
        source = output/'input/verify_qk.py'
        original = source.read_text(encoding='utf-8')
        old = "'/mnt/data/theory_work/qk_verification_results.json'"
        if original.count(old) != 1:
            raise RuntimeError('Expected original output constant not found exactly once; refusing patch.')
        destination = output/'qk_verification_results.json'
        patched = original.replace(old, repr(str(destination)))
        runnable = output/'verify_qk_output_path_only_patch.py'
        runnable.write_text(patched, encoding='utf-8')
        receipt = {'change': 'Only the literal output filename was redirected; algorithm unchanged.',
                   'original_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                   'patched_sha256': hashlib.sha256(runnable.read_bytes()).hexdigest(),
                   'original_output_literal': old, 'new_output': str(destination)}
        (output/'portability_patch.json').write_text(json.dumps(receipt, indent=2)+'\n')
        run([sys.executable, str(runnable)], output/'run.log')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
