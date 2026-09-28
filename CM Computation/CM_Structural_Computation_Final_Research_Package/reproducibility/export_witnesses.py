"""Export selected exact witnesses in both serializations, with externally bound hashes."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from artifacts import discover
from codec import dumps_binary,loads_binary
from checker import verify

def main():
    cases=json.loads((ROOT/'data/cases.json').read_text())
    dest=ROOT/'data/selected_witnesses';dest.mkdir(exist_ok=True)
    index=[]
    for i,case in enumerate(cases):
        truth=int(case['truth_hex'],16)
        for policy in ('json','binary'):
            a,_=discover(truth,case['n'],16,encoding=policy)
            assert verify(a,truth)
            binary=dumps_binary(a);assert verify(loads_binary(binary),truth)
            jsonblob=a.dumps();stem=f'{i:02d}_{policy}'
            (dest/(stem+'.json')).write_bytes(jsonblob+b'\n');(dest/(stem+'.scb')).write_bytes(binary)
            index.append({'case_id':case['id'],'n':case['n'],'truth_hex':case['truth_hex'],'selection':policy,
                          'kind':a.kind,'ideal_bits':a.ideal_bits(),'json_bytes':len(jsonblob),'binary_bytes':len(binary),
                          'json_file':stem+'.json','binary_file':stem+'.scb',
                          'json_sha256':hashlib.sha256(jsonblob+b'\n').hexdigest(),
                          'binary_sha256':hashlib.sha256(binary).hexdigest(),
                          'note':'JSON file has one extra final newline, excluded from benchmark JSON byte size'})
    (dest/'INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
    print(json.dumps({'exported_witnesses':len(index),'external_equivalence':'PASS'},indent=2))
if __name__=='__main__':main()
