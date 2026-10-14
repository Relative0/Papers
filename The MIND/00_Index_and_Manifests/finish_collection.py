from pathlib import Path
import json,hashlib,collections,zipfile,os,csv,subprocess
A=Path(__file__).resolve().parent;M=A.parent;R=M.parent
P1=M/'01_Papers/01_Observation_Refinement_and_Concept_Differentiation';P2=M/'01_Papers/02_Hierarchical_Concepts_Paper_U';P3=M/'01_Papers/03_Structured_Boolean_Factorization';S=M/'02_Shared_and_Exploratory_Research';OLD=M/'90_Preserved_Sources/Original_The_MIND';EX=M/'90_Preserved_Sources/Extracted_Archives'
def read(n):return json.loads((A/n).read_text(encoding='utf-8'))
def out(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:f.write(data if isinstance(data,str) else json.dumps(data,indent=2,ensure_ascii=False))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def link(label,p,base):return f'[{label}](<{os.path.relpath(p,base).replace(chr(92),"/")}>)'
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 with src.open('rb') as i,dst.open('xb') as o:
  import shutil;shutil.copyfileobj(i,o)
 assert sha(src)==sha(dst)
 return {'source':str(src),'destination':str(dst),'sha256':sha(dst)}
additional=[]
# Expose earlier manuscript versions without changing their source packages.
tr=P1/'Supporting_Research/Transferred_Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29'
for ver,folder in [('v0.1',tr/'04_OBSERVATION_REFINEMENT_DRAFT'),('v0.2',tr/'04_OBSERVATION_REFINEMENT_DRAFT'),('v0.3',tr/'01_CURRENT_MANUSCRIPT')]:
 for src in folder.glob(f'Observation_Refinement_Descent_and_Cone_Draft_{ver}.*'):
  if src.suffix in ['.tex','.pdf']:additional.append(copy(src,P1/'Manuscript_Versions'/ver/src.name))
v1=P2/'Supporting_Research/Original_Theme_Ultrametrics/PAPER_U_RESOLUTION_LIMITED_ULTRAMETRIC_CONCEPTS_DRAFT_v0.1'
for src in v1.iterdir():
 if src.suffix in ['.tex','.pdf','.bib']:additional.append(copy(src,P2/'Manuscript_Versions/v0.1_Original_Draft'/src.name))
for src in [R/'Structured Factorization/phase5b_output/STRUCTURED_FACTORIZATION_PHASE5B_2026-09-29.zip',R/'Structured Factorization/phase5b_output/STRUCTURED_FACTORIZATION_PHASE5B_2026-09-29.zip.sha256']:
 additional.append(copy(src,P3/'Original_Packages'/src.name))
out(A/'additional_reading_copies.json',additional)
# Resolve explicitly linked related publications without relocating their workflows.
related_paths=[R/'ProLT.zip',R/'ProLT-Homology.zip',R/'ProLT-Homology/HISTORY/ORIGINAL_RELEASES/ProLT_Homology - 24-9-2026.zip',R/'CM-LM Publication Program - Reviews and Registers/08_PORTFOLIO_PROGRAM_REPORTS_20260921/REPRODUCTION_SUPPLEMENT.zip']
related=[];related_members=[]
for p in related_paths:
 if not p.exists():related.append({'source':str(p),'reason':'Referenced related-publication artifact unavailable'});continue
 related.append({'source':str(p),'size':p.stat().st_size,'sha256':sha(p),'scope':'linked_related_publication','organized_location':str(p),'preserved_location':str(p),'disposition':'linked original retained','reason':'Existing separate publication program; no reorganization authorized.'})
 with zipfile.ZipFile(p) as z:
  for i in z.infolist():
   b=z.read(i) if not i.is_dir() else b''
   related_members.append({'archive':str(p),'member':i.filename,'kind':'directory' if i.is_dir() else 'file','size':i.file_size,'sha256':hashlib.sha256(b).hexdigest() if not i.is_dir() else None,'organized_location':str(p)+'!/'+i.filename,'disposition':'related-publication archive retained at original path; CRC read verified; not extracted or reorganized'})
out(A/'linked_related_inventory.json',related);out(A/'linked_related_archive_members.json',related_members)
source=read('source_map_before_relocation.json')+related
out(A/'source_manifest.json',source)
with (A/'source_manifest.csv').open('x',encoding='utf-8-sig',newline='') as f:
 cols=['source','size','sha256','scope','organized_location','preserved_location','disposition','reason'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(source)
members=read('archive_member_map.json')
for r in members:
 r['extracted_location']=str(EX/Path(r['staging']).relative_to(A/'staging'))
 if r['kind']=='directory':r['organized_location']=r['extracted_location']
out(A/'archive_members_final.json',members)
# Expand canonical member inventories for EVERY local archive occurrence, including
# identical and recursively nested ZIPs. Original paths remain provenance keys.
ar=read('archive_inventory_extended.json');canonical=collections.defaultdict(list)
for r in members:canonical[r['archive_sha256']].append(r)
occ=[]
def expand(h,origin,depth=0):
 if depth>12:raise ValueError('Archive depth exceeded')
 for m in canonical[h]:
  row={'source':origin+'!/'+m['member'],'archive':origin,'archive_sha256':h,'member':m['member'],'kind':m['kind'],'size':m.get('size'),'sha256':m.get('sha256'),'organized_location':m['organized_location'],'extracted_location':m['extracted_location'],'disposition':m['disposition']};occ.append(row)
  if m['kind']=='file' and m['member'].lower().endswith('.zip') and m['sha256'] in canonical:expand(m['sha256'],row['source'],depth+1)
for r in source:
 if str(r['source']).lower().endswith('.zip') and r.get('sha256') in canonical:expand(r['sha256'],r['source'])
out(A/'archive_occurrence_manifest.json',occ)
reference=read('reference_register.json')
for r in reference:
 if r['artifact'] in ['2024-9-2026.zip','24-9-2026.zip']:
  r.update(status='resolved truncated filename / URL encoding',actual_artifact='ProLT_Homology - 24-9-2026.zip',available_locations=[str(related_paths[2])])
 if r['artifact']=='REPRODUCTION_SUPPLEMENT.zip':r.update(status='available; related publication program retained',available_locations=[str(related_paths[3])])
out(A/'reference_register_final.json',reference)
# Curated navigation; these are organizational descriptions, not scientific edits.
p1pdf=P1/'Current_Manuscript/Observation_Refinement_Descent_and_Cone_Draft_v0.5.pdf'
p2pdf=P2/'Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications/Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3.pdf'
p3report=P3/'Current_Research_Status/PHASE5B_MASTER_REPORT.md'
cross=[
 {'original_theme':'Gluing','primary_destination':'Structured Boolean Factorization','related_destination':'Observation Refinement; shared historical sources','evidence':'GLUING_CONCEPTS_RESEARCH_PACKAGE README recommends succinct structured factorization; Phase 3/4/5 notes and continuity snapshot trace the same finest carrier/semantic partition problem.','later_findings':'Phase 3 bounded incidence width; Phase 4 direct/residual SDD extraction; Phase 5 vtree alignment/defects; Phase 5B mathematical-note survival and pilot runtime NO-GO; later live-vtree tooling GO is separate.'},
 {'original_theme':'Symmetry Breaking and Consciousness','primary_destination':'Shared research / Measurement and RF-IDENT','related_destination':'Observation Refinement; Paper U; existing ProLT papers','evidence':'CM measurement audit separates observation refinement from conditioning; two-operation handoff U1-U6 and height-two gate; bounded subclass and independent review.','later_findings':'U2 quotient-order, U4 cone terminology, U6 fine measurability and A1 preserved; fixed-library branch cancellation and repair dynamics; bounded-height-two feasibility theorem reviewed. No independent publication manuscript identified.'},
 {'original_theme':'Unfolding','primary_destination':'Observation Refinement and Concept Differentiation','related_destination':'Structured Factorization; shared two-operation calculus','evidence':'Transferred START_HERE and manuscript title establish Successive Concept Differentiation as Observation Refinement; convergence/repair handoffs establish v0.3 -> v0.4 -> v0.5.','later_findings':'Carrier splitting, matching formula, interaction-core spectral sequence, signed d2 witnesses, torsion and bounded referee repairs. Historical Paper F bridge is a research label, not proof of a fourth manuscript.'},
 {'original_theme':'Ultrametrics and Unconsciousness','primary_destination':'Hierarchical Concepts Under Finite Resolution (Paper U)','related_destination':'Shared historical thesis; historical Paper U/F bridge','evidence':'v0.1 draft and transfer closure v0.2; first independent review v0.3; later fresh referee and rebuilt recovery provenance.','later_findings':'Observation quotients, completion, adaptive symmetry; narrowed synthesis/correction note. Two materially different v0.3 source variants retained; rebuilt variant is recommended.'}
]
out(A/'paper_theme_crosswalk.json',cross)
lines=['# Original themes and resulting papers','', '| Original theme | Main home | Later findings / boundary |','|---|---|---|']
for r in cross:lines.append(f"| {r['original_theme']} | {r['primary_destination']} | {r['later_findings']} |")
lines += ['', 'The four themes are historical research entry points, not four established paper titles. RF-IDENT and its review belong together in the measurement branch; they were packaged beside the observation-refinement manuscript, but have not been integrated into v0.5. The historical Paper F label spans gluing/unfolding ideas and is not assigned a separate paper without an independent manuscript.','', 'Evidence and exact origins are in `paper_theme_crosswalk.json`, `chat_evidence/`, and the source/archive manifests. Existing ProLT, ProLT-Homology, CM/LM and chain-ring papers occur as reference sources; their publication homes remain outside this collection.']
out(A/'THEME_CROSSWALK.md','\n'.join(lines)+'\n')
out(P1/'README.md',f'''# Successive Concept Differentiation as Observation Refinement

Start with {link('the current v0.5 PDF',p1pdf,P1)}. The adjacent TeX is byte-identical to the delivered referee-repair source. Subtitle: **Carrier Splitting, Interaction-Core Homology, and Descent**.

## Version history
- `Manuscript_Versions/v0.1` and `v0.2`: early descent/cone drafts.
- `Manuscript_Versions/v0.3`: frozen carrier-splitting baseline; later matching section was initially unmerged.
- `Manuscript_Versions/v0.4_Convergence`: matching and interaction results integrated, descent-extension claim corrected.
- `Manuscript_Versions/v0.5_Referee_Repairs`: latest integrated manuscript, response, signed witness supplement, receipts and historical build files.

## Research, review and reproduction
{link('Referee response',P1/'Manuscript_Versions/v0.5_Referee_Repairs/RESPONSE_TO_REFEREE.md',P1)}; {link('independent v0.4 review',P1/'Reviews/Independent_Expert_Review_of_v0.4/INDEPENDENT_EXPERT_REPORT.md',P1)}; {link('interaction-core handoff',P1/'Supporting_Research/Interaction_Core_Gate/HANDOFF_TO_MASTER.md',P1)}.

Sources: the original Unfolding theme, consolidated transferred research, carrier-splitting and higher-dimensional gates. Original delivery ZIPs are in `Original_Packages`; archive-only predecessors are indexed in `Archive_Only_Content`. Scientific bytes and original filenames are unchanged. Historical scripts may embed old absolute paths: see {link('preserved source layout',OLD,M if False else P1)} and the relocation manifest before rerunning in a disposable copy.

RF-IDENT is related follow-up research in {link('Measurement and RF-IDENT',S/'Measurement_and_RF_IDENT/README.md',P1)}, not part of this integrated v0.5. The combined delivery ZIP does not establish manuscript identity.

Open questions: publication novelty, human/venue review, intended public author attribution (Brian Theory versus Brian Droncheff in different historical sources), and optional nonunit C4 secondary-differential research. This organization does not resolve them or rerun scientific experiments.
''')
out(P2/'README.md',f'''# Hierarchical Concepts Under Finite Resolution — Paper U

Start with {link('the rebuilt v0.3 reading PDF',p2pdf,P2)} and {link('the recovered referee report',P2/'Reviews/Rebuilt_Complete_Review/FINAL_REPORT.md',P2)}. Current subtitle: **Observation Quotients and Adaptive Symmetry**. Recommended delivery: {link('Paper_U_Complete_Rebuilt.zip',P2/'Original_Packages/Paper_U_Complete_Rebuilt.zip',P2)}.

## Versions and recovery provenance
- `Manuscript_Versions/v0.1_Original_Draft`: original ultrametric geometry / observational equivalence draft.
- `Manuscript_Versions/v0.2_Research_Closure`: narrowed research-closure manuscript.
- `Manuscript_Versions/v0.3_Initial_Review`: first reviewed version, retained separately.
- `Current_Manuscript/v0.3_Rebuilt_Referee_Clarifications`: later same-numbered version with the fresh referee's three minor clarifications. Distinct hashes identify it; **v0.3 filenames alone do not identify the version**.

The original `Paper_U_Fresh_Referee_2026-09-29` output folder and `PAPER_U_FRESH_INDEPENDENT_REFEREE_COMPLETE_2026-09-29.zip` were not found. The later chat explicitly recommends the rebuilt ZIP. Its README/receipt state that review documents were reconstructed from the task record, not restored byte-for-byte. Both the original review/transfer packages and this replacement are preserved. The collection is consequently not a complete recovery of every historical artifact.

`Reviews` holds the initial review handoff, recovered complete review and supporting historical/priority/tree checks. `Supporting_Research` contains the original ultrametric theme and v0.2 account transfer. Reproduction scripts/checks remain with their intact review bundles, with a directory guide in `Reproducibility`. The sibling {link('original review workspace',R/'Paper_U_Independent_Review_2026-09-29',P2)} remains in place because its packaging/recovery workflow uses those paths.

Open questions: exact adaptive-criterion priority, original mathematical novelty, source-access limitations (including Lauro-Grotto page images), and venue fit. The existing verdict concerns a short synthesis/correction note; no stronger scientific status is inferred here.
''')
out(P3/'README.md',f'''# Structured Boolean Factorization — evolving theorem note

Start with {link('the Phase 5B master report',p3report,P3)}. The latest available manuscript note is {link('Phase 5: Vtree Alignment and Higher-Order Four-Corner Defects in Exact Boolean Factorization',P3/'Manuscript_Versions/Phase5/THEOREM_NOTE_DRAFT.pdf',P3)}; read it with the later {link('Phase 5B proofs and corrections',P3/'Current_Research_Status/THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md',P3)}. There is no newly integrated Phase 5B manuscript in the inspected material.

The manuscript family is identified by the same carrier-constrained finest Boolean AND-factorization problem and the documented phase continuity, not by the ZIP dates. Retained earlier titles: Phase 3 **Carrier-Aware Boolean Factorization at Bounded Incidence Width**; Phase 4 **Direct and Residual Factor Extraction for Carrier-Constrained Boolean Structures**. `Manuscript_Versions` contains these separate notes. They are an evolving research-note line, not asserted to be three publication-ready papers.

`Supporting_Research/Original_Theme_Gluing` preserves the original research theme. `Supporting_Research/Structured_Factorization_Snapshot` preserves continuity, Phase 5B code/data/reviews and the later live-vtree probe. `Original_Packages` contains the verified Phase 5B delivery and named Downloads transfers. Archive-only materials are indexed separately.

The sibling {link('Structured Factorization workspace',R/'Structured Factorization',P3)} remains the active workflow location, including its environment. Existing chats reference its fixed paths. The copied snapshot is a reading collection, not a relocated runnable environment.

Status: Phase 5B mathematical-note survival, algorithmic NO-GO for the frozen pilot; later live-vtree **tooling GO** does not overturn that pilot result. Novelty and external theorem-level priority review remain unresolved. No campaign integration, retuning, benchmark rerun or new research is performed by this organization.
''')
branch=S/'Measurement_and_RF_IDENT'
out(branch/'README.md',f'''# CM measurement, two-operation calculus and RF-IDENT

This is a shared research branch with proposed paper sequences and reviewed theorems, but no separate integrated publication manuscript identified in the inspected sources. It is not a fourth current paper.

Start with {link('the bounded-height-two theorem',branch/'Supporting_Research/Bounded_Height2_RF_IDENT/THEOREM.md',branch)} and {link('its independent review',branch/'Reviews/Bounded_Height2_Independent_Review/REVIEW.md',branch)}. For prerequisites use {link('the fixed-library gate audit',branch/'Supporting_Research/Height2_Fixed_Library_Gate/research/HEIGHT2_ADAPTIVE_MASTER_AUDIT.md',branch)}.

History: Symmetry Breaking and Consciousness -> CM measurement audit -> two-operation refinement/conditioning calculus -> unification and U1-U6 hostile audit -> fixed-library height-two gate -> bounded-height-two RF-IDENT theorem -> independent proof/verifier review. The transfer packages retain the U2 quotient-order repair, U4 cone terminology, U6 fine-measurability hypothesis and A1, plus inherited ProLT corrections.

The exact subclass has a global least and greatest element and an antichain of middle states. “Bounded” describes these endpoints, not a bound on state count. General height-two feasibility and optimal depth remain open. The independent review found no blocking mathematical gap; it documented the verifier's explicit-order-input limitation and empty-carrier constructor issue. The theorem and review stay together; neither is relabeled as the unfolding manuscript or silently merged into v0.5.

Scripts, results and receipts remain in their original research/review groups. For relative sibling links use the preserved original layout; historical absolute paths need an explicit future adaptation before rerunning. The combined observation-refinement/RF-IDENT delivery is under `../Original_Packages`; co-packaging records a relationship, not a single-paper identity.
''')
out(S/'README.md',f'''# Shared and exploratory research

- {link('Measurement and RF-IDENT',branch/'README.md',S)}: original symmetry/measurement theme, two-operation framework, fixed-library gate and reviewed bounded subclass.
- `Historical_Primary_Sources`: unchanged thesis / Logical Complexes source copies, distinguished by hash where needed.
- `Chat_Attachments`: all four directly referenced pasted-text attachments, copied and verified.
- `Original_Packages`: shared transfers and the combined observation-refinement/RF-IDENT delivery.
- `Archive_Only_Content`: material found only in original packages, with its complete archive-member mapping in the index.

Related publication homes retained in place: {link('General ProLT Observation Refinement',R/'General ProLT Observation Refinement (Research Direction)/README_FIRST.md',S)}, {link('ProLT',R/'ProLT/README_FIRST.md',S)}, {link('ProLT-Homology',R/'ProLT-Homology/README_FIRST.md',S)}. Their source copies inside transfers are supporting references, not additional MIND manuscript identities. The shared {link('reproduction supplement',related_paths[3],S)} remains in its publication-program home. No unrelated publication project was reorganized.

The historical Paper U / Paper F bridge is exploratory: resolution refinement and structural unfolding/gluing are different operations. It does not establish a separate current Paper F manuscript, nor authorize expanding Paper U into CM, quantum or ProLT claims.
''')
# Practical category guides keep related bundles intact rather than rewriting code paths.
for paper in [P1,P2,P3]:
 repro=paper/'Reproducibility';review=paper/'Reviews'
 out(repro/'README.md',f'''# Reproducibility material

Code, data, receipts and original logs are retained with their intact research/review bundles under this paper's `Supporting_Research`, `Reviews`, `Manuscript_Versions` and `Archive_Only_Content`. Packaging helpers, where supplied, are in `Packaging`. Use {link('this paper README',paper/'README.md',repro)} to select the correct version.

This organization verified file bytes, archive CRCs and recorded hashes; it did not rerun scientific experiments or rebuild manuscripts. Historical scripts can contain original absolute paths. Work in a disposable copy and resolve paths deliberately before rerunning; do not execute a packaging script in the preserved source area. {link('Source manifest',A/'source_manifest.csv',repro)} records all original and new locations.
''')
 if not (review/'README.md').exists():out(review/'README.md',f'''# Review guide

See {link('paper status and version history',paper/'README.md',review)}. Review documents retain their original scope, verdict and date. For Structured Factorization, the Phase 5B `reviews` folder and `HOSTILE_REVIEW_LEDGER.md` are in the preserved reading snapshot under `Supporting_Research/Structured_Factorization_Snapshot/phase5b_output`. Reviews are not evidence of external human refereeing unless the source explicitly establishes that.
''')
out(M/'90_Preserved_Sources/README.md','''# Preserved sources — provenance, not the reading entry point

`Original_The_MIND` contains every original local file and directory, relocated only after a verified reading copy existed. The original relative layout is preserved; historical absolute paths are not rewritten. Nothing was deleted or scientifically edited.

`Extracted_Archives` contains safely extracted unique ZIP payloads, keyed by the first 16 hexadecimal characters of each full SHA-256. Paths were checked for traversal, absolute/drive paths, links and case collisions; CRC reads succeeded. Full hashes and every occurrence, including nested and identical archives, are in the index manifests. Extraction here is preserved evidence, not a current-version recommendation.

Sibling and Downloads originals were left in place. Exact duplicates are recorded in `../00_Index_and_Manifests/duplicate_groups.json`; none was silently discarded. Start from the root README to read the papers.
''')
out(M/'01_Papers/README.md',f'''# Paper collections

1. {link('Observation Refinement and Concept Differentiation',P1/'README.md',M/'01_Papers')} — integrated manuscript v0.5.
2. {link('Hierarchical Concepts Under Finite Resolution — Paper U',P2/'README.md',M/'01_Papers')} — rebuilt, clarified v0.3 with a documented recovery caveat.
3. {link('Structured Boolean Factorization',P3/'README.md',M/'01_Papers')} — evolving theorem note; latest manuscript Phase 5, status and corrections Phase 5B.

The two-operation / RF-IDENT work is retained as shared research until a distinct manuscript establishes a separate paper.
''')
out(M/'README.md',f'''# The MIND — paper-centered research collection

Organized 30 September 2026 from manuscript identity, project history and verified source packages. **Organization of accessible material is complete; recovery of all historical material is not.** The original fresh Paper U referee outputs are unavailable; their explicitly reconstructed replacement is retained. Earlier account chats are represented by transferred records, not directly accessible chat history.

| Paper / note | Recommended start | Status |
|---|---|---|
| Successive Concept Differentiation as Observation Refinement | {link('v0.5 PDF',p1pdf,M)} · {link('README',P1/'README.md',M)} | Latest integrated draft after bounded referee repairs |
| Hierarchical Concepts Under Finite Resolution (Paper U) | {link('rebuilt clarified v0.3 PDF',p2pdf,M)} · {link('README',P2/'README.md',M)} | Short synthesis/correction note; reconstructed review provenance |
| Structured Boolean Factorization | {link('Phase 5B status',p3report,M)} · {link('README',P3/'README.md',M)} | Phase 5 manuscript plus later research corrections; novelty unresolved |

{link('Measurement and RF-IDENT',branch/'README.md',M)} holds the reviewed bounded-height-two result with its independent review and fixed-library prerequisites. It is related research, not an additional integrated manuscript. {link('Theme crosswalk',A/'THEME_CROSSWALK.md',M)} connects all four original themes and later findings.

## Navigation
- `01_Papers/`: three paper/note collections, each with current reading pointers, versions, research, review, reproduction and packages.
- `02_Shared_and_Exploratory_Research/`: measurement/two-operation/RF-IDENT work, historical sources, cross-paper inputs and attachments.
- `90_Preserved_Sources/`: complete old local layout and safe archive extractions.
- `00_Index_and_Manifests/`: provenance, hashes, chat evidence, archive-member reconciliation and verification reports.

## Provenance and limits
{link('Final verification',A/'FINAL_VERIFICATION.md',M)} · {link('Source-to-location manifest (CSV)',A/'source_manifest.csv',M)} · {link('Full source manifest (JSON)',A/'source_manifest.json',M)} · {link('Every archive occurrence',A/'archive_occurrence_manifest.json',M)} · {link('Exact duplicate groups',A/'duplicate_groups.json',M)} · {link('Unavailable material and unresolved questions',A/'UNRESOLVED_AND_ACCESS.md',M)} · {link('Folder tree',A/'FOLDER_TREE.txt',M)}.

All scientific files and original ZIPs retain their bytes. Original `The MIND` folders moved only after copy verification. The sibling Paper U review and Structured Factorization workspaces, General ProLT research and named Downloads files remain at their original paths; the manifests map these intentional duplicate locations. Scientific claims and journal readiness were not reassessed. No deletion, commit, push or external publication was performed.
''')
print(json.dumps({'source_records':len(source),'archive_occurrences':len(occ),'related_archive_members':len(related_members),'navigation':'written','additional_reading_copies':len(additional)},indent=2))
