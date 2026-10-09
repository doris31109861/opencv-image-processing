"""
fisheye.py — 魚眼映射的兩種實作：原本的雙層迴圈版，以及 NumPy 向量化版

fisheye_effect_loop() 取自課程講義範例（數位影像處理 Ch14 fisheye_effect.py）：
以畫面中心為原點換成極座標 (r, θ)，把半徑改成 r²/R 後用 cv2.remap 重新取樣。
逐像素用 Python 迴圈計算，640×480 的畫面要跑 30 萬次，速度很慢。

fisheye_maps() 用 NumPy 一次對整張座標網格做同樣的運算（結果與迴圈版相同），
而且同樣大小的畫面只需計算一次映射表，之後每一幀只要呼叫 cv2.remap。
"""

from functools import lru_cache

import cv2
import numpy as np


def fisheye_effect_loop(f):
    """原本的逐像素迴圈版（保留作為比較基準）。"""
    nr, nc = f.shape[:2]
    map_x = np.zeros([nr, nc], dtype='float32')
    map_y = np.zeros([nr, nc], dtype='float32')
    x0, y0 = nr // 2, nc // 2
    R = np.sqrt(nr ** 2 + nc ** 2) / 2
    for x in range(nr):
        for y in range(nc):
            r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
            if r == 0:
                theta = 0
            else:
                theta = np.arccos((x - x0) / r)
            r = (r * r) / R
            if y - y0 < 0:
                theta = -theta
            map_x[x, y] = np.clip(y0 + r * np.sin(theta), 0, nc - 1)
            map_y[x, y] = np.clip(x0 + r * np.cos(theta), 0, nr - 1)
    return cv2.remap(f, map_x, map_y, cv2.INTER_CUBIC)


@lru_cache(maxsize=4)
def fisheye_maps(nr, nc):
    """向量化計算 (nr, nc) 大小畫面的映射表；結果會被快取，同尺寸只算一次。"""
    x0, y0 = nr // 2, nc // 2
    R = np.sqrt(nr ** 2 + nc ** 2) / 2
    # X、Y 分別是每個像素的列、行座標（形狀都是 nr × nc）
    X, Y = np.meshgrid(np.arange(nr), np.arange(nc), indexing='ij')
    dx, dy = X - x0, Y - y0
    r = np.sqrt(dx ** 2 + dy ** 2)
    # r == 0（中心點）時 θ = 0，其餘 θ = arccos(dx / r)；用 where 避免除以 0
    cos_arg = np.divide(dx, r, out=np.zeros_like(r), where=r != 0)
    theta = np.where(r == 0, 0.0, np.arccos(cos_arg))
    theta = np.where(dy < 0, -theta, theta)      # 左半邊角度取負
    r2 = (r * r) / R                             # 魚眼：半徑平方後除以 R
    map_x = np.clip(y0 + r2 * np.sin(theta), 0, nc - 1).astype('float32')
    map_y = np.clip(x0 + r2 * np.cos(theta), 0, nr - 1).astype('float32')
    return map_x, map_y


def fisheye_effect(f):
    """向量化版：與 fisheye_effect_loop 結果相同。"""
    map_x, map_y = fisheye_maps(*f.shape[:2])
    return cv2.remap(f, map_x, map_y, cv2.INTER_CUBIC)
