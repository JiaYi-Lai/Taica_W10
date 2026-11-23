---
id: nfc-security
title: NFC 安全入門
type: concept
updated_at: 2026-11-23
sources:
  - S09
---

# NFC 安全入門

## 核心概念

NFC 是通訊方式；應用程式仍需要安全處理收到的資料。Android 安全文件指出，無線資料可能被攔截，應用程式也可能收到經過修改或不符合預期的資料。[S09，p0065-74133d6c5f；p0069-db0a461406；p0070-1e97924b50；p0071-4a14066a0a]

## 詳細說明

Android 文件列出 NFC 相關的 Android 應用風險，包括惡意應用程式註冊相似 intent filters，以及應用程式未驗證 NDEF 內容而處理惡意資料。[S09，p0247-6b815e14b0；p0248-a170c1e3f3；p0249-a37a607bb4；p0250-fdbd78df3b；p0251-6230d1532d；p0254-6e0b14c0f9；p0271-dc51465c11；p0272-df0537b725；p0273-c1a07eea92；p0274-12d53c7dae]

對開發者而言，來源建議在把 NDEF 內容交給其他應用元件前，確認資料格式和內容符合預期；若無線傳輸敏感資料，應考慮應用層加密等保護方式。[S09，p0077-9d9539ff7b；p0078-e50a8a9947；p0079-a0d90c4c53；p0276-3b93dac3c3；p0277-e9ad686162；p0278-fb0d19f0e3]

這些是 Android 應用程式的風險和建議，不等於每個 NFC 使用情境都會遇到相同風險，也不代表 NFC 傳輸本身提供完整的安全保證。

## 相關知識

- [NFC 標籤與 NDEF](./ndef-and-tags.md)
- [NFC 基礎概念](./nfc-basics.md)
- [Android NFC 安全來源摘要](../sources/S09-android-nfc-security.md)

## 來源

- S09: `p0065-74133d6c5f`–`p0072-e26247f9d2`, `p0077-9d9539ff7b`–`p0079-a0d90c4c53`, `p0247-6b815e14b0`–`p0261-1552c9598e`, `p0271-dc51465c11`–`p0278-fb0d19f0e3`。
