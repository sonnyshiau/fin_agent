# fin_agent Core Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first source-grounded `report/` to Markdown memo pipeline for fin_agent.

**Architecture:** Implement a small Python package with three isolated layers: ingestion, retrieval/evidence, and memo generation/supervision. Each layer has focused files, fixture-based tests, and no dependency on committed report PDFs.

**Tech Stack:** Python 3, pytest, python-dotenv, OpenAI-compatible API client boundary, local JSONL artifacts for chunks and memos.

---

## File Structure

Agent 1 owns ingestion:

- Create `pyproject.toml`
- Create `src/fin_agent/__init__.py`
- Create `src/fin_agent/config.py`
- Create `src/fin_agent/ingestion.py`
- Create `tests/fixtures/sample_report.txt`
- Create `tests/test_ingestion.py`

Agent 2 owns retrieval and evidence:

- Create `src/fin_agent/retrieval.py`
- Create `src/fin_agent/evidence.py`
- Create `tests/test_retrieval.py`
- Create `tests/test_evidence.py`

Agent 3 owns memo generation, flow supervision, and CLI integration:

- Create `src/fin_agent/model_provider.py`
- Create `src/fin_agent/memo.py`
- Create `src/fin_agent/flow_check.py`
- Create `src/fin_agent/cli.py`
- Create `tests/test_memo.py`
- Create `tests/test_flow_check.py`
- Modify `README.md`
- Modify `flow.md` only after verification passes.

All workers must avoid committing `.env`, `report/`, and `outputs/`.

## Shared Data Contracts

Use these dataclasses consistently:

```python
@dataclass(frozen=True)
class SourceDocument:
    source_file: str
    source_type: str
    text: str
    page: int | None = None
    section: str | None = None

@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_file: str
    source_type: str
    text: str
    page: int | None = None
    section: str | None = None

@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
```

## Agent 1: Ingestion

### Task 1: Project Skeleton And TXT Ingestion

**Files:**
- Create: `pyproject.toml`
- Create: `src/fin_agent/__init__.py`
- Create: `src/fin_agent/config.py`
- Create: `src/fin_agent/ingestion.py`
- Create: `tests/fixtures/sample_report.txt`
- Create: `tests/test_ingestion.py`

- [ ] **Step 1: Write fixture**

Create `tests/fixtures/sample_report.txt`:

```text
Marvell 的 AI data center 需求持續成長。
CPO 與 optical interconnect 是下一代 product cycle 重點。
Forward guidance 顯示 networking revenue 有機會上修。
```

- [ ] **Step 2: Write failing tests**

Create `tests/test_ingestion.py`:

```python
from pathlib import Path

from fin_agent.ingestion import Chunk, DocumentLoader, SourceDocument, chunk_document


def test_load_txt_preserves_source_metadata():
    loader = DocumentLoader()
    doc = loader.load_txt(Path("tests/fixtures/sample_report.txt"))
    assert isinstance(doc, SourceDocument)
    assert doc.source_file == "sample_report.txt"
    assert doc.source_type == "txt"
    assert "Marvell" in doc.text
    assert doc.section is None


def test_scan_report_dir_ignores_unknown_extensions(tmp_path):
    (tmp_path / "note.txt").write_text("CPO demand", encoding="utf-8")
    (tmp_path / "ignore.csv").write_text("not supported", encoding="utf-8")
    loader = DocumentLoader()
    docs = loader.scan(tmp_path)
    assert [doc.source_file for doc in docs] == ["note.txt"]


def test_chunk_document_preserves_metadata():
    doc = SourceDocument(
        source_file="sample_report.txt",
        source_type="txt",
        text="A" * 1200,
        section="body",
    )
    chunks = chunk_document(doc, chunk_size=500)
    assert all(isinstance(chunk, Chunk) for chunk in chunks)
    assert chunks[0].chunk_id == "sample_report.txt:0"
    assert chunks[0].source_file == "sample_report.txt"
    assert chunks[0].section == "body"
    assert len(chunks) == 3
```

- [ ] **Step 3: Run tests and verify failure**

Run:

```powershell
python -m pytest tests/test_ingestion.py -v
```

Expected: fails because `fin_agent.ingestion` does not exist.

