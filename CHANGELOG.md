# Changelog

## 2026-10-09 — 補上檔案說明註解、更正魚眼程式來源

- **內容**：`camera.py`、`snake.py` 開頭加上用途說明；`camera.py` 註明 `fisheye_effect()` 取自課程講義範例（Ch14 `fisheye_effect.py`），自己的部分是接上攝影機做即時處理；README 的魚眼說明同步更正。
- **原因**：讓程式來源與自己的貢獻清楚，面試時不會被問倒。
- **測試**：只改註解與 README；兩個檔案通過 `py_compile`。

## 2026-10-09 — README 加入處理前後對照圖

- **內容**：把 CI 實際執行 `bilinear-resize --save` 的輸出（加簽名原圖、灰階、0.5x、1.5x）放到 `docs/bilinear-resize/`，README 新增對照表；編譯指令更新為新的執行檔名與參數。
- **原因**：讓人不用編譯就能看到演算法效果。
- **測試**：圖片來自 CI 實際執行結果。

## 2026-10-09 — bilinear-resize 加入命令列參數與存檔模式、CI

- **內容**：`main.cpp` 開頭補上用途與用法說明；縮放倍率可由命令列指定（`./bilinear_resize 1.5`），加 `--save` 時不開視窗、改把加簽名原圖／灰階／縮放結果存到 `output/`；未給參數時維持原本互動輸入＋視窗顯示的行為。新增 GitHub Actions：在 Ubuntu 安裝 OpenCV、編譯並以 0.5x、1.5x 實際執行。
- **原因**：方便沒有螢幕的環境執行，也能產生處理前後的對照圖放進 README。
- **測試**：本機沒有 OpenCV 開發環境；GitHub Actions（ubuntu-latest + libopencv-dev）實測編譯成功，0.5x 輸出 92×80、1.5x 輸出 277×240。
