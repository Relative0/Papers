"""Run delivered bounded verifiers only in disposable-by-policy, retained local copies."""
from snapshot import ROOT,OUT,dump,sha
import shutil,pathlib,subprocess,sys,json,importlib.util,time
def main():
    work=OUT/'Verification_Work';work.mkdir(exist_ok=True);results=[]
    def run(name,args,cwd,timeout=180):
        t=time.time()
        try:
            p=subprocess.run([sys.executable,'-X','utf8',*args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',timeout=timeout)
            (work/(name+'.log')).write_text(p.stdout+'\nSTDERR:\n'+p.stderr,encoding='utf-8')
            r={'name':name,'command':args,'cwd':str(cwd.relative_to(ROOT)),'exit_code':p.returncode,'elapsed_seconds':round(time.time()-t,2),'log':str((work/(name+'.log')).relative_to(ROOT))}
        except subprocess.TimeoutExpired as e:
            r={'name':name,'status':'TIMEOUT','timeout_seconds':timeout}
        results.append(r);dump('project_checks.json',results);print(json.dumps(r),flush=True)
    guard=ROOT/'Guarded Boolean Operator (Paper B)/REVIEWED_PACKAGE_2026-09-28/Guarded_Boolean_Paper_B_Reviewed_2026-09-28'
    target=work/'guarded';shutil.copytree(guard,target,dirs_exist_ok=True)
    if importlib.util.find_spec('sympy'):
        run('guarded_full_verifier',['code/verify_guarded_dispatch.py','--out','fresh_results'],target)
        actual=target/'fresh_results/verification_results.json';expected=guard/'evidence/fresh_run/verification_results.json'
        if actual.exists() and expected.exists():results.append({'name':'guarded_semantic_output_comparison','byte_identical':sha(actual)==sha(expected),'parsed_json_equal':json.loads(actual.read_bytes())==json.loads(expected.read_bytes()),'newline_normalized_equal':actual.read_bytes().replace(b'\r\n',b'\n')==expected.read_bytes().replace(b'\r\n',b'\n'),'actual_sha256':sha(actual),'expected_sha256':sha(expected)})
    else:
        results.append({'name':'guarded_full_verifier','status':'SKIPPED','reason':'SymPy is not installed in selected interpreter; no dependencies installed'})
        for n,args in [('coordinate',['2','1/2','--mode','coordinate']),('quartic',['2','1/2','--mode','quartic']),('boundary',['1','1/2','--mode','quartic'])]:run('guarded_'+n,['code/guarded_dispatch.py',*args],target)
    phase=ROOT/'Intrinsic Boolean CM Phase Algebra/REVIEWED_PACKAGE_2026-09-28/CM_Phase_Research_Revision_2026-09-28'
    target=work/'intrinsic';shutil.copytree(phase/'reproducibility',target/'reproducibility',dirs_exist_ok=True)
    run('intrinsic_revision_verifier',['reproducibility/code/verify_revision.py'],target)
    bt=ROOT/'ProLT-Homology/ProLT-Homology-Reviewed-2026-09-27/02_REVIEWED_MANUSCRIPT_20260927/reproducibility/verify_two_bit_height_two_counterexample.py'
    target=work/'binary_thinning';target.mkdir(exist_ok=True);shutil.copy2(bt,target/bt.name)
    run('seven_state_certificate',[bt.name],target)
    dump('project_checks.json',results)
if __name__=='__main__':main()
