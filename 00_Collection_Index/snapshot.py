"""Read-only source snapshot; deliberately never traverses The MIND or .git."""
import os, json, hashlib, subprocess, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / '00_Collection_Index'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snapshot():
    files=[]; dirs=[]
    for base, ds, fs in os.walk(ROOT,followlinks=False):
        rel=pathlib.Path(base).relative_to(ROOT)
        if rel==pathlib.Path('.'):
            ds[:]=[d for d in ds if d not in ('.git','The MIND','00_Collection_Index')]
        for d in ds:
            p=pathlib.Path(base)/d
            dirs.append({'original_path':p.relative_to(ROOT).as_posix(),'symlink':p.is_symlink()})
        for fn in fs:
            p=pathlib.Path(base)/fn; s=p.stat()
            sensitive=fn.startswith('.env') or fn.lower() in ('id_rsa','id_ed25519','credentials.json')
            files.append({'original_path':p.relative_to(ROOT).as_posix(),'size':s.st_size,'mtime_ns':s.st_mtime_ns,'sha256':None if sensitive else sha(p),'reason':'Sensitive store: not read' if sensitive else None})
    dump('baseline_sources.json',files); dump('baseline_directories.json',dirs)
    for name,args in [('git_status_before.txt',['status','--short']),('git_diff_stat_before.txt',['diff','--stat']),('git_head_before.txt',['rev-parse','HEAD'])]:
        r=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        (OUT/name).write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf-8')
    dump('snapshot_metadata.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(ROOT),'excluded_contents':['The MIND','.git'],'generated_after_baseline':'00_Collection_Index','files':len(files),'directories':len(dirs),'bytes':sum(x['size'] for x in files)})
    print(json.dumps({'files':len(files),'directories':len(dirs),'bytes':sum(x['size'] for x in files),'by_root':{r:sum(1 for f in files if f['original_path'].split('/')[0]==r) for r in sorted({f['original_path'].split('/')[0] for f in files})}},indent=2))
if __name__=='__main__': snapshot()
