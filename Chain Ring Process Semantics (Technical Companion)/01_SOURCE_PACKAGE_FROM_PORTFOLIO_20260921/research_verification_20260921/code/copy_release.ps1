$ErrorActionPreference = 'Stop'
$source = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$parent = 'C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research'
$destination = [System.IO.Path]::GetFullPath((Join-Path $parent 'Research_Verification_20260921'))
if (-not $destination.StartsWith(([System.IO.Path]::GetFullPath($parent) + '\'), [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Destination escaped requested parent' }
if (Test-Path -LiteralPath $destination) { throw 'Refusing to overwrite an existing research snapshot' }
$inventory = Get-Content -LiteralPath (Join-Path $source 'ARTIFACT_INVENTORY.txt')
foreach ($relative in $inventory) {
    $inputFile = [System.IO.Path]::GetFullPath((Join-Path $source $relative))
    if (-not $inputFile.StartsWith(($source + '\'), [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid source inventory path' }
    if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf)) { throw "Missing release file: $relative" }
}
New-Item -ItemType Directory -Path $destination | Out-Null
foreach ($relative in $inventory) {
    $inputFile = Join-Path $source $relative
    $outputFile = Join-Path $destination $relative
    $outputParent = Split-Path -Parent $outputFile
    if (-not (Test-Path -LiteralPath $outputParent)) { New-Item -ItemType Directory -Path $outputParent -Force | Out-Null }
    Copy-Item -LiteralPath $inputFile -Destination $outputFile
    if ((Get-FileHash -LiteralPath $inputFile -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $outputFile -Algorithm SHA256).Hash) { throw "Hash mismatch: $relative" }
}
[pscustomobject]@{ status='PASS'; destination=$destination; copied_files=$inventory.Count; every_file_hash_verified=$true } | ConvertTo-Json
