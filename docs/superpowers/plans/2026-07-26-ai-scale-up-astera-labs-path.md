# AI Scale-up and Astera Labs Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a standalone Traditional Chinese interactive HTML that separates Host, CXL memory, CPU–GPU coherent, and GPU scale-up paths while placing Astera Labs products on the correct layers.

**Architecture:** One self-contained HTML file contains semantic content, an inline SVG signal-plane topology, inline CSS, and five defensive vanilla-JavaScript controllers. A Node/jsdom contract validates structure and deterministic interaction states; Playwright validates real-browser layout, animation controls, accessibility, and responsive behavior.

**Tech Stack:** HTML5, CSS Grid, inline SVG, vanilla JavaScript, Node.js, jsdom, Playwright, PowerShell local HTTP server

---

## File Structure

- Create `ai-scale-up-astera-labs-path.html`: complete offline-capable learning dashboard and all interactions.
- Create `tests/check_ai_scale_up_astera_labs_path.mjs`: static and DOM interaction contract.
- Reference `docs/superpowers/specs/2026-07-26-ai-scale-up-astera-labs-path-design.md`: approved architecture and visual requirements.

The page remains a single file for portability. The JavaScript controllers remain separate initializer functions inside that file so each interaction can fail independently without hiding the written content.

### Task 1: Establish the document contract

**Files:**
- Create: `tests/check_ai_scale_up_astera_labs_path.mjs`
- Test: `tests/check_ai_scale_up_astera_labs_path.mjs`

- [ ] **Step 1: Write the failing contract test**

Create a Node test that reads `ai-scale-up-astera-labs-path.html`, imports jsdom from `web/node_modules/jsdom/lib/api.js`, and asserts:

```js
const requiredText = [
  "GPU Scale-up", "Host / Model Load", "CXL Memory Expansion",
  "CPU–GPU Coherent", "Physical Channel", "DDR5", "LPDDR5X", "HBM",
  "Leo", "Scorpio P-Series", "Scorpio X-Series", "Aries",
  "NVLink", "NVSwitch", "UALink", "Scale-out"
];
```

The test must also assert:

```js
if (!html.includes('<html lang="zh-Hant">')) throw new Error("Missing zh-Hant language.");
if (!html.includes('<link rel="icon" href="data:,">')) throw new Error("Missing favicon guard.");
if (/<script[^>]+src=|<link[^>]+stylesheet/i.test(html)) throw new Error("External runtime found.");
if (/TBD|TODO|lorem ipsum/i.test(html)) throw new Error("Placeholder content found.");
```

After constructing jsdom with `runScripts: "dangerously"`, assert exactly six `[data-path-mode]` controls, four `[data-product]` controls, two `[data-layer-mode]` controls, and the following behavior:

```js
for (const button of document.querySelectorAll("[data-path-mode]")) {
  button.click();
  if (document.body.dataset.path !== button.dataset.pathMode) throw new Error("Path state failed.");
  if (button.getAttribute("aria-pressed") !== "true") throw new Error("Path aria state failed.");
}

document.querySelector('[data-product="scorpio-x"]').click();
if (!document.querySelector("#product-title").textContent.includes("Scorpio X")) {
  throw new Error("Product detail failed.");
}

document.querySelector('[data-layer-mode="physical"]').click();
if (document.body.dataset.layer !== "physical") throw new Error("Layer state failed.");

document.querySelector("#motion-toggle").click();
if (document.body.dataset.motion !== "paused") throw new Error("Motion pause failed.");
```

Check every inline SVG for a `<title>` or accessible label, every interactive element for an accessible name, and close the jsdom window.

- [ ] **Step 2: Run the contract and confirm failure**

Run:

```powershell
node .\tests\check_ai_scale_up_astera_labs_path.mjs
```

Expected: `ENOENT` because `ai-scale-up-astera-labs-path.html` does not exist.

- [ ] **Step 3: Commit the contract boundary**

```powershell
git add -- tests/check_ai_scale_up_astera_labs_path.mjs
git commit -m "Test AI scale-up path contract"
```

### Task 2: Build the semantic shell and signal-plane topology

**Files:**
- Create: `ai-scale-up-astera-labs-path.html`
- Test: `tests/check_ai_scale_up_astera_labs_path.mjs`

- [ ] **Step 1: Create the accessible document shell**

Use this top-level structure:

```html
<body data-path="overview" data-layer="logical" data-motion="running">
  <a class="skip-link" href="#main">跳至主要內容</a>
  <header class="hero shell">...</header>
  <main id="main">
    <section id="signal-plane" aria-labelledby="signal-title">...</section>
    <section id="path-definitions" aria-labelledby="definitions-title">...</section>
    <section id="product-map" aria-labelledby="products-title">...</section>
    <section id="fabric-comparison" aria-labelledby="comparison-title">...</section>
    <section id="review" aria-labelledby="review-title">...</section>
  </main>
  <footer>...</footer>
</body>
```

