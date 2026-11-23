# 可執行流程與重試規則

流程節點由 Codex 維護知識、Python CLI 執行可重現檢查、JSON run record 和 `wiki/log.md` 留存實際執行。每次輸入、輸出、狀態、錯誤、修正和驗證都要能追查。使用者確認節點依當次授權行事；明確批次授權可覆蓋逐篇暫停。

## Graph A：Ingest

```mermaid
flowchart TD
  A([開始：選一份官方來源]) --> B[Acquire：取得正文、URL、時間與 hash]
  B --> C{正文可讀且主題相符？}
  C -- 否 --> C1[記錄 failed；不補寫來源內容]
  C1 --> C2{仍有安全的官方替代取得方式？}
  C2 -- 有，最多 3 次 --> B
  C2 -- 無／達上限 --> Z([停止此來源並回報])
  C -- 是 --> D[保存不可變 raw 與 metadata]
  D --> E[Inspect：讀 index、overview、相關頁]
  E --> F[Codex 提出摘要與 create/update/conflict 清單]
  F --> G{使用者已確認此來源或批次？}
  G -- 否 --> H([等待確認])
  G -- 是 --> I[Integrate：寫摘要、更新概念頁、連結、overview、index]
  I --> J[Deterministic Lint + citation audit + Codex semantic review]
  J --> K{通過？}
  K -- 是 --> L[追加 log 與 JSON run record]
  L --> M([完成])
  K -- 格式／連結／引用錯誤 --> N[按錯誤原因修補；最多 3 次]
  N --> J
  K -- 語意衝突／來源不完整 --> O[標記分歧或知識缺口；不可猜測]
  O --> F
```

### Ingest 失敗分流

- TLS、HTTP 或空正文：記錄為 Acquire failure；最多使用 3 次安全取得嘗試。不得停用 TLS 驗證、繞過存取限制或以模型記憶補原文。
- 正文不完整或只有 JavaScript shell：標記 failed，必要時提出可信的官方替代頁面。
- Broken link、缺 citation 或 metadata：修正並重新 Lint；同一錯誤最多 3 次自動修復。
- 主張衝突：並列來源、語境及段落 ID；無法判定就保留「來源存在分歧／待確認」。

## Graph B：Wiki 到 HTML 簡報

```mermaid
flowchart TD
  A([設定初學者教學目標]) --> B[Query：先讀 wiki/index.md]
  B --> C[讀取被索引的概念／比較／來源頁]
  C --> D{Wiki 證據足夠？}
  D -- 否 --> E[記錄知識缺口；返回 Ingest]
  E --> B
  D -- 是 --> F[Codex 整理教學大綱]
  F --> G[Coverage：逐頁核對 Wiki 頁與 raw source ID]
  G --> H[Codex 由 Wiki 撰寫 8–12 張投影片]
  H --> I[內容審查：主張、來源、語境、教學順序]
  I --> J[產生獨立 HTML：CSS／JS 內嵌]
  J --> K[HTML 驗證：張數、來源、控制鈕、鍵盤、結構]
  K --> L{通過？}
  L -- 是 --> M[保存 HTML、執行 trace、log]
  M --> N([交付])
  L -- 否，最多 3 次 --> O[帶入上次錯誤修正該節點]
  O --> J
  L -- 仍失敗 --> P[停止並輸出待人工處理報告]
```

### Retry 規則

- 所有修復都必須記錄上一次錯誤和本次修正，不得無條件重跑同一節點。
- 可自動修復的 Markdown/HTML 問題最多 3 次；第三次仍失敗就停止該分支。
- 需要使用者判斷的來源選擇或無法由資料消解的分歧，不算自動重試；停在待確認狀態並保留依據。
- 真實失敗和注入錯誤的測試必須分開記錄。本專案本次未注入測試錯誤。

## 目前實際運作方式

`app.ingest.cli` 執行 Acquire / Clean / immutable snapshot；Codex 執行 Inspect、Discuss、Integrate 及語意審查；`app.wiki.cli context` 執行 index-first Query；`app.wiki.cli lint` 執行 deterministic checks。Slides 的內容維護由 Codex 按 Query 輸出的 Wiki 上下文完成，HTML 是靜態自包含輸出，不需要 API key。
