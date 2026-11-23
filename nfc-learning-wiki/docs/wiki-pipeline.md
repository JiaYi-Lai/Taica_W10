# NFC Wiki 操作方式

本專案採用 Karpathy-style LLM Wiki：原始來源唯讀保存，Codex 維護相互連結的 Markdown Wiki。查詢先讀 Wiki，簡報也由 Wiki 派生，不由 RAG chunks 或模型內部知識直接寫成教材。

## Ingest

每份來源保存來源 ID、標題、publisher、URL、擷取時間、HTTP 狀態、SHA-256、存取備註及不可變 raw 路徑。成功來源快照按 `source_id/SHA-256` 版本化；原本 flat 檔案保留，不覆寫。

Ingest 先讀 `wiki/index.md`、`wiki/overview.md` 和受影響頁面，再檢查來源正文及 paragraph IDs。預設逐篇提出異動清單並等候使用者確認；使用者明確批准批次後，可以同批處理剩餘成功來源。整合時要建立來源摘要、更新概念頁和交叉連結、更新 overview/index，最後執行 Lint 並追加 log 和 JSON run record。

本次批次依明確授權整合 S03、S04、S05、S08、S09；先前已整合 S06。S01/S02 因 TLS 憑證驗證失敗、S07 因只擷取到過短的 JavaScript 殼頁而保持 failed，沒有計入成功來源。ID 對照見 `source-id-map.md`。

## Query

```powershell
python -m app.wiki.cli context "NFC 標籤 NDEF 訊息" --max-pages 10
```

CLI 先讀 `wiki/index.md`，再讀被索引連結的相關頁面；它只準備上下文，不冒充 LLM 已回答。Codex 讀取這些頁面和引用後生成答案、教學或簡報。若 Wiki 證據不足，要標示缺口並返回 Ingest。查詢記錄保存選取頁面及 run ID。中文索引詞加入雙字元匹配，避免中文詞語因無空格而漏選頁面。

## Lint

```powershell
python -m app.wiki.cli lint
```

程式檢查 front matter、索引涵蓋、相對連結、來源成功狀態、raw snapshot、paragraph citation、孤立頁和重複標題。Codex 另閱讀引用來源與 Wiki 主張，檢查矛盾、過時內容、近重複和知識缺口；語意審查不能只由字串規則宣稱完成。

## HTML 簡報

先以 index-first Query 選擇 Wiki 頁面，Codex 再按教學目標編寫 8–12 張投影片，檢查來源涵蓋與引文後產生獨立 HTML，最後驗證投影片數、引用、互動導覽和 HTML 結構。生成和驗證紀錄保存於 `wiki/log.md`、`data/runs/` 與 `reports/`。目前成果是 `slides/nfc-intro.html`。

## 舊式原型

`app/wiki/workflow.py` 與 `legacy-draft` 是早期「檢索 raw 段落後生成單篇文章」原型，保留相容性但不作為新版 Wiki Ingest/Query 主流程。核心 Wiki 維護由 Codex 執行，不要求付費 API 或網站按鈕。
