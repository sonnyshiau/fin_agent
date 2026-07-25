# Crusoe Research Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive, self-contained Traditional Chinese HTML research dashboard that explains Crusoe through an Energy-to-Intelligence system map, business analysis, evidence labels, and investment risks.

**Architecture:** Create one standalone semantic HTML document with embedded CSS and progressive-enhancement JavaScript. Add a focused PowerShell contract test for content, accessibility, offline behavior, and prohibited visual patterns, then use a real browser for desktop/mobile rendering and interaction checks.

**Tech Stack:** HTML5, embedded CSS, vanilla JavaScript, PowerShell contract checks, Playwright browser verification.

---

## File Structure

- Create `crusoe-ai-factory-dashboard.html`: the complete offline dashboard, visual system, content, and progressive interactions.
- Create `tests/check_crusoe_dashboard.ps1`: fast structural and content-quality contract checks.
- Modify `docs/superpowers/plans/2026-07-25-crusoe-research-dashboard.md`: mark completed checkboxes during execution.

No existing application or dashboard files will be modified.

### Task 1: Add the dashboard contract test

**Files:**
- Create: `tests/check_crusoe_dashboard.ps1`
- Test: `tests/check_crusoe_dashboard.ps1`

- [ ] **Step 1: Write the failing structural test**

Create `tests/check_crusoe_dashboard.ps1` with:

```powershell
$ErrorActionPreference = 'Stop'

$dashboardPath = Join-Path $PSScriptRoot '..\crusoe-ai-factory-dashboard.html'
if (-not (Test-Path $dashboardPath)) {
  throw 'Crusoe dashboard HTML is missing.'
}

$html = Get-Content -Raw -Encoding UTF8 $dashboardPath

$requiredPatterns = @(
  '<html lang="zh-Hant">',
  '<meta name="viewport"',
  'Crusoe',
  'Energy-to-Intelligence',
  '能源',
  'AI 資料中心',
  'GPU / HBM / Network',
  'Crusoe Cloud',
  '有效 Token',
  '商業模式',
  '護城河',
  '風險',
  '資料缺口',
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
```

- [ ] **Step 2: Run the test and verify the intended failure**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tests\check_crusoe_dashboard.ps1
```

Expected: FAIL with `Crusoe dashboard HTML is missing.`

- [ ] **Step 3: Commit the failing contract**

Run:

```powershell
git add -- tests/check_crusoe_dashboard.ps1
git commit -m "Test Crusoe dashboard contract"
```

Expected: one commit containing only the new test.

### Task 2: Build the semantic dashboard and core visual system

**Files:**
- Create: `crusoe-ai-factory-dashboard.html`
- Test: `tests/check_crusoe_dashboard.ps1`

- [ ] **Step 1: Add the document shell and top-level landmarks**

Create the document with this exact structural skeleton:

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Crusoe AI Factory 研究儀表板：從能源、資料中心與 GPU Cloud 理解其商業模式、護城河與風險。">
  <title>Crusoe｜Energy-to-Intelligence 研究儀表板</title>
  <link rel="icon" href="data:,">
  <style>
    /* Task 2 Step 2 supplies the complete token and layout rules. */
  </style>
</head>
<body>
  <a class="skip-link" href="#main">跳到主要內容</a>
  <header class="masthead" id="overview"></header>
  <main id="main">
    <section id="system-map" data-observe="energy"></section>
    <section id="transformation" data-observe="facility"></section>
    <section id="business-model" data-observe="cloud"></section>
    <section id="moat" data-observe="compute"></section>
    <section id="facts" data-observe="facility"></section>
    <section id="investment-view" data-observe="output"></section>
  </main>
  <aside class="context-rail" aria-label="垂直整合層級"></aside>
  <footer></footer>
  <script>
    /* Task 3 supplies progressive interaction behavior. */
  </script>
</body>
</html>
```

- [ ] **Step 2: Implement the token system and responsive layout**

Define these CSS tokens and base rules; all later selectors must derive from them:

