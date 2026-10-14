#!/usr/bin/env python3
"""Reproduce independent experiments and regenerate validated report indexes."""
from pathlib import Path
import subprocess,sys,argparse,time,json,platform
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout',type=int,default=120,help='timeout in seconds for each independent script (default: 120)')
    args=parser.parse_args()
    if args.timeout<=0:parser.error('--timeout must be positive')
    (ROOT/'logs').mkdir(exist_ok=True)
    stages=[('laboratory.py','independent_run.log'),('ablations.py','ablations_run.log'),('bridges_phase.py','bridges_phase_run.log'),('two_setting_theorem.py','two_setting_run.log'),('validate_and_index.py','validation.log')]
    timings=[]
    for filename,logname in stages:
        print('Running',filename,flush=True);start=time.perf_counter()
        with (ROOT/'logs'/logname).open('w') as log:
            try:
                result=subprocess.run([sys.executable,str(ROOT/'code'/filename)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=args.timeout,check=False)
            except subprocess.TimeoutExpired:
                print('TIMEOUT; inspect logs/'+logname,file=sys.stderr);return 124
        if result.returncode:
            print('FAILED; inspect logs/'+logname,file=sys.stderr);return result.returncode
        timings.append({'script':filename,'seconds':time.perf_counter()-start,'exit_code':0,'log':'logs/'+logname})
    (ROOT/'data/run_summary.json').write_text(json.dumps({'success':True,'python':sys.version,'platform':platform.platform(),'scripts':timings,'total_seconds':sum(t['seconds'] for t in timings)},indent=2)+'\n')
    print('All independent stages and cross-validation passed.',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
