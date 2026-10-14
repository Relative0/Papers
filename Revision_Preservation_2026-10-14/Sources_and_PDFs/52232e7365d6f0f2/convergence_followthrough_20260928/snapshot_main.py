"""Freeze only loaded repository source dependencies identified by the C1 run."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent
receipt=json.loads((ROOT/'runs/coordinate_integration_v2/integration_results.json').read_text())
records=[]
for name,expected in receipt['source_sha256'].items():
    if name.replace('\\','/').startswith('convergence_followthrough_20260928/'):continue
    src=REPO/name
    if hashlib.sha256(src.read_bytes()).hexdigest()!=expected:raise RuntimeError('source changed since C1: '+name)
    dest=ROOT/'main_source_snapshot'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    records.append({'path':name,'sha256':expected})
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
(ROOT/'MAIN_SOURCE_PIN.json').write_text(json.dumps({'head':head,'dirty_source':True,'identity':'file hashes, not HEAD alone','files':records},indent=2))
print('Frozen',len(records),'loaded source modules')
