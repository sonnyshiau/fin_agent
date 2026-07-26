# AI Data Center Memory Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a self-contained Traditional Chinese HTML atlas that explains SRAM, DRAM, HBM, GDDR, NAND, NOR, SSD, and KV cache through an interactive AI data-center data path.

**Architecture:** One standalone HTML file contains semantic content, inline CSS, original inline SVG diagrams, and four defensive vanilla-JavaScript controllers for scenario playback, component details, bandwidth calculation, and the quiz. A Node/jsdom contract test validates structure and deterministic interaction states; real-browser checks validate rendering, responsiveness, accessibility, and motion behavior.

**Tech Stack:** HTML5, CSS Grid, inline SVG, vanilla JavaScript, Node.js, jsdom, local HTTP server, Playwright browser verification

---

## File Structure

- Create `ai-datacenter-memory-atlas.html`: complete offline-capable learning dashboard, diagrams, factual source notes, and interactions.
- Create `tests/check_ai_datacenter_memory_atlas.mjs`: DOM contract and interaction tests using the repository's existing jsdom installation.
- Reference `docs/superpowers/specs/2026-07-26-ai-datacenter-memory-atlas-design.md`: approved product and visual requirements; do not modify during implementation.

The page remains one HTML file because portability is a core requirement. JavaScript responsibilities stay isolated through four initializer functions rather than being split into runtime files that would break the standalone artifact.

### Task 1: Establish the HTML and interaction contract

**Files:**
- Create: `tests/check_ai_datacenter_memory_atlas.mjs`
- Test: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Write the failing DOM contract test**

Create `tests/check_ai_datacenter_memory_atlas.mjs` with this complete content:

```js
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(import.meta.dirname, "..");
const jsdomPath = path.join(root, "web/node_modules/jsdom/lib/api.js");
if (!fs.existsSync(jsdomPath)) throw new Error("Existing jsdom runtime is missing.");
const { JSDOM } = await import(pathToFileURL(jsdomPath).href);

const htmlPath = path.join(root, "ai-datacenter-memory-atlas.html");
const html = fs.readFileSync(htmlPath, "utf8");

const requiredText = [
  "AI Data Center Memory Atlas", "SRAM", "DDR DRAM", "GDDR", "HBM",
  "KV Cache", "NAND Flash", "NOR Flash", "NVMe SSD",
  "Model Load", "Prefill", "Decode",
  "Bandwidth (GB/s) = data rate × interface width × stacks ÷ 8"
];
for (const value of requiredText) {
  if (!html.includes(value)) throw new Error(`Missing required content: ${value}`);
}

if (!html.includes('<html lang="zh-Hant">')) throw new Error("Document language must be zh-Hant.");
if (!html.includes('<link rel="icon" href="data:,">')) throw new Error("Inline favicon guard is missing.");
if (/<script[^>]+src=|<link[^>]+stylesheet/i.test(html)) throw new Error("External runtime dependency found.");
if (/TBD|TODO|lorem ipsum/i.test(html)) throw new Error("Placeholder content found.");

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  pretendToBeVisual: true,
  url: "http://127.0.0.1/ai-datacenter-memory-atlas.html"
});
const { document } = dom.window;

const scenarios = [...document.querySelectorAll("[data-scenario]")];
if (scenarios.length !== 3) throw new Error("Expected exactly three scenario controls.");
for (const button of scenarios) {
  button.click();
  if (document.body.dataset.scenario !== button.dataset.scenario) {
    throw new Error(`Scenario failed: ${button.dataset.scenario}`);
  }
  if (button.getAttribute("aria-pressed") !== "true") throw new Error("Scenario aria state failed.");
}

const componentButtons = [...document.querySelectorAll("[data-component]")];
if (componentButtons.length < 8) throw new Error("Expected at least eight component controls.");
componentButtons.find((button) => button.dataset.component === "kv").click();
if (document.querySelector("#detail-category").textContent !== "模型資料結構") {
  throw new Error("KV cache classification failed.");
}

const rate = document.querySelector("#hbm-rate");
const width = document.querySelector("#hbm-width");
const stacks = document.querySelector("#hbm-stacks");
rate.value = "3.2";
width.value = "1024";
stacks.value = "2";
rate.dispatchEvent(new dom.window.Event("input", { bubbles: true }));
if (document.querySelector("#bandwidth-result").textContent !== "819.2 GB/s") {
  throw new Error("HBM bandwidth calculation failed.");
}

const firstChoice = document.querySelector("[data-quiz-choice]");
firstChoice.click();
if (!document.querySelector("#quiz-feedback").textContent.trim()) {
  throw new Error("Quiz feedback did not render.");
}

for (const svg of document.querySelectorAll("svg")) {
  if (!svg.querySelector("title") && !svg.getAttribute("aria-label")) {
    throw new Error("Inline SVG is missing an accessible title or label.");
  }
}

dom.window.close();
console.log("AI Data Center Memory Atlas checks passed.");
```

