"""Rerun the supplied corrected audit without modifying its source.
Usage: python reproduce_supplied.py "/path/to/02_FINAL_AUDIT/CM_Final_Audit"
Install the supplied audit's requirements in a separate environment first.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('audit_root',type=Path)
    ap.add_argument('--output',type=Path,default=Path('reproduction/new_run'))
    args=ap.parse_args();root=args.audit_root.resolve()
    for name in ('run_all.py','code/run_historical.py'):
        if not (root/name).is_file():ap.error(f'Missing expected input file: {root/name}')
    args.output.mkdir(parents=True,exist_ok=True);status=[]
    for label,script in [('independent','run_all.py'),('historical','code/run_historical.py')]:
        start=time.perf_counter()
        with (args.output/f'{label}.log').open('w',encoding='utf-8') as log:
            p=subprocess.run([sys.executable,script],cwd=root,stdout=log,stderr=subprocess.STDOUT,check=False)
        status.append(dict(stage=label,returncode=p.returncode,elapsed_seconds=time.perf_counter()-start))
        (args.output/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
        print(f'{label}: exit {p.returncode}; see {args.output/label}.log')
        if p.returncode:return p.returncode
    return 0
if __name__=='__main__':raise SystemExit(main())