The head includes UTF-8 metadata, viewport metadata, a useful description, the title `AI Scale-up Signal Plane｜Astera Labs 產品路徑圖`, and `<link rel="icon" href="data:,">`.

- [ ] **Step 2: Implement the approved visual tokens**

Start with:

```css
:root {
  --backplane:#081018; --module:#101c26; --module-raised:#142430;
  --trace:#294252; --host:#4ca6dd; --scale:#f06cad;
  --physical:#f3b45a; --memory:#57d6c0;
  --text:#e8f0f5; --muted:#92a8b7; --danger:#ff8074;
  --page:1440px; --radius:4px;
}
*{box-sizing:border-box}
html{color-scheme:dark;scroll-behavior:smooth}
body{margin:0;background:var(--backplane);color:var(--text);font-family:"Microsoft JhengHei",system-ui,sans-serif}
h1,h2,h3{font-family:Bahnschrift,"Arial Narrow","Microsoft JhengHei",sans-serif}
.mono,code,.eyebrow{font-family:Consolas,monospace}
:focus-visible{outline:3px solid #fff;outline-offset:3px}
```

Use thin engineering dividers, square module nodes, compact labels, and no decorative gradient or glass-card effects. Color must be redundant with text labels and line patterns.

- [ ] **Step 3: Draw the complete inline SVG topology**

The SVG must have labeled groups for:

```text
Storage: NVMe SSD
Host: CPU Root Complex, DDR5 DIMMs, LPDDR5X alternative, PCIe/CXL Root Port
Physical: Aries Retimer
Front-end: Scorpio P-Series, GPU/NIC/SSD endpoints
CXL memory: Leo Controller, DDR5 expansion pool
Accelerator 0..N: Compute, DMA/NoC, Memory Controller, HBM stacks
Open scale-up: Scorpio X-Series
Closed scale-up: NVLink and NVSwitch alternative
Boundary: Scale-out NIC to Ethernet/InfiniBand
```

Every link receives both a stable `data-link` value and a visible text label. Request and response paths use separate SVG paths so direction can be independently highlighted.

- [ ] **Step 4: Add desktop and mobile layouts**

Desktop uses a topology/detail-rail grid. At `max-width: 820px`, replace the topology with a vertical `.mobile-path` stepper containing the same nodes and non-function warnings. Do not merely scale the SVG below legible size.

- [ ] **Step 5: Run the contract to expose interaction failures**

Run `node .\tests\check_ai_scale_up_astera_labs_path.mjs`.

Expected: required content and structural counts pass; unimplemented interaction assertions fail.

### Task 3: Implement deterministic path, layer, product, and motion controls

**Files:**
- Modify: `ai-scale-up-astera-labs-path.html`
- Test: `tests/check_ai_scale_up_astera_labs_path.mjs`

- [ ] **Step 1: Add the path dataset**

Define six exact path keys:

```js
const PATHS = {
  overview: { title: "System Overview", links: [] },
  host: { title: "Host / Model Load", links: ["storage-host","host-aries","aries-p","p-gpu","gpu-hbm"] },
  cxl: { title: "CXL Memory Expansion", links: ["host-aries","aries-leo","leo-ddr"] },
  coherent: { title: "CPU–GPU Coherent", links: ["cpu-lpddr","cpu-gpu-c2c","gpu-hbm"] },
  scaleup: { title: "GPU Scale-up", links: ["gpu0-x-request","x-gpu1-request","gpu1-hbm","gpu1-x-response","x-gpu0-response"] },
  physical: { title: "Physical Channel", links: ["host-aries","aries-p","p-gpu"] }
};
```

Each entry also supplies a one-sentence purpose, a traffic label, and a misconception correction for the live rail.

- [ ] **Step 2: Implement `initPathController()`**

On activation, set `body.dataset.path`, update all path buttons' `aria-pressed`, apply `.is-active` only to relevant `[data-link]` elements, update `#active-path-title`, `#active-path-purpose`, and `#active-path-warning`, and reset the hop index.

- [ ] **Step 3: Implement `initProductController()`**

Use one data object with exact fields `name`, `layer`, `sits`, `moves`, `solves`, `not`, `driver`, and `dependency` for `aries`, `leo`, `scorpio-p`, and `scorpio-x`. Update the fixed engineering rail and `aria-pressed` state without moving the topology.

- [ ] **Step 4: Implement `initLayerController()`**

