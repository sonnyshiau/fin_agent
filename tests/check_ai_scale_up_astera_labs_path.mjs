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

const htmlPath = path.join(root, "ai-scale-up-astera-labs-path.html");
const html = fs.readFileSync(htmlPath, "utf8");

const requiredText = [
  "GPU Scale-up", "Host / Model Load", "CXL Memory Expansion",
  "CPU–GPU Coherent", "Physical Channel", "DDR5", "LPDDR5X", "HBM",
  "Leo", "Scorpio P-Series", "Scorpio X-Series", "Aries",
  "NVLink", "NVSwitch", "UALink", "Scale-out"
];
for (const value of requiredText) {
  if (!html.includes(value)) throw new Error(`Missing required content: ${value}`);
}

if (!html.includes('<html lang="zh-Hant">')) throw new Error("Missing zh-Hant language.");
if (!html.includes('<link rel="icon" href="data:,">')) throw new Error("Missing favicon guard.");
if (/<script[^>]+src=|<link[^>]+stylesheet/i.test(html)) throw new Error("External runtime found.");
if (/TBD|TODO|lorem ipsum/i.test(html)) throw new Error("Placeholder content found.");

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  pretendToBeVisual: true,
  url: "http://127.0.0.1/ai-scale-up-astera-labs-path.html"
});
const { document } = dom.window;

const pathControls = [...document.querySelectorAll("[data-path-mode]")];
if (pathControls.length !== 6) throw new Error("Expected exactly six path controls.");
for (const button of pathControls) {
  button.click();
  if (document.body.dataset.path !== button.dataset.pathMode) {
    throw new Error(`Path state failed: ${button.dataset.pathMode}`);
  }
  if (button.getAttribute("aria-pressed") !== "true") throw new Error("Path aria state failed.");
}

const products = [...document.querySelectorAll("[data-product]")];
if (products.length !== 4) throw new Error("Expected exactly four product controls.");
document.querySelector('[data-product="scorpio-x"]').click();
if (!document.querySelector("#product-title").textContent.includes("Scorpio X")) {
  throw new Error("Product detail failed.");
}

const layerControls = [...document.querySelectorAll("[data-layer-mode]")];
if (layerControls.length !== 2) throw new Error("Expected exactly two layer controls.");
document.querySelector('[data-layer-mode="physical"]').click();
if (document.body.dataset.layer !== "physical") throw new Error("Layer state failed.");

const motionToggle = document.querySelector("#motion-toggle");
motionToggle.click();
if (document.body.dataset.motion !== "paused") throw new Error("Motion pause failed.");

document.querySelector('[data-path-mode="scaleup"]').click();
const activeLinks = [...document.querySelectorAll("[data-link].is-active")];
if (activeLinks.length < 5) throw new Error("Scale-up path did not highlight all request/response hops.");
if (activeLinks.some((link) => /host|aries|leo|ddr/i.test(link.dataset.link))) {
  throw new Error("Scale-up hot path incorrectly includes host memory or host-link products.");
}

const stepButton = document.querySelector("#step-path");
stepButton.click();
if (!document.querySelector("[data-link].is-current-hop")) throw new Error("Path stepping failed.");

for (const svg of document.querySelectorAll("svg")) {
  if (!svg.querySelector("title") && !svg.getAttribute("aria-label")) {
    throw new Error("Inline SVG is missing an accessible title or label.");
  }
}

for (const control of document.querySelectorAll("button, a[href]")) {
  const name = control.getAttribute("aria-label") || control.textContent.trim();
  if (!name) throw new Error("Interactive control is missing an accessible name.");
}

dom.window.close();
console.log("AI Scale-up and Astera Labs path checks passed.");
