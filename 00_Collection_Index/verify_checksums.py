"""Verify recorded SHA-256 claims without rewriting historical manifests."""
from snapshot import ROOT,OUT,dump
import json,csv,io,re,pathlib,posixpath,zipfile,collections
HEX=re.compile(r'^[0-9a-fA-F]{64}$')
def claims(text,name):
    out=[]
    def walk(o):
        if isinstance(o,list):
            for v in o:walk(v)
        elif isinstance(o,dict):
            lower={k.lower():v for k,v in o.items()}
            p=next((lower[k] for k in ('path','relativepath','relative_path','file','archive','zip','name','recorded_path','new','original_path') if isinstance(lower.get(k),str)),None)
            h=next((lower[k] for k in ('sha256','sha_256','sha256_hash','expected','hash') if isinstance(lower.get(k),str) and HEX.fullmatch(lower[k])),None)
            if p and h:out.append((p,h.lower()))
            for k,v in o.items():
                if isinstance(v,str) and HEX.fullmatch(v) and ('.' in k or '/' in k or '\\' in k):out.append((k,v.lower()))
                elif isinstance(v,(dict,list)):walk(v)
    try:
        if name.lower().endswith('.json'):walk(json.loads(text))
        elif name.lower().endswith('.csv'):
            for row in csv.DictReader(io.StringIO(text)):walk(row)
        else:
            for line in text.splitlines():
                m=re.match(r'^\s*([a-fA-F0-9]{64})\s+\*?(.+?)\s*$',line)
                if m:out.append((m[2],m[1].lower()))
    except (ValueError,csv.Error):pass
    return list(dict.fromkeys(out))
def main():
    B=json.loads((OUT/'baseline_sources.json').read_text(encoding='utf-8'));E=json.loads((OUT/'external_sources.json').read_text(encoding='utf-8'));A=json.loads((OUT/'archive_catalog.json').read_text(encoding='utf-8'))
    bypath={x['original_path'].replace('\\','/'):x['sha256'] for x in B+E};byhash=collections.defaultdict(list)
    for p,h in bypath.items():byhash[h].append(p)
    for h,a in A.items():
        for m in a['members']:
            if m.get('sha256'):byhash[m['sha256']].append('zip-sha256:'+h+'!/'+m['path'])
    rows=[];records=[]
    def verify(text,name,context,lookup):
        cs=claims(text,name);records.append({'record':context,'claims':len(cs),'status':'HASH_CLAIMS_INSPECTED' if cs else 'NO_SUPPORTED_FILE_HASH_CLAIMS'})
        base=posixpath.dirname(name.replace('\\','/'))
        for path,expected in cs:
            p=path.replace('\\','/'); direct=posixpath.normpath(posixpath.join(base,p))
            # Only compare inventoried paths; excluded The MIND is never opened.
            candidates=[];parent=base
            for _ in range(len(base.split('/'))+1):
                q=posixpath.normpath(posixpath.join(parent,p))
                if q in lookup:candidates.append(q)
                parent=posixpath.dirname(parent)
            if p in lookup:candidates.append(p)
            if p.startswith(str(ROOT).replace('\\','/')+'/'):
                rp=p[len(str(ROOT))+1:]
                if rp in lookup:candidates.append(rp)
            exact=next((q for q in candidates if lookup[q]==expected),None)
            if exact:status='PASS_AT_RESOLVED_PATH';actual=lookup[exact]
            elif candidates:status='RECORDED_PATH_DIFFERS';actual=lookup[candidates[0]]
            else:status='RECORDED_PATH_NOT_PRESENT';actual=None
            alternatives=byhash.get(expected,[])
            rows.append({'record':context,'recorded_path':path,'expected_sha256':expected,'status':status,'resolved_path':exact or (candidates[0] if candidates else None),'actual_sha256':actual,'recorded_bytes_retained':bool(alternatives),'matching_locations':alternatives[:12],'matching_location_count':len(alternatives)})
    for f in B:
        p=ROOT/f['original_path']
        if re.search(r'manifest|receipt|sha256|checksum',p.name,re.I) and p.suffix.lower() in ('.txt','.csv','.json','.sha256','') and f['size']<12_000_000:
            verify(p.read_text(encoding='utf-8-sig',errors='replace'),f['original_path'],f['original_path'],bypath)
    cache={}
    def zip_bytes(h):
        if h in cache:return cache[h]
        loc=A[h]['locations'][0]
        if 'source_path' in loc:
            p=pathlib.Path(loc['source_path']);p=p if p.is_absolute() else ROOT/p
            data=p.read_bytes()
        else:
            with zipfile.ZipFile(io.BytesIO(zip_bytes(loc['parent_archive_sha256']))) as z:data=z.read(z.infolist()[loc['member_index']])
        cache[h]=data;return data
    for h,a in A.items():
        lookup={posixpath.normpath(m['path'].replace('\\','/')):m.get('sha256') for m in a['members']}
        todo=[m for m in a['members'] if not m['directory'] and re.search('manifest|receipt|sha256|checksum',pathlib.PurePosixPath(m['path']).name,re.I) and pathlib.PurePosixPath(m['path']).suffix.lower() in ('.txt','.csv','.json','.sha256','') and m['size']<12_000_000]
        if todo:
            with zipfile.ZipFile(io.BytesIO(zip_bytes(h))) as z:
                for m in todo:verify(z.read(z.infolist()[m['index']]).decode('utf-8-sig',errors='replace'),m['path'],'zip-sha256:'+h+'!/'+m['path'],lookup)
    dump('checksum_records.json',records);dump('checksum_claims.json',rows)
    summary={'records_inspected':len(records),'hash_claims':len(rows),'status_counts':dict(collections.Counter(x['status'] for x in rows)),'recorded_hash_unlocated':sum(not r['recorded_bytes_retained'] for r in rows),'scope':'Recorded path/hash pairs only. Historical execution, scientific validity and receipt narrative claims are not re-certified.'}
    dump('checksum_summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