- [ ] **Step 2: Run the contract and confirm the expected failure**

Run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
```

Expected: `ENOENT` for `ai-datacenter-memory-atlas.html` because implementation has not been created.

- [ ] **Step 3: Commit the contract boundary**

Run:

```powershell
git add -- tests/check_ai_datacenter_memory_atlas.mjs
git commit -m "Test AI memory atlas contract"
```

Expected: one commit containing only the new contract test.

### Task 2: Build the semantic shell and visual system

**Files:**
- Create: `ai-datacenter-memory-atlas.html`
- Test: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Create the accessible document shell**

Create a complete HTML5 document with these top-level landmarks and exact IDs:

```html
<body data-scenario="load">
  <a class="skip-link" href="#atlas-main">跳至主要內容</a>
  <header class="site-header">...</header>
  <main id="atlas-main">
    <section id="orientation" aria-labelledby="orientation-title">...</section>
    <section id="data-path" aria-labelledby="data-path-title">...</section>
    <section id="layers" aria-labelledby="layers-title">...</section>
    <section id="hbm-anatomy" aria-labelledby="hbm-title">...</section>
    <section id="comparison" aria-labelledby="comparison-title">...</section>
    <section id="four-axes" aria-labelledby="axes-title">...</section>
    <section id="review" aria-labelledby="review-title">...</section>
  </main>
  <footer>...</footer>
