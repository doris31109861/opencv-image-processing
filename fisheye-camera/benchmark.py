"""
benchmark.py — 比較魚眼映射的迴圈版與 NumPy 向量化版：結果是否一致、速度差多少

不需要攝影機，用 bilinear-resize/tiger.jpeg 放大成常見的攝影機尺寸 640×480 來測。
用法：python fisheye-camera/benchmark.py [--save docs/fisheye]
"""

import argparse
import time
from pathlib import Path

import cv2
import numpy as np

from fisheye import fisheye_effect, fisheye_effect_loop, fisheye_maps

ROOT = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("--save", help="把原圖與魚眼結果存到這個資料夾")
args = ap.parse_args()

img = cv2.imread(str(ROOT / "bilinear-resize" / "tiger.jpeg"))
img = cv2.resize(img, (640, 480))

t0 = time.perf_counter()
slow = fisheye_effect_loop(img)
t_loop = time.perf_counter() - t0

fisheye_maps.cache_clear()                 # 確保向量化版也要從頭算映射表
t0 = time.perf_counter()
fast = fisheye_effect(img)
t_vec = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(10):
    fisheye_effect(img)                    # 之後每一幀只需 remap（映射表已快取）
t_cached = (time.perf_counter() - t0) / 10

# 向量化的三角函數與逐一計算可能有最後一位的浮點誤差，比較像素最大差值
max_diff = int(np.abs(slow.astype(int) - fast.astype(int)).max())
same = max_diff <= 1
print(f"迴圈版：{t_loop * 1000:.1f} ms")
print(f"向量化版（含計算映射表）：{t_vec * 1000:.1f} ms，快 {t_loop / t_vec:.0f} 倍")
print(f"向量化版（映射表已快取，每幀）：{t_cached * 1000:.2f} ms，快 {t_loop / t_cached:.0f} 倍")
print(f"兩種輸出的像素最大差值：{max_diff}（<= 1 視為相同）")

if args.save:
    out = Path(args.save)
    out.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out / "input.png"), img)
    cv2.imwrite(str(out / "fisheye.png"), fast)

if not same:
    raise SystemExit(1)
