# Source ID 對照與沿革

`source_id` 一旦被 raw、log 或 Wiki 引用使用，就視為穩定識別碼。新版 `AGENTS.md` 的候選清單調整了部分編號，不能直接重編現有來源，以免破壞引用。

| 現有 ID（保留） | 目前 `data/sources.json` 對應來源 | 新版候選清單中的名稱／衝突 |
|---|---|---|
| S01 | NFC Forum — NFC Technology | 相同 |
| S02 | NFC Forum — What NFC Does（目前擷取失敗） | 新版 S02 是 Specifications；新版 S08 才是 What NFC Does |
| S03 | Android Developers — NFC basics | 新版 S04 |
| S04 | Android Developers — HCE | 新版 S06 |
| S05 | STMicroelectronics — NFC technology resources | 新版 S03 |
| S06 | EMVCo — Contactless Chip | 新版 S05 |
| S07 | Apple Developer — Core NFC（正文擷取失敗） | 新版 S07 |
| S08 | Android Developers — NFC overview | 新版 S08 是 NFC Forum — What NFC Does |
| S09 | Android Developers — NFC security risks | 新增安全候選，未列在原候選表 |

已存在的 source ID 和引用一律保留；新版新增候選先使用未占用的新 ID（目前下一個可用為 S10），並在 registry 中記錄正式 URL、標題及 publisher，不用候選清單編號覆蓋既有來源。
