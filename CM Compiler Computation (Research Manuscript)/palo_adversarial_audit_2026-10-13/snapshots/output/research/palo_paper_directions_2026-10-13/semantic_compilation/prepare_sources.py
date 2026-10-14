"""Read-only local source extraction; all outputs stay beside this script."""
from pathlib import Path
import hashlib, json, subprocess
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
inventory = json.loads((ROOT / 'output/pdf/palo_cm_relationships_2026-10-13/source_inventory.json').read_text(encoding='utf-8'))
rows = []
for s in inventory['sources']:
    if s['key'] not in ('PALO', 'LM', 'COMP', 'GU'):
        continue
    path = Path(s['path'])
    reader = PdfReader(path)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha == s['sha256'], (s['key'], 'source changed')
    pages = [p.extract_text() or '' for p in reader.pages]
    (OUT / (s['key'].lower() + '_pages.json')).write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / (s['key'].lower() + '_source_text.txt')).write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{p}' for i,p in enumerate(pages)), encoding='utf-8')
    rows.append({**s, 'verified_pages':len(pages), 'hash_matches_handoff':True})
(OUT/'local_source_inventory.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
status = subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True)
(OUT/'git_status_initial.txt').write_text(status.stdout,encoding='utf-8')
(OUT/'git_status_initial_stderr.txt').write_text(status.stderr,encoding='utf-8')
print(json.dumps([{'key':r['key'],'pages':r['verified_pages'],'hash_matches':r['hash_matches_handoff']} for r in rows]))
