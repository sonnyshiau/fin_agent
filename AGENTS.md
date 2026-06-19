# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains source materials for a fundamental-analysis AI agent.

- `分析框架.txt`: primary analysis framework and checklist for company research.
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
- `python src/main.py --input report --framework 分析框架.txt`: run a local analysis workflow.
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
