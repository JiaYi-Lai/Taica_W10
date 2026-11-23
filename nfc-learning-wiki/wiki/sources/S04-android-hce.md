---
id: source-s04-android-hce
title: Android 主機卡片模擬（HCE）
type: source
updated_at: 2026-11-23
sources:
  - S04
source_id: S04
---

# Android 主機卡片模擬（HCE）

## 來源摘要

Android Developers 說明 Android 卡片模擬的兩種資料路徑：使用 Secure Element（安全元件）時，讀卡機資料會被導向安全元件，由它與終端通訊；使用 Host-based Card Emulation（HCE，主機卡片模擬）時，資料會導向裝置的主機 CPU，而不是安全元件。[S04，p0048-4237a45731；p0049-d04d2d6598；p0050-861782142e；p0051-28d326ac29；p0054-3689f83a29；p0059-cae55ff30a；p0060-7c624ecd0f]

## 可整合知識

- Card Emulation 是讓手機以卡片的方式回應外部 NFC 讀卡機。[S04，p0043-7eadf7ac0c]
- HCE 與 Secure Element 的差別，首先是交易資料被路由到不同的裝置元件；不能只憑這一點推論哪一種支付方案整體上更安全。[S04，p0048-4237a45731；p0054-3689f83a29；p0059-cae55ff30a；p0060-7c624ecd0f]
- Android HCE 以 APDU 和 AID 等技術機制選擇服務；這些是開發者層級細節，初學者理解概念時不必先記住。[S04，p0075-81c66c4f1f；p0076-7647ac317b；p0095-2d2c637e0d]

## 既有頁面異動

- 建立 [Android 卡片模擬與 HCE](../concepts/hce-and-secure-element.md)，區分 Secure Element 路徑和 HCE 路徑。
- 更新 [NFC 運作模式](../concepts/nfc-operating-modes.md) 和 [NFC 知識概觀](../overview.md)。

## 來源限制

- 本來源說明 Android 平台的實作方式；其他手機作業系統或支付產品可能使用不同實作。
- 本頁保留來源對資料路由的描述，不從「經過 CPU 或 Secure Element」自行推導支付安全等級。

## 相關知識

- [Android 卡片模擬與 HCE](../concepts/hce-and-secure-element.md)
- [NFC 運作模式](../concepts/nfc-operating-modes.md)
- [NFC 與感應式支付](../concepts/nfc-and-contactless-payments.md)

## 來源

- Android Developers, [Host-based card emulation overview](https://developer.android.com/develop/connectivity/nfc/hce)
- Raw snapshot: `data/raw/S04/45220405d81f3fe1251810eaa26700064b18b3e0a178eda32506cfd8146a09c1/source.html`
- SHA-256: `45220405d81f3fe1251810eaa26700064b18b3e0a178eda32506cfd8146a09c1`
