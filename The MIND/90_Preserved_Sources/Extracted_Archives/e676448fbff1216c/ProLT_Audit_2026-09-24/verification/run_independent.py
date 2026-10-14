"""Run the independent checks in a fresh output directory.

Example:
    python run_independent.py --output ./my_rerun --include-five-state
Install requirements.txt first. Reference JSON files are never overwritten.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main() -> int:
    if not __debug__:
        raise RuntimeError('Assertions are required: do not run Python with -O.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('prolt_independent_rerun'))
    parser.add_argument('--include-five-state', action='store_true',
                        help='Also exhaust all two-bit height<=2 profiles on five vertices.')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f'Output path already exists; choose a fresh path: {output}')
    output.mkdir(parents=True)
    source = Path(__file__).resolve().parent / 'independent'
    for name in ('audit_checks.py', 'higher_height_and_edges.py', 'extend_two_bits.py', 'minimize_named_labels.py'):
        shutil.copy2(source / name, output / name)
    commands = [['audit_checks.py'], ['higher_height_and_edges.py'], ['minimize_named_labels.py']]
    if args.include_five_state:
        commands.append(['extend_two_bits.py', '--n', '5'])
    results = []
    for command in commands:
        started = time.perf_counter()
        logfile = output / (Path(command[0]).stem + '.log')
        with logfile.open('w', encoding='utf-8') as log:
            proc = subprocess.run([sys.executable, *command], cwd=output,
                                  stdout=log, stderr=subprocess.STDOUT, check=False)
        results.append({'command': command, 'returncode': proc.returncode,
                        'seconds': time.perf_counter() - started, 'log': logfile.name})
        (output / 'rerun_metadata.json').write_text(
            json.dumps({'python': sys.version, 'results': results}, indent=2), encoding='utf-8')
        print(command, 'exit', proc.returncode, 'log', logfile, flush=True)
        if proc.returncode:
            return proc.returncode
    print('All independent assertions passed. Results:', output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
