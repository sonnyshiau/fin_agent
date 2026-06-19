# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains source materials for a fundamental-analysis AI agent.

- `分析框架.md`: primary analysis framework and checklist for company research.
- `report/`: input research materials, including PDFs and short text notes.
- `AGENTS.md`: contributor and agent operating guide.

When implementation code is added, keep it separate from raw research assets. Recommended future layout:

- `src/`: agent logic, document parsing, prompt templates, and report generation.
- `tests/`: unit and integration tests.
- `docs/`: design notes, specifications, and generated documentation.
- `outputs/`: generated analysis reports; avoid committing large generated files unless needed.

## Build, Test, and Development Commands

There are no build or test commands yet because the repository has not been initialized as an application. Once code is added, document exact commands here. Suggested examples:

- `python -m pytest`: run Python tests.
- `python src/main.py --input report --framework 分析框架.md`: run a local analysis workflow.
- `ruff check src tests`: lint Python code, if Ruff is adopted.

Prefer commands that work from the repository root.

## Coding Style & Naming Conventions

Use clear, small modules with single responsibilities: parsing, extraction, scoring, and report writing should be separate. Prefer UTF-8 for all text files because the project includes Chinese-language materials. Use descriptive file names such as `pdf_parser.py`, `framework_loader.py`, or `fundamental_report.md`.

For generated reports, use date or ticker prefixes where helpful, for example `2026-06-19-MRVL-analysis.md`.

## Testing Guidelines

Add tests alongside implementation. Cover document parsing, framework mapping, output schema validation, and missing-data behavior. Test fixtures should be small excerpts, not full copyrighted reports. Name tests by behavior, for example `test_extracts_revenue_growth_from_report_text`.

## Commit & Pull Request Guidelines

This directory is not currently a git repository, so no commit history conventions exist yet. Once git is initialized, use concise imperative commit messages, such as `Add PDF extraction pipeline` or `Document report output schema`.

Pull requests should include a short summary, changed files or modules, test results, and sample output when report behavior changes.

## Agent-Specific Instructions

Treat `report/` files as source evidence. Do not invent financial figures. When data is unavailable, mark it as missing instead of estimating. Separate facts from interpretation, and cite the source document name in generated analysis.

## Tech Investment Research Heuristics

For technology-sector research, prioritize product-cycle analysis over reacting to already-public news. Tech investors are often underwriting changes in product cycles, especially when new technology reshuffles supply chains and changes where value accrues.

When analyzing an AI hardware or semiconductor product cycle, explicitly ask:

- Which components or supply-chain steps have rising content value?
- Which parts of the chain are most supply constrained?
- Which vendors have won design slots or appear positioned for design wins?
- When does the new platform begin volume ramp?
- How does the next-generation design differ from the current generation?
- Which component categories benefit or lose from those design changes?

Use Vera Rubin, its related AI hardware supply chain, and later-generation platforms such as Feynman as examples of the kind of forward product-cycle work expected. A strong tech investor should try to maintain 12-18 months of visibility on major product cycles. This visibility will not be perfect; specifications, timing, allocations, and demand can change. Maintain the view through repeated channel checks.

Do not treat earnings calls, company announcements, or mainstream news as early information. By the time these appear, the information is often already stale for specialist investors. Good channel checks may surface supply-chain changes 6-9 months before they become obvious to the broader market.

For shorter-term trading analysis, identify catalysts. High-frequency pricing, lead-time changes, order momentum, supply shortages, and allocation signals can all serve as catalysts. If no direct pricing signal exists, reason from the question: "What might the news be writing 2-3 months from now?" Use this to infer likely narratives, data points, or events that could cause repricing.
