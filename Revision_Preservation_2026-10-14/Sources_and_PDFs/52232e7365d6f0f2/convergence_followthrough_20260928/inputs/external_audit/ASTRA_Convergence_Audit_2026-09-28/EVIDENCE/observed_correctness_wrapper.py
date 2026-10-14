import runpy, subprocess, sys, time, json
from pathlib import Path
base=Path('/mnt/data/convergence_work/inputs/computation/CM_COMPUTATION_BASELINE_HANDOFF')
out=Path('/mnt/data/ASTRA_Convergence_Audit_2026-09-28/EVIDENCE')
real_run=subprocess.run
partial=[]
def observed(*args,**kw):
    print('START',args[0],flush=True);start=time.monotonic()
    try:
        r=real_run(*args,**kw)
        partial.append({'command':args[0],'returncode':r.returncode,'seconds':time.monotonic()-start,'stdout':r.stdout,'stderr':r.stderr})
        (out/'correctness_progress.json').write_text(json.dumps(partial,indent=2))
        print('END',r.returncode,time.monotonic()-start,flush=True)
        return r
    except Exception as e:
        print('EXCEPTION',repr(e),flush=True)
        raise
subprocess.run=observed
sys.argv=[str(base/'reproducibility/run_correctness.py'),'--output',str(out/'clean_correctness_replay.json')]
runpy.run_path(sys.argv[0],run_name='__main__')
