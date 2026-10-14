from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[2]
src=REPO/'output/research/palo_paper_directions_2026-10-13'
snapshot=json.loads((OUT/'source_snapshot.json').read_text())
now=datetime.now(timezone.utc).isoformat()
event={'utc':now,'records':[]}
for direction in ['representational_limits','certified_boolean_extraction','semantic_compilation']:
    for name in ['research_dossier.md','references.bib','claim_matrix.csv','proof_notes.md','verification_results.json','checker_results.json','demo_results.json','verify_candidates.py','semantic_contract_checker.py','exact_extraction_demo.py']:
        p=src/direction/name
        if not p.exists():
            if name in ['research_dossier.md','references.bib','claim_matrix.csv']:event['records'].append({'path':str(p),'status':'unavailable'})
            continue
        data=p.read_bytes();dest=OUT/'dossier_snapshots'/direction/name
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        immutable=OUT/'immutable_snapshots'/direction/hashlib.sha256(data).hexdigest()[:16]/name
        immutable.parent.mkdir(parents=True,exist_ok=True)
        immutable.write_bytes(data)
        event['records'].append({'path':str(p),'snapshot_path':str(dest),'sha256':hashlib.sha256(data).hexdigest(),
                                 'immutable_snapshot_path':str(immutable),
                                 'bytes':len(data),'mtime_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat(),
                                 'status':'available snapshot; completion checked separately'})
snapshot.setdefault('refresh_events',[]).append(event)
(OUT/'source_snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'path':r['path'],'status':r['status']} for r in event['records'] if r['path'].endswith('research_dossier.md')],indent=2))
