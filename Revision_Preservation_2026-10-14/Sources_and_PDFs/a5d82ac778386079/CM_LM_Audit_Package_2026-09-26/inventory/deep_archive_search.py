import hashlib, io, json, re, zipfile
from pathlib import Path
ROOT=Path('/mnt/data/cm_lm_audit_20260926')
seen_zips={}; entries=[]; hits=[]; py_seen=set(); totals={'zip_occurrences':0,'unique_zip_contents':0,'file_occurrences_visited':0,'unique_python_contents':0,'uncompressed_bytes_read':0}
patterns=re.compile(r'20[, _]?873|verify_cm_lm|1[, _]?536[, _]?530',re.I)

def walk(data,label,depth=0):
 if depth>10:raise RuntimeError('Excessive archive depth')
 digest=hashlib.sha256(data).hexdigest();totals['zip_occurrences']+=1
 if digest in seen_zips:
  entries.append({'archive':label,'sha256':digest,'identical_to':seen_zips[digest],'inspection':'duplicate archive: identical content to searched archive'});return
 seen_zips[digest]=label;totals['unique_zip_contents']+=1
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for info in z.infolist():
   if info.is_dir():continue
   if info.file_size>200_000_000:raise RuntimeError('Oversized member')
   b=z.read(info);path=label+'!/'+info.filename;totals['file_occurrences_visited']+=1;totals['uncompressed_bytes_read']+=len(b)
   h=hashlib.sha256(b).hexdigest();suffix=Path(info.filename).suffix.lower();e={'path':path,'bytes':len(b),'sha256':h,'depth':depth,'inspection':'filename/hash inventory'}
   if suffix in ['.py','.md','.txt','.tex','.json','.yaml','.yml','.csv','.toml','.sh','.log']:
    s=b.decode('utf-8',errors='replace');e['inspection']='text searched for historical-checker identifiers; not full content review'
    mh=[{'line':i+1,'text':l[:800]} for i,l in enumerate(s.splitlines()) if patterns.search(l)]
    if mh:hits.append({'path':path,'matches':mh})
   if suffix=='.py':py_seen.add(h)
   entries.append(e)
   if suffix=='.zip':walk(b,path,depth+1)
walk(Path('/mnt/data/Papers for Publication(3).zip').read_bytes(),'Papers for Publication(3).zip')
totals['unique_python_contents']=len(py_seen)
(ROOT/'inventory/deep_virtual_manifest.json').write_text(json.dumps({'totals':totals,'members':entries},indent=2))
(ROOT/'inventory/deep_historical_checker_hits.json').write_text(json.dumps(hits,indent=2))
print(json.dumps(totals,indent=2))
print('Files containing target identifiers:',len(hits))
print('Python hits:',[h['path'] for h in hits if h['path'].endswith('.py')])
