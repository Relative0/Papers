#!/usr/bin/env python3
"""Expand the modular paper into a self-contained LaTeX source."""
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'paper.tex').read_text()
def replace(match):return (root/(match.group(1)+'.tex')).read_text()
s=re.sub(r'\\input\{([^}]+)\}',replace,s)
preamble='% Self-contained source. Compile with latexmk -pdf (uses Biber).\n'
preamble+='\\begin{filecontents*}{references.bib}\n'+(root/'references.bib').read_text()+'\\end{filecontents*}\n'
(root/'standalone.tex').write_text(preamble+s)
