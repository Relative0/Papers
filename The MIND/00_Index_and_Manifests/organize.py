from pathlib import Path
import json,hashlib,shutil,collections,os
A=Path(__file__).resolve().parent;M=A.parent;R=M.parent
P1=M/'01_Papers/01_Observation_Refinement_and_Concept_Differentiation'
P2=M/'01_Papers/02_Hierarchical_Concepts_Paper_U'
P3=M/'01_Papers/03_Structured_Boolean_Factorization'
S=M/'02_Shared_and_Exploratory_Research'
OLD=M/'90_Preserved_Sources/Original_The_MIND'
def read(n):return json.loads((A/n).read_text(encoding='utf-8'))
def write(n,o):
 with (A/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2,ensure_ascii=False)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
sources=read('original_inventory.json')['files']+read('supplemental_inventory.json')+read('named_download_discovery.json')['available']+read('additional_download_inventory.json')+[r for r in read('attachment_inventory.json') if 'sha256' in r]
arc=read('archive_inventory_extended.json')
mapping=[];copies=[];byhash=collections.defaultdict(list)
def cp(src,dst,expected):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():
  if sha(dst)!=expected:raise RuntimeError('Destination collision '+str(dst))
 else:
  with src.open('rb') as fi,dst.open('xb') as fo:shutil.copyfileobj(fi,fo)
  shutil.copystat(src,dst)
 if sha(dst)!=expected:raise RuntimeError('Copy verification failed '+str(dst))
 byhash[expected].append(str(dst));copies.append({'source':str(src),'destination':str(dst),'sha256':expected})
 return str(dst)
tops={
 'Gluing':P3/'Supporting_Research/Original_Theme_Gluing',
 'Unfolding':P1/'Supporting_Research/Original_Theme_Unfolding',
 'Ultrametrics and Unconsciousness':P2/'Supporting_Research/Original_Theme_Ultrametrics',
 'Symmetry Breaking and Consciousness':S/'Measurement_and_RF_IDENT/Original_Theme_Symmetry',
 'Height2 Fixed Library Gate 2026-09-29':S/'Measurement_and_RF_IDENT/Supporting_Research/Height2_Fixed_Library_Gate',
 'RF-IDENT Bounded Height2 2026-09-29':S/'Measurement_and_RF_IDENT/Supporting_Research/Bounded_Height2_RF_IDENT',
 'RF-IDENT Bounded Height2 Independent Review 2026-09-29':S/'Measurement_and_RF_IDENT/Reviews/Bounded_Height2_Independent_Review',
 'Interaction Core Gate 2026-09-29':P1/'Supporting_Research/Interaction_Core_Gate',
 'Independent Expert Review':P1/'Reviews/Independent_Expert_Review_of_v0.4',
 'Manuscript Convergence 2026-09-29':P1/'Manuscript_Versions/v0.4_Convergence',
 'Manuscript Referee Repairs 2026-09-29':P1/'Manuscript_Versions/v0.5_Referee_Repairs',
 'Transferred Research':P1/'Supporting_Research/Transferred_Research',
 'Observation Refinement Consolidated Archive 2026-09-29':S/'Original_Packages/Combined_Observation_Refinement_and_RF_IDENT',
}
for r in sources:
 src=Path(r['source']);scope=r['scope'];dest=None;reason=None
 if scope=='The MIND':
  rel=src.relative_to(M);top=rel.parts[0]
  if top in tops:dest=tops[top]/Path(*rel.parts[1:])
  elif src.suffix=='.py':dest=P1/'Reproducibility/Packaging'/src.name
  else:dest=P1/'Original_Packages'/src.name
 elif scope=='Paper_U_Independent_Review_2026-09-29':
  rel=src.relative_to(R/scope);top=rel.parts[0]
  if top=='Recovered_Complete_Review':dest=P2/'Reviews/Rebuilt_Complete_Review'/Path(*rel.parts[1:])
  elif top=='PAPER_U_INDEPENDENT_REVIEW_HANDOFF_2026-09-29':dest=P2/'Reviews/Initial_Independent_Review_Handoff'/Path(*rel.parts[1:])
  elif top=='PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29':dest=P2/'Supporting_Research/Account_Transfer_v0.2'/Path(*rel.parts[1:])
  elif top in ['recovery_check_xymc4qpa','recovery_extraction_check','qa']:reason='Retained sibling QA/recovery duplicate tree; workflow path preserved.'
  elif len(rel.parts)==1 and (src.suffix=='.zip' or 'receipt' in src.name.lower() or 'sha256' in src.name.lower()):dest=P2/'Original_Packages'/src.name
  elif len(rel.parts)==1 and src.suffix=='.py':dest=P2/'Reproducibility/Packaging'/src.name
  else:dest=P2/'Reviews/Original_Review_Work'/rel
 elif scope=='Structured Factorization':
  rel=src.relative_to(R/scope)
  if '.venv' in rel.parts or 'package_verification' in rel.parts or '__pycache__' in rel.parts:reason='Retained sibling environment or validation extraction; active workflow path preserved.'
  else:dest=P3/'Supporting_Research/Structured_Factorization_Snapshot'/rel
 elif scope=='General ProLT Observation Refinement (Research Direction)':reason='Related independent publication-program research folder retained in place; linked in shared-research README.'
 elif scope=='named_download':
  if src.name.startswith('PAPER_U'):base=P2
  elif src.name.startswith('STRUCTURED_FACTORIZATION'):base=P3
  elif 'Unfolding' in src.name:base=P1
  else:base=S
  dest=base/'Original_Packages/Named_Downloads'/src.name
 elif scope=='chat_attachment':dest=S/'Chat_Attachments'/src.parent.name/src.name
 if dest:organized=cp(src,dest,r['sha256'])
 else:organized=str(src)
 preserved=str(OLD/src.relative_to(M)) if scope=='The MIND' else str(src)
 mapping.append(dict(r,organized_location=organized,preserved_location=preserved,disposition='copied and SHA-256 verified' if dest else 'linked original retained',reason=reason))