- [ ] **Step 4: Implement minimal ingestion**

Create `src/fin_agent/ingestion.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceDocument:
    source_file: str
    source_type: str
    text: str
    page: int | None = None
    section: str | None = None


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_file: str
    source_type: str
    text: str
    page: int | None = None
    section: str | None = None


class DocumentLoader:
    def scan(self, report_dir: Path) -> list[SourceDocument]:
        docs: list[SourceDocument] = []
        for path in sorted(report_dir.iterdir()):
            if path.suffix.lower() == ".txt":
                docs.append(self.load_txt(path))
        return docs

    def load_txt(self, path: Path) -> SourceDocument:
        return SourceDocument(
            source_file=path.name,
            source_type="txt",
            text=path.read_text(encoding="utf-8"),
        )


def chunk_document(doc: SourceDocument, chunk_size: int = 1000) -> list[Chunk]:
    chunks: list[Chunk] = []
    for index, start in enumerate(range(0, len(doc.text), chunk_size)):
        text = doc.text[start : start + chunk_size]
        chunks.append(
            Chunk(
                chunk_id=f"{doc.source_file}:{index}",
                source_file=doc.source_file,
                source_type=doc.source_type,
                text=text,
                page=doc.page,
                section=doc.section,
            )
        )
    return chunks
```

Create `src/fin_agent/__init__.py`:

```python
"""fin_agent core package."""
```

Create `src/fin_agent/config.py`:

```python
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str = "gpt-5.5"


def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
    )
```

Create `pyproject.toml`:

```toml
[project]
name = "fin-agent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "pytest>=8.0.0",
  "python-dotenv>=1.0.0",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

- [ ] **Step 5: Run tests and verify pass**

Run:

```powershell
python -m pytest tests/test_ingestion.py -v
```

Expected: 3 passed.

## Agent 2: Retrieval And Evidence Map

### Task 2: Search And Evidence Mapping

**Files:**
- Create: `src/fin_agent/retrieval.py`
- Create: `src/fin_agent/evidence.py`
- Create: `tests/test_retrieval.py`
- Create: `tests/test_evidence.py`

- [ ] **Step 1: Write failing retrieval tests**

Create `tests/test_retrieval.py`:

```python
from fin_agent.ingestion import Chunk
from fin_agent.retrieval import SearchIndex


def test_search_ranks_matching_chunks_first():
    chunks = [
        Chunk("a", "a.txt", "txt", "CPO optical interconnect demand is rising"),
        Chunk("b", "b.txt", "txt", "Consumer weakness continues"),
    ]
    index = SearchIndex(chunks)
    results = index.search("CPO optical", limit=2)
    assert results[0].chunk.chunk_id == "a"
    assert results[0].score > results[1].score


def test_search_returns_empty_for_no_terms():
    index = SearchIndex([])
    assert index.search("MRVL") == []
```

- [ ] **Step 2: Write failing evidence tests**

Create `tests/test_evidence.py`:

```python
from fin_agent.ingestion import Chunk
from fin_agent.retrieval import SearchResult
from fin_agent.evidence import build_evidence_map


def test_evidence_map_extracts_sources_and_missing_fields():
    results = [
        SearchResult(
            chunk=Chunk("a", "mrvl.txt", "txt", "Marvell has AI data center exposure"),
            score=2.0,
        )
    ]
    evidence = build_evidence_map("MRVL", results)
    assert evidence["query"] == "MRVL"
    assert evidence["source_files"] == ["mrvl.txt"]
    assert "valuation" in evidence["missing_fields"]
    assert evidence["confidence"] == "Medium"
```

- [ ] **Step 3: Run tests and verify failure**

Run:

```powershell
python -m pytest tests/test_retrieval.py tests/test_evidence.py -v
```

Expected: fails because modules do not exist.

- [ ] **Step 4: Implement retrieval**

Create `src/fin_agent/retrieval.py`:

```python
from __future__ import annotations

from dataclasses import dataclass

from fin_agent.ingestion import Chunk


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


