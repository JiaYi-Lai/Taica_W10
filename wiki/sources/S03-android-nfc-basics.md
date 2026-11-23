---
id: source-s03-android-nfc-basics
title: Android NFC 基礎與 NDEF
type: source
updated_at: 2026-11-23
sources:
  - S03
source_id: S03
---

# Android NFC 基礎與 NDEF

## 來源摘要

Android Developers 的 NFC Basics 說明 Android 如何收發 NDEF 訊息，以及系統如何讀取 NFC 標籤、判讀資料並交給相符的應用程式處理。[S03，p0037-7a142dbc46；p0038-6c507c30c8；p0041-01f1a23d3f；p0042-ca7fb5325c；p0043-88d169c245]

NDEF 訊息可以包含一筆或多筆 NDEF records。Android 也支援不含 NDEF 的標籤，但這類資料可能需要開發者使用較底層的技術介面自行處理。[S03，p0069-181c7b789d；p0070-0795159269；p0071-38b0204d38；p0073-0da52fdc33；p0074-9e26929f4c；p0075-11cee96984；p0076-c9e02948d2]

## 可整合知識

- NDEF 可把資料整理成 message 與 records；讀取到標籤不代表全部資料一定只有一筆 record。[S03，p0070-0795159269；p0071-38b0204d38]
- Android 的 tag dispatch system 會分析標籤並選擇能處理該資料的應用程式。[S03，p0041-01f1a23d3f；p0042-ca7fb5325c；p0043-88d169c245]
- Android 支援非 NDEF 標籤，但官方建議在可行時優先使用 NDEF，因為自行處理其他標籤技術需要更多底層工作。[S03，p0073-0da52fdc33；p0074-9e26929f4c；p0075-11cee96984；p0076-c9e02948d2]

## 既有頁面異動

- 建立 [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)，解釋 message、record 與標籤的關係。
- 更新 [NFC 知識概觀](../overview.md) 和 [Wiki 索引](../index.md)。

## 來源限制

- 這是 Android 開發者文件，著重 Android 應用程式如何處理標籤；它不是所有 NFC 裝置共通行為的完整規格。
- 本頁只摘要入門概念，不展開完整 NDEF 格式欄位或程式碼範例。

## 相關知識

- [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)
- [Android 卡片模擬與 HCE](../concepts/hce-and-secure-element.md)
- [NFC 安全入門](../concepts/nfc-security.md)

## 來源

- Android Developers, [NFC basics](https://developer.android.com/develop/connectivity/nfc/nfc)
- Raw snapshot: `data/raw/S03/7b43c9e109378ce065d2e3583adbf146d1d4877546e0b051c61b0850b8ee426b/source.html`
- SHA-256: `7b43c9e109378ce065d2e3583adbf146d1d4877546e0b051c61b0850b8ee426b`
