# AI Inference Memory Data Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a self-contained animated HTML diagram showing LLM prefill, decode, KV-hit, and KV-miss data movement through on-chip SRAM, GPU HBM, host DRAM, and NVMe.

**Architecture:** One standalone HTML file contains the accessible document structure, responsive research-dashboard styling, SVG topology, scenario data, and a small animation state machine. A Node/jsdom contract test loads the document, executes its embedded script, and validates scenario switching and playback controls without external dependencies.

**Tech Stack:** HTML5, CSS Grid, inline SVG, vanilla JavaScript, Node.js, jsdom

---

## File Structure

- Create `ai-inference-memory-data-path.html`: complete visualization, styles, SVG, scenario definitions, and animation controller.
- Create `tests/check_ai_inference_memory_data_path.mjs`: static structure and interactive DOM-state checks.

### Task 1: Establish the visualization contract

**Files:**
- Create: `tests/check_ai_inference_memory_data_path.mjs`
- Test: `tests/check_ai_inference_memory_data_path.mjs`

- [ ] **Step 1: Write the failing contract test**

Create a jsdom test that requires Traditional Chinese metadata, all four memory tiers, all four scenario controls, the SVG paths, and the animation API:

```js
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(import.meta.dirname, "..");
const jsdomCandidates = [
  path.join(root, "web/node_modules/jsdom/lib/api.js"),
  path.resolve(root, "../../web/node_modules/jsdom/lib/api.js")
];
const jsdomPath = jsdomCandidates.find(fs.existsSync);
if (!jsdomPath) throw new Error("Unable to locate the existing jsdom installation.");
const { JSDOM } = await import(pathToFileURL(jsdomPath).href);
const htmlPath = path.join(root, "ai-inference-memory-data-path.html");
const html = fs.readFileSync(htmlPath, "utf8");
const requiredText = ["On-chip SRAM", "GPU HBM", "Host DRAM", "NVMe SSD", "Prefill", "Decode", "KV Hit", "KV Miss"];
for (const text of requiredText) {
  if (!html.includes(text)) throw new Error(`Missing required content: ${text}`);
}

const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true });
const { document } = dom.window;
const buttons = [...document.querySelectorAll("[data-scenario]")];
if (buttons.length !== 4) throw new Error("Expected four scenario buttons.");

for (const button of buttons) {
  button.click();
  if (document.body.dataset.scenario !== button.dataset.scenario) {
    throw new Error(`Scenario did not activate: ${button.dataset.scenario}`);
  }
}

document.querySelector("#pause-button").click();
if (document.body.dataset.playback !== "paused") throw new Error("Pause control failed.");
document.querySelector("#play-button").click();
if (document.body.dataset.playback !== "playing") throw new Error("Play control failed.");
document.querySelector("#replay-button").click();
if (document.querySelector("#step-index").textContent !== "1") throw new Error("Replay did not reset to step one.");

for (const speed of ["slow", "normal", "fast"]) {
  const input = document.querySelector(`#speed-${speed}`);
  input.click();
  if (document.body.dataset.speed !== speed) throw new Error(`Speed failed: ${speed}`);
}

dom.window.close();
console.log("AI inference memory data-path checks passed.");
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `node tests/check_ai_inference_memory_data_path.mjs`

Expected: failure with `ENOENT` because `ai-inference-memory-data-path.html` does not exist.

- [ ] **Step 3: Commit the test boundary**

Run:

```powershell
git add -- tests/check_ai_inference_memory_data_path.mjs
git commit -m "Test inference memory data path contract"
```

Expected: one commit containing only the new test.

### Task 2: Build the self-contained SVG visualization

**Files:**
- Create: `ai-inference-memory-data-path.html`
- Test: `tests/check_ai_inference_memory_data_path.mjs`

- [ ] **Step 1: Add the semantic page and static SVG topology**

Create one `lang="zh-Hant"` document with a single `h1`, a control bar, a `viewBox="0 0 1200 720"` SVG, and an explanation panel. Use IDs `request-node`, `compute-node`, `sram-node`, `hbm-node`, `dram-node`, `nvme-node`, and `output-node`. Define named paths for request ingress, weight reads, KV reads/writes, offload, reload, and token egress. Every path must be visible in its inactive state.

- [ ] **Step 2: Add the four complete scenario definitions**

Embed this state model and bind every referenced path ID to the SVG:

