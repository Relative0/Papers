$ErrorActionPreference = 'Stop'
$buildDirectory = Join-Path (Split-Path $PSScriptRoot -Parent) 'manuscript'
$documentName = 'Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.3'
Push-Location $buildDirectory
try {
    & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$documentName.tex" *> 'build-pass1.txt'
    if ($LASTEXITCODE -ne 0) { throw 'First LaTeX pass failed.' }
    & biber $documentName *> 'biber-output.txt'
    if ($LASTEXITCODE -ne 0) { throw 'Biber failed.' }
    foreach ($pass in 2,3) {
        & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error "$documentName.tex" *> "build-pass$pass.txt"
        if ($LASTEXITCODE -ne 0) { throw "LaTeX pass $pass failed." }
    }
} finally { Pop-Location }
