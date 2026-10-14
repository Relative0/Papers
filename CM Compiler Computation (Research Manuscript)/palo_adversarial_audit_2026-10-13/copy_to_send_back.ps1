$ErrorActionPreference = 'Stop'
$copySource = [System.IO.Path]::GetFullPath('C:\Users\brian\Documents\CM_Computation\output\research\palo_adversarial_audit_2026-10-13')
$copyTarget = [System.IO.Path]::GetFullPath('C:\Users\brian\Downloads\B_papers\B_papers\Send Back')
$packageTarget = [System.IO.Path]::GetFullPath((Join-Path $copyTarget 'palo_adversarial_audit_2026-10-13'))
$compilerSource = 'C:\Users\brian\Documents\Math Latex etc\Papers for Publication\CM Compiler Computation (Research Manuscript)\Current_Compiler_Study\02_CONTRACT_REVISION_20260926'
if (-not $packageTarget.StartsWith($copyTarget + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid package destination' }
if (-not (Test-Path -LiteralPath $copySource -PathType Container)) { throw 'Missing audit source folder' }
New-Item -ItemType Directory -Path $copyTarget -Force | Out-Null
New-Item -ItemType Directory -Path $packageTarget -Force | Out-Null
$records = [System.Collections.Generic.List[object]]::new()
function Copy-VerifiedArtifact([string]$sourceFile, [string]$destinationFile) {
    $resolvedDest = [System.IO.Path]::GetFullPath($destinationFile)
    if (-not $resolvedDest.StartsWith($copyTarget + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Copy outside requested destination' }
    $sourceHash = (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash
    if (Test-Path -LiteralPath $resolvedDest) {
        if ((Get-FileHash -LiteralPath $resolvedDest -Algorithm SHA256).Hash -ne $sourceHash) { throw "Existing different file preserved: $resolvedDest" }
    } else {
        New-Item -ItemType Directory -Path ([System.IO.Path]::GetDirectoryName($resolvedDest)) -Force | Out-Null
        Copy-Item -LiteralPath $sourceFile -Destination $resolvedDest -ErrorAction Stop
    }
    if ((Get-FileHash -LiteralPath $resolvedDest -Algorithm SHA256).Hash -ne $sourceHash) { throw "Copy hash mismatch: $resolvedDest" }
    if ((Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash -ne $sourceHash) { throw "Source changed during copying: $sourceFile" }
    $records.Add([PSCustomObject]@{ source=$sourceFile; destination=$resolvedDest; sha256=$sourceHash.ToLowerInvariant() })
}
foreach ($file in Get-ChildItem -LiteralPath $copySource -Recurse -File) {
    $relative = $file.FullName.Substring($copySource.Length + 1)
    Copy-VerifiedArtifact $file.FullName (Join-Path $packageTarget $relative)
}
Copy-VerifiedArtifact (Join-Path $copySource 'palo_adversarial_audit_2026-10-13.pdf') (Join-Path $copyTarget 'palo_adversarial_audit_2026-10-13.pdf')
$compilerManifest = Get-Content -LiteralPath (Join-Path $compilerSource 'MANIFEST_SHA256.json') -Raw | ConvertFrom-Json
foreach ($pair in @(
    @('Operator_Level_CM_Compiler_Revised_Draft.pdf','Operator_Level_CM_Compiler_Updated_2026-10-13.pdf'),
    @('Operator_Level_CM_Compiler_Revised_Draft.tex','Operator_Level_CM_Compiler_Updated_2026-10-13.tex'),
    @('SEMANTIC_BOUNDARY_ADDITION_2026-10-13.md','CM_Compiler_Semantic_Addition_2026-10-13.md')
)) {
    $sourceFile = Join-Path $compilerSource $pair[0]
    $entry = $compilerManifest.files | Where-Object { $_.path -eq $pair[0] } | Select-Object -First 1
    if ($null -eq $entry -or (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { throw 'Compiler source does not match its recorded build manifest' }
    Copy-VerifiedArtifact $sourceFile (Join-Path $copyTarget $pair[1])
}
$readme = @'
PALO / CM delivery - 13 October 2026

palo_adversarial_audit_2026-10-13.pdf: newly rendered 12-page audit.
palo_adversarial_audit_2026-10-13/: full copy of the audit artifacts, snapshots, claim ledger, errata and reproduction scripts/results.
Operator_Level_CM_Compiler_Updated_2026-10-13.pdf: already compiled 20-page current compiler manuscript, including the October 13 semantic-boundary addition. Its matching TeX and addition note are beside it.
palo_cm_relationships.pdf: the pre-existing 23-page synthesis; kept untouched.

The audit complements the research and does not replace the compiler manuscript or historical evidence. Original files remain in their original folders. The audit describes frozen initial versions; later research/manuscript continuations are outside its full proof coverage.

SHA-256 copy verification is recorded in delivery_manifest_2026-10-13.json. Reproduction commands in the copied audit README refer to the original CM_Computation workspace; this is a delivery copy, not a relocated repository.
'@
$readmeDest = Join-Path $copyTarget 'README_AUDIT_DELIVERY_2026-10-13.txt'
if (Test-Path -LiteralPath $readmeDest) {
    if ((Get-Content -LiteralPath $readmeDest -Raw).TrimEnd() -ne $readme.TrimEnd()) { throw 'Different existing delivery README preserved' }
} else { [System.IO.File]::WriteAllText($readmeDest, $readme, [System.Text.UTF8Encoding]::new($false)) }
$manifestDest = Join-Path $copyTarget 'delivery_manifest_2026-10-13.json'
if (Test-Path -LiteralPath $manifestDest) { throw 'Existing delivery manifest preserved; inspect before updating' }
$payload = [PSCustomObject]@{ copied_utc=[DateTime]::UtcNow.ToString('o'); mode='copy; originals retained'; verification='all copied files SHA-256 matched'; files=$records }
[System.IO.File]::WriteAllText($manifestDest, ($payload | ConvertTo-Json -Depth 5), [System.Text.UTF8Encoding]::new($false))
$payload | ConvertTo-Json -Depth 1
