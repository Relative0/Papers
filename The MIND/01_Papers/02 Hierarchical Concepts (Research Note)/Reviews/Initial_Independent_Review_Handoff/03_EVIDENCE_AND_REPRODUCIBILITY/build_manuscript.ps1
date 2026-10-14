param([string]$OutputDirectory = (Join-Path $PSScriptRoot 'build'))
$ErrorActionPreference='Stop'
$manuscript=Join-Path (Split-Path $PSScriptRoot -Parent) '01_CURRENT_MANUSCRIPT'
$name='Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3'
$build=New-Item -ItemType Directory -Path $OutputDirectory -Force
Copy-Item -LiteralPath (Join-Path $manuscript "$name.tex") -Destination $build.FullName
Copy-Item -LiteralPath (Join-Path $manuscript 'paper_u_refs_v0.3.bib') -Destination $build.FullName
Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'latex_support') -File | Where-Object { $_.Extension -in '.sty','.def' } | Copy-Item -Destination $build.FullName
Push-Location $build.FullName
try {
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$name.tex" *> 'pdflatex_pass1.txt'
    if($LASTEXITCODE -ne 0){ throw 'First pdfLaTeX pass failed; see pdflatex_pass1.txt' }
    & biber $name *> 'biber_output.txt'
    if($LASTEXITCODE -ne 0){ throw 'Biber failed; see biber_output.txt' }
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$name.tex" *> 'pdflatex_pass2.txt'
    if($LASTEXITCODE -ne 0){ throw 'Second pdfLaTeX pass failed; see pdflatex_pass2.txt' }
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$name.tex" *> 'pdflatex_pass3.txt'
    if($LASTEXITCODE -ne 0){ throw 'Third pdfLaTeX pass failed; see pdflatex_pass3.txt' }
    Copy-Item -LiteralPath "$name.pdf" -Destination $manuscript
    Copy-Item -LiteralPath "$name.bbl" -Destination $manuscript
    Write-Output "Built $name.pdf"
} finally { Pop-Location }