```css
:root {
  color-scheme: dark;
  --canvas: #0b1116;
  --surface: #111a21;
  --surface-raised: #17232b;
  --ink: #e8f0f2;
  --muted: #8fa2aa;
  --line: #293942;
  --energy: #f2a541;
  --compute: #58b7c4;
  --output: #7dcb9d;
  --risk: #e2746b;
  --max: 1440px;
  --rail: 240px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: "Noto Sans TC", "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif;
  line-height: 1.65;
}
.shell {
  width: min(var(--max), calc(100% - 40px));
  margin-inline: auto;
}
.content-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) var(--rail);
  gap: 32px;
  align-items: start;
}
section {
  padding-block: clamp(48px, 7vw, 88px);
  border-top: 1px solid var(--line);
}
:focus-visible {
  outline: 3px solid var(--compute);
  outline-offset: 4px;
}
@media (max-width: 900px) {
  .shell { width: min(100% - 28px, 760px); }
  .content-layout { display: block; }
  .context-rail {
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    overflow-x: auto;
  }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 3: Populate the first viewport and classification**

The masthead must contain:

```html
<div class="shell masthead-grid">
  <div>
    <p class="kicker">AI INFRASTRUCTURE / PRIVATE COMPANY</p>
    <h1>Crusoe 把電力<br>變成可用的 AI 產能</h1>
    <p class="lede">它不是晶片公司，而是把能源、AI 資料中心、GPU 系統與 Cloud 軟體垂直整合的 AI Factory 業者。</p>
  </div>
  <dl class="identity-ledger" aria-label="Crusoe 公司分類">
    <div><dt>公司本質</dt><dd>能源驅動的 AI 基礎設施</dd></div>
    <div><dt>主要產品</dt><dd>資料中心容量＋GPU Cloud</dd></div>
    <div><dt>不是什麼</dt><dd>不是 NVIDIA 的晶片競爭者</dd></div>
    <div><dt>公司狀態</dt><dd>未上市私人公司</dd></div>
  </dl>
</div>
```

- [ ] **Step 4: Build the Energy-to-Intelligence system map**

Use an ordered list so the architecture remains understandable without CSS:

```html
<ol class="pipeline" aria-label="Energy-to-Intelligence 系統路徑">
  <li class="pipeline-node" data-layer="energy">
    <span class="node-index">01</span><strong>能源</strong>
    <small>天然氣、再生能源、儲能與電網資源</small>
    <em>瓶頸：可取得且可快速上線的 MW</em>
  </li>
  <li class="pipeline-node" data-layer="facility">
    <span class="node-index">02</span><strong>AI 資料中心</strong>
    <small>土地、變電、配電、液冷與模組化施工</small>
    <em>瓶頸：許可、工期、功率密度</em>
  </li>
  <li class="pipeline-node" data-layer="compute">
    <span class="node-index">03</span><strong>GPU / HBM / Network</strong>
    <small>NVIDIA／AMD 加速器與高速互連</small>
    <em>瓶頸：供應、網路與記憶體效率</em>
  </li>
  <li class="pipeline-node" data-layer="cloud">
    <span class="node-index">04</span><strong>Crusoe Cloud</strong>
    <small>訓練、Managed Inference 與資源調度</small>
    <em>瓶頸：利用率、軟體與客戶長約</em>
  </li>
  <li class="pipeline-node" data-layer="output">
    <span class="node-index">05</span><strong>有效 Token</strong>
    <small>在延遲與成本目標內完成的 AI 工作</small>
    <em>價值：每瓦電完成更多任務</em>
  </li>
</ol>
```

- [ ] **Step 5: Add the remaining research sections**

Populate semantic headings and concise modules with the following required content:

- Transformation timeline: flare-gas mitigation → Bitcoin mining → Crusoe Cloud → Abilene/Stargate-scale AI factories.
- Business models: AI data-center development versus Crusoe Cloud.
- Moat: power access, construction velocity, vertical integration, financing and customer contracts.
- Competition: position Crusoe between energy/data-center developers and GPU clouds; explicitly state it does not own proprietary accelerator silicon.
- Fact ledger: label entries `公司公告` or `分析推論`.
- Missing-data ledger: revenue, profitability, utilization, customer concentration, project returns, normalized FCF.
- Investment view: upside, downside, what may be underappreciated, what is already priced into the narrative, and the conclusion that Crusoe is closer to an energy-enabled CoreWeave plus data-center developer than to NVIDIA.

Use `<dl>`, `<table>`, `<ol>`, and `<article>` based on content meaning. Do not use decorative icon cards.

- [ ] **Step 6: Run the contract test**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tests\check_crusoe_dashboard.ps1
```

Expected: `Crusoe dashboard contract checks passed.`

- [ ] **Step 7: Commit the semantic dashboard**

Run:

```powershell
git add -- crusoe-ai-factory-dashboard.html
git commit -m "Build Crusoe research dashboard"
```

Expected: one commit containing the standalone dashboard.

### Task 3: Add progressive interaction and browser verification

**Files:**
- Modify: `crusoe-ai-factory-dashboard.html`
- Test: `tests/check_crusoe_dashboard.ps1`

- [ ] **Step 1: Add accessible context-rail navigation**

The rail must contain anchors rather than click-only JavaScript:

```html
<nav class="rail-nav" aria-label="Energy-to-Intelligence 導覽">
  <a href="#system-map" data-layer="energy"><span>能源</span></a>
  <a href="#transformation" data-layer="facility"><span>資料中心</span></a>
  <a href="#moat" data-layer="compute"><span>運算系統</span></a>
  <a href="#business-model" data-layer="cloud"><span>Cloud</span></a>
  <a href="#investment-view" data-layer="output"><span>有效產出</span></a>
</nav>
```

- [ ] **Step 2: Add progressive section and pipeline state**

Use this complete behavior:

```javascript
document.documentElement.classList.add('js');

const railLinks = [...document.querySelectorAll('.rail-nav [data-layer]')];
const observedSections = [...document.querySelectorAll('[data-observe]')];
const pipelineNodes = [...document.querySelectorAll('.pipeline-node')];

function setActiveLayer(layer) {
  railLinks.forEach((link) => {
    const active = link.dataset.layer === layer;
    link.classList.toggle('is-active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  pipelineNodes.forEach((node) => {
    node.classList.toggle('is-active', node.dataset.layer === layer);
  });
  document.documentElement.dataset.activeLayer = layer;
}

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) setActiveLayer(visible.target.dataset.observe);
  }, { rootMargin: '-20% 0px -55%', threshold: [0.15, 0.35, 0.6] });

  observedSections.forEach((section) => observer.observe(section));
}

setActiveLayer('energy');
```

- [ ] **Step 3: Add restrained motion styling**

Animate only the signature route and section entry:

```css
.pipeline-node {
  opacity: .72;
  transform: translateY(0);
  transition: opacity 240ms ease, border-color 240ms ease, background-color 240ms ease;
}
.pipeline-node.is-active {
  opacity: 1;
  border-color: currentColor;
}
.js .reveal {
  opacity: 0;
  transform: translateY(12px);
}
.js .reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 420ms ease, transform 420ms ease;
}
```

Extend the JavaScript with a second `IntersectionObserver` that adds `is-visible` once and immediately unobserves the element. When `prefers-reduced-motion: reduce` matches, add `is-visible` synchronously instead.

- [ ] **Step 4: Run structural checks**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tests\check_crusoe_dashboard.ps1
git diff --check -- crusoe-ai-factory-dashboard.html tests/check_crusoe_dashboard.ps1
```

Expected: contract passes and `git diff --check` produces no output.

- [ ] **Step 5: Verify in a real browser**

Open the local HTML and verify:

- Desktop viewport `1440 × 1000`: the first viewport shows the thesis, company classification, and complete pipeline without overlap.
- Mobile viewport `390 × 844`: pipeline stages stack, rail becomes horizontal, and there is no horizontal page scrolling.
- Keyboard: Tab reaches the skip link and each rail anchor with a visible focus ring.
- Motion: normal mode updates active layer; reduced-motion mode displays all content without entrance movement.
- Offline: browser network log contains no HTTP requests.

Capture desktop and mobile screenshots for visual review.

- [ ] **Step 6: Correct visual defects found during browser review**

Allow only scoped CSS corrections for:

- Overflow or clipping.
- Text hierarchy and line length.
- Pipeline route alignment.
- Sticky rail collision.
- Focus visibility.
- Contrast.

Re-run Step 4 and Step 5 after corrections.

- [ ] **Step 7: Commit the verified interaction pass**

Run:

```powershell
git add -- crusoe-ai-factory-dashboard.html tests/check_crusoe_dashboard.ps1
git commit -m "Verify Crusoe dashboard interactions"
```

Expected: final commit contains only the verified dashboard and its contract test.

## Completion Criteria

- The contract test passes.
- The page renders without external dependencies.
- Desktop and mobile screenshots show no overlap or horizontal overflow.
- All five system layers remain legible without JavaScript.
- Company disclosures, analysis, and missing data are visibly separated.
- Reduced-motion and keyboard navigation work.
- No unrelated working-tree changes are staged or committed.
