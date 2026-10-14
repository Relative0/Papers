from pathlib import Path
import json,hashlib,os,re,shutil,zipfile,io,stat,collections,csv
A=Path(__file__).resolve().parent; M=A.parent;R=M.parent
F=R/'Paper_U_Fresh_Referee_2026-09-29'
U=M/'01_Papers/02_Hierarchical_Concepts_Paper_U'
EX=M/'90_Preserved_Sources/Extracted_Archives'
H=A/'Before_Fresh_Referee_Restore'
H.mkdir(exist_ok=False)
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False) if not isinstance(o,str) else o,encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():
  with src.open('rb') as i,dst.open('xb') as o:shutil.copyfileobj(i,o)
 if src.stat().st_size!=dst.stat().st_size or sha(src)!=sha(dst):raise ValueError('Copy mismatch: '+str(dst))
 return str(dst)
target_names=['source_manifest.json','source_manifest.csv','folder_manifest.json','archive_members_final.json','archive_occurrence_manifest.json','duplicate_groups.json','manuscript_version_catalog.json','final_content_inventory.json','final_verification.json','collection_manifest.json','unresolved_source_manifest.json','UNRESOLVED_AND_ACCESS.md','FINAL_VERIFICATION.md','audit_metadata_checksums.json']
for n in target_names:copy(A/n,H/n)
for p in [M/'README.md',U/'README.md']:copy(p,H/p.name.replace('README','ROOT_README' if p==M/'README.md' else 'PAPER_U_README'))
# Verify the original delivery and retain every file under the live sibling path.
manifest=load(F/'MANIFEST_SHA256.json')
if len(manifest)!=38:raise ValueError('Unexpected fresh manifest length')
for rel,h in manifest.items():
 p=F/rel
 if not p.is_file() or sha(p)!=h:raise ValueError('Fresh manifest mismatch: '+rel)
freshzip=F/'PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip'
with zipfile.ZipFile(freshzip) as z:
 if z.testzip() is not None:raise ValueError('Fresh ZIP CRC failure')
