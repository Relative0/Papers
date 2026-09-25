"""Read-only source audit; writes receipts only inside this new research folder."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]
CANON=WORK/'output/cm_lm_publication_20260918/runs/canonical_01'
PAPERS=Path(r'C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sources=[PAPERS/n for n in ['ADDITIONAL_PUBLICATION_OPPORTUNITIES.md','RESEARCH_GAPS_AFTER_DEEP_DIVE.md',
        'P01/main.tex','P01/FINAL_CLAIMS.md','P01/PRIMARY_SOURCE_REVIEW.csv','P01/PRIORITY_AND_NOVELTY_LEDGER.csv',
        'P02/main.tex','P02/FINAL_CLAIMS.md','Paper_B/FINAL_CLAIMS.md']]
    sources += [CANON/n for n in ['audit/paper/CM_Correctness_Audit_Standalone.tex','audit/paper/CM_Correctness_Audit.pdf',
        'audit/MANIFEST_SHA256.txt','adversarial/NOVELTY_MATRIX.md','adversarial/COMPLETE_RESEARCH_DOSSIER.md']]
    sources.append(Path(r'C:\Users\brian\Downloads\CM_Correctness_Audit_Standalone.tex'))
    for sub in ['code','tests','data']:
        sources += sorted(p for p in (CANON/'audit'/sub).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    prior=PAPERS/'Process_Semantics_Research'
    sources += sorted(p for p in prior.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                      and 'Research_Verification_20260921' not in p.parts)
    rows=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),
           'modified_epoch':p.stat().st_mtime} for p in sources]
    (ROOT/'data/source_inventory.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    results=[]
    for line in (CANON/'audit/MANIFEST_SHA256.txt').read_text(encoding='utf-8-sig').splitlines():
        if not line.strip():continue
        expected,name=line.split(maxsplit=1)
        p=CANON/'audit'/name.strip().lstrip('*')
        results.append({'path':name.strip(),'present':p.is_file(),'expected_sha256':expected.lower(),
                        'actual_sha256':sha(p) if p.is_file() else None,
                        'match':p.is_file() and sha(p)==expected.lower()})
    output={'entries':len(results),'matching':sum(x['match'] for x in results),
       'mismatches':[x for x in results if not x['match']],
       'canonical_download_tex_identical':sha(CANON/'audit/paper/CM_Correctness_Audit_Standalone.tex')==sha(sources[14]),
       'note':'Existing manifest checked as supplied; no canonical output regenerated.'}
    (ROOT/'data/source_integrity.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
