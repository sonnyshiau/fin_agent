# FIN_AGENT README Research Homepage Implementation Plan

> **For agentic workers:** Implement in an isolated worktree and validate each completion claim with fresh evidence.

**Goal:** Finish the GitHub-native FIN_AGENT research homepage with a complete research map, Chinese-first information hierarchy, and a mobile-readable banner.

**Architecture:** Use one repository-owned static SVG as the signature visual. Keep the README in standard Markdown, including an accessible bullet list for featured reports, with no third-party rendering dependency.

**Tech Stack:** GitHub Flavored Markdown, static SVG, PowerShell, Python XML parsing, pytest.

---

## File Map

- Modify `README.md`: add research coverage and Chinese-first headings and workflow labels.
- Modify `docs/assets/fin-agent-readme-hero.svg`: simplify embedded copy for mobile readability while preserving the technical schematic.
- Modify `docs/superpowers/specs/2026-07-12-readme-research-homepage-design.md`: formalize accessibility and content decisions.
- Modify this plan to reflect the completion work and actual verification state.
- Do not modify application source or unrelated research assets.

### Task 1: Confirm the completion baseline

- [x] **Step 1: Confirm the worktree starts on `codex/readme-completion` at live remote baseline `7bad96f`.**
- [x] **Step 2: Confirm README already contains all five public URLs and uses Markdown bullets for the three featured links.**
- [x] **Step 3: Run a focused requirement validator before editing and observe expected failures for Chinese-first headings, Research Coverage, Chinese-first workflow labels, and small SVG text.**

### Task 2: Complete the README information architecture

- [x] **Step 1: Rename major H2 headings to Traditional Chinese first, with English in parentheses.**
- [x] **Step 2: Add `研究版圖（Research Coverage）` and explain the system path from compute through packaging, networking, power/cooling, and AI factory infrastructure.**
- [x] **Step 3: Connect architectural bottlenecks to supply-chain value, fundamentals and EPS, valuation, catalysts, and Thesis Broken conditions.**
- [x] **Step 4: Make workflow labels Chinese first and preserve the five exact public URLs plus the three featured links.**

### Task 3: Improve the mobile banner

- [x] **Step 1: Preserve the `1200 × 360` accessible SVG shell and rack/circuit visual.**
- [x] **Step 2: Remove topic pills and small workflow copy; retain only dominant `FIN_AGENT` and the supporting line `AI INFRA RESEARCH` at source font sizes of at least 48 px.**
- [x] **Step 3: Keep the SVG free of gradients, scripts, images, filters, animation, and external resource-bearing attributes or elements. Allow the standard `xmlns="http://www.w3.org/2000/svg"` declaration.**

### Task 4: Synchronize documentation decisions

- [x] **Step 1: Replace the earlier featured-report HTML table direction with accessible Markdown bullets.**
- [x] **Step 2: Document Chinese-first headings, the new Research Coverage section, and the simplified mobile banner.**
- [x] **Step 3: Correct SVG validation so it permits the standard namespace and checks resource-bearing attributes and unsafe elements instead.**

### Task 5: Verify and commit

#### Commands

**Step 1: Run the focused content and SVG validator.**

```powershell
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
@'
from pathlib import Path
from xml.etree import ElementTree as ET
import re

readme = Path('README.md').read_text(encoding='utf-8')
svg_path = Path('docs/assets/fin-agent-readme-hero.svg')
root = ET.parse(svg_path).getroot()

headings = [
    '## 精選研究（Featured Research）',
    '## 研究版圖（Research Coverage）',
    '## 研究方法（Research Framework）',
    '## 已發布研究（Published Research）',
    '## 證據紀律（Evidence Discipline）',
]
positions = [readme.index(heading) for heading in headings]
assert positions == sorted(positions), positions

coverage = readme.split(headings[1], 1)[1].split('\n## ', 1)[0]
coverage_terms = [
    'AI GPU', 'ASIC', 'CPU', 'HBM', 'CoWoS', 'SoIC', 'CoPoS', 'ABF',
    'CPO', 'NPO', 'LPO', '矽光子', '800VDC', 'BBU', '液冷',
    'rack-scale', '資料中心', '供應鏈價值', 'EPS', '估值', '催化劑',
    'Thesis Broken',
]
for term in coverage_terms:
    assert term in coverage, term

featured = readme.split(headings[0], 1)[1].split('\n## ', 1)[0]
assert '<table' not in readme.lower()
assert len(re.findall(r'^- \*\*\[', featured, re.M)) == 3

expected_urls = {
    'https://sonnyshiau.github.io/fin_agent/800vdc-kyber-power-industry.html',
    'https://sonnyshiau.github.io/fin_agent/ai-supply-chain-cowos.html',
    'https://sonnyshiau.github.io/fin_agent/vera-rubin-rack-map.html',
    'https://sonnyshiau.github.io/fin_agent/be-interview/',
    'https://sonnyshiau.github.io/retirement-calculator/',
}
assert set(re.findall(r'https://[^)\s]+', readme)) == expected_urls

assert root.attrib.get('viewBox') == '0 0 1200 360'
assert root.attrib.get('role') == 'img'
label_ids = set(root.attrib.get('aria-labelledby', '').split())
elements_by_id = {
    element.attrib.get('id'): element.tag.rsplit('}', 1)[-1]
    for element in root.iter() if element.attrib.get('id')
}
assert label_ids
assert {elements_by_id.get(label_id) for label_id in label_ids} == {'title', 'desc'}

unsafe_elements = {
    'script', 'image', 'filter', 'animate', 'animatetransform', 'set',
    'lineargradient', 'radialgradient', 'foreignobject', 'style', 'use',
    'feimage',
}
for element in root.iter():
    tag = element.tag.rsplit('}', 1)[-1].lower()
    assert tag not in unsafe_elements, tag
    for name, value in element.attrib.items():
        local_name = name.rsplit('}', 1)[-1].lower()
        assert local_name not in {'href', 'src'}, (local_name, value)
        assert not re.search(r'(?i)(?:https?:)?//|data:', value), value

visible_text = [
    element for element in root.iter()
    if element.tag.rsplit('}', 1)[-1] == 'text'
]
assert visible_text
assert all(float(element.attrib.get('font-size', '0')) >= 48 for element in visible_text)
visible_copy = ' '.join(''.join(element.itertext()) for element in visible_text)
assert 'FIN_AGENT' in visible_copy
assert 'AI INFRA RESEARCH' in visible_copy

print('Focused validation passed')
'@ | python -X utf8 -
```

**Step 2: Check whitespace and patch formatting.**

```powershell
git diff --check
```

**Step 3: Run the repository test suite.**

```powershell
python -m pytest
```

#### Expected outcomes

- Focused validator prints `Focused validation passed` and exits 0.
- `git diff --check` exits 0 with no whitespace errors; line-ending conversion notices are acceptable.
- `python -m pytest` exits 0 with all 10 tests passing.
- The final diff and staged set contain only the four files listed in the File Map.

#### Observed completion evidence

- Focused validator: `Focused validation passed` (exit 0).
- `git diff --check`: exit 0 with no whitespace errors; only line-ending conversion notices.
- `python -m pytest`: 10 passed in 0.05 seconds.
- Self-review: the diff contains only the four files in the File Map; the repeated Featured Research and full published index remain intentional.
- No screenshot verification was performed or claimed.
