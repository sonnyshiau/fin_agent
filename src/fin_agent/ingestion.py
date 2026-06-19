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
