"""Extend provenance using actual files and the final frozen review artifacts."""
from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
import json,hashlib,subprocess
OUT=Path(__file__).resolve().parent;REPO=OUT.parents[2]
snapshot=json.loads((OUT/'source_snapshot.json').read_text())
inv=json.loads((REPO/'output/pdf/palo_cm_relationships_2026-10-13/source_inventory.json').read_text())
root=Path('C:/Users/brian/Documents/Math Latex etc/Papers for Publication')
nav=[]
for folder in ['CM LM Boolean Calculus (Research Manuscript)','CM Compiler Computation (Research Manuscript)',
               'Guarded Boolean Dispatch (Methods Note)','Finite Jet Sign Rigidity (Research Manuscript)',
               'Chain Ring Contextuality (Research Manuscript)','Chain Ring Process Semantics (Technical Companion)']:
    for name in ['COLLECTION_README.md','README_FIRST.md']:
        p=root/folder/name
        if p.exists():
            data=p.read_bytes();dest=OUT/'navigation'/folder/name
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            nav.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'snapshot_path':str(dest)})
snapshot['navigation_review']=nav
snapshot['source_hash_recheck']=[{'key':s['key'],'path':s['path'],'sha256':hashlib.sha256(Path(s['path']).read_bytes()).hexdigest(),
                                'matches_report':hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()==s['sha256']} for s in inv['sources']]
lit=[]
for folder,files in [('certified_boolean_extraction/literature',{'averkovbey2010.pdf':[0,2,3,4,5,6],'averkov2010.pdf':[0,1,4],
                        'thrun1995.pdf':[0,1,2,3,7],'thrun1993.pdf':[0,4,5,13,14],'wurm2025.pdf':[0,1,2,3,4,5],'abate2022.pdf':[3,4,5]}),
                     ('semantic_compilation/sources',{'xu2018.pdf':[1,2,4],'amc2017.pdf':[10,11,12,13,14,17],
                        'spl2022.pdf':[3,4,5,14],'semirings2024.pdf':[3,4,9,10,11],'qll2026.pdf':[5,6,7,14],
                        'adequate2026.pdf':[20,21]})]:
    for name,pages in files.items():
        p=REPO/'output/research/palo_paper_directions_2026-10-13'/folder/name
        if p.exists():
            reader=PdfReader(p);dest=OUT/'literature_passages'/name.replace('.pdf','.txt');dest.parent.mkdir(exist_ok=True)
            used=[i for i in pages if i<len(reader.pages)]
            dest.write_text('\n\n'.join(f'PDF PAGE {i+1}\n'+reader.pages[i].extract_text() for i in used),encoding='utf-8')
            lit.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(reader.pages),
                        'extracted_pages':[i+1 for i in used],'passages_path':str(dest),'status':'primary cached PDF; selected passages extracted for audit'})
snapshot['primary_cached_literature']=lit
reader=PdfReader(REPO/'output/pdf/palo_cm_relationships_2026-10-13/palo_cm_relationships.pdf')
dest=OUT/'extracted/SYNTHESIS.txt'
dest.write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+p.extract_text() for i,p in enumerate(reader.pages)),encoding='utf-8')
snapshot['finalized_utc']=datetime.now(timezone.utc).isoformat()
(OUT/'source_snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
for args,name in [(['status','--short'],'final_git_status.txt'),(['diff','--stat'],'final_git_diff_stat.txt')]:
    r=subprocess.run(['git',*args],cwd=REPO,capture_output=True,text=True)
    (OUT/name).write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf-8')
print(json.dumps({'all_seven_source_hashes_match':all(r['matches_report'] for r in snapshot['source_hash_recheck']),
                  'navigation_records':len(nav),'primary_literature_records':len(lit),'report_pages':len(reader.pages)},indent=2))
