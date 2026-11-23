---
id: source-s06-emv-contactless-chip
title: EMV 感應式晶片支付
type: source
updated_at: 2026-11-23
sources:
  - S06
source_id: S06
---

# EMV 感應式晶片支付

## 來源摘要

EMVCo 的官方介紹說明，EMV Contactless Chip 用於店內感應式支付，支援感應式晶片卡及具 NFC 功能的行動裝置與收款終端機互動。EMVCo 將支付流程相關要求放在 EMV Chip、EMV Contactless 與 EMV Contactless Kernel 規格中，並提供產品測試、核准與評估流程。[S06，p0064-4f8a50ce33；p0065-abeb47faea；p0066-54224a6607]

頁面也描述每筆交易會產生一次性安全碼以協助防範詐欺。[S06，p0064-4f8a50ce33] 這是 EMVCo 對其支付技術的說明，不能推論為 NFC 通訊本身會替所有應用提供相同的安全保護。

## 可整合知識

- NFC 可作為行動裝置與收款終端間的近距離通訊方式；EMV Contactless 則描述支付產品如何依 EMV 規格處理感應式交易。[S06，p0064-4f8a50ce33；p0065-abeb47faea]
- 收款終端的 contactless kernel 是支付應用處理感應式交易的一組功能，並有對應的 EMV 規格及評估流程。[S06，p0139-1ba79f3cff]
- 來源聚焦於 EMV 支付規格與其認證／評估，不是 NFC 所有用途或所有支付系統的完整技術說明。

## 既有頁面異動

- 新增 [NFC 與感應式支付](../concepts/nfc-and-contactless-payments.md)，將 NFC 通訊與 EMV 支付流程分開說明。
- 更新 [知識概觀](../overview.md) 與 [Wiki 索引](../index.md)，加入已由 S06 支持的支付主題。

## 來源限制

- 這是 EMVCo 的概覽頁，不等同於完整 EMV 規格文件；本摘要不推導規格中的底層訊息、密碼流程或認證細節。
- 「一次性安全碼」的描述只適用於來源所述的 EMV 感應式支付脈絡，不能當成所有 NFC 標籤、裝置或應用的通用特性。
- 本地快照是 2026-11-23 擷取的 HTML。原始快照以 SHA-256 版本化保存，正文段落保留可追溯 ID。

## 相關知識

- [NFC 與感應式支付](../concepts/nfc-and-contactless-payments.md)
- [知識概觀](../overview.md)

## 來源

- EMVCo, [EMV Contactless Chip](https://www.emvco.com/emv-technologies/emv-contactless-chip/)
- Raw snapshot: `data/raw/S06/b62441f6eeb003325659fe38e576b6cb9f3fcd6f0ba8613302b3502c5d6b7d44/source.html`
- SHA-256: `b62441f6eeb003325659fe38e576b6cb9f3fcd6f0ba8613302b3502c5d6b7d44`
