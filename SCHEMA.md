# NFC Wiki Markdown Schema

本 schema 定義根目錄 `wiki/` 的正式知識頁。`data/raw/` 是來源快照，`wiki/` 是由 LLM 維護的知識成品；擷取段落與搜尋索引不能取代 Wiki 頁面。

## 頁面 front matter

所有正式頁面以 YAML front matter 開始，欄位採以下格式：

```yaml
---
id: nfc-basics
title: NFC 基礎概念
type: concept
updated_at: 2026-11-23
sources:
  - S05
---
```

必填欄位：`id`（唯一、英文小寫與連字號）、`title`、`type`、`updated_at`（ISO 日期）、`sources`（至少一筆已成功擷取的 source ID）。來源索引頁使用 `type: source` 和 `source_id`；非來源知識頁的 `sources` 必須能回溯到成功的 raw snapshot。

## 頁面類型與路徑

- 來源摘要：`wiki/sources/<source-id>-<slug>.md`，記錄來源內容摘要、可支持的主張、影響頁面與限制。
- 概念頁：`wiki/concepts/<slug>.md`，解釋可長期維護的 NFC 概念。
- 比較頁：`wiki/comparisons/<slug>.md`，呈現來源差異或技術比較，不把不同語境硬併成單一數字。
- 綜合頁：`wiki/synthesis/<slug>.md`，整理跨頁知識與初學者學習路徑。
- `_template.md` 是空白樣板，不是正式知識頁，不列入索引或 lint 的知識頁統計。

## 概念、比較與綜合頁必備段落

```markdown
## 核心概念
## 詳細說明
## 相關知識
## 來源
```

主要技術主張在段落旁標示 source ID 與原文 paragraph ID。`相關知識` 必須有可用的相對 Markdown 連結，例如 `[NDEF](./ndef.md)`。不確定資訊標示「待確認」；來源說法不同時標示「來源存在分歧」，列出各來源的主張和適用語境。

## 來源頁必備段落

來源摘要頁需列出 `source_id`、官方標題、publisher、來源 URL、raw snapshot 路徑與 hash，並包含 `## 來源摘要`、`## 可整合知識`、`## 既有頁面異動`、`## 來源限制`、`## 相關知識`。不可貼入或改寫成完整原文；以轉述及必要短引文為主。

## 全站特殊頁

- `wiki/index.md`：分類列出所有正式 Wiki 頁面的相對連結與一句話摘要；每次整合後更新。
- `wiki/overview.md`：描述目前已由來源支持的知識輪廓及待查缺口；不可先填入未 ingest 的技術事實。
- `wiki/log.md`：append-only 時間軸，記錄 ingest、query、lint、slides 的 run_id、輸入、頁面變更、驗證與失敗修復。

## Lint 規則

Lint 對正式頁檢查 front matter、索引涵蓋、檔案連結、source ID、raw snapshot、孤立頁與重複標題；狀態分 `error`、`warning`、`info`。語意矛盾、過期說法、近重複概念與知識缺口由 LLM/Codex 提出，並附引用依據，不能只靠字串程式宣稱語意已驗證。
