# AI Inference Memory Data Path — Design Specification

## Objective

Create a directly openable, self-contained HTML visualization that explains how data moves through the memory hierarchy during LLM inference. The artifact focuses on technical data flow rather than investment analysis.

## Deliverable

- File: `ai-inference-memory-data-path.html`
- Runtime: modern desktop and mobile browsers without a build step
- Packaging: all HTML, CSS, SVG, and JavaScript embedded in one file
- Language: Traditional Chinese with standard English hardware terms

## Visual Architecture

The main diagram uses an SVG data-path canvas. Requests and tokens enter from the left, GPU compute sits in the center, and the memory hierarchy is arranged on the right:

1. On-chip SRAM: registers, shared memory, and L2 cache
2. GPU HBM: model weights, active KV cache, and working data
3. Host DRAM: offloaded or warm KV cache and model staging
4. NVMe SSD: cold or evicted KV cache

Directional paths and animated particles show reads, writes, offloads, reloads, and generated-token output. Every path remains visible when inactive so the topology is always understandable.

## Interactive Scenarios

The control bar exposes four mutually exclusive scenarios:

### Prefill

The prompt enters the GPU, weights are read from HBM, Tensor Core computation runs, and the newly calculated K/V tensors are written into the active KV cache in HBM.

### Decode

The current token enters the GPU while weights and historical KV data are read from HBM. The result produces one output token, and its new K/V data is appended to HBM.

### KV Hit

The active KV block is found in HBM and returned directly to the compute path. This emphasizes the short, low-latency path.

### KV Miss / Offload

The active block is absent from HBM. Lookup proceeds to host DRAM and then NVMe when necessary. The selected block is reloaded through DRAM into HBM before decode continues. This scenario emphasizes stall and data-movement cost.

## Animation Semantics

- Blue particles: model weights
- Purple particles: KV cache
- Green particles: prompts, activations, and generated tokens
- Red particles and paths: cache miss, stall, or high-latency movement

Animation timing is illustrative and does not claim exact hardware latency ratios. A visible note will state this limitation.

## Controls and State

- Scenario buttons: Prefill, Decode, KV Hit, KV Miss / Offload
- Playback controls: play, pause, and replay
- Speed control: slow, normal, and fast
- Step panel: current operation, source, destination, and technical explanation
- Legend: data categories and memory-temperature meaning

Switching scenarios cancels the current animation, resets visual state, selects the new scenario, and starts it from its first step. Replay resets only the active scenario. Pause preserves the current step and particle position.

## Responsive Behavior

Desktop uses the full horizontal data-path canvas. Below tablet width, the diagram remains an SVG with a fixed internal coordinate system and scales to the viewport; controls and explanatory panels stack vertically. Labels must remain legible without horizontal page scrolling.

## Accessibility and Fallbacks

- Controls use native buttons with visible focus states and ARIA labels.
- Color is reinforced by labels and line styles rather than acting as the only signal.
- `prefers-reduced-motion` disables particle travel and advances through highlighted steps without continuous animation.
- If JavaScript is unavailable, the complete static topology and legend remain visible.

## Verification

1. Parse embedded JavaScript without syntax errors.
2. Verify every scenario button changes the active scenario and step text.
3. Verify play, pause, replay, and speed controls update state.
4. Serve through local HTTP and inspect the desktop and mobile layouts in a real browser.
5. Confirm no overlapping labels, clipped paths, console errors, or external asset requests.

## Out of Scope

- Investment beneficiaries, vendor names, market-share data, or valuation
- Exact cycle-accurate latency simulation
- Live GPU telemetry or external APIs
- Multi-page application scaffolding
