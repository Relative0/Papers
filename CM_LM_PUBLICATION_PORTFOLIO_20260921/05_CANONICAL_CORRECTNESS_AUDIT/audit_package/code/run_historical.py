"""Run original test suites, unchanged, in separate interpreters."""
from pathlib import Path
import subprocess, os, time, json, sys
ROOT=Path(__file__).resolve().parents[1]
results=[]
for name in ['Pure_Boolean_Modal_Quantum','Native_Boolean_CM_Rotation_Phase','Native_Boolean_CM_Block_Quantum','Independent_Phase_CM_Tensor_Audit']:
    cwd=ROOT/'source_snapshots'/name
    env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';env['PYTHONPATH']=str(cwd/'code')+os.pathsep+str(cwd)
    start=time.time()
    p=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','tests'],cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (ROOT/'logs'/(name+'_rerun.txt')).write_text(p.stdout)
    rec={'suite':name,'returncode':p.returncode,'seconds':time.time()-start,'output':p.stdout}
    results.append(rec);print(name,p.returncode,p.stdout[-500:],flush=True)
(ROOT/'data'/'historical_test_rerun.json').write_text(json.dumps(results,indent=2))

if any(r["returncode"] for r in results): raise SystemExit(1)