</body>
```

The `<head>` must contain UTF-8 metadata, responsive viewport metadata, the title `AI Data Center Memory Atlas｜AI 資料中心記憶體全圖解`, a useful description, and `<link rel="icon" href="data:,">`.

- [ ] **Step 2: Implement the approved design tokens and layout**

Use this token foundation and derive every component color from it:

```css
:root {
  --backplane: #0b1118;
  --module: #121d27;
  --module-raised: #182632;
  --trace: #2b3b49;
  --trace-active: #d7e3ea;
  --sram: #53d6c1;
  --dram: #5da9ff;
  --flash: #f2b45b;
  --compute: #e879a9;
  --text: #e8eef2;
  --muted: #92a2ae;
  --danger: #ff7f73;
  --focus: #ffffff;
  --radius: 6px;
  --page: 1280px;
}
* { box-sizing: border-box; }
html { color-scheme: dark; scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--backplane);
  color: var(--text);
  font-family: "Noto Sans TC", "Microsoft JhengHei", system-ui, sans-serif;
  line-height: 1.55;
}
.shell { width: min(var(--page), calc(100vw - 32px)); margin-inline: auto; }
.mono, .metric, code { font-family: Consolas, "IBM Plex Mono", monospace; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
@media (max-width: 760px) {
  .shell { width: min(100% - 20px, var(--page)); }
  .data-path-grid, .hbm-grid { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
```

Use thin trace-like dividers, square engineering labels, limited 6 px radii, and no decorative gradients, glass effects, glows, or repeated generic icon cards.

- [ ] **Step 3: Add the orientation taxonomy and concise copy**

The first viewport must immediately show the thesis sentence and these four labeled categories:

```html
<ul class="taxonomy" aria-label="名詞分類">
  <li><b>物理技術</b><span>SRAM · DRAM · NAND · NOR</span></li>
  <li><b>系統角色</b><span>CPU Cache · 內存 · 顯存</span></li>
  <li><b>裝置／封裝</b><span>DIMM · HBM Stack · SSD</span></li>
  <li><b>模型資料結構</b><span>KV Cache</span></li>
</ul>
```

No explanatory paragraph in the page may exceed three sentences. Prefer labels, tables, and short callouts.

- [ ] **Step 4: Run the contract to expose remaining behavior failures**

Run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
```

Expected: the file is found and static required text checks advance; the test still fails on missing scenario or interaction elements.

### Task 3: Implement the rack-to-chip data path and component inspector

**Files:**
- Modify: `ai-datacenter-memory-atlas.html`
- Test: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Draw the original rack-to-chip SVG**

Inside `#data-path`, add one responsive SVG with `viewBox="0 0 1080 620"`, a `<title>AI 資料中心從 SSD 到運算單元的資料路徑</title>`, and component groups identified by `ssd-node`, `cpu-node`, `ddr-node`, `pcie-node`, `hbm-node`, `sram-node`, and `compute-node`. Add separate named paths for:

```html
<path id="path-ssd-ddr" class="trace flash-path" ... />
<path id="path-ddr-hbm" class="trace dram-path" ... />
<path id="path-hbm-sram" class="trace dram-path" ... />
<path id="path-sram-compute" class="trace sram-path" ... />
<path id="path-compute-hbm" class="trace compute-path" ... />
```

Use arrow markers and adjacent text labels so the flow is understandable without relying on color. The selected path receives `.is-active`; the current payload is represented by one SVG circle following the active route. Do not animate in reduced-motion mode.

- [ ] **Step 2: Add the three scenario controls and state data**

Add native buttons with `data-scenario="load"`, `data-scenario="prefill"`, and `data-scenario="decode"`. Implement this complete scenario model:

```js
const scenarios = {
  load: {
    label: "Model Load",
    summary: "SSD 的 NAND 保存模型；啟動服務時，權重經 Host DRAM 搬入 GPU HBM。",
    paths: ["path-ssd-ddr", "path-ddr-hbm"]
  },
  prefill: {
    label: "Prefill",
    summary: "GPU 平行處理 prompt；權重與 activation 在 HBM、SRAM、運算單元間流動，K/V 寫回 HBM。",
    paths: ["path-hbm-sram", "path-sram-compute", "path-compute-hbm"]
  },
  decode: {
    label: "Decode",
    summary: "每一步讀取權重與歷史 KV，分塊搬入 SRAM 完成 attention，再把新 K/V append 到 HBM。",
    paths: ["path-hbm-sram", "path-sram-compute", "path-compute-hbm"]
  }
};

function initScenarioController() {
  const buttons = [...document.querySelectorAll("[data-scenario]")];
  const summary = document.querySelector("#scenario-summary");
  if (!buttons.length || !summary) return;
  const activate = (name) => {
    const scenario = scenarios[name];
    if (!scenario) return;
    document.body.dataset.scenario = name;
    buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.scenario === name)));
    document.querySelectorAll(".trace").forEach((path) => path.classList.toggle("is-active", scenario.paths.includes(path.id)));
    summary.textContent = scenario.summary;
  };
  buttons.forEach((button) => button.addEventListener("click", () => activate(button.dataset.scenario)));
  activate(document.body.dataset.scenario || "load");
}
```

- [ ] **Step 3: Add the component data model and inspector**

Create at least these keys in `componentFacts`: `sram`, `ddr`, `gddr`, `hbm`, `kv`, `nand`, `nor`, `ssd`. Every record must contain `name`, `category`, `medium`, `stores`, `purpose`, `volatile`, and `misconception`. KV must use `category: "模型資料結構"`; SSD must use `category: "裝置"`.

Implement the inspector:

```js
function initComponentInspector() {
  const buttons = [...document.querySelectorAll("[data-component]")];
  const fields = ["name", "category", "medium", "stores", "purpose", "volatile", "misconception"];
  if (!buttons.length) return;
  const show = (key) => {
    const fact = componentFacts[key];
    if (!fact) return;
    fields.forEach((field) => {
      const node = document.querySelector(`#detail-${field}`);
      if (node) node.textContent = fact[field];
    });
    buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.component === key)));
  };
  buttons.forEach((button) => button.addEventListener("click", () => show(button.dataset.component)));
  show("sram");
}
```

Component controls must be actual `<button>` elements arranged as an annotated hierarchy, not identical floating cards.

- [ ] **Step 4: Verify data-path and inspector behavior**

Run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
```

Expected: scenario and KV classification checks pass; the test may still fail at the missing calculator or quiz.

- [ ] **Step 5: Commit the first working slice**

Run:

```powershell
git add -- ai-datacenter-memory-atlas.html
git commit -m "Build AI memory hierarchy data path"
```

Expected: one commit containing the semantic shell, visual system, data-path scenarios, and component inspector.

### Task 4: Add HBM anatomy, calculator, comparison, and review mode

**Files:**
- Modify: `ai-datacenter-memory-atlas.html`
- Test: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Draw the HBM exploded-view SVG**

