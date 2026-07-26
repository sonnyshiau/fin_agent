# AI Data Center Memory Atlas — Design Specification

## Objective

Create a new self-contained Traditional Chinese HTML learning dashboard named `ai-datacenter-memory-atlas.html`. Its single job is to help a technically experienced reader quickly reconstruct the complete AI data-center memory hierarchy and distinguish hardware memory technologies from software cache concepts.

The page must answer these questions without requiring external context:

- What do CPU cache, 內存, 顯存, HBM, KV cache, NAND, NOR, and SSD each mean?
- Which terms describe a physical memory technology, a system role, a device, or a software data structure?
- During model loading, prefill, and decode, where does data move and why?
- Why does HBM achieve high bandwidth, and what do stacking, TSVs, bus width, and stack count each contribute?

## Audience and Tone

The primary reader is a digital IC engineer and semiconductor investor who understands buses, SRAM/DRAM, packaging, and system architecture. Begin with the complete system and then expose component-level details. Use Traditional Chinese with standard English hardware terms. Keep paragraphs short and make diagrams carry most of the explanation.

The tone is technical and direct, not promotional. Clearly distinguish physical implementation, logical role, and simplified teaching analogy.

## Information Architecture

### 1. Orientation

Open with one sentence:

> AI 運算的資料旅程，是在容量、頻寬、延遲與持久性之間逐層交換。

Directly below it, show four classification labels that remain consistent throughout the page:

- Physical technology: SRAM, DRAM, NAND Flash, NOR Flash
- System role: CPU cache, system memory, VRAM
- Device/package: DIMM, HBM stack, SSD
- Model data structure: KV cache

### 2. Interactive AI Data Center Cross-Section

The main visual is a rack-to-chip data path, not a generic hero illustration:

```text
NVMe SSD / NAND
       ↓ model load
CPU + DDR5 DIMM
       ↓ PCIe / CXL
GPU package + HBM stacks
       ↓ on-package bandwidth
GPU L2 / shared SRAM
       ↓ tile movement
Tensor Core / attention compute
```

Each node is keyboard-focusable and opens a compact explanation containing:

- What it is
- Physical medium
- Data stored there
- Why it exists
- Volatile or non-volatile
- Common misconception

The path has three selectable operating modes:

1. Model load: NAND SSD → host DRAM → GPU HBM
2. Prefill: HBM weights and activations → on-chip SRAM → compute; K/V written to HBM
3. Decode: weights and historical KV read from HBM in tiles → SRAM → compute; new K/V appended

Only the selected path animates. Animation must communicate movement rather than decorate the page.

### 3. Memory Layer Deconstruction

Provide compact panels for:

- CPU L1/L2/L3 cache: SRAM arrays plus tags and control logic
- 內存 / system memory: usually DDR DRAM attached to the CPU memory controller
- 顯存 / VRAM: a functional role, implemented with GDDR, HBM, or shared memory
- HBM: stacked DRAM with TSVs and a wide in-package interface
- KV cache: per-layer K/V tensors produced during autoregressive inference, usually stored in HBM
- NAND Flash: dense, block-erased, non-volatile storage used by SSDs
- NOR Flash: random-readable, executable non-volatile storage used for firmware and boot code
- SSD: NAND packages plus controller, firmware, mapping metadata, ECC, and optional DRAM

Every panel uses no more than one short paragraph plus structured labels.

### 4. HBM Exploded View and Bandwidth Calculator

Draw an original inline SVG exploded view showing:

- Multiple DRAM dies
- TSV columns
- Base/interface die
- Micro-bumps
- Silicon interposer
- GPU or accelerator die
- Package substrate

The diagram must explicitly correct this misconception:

> More dies primarily increase capacity; they do not multiply the external 1024-bit stack interface by the die count.

Calculator inputs:

- Per-pin data rate in Gb/s
- Interface width in bits
- Number of independent stacks

Formula:

```text
Bandwidth (GB/s) = data rate × interface width × stacks ÷ 8
```

Include a preset example of 3.2 Gb/s × 1024-bit × 2 stacks = 819.2 GB/s. Label this as theoretical peak bandwidth and note that achieved bandwidth depends on access patterns, protocol overhead, bank conflicts, thermals, and controller scheduling.

### 5. Comparison Matrix

Use a dense comparison table with columns:

- Term
- Category
- Cell/media
- Volatility
- Typical location
- Optimized for
- AI data-center example

Include SRAM, DDR DRAM, GDDR, HBM, NAND, NOR, SSD, and KV cache. KV cache must be visibly marked as a data structure rather than a memory technology.

### 6. Bandwidth, Latency, Capacity, Persistence

Use one compact visual analogy with four independent axes:

- Bandwidth: data per second
- Latency: time until the first requested data arrives
- Capacity: total data held
- Persistence: whether data survives power loss

