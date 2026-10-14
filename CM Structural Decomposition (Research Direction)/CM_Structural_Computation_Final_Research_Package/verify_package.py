"""Verify recorded package bytes. Run before editing or rebuilding frozen files."""
from pathlib import Path
import hashlib,json,sys

def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'05_MANIFEST_SHA256.json').read_text())
    bad=[]
    for item in manifest['files']:
        p=root/item['path']
        if not p.is_file():bad.append({'path':item['path'],'error':'missing'});continue
        if p.stat().st_size!=item['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            bad.append({'path':item['path'],'error':'bytes or SHA-256 mismatch'})
    print(json.dumps({'status':'PASS' if not bad else 'FAIL','files_checked':len(manifest['files']),'issues':bad},indent=2))
    return int(bool(bad))
if __name__=='__main__':sys.exit(main())
