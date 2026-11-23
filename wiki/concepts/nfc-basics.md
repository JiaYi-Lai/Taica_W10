---
id: nfc-basics
title: NFC 基礎概念
type: concept
updated_at: 2026-11-23
sources:
  - S05
  - S08
---

# NFC 基礎概念

## 核心概念

NFC 是近距離無線通訊技術。常見使用方式是把手機或卡片靠近另一個 NFC 裝置或標籤，讓兩者交換少量資料或觸發一個動作。[S05，p0064-32c71d7b8a；p0065-8be7257988；S08，p0037-68507b3450；p0038-d1d275e2d0；p0039-e25553f552]

## 詳細說明

STMicroelectronics 說明 NFC 使用 13.56 MHz，並將可用距離描述為最遠約 10 公分。[S05，p0044-c604cf788c] Android 的平台概覽則說，啟動連線通常需要 4 公分或更近。[S08，p0037-68507b3450；p0038-d1d275e2d0] 兩者是不同來源、不同語境的描述，請參見 [距離說法比較](../comparisons/nfc-distance.md)，不應把單一數字當成任何裝置都保證的距離。

NFC 標籤可讓手機開啟應用程式或顯示相關內容；標籤資料也可能連到網路，因此「觸碰標籤」不等於後續操作完全離線。[S05，p0065-8be7257988] NFC Forum 是相關標準與相容性工作的產業組織之一。[S05，p0046-9a12d49599]

NFC 的用途包括付款、交通、分享資訊和配對裝置等。[S05，p0083-af3c385e28] 不過通訊方式、標籤資料格式、手機作業系統支援，以及支付規格是不同層次；例如支付的進一步說明見 [NFC 與感應式支付](./nfc-and-contactless-payments.md)。

## 相關知識

- [NFC 距離說法比較](../comparisons/nfc-distance.md)
- [NFC 標籤與 NDEF](./ndef-and-tags.md)
- [NFC 運作模式](./nfc-operating-modes.md)
- [NFC 與感應式支付](./nfc-and-contactless-payments.md)

## 來源

- S05, STMicroelectronics: `p0044-c604cf788c`, `p0064-32c71d7b8a`, `p0065-8be7257988`, `p0083-af3c385e28`。
- S08, Android Developers: `p0037-68507b3450`, `p0038-d1d275e2d0`, `p0039-e25553f552`。
