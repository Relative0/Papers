"""Read original code, redirect every certificate write into this review."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import contextlib, hashlib, importlib, json, platform, time
import sympy
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
GATE=PROJECT/'Interaction Core Gate 2026-09-29'
OUT=ROOT/'regenerated_certificates'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(GATE))

def snapshot():
    roots=[GATE,PROJECT/'Manuscript Convergence 2026-09-29',PROJECT/'Transferred Research'/'MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29']
    return {str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for root in roots for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    before=snapshot(); start=time.perf_counter()
    receipt={'python':platform.python_version(),'sympy':sympy.__version__}
    with (ROOT/'supplied_verifiers_stdout.txt').open('w',encoding='utf-8') as log, contextlib.redirect_stdout(log):
        for values in ([[2,4,0],[0,6,0]],[[1,2],[3,4]],[[0,0],[0,0]]):
            a=DomainMatrix.from_Matrix(Matrix(values)).convert_to(ZZ)
            d,s,t=smith_normal_decomp(a)
            assert d.to_Matrix()==s.to_Matrix()*a.to_Matrix()*t.to_Matrix()
            assert abs(s.to_Matrix().det())==abs(t.to_Matrix().det())==1
        cert=importlib.import_module('verify_d2_certificate')
        data=json.loads((GATE/'minimal_star_d2.json').read_text())
        cert.ROOT=OUT
        cert.run(data)
        cert.c4_case()
        torsion=importlib.import_module('verify_torsion_star')
        torsion.ROOT=OUT
        torsion.main()
    comparisons={}
    for name in ['star_d2_integral_certificate.json','c4_d2_integral_certificate.json','interaction_torsion_star.json']:
        old=json.loads((GATE/name).read_text()); new=json.loads((OUT/name).read_text())
        differences={k:{'prior':old.get(k),'regenerated':new.get(k)} for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
        assert set(differences)<={'minimality_scope','induced_subsets_checked_by_size'}
        comparisons[name]={'mathematical_fields_equal':True,'annotation_differences':differences}
    after=snapshot()
    assert before==after, 'Source/evidence file changed'
    integration=json.loads((PROJECT/'Manuscript Convergence 2026-09-29'/'INTEGRATION_RECEIPT.json').read_text())
    for name,sha in integration['input_sha256'].items():
        assert hashlib.sha256((PROJECT/name).read_bytes()).hexdigest()==sha
    assert hashlib.sha256((PROJECT/'Manuscript Convergence 2026-09-29'/integration['output']).read_bytes()).hexdigest()==integration['output_sha256']
    receipt.update({'checks_passed':True,'smith_convention_and_unimodularity':True,'source_files_unchanged':len(before),'integration_hashes_match':True,'certificate_comparison':comparisons,'elapsed_seconds':round(time.perf_counter()-start,3)})
    (ROOT/'source_hashes_at_verification.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    (ROOT/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
