from pathlib import Path
exec((Path(__file__).parent/'discover.py').read_text().split('records=[];')[0])
import io, collections
inv=json.loads((AUD/'original_inventory.json').read_text())
# Supplement the initial scan with bytecode/cache files; every original file is retained.
extra=[]
seen={x['source'] for x in inv['files']}
for scope in [MIND,ROOT/'Paper_U_Independent_Review_2026-09-29',ROOT/'Structured Factorization',ROOT/'General ProLT Observation Refinement (Research Direction)']:
    for base,dirs,files in os.walk(scope,followlinks=False):
        dirs[:]=[d for d in dirs if d not in ['00_Index_and_Manifests','.git']]
        for n in files:
            p=Path(base)/n
            if str(p) not in seen and not n.startswith('.env'):
                extra.append({'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':scope.name})
if not (AUD/'supplemental_inventory.json').exists():dump('supplemental_inventory.json',extra)
sources=inv['files']+extra+json.loads((AUD/'named_download_discovery.json').read_text())['available']
attachments=[]
for p in (AUD/'chat_evidence').glob('*.json'):
    t=p.read_text(encoding='utf-8'); obj=json.loads(t)
    text=json.dumps(obj,ensure_ascii=False).replace('\\\\','\\')
    for hit in re.findall(r'C:[/\\]Users[/\\]brian[/\\]\.codex[/\\]attachments[/\\][a-z0-9-]+[/\\][^\n"<>]+?\.(?:txt|zip|pdf)',text,re.I):
        q=Path(hit)
        if any(x['source']==str(q) for x in attachments):continue
        if q.is_file():attachments.append({'source':str(q),'size':q.stat().st_size,'sha256':sha(q),'scope':'chat_attachment'})
        else:attachments.append({'source':str(q),'reason':'referenced chat attachment unavailable'})
dump('attachment_inventory.json',attachments)
sources += [r for r in attachments if 'sha256' in r]
archives=[]; members=[]; unique={}; texts=[]
stage=AUD/'staging';stage.mkdir(exist_ok=False)
def visit(data,origin,depth=0):
    h=hashlib.sha256(data).hexdigest()
    if h in unique:
        archives.append({'source':origin,'sha256':h,'same_archive_as':unique[h]['source'],'staging':unique[h]['staging'],'status':'identical archive bytes; members mapped through canonical archive'})
        return
    dest=stage/h[:16];dest.mkdir()
    rec={'source':origin,'sha256':h,'staging':str(dest),'status':'pending'};unique[h]=rec;archives.append(rec)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos=z.infolist();keys=set()
            if sum(i.file_size for i in infos)>1024**3:raise ValueError('expanded size exceeds 1 GiB review limit')
            for i in infos:
                name=i.filename.replace('\\','/');parts=name.split('/')
                if name.startswith('/') or any(x in ('..',) or ':' in x for x in parts) or stat.S_ISLNK(i.external_attr>>16):raise ValueError('unsafe member '+name)
                k=name.rstrip('/').casefold()
                if k in keys:raise ValueError('duplicate/case-colliding archive path '+name)
                keys.add(k)
            for i in infos:
                out=dest/i.filename.replace('\\','/')
                if not out.resolve().is_relative_to(dest.resolve()):raise ValueError('path escape')
                if i.is_dir():out.mkdir(parents=True,exist_ok=True);members.append({'archive':origin,'archive_sha256':h,'member':i.filename,'kind':'directory','staging':str(out)});continue
                b=z.read(i);out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('xb') as f:f.write(b)
                mh=hashlib.sha256(b).hexdigest()
                members.append({'archive':origin,'archive_sha256':h,'member':i.filename,'kind':'file','size':len(b),'sha256':mh,'staging':str(out)})
                if out.suffix.lower() in ['.md','.tex','.json','.sha256','.txt'] and len(b)<1000000:
                    texts.append({'source':origin+'!/'+i.filename,'staging':str(out),'text':b.decode('utf-8',errors='replace')})
                if out.suffix.lower()=='.zip':
                    if depth>=8:raise ValueError('nested depth limit')
                    visit(b,origin+'!/'+i.filename,depth+1)
            rec.update(status='safe extraction and CRC verified',files=sum(not i.is_dir() for i in infos),bytes=sum(i.file_size for i in infos))
    except Exception as e:rec.update(status='unresolved',reason=str(e))
for r in sources:
    if Path(r['source']).suffix.lower()=='.zip':visit(Path(r['source']).read_bytes(),r['source'])
dump('archive_inventory.json',{'archives':archives,'members':members})
dump('archive_texts.json',texts)
print(json.dumps({'supplemental_files':len(extra),'attachments':attachments,'archives':len(archives),'unique_archives':len(unique),'members':len(members),'issues':[r for r in archives if r['status']=='unresolved']},indent=2))
