import pathlib,json,hashlib,subprocess,sys
W=pathlib.Path(__file__).parent.resolve(); R=pathlib.Path(r'C:\Users\brian\Documents\Math Latex etc\Papers for Publication').resolve()
plan=json.loads((W/'partition_plan.json').read_text(encoding='utf-8')); rows=json.loads((W/'inventory_before.json').read_text(encoding='utf-8'))
def safe(rel):
 p=(R/rel).resolve(); assert p.is_relative_to(R) and p!=R and '.git' not in p.relative_to(R).parts,rel; return p
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8',stderr=subprocess.STDOUT)
assert git('rev-parse','HEAD').strip()==plan['starting_commit']
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip(),'Unexpected tracked changes'
for x in rows:assert sha(safe(x['path']))==x['sha256'],('Changed since inventory',x['path'])
for x in plan['moves']:assert not safe(x['new']).exists(),('Destination exists',x['new'])
# Reverify exact portfolio coverage against the retained tracked files immediately before mutation.
tracked=set(git('ls-files','-z').split('\0'))
for x in plan['deletes']:
 assert x['canonical_before'] in tracked and sha(safe(x['canonical_before']))==x['sha256']
log=[]
for x in plan['moves']:
 dst=safe(x['new']); dst.parent.mkdir(parents=True,exist_ok=True)
 git('mv','--',x['old'],x['new']); assert sha(dst)==x['sha256']; log.append(dict(action='git mv',**x))
tracked=set(git('ls-files','-z').split('\0'))
for x in plan['deletes']:
 assert x['canonical'] in tracked and sha(safe(x['canonical']))==x['sha256']
 assert sha(safe(x['old']))==x['sha256']
 if x['tracked']:git('rm','--',x['old'])
 else:safe(x['old']).unlink() # three explicitly authorized untracked exact ZIP duplicates only
 log.append(dict(action='git rm' if x['tracked'] else 'unlink verified untracked ZIP',**x))
# Remove only empty directories left by Git; no recursive filesystem deletion.
for d in sorted((p for p in R.rglob('*') if p.is_dir() and '.git' not in p.relative_to(R).parts),key=lambda p:len(p.parts),reverse=True):
 assert d.resolve().is_relative_to(R)
 if not any(d.iterdir()):d.rmdir()
assert not (R/'CM_LM_PUBLICATION_PORTFOLIO_20260921').exists()
(W/'mutation_receipt.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
print(json.dumps({'moves':len(plan['moves']),'exact_duplicate_files_removed':len(plan['deletes']),'portfolio_removed':True,'unique_file_bytes_modified':0},indent=2))
