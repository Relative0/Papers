from __future__ import annotations
import json, os, platform, time, hashlib
from pathlib import Path
import n2_p1_harness as h
ROOT=Path('/mnt/data/cm_n2_p1'); CH=ROOT/'chunks'
selection=json.loads((ROOT/'natural_selection_frozen.json').read_text())
# Load all chunks and concatenate, with strict completeness checks.
nsym=[]; ntime=[]
for p in sorted(CH.glob('*.json')):
    d=json.loads(p.read_text())
    nsym.extend(d.get('symbolic',[])); ntime.extend(d.get('timing',[]))
case_ids=[]
for c in selection['circuits']:
    for x in c['selected']:
        case_ids.append(f"{c['circuit']}:{x['root']}")
assert len(case_ids)==10, case_ids
# Strict symbolic and timing coverage.
for cid in case_ids:
    sr=[r for r in nsym if r['case_id']==cid]
    tr=[r for r in ntime if r['case_id']==cid]
    assert len(sr)==len(h.ARMS), (cid,len(sr))
    assert {r['arm'] for r in sr}==set(h.ARMS), cid
    assert len(tr)==h.NATURAL_TIMING_REPS*len(h.ARMS), (cid,len(tr))
    assert sorted(r['rep'] for r in tr)==list(range(h.NATURAL_TIMING_REPS*len(h.ARMS))), cid
    for arm in h.ARMS:
        assert sum(r['arm']==arm for r in tr)==h.NATURAL_TIMING_REPS, (cid,arm)
assert len(nsym)==50, len(nsym); assert len(ntime)==750, len(ntime)
assert all(r['ok'] for r in nsym+ntime)
# Gate-P and fuzz are fast and rerun once for final payload.
fuzz=h.fuzz_profit(); assert fuzz['passed']
gsym,gtime=h.gatep_campaign(); assert all(r['ok'] for r in gsym+gtime)
summary=h.summarize(nsym,ntime,gsym,gtime,fuzz)
selsha=h.sha256_file(ROOT/'natural_selection_frozen.json')
meta={'schema':'cm-n2-p1-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_s':None,
      'prereg_sha256':h.PREREG_SHA256,'preregistered_harness_sha256':'469911b7e6e4a5222aa023dfddbc87e3075bbc5d595f16cc82cc2b7f456ffa5f',
      'executed_harness_sha256':h.sha256_file(ROOT/'n2_p1_harness.py'),'natural_selection_sha256':selsha,'epfl_commit':h.EPFL_COMMIT,'seed':h.SEED,
      'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
      'execution_note':'The frozen harness was executed in case/chunk orchestration because the container enforces a short per-command wall limit. The selector, arms, schedules, repetition counts, seeds, and success criterion were unchanged. Structural selection was deterministic; debug orchestration re-emitted its JSON timestamp only, without changing selected roots.',
      'protocol':{'arms':h.ARMS,'natural_timing_reps':h.NATURAL_TIMING_REPS,'gatep_timing_reps':h.GATEP_TIMING_REPS,
                  'gatep_depths':h.GATEP_DEPTHS,'gatep_cases_per_depth':h.GATEP_CASES_PER_DEPTH,'fuzz_cases':h.FUZZ_CASES,
                  'selector':{'monomial_cap':h.MONOMIAL_CAP,'benefit_min':h.BENEFIT_MIN,'shared_fraction_min':h.SHARED_FRACTION_MIN,'unshared_fraction_min':h.UNSHARED_FRACTION_MIN}}}
payload={'meta':meta,'selection':selection,'summary':summary,'natural_symbolic_rows':nsym,'natural_timing_rows':ntime,'gatep_symbolic_rows':gsym,'gatep_timing_rows':gtime,'fuzz':fuzz}
(ROOT/'n2_p1_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
report=h.make_report(meta,selection,summary,nsym,ntime,gsym,gtime)
report += '\n## Execution/orchestration note\n\n' + meta['execution_note'] + '\n'
(ROOT/'N2_P1_RESULTS.md').write_text(report,encoding='utf-8')
# Source manifest with cryptographic provenance.
sources=[]
for circuit,(fname,blob_expected) in h.NATURAL_SOURCES.items():
    p=ROOT/'epfl'/fname; b=p.read_bytes(); blob=hashlib.sha1(f'blob {len(b)}\\0'.encode()+b).hexdigest()
    # Above literal backslash-zero is wrong for Git object; compute canonical separately.
    blob=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
    sources.append({'circuit':circuit,'file':fname,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':blob,'expected_git_blob_sha1':blob_expected,'verified':blob==blob_expected})
assert all(x['verified'] for x in sources)
manifest={'schema':'cm-n2-p1-epfl-source-manifest/v1','epfl_repository':'lsils/benchmarks','epfl_commit':h.EPFL_COMMIT,'sources':sources}
(ROOT/'EPFL_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'summary':summary,'counts':{'natural_symbolic':len(nsym),'natural_timing':len(ntime),'gatep_symbolic':len(gsym),'gatep_timing':len(gtime)},'selection_sha256':selsha},indent=2))
