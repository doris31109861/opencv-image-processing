"""
camera.py — 即時魚眼特效：從攝影機逐張擷取畫面，套用魚眼映射後顯示

魚眼映射在 fisheye.py（原理取自課程講義範例，改寫成 NumPy 向量化並快取映射表）。
操作：按 s 存下目前畫面（檔名為時間），按 q 離開。
"""

import time

import cv2

from fisheye import fisheye_effect

cap = cv2.VideoCapture(0)  # 0 為預設攝影機

while True:
    # 從攝影機擷取一張影像
    ret, frame = cap.read()
    if not ret:
        print("讀不到攝影機畫面")
        break

    # 套用魚眼效果（同尺寸的映射表只在第一幀計算一次）
    output = fisheye_effect(frame)
    cv2.imshow('fisheye', output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # 以目前時間命名存檔
        filename = time.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
        cv2.imwrite(filename, output)
        print("saved", filename)
    elif key == ord('q'):
        break

# 釋放攝影機並關閉視窗
cap.release()
cv2.destroyAllWindows()
