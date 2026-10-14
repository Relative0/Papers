"""Build the main article and optional note using an installed TeX distribution."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=ROOT / 'validation/build')
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    latex = shutil.which('pdflatex')
    bibtex = shutil.which('bibtex')
    if not latex or not bibtex:
        raise RuntimeError('Install a TeX distribution providing pdflatex and bibtex')
    version = subprocess.run([latex, '--version'], capture_output=True, text=True).stdout
    bib_version = subprocess.run([bibtex, '--version'], capture_output=True, text=True).stdout
    flags = ['-interaction=nonstopmode', '-halt-on-error', '-no-shell-escape']
    if 'MiKTeX' in version:
        flags.append('-disable-installer')
    receipts = []
    for stem, source, inputs, bibliography in [
        ('main', ROOT / 'manuscript', ['main.tex', 'references.bib', 'smith_table.tex'], True),
        ('boolean_interface', ROOT / 'supplement', ['boolean_interface.tex'], False),
    ]:
        work = out / stem
        work.mkdir(exist_ok=True)
        for name in inputs:
            shutil.copyfile(source / name, work / name)
        commands = [[latex, *flags, stem + '.tex']]
        if bibliography:
            commands.append([bibtex, stem])
        commands += [[latex, *flags, stem + '.tex']] * 2
        for i, command in enumerate(commands, 1):
            start = time.monotonic()
            proc = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                  encoding='utf-8', errors='replace')
            (work / f'stage_{i}.txt').write_text(proc.stdout + proc.stderr, encoding='utf-8')
            receipts.append(dict(document=stem, argv=command, cwd=str(work),
                                 exit_code=proc.returncode, seconds=time.monotonic()-start))
            if proc.returncode:
                raise RuntimeError(f'Build failed: {work / ("stage_" + str(i) + ".txt")}')
        log = (work / (stem + '.log')).read_text(encoding='utf-8', errors='replace')
        warnings = [line for line in log.splitlines()
                    if re.search(r'Overfull|Underfull|undefined|LaTeX Warning|Package .*Warning', line)]
        shutil.copyfile(work / (stem + '.pdf'), source / (stem + '.pdf'))
        if bibliography:
            shutil.copyfile(work / 'main.bbl', source / 'main.bbl')
        receipts.append(dict(document=stem, final_warnings=warnings,
                             pdf_sha256=hashlib.sha256((source / (stem + '.pdf')).read_bytes()).hexdigest()))
    result = dict(status='PASS', utc=datetime.now(timezone.utc).isoformat(),
                  python=sys.version, pdflatex_version=version, bibtex_version=bib_version,
                  receipts=receipts)
    (out / 'build_record.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