freshpdf=F/'revised_manuscript/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf'
rebuiltpdf=U/'Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf'
if sha(freshpdf)==sha(rebuiltpdf):raise ValueError('Expected distinct original/rebuilt PDF bytes')
sources=load(A/'source_manifest.json');existing={r['source'] for r in sources};new=[]
for base,dirs,files in os.walk(F,followlinks=False):
 dirs.sort()
 for n in sorted(files):
  p=Path(base)/n
  if p.is_symlink() or n.startswith('.env'):raise ValueError('Unexpected excluded source: '+str(p))
  rel=p.relative_to(F)
  dest=U/'Reviews/Original_Fresh_Referee'/rel
  organized=copy(p,dest)
  r={'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'Paper_U_Fresh_Referee_2026-09-29','organized_location':organized,'preserved_location':str(p),'disposition':'copied and SHA-256 verified; original sibling workspace retained','reason':None}
  if r['source'] in existing:raise ValueError('Fresh source already inventoried')
  new.append(r)
sources.extend(new)
for p in (F/'revised_manuscript').iterdir():
 if p.suffix in ['.tex','.pdf','.bib']:
  copy(p,U/'Current_Manuscript/v0.3_Original_Fresh_Referee'/p.name)
copy(freshzip,U/'Original_Packages'/freshzip.name)
save(A/'source_manifest.json',sources)
with (A/'source_manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
 cols=['source','size','sha256','scope','organized_location','preserved_location','disposition','reason'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(sources)
folders=load(A/'folder_manifest.json')
folders.append({'source':str(F),'organized_location':str(F),'disposition':'original fresh-referee workspace retained'})
folders.extend({'source':str(p),'organized_location':str(p),'disposition':'original fresh-referee workspace retained'} for p in F.rglob('*') if p.is_dir())
save(A/'folder_manifest.json',folders)
# Archive inventory: previous canonical member map is immutable evidence; add new
# verified ZIPs and recursively inspect any nested packages not yet represented.
members=load(A/'archive_members_final.json');canonical=collections.defaultdict(list)
for r in members:canonical[r['archive_sha256']].append(r)
newcanon=[];source_zips=[r for r in new if r['source'].lower().endswith('.zip')]
def visit(data,origin,depth=0):
 h=hashlib.sha256(data).hexdigest()
 if h in canonical:return h
 if depth>8:raise ValueError('Nested ZIP depth exceeded')
 dest=EX/h[:16]
 if dest.exists():raise ValueError('Unexpected existing extraction directory')
 dest.mkdir()
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  infos=z.infolist()
  if sum(i.file_size for i in infos)>1024**3:raise ValueError('Archive size exceeds bound')
  names=set()
  for i in infos:
   name=i.filename.replace('\\','/');parts=name.split('/')
   if name.startswith('/') or any(x=='..' or ':' in x for x in parts) or stat.S_ISLNK(i.external_attr>>16):raise ValueError('Unsafe archive path')
   key=name.rstrip('/').casefold()
   if key in names:raise ValueError('Archive path collision')
   names.add(key)
  for i in infos:
   out=dest/i.filename.replace('\\','/')
   if not out.resolve().is_relative_to(dest.resolve()):raise ValueError('Archive path escape')
   if i.is_dir():
    out.mkdir(parents=True,exist_ok=True)
    row={'archive':origin,'archive_sha256':h,'member':i.filename,'kind':'directory','staging':None,'organized_location':str(out),'extracted_location':str(out),'disposition':'preserved archive directory in safe extraction'}
   else:
    b=z.read(i);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('xb') as f:f.write(b)
    bh=hashlib.sha256(b).hexdigest();matches=[r['organized_location'] for r in sources if r['sha256']==bh]
    row={'archive':origin,'archive_sha256':h,'member':i.filename,'kind':'file','size':len(b),'sha256':bh,'staging':None,'organized_location':matches[0] if matches else str(out),'extracted_location':str(out),'disposition':'exact duplicate mapped to organized copy' if matches else 'archive-only content safely extracted and retained'}
    if i.filename.lower().endswith('.zip'):visit(b,origin+'!/'+i.filename,depth+1)
   canonical[h].append(row);newcanon.append(row)
 return h
for r in source_zips:visit(Path(r['source']).read_bytes(),r['source'])
members.extend(newcanon);save(A/'archive_members_final.json',members)
occ=load(A/'archive_occurrence_manifest.json')
def expand(h,origin,depth=0):
 if depth>12:raise ValueError('Archive occurrence depth exceeded')
 for m in canonical[h]:
  row={'source':origin+'!/'+m['member'],'archive':origin,'archive_sha256':h,'member':m['member'],'kind':m['kind'],'size':m.get('size'),'sha256':m.get('sha256'),'organized_location':m['organized_location'],'extracted_location':m['extracted_location'],'disposition':m['disposition']};occ.append(row)
  if m['kind']=='file' and m['member'].lower().endswith('.zip') and m['sha256'] in canonical:expand(m['sha256'],row['source'],depth+1)
for r in source_zips:expand(r['sha256'],r['source'])
save(A/'archive_occurrence_manifest.json',occ)
# Make the original fresh package the default while retaining the rebuilt PDF
# as a separate, hash-distinct reproduction.
u_readme=U/'README.md';t=u_readme.read_text(encoding='utf-8')
t=t.replace('Start with [the rebuilt v0.3 reading PDF](<Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf>) and [the recovered referee report](<Reviews/Rebuilt_Complete_Review/FINAL_REPORT.md>). Current subtitle: **Observation Quotients and Adaptive Symmetry**. Recommended delivery: [Paper_U_Complete_Rebuilt.zip](<Original_Packages/Paper_U_Complete_Rebuilt.zip>).','Start with [the original fresh-referee v0.3 PDF](<Current_Manuscript/v0.3_Original_Fresh_Referee/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf>) and [its referee report](<Reviews/Original_Fresh_Referee/00_FINAL_REFEREE_REPORT.md>). Current subtitle: **Observation Quotients and Adaptive Symmetry**. Recommended original delivery: [fresh-referee ZIP](<Original_Packages/PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip>). The [rebuilt replacement](<Original_Packages/Paper_U_Complete_Rebuilt.zip>) remains available for provenance.')
t=t.replace('The original `Paper_U_Fresh_Referee_2026-09-29` output folder and `PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip` were not found. The later chat explicitly recommends the rebuilt ZIP. Its README/receipt state that review documents were reconstructed from the task record, not restored byte-for-byte. Both the original review/transfer packages and this replacement are preserved. The collection is consequently not a complete recovery of every historical artifact.','The original `Paper_U_Fresh_Referee_2026-09-29` output folder and delivery ZIP became available on 30 September 2026 and were verified. Its 38-file manifest passed, and the ZIP passed CRC. Its revised TeX and bibliography match the rebuilt copy byte for byte; the PDF bytes differ. Both PDFs are retained. The rebuilt ZIP remains a clearly labeled reconstruction of material that had been unavailable during the earlier task; its historical claim that the fresh folder was absent was true when written, but no longer describes current access.')
t=t.replace('`Reviews` holds the initial review handoff, recovered complete review and supporting historical/priority/tree checks.','`Reviews` holds the original fresh referee, initial review handoff, rebuilt complete review and supporting historical/priority/tree checks.')
save(u_readme,t)
root=M/'README.md';t=root.read_text(encoding='utf-8')
t=t.replace('**Organization of accessible material is complete; recovery of all historical material is not.** The original fresh Paper U referee outputs are unavailable; their explicitly reconstructed replacement is retained. Earlier account chats are represented by transferred records, not directly accessible chat history.','**The original fresh Paper U referee outputs are now available and verified.** The rebuilt replacement remains preserved. Earlier account chats are represented by transferred records; their direct history is still unavailable.')
t=t.replace('[rebuilt clarified v0.3 PDF](<01_Papers/02_Hierarchical_Concepts_Paper_U/Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf>)','[original fresh-referee v0.3 PDF](<01_Papers/02_Hierarchical_Concepts_Paper_U/Current_Manuscript/v0.3_Original_Fresh_Referee/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf>)')
t=t.replace('Short synthesis/correction note; reconstructed review provenance','Short synthesis/correction note; original review recovered, rebuilt copy retained')
save(root,t)
# Reconcile new sources, archive members and current reading copies.
for r in new:
 for key in ['source','organized_location']:
  p=Path(r[key])
  if not p.is_file() or p.stat().st_size!=r['size'] or sha(p)!=r['sha256']:raise ValueError('Fresh source reconciliation failed: '+str(p))
for r in newcanon:
 p=Path(r['extracted_location'])
 if r['kind']=='file' and (not p.is_file() or p.stat().st_size!=r['size'] or sha(p)!=r['sha256']):raise ValueError('Archive member reconciliation failed')
unresolved=[r for r in load(A/'unresolved_source_manifest.json') if not (str(F) in r['source'])]
save(A/'unresolved_source_manifest.json',unresolved)
coll=load(A/'collection_manifest.json');coll['unresolved_sources']=unresolved;coll['historical_recovery_complete']=False;coll['fresh_referee_original_available']=True;coll['fresh_referee_zip_sha256']=sha(freshzip);save(A/'collection_manifest.json',coll)
access=A/'UNRESOLVED_AND_ACCESS.md';t=access.read_text(encoding='utf-8')
t=t.replace('## Historical recovery is incomplete\n- The chat **Ultrametric-REVIEW** referenced `Paper_U_Fresh_Referee_2026-09-29/00_FINAL_REFEREE_REPORT.md`, a revised-manuscript directory, and `PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip`. That sibling folder and the named ZIP were not present at the referenced locations or in named Downloads checks. The later `Paper_U_Complete_Rebuilt.zip` is available and verified. Its recovery README/receipt explicitly identify reconstructed reports; it is not a byte-for-byte recovery of the lost outputs.','## Historical access\n- The original `Paper_U_Fresh_Referee_2026-09-29` folder and `PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip` became available on 30 September 2026. All 38 listed file hashes and the ZIP CRC now verify. The rebuilt ZIP is retained as a separate reconstruction, and its old README describes the earlier absence rather than current access.')
save(access,t)
summary=A/'FINAL_VERIFICATION.md';t=summary.read_text(encoding='utf-8')
t=t.replace('**PASS for accessible material. Historical recovery remains incomplete.**','**PASS for accessible material, including the newly available original fresh Paper U referee package.**')
t=t.replace('The original Paper U fresh-review output is unavailable. Its recommended rebuilt replacement is verified but contains clearly labeled reconstructed reports. Prior-account chat access is unavailable directly. Read `UNRESOLVED_AND_ACCESS.md`; do not describe this as complete historical recovery.','The original Paper U fresh-review folder and ZIP are now available and verified. The separately rebuilt replacement remains preserved, including its reconstruction caveat. Direct access to prior-account chats remains unavailable. Read `UNRESOLVED_AND_ACCESS.md`; source-package recovery and chat-history access are separate issues.')
save(summary,t)
ver=load(A/'final_verification.json');ver['status']='PASS';ver['all_source_paths']=len(sources);ver['source_scopes']=dict(collections.Counter(r['scope'] for r in sources));ver['canonical_archive_members']=len(members);ver['archive_occurrence_rows']=len(occ);ver['fresh_referee_manifest_files_verified']=len(manifest);ver['fresh_referee_zip_sha256']=sha(freshzip);ver['fresh_referee_zip_crc']='PASS';ver['fresh_referee_original_pdf_sha256']=sha(freshpdf);ver['rebuilt_pdf_sha256']=sha(rebuiltpdf);ver['missing_historical_artifacts']=['Earlier account chats unavailable directly; transferred records retained.'];ver['recovery_update']='Original Paper U fresh-referee folder and ZIP discovered and verified 30 September 2026.';save(A/'final_verification.json',ver)
# Rebuild duplicate map from all original and archive occurrences. Preserve old
# groups in the snapshot for auditability.
groups=collections.defaultdict(lambda:{'original_sources':[],'archive_occurrences':[],'current_locations':[]})
for r in sources:groups[r['sha256']]['original_sources'].append({'path':r['source'],'retained_at':r['preserved_location'],'organized_at':r['organized_location']})
for r in occ:
 if r['kind']=='file':groups[r['sha256']]['archive_occurrences'].append(r['source'])
final=[]
for p in M.rglob('*'):
 if p.is_file() and not p.is_relative_to(A):
  h=sha(p);final.append({'path':str(p),'size':p.stat().st_size,'sha256':h});groups[h]['current_locations'].append(str(p))
save(A/'final_content_inventory.json',final)
dups=[dict(sha256=h,**v) for h,v in groups.items() if len(v['original_sources'])+len(v['archive_occurrences'])>1 or len(v['current_locations'])>1];save(A/'duplicate_groups.json',dups)
catalog=[]
for h,v in groups.items():
 loc=[p for p in v['current_locations'] if p.endswith('.tex') and any(t in Path(p).name for t in ['Observation_Refinement_Descent','Paper_U_Resolution','THEOREM_NOTE_DRAFT'])]
 if loc:catalog.append({'sha256':h,'locations':loc,'original_sources':v['original_sources'],'archive_occurrences':v['archive_occurrences']})
save(A/'manuscript_version_catalog.json',catalog)
ver['final_content_files']=len(final);ver['duplicate_hash_groups']=len(dups);ver['unique_manuscript_tex_hashes']=len(catalog);save(A/'final_verification.json',ver)
tree=['The MIND/']
for base,dirs,files in os.walk(M):
 dirs.sort();rel=Path(base).relative_to(M)
 if str(rel)!='.':tree.append('  '*len(rel.parts)+rel.name+f'/  ({len(files)} files)')
save(A/'FOLDER_TREE.txt','\n'.join(tree)+'\n')
print(json.dumps({'fresh_sources':len(new),'fresh_manifest_checked':len(manifest),'fresh_zips':len(source_zips),'new_canonical_members':len(newcanon),'archive_occurrences':len(occ),'all_source_paths':len(sources),'original_pdf_matches_rebuilt':False,'remaining_unresolved':unresolved},indent=2))
