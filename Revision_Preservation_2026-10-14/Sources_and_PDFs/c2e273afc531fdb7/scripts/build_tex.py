"""Compile only an existing task-local TeX manuscript; retain every command and log."""
import hashlib
import json
import subprocess
import sys
import time
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
target = Path(sys.argv[1]).resolve()
if not target.is_relative_to(ROOT) or target.suffix != ".tex" or not target.is_file():
    raise SystemExit("Expected an existing TeX source within this portfolio directory")
commands = [
    ["pdflatex", "--disable-installer", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", target.name],
    ["bibtex", target.stem],
    ["pdflatex", "--disable-installer", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", target.name],
    ["pdflatex", "--disable-installer", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", target.name],
]
history = target.parent / 'build_history' / str(time.time_ns())
history.mkdir(parents=True)
for previous in [target.parent/'BUILD_MANIFEST.json', *target.parent.glob('build_stage_*.txt')]:
    if previous.is_file():
        shutil.copy2(previous, history/('previous_'+previous.name))
before = hashlib.sha256(target.read_bytes()).hexdigest()
records = []
for index, command in enumerate(commands):
    started = time.monotonic()
    run = subprocess.run(command, cwd=target.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    (target.parent / f"build_stage_{index+1}.txt").write_bytes(run.stdout)
    records.append({"command": command, "returncode": run.returncode, "seconds": time.monotonic()-started})
    if run.returncode:
        print(run.stdout.decode(errors="replace")[-3000:])
        break
log = (target.parent / (target.stem + ".log")).read_text(errors="replace")
if len(records)==4 and all(r['returncode']==0 for r in records):
    for extra in range(2):
        if 'Label(s) may have changed' not in log and 'Rerun to get cross-references right' not in log:break
        started=time.monotonic();run=subprocess.run(commands[-1],cwd=target.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (target.parent/f'build_stage_{len(records)+1}.txt').write_bytes(run.stdout)
        records.append({'command':commands[-1],'returncode':run.returncode,'seconds':time.monotonic()-started,'reason':'Resolve cross-reference convergence'})
        log=(target.parent/(target.stem+'.log')).read_text(errors='replace')
        if run.returncode:break
findings = [line for line in log.splitlines() if any(s in line for s in (
    "undefined", "Overfull", "Underfull", "Rerun", "LaTeX Warning", "Package natbib Warning"))]
result = {"source": str(target), "source_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
          "stages": records, "findings": findings, "source_unchanged": before == hashlib.sha256(target.read_bytes()).hexdigest(),
          "history": str(history)}
pdf = target.with_suffix(".pdf")
if pdf.is_file():
    result["pdf_sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()
(target.parent / "BUILD_MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
shutil.copy2(target.parent/'BUILD_MANIFEST.json', history/'BUILD_MANIFEST.json')
print(json.dumps(result, indent=2))
raise SystemExit(0 if len(records) >= 4 and all(r["returncode"] == 0 for r in records) and 'Label(s) may have changed' not in log else 1)
