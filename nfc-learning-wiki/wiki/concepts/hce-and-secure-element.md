---
id: hce-and-secure-element
title: Android 卡片模擬與 HCE
type: concept
updated_at: 2026-11-23
sources:
  - S04
---

# Android 卡片模擬與 HCE

## 核心概念

卡片模擬是讓手機在讀卡機看來像一張 NFC 卡片。Android 文件描述的 HCE（Host-based Card Emulation，主機卡片模擬）會把讀卡機資料送到手機主機 CPU；使用 Secure Element 的卡片模擬則把資料送到安全元件。[S04，p0043-7eadf7ac0c；p0048-4237a45731；p0050-861782142e；p0051-28d326ac29；p0054-3689f83a29；p0059-cae55ff30a；p0060-7c624ecd0f]

## 詳細說明

可以把它想成兩種不同的「卡片工作位置」：一種由手機內的安全元件直接和讀卡機溝通；另一種由 Android 主機上的 HCE 服務處理資料。Android 文件進一步使用 APDU 和 AID 來說明 HCE 服務如何和讀卡機選擇、交換資料。[S04，p0075-81c66c4f1f；p0076-7647ac317b；p0095-2d2c637e0d；p0159-ed1df60fb2；p0167-07b70cee86]

這些細節是 Android 平台文件的描述，不能直接推論所有手機都以同一方式實作，也不能只根據資料路徑判定支付方案的整體安全性。

## 相關知識

- [NFC 運作模式與平台支援](./nfc-operating-modes.md)
- [NFC 與感應式支付](./nfc-and-contactless-payments.md)
- [Android HCE 來源摘要](../sources/S04-android-hce.md)

## 來源

- S04: `p0043-7eadf7ac0c`, `p0048-4237a45731`, `p0054-3689f83a29`, `p0059-cae55ff30a`, `p0060-7c624ecd0f`, `p0075-81c66c4f1f`, `p0076-7647ac317b`。
