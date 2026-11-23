# NFC 近場通訊技術入門 Wiki

本專案以可追溯的官方公開資料建立 NFC 初學者 Wiki，後續階段才會加入 Wiki 生成、搜尋、Workflow / Graph 與 HTML 教學簡報。

## 目前狀態：第一階段

目前程式包含來源登錄、HTTP Fetch、HTML Clean、SHA-256 去重與 run JSON 紀錄。一次實際擷取已成功保存 5 份不同官方正文，Run ID 為 `bb104b1b-dcb4-4952-9de7-6304ab9c09f2`；候選總數 8、失敗 3。來源結果見 `docs/sources.md`。**尚未完成 LLM、Wiki 文章、搜尋、Graph、完整 UI 或簡報功能；來源清單也不代表已成功 Ingest。**

## 環境與執行

需要 Python 3.11+。第一階段僅使用 Python 標準函式庫，不需要 API 金鑰。

在本目錄執行測試：

```powershell
python -m unittest discover -s tests -v
```

執行官方來源 Ingest：

```powershell
python -m app.ingest.cli
```

命令會更新 `data/sources.json`，將原始 HTML 寫入 `data/raw/`、清理後段落 JSON 寫入 `data/cleaned/`，並在 `data/runs/` 留下執行紀錄。請以實際 `ingest_status` 檢視成功數；遇到網站拒絕、逾時、JavaScript 頁面或抽取不足時，會記錄失敗，不會以猜測內容補足。

若命令列有任何來源失敗，CLI 會以非零狀態結束；這不會抹除同一次執行中其他成功來源的紀錄。

## 來源與著作權

候選來源均為來源清單所列官方網站。規格索引不視為規格正文；付費、受限制或無法讀取的資料不會被假設已取得。原始頁面僅供本機驗證；若來源有再散布限制，提交時只保留來源 URL、Metadata 與自行撰寫的轉述。請遵守網站使用條款與合理請求頻率。

## 第一階段驗收

- Fetch 成功、404、非 HTML、空白正文及有限重試行為有測試。
- Clean 移除導覽與頁尾並保留正文、產生段落定位。
- Metadata 可保存來源欄位、計算 hash、偵測重複。
- 正式擷取至少 5 份不同有效正文後，才可宣告來源 Ingest 驗收通過。
