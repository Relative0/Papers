"""Reproduce the archived nonlinear output, changing only its output filename.

Run only with the supplied, reviewed original archive. This executes the exact
historical script after a single validated string replacement. It is not a
sandbox for arbitrary untrusted archives.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile


def main() -> None:
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,default=root/'history/original_uploaded_Paper_B.zip')
    parser.add_argument('--out',type=Path,default=root/'evidence/historical_portable_replay')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.archive) as archive:
        suffix='01_CURRENT_MANUSCRIPT_AND_REVIEW_20260924/restricted_guard_probe_case_study.py'
        names=[n for n in archive.namelist() if n.endswith(suffix)]
        if len(names)!=1:raise ValueError('Expected exactly one current historical script.')
        original=archive.read(names[0]).decode('utf-8')
        result_name=names[0].rsplit('/',1)[0]+'/nonlinear_case_study_results.json'
        expected=json.loads(archive.read(result_name))
    old="'/mnt/data/Restricted_Guard_CM_LM_Research_2026-09-24/nonlinear_case_study_results.json'"
    if original.count(old)!=1:raise ValueError('Historical output path contract has changed.')
    output=args.out.resolve()/'nonlinear_case_study_results.json'
    patched=original.replace(old,repr(str(output)))
    script=args.out.resolve()/'historical_output_path_only_patch.py'
    script.write_text(patched)
    run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,check=False)
    (args.out/'stdout.txt').write_text(run.stdout)
    (args.out/'stderr.txt').write_text(run.stderr)
    if run.returncode!=0:raise RuntimeError('Historical replay failed; see stderr.txt.')
    observed=json.loads(output.read_text())
    if observed!=expected:raise AssertionError('Historical semantic JSON changed.')
    record={'status':'PASS','parsed_json_identical':True,'source_sha256':hashlib.sha256(original.encode()).hexdigest(),
            'patch_scope':'One output filename literal replaced. Mathematical code unchanged.'}
    (args.out/'comparison.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
