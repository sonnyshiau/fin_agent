# FIN_AGENT README Research Homepage Implementation Plan

> **For agentic workers:** Implement in an isolated worktree and validate each completion claim with fresh evidence.

**Goal:** Finish the GitHub-native FIN_AGENT research homepage with a complete research map, Chinese-first information hierarchy, and a mobile-readable banner.

**Architecture:** Use one repository-owned static SVG as the signature visual. Keep the README in standard Markdown, including an accessible bullet list for featured reports, with no third-party rendering dependency.

**Tech Stack:** GitHub Flavored Markdown, static SVG, PowerShell, Python XML parsing, pytest.

---

## File Map

- Modify `README.md`: add research coverage and Chinese-first headings and workflow labels.
- Modify `docs/assets/fin-agent-readme-hero.svg`: simplify embedded copy for mobile readability while preserving the technical schematic.
- Modify `docs/superpowers/specs/2026-07-12-readme-research-homepage-design.md`: formalize accessibility and content decisions.
- Modify this plan to reflect the completion work and actual verification state.
- Do not modify application source or unrelated research assets.

### Task 1: Confirm the completion baseline

- [x] **Step 1: Confirm the worktree starts on `codex/readme-completion` at live remote baseline `7bad96f`.**
- [x] **Step 2: Confirm README already contains all five public URLs and uses Markdown bullets for the three featured links.**
- [x] **Step 3: Run a focused requirement validator before editing and observe expected failures for Chinese-first headings, Research Coverage, Chinese-first workflow labels, and small SVG text.**

### Task 2: Complete the README information architecture

- [x] **Step 1: Rename major H2 headings to Traditional Chinese first, with English in parentheses.**
- [x] **Step 2: Add `研究版圖（Research Coverage）` and explain the system path from compute through packaging, networking, power/cooling, and AI factory infrastructure.**
- [x] **Step 3: Connect architectural bottlenecks to supply-chain value, fundamentals and EPS, valuation, catalysts, and Thesis Broken conditions.**
- [x] **Step 4: Make workflow labels Chinese first and preserve the five exact public URLs plus the three featured links.**

### Task 3: Improve the mobile banner

- [x] **Step 1: Preserve the `1200 × 360` accessible SVG shell and rack/circuit visual.**
- [x] **Step 2: Remove topic pills and small workflow copy; retain only dominant `FIN_AGENT` and one supporting line at source font sizes of at least 34 px.**
- [x] **Step 3: Keep the SVG free of gradients, scripts, images, filters, animation, and external resource-bearing attributes or elements. Allow the standard `xmlns="http://www.w3.org/2000/svg"` declaration.**

### Task 4: Synchronize documentation decisions

- [x] **Step 1: Replace the earlier featured-report HTML table direction with accessible Markdown bullets.**
- [x] **Step 2: Document Chinese-first headings, the new Research Coverage section, and the simplified mobile banner.**
- [x] **Step 3: Correct SVG validation so it permits the standard namespace and checks resource-bearing attributes and unsafe elements instead.**

### Task 5: Verify and commit

- [x] **Step 1: Run the focused Python validator for headings, coverage terms, exact URLs, bullet-list structure, SVG accessibility, safety, and font sizes.** Passed with five ordered headings, the exact five-URL set, three featured bullets, two visible SVG text nodes, and a 36 px minimum source font size.
- [x] **Step 2: Run `git diff --check`.** Passed with no whitespace errors; Git emitted only line-ending conversion notices.
- [x] **Step 3: Run `python -m pytest` and record the actual result.** Passed: 10 tests in 0.07 seconds.
- [x] **Step 4: Self-review the full diff and confirm only the four allowed files changed.** Confirmed; corrected the design document's section order during review.
- [x] **Step 5: Commit only the four allowed files with an imperative commit message.** Committed the four-file scope as `Complete README research homepage`; no unrelated file was staged.
