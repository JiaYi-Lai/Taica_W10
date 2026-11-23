---
id: overview
title: NFC 知識概觀
type: overview
updated_at: 2026-11-23
sources:
  - S03
  - S04
  - S05
  - S06
  - S08
  - S09
---

# NFC 知識概觀

本頁是知識地圖，不是已完成的 NFC 教材。概念範圍依新版專案規範規劃；只有完成來源整合並附上來源 ID、paragraph ID 後，才會寫成確定的技術說明。

## 初期知識地圖

- **基礎**：NFC 定義、用途、頻率、短距離通訊。
- **技術**：電磁感應／近場耦合、主動與被動裝置、標準與相容性。
- **運作方式**：Reader/Writer、Card Emulation、Peer-to-Peer；區分標準與平台支援。
- **資料**：NFC Tag、Tag 類型、NDEF、Record、讀寫流程。
- **應用**：支付、交通、門禁、配對與智慧標籤。
- **安全**：惡意標籤、未授權讀取、資訊保護與安全限制。

## 目前證據狀態

來源 Registry 記錄 6 份成功 Ingest 的官方正文，現已完成 Wiki 整合：S03 Android NFC basics、S04 Android HCE、S05 STMicroelectronics NFC、S06 EMVCo、S08 Android NFC overview、S09 Android NFC security。另有 3 份候選來源擷取失敗或正文不足，不計入成功來源。各頁及來源狀態可由 [Wiki 索引](./index.md)、[來源 Registry](../data/sources.json) 和 [來源 ID 對照](../docs/source-id-map.md) 查閱。[S03，p0069-181c7b789d；S04，p0059-cae55ff30a；S05，p0044-c604cf788c；S06，p0065-abeb47faea；S08，p0049-3f564abd29；S09，p0276-3b93dac3c3]

## 待查與待整合

- 目前 6 份成功來源均已有摘要和相關概念頁；後續新來源需再逐篇比較及更新既有頁面。
- 保留不同官方文件的距離、模式或平台描述差異，不在缺少上下文時合併數值。[S05，p0044-c604cf788c；S08，p0037-68507b3450；p0038-d1d275e2d0]
- S06 是支付領域概覽；NFC 的通訊方式與 EMV 支付規格仍應分開描述，避免把 EMV 的支付安全特性套用到所有 NFC 應用。[S06，p0064-4f8a50ce33；p0065-abeb47faea]
- 尚無跨領域綜合教學頁；目前已建立距離說法比較頁。

## 相關導覽

- [Wiki 索引](./index.md)
- [來源與內容 schema](../SCHEMA.md)
- [NFC 基礎概念](./concepts/nfc-basics.md)
- [NFC 安全入門](./concepts/nfc-security.md)
