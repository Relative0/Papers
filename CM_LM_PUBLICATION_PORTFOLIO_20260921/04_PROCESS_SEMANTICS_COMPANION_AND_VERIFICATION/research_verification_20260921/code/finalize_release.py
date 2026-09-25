"""Validate, inventory and hash the completed new snapshot; never alter sources."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    required=['STATUS.md','LITERATURE_LEDGER.csv','SEARCH_LOG.csv','MODEL_CANDIDATE_COMPARISON.md',
        'THEOREM_COUNTEREXAMPLE_LEDGER.md','PROCESS_SEMANTICS_SPECIFICATION.md','RESOURCE_RESULTS_REASSESSMENT.md',
        'GO_NO_GO_MEMO.md','RESEARCH_STUB.md','P03_STUB/main.tex','P03_STUB/references.bib',
        'P03_STUB/FINAL_CLAIMS.md','P03_STUB/UNRESOLVED_PRIORITY_AND_ISSUES.md']
    for name in required:assert (ROOT/name).is_file(),name
    for name in ['run_record','verification_results']:
        assert json.loads((ROOT/'data'/f'{name}.json').read_text())['status']=='PASS'
    sources=json.loads((ROOT/'data/source_inventory.json').read_text())
    changed=[s['path'] for s in sources if sha(Path(s['path']))!=s['sha256']]
    assert not changed,changed
    log=(ROOT/'P03_STUB/build/main.log').read_text(errors='replace')
    assert not re.search(r'LaTeX Warning:|Overfull|^!',log,re.MULTILINE)
    counts={name:len(list(csv.DictReader((ROOT/name).open(encoding='utf-8'))))
        for name in ['LITERATURE_LEDGER.csv','SEARCH_LOG.csv']}
    result={'status':'PASS','required_artifacts':len(required),'csv_records':counts,
       'source_files_unchanged':len(sources),'latex_draftmode_check':'PASS; expected no-PDF warning only',
       'pdf_generated':False,'git':'workspace is not a Git repository'}
    (ROOT/'data/release_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    names=sorted({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts} | {'ARTIFACT_INVENTORY.txt','MANIFEST_SHA256.txt'})
    status=(ROOT/'STATUS.md').read_text(encoding='utf-8').split('<!-- INVENTORY -->')[0]
    status+='<!-- INVENTORY -->\n\n## Exact release inventory\n\n'+''.join(f'- `{n}`\n' for n in names)
    (ROOT/'STATUS.md').write_text(status,encoding='utf-8')
    (ROOT/'ARTIFACT_INVENTORY.txt').write_text('\n'.join(names)+'\n',encoding='utf-8')
    manifest=''.join(f'{sha(ROOT/n)}  {n}\n' for n in names if n!='MANIFEST_SHA256.txt')
    (ROOT/'MANIFEST_SHA256.txt').write_text(manifest,encoding='utf-8')
    for line in manifest.splitlines():
        expected,name=line.split('  ',1)
        assert sha(ROOT/name)==expected
    print(json.dumps({**result,'release_files':len(names),'manifest_entries':len(names)-1},indent=2))

if __name__=='__main__':main()
