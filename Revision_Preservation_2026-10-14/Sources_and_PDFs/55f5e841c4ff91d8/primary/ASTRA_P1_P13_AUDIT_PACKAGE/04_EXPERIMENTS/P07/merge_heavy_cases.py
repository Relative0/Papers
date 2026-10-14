import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def merge(case_id,subdir,outname):
    d=HERE/'natural'/subdir
    symmem=json.load(open(d/'symmem.json'))
    lower=[]; pipe=[]
    for p in sorted(d.glob('lower_*.json')): lower += json.load(open(p)).get('lower_timing_rows',[])
    for p in sorted(d.glob('pipe_*.json')): pipe += json.load(open(p)).get('pipeline_timing_rows',[])
    # validate schedule indexes exactly once
    lr=sorted(r['rep'] for r in lower); pr=sorted(r['rep'] for r in pipe)
    assert lr==list(range(100)), (case_id,'lower',lr[:5],lr[-5:],len(lr))
    assert pr==list(range(60)), (case_id,'pipe',pr[:5],pr[-5:],len(pr))
    obj={'schema':'cm-n2-p7-natural-case/v1','case_id':case_id,'selection_sha256':symmem['selection_sha256'],
         'symbolic_rows':symmem['symbolic_rows'],'lower_timing_rows':sorted(lower,key=lambda r:r['rep']),
         'pipeline_timing_rows':sorted(pipe,key=lambda r:r['rep']),'pipeline_memory_rows':symmem['pipeline_memory_rows']}
    (HERE/'natural'/outname).write_text(json.dumps(obj,indent=2)+'\n')
    print(case_id,len(obj['symbolic_rows']),len(lower),len(pipe),len(obj['pipeline_memory_rows']))
merge('priority:new_n174','priority174_chunks','priority_new_n174.json')
merge('cavlc:35','cavlc35_chunks','cavlc_35.json')
