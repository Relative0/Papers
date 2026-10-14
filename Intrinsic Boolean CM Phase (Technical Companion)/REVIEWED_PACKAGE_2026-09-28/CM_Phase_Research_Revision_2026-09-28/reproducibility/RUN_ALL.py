#!/usr/bin/env python3
"""Run the inherited and new verification from any working directory.

Requires Python 3.10+ and NumPy for the inherited inventory. The new
verification and report checker themselves use the standard library only.
No network access is used. Generated data are refreshed in this package.
"""
from pathlib import Path
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    logs = root / 'logs'
    logs.mkdir(exist_ok=True)
    jobs = [
        ('legacy_inventory', root / 'legacy/code/verify_intrinsic.py'),
        ('legacy_report_check', root / 'legacy/code/check_report.py'),
        ('revision_verification', root / 'code/verify_revision.py'),
    ]
    for name, script in jobs:
        print(f'Running {name}', flush=True)
        with (logs / f'{name}.log').open('w', encoding='utf-8') as output:
            result = subprocess.run(
                [sys.executable, str(script)], cwd=script.parent.parent,
                stdout=output, stderr=subprocess.STDOUT, check=False,
            )
        if result.returncode:
            print(f'FAILED: {name}; see {logs / (name + ".log")}', file=sys.stderr)
            return result.returncode
        print(f'PASS: {name}', flush=True)
    print('All declared verification stages passed.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
