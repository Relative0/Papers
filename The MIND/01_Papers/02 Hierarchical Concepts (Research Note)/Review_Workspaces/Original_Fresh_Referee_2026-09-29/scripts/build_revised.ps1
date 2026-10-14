$ErrorActionPreference = 'Stop'
$reviewRoot = Split-Path $PSScriptRoot -Parent
$manuscriptDirectory = Join-Path $reviewRoot 'revised_manuscript'
$manuscriptName = 'Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3'
Push-Location $manuscriptDirectory
try {
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$manuscriptName.tex" *> 'pdflatex_pass1.txt'
    if ($LASTEXITCODE -ne 0) { throw 'First pdfLaTeX pass failed.' }
    & biber $manuscriptName *> 'biber_output.txt'
    if ($LASTEXITCODE -ne 0) { throw 'Biber failed.' }
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$manuscriptName.tex" *> 'pdflatex_pass2.txt'
    if ($LASTEXITCODE -ne 0) { throw 'Second pdfLaTeX pass failed.' }
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$manuscriptName.tex" *> 'pdflatex_pass3.txt'
    if ($LASTEXITCODE -ne 0) { throw 'Final pdfLaTeX pass failed.' }
    Write-Output "Built $manuscriptName.pdf"
} finally {
    Pop-Location
}
