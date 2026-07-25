# Crusoe Research Dashboard Design

## Objective

Create a self-contained Chinese HTML research dashboard that helps a technically literate semiconductor investor understand what Crusoe is, how it converts energy into AI compute, why its vertical integration matters, and where the business carries upside and risk.

The page has one job: make Crusoe's position in the AI infrastructure stack understandable within the first viewport, then support progressively deeper reading without turning into a generic company profile.

## Audience

The primary reader understands semiconductors, servers, high-speed networking, data centers, and investment analysis. The page should establish the complete architecture before discussing individual components, financing, or valuation implications.

## Content Scope

The dashboard will synthesize the previously discussed material into these sections:

1. One-sentence definition of Crusoe.
2. Energy-to-Intelligence system map.
3. Five-layer vertical integration model.
4. Transformation timeline from flare-gas computing to AI factories.
5. Data-center development and Crusoe Cloud business models.
6. Competitive positioning and sources of differentiation.
7. Key disclosed facts, including Abilene, funding, and energy pipeline.
8. Investment interpretation: what matters, upside, downside, and final judgment.
9. Evidence-quality note distinguishing company disclosures from interpretation.

The dashboard will not add unsupported revenue, profitability, utilization, customer concentration, or valuation estimates. Company-stated figures will be labeled as such.

## Information Architecture

### First viewport

The first viewport will answer three questions immediately:

- What is Crusoe?
- What does it sell?
- Why is it different from a normal GPU cloud?

It will contain:

- A compact title and one-sentence conclusion.
- A short classification: energy developer + AI data-center builder + GPU cloud.
- The Energy-to-Intelligence pipeline as the primary visual.
- A compact status note identifying Crusoe as a private company.

### Main reading flow

The main column follows this order:

1. System map
2. Company transformation
3. Revenue engines
4. Moat and competitive position
5. Key facts
6. Investment interpretation

The order moves from physical architecture to company history and then to financial meaning. It avoids opening with funding numbers before the reader understands the business.

### Persistent context rail

On wide screens, a narrow right rail shows the five vertical-integration layers:

1. Energy
2. Data center
3. Compute
4. Cloud software
5. Completed AI work

As the reader enters a corresponding section, the active layer changes. On mobile, the rail becomes a compact horizontal progress strip and does not obscure content.

## Signature Visual: Energy-to-Intelligence Pipeline

The page's memorable element is a technical pipeline showing:

`Energy → Power delivery and cooling → GPU/HBM/network → Crusoe Cloud → Effective tokens and completed tasks`

Each stage explains:

- The physical or software function.
- Crusoe's role.
- The primary bottleneck.
- The business value created.

The visual should resemble an engineering system path rather than a marketing funnel. Thin routed lines, labeled interfaces, directional flow, and small operational annotations will encode the architecture. Decorative glows, floating spheres, and generic AI imagery are prohibited.

## Visual Direction

### Product feel

The page should feel like an AI-factory control schematic crossed with an institutional investment brief: technical, dense, calm, and deliberate. It should not resemble a consumer landing page or a generic SaaS dashboard.

### Color tokens

- `--canvas: #0B1116` — deep graphite-blue page background.
- `--surface: #111A21` — primary information surface.
- `--surface-raised: #17232B` — raised or active surface.
- `--ink: #E8F0F2` — primary text.
- `--muted: #8FA2AA` — supporting text.
- `--line: #293942` — structural rules.
- `--energy: #F2A541` — power, heat, and infrastructure.
- `--compute: #58B7C4` — silicon, network, and cloud.
- `--output: #7DCB9D` — useful output and completed work.
- `--risk: #E2746B` — downside and thesis risk.

Color must encode system roles. Orange is not general decoration; it represents energy and thermal infrastructure. Teal represents compute movement. Green is reserved for completed work or positive output.

### Typography

