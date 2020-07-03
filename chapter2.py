import cv2
import numpy as np

# Converting image to Grayscale
# Read Image
img = cv2.imread("resources/lena.png")

# Converting BGR to Gray
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)

# Edge detector
# Canny edge detector
imgCanny = cv2.Canny(img, 150, 200)

# Dilation
kernel = np.ones((5,5), np.uint8)

imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)

# Erosion (opposite of dilation)
imgEroded = cv2.erode(imgDilation, kernel, iterations=1)

# Show all images
cv2.imshow("Gray", imgGray)
cv2.imshow("Blurred", imgBlur)
cv2.imshow("Canny", imgCanny)
cv2.imshow("Dilation", imgDilation)
cv2.imshow("Erosion", imgEroded)

cv2.waitKey(0)
