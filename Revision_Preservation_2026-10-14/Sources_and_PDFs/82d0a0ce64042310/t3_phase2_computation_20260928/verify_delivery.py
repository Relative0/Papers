from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
def included(p):
    rel=p.relative_to(ROOT)
    return '__pycache__' not in rel.parts and 'replay-venv' not in rel.parts and rel.as_posix()!='MANIFEST_SHA256.json' and p.is_file()
def main():
    manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text());issues=[]
    for row in manifest['files']:
        p=(ROOT/row['path']).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():issues.append([row['path'],'missing/unsafe']);continue
        data=p.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:issues.append([row['path'],'hash/size'])
    expected={r['path'] for r in manifest['files']};actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if included(p)}
    issues.extend([x,'unexpected'] for x in sorted(actual-expected))
    print(json.dumps({'status':'PASS' if not issues else 'FAIL','files':len(expected),'issues':issues},indent=2));return bool(issues)
if __name__=='__main__':sys.exit(main())
