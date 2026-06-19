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
