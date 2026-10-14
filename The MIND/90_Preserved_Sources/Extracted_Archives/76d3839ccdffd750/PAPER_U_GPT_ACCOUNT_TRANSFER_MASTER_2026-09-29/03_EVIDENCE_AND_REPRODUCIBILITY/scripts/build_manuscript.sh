#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
name=Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.2
command -v pdflatex >/dev/null 2>&1 || { echo "pdfLaTeX is required" >&2; exit 1; }
command -v biber >/dev/null 2>&1 || { echo "Biber is required" >&2; exit 1; }
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
biber "$name"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
echo "Built $name.pdf"
