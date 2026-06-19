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
            results.append(SearchResult(chunk=chunk, score=float(score)))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]
