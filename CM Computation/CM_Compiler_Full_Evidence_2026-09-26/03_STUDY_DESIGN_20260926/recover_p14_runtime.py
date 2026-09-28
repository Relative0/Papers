"""Package located historical P14 runtime candidates and replay its analyzer.

The P14 freeze did not hash the whole imported runtime, so this recovery can
show a compatible local closure but cannot prove its historical execution ID.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo

HERE = Path(__file__).resolve().parent
AUDIT = Path(r'C:\Users\brian\Documents\CM_Computation\audit_p1_p13_20260918')
HISTORICAL = HERE.parent/'02_CONTRACT_REVISION_20260926/reproducibility/historical_evidence.zip'
BUNDLE = HERE/'P14_PORTABLE_RUNTIME_CANDIDATE.zip'
MANIFEST = HERE/'P14_RUNTIME_RECOVERY.json'
REPORT = HERE/'P14_ORIGINAL_ANALYZER_REPLAY.json'

def digest(data):
    return sha256(data).hexdigest()

def add_bytes(z, name, data, origin, members):
    if name in members:
        raise ValueError(name)
    info = ZipInfo(name, (2026, 9, 26, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    z.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=6)
    members[name] = {'sha256': digest(data), 'bytes': len(data), 'origin': origin}

def build():
    if not AUDIT.is_dir() or not HISTORICAL.is_file():
        raise FileNotFoundError('Historical local runtime or preserved archive is absent')
    root = AUDIT.resolve()
    members = {}
    natural_checked = {}
    with ZipFile(HISTORICAL) as historical, ZipFile(BUNDLE, 'w') as output:
        for name in historical.namelist():
            if name.startswith('p14_original/') and not name.endswith('/'):
                data = historical.read(name)
                add_bytes(output, 'p14_py0/'+name.split('/',1)[1], data,
                          'preserved historical_evidence.zip:'+name, members)
        natural = json.loads(historical.read('p14_original/natural_holdout.json'))
        for design in natural['designs']:
            relative = Path('p14_py0')/design['path']
            path = (root/relative).resolve()
            assert root in path.parents and path.is_file()
            data = path.read_bytes()
            assert digest(data) == design['sha256'], design['design']
            natural_checked[design['design']] = {'sha256': digest(data), 'bytes': len(data)}
            add_bytes(output, relative.as_posix(), data, str(path), members)
        for subdir in ('runtime', 'primary/ASTRA_P1_P13_AUDIT_PACKAGE', 'python_diagnostics'):
            for path in sorted((root/subdir).rglob('*')):
                if not path.is_file() or '__pycache__' in path.parts or path.suffix.lower() in ('.pyc','.pyo'):
                    continue
                resolved = path.resolve()
                assert root in resolved.parents and not path.is_symlink()
                relative = path.relative_to(root).as_posix()
                assert not any(s in path.name.lower() for s in ('.env', 'private_key', 'credential', 'secret'))
                add_bytes(output, relative, path.read_bytes(), str(resolved), members)
        diagnostic = root/'stats_free_diagnostic.py'
        add_bytes(output, diagnostic.relative_to(root).as_posix(), diagnostic.read_bytes(),
                  str(diagnostic), members)
    with ZipFile(BUNDLE) as z:
        assert z.testzip() is None and set(z.namelist()) == set(members)
    record = {
        'status': 'LOCATED_COMPATIBLE_RUNTIME_CANDIDATE',
        'historical_archive_sha256': digest(HISTORICAL.read_bytes()),
        'original_workspace': str(root),
        'bundle': BUNDLE.name, 'bundle_sha256': digest(BUNDLE.read_bytes()),
        'member_count': len(members), 'natural_designs_verified': natural_checked,
        'members': members,
        'provenance_limit': 'The P14 freeze hashes six P14 scripts and two holdouts, not the complete imported runtime tree. The local candidate cannot alone certify which runtime bytes were executed historically.',
    }
    MANIFEST.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(f"PACKAGED: {len(members)} members, {BUNDLE.stat().st_size} bytes")

def replay():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert digest(BUNDLE.read_bytes()) == manifest['bundle_sha256']
    temporary = Path(tempfile.mkdtemp(prefix='p14-analyzer-', dir=HERE)).resolve()
    assert HERE.resolve() in temporary.parents and temporary.name.startswith('p14-analyzer-')
    try:
        with ZipFile(BUNDLE) as z:
            for info in z.infolist():
                target = (temporary/info.filename).resolve()
                assert temporary in target.parents
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(info))
        p14 = temporary/'p14_py0'
        expected = json.loads((p14/'P14_RESULTS.json').read_text(encoding='utf-8'))
        original_hash = digest((p14/'P14_RESULTS.json').read_bytes())
        proc = subprocess.run([sys.executable, str(p14/'analyze_p14_optimized.py')], cwd=p14,
                              env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},
                              capture_output=True, text=True, timeout=600)
        (HERE/'P14_ORIGINAL_ANALYZER_STDOUT.txt').write_text(proc.stdout+proc.stderr, encoding='utf-8')
        if proc.returncode:
            raise RuntimeError(f'Archived analyzer failed: {proc.returncode}; see stdout file')
        actual = json.loads((p14/'P14_RESULTS.json').read_text(encoding='utf-8'))
        report = {'status':'PASS' if actual==expected else 'MISMATCH',
                  'analyzer':'Archived unchanged analyze_p14_optimized.py',
                  'archive_source_sha256': manifest['historical_archive_sha256'],
                  'runtime_bundle_sha256': manifest['bundle_sha256'],
                  'original_result_sha256': original_hash,
                  'replayed_result_sha256': digest((p14/'P14_RESULTS.json').read_bytes()),
                  'full_json_exact_match': actual==expected,
                  'raw_rows': actual.get('raw_rows'),
                  'scope':'Analysis replay with located local runtime candidate; does not prove historical timing runtime identity or rerun timing.'}
        REPORT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,indent=2))
        if actual != expected:
            raise RuntimeError('Archived analyzer output differs; inspect report')
    finally:
        assert HERE.resolve() in temporary.parents and temporary.name.startswith('p14-analyzer-')
        shutil.rmtree(temporary)

if __name__=='__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ('build', 'replay'):
        raise SystemExit('usage: python recover_p14_runtime.py {build|replay}')
    if sys.argv[1] == 'build':
        build()
    else:
        replay()
