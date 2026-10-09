import cv2
import numpy as np
import random

# 設定視窗大小
window_width = 650
window_height = 400

# 設定貪吃蛇線段寬度和長度
snake_width = 5
snake_length = 10

# 設定紅色圓點大小
dot_size = 4

# 設定遊戲結束字體和大小
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 1

# 初始化貪吃蛇的位置和方向
snake_x = window_width // 2
snake_y = window_height // 2
snake_dx = snake_width
snake_dy = 0

# 初始化紅色圓點的位置
dot_x = random.randint(0, window_width - dot_size)
dot_y = random.randint(0, window_height - dot_size)

# 初始化貪吃蛇身體的位置
snake_body = [(snake_x - i * snake_width, snake_y) for i in range(snake_length)]

# 計算分數
score = 0

# 建立 OpenCV 視窗
cv2.namedWindow("11102_1_D1051121曾苔湘")

# 遊戲循環
while True:
    # 建立黑色背景
    img = np.zeros((window_height, window_width, 3), np.uint8)

    # 畫出貪吃蛇身體
    for i in range(snake_length):
        cv2.circle(img, snake_body[i], snake_width, (255, 255, 255), -1)

    # 畫出紅色圓點
    cv2.circle(img, (dot_x, dot_y), dot_size, (0, 0, 255), -1)

    # 顯示分數
    cv2.putText(img, "Score: {}".format(score), (10, 50), font, font_size, (255, 255, 255), 2)

    # 顯示畫面
    cv2.imshow("11102_1_D1051121曾苔湘", img)

    # 等待按鍵輸入
    key = cv2.waitKey(100)

    # 根據按鍵輸入更新貪吃蛇方向
    if key == ord('w') or key == ord('W'):
        snake_dx = 0
        snake_dy = -snake_width
    elif key == ord('a') or key == ord('A'):
        snake_dx = -snake_width
        snake_dy = 0
    elif key == ord('d') or key == ord('D'):
        snake_dx = snake_width
        snake_dy = 0
    elif key == ord('s') or key == ord('S'):
        snake_dx = 0
        snake_dy = snake_width

    # 更新貪吃蛇位置
    snake_x += snake_dx
    snake_y += snake_dy

    # 如果貪吃蛇碰到邊界，遊戲結束
    if snake_x < 0 or snake_x > window_width - snake_width or snake_y < 0 or snake_y > window_height - snake_width:
        cv2.putText(img, "GAME OVER", (window_width // 2 - 180, window_height // 2), font, 2 * font_size, (0, 0, 255), 3)
        cv2.putText(img, "Total Score: {}".format(score), (window_width // 2 - 240, window_height // 2+60), font, 2 * font_size, (0, 0, 255), 3)
        cv2.imshow("11102_1_D1051121曾苔湘", img)
        cv2.waitKey(2000)
        break
    # 如果貪吃蛇碰到紅色圓點，身體增長並更新分數和紅色圓點位置
    if snake_x <= dot_x <= snake_x + snake_width and snake_y <= dot_y <= snake_y + snake_width:
        score += 10
        dot_x = random.randint(0, window_width - dot_size)
        dot_y = random.randint(0, window_height - dot_size)
        snake_length += 1
        snake_body.insert(0, (snake_x, snake_y))
    
    # 更新貪吃蛇身體位置
    snake_body.pop()
    snake_body.insert(0, (snake_x, snake_y))
    
    # 延遲時間
    cv2.waitKey(50)
cv2.destroyAllWindows()
