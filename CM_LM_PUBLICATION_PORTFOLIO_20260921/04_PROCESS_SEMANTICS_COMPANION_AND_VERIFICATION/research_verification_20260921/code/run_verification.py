"""Run final check receipts without modifying any input source or historic data."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]

def run(label,args,cwd):
    start=time.time()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
    proc=subprocess.run(args,cwd=cwd,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True)
    (ROOT/'logs'/f'{label}.stdout.txt').write_text(proc.stdout,encoding='utf-8')
    (ROOT/'logs'/f'{label}.stderr.txt').write_text(proc.stderr,encoding='utf-8')
    record={'label':label,'argv':args,'cwd':str(cwd),'exit_code':proc.returncode,'seconds':time.time()-start}
    if proc.returncode:
        print(proc.stdout+proc.stderr)
        raise RuntimeError(record)
    return record

def main():
    (ROOT/'logs').mkdir(exist_ok=True)
    receipts=[run('source_capture',[sys.executable,'-B',str(ROOT/'code/capture_provenance.py')],ROOT)]
    sources=json.loads((ROOT/'data/source_inventory.json').read_text())
    receipts.append(run('exhaustive',[sys.executable,'-B',str(ROOT/'code/verify_semantics.py')],ROOT))
    receipts.append(run('unit_tests',[sys.executable,'-B',str(ROOT/'code/test_semantics.py')],ROOT))
    receipts.append(run('canonical_tests',[sys.executable,'-B','-m','pytest',
        str(WORK/'output/cm_lm_publication_20260918/runs/canonical_01/audit/tests/test_independent_audit.py'),
        '-q','-p','no:cacheprovider'],WORK))
    receipts.append(run('disposal_witness',[sys.executable,'-B','-c',
        "import sys,json; from pathlib import Path; sys.path.insert(0,'code'); "
        "from prior_review_checks import phase_disposal_witness; r=phase_disposal_witness(); "
        "Path('data/resolved_disposal_witness.json').write_text(json.dumps(r,indent=2)+'\\n'); print(json.dumps(r,indent=2))"],ROOT))
    changed=[s['path'] for s in sources if hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()!=s['sha256']]
    assert not changed,changed
    result={'status':'PASS','receipts':receipts,'source_files_verified_unchanged':len(sources),
            'source_changes':changed,'new_named_tests':10,'canonical_named_tests':31,
            'scope':'new exact enumeration plus selected inherited witness; not all historical driver reruns'}
    (ROOT/'data/run_record.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