# Promote explicit reading copies; same version label does not mean same bytes.
promotions=[
 (M/'Manuscript Referee Repairs 2026-09-29/Observation_Refinement_Descent_and_Cone_Draft_v0.5.pdf',P1/'Current_Manuscript/Observation_Refinement_Descent_and_Cone_Draft_v0.5.pdf'),
 (M/'Manuscript Referee Repairs 2026-09-29/Observation_Refinement_Descent_and_Cone_Draft_v0.5.tex',P1/'Current_Manuscript/Observation_Refinement_Descent_and_Cone_Draft_v0.5.tex'),
]
u=R/'Paper_U_Independent_Review_2026-09-29'
for p in (u/'Recovered_Complete_Review/manuscript').iterdir():
 if p.suffix in ['.tex','.pdf','.bib']:promotions.append((p,P2/'Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications'/p.name))
for label,folder in [('v0.2_Research_Closure',u/'PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29/01_CURRENT_MANUSCRIPT'),('v0.3_Initial_Review',u/'PAPER_U_INDEPENDENT_REVIEW_HANDOFF_2026-09-29/01_CURRENT_MANUSCRIPT')]:
 for p in folder.iterdir():
  if p.suffix in ['.tex','.pdf','.bib']:promotions.append((p,P2/'Manuscript_Versions'/label/p.name))
for phase,folder in [('Phase3',M/'Gluing/STRUCTURED_FACTORIZATION_PHASE3_2026-09-29/structured_factorization_phase3'),('Phase4',R/'Structured Factorization/continuity_archive/03_UNPACKED_PHASE4/structured_factorization_phase4'),('Phase5',R/'Structured Factorization/continuity_archive/04_UNPACKED_PHASE5/phase5_output')]:
 for p in folder.glob('THEOREM_NOTE_DRAFT.*'):promotions.append((p,P3/'Manuscript_Versions'/phase/p.name))
for name in ['PHASE5B_MASTER_REPORT.md','THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md','THEOREM_STATUS.csv','NEXT_RESEARCH_GATE.md']:
 promotions.append((R/'Structured Factorization/phase5b_output'/name,P3/'Current_Research_Status'/name))
for src,dst in promotions:cp(src,dst,sha(src))
# Shared historical sources: never promote these to current manuscripts.
for r in sources:
 p=Path(r['source'])
 if p.name in ['Thesis_v_12_2015.pdf','Logical Complexes.tex']:
  dst=S/'Historical_Primary_Sources'/(r['sha256'][:10]+'__'+p.name)
  if not dst.exists():cp(p,dst,r['sha256'])
# Keep the complete safe extraction as an indexed source store; supplement reading
# collections with genuinely archive-only bytes, assigning by innermost package.
member_map=[]
for r in arc['members']:
 if r['kind']=='directory':
  member_map.append(dict(r,organized_location=r['staging'],disposition='preserved archive directory in safe extraction'));continue
 h=r['sha256'];p=Path(r['staging']);origin=(r['archive'].split('!/')[-1]).lower()
 if byhash.get(h):dest=byhash[h][0];disp='exact byte duplicate mapped to verified organized copy'
 else:
  if 'paper_u' in origin or 'padic_ultrametric' in origin:base=P2
  elif 'structured_factorization' in origin or 'gluing_concepts' in origin:base=P3
  elif any(s in origin for s in ['unfolding','carrier_splitting','higher_dimensional']):base=P1
  else:base=S
  dest=cp(p,base/'Archive_Only_Content'/r['archive_sha256'][:12]/r['member'],h);disp='archive-only content copied and verified'
 member_map.append(dict(r,organized_location=dest,disposition=disp))
# Match noncopied external duplicates to reading copies without losing retained path.
for r in mapping:
 if r['disposition']=='linked original retained' and byhash.get(r['sha256']):r['duplicate_reading_copy']=byhash[r['sha256']][0]
original_tops=sorted({Path(r['source']).relative_to(M).parts[0] for r in sources if r['scope']=='The MIND'})
plan=[{'source':str(M/t),'destination':str(OLD/t)} for t in original_tops]
write('source_map_before_relocation.json',mapping);write('archive_member_map.json',member_map);write('copy_verification.json',copies);write('relocation_plan.json',plan)
# Record all directories now, including initial cache directories and empty ones.
dirs=[]
for t in original_tops:
 p=M/t
 if p.is_dir():
  dirs.append({'source':str(p),'preserved_location':str(OLD/t)})
  dirs.extend({'source':str(q),'preserved_location':str(OLD/q.relative_to(M))} for q in p.rglob('*') if q.is_dir())
write('original_directory_map.json',dirs)
print(json.dumps({'source_files':len(sources),'verified_copies':len(copies),'archive_members':len(member_map),'relocations_prepared':len(plan),'paper_folders':[str(P1),str(P2),str(P3)]},indent=2))
