$ErrorActionPreference = 'Stop'

$reportPath = Join-Path $PSScriptRoot '..\optical-cpo-npo-guide.html'
if (-not (Test-Path -LiteralPath $reportPath)) {
    throw 'Expected optical-cpo-npo-guide.html to exist.'
}

$html = Get-Content -Raw -Encoding UTF8 -LiteralPath $reportPath

if ($html -notmatch '<html lang="zh-Hant">') { throw 'Expected Traditional Chinese document language.' }
if (([regex]::Matches($html, '<h1(?:\s|>)')).Count -ne 1) { throw 'Expected exactly one H1.' }
if ($html -notmatch 'Noto Sans TC') { throw 'Expected a Traditional Chinese-first type stack.' }
if ($html -match 'radial-gradient|conic-gradient|linear-gradient') { throw 'Decorative gradients are not allowed.' }
if ($html -match '<script[^>]+src=|<link[^>]+stylesheet') { throw 'Report must be self-contained.' }

foreach ($diagram in @('placement-matrix', 'architecture-cross-sections', 'value-transfer')) {
    if ($html -notmatch ('data-diagram="' + [regex]::Escape($diagram) + '"')) {
        throw "Missing diagram: $diagram"
    }
}

foreach ($architecture in @('Pluggable', 'LPO', 'OBO', 'NPO', 'CPO')) {
    if ($html -notmatch [regex]::Escape($architecture)) { throw "Missing architecture: $architecture" }
}

$glossaryCount = ([regex]::Matches($html, 'data-glossary-term=')).Count
if ($glossaryCount -lt 35 -or $glossaryCount -gt 45) {
    throw "Expected 35-45 glossary entries, found $glossaryCount."
}

foreach ($modelMarker in @('data-model="LITE"', 'data-model="TSEM"', 'data-scenario="bear"', 'data-scenario="base"', 'data-scenario="bull"', 'reset-models')) {
    if ($html -notmatch [regex]::Escape($modelMarker)) { throw "Missing model marker: $modelMarker" }
}

function Read-EmbeddedJson([string] $id) {
    $pattern = '<script type="application/json" id="' + [regex]::Escape($id) + '">([\s\S]*?)</script>'
    $match = [regex]::Match($html, $pattern)
    if (-not $match.Success) { throw "Missing embedded JSON: $id" }
    return ($match.Groups[1].Value | ConvertFrom-Json)
}

$sources = @(Read-EmbeddedJson 'sources-data')
$claims = @(Read-EmbeddedJson 'claims-data')
$glossary = @(Read-EmbeddedJson 'glossary-data')
$snapshot = Read-EmbeddedJson 'research-snapshot'

if ($sources.Count -lt 12) { throw 'Expected at least 12 sources.' }
if ($claims.Count -lt 20) { throw 'Expected at least 20 material claims.' }
if ($glossary.Count -ne $glossaryCount) { throw 'Rendered glossary and glossary JSON counts differ.' }
if (-not $snapshot.LITE -or -not $snapshot.TSEM) { throw 'Research snapshot must contain LITE and TSEM.' }
if ($html -notmatch 'data-model-formula="eps-pe-ev-ebitda-v1"') { throw 'Expected a versioned valuation formula marker.' }
if ($html -notmatch 'function renderGlossarySources') { throw 'Expected visible glossary source links to be rendered.' }

foreach ($periodMarker in @('data-model-period="LITE-FY26"', 'data-model-period="LITE-FY27"', 'data-model-period="LITE-FY28"', 'data-model-period="TSEM-CY26"', 'data-model-period="TSEM-CY27"', 'data-model-period="TSEM-CY28"')) {
    if ($html -notmatch [regex]::Escape($periodMarker)) { throw "Missing three-year model period: $periodMarker" }
}
if (@($snapshot.LITE.forecast).Count -ne 3 -or @($snapshot.TSEM.forecast).Count -ne 3) {
    throw 'Each company must have a three-period forecast bridge.'
}

foreach ($company in @('LITE', 'TSEM')) {
    foreach ($scenarioName in @('bear', 'base', 'bull')) {
        $scenario = $snapshot.$company.scenarios.$scenarioName
        foreach ($field in @('revenue', 'opMargin', 'taxRate', 'shares', 'multiple', 'netCash', 'daMargin', 'fcfMargin')) {
            if ($null -eq $scenario.$field) { throw "$company $scenarioName is missing $field." }
        }
        $netIncome = $scenario.revenue * ($scenario.opMargin / 100) * (1 - $scenario.taxRate / 100)
        $eps = $netIncome * 1000 / $scenario.shares
        $target = $eps * $scenario.multiple
        if ($eps -le 0 -or $target -le 0 -or [double]::IsNaN($target)) {
            throw "$company $scenarioName produces an invalid valuation."
        }
    }
}

$sourceIds = @{}
foreach ($source in $sources) {
    foreach ($field in @('id', 'title', 'url', 'date', 'level', 'confidence')) {
        if (-not $source.$field) { throw "Source is missing required field: $field" }
    }
    $sourceIds[$source.id] = $true
}

foreach ($claim in $claims) {
    if (-not $claim.id -or -not $claim.text -or -not $claim.level -or -not $claim.confidence) {
        throw 'Claim is missing required metadata.'
    }
    if (@($claim.sourceIds).Count -eq 0) { throw "Claim $($claim.id) has no sources." }
    foreach ($sourceId in @($claim.sourceIds)) {
        if (-not $sourceIds.ContainsKey($sourceId)) { throw "Claim $($claim.id) references missing source $sourceId." }
    }
}

foreach ($entry in $glossary) {
    if (@($entry.sourceIds).Count -eq 0) { throw "Glossary entry $($entry.id) has no source." }
    foreach ($sourceId in @($entry.sourceIds)) {
        if (-not $sourceIds.ContainsKey($sourceId)) { throw "Glossary entry $($entry.id) references missing source $sourceId." }
    }
}

Write-Output "Optical CPO/NPO report checks passed: $glossaryCount glossary terms, $($claims.Count) claims, $($sources.Count) sources."
