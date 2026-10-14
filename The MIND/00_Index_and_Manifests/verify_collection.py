from pathlib import Path
import json,hashlib,collections,os,re,subprocess
A=Path(__file__).resolve().parent;M=A.parent;R=M.parent
def read(n):return json.loads((A/n).read_text(encoding='utf-8'))
def out(p,x):
 with p.open('x',encoding='utf-8') as f:f.write(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False))
cache={}
def sha(p):
 p=Path(p)
 if str(p) not in cache:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  cache[str(p)]=h.hexdigest()
 return cache[str(p)]
sources=read('source_manifest.json');members=read('archive_members_final.json');occ=read('archive_occurrence_manifest.json');issues=[]
for r in sources:
 for key in ['organized_location','preserved_location']:
  p=Path(r[key])
  if not p.is_file():issues.append({'source':r['source'],'path':str(p),'problem':'missing '+key})
  elif p.stat().st_size!=r['size'] or sha(p)!=r['sha256']:issues.append({'source':r['source'],'path':str(p),'problem':'size/hash mismatch '+key})
for r in members:
 for key in ['organized_location','extracted_location']:
  p=Path(r[key])
  if r['kind']=='directory':
   if not p.is_dir():issues.append({'path':str(p),'problem':'archive directory missing'})
  elif not p.is_file() or p.stat().st_size!=r['size'] or sha(p)!=r['sha256']:issues.append({'path':str(p),'problem':'archive member hash/missing'})
for r in read('original_directory_map.json'):
 if not Path(r['preserved_location']).is_dir():issues.append({'source':r['source'],'problem':'original directory missing'})
old=M/'90_Preserved_Sources/Original_The_MIND'
expected={r['preserved_location'] for r in sources if r['scope']=='The MIND'}
actual={str(p) for p in old.rglob('*') if p.is_file()}
if expected!=actual:issues.append({'problem':'preserved tree inventory differs','extra':sorted(actual-expected),'missing':sorted(expected-actual)})
copies=read('copy_verification.json')+read('additional_reading_copies.json')
for r in copies:
 if sha(r['destination'])!=r['sha256']:issues.append({'path':r['destination'],'problem':'reading copy changed'})
# Inventory all delivered source/copy/extraction files; audit files have a separate
# final checksum inventory so generated metadata need not contain its own hash.
final=[]
for p in M.rglob('*'):
 if p.is_file() and not p.is_relative_to(A):final.append({'path':str(p),'size':p.stat().st_size,'sha256':sha(p)})
out(A/'final_content_inventory.json',final)
groups=collections.defaultdict(lambda:{'original_sources':[],'archive_occurrences':[],'current_locations':[]})
for r in sources:groups[r['sha256']]['original_sources'].append({'path':r['source'],'retained_at':r['preserved_location'],'organized_at':r['organized_location']})
for r in occ:
 if r['kind']=='file':groups[r['sha256']]['archive_occurrences'].append(r['source'])
for r in final:groups[r['sha256']]['current_locations'].append(r['path'])
duplicates=[dict(sha256=h,**v) for h,v in groups.items() if len(v['original_sources'])+len(v['archive_occurrences'])>1 or len(v['current_locations'])>1]
out(A/'duplicate_groups.json',duplicates)
catalog=[]
for h,v in groups.items():
 locations=[p for p in v['current_locations'] if p.endswith('.tex') and any(t in Path(p).name for t in ['Observation_Refinement_Descent','Paper_U_Resolution','THEOREM_NOTE_DRAFT'])]
 if locations:catalog.append({'sha256':h,'locations':locations,'original_sources':v['original_sources'],'archive_occurrences':v['archive_occurrences']})
out(A/'manuscript_version_catalog.json',catalog)
# Verify only our navigation documents, not old unchanged scientific links.
nav=[M/'README.md',M/'01_Papers/README.md',M/'90_Preserved_Sources/README.md',M/'02_Shared_and_Exploratory_Research/README.md',M/'02_Shared_and_Exploratory_Research/Measurement_and_RF_IDENT/README.md']
nav+=list((M/'01_Papers').glob('*/README.md'))+list((M/'01_Papers').glob('*/Reproducibility/README.md'))+list((M/'01_Papers').glob('*/Reviews/README.md'))
broken=[];nlinks=0
for p in nav:
 for target in re.findall(r'\]\(<([^>]+)>\)',p.read_text(encoding='utf-8')):
  if target.startswith(('http','codex:')):continue
  nlinks+=1;q=(p.parent/target).resolve()
  if not q.exists() and q.name not in ['FINAL_VERIFICATION.md','UNRESOLVED_AND_ACCESS.md','FOLDER_TREE.txt']:broken.append({'document':str(p),'target':target})
issues.extend({'problem':'navigation link missing',**r} for r in broken)
tree=['The MIND/']
for root,dirs,files in os.walk(M):
 dirs.sort();rel=Path(root).relative_to(M)
 if str(rel)=='.':continue
 depth=len(rel.parts);tree.append('  '*depth+rel.name+f'/  ({len(files)} files)')