Add an inline SVG with `<title>HBM DRAM 堆疊、TSV、Interposer 與 GPU 封裝剖面</title>`. Label four or eight conceptual DRAM dies, TSVs, base/interface die, micro-bumps, silicon interposer, GPU die, and package substrate. Connect the stack to the GPU with one explicitly labeled `1024-bit per stack` interface.

Place this correction beside the diagram:

```html
<aside class="correction">
  <strong>堆疊層數 ≠ 外部介面倍增</strong>
  <p>增加 DRAM die 主要提高容量與內部平行性；HBM2E 的完整 stack 對處理器仍呈現 1024-bit 總介面。</p>
</aside>
```

- [ ] **Step 2: Implement the bandwidth calculator**

Add numeric inputs `#hbm-rate`, `#hbm-width`, and `#hbm-stacks`, plus `#bandwidth-result` and an `aria-live="polite"` note. Defaults are 3.2, 1024, and 2.

Use this controller exactly:

```js
function initBandwidthCalculator() {
  const rate = document.querySelector("#hbm-rate");
  const width = document.querySelector("#hbm-width");
  const stacks = document.querySelector("#hbm-stacks");
  const output = document.querySelector("#bandwidth-result");
  if (!rate || !width || !stacks || !output) return;
  const update = () => {
    const values = [rate, width, stacks].map((input) => Number(input.value));
    const valid = values.every((value) => Number.isFinite(value) && value > 0);
    output.textContent = valid ? `${(values[0] * values[1] * values[2] / 8).toFixed(1)} GB/s` : "請輸入正數";
  };
  [rate, width, stacks].forEach((input) => input.addEventListener("input", update));
  update();
}
```

Show `Bandwidth (GB/s) = data rate × interface width × stacks ÷ 8` verbatim and label the result as theoretical peak bandwidth.

- [ ] **Step 3: Add the comparison matrix and four-axis explanation**

Add a real `<table>` with the exact columns `名詞`, `分類`, `Cell／介質`, `斷電`, `典型位置`, `最佳化目標`, and `AI Data Center 例子`. Include rows for SRAM, DDR DRAM, GDDR, HBM, NAND Flash, NOR Flash, NVMe SSD, and KV Cache. Set KV Cache's technology cell to `不是記憶體技術；是 K/V tensor`.

Add a four-axis visual with independent meters for bandwidth, latency, capacity, and persistence. Include the sentence `高頻寬不等於低延遲` as a visible engineering note.

- [ ] **Step 4: Implement the deterministic classification quiz**

Use this data and controller:

```js
const quizQuestions = [
  { term: "HBM", answer: "物理技術", why: "HBM 是以堆疊 DRAM 與寬介面實作的記憶體技術。" },
  { term: "顯存／VRAM", answer: "系統角色", why: "顯存描述 GPU 使用的記憶體角色，可由 GDDR、HBM 或共享 DRAM 實作。" },
  { term: "SSD", answer: "裝置／封裝", why: "SSD 是由 NAND、控制器、韌體與介面組成的儲存裝置。" },
  { term: "KV Cache", answer: "模型資料結構", why: "KV cache 是 attention 的歷史 K/V tensor，不是一種 SRAM 或 DRAM。" }
];

function initQuiz() {
  const term = document.querySelector("#quiz-term");
  const feedback = document.querySelector("#quiz-feedback");
  const next = document.querySelector("#quiz-next");
  const choices = [...document.querySelectorAll("[data-quiz-choice]")];
  if (!term || !feedback || !next || !choices.length) return;
  let index = 0;
  const render = () => {
    term.textContent = quizQuestions[index].term;
    feedback.textContent = "選擇它屬於哪一類。";
    choices.forEach((choice) => { choice.disabled = false; choice.removeAttribute("data-result"); });
  };
  choices.forEach((choice) => choice.addEventListener("click", () => {
    const question = quizQuestions[index];
    const correct = choice.dataset.quizChoice === question.answer;
    feedback.textContent = `${correct ? "正確。" : `答案是${question.answer}。`} ${question.why}`;
    choices.forEach((item) => { item.disabled = true; });
    choice.dataset.result = correct ? "correct" : "incorrect";
  }));
  next.addEventListener("click", () => { index = (index + 1) % quizQuestions.length; render(); });
  render();
}
```

Initialize all four controllers inside one `DOMContentLoaded` callback. Add a `visibilitychange` listener that removes the SVG payload animation class while hidden and restores it only if reduced motion is not requested.

- [ ] **Step 5: Add factual source notes**

At the bottom, include short direct links to official technical sources used for factual verification:

