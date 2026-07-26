# AI Scale-up and Astera Labs Path — Design Specification

## Objective

Create a new self-contained Traditional Chinese HTML learning dashboard named `ai-scale-up-astera-labs-path.html`. It must explain CPU, DDR, LPDDR, GPU, HBM, Host I/O, CPU–GPU coherence, CXL memory expansion, and GPU scale-up as separate but related system paths. It must then place Astera Labs Leo, Scorpio P-Series, Scorpio X-Series, and Aries products on the correct paths.

The page's single job is to prevent this common category error:

> GPU scale-up is accelerator-to-accelerator communication. It is not the generic CPU-to-HBM or DDR-to-HBM data path.

## Audience and Language

The primary reader is a digital IC engineer and semiconductor investor. Begin with the complete topology, then expose protocol, device, memory, and physical-channel details. Use Traditional Chinese with standard English hardware terms. Keep prose compact and let the diagrams carry the explanation.

The page is an architecture learning tool with a product-strategy overlay, not an investment valuation dashboard.

## Architecture Truth Model

### Component definitions

| Component | System role | Primary attachment |
|---|---|---|
| CPU | Host control, scheduling, data preparation | DDR or LPDDR, PCIe/CXL |
| DDR | Conventional host memory | CPU memory controller and DIMMs |
| LPDDR | Power-efficient CPU or SoC memory | CPU or integrated SoC memory controller |
| GPU or XPU | AI accelerator | Local HBM, host I/O, scale-up ports |
| HBM | Accelerator-local high-bandwidth memory | Accelerator memory controller |
| Scale-up switch | Switches accelerator-to-accelerator traffic | Accelerator scale-up ports |

DDR and LPDDR are normally alternative host-memory implementations. They are not sequential stages between the CPU and HBM. HBM remains a separate physical memory domain local to the GPU or accelerator.

## Canonical Data Paths

The page must present four distinct paths. Only one path is active at a time; all other paths remain visible but visually recessed.

### 1. Host and Model Load Path

```text
NVMe SSD
  → CPU Root Complex ↔ DDR or LPDDR
  → PCIe
  → Aries Retimer, when the channel budget requires it
  → Scorpio P-Series, when fan-out or peer-to-peer switching is required
  → GPU PCIe Endpoint
  → GPU NoC / DMA / Memory Controller
  → GPU-local HBM
```

Purpose: model loading, host-to-device copies, control, storage traffic, and general accelerator I/O.

This is a CPU-to-accelerator path. It must never be labeled GPU scale-up.

### 2. CXL Memory Expansion Path

```text
CPU CXL Root Port
  → Aries Retimer, optional
  → PCIe/CXL fabric, topology-dependent
  → Leo CXL Smart Memory Controller
  → DDR5 memory expansion or pool
```

Purpose: increase host-visible memory capacity, improve memory utilization, or support pooling and sharing.

Leo terminates CXL transactions and controls DDR memory. It does not expand the GPU's local HBM bandwidth and must not be drawn inside the GPU scale-up hot path.

### 3. CPU–GPU Coherent Path

Use a Grace Hopper-style architecture as the explicit example:

```text
CPU ↔ LPDDR5X
  ↕ coherent chip-to-chip interconnect such as NVLink-C2C
GPU ↔ HBM
```

Purpose: allow CPU and GPU to access a shared address space while retaining two distinct physical memory domains and locality characteristics.

This is heterogeneous CPU–GPU coherence. It is not the same thing as a multi-GPU scale-up fabric.

### 4. GPU Scale-up Hot Path

Remote-read request:

```text
GPU 0 Compute / DMA
  → GPU 0 NoC and Scale-up Port
  → NVLink or UALink-class Scale-up Link
  → NVSwitch, Scorpio X-Series, or another compatible Scale-up Switch
  → GPU 1 Scale-up Port and NoC
  → GPU 1 Memory Controller
  → GPU 1 HBM
```

Data response:

```text
GPU 1 HBM
  → GPU 1 Memory Controller and NoC
  → Scale-up Fabric
  → GPU 0 NoC
  → GPU 0 Compute
```

Purpose: GPU-to-GPU remote memory access, collectives, synchronization, expert routing, and other high-bandwidth back-end communication.

CPU, DDR, and LPDDR are outside the default hot path. The page may show them in context, but they must remain visually separated from the active scale-up trace.

