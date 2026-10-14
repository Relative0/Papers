from pathlib import Path
import json,re,hashlib,zipfile,io,stat,collections
A=Path(__file__).resolve().parent;AUD=A;ROOT=A.parents[1];MIND=ROOT/'The MIND'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,o):
 with (A/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2,ensure_ascii=False)
inv=json.loads((A/'original_inventory.json').read_text(encoding='utf-8'))['files']+json.loads((A/'supplemental_inventory.json').read_text(encoding='utf-8'))+json.loads((A/'named_download_discovery.json').read_text(encoding='utf-8'))['available']
arc=json.loads((A/'archive_inventory.json').read_text(encoding='utf-8'))
known=collections.defaultdict(list)
for r in inv:known[Path(r['source']).name].append(r['source'])
for r in arc['members']:known[Path(r['member']).name].append(r['archive']+'!/'+r['member'])
refs=collections.defaultdict(set)
for filename in ['discovery_texts.json','archive_texts.json']:
 for r in json.loads((A/filename).read_text(encoding='utf-8')):
  if '.venv' in r['source']:continue
  for n in re.findall(r'\b([A-Za-z0-9][A-Za-z0-9_.-]{8,}\.zip)\b',r['text']):refs[n].add(r['source'])
new=[];register=[]
for n,s in sorted(refs.items()):
 p=Path('C:/Users/brian/Downloads')/n
 if p.is_file() and str(p) not in {r['source'] for r in inv}:
  r={'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'named_download'};new.append(r);known[n].append(str(p))
 register.append({'artifact':n,'referenced_by':sorted(s),'available_locations':known[n],'downloads_checked':str(p),'status':'available' if known[n] else 'referenced artifact unavailable at inspected paths'})
dump('additional_download_inventory.json',new)
archives=arc['archives'];members=arc['members'];unique={r['sha256']:r for r in archives if 'same_archive_as' not in r};texts=[];stage=A/'staging'
code=(A/'inspect_archives.py').read_text(encoding='utf-8');exec(code[code.index('def visit('):code.index('for r in sources:')])
for r in new:visit(Path(r['source']).read_bytes(),r['source'])
dump('archive_inventory_extended.json',{'archives':archives,'members':members})
dump('additional_archive_texts.json',texts)
dump('reference_register.json',register)
dump('access_limits.json',{'missing_fresh_review_directory':str(ROOT/'Paper_U_Fresh_Referee_2026-09-29'),'exists':(ROOT/'Paper_U_Fresh_Referee_2026-09-29').exists(),'missing_artifact':'PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip','replacement':'Paper_U_Independent_Review_2026-09-29/Paper_U_Complete_Rebuilt.zip','recovery_limit':'Replacement contains reconstructed review documents, not byte-for-byte restoration.','earlier_account_chats':'Not directly accessible through current account; transferred handoff/history records inspected instead.','chat_discovery':'50 recent Codex/chat entries, 100 archived Codex entries, 2 archived ChatGPT entries; 10 directly relevant chats read; older account history not claimed complete.','backup_zip':'Papers for Publication.zip inspected: 469 members, no The MIND, Paper_U or Structured Factorization members; left outside research scope.'})
print(json.dumps({'new_downloads':new,'missing':[r['artifact'] for r in register if not r['available_locations']]},indent=2))
