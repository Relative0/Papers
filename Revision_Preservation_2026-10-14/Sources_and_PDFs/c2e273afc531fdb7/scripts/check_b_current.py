from pathlib import Path
import hashlib,json,shutil,subprocess,sys,time,os
O=Path(__file__).resolve().parent; SRC=Path(r'C:\Users\brian\Documents\CM_Computation')
R=O/'runs'/('paper_b_current_'+(sys.argv[1] if len(sys.argv)>1 else '01'));R.mkdir(exist_ok=True)
selected=list(SRC.glob('*.py'))+list((SRC/'cmbench').rglob('*.py'))+[SRC/'scripts/cm_memory_estimator_study.py']+[SRC/'tests'/p for p in ['conftest.py','test_cm_pair_alignment.py','test_cm_optimizations.py','test_output_budget.py','test_bitset_backend.py']]
manifest={}
for p in selected:
    if '__pycache__' in p.parts:continue
    rel=p.relative_to(SRC);t=R/'source'/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);manifest[rel.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
command=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--basetemp',str(R/'pytest_tmp'),*[f'tests/{p}' for p in ['test_cm_pair_alignment.py','test_cm_optimizations.py','test_output_budget.py','test_bitset_backend.py']]]
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
started=time.monotonic();r=subprocess.run(command,cwd=R/'source',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
(R/'pytest_output.txt').write_bytes(r.stdout)
unchanged=all(hashlib.sha256((SRC/rel).read_bytes()).hexdigest()==h for rel,h in manifest.items())
out=dict(command=command,interpreter=sys.version,seconds=time.monotonic()-started,returncode=r.returncode,original_source_unchanged=unchanged,source_files=len(manifest),output_sha256=hashlib.sha256(r.stdout).hexdigest(),scope='Fresh local isolated copy of four current implementation test files; no network/cloud calls or performance campaign',seed='Test-local seeds unchanged')
(R/'RUN_MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n');print(r.stdout.decode(errors='replace'));print(json.dumps(out,indent=2))
raise SystemExit(r.returncode)
