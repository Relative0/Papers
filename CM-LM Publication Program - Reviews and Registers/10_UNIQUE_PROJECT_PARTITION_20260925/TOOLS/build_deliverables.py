import pathlib,json,csv,io,re,hashlib,collections,itertools,zipfile,shutil,urllib.parse
from partition_data import *
W=pathlib.Path(__file__).parent.resolve(); S=W/'staged_docs'; S.mkdir(exist_ok=True)
R=pathlib.Path(r'C:\Users\brian\Documents\Math Latex etc\Papers for Publication')
def load(n):return json.loads((W/(n+'.json')).read_text(encoding='utf-8'))
rows=load('inventory_before'); profiles=load('profiles'); plan=load('partition_plan'); stats=load('folder_overlap_stats'); pairs=load('pairwise_surviving'); opairs=load('pairwise_original'); arcs=load('archive_members'); prof={x['sha256']:x for x in profiles}; idx={x['path']:x for x in rows}; deleted={x['old']:x for x in plan['deletes']}
def put(path,text):
 p=S/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')
def jput(path,obj):put(path,json.dumps(obj,indent=2,ensure_ascii=False))
def link(label,path):return '['+label+']('+urllib.parse.quote(path.replace('\\','/'),safe='/#:.')+')'
def canonical(s):return plan['mapping'].get(s) or deleted[s]['canonical']
def disposition(p):return ('KEEP — program register, not a publication' if p['id']=='RG' else 'KEEP — substantial research direction' if p['id'] in {'GR','SC'} else 'KEEP — technical companion or correction report' if p['id'] in {'SP','PC','BR','AU'} else 'KEEP — publication-track manuscript')
def readtext(h):return (W/'text'/(h+'.txt')).read_text(encoding='utf-8') if (W/'text'/(h+'.txt')).exists() else ''
extractions=[]
for src,dest in [
 (SIGNED+'/REPRODUCIBILITY/ORIGINAL_SOURCE_ARCHIVE/CM_Phase_Calculus_Source_and_Verification.zip',SIGNED+'/REPRODUCIBILITY/SOURCE_PACKAGE'),
 (INTR+'/REPRODUCIBILITY/ORIGINAL_SOURCE_ARCHIVE/Intrinsic_Boolean_CM_Phase_Source_and_Verification.zip',INTR+'/REPRODUCIBILITY/SOURCE_PACKAGE'),
 (GUARD+'/HISTORY/ORIGINAL_RELEASES/Paper_B_Fresh_Adversarial_Review_2026-09-24.zip',GUARD+'/REVIEWS_AND_RECOMMENDATIONS/FRESH_ADVERSARIAL_REVIEW_20260924')]:
 with zipfile.ZipFile(R/src) as z:
  for m in z.infolist():
   if m.is_dir():continue
   target=dest+'/'+m.filename; p=(S/target).resolve(); assert p.is_relative_to(S);p.parent.mkdir(parents=True,exist_ok=True); b=z.read(m)
   if p.exists():assert p.read_bytes()==b
   else:p.write_bytes(b)
   extractions.append(dict(archive=src,member=m.filename,path=target,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),role='Frozen source/review extraction; preserves original archive bytes and internal relative layout.'))
jput(EVID+'/archive_extractions.json',extractions)

