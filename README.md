# fin_agent

`fin_agent` 是一個本地研究流程工具，用來把私人研究報告整理成有來源依據、結構化的投資研究 memo。

這個專案目前圍繞兩份本地知識文件：

- `分析框架.md`：主要基本面分析框架，用來規範 memo 結構。
- `tech_investing_product_cycle.md`：科技投資中的 product cycle、預期差與 catalyst 研究筆記。

原始研究報告放在 `report/`，並且刻意不進 git。

## 目前狀態

已完成：

- TXT 報告讀取
- 文字切 chunk，並保留來源 metadata
- 本地關鍵字搜尋
- Evidence map 產生
- Markdown memo 輸出
- 基本 CLI
- `flow.md` 階段檢查流程

尚未完成：

- PDF 文字抽取
- 真正串接 OpenAI API 產生 memo
- 網站 UI
- 向量搜尋
- 即時市場資料

## 環境設定

在 repo 根目錄執行：

```powershell
python -m pytest
```

API 設定放在 `.env`。可以先複製範本：

```powershell
Copy-Item .env.example .env
```

然後編輯 `.env`：

```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-5.5
```

不要 commit `.env`、`report/` 或 `outputs/`。

## 放入研究報告

把本地研究資料放在：

```text
report/
```

目前 pipeline 支援 `.txt` 檔。PDF 可以先放在 `report/`，但 PDF parsing 是下一階段功能。

TXT 範例：

```text
Marvell 的 AI data center 需求持續成長。
CPO 與 optical interconnect 是下一代 product cycle 重點。
Forward guidance 顯示 networking revenue 有機會上修。
```

## 產生 Memo

執行本地查詢：

```powershell
$env:PYTHONPATH="src"
python -m fin_agent.cli CoPoS
```

CLI 會做：

1. 掃描 `report/`
2. 讀取支援的 TXT 檔
3. 把文字切成 chunks
4. 搜尋 `CoPoS`
5. 建立 evidence map
6. 輸出 Markdown memo 到 `outputs/CoPoS-memo.md`

目前 memo generation 還是 placeholder：

```text
Model generation is not wired yet.
```

但 evidence map 和來源引用已可用來驗證搜尋與資料調用是否正確。

## 執行測試

```powershell
python -m pytest -v
```

目前預期結果：

```text
10 passed
```

## Flow Gates

用 `flow.md` 追蹤每個 phase 是否完成。

規則：

- deliverables 沒完成，不能打勾。
- 測試或人工驗證沒跑，不能打勾。
- 如果 `.env`、`report/` 或 `outputs/` 被 staged，不能打勾。

檢查 Phase 0：

```powershell
$env:PYTHONPATH="src"
python -c "from pathlib import Path; from fin_agent.flow_check import phase_zero_ready; print(phase_zero_ready(Path('.')))"
```

預期結果：

```text
True
```

## 下一階段建議

下一個有價值的 milestone 是完成 Phase 1：

- 加入 PDF extraction
- 保留頁碼 metadata
- 加入 PDF 成功解析或清楚失敗的 fixture tests
- 驗證通過後才更新 `flow.md`

## GitHub Pages

- [Vera Rubin / Rubin Ultra NVL72 Rack Architecture](https://sonnyshiau.github.io/fin_agent/)
- [Retirement Calculator](https://sonnyshiau.github.io/retirement-calculator/)
