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
