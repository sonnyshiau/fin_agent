# MRVL FY27-FY29 Valuation Dashboard — Design Specification

## Objective

Create two self-contained Traditional Chinese HTML investment-research artifacts for Marvell Technology (MRVL):

1. A local full-evidence edition that preserves the detailed broker cross-check, assumption disagreements, and evidence classification.
2. A sanitized public edition suitable for GitHub Pages that uses public sources, anonymized estimate ranges, and original analysis without reproducing restricted broker content.

Both editions must use the same valuation assumptions and calculation logic so their financial conclusions cannot drift apart.

## Deliverables

- Local full edition: `outputs/mrvl-valuation-full.html`
- Public edition: `mrvl-valuation/index.html` in the existing `gh-pages` worktree
- Public URL: `https://sonnyshiau.github.io/fin_agent/mrvl-valuation/`
- Runtime: modern desktop and mobile browsers without a build step
- Packaging: all HTML, CSS, SVG, data, and JavaScript embedded in each file
- Language: Traditional Chinese with standard English financial and semiconductor terminology

## Research Scope

The analysis covers:

- Current price and the drawdown from the recent high
- FY27, FY28, and FY29 revenue, margin, EPS, and valuation
- Marvell's data-center semiconductor TAM and revenue-capture assumptions
- Custom XPU, XPU-attach silicon, CXL, DPU, switching, DCI, 800G/1.6T DSP, TIA/driver, NPO/CPO, and Celestial AI
- Management guidance versus public consensus and aggressive sell-side scenarios
- Bull, Base, and Bear cases
- Catalysts, key risks, and thesis-broken conditions

The report must distinguish confirmed facts, management statements, sell-side estimates, supply-chain checks, market claims, and original inference. Missing data must remain marked as missing.

## Shared Evidence and Valuation Model

The two editions derive from one logical evidence and valuation model. The model contains:

- Source identity and source type
- Publication or observation date
- Claim or numerical input
- Fiscal period
- Evidence classification
- Confidence level: High, Medium, or Low
- Public-safe summary
- Restricted internal detail when applicable
- Scenario applicability: Bull, Base, Bear, or all

The local edition may expose broker names, individual estimates, report dates, and detailed contradictions. The public edition may only expose public sources, anonymized estimate ranges, and original calculations.

## Valuation Methodology

Primary valuation uses non-GAAP forward EPS and a scenario-appropriate forward P/E multiple. EV/Sales provides a secondary reasonableness check because Marvell's margin structure and acquisition-related dilution can make a single P/E output look more precise than the underlying assumptions justify.

### FY27 Anchor

- Revenue anchor: management outlook of approximately $11.5 billion
- EPS anchor: approximately $4.0, cross-checked against current public consensus and quarterly guidance
- The model must reconcile Q1 actual results, Q2 guidance, and the sequential growth required in Q3 and Q4

### FY28 Anchor

- Base revenue anchor: management outlook of approximately $16.5 billion
- Base EPS anchor: current public consensus near $6.18, subject to refresh immediately before artifact generation
- Aggressive reference: approximately $19.66 billion revenue and $7.57 EPS from a restricted broker scenario; the public edition must describe this only as an anonymized aggressive case

### FY29 Derivation

FY29 is derived rather than copied from one target-price report. Revenue growth, product mix, gross margin, operating leverage, tax rate, and diluted share count must be explicit scenario inputs. The aggressive $14 EPS estimate is treated as a Bull reference point, not consensus.

### Target Price

Each scenario calculates:

`FY29 non-GAAP EPS × selected P/E multiple = scenario target price`

The dashboard must also show upside or downside from the refreshed market price and identify which combination of FY29 EPS and P/E is implied by the current share price.

### CXL Treatment

The model must keep two opportunities separate:

1. XConn's standalone PCIe/CXL switch products, for which Marvell publicly indicated approximately $100 million of FY28 revenue.
2. Customer-specific CXL/DPU and other XPU-attach silicon, which could have substantially greater content value but currently has lower evidence confidence.

CXL must not be presented as a near-term multi-billion-dollar confirmed revenue stream. It is an option-value thesis whose importance rises only if attach content, design wins, and volume deployment are independently verified.

## Page Architecture

The report follows this order:

1. Header with report date, current-price context, one-sentence conclusion, and confidence label
2. Thesis strip: investment thesis, why now, and key risk
3. Executive metrics: current price, FY27 P/E, FY28 P/E, and Base target return
4. Drawdown valuation: what the recent decline removed and what remains priced in
5. Company essence and supply-chain position
6. FY27-FY29 financial model
7. TAM and revenue-capture framework
8. Bull/Base/Bear interactive scenario framework
9. Valuation sensitivity matrix
10. Priced-in versus not-yet-priced matrix
11. CXL and XPU-attach deep dive
12. Product-cycle and catalyst timeline
13. Risks and thesis-broken indicators
14. Evidence ledger, methodology, data date, and disclaimer

## Visual Design

Use the repository's established research-dashboard style:

