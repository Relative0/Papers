"""Validate audit deliverables and record version-scoped coverage; no source edits."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,re,subprocess
OUT=Path(__file__).resolve().parent;REPO=OUT.parents[2]
required=['adversarial_audit.md','claim_audit.csv','proposed_corrections.md','source_snapshot.json','reproduction_results.json']
for name in required:assert (OUT/name).is_file() and (OUT/name).stat().st_size>0,name
rows=list(csv.DictReader((OUT/'claim_audit.csv').open(encoding='utf-8-sig',newline='')))
assert len(rows)==73 and len({r['claim_id'] for r in rows})==73
assert all(all(r[k] for k in r) for r in rows)
assert {r['severity'] for r in rows}<={'critical','major','minor','none'}
snap=json.loads((OUT/'source_snapshot.json').read_text())
for source in snap['source_hash_recheck']:
    observed=hashlib.sha256(Path(source['path']).read_bytes()).hexdigest()
    source['final_read_hash_matches']=observed==source['sha256']
    source['current_sha256']=observed
    source['final_read_scope']='Audited original hash retained; a different current hash is a later source version, not retroactive audit coverage.'
snap['source_hash_final_read_utc']=datetime.now(timezone.utc).isoformat()
snap['final_thread_status_observation']=json.loads((OUT/'thread_status_cutoff.json').read_text())
snap['coverage_cutoff_utc']='2026-10-13T16:08:12Z'
snap['coverage_policy']='Initial three completed dossiers at frozen hashes. Later extraction and semantic-compilation continuations are pending/unreviewed; not an evolving-portfolio guarantee.'
reviewed=[]
for direction in ['representational_limits','certified_boolean_extraction','semantic_compilation']:
    base=OUT/'dossier_snapshots'/direction
    for name in ['research_dossier.md','references.bib','claim_matrix.csv']:
        p=base/name;assert p.exists(),p
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        immutable=OUT/'immutable_snapshots'/direction/digest[:16]/name
        assert immutable.exists() and immutable.read_bytes()==p.read_bytes()
        record={'direction':direction,'snapshot_path':str(immutable),'sha256':digest,'status':'initial completed dossier component reviewed; later versions excluded'}
        if name=='claim_matrix.csv':
            matrix=list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
            record['source_claim_rows']=len(matrix)
        reviewed.append(record)
snap['reviewed_dossier_components']=reviewed
pending=[]
for direction in ['certified_boolean_extraction','semantic_compilation']:
    base=REPO/'output/research/palo_paper_directions_2026-10-13'/direction
    for p in base.rglob('*'):
        if p.is_file() and p.suffix.lower() in ['.tex','.md','.py','.json','.csv','.pdf'] and len(p.relative_to(base).parts)>1:
            if p.relative_to(base).parts[0] not in ['literature','sources']:
                pending.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                                'mtime_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat(),
                                'status':'later continuation; metadata snapshot only, no mathematical endorsement'})
snap['later_continuation_paths']=pending
snap['web_primary_review']=[
 {'url':'https://www.numdam.org/item/AIF_1989__39_3_611_0.pdf','version':'1989 published 23-page archive with cover','coverage':'opening example, Proposition2.4, Section4/Theorem4.2'},
 {'url':'https://arxiv.org/pdf/2107.01061v2','version':'2021-12-30 author v2; cover January3,2022; journal2022','coverage':'Thm3.6,Cor3.12,Remark3.13; normalized-weight comparison'},
 {'url':'https://web.cs.ucla.edu/~sherstov/pdf/hshs.pdf','version':'47-page author journal manuscript; journal2013; earlier arXiv2009 distinct pagination','coverage':'Thm1.10 and majority/rational-composition premises; complete lower-bound proof not independently re-proved'},
 {'url':'https://ftp.cs.wisc.edu/pub/users/prem/rfuns.pdf','version':'65-page Shapiro2007 author manuscript','coverage':'Sections3.3/3.6; R-conjunction and finite regularity'},
 {'url':'https://arxiv.org/pdf/1002.0941v1','version':'2010-02-04 deposit; journalonline2010/issue2011; later typesetting date ignored','coverage':'factor/coding propositions and relevant proofs'},
 {'url':'https://emis.de/ft/11056','version':'Averkov2009 published12pp,271–282','coverage':'Lemma2.1,Thm2.2 and proof PDFpp4–6'},
 {'url':'https://proceedings.neurips.cc/paper/1994/file/bea5955b308361a1b07bc55042e25e54-Paper.pdf','version':'NIPS7,1994 conference/1995 proceedings','coverage':'Sections2–3 regional validity intervals and rule verification'},
 {'url':'https://arxiv.org/html/2509.16547v1','version':'2025-09-20 arXivv1; IJCNN metadata separate','coverage':'rule definitions, complexity statements, broad priority wording; full complexity proof not independently audited'},
 {'url':'https://proceedings.mlr.press/v80/xu18h/xu18h.pdf','version':'ICML2018/PMLR80 fullpaper','coverage':'Definition1,Proposition2 and syntax-independence'},
 {'url':'https://arxiv.org/pdf/2206.00426','version':'NeurIPS2022 author fulltext','coverage':'Sections3.1–3.3, compatible circuits; cachedPDFhash recorded'},
 {'url':'https://arxiv.org/html/2402.13782v1','version':'2024arXivv1 with IJAR171,109130 journalmetadata','coverage':'compilation/semiring properties and gradient evaluation'},
 {'url':'https://arxiv.org/pdf/2605.13845v2','version':'2026-05-14v2; preprint','coverage':'law/gradient discussion; Thm3.7 infinite-hardness premise'},
 {'url':'https://arxiv.org/html/2605.13348v3','version':'v3,2026preprint','coverage':'propositional pQLL quantitative adequacy Thm6.4; not independently proof-audited in full'},
 {'url':'https://drops.dagstuhl.de/storage/00lipics/lipics-vol337-fscd2025/html/LIPIcs.FSCD.2025.2/LIPIcs.FSCD.2025.2.html','version':'FSCD2025 published invitedpaper','coverage':'Section4.2 backends,4.2.4 soundness and limitations'},
 {'url':'https://arxiv.org/pdf/2301.11683v1','version':'January2023arXiv posting; NeurIPS2022 paper','coverage':'Thm1,dynamics abstraction, learner/certifier target'},
 {'url':'https://ojs.aaai.org/index.php/AAAI/article/download/40965/44926','version':'AAAI2026published10-pagepaper','coverage':'finite bounded-integer states;Theorems7–8; not general continuous termination'},
 {'url':'https://link.springer.com/article/10.1007/s00605-010-0224-x','version':'publisherrecord','coverage':'2010online/2011issue metadata; fulljournaltextsubscriptionnot accessed'},
 {'url':'https://www.csl.sri.com/users/mkim/pub.html','version':'authorpublicationrecord,accessed2026-10-13','coverage':'PALO2022journalidentity; related2019reportdistinction'}]
snap['remaining_source_access_limits']=['Complete PALO supplied-author versus final-journal text comparison unavailable.',
 'Exact-title Thrun1993 report inaccessible; alternate author copy distinguished from NIPS1995 primary text.',
 'Full1992 signature/flatness and1993 correction and original Russian R-function texts not obtained.',
 'Publisher Wurm fulltext unavailable; IJCNN metadata does not certify equality to audited arXivv1.',
 'Broader Scallop/atlas implementation equivalence and full specialist ring proofs not independently audited.']
(OUT/'source_snapshot.json').write_text(json.dumps(snap,indent=2)+'\n',encoding='utf-8')
for args,name in [(['status','--short'],'final_git_status.txt'),(['diff','--stat'],'final_git_diff_stat.txt')]:
    r=subprocess.run(['git',*args],cwd=REPO,capture_output=True,text=True)
    (OUT/name).write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf-8')
repro=json.loads((OUT/'reproduction_results.json').read_text())
assert repro['independent_total_assertions']==10990
assert all(s['matches_report'] for s in snap['source_hash_recheck'])
quality={'status':'PASS','claim_rows':len(rows),'critical_findings':0,'major_publication_risks':4,'minor_repairs':4,
         'current_sources_matching_audited_hash':sum(s['final_read_hash_matches'] for s in snap['source_hash_recheck']),
         'changed_source_versions':[s['key'] for s in snap['source_hash_recheck'] if not s['final_read_hash_matches']],
         'reviewed_initial_dossier_components':len(reviewed),'later_unreviewed_paths':len(pending),
         'tracked_diff_stat_matches_initial':(OUT/'initial_git_diff_stat.txt').read_bytes()==(OUT/'final_git_diff_stat.txt').read_bytes(),
         'git_status_matches_initial':(OUT/'initial_git_status.txt').read_bytes()==(OUT/'final_git_status.txt').read_bytes(),
         'check_scope':'Required files, unique CSV IDs/nonempty fields, JSON readability, source/snapshot hashes and recorded result consistency. No omnibus correctness guarantee.',
         'checked_utc':datetime.now(timezone.utc).isoformat()}
(OUT/'quality_checks.json').write_text(json.dumps(quality,indent=2)+'\n',encoding='utf-8')
(OUT/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256((OUT/name).read_bytes()).hexdigest()+'  '+name for name in required+['independent_checks.py','additional_checks.py','quality_checks.json'])+'\n',encoding='utf-8')
print(json.dumps(quality,indent=2))
