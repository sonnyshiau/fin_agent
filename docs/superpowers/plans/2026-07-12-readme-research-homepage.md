# FIN_AGENT README Research Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the plain README opening with a branded GitHub-native research homepage.

**Architecture:** Use one repository-owned static SVG as the signature visual. Keep the README standard Markdown plus one compact HTML table for featured reports, with no third-party rendering dependency.

**Tech Stack:** GitHub Flavored Markdown, static SVG, PowerShell, Python XML parsing, GitHub Pages.

---

## File Map

- Create `docs/assets/fin-agent-readme-hero.svg`: accessible brand banner.
- Modify `README.md`: research positioning, topic map, featured work, methodology, page index, and evidence discipline.
- Do not modify application source or the approved design spec.

### Task 1: Confirm the starting state

**Files:**
- Inspect: `README.md`
- Inspect: `docs/superpowers/specs/2026-07-12-readme-research-homepage-design.md`

- [ ] **Step 1: Verify the new homepage structure is absent**

Run:

```powershell
$text = Get-Content -Raw -Encoding utf8 README.md
foreach ($token in @('docs/assets/fin-agent-readme-hero.svg','## Featured Research','## Evidence Discipline')) {
  if ($text.Contains($token)) { throw "Unexpected token: $token" }
}
'Precondition confirmed'
```

Expected: `Precondition confirmed`.

- [ ] **Step 2: Record the existing links that must survive**

Run:

```powershell
Select-String README.md -Pattern 'https://[^)]+' -AllMatches |
  ForEach-Object { $_.Matches.Value }
```

Expected: the five existing URLs for 800VDC, CoWoS, Vera Rubin, Bloom Energy, and Retirement Calculator.

### Task 2: Create the brand banner

**Files:**
- Create: `docs/assets/fin-agent-readme-hero.svg`

- [ ] **Step 1: Create the SVG**

Create a `1200 × 360` SVG with this accessible shell:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
  <title id="title">FIN_AGENT AI Infrastructure Investment Research</title>
  <desc id="desc">Research from architecture and supply chains through earnings and valuation.</desc>
  <rect width="1200" height="360" rx="24" fill="#15362c"/>
  <g fill="none" stroke="#31584a" stroke-width="1" opacity="0.7">
    <path d="M760 0V360M840 0V360M920 0V360M1000 0V360M1080 0V360"/>
    <path d="M700 60H1200M700 120H1200M700 180H1200M700 240H1200M700 300H1200"/>
  </g>
  <g fill="none" stroke="#6aa58c" stroke-width="2" opacity="0.8">
    <rect x="862" y="72" width="212" height="220" rx="8"/>
    <path d="M884 104H1052M884 140H1052M884 176H1052M884 212H1052M884 248H1052"/>
    <path d="M742 180H830L850 160H884M1074 180H1140"/>
    <circle cx="742" cy="180" r="5" fill="#9ed1b8"/>
    <circle cx="1140" cy="180" r="5" fill="#9ed1b8"/>
  </g>
  <text x="72" y="76" fill="#9ed1b8" font-family="Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="4">FIN_AGENT</text>
  <text x="72" y="148" fill="#ffffff" font-family="Arial, sans-serif" font-size="44" font-weight="700">AI Infrastructure</text>
  <text x="72" y="198" fill="#ffffff" font-family="Arial, sans-serif" font-size="44" font-weight="700">Investment Research</text>
  <text x="72" y="244" fill="#c7ddd3" font-family="Arial, sans-serif" font-size="18">Architecture  →  Supply Chain  →  Earnings  →  Valuation</text>
  <g fill="#24483a" stroke="#4d7465">
    <rect x="72" y="278" width="104" height="34" rx="17"/><rect x="186" y="278" width="114" height="34" rx="17"/><rect x="310" y="278" width="120" height="34" rx="17"/><rect x="440" y="278" width="90" height="34" rx="17"/><rect x="540" y="278" width="92" height="34" rx="17"/>
  </g>
  <g fill="#d9ebe3" font-family="Arial, sans-serif" font-size="13" text-anchor="middle">
    <text x="124" y="300">Compute</text><text x="243" y="300">Packaging</text><text x="370" y="300">Networking</text><text x="485" y="300">Power</text><text x="586" y="300">Cooling</text>
  </g>
