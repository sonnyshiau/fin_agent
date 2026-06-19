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
