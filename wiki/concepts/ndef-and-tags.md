---
id: ndef-and-tags
title: NFC 標籤與 NDEF
type: concept
updated_at: 2026-11-23
sources:
  - S03
  - S08
  - S09
---

# NFC 標籤與 NDEF

## 核心概念

NFC 標籤是可以被相容裝置讀取或互動的媒介；NDEF 是 NFC Forum 定義的一種資料格式。Android 文件描述 NDEF message 可由一筆或多筆 NDEF records 組成。[S03，p0069-181c7b789d；p0070-0795159269；p0071-38b0204d38]

## 詳細說明

標籤的能力有簡有繁。Android 概覽提到簡單標籤可供讀寫，也有更複雜、包含額外功能或密碼硬體的標籤。[S08，p0041-b2ef7d5e95；p0042-192c952178；p0043-76c1fde1f2]

Android 讀取 NDEF 標籤時，系統會判讀資料並將它交給可處理該資料的應用程式。Android 也支援部分非 NDEF 標籤，但其處理方式可能需要更底層的應用程式工作。[S03，p0041-01f1a23d3f；p0042-ca7fb5325c；p0043-88d169c245；p0073-0da52fdc33；p0074-9e26929f4c；p0075-11cee96984；p0076-c9e02948d2]

標籤資料應視為輸入資料，而不是可信指令。Android 安全文件建議在把 NDEF 內容交給其他應用程式元件前，檢查資料格式與預期內容。[S09，p0265-5bf2ae56e1；p0271-dc51465c11；p0272-df0537b725；p0276-3b93dac3c3；p0277-e9ad686162；p0278-fb0d19f0e3]

## 相關知識

- [NFC 基礎概念](./nfc-basics.md)
- [NFC 安全入門](./nfc-security.md)
- [Android NFC 基礎與 NDEF 來源摘要](../sources/S03-android-nfc-basics.md)

## 來源

- S03: `p0069-181c7b789d`, `p0070-0795159269`, `p0071-38b0204d38`, `p0041-01f1a23d3f`, `p0042-ca7fb5325c`, `p0043-88d169c245`。
- S08: `p0041-b2ef7d5e95`, `p0042-192c952178`, `p0043-76c1fde1f2`。
- S09: `p0265-5bf2ae56e1`, `p0271-dc51465c11`, `p0276-3b93dac3c3`, `p0277-e9ad686162`, `p0278-fb0d19f0e3`。
