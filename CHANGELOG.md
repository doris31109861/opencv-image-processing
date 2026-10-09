# Changelog

## 2026-10-09 — 魚眼程式修正主迴圈並改成 NumPy 向量化

- **內容**：
  - 原本 `camera.py` 的主迴圈其實沒有呼叫 `fisheye_effect`：每秒讀取固定檔案 `savedImage.jpg` 做 `cv2.stylization` 後存檔，與 README 描述的「即時魚眼」不符。改成對每一幀攝影機畫面套用魚眼並顯示，按 s 存檔、q 離開。
  - 新增 `fisheye.py`：保留原本的雙層迴圈版 `fisheye_effect_loop()` 作為比較基準，新增向量化版 `fisheye_maps()`（`np.meshgrid` 一次算整張座標網格，`lru_cache` 讓同尺寸畫面只算一次映射表）與 `fisheye_effect()`。
  - 新增 `benchmark.py`（不需攝影機）：比較兩版的執行時間與輸出差異，CI 自動執行。
- **原因**：讓程式行為與 README 一致；迴圈版每幀要跑數十萬次 Python 迴圈，無法即時。
- **測試**：`py_compile` 通過；速度與結果比較由 CI 執行（見下一筆紀錄）。攝影機部分需實體鏡頭，未實測。

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
