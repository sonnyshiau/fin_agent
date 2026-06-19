# fin_agent Core Pipeline Design

## Goal

Build the first usable version of `fin_agent`: a local research pipeline that reads reports from `report/`, applies `分析框架.md`, and produces evidence-backed investment research memos.

The first implementation should prioritize trustworthiness over breadth. It should not behave like a generic summarizer. It must first extract evidence, map sources, identify missing data, then generate a structured memo.

## Scope

In scope:

- Read local PDF and TXT files from `report/`.
- Extract text and preserve source metadata.
- Split documents into searchable chunks.
- Build a local keyword/BM25-style search index.
- Retrieve relevant chunks for a company, ticker, or theme query.
- Generate an evidence map.
- Generate a structured memo using `分析框架.md`.
- Save outputs under `outputs/`.
- Keep `.env`, `report/`, and `outputs/` out of git.

Out of scope for the init version:

- Live market data.
- Automatic news crawling.
- Full DCF modeling.
- Portfolio management.
- Trading recommendations.
- Local model server dependency.
- Vector database as a required dependency.

## Product Shape

The first valuable workflow is:

1. User places reports in `report/`.
2. User asks for a company or theme memo, such as `MRVL`, `CPO`, `ASIC`, or `CoPoS`.
3. fin_agent retrieves relevant source chunks.
4. fin_agent builds an evidence map.
5. fin_agent applies `分析框架.md`.
6. fin_agent writes a Markdown memo to `outputs/`.

A web workbench can wrap this pipeline later. The pipeline should be usable independently first.

## Architecture

### Components

- `DocumentLoader`: scans `report/`, reads TXT files, and extracts text from PDFs.
- `Chunker`: splits extracted text into chunks and attaches metadata.
- `IndexStore`: stores chunks and supports local search.
- `Retriever`: ranks chunks for a query.
- `FrameworkLoader`: loads `分析框架.md`.
- `EvidenceMapper`: produces source coverage, key facts, missing fields, confidence levels, and contradictions.
- `MemoGenerator`: calls the configured OpenAI-compatible model and generates the memo.
- `OutputWriter`: saves generated Markdown reports under `outputs/`.
- `SupervisorChecker`: verifies phase gates in `flow.md` before a phase is marked complete.

### Model Provider

Use OpenAI API first. Configuration comes from `.env`:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.5
```

The code should keep model access behind a provider boundary so another OpenAI-compatible provider can be added later.

## Data Model

Each chunk should retain:

- `chunk_id`
- `source_file`
- `source_type`
- `page` or `section`
- `text`
- `created_at`
- optional tags: company, ticker, theme, product, customer

Each memo should include:

- Evidence map
- One-line conclusion
- Core thesis
- Industry and product cycle
- Financial quality
- Valuation
- Expectation gap
- Bull/Base/Bear
- Catalyst
- Risks and thesis broken indicators
- Follow-up checklist
- Confidence levels and unresolved questions
- Source citations

## Error Handling

- If a file cannot be parsed, mark it as failed with the file name and reason.
- If retrieval finds weak evidence, produce a limited memo and mark missing data.
- If model generation fails, keep the evidence map and show the model error.
- If `.env` is missing, fail with a setup message and point to `.env.example`.
- Never silently omit source metadata.

## Testing Strategy

Use small fixtures rather than full copyrighted reports.

Required test coverage:

- TXT loading preserves source metadata.
- PDF extraction failure is reported clearly.
- Chunking preserves `source_file` and page/section metadata.
- Retrieval returns relevant chunks for known terms.
- Evidence map includes missing-data fields when evidence is absent.
- Memo output contains all required sections.
- Supervisor checks cannot mark a phase complete without required artifacts.

## Implementation Phases

Phase 0: Spec and flow gate.

Phase 1: Local ingestion and chunking.

Phase 2: Search and evidence map.

Phase 3: Memo generation.

Phase 4: Web workbench.

Phase 5: Advanced research workflows, including company comparison, watchlists, and catalyst tracking.

Each phase is gated by `flow.md`.