```js
const scenarios = {
  prefill: [
    { path: "path-request-compute", kind: "activation", title: "Prompt 進入 GPU", detail: "整段 prompt 形成可平行處理的 token batch。" },
    { path: "path-hbm-compute", kind: "weight", title: "從 HBM 讀取 Weights", detail: "大型 GEMM 重用權重，Prefill 通常具有較高 arithmetic intensity。" },
    { path: "path-compute-sram", kind: "activation", title: "On-chip 工作集", detail: "Register、Shared Memory 與 L2 承接當下 tile 與 activation。" },
    { path: "path-compute-hbm", kind: "kv", title: "寫入 Active KV Cache", detail: "各層 K/V tensor 寫入 HBM，供後續 decode 重用。" }
  ],
  decode: [
    { path: "path-request-compute", kind: "activation", title: "輸入目前 Token", detail: "Decode 一次生成少量 token，並行度通常低於 prefill。" },
    { path: "path-hbm-compute", kind: "weight", title: "Weight Streaming", detail: "每層 weights 從 HBM 串流至計算單元。" },
    { path: "path-hbm-compute", kind: "kv", title: "讀取歷史 KV", detail: "Attention 讀取先前所有有效 context 的 K/V。" },
    { path: "path-compute-hbm", kind: "kv", title: "Append 新 K/V", detail: "新 token 的 K/V 加入 active cache。" },
    { path: "path-compute-output", kind: "activation", title: "輸出新 Token", detail: "完成本輪 decode，下一輪再次讀取 weights 與 KV。" }
  ],
  hit: [
    { path: "path-hbm-compute", kind: "kv", title: "HBM KV Hit", detail: "需要的 KV block 已在 HBM，直接進入 attention。" },
    { path: "path-compute-output", kind: "activation", title: "低延遲完成 Decode", detail: "沒有 host-memory 或 storage round trip。" }
  ],
  miss: [
    { path: "path-hbm-dram", kind: "stall", title: "HBM Miss：查找 Host DRAM", detail: "GPU active pool 中沒有目標 KV block。" },
    { path: "path-dram-nvme", kind: "stall", title: "DRAM Miss：查找 NVMe", detail: "更冷的 KV block 位於較大、較慢的儲存層。" },
    { path: "path-nvme-dram", kind: "kv", title: "NVMe → DRAM", detail: "先將 KV block 提升至 host memory。" },
    { path: "path-dram-hbm", kind: "kv", title: "DRAM → HBM Reload", detail: "KV 必須回到 GPU 可高效存取的 active tier。" },
    { path: "path-hbm-compute", kind: "kv", title: "恢復 Decode", detail: "Reload 完成後 attention 才能繼續。" }
  ]
};
```

- [ ] **Step 3: Implement the animation state machine**

Implement `activateScenario(name)`, `renderStep(index)`, `scheduleNext()`, `setPlayback(state)`, `setSpeed(speed)`, and `replay()`. The controller must update `document.body.dataset.scenario`, `dataset.playback`, `dataset.speed`, `#step-index`, step title/detail, active path classes, particle color, and an SVG `animateMotion` reference. Scenario switching cancels the existing timer before resetting to step one.

- [ ] **Step 4: Add responsive and reduced-motion behavior**

Use a maximum page width of 1160px, compact neutral panels, and semantic blue/purple/green/red colors. Below 760px stack controls and the explanation panel, keep the SVG scalable, and retain readable labels. Under `prefers-reduced-motion: reduce`, disable continuous particle movement and keep step/path highlighting functional.

- [ ] **Step 5: Run the contract test**

Run: `node tests/check_ai_inference_memory_data_path.mjs`

Expected: `AI inference memory data-path checks passed.`

- [ ] **Step 6: Commit the implementation**

Run:

```powershell
git add -- ai-inference-memory-data-path.html
git commit -m "Add animated inference memory data path"
```

Expected: one commit containing only the standalone HTML.

### Task 3: Browser and responsive verification

**Files:**
- Modify: `ai-inference-memory-data-path.html` only if browser verification exposes a defect
- Test: `tests/check_ai_inference_memory_data_path.mjs`

- [ ] **Step 1: Serve the workspace through local HTTP**

Run: `python -m http.server 8765 --bind 127.0.0.1`

Expected: the server exposes `/ai-inference-memory-data-path.html` with HTTP 200.

- [ ] **Step 2: Verify desktop interaction in a real browser**

Open `http://127.0.0.1:8765/ai-inference-memory-data-path.html`, click all four scenarios, pause/play/replay, and change all three speeds. Confirm step text, highlighted paths, and moving particle update with no console errors.

- [ ] **Step 3: Verify mobile layout**

At a 390 × 844 viewport, confirm no horizontal page overflow, controls remain tappable, SVG labels remain readable, and explanation panels stack below the diagram.

- [ ] **Step 4: Re-run automated verification**

Run: `node tests/check_ai_inference_memory_data_path.mjs`

Expected: `AI inference memory data-path checks passed.`

- [ ] **Step 5: Record any final scoped fix**

If browser verification required an HTML fix, run:

```powershell
git add -- ai-inference-memory-data-path.html
git commit -m "Polish inference memory data path visualization"
```

If no fix was required, do not create an empty commit.
