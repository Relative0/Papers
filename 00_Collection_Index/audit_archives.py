"""Inventory immutable archives by content hash, including nested ZIPs, without extraction."""
from snapshot import ROOT,OUT,sha,dump
import pathlib,zipfile,hashlib,io,json,re,os,stat,collections
def safe_member(name):
    s=name.replace('\\','/'); p=pathlib.PurePosixPath(s)
    return not (s.startswith('/') or '..' in p.parts or any(':' in x for x in p.parts))
def main():
    baseline=json.loads((OUT/'baseline_sources.json').read_text())
    chats=[]
    for cp in OUT.glob('chat_evidence*.json'):chats.extend(json.loads(cp.read_text(encoding='utf-8')))
    txt=json.dumps(chats,ensure_ascii=False).replace('\\\\','\\')
    names=set(re.findall(r'[A-Za-z0-9][A-Za-z0-9_ ()+.-]*\.zip',txt,re.I))
    if (OUT/'checksum_claims.json').exists():
        for row in json.loads((OUT/'checksum_claims.json').read_text(encoding='utf-8')):
            m=re.search(r'([^/\\]+\.zip)',row['recorded_path'],re.I)
            if m:names.add(m[1])
    downloads=pathlib.Path('C:/Users/brian/Downloads')
    external=[]
    # Match only specifically named packages in research records; do not sweep Downloads.
    evidence_texts=[]
    for f in baseline:
        p=ROOT/f['original_path']
        if p.suffix.lower() in ('.md','.txt','.json','.csv') and f['size']<8_000_000 and f['sha256']:
            evidence_texts.append((f['original_path'],p.read_text(encoding='utf-8-sig',errors='replace')))
    cited_by={}
    for p in downloads.glob('*.zip'):
        refs=[name for name,t in evidence_texts if p.name in t]
        if p.name in names or refs:
            names.add(p.name)
            external.append({'original_path':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'specifically named in inspected chats or workspace records','cited_by':refs[:20]})
    # Explicit current evidence mentioned in the CM convergence chat, outside Downloads.
    for name in ['CM_Structural_Computation_C1-C4_T3_Phase2_2026-09-28.zip','CM_Convergence_Audit_and_Computation_Preparation_2026-09-28.zip']:
        p=pathlib.Path('C:/Users/brian/Documents/CM_Computation')/name
        if p.exists():external.append({'original_path':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'exact package referenced by CM convergence chat'})
    dump('external_sources.json',external)
    dump('chat_referenced_zip_names.json',sorted(names))
    archives={}; errors=[]
    def scan(source,h,location,depth=0):
        if h in archives:
            if location not in archives[h]['locations']:archives[h]['locations'].append(location)
            return
        record={'sha256':h,'locations':[location],'members':[],'crc_status':'PASS'};archives[h]=record
        try:
            with zipfile.ZipFile(source) as z:
                for index,info in enumerate(z.infolist()):
                    m={'index':index,'path':info.filename,'size':info.file_size,'compressed_size':info.compress_size,'crc32':f'{info.CRC:08x}','directory':info.is_dir(),'safe_path':safe_member(info.filename),'symlink':stat.S_ISLNK(info.external_attr>>16)}
                    if not info.is_dir():
                        if info.file_size>1024**3: m['unresolved']='Single member exceeds 1 GiB inspection cap'
                        else:
                            try:
                                data=z.read(info); mh=hashlib.sha256(data).hexdigest();m['sha256']=mh
                                if info.filename.lower().endswith('.zip'):
                                    m['nested_archive_sha256']=mh
                                    if depth>=12:m['unresolved']='Nested archive depth exceeds 12'
                                    else:scan(io.BytesIO(data),mh,{'parent_archive_sha256':h,'member_index':index,'member':info.filename},depth+1)
                            except Exception as e:m['unresolved']=str(e);record['crc_status']='FAIL'
                    record['members'].append(m)
        except Exception as e:record['error']=str(e);record['crc_status']='FAIL';errors.append({'location':location,'error':str(e)})
    for f in baseline+external:
        if f['original_path'].lower().endswith('.zip'):
            p=pathlib.Path(f['original_path']);p=p if p.is_absolute() else ROOT/p
            scan(p,f['sha256'],{'source_path':f['original_path']})
    dump('archive_catalog.json',archives)
    summary={'unique_zip_streams':len(archives),'direct_zip_paths':sum(f['original_path'].lower().endswith('.zip') for f in baseline+external),'members_per_unique_archive':sum(len(a['members']) for a in archives.values()),'external_packages':len(external),'errors':errors,'bad_archives':[h for h,a in archives.items() if a['crc_status']!='PASS']}
    dump('archive_audit_summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
