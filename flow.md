# fin_agent Flow Check

This file is the project execution gate. A phase can be checked only after its required artifacts exist and its verification steps pass. Do not check boxes based on intent or partial progress.

## Flow Rules

- Only mark a phase complete after every required deliverable is present.
- If a deliverable is missing, leave the phase unchecked.
- If verification was not run, leave the phase unchecked.
- If verification fails, leave the phase unchecked and record the blocker.
- `report/`, `.env`, and `outputs/` must never be committed.
- Each completed phase should have a short note explaining what was verified.

## Supervisor Agent

Use a dedicated Supervisor Agent role before advancing phases.

Supervisor responsibilities:

- Inspect changed files.
- Confirm required artifacts exist.
- Confirm ignored files stay ignored.
- Confirm tests or manual checks were run.
- Confirm no phase is checked without evidence.
- Refuse to advance if source citations, missing-data handling, or verification are absent.

Supervisor prompt:

```text
You are the fin_agent Supervisor. Review the current repository against flow.md.
Do not implement features. Only verify whether the next unchecked phase can be marked complete.
List missing artifacts, failed checks, and risks. Approve phase advancement only when all gates pass.
```

## Phase 0: Spec And Project Groundwork

- [x] Design spec exists under `docs/superpowers/specs/`.
- [x] `分析框架.md` exists and is readable as UTF-8 Markdown.
- [x] `tech_investing_product_cycle.md` exists.
- [x] `.env.example` exists without real secrets.
- [x] `.gitignore` ignores `.env`, `report/`, and `outputs/`.
- [x] Supervisor reviewed that no secret or report file is staged.

Done note:

```text
Verified with `PYTHONPATH=src python -c "from pathlib import Path; from fin_agent.flow_check import phase_zero_ready; print(phase_zero_ready(Path('.')))"`, which returned True. Full test suite passed with 10 tests. Git status showed `.env` and `report/` ignored, not staged.
```

## Phase 1: Local Ingestion

- [ ] `report/` scanner lists PDF and TXT files.
- [ ] TXT loader reads UTF-8 Chinese text correctly.
- [ ] PDF loader extracts text or records a clear parse failure.
- [ ] Loader stores source metadata: file name, type, page or section.
- [ ] Ingestion can run without committing `report/`.
- [ ] Tests or fixture checks cover TXT and PDF paths.

Done note:

```text
Pending.
```

## Phase 2: Chunking, Search, And Evidence Map

- [ ] Documents are split into chunks with stable `chunk_id`.
- [ ] Every chunk preserves source metadata.
- [ ] Local keyword or BM25 search works for company and theme queries.
- [ ] Evidence map includes source files, key facts, missing data, confidence levels, and contradictions.
- [ ] Weak evidence is explicitly marked instead of upgraded into a strong conclusion.
- [ ] Tests or fixture checks cover retrieval and evidence map output.

Done note:

```text
Pending.
```

## Phase 3: Memo Generation

- [ ] Model config reads `OPENAI_API_KEY` and `OPENAI_MODEL` from `.env`.
- [ ] Generation uses `分析框架.md` as the memo structure.
- [ ] Output includes all required sections from the framework.
- [ ] Claims include source citations or are marked as missing/low confidence.
- [ ] Markdown memo is saved under `outputs/`.
- [ ] Model failure leaves evidence map available and reports the error.
- [ ] Tests or manual checks verify one sample memo.

Done note:

```text
Pending.
```

## Phase 4: Local Web Workbench

- [ ] Web app starts locally.
- [ ] Report library view lists parsed files and statuses.
- [ ] Research task input accepts company, ticker, or theme.
- [ ] Memo view displays structured output and source citations.
- [ ] User can save or download generated Markdown.
- [ ] Error states are visible for parse, retrieval, and model failures.
- [ ] Desktop and mobile layouts are checked.

Done note:

```text
Pending.
```

## Phase 5: Advanced Research Workflows

- [ ] Company comparison mode works.
- [ ] Theme or supply-chain map mode works.
- [ ] Watchlist and catalyst tracking exist.
- [ ] Contradiction review highlights conflicting source claims.
- [ ] Follow-up questions can be generated from missing data.
- [ ] Outputs remain source-grounded and confidence-scored.

Done note:

```text
Pending.
```

## Current Blockers

- No implementation code exists yet.
- No ingestion, retrieval, memo generation, or web app tests exist yet.
- `flow.md` itself must be reviewed before Phase 0 is checked.
