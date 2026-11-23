# NFC Wiki 完整執行紀錄與反思

日期：2026-11-23（Asia/Taipei）  
執行者：Codex（以 LLM 維護 Wiki）  
批次授權：使用者明確要求「全部執行並按照 AGENTS.md 修改」。

## 成果

- 6 份官方來源正文成功擷取，並都已整合進新版 Wiki：S03 Android NFC basics、S04 Android HCE、S05 STMicroelectronics NFC、S06 EMVCo Contactless Chip、S08 Android NFC overview、S09 Android NFC security。
- 新增 5 篇來源摘要、5 篇概念頁與 1 篇比較頁；更新 S06 支付概念、`wiki/overview.md`、`wiki/index.md`。
- 來源快照保留舊檔，並以 `source_id/SHA-256` 版本化路徑新增 raw、metadata 和 cleaned 段落檔。所有 Wiki 引用段落經逐條比對，都存在於該頁聲明的成功來源中。
- 建立 [11 頁 HTML 入門簡報](../slides/nfc-intro.html)，由已 Query 的 Wiki 撰寫；每頁標示 Wiki 和來源 ID，末頁列出 6 份官方來源。
- 建立 Ingest / Slides Mermaid Graph、錯誤分流和最多 3 次修復規則，見 [流程說明](../docs/workflows.md)。

## 實際節點紀錄

| 節點 | 實際結果 | 可查紀錄 |
|---|---|---|
| Acquire（既有官方快照） | 6 成功、3 失敗；成功快照的 SHA-256 與 Registry 相符，並已建立版本化副本。 | `data/runs/93ce18bc-9680-4e6b-b3fd-99566e451ae8.json` |
| Inspect / Integrate | Codex 讀取 Wiki 與來源段落，完成 S03、S04、S05、S08、S09 批次整合；S06 已先前整合。 | `wiki/log.md`，以及下方本次 run records |
| Citation audit | 14 頁全部通過：每個 paragraph ID 都存在於頁面列出的成功來源。 | 本次整合 run record |
| Query | 5 組中文 index-first Query 均讀取了相關 Wiki 頁；其中涵蓋 NFC 基礎、NDEF、操作模式/HCE、支付與安全。 | `data/runs/44b15bec-97d4-4ce9-9165-99e778322042.json`、`3f0ebcc3-3fc8-4abd-835e-44160cebf220.json`、`e54de8d1-7a92-476f-813d-633e806c3972.json`、`5b3f0fe4-c78a-4c4c-8635-0dde7edddd8f.json`、`a7b0961f-efa7-47e4-a02f-b98fee032296.json` |
| Wiki Lint | 14 頁檢查通過，0 error、0 warning、1 info（提醒語意審查需由 Codex 執行）。 | `data/runs/9e9dfc7d-68df-4dc9-85d4-044160479e45.json` |
| Unit tests | 34 項通過，包括新增的中文查詢詞測試。 | 命令：`python -m unittest discover -s tests -v` |
| HTML validation | 11 頁、全部有成功來源 ID、6 個官方連結、自包含 CSS/JS、按鈕與鍵盤導覽正常。 | 本次 slides run record |

## 真實擷取失敗與修復反思

最近的實際來源擷取 run 有 3 個失敗：S01 與 S02 因 Python TLS 憑證鏈驗證錯誤；S07 的 HTTP 狀態是 200，但取得內容只有 40 字元的 JavaScript 殼頁，未達正文門檻。它們沒有被當成成功來源，也沒有關閉 TLS 驗證或用模型知識補原文。S03、S04、S05、S06、S08、S09 有可用正文，總數已達規範要求的至少 5 份。

本次觀察到最常出錯的節點是 **Acquire**：3 個來源失敗中，2 個是 TLS 驗證，1 個是頁面可讀性/正文不足。這些是既有真實擷取紀錄，並非為了測試而注入。沒有觀察到 Wiki Lint 或 HTML 驗證失敗。第一次透過 PowerShell 包裝 CLI 時，PowerShell 無法解析完整的 Unicode JSON；改由 Python 直接捕捉 CLI 輸出後，5 組 Query 均成功。這是執行包裝層問題，不是 Wiki Query 節點失敗。

另一項需要持續保留的差異是距離說法：S05 把 NFC 描述為最遠 10 公分；S08 說 Android NFC 啟動連線通常需要 4 公分或更近。比較頁列出兩種語境並標示仍待 NFC Forum 正式資料確認，沒有硬把兩者判為矛盾或擅自折衷。S01/S02 失敗使這個規格層級缺口目前仍存在。

## 本次流程檢討

- 本次批次中中文 Query 初次選頁不穩，檢視後發現無空格中文詞無法和索引詞匹配；已在 `app/wiki/query.py` 加入 CJK 雙字元詞組，新增測試並確認中文安全主題可找到對應頁。
- 來源摘要與概念頁同時補交叉連結，尤其把 NDEF 資料驗證連回 Android 安全來源，讓安全頁內容不只停在單篇摘要。
- 距離比較先前移到概念整合時處理，因為初學者會直接把兩種數值當成一條規則。之後取得 NFC Forum 官方資料時再更新該頁並記錄新證據。
- 本次沒有注入錯誤來模擬自動重試，也沒有實測 HTML 自動修復迴圈；Graph 的 3 次上限是明確流程規則，不把它冒充成已發生的成功重試。


## 最終 Query 與驗證補記

修正中文索引命中與知識缺口判定後，再執行 5 組中文主題 Query；5 組均找到對應 Wiki context，並用「quantum teleportation」確認無匹配時回報 knowledge gap。最終 Query IDs：44b15bec-97d4-4ce9-9165-99e778322042、3f0ebcc3-3fc8-4abd-835e-44160cebf220、e54de8d1-7a92-476f-813d-633e806c3972、5b3f0fe4-c78a-4c4c-8635-0dde7edddd8f、a7b0961f-efa7-47e4-a02f-b98fee032296；gap check：a8a55f3e-854a-4bf4-b423-55febb8cc109。

Final validation run: `data/runs/e3d79e1c-829f-458e-b8a6-d8cfe69a6492.json`. Batch integration run: `data/runs/b283c3d0-7708-44d4-ac30-b8591fa040f4.json`. Slides generation and HTML QA run: `data/runs/3daa7723-46d9-4535-86fa-8c8aec44a474.json`.
