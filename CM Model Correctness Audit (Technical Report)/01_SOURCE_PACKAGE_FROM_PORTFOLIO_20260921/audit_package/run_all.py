"""Reproduce the audit. Run from any working directory using Python 3.11+."""
from pathlib import Path
import subprocess,sys,argparse,os
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--historical',action='store_true',help='also rerun all four preserved historical test suites')
args=p.parse_args()
commands=[]
if args.historical:commands.append([sys.executable,str(ROOT/'code/run_historical.py')])
commands += [[sys.executable,str(ROOT/'code'/s)] for s in ('audit_models.py','audit_protocols.py','audit_restrictions.py','verify_artifacts.py','generate_report_tables.py')]
commands.append([sys.executable,'-m','pytest','-q',str(ROOT/'tests'),'-p','no:cacheprovider'])
for cmd in commands:
    print('Running:', ' '.join(cmd),flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True,env={**os.environ,"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1"})
