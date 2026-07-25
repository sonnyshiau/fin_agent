$ErrorActionPreference = 'Stop'

$dashboardPath = Join-Path $PSScriptRoot '..\crusoe-ai-factory-dashboard.html'
if (-not (Test-Path $dashboardPath)) {
  throw 'Crusoe dashboard HTML is missing.'
}

$html = Get-Content -Raw -Encoding UTF8 $dashboardPath

function ConvertFrom-CodePoints {
  param([int[]]$CodePoints)
  return -join ($CodePoints | ForEach-Object { [char]$_ })
}

$requiredPatterns = @(
  '<html lang="zh-Hant">',
  '<meta name="viewport"',
  'Crusoe',
  'Energy-to-Intelligence',
  (ConvertFrom-CodePoints @(0x80FD, 0x6E90)),
  ('AI ' + (ConvertFrom-CodePoints @(0x8CC7, 0x6599, 0x4E2D, 0x5FC3))),
  'GPU / HBM / Network',
  'Crusoe Cloud',
  ((ConvertFrom-CodePoints @(0x6709, 0x6548)) + ' Token'),
  (ConvertFrom-CodePoints @(0x5546, 0x696D, 0x6A21, 0x5F0F)),
  (ConvertFrom-CodePoints @(0x8B77, 0x57CE, 0x6CB3)),
  (ConvertFrom-CodePoints @(0x98A8, 0x96AA)),
  (ConvertFrom-CodePoints @(0x8CC7, 0x6599, 0x7F3A, 0x53E3)),
  'data-layer="energy"',
  'data-layer="facility"',
  'data-layer="compute"',
  'data-layer="cloud"',
  'data-layer="output"',
  'aria-label="Energy-to-Intelligence',
  'prefers-reduced-motion'
)

foreach ($pattern in $requiredPatterns) {
  if ($html -notmatch [regex]::Escape($pattern)) {
    throw "Expected dashboard content: $pattern"
  }
}

if ($html -match '<script[^>]+src=') {
  throw 'Dashboard must not load external JavaScript.'
}
if ($html -match '<link[^>]+href="https?://') {
  throw 'Dashboard must not load external stylesheets or fonts.'
}
if ($html -match '<img[^>]+src="https?://') {
  throw 'Dashboard must not load external images.'
}
if ($html -match 'radial-gradient|conic-gradient') {
  throw 'Decorative glow gradients are prohibited.'
}

$sectionCount = ([regex]::Matches($html, '<section\b')).Count
if ($sectionCount -lt 6) {
  throw "Expected at least 6 semantic sections; found $sectionCount."
}

Write-Output 'Crusoe dashboard contract checks passed.'
