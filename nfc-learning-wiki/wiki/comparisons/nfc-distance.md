---
id: nfc-distance
title: NFC 距離說法比較
type: comparison
updated_at: 2026-11-23
sources:
  - S05
  - S08
---

# NFC 距離說法比較

## 核心概念

不同官方來源用不同方式描述 NFC 距離：STMicroelectronics 說兩個相容裝置最遠可相距 10 公分；Android 概覽說 Android NFC 啟動連線通常需要 4 公分或更近。[S05，p0044-c604cf788c；S08，p0037-68507b3450；p0038-d1d275e2d0]

## 詳細說明

| 來源 | 原文描述 | 應如何理解 |
|---|---|---|
| S05 STMicroelectronics | 相容裝置「up to 10 centimeters apart」 | 這是該學習頁的 NFC 概述說法。 |
| S08 Android Developers | Android NFC 啟動連線「typically ... 4 cm or less」 | 這是 Android 平台的常見連線距離描述。 |

目前不能只靠這兩段文字判定它們互相矛盾：一段說最遠距離，另一段說 Android 裝置通常啟動連線的距離。也不能把 10 公分當成所有手機、標籤和環境的保證值。若需要標準層級的定義，仍須取得 NFC Forum 的相關正式資料；目前候選來源 S01 因 TLS 驗證失敗而未成功擷取。[S05，p0044-c604cf788c；S08，p0037-68507b3450；p0038-d1d275e2d0]

## 相關知識

- [NFC 基礎概念](../concepts/nfc-basics.md)
- [STMicroelectronics 來源摘要](../sources/S05-st-nfc.md)
- [Android NFC 概觀來源摘要](../sources/S08-android-nfc-overview.md)

## 來源

- S05: `p0044-c604cf788c`。
- S08: `p0037-68507b3450`, `p0038-d1d275e2d0`。