- Soft gray-green background and white surfaces
- Dark charcoal text with restrained blue, green, amber, and red semantic accents
- Thin dividers, small radii, compact cards, and readable tables
- Page width around 1160 pixels with mobile gutters
- Chinese-friendly font stack using Noto Sans TC, Microsoft JhengHei, PingFang TC, Arial, and sans-serif
- One H1 and clear analytical H2 headings
- No decorative gradients, oversized marketing copy, stock photography, floating blobs, or ornamental hero graphics

Colors must communicate meaning: positive or Bull in green, Base or watch items in blue/amber, and Bear or thesis risk in red.

## Interactive Components

### Scenario Switcher

Bull, Base, and Bear controls update:

- FY27-FY29 revenue
- Revenue growth
- Gross and operating margins
- EPS
- Valuation multiple
- Target price
- Upside or downside
- Scenario assumptions and trigger conditions

The initial state is Base.

### Valuation Sensitivity Matrix

Rows represent P/E multiples and columns represent FY29 EPS values. Cells display implied share prices. The matrix highlights:

- Current price
- Base case
- Restricted aggressive reference in the local edition
- An anonymized aggressive boundary in the public edition

### TAM Capture Framework

Show the relationship among:

- Approximately $94 billion CY28 data-center semiconductor TAM
- Approximately $55.4 billion custom accelerated-compute devices
- Approximately $40.8 billion custom XPU TAM
- Approximately $14.6 billion implied XPU-attach TAM
- Marvell FY28 revenue and scenario-specific data-center revenue

The visualization must state that TAM is not revenue and that categories may not map perfectly to Marvell's reported segments.

### Expectation-Gap Bridge

Bridge management's FY28 revenue outlook to Base and Bull estimates. Each increment must be labeled with its assumed source, such as:

- Custom program ramps
- Scale-out optics and switching
- Scale-up optics
- DCI modules
- XPU-attach silicon
- Celestial AI
- CXL/PCIe switching

The bridge must not imply that all opportunities are additive without overlap.

### Not-Yet-Priced Matrix

Compare custom XPU, XPU attach, CXL, scale-up switching, NPO/CPO, DCI, and 1.6T optics by:

- Evidence confidence
- Expected materiality
- Earliest meaningful revenue period
- Main validation milestone
- Risk of double counting

## Public Sanitization Rules

The public edition must not contain:

- Broker PDF files or Google Drive links
- Broker report excerpts or copied charts
- Analyst names or contact information
- Restricted report page images
- Language implying that confidential checks are confirmed company facts

Restricted numerical views may appear only as anonymized ranges or scenario boundaries. Every public claim must be independently supportable through company filings, investor materials, official product announcements, or publicly accessible market-data sources.

Run a case-insensitive sensitive-content scan before publication for broker names, Drive URLs, analyst email addresses, and known restricted report titles.

## Responsive and Accessible Behavior

- Desktop uses multi-column metric, scenario, and comparison grids.
- Tablet and mobile stack into one column.
- Wide financial tables and sensitivity matrices scroll horizontally within their panels rather than causing page-level overflow.
- Native buttons provide visible focus states and ARIA pressed-state labels.
- Color is reinforced with text labels and symbols.
- `prefers-reduced-motion` removes non-essential transitions.
- With JavaScript disabled, the Base scenario, core financial table, conclusion, and risk section remain readable.

## Data Refresh and Error Handling

- Market price, market capitalization, public consensus, and analyst price-target ranges must be refreshed immediately before final generation.
- The page displays an explicit data-as-of timestamp.
- Missing or unavailable values display `N/A`; they are never silently estimated.
- Scenario calculations reject non-finite or negative inputs.
- If a public market-data source is unavailable, the artifact uses the last verified observation and labels its date rather than presenting it as live.

## Verification

1. Verify FY27 quarterly reconciliation against the full-year revenue and EPS assumptions.
2. Verify FY28 and FY29 revenue, margin, EPS, target-price, and return calculations for all scenarios.
3. Verify the sensitivity matrix against independent spot calculations.
4. Parse embedded JavaScript without syntax errors.
5. Verify all scenario controls update every dependent field and accessible state.
6. Verify no horizontal page overflow at desktop, tablet, and mobile widths.
7. Verify the Base analysis remains readable with JavaScript disabled.
8. Run the public sensitive-content scan and confirm no restricted source names, links, excerpts, or analyst details remain.
9. Serve both files through local HTTP and inspect them in a real browser.
10. Publish only the sanitized version from the existing `gh-pages` worktree.
11. Confirm the Pages deployment succeeds and `https://sonnyshiau.github.io/fin_agent/mrvl-valuation/` returns HTTP 200.

## Out of Scope

- Live brokerage trading or portfolio actions
- A continuously updating quote feed
- Reproduction or public distribution of broker research
- Exact customer identities when they are not publicly confirmed
- Treating supply-chain estimates as company guidance
- A multi-page web application or backend service
- Automated investment recommendations personalized to position size or cost basis

