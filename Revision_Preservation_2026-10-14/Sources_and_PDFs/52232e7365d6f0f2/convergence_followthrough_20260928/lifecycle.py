"""C4 preparation harness. Main T3 campaign deliberately has no launch command.

Smoke timing is infrastructure validation only. Fresh process does not imply
cold OS page cache. Peak RSS is process-wide high-water memory, not payload size.
"""
from pathlib import Path
import argparse, ctypes, hashlib, json, os, platform, random, struct, subprocess, sys, time, traceback
from backends import METHODS, make
from corpus import extract, cut_rank, truth_hash

ROOT=Path(__file__).resolve().parent
PHASES=['source','discover_compile','verify_before','serialize','load','verify_after','index','update','query','warmup']

def sha(data):return hashlib.sha256(data).hexdigest()
def peak_rss():
    if os.name!='nt':
        import resource
        value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform=='darwin' else value*1024)
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
            ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    counters=Counters();counters.cb=ctypes.sizeof(counters)
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);kernel.GetCurrentProcess.restype=wintypes.HANDLE
    psapi=ctypes.WinDLL('psapi',use_last_error=True);psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(counters),counters.cb):raise ctypes.WinError(ctypes.get_last_error())
    return int(counters.PeakWorkingSetSize)

def environment():
    import importlib.metadata, sysconfig
    versions={}
    for name in ('dd','astutils','networkx','ply','setuptools'):
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:pass
    return {'python':sys.version,'platform':platform.platform(),'machine':platform.machine(),'processor':platform.processor(),
        'cpu_count':os.cpu_count(),'dependency_versions':versions,'python_compiler':platform.python_compiler(),
        'python_build_flags':sysconfig.get_config_var('CFLAGS'),'cudd_compiler_flags':'upstream wheel flags not exposed; pin wheel and binary hash',
        'source_hashes':{p.name:sha(p.read_bytes()) for p in ROOT.glob('*.py')},'clock':str(time.get_clock_info('perf_counter'))}

def queries(n,k,count,semantics,seed):
    rng=random.Random(seed);result=[];rho={};order=[];episode=-1
    for i in range(count):
        if semantics=='independent':
            rho={v:rng.randrange(2) for v in rng.sample(range(n),k)};delta=dict(rho);episode=i
        else:
            if i%max(k,1)==0:
                episode+=1;rho={};order=rng.sample(range(n),k)
            delta={} if k==0 else {order[i%k]:rng.randrange(2)};rho.update(delta)
        result.append({'episode':episode,'restriction':dict(rho),'delta':delta})
    return result

def scalar_count(bits,n,rho):
    return sum((bits>>a)&1 for a in range(1<<n) if all(((a>>(n-1-v))&1)==b for v,b in rho.items()))

