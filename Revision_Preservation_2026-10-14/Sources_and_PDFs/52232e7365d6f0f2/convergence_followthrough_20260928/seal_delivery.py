"""Assemble context, validate results, index experiments and seal the new delivery."""
from pathlib import Path
import collections,csv,hashlib,json,shutil,subprocess,sys,zipfile
from verify_delivery import included
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel):return json.loads((ROOT/rel).read_text())

def main():
    checks={}
    external=load('inputs/external_audit/ASTRA_Convergence_Audit_2026-09-28/EVIDENCE/independent_math_results.json')
    new=load('runs/independent_replay/independent_math_results.json');checks['oracle_substantive_results_equal']=new['tests']==external['tests']
    theory=load('inputs/theory/qk_verification_results.json');replayed=load('runs/theory_replay/qk_verification_results.json')
    checks['theory_results_equal']=theory==replayed
    old=load('inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/raw_results/benchmark_v3_replay.json')
    timed=load('runs/benchmark_replay/timing_replay/reproducibility/raw_results/benchmark_v3_replay.json')
    checks['timing_case_and_query_identity']=[(x['id'],x['query_batch_sha256']) for x in old]==[(x['id'],x['query_batch_sha256']) for x in timed]
    checks['timing_38_cases']=len(timed)==38
    checks['original_570_trials']=sum(len(v) for x in timed for v in x['timings'].values())==570
    checks['zero_artifact_wins']=not any(x['artifact_better_than_packed'] for x in timed)
    for label,path in [('final_correctness','runs/final_correctness/RECEIPT.json'),('linux_correctness','runs/final_correctness_linux_v2/RECEIPT.json'),
                       ('final_lifecycle','runs/final_lifecycle_acceptance/SUMMARY.json'),('corpus_crosscheck','runs/corpus_crosscheck.json'),
                       ('cudd_exhaustive','runs/infrastructure_validation_linux_v2/validation.json')]:
        checks[label]=load(path)['status']=='PASS'
    acceptance=load('runs/final_lifecycle_acceptance/SUMMARY.json')
    checks['18_acceptance_trials']=len(acceptance['trials'])==18
    required=load('EXPERIMENT_SCHEMA.json')['required']
    checks['successful_record_schema']=all(set(required)<=x['result'].keys() for x in acceptance['trials'])
    checks['no_hidden_main_campaign']=load('PROTOCOL_C2_PENDING.json')['main_campaign_authorized'] is False
    if not all(checks.values()):raise AssertionError(checks)
    # Keep full relevant manuscript projects; earlier three-draft archive already in original intake.
    intake=REPO/'astra_convergence_intake_20260928/inputs'
    contexts={'structural_three_drafts':intake/'01_structural_three_draft_package/manuscripts',
              'latest_cm_lm':intake/'02_latest_cm_lm_revision/revised_manuscript',
              'pair_compiler':intake/'03_pair_compiler_revision'}
    context_rows=[]
    for label,source in contexts.items():
        for p in source.rglob('*'):
            if not p.is_file() or p.suffix not in ('.tex','.bib','.pdf','.md','.json'):continue
            dst=ROOT/'context'/label/p.relative_to(source);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
            context_rows.append({'source':str(p),'delivery':dst.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    (ROOT/'CONTEXT_PROVENANCE.json').write_text(json.dumps(context_rows,indent=2))
    entries=[
      ('N02','independent_math','runs/independent_replay/independent_math_results.json','inputs/external_audit/ASTRA_Convergence_Audit_2026-09-28/EVIDENCE/independent_math_audit.py'),
      ('N03','baseline_replay','runs/baseline_replay/clean_correctness_replay.json','inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/run_correctness.py'),
      ('N04','theory_replay','runs/theory_replay/qk_verification_results.json','inputs/theory/verify_qk.py'),
      ('N05','old_timing_replay','runs/benchmark_replay/timing_replay/reproducibility/raw_results/benchmark_v3_replay.json','inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code/benchmark_replay_v3.py'),
      ('N06','coordinate_integration','runs/final_correctness/integration/integration_results.json','regression.py'),
      ('N07','corpus_screen','corpus_v1/SCREEN.json','corpus.py'),
      ('N08','corpus_crosscheck','runs/corpus_crosscheck.json','crosscheck_corpus.py'),
      ('N10','compiled_correctness','runs/infrastructure_validation_linux_v2/validation.json','validate_infrastructure.py'),
      ('N12','final_lifecycle_acceptance','runs/final_lifecycle_acceptance/SUMMARY.json','lifecycle.py'),
      ('N13','one_command_windows','runs/final_correctness/RECEIPT.json','reproduce.py'),
      ('N14','one_command_linux','runs/final_correctness_linux_v2/RECEIPT.json','reproduce.py')]
    with (ROOT/'EXPERIMENT_MANIFEST.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['id','experiment','raw_result','result_sha256','code','code_sha256','status','scope'])
        for id,name,raw,code in entries:w.writerow([id,name,raw,sha(ROOT/raw),code,sha(ROOT/code),'PASS','legacy replay or infrastructure; not T3 campaign'])
        w.writerow(['C2','main_T3_campaign','','','PROTOCOL_C2_PENDING.json',sha(ROOT/'PROTOCOL_C2_PENDING.json'),'HELD','Theory target missing; explicit user hold'])
    (ROOT/'DELIVERY_VALIDATION.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
    manifest=[]
    for p in sorted(ROOT.rglob('*')):
        if included(p):manifest.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    (ROOT/'MANIFEST_SHA256.json').write_text(json.dumps({'files':manifest},indent=2))
    subprocess.run([sys.executable,str(ROOT/'verify_delivery.py')],check=True)
    dest=REPO/'CM_Convergence_Audit_and_Computation_Preparation_2026-09-28.zip'
    if dest.exists():raise FileExistsError(dest)
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in manifest:z.write(ROOT/row['path'],'convergence_followthrough_20260928/'+row['path'])
        z.write(ROOT/'MANIFEST_SHA256.json','convergence_followthrough_20260928/MANIFEST_SHA256.json')
    print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest),'manifest_files':len(manifest)},indent=2))
if __name__=='__main__':main()