Logical mode emphasizes transaction semantics and hides physical annotations. Physical mode emphasizes lanes, connectors, retimer/AEC positions, and reach notes. Set `body.dataset.layer` and `aria-pressed` deterministically.

- [ ] **Step 5: Implement `initMotionController()`**

The controller provides `#motion-toggle` and `#step-path`. Pause when the document is hidden. Honor `matchMedia("(prefers-reduced-motion: reduce)")` by defaulting to paused and showing numbered hops. The step button advances one active link and wraps at the end.

- [ ] **Step 6: Run the contract and confirm pass**

Run `node .\tests\check_ai_scale_up_astera_labs_path.mjs`.

Expected: `AI Scale-up and Astera Labs path checks passed.`

- [ ] **Step 7: Commit the functional dashboard**

```powershell
git add -- ai-scale-up-astera-labs-path.html tests/check_ai_scale_up_astera_labs_path.mjs
git commit -m "Build interactive AI scale-up path atlas"
```

### Task 4: Complete explanations, product boundaries, comparison, and sources

**Files:**
- Modify: `ai-scale-up-astera-labs-path.html`
- Test: `tests/check_ai_scale_up_astera_labs_path.mjs`

- [ ] **Step 1: Add four canonical path definition panels**

Each panel uses the same four fields:

```text
Starts here / Crosses / Ends here / Why it is not another path
```

DDR and LPDDR must be labeled alternatives. CPU–GPU coherent memory must state that shared address space does not merge the physical LPDDR and HBM domains. GPU scale-up must explicitly exclude CPU, DDR, and LPDDR from its default hot trace.

- [ ] **Step 2: Add the Astera product map**

Use four compact products with the factual boundaries from the approved spec. Include the sentence `Scorpio P 是 PCIe 前端；Scorpio X 才直接進入 Accelerator Scale-up 後端。` prominently.

- [ ] **Step 3: Add the fabric comparison table**

Rows: PCIe/CXL Host, NVLink/NVSwitch, UALink/Open Scale-up, Ethernet/InfiniBand Scale-out. Columns: participants, semantics, CPU hot-path involvement, switch role, memory destination, domain, and Astera exposure.

- [ ] **Step 4: Add source discipline and official links**

Include visible source links to CXL Consortium, UALink Consortium, NVIDIA NVLink, NVIDIA Grace memory guidance, and official Astera product pages. Label vendor performance claims as vendor claims and separate current product positioning from roadmap statements.

- [ ] **Step 5: Add the four-question review block**

Provide immediate one-sentence feedback for questions covering CPU memory attachment, accelerator-local memory, true GPU scale-up, and Astera layer placement. No persistent score is required.

- [ ] **Step 6: Re-run contract and placeholder scans**

```powershell
node .\tests\check_ai_scale_up_astera_labs_path.mjs
rg -n "TBD|TODO|lorem ipsum|example text" .\ai-scale-up-astera-labs-path.html
git diff --check
```

Expected: contract passes; `rg` returns no matches; diff check is clean.

### Task 5: Verify in a real browser and finish

**Files:**
- Modify if required: `ai-scale-up-astera-labs-path.html`
- Create locally only: `output/ai-scale-up-desktop.png`
- Create locally only: `output/ai-scale-up-mobile.png`

- [ ] **Step 1: Serve the worktree through localhost**

Run a hidden local server from the worktree and verify `http://127.0.0.1:<port>/ai-scale-up-astera-labs-path.html` returns HTTP 200.

- [ ] **Step 2: Exercise the desktop UI at 1440 × 1000**

Use Playwright to activate all six path modes, all four products, both layer modes, pause/resume, and step-through. Assert body datasets and updated rail text. Capture `output/ai-scale-up-desktop.png`.

- [ ] **Step 3: Exercise mobile at 390 × 844**

Verify the mobile stepper is visible, the desktop topology is not used as unreadable scaled content, all path controls remain reachable, and page-level horizontal overflow is zero. Capture `output/ai-scale-up-mobile.png`.

- [ ] **Step 4: Check accessibility and runtime health**

Verify keyboard focus order, visible focus, reduced-motion rendering, no console errors, no failed required resources, and no external runtime requests.

- [ ] **Step 5: Run final verification**

```powershell
node .\tests\check_ai_scale_up_astera_labs_path.mjs
git diff --check
git status --short
```

Expected: contract passes; diff check is clean; only intended HTML/test changes and ignored or pre-existing `output/` artifacts are present.

- [ ] **Step 6: Commit verified fixes if browser validation changed the page**

```powershell
git add -- ai-scale-up-astera-labs-path.html tests/check_ai_scale_up_astera_labs_path.mjs
git commit -m "Verify AI scale-up path atlas"
```
