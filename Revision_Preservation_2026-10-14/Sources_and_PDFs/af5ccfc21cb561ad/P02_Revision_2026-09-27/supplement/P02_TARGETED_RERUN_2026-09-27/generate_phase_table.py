#!/usr/bin/env python3
"""Generate phase_table.tex from package-local new_phase_fourier.json.
This is a reconstruction created for the 2026-09-27 P02 revision; it is not the missing historical complete_p02.py.
"""
from pathlib import Path
import argparse, hashlib, json

p=argparse.ArgumentParser()
p.add_argument('--input', default='capability/data/new_phase_fourier.json')
p.add_argument('--output', default='phase_table.tex')
a=p.parse_args()
source=Path(a.input)
data=json.loads(source.read_text())
rows=data['Walsh_R_squared_ranks']
lines=[r'\begin{table}[ht]\centering',
       r'\begin{tabular}{rrrr}\toprule',
       r'$n$ & $A$ dimension & Binary dimension & Binary rank\\\midrule']
for row in rows:
    lines.append(f"{row['n']} & {row['ring_matrix_dimension']} & {row['binary_matrix_dimension']} & {row['binary_rank']}\\\\")
lines += [r'\bottomrule\end{tabular}',
          r'\caption{Finite checks of the balanced-$A$ analyzer in Proposition~\ref{prop:phase}. Values are generated from the package-local rerun JSON for $n=1,\ldots,6$. This is a rank table, not a probability distribution.}\label{tab:phase}',
          r'\end{table}']
out='\n'.join(lines)+'\n'
Path(a.output).write_text(out)
print(json.dumps({'input':str(source),'output':a.output,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.encode()).hexdigest(),'rows':len(rows)},indent=2))
