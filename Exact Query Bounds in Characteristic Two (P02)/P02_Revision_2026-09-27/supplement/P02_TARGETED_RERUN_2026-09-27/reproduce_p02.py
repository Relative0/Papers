#!/usr/bin/env python3
"""Targeted P02 reproducibility driver.
Runs the recovered oracle-contract checker, the independent 2026-09-27 P02 verifier,
recovered capability stages, and a deterministic phase-table reconstruction.
"""
from pathlib import Path
import hashlib, json, platform, shutil, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'fresh_outputs'; OUT.mkdir(exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(name, cmd, cwd=ROOT):
    log=OUT/f'{name}.log'; t=time.perf_counter()
    with log.open('w') as f:
        r=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=False)
    sec=time.perf_counter()-t
    if r.returncode: raise SystemExit(f'{name} failed with {r.returncode}; see {log}')
    return {'name':name,'seconds':sec,'returncode':r.returncode,'log':str(log.relative_to(ROOT))}

stages=[]
# Run a copy so the recovered script itself remains untouched.
contract=OUT/'oracle_contract_check.py'; shutil.copy2(ROOT/'oracle_contract_check.py',contract)
stages.append(run('oracle_contract',[sys.executable,str(contract)],OUT))
stages.append(run('independent_checks',[sys.executable,str(ROOT/'fresh_checks'/'independent_checks.py'),'--output',str(OUT/'independent_checks.json')],ROOT))
stages.append(run('capability',[sys.executable,str(ROOT/'capability'/'code'/'run_all.py'),'--timeout','120'],ROOT/'capability'))
stages.append(run('phase_table',[sys.executable,str(ROOT/'generate_phase_table.py'),'--input',str(ROOT/'capability'/'data'/'new_phase_fourier.json'),'--output',str(OUT/'phase_table.tex')],ROOT))

relevant=[OUT/'oracle_contract_check.json',OUT/'independent_checks.json',ROOT/'capability'/'data'/'new_algorithm_checks.json',ROOT/'capability'/'data'/'new_phase_fourier.json',ROOT/'capability'/'data'/'small_simon.json',ROOT/'capability'/'data'/'description_readout_ablation.json',ROOT/'capability'/'data'/'unique_sat_reproduction.csv',OUT/'phase_table.tex']
manifest={'success':True,'python':sys.version,'platform':platform.platform(),'stages':stages,'outputs':[{ 'path':str(p.relative_to(ROOT)), 'sha256':sha(p), 'bytes':p.stat().st_size} for p in relevant]}
(ROOT/'P02_RERUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
