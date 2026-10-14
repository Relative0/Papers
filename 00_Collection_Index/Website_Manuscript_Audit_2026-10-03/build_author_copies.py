from pathlib import Path
import json, shutil, subprocess

OUT=Path(__file__).resolve().parent
MIKTEX=Path(r'C:\Users\brian\AppData\Local\Programs\MiKTeX\miktex\bin\x64')
records=[]
for stem in ['observation-refinement-r2-v0.5','hierarchical-concepts-r2-v0.3']:
    folder=OUT/'author_corrected_sources'/stem
    sequence=['pdflatex']*3 if stem.startswith('observation') else ['pdflatex','biber','pdflatex','pdflatex']
    for index,tool in enumerate(sequence,1):
        args=[str(MIKTEX/(tool+'.exe'))]
        args+=['-disable-installer','-interaction=nonstopmode','-halt-on-error','-no-shell-escape',stem+'.tex'] if tool=='pdflatex' else [stem]
        run=subprocess.run(args,cwd=folder,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (folder/f'build_{index}_{tool}.txt').write_bytes(run.stdout)
        records.append(dict(file=stem,step=index,tool=tool,exit_code=run.returncode))
        if run.returncode:
            print(run.stdout.decode('utf-8',errors='replace')[-4000:])
            raise RuntimeError(f'{stem}: {tool} failed')
    log=(folder/(stem+'.log')).read_text(encoding='utf-8',errors='replace')
    warnings=[s for s in log.splitlines() if any(x in s for x in ['Warning','Overfull','Underfull','Output written'])]
    print(json.dumps(dict(file=stem,diagnostics=warnings)))
    shutil.copy2(folder/(stem+'.pdf'),OUT/'prepared_website/public/manuscripts'/(stem+'.pdf'))
(OUT/'build_results.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
