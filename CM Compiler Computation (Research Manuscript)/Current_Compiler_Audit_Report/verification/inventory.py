from pathlib import Path
import csv, hashlib, json, re
from urllib.parse import unquote
from collections import Counter, defaultdict
root=Path('/mnt/data/cm_audit_input/CM Computation')
out=Path('/mnt/data/cm_publication_audit_2026-09-26/evidence')
files=sorted(p for p in root.rglob('*') if p.is_file())
records=[dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
by={x['path']:x for x in records}
checks=[]
for m in root.rglob('*SHA256.csv'):
 rows=list(csv.DictReader(m.open(encoding='utf-8-sig')))
 for row in rows:
  rel=row.get('RelativePath',''); target=root/rel
  if not target.exists(): target=m.parent/rel
  actual=hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
  checks.append(dict(manifest=str(m.relative_to(root)),path=rel,expected=row.get('SHA256'),actual=actual,status='PASS' if actual==row.get('SHA256') else ('MISSING' if actual is None else 'MISMATCH')))
groups=defaultdict(list)
for r in records: groups[r['sha256']].append(r['path'])
links=[]
for p in files:
 if p.suffix.lower() not in ['.md','.tex']:continue
 text=p.read_text(errors='replace')
 for match in re.finditer(r'\]\(([^\n]+?)\)',text):
  target=match.group(1).strip('<>')
  if re.match(r'https?://|mailto:',target) or target.startswith('#'):continue
  resolved=(p.parent/unquote(target.split('#')[0])).resolve()
  if not resolved.exists():links.append({'file':str(p.relative_to(root)),'line':text.count('\n',0,match.start())+1,'target':target,'outside_root':not resolved.is_relative_to(root.resolve())})
result={'file_count':len(files),'extensions':dict(Counter(p.suffix for p in files)),'inventory':records,'manifest_checks':checks,'duplicates':[v for v in groups.values() if len(v)>1],'broken_relative_links':links}
(out/'archive_inventory.json').write_text(json.dumps(result,indent=2))
print('FILES',len(files),'EXTENSIONS',result['extensions'])
for m in sorted(set(x['manifest'] for x in checks)):
 print(m,dict(Counter(x['status'] for x in checks if x['manifest']==m)))
print('DUPLICATES',json.dumps(result['duplicates'],indent=2))
print('BROKEN RELATIVE LINKS',len(links))
print('CURRENT HASH',by['01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/Operator_Level_CM_Compiler_Revised_Draft.tex']['sha256'])
