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
