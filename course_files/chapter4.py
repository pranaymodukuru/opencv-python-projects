import cv2
import numpy as np

# Shapes and text on images

img = np.zeros((512, 512, 3), np.uint8)
print(img.shape)

# Color
# img[:] = 255, 0 , 0
# img[200:300, 100:300] = 255, 0, 0

# Line
cv2.line(img, (0,0), (img.shape[1],img.shape[0]), (0,0,255), 2)

# Rectangle
cv2.rectangle(img, (0,0), (250, 350), (0,255,0), cv2.FILLED)

# Circle
cv2.circle(img, (400, 50), 30, (255,255,0), 5)

# Text
cv2.putText(img, " OPENCV ", (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 0), 3)

cv2.imshow("Image",img)
cv2.waitKey(0)