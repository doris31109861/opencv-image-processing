# Image Processing with OpenCV (C++ / Python)

> 數位影像處理、感測定位平台課程作業｜逢甲大學資訊工程學系

[中文](#中文) | [English](#english)

---

## 中文

逐像素自己實作影像處理演算法，了解 OpenCV 函式背後的原理，並用 OpenCV 做幾個小應用。

| 資料夾 | 語言 | 內容 |
|---|---|---|
| `bilinear-resize/` | C++ | **自己實作雙線性內插**，將影像縮放 0.1–2 倍；以加權 RGB 轉灰階；疊加簽名並去除白色背景 |
| `fisheye-camera/` | Python | 擷取攝影機畫面，以自訂極座標映射搭配 `cv2.remap` 做出**魚眼效果** |
| `snake-game/` | Python | 完全用 OpenCV 繪圖函式做的貪吃蛇，含鍵盤控制、碰撞偵測與計分 |

### 編譯與執行

```bash
# C++（需要 OpenCV 4）
cd bilinear-resize
g++ main.cpp -o resize `pkg-config --cflags --libs opencv4`
./resize            # 輸入 0.1 到 2 之間的縮放倍率

# Python
pip install opencv-python numpy
python fisheye-camera/camera.py
python snake-game/snake.py
```

### 學到的東西

- 內插與幾何轉換的數學原理，不依賴內建函式自己實作
- 以 `Mat::at<Vec3b>` 直接存取像素、處理色彩空間
- 用 OpenCV 做即時影像與互動式應用

---

## English

Image processing algorithms written pixel by pixel to understand how OpenCV works internally, plus some small OpenCV applications.

| Folder | Language | What it does |
|---|---|---|
| `bilinear-resize/` | C++ | Resizes an image 0.1–2× with **hand-written bilinear interpolation**, converts to grayscale with a weighted RGB sum, and overlays a signature with white-background removal |
| `fisheye-camera/` | Python | Applies a **fisheye distortion** to webcam frames using a custom polar-coordinate mapping and `cv2.remap` |
| `snake-game/` | Python | A Snake game drawn entirely with OpenCV primitives, with keyboard control, collision detection and scoring |

### Build & Run

```bash
cd bilinear-resize
g++ main.cpp -o resize `pkg-config --cflags --libs opencv4`
./resize
pip install opencv-python numpy
python fisheye-camera/camera.py
python snake-game/snake.py
```

### What I learned

- The math behind interpolation and geometric transforms, implemented without built-in helpers
- Direct pixel access with `Mat::at<Vec3b>` and working with color spaces
- Building real-time video and interactive apps with OpenCV
