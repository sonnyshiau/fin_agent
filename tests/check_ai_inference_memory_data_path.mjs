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
const requiredText = [
  "On-chip SRAM",
  "GPU HBM",
  "Host DRAM",
  "NVMe SSD",
  "Prefill",
  "Decode",
  "KV Hit",
  "KV Miss"
];

for (const text of requiredText) {
  if (!html.includes(text)) throw new Error(`Missing required content: ${text}`);
}

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  pretendToBeVisual: true
});
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
if (document.querySelector("#step-index").textContent !== "1") {
  throw new Error("Replay did not reset to step one.");
}

for (const speed of ["slow", "normal", "fast"]) {
  const input = document.querySelector(`#speed-${speed}`);
  input.click();
  if (document.body.dataset.speed !== speed) throw new Error(`Speed failed: ${speed}`);
}

if (document.querySelectorAll(".data-path").length < 8) {
  throw new Error("Expected the complete SVG data-path topology.");
}

dom.window.close();
console.log("AI inference memory data-path checks passed.");
