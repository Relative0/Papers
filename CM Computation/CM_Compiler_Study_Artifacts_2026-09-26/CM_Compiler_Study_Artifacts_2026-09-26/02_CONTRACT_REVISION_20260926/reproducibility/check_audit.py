"""Verify the supplied audit archive and rerun its inspected reference checker.

The archive is immutable. The unmodified standard-library checker runs in a
temporary directory, so the audit's recorded results are never overwritten.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / 'audit' / 'CM_Publication_Audit_Evidence_2026-09-26.zip'


def check():
    with ZipFile(ARCHIVE) as z:
        manifest = json.loads(z.read('AUDIT_BUNDLE_SHA256.json'))
        assert set(z.namelist()) == set(manifest) | {'AUDIT_BUNDLE_SHA256.json'}
        for name, expected in manifest.items():
            assert hashlib.sha256(z.read(name)).hexdigest() == expected, name
        code = z.read('verification/independent_finite_checks.py')
        recorded = json.loads(z.read('verification/independent_finite_results.json'))
    with tempfile.TemporaryDirectory(prefix='cm-audit-check-') as temporary:
        script = Path(temporary) / 'independent_finite_checks.py'
        script.write_bytes(code)
        run = subprocess.run([sys.executable, str(script)], cwd=temporary,
                             capture_output=True, text=True, timeout=60)
        assert run.returncode == 0, run.stderr
        fresh = json.loads((Path(temporary) / 'independent_finite_results.json').read_text())
        assert fresh == recorded, 'Reference-check results differ from supplied audit'
    result = {'status': 'PASS', 'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
              'manifest_entries_verified': len(manifest), 'python': sys.version,
              'unmodified_checker_sha256': hashlib.sha256(code).hexdigest(),
              'matches_supplied_results_exactly': True, 'results': fresh,
              'scope': 'Rerun of supplied mathematical/reference model, separate from production-source tests and timing evidence.'}
    (ROOT / 'AUDIT_CHECK_RERUN.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'AUDIT_CHECK_STDOUT.txt').write_text(run.stdout + run.stderr, encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
