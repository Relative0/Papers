import pathlib,json,hashlib,subprocess,sys,shutil,zipfile,re
W=pathlib.Path(__file__).parent.resolve(); R=pathlib.Path(r'C:\Users\brian\Documents\Math Latex etc\Papers for Publication'); T=W/'verification'; T.mkdir(exist_ok=True)
rows=json.loads((W/'inventory_before.json').read_text(encoding='utf-8')); results=[]
for needle,name in [('verify_two_bit_height_two_counterexample.py','seven_state'),('restricted_guard_probe_case_study.py','nonlinear_guard')]:
 src=next(R/x['path'] for x in rows if x['path'].endswith(needle) and not x['path'].startswith('CM_LM_'))
 b=src.read_bytes(); dest=T/name; dest.mkdir(exist_ok=True); text=b.decode('utf-8'); adaptation=None
 if name=='nonlinear_guard':
  old='/mnt/data/Restricted_Guard_CM_LM_Research_2026-09-24/nonlinear_case_study_results.json'
  new=(dest/'nonlinear_case_study_results.json').as_posix(); assert old in text; text=text.replace(old,new); adaptation={'old':old,'new':'isolated verification/nonlinear_guard/nonlinear_case_study_results.json','scope':'output path only, temporary copy; retained source untouched'}
 (dest/src.name).write_text(text,encoding='utf-8'); p=subprocess.run([sys.executable,'-X','utf8',src.name],cwd=dest,capture_output=True,text=True,encoding='utf-8',timeout=60)
 (dest/'stdout.txt').write_text(p.stdout,encoding='utf-8'); (dest/'stderr.txt').write_text(p.stderr,encoding='utf-8')
 results.append({'name':name,'source':src.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(b).hexdigest(),'exit_code':p.returncode,'adaptation':adaptation,'stdout':p.stdout,'stderr':p.stderr})
tracked=set(json.loads((W/'tracked_before.json').read_text())); outside={}
for x in rows:
 if not x['path'].startswith('CM_LM_PUBLICATION_PORTFOLIO_20260921/') and x['path'] in tracked:outside.setdefault(x['sha256'],[]).append(x['path'])
coverage=[dict(x,canonical_tracked_matches=outside.get(x['sha256'],[])) for x in rows if x['path'].startswith('CM_LM_PUBLICATION_PORTFOLIO_20260921/')]
assert len(coverage)==353 and all(x['canonical_tracked_matches'] for x in coverage)
(W/'portfolio_coverage_before.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
(W/'verification_runs.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'tests':[(x['name'],x['exit_code'],x['stderr'][:200]) for x in results],'portfolio_files':len(coverage),'portfolio_bytes':sum(x['bytes'] for x in coverage),'all_have_tracked_outside_copy':True},indent=2))
