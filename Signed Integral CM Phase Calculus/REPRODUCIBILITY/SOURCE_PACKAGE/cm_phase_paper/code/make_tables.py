#!/usr/bin/env python3
"""Generate the printed finite interference tables from verified JSON data."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/interference_tables.json').read_text())['tables']
out=[r'\section{The four complete Boolean interference tables}\label{app:tables}',
 r'The entry in row $A$, column $B$ of table $k$ is the integer encoding of $A\oplus\rot^kB$. Encodings are defined below. These are binary support-interference tables, not tables of complex amplitude addition.',
 r'\begin{center}\small\begin{tabular}{@{}rll@{}}\toprule Code & Cyclic polynomial & CM label\\\midrule']
labels=[r'0',r'[\land]',r'[\Uparrow]',r'[L]',r'[\neg\lor]',r'[\Leftrightarrow]',r'[\neg R]',r'[\Leftarrow]',r'[\Downarrow]',r'[R]',r'[\mathrm{XOR}]',r'[\lor]',r'[\neg L]',r'[\Rightarrow]',r'[\neg\land]',r'\ones']
for a in range(16):
    terms=[('1' if j==0 else 'g' if j==1 else 'g^'+str(j)) for j in range(4) if a>>j&1]
    poly=r'\oplus '.join(terms) or '0'
    out.append(f'{a} & ${poly}$ & ${labels[a]}$'+r'\\')
out+=[r'\bottomrule\end{tabular}\end{center}',r'Clockwise coordinate order is $(a_0,a_1,a_2,a_3)$ around the square, with the displayed array $\begin{pmatrix}a_0&a_1\\a_3&a_2\end{pmatrix}$. The names are only labels for the arrays; all computation uses the encoded coefficients.']
for k in range(4):
    if k%2==0: out.append(r'\clearpage')
    out += [r'\begin{table}[!htbp]\centering\small',r'\setlength{\tabcolsep}{5.0pt}\renewcommand{\arraystretch}{1.10}',r'\begin{tabular}{r|rrrrrrrrrrrrrrrr}\toprule',
            r'$A\backslash B$ & '+' & '.join(map(str,range(16)))+r'\\\midrule']
    for a,row in enumerate(data[str(k)]):out.append(str(a)+' & '+' & '.join(map(str,row))+r'\\')
    out += [r'\bottomrule\end{tabular}',f'\\caption{{Complete table for $k={k}$: $A\\oplus\\rot^{k}B$.}}',r'\end{table}']
(root/'sections/08_tables.tex').write_text('\n'.join(out)+'\n')
