from __future__ import annotations


def render_memo(query: str, evidence: dict[str, object], model_summary: str) -> str:
    source_files = _string_list(evidence.get("source_files", []))
    missing_fields = _string_list(evidence.get("missing_fields", []))
    key_facts = _string_list(evidence.get("key_facts", []))
    contradictions = _string_list(evidence.get("contradictions", []))
    confidence = str(evidence.get("confidence", "Low"))

    return "\n".join(
        [
            f"# fin_agent Memo: {query}",
            "",
            "## Evidence Map",
            f"- Source files: {', '.join(source_files) if source_files else 'Missing'}",
            f"- Confidence: {confidence}",
            f"- Missing fields: {', '.join(missing_fields) if missing_fields else 'None'}",
            f"- Contradictions: {', '.join(contradictions) if contradictions else 'None'}",
            "",
            "## 核心 Thesis",
            model_summary,
            "",
            "## Key Facts",
            *(_bullet_lines(key_facts) if key_facts else ["- Missing"]),
            "",
            "## Sources",
            *(_bullet_lines(source_files) if source_files else ["- Missing"]),
            "",
        ]
    )


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _bullet_lines(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]
