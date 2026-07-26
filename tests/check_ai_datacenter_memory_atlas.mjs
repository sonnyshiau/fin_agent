import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(import.meta.dirname, "..");
const jsdomCandidates = [
  path.join(root, "web/node_modules/jsdom/lib/api.js"),
  path.resolve(root, "../../web/node_modules/jsdom/lib/api.js")
];
const jsdomPath = jsdomCandidates.find(fs.existsSync);
if (!jsdomPath) throw new Error("Existing jsdom runtime is missing.");
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
if (document.readyState === "loading") {
  await new Promise((resolve) => document.addEventListener("DOMContentLoaded", resolve, { once: true }));
}

const scenarios = [...document.querySelectorAll("button[data-scenario]")];
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

const pcieRoute = document.querySelector("#path-ddr-hbm")?.getAttribute("d") || "";
const pcieRouteSegments = (pcieRoute.match(/M/g) || []).length;
if (pcieRouteSegments < 2) {
  throw new Error("PCIe route must stop at the gateway edges instead of crossing its label.");
}

dom.window.close();
console.log("AI Data Center Memory Atlas checks passed.");
