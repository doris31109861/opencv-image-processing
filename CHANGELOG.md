# Changelog

## 2026-10-09 — bilinear-resize 加入命令列參數與存檔模式、CI

- **內容**：`main.cpp` 開頭補上用途與用法說明；縮放倍率可由命令列指定（`./bilinear_resize 1.5`），加 `--save` 時不開視窗、改把加簽名原圖／灰階／縮放結果存到 `output/`；未給參數時維持原本互動輸入＋視窗顯示的行為。新增 GitHub Actions：在 Ubuntu 安裝 OpenCV、編譯並以 0.5x、1.5x 實際執行。
- **原因**：方便沒有螢幕的環境執行，也能產生處理前後的對照圖放進 README。
- **測試**：本機沒有 OpenCV 開發環境；編譯與執行由 GitHub Actions 驗證（結果見下一筆紀錄）。
