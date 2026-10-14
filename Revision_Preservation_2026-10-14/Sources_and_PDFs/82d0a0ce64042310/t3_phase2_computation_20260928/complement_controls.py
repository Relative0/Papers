"""Complete the explicitly requested paired complementary-parity control family."""
from common import *
import random,signal
def freeze():
    cases=json.loads((ROOT/'inputs/TIMING_CASES.json').read_text());out=[]
    for c in cases:
        if c['family']!='rank_two_complementary_parity':continue
        c={**c,'case_id':c['case_id']+'_complement','design':c['design']+'_complement','W':[v^3 for v in c['W']]}
        c['factor_sha256']=sha(factor_bytes(c));out.append(c)
    dest=ROOT/'inputs/COMPLEMENT_CONTROLS.json'
    if dest.exists():raise FileExistsError(dest)
    write(dest,out);write(ROOT/'COMPLEMENT_CONTROL_ADDENDUM.json',{
      'reason':'The primary generator included parity but omitted its explicit complement, despite the frozen family name and user request. This fixed symmetry completion adds every complement at the same five dimensions; it does not alter criteria or replace any previous trial.',
      'cases_sha256':sha(dest.read_bytes()),'frozen_before_extension_outcomes':True,
      'protocol_sha256':sha((ROOT/'PROTOCOL.json').read_bytes()),'grid':'same k, batch, modes, repetitions and methods as main; no outcome-dependent selection'})
def run():
    from campaign import trial,METHODS,alarm
    signal.signal(signal.SIGALRM,alarm);cases=json.loads((ROOT/'inputs/COMPLEMENT_CONTROLS.json').read_text());rng=random.Random(20260928)
    dest=ROOT/'results/trials_complement.jsonl'
    if dest.exists():raise FileExistsError(dest)
    counts=Counter()
    with dest.open('w',buffering=1) as f:
        for c in cases:
            for k in sorted({min(c['n'],v) for v in (0,1,2,4,c['n'])}):
                for mode in ('warm_persistent','fresh_object_reload'):
                    for batch in (1,8,64,256):
                        for rep in range(2):
                            for method in rng.sample(METHODS,len(METHODS)):
                                row=trial(c,k,method,mode,batch,rep);f.write(json.dumps(row)+'\n');counts[row['status']]+=1
            print(c['case_id'],dict(counts),flush=True)
    write(ROOT/'results/completion_complement.json',{'status':'COMPLETE','counts':dict(counts),'source_hashes':{p.name:sha(p.read_bytes()) for p in ROOT.glob('*.py')}})
if __name__=='__main__':freeze() if sys.argv[1]=='freeze' else run()
