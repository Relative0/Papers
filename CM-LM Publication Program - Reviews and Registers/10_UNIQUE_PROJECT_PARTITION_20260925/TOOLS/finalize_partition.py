import pathlib,json,hashlib,csv,io,re,subprocess,sys,urllib.parse,itertools,collections,zipfile
from partition_data import *
W=pathlib.Path(__file__).parent.resolve(); R=pathlib.Path(r'C:\Users\brian\Documents\Math Latex etc\Papers for Publication').resolve(); S=W/'staged_docs'
def load(n):return json.loads((W/(n+'.json')).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(rel):
 p=(R/rel).resolve();assert p.is_relative_to(R) and p!=R and '.git' not in p.relative_to(R).parts;return p
def put(rel,t):
 p=safe(rel);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def jput(rel,o):put(rel,json.dumps(o,indent=2,ensure_ascii=False)+'\n')
plan=load('partition_plan'); rows=load('inventory_before'); deleted={x['old']:x for x in plan['deletes']}
def canonical(s):return plan['mapping'].get(s) or deleted[s]['canonical']
mode=sys.argv[1] if len(sys.argv)>1 else 'preflight'
staged=[p for p in S.rglob('*') if p.is_file()]
overlay={p.relative_to(S).as_posix() for p in staged}|{p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts}
overlay|={p['folder']+'/SOURCE_MANIFEST_SHA256.csv' for p in P}
link_errors=[]; checked_links=0
for f in staged:
 if f.suffix!='.md' or '/TOOLS/' in f.as_posix():continue
 # Original extracted reviews may retain historic external/local links; only generated navigation is checked.
 if 'FRESH_ADVERSARIAL_REVIEW_20260924' in f.as_posix() or '/SOURCE_PACKAGE/' in f.as_posix():continue
 text=f.read_text(encoding='utf-8'); rel=f.relative_to(S)
 for match in re.finditer(r'\[[^\]\n]+\]\(([^)]+)\)',text):
  href=urllib.parse.unquote(match.group(1).split('#')[0])
  if not href or re.match(r'^[a-z]+:',href):continue
  path=(R/rel.parent/href).resolve();checked_links+=1
  if not path.is_relative_to(R):link_errors.append((str(rel),href,'outside repository'));continue
  target=path.relative_to(R).as_posix()
  if target not in overlay and not any(x.startswith(target+'/') for x in overlay):link_errors.append((str(rel),href,'missing'))
assert not link_errors,link_errors

before_paths={x['path'] for x in rows}; after_paths=overlay
dependencies=[]
for x in rows:
 if not x['path'].endswith('.tex'):continue
 old=pathlib.PurePosixPath(x['path']); new=pathlib.PurePosixPath(canonical(x['path'])); text=safe(str(new)).read_text(encoding='utf-8-sig',errors='replace')
 generated=set(re.findall(r'\\begin\{filecontents\*?\}\{([^}]+)\}',text))
 for m in re.finditer(r'\\(input|include|includegraphics|bibliography|addbibresource)(?:\[[^\]]*\])?\{([^}]+)\}',text):
  cmd,arg=m.groups()
  if '\\' in arg or '#' in arg:continue
  for name in arg.split(','):
   candidates=[name] if pathlib.PurePosixPath(name).suffix else [name+ext for ext in (['.png','.pdf','.jpg','.eps'] if cmd=='includegraphics' else ['.bib'] if cmd in {'bibliography','addbibresource'} else ['.tex'])]
   def resolved(parent,files):
    for q in candidates:
     p=(R/str(parent)/q).resolve()
     if p.is_relative_to(R) and p.relative_to(R).as_posix() in files:return True
    return name in generated or any(q in generated for q in candidates)
   b=resolved(old.parent,before_paths);a=resolved(new.parent,after_paths)
   dependencies.append(dict(original_source=x['path'],current_source=str(new),command=cmd,argument=name,before_resolved=b,after_resolved=a,generated_by_filecontents=name in generated or any(q in generated for q in candidates)))
new_missing=[x for x in dependencies if x['before_resolved'] and not x['after_resolved']]
assert not new_missing, new_missing
if mode=='preflight':
 print(json.dumps({'generated_links_checked':checked_links,'link_errors':link_errors,'dependency_references':len(dependencies),'newly_broken_dependencies':new_missing,'existing_unresolved_dependency_instances':sum(not x['after_resolved'] for x in dependencies),'staged_files':len(staged)},indent=2));sys.exit()
assert mode=='apply'
for f in staged:
 dst=safe(f.relative_to(S).as_posix());dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():assert dst.read_bytes()==f.read_bytes(),('Refusing to overwrite unrelated file',str(dst))
 else:dst.write_bytes(f.read_bytes())
jput(EVID+'/source_dependency_check.json',dependencies)
preservation=[]
for x in rows:
 dest=canonical(x['path']);h=sha(safe(dest));assert h==x['sha256'],x['path'];preservation.append(dict(original=x['path'],retained=dest,sha256=h,bytes=x['bytes'],action='removed exact duplicate' if x['path'] in deleted else 'git mv' if dest!=x['path'] else 'retained in place'))
jput(EVID+'/complete_preservation_map.json',preservation)
assert len({x['sha256'] for x in preservation})==597
assert len(preservation)==1086
actual_folders={p.name for p in R.iterdir() if p.is_dir() and p.name!='.git'};assert actual_folders=={p['folder'] for p in P}
for p in P:
 for rel in ['README_FIRST.md','CLAIMS_AND_UNIQUENESS.md',p['source'],'HISTORY/README.md','REVIEWS_AND_RECOMMENDATIONS/README.md','REPRODUCIBILITY/README.md']:assert safe(p['folder']+'/'+rel).is_file(),(p['id'],rel)

# Re-read final documents, verify archive CRC, and repeat the lexical overlap screen on preserved content.
pr={x['sha256']:x for x in load('profiles')}; documents={}; archive_checks=[]
for x in sorted(rows,key=lambda x:('/HISTORY/' in canonical(x['path']),len(canonical(x['path'])))):
 final=canonical(x['path']);h=x['sha256']
 if h not in documents and pathlib.PurePosixPath(final).suffix in {'.md','.tex','.pdf'} and h in pr:documents[h]=final
seen_arch=set()
for x in rows:
 if not x['path'].endswith('.zip') or x['sha256'] in seen_arch:continue
 seen_arch.add(x['sha256']);final=canonical(x['path'])
 with zipfile.ZipFile(safe(final)) as z:
  bad=z.testzip();assert bad is None;archive_checks.append(dict(path=final,sha256=x['sha256'],members=len([m for m in z.infolist() if not m.is_dir()]),crc='PASS'))
  for m in z.infolist():
   if m.is_dir() or pathlib.PurePosixPath(m.filename).suffix.lower() not in {'.md','.tex','.pdf'}:continue
   b=z.read(m);h=hashlib.sha256(b).hexdigest()
   if h not in documents and h in pr:documents[h]=final+'!/'+m.filename
docs=[]
for h,path in documents.items():
 if '!/' not in path and not path.endswith('.pdf'):t=safe(path).read_text(encoding='utf-8-sig',errors='replace')
 else:t=(W/'text'/(h+'.txt')).read_text(encoding='utf-8') # byte identity/CRC checked above; identical extraction input
 words=re.findall(r'[a-z0-9]+',re.sub(r'\\[a-zA-Z]+\*?',' ',t).lower()); shingles={hashlib.blake2b(' '.join(words[i:i+5]).encode(),digest_size=8).digest() for i in range(len(words)-4)}
 if len(shingles)>100:docs.append((h,path,shingles))
hits=[]
for (ha,a,sa),(hb,b,sb) in itertools.combinations(docs,2):
 if a.split('/')[0]==b.split('/')[0]:continue
 n=len(sa&sb);con=n/min(len(sa),len(sb))
 if n>=100 and con>=.30:hits.append(dict(a=a,b=b,a_sha256=ha,b_sha256=hb,containment=round(con,4),jaccard=round(n/len(sa|sb),4),shared_5grams=n))
jput(EVID+'/semantic_screen_after.json',dict(docs=len(docs),hits=hits,method='Final paths and re-read text; PDFs and ZIP text reuse extraction only after final byte identity and archive CRC verification; threshold 100 five-grams / containment .30. No semantic deletion.'))
jput(EVID+'/archive_crc_checks.json',archive_checks)

# Enrich every pair before the final content inventory hashes it.
matrix=load('pairwise_surviving')
for item in matrix:
 for key in ['a','b']:
  p=BY[item[key]];path=p['folder']+'/'+p['source'];item[key+'_source']=path;item[key+'_source_sha256']=sha(safe(path));item[key+'_section_anchors']=p['refs']
jput(EVID+'/pairwise_surviving.json',matrix)
finalrows=[]
for f in sorted(R.rglob('*')):
 if not f.is_file() or '.git' in f.relative_to(R).parts:continue
 rel=f.relative_to(R).as_posix()
 if f.name=='SOURCE_MANIFEST_SHA256.csv' and len(f.relative_to(R).parts)==2:continue
 if rel in {'PARTITION_VERIFICATION_RECEIPT.json',EVID+'/content_inventory_after.json',EVID+'/exact_groups_after.json'}:continue
 finalrows.append(dict(path=rel,bytes=f.stat().st_size,sha256=sha(f)))
g=collections.defaultdict(list)
for x in finalrows:g[x['sha256']].append(x)
jput(EVID+'/content_inventory_after.json',dict(scope='All repository content before this inventory, exact-groups index and top-level manifest generation. Those generated bookkeeping files are covered by final top-level manifests and root receipt. .git excluded.',files=finalrows))
jput(EVID+'/exact_groups_after.json',[dict(sha256=h,instances=v,policy='Preserved original self-contained/frozen source/review/evidence package or generated navigation/report copy; see claim-owner matrix and README duplication policies.') for h,v in g.items() if len(v)>1])
manifests=[]
for p in P:
 folder=safe(p['folder']);out=io.StringIO(newline='');writer=csv.writer(out,lineterminator='\n');writer.writerow(['RelativePath','SHA256','Bytes'])
 for f in sorted(folder.rglob('*')):
  if f.is_file() and f!=folder/'SOURCE_MANIFEST_SHA256.csv':writer.writerow([f.relative_to(folder).as_posix(),sha(f),f.stat().st_size])
 m=folder/'SOURCE_MANIFEST_SHA256.csv';m.write_text(out.getvalue(),encoding='utf-8',newline='');count=0
 for e in csv.DictReader(io.StringIO(m.read_text(encoding='utf-8'))):assert sha(folder/e['RelativePath'])==e['SHA256'];count+=1
 manifests.append(dict(path=m.relative_to(R).as_posix(),entries=count,sha256=sha(m)))
assert (R/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md').read_bytes()==(R/REG/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md').read_bytes()
receipt=dict(starting_commit=plan['starting_commit'],before_files=1086,before_distinct_sha256=597,all_1086_original_instances_have_byte_identical_retained_destination=True,all_597_original_byte_streams_preserved=True,portfolio_verified_before_removal=353,portfolio_removed=not (R/PORT).exists(),moves=len(plan['moves']),exact_duplicate_removals=len(plan['deletes']),removed_bytes=sum(x['bytes'] for x in plan['deletes']),surviving_top_level_projects=len(P),project_structure='PASS',generated_links_checked=checked_links,newly_broken_static_dependencies=new_missing,preexisting_unresolved_dependency_instances=sum(not x['after_resolved'] for x in dependencies),semantic_rescreen_documents=len(docs),semantic_rescreen_hits=len(hits),archive_crc_checks=archive_checks,tests=[dict(name=x['name'],exit_code=x['exit_code'],adaptation=x['adaptation']) for x in load('verification_runs')],report_sha256=sha(R/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md'),manifests=manifests,git_status='Changes prepared; staged diff review and local commit follow. Final commit and post-commit clean status are recorded in the external completion receipt. No push.',manifest_scope='Every file under each project except that project manifest itself; includes historical manifests. Root receipt is outside manifests to avoid cyclic hashes.')
jput('PARTITION_VERIFICATION_RECEIPT.json',receipt)
(W/'final_verification.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'manifests','archive_crc_checks'}},indent=2))
