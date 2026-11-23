# NFC 運作模式

「NFC 模式」描述裝置在一次互動中扮演什麼角色。不同作業系統與裝置提供的功能不一定相同，不能只因為裝置有 NFC，就推論它支援所有模式。

## Reader/Writer

在 Reader/Writer 模式中，NFC 裝置讀取或寫入被動式標籤。Android 概覽也用貼紙作為例子。〔S08，p0051–p0052〕

## Card Emulation

在 Card Emulation 模式中，裝置表現得像一張非接觸式卡片，外部 Reader 可以讀取它。Android 的 HCE 文件說明，Android 4.4 起提供不需 Secure Element 的卡片模擬方式；這是 Android 平台的實作說明，不能直接推廣到所有手機。〔S08，p0053–p0055；S04，p0041–p0043〕

## 裝置對裝置交換

Android NFC 概覽提到，少量資料可在 NFC 標籤與 Android 裝置間交換，也可在兩台 Android 裝置間交換。這可作為 Peer-to-Peer（裝置對裝置）情境的入門例子；但這份文件沒有證明所有平台或現代手機都提供相同的 Peer-to-Peer 功能。〔S08，p0039–p0040〕

## 來源

- [S08 — Android Developers NFC overview](https://developer.android.com/develop/connectivity/nfc)（p0039–p0055）
- [S04 — Android Developers HCE overview](https://developer.android.com/develop/connectivity/nfc/hce)（p0041–p0043）