</svg>
```

Use only SVG primitives and system fonts. Required visible strings: `FIN_AGENT`, `AI Infrastructure Investment Research`, `Architecture`, `Supply Chain`, `Earnings`, `Valuation`, `Compute`, `Packaging`, `Networking`, `Power`, and `Cooling`. Do not use scripts, images, filters, gradients, external URLs, or animation.

- [ ] **Step 2: Validate the SVG**

Run:

```powershell
@'
from pathlib import Path
from xml.etree import ElementTree as ET
p=Path('docs/assets/fin-agent-readme-hero.svg')
root=ET.parse(p).getroot()
text=p.read_text(encoding='utf-8')
assert root.attrib['viewBox']=='0 0 1200 360'
for bad in ['<script','<image','http://','https://','<filter','Gradient','<animate']:
    assert bad not in text, bad
for value in ['FIN_AGENT','AI Infrastructure Investment Research','Architecture','Supply Chain','Earnings','Valuation']:
    assert value in text, value
print('SVG validation passed')
'@ | python -
```

Expected: `SVG validation passed`.

- [ ] **Step 3: Commit the banner**

```powershell
git add docs/assets/fin-agent-readme-hero.svg
git commit -m "Add FIN_AGENT README brand banner"
```

### Task 3: Rebuild the README hierarchy

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Write the approved section structure**

Use this exact order:

```markdown
# fin_agent
![FIN_AGENT — AI Infrastructure Investment Research](docs/assets/fin-agent-readme-hero.svg)
> 從技術架構與產品週期出發，追蹤 AI 基礎設施的供應鏈瓶頸、價值量轉移與基本面傳導，最後連接到 EPS、估值與投資策略。
`Compute` · `Advanced Packaging` · `Networking & Optics` · `Power & Cooling` · `AI Factory Infrastructure`
## Featured Research
## Research Framework
## Published Research
## Evidence Discipline
```

Under `Featured Research`, use a three-column HTML table with `width="33%"` cells for 800VDC × Kyber, Vera Rubin Rack Map, and CoWoS 2027. Each cell contains a linked title and one sentence. Under `Research Framework`, show Architecture → Product Cycle → Supply Chain → Fundamentals → Valuation as a numbered sequence. Under `Published Research`, retain all five existing links. Under `Evidence Discipline`, show Official → Company Guidance → Broker Estimate → Channel Check → Market Rumor → Independent Inference.

- [ ] **Step 2: Validate structure and URLs**

Run:

```powershell
@'
from pathlib import Path
import re
text=Path('README.md').read_text(encoding='utf-8')
for heading in ['## Featured Research','## Research Framework','## Published Research','## Evidence Discipline']:
    assert heading in text, heading
for url in [
'https://sonnyshiau.github.io/fin_agent/800vdc-kyber-power-industry.html',
'https://sonnyshiau.github.io/fin_agent/ai-supply-chain-cowos.html',
'https://sonnyshiau.github.io/fin_agent/vera-rubin-rack-map.html',
'https://sonnyshiau.github.io/fin_agent/be-interview/',
'https://sonnyshiau.github.io/retirement-calculator/']:
    assert url in text, url
assert 'docs/assets/fin-agent-readme-hero.svg' in text
assert not re.search(r'img\.shields\.io|<style|<script',text)
print('README validation passed')
'@ | python -
git diff --check -- README.md docs/assets/fin-agent-readme-hero.svg
```

Expected: `README validation passed` and no diff errors.

- [ ] **Step 3: Commit the README**

```powershell
git add README.md
git commit -m "Redesign README as research homepage"
```

### Task 4: Visual and repository verification

**Files:**
- Verify: `README.md`
- Verify: `docs/assets/fin-agent-readme-hero.svg`

- [ ] **Step 1: Render the SVG at desktop and mobile widths**

Use Playwright to open the local SVG, capture a `1200 × 360` screenshot and a `390px` viewport screenshot, and inspect for clipped text, weak contrast, overflow, broken glyphs, and excessive decoration.

- [ ] **Step 2: Run repository tests**

Run:

```powershell
python -m pytest
```

Expected: all tests pass with zero failures.

- [ ] **Step 3: Verify final scope**

Run:

```powershell
git diff main...HEAD --stat
git diff main...HEAD -- README.md docs/assets/fin-agent-readme-hero.svg
```

Expected: implementation changes are limited to README, the SVG, and the approved design/plan documents.

- [ ] **Step 4: Integrate, push, and verify GitHub rendering**

After integration into `main`, push `origin/main`. Open `https://github.com/sonnyshiau/fin_agent` and verify the banner, featured links, research workflow, page index, and evidence discipline. Require HTTP 200 from every published research link.
