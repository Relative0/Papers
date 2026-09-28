"""Copy sources to a fresh directory and rerun all exact checks without changing originals.

Usage: python reproducibility/run_correctness.py --output replay_receipt_new.json
No network, optional modules, or LaTeX are needed. Timing benchmarks are separate.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,time

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(output):
    base=Path(__file__).resolve().parent;package=base.parent
    receipt={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,
             'method':'new temporary directory; separate child processes; user PYTHONPATH removed; no original output overwritten',
             'code_hashes':{p.name:sha(p) for p in sorted((base/'code').glob('*.py'))},'commands':[]}
    with tempfile.TemporaryDirectory(prefix='sc_clean_replay_') as temp:
        root=Path(temp);repro=root/'reproducibility';repro.mkdir()
        for name in ('code','tests','data'):
            shutil.copytree(base/name,repro/name,ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('raw_results','logs','environment'):(repro/name).mkdir()
        source=root/'legacy_source'
        shutil.copytree(package/'historical_source_material/recovered_source',source,ignore=shutil.ignore_patterns('__pycache__'))
        commands=[
            ['code/datasets.py'], ['tests/test_core.py'], ['tests/test_extensions_v2.py'],
            ['tests/test_field_ranks.py'], ['tests/test_legacy_adapter.py','--source',str(source)],
            ['tests/test_persistence_v3.py'], ['tests/test_scope_limits.py'],
            ['code/audit_historical.py','--source',str(source),'--output',str(repro/'raw_results/historical_contract_audit.json')]]
        env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
        for args in commands:
            cmd=[sys.executable,str(repro/args[0])]+args[1:];start=time.perf_counter()
            result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=90)
            record={'command':[sys.executable,args[0]]+[v.replace(str(root),'<CLEAN_ROOT>') for v in args[1:]],
                    'returncode':result.returncode,'elapsed_seconds':time.perf_counter()-start,
                    'stdout':result.stdout,'stderr':result.stderr}
            receipt['commands'].append(record)
            if result.returncode:raise RuntimeError(json.dumps(record,indent=2))
        receipt['dataset_sha256']=sha(repro/'data/cases.json')
        assert receipt['dataset_sha256']==sha(base/'data/cases.json')
        receipt['results']={p.name:json.loads(p.read_text()) for p in sorted((repro/'raw_results').glob('*.json'))}
        expected={
            'core_exhaustive_v1.json':('conditioning_checks',105292),
            'extensions_v2.json':('counts',None),
            'persistence_v3.json':('counts',None)}
        assert receipt['results']['core_exhaustive_v1.json']['conditioning_checks']==105292
        assert receipt['results']['extensions_v2.json']['counts']['matrices_4x4']==65536
        assert receipt['results']['persistence_v3.json']['counts']['fresh_instance_query_triples']==7070
        assert receipt['results']['legacy_adapter_v2.json']['counts']['queries']==6750
        receipt['status']='PASS'
    receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'commands':len(receipt['commands']),'receipt':str(output)},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('replay_receipt_new.json'))
    main(parser.parse_args().output)