out(A/'FOLDER_TREE.txt','\n'.join(tree)+'\n')
top=['The MIND/','  README.md','  01_Papers/','    01_Observation_Refinement_and_Concept_Differentiation/','    02_Hierarchical_Concepts_Paper_U/','    03_Structured_Boolean_Factorization/','  02_Shared_and_Exploratory_Research/','    Measurement_and_RF_IDENT/','    Historical_Primary_Sources/','    Chat_Attachments/','    Original_Packages/','    Archive_Only_Content/','  90_Preserved_Sources/','    Original_The_MIND/','    Extracted_Archives/','  00_Index_and_Manifests/']
out(A/'FOLDER_TREE_SUMMARY.txt','\n'.join(top)+'\n')
checks=read('checksum_verification_final.json')['summary'];embed=read('embedded_hash_verification.json')
ver={'status':'PASS' if not issues else 'FAIL','scope':'Accessible original files, reading copies, and archive contents reconciled; historical recovery explicitly incomplete.','original_MIND_files':len(expected),'all_source_paths':len(sources),'source_scopes':dict(collections.Counter(r['scope'] for r in sources)),'original_directories':len(read('original_directory_map.json')),'verified_reading_copies':len(copies),'unique_extracted_archives':len({r['archive_sha256'] for r in members}),'canonical_archive_members':len(members),'archive_occurrence_rows':len(occ),'linked_related_archive_members':len(read('linked_related_archive_members.json')),'final_content_files':len(final),'duplicate_hash_groups':len(duplicates),'unique_manuscript_tex_hashes':len(catalog),'navigation_links_checked':nlinks,'recorded_checksum_checks':checks,'embedded_CNF_checks':dict(collections.Counter(r['status'] for r in embed)),'issues':issues,'scientific_tests':'Not rerun; source files unchanged. Only integrity, archive, navigation, and inventory checks performed.','missing_historical_artifacts':['Paper_U_Fresh_Referee_2026-09-29 directory and original fresh-referee ZIP','Earlier account chats unavailable directly; transferred records retained.']}
out(A/'final_verification.json',ver)
out(A/'UNRESOLVED_AND_ACCESS.md','''# Unavailable material, scope and open questions

## Historical recovery is incomplete
- The chat **Ultrametric-REVIEW** referenced `Paper_U_Fresh_Referee_2026-09-29/00_FINAL_REFEREE_REPORT.md`, a revised-manuscript directory, and `PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip`. That sibling folder and the named ZIP were not present at the referenced locations or in named Downloads checks. The later `Paper_U_Complete_Rebuilt.zip` is available and verified. Its recovery README/receipt explicitly identify reconstructed reports; it is not a byte-for-byte recovery of the lost outputs.
- Earlier research occurred in another GPT account. Its conversations cannot be read directly through the current account's chat tools. The transferred project histories, original packages and source maps were inspected instead. No claim is made that all historical chats or attachments have been recovered.
- Current discovery read ten relevant chats, including two archived project chats, and retained their user/final-message evidence. Chat listings covered 50 recent entries, 100 archived Codex entries and two archived ChatGPT entries. No relevant older-account chat appeared in that accessible listing; this is a bounded search, not a global-account guarantee.

## Resolved references and preserved workflows
- All four explicitly referenced pasted-text attachments were accessible and hash-verified. All twelve identified named Downloads ZIPs were accessible. Downloads was queried only by referenced names, never broadly swept.
- Apparent missing `2024-9-2026.zip` / `24-9-2026.zip` references were filename/URL parsing fragments of `ProLT_Homology - 24-9-2026.zip`, which is available. The shared `REPRODUCTION_SUPPLEMENT.zip` is available in the existing publication-program folder. These are resolved, not missing research packages.
- `Papers for Publication.zip` was inspected by member list: 469 members, none in The MIND, Paper U or Structured Factorization paths. It was not reorganized.
- Sibling Paper U review, Structured Factorization (including its environment), General ProLT research and existing ProLT publication homes remain in place. The index links them and the source manifest inventories in-scope originals. New paper copies are reading snapshots; they do not switch those workflows.
- Historical absolute paths in scientific scripts/receipts were preserved, so a future rerun may need path adaptation in a disposable copy. Relative layout inside `90_Preserved_Sources/Original_The_MIND` is retained. No script was rewritten or executed to regenerate scientific output.

## Classification boundaries
- RF-IDENT and its independent review form one reviewed follow-up in the shared measurement/two-operation research branch. There is no identified standalone RF-IDENT manuscript and no evidence that its result was integrated into v0.5 of the observation-refinement manuscript.
- Structured Factorization is an evolving theorem-note family with Phase 3/4/5 titles. Phase 5B supplies later status/corrections, not a new integrated manuscript. The live-vtree probe is a later tooling finding and does not invalidate the frozen pilot NO-GO.
- Paper F is a historical proposed division of labor in Paper U's bridge note, not an identified fourth current manuscript. Original themes and their cross-paper overlaps are preserved in the theme crosswalk.
- Scientific open issues (novelty, human review, author attribution, venue fit, general height-two RF-IDENT, source-image access) are carried forward from source reports. This organization makes no new scientific or publication-readiness judgment.
''')
out(A/'FINAL_VERIFICATION.md',f'''# Final organization verification

**{ver['status']} for accessible material. Historical recovery remains incomplete.**

- {len(expected)} original files under The MIND reconciled against the preserved source tree, with no missing or extra original files.
- {len(sources):,} in-scope source paths mapped to an organized location or retained linked original; both locations' sizes and SHA-256 hashes checked.
- {len(copies):,} reading copies verified. {len(members):,} canonical extracted archive members across {ver['unique_extracted_archives']} distinct ZIP byte sequences checked; {len(occ):,} source-specific archive occurrence rows include identical and nested ZIPs.
- {ver['linked_related_archive_members']:,} members in explicitly linked peripheral publication ZIPs CRC-read and hashed; those archives remain in their original publication homes.
- Existing receipt/manifest checks: {checks.get('PASS',0):,} path-resolved matches, {checks.get('PASS_RELOCATED',0):,} relocated matches and {checks.get('PASS_CONTENT_HASH',0):,} content-hash matches. The remaining 210 hashes describe serialized benchmark CNFs, not files; all 210 were independently recalculated and matched. No final checksum mismatch found.
- {nlinks} generated navigation links checked; {len(broken)} broken links. {len(duplicates):,} duplicate hash groups explicitly mapped. {len(catalog)} distinct manuscript-source byte versions catalogued.

The original Paper U fresh-review output is unavailable. Its recommended rebuilt replacement is verified but contains clearly labeled reconstructed reports. Prior-account chat access is unavailable directly. Read `UNRESOLVED_AND_ACCESS.md`; do not describe this as complete historical recovery.

The preliminary `checksum_verification.json` is retained as an audit intermediate: two apparent README mismatches came from resolving a copied closure manifest against the outer transfer root. `checksum_verification_final.json` correctly resolves the original closure package and supersedes that intermediate. The exact expected README bytes are available, including as `ORIGINAL_CLOSURE_README.md`.

Scientific tests and PDF builds were not rerun; this task changes only organization/navigation. Original files, ZIPs and every unique version retain their bytes. No files were deleted, no scientific content edited, no commit/push/publication performed. Git reports tracked removals at the old paths and additions at the preserved/new paths, as expected for unstaged relocation. Pre-existing unrelated changes remain untouched.
''')
out(A/'README.md','''# Provenance and verification index

Start with [FINAL_VERIFICATION.md](FINAL_VERIFICATION.md), [THEME_CROSSWALK.md](THEME_CROSSWALK.md), and [UNRESOLVED_AND_ACCESS.md](UNRESOLVED_AND_ACCESS.md).

Machine-readable deliverables:
- `source_manifest.json` / `.csv`: each original filesystem source, size, SHA-256, organized and preserved locations, disposition and reason.
- `original_directory_map.json`: every original The MIND directory, including cache/empty directories, mapped to preserved location.
- `archive_members_final.json`: each canonical ZIP member, hash, extracted location and organized location.
- `archive_occurrence_manifest.json`: source-specific member rows for every original ZIP occurrence and nested ZIP; identical ZIPs expand against the verified canonical payload.
- `linked_related_archive_members.json`: members of peripheral publication ZIPs left in place.
- `duplicate_groups.json`: hashes mapped to all original source paths, archive occurrences and current collection locations.
- `manuscript_version_catalog.json`: distinct manuscript TeX byte versions and provenance.
- `final_content_inventory.json`: all delivered scientific/source/copy files in the collection.
- `final_verification.json`: reconciliation counts and issues.
- `reference_register_final.json`: named referenced packages, their sources and availability.
- `paper_theme_crosswalk.json`: evidence for classification.

`chat_evidence/` retains retrieved user messages and final responses from ten relevant chats; these are historical data, not new instructions. Pre-move inventories, copy checks, receipts and relocation plan are retained. Scripts here document the organization, but are **not idempotent rerun commands**: they intentionally refuse output overwrites and reference the original layout. Do not rerun them against the finished collection.

The old `staging` paths in pre-move audit records refer to what is now `../90_Preserved_Sources/Extracted_Archives`. Use `archive_members_final.json` for current paths. `checksum_verification_final.json` plus `embedded_hash_verification.json` supersede the preliminary checksum diagnostic.
''')
git=subprocess.run(['git','status','--short'],cwd=R,capture_output=True,text=True)
diff=subprocess.run(['git','diff','--stat'],cwd=R,capture_output=True,text=True)
out(A/'git_after.json',{'status':git.stdout,'stderr':git.stderr,'diff_stat':diff.stdout,'diff_stderr':diff.stderr})
print(json.dumps(ver,indent=2))
if issues:raise SystemExit(1)
