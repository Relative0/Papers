"""Untimed source checks and independent Theory replay, separate from campaign timing."""
from common import *
import importlib.util,platform,subprocess,os
def theory():
    spec=importlib.util.spec_from_file_location('frozen_theory',ROOT/'theory/verify_profile_moment_state.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.OUT=ROOT/'results/theory_replay.json';m.main()
    assert json.loads(m.OUT.read_text())==json.loads((ROOT/'theory/t3_verification_results.json').read_text())
def sources():
    sys.path.insert(0,str(PRIOR));import corpus
    sys.path.insert(0,str(PRIOR/'inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code'));from artifacts import matrix_rows,rank_factor
    cases=json.loads((ROOT/'inputs/TIMING_CASES.json').read_text());rows=[]
    for c in cases:
        if c['kind']!='natural':continue
        ph={};t=time.perf_counter_ns();source=PRIOR/'corpus_v1'/c['source_path'];actual=sha(source.read_bytes());ph['source_read_hash_ns']=time.perf_counter_ns()-t;assert actual==c['source_sha256']
        t=time.perf_counter_ns();bits,names=corpus.extract(source,c['output']);ph['parse_extract_ns']=time.perf_counter_ns()-t
        t=time.perf_counter_ns();m,right=matrix_rows(bits,tuple(range(c['n'])),tuple(c['left']));u,b=rank_factor(m);w=[sum(((v>>y)&1)<<i for i,v in enumerate(b)) for y in range(1<<c['q'])];ph['factor_discovery_ns']=time.perf_counter_ns()-t
        t=time.perf_counter_ns();assert list(u)==c['U'] and w==c['W'] and list(names)==c['variable_names'] and corpus.truth_hash(bits,c['n'])==c['truth_sha256'];ph['source_factor_verification_ns']=time.perf_counter_ns()-t
        rows.append({'case_id':c['case_id'],'status':'PASS','source_sha256':actual,'factor_sha256':c['factor_sha256'],'phases_ns':ph,'total_ns':sum(ph.values()),'note':'actual separately executed upstream BLIF-to-supplied-factor step; not silently included in artifact-input timing'})
    write(ROOT/'results/SOURCE_PREPARATION.json',rows)
def environment():
    import dd.cudd,sysconfig
    data={'python':sys.version,'platform':platform.platform(),'cpu_count':os.cpu_count(),'clock':str(time.get_clock_info('perf_counter')),
          'dependencies':{n:importlib.metadata.version(n) for n in ('dd','numpy','astutils','networkx','ply','setuptools')},
          'compiler_command':['g++','-std=c++17','-O3','-DNDEBUG','-fPIC','-shared','native_count.cpp','-o','native_count.so'],
          'compiler_version':subprocess.check_output(['g++','--version'],text=True),'native_sha256':sha((ROOT/'native_count.so').read_bytes()),
          'cudd_extension_sha256':sha(Path(dd.cudd.__file__).read_bytes()),'cudd_upstream_wheel_build_flags':'not exposed; previous delivery pins wheel',
          'cpuinfo':Path('/proc/cpuinfo').read_text().split('\n\n')[0],'meminfo':Path('/proc/meminfo').read_text(),
          'protocol_sha256':sha((ROOT/'PROTOCOL.json').read_bytes()),'runpod':'not used','python_build_flags':sysconfig.get_config_var('CFLAGS')}
    write(ROOT/'ENVIRONMENT.json',data)
if __name__=='__main__':
    import importlib.metadata
    {'theory':theory,'sources':sources,'environment':environment}[sys.argv[1]]()
