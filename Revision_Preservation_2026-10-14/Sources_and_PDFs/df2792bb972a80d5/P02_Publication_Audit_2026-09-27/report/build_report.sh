#!/bin/sh
set -eu
cd "$(dirname "$0")"
pandoc P02_Publication_Readiness_Audit.md --standalone --from=markdown+tex_math_dollars+raw_tex --to=latex --include-in-header=header.tex --lua-filter=code_breaks.lua --output=P02_Publication_Readiness_Audit.tex
pdflatex -interaction=nonstopmode -halt-on-error P02_Publication_Readiness_Audit.tex > report_pass1.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error P02_Publication_Readiness_Audit.tex > report_pass2.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error P02_Publication_Readiness_Audit.tex > report_pass3.log 2>&1
