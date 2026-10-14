from pathlib import Path
import hashlib, json, subprocess
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SITE = Path(r'C:\Users\brian\Documents\B-Theory\Website')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

files = subprocess.check_output(['rg', '--files', '--hidden', '-g', '*.pdf', '-g', '!**/.git/**', '-g', '!**/node_modules/**'], cwd=ROOT, text=True).splitlines()
pdfs = [ROOT / f for f in files]
records = []
for path in sorted((SITE / 'public/manuscripts').glob('*.pdf')):
    reader = PdfReader(path)
    digest = sha(path)
    pages = [p.extract_text() or '' for p in reader.pages]
    matches = [str(p.relative_to(ROOT)) for p in pdfs if p.stat().st_size == path.stat().st_size and sha(p) == digest]
    rec = dict(site_file=str(path), sha256=digest, size=path.stat().st_size, pages=len(pages), metadata=dict(reader.metadata or {}), matches=matches, name_occurrences=[dict(page=i+1, lines=[line for line in txt.splitlines() if 'Brian' in line or 'Droncheff' in line]) for i,txt in enumerate(pages) if 'Brian' in txt or 'Droncheff' in txt])
    records.append(rec)
    (OUT / (path.stem + '.txt')).write_text('\n\n'.join(f'--- PAGE {i+1} ---\n{txt}' for i,txt in enumerate(pages)), encoding='utf-8')
(OUT / 'provenance_before.json').write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps([dict(file=Path(r['site_file']).name, sha256=r['sha256'], pages=r['pages'], metadata=r['metadata'], matches=[p for p in r['matches'] if not any(s in p for s in ['90_Preserved_Sources','Review_Workspaces','Archive_Only_Content','Supporting_Research'])], name_occurrences=r['name_occurrences']) for r in records], indent=2, ensure_ascii=False))
