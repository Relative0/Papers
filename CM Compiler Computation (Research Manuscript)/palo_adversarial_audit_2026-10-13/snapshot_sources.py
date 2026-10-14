"""Read-only source inventory and PDF extraction; all outputs stay beside this file."""
from pathlib import Path
import hashlib, json, shutil, subprocess
from datetime import datetime, timezone
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
BASE = REPO / 'output/pdf/palo_cm_relationships_2026-10-13'
DIRECTIONS = REPO / 'output/research/palo_paper_directions_2026-10-13'

def record(p, role, copy=False):
    p = Path(p)
    if not p.exists():
        return {'path': str(p), 'role': role, 'status': 'unavailable'}
    data = p.read_bytes()
    r = {'path': str(p), 'role': role, 'bytes': len(data),
         'sha256': hashlib.sha256(data).hexdigest(),
         'mtime_utc': datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
         'status': 'snapshot; producer completion not yet established'}
    if copy:
        relative = p.relative_to(REPO)
        dest = OUT / 'snapshots' / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        r['snapshot_path'] = str(dest)
    return r

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for name in ['palo_cm_relationships.tex','palo_cm_relationships.pdf','source_inventory.json',
                 'verify_bridges.py','verification_results.json','README.txt','build_status.txt','quality_checks.json']:
        records.append(record(BASE/name, 'synthesis', True))
    inv = json.loads((BASE/'source_inventory.json').read_text())
    for item in inv['sources']:
        p = Path(item['path'])
        r = record(p, item['key'])
        r['report_source_hash_matches'] = r.get('sha256') == item['sha256']
        reader = PdfReader(p)
        r['pages'] = len(reader.pages)
        dest = OUT / 'extracted' / (item['key']+'.txt')
        dest.parent.mkdir(exist_ok=True)
        dest.write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+page.extract_text() for i,page in enumerate(reader.pages)), encoding='utf-8')
        r['extracted_path'] = str(dest)
        records.append(r)
    for direction in ['representational_limits','certified_boolean_extraction','semantic_compilation']:
        folder = DIRECTIONS / direction
        for name in ['research_dossier.md','references.bib','claim_matrix.csv']:
            records.append(record(folder/name, direction, True))
        for p in folder.rglob('*'):
            if p.is_file() and p.suffix.lower() in ['.py','.json','.md','.csv','.bib','.txt','.pdf'] and p.name not in ['research_dossier.md','references.bib','claim_matrix.csv']:
                records.append(record(p, direction, p.suffix.lower() != '.pdf'))
    now = datetime.now(timezone.utc).isoformat()
    snapshot = {'snapshot_utc':now,'user_date':'2026-10-13','timezone':'Asia/Bangkok',
                'version_authority':'Hash freezes reviewed version; mtime alone does not establish authority.',
                'records':records}
    (OUT/'source_snapshot.json').write_text(json.dumps(snapshot, indent=2)+'\n',encoding='utf-8')
    for arg,name in [(['status','--short'],'initial_git_status.txt'),(['diff','--stat'],'initial_git_diff_stat.txt')]:
        result=subprocess.run(['git',*arg],cwd=REPO,capture_output=True,text=True)
        (OUT/name).write_text(result.stdout+'\nSTDERR:\n'+result.stderr,encoding='utf-8')
    print(json.dumps({'snapshot_utc':now,'records':len(records),'source_hash_matches':[(r['role'],r['report_source_hash_matches']) for r in records if 'report_source_hash_matches' in r],
                      'dossiers':[(r['role'],r['status']) for r in records if Path(r['path']).name=='research_dossier.md']},indent=2))

if __name__ == '__main__': main()
