import cv2
import time
import numpy as np

def fisheye_effect( f ):
    nr,nc = f.shape[:2]
    map_x = np.zeros( [nr, nc], dtype = 'float32' )
    map_y = np.zeros( [nr, nc], dtype = 'float32' )
    x0, y0 = nr // 2, nc // 2
    R = np.sqrt( nr ** 2 + nc ** 2 ) / 2
    for x in range( nr ):
        for y in range( nc ):
            r = np.sqrt( ( x - x0 ) ** 2 + ( y - y0 ) ** 2 )
            if r == 0:  theta = 0
            else:       theta = np.arccos( ( x - x0 ) / r )
            r = ( r * r ) / R
            if y - y0 < 0:  theta = -theta
            map_x[x,y] = np.clip( y0 + r * np.sin( theta ), 0, nc - 1 )
            map_y[x,y] = np.clip( x0 + r * np.cos( theta ), 0, nr - 1 )
    g = cv2.remap( f, map_x, map_y, cv2.INTER_CUBIC )
    return g

# 選擇第二隻攝影機
cap = cv2.VideoCapture(0)

while(True):
  # 從攝影機擷取一張影像
  ret, frame = cap.read()

  # 顯示圖片
  #cv2.imshow('frame', frame)
  
  # Filename 
  filename = 'savedImage.jpg'

  # 存圖片
  localtime = time.localtime()
  result = time.strftime("%Y-%m-%d-%I-%M-%S", localtime)
  filename = result+".jpg"
  print (filename)
  # cv2.imwrite(filename, frame)
  img1 = cv2.imread('savedImage.jpg',-1)
  img2 = cv2.stylization( img1 ) # === 影像處理 ===
  cv2.imwrite(filename, img2)
  
  time.sleep(1) # 每1秒抓一張圖
  
  # 若按下 q 鍵則離開迴圈
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