class SearchIndex:
    def __init__(self, chunks: list[Chunk]) -> None:
        self._chunks = chunks

    def search(self, query: str, limit: int = 8) -> list[SearchResult]:
        terms = [term.lower() for term in query.split() if term.strip()]
        if not terms:
            return []
        results: list[SearchResult] = []
        for chunk in self._chunks:
            text = chunk.text.lower()
            score = sum(text.count(term) for term in terms)
            if score > 0:
                results.append(SearchResult(chunk=chunk, score=float(score)))
            else:
                results.append(SearchResult(chunk=chunk, score=0.0))
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]
```

- [ ] **Step 5: Implement evidence map**

Create `src/fin_agent/evidence.py`:

```python
from __future__ import annotations

from fin_agent.retrieval import SearchResult


REQUIRED_FIELDS = [
    "thesis",
    "product_cycle",
    "financial_quality",
    "valuation",
    "catalyst",
    "risk",
]


def build_evidence_map(query: str, results: list[SearchResult]) -> dict[str, object]:
    source_files = sorted({result.chunk.source_file for result in results if result.score > 0})
    combined_text = " ".join(result.chunk.text.lower() for result in results if result.score > 0)
    missing_fields = [
        field for field in REQUIRED_FIELDS if _field_is_missing(field, combined_text)
    ]
    confidence = "Low"
    if len(source_files) >= 2:
        confidence = "High"
    elif source_files:
        confidence = "Medium"
    return {
        "query": query,
        "source_files": source_files,
        "key_facts": [result.chunk.text for result in results if result.score > 0],
        "missing_fields": missing_fields,
        "confidence": confidence,
        "contradictions": [],
    }


def _field_is_missing(field: str, text: str) -> bool:
    terms = {
        "thesis": ["thesis", "核心", "受惠"],
        "product_cycle": ["product cycle", "ramp", "cycle", "平台"],
        "financial_quality": ["revenue", "margin", "eps", "fcf", "營收", "毛利"],
        "valuation": ["valuation", "pe", "ev/sales", "估值"],
        "catalyst": ["catalyst", "guidance", "上修", "催化"],
        "risk": ["risk", "風險", "下修"],
    }
    return not any(term in text for term in terms[field])
```

- [ ] **Step 6: Run tests and verify pass**

Run:

```powershell
python -m pytest tests/test_retrieval.py tests/test_evidence.py -v
```

Expected: all tests pass.

## Agent 3: Memo Generation, CLI, And Flow Supervisor

### Task 3: Memo Renderer And Flow Check

**Files:**
- Create: `src/fin_agent/model_provider.py`
- Create: `src/fin_agent/memo.py`
- Create: `src/fin_agent/flow_check.py`
- Create: `src/fin_agent/cli.py`
- Create: `tests/test_memo.py`
- Create: `tests/test_flow_check.py`
- Modify: `README.md`

- [ ] **Step 1: Write failing memo tests**

Create `tests/test_memo.py`:

```python
from fin_agent.memo import render_memo


def test_render_memo_contains_required_sections():
    evidence = {
        "query": "CPO",
        "source_files": ["cpo.txt"],
        "key_facts": ["CPO demand is rising"],
        "missing_fields": ["valuation"],
        "confidence": "Medium",
        "contradictions": [],
    }
    memo = render_memo("CPO", evidence, model_summary="CPO thesis summary")
    assert "# fin_agent Memo: CPO" in memo
    assert "## Evidence Map" in memo
    assert "## 核心 Thesis" in memo
    assert "valuation" in memo
    assert "cpo.txt" in memo
```

- [ ] **Step 2: Write failing flow check tests**

Create `tests/test_flow_check.py`:

```python
from pathlib import Path

from fin_agent.flow_check import phase_zero_ready


def test_phase_zero_ready_requires_core_files(tmp_path):
    (tmp_path / "docs/superpowers/specs").mkdir(parents=True)
    (tmp_path / "docs/superpowers/specs/spec.md").write_text("# Spec", encoding="utf-8")
    (tmp_path / "分析框架.md").write_text("# Framework", encoding="utf-8")
    (tmp_path / "tech_investing_product_cycle.md").write_text("# Notes", encoding="utf-8")
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=x", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nreport/\noutputs/\n", encoding="utf-8")
    assert phase_zero_ready(tmp_path) is True


