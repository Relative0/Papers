"""Compare every admitted nonconstant natural output to the repository parser."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parent))
from cmbench.recognition.blif import parse_blif
from corpus import extract,truth_hash

def main():
    base=ROOT/'corpus_v1';records=json.loads((base/'SCREEN.json').read_text());loaded={};checked=0;constants=0;issues=[]
    for rec in records:
        if rec['status']!='success':continue
        path=base/rec['source_path']
        if rec['design'] not in loaded:loaded[rec['design']]=parse_blif(path)
        net=loaded[rec['design']]
        try:
            if rec['structural_support']==0:
                # Reference evaluator excludes constant cones. Independently evaluate its parsed cube graph.
                memo={}
                def value(name):
                    if name in memo:return memo[name]
                    node=net.nodes[name]
                    hit=any(all(c=='-' or value(v)==int(c) for v,c in zip(node.inputs,pat)) for pat in node.cubes)
                    memo[name]=int(hit) if node.cube_output else int(not hit);return memo[name]
                bits=value(rec['output']);n=0;constants+=1
            else:
                bits,names=net.packed_value(rec['output']);n=len(names)
            if truth_hash(bits,n)!=rec['truth_sha256']:issues.append({'design':rec['design'],'output':rec['output'],'issue':'truth hash mismatch'})
            checked+=1
        except Exception as exc:issues.append({'design':rec['design'],'output':rec['output'],'error':repr(exc)})
    result={'status':'PASS' if not issues else 'FAIL','outputs_checked':checked,'constant_outputs_independent_scalar':constants,'issues':issues,
        'extractor_sha256':hashlib.sha256((ROOT/'corpus.py').read_bytes()).hexdigest(),
        'reference_parser_sha256':hashlib.sha256((ROOT.parent/'cmbench/recognition/blif.py').read_bytes()).hexdigest()}
    out=ROOT/'runs/corpus_crosscheck.json'
    if out.exists():raise FileExistsError(out)
    out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return bool(issues)
if __name__=='__main__':sys.exit(main())
