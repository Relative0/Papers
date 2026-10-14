from common import *
from verify_delivery import included
import shutil,subprocess,zipfile,csv
def main():
    original=ROOT.parent/'CM_Convergence_Audit_and_Computation_Preparation_2026-09-28.zip'
    assert sha(original.read_bytes())=='52232e7365d6f0f254f9f0e6f4b18d81f803034aefc22bf8a65c530ec0206fdc'
    if not (ROOT/'PRIOR_PHASE_PACKAGE.zip').exists():shutil.copy2(original,ROOT/'PRIOR_PHASE_PACKAGE.zip')
    assert sha((ROOT/'PRIOR_PHASE_PACKAGE.zip').read_bytes())==sha(original.read_bytes())
    analysis=json.loads((ROOT/'results/ANALYSIS.json').read_text())
    assert analysis['status']=='PASS' and analysis['executed_queries']==7445928 and analysis['executed_updates']==70662
    assert not any(k.endswith(':FAIL') or k.endswith(':TIMEOUT') for k in analysis['trial_statuses'])
    assert analysis['all_cold_zero_resident_before_load'] and analysis['cold_verified_passes']==115
    memory=json.loads((ROOT/'results/ISOLATED_MEMORY_SUMMARY.json').read_text())
    assert memory['statuses']=={'UNSUPPORTED':5,'PASS':115} and memory['actual_extra_queries']==21056 and memory['actual_extra_updates']==214
    for rel in ('results/correctness_t3.json','results/correctness_native.json','results/theory_replay.json'):
        assert json.loads((ROOT/rel).read_text())['status']=='PASS'
    assert json.loads((ROOT/'results/theory_replay.json').read_text())==json.loads((ROOT/'theory/t3_verification_results.json').read_text())
    mainrec=json.loads((ROOT/'results/completion_main.json').read_text())
    assert sha((ROOT/'source_snapshots/campaign_main_v1.py').read_bytes())==mainrec['source_hashes']['campaign.py']
    for code in ('state.py','common.py','comparators.py'):
        assert sha((ROOT/code).read_bytes())==mainrec['source_hashes'][code]
        assert sha((ROOT/code).read_bytes())==json.loads((ROOT/'results/correctness_native.json').read_text())['source_hashes'][code]
    assert sha((ROOT/'native_count.so').read_bytes())==mainrec['native_sha256']
    assert sha((ROOT/'PROTOCOL.json').read_bytes())==(ROOT/'PROTOCOL.sha256').read_text().strip()
    commands=[('C1','python ../convergence_followthrough_20260928/verify_delivery.py','prior manifest: PASS 4912'),
      ('freeze','python prepare.py freeze','PROTOCOL.sha256'),('inputs','python prepare.py prepare','inputs/IDENTITY.json'),
      ('compile','g++ -std=c++17 -O3 -DNDEBUG -fPIC -shared native_count.cpp -o native_count.so','ENVIRONMENT.json'),
      ('correctness','python validate.py --native','validation_linux.log'),('main','python campaign.py main','campaign_main.log'),
      ('cold','python campaign.py cold','campaign_cold.log'),('complement-freeze','python complement_controls.py freeze','COMPLEMENT_CONTROL_ADDENDUM.json'),
      ('complement','python complement_controls.py run','campaign_complement.log'),('theory','python supplement.py theory','theory_replay.log'),
      ('source','python supplement.py sources','source_preparation.log'),('environment','python supplement.py environment','ENVIRONMENT.json'),
      ('analysis','python analyze.py','analysis.log'),('tables','python report_tables.py','LIFECYCLE_SUMMARY.csv'),
      ('isolated-memory','python isolated_memory.py run','isolated_memory.log'),('minimized-byte-witness','python minimize_metadata.py','results/MINIMIZED_MATCHED_BYTE_WITNESS.json')]
    write(ROOT/'COMMAND_MANIFEST.json',{'cwd':str(ROOT),'linux_interpreter':'/mnt/c/Users/brian/Documents/CM_Computation/convergence_followthrough_20260928/runtime/linux-venv/bin/python','windows_interpreter':str(ROOT.parent/'.venv/Scripts/python.exe'),'linux_launcher':['wsl','-d','Ubuntu-24.04','--'],'commands':[{'id':a,'command':b,'evidence':c} for a,b,c in commands]})
    write(ROOT/'SOURCE_REVISION.json',{'git_head':'9a8ec9172fa1ba841c7960d088b94ef04c67c9b8','status':'new uncommitted scoped directory; original tracked changes unchanged','source_files':{p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.suffix in ('.py','.cpp','.so') and '__pycache__' not in p.parts},'theory_zip_sha256':sha((ROOT/'THEORY_PHASE2_T1_T3_HANDOFF_2026-09-28.zip').read_bytes()),'prior_zip_sha256':sha(original.read_bytes())})
    with (ROOT/'EXPERIMENT_MANIFEST.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['experiment','raw_file','sha256','status'])
        for p in sorted((ROOT/'results').glob('*')):
            if p.is_file():w.writerow([p.stem,p.relative_to(ROOT).as_posix(),sha(p.read_bytes()),'recorded; inspect per-row status'])
    write(ROOT/'DELIVERY_VALIDATION.json',{'status':'PASS','prior_preserved':True,'source_versions_match_validation':True,'main_runner_snapshot_matches':True,'protocol_hash_unchanged':True,'theory_exact_replay_match':True,'campaign_executed_queries':analysis['executed_queries'],'campaign_executed_updates':analysis['executed_updates'],'extra_memory_queries':21056,'extra_memory_updates':214,'cold_verified_passes':115,'isolated_memory_passes':115,'campaign_unsupported_trials_retained':405,'extra_memory_unsupported':5})
    files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(ROOT.rglob('*')) if included(p)]
    write(ROOT/'MANIFEST_SHA256.json',{'files':files})
    subprocess.run([sys.executable,str(ROOT/'verify_delivery.py')],check=True)
    dest=ROOT.parent/'CM_Structural_Computation_C1-C4_T3_Phase2_2026-09-28.zip'
    if dest.exists():raise FileExistsError(dest)
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for row in files:z.write(ROOT/row['path'],ROOT.name+'/'+row['path'])
        z.write(ROOT/'MANIFEST_SHA256.json',ROOT.name+'/MANIFEST_SHA256.json')
    checksum=sha(dest.read_bytes());dest.with_suffix(dest.suffix+'.sha256').write_text(checksum+'  '+dest.name+'\n')
    print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'files':len(files),'sha256':checksum},indent=2))
if __name__=='__main__':main()
