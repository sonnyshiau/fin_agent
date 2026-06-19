from pathlib import Path

from fin_agent.flow_check import phase_zero_ready


def test_phase_zero_ready_requires_core_files(tmp_path: Path):
    (tmp_path / "docs/superpowers/specs").mkdir(parents=True)
    (tmp_path / "docs/superpowers/specs/spec.md").write_text("# Spec", encoding="utf-8")
    (tmp_path / "分析框架.md").write_text("# Framework", encoding="utf-8")
    (tmp_path / "tech_investing_product_cycle.md").write_text("# Notes", encoding="utf-8")
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=x", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nreport/\noutputs/\n", encoding="utf-8")
    assert phase_zero_ready(tmp_path) is True


def test_phase_zero_ready_accepts_repository_framework_name(tmp_path: Path):
    (tmp_path / "docs/superpowers/specs").mkdir(parents=True)
    (tmp_path / "docs/superpowers/specs/spec.md").write_text("# Spec", encoding="utf-8")
    (tmp_path / "分析框架.md").write_text("# Framework", encoding="utf-8")
    (tmp_path / "tech_investing_product_cycle.md").write_text("# Notes", encoding="utf-8")
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=x", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nreport/\noutputs/\n", encoding="utf-8")
    assert phase_zero_ready(tmp_path) is True


def test_phase_zero_ready_rejects_missing_outputs_ignore(tmp_path: Path):
    (tmp_path / "docs/superpowers/specs").mkdir(parents=True)
    (tmp_path / "docs/superpowers/specs/spec.md").write_text("# Spec", encoding="utf-8")
    (tmp_path / "分析框架.md").write_text("# Framework", encoding="utf-8")
    (tmp_path / "tech_investing_product_cycle.md").write_text("# Notes", encoding="utf-8")
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=x", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(".env\nreport/\n", encoding="utf-8")
    assert phase_zero_ready(tmp_path) is False
