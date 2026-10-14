"""Build the dated draft in temporary space, preserving clean release paths."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
NAME = 'Operator_Level_CM_Compiler_Revised_Draft'
engine = shutil.which('pdflatex')
if not engine:
    raise SystemExit('pdfLaTeX is required (MiKTeX or TeX Live).')
logs = []
with tempfile.TemporaryDirectory(prefix='cm-contract-build-') as temp:
    for pass_number in range(1, 4):
        command = [engine, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
                   '-output-directory=' + temp, str(ROOT / (NAME + '.tex'))]
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors='replace')
        logs.append(f'PASS {pass_number}\n' + run.stdout + run.stderr)
        (ROOT / 'BUILD_LOG.txt').write_text('\n'.join(logs), encoding='utf-8')
        if run.returncode:
            print(logs[-1])
            raise SystemExit(run.returncode)
    shutil.copy2(Path(temp) / (NAME + '.pdf'), ROOT / (NAME + '.pdf'))
    texlog = (Path(temp) / (NAME + '.log')).read_text(errors='replace')
    warnings = [line for line in texlog.splitlines() if any(w in line for w in ('Overfull', 'Underfull', 'Warning', 'undefined'))]
    print('\n'.join(warnings) or 'No LaTeX layout/reference warnings.')
    print('Built', ROOT / (NAME + '.pdf'))
