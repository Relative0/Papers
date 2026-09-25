"""Capture raw runs and verify the frozen baseline without modifying it."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent/'cm_lm_process_semantics_20260920'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_base():
    records = []
    for line in (BASE/'MANIFEST_SHA256.txt').read_text(encoding='utf-8-sig').splitlines():
        digest,relative = line.split('  ',1)
        actual = sha(BASE/relative)
        assert actual == digest, relative
        records.append({'path':relative,'sha256':actual})
    return records

def main():
    (ROOT/'logs').mkdir(exist_ok=True)
    (ROOT/'data').mkdir(exist_ok=True)
    before = verify_base()
    # Copy only the exact checker and its tests; new runs write into this copy.
    regression = ROOT/'baseline_regression'
    for relative in ['code/verify_process_semantics.py','tests/test_process_contract.py']:
        dest = regression/relative
        dest.parent.mkdir(exist_ok=True,parents=True)
        shutil.copyfile(BASE/relative,dest)
        assert sha(dest) == sha(BASE/relative)
    commands = [
        ('review_checks',[sys.executable,'-B',str(ROOT/'code'/'review_checks.py')]),
        ('baseline_exhaustive',[sys.executable,'-B',str(regression/'code'/'verify_process_semantics.py')]),
        ('baseline_unit_tests',[sys.executable,'-B',str(regression/'tests'/'test_process_contract.py')]),
    ]
    runs = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    for name,command in commands:
        start = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',env=env)
        (ROOT/'logs'/f'{name}.stdout.txt').write_text(result.stdout,encoding='utf-8')
        (ROOT/'logs'/f'{name}.stderr.txt').write_text(result.stderr,encoding='utf-8')
        runs.append({'name':name,'command':command,'start_utc':start,
                     'end_utc':datetime.now(timezone.utc).isoformat(),'exit_code':result.returncode})
        print(f'{name}: exit {result.returncode}',flush=True)
        if result.returncode:
            print(result.stderr)
            raise RuntimeError(name)
    after = verify_base()
    assert before == after
    report = {'status':'PASS','baseline':str(BASE),'baseline_manifest_sha256':sha(BASE/'MANIFEST_SHA256.txt'),
              'verified_manifest_entries':len(before),'baseline_unchanged':True,
              'runs':runs,'baseline_files':before,
              'git_note':'cwd is not a Git repository; status/diff unavailable; SHA256 inventories used.'}
    (ROOT/'data'/'run_record.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
