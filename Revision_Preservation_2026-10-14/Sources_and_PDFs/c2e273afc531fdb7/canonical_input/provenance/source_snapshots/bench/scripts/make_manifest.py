from __future__ import annotations
import hashlib,json,os,platform,sys,datetime
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
files={}
for dp,dns,fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d != '__pycache__']
    for fn in sorted(fns):
        p=os.path.join(dp,fn); rel=os.path.relpath(p,ROOT).replace(os.sep,'/')
        if rel in ('manifest.json','Computation_and_Benchmarks.zip') or rel.endswith('.pyc'): continue
        h=hashlib.sha256(open(p,'rb').read()).hexdigest(); files[rel]={"sha256":h,"bytes":os.path.getsize(p)}
manifest={
 "schema":2,
 "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"gate_a_s1_s2_local_completed",
 "protocol":"BENCHMARK_PROTOCOL.md frozen v0.1 with documented source-integration and S2 implementation-correction addenda",
 "seeds":{
   "S1":"seed 0..49 for each depth x affine_fraction x reverse_fraction cell; deterministic case_seed derived in workloads.py",
   "S2":"seed 0..49 for each live_k x depth x shared_fraction x affine_fraction cell; deterministic case_seed derived in workloads.py",
 },
 "safety_budget":{
   "max_monomials":150000,
   "max_pair_terms_per_multiply":2000000,
   "max_pair_terms_total":10000000,
 },
 "environment":{
   "python":sys.version,
   "implementation":platform.python_implementation(),
   "platform":platform.platform(),
   "processor":platform.processor(),
   "cpu_count":os.cpu_count(),
 },
 "headline_counts":{
   "rows_total":10500,
   "rows_admitted":10389,
   "s1_admitted":3750,
   "s2_admitted":6639,
   "budget_rows":111,
   "correctness_mismatches":0,
 },
 "evidence_boundaries":[
   "SC-A is supported by corrected synthetic S1 results",
   "S1/S2 do not satisfy SC-B because SC-B requires a predeclared natural structural stratum",
   "single-pass local timing fields are diagnostic only",
   "SC-C requires XAG optimization and remains open",
   "SC-D requires specialized ZDD/FDD comparison and remains open",
   "the first S2 run is retained under results/superseded and is excluded from corrected conclusions",
   "the user's local Windows folder was not directly accessed",
 ],
 "files":files,
}
with open(os.path.join(ROOT,'manifest.json'),'w',encoding='utf-8') as f: json.dump(manifest,f,indent=2,sort_keys=True)
