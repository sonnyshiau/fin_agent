from __future__ import annotations

import argparse
from pathlib import Path

from fin_agent.evidence import build_evidence_map
from fin_agent.ingestion import DocumentLoader, chunk_document
from fin_agent.memo import render_memo
from fin_agent.model_provider import StaticModelProvider
from fin_agent.retrieval import SearchIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--report-dir", default="report")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    loader = DocumentLoader()
    docs = loader.scan(Path(args.report_dir))
    chunks = [chunk for doc in docs for chunk in chunk_document(doc)]
    results = SearchIndex(chunks).search(args.query)
    evidence = build_evidence_map(args.query, results)
    provider = StaticModelProvider("Model generation is not wired yet.")
    memo = render_memo(args.query, evidence, provider.summarize(args.query))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{args.query}-memo.md"
    output_path.write_text(memo, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
