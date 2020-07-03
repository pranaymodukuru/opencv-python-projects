import cv2

# Resize and Crop
img = cv2.imread("resources/lambo.png")

print(img.shape) # 462,623,3 # H, W, C

# Resize
imgResized = cv2.resize(img, (300, 200))  # (W, H)
print(imgResized.shape)

# Crop
imgCropped = img[0:200, 200:500]   # H, W

cv2.imshow("Image", img)
cv2.imshow("Resized", imgResized)
cv2.imshow("Cropped", imgCropped)


cv2.waitKey(0)
