from pathlib import Path
import json, hashlib, os, re, subprocess, zipfile, stat
ROOT=Path(__file__).resolve().parents[2]
MIND=ROOT/'The MIND'
AUD=MIND/'00_Index_and_Manifests'
def dump(name,obj):
    p=AUD/name
    if p.exists(): raise RuntimeError('Refusing overwrite: '+str(p))
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
records=[]; folders=[]; errors=[]
scopes=[MIND, ROOT/'Paper_U_Independent_Review_2026-09-29',ROOT/'Structured Factorization']
for scope in scopes:
    for base,dirs,files in os.walk(scope,followlinks=False):
        dirs[:]=[d for d in dirs if d not in ['00_Index_and_Manifests','.git','__pycache__']]
        folders.append(str(Path(base)))
        for n in files:
            p=Path(base)/n
            if p.is_symlink() or n.startswith('.env'):errors.append({'path':str(p),'reason':'sensitive name or symbolic link; not read'});continue
            try: records.append({'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':scope.name})
            except Exception as e:errors.append({'path':str(p),'reason':str(e)})
dump('original_inventory.json',{'files':records,'folders':folders,'errors':errors})
git=subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True)
dump('git_before.json',{'status':git.stdout,'stderr':git.stderr,'diff_stat':subprocess.run(['git','diff','--stat'],cwd=ROOT,capture_output=True,text=True).stdout})
texts=[]
for r in records:
    p=Path(r['source'])
    if p.suffix.lower() in ['.md','.json','.tex','.txt','.py','.ps1','.sha256'] and r['size']<2000000:
        texts.append((str(p),p.read_text(encoding='utf-8',errors='replace')))
for p in (AUD/'chat_evidence').glob('*.json'):texts.append((str(p),p.read_text(encoding='utf-8')))
names={}
for source,t in texts:
    for n in re.findall(r'(?<![\w])([A-Za-z0-9][A-Za-z0-9_.() -]*\.zip)\b',t,re.I):
        n=n.strip()
        if len(n)<180:names.setdefault(n,[]).append(source)
downloads=Path('C:/Users/brian/Downloads'); external=[]; missing=[]
for n,refs in sorted(names.items()):
    p=downloads/n
    try:
        if p.is_file():external.append({'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'named_download','referenced_by':list(dict.fromkeys(refs))})
        else:missing.append({'name':n,'checked':str(p),'referenced_by':list(dict.fromkeys(refs))})
    except Exception as e:missing.append({'name':n,'checked':str(p),'reason':str(e),'referenced_by':refs})
dump('named_download_discovery.json',{'available':external,'not_found_at_downloads':missing})
dump('discovery_texts.json',[{'source':p,'text':t} for p,t in texts])
print(json.dumps({'files':len(records),'folders':len(folders),'bytes':sum(r['size'] for r in records),'downloads':[(r['source'],r['size']) for r in external],'errors':errors},indent=2))
