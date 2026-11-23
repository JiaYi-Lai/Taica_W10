---
id: nfc-operating-modes
title: NFC 運作模式與平台支援
type: concept
updated_at: 2026-11-23
sources:
  - S05
  - S08
---

# NFC 運作模式與平台支援

## 核心概念

「NFC 有哪些模式」要看是在說技術用途分類，還是在說特定手機平台提供哪些功能。不能把一個平台的功能清單當成所有 NFC 裝置的完整清單。

## 詳細說明

STMicroelectronics 的概覽列出 Reader、Card Emulation、Peer-to-Peer 和 Charging 等用途類別。[S05，p0067-fbfd1efc2d；p0068-0bb66a660a；p0069-17ff8c57d3；p0070-2f4120ace3；p0071-f06f4ff6f3；p0072-97e56a99df]

Android 概覽則特別列出 Android 裝置的兩種主要模式：Reader/Writer 可讀寫被動標籤；Card Emulation 讓 Android 裝置像卡片一樣被外部讀卡機讀取。[S08，p0049-3f564abd29；p0050-a949b54b13；p0051-be9907b3b6；p0052-d9e433da58；p0053-5f01cd4180；p0054-d10fe14ce4]

Android 的 HCE 是 Card Emulation 的一種 Android 實作方式。它的資料路徑和使用 Secure Element 的路徑不同，細節見 [Android 卡片模擬與 HCE](./hce-and-secure-element.md)。

## 相關知識

- [NFC 基礎概念](./nfc-basics.md)
- [Android 卡片模擬與 HCE](./hce-and-secure-element.md)
- [NFC 標籤與 NDEF](./ndef-and-tags.md)

## 來源

- S05: `p0067-fbfd1efc2d`–`p0072-97e56a99df`。
- S08: `p0049-3f564abd29`–`p0054-d10fe14ce4`。
