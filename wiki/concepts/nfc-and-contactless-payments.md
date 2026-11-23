---
id: nfc-and-contactless-payments
title: NFC 與感應式支付
type: concept
updated_at: 2026-11-23
sources:
  - S05
  - S06
---

# NFC 與感應式支付

## 核心概念

在感應式刷卡或手機付款時，NFC 是裝置與收款終端近距離互動的一種通訊方式；EMV Contactless 則是支付領域的一組規格，說明支付卡片、行動裝置和收款終端如何處理感應式交易。兩者有關聯，但不是同一件事。[S06，p0064-4f8a50ce33；p0065-abeb47faea]

## 詳細說明

EMVCo 表示，EMV Contactless 支援店內感應式晶片卡及具 NFC 功能的行動裝置。消費者可將裝置靠近或輕觸收款終端完成交易；相關規格共同界定晶片與終端如何溝通和處理交易。[S06，p0064-4f8a50ce33；p0065-abeb47faea]

可以先用這個簡化方式理解：**NFC 負責近距離通訊；EMV 規格描述支付交易如何被處理。** 這只是入門層次的區分，實際支付系統仍包含來源未在此頁完整說明的裝置、支付網路及驗證流程。

EMVCo 頁面提到每筆交易會產生一次性安全碼以協助防範詐欺。[S06，p0064-4f8a50ce33] 這項說明屬於 EMV 支付脈絡，不應擴大解讀成 NFC 技術本身保證所有傳輸或應用安全。

STMicroelectronics 也把行動支付列為 NFC 的常見用途之一。[S05，p0083-af3c385e28] 這描述的是 NFC 可用於支付的情境；EMVCo 的規格頁則補充支付產品如何處理感應式交易。兩份來源描述不同層次，不能把它們混成一套規格。

## 相關知識

- [EMV 感應式晶片支付來源摘要](../sources/S06-emv-contactless-chip.md)
- [STMicroelectronics NFC 技術概覽](../sources/S05-st-nfc.md)
- [NFC 基礎概念](./nfc-basics.md)
- [知識概觀](../overview.md)

## 來源

- S06, EMVCo, [EMV Contactless Chip](https://www.emvco.com/emv-technologies/emv-contactless-chip/)
  - `p0064-4f8a50ce33`：感應式支付裝置、終端及一次性安全碼。
  - `p0065-abeb47faea`：EMV 規格對晶片與終端通訊及交易處理的涵蓋範圍。
  - `p0139-1ba79f3cff`：收款終端 contactless kernel 的用途。
- S05: `p0083-af3c385e28`：NFC 支付與其他常見使用情境。
