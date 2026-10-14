"""Verify final delivery bytes; no experiments or network calls."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
def included(p):
    parts=p.relative_to(ROOT).parts
    if '__pycache__' in parts or parts[:2]==('runtime','linux-venv') or parts==('MANIFEST_SHA256.json',):
        return False
    return p.is_file()
def main():
    rows=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())['files'];issues=[]
    for row in rows:
        p=(ROOT/row['path']).resolve()
        if not p.is_relative_to(ROOT):raise ValueError('escaping manifest path')
        if not p.is_file():issues.append([row['path'],'missing']);continue
        if len(p.read_bytes())!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:issues.append([row['path'],'hash/size'])
    expected={x['path'] for x in rows};actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if included(p)}
    issues.extend([x,'unexpected file'] for x in sorted(actual-expected))
    print(json.dumps({'status':'PASS' if not issues else 'FAIL','files_checked':len(rows),'issues':issues},indent=2));return bool(issues)
if __name__=='__main__':sys.exit(main())
