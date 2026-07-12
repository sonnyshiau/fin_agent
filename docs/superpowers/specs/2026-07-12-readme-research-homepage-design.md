# FIN_AGENT README Research Homepage Design

## Goal

Turn the repository README into a polished research homepage that communicates FIN_AGENT's identity, research coverage, methodology, and featured work at a glance. The result must remain reliable in GitHub Markdown on desktop, mobile, light mode, and dark mode.

## Visual Direction

Use the approved **Brand-led Research Homepage** direction.

- Create `docs/assets/fin-agent-readme-hero.svg` as the single signature visual.
- Use a dark graphite-green background with restrained rack, circuit, power-path, and grid linework.
- Display `FIN_AGENT`, `AI Infrastructure Investment Research`, and `Architecture → Supply Chain → Earnings → Valuation`.
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
5. Research workflow from technical architecture through valuation.
6. Full published-pages list, retaining Bloom Energy and Retirement Calculator links.
7. Evidence-discipline section distinguishing official data, company guidance, broker estimates, channel checks, market rumors, and independent inference.

## Markdown Implementation

- Use standard Markdown wherever possible.
- Use a small HTML table only for the three featured research cards because GitHub Markdown has no responsive card primitive.
- Use the local SVG through a relative repository path so the README has no third-party rendering dependency.
- Keep headings shallow and scannable; use one H1 and descriptive H2 headings.
- Preserve all current public URLs exactly.
- Avoid Mermaid in the README because the research workflow is clearer as a compact numbered sequence and renders more consistently across surfaces.

## Acceptance Criteria

- The first viewport shows the FIN_AGENT identity, research positioning, topic coverage, and featured research.
- Every existing page remains linked and every link uses HTTPS.
- The SVG contains no external resources, scripts, animation, or inaccessible low-contrast text.
- The README remains readable without the SVG if image rendering is disabled.
- Markdown passes whitespace checks and renders without broken HTML.
- Only the new SVG, this design document, and README are included in the implementation scope.
