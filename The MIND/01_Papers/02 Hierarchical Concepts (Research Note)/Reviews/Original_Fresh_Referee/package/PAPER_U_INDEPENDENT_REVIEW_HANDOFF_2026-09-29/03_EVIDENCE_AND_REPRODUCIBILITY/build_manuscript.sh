#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
src="$here/../01_CURRENT_MANUSCRIPT"
build="${1:-$here/build}"
name=Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3
mkdir -p "$build"
cp "$src/$name.tex" "$src/paper_u_refs_v0.3.bib" "$build/"
cp "$here/latex_support/"*.sty "$here/latex_support/"*.def "$build/"
cd "$build"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" > pdflatex_pass1.txt
biber "$name" > biber_output.txt
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" > pdflatex_pass2.txt
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" > pdflatex_pass3.txt
cp "$name.pdf" "$name.bbl" "$src/"
printf 'Built %s.pdf\n' "$name"
