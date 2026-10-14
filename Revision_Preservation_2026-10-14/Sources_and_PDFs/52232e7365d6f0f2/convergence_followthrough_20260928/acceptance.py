"""Final limited lifecycle validation, including raw source and advisory cold load."""
from pathlib import Path
import argparse,json,os
from lifecycle import invoke,environment
ROOT=Path(__file__).resolve().parent

def main(output):
    output.mkdir(parents=True,exist_ok=False)
    cases=json.loads((ROOT/'corpus_v1/CASES.json').read_text())
    natural=next(c for c in cases if c['split']=='development' and 2<=c['n']<=5)
    case=output/'natural.json'
    case.write_text(json.dumps({**natural,'raw_source':str((ROOT/'corpus_v1'/natural['source_path']).resolve())}))
    records=[]
    for method in ('packed_binary','coordinate_rank_baseline','cudd_fixed_order_binary'):
        for sem in ('independent','sequential_cumulative'):
            for mode in ('same_process_fresh_object','warm_reuse','fresh_process_load'):
                key=f'{method}_{sem}_{mode}'
                cfg={'case_path':str(case.resolve()),'method':method,'k':2,'query_count':8,'semantics':sem,'mode':mode,
                    'seed':20260928,'blob_path':str((output/(key+'.bin')).resolve()),'role':'full'}
                if mode=='fresh_process_load':
                    prep=invoke({**cfg,'role':'prepare_only'},output/(key+'_prepare'));assert prep['status']=='PASS'
                    cfg.update(role='load_only',cache_policy='advisory_evict')
                    result=invoke(cfg,output/key)
                    records.append({'key':key,'prepare':prep,'result':result})
                else:records.append({'key':key,'result':invoke(cfg,output/key)})
                print(key,records[-1]['result']['status'],flush=True)
    result={'status':'PASS' if all(x['result']['status']=='PASS' for x in records) else 'FAIL',
        'purpose':'one development natural case infrastructure test; not main campaign or holdout timing',
        'case_id':natural['case_id'],'trials':records,'environment':environment()}
    (output/'SUMMARY.json').write_text(json.dumps(result,indent=2))
    if result['status']!='PASS':raise RuntimeError('acceptance failure')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
