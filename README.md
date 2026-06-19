# fin_agent

## Local Pipeline

The initial pipeline reads local research files from `report/`, builds a small local search index, creates an evidence map, and writes Markdown memos to `outputs/`.

```powershell
python -m pytest
python -m fin_agent.cli CPO
```

Secrets belong in `.env`; use `.env.example` as the template. Do not commit `.env`, `report/`, or `outputs/`.
