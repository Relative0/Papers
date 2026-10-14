"""Frozen bounded local campaign; actual calls, separated phases, raw trials retained."""
from common import *
from state import State
from comparators import Native,Raw,Histogram,cudd_blob
import os,random,resource,signal,subprocess,tempfile,traceback,gc,ctypes,mmap,argparse,platform,importlib.metadata
METHODS=['t3_dense_row','t3_sparse_row','t3_sparse_column','t3_adaptive','raw_factor','draft3_histogram','packed_native','cudd_native']
def clock():return time.perf_counter_ns()
def timed(ph,key,fn):
    t=clock();v=fn();ph[key]=ph.get(key,0)+clock()-t;return v
def make(method,c,k):
    if method.startswith('t3'):
        orientation=payloads(c,k)['chosen_orientation'] if method=='t3_adaptive' else 'column' if method=='t3_sparse_column' else 'row'
        s=(1<<c['r'])-1 if method=='t3_dense_row' else len(set(c['U'] if orientation=='row' else c['W'])-{0})
        cells=s*(D(c['p'],k)+D(c['q'],k))
        if (method=='t3_dense_row' and c['r']>12) or cells>200000:raise NotImplementedError(f'preregistered allocation cap: {cells} counters')
        return State(c,k,orientation,method=='t3_dense_row')
    if method=='raw_factor':return Raw(c)
    if method=='draft3_histogram':return Histogram(c)
    if method=='packed_native':return Native.packed(c)
    return Native.loads(cudd_blob(c))
def loader(method):return State.loads if method.startswith('t3') else Raw.loads if method=='raw_factor' else Histogram.loads if method=='draft3_histogram' else Native.loads
def plan(c,k,batch,rep):
    seed=int(sha(f"{c['case_id']}:{k}:{rep}:20260928".encode())[:16],16);rng=random.Random(seed)
    path=[(z,rng.randrange(2)) for z in rng.sample(c['left']+c['right'],k)]
    rho={};expected=[oracle(c,rho)]
    for z,b in path:rho[z]=b;expected.append(oracle(c,rho))
    return path,expected,seed
def metadata(c,k,method,mode,batch,rep,path,expected,seed):
    return {'case_id':c['case_id'],'design':c['design'],'family':c['family'],'kind':c['kind'],'split':c['split'],
      'n':c['n'],'p':c['p'],'q':c['q'],'r':c['r'],'actual_rank':c['actual_rank'],'k':k,'left':c['left'],'right':c['right'],
      'method':method,'mode':mode,'batch':batch,'rep':rep,'seed':seed,'path':path,'expected':expected,
      'factor_sha256':c['factor_sha256'],'query_sha256':sha(json.dumps([path,batch]).encode()),'payloads':payloads(c,k),
      'query_count':(k+1)*batch,'update_count':k,'restriction_semantics':'cumulative distinct-coordinate destructive',
      'orientation':payloads(c,k)['chosen_orientation'] if method=='t3_adaptive' else 'column' if method=='t3_sparse_column' else 'row' if method.startswith('t3') else None}
def execute(obj,rec,ph):
    ops=[];rho={};left=set(rec['left']);right=set(rec['right']);total=0
    for depth in range(rec['k']+1):
        if depth:
            z,b=rec['path'][depth-1];t=clock();obj.update(z,b);update_ns=clock()-t;ph['update']=ph.get('update',0)+update_ns;rho[z]=b
        else:update_ns=0
        values=[];dur=[]
        for _ in range(rec['batch']):
            t=clock();values.append(obj.count());dur.append(clock()-t)
        ph['query']=ph.get('query',0)+sum(dur)
        t=clock();assert all(v==rec['expected'][depth] for v in values), (rec['case_id'],rec['method'],depth,values[0],rec['expected'][depth]);ph['verification']=ph.get('verification',0)+clock()-t
        ops.append({'depth':depth,'horizon':rec['k']-depth,'residual_p':len(left-set(rho)),'residual_q':len(right-set(rho)),
          'count':values[0],'executed_queries':len(values),'query_ns':dur,'update_ns':update_ns,
          'moment_counter_operations':getattr(obj,'last_operations',None),'s':getattr(obj,'s',None),
          'live_payload_bits':obj.payload_bits() if isinstance(obj,State) else None})
        total+=len(values)
    assert total==rec['query_count'];rec['operations']=ops
