from __future__ import annotations
import argparse, json
from pathlib import Path
import n2_p2_harness as h

ap=argparse.ArgumentParser()
ap.add_argument('--mode',choices=['fuzz','natural','gatep'],required=True)
ap.add_argument('--case-id')
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args()
a.out.parent.mkdir(parents=True,exist_ok=True)
if a.mode=='fuzz':
    x=h.fuzz_p2(); payload={'mode':'fuzz','fuzz':x}
elif a.mode=='natural':
    cases,selection,selsha=h.freeze_cases(h.HERE/'epfl',h.HERE)
    matches=[c for c in cases if c['case_id']==a.case_id]
    if len(matches)!=1: raise SystemExit(f'case not found/ambiguous {a.case_id}: {len(matches)}')
    nsym,ntime=h.natural_campaign(matches)
    payload={'mode':'natural','case_id':a.case_id,'selection_sha256':selsha,'symbolic':nsym,'timing':ntime}
else:
    gsym,gtime=h.gatep_campaign(); payload={'mode':'gatep','symbolic':gsym,'timing':gtime}
a.out.write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(a.out)
