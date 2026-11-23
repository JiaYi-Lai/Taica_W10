# NFC 近場通訊技術入門 Wiki

本專案採用 Karpathy-style LLM Wiki：官方來源快照唯讀保存，Codex 逐篇讀取和整合來源，維護互相連結的 Markdown Wiki。查詢與簡報先使用 Wiki，不以向量檢索或模型內部知識代替可追溯內容。

## 目前完成

- 6 份官方來源正文成功保存並整合；另外 3 份候選來源因擷取失敗或正文不足，仍標記為 failed。
- 建立 6 篇來源摘要、6 篇概念頁、1 篇比較頁，以及 `wiki/index.md`、`wiki/overview.md`、`wiki/log.md`。
- 原始快照按 source ID 和 SHA-256 版本保存；原有平面快照和 3 篇舊草稿保留。
- 已產生 11 頁自包含 HTML 入門簡報：`slides/nfc-intro.html`。內容由 Query 正式 Wiki 後整理，引用來源列在每頁和最後一頁。
- Ingest / Slides Graph、重試規則、實際 run records 和反思見 `docs/workflows.md`、`reports/phase-completion.md`。

## Wiki 與來源

- Wiki 導覽：`wiki/index.md`
- 操作紀錄：`wiki/log.md`
- Schema：`SCHEMA.md`
- 來源 ID 沿革：`docs/source-id-map.md`
- 官方擷取情況：`docs/sources.md`

## Ingest：擷取一份來源

先在 `data/sources.json` 確認來源 ID，然後執行：

```powershell
python -m app.ingest.cli --source-id S05
```

這會取得來源並保存版本化 raw snapshot 和 metadata。預設流程是 Codex 先讀 Wiki、提出頁面變更清單，等待使用者確認後再寫 Wiki；使用者明確授權批次時，可一次處理剩餘成功來源。不得覆寫 raw，也不能把失敗來源當成成功。

## Query：先讀 Wiki

```powershell
python -m app.wiki.cli context "NFC 標籤 NDEF 訊息" --max-pages 10
```

指令先讀 `wiki/index.md`，再選擇被索引的 Markdown 頁面，並留下 Query 記錄。它負責準備上下文；答案或教材由 Codex 讀取頁面及來源後整理。若證據不足，應回報知識缺口。

## Lint：檢查 Wiki

```powershell
python -m app.wiki.cli lint
```

程式會檢查頁面格式、索引、連結、來源 ID、raw snapshot、paragraph citation、孤立頁與重複標題。Codex 另外檢查語意矛盾、過時主張和知識缺口。

## HTML 簡報

直接用瀏覽器開啟 `slides/nfc-intro.html`。可按上一頁/下一頁，或使用鍵盤左右方向鍵；最後一頁列出 6 份官方來源。完整執行紀錄與反思見 `reports/phase-completion.md`。

## Python 與測試

需要 Python 3.11 或更新版本：

```powershell
python --version
python -m unittest discover -s tests -v
```

若 Windows 顯示「Python was not found」，需安裝 Python 並加入 PATH，或使用本機已安裝的 Python 執行檔完整路徑。

## 舊式原型

`app/wiki/workflow.py`、`legacy-draft` 和 `app/llm` 保留早期檢索 raw 段落並生成單篇草稿的原型，不是新版 Wiki 的核心 Ingest / Query 流程。Wiki 維護不要求 API key。
