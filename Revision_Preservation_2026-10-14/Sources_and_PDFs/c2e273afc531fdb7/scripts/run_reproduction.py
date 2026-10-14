"""Run the supplied runner unchanged, with an outer provenance envelope."""
from pathlib import Path
import hashlib, json, platform, subprocess, sys, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'tmp/cm_canonical/CM_LM_RESEARCH_CONSOLIDATION'
RUN = HERE / 'runs/canonical_01'
def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
command = [sys.executable, str(ROOT/'computation/reproduce.py'), '--all', '--historical', '--workdir', str(RUN), '--timeout', '180']
record = dict(command=command, python=sys.version, platform=platform.platform(),
              inputs=inventory(ROOT), seed_policy='Unchanged seeds in hashed supplied scripts; no timing campaign.',
              purpose='Reproduce finite checks; not mathematical proof or priority evidence.')
record['dependencies'] = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True).splitlines()
t = time.monotonic()
result = subprocess.run(command)
record.update(returncode=result.returncode, seconds=time.monotonic()-t, outputs=inventory(RUN))
(HERE/'evidence/REPRODUCTION_ENVELOPE.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
raise SystemExit(result.returncode)