- AMD HBM topology documentation for 1024-bit stack organization and pseudo-channels
- Micron HBM2E technical paper for per-pin rate, width, and device bandwidth comparison
- Hugging Face cache explanation for per-layer K/V tensor shape and autoregressive reuse

Do not embed third-party images unless an official product image adds information not already present in the inline SVG. If an image is used, add explicit attribution, alt text, width/height, and an adjacent SVG/text fallback.

- [ ] **Step 6: Run the full contract test**

Run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
```

Expected: `AI Data Center Memory Atlas checks passed.`

- [ ] **Step 7: Commit the completed interaction set**

Run:

```powershell
git add -- ai-datacenter-memory-atlas.html
git commit -m "Complete AI memory atlas interactions"
```

Expected: one commit containing HBM anatomy, calculator, comparison matrix, four-axis explanation, quiz, and source notes.

### Task 5: Verify responsive rendering and accessibility in a real browser

**Files:**
- Modify: `ai-datacenter-memory-atlas.html` only if verification exposes a scoped defect
- Test: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Start a local HTTP server from the repository root**

Run:

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory C:\Users\User\Desktop\fin_agent
```

Expected: `http://127.0.0.1:8765/ai-datacenter-memory-atlas.html` returns HTTP 200. Keep this process running only for browser verification.

- [ ] **Step 2: Verify desktop behavior at 1440 × 1000**

Open the page in Playwright and verify:

- The first viewport exposes the thesis, taxonomy, and beginning of the data path
- Model Load, Prefill, and Decode update `body[data-scenario]`, path highlighting, summary text, and `aria-pressed`
- Every component button updates the inspector without layout shift
- Calculator defaults to `819.2 GB/s` and handles zero/empty values with `請輸入正數`
- Quiz choices render one-sentence feedback and Next advances the term
- No console errors, unhandled exceptions, or failed required resources

Capture a desktop screenshot for visual review; do not commit the screenshot.

- [ ] **Step 3: Verify mobile behavior at 390 × 844**

Confirm:

- `document.documentElement.scrollWidth === document.documentElement.clientWidth`
- Data-path and HBM grids stack vertically
- The comparison table scrolls within its own wrapper rather than expanding the page
- Buttons remain at least 40 px tall and do not overlap
- SVG labels remain readable through responsive scaling
- The detail rail appears directly after the diagram

Capture a mobile screenshot for visual review; do not commit the screenshot.

- [ ] **Step 4: Verify keyboard and reduced-motion behavior**

Using only Tab, Shift+Tab, Enter, and Space, exercise scenario buttons, component controls, calculator fields, and quiz controls. Confirm visible focus throughout. Emulate `prefers-reduced-motion: reduce` and verify active paths still change but the payload does not move continuously.

- [ ] **Step 5: Apply only defects found during verification**

If verification reveals a defect, edit only `ai-datacenter-memory-atlas.html`, then run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
git diff --check -- ai-datacenter-memory-atlas.html tests/check_ai_datacenter_memory_atlas.mjs
```

Expected: contract passes and `git diff --check` produces no output.

- [ ] **Step 6: Run the repository regression suite**

Run:

```powershell
python -m pytest -q
```

Expected: all pre-existing Python tests pass. If an unrelated pre-existing failure occurs, record it without changing unrelated files.

- [ ] **Step 7: Commit browser-polish fixes if needed**

If the browser pass required changes, run:

```powershell
git add -- ai-datacenter-memory-atlas.html
git commit -m "Polish AI memory atlas presentation"
```

If no HTML change was required, do not create an empty commit.

### Task 6: Final completion audit

**Files:**
- Verify: `ai-datacenter-memory-atlas.html`
- Verify: `tests/check_ai_datacenter_memory_atlas.mjs`

- [ ] **Step 1: Re-run deterministic checks**

Run:

```powershell
node .\tests\check_ai_datacenter_memory_atlas.mjs
python -m pytest -q
git diff --check
```

Expected: the atlas contract passes, Python tests pass, and no whitespace errors are reported.

- [ ] **Step 2: Confirm scope and artifact status**

Run:

```powershell
git status --short
git log -5 --oneline
```

Expected: the new HTML and contract test are committed. Existing unrelated user changes remain untouched. GitHub Pages publication is not performed because it is outside the approved specification.

- [ ] **Step 3: Hand off the artifact**

Report the absolute clickable path to `ai-datacenter-memory-atlas.html`, summarize the four interactions, list the exact verification results, and explicitly state that the page is local-only until publication is separately requested.
