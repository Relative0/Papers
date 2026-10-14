"""One-command correctness reproduction into a new output tree. No network."""
from pathlib import Path
import argparse, importlib.util, json, subprocess, sys, time
ROOT=Path(__file__).resolve().parent

def main(output):
    output=output.resolve();output.mkdir(parents=True,exist_ok=False);records=[]
    audit=ROOT/'inputs/external_audit/ASTRA_Convergence_Audit_2026-09-28'
    commands=[
        [sys.executable,str(audit/'verify_delivery.py')],
        [sys.executable,str(audit/'reproduce.py'),'independent','--output',str(output/'independent')],
        [sys.executable,str(audit/'reproduce.py'),'baseline','--output',str(output/'baseline')],
        [sys.executable,str(ROOT/'regression.py'),'--output',str(output/'integration')],
        [sys.executable,str(ROOT/'validate_infrastructure.py'),'--output',str(output/'backends')],
    ]
    try:has_cudd=importlib.util.find_spec('dd.cudd') is not None
    except ModuleNotFoundError:has_cudd=False
    if has_cudd:commands[-1].append('--cudd')
    for i,cmd in enumerate(commands):
        start=time.perf_counter();log=output/f'{i:02d}.log'
        with log.open('w') as stream:
            try:rc=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
            except subprocess.TimeoutExpired:rc='TIMEOUT'
        records.append({'command':cmd,'returncode':rc,'seconds':time.perf_counter()-start,'log':str(log)})
        (output/'RECEIPT.json').write_text(json.dumps({'status':'RUNNING' if rc==0 else 'FAIL','commands':records,'cudd_included':has_cudd},indent=2))
        if rc!=0:raise RuntimeError(f'Failed; preserved log: {log}')
        print(i,'PASS',flush=True)
    (output/'RECEIPT.json').write_text(json.dumps({'status':'PASS','commands':records,'cudd_included':has_cudd},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
