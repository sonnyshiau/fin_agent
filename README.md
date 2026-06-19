# fin_agent

`fin_agent` is a local research pipeline for turning private research reports into structured, source-grounded investment memos.

The project is designed around two local knowledge files:

- `分析框架.md`: the main fundamental-analysis framework used to structure memos.
- `tech_investing_product_cycle.md`: product-cycle and catalyst heuristics for technology investing.

Raw research reports live in `report/` and are intentionally ignored by git.

## Current Status

Implemented:

- TXT report ingestion
- Text chunking with source metadata
- Local keyword search
- Evidence map generation
- Markdown memo rendering
- Basic CLI
- Flow gate checks in `flow.md`

Not implemented yet:

- PDF text extraction
- Real OpenAI API memo generation
- Web UI
- Vector search
- Live market data

## Setup

From the repository root:

```powershell
python -m pytest
```

Optional API config lives in `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-5.5
```

Do not commit `.env`, `report/`, or `outputs/`.

## Add Reports

Put local research files under:

```text
report/
```

Current pipeline supports `.txt` files. PDF files can stay in `report/`, but PDF parsing is a later phase.

Example TXT content:

```text
Marvell 的 AI data center 需求持續成長。
CPO 與 optical interconnect 是下一代 product cycle 重點。
Forward guidance 顯示 networking revenue 有機會上修。
```

## Run A Memo

Run a local query:

```powershell
$env:PYTHONPATH="src"
python -m fin_agent.cli CoPoS
```

The CLI will:

1. Scan `report/`
2. Load supported TXT files
3. Split text into chunks
4. Search for `CoPoS`
5. Build an evidence map
6. Write a Markdown memo to `outputs/CoPoS-memo.md`

Current memo generation uses a placeholder model response:

```text
Model generation is not wired yet.
```

The evidence map and source citations are still useful for validating retrieval.

## Run Tests

```powershell
python -m pytest -v
```

Expected current result:

```text
10 passed
```

## Flow Gates

Use `flow.md` to track phase completion.

Rules:

- Do not check a phase until all deliverables exist.
- Do not check a phase unless tests or manual verification passed.
- Do not check a phase if `.env`, `report/`, or `outputs/` are staged.

Check Phase 0 readiness:

```powershell
$env:PYTHONPATH="src"
python -c "from pathlib import Path; from fin_agent.flow_check import phase_zero_ready; print(phase_zero_ready(Path('.')))"
```

Expected:

```text
True
```

## Suggested Next Phase

The next useful milestone is Phase 1 completion:

- Add PDF extraction
- Preserve page metadata
- Add fixture tests for PDF parse success or clear parse failure
- Update `flow.md` only after verification passes
