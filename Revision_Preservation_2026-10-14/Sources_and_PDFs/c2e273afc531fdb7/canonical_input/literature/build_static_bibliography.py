"""Build a deterministic no-BibTeX bibliography from REFERENCE_RECORDS.json.
The .bib file remains the normal journal-tooling source; this fallback permits
pdflatex-only builds in environments without a BibTeX executable.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def tex(s):
    chars={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}
    return ''.join(chars.get(c,c) for c in s)

records=json.loads((ROOT/'REFERENCE_RECORDS.json').read_text())
lines=['% Generated from REFERENCE_RECORDS.json; do not hand-edit.',r'\begin{thebibliography}{99}']
for r in records:
    lines += [r'\bibitem{'+r['key']+'}',tex(r['authors'])+'.',r'\emph{'+tex(r['title'])+'}. '+r['year']+'.']
    if r['url']:lines.append(r'\url{'+r['url']+'}.')
    if r['key']=='PaperB':lines.append('Unpublished manuscript supplied with this consolidation.')
lines.append(r'\end{thebibliography}')
(ROOT/'references_static.tex').write_text('\n'.join(lines)+'\n')
print('Static bibliography:',len(records),'records')
