---
id: source-s09-android-nfc-security
title: Android NFC 通訊風險與資料驗證
type: source
updated_at: 2026-11-23
sources:
  - S09
source_id: S09
---

# Android NFC 通訊風險與資料驗證

## 來源摘要

Android Developers 的安全文件指出，NFC 等無線通訊可能遭到攔截，攻擊者也可能偽裝通訊端點；風險取決於應用程式交換的資料及實作方式。[S09，p0065-74133d6c5f；p0066-07f7244aca；p0069-db0a461406；p0070-1e97924b50；p0071-4a14066a0a；p0072-e26247f9d2]

文件針對 NFC 提到兩種 Android 應用風險：惡意應用程式可能註冊相似的 intent filter，試圖接收標籤資料；未驗證 NDEF 內容的應用程式，可能把不預期資料交給其他元件而造成錯誤行為。[S09，p0247-6b815e14b0；p0248-a170c1e3f3；p0249-a37a607bb4；p0250-fdbd78df3b；p0251-6230d1532d；p0265-5bf2ae56e1；p0271-dc51465c11；p0272-df0537b725；p0273-c1a07eea92；p0274-12d53c7dae]

## 可整合知識

- Android 的 mitigations 包括只處理應用程式真正需要的標籤類型、在可能情況下使用 Android Application Record（AAR），以及在把 NDEF 資料交給其他應用元件前檢查格式與內容。[S09，p0258-2792468888；p0259-3ce22736cb；p0260-8a079342f0；p0261-1552c9598e；p0276-3b93dac3c3；p0277-e9ad686162；p0278-fb0d19f0e3]
- NFC 是通訊管道；此來源討論的是應用程式如何安全處理資料，不表示每個 NFC 標籤都會造成風險或 NFC 本身等同於安全機制。[S09，p0065-74133d6c5f；p0069-db0a461406；p0070-1e97924b50]

## 既有頁面異動

- 建立 [NFC 安全入門](../concepts/nfc-security.md)，把來源明確限定在 Android 應用程式情境。
- 更新 [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)、[NFC 知識概觀](../overview.md) 和 [Wiki 索引](../index.md)。

## 來源限制

- 文件討論 Android 開發者風險和緩解方式，不是 NFC 標準的完整威脅模型，也不是一般消費者防詐指引。
- AAR 和 intent filter 是 Android 應用機制；不可把它們描述成所有 NFC 裝置皆有的通用防護。

## 相關知識

- [NFC 安全入門](../concepts/nfc-security.md)
- [NFC 標籤與 NDEF](../concepts/ndef-and-tags.md)
- [NFC 基礎概念](../concepts/nfc-basics.md)

## 來源

- Android Developers, [Insecure machine-to-machine communication setup: NFC risks](https://developer.android.com/privacy-and-security/risks/insecure-machine-to-machine)
- Raw snapshot: `data/raw/S09/4361a4f78beb41ed679fe9ffcf057db02d5da5eb9810dae793d650fdf59d6d9b/source.html`
- SHA-256: `4361a4f78beb41ed679fe9ffcf057db02d5da5eb9810dae793d650fdf59d6d9b`
