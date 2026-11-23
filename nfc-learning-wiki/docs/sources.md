# 第一階段官方來源與擷取結果

## 核實原則

候選頁面來自 NFC Forum、Android Developers、STMicroelectronics、EMVCo 與 Apple Developer 官方網站。正式擷取僅將 HTTP 成功、正文通過長度與 NFC 主題檢查、且 SHA-256 不重複的項目列為成功。HTTP 200 本身不足以代表正文有效。NFC Forum 規格頁是規格索引，不視為已讀取規格正文。

官方頁面的文字檢視顯示，NFC Forum 技術概述涵蓋 13.56 MHz、典型距離與操作模式；Android 文件說明 NDEF 與 HCE；EMVCo 頁面介紹 contactless chip。來源頁面與其用途見 [來源登錄](../data/sources.json)。

## 實際 Ingest

Run ID：`bb104b1b-dcb4-4952-9de7-6304ab9c09f2`（UTC：2026-11-23）。候選 8 份，成功 5、失敗 3、重複 0。成功來源各有原始 HTML、清理段落 JSON、HTTP 狀態與 SHA-256，位於 `data/raw/`、`data/cleaned/` 和 `data/sources.json`。完整節點事件見 `data/runs/bb104b1b-dcb4-4952-9de7-6304ab9c09f2.json`。

| ID | 官方機構／文件 | 結果 | HTTP | 說明 |
|---|---|---:|---:|---|
| S01 | NFC Forum — NFC Technology | 失敗 | — | TLS 憑證鏈無法由目前 Python 執行環境驗證；未停用 TLS 驗證。 |
| S02 | NFC Forum — What NFC Does | 失敗 | — | 同為 TLS 憑證鏈驗證錯誤。 |
| S03 | Android Developers — NFC basics | 成功 | 200 | 清理後 674 段、約 33,509 字元。 |
| S04 | Android Developers — HCE overview | 成功 | 200 | 清理後 551 段、約 30,084 字元。 |
| S05 | STMicroelectronics — NFC resources | 成功 | 200 | 清理後 168 段、約 11,310 字元。 |
| S06 | EMVCo — Contactless Chip | 成功 | 200 | 清理後 193 段、約 9,831 字元。 |
| S07 | Apple Developer — Core NFC | 失敗 | 200 | 回應為 JavaScript 殼頁，正文僅 40 字元，未計入成功。 |
| S08 | Android Developers — NFC overview | 成功 | 200 | 以官方概覽補足來源數，清理後 76 段、約 3,347 字元。 |

Apple Developer Core NFC 主題頁透過文件檢視可見官方內容，但目前直接 HTTP HTML 擷取只取得要求 JavaScript 的短頁面，因此本次程式 Ingest 判定仍為失敗。後續可評估官方可讀 Markdown 頁面或具體 API 文件作為替代來源，並須由 pipeline 實際抓取驗證。

## 存取與權利備註

原始 HTML 僅保存在本機供核對。這些檔案不應被視為可任意再散布的內容；分享或提交時應優先提供官方連結、來源 Metadata 與自行撰寫的摘要。擷取器不繞過付費或存取限制，亦不關閉 TLS 憑證驗證。
