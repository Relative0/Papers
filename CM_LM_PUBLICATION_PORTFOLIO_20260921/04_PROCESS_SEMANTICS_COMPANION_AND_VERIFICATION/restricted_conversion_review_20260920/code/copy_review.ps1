$ErrorActionPreference = 'Stop'
$reviewSource = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$reviewParent = 'C:\Users\brian\Documents\CM Quantum\CM_LM_RESEARCH_CONSOLIDATION_2026-09-18\CM_LM_RESEARCH_CONSOLIDATION\publication_writer_run_20260918\Process_Semantics_Research'
$reviewTarget = [IO.Path]::GetFullPath((Join-Path $reviewParent 'Restricted_Conversion_Review_20260920'))
if ([IO.Path]::GetDirectoryName($reviewTarget) -ne $reviewParent) { throw 'Unexpected review target.' }
if (-not (Test-Path -LiteralPath $reviewParent -PathType Container)) { throw 'Research parent missing.' }
if (Test-Path -LiteralPath $reviewTarget) { throw 'Target already exists; refusing to overwrite.' }
$reviewManifest = Join-Path $reviewSource 'MANIFEST_SHA256.txt'
if (-not (Test-Path -LiteralPath $reviewManifest -PathType Leaf)) { throw 'Finalize review before copying.' }
foreach ($reviewLine in Get-Content -LiteralPath $reviewManifest) {
    $reviewParts = $reviewLine -split '  ',2
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $reviewSource $reviewParts[1])).Hash.ToLowerInvariant() -ne $reviewParts[0]) { throw 'Review source mismatch.' }
}
# The previous delivery remains frozen; verify its original manifest entries.
foreach ($baselineLine in Get-Content -LiteralPath (Join-Path $reviewParent 'MANIFEST_SHA256.txt')) {
    $baselineParts = $baselineLine -split '  ',2
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $reviewParent $baselineParts[1])).Hash.ToLowerInvariant() -ne $baselineParts[0]) { throw 'Existing delivery mismatch.' }
}
$reviewFiles = @(Get-ChildItem -LiteralPath $reviewSource -File -Recurse)
New-Item -ItemType Directory -Path $reviewTarget | Out-Null
foreach ($reviewFile in $reviewFiles) {
    $reviewRelative = $reviewFile.FullName.Substring($reviewSource.Length).TrimStart('\','/')
    $reviewDestination = Join-Path $reviewTarget $reviewRelative
    $reviewDirectory = [IO.Path]::GetDirectoryName($reviewDestination)
    if (-not (Test-Path -LiteralPath $reviewDirectory)) { New-Item -ItemType Directory -Path $reviewDirectory -Force | Out-Null }
    Copy-Item -LiteralPath $reviewFile.FullName -Destination $reviewDestination
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $reviewFile.FullName).Hash -ne (Get-FileHash -Algorithm SHA256 -LiteralPath $reviewDestination).Hash) { throw "Review copy mismatch: $reviewRelative" }
}
if (@(Get-ChildItem -LiteralPath $reviewTarget -File -Recurse).Count -ne $reviewFiles.Count) { throw 'Review inventory mismatch.' }
[pscustomobject]@{status='PASS';source=$reviewSource;target=$reviewTarget;files=$reviewFiles.Count;all_hashes_equal=$true;existing_files_overwritten=$false} | ConvertTo-Json