def worker(config_path,output):
    cfg=json.loads(config_path.read_text());cfg['blob_path']=str(Path(cfg['blob_path']).resolve())
    rec={'status':'RUNNING','config':cfg,'phases_ns':{p:0 for p in PHASES},'started_ns':time.time_ns(),'environment':environment()}
    def measure(name,fn):
        start=time.perf_counter_ns()
        try:return fn()
        finally:rec['phases_ns'][name]+=time.perf_counter_ns()-start
    begin=time.perf_counter_ns()
    try:
        def source():
            case=json.loads(Path(cfg['case_path']).read_text())
            if 'raw_source' in case:
                bits,names=extract(Path(case['raw_source']),case['output']);n=len(names)
            else:bits=int(case['truth_hex'],16);n=case['n']
            return case,bits,n
        case,bits,n=measure('source',source);left=tuple(case['left']);method=cfg['method']
        if not 0<=cfg['k']<=n:raise ValueError('invalid depth')
        qq=queries(n,cfg['k'],cfg['query_count'],cfg['semantics'],cfg['seed'])
        # Metadata/oracle preparation is explicit validation overhead outside method phases.
        meta_start=time.perf_counter_ns();r=cut_rank(bits,n,left)
        expected=[scalar_count(bits,n,q['restriction']) for q in qq]
        rec['oracle_metadata_ns']=time.perf_counter_ns()-meta_start
        rec.update(n=n,p=len(left),q=n-len(left),actual_rank=r,stored_width=r if method=='coordinate_rank_baseline' else None,
            cut_order=list(left)+[v for v in range(n) if v not in left],k=cfg['k'],total_restriction_budget=cfg['k'],
            state_type=method,query_count=cfg['query_count'],restriction_semantics=cfg['semantics'],reuse_mode=cfg['mode'],
            truth_sha256=truth_hash(bits,n),query_sha256=sha(json.dumps(qq,sort_keys=True).encode()),
            cold_cache_claim=False,process_id=os.getpid(),peak_rss_start_bytes=peak_rss())
        blob_path=Path(cfg['blob_path'])
        def verify(obj):
            for a in range(1<<n):
                assignment={j:(a>>(n-1-j))&1 for j in range(n)}
                if obj.point(assignment)!=(bits>>a)&1:raise AssertionError(('source mismatch',a))
        if cfg['role']!='load_only':
            obj=measure('discover_compile',lambda:make(method,bits,n,left))
            measure('verify_before',lambda:verify(obj))
            def save():
                blob=obj.dumps();blob_path.parent.mkdir(parents=True,exist_ok=True);blob_path.write_bytes(blob);return len(blob)
            rec['serialized_bytes']=measure('serialize',save)
            if cfg['role']=='prepare_only':
                rec['status']='PASS';return rec
            del obj
        rec['serialized_bytes']=blob_path.stat().st_size
        rec['artifact_sha256']=sha(blob_path.read_bytes())
        rec['cache_policy']=cfg.get('cache_policy','uncontrolled_OS_cache')
        if rec['cache_policy']=='advisory_evict':
            if not hasattr(os,'posix_fadvise'):raise RuntimeError('advisory cold-load requires POSIX fadvise')
            cache_start=time.perf_counter_ns()
            with blob_path.open('rb') as cache_file:
                os.fsync(cache_file.fileno())
                os.posix_fadvise(cache_file.fileno(),0,0,os.POSIX_FADV_DONTNEED)
            rec['cache_preparation_ns']=time.perf_counter_ns()-cache_start
            rec['cache_note']='file-specific advisory eviction; host/filesystem may retain pages; physical cold-cache claim remains false'
        obj=measure('load',lambda:METHODS[method].loads(blob_path.read_bytes()))
        measure('verify_after',lambda:verify(obj))
        measure('index',obj.index)
        if cfg['mode']=='warm_reuse':
            # Exactly one full warm-up batch is charged and its answers checked.
            warm=measure('warmup',lambda:[obj.query(q['restriction']) for q in qq])
            assert warm==expected
        answers=[];state=obj;episode=None;per_query=[]
        for spec,want in zip(qq,expected):
            row={'restriction':spec['restriction'],'episode':spec['episode'],
                 'residual_row_dimensions':1<<(len(left)-len(set(left)&spec['restriction'].keys())),
                 'residual_column_dimensions':1<<(n-len(left)-len((set(range(n))-set(left))&spec['restriction'].keys()))}
            before=dict(rec['phases_ns'])
            if cfg['semantics']=='sequential_cumulative':
                if episode!=spec['episode']:state=obj;episode=spec['episode']
                state=measure('update',lambda:state.condition(spec['delta']))
                measure('index',state.index)
                answer=measure('query',lambda:state.query({}))
            else:answer=measure('query',lambda:obj.query(spec['restriction']))
            if answer!=want:raise AssertionError(('count mismatch',spec,answer,want))
            answers.append(answer);row.update(answer=answer,phase_ns={p:rec['phases_ns'][p]-before[p] for p in ('update','index','query')})
            per_query.append(row)
        rec.update(status='PASS',executed_queries=len(answers),warmup_queries=len(qq) if cfg['mode']=='warm_reuse' else 0,
                   answer_sha256=sha(json.dumps(answers).encode()),per_query=per_query)
    except Exception as exc:rec.update(status='FAIL',error=repr(exc),traceback=traceback.format_exc())
    finally:
        rec.update(elapsed_ns=time.perf_counter_ns()-begin,peak_rss_bytes=peak_rss(),finished_ns=time.time_ns())
        rec['method_phase_total_ns']=sum(rec['phases_ns'].values())
        rec['memory_scope']='process-wide absolute high-water RSS; includes runtime, input and verification; not incremental backend allocation'
        output.write_text(json.dumps(rec,indent=2))
    return rec