# Full file inventory, including individual archive members. Metadata is an index, not a proof certification.
folder_to_p={p['folder']:p for p in P}
def metadata(path,h,size,final):
 suffix=pathlib.PurePosixPath(path).suffix.lower(); pr=prof.get(h,{}); text=readtext(h); base=pathlib.PurePosixPath(path).name
 owner=folder_to_p.get(final.split('/')[0],BY['RG'])
 if '!/' in path:
  inner=path.split('!/',1)[1].lower()
  for tags,pid in [(['p01','chain_ring_resources'],'P01'),(['p02','query_obstruction'],'P02'),(['p03','process_semantics','technical_companion'],'PC'),(['paper_b','p14_','operator-level-boolean','cmbench'],'CO'),(['cm_phase_paper'],'SP'),(['intrinsic_boolean_cm_phase'],'IP')]:
   if any(t in inner for t in tags):owner=BY[pid];break
 current=(final==owner['folder']+'/'+owner['source'] or final==owner['folder']+'/'+owner['source'].replace('.tex','.pdf'))
 if suffix=='.zip':kind='archive / immutable source or release package'
 elif suffix in {'.pdf','.tex'}:kind='manuscript/report' if '\\documentclass' in text or suffix=='.pdf' else 'LaTeX fragment / build support'
 elif suffix=='.md':kind='review/report/research note' if not any(t in base.upper() for t in ['README','MANIFEST','CONTEXT']) else 'administrative/context/index'
 elif suffix in {'.py','.cpp','.sh','.ps1'}:kind='verifier / executable source'
 elif suffix in {'.csv','.json','.tsv'}:kind='dataset / evidence ledger'
 elif suffix in {'.aux','.log','.out','.toc','.fls','.fdb_latexmk','.bbl','.blg'}:kind='build or verification output (not a separate paper)'
 else:kind='support / metadata / binary artifact'
 status='current working manuscript' if current else 'historical/superseded or frozen package' if any(t in final.lower() for t in ['history/','snapshots','prior_','predecessor','source_package/cm_phase','source_package/intrinsic']) else 'proposal/unfinished research' if owner['id'] in {'GR','SC'} else 'supporting evidence / companion / review'
 if 'v0.5' in path:status+='; false dimension identity/hardness excluded'
 if size==0:status+='; empty file retained, not a usable manuscript'
 abstracts=re.findall(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',text,re.S)
 objectives=' '.join((abstracts[0] if abstracts else pr.get('start','')).split())[:1400]
 title=next((q['text'] for q in pr.get('headings',[]) if q['text'].startswith('\\title{') or q['text'].startswith('# ')),None)
 if not title:title=next((l.strip() for l in text.splitlines() if l.strip() and not l.startswith('[PAGE')),base)[:250]
 headings=pr.get('headings',[])
 structure=[]
 if suffix in {'.py','.cpp'}:structure=[l.strip()[:200] for l in text.splitlines() if re.match(r'\s*(def |class |assert |#)',l)][:35]
 elif suffix=='.csv':structure=text.splitlines()[:2]
 elif suffix=='.json':
  try:
   data=json.loads(text);structure=list(data)[:25] if isinstance(data,dict) else ['rows: '+str(len(data))] if isinstance(data,list) else [type(data).__name__]
  except Exception:pass
 return dict(path=path,bytes=size,sha256=h,canonical_path=final,kind=kind,status=status,family=owner['id'],title_or_first_content_line=title,abstract_or_stated_objective_excerpt=objectives,source_claim_and_section_anchors=headings,code_checks_or_data_schema=structure,model_and_claim_boundary=owner['excluded'],review_depth='Current-family claims and model contracts read; other items machine-indexed and screened by headings, objectives, duplicates and cited evidence. No universal proof or row-by-row data certification.')
inv=[metadata(x['path'],x['sha256'],x['bytes'],canonical(x['path'])) for x in rows]
jput(EVID+'/complete_file_inventory_before.json',inv)
member_inv=[]
for x in arcs:
 final=canonical(x['archive'])+'!/'+x['member']; m=metadata(x['archive']+'!/'+x['member'],x['sha256'],x['bytes'],final)
 # Keep archive ledger compact; anchors for unique text are separately recorded once.
 m.pop('source_claim_and_section_anchors',None);m['abstract_or_stated_objective_excerpt']=m['abstract_or_stated_objective_excerpt'][:500];member_inv.append(m)
jput(EVID+'/complete_archive_member_inventory.json',member_inv)
all_claims=[]
for p in P:
 for c in p['claims']:all_claims.append(dict(project=p['id'],canonical_folder=p['folder'],claim=c,source=p['folder']+'/'+p['source'],source_anchors=p['refs'],excluded=p['excluded'],corrections=p['corrections']))
jput(EVID+'/claim_ownership_ledger.json',all_claims)

# Reusable evidence sources and original reports remain unchanged.
for n in ['portfolio_coverage_before','manifest_checks_before','folder_overlap_stats','exact_groups_before','pairwise_original','pairwise_surviving','semantic_screen_before','verification_runs','mutation_receipt','partition_plan','extraction_errors']:
 jput(EVID+'/'+n+'.json',load(n))
jput(EVID+'/projects.json',P)
put(EVID+'/METHODOLOGY.md','''# Evidence method and limits

The scan read every non-.git file in the named repository and every member of every ZIP using Python zipfile. SHA-256 and size identify bytes, including untracked ZIPs. pypdf extracted all distinct PDF byte streams without errors; LaTeX is preferred for mathematical contracts. No source PDF was edited or rebuilt.

Every file/member has a category, source excerpt when text is available, family assignment and status. Current manuscript theorem statements, scope sections, known overlap cases, correction notes and available reviews were inspected. This is a publication partition and preservation audit, not a line-by-line proof audit of every archive member or a rerun of every dataset row. Broad archive code was indexed, not certified.

All 171 original-folder pairs and all 120 surviving-project pairs are recorded. Codes: C acceptable core; S substantive non-core correspondence; V version lineage; H companion/history; E repeated evidence; N no substantive correspondence identified. N is a scoped finding, not proof of absolute disjointness. Exact file groups and semantic correspondences are separate.

Lexical screening uses normalized five-word shingles, at least 100 shared shingles and containment at least 0.30. It finds candidate relationships; it never authorizes semantic deletion. Representative files are deduplicated by hash before screening. Manuscript/source/PDF renditions can still differ; bibliography and boilerplate can dominate similarity. Same-family history is also manually indexed.

All removals require an equal SHA-256 retained tracked copy. Divergent sources, archives, corrections, negative results and historical manifests are retained. A complete final preservation map covers every one of the 1,086 starting files, including all 597 distinct byte streams. Top-level manifests exclude only themselves; historical manifests are immutable evidence and can retain their old relative-path conventions.

New README/research/claim/index files are editorial navigation. They do not amend historical manuscript text, declare external novelty, or certify submission readiness. Existing documents labelled panel/referee/GO can be simulated reviews and are not treated as independent human refereeing.
''')

for p in P:
 f=p['folder']; head=p['source']; source=R/f/head
 if p['id'] not in {'GR','SC','RG'}:assert source.exists(),str(source)
 body=f"# {p['title']}\n\n**Status:** {p['stage']}. **Disposition:** {disposition(p)}.\n\n{p['form']}. {p['uniqueness']} within this portfolio; external priority remains separate.\n\nCurrent entry point: {link(head,head)}.\n\n"+'\n'.join('- '+c for c in p['claims'])+f"\n\nRead [CLAIMS_AND_UNIQUENESS.md](CLAIMS_AND_UNIQUENESS.md) for boundaries, corrections and evidence.\n\n**Remaining work:** {p['remaining']}\n\n**Main risk:** {p['risk']}\n\n- [Reviews and recommendations](REVIEWS_AND_RECOMMENDATIONS/README.md)\n- [Reproducibility and duplicate policy](REPRODUCIBILITY/README.md)\n- [Version history](HISTORY/README.md)\n- [Current source manifest](SOURCE_MANIFEST_SHA256.csv)\n- {link('Program project register','../'+REG+'/PROJECT_REGISTER.md')}\n\nThis navigation was added on 2026-09-25. Historical manuscript, review, code, data and archive bytes were preserved.\n"
 put(f+'/README_FIRST.md',body)
 claims=f"# Claims and uniqueness — {p['title']}\n\n**Canonical owner:** {p['id']} — `{f}`.\n\n**Stage / recommended form:** {p['stage']} / {p['form']}.\n\n## Unique results or bounded research targets\n\n"+'\n'.join('- '+x for x in p['claims'])+f"\n\n## Shared or excluded from novelty\n\n{p['excluded']}\n\n## Corrections and excluded claims\n\n{p['corrections']}\n\n## Evidence and locators\n\nCurrent source: {link(head,head)}. Line ranges below refer to the preserved source text after normalizing newline sequences for inspection; theorem labels/section titles are authoritative locators.\n\n"+'\n'.join('- `'+x+'`' for x in p['refs'])+f"\n\nFile and ZIP-member SHA-256, titles/objectives and section anchors are in the {link('complete evidence inventory','../'+EVID+'/complete_file_inventory_before.json')}. The {link('pairwise matrix','../'+EVID+'/pairwise_surviving.json')} specifies ownership, treatment and residual content for every project pair.\n\n## Work still required\n\n{p['remaining']}\n\n{p['risk']}\n"
 put(f+'/CLAIMS_AND_UNIQUENESS.md',claims)
 related=[x for x in rows if canonical(x['path']).startswith(f+'/')]
 reviewpaths=sorted({canonical(x['path']) for x in related if any(t in x['path'].lower() for t in ['review','audit','revision','changed_claims','changelog','readiness']) and x['path'].endswith(('.md','.pdf','.tex')) and '00_PUBLICATION' not in x['path']})
 put(f+'/REVIEWS_AND_RECOMMENDATIONS/README.md',f"# Reviews and recommendations\n\n{p['remaining']}\n\n{p['risk']}\n\nReviews are preserved as received; labels such as panel/referee do not establish independent human review. Original package-relative layouts are retained where build or provenance depends on them.\n\n"+('\n'.join('- '+link(path[len(f)+1:],'../'+path[len(f)+1:]) for path in reviewpaths) if reviewpaths else '- No separate substantive reviewer artifact was located in this project. Read the program preservation/consolidation audits and the project claim boundary.')+f"\n\nProgram-level review record: {link('audits','../../'+REG+'/05_CURRENT_AUDIT_AND_RECOMMENDATIONS')}.\n")
 repro=[canonical(x['path']) for x in related if x['path'].endswith(('.py','.cpp','.zip')) and x['folder']!=PORT]
 put(f+'/REPRODUCIBILITY/README.md',f"# Reproducibility and evidence policy\n\nSource of record: {link(head,'../'+head)}.\n\nKeep package-relative files together. Repeated data/code in frozen release, source-snapshot and submission bundles is intentional: it records the inputs used for that package and permits isolated reproduction. It is not another novelty claim. The exact overlap ledger records every repeated hash. Current manuscript pointers and HISTORY labels distinguish loose manuscript heads from archival copies.\n\n"+'\n'.join('- '+link(path[len(f)+1:],'../'+path[len(f)+1:]) for path in sorted(set(repro)))+f"\n\nShared evidence: {link('program reproduction supplement','../../'+REG+'/08_PORTFOLIO_PROGRAM_REPORTS_20260921/REPRODUCTION_SUPPLEMENT.zip')}; {link('phase handoff tables','../../'+SHARED)}. Canonical model corrections: {link('audit project','../../'+BY['AU']['folder']+'/README_FIRST.md')}.\n\nThe cleanup verifies bytes and path dependencies; it does not certify all mathematical proofs or rerun performance campaigns. Historical `/mnt/data` imports/output paths are retained and documented. Fresh checks are in {link('verification ledger','../../'+EVID+'/verification_runs.json')}. No timings or historical outputs were rewritten.\n")
 histories=sorted({canonical(x['path']) for x in related if '/HISTORY/' in canonical(x['path']) and x['path'].endswith(('.pdf','.tex','.zip','.md'))})
 put(f+'/HISTORY/README.md',f"# Version history and preserved context\n\nWorking head: {link(head,'../'+head)}. Historical filenames, dates and claims describe their own snapshots. They do not override CLAIMS_AND_UNIQUENESS.md.\n\n{p['corrections']}\n\n"+'\n'.join('- '+link(path[len(f)+1:],'../'+path[len(f)+1:]) for path in histories)+f"\n\nFull old-to-new path map and hashes: {link('mutation receipt','../../'+EVID+'/mutation_receipt.json')}. Original context notes and manifests are preserved under this history or the merged subdirection; current top-level manifests were regenerated.\n")
 if p['id'] in {'GR','SC'}:put(f+'/RESEARCH_BRIEF.md',claims.replace('# Claims and uniqueness —','# Research brief —')+'\n\nThis is an unfinished direction, not a submission manuscript. The referenced working notes retain their original claims and corrections as evidence.\n')

put(GUARD+'/RESEARCH_BRIEFS/CERTIFIED_GUARD_SYNTHESIS.md',f'''# Certified CM-LM guard synthesis — deferred research brief

The former top-level folder held seven substantive files, all exact copies: the current guarded PDF/TeX, review/revision record, verifier/result, and a structural planning document. Its unique generated context and manifest are preserved in HISTORY/FORMER_GUARD_SYNTHESIS_FOLDER. It does not supply a distinct completed synthesis algorithm, certificate framework, or application beyond the current GU paper.

GU already owns exact sign quotient/zero handling, representation-invariant dispatch, finite-predicate minimum tests, the nonlinear affine/quadratic separation and three-probe result. A future synthesis project must specify a restricted guard library and cost model, produce an algorithm and sound certificates, and demonstrate a theorem or application beyond those results and classical test-set/real-algebraic machinery.

Canonical paper: {link('guarded manuscript','../'+BY['GU']['source'])}. Planning source: {link('structural computation','../../'+BY['SC']['folder']+'/README_FIRST.md')}. Every old file and canonical hash is listed in the partition report. **Disposition: brief attached to GU; standalone route deferred until new evidence exists.**
''')
put(FOUND+'/RESEARCH_BRIEFS/COMPACT_SPECTRAL_DYNAMICAL_ATLAS.md',f'''# Compact CM spectral and dynamical atlas — deferred research brief

The former folder held five substantive files, all exact copies of the foundations audit, master inventory and theorem bank. No unique atlas manuscript, generation code or classification-output package was found in that folder. Its unique context and manifest remain in HISTORY/FORMER_ATLAS_FOLDER.

FO already owns its compact spectral boundary appendix. A larger atlas could study similarity/minimal-polynomial classes, iteration/functional graphs, frame spectra and semigroups, but those are research targets here. Recover traceable generation code, exhaustive output tables and proofs before claiming a new classification. Distinguish matrix-element semantics from spectral truth values.

Canonical foundations: {link('manuscript','../'+BY['FO']['source'])}. Canonical theorem bank: {link('bank','../../'+REG+'/01_THEOREM_BANK/THEOREM_BANK.tex')}. **Disposition: reference/research brief attached to FO; no independent paper yet.**
''')
put(GEN+'/OBSERVATION_DESIGN_AND_SAFE_REFINEMENT/RESEARCH_BRIEF.md',f'''# Constrained observation design and joint-versus-sequential safety

**Status: corrected research subdirection within GR.** The v0.3-v0.5 notes are in HISTORY/WORKING_NOTES, preserved byte for byte. They are not three current papers. The common verification scripts and v0.1-v0.5 ledger live once in the parent GR project; BT retains its self-contained versioned verifier package.

The substantive residue is the v0.5 three-chain destructive-interaction and five-state compensating-interaction examples (section Interaction defects): coordinatewise safety need not imply joint safety, and joint safety need not admit a safe first coordinate. Preserve these examples and compare scheduling/selection rules under an explicit permitted observation family and cost model. Much repair/Horn/chain/height-two material now belongs to BT post-audit v2, whose seven-state example strengthens the old eight-state example.

**Excluded:** v0.5 Proposition Connection with classical 2-dimension and its dependent Complexity inheritance corollary. The argument wrongly turns a one-direction comparison condition into an injective order embedding. For a nontrivial chain P=Q, the defined relative observation dimension is zero while classical Boolean embedding dimension is positive. This invalidates that proof of hardness; it does not prove the corrected optimization problem easy or hard.

Current question: which restricted observation families allow efficient safe selection, batch scheduling or certificates beyond classical minimum test-set/hitting-set formulations? GU already owns its exact-dispatch specialization. No new hardness theorem or general solver is claimed.

- {link('Canonical verification scripts','../03_VERIFICATION')}
- {link('Original research ledger','../04_RESEARCH_LEDGER/ProLT_Research_Ledger_v0.1-v0.5.md')}
- {link('Current binary-thinning paper','../../'+BY['BT']['folder']+'/README_FIRST.md')}

Promote to a separate project only after a distinct constrained theorem, algorithm or application is established. The present merge preserves its theoretical boundary and all negative/corrective evidence.
''')

for f in [COMP,FOUND]:
 dels=[x for x in plan['deletes'] if x['old'].startswith(f+'/')]
 put(f+'/CANONICAL_REFERENCES.md','# Canonical references replacing loose cross-project copies\n\nOriginal release ZIPs and package manifests remain immutable historical records. Current entry points below replace unnecessary loose PDF/source/review duplication; no LaTeX build dependency was redirected to a Markdown file.\n\n'+'\n'.join('- `'+x['old'][len(f)+1:]+'` → '+link(x['canonical'],'../'+x['canonical'])+'; SHA-256 `'+x['sha256']+'`.' for x in dels))
put(COMP+'/01_CURRENT_REVISED_COMPILER_AND_REVIEW_20260922/CANONICAL_REFERENCES.md','# Current compiler versus historical references\n\nUse Operator_Level_CM_Compiler_Revised_Draft.pdf and .tex (14 pages). The older file named current.pdf is the 24-page predecessor; its canonical retained copy is ../HISTORY/PORTFOLIO_PREDECESSOR_20260921/manuscript/main.pdf. The foundations files formerly next to this draft have canonical tracked copies in CM-LMs and lifting. See [the complete path/hash map](../CANONICAL_REFERENCES.md). Existing handoff prompts describe the original package layout.\n')
put(SHARED+'/README_FIRST.md',f'''# Shared phase handoff — historical evidence, not a paper

This is the former Modal Quantum CM-LMs release context and shared table collection. The original CM_Quantum_Handoff_2026-09-17.zip remains an immutable bundle containing both papers. The loose paper sources, PDFs, bibliographies and source ZIPs now have separate canonical homes:

- {link('Signed/integral phase synthesis','../../'+SIGNED+'/README_FIRST.md')}
- {link('Intrinsic Boolean phase algebra','../../'+INTR+'/README_FIRST.md')}

Historical FILE_MANIFEST and SHA256SUMS retain their release path conventions. The current program SOURCE_MANIFEST_SHA256.csv covers the relocated bytes. The two former paper source ZIPs are unpacked intact in their respective REPRODUCIBILITY/SOURCE_PACKAGE directories. Modular paper.tex versus standalone TeX are preserved variants; no rebuild-equivalence claim is made. Tables here support both branches, so their canonical shared home is the register rather than duplicated new paper folders.
''')

# The theorem bank is an ownership register, including residual appendices not promoted to papers.
bank=[('Cyclic phase lifts, nilpotent filtration and ANF degree','IP','Algebra appendix candidate; distinguish existing C4 paper from prospective higher cyclic generalization.'),('Smith resources, coding and raw teleportation','P01','Current general manuscript; bank is historical/supporting formulation.'),('Exact charged-oracle query results','P02','Current technical note; do not turn finite Simon scans into a universal claim.'),('Transpose-orthogonal span (d-1)^2+1 and form obstruction','P01 / AU','Resource-restriction appendix with prior-art review; no separate paper.'),('Qualified no-deletion and retained-syndrome criterion','PC','Technical companion appendix; retain noninjective deletion exception.'),('Finite GHZ six-context certificate and failed smaller subsets','AU','Finite reproducibility evidence; no universal minimality claim.'),('Symbolic support/enrichment and updates','BR','Full bridge report, conditional on chosen scalar/effect structure.'),('Compact spectral/dynamical extension','FO brief','Deferred until actual outputs/code/proofs are recovered.'),('Lie/Bector/fuzzy/cognitive/temporal proposals','RG','Unlocated or undeveloped primary material; no publication slot assigned.')]
put(REG+'/THEOREM_BANK_OWNERSHIP.md','# Theorem-bank ownership and residual material\n\nThe preserved theorem bank is a historical register, not a paper or a current independent claim of all listed results.\n\n| Topic | Canonical owner | Disposition |\n|---|---|---|\n'+'\n'.join('| '+' | '.join(t)+' |' for t in bank))
register='# CM-LM publication project register\n\n**2026-09-25 partition:** 16 top-level projects/registers. Ten located manuscript families are evaluated independently; nine remain publication-track in different states, while signed/integral phase is classified as a technical synthesis companion. Two substantial research directions, four companions/correction packages including signed phase, and this register remain. These are not sixteen submission-ready papers.\n\n| ID | Canonical project | Stage | Recommended form |\n|---|---|---|---|\n'
register+='\n'.join(f"| {p['id']} | {link(p['title'],'../'+p['folder']+'/README_FIRST.md')} | {p['stage']} | {p['form']} |" for p in P)
register+='\n\nCanonical common evidence: [portfolio reproduction supplement](08_PORTFOLIO_PROGRAM_REPORTS_20260921/REPRODUCTION_SUPPLEMENT.zip), [shared phase handoff](11_SHARED_PHASE_HANDOFF_20260917/README_FIRST.md), [theorem-bank ownership](THEOREM_BANK_OWNERSHIP.md), [partition evidence](10_UNIQUE_PROJECT_PARTITION_20260925/METHODOLOGY.md).\n\n'+link('Full partition report','CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md')
put(REG+'/PROJECT_REGISTER.md',register)

# Version families are keyed to content, not generic main.tex/current.pdf filenames.
versions=[]
for x in rows:
 if pathlib.PurePosixPath(x['path']).suffix in {'.pdf','.tex'}:
  m=next(t for t in inv if t['path']==x['path']); versions.append({k:m[k] for k in ['path','sha256','bytes','canonical_path','family','kind','status','title_or_first_content_line']})
jput(EVID+'/version_family_and_renamed_manuscript_map.json',versions)

dispositions=[]
for f in sorted({x['folder'] for x in rows}):
 if f==PORT:d='REMOVE AFTER VERIFIED MERGE';dest='Canonical projects and program register';u='Fully redundant except for administrative/context material';reason='353/353 exact tracked coverage; release layout preserved by inventories/path map and starting Git commit.'
 elif f==GS:d='CONVERT TO RESEARCH BRIEF or index';dest=GUARD+'/RESEARCH_BRIEFS';u='Fully redundant except for administrative/context material';reason='7/7 substantive files exact copies; no separate synthesis algorithm/certificate/application supported.'
 elif f==ATLAS:d='CONVERT TO RESEARCH BRIEF or index';dest=FOUND+'/RESEARCH_BRIEFS';u='Fully redundant except for administrative/context material';reason='5/5 substantive files exact copies; classification-output/generation package not located in this folder.'
 elif f==DESIGN:d='MERGE INTO '+GEN;dest=GEN+'/OBSERVATION_DESIGN_AND_SAFE_REFINEMENT';u='High non-core overlap';reason='Keep 3/5-state interaction examples and constrained-design question; archive superseded v0.3-v0.5 theorem material and mark false dimension/hardness claims. Common verification and ledger centralized.'
 elif f==MODAL:d='KEEP — technical companion or correction report (split mixed folder)';dest=SIGNED+'; '+INTR+'; '+SHARED;u='High uniqueness';reason='One original folder holds two different scalar models/manuscript families. Separate canonical projects; shared historical evidence in register. IP publication-track; SP technical synthesis companion.'
 else:
  p=folder_to_p[f];d=disposition(p);dest=f;u=p['uniqueness'];reason=p['claims'][0]+' '+p['risk']
 dispositions.append(dict(original=f,disposition=d,destination=dest,uniqueness=u,reason=reason))
jput(EVID+'/original_folder_dispositions.json',dispositions)

report=['# CM-LM Unique Project Partition and Overlap Report','', '**Date:** 2026-09-25. **Repository:** Relative0/Papers. **Starting commit:** `7b9cdedadd8d2ec75d489f82917109b723f56e0c` (verified exact HEAD and ancestor before mutation). Local cleanup and commit are authorized; no push is performed.','', '## 1. Executive decision summary','',
'The workspace is partitioned from 19 to 16 top-level folders. This is nine publication-track manuscript projects of differing maturity, two substantial but incomplete research directions, four technical companions/correction projects (including signed/integral phase), and one program register. All ten requested manuscript families were independently assessed; signed/integral phase is retained as synthesis/companion rather than promoted as a novel quantum-algorithm paper. Internal uniqueness is distinct from external priority and submission readiness.','',
'Guard synthesis and the spectral atlas become parent-project briefs; observation design becomes a clearly bounded subdirection of general refinement. The mixed modal phase folder is split into signed/integral and intrinsic Boolean projects, with shared historical evidence in the register. The compiler/foundations split and 14-page/24-page/21-page version lineage are explicit.','',
'The fresh inventory includes **1,086 files, 148,795,700 bytes, 597 distinct SHA-256 byte streams**, plus **4,594 ZIP-member instances**. All 18 old source manifests matched every listed entry. The portfolio passed **353/353**, **62,793,791 bytes**, with tracked outside copies, immediately before deletion. The cleanup used **173 git mv file relocations** and removed **389 exact duplicate file instances (67,799,050 bytes)**, including the three untracked ZIP copies. Archive packages and legitimate self-contained duplicated evidence remain. These gross removed bytes are not net repository-size savings, since Git history, new inventories and accessible source packages remain.','',
'No original manuscript, proof, negative result, correction, data, source, review or archive byte stream was edited. Original manifests/context notes are retained as history. New manifests, README/claim statements and research briefs provide current navigation. Preservation is checked by complete before-to-after SHA-256 mapping, not filename similarity.','',
'## 2. Before/after top-level folder map','', '| Original folder | Surviving destination |','|---|---|']
report += ['| `'+d['original']+'` | `'+d['destination']+'` |' for d in dispositions]
report+=['','## 3. Complete original-folder dispositions and exact overlap','', 'Counts below exclude only generated context and SOURCE_MANIFEST from the content denominator. Cross-folder duplicates are counted against other non-portfolio folders so the portfolio does not make every project appear redundant. Bytes/file identity do not measure intellectual novelty.','', '| Original | Disposition | Uniqueness | Exact content overlap (files; bytes) | Reason |','|---|---|---|---|---|']
for d in dispositions:
 st=next(x for x in stats if x['folder']==d['original']);report.append(f"| {d['original']} | {d['disposition']} | {d['uniqueness']} | {st['content_duplicate_files']}/{st['content_files']}; {st['content_duplicate_bytes']:,}/{st['content_bytes']:,} | {d['reason']} |")
report+=['','## 4. Ranked manuscript families and publication-track projects','', 'Ranking balances a distinct non-core theorem package, existing evidence and tractable next work. It is a portfolio judgment, not journal acceptance or worldwide-firstness certification. Signed phase is included as the tenth required family but explicitly ranked as companion/reference.']
for p in P[:10]:
 report+=['',f"### {p['priority']}. {p['title']} ({p['id']})",'',f"**Canonical folder:** `{p['folder']}`. **Stage:** {p['stage']}. **Uniqueness:** {p['uniqueness']}. **Form:** {p['form']}.",'',f"**Current source:** `{p['folder']}/{p['source']}`.",'','**Principal contribution:**','']+['- '+x for x in p['claims']]+['', '**Excluded/shared:** '+p['excluded'],'','**Corrections:** '+p['corrections'],'','**Remaining work:** '+p['remaining'],'','**Risk:** '+p['risk'],'','**Source anchors:** '+'; '.join('`'+x+'`' for x in p['refs'])]
report+=['','## 5. Ranked substantial but incomplete research directions','']
for p in [BY['GR'],BY['SC']]:
 report += ['### '+p['title'],'',f"**Canonical:** `{p['folder']}`. {p['uniqueness']}. {p['form']}.",'']+['- '+c for c in p['claims']]+['','**Already owned elsewhere:** '+p['excluded'],'','**Required:** '+p['remaining'],'','**Corrections/risk:** '+p['corrections']+' '+p['risk'],'']
report+=['Guard synthesis and the spectral atlas are deferred briefs under GU and FO. Their original folder names did not justify independent paper projects. Observation design remains a distinct question inside GR; preserving a theoretical boundary does not require preserving a thin top-level folder.','', '## 6. Companions, corrections and registers','']
for k in ['PC','BR','AU','SP','RG']:
 p=BY[k];report += [f"### {k}: {p['title']}",'',f"`{p['folder']}` — {p['form']}. "+' '.join(p['claims']),'','**Why retain separately:** '+p['risk'],'','**Next required research work:** '+p['remaining'],'']
report+=['## 7. Full pairwise substantive-overlap matrix','', 'C = acceptable core; S = substantive correspondence; V = version; H = companion/history; E = evidence; N = no substantive correspondence identified. The complete 120 surviving-project pairs below specify ownership, treatment and residual contribution. The original 171 pairs, including dissolved folders, are in Appendix A and pairwise_original.json. File-level hashes and paths are in exact_groups_before.json and the deletion/move tables.','', '| Pair | Class | Section/claim/topic correspondence | Canonical ownership and action | Unique residue |','|---|---|---|---|---|']
for x in pairs:report.append('| '+x['a']+' / '+x['b']+' | '+x['kind']+' | '+x['correspondence']+' | '+x['canonical_owner']+'; '+x['action']+' | '+x['unique_residual']+' |')
report+=['','## 8. In-depth overlap findings and canonical evidence','', 'All project IDs resolve to the canonical folders and precise sources in sections 4–6. The following are the cases where a naive folder or filename judgment would lose important distinctions.','',
'### 8.1 Thin copied directions','',
'Guard synthesis: current guarded release and verifier are exact copies; the planning document is also held in structural computation. Seven substantive files add zero unique bytes. The new GU brief states the future synthesis problem and evidence gate; original context/manifest are kept. Spectral atlas: five substantive audit/inventory/theorem-bank files add zero unique bytes. The FO brief retains the classification question but does not invent generated tables. All exact old/new paths and full hashes appear in section 10.','',
'### 8.2 Foundations versus compiler','',
'The 31-page foundations PDF has SHA-256 `ca4c64497e29c40e7398746ef57550f5915e5ce7b5be480cc579dc13601bb4ca`. The 24-page compiler predecessor is `a02ba8aded23edd94b5f816bbf6b5f8afee881576762eb89371eb884613c4133`; it is not the foundations paper even where a directory calls both current. The revised compiler source is `5189ac98c826c54af4e291e0516216caffa93dc521e54bec679ee33a2e5e7fd4`. FO valuation/coherence and CO selection/fusion necessarily overlap, but CO sections Typed normalization, Pair compiler and soundness, Current evidence own different claims. Loose duplicate foundations files and cross-folder compiler reviews/PDFs are removed, with canonical references. Frozen mixed handoff ZIP remains historical provenance.','',
'### 8.3 General refinement, design and thinning','',
'GR v0.2 fiber-profile normal form allows points (p,a) and a forgetful carrier map. BT post-audit v2 explicitly assumes same-carrier order thinning and observation factorization through the old T0 quotient. These are distinct objects. GR imports mapping-cone/fiber machinery as standard background; BT owns the focused integral recognition/collapse and sharp-limit package. Original design v0.3/v0.4/v0.5 theorem material is history when BT supersedes it. The three-chain 010/101 and five-state compensating examples remain useful for a constrained selection/scheduling question. Their presence warrants preservation inside GR, but no independent optimization theorem currently justifies a separate project. The v0.5 equality with 2-dimension is false even at P=Q a nontrivial chain; its hardness corollary is unsupported. No manuscript bytes were rewritten to conceal the error.','',
'The old core v0.8 PDF is moved to ProLT HISTORY; v0.8.1 is current. The shingle screen found 0.9379 containment for the v0.8/v0.8.1 PDFs, corroborating version identity without treating it as an exact replacement. v0.6 remains history. General/design verification and ledger duplicates are centralized; BT keeps its self-contained verifier package, including both the original absolute-import and portable repair-forest variants.','',
'### 8.4 Bridge, audit, P01 and process','',
'BR has a full idempotent/scalar/support/update report; P01 Appendix A is a summary of that chosen-enrichment construction, not a replacement. BR and AU share eighteen exact evidence files, including the 65,536-row resource inventory and related teleportation/coding/contextuality tables. The package copies remain because they are historical, self-contained input/output evidence; AU is canonical for the correction datasets and BR for the bridge report. The exact paired paths/hashes follow in Appendix B.','',
'P01 general complete-basis trichotomy, d*h codebook and raw teleportation are static resource results. PC proves independent-success and conditioning obstructions, gives a changed binary completion, and analyzes marked normalizers, filters, retained phase and resolved disposal. This is enough separate technical function to retain a companion; merging it into P01 would obscure model changes and negative results. Bare nonzero ring support is not declared tensor-closed.','',
'### 8.5 Sign-law descendants','',
'FJ and GU share the Evolving Propositions parent and sign conventions. FJ whole-orthant/arrangement realizability has smooth/finite-jet/Denjoy--Carleman hypotheses; GU takes finitely many scores as given and studies exact zero-aware quotients and restricted probes. GU explicitly identifies the companion regularity question. Keep both, retain the parent in FJ history, and cite the boundary in both claim records. The freshly extracted GU review ZIP contains unique review/planning/checker material; it remains review history, and the current nonlinear manuscript already responds to several recommendations.','',
'### 8.6 Phase split and computational/resource boundaries','',
'SP changes to integral/signed arithmetic; IP stays in F2[C4]. Both repeat the native Boolean stage and norm/isometry boundaries, which are necessary context and not two novelty claims. SP is a useful technical synthesis with strong prior overlap; IP has its own intrinsic phase-ANF/nilpotent package. P01 uses general chain-ring resources and P02 charges access. IP inspection of a built ANF is not a contradiction to P02 query lower bounds. The shared phase handoff is a named register evidence location. Both source ZIPs are unpacked without editing their modular variants.','',
'### 8.7 Additional archive recovery and substantive evidence','',
'The reproduction supplement has 2,161 members and 691 distinct member byte streams absent from the loose-file inventory. It contains source/raw evidence, older compiler material, theorem/claim registries and reconciliation records. It is retained whole and member-indexed. This improves evidence discoverability; it does not establish a completed current confirmatory compiler campaign. The current 116-test / 1,048,576-case claims are not rerun here. GU fresh-review ZIP contributes four text/code byte streams absent from loose files. The phase source ZIPs contribute 27 and 29 distinct member streams absent from loose files, including modular sections and code. No archive-only material is silently discarded.','',
'## 9. Version-family and renamed-manuscript map','',
'The complete PDF/TeX instance map, hashes and statuses is `10_UNIQUE_PROJECT_PARTITION_20260925/version_family_and_renamed_manuscript_map.json` in the register. Principal families:','',
'| Family | Current head | Preserved lineage / status |','|---|---|---|',
'| Foundations FO | 31-page LM-centered PDF and editable source | Alias CM_LM_Boolean_Operator_Calculus_LM_Centered_V1.pdf is exact same PDF; historical mixed handoff ZIP retained. |',
'| Compiler CO | 14-page Revised_Draft PDF/TeX | 24-page current.pdf/main.pdf → HISTORY portfolio predecessor; 21-page PDF → HISTORY legacy; archive-only earlier compiler and proof variants retained/indexed. Paper B in old portfolio means CO, not GU. |',
'| Finite jet FJ | 13-page submission candidate | 12-page referee-revised and 29-page continuous-score parent kept as history; do not overwrite divergent text. |',
'| Guarded GU | 18-page restricted-dispatch/nonlinear release | Original release and fresh-review ZIPs kept; fresh unique review material exposed under REVIEWS_AND_RECOMMENDATIONS. |',
'| Signed phase SP | 33-page standalone PDF/TeX | Modular source ZIP/paper.tex preserved as source-package variant; common original handoff in register. |',
'| Intrinsic phase IP | 26-page standalone PDF/TeX | Modular paper.tex/tables differ from standalone edition; preserve both pending build comparison. |',
'| ProLT PL | v0.8.1, 19 pages | v0.8, 18 pages, now HISTORY; v0.6, 15 pages, history; old broad agendas not current results. |',
'| Binary thinning BT | post-audit v2, 16 pages | v0.1–v0.5 research ancestry preserved in GR; v0.3 TeX empty; v0.4/v0.5 current-theorem overlap not new papers. |',
'| P01 | 11-page mature main.pdf/main.tex | Earlier skeleton/history within preserved archives remains historical; general proofs present, not just a proposal. |',
'| P02 | 9-page Bounds note | Earlier Obstructions labels/skeletons refer to same developing family. |',
'| Process PC | 9-page companion plus later verification | P03_STUB/main.tex is a related verification/stub document, not an exact replacement. |',
'| Correctness AU | 28-page report and source | Standalone TeX inlines generated tables; old pure-modal addendum is a corrected historical snapshot. |',
'| Bridge BR | full report TeX | P01 conditional interface is a summary; preserve full proof/effect/update report. |','',
'## 10. Exact duplicates removed or converted to canonical references','',
'Every entry below had an equal SHA-256 tracked canonical file before removal and an equal retained copy after relocation. Removal is per-file, not semantic inference. Three portfolio ZIP entries were untracked; their canonical copies were tracked.','', '| Removed original path | Retained canonical path | Bytes | SHA-256 |','|---|---|---|---|']
report += ['| `'+x['old']+'` | `'+x['canonical']+'` | '+str(x['bytes'])+' | `'+x['sha256']+'` |' for x in plan['deletes']]
report+=['','## 11. Files moved with Git','', '| Original path | New path | SHA-256 |','|---|---|---|']
report += ['| `'+x['old']+'` | `'+x['new']+'` | `'+x['sha256']+'` |' for x in plan['moves']]
report+=['','## 12. Historical, superseded and corrected material retained','',
'All 18 old SOURCE_MANIFEST files and 17 generated project-context notes remain byte-identical history (the original program register used README_FIRST rather than a context note). Original release ZIPs, source snapshots, P14 negatives, rejected claims, review responses, raw outputs and timing differences are untouched. Both compiler generations and earlier PDF, finite-jet parent/referee history, ProLT v0.6/v0.8 and v0.1–v0.5 notes are preserved. The phase modular sources are not overwritten by standalone sources. Empty v0.3 TeX remains an explicitly empty historical file.','',
'Historical SHA256SUMS, source manifests and instructions still describe their original package layouts. The current manifests and full relocation map are separate. The nine old correctness-audit manifest discrepancies identified by the prior preservation audit are not repaired by changing evidence; this pass only confirms preservation of the currently present bytes.','',
'## 13. Do not delete','',
'- Current manuscript TeX/PDF pairs, bibliographies, proof appendices and every required source fragment.','- Correction report, process companion and full bridge; especially nonzero-independence, conditioning, activation/disposal and probability-obstruction results.','- Original archives: reproduction supplement; both phase source ZIPs; shared phase handoff; foundations/compiler handoff; guarded release and fresh review; ProLT v0.8.1 and thinning release.','- Seven-state certificate, six-vertex enumeration source/output, original and portable repair-forest scripts, negative searches and historical v0.5 correction context.','- Old manifests/context/review/history bytes and this partition path/hash ledger.','- Compiler generic tie/P14 negative result and raw reconciliation records; no speedup-only selection of evidence.','',
'## 14. Drop or defer claims/projects','',
'Drop the false v0.5 relative observation-dimension/2-dimension identification and its dependent hardness proof from active claims. Do not infer a replacement complexity result. Defer standalone guard synthesis, spectral atlas and observation design until they have a new verified payload beyond GU/FO/BT and classical methods. Keep signed phase as a technical synthesis, ProLT core as a conservative framework/methods candidate, and structural computation conditional on matched raw evidence.','',
'Exclude unqualified finite-copy no-activation, an unchanged tensor-closed nonzero ring process model, bare-LM-derived modal measurement, a degenerate Hermitian-pairing claim where isotropic self-products are meant, Boolean Born-rule derivation, free ANF inspection inside charged query bounds, a general Simon theorem from small scans, general DJ optimality, and CM-specific speedup inferred from unmatched tasks. Preserve the original assertions as history with correction pointers.','',
'## 15. Publication roadmap','',
'1. Finish theorem/priority and source-package review of FJ, BT, P01 and P02. Their distinct packages are strongest; BT enumeration coverage and P01/P02 exact model quantifiers are priority checks.','2. Reconcile GU current nonlinear claims with its fresh review, and CO 14-page rule/completeness package with recoverable current implementation. A new empirical campaign is a separate scoped task, not part of this file cleanup.','3. Reconcile IP/SP against AU/PC contracts; publish only the defensible model-specific contribution. Assess FO/PL as coherent frameworks with explicit classical content.','4. Develop one GR carrier-changing theorem/certificate target. Keep design interactions as a subdirection; promote only with a distinct constrained result.','5. Recover one SC endpoint and raw evidence before more drafting. Leave guard/atlas briefs deferred; preserve companions/register as stable references.','',
'The bounded primary-literature check confirms close antecedents, not absence of prior art: [Barmak on poset fiber criteria](https://arxiv.org/abs/1005.0538), [Bernardi–Klivans on higher-dimensional rooted forests](https://arxiv.org/abs/1512.07757), [de Beaudrap on computation over scalar rings](https://arxiv.org/abs/1405.7381), and [Abramsky–Brandenburger on contextuality/global sections](https://arxiv.org/abs/1102.0264). These are background boundaries for GR/BT/P01; a complete priority audit remains required.','',
'## 16. Remaining uncertainties and checks not completed','',
'This pass does not independently certify every proof, external novelty, all archive code or all historical dataset rows. PDF text extraction can miss visual/formula detail; TeX contracts were preferred and no visual-layout edit was made. No full LaTeX builds, broad benchmark campaign or six-vertex exhaustive thinning rerun was performed. Seven-state and nonlinear guard checks were rerun in isolated workspace copies. The guard verifier required only an output-path substitution in the temporary copy; the repository source remains unchanged.','',
'Known defects retained: historical 24-page compiler source references missing ../04_figures notation/PNG assets; the foundations 20,873-check output lacks its matched checker in the inspected loose tree; v0.3 TeX is empty; some historic verifiers refer to /mnt/data; old audit digest discrepancies remain historical. The dependency scan records missing paths before/after rather than guessing a replacement. Archive indexing can reveal candidate recovery material but does not certify an exact replacement. No external CM Quantum or Downloads tree was modified or assumed fully preserved by this repository.','',
'## 17. Verification and repository status','',
'The initial Git state was exactly the requested commit with only three untracked portfolio ZIPs. All retained loose bytes and archive members were indexed. The immediate deletion gate rechecked hashes against tracked retained files. The final verifier checks every original file has an equal retained canonical byte stream, every removed path maps to a retained equal hash, every relocation is unchanged, every surviving project has a current entry point/claim statement/review/reproducibility/history index, all generated links resolve, and all current manifests match final bytes.','',
'Machine-readable final results are in the root `PARTITION_VERIFICATION_RECEIPT.json`; complete preservation mapping is in the register evidence directory. Final hashes for all project content are in each top-level SOURCE_MANIFEST_SHA256.csv, and the receipt hashes those manifests and both report copies without a circular self-hash. A commit cannot embed its own hash; the local commit hash is returned in the completion receipt and final response. No push is performed.','',
'The staged diff and status are reviewed before the local commit. Mathematical test results: exact seven-state verifier **PASS**; nonlinear guard symbolic/probe/grid verifier **PASS** with isolated output-path adaptation. Hash, dependency, semantic-rescreen, manifest results are in the verification receipt; the post-commit clean-state check is recorded in the separate completion receipt delivered with the final response.','',
'## Appendix A. All 171 original-folder pairs','', '| Original pair | Exact hash groups | Files / bytes in A; in B | Substantive relationship classes |','|---|---|---|---|']
for x in opairs:report.append(f"| {x['folder_a']} / {x['folder_b']} | {x['hash_groups']} | {x['a_files']} / {x['a_bytes']}; {x['b_files']} / {x['b_bytes']} | "+'; '.join(sorted({r['kind'] for r in x['relationships']}))+' |')
report+=['','Appendix A is the compact original-folder matrix; pairwise_original.json retains every associated correspondence, owner, treatment and residue, including one-to-many mixed-folder relationships.','', '## Appendix B. Retained cross-folder exact evidence and manuscript-package copies','', 'These repeated byte streams remain intentionally for frozen provenance or self-contained packages. Canonical claim ownership is given above. Administrative generated files are not intellectual overlap.','']
retained=[dict(x,path=plan['mapping'][x['path']],folder=plan['mapping'][x['path']].split('/')[0]) for x in rows if plan['mapping'][x['path']]]
groups=collections.defaultdict(list)
for x in retained:groups[x['sha256']].append(x)
for h,g in sorted(groups.items()):
 if len({x['folder'] for x in g})<2:continue
 report+=['- SHA-256 `'+h+'`, '+str(g[0]['bytes'])+' bytes: '+ '; '.join('`'+x['path']+'`' for x in g)+'. Retained as package-relative evidence/history; manuscript claim ownership is unchanged.']
put('CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md','\n'.join(report))
put(REG+'/CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md','\n'.join(report))
# Keep the exact reconstruction/verification procedure with the evidence.
for name in ['inventory.py','checks.py','partition_data.py','make_plan.py','apply_partition.py','overlap.py','build_deliverables.py']:
 put(EVID+'/TOOLS/'+name,(W/name).read_text(encoding='utf-8'))
print(json.dumps({'staged_files':sum(p.is_file() for p in S.rglob('*')),'archive_members_exposed':len(extractions),'report_bytes':(S/'CM_LM_UNIQUE_PROJECT_PARTITION_AND_OVERLAP_REPORT.md').stat().st_size,'inventory_rows':len(inv),'archive_member_rows':len(member_inv),'original_dispositions':len(dispositions)},indent=2))
