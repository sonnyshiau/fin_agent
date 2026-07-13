# FIN_AGENT README Research Homepage Design

## Goal

Turn the repository README into a polished research homepage that communicates FIN_AGENT's identity, research coverage, methodology, and featured work at a glance. The result must remain reliable in GitHub Markdown on desktop, mobile, light mode, and dark mode.

## Visual Direction

Use the approved **Brand-led Research Homepage** direction.

- Create `docs/assets/fin-agent-readme-hero.svg` as the single signature visual.
- Use a dark graphite-green background with restrained rack, circuit, power-path, and grid linework.
- Keep `FIN_AGENT` dominant and retain only one supporting line, `AI INFRASTRUCTURE RESEARCH`, so the banner remains legible when GitHub renders it around 309 px wide.
- Use source font sizes of at least 34 px for visible SVG text; remove topic pills and small embedded workflow copy. Preserve the rack, circuit, network, and power-path schematic.
- Keep all important text within the SVG safe area and maintain high contrast in both GitHub themes.
- Do not use gradients, animated SVG, remote image services, decorative badge walls, or marketing-style illustrations.

## README Structure

1. Local SVG brand banner.
2. One-sentence Traditional Chinese research positioning statement.
3. Compact topic labels for Compute, Packaging, Networking, Power, and Cooling.
4. Three featured research links:
   - 800VDC × Kyber Power Industry Research.
   - Vera Rubin / Rubin Ultra Rack Map.
   - AI Supply Chain: CoWoS 2027 Bottleneck.
5. A concise `研究版圖（Research Coverage）` section explaining how Compute, Advanced Packaging, Networking & Optics, Power & Cooling, and AI Factory Infrastructure form one system, then connecting bottlenecks to supply-chain value, fundamentals and EPS, valuation, catalysts, and Thesis Broken conditions.
6. Research workflow from technical architecture through valuation.
7. Full published-pages list, retaining Bloom Energy and Retirement Calculator links.
8. Evidence-discipline section distinguishing official data, company guidance, broker estimates, channel checks, market rumors, and independent inference.

## Markdown Implementation

- Use standard Markdown wherever possible.
- Use an accessible Markdown bullet list for the three featured reports. Do not use the earlier three-column HTML table proposal; bullets scan and reflow better on mobile and remain useful to screen readers.
- Use the local SVG through a relative repository path so the README has no third-party rendering dependency.
- Keep headings shallow and scannable; use one H1 and Traditional Chinese-first H2 headings with English in parentheses: 精選研究, 研究版圖, 研究方法, 已發布研究, and 證據紀律.
- Use Traditional Chinese first for primary workflow labels, with English in parentheses where it improves recognition.
- Preserve all current public URLs exactly.
- Avoid Mermaid in the README because the research workflow is clearer as a compact numbered sequence and renders more consistently across surfaces.

## Acceptance Criteria

- The opening shows the FIN_AGENT identity and research positioning, while the following sections make coverage and featured research easy to scan.
- Every existing page remains linked and every link uses HTTPS.
- The SVG retains its accessible title and description, `1200 × 360` viewBox, and rack/circuit visual. It contains no gradients, scripts, images, filters, animation, or external resource-bearing attributes. The standard SVG namespace is allowed.
- The README remains readable without the SVG if image rendering is disabled.
- Markdown passes whitespace checks and renders without broken HTML.
- Only the SVG, README, this design document, and its implementation plan are included in the completion scope.