def invoke(cfg,folder,timeout=90):
    folder.mkdir(parents=True,exist_ok=False);config=folder/'command.json';result=folder/'result.json'
    config.write_text(json.dumps(cfg,indent=2));command=[sys.executable,str(Path(__file__).resolve()),'worker','--config',str(config),'--output',str(result)]
    start=time.perf_counter_ns()
    with (folder/'stdout.log').open('w') as out,(folder/'stderr.log').open('w') as err:
        try:
            cp=subprocess.run(command,stdout=out,stderr=err,timeout=timeout)
            rec=json.loads(result.read_text()) if result.exists() else {'status':'FAIL','error':'no result'}
            rec['returncode']=cp.returncode
        except subprocess.TimeoutExpired:rec={'status':'TIMEOUT','timeout_seconds':timeout}
    rec['command']=command;rec['parent_wall_ns']=time.perf_counter_ns()-start
    (folder/'execution.json').write_text(json.dumps(rec,indent=2));return rec

def smoke(output,methods):
    output.mkdir(parents=True,exist_ok=False);records=[]
    # Tiny fixtures exercise endpoints only; do not estimate T3 performance.
    fixtures=[('zero',0,0),('one',1,0),('rectangle',0x8888,4),('parity',0x6996,4),('unequal',0x914725ab,5)]
    for label,bits,n in fixtures:
        case=output/(label+'.json');case.write_text(json.dumps({'truth_hex':hex(bits),'n':n,'left':list(range(n//2))}))
        for method in methods:
            for semantics in ('independent','sequential_cumulative'):
                for mode in ('same_process_fresh_object','fresh_process_load','warm_reuse'):
                    key=f'{label}_{method}_{semantics}_{mode}'
                    cfg={'case_path':str(case.resolve()),'method':method,'k':min(2,n),'query_count':8,
                        'semantics':semantics,'mode':mode,'seed':20260928,'blob_path':str((output/(key+'.bin')).resolve()),'role':'full'}
                    if mode=='fresh_process_load':
                        prep=invoke({**cfg,'role':'prepare_only'},output/(key+'_prepare'))
                        if prep['status']!='PASS':records.append({'key':key,'prepare':prep});continue
                        run=invoke({**cfg,'role':'load_only'},output/key)
                        records.append({'key':key,'prepare':prep,'run':run,
                            'combined_method_phase_total_ns':prep['method_phase_total_ns']+run.get('method_phase_total_ns',0)})
                    else:records.append({'key':key,'run':invoke(cfg,output/key)})
        print('Infrastructure fixture',label,'complete',flush=True)
    (output/'SUMMARY.json').write_text(json.dumps({'purpose':'infrastructure smoke, not T3 performance campaign','trials':records,
        'status':'PASS' if all(x.get('run',{}).get('status')=='PASS' for x in records) else 'FAIL'},indent=2))
    print('Smoke trials',len(records),'failures',sum(x.get('run',{}).get('status')!='PASS' for x in records))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['worker','smoke']);p.add_argument('--config',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--methods',nargs='+',default=['packed_binary','coordinate_rank_baseline'])
    a=p.parse_args()
    if a.mode=='worker':sys.exit(0 if worker(a.config,a.output)['status']=='PASS' else 1)
    smoke(a.output,a.methods)