def test_phase_zero_ready_rejects_missing_outputs_ignore(tmp_path):
    (tmp_path / "docs/superpowers/specs").mkdir(parents=True)
    (tmp_path / "docs/superpowers/specs/spec.md").write_text("# Spec", encoding="utf-8")
    (tmp_path / "分析框架.md").write_text("# Framework", encoding="utf-8")
    (tmp_path / "tech_investing_product_cycle.md").write_text("# Notes", encoding="utf-8")
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=x", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nreport/\n", encoding="utf-8")
    assert phase_zero_ready(tmp_path) is False
```

- [ ] **Step 3: Run tests and verify failure**

Run:

```powershell
python -m pytest tests/test_memo.py tests/test_flow_check.py -v
```

Expected: fails because modules do not exist.

- [ ] **Step 4: Implement memo renderer**

Create `src/fin_agent/memo.py`:

```python
from __future__ import annotations


def render_memo(query: str, evidence: dict[str, object], model_summary: str) -> str:
    source_files = evidence.get("source_files", [])
    missing_fields = evidence.get("missing_fields", [])
    key_facts = evidence.get("key_facts", [])
    confidence = evidence.get("confidence", "Low")
    return "\n".join(
        [
            f"# fin_agent Memo: {query}",
            "",
            "## Evidence Map",
            f"- Source files: {', '.join(source_files) if source_files else '缺資料'}",
            f"- Confidence: {confidence}",
            f"- Missing fields: {', '.join(missing_fields) if missing_fields else 'None'}",
            "",
            "## 核心 Thesis",
            model_summary,
            "",
            "## Key Facts",
            *[f"- {fact}" for fact in key_facts],
            "",
            "## 來源引用",
            *[f"- {source}" for source in source_files],
            "",
        ]
    )
```

- [ ] **Step 5: Implement flow checker**

Create `src/fin_agent/flow_check.py`:

```python
from __future__ import annotations

from pathlib import Path


def phase_zero_ready(root: Path) -> bool:
    spec_dir = root / "docs" / "superpowers" / "specs"
    required_files = [
        root / "分析框架.md",
        root / "tech_investing_product_cycle.md",
        root / ".env.example",
        root / ".gitignore",
    ]
    if not spec_dir.exists() or not any(spec_dir.glob("*.md")):
        return False
    if not all(path.exists() for path in required_files):
        return False
    ignore_text = (root / ".gitignore").read_text(encoding="utf-8")
    return all(pattern in ignore_text for pattern in [".env", "report/", "outputs/"])
```

- [ ] **Step 6: Implement model provider placeholder and CLI**

Create `src/fin_agent/model_provider.py`:

```python
from __future__ import annotations


class ModelProvider:
    def summarize(self, prompt: str) -> str:
        raise NotImplementedError


class StaticModelProvider(ModelProvider):
    def __init__(self, response: str) -> None:
        self._response = response

    def summarize(self, prompt: str) -> str:
        return self._response
```

Create `src/fin_agent/cli.py`:

```python
from __future__ import annotations

import argparse
from pathlib import Path

from fin_agent.evidence import build_evidence_map
from fin_agent.ingestion import DocumentLoader, chunk_document
from fin_agent.memo import render_memo
from fin_agent.model_provider import StaticModelProvider
from fin_agent.retrieval import SearchIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--report-dir", default="report")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    loader = DocumentLoader()
    docs = loader.scan(Path(args.report_dir))
    chunks = [chunk for doc in docs for chunk in chunk_document(doc)]
    results = SearchIndex(chunks).search(args.query)
    evidence = build_evidence_map(args.query, results)
    provider = StaticModelProvider("Model generation is not wired yet.")
    memo = render_memo(args.query, evidence, provider.summarize(args.query))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{args.query}-memo.md"
    output_path.write_text(memo, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Update README**

Append to `README.md`:

```markdown

## Local Pipeline

The initial pipeline reads local research files from `report/`, builds a small local search index, creates an evidence map, and writes Markdown memos to `outputs/`.

```powershell
python -m pytest
python -m fin_agent.cli CPO
```

Secrets belong in `.env`; use `.env.example` as the template. Do not commit `.env`, `report/`, or `outputs/`.
```

- [ ] **Step 8: Run tests and verify pass**

Run:

```powershell
python -m pytest tests/test_memo.py tests/test_flow_check.py -v
```

Expected: all tests pass.

