import cv2
import numpy as np
img = np.zeros((200, 200, 3), dtype=np.uint8)
cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), 2)
cv2.imshow("test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()