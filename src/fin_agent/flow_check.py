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