- Chinese body and navigation: `"Noto Sans TC"`, `"Microsoft JhengHei"`, system sans-serif.
- English headings and numeric labels: `"Arial Narrow"`, `"Roboto Condensed"`, `"Segoe UI"`, sans-serif.
- Technical annotations: `"Cascadia Mono"`, `"SFMono-Regular"`, monospace.

The page must remain usable without web-font downloads. Numeric values use tabular figures where supported.

### Layout

- Maximum reading width: approximately 1440 px.
- Desktop: 12-column grid with a 9-column main area and 3-column context rail.
- Tablet: single main column with a top progress strip.
- Mobile: one column, no horizontal scrolling, pipeline stages stack vertically.
- Section spacing is compact but breathable; structural rules replace unnecessary cards.

### Components

- System pipeline nodes with functional labels.
- Comparison bands for "Crusoe is / is not".
- Two-column business-model comparison.
- Transformation timeline with only meaningful dated transitions.
- Competitive-position matrix.
- Fact ledger with source-type labels.
- Upside/downside split panel.
- Final judgment block.

Cards will be used only when content needs an independent boundary. Repeating identical rounded cards for every fact is prohibited.

## Content Model

### Confirmed or company-disclosed facts

These will use a visible source-type label:

- Private-company status.
- Historical Digital Flare Mitigation business.
- Exit from Bitcoin mining.
- Abilene data-center disclosures.
- Series D and Series E financing disclosures.
- Company-disclosed energy pipeline and bookings growth.

### Interpretation

These will be explicitly labeled as analysis:

- Crusoe resembles an energy-enabled CoreWeave plus data-center developer.
- Power acquisition and execution are more important than proprietary silicon.
- The business may benefit as the bottleneck shifts from GPU availability to energized capacity.
- Capital intensity, customer concentration, GPU depreciation, and construction execution are central risks.

### Missing data

The page will state that public information is insufficient to verify:

- Revenue and profitability.
- Cloud utilization.
- Customer concentration.
- Project-level returns.
- Normalized free cash flow.
- Comparable cost per token under controlled conditions.

## Interaction and Motion

- On initial load, the Energy-to-Intelligence route draws once from energy to output.
- Section entry uses short opacity and vertical-position transitions.
- Pipeline nodes expose a concise explanation on hover and keyboard focus.
- The persistent context rail updates using section intersection state.
- Motion duration stays between 180 ms and 500 ms.
- `prefers-reduced-motion: reduce` disables route drawing and entrance movement while preserving all content.
- No continuous ambient animation.

The page must remain fully understandable if JavaScript is disabled; JavaScript only enhances progress state and motion.

## Accessibility

- Semantic headings and landmark elements.
- Minimum WCAG AA text contrast.
- Visible keyboard focus.
- No information encoded by color alone.
- Pipeline stages use text labels and ordered structure.
- Interactive explanations are accessible by keyboard and touch.
- Mobile tap targets are at least 44 px where controls exist.

## Technical Architecture

Deliver one standalone HTML file with:

- Semantic HTML.
- Embedded CSS.
- Minimal embedded vanilla JavaScript.
- No build step.
- No framework dependency.
- No external image dependency.
- No data collection or network calls.

The proposed output path is:

`C:\Users\User\Desktop\fin_agent\crusoe-ai-factory-dashboard.html`

## Verification

The implementation is complete only after:

1. Opening successfully as a local file.
2. Verifying the first viewport at desktop size.
3. Verifying the stacked pipeline at mobile size.
4. Checking for text overflow, clipped labels, and horizontal scrolling.
5. Testing keyboard focus on interactive elements.
6. Testing reduced-motion behavior.
7. Confirming the page works without external network resources.
8. Confirming all material figures carry an evidence-quality label.
9. Reviewing a rendered screenshot for hierarchy and visual balance.

## Explicit Non-Goals

- No live market data.
- No Crusoe valuation model.
- No account-specific investment recommendation.
- No comparison requiring unsupported competitor financial data.
- No GitHub Pages deployment unless separately requested.
- No modification of existing dashboards or unrelated repository files.