Avoid implying that high bandwidth automatically means low latency.

### 7. Review Mode

Include a small, deterministic classification quiz. Questions ask the reader to classify a term as physical technology, system role, device/package, or model data structure. Feedback appears immediately and explains the classification in one sentence. No score tracking beyond the current browser session is required.

End with the compact mental model:

```text
SSD / NAND keeps the model.
DDR stages and serves the host.
HBM feeds the accelerator.
SRAM feeds the compute units.
KV cache remembers prior-token attention states.
```

## Visual Direction

### Design Concept

The page resembles an annotated AI accelerator board and rack service manual: dense, legible, and diagram-first. It must not resemble a marketing landing page or a generic card dashboard.

### Palette

- Backplane — `#0B1118`: primary dark technical background
- Module — `#121D27`: component surfaces
- Trace — `#2B3B49`: dividers and inactive data paths
- SRAM — `#53D6C1`: low-latency on-chip memory
- DRAM — `#5DA9FF`: DDR, GDDR, and HBM family
- Flash — `#F2B45B`: NAND, NOR, and persistent storage
- Compute — `#E879A9`: compute and active attention operations
- Text — `#E8EEF2`; secondary text — `#92A2AE`

Colors encode memory families consistently. They are not decorative gradients.

### Typography

- Display: `Arial Narrow`, `Roboto Condensed`, or system condensed fallback for architectural headings
- Body: `Noto Sans TC`, `Microsoft JhengHei`, or system sans-serif
- Data and labels: `Consolas`, `IBM Plex Mono`, or monospace fallback

Avoid externally loaded font files so the artifact remains self-contained and reliable offline.

### Layout

- Desktop: 12-column grid with the main cross-section occupying 8–9 columns and an explanation rail occupying 3–4 columns
- Tablet: cross-section above the explanation rail
- Mobile: vertical data path, horizontally scrollable comparison table with an explicit scroll affordance
- Maximum content width: approximately 1280 px
- Compact spacing and thin dividers; limited border radius

### Signature Element

The memorable element is a rack-to-transistor “zoom path.” Selecting a stage visually narrows the system from storage device to package to on-chip SRAM tile, while preserving the same highlighted data payload. This embodies the subject rather than adding decoration.

## Image and Source Strategy

The explanatory diagrams must be original inline SVG so the file works offline and can precisely label TSVs, interposer links, cache hierarchy, and data paths.

Use web research for factual verification and visual reference. At most two externally sourced official images may be embedded only if they materially improve recognition of a real package or module. If used:

- Prefer manufacturer or standards-body sources
- Show a visible source label and direct link
- Provide meaningful alt text
- Do not depend on the image for essential explanation
- Keep a diagram fallback so the page remains understandable if an external image fails

## Interaction and Accessibility

- All interactive nodes use native buttons or keyboard-operable elements
- Visible `:focus-visible` treatment
- `aria-pressed`, `aria-live`, and descriptive labels where appropriate
- No information conveyed by color alone
- Respect `prefers-reduced-motion`
- Pause movement when the page is not visible
- JavaScript failure leaves all essential written content visible
- Include `<link rel="icon" href="data:,">` to avoid an external favicon request

## Technical Architecture

Deliver one HTML file containing:

- Semantic HTML
- Inline CSS
- Inline SVG diagrams
- Plain JavaScript with no framework or build step
- No required external runtime assets

JavaScript is divided conceptually into four isolated controllers:

1. Data-path scenario controller
2. Component detail controller
3. HBM calculator
4. Review quiz

Each controller initializes defensively and must not prevent other sections from working if one target element is unavailable.

## Verification

### Static contract checks

- Required title, section markers, concepts, and formula exist
- No placeholder text
- No external scripts or stylesheets
- Inline SVG has accessible titles or labels
- All buttons have accessible names

### Browser checks

- Serve through localhost rather than `file://`
- Verify desktop at approximately 1440 × 1000
- Verify mobile at approximately 390 × 844
- Exercise all three data-path scenarios
- Exercise component selection, calculator, and quiz
- Confirm no horizontal page overflow; table-local scrolling is allowed
- Confirm keyboard focus order and visible focus
- Confirm reduced-motion behavior
- Check console for errors and failed required resources

### Completion criteria

The artifact is complete when the standalone HTML opens locally, all core concepts are represented accurately, interactions work by mouse and keyboard, and desktop/mobile browser checks pass. Publication to GitHub Pages is outside the current request.

## Explicit Non-Goals

- No investment analysis or vendor scorecard
- No live hardware pricing or market-share data
- No user accounts, persistence, or backend
- No detailed DRAM timing tutorial beyond what supports the hierarchy
- No exhaustive coverage of every HBM generation
- No GitHub Pages deployment unless separately requested
