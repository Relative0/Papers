"""Fresh-process full-lifecycle RSS on the already frozen cold-panel cases.
These extra instrumentation timings are not pooled with scientific timing cells.
"""
from common import *
import argparse,subprocess,signal
def child(config,out):
    from campaign import trial,alarm
    signal.signal(signal.SIGALRM,alarm);cfg=json.loads(config.read_text());c=cfg['case']
    row=trial(c,min(2,c['n']),cfg['method'],'fresh_object_reload',64,0)
    row['mode']='isolated_full_lifecycle_memory';row['rss_scope']='fresh process for this case/method, includes construction, verification and reload; absolute process RSS'
    write(out,row)
def main():
    from campaign import METHODS
    cases=json.loads((ROOT/'inputs/TIMING_CASES.json').read_text());logs=ROOT/'logs/memory';logs.mkdir(parents=True,exist_ok=True)
    out=ROOT/'results/ISOLATED_MEMORY.json'
    if out.exists():raise FileExistsError(out)
    records=[]
    for c in cases:
        if c['kind']!='natural' and c['p']!=8:continue
        for method in METHODS:
            tag=sha((c['case_id']+method).encode())[:18];cfg=logs/f'{tag}.config.json';result=logs/f'{tag}.result.json'
            write(cfg,{'case':c,'method':method});cmd=[sys.executable,str(ROOT/'isolated_memory.py'),'child','--config',str(cfg),'--output',str(result)];start=time.perf_counter_ns()
            try:
                with (logs/f'{tag}.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=90)
                row=json.loads(result.read_text()) if p.returncode==0 and result.exists() else {'status':'FAIL','case_id':c['case_id'],'method':method,'returncode':p.returncode}
            except subprocess.TimeoutExpired:row={'status':'TIMEOUT','case_id':c['case_id'],'method':method}
            row['command']=cmd;row['process_wall_ns']=time.perf_counter_ns()-start;records.append(row);write(out,records)
        print(c['case_id'],len(records),flush=True)
    write(ROOT/'results/ISOLATED_MEMORY_SUMMARY.json',{'statuses':dict(Counter(x['status'] for x in records)),
      'actual_extra_queries':sum(x['query_count'] for x in records if x['status']=='PASS'),'actual_extra_updates':sum(x['update_count'] for x in records if x['status']=='PASS'),
      'source_sha256':sha(Path(__file__).read_bytes()),'scope':'additional instrumentation panel, not pooled with main timings'})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['run','child']);p.add_argument('--config',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    main() if a.mode=='run' else child(a.config,a.output)
