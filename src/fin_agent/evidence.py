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
    matching_results = [result for result in results if result.score > 0]
    source_files = sorted({result.chunk.source_file for result in matching_results})
    combined_text = " ".join(result.chunk.text.lower() for result in matching_results)
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
        "key_facts": [result.chunk.text for result in matching_results],
        "missing_fields": missing_fields,
        "confidence": confidence,
        "contradictions": [],
    }


def _field_is_missing(field: str, text: str) -> bool:
    terms = {
        "thesis": ["thesis", "investment case", "核心", "受惠", "投資"],
        "product_cycle": ["product cycle", "ramp", "cycle", "platform", "平台", "放量", "產品週期"],
        "financial_quality": ["revenue", "margin", "eps", "fcf", "cash flow", "營收", "毛利", "現金流"],
        "valuation": ["valuation", "pe", "p/e", "ev/sales", "multiple", "估值", "本益比"],
        "catalyst": ["catalyst", "guidance", "lead time", "order momentum", "催化", "上修", "交期"],
        "risk": ["risk", "shortage", "allocation", "competition", "風險", "短缺", "競爭"],
    }
    return not any(term in text for term in terms[field])
