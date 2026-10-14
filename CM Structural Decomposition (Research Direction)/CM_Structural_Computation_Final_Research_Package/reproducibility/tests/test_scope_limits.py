"""Document numerical cap versus actual JSON integer conversion policy.

The guard is not disabled globally. SC binary round trips are tested at n=14,16.
"""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from artifacts import Artifact
from codec import dumps_binary,loads_binary
from baselines import PackedTruth

def run():
    guard=getattr(sys,'get_int_max_str_digits',lambda:0)()
    rows=[]
    for n in (14,16):
        truth=(1<<(1<<n))-1
        a=Artifact('flat',tuple(range(n)),(truth,))
        blob=dumps_binary(a);loaded=loads_binary(blob)
        assert loaded.scope==a.scope and loaded.payload==a.payload and loaded.count()==1<<n
        row={'n':n,'binary_bytes':len(blob),'binary_roundtrip':'PASS','unconditional_count':1<<n}
        for name,writer in [('artifact_json',a.dumps),('packed_json',PackedTruth(truth,n).dumps)]:
            try:writer();row[name]='accepted by current Python integer conversion policy'
            except ValueError as e:
                if 'integer string conversion' not in str(e):raise
                row[name]='rejected by Python decimal conversion guard'
        if guard==4300:
            assert all(row[k].startswith('rejected') for k in ('artifact_json','packed_json'))
        rows.append(row)
    return {'status':'PASS; policy limitation reproduced, not silently disabled','python_decimal_guard':guard,
            'cases':rows,'implication':'n<=16 is a numerical policy cap, not a guarantee that every JSON encoding works; measured cases stop at n=12'}

if __name__=='__main__':
    out=run();root=Path(__file__).resolve().parents[1]
    (root/'raw_results/scope_limits_v3.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
