# NFC 運作原理

可以把 NFC 想成一場很短的近距離對話：一端建立電磁場，附近的裝置依照共同協定回應。它適合「靠近後快速交換一點資料」，不是拿來取代 Wi-Fi 或行動網路。

## 頻率與距離

STMicroelectronics 的說明以 13.56 MHz 為基礎，並稱相容裝置可在最遠約 10 公分內通訊。Android 概覽則說 NFC 通常需要在 4 公分以內才開始連線。兩者描述情境不同；閱讀距離數字時要連同來源與用途一起看，不應視為每台裝置都保證達到的距離。〔S05，p0044；S08，p0038〕

## 近距離如何交換資料？

ST 描述 Reader/Writer 會送出電磁場；範圍內的裝置偵測到訊號後，依設定的協定回傳資料。這說明 NFC 互動需要裝置靠近並遵循通訊規則。〔S05，p0087〕

## 和 Wi-Fi 有什麼不同？

NFC 本身提供近距離的連線與資料交換。ST 指出這種連線不依賴 Wi-Fi、4G 或 LTE；因此 NFC 常用來開始一個快速互動，而長距離網路連線是另一件事。〔S05，p0045〕

## 來源

- [S05 — STMicroelectronics NFC technology resources](https://www.st.com/content/st_com/en/support/learning/essentials-and-insights/connectivity/nfc.html)（p0044、p0045、p0087）
- [S08 — Android Developers NFC overview](https://developer.android.com/develop/connectivity/nfc)（p0038）
