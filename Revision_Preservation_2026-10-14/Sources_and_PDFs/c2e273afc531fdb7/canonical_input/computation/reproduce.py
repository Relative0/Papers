#!/usr/bin/env python3
"""Reproduce exact finite checks in an isolated, new output directory.
Default: new independent checks only. No install, network, or benchmark campaign.
--all adds supplied mathematical stages; --historical adds embedded test suites.
"""
from __future__ import annotations
import argparse,json,os,platform,shutil,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/'provenance/source_snapshots'

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workdir',type=Path,required=True,help='New directory; existing paths are rejected.')
    g=p.add_mutually_exclusive_group()
    g.add_argument('--quick',action='store_true',help='Only new independent standard-library checks (default).')
    g.add_argument('--all',action='store_true',help='Also rerun explicit supplied mathematical stages.')
    p.add_argument('--historical',action='store_true',help='With --all, run four unchanged historical suites separately.')
    p.add_argument('--timeout',type=int,default=180,help='Per-stage timeout in seconds, default180.')
    a=p.parse_args()
    if a.historical and not a.all:p.error('--historical requires --all')
    if a.timeout<=0:p.error('--timeout must be positive')
    work=a.workdir.expanduser().resolve()
    if work.exists():p.error('Work directory already exists; choose a new path.')
    if work==ROOT or ROOT in work.parents:p.error('Choose a work directory outside this repository.')
    work.mkdir(parents=True)
    logs=work/'logs';logs.mkdir()
    independent=work/'independent';independent.mkdir()
    for name in ['consolidation_checks.py','oracle_contract_check.py']:
        shutil.copy2(ROOT/'computation/independent'/name,independent/name)
    stages=[('independent',independent,['consolidation_checks.py',str(SNAP/'bench')]),
            ('oracle_contract',independent,['oracle_contract_check.py'])]
    if a.all:
        for name in ['audit','capability','bridge','adversarial','bench']:
            shutil.copytree(SNAP/name,work/name,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
        stages += [('audit_tests',work/'audit',['-m','pytest','-q','-p','no:cacheprovider','tests'])]
        if a.historical:
            for short,name in [('pure','Pure_Boolean_Modal_Quantum'),('rotation','Native_Boolean_CM_Rotation_Phase'),('block','Native_Boolean_CM_Block_Quantum'),('tensor','Independent_Phase_CM_Tensor_Audit')]:
                stages.append(('historical_'+short,work/'audit/source_snapshots'/name,['-m','pytest','-q','-p','no:cacheprovider','tests']))
        for name in ['audit_models','audit_protocols','audit_restrictions']:
            stages.append((name,work/'audit',['code/'+name+'.py']))
        stages += [('bridge_expanded',work/'bridge',['tests/lm_modal_bridge_checks.py']),
                   ('bridge_original',work/'bridge',['tests/cm_bridge_checks_original.py'])]
        for name in ['laboratory','ablations','bridges_phase','two_setting_theorem','validate_and_index']:
            stages.append(('capability_'+name,work/'capability',['code/'+name+'.py']))
        stages += [('adversarial_extensions',work/'adversarial',['checks/independent_extensions.py']),
                   ('adversarial_boundaries',work/'adversarial',['checks/additional_boundaries.py']),
                   ('benchmark_tests',work/'bench',['-m','pytest','-q','-p','no:cacheprovider','tests']),
                   ('benchmark_raw_audit',work/'bench',['scripts/audit_gate_a_results.py'])]
    manifest={'python':sys.version,'platform':platform.platform(),'source_repository':str(ROOT),
              'fresh_timing_campaign':False,'stages':[]}
    for name,cwd,args in stages:
        env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
        env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1';env['MKL_NUM_THREADS']='1'
        env['PYTHONPATH']=os.pathsep.join(map(str,[cwd/'code',cwd/'src',cwd]))
        command=[sys.executable,*args]
        print('RUN',name,flush=True);t=time.monotonic()
        try:
            run=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=a.timeout)
            text=run.stdout;code=run.returncode;status='PASS' if code==0 else 'FAIL'
        except subprocess.TimeoutExpired as e:
            raw=e.stdout or b'';text=raw.decode(errors='replace') if isinstance(raw,bytes) else raw
            text+='\nTIMEOUT\n';code=None;status='TIMEOUT'
        except OSError as e:
            text=repr(e)+'\n';code=None;status='EXECUTION_ERROR'
        (logs/(name+'.log')).write_text(text)
        record={'name':name,'command':command,'cwd':str(cwd),'seconds':time.monotonic()-t,
                'returncode':code,'status':status,'log':'logs/'+name+'.log'}
        manifest['stages'].append(record)
        (work/'RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(status,name,round(record['seconds'],3),flush=True)
        if status!='PASS':print('Stopped. Inspect',logs/(name+'.log'),file=sys.stderr);return 1
    print('Completed',len(stages),'explicit stages. Output:',work)
    return 0

if __name__=='__main__':raise SystemExit(main())