def alarm(sig,frame):raise TimeoutError('preregistered 60 second trial limit')
def trial(c,k,method,mode,batch,rep):
    start=clock();ph={x:0 for x in ('source_read','construction','verification','serialization','file_write','file_read','loading','indexing','update','query')}
    t=clock();path,expected,seed=plan(c,k,batch,rep);oracle_ns=clock()-t
    rec=metadata(c,k,method,mode,batch,rep,path,expected,seed);rec['phases_ns']=ph;rec['oracle_preparation_ns']=oracle_ns
    try:
        signal.alarm(60)
        # Actual parse of the canonical supplied artifact is the primary raw-input endpoint.
        supplied=timed(ph,'source_read',lambda:json.loads(factor_bytes(c)));supplied.update(case_id=c['case_id'])
        obj=timed(ph,'construction',lambda:make(method,supplied,k))
        rec['peak_rss_after_construction_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
        blob=timed(ph,'serialization',obj.dumps);rec['serialized_bytes']=len(blob);rec['artifact_sha256']=sha(blob)
        rec['persistent_payload_bits']=obj.payload_bits() if isinstance(obj,State) else rec['payloads']['raw_factor_bits'] if method in ('raw_factor','draft3_histogram') else (1<<c['n']) if method=='packed_native' else None
        if mode=='fresh_object_reload':
            del obj;obj=timed(ph,'loading',lambda:loader(method)(blob))
        execute(obj,rec,ph);del obj
        rec['status']='PASS'
    except NotImplementedError as e:rec.update(status='UNSUPPORTED',error=str(e))
    except TimeoutError as e:rec.update(status='TIMEOUT',error=str(e))
    except Exception:rec.update(status='FAIL',error=traceback.format_exc())
    finally:signal.alarm(0)
    rec['end_to_end_phases_ns']=sum(ph.values());rec['trial_wall_ns']=clock()-start;rec['peak_rss_process_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    rec['rss_scope']='absolute process high-water; in-process cells share earlier process peak; isolated cold consumer reported separately'
    return rec

def residency(path):
    size=path.stat().st_size;fd=os.open(path,os.O_RDWR);mm=mmap.mmap(fd,size,access=mmap.ACCESS_COPY);buf=(ctypes.c_char*size).from_buffer(mm)
    pages=(size+mmap.PAGESIZE-1)//mmap.PAGESIZE;vec=(ctypes.c_ubyte*pages)();libc=ctypes.CDLL(None,use_errno=True)
    libc.mincore.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
    if libc.mincore(ctypes.addressof(buf),size,vec):raise OSError(ctypes.get_errno(),'mincore')
    resident=sum(v&1 for v in vec);del buf;mm.close();os.close(fd);return {'pages':pages,'resident':resident}
def cold_worker(config,out):
    rec=json.loads(config.read_text());ph=rec['phases_ns'];path=Path(rec.pop('blob_path'));start=clock()
    try:
        before=residency(path);rec['page_cache_before_load']=before
        if before['resident']:raise RuntimeError('page-cold certification failed')
        blob=timed(ph,'file_read',path.read_bytes);obj=timed(ph,'loading',lambda:loader(rec['method'])(blob))
        assert sha(blob)==rec['artifact_sha256'];execute(obj,rec,ph);del obj;rec['status']='PASS'
    except Exception:rec.update(status='FAIL',error=traceback.format_exc())
    rec['consumer_wall_ns']=clock()-start;rec['peak_rss_consumer_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    rec['end_to_end_phases_ns']=sum(ph.values());write(out,rec)
def cold_trial(c,k,method):
    path,expected,seed=plan(c,k,64,0);rec=metadata(c,k,method,'fresh_process_verified_page_cold',64,0,path,expected,seed)
    ph={x:0 for x in ('source_read','construction','verification','serialization','file_write','file_read','loading','indexing','update','query')};rec['phases_ns']=ph
    start=clock();tag=sha(json.dumps([c['case_id'],k,method]).encode())[:18];logs=ROOT/'logs/cold';logs.mkdir(parents=True,exist_ok=True)
    try:
        signal.alarm(60)
        supplied=timed(ph,'source_read',lambda:json.loads(factor_bytes(c)))
        obj=timed(ph,'construction',lambda:make(method,supplied,k));blob=timed(ph,'serialization',obj.dumps)
        rec.update(serialized_bytes=len(blob),artifact_sha256=sha(blob),peak_rss_producer_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
        del obj,supplied
        with tempfile.TemporaryDirectory(prefix='cm-t3-cold-') as temp:
            artifact=Path(temp)/'state.bin';t=clock()
            with artifact.open('wb') as f:f.write(blob);f.flush();os.fsync(f.fileno())
            ph['file_write']=clock()-t;del blob
            t=clock();fd=os.open(artifact,os.O_RDONLY);os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED);os.close(fd);rec['cache_preparation_ns']=clock()-t
            rec['page_cache_producer_check']=residency(artifact);rec['blob_path']=str(artifact)
            config=logs/f'{tag}.config.json';result=logs/f'{tag}.result.json';write(config,rec)
            cmd=[sys.executable,str(ROOT/'campaign.py'),'child','--config',str(config),'--output',str(result)]
            t=clock()
            with (logs/f'{tag}.log').open('w') as f:completed=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=60)
            wall=clock()-t;write(logs/f'{tag}.execution.json',{'command':cmd,'returncode':completed.returncode,'parent_child_wall_ns':wall})
            if completed.returncode or not result.exists():raise RuntimeError('cold child failed')
            rec=json.loads(result.read_text());rec['parent_child_wall_ns']=wall
    except NotImplementedError as e:rec.update(status='UNSUPPORTED',error=str(e))
    except (TimeoutError,subprocess.TimeoutExpired) as e:rec.update(status='TIMEOUT',error=str(e))
    except Exception:rec.update(status='FAIL',error=traceback.format_exc())
    finally:signal.alarm(0)
    rec['producer_and_child_wall_ns']=clock()-start;return rec

def main(section):
    assert sha((ROOT/'PROTOCOL.json').read_bytes())==(ROOT/'PROTOCOL.sha256').read_text().strip()
    assert json.loads((ROOT/'results/correctness_native.json').read_text())['status']=='PASS'
    cases=json.loads((ROOT/'inputs/TIMING_CASES.json').read_text());rng=random.Random(20260928);dest=ROOT/'results'/f'trials_{section}.jsonl'
    if dest.exists():raise FileExistsError(dest)
    counts=Counter();start=time.time()
    with dest.open('w',buffering=1) as out:
        for c in cases:
            if section=='cold':
                if c['kind']!='natural' and c['p']!=8:continue
                for method in rng.sample(METHODS,len(METHODS)):
                    rec=cold_trial(c,min(2,c['n']),method);out.write(json.dumps(rec)+'\n');counts[rec['status']]+=1
            else:
                for k in sorted({min(c['n'],x) for x in [0,1,2,4,c['n']]}):
                    for mode in ('warm_persistent','fresh_object_reload'):
                        for batch in (1,8,64,256):
                            for rep in range(2):
                                for method in rng.sample(METHODS,len(METHODS)):
                                    rec=trial(c,k,method,mode,batch,rep);out.write(json.dumps(rec)+'\n');counts[rec['status']]+=1
            print(c['case_id'],dict(counts),round(time.time()-start,1),flush=True)
    write(ROOT/'results'/f'completion_{section}.json',{'status':'COMPLETE','counts':dict(counts),'seconds':time.time()-start,'source_hashes':{p.name:sha(p.read_bytes()) for p in ROOT.glob('*.py')},'native_sha256':sha((ROOT/'native_count.so').read_bytes())})
if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm)
    p=argparse.ArgumentParser();p.add_argument('section',choices=['main','cold','child']);p.add_argument('--config',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.section=='child':cold_worker(a.config,a.output)
    else:main(a.section)
