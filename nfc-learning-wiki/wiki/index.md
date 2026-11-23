# NFC Wiki 索引

> 本索引只列根目錄 `wiki/` 中已整合並通過 lint 的正式知識頁。`data/wiki/` 的舊草稿保留在原處，尚未提升為正式 Wiki 頁。

## 概觀

- [NFC 知識概觀](./overview.md) — 說明目前知識地圖、證據狀態與待查缺口。

## 來源摘要

- [Android NFC 基礎與 NDEF（S03）](./sources/S03-android-nfc-basics.md) — 說明 Android 如何讀取 NDEF 標籤並將內容交給應用程式。
- [Android HCE（S04）](./sources/S04-android-hce.md) — 比較 Android 卡片模擬的安全元件與主機 CPU 路徑。
- [STMicroelectronics NFC（S05）](./sources/S05-st-nfc.md) — NFC 的近距離使用體驗、頻率和應用概覽。
- [EMV 感應式晶片支付（S06）](./sources/S06-emv-contactless-chip.md) — EMVCo 對感應式支付、交易規格和支付安全說明的官方概覽。
- [Android NFC 概觀（S08）](./sources/S08-android-nfc-overview.md) — Android 標籤、NDEF、距離和平台操作模式。
- [Android NFC 安全（S09）](./sources/S09-android-nfc-security.md) — 標籤資料驗證及 Android 應用程式風險。

## 概念頁

- [NFC 與感應式支付](./concepts/nfc-and-contactless-payments.md) — 區分近距離通訊方式與支付交易規格。
- [NFC 基礎概念](./concepts/nfc-basics.md) — NFC 的近距離使用方式、常見用途和距離脈絡。
- [NFC 標籤與 NDEF](./concepts/ndef-and-tags.md) — NFC 標籤、NDEF message 和 records 的入門說明。
- [NFC 運作模式與平台支援](./concepts/nfc-operating-modes.md) — 區分 NFC 應用模式類別與 Android 平台支援。
- [Android 卡片模擬與 HCE](./concepts/hce-and-secure-element.md) — 說明 Android Secure Element 與 HCE 的資料路徑。
- [NFC 安全入門](./concepts/nfc-security.md) — 整理 Android 文件中的標籤處理風險與防護方式。

## 比較頁

- [NFC 距離說法比較](./comparisons/nfc-distance.md) — 並列 ST 與 Android 的描述，保留語境差異。

## 綜合頁

尚無正式綜合頁。

## 待遷移草稿

- [NFC 基礎概念草稿](../data/wiki/ch01-nfc-basics.md)
- [NFC 運作原理草稿](../data/wiki/ch02-nfc-principle.md)
- [NFC 運作模式草稿](../data/wiki/ch03-nfc-modes.md)

以上三篇保留為遷移候選；引用定位存在，但尚未完成新版 Ingest 討論流程、Wiki cross-links 與正式 Lint。