## Protocol and Fabric Boundaries

The page must distinguish three connectivity families:

1. **Host I/O and memory attachment:** PCIe and CXL connect processors, accelerators, storage, and memory expansion devices.
2. **Scale-up:** NVLink/NVSwitch represents NVIDIA's proprietary GPU scale-up path. UALink and compatible merchant fabrics represent an open accelerator scale-up path. Scorpio X belongs here.
3. **Scale-out:** Ethernet or InfiniBand connects systems or racks through NICs. It appears only as a boundary marker so users do not confuse it with scale-up.

Memory-semantic access must be described as load/store, DMA, and atomic-capable remote access where the applicable protocol supports those operations. The page must not imply that all scale-up fabrics use identical coherency models.

## Astera Labs Product Placement

### Aries PCIe/CXL Smart DSP Retimer

- Layer: physical/link integrity.
- Placement: inline on PCIe/CXL copper channels when loss, reach, connectors, or topology require retiming.
- Function: equalization, clock/data recovery, signal regeneration, link telemetry, and reach extension.
- Non-function: it does not route transactions, switch endpoints, control DDR, or create GPU scale-up semantics.
- Scale-up caveat: do not place Aries on the Scorpio X path by default. Show a retimer or cable module there only when a documented platform uses a compatible part and the channel budget requires it.

### Leo CXL Smart Memory Controller

- Layer: CXL memory endpoint/controller.
- Placement: between a CXL host/fabric and DDR5 memory.
- Function: memory expansion, pooling, and sharing.
- Non-function: it does not replace HBM and is not a GPU-to-GPU switch.

### Scorpio P-Series

- Layer: PCIe host/front-end fabric switch.
- Placement: between CPU/root ports and mixed PCIe endpoints such as GPUs, NICs, and SSDs.
- Function: fan-out, peer-to-peer traffic, mixed-endpoint connectivity, and configurable PCIe topologies.
- Non-function: it is not the primary homogeneous GPU back-end scale-up fabric.

### Scorpio X-Series

- Layer: accelerator back-end scale-up fabric switch.
- Placement: between GPU or XPU scale-up ports.
- Function: memory-semantic accelerator-to-accelerator communication, high-radix topology, collective acceleration, and single-hop scale-up where supported.
- Non-function: it does not increase local HBM bandwidth or capacity and is not an Ethernet scale-out switch.

## Information Architecture

### 1. Opening Thesis

Open with a direct statement:

> CPU feeds and controls accelerators through the host path. Scale-up lets accelerators communicate with each other without putting the CPU in every hot transfer.

Below the thesis, provide five mode buttons:

- System Overview
- Host / Model Load
- CXL Memory Expansion
- CPU–GPU Coherent
- GPU Scale-up

A sixth Physical Channel mode reveals board, connector, retimer, and cable placement.

### 2. Interactive Signal Plane

The main visual is a persistent system topology, not a set of unrelated slides. Switching modes changes the active lanes and explanatory rail while preserving spatial orientation.

The topology contains:

- NVMe SSD
- CPU root complex and memory controller
- DDR DIMMs and an LPDDR alternative
- PCIe/CXL root port
- Aries retimer position
- Scorpio P-Series fabric position
- Leo with external DDR5 expansion
- Two or more accelerator packages
- Accelerator compute die, NoC/DMA, memory controller, and HBM stacks
- Scorpio X-Series scale-up switch
- NVLink/NVSwitch alternative path
- Scale-out NIC boundary

Each active trace displays request and response direction separately. Text labels identify the traffic type, not merely the protocol name.

### 3. Product Engineering Rail

Selecting a product opens a fixed detail rail with:

- Sits here
- Carries or controls
- Solves this bottleneck
- Does not do
- Attach-rate driver
- Adoption dependency

Product descriptions remain architecture-focused. Avoid unsupported market-share or revenue claims.

### 4. Logical and Physical Layer Toggle

Logical view emphasizes transactions, protocols, address domains, and request/response direction.

Physical view emphasizes lanes, connectors, retimers, cable modules, PCB reach, package links, and switch ports.

This toggle is essential because a retimer and a fabric switch may sit on the same drawn line while performing fundamentally different jobs.

### 5. Fabric Comparison

Provide a compact comparison covering:

- PCIe/CXL Host Path
- NVIDIA NVLink/NVSwitch Scale-up
- UALink/Open Scale-up with Scorpio X
- Ethernet/InfiniBand Scale-out

Columns include participants, semantic model, CPU hot-path involvement, switch role, memory destination, distance/domain, and Astera product exposure.

### 6. Review Summary

End with four reconstruction prompts:

1. Where is CPU-attached memory?
2. Where is accelerator-local memory?
3. Which path is true GPU scale-up?
4. Which Astera product belongs to each layer?

## Visual Direction

### Concept

The page resembles a live signal-integrity and fabric observability console. The design is dense, technical, and diagram-first without resembling a generic SaaS dashboard.

### Token system

- Backplane — `#081018`
- Module — `#101C26`
- Host Blue — `#4CA6DD`
- Scale-up Pink — `#F06CAD`
- Physical Amber — `#F3B45A`
- Memory Jade — `#57D6C0`
- Text — `#E8F0F5`
- Muted — `#92A8B7`

Colors encode architectural layers. Labels, line patterns, and icons provide redundant meaning so color is never the only differentiator.

### Typography

- Display and topology headings: Bahnschrift Condensed or Arial Narrow fallback
- Traditional Chinese body: Microsoft JhengHei or system sans-serif
- Protocol, lane, state, and metric labels: Consolas or monospace fallback

No external fonts are required.

### Signature interaction

The memorable element is a persistent payload that changes route without changing the topology. When the user selects GPU Scale-up, CPU and host memory remain visible but recessed, while request and response packets move only between accelerator memory domains. This makes the architecture distinction perceptible rather than merely stated.

## Motion and Interaction

- Animate only the selected data path.
- Request and response packets use different shapes or dash patterns.
- Hover reveals port or protocol labels; click or keyboard activation pins the detail.
- Product selection updates the engineering rail without moving the topology.
- A playback control pauses animation and steps through each hop.
- Respect `prefers-reduced-motion`; reduced-motion mode uses static path highlighting and numbered hops.
- Pause all animation when the document is hidden.

## Responsive Behavior

- Desktop: topology occupies approximately three quarters of the width; detail rail occupies one quarter.
- Tablet: topology above the detail rail.
- Mobile: convert each path into a vertical stepper. Do not shrink the desktop topology until labels become illegible.
- Fabric comparison may scroll within its own container, but the page itself must not overflow horizontally.

## Technical Architecture

Deliver one standalone HTML file with semantic HTML, inline CSS, inline SVG, and defensive plain JavaScript. No framework, build step, external script, or required image asset.

JavaScript is divided conceptually into:

1. Path mode controller
2. Product selection controller
3. Logical/physical layer controller
4. Animation and step controller
5. Responsive navigation helper

Failure of one controller must not hide essential written content or prevent other sections from rendering.

## Source and Claim Discipline

- Use official product pages and standards bodies for protocol and product positioning.
- Separate product shipping status from roadmap features.
- Mark vendor performance claims as vendor claims.
- Do not claim that Aries is required on every channel.
- Do not claim that CXL is inherently the GPU scale-up fabric.
- Do not imply that LPDDR and HBM are one physical memory pool solely because a unified address space exists.

## Verification

### Static checks

- All four canonical paths and six mode controls exist.
- Leo, Scorpio P, Scorpio X, and Aries have correct placement and non-function statements.
- DDR and LPDDR are presented as host-memory alternatives.
- GPU scale-up excludes CPU/DDR/LPDDR from its default hot trace.
- No placeholder text, external scripts, or external stylesheets.
- All controls have accessible names and state attributes.

### Browser checks

- Serve through localhost.
- Verify desktop near 1440 × 1000 and mobile near 390 × 844.
- Exercise every path mode and product selection.
- Verify request and response direction.
- Verify logical and physical views.
- Verify pause, step, keyboard focus, and reduced-motion behavior.
- Confirm no page-level horizontal overflow and no console errors.

## Completion Criteria

The new HTML is complete when a reader can correctly answer, using the page alone:

- Why CPU-to-HBM is not synonymous with GPU scale-up.
- Where DDR, LPDDR, and HBM physically attach.
- How a remote GPU HBM read traverses the scale-up fabric.
- Why Leo, Scorpio P, Scorpio X, and Aries occupy different architectural layers.

GitHub Pages deployment and README modification are outside the current request unless separately requested.
