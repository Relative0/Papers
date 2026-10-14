from __future__ import annotations
import json,time,platform,os
from pathlib import Path
import n2_p2_harness as h

HERE=Path(__file__).resolve().parent
chunks=HERE/'chunks'
fuzz=json.loads((chunks/'fuzz.json').read_text())['fuzz']
nsym=[]; ntime=[]
for p in sorted(chunks.glob('natural_*.json')):
    x=json.loads(p.read_text()); nsym.extend(x['symbolic']); ntime.extend(x['timing'])
g=json.loads((chunks/'gatep.json').read_text()); gsym=g['symbolic']; gtime=g['timing']
# Recompute/verify the exact frozen selection and source hashes one more time.
cases,selection,selsha=h.freeze_cases(HERE/'epfl',HERE)
expected=sorted(c['case_id'] for c in cases); got=sorted({r['case_id'] for r in nsym})
if got!=expected: raise SystemExit(f'natural chunk cases mismatch got={got} expected={expected}')
summary=h.summarize(nsym,ntime,gsym,gtime,fuzz)
meta={'schema':'cm-n2-p2-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_s':None,
      'prereg_sha256':h.PREREG_SHA256,'harness_sha256':h.sha256_file(HERE/'n2_p2_harness.py'),'natural_selection_sha256':selsha,
      'epfl_commit':h.p1.EPFL_COMMIT,'seed':h.SEED,'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
      'execution':'chunked replay of frozen harness; no selector/rule changes',
      'protocol':{'arms':h.ARMS,'natural_timing_reps':h.NATURAL_TIMING_REPS,'gatep_timing_reps':h.GATEP_TIMING_REPS,'fuzz_cases':h.FUZZ_CASES,
                  'selector':{'monomial_cap':h.p1.MONOMIAL_CAP,'benefit_min':h.p1.BENEFIT_MIN,'shared_fraction_min':h.p1.SHARED_FRACTION_MIN,'unshared_fraction_min':h.p1.UNSHARED_FRACTION_MIN}}}
payload={'meta':meta,'selection':selection,'summary':summary,'natural_symbolic_rows':nsym,'natural_timing_rows':ntime,'gatep_symbolic_rows':gsym,'gatep_timing_rows':gtime,'fuzz':fuzz}
(HERE/'n2_p2_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
(HERE/'N2_P2_RESULTS.md').write_text(h.report(meta,selection,summary,nsym,gsym),encoding='utf-8')
print(json.dumps(summary,indent=2))
