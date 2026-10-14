"""Build manuscript PDFs in a separate directory without overwriting frozen releases."""
from pathlib import Path
import argparse,shutil,subprocess

def main(out):
    root=Path(__file__).resolve().parent
    exe=shutil.which('pdflatex')
    if not exe:raise SystemExit('pdflatex is required. Editable TeX and precompiled PDFs are included.')
    if out.exists():raise SystemExit('Output directory exists; choose another to preserve prior builds.')
    out.mkdir(parents=True)
    for v in ('v1','v2','v3'):
        dest=out/v;dest.mkdir()
        for p in (root/'manuscripts'/v).iterdir():
            if p.suffix in ('.tex','.bib'):shutil.copy2(p,dest/p.name)
        with (dest/'build.log').open('w') as log:
            for _ in range(2):
                subprocess.run([exe,'-interaction=nonstopmode','-halt-on-error',f'paper_{v}.tex'],cwd=dest,stdout=log,stderr=subprocess.STDOUT,check=True)
        print(dest/f'paper_{v}.pdf')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('rebuilt_manuscripts'))
    main(p.parse_args().output.resolve())
