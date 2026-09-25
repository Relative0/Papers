[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $Destination
)

$ErrorActionPreference = 'Stop'
$sourceRoot = $PSScriptRoot
$finalPdf = Join-Path (Split-Path $sourceRoot -Parent) 'CM_LM_Technical_Companion_20260920.pdf'
$destinationRoot = [System.IO.Path]::GetFullPath($Destination)

if (Test-Path -LiteralPath $destinationRoot) {
    throw "Destination already exists; refusing to overwrite: $destinationRoot"
}

$files = @(
    @{ Source = $finalPdf; Relative = 'CM_LM_Technical_Companion_20260920.pdf' },
    @{ Source = (Join-Path $sourceRoot 'main.tex'); Relative = 'main.tex' },
    @{ Source = (Join-Path $sourceRoot 'references.bib'); Relative = 'references.bib' },
    @{ Source = (Join-Path $sourceRoot 'BUILD_AND_VALIDATION.md'); Relative = 'BUILD_AND_VALIDATION.md' },
    @{ Source = (Join-Path $sourceRoot 'MANIFEST_SHA256.txt'); Relative = 'MANIFEST_SHA256.txt' },
    @{ Source = (Join-Path $sourceRoot 'copy_companion.ps1'); Relative = 'copy_companion.ps1' },
    @{ Source = (Join-Path $sourceRoot 'build\main.log'); Relative = 'build\main.log' },
    @{ Source = (Join-Path $sourceRoot 'build\main.bbl'); Relative = 'build\main.bbl' }
)

foreach ($file in $files) {
    if (-not (Test-Path -LiteralPath $file.Source -PathType Leaf)) {
        throw "Required source file is missing: $($file.Source)"
    }
}

New-Item -ItemType Directory -Path $destinationRoot | Out-Null
New-Item -ItemType Directory -Path (Join-Path $destinationRoot 'build') | Out-Null

foreach ($file in $files) {
    $target = Join-Path $destinationRoot $file.Relative
    Copy-Item -LiteralPath $file.Source -Destination $target
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.Source).Hash
    $targetHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash
    if ($sourceHash -ne $targetHash) {
        throw "Hash mismatch after copy: $($file.Relative)"
    }
}

$copied = Get-ChildItem -LiteralPath $destinationRoot -File -Recurse
if ($copied.Count -ne $files.Count) {
    throw "Unexpected copied file count: expected $($files.Count), found $($copied.Count)"
}

[pscustomobject]@{
    Destination = $destinationRoot
    FileCount = $copied.Count
    PdfSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $destinationRoot 'CM_LM_Technical_Companion_20260920.pdf')).Hash.ToLowerInvariant()
}
