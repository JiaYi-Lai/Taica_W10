---
id: source-s08-android-nfc-overview
title: Android NFC 概觀
type: source
updated_at: 2026-11-23
sources:
  - S08
source_id: S08
---

# Android NFC 概觀

## 來源摘要

Android Developers 將 NFC 描述為短距離無線技術，表示 Android 裝置啟動連線通常需要 4 公分或更近，並可在 NFC 標籤與 Android 裝置、或兩台 Android 裝置之間交換少量資料。[S08，p0037-68507b3450；p0038-d1d275e2d0；p0039-e25553f552]

Android 文件介紹兩種主要操作模式：Reader/Writer（讀寫標籤）和 Card Emulation（手機模擬卡片，供外部讀卡機讀取）。也指出標籤功能由簡單讀寫到內含密碼硬體等複雜型態皆有，而許多 Android API 以 NFC Forum 的 NDEF 為基礎。[S08，p0041-b2ef7d5e95；p0042-192c952178；p0043-76c1fde1f2；p0048-da550b16a7；p0049-3f564abd29；p0051-be9907b3b6；p0052-d9e433da58；p0053-5f01cd4180；p0054-d10fe14ce4]

## 可整合知識

- 4 公分說法是 Android 對其 NFC 使用情境的概述；它與 ST 頁面「最遠 10 公分」的寫法語境不同，Wiki 先並列兩者，不自行判定為規格矛盾。[S08，p0037-68507b3450；p0038-d1d275e2d0]
- Android 文件列出的兩種主要模式是 Android 平台概述，不代表所有 NFC 標準或裝置只存在兩種模式。[S08，p0049-3f564abd29；p0051-be9907b3b6；p0053-5f01cd4180]
- NFC 標籤的能力有簡有繁；只看到「NFC 標籤」不能假設它一定支援相同功能。[S08，p0041-b2ef7d5e95；p0042-192c952178；p0043-76c1fde1f2]

## 既有頁面異動

- 更新 [NFC 基礎概念](../concepts/nfc-basics.md)、[NFC 距離說法比較](../comparisons/nfc-distance.md) 和 [NFC 運作模式](../concepts/nfc-operating-modes.md)。
- 更新 [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)、[NFC 知識概觀](../overview.md) 和 [Wiki 索引](../index.md)。

## 來源限制

- 本頁說明 Android 平台概覽，不應直接代表其他平台的支援狀態。
- 距離描述是「typically」啟動連線所需的距離，不是保證每個裝置在所有環境下都達到的測量值。

## 相關知識

- [NFC 基礎概念](../concepts/nfc-basics.md)
- [NFC 距離說法比較](../comparisons/nfc-distance.md)
- [NFC 運作模式](../concepts/nfc-operating-modes.md)
- [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)

## 來源

- Android Developers, [NFC overview](https://developer.android.com/develop/connectivity/nfc)
- Raw snapshot: `data/raw/S08/9faaf8b8cde913eddabb7fad9e603f593dd1108473d59c332fb9b256b8f0ad73/source.html`
- SHA-256: `9faaf8b8cde913eddabb7fad9e603f593dd1108473d59c332fb9b256b8f0ad73`
