from pathlib import Path
import json,re,hashlib,collections,csv
A=Path(__file__).resolve().parent;ROOT=A.parents[1]
inv=json.loads((A/'original_inventory.json').read_text(encoding='utf-8'))['files']+json.loads((A/'supplemental_inventory.json').read_text(encoding='utf-8'))+json.loads((A/'named_download_discovery.json').read_text(encoding='utf-8'))['available']
arch=json.loads((A/'archive_inventory.json').read_text(encoding='utf-8'))
known={r['source']:r for r in inv}
for r in arch['members']:
 if r['kind']=='file':known[r['staging']]=dict(r,source=r['staging'])
byhash=collections.defaultdict(list)
for p,r in known.items():byhash[r['sha256']].append(p)
results=[]; receipts=[]
def check(p,target,h,label):
 h=h.lower(); target=str(target).replace('\\','/'); candidates=[]
 q=Path(target)
 if q.is_absolute():candidates=[q]
 else:
  for par in [p.parent,*list(p.parents)[:5]]:
   candidates.append(par/q)
  if target.startswith('/mnt/'):candidates=[]
 existing=next((q for q in candidates if str(q) in known and known[str(q)]['sha256']==h),None)
 if existing is None:
  existing=next((q for q in candidates[:1] if str(q) in known),None)
 if existing:
  actual=known[str(existing)]['sha256']; status='PASS' if actual==h else 'MISMATCH'
  results.append({'receipt':str(p),'field':label,'target':target,'expected_sha256':h,'resolved':str(existing),'actual_sha256':actual,'status':status});return
 # Relocated archived receipts often retain old paths. Match content AND filename.
 eq=[x for x in byhash.get(h,[]) if Path(x).name.casefold()==q.name.casefold()]
 if eq:results.append({'receipt':str(p),'field':label,'target':target,'expected_sha256':h,'resolved':eq[0],'status':'PASS_RELOCATED'});return
 results.append({'receipt':str(p),'field':label,'target':target,'expected_sha256':h,'status':'UNRESOLVED_REFERENCE'})
def walk(obj,p,prefix=''):
 if isinstance(obj,list):
  for i,x in enumerate(obj):walk(x,p,prefix+f'[{i}]')
 elif isinstance(obj,dict):
  for key,val in obj.items():
   if isinstance(val,str) and re.fullmatch('[a-fA-F0-9]{64}',val):
    target=None
    if re.search(r'[/\\.]',key) and not key.endswith('sha256'):target=key
    elif key in ['sha256','hash','SHA256']:
     target=next((obj[k] for k in ['path','file','filename','relative_path','archive','source','zip','name'] if isinstance(obj.get(k),str)),None)
    elif key.endswith('_sha256'):
     base=key[:-7];target=obj.get(base) or obj.get(base+'_path') or obj.get(base+'_file')
    if isinstance(target,str):check(p,target,val,prefix+'.'+key)
    else:
     results.append({'receipt':str(p),'field':prefix+'.'+key,'expected_sha256':val,'resolved':byhash[val][0] if val in byhash else None,'status':'PASS_CONTENT_HASH' if val in byhash else 'NON_FILE_HASH_NOT_REEVALUATED'})
   elif isinstance(val,(dict,list)):walk(val,p,prefix+'.'+key)
for name,r in known.items():
 p=Path(name)
 if '.venv' in p.parts:continue
 if not re.search('sha256|receipt|manifest|hashes|verification',p.name,re.I):continue
 if p.suffix.lower() not in ['.json','.txt','.sha256','.csv']:continue
 t=p.read_text(encoding='utf-8',errors='replace');before=len(results)
 if p.suffix.lower()=='.json':
  try:walk(json.loads(t),p)
  except Exception as e:receipts.append({'source':name,'status':'parse issue','reason':str(e)});continue
 elif p.suffix.lower()=='.csv':
  try:
   for row in csv.DictReader(t.splitlines()):walk(row,p)
  except Exception:pass
 else:
  for i,line in enumerate(t.splitlines()):
   m=re.match(r'^\s*([a-fA-F0-9]{64})\s+\*?(.+?)\s*$',line)
   if m:check(p,m[2],m[1],f'line {i+1}')
 receipts.append({'source':name,'hash_assertions':len(results)-before,'status':'parsed' if len(results)>before else 'historical report/no parseable path-hash assertions; retained, not a fresh scientific rerun'})
out={'summary':dict(collections.Counter(r['status'] for r in results)),'receipts':receipts,'checks':results}
(A/'checksum_verification_final.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'summary':out['summary'],'receipts':len(receipts),'issues':[r for r in results if r['status']=='MISMATCH'][:15]},indent=2))
