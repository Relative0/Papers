"""Portable entry point for this revision's source-bound correctness evidence."""
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

from check_historical import check
from check_audit import check as check_audit

ROOT = Path(__file__).resolve().parent
snapshot = json.loads((ROOT / 'SOURCE_SNAPSHOT.json').read_text())
for name, record in snapshot['files'].items():
    assert hashlib.sha256((ROOT / 'source' / name).read_bytes()).hexdigest() == record['sha256'], name
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
args = [sys.executable, '-m', 'pytest', '-p', 'no:cacheprovider', '-q',
        'source/tests/test_cm_pair_alignment.py', 'source/tests/test_output_budget.py', 'test_contract.py']
run = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True)
(ROOT / 'TEST_STDOUT.txt').write_text(run.stdout + run.stderr, encoding='utf-8')
print(run.stdout + run.stderr, end='')
if run.returncode:
    raise SystemExit(run.returncode)
historical = check()
(ROOT / 'HISTORICAL_CHECKS.json').write_text(json.dumps(historical, indent=2) + '\n')
audit = check_audit()
versions = {}
for package in ('numpy', 'pytest', 'requests', 'psutil', 'numba', 'dd'):
    try:
        versions[package] = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        versions[package] = None
result = {'status': 'PASS', 'source_commit': snapshot['commit'], 'source_files_verified': len(snapshot['files']),
          'python': sys.version, 'platform': platform.platform(), 'dependencies': versions,
          'test_command': ['python'] + args[1:], 'test_returncode': run.returncode,
          'test_scope': '90 upstream tests and 33 contract cases; one contract test includes 327680 scalar fusion comparisons.',
          'historical': historical, 'audit_reference_model': audit, 'timing_campaign_executed': False}
(ROOT / 'CHECK_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print('Source hashes, contract tests, S1/S2 recount, P14 point estimates, and supplied audit checker: PASS')
